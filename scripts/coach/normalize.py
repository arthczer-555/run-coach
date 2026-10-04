"""Transforme les réponses brutes Garmin (data/raw) en fichiers propres (data/).

Toujours reconstruit à partir de zéro : on peut corriger un parseur puis relancer
`uv run scripts/sync.py --normalize-only` sans rappeler Garmin.
"""

from __future__ import annotations

from datetime import date
from typing import Any

import pandas as pd

from coach.paths import (
    ACTIVITIES_CSV, GARMIN_ACTIVITY_URL, GARMIN_PROFILE_JSON, METRICS_CSV, PLANNED_JSON, RAW,
    RAW_ACTIVITIES, RAW_WORKOUTS, RECORDS_JSON, WELLNESS_CSV,
)
from coach.sports import sport_of
from coach.util import fmt_pace, pick, read_json, speed_to_pace, write_json

# --- Activités ----------------------------------------------------------------

FEEL_LABELS = {0: "très mal", 25: "mal", 50: "normal", 75: "bien", 100: "très bien"}


def _zones_minutes(summary: dict[str, Any], detail: dict[str, Any]) -> list[float | None]:
    zones: list[float | None] = []
    for i in range(1, 6):
        v = summary.get(f"hrTimeInZone_{i}")
        zones.append(round(v / 60, 1) if v is not None else None)
    if any(z is not None for z in zones):
        return zones
    hz = detail.get("hr_zones")
    if isinstance(hz, list) and hz:
        by_zone = {z.get("zoneNumber"): z.get("secsInZone") for z in hz}
        return [round(by_zone[i] / 60, 1) if by_zone.get(i) is not None else None for i in range(1, 6)]
    return zones


def activity_row(summary: dict[str, Any], detail: dict[str, Any]) -> dict[str, Any]:
    aid = summary["activityId"]
    type_key = (summary.get("activityType") or {}).get("typeKey", "")
    sport = sport_of(type_key)
    start_local = summary.get("startTimeLocal") or ""
    dist_km = (summary.get("distance") or 0) / 1000
    duration_s = summary.get("duration") or 0
    moving_s = summary.get("movingDuration") or duration_s
    speed = summary.get("averageSpeed")
    act = detail.get("activity") or {}
    rpe_raw = pick(act, "summaryDTO.directWorkoutRpe") or summary.get("directWorkoutRpe")
    feel_raw = pick(act, "summaryDTO.directWorkoutFeel") or summary.get("directWorkoutFeel")
    z = _zones_minutes(summary, detail)
    laps = pick(detail, "splits.lapDTOs", default=[]) or []
    return {
        "id": aid,
        "date": start_local[:10],
        "start_local": start_local.replace(" ", "T")[:16],
        "sport": sport,
        "type": type_key,
        "name": summary.get("activityName") or "",
        "distance_km": round(dist_km, 2),
        "duration_min": round(duration_s / 60, 1),
        "moving_min": round(moving_s / 60, 1),
        "pace_min_km": round(speed_to_pace(speed), 3) if sport == "run" and speed_to_pace(speed) else None,
        "speed_kmh": round(speed * 3.6, 1) if speed and sport == "bike" else None,
        "elev_gain_m": round(summary["elevationGain"]) if summary.get("elevationGain") is not None else None,
        "avg_hr": summary.get("averageHR"),
        "max_hr": summary.get("maxHR"),
        "cadence": summary.get("averageRunningCadenceInStepsPerMinute") or summary.get("averageBikingCadenceInRevPerMinute"),
        "avg_power": summary.get("avgPower"),
        "calories": summary.get("calories"),
        "aerobic_te": summary.get("aerobicTrainingEffect"),
        "anaerobic_te": summary.get("anaerobicTrainingEffect"),
        "te_label": summary.get("trainingEffectLabel"),
        "training_load": round(summary["activityTrainingLoad"], 1) if summary.get("activityTrainingLoad") is not None else None,
        # TRIMP d'Edwards (minutes en zone × numéro de zone) : charge interne quand la montre ne calcule pas de training load.
        "trimp": round(sum((zi or 0) * (i + 1) for i, zi in enumerate(z)), 1) if any(zi is not None for zi in z) else None,
        "vo2max": summary.get("vO2MaxValue"),
        "z1_min": z[0], "z2_min": z[1], "z3_min": z[2], "z4_min": z[3], "z5_min": z[4],
        "rpe": round(rpe_raw / 10, 1) if isinstance(rpe_raw, (int, float)) else None,
        "feel": FEEL_LABELS.get(feel_raw, feel_raw) if feel_raw is not None else None,
        "laps": len(laps) or None,
        "description": (act.get("description") or summary.get("description") or "").replace("\n", " ").strip(),
        "url": GARMIN_ACTIVITY_URL.format(id=aid),
    }


def build_activities() -> pd.DataFrame | None:
    index: dict[str, dict[str, Any]] = read_json(RAW / "activities_index.json", {})
    if not index:
        return None
    rows = []
    for aid, summary in index.items():
        detail = read_json(RAW_ACTIVITIES / f"{aid}.json", {})
        rows.append(activity_row(summary, detail))
    df = pd.DataFrame(rows).sort_values("start_local").reset_index(drop=True)
    df.to_csv(ACTIVITIES_CSV, index=False)
    return df


# --- Wellness -------------------------------------------------------------------


def build_wellness() -> None:
    store: dict[str, dict[str, Any]] = read_json(RAW / "wellness.json", {})
    if not store:
        return
    days: dict[str, dict[str, Any]] = {}

    def row(d: str) -> dict[str, Any]:
        return days.setdefault(d, {"date": d})

    for d, h in store.get("hrv", {}).items():
        r = row(d)
        r["hrv_night"] = pick(h, "lastNightAvg")
        r["hrv_7d"] = pick(h, "weeklyAvg")
        r["hrv_status"] = pick(h, "status")
        r["hrv_base_low"] = pick(h, "baseline.balancedLow")
        r["hrv_base_high"] = pick(h, "baseline.balancedUpper")
    for d, s in store.get("sleep", {}).items():
        r = row(d)
        secs = pick(s, "values.totalSleepTimeInSeconds", "values.totalSleepSeconds", "values.sleepTimeSeconds",
                    "totalSleepTimeInSeconds", "sleepTimeSeconds")
        r["sleep_h"] = round(secs / 3600, 2) if isinstance(secs, (int, float)) else None
        r["sleep_score"] = pick(s, "values.sleepScore", "values.overallScore", "sleepScore", "values.sleepScoreValue")
    # FC de repos et Body Battery n'ont de sens que si la montre a été portée la nuit (sinon Garmin prend
    # par exemple la FC minimale d'une séance : 85-110 bpm). On ne les garde que les jours avec une nuit mesurée.
    night = {d for d, r in days.items() if r.get("sleep_h") or r.get("hrv_night")}
    for d, v in store.get("rhr", {}).items():
        if d in night:
            row(d)["rhr"] = pick(v, "value")
    for d, b in store.get("body_battery", {}).items():
        if d not in night:
            continue
        r = row(d)
        values = [p[1] for p in (b.get("bodyBatteryValuesArray") or []) if isinstance(p, list) and len(p) > 1 and p[1] is not None]
        r["bb_max"] = max(values) if values else None
        r["bb_charged"] = b.get("charged")
    for d, t in store.get("readiness", {}).items():
        r = row(d)
        r["readiness"] = pick(t, "score")
        r["readiness_level"] = pick(t, "level")
    df = pd.DataFrame(sorted(days.values(), key=lambda x: x["date"]))
    df.to_csv(WELLNESS_CSV, index=False)


# --- Métriques (VO2max, prédictions, training status) -------------------------


def build_metrics() -> None:
    store: dict[str, dict[str, Any]] = read_json(RAW / "metrics.json", {})
    if not store:
        return
    days: dict[str, dict[str, Any]] = {}

    def row(d: str) -> dict[str, Any]:
        return days.setdefault(d, {"date": d})

    for d, m in store.get("max_metrics", {}).items():
        r = row(d)
        r["vo2max_run"] = pick(m, "generic.vo2MaxPreciseValue", "generic.vo2MaxValue")
        r["vo2max_bike"] = pick(m, "cycling.vo2MaxPreciseValue", "cycling.vo2MaxValue")
    for d, p in store.get("race_predictions", {}).items():
        r = row(d)
        r["pred_5k_s"] = p.get("time5K")
        r["pred_10k_s"] = p.get("time10K")
        r["pred_semi_s"] = p.get("timeHalfMarathon")
        r["pred_marathon_s"] = p.get("timeMarathon")
    for d, t in store.get("training_status", {}).items():
        r = row(d)
        latest = pick(t, "mostRecentTrainingStatus.latestTrainingStatusData", default={}) or {}
        device = next(iter(latest.values()), {}) if isinstance(latest, dict) else {}
        r["training_status"] = pick(device, "trainingStatusFeedbackPhrase", "trainingStatus")
        r["acute_load"] = pick(device, "acuteTrainingLoadDTO.dailyTrainingLoadAcute")
        r["chronic_load"] = pick(device, "acuteTrainingLoadDTO.dailyTrainingLoadChronic")
        r["acwr"] = pick(device, "acuteTrainingLoadDTO.dailyAcuteChronicWorkloadRatio")
    df = pd.DataFrame(sorted(days.values(), key=lambda x: x["date"]))
    df.to_csv(METRICS_CSV, index=False)


# --- Records et profil Garmin ----------------------------------------------------

RUN_PR_TYPES = {1: "1 km", 2: "1 mile", 3: "5 km", 4: "10 km", 5: "Semi", 6: "Marathon", 7: "Plus longue sortie"}


def build_profile_and_records(activities: pd.DataFrame | None) -> None:
    prof = read_json(RAW / "profile.json", {})
    if not prof:
        return
    names = {}
    if activities is not None:
        names = dict(zip(activities["id"].astype(str), activities["name"]))
    records = []
    for pr in prof.get("personal_records") or []:
        type_id = pr.get("typeId")
        if type_id not in RUN_PR_TYPES or (pr.get("activityType") not in (None, "running")):
            continue
        aid = pr.get("activityId")
        records.append({
            "type_id": type_id,
            "label": RUN_PR_TYPES[type_id],
            "value": pr.get("value"),
            "unit": "m" if type_id == 7 else "s",
            "date": (pr.get("actStartDateTimeInGMTFormatted") or pr.get("prStartTimeGmtFormatted") or "")[:10],
            "activity_id": aid,
            "activity_name": names.get(str(aid), pr.get("activityName") or ""),
            "url": GARMIN_ACTIVITY_URL.format(id=aid) if aid else None,
        })
    write_json(RECORDS_JSON, sorted(records, key=lambda r: r["type_id"]))

    zones_out = []
    for z in prof.get("hr_zones") or []:
        zones_out.append({
            "sport": z.get("sport"),
            "method": z.get("trainingMethod"),
            "max_hr": z.get("maxHeartRateUsed"),
            "resting_hr": z.get("restingHeartRateUsed"),
            "lthr": z.get("lactateThresholdHeartRateUsed"),
            "floors": [z.get(f"zone{i}Floor") for i in range(1, 6)],
        })
    lt = prof.get("lactate_threshold") or {}
    user = pick(prof, "user_profile.userData", "user_settings.userData", default={}) or {}
    birth = user.get("birthDate")
    age = None
    if birth:
        b = date.fromisoformat(birth[:10])
        t = date.today()
        age = t.year - b.year - ((t.month, t.day) < (b.month, b.day))
    write_json(GARMIN_PROFILE_JSON, {
        "hr_zones": zones_out,
        "lactate_threshold_hr": pick(lt, "speed_and_heart_rate.heartRate"),
        # Unité de vitesse Garmin à confirmer sur données réelles avant conversion en allure.
        "lactate_threshold_speed_raw": pick(lt, "speed_and_heart_rate.speed"),
        "age": age,
        "weight_kg": round(user["weight"] / 1000, 1) if user.get("weight") else pick(lt, "power.weight"),
        "height_cm": user.get("height"),
        "devices": [d.get("productDisplayName") or d.get("displayName") for d in prof.get("devices") or []
                    if isinstance(d, dict)],
        "vo2max_run": user.get("vo2MaxRunning"),
        "vo2max_bike": user.get("vo2MaxCycling"),
    })


# --- Séances planifiées (calendrier Garmin) --------------------------------------

STEP_LABELS = {
    "warmup": "Échauffement", "cooldown": "Retour au calme", "interval": "", "recovery": "Récup",
    "rest": "Repos", "other": "", "repeat": "",
}


def _fmt_end(step: dict[str, Any]) -> str:
    cond = pick(step, "endCondition.conditionTypeKey", default="")
    val = step.get("endConditionValue")
    if cond == "time" and val:
        m, s = divmod(int(val), 60)
        return f"{m} min" if not s else f"{m}:{s:02d}"
    if cond == "distance" and val:
        return f"{val / 1000:g} km" if val >= 1000 else f"{int(val)} m"
    if cond == "lap.button":
        return "jusqu'au tour"
    return ""


def _fmt_target(step: dict[str, Any]) -> str:
    kind = pick(step, "targetType.workoutTargetTypeKey", default="no.target")
    lo, hi = step.get("targetValueOne"), step.get("targetValueTwo")
    if kind == "pace.zone" and lo and hi:
        fast, slow = sorted([speed_to_pace(lo), speed_to_pace(hi)])
        return f" @ {fmt_pace(fast)}-{fmt_pace(slow)}/km"
    if kind == "heart.rate.zone":
        zone = step.get("zoneNumber")
        if zone:
            return f" @ Z{zone} FC"
        if lo and hi:
            return f" @ {int(lo)}-{int(hi)} bpm"
    return ""


def _fmt_steps(steps: list[dict[str, Any]]) -> list[str]:
    out = []
    for st in sorted(steps, key=lambda s: s.get("stepOrder", 0)):
        if st.get("type") == "RepeatGroupDTO" or st.get("numberOfIterations"):
            inner = " + ".join(_fmt_steps(st.get("workoutSteps") or []))
            out.append(f"{st.get('numberOfIterations', '?')} × ({inner})")
            continue
        kind = pick(st, "stepType.stepTypeKey", default="other")
        label = STEP_LABELS.get(kind, "")
        txt = " ".join(x for x in [label, _fmt_end(st)] if x) + _fmt_target(st)
        if st.get("description"):
            txt += f" ({st['description']})"
        out.append(txt.strip())
    return out


def build_planned() -> None:
    cal = read_json(RAW / "calendar.json", {})
    planned = []
    seen: set[tuple[Any, ...]] = set()
    for it in cal.get("items", []):
        # Les mois du calendrier Garmin se chevauchent (semaines à cheval) : une séance peut revenir deux fois.
        key = (it.get("id"), it.get("date"), it.get("workoutId"), it.get("title"), it.get("itemType"))
        if key in seen:
            continue
        seen.add(key)
        item_type = it.get("itemType") or ""
        if item_type == "workout":
            wid = it.get("workoutId")
            w = read_json(RAW_WORKOUTS / f"{wid}.json", {}) if wid else {}
            steps: list[str] = []
            for seg in w.get("workoutSegments") or []:
                steps += _fmt_steps(seg.get("workoutSteps") or [])
            sport_key = pick(w, "sportType.sportTypeKey") or it.get("sportTypeKey") or ""
            dur = w.get("estimatedDurationInSecs") or it.get("duration")
            dist = w.get("estimatedDistanceInMeters") or it.get("distance")
            planned.append({
                "date": it.get("date"),
                "sport": sport_of(sport_key) if sport_key != "running" else "run",
                "title": it.get("title") or w.get("workoutName") or "Séance",
                "details": " · ".join(steps),
                "description": (w.get("description") or "").strip(),
                "duration_min": round(dur / 60) if dur else None,
                "distance_km": round(dist / 1000, 1) if dist else None,
                "source": "garmin",
                "workout_id": wid,
            })
        elif "event" in item_type.lower() or "race" in item_type.lower():
            planned.append({
                "date": it.get("date"), "sport": "race", "title": it.get("title") or "Événement",
                "details": "", "description": "", "duration_min": None, "distance_km": None,
                "source": "garmin", "workout_id": None,
            })
    planned.sort(key=lambda p: (p["date"] or "", p["title"]))
    write_json(PLANNED_JSON, {"fetched": cal.get("fetched"), "items": planned})


def rebuild_all() -> None:
    acts = build_activities()
    build_wellness()
    build_metrics()
    build_profile_and_records(acts)
    build_planned()
