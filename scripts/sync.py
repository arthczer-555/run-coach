"""Sync Garmin Connect -> data/ (activités, wellness, métriques, records, calendrier).

Usage :
  uv run scripts/sync.py                   # incrémental (depuis la dernière sync, avec chevauchement)
  uv run scripts/sync.py --full            # tout l'historique (premier lancement, plusieurs minutes)
  uv run scripts/sync.py --hook            # appelé par le hook Claude Code : 1 fois / 30 min max, jamais bloquant
  uv run scripts/sync.py --normalize-only  # reconstruit les CSV depuis data/raw sans appeler Garmin

Les réponses brutes vont dans data/raw/ (gitignored, re-téléchargeables), puis
coach.normalize produit les fichiers propres de data/ lus par les autres scripts.
"""

from __future__ import annotations

import argparse
import sys
import time
from collections.abc import Callable
from datetime import date, datetime, timedelta
from typing import Any

from coach import normalize
from coach.paths import RAW, RAW_ACTIVITIES, RAW_WORKOUTS, SYNC_STATE, TOKENSTORE
from coach.sports import sport_of
from coach.util import date_chunks, days_between, fmt_duration, read_json, write_json

THROTTLE_MINUTES = 30
OVERLAP_DAYS = 3
FULL_START = date(2010, 1, 1)
WELLNESS_FULL_DAYS = 365
READINESS_FULL_DAYS = 120
FIRST_INCREMENTAL_DAYS = 42
PAUSE_S = 0.4


class Sync:
    def __init__(self, api: Any, verbose: bool) -> None:
        self.api = api
        self.verbose = verbose
        self.errors: list[str] = []

    def log(self, msg: str) -> None:
        if self.verbose:
            print(msg, flush=True)

    def safe(self, label: str, fn: Callable[..., Any], *args: Any) -> Any:
        try:
            return fn(*args)
        except Exception as e:  # noqa: BLE001 - un endpoint en échec ne doit pas bloquer les autres
            self.errors.append(f"{label}: {type(e).__name__}: {str(e)[:160]}")
            return None

    # -- Activités ---------------------------------------------------------

    def activities(self, start: date, end: date) -> list[dict[str, Any]]:
        index_path = RAW / "activities_index.json"
        index: dict[str, dict[str, Any]] = read_json(index_path, {})
        self.log(f"Activités du {start} au {end}…")
        summaries = self.api.get_activities_by_date(start.isoformat(), end.isoformat(), None, "asc")
        returned = {str(a["activityId"]): a for a in summaries}
        new = [a for aid, a in returned.items() if aid not in index]

        # Activités supprimées dans Garmin pendant la fenêtre synchronisée.
        for aid, a in list(index.items()):
            d = (a.get("startTimeLocal") or "")[:10]
            if start.isoformat() <= d <= end.isoformat() and aid not in returned:
                del index[aid]
                (RAW_ACTIVITIES / f"{aid}.json").unlink(missing_ok=True)

        index.update(returned)
        write_json(index_path, index, compact=True)

        # Détails (laps, zones FC, RPE, séries de renfo). Les activités récentes sont
        # re-téléchargées pour capter un RPE ou une description ajoutés après coup.
        recent = (date.today() - timedelta(days=2)).isoformat()
        todo = []
        for aid, a in index.items():
            sport = sport_of((a.get("activityType") or {}).get("typeKey"))
            path = RAW_ACTIVITIES / f"{aid}.json"
            is_recent = (a.get("startTimeLocal") or "")[:10] >= recent
            if sport != "other" and (not path.exists() or is_recent):
                todo.append((aid, sport, path))
        for i, (aid, sport, path) in enumerate(todo, 1):
            if i % 25 == 0:
                self.log(f"  détails {i}/{len(todo)}")
            detail = {
                "activity": self.safe(f"activité {aid}", self.api.get_activity, aid),
                "hr_zones": self.safe(f"zones {aid}", self.api.get_activity_hr_in_timezones, aid),
            }
            if detail["activity"] is None:
                continue  # on retentera à la prochaine sync
            if sport in ("run", "bike"):
                detail["splits"] = self.safe(f"laps {aid}", self.api.get_activity_splits, aid)
            if sport == "strength":
                detail["exercise_sets"] = self.safe(f"séries {aid}", self.api.get_activity_exercise_sets, aid)
            write_json(path, detail, compact=True)
            time.sleep(PAUSE_S)
        return new

    # -- Wellness (HRV, sommeil, FC repos, Body Battery, Training Readiness) --

    def wellness(self, start: date, end: date, readiness_start: date) -> None:
        path = RAW / "wellness.json"
        store: dict[str, dict[str, Any]] = read_json(path, {})

        def put(kind: str, day: str | None, payload: Any) -> None:
            if day:
                store.setdefault(kind, {})[day[:10]] = payload

        self.log(f"Wellness du {start} au {end}…")
        for s, e in date_chunks(start, end, 28):
            hrv = self.safe("hrv", self.api.get_hrv_data_range, s, e)
            rows = hrv.get("hrvSummaries", []) if isinstance(hrv, dict) else (hrv or [])
            for row in rows:
                put("hrv", row.get("calendarDate"), row)
            for row in self.safe("body battery", self.api.get_body_battery, s, e) or []:
                put("body_battery", row.get("date") or row.get("calendarDate"), row)
        for row in self.safe("sommeil", self.api.get_sleep_daily, start.isoformat(), end.isoformat()) or []:
            put("sleep", row.get("calendarDate"), row)
        for s, e in date_chunks(start, end, 360):
            for row in self.safe("fc repos", self.api.get_rhr_daily, s, e) or []:
                put("rhr", row.get("calendarDate"), row)
        for d in days_between(readiness_start, end):
            r = self.safe(f"readiness {d}", self.api.get_morning_training_readiness, d.isoformat())
            if r:
                put("readiness", d.isoformat(), r)
            time.sleep(0.15)
        write_json(path, store, compact=True)

    # -- Métriques (VO2max, prédictions de course, training status) ---------

    def metrics(self, start: date, end: date) -> None:
        path = RAW / "metrics.json"
        store: dict[str, dict[str, Any]] = read_json(path, {})
        self.log(f"Métriques du {start} au {end}…")
        for s, e in date_chunks(start, end, 28):
            mm = self.safe("vo2max", self.api.get_max_metrics_range, s, e)
            for row in mm if isinstance(mm, list) else []:
                day = (row.get("generic") or row.get("cycling") or row).get("calendarDate")
                if day:
                    store.setdefault("max_metrics", {})[day] = row
        for s, e in date_chunks(start, end, 360):
            rp = self.safe("prédictions", self.api.get_race_predictions, s, e, "daily")
            for row in rp if isinstance(rp, list) else []:
                day = row.get("calendarDate")
                if day:
                    store.setdefault("race_predictions", {})[day] = row
        ts = self.safe("training status", self.api.get_training_status, end.isoformat())
        if ts:
            store.setdefault("training_status", {})[end.isoformat()] = ts
        write_json(path, store, compact=True)

    # -- Profil (records, zones FC, seuil lactique, réglages) ----------------

    def profile(self) -> None:
        self.log("Profil, records, zones…")
        prof = {
            "personal_records": self.safe("records", self.api.get_personal_record),
            "hr_zones": self.safe("zones FC", self.api.get_heart_rate_zones),
            "lactate_threshold": self.safe("seuil lactique", self.api.get_lactate_threshold),
            "user_settings": self.safe("réglages", self.api.get_userprofile_settings),
            "user_profile": self.safe("profil", self.api.get_user_profile),
            "devices": self.safe("appareils", self.api.get_devices),
        }
        old = read_json(RAW / "profile.json", {})
        write_json(RAW / "profile.json", {k: v if v is not None else old.get(k) for k, v in prof.items()})

    # -- Calendrier (séances planifiées, dont celles exportées par Kiprun Pacer) --

    def calendar(self, today: date) -> None:
        self.log("Calendrier Garmin (séances planifiées)…")
        items: list[dict[str, Any]] = []
        y, m = today.year, today.month
        for offset in (-1, 0, 1, 2):
            mm = m + offset
            yy = y + (mm - 1) // 12
            mm = (mm - 1) % 12 + 1
            cal = self.safe(f"calendrier {yy}-{mm:02d}", self.api.get_scheduled_workouts, yy, mm)
            items += (cal or {}).get("calendarItems", []) if isinstance(cal, dict) else []
        for it in items:
            wid = it.get("workoutId")
            if it.get("itemType") == "workout" and wid and not (RAW_WORKOUTS / f"{wid}.json").exists():
                w = self.safe(f"séance {wid}", self.api.get_workout_by_id, wid)
                if w:
                    write_json(RAW_WORKOUTS / f"{wid}.json", w, compact=True)
        write_json(RAW / "calendar.json", {"fetched": datetime.now().isoformat(timespec="seconds"), "items": items})


def connect() -> Any:
    from garminconnect import Garmin

    api = Garmin()
    api.login(TOKENSTORE)
    return api


def describe_new(new: list[dict[str, Any]]) -> str:
    parts = []
    for a in new:
        sport = sport_of((a.get("activityType") or {}).get("typeKey"))
        km = (a.get("distance") or 0) / 1000
        dur = fmt_duration(a.get("duration"))
        label = {"run": "course", "bike": "vélo", "strength": "renfo"}.get(sport, sport)
        parts.append(f"{label} {km:.1f} km en {dur}" if km >= 0.5 else f"{label} {dur}")
    return ", ".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--full", action="store_true", help="rapatrie tout l'historique")
    parser.add_argument("--hook", action="store_true", help="mode hook : throttle + sortie d'une ligne")
    parser.add_argument("--normalize-only", action="store_true", help="reconstruit data/ depuis data/raw")
    args = parser.parse_args()

    if args.normalize_only:
        normalize.rebuild_all()
        print("data/ reconstruit depuis data/raw.")
        return 0

    now = datetime.now()
    state: dict[str, Any] = read_json(SYNC_STATE, {})
    if args.hook and state.get("last_attempt"):
        last = datetime.fromisoformat(state["last_attempt"])
        if now - last < timedelta(minutes=THROTTLE_MINUTES):
            return 0
    state["last_attempt"] = now.isoformat(timespec="seconds")
    write_json(SYNC_STATE, state)

    today = date.today()
    try:
        api = connect()
    except Exception as e:  # noqa: BLE001
        msg = f"⚠️ Sync Garmin impossible ({type(e).__name__}). Connexion : `uv run scripts/garmin_login.py`."
        print(msg)
        return 0 if args.hook else 1

    sync = Sync(api, verbose=not args.hook)
    last_ok = state.get("last_success_date")
    if args.full:
        act_start = FULL_START
        well_start = today - timedelta(days=WELLNESS_FULL_DAYS)
        ready_start = today - timedelta(days=READINESS_FULL_DAYS)
    elif last_ok:
        act_start = well_start = date.fromisoformat(last_ok) - timedelta(days=OVERLAP_DAYS)
        ready_start = max(well_start, today - timedelta(days=14))
    else:
        act_start = well_start = ready_start = today - timedelta(days=FIRST_INCREMENTAL_DAYS)

    try:
        new = sync.activities(act_start, today)
    except Exception as e:  # noqa: BLE001
        print(f"⚠️ Sync Garmin : échec de la récupération des activités ({type(e).__name__}: {str(e)[:120]}).")
        return 0 if args.hook else 1
    sync.wellness(well_start, today, ready_start)
    sync.metrics(well_start, today)
    sync.profile()
    sync.calendar(today)
    normalize.rebuild_all()

    state["last_success_date"] = today.isoformat()
    state["last_success"] = now.isoformat(timespec="seconds")
    write_json(SYNC_STATE, state)

    summary = f"🔄 Sync Garmin OK : {len(new)} nouvelle(s) activité(s)"
    if new and len(new) <= 6:
        summary += f" ({describe_new(new)})"
    if sync.errors:
        summary += f". {len(sync.errors)} endpoint(s) en échec"
    print(summary + ".")
    if sync.errors and not args.hook:
        print("\n".join(f"  - {e}" for e in sync.errors[:20]))
    if not last_ok and not args.full:
        print("ℹ️ Première sync limitée à 6 semaines. Historique complet : `uv run scripts/sync.py --full`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
