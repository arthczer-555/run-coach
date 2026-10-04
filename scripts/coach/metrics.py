"""Calculs d'entraînement : volumes hebdo, planifié vs réalisé, intensité, charge, forme, signaux."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any

import pandas as pd

from coach.sports import SPORT_EMOJI
from coach.util import FR_DAYS, fmt_duration, fmt_pace, monday_of

ZONE_COLS = ["z1_min", "z2_min", "z3_min", "z4_min", "z5_min"]
ACT_COLUMNS = [
    "id", "date", "start_local", "sport", "type", "name", "distance_km", "duration_min", "moving_min",
    "pace_min_km", "speed_kmh", "elev_gain_m", "avg_hr", "max_hr", "training_load", "rpe", "feel",
    "description", "url", "trimp", *ZONE_COLS,
]


def ensure_columns(acts: pd.DataFrame) -> pd.DataFrame:
    if acts.empty:
        return pd.DataFrame(columns=ACT_COLUMNS).astype({"date": "datetime64[ns]", "start_local": "datetime64[ns]"})
    return acts


def ts(d: date) -> pd.Timestamp:
    return pd.Timestamp(d)


def between(df: pd.DataFrame, start: date, end: date, col: str = "date") -> pd.DataFrame:
    if df.empty:
        return df
    return df[(df[col] >= ts(start)) & (df[col] <= ts(end))]


# --- Volumes hebdomadaires --------------------------------------------------------


def weekly(acts: pd.DataFrame, end: date, weeks: int) -> pd.DataFrame:
    """Une ligne par semaine ISO (lundi), des `weeks` dernières semaines jusqu'à celle de `end`."""
    acts = ensure_columns(acts)
    last_mon = monday_of(end)
    rows = []
    for i in range(weeks - 1, -1, -1):
        mon = last_mon - timedelta(weeks=i)
        w = between(acts, mon, mon + timedelta(days=6))
        run, bike = w[w["sport"] == "run"], w[w["sport"] == "bike"]
        zones = w[ZONE_COLS].fillna(0).sum() if not w.empty else pd.Series(0.0, index=ZONE_COLS)
        total_z = float(zones.sum())
        rows.append({
            "monday": mon,
            "run_km": float(run["distance_km"].sum()),
            "run_n": len(run),
            "run_min": float(run["duration_min"].sum()),
            "long_run_km": float(run["distance_km"].max()) if len(run) else 0.0,
            "bike_min": float(bike["duration_min"].sum()),
            "bike_km": float(bike["distance_km"].sum()),
            "bike_n": len(bike),
            "strength_n": int((w["sport"] == "strength").sum()),
            "elev_m": float(run["elev_gain_m"].fillna(0).sum()),
            "load": float(w["training_load"].fillna(0).sum()) if w["training_load"].notna().any()
            else float(w.get("trimp", pd.Series(dtype=float)).fillna(0).sum()),
            "zone_min": total_z,
            "z12_pct": (zones["z1_min"] + zones["z2_min"]) / total_z * 100 if total_z > 0 else None,
            "z3_pct": zones["z3_min"] / total_z * 100 if total_z > 0 else None,
            "z45_pct": (zones["z4_min"] + zones["z5_min"]) / total_z * 100 if total_z > 0 else None,
        })
    return pd.DataFrame(rows)


# --- Charge aiguë / chronique ---------------------------------------------------------


def load_series(acts: pd.DataFrame, end: date, days: int = 180) -> tuple[pd.DataFrame, str]:
    """Charge quotidienne + aiguë (7 j) / chronique (moyenne hebdo sur 28 j) + ratio.

    Utilise la "training load" Garmin si elle est renseignée sur la plupart des séances
    récentes, sinon le TRIMP d'Edwards (zones FC), sinon la durée (min). Le ratio est un simple signal
    d'alerte, pas un prédicteur fiable de blessure (voir knowledge/charge-blessures.md).
    """
    acts = ensure_columns(acts)
    start = end - timedelta(days=days + 28)
    w = between(acts, start, end)
    recent = between(acts, end - timedelta(days=60), end)
    if not recent.empty and recent["training_load"].notna().mean() >= 0.8:
        col, unit = "training_load", "charge Garmin"
    elif "trimp" in acts and not recent.empty and recent["trimp"].notna().mean() >= 0.8:
        col, unit = "trimp", "TRIMP"
    else:
        col, unit = "duration_min", "minutes"
    idx = pd.date_range(start, end, freq="D")
    daily = w.groupby("date")[col].sum().reindex(idx, fill_value=0.0) if not w.empty else pd.Series(0.0, index=idx)
    out = pd.DataFrame({"daily": daily})
    out["acute"] = out["daily"].rolling(7, min_periods=7).sum()
    out["chronic"] = out["daily"].rolling(28, min_periods=28).sum() / 4
    out["ratio"] = out["acute"] / out["chronic"].where(out["chronic"] > 0)
    return out.iloc[28:], unit


# --- Forme (wellness) ------------------------------------------------------------------


def form(wellness: pd.DataFrame, ref: date) -> dict[str, Any]:
    if wellness.empty:
        return {}
    w7 = between(wellness, ref - timedelta(days=6), ref)
    w28 = between(wellness, ref - timedelta(days=27), ref)
    w5 = between(wellness, ref - timedelta(days=4), ref)

    def mean(df: pd.DataFrame, col: str) -> float | None:
        if col not in df or df[col].dropna().empty:
            return None
        return float(df[col].dropna().mean())

    last = wellness[wellness["date"] <= ts(ref)].tail(1)
    out: dict[str, Any] = {
        "hrv_7d": mean(w7, "hrv_night"), "hrv_28d": mean(w28, "hrv_night"),
        "rhr_7d": mean(w7, "rhr"), "rhr_28d": mean(w28, "rhr"),
        "sleep_7d": mean(w7, "sleep_h"), "sleep_score_7d": mean(w7, "sleep_score"),
        "readiness_7d": mean(w7, "readiness"),
    }
    if not last.empty:
        row = last.iloc[0]
        out["hrv_status"] = row.get("hrv_status")
        out["hrv_base_low"] = row.get("hrv_base_low")
        out["hrv_base_high"] = row.get("hrv_base_high")
        out["readiness_last"] = row.get("readiness")
    if "hrv_night" in w5 and "hrv_base_low" in w5:
        below = w5.dropna(subset=["hrv_night", "hrv_base_low"])
        out["hrv_below_5d"] = int((below["hrv_night"] < below["hrv_base_low"]).sum())
    return out


# --- Efficience aérobie ------------------------------------------------------------------


def aerobic_efficiency(acts: pd.DataFrame) -> pd.DataFrame:
    """Mètres parcourus par battement cardiaque sur les sorties faciles (≥ 20 min, ≥ 70 % en Z1-Z2).

    Une hausse à effort égal traduit une meilleure condition aérobie. Sensible à la
    chaleur, au dénivelé et à la fatigue : à lire en tendance, jamais séance par séance.
    """
    acts = ensure_columns(acts)
    run = acts[(acts["sport"] == "run") & (acts["duration_min"] >= 20)].dropna(subset=["avg_hr", "pace_min_km"]).copy()
    if run.empty:
        return pd.DataFrame(columns=["date", "ef"])
    zones = run[ZONE_COLS].fillna(0)
    total = zones.sum(axis=1)
    easy = (total > 0) & ((zones["z1_min"] + zones["z2_min"]) / total.where(total > 0) >= 0.7)
    run = run[easy]
    run["ef"] = (1000 / run["pace_min_km"]) / run["avg_hr"]
    return run[["date", "ef", "distance_km", "avg_hr", "pace_min_km"]]


# --- Planifié vs réalisé ---------------------------------------------------------------------


@dataclass
class DayPlan:
    day: date
    planned: list[dict[str, Any]] = field(default_factory=list)  # chaque item porte "status"
    extra: list[dict[str, Any]] = field(default_factory=list)  # activités hors plan


def act_summary(a: pd.Series | dict[str, Any]) -> str:
    sport = a["sport"]
    emo = SPORT_EMOJI.get(sport, "✨")
    parts: list[str] = []
    if sport == "run":
        parts = [f"{a['distance_km']:.1f} km", fmt_duration(a["duration_min"] * 60), f"{fmt_pace(a['pace_min_km'])}/km"]
    elif sport == "bike":
        parts = [fmt_duration(a["duration_min"] * 60)]
        if a["distance_km"] and a["distance_km"] > 0.5:
            parts.append(f"{a['distance_km']:.0f} km")
    else:
        parts = [fmt_duration(a["duration_min"] * 60)]
    if pd.notna(a.get("avg_hr")):
        parts.append(f"{int(a['avg_hr'])} bpm")
    if pd.notna(a.get("rpe")):
        parts.append(f"RPE {a['rpe']:g}")
    return f"{emo} " + " · ".join(parts)


def plan_summary(p: pd.Series | dict[str, Any]) -> str:
    emo = SPORT_EMOJI.get(p["sport"], "✨")
    bits = [p["title"]]
    if pd.notna(p.get("distance_km")) and p.get("distance_km"):
        bits.append(f"{p['distance_km']:g} km")
    elif pd.notna(p.get("duration_min")) and p.get("duration_min"):
        bits.append(fmt_minutes(p["duration_min"]))
    return f"{emo} " + " · ".join(bits)


def fmt_minutes(minutes: float) -> str:
    """Durée prévue : 45 -> '45 min', 75 -> '1h15'."""
    minutes = int(round(minutes))
    return f"{minutes} min" if minutes < 60 else f"{minutes // 60}h{minutes % 60:02d}"


STATUS = {"done": "✅", "moved": "🔄", "missed": "❌", "today": "⏳", "future": "🗓️"}


def week_plan(acts: pd.DataFrame, planned: pd.DataFrame, monday: date, today: date) -> list[DayPlan]:
    """Associe chaque séance prévue de la semaine à une activité réalisée (même jour, puis ±1 jour)."""
    acts = ensure_columns(acts)
    days = [DayPlan(monday + timedelta(days=i)) for i in range(7)]
    w_acts = between(acts, monday - timedelta(days=1), monday + timedelta(days=7)).copy()
    w_plan = between(planned, monday, monday + timedelta(days=6)) if not planned.empty else planned
    used: set[Any] = set()
    items = [dict(p) for _, p in w_plan.iterrows()] if not w_plan.empty else []

    def candidates(p: dict[str, Any], delta: int) -> pd.DataFrame:
        sport = "run" if p["sport"] == "race" else p["sport"]
        target = p["date"] + pd.Timedelta(days=delta)
        return w_acts[(w_acts["sport"] == sport) & (w_acts["date"] == target) & ~w_acts["id"].isin(used)]

    for p in items:
        c = candidates(p, 0)
        if not c.empty:
            p["status"], p["activity"] = "done", c.iloc[0]
            used.add(c.iloc[0]["id"])
    for p in items:
        if "status" in p:
            continue
        pdate = p["date"].date()
        if pdate > today:
            p["status"] = "future"
            continue
        moved = None
        for delta in (-1, 1):
            c = candidates(p, delta)
            if not c.empty:
                moved = c.iloc[0]
                break
        if moved is not None:
            p["status"], p["activity"] = "moved", moved
            used.add(moved["id"])
        else:
            p["status"] = "today" if pdate == today else "missed"
    for p in items:
        days[(p["date"].date() - monday).days].planned.append(p)
    in_week = between(w_acts, monday, monday + timedelta(days=6))
    for _, a in in_week.iterrows():
        if a["id"] not in used:
            days[(a["date"].date() - monday).days].extra.append(dict(a))
    return days


def week_table_md(days: list[DayPlan], today: date) -> str:
    lines = ["| Jour | Prévu | Réalisé | |", "|---|---|---|:-:|"]
    for d in days:
        label = f"**{FR_DAYS[d.day.weekday()]} {d.day.day}**" if d.day == today else f"{FR_DAYS[d.day.weekday()]} {d.day.day}"
        rows: list[tuple[str, str, str]] = []
        for p in d.planned:
            done = act_summary(p["activity"]) if "activity" in p else ""
            rows.append((plan_summary(p), done, STATUS[p["status"]]))
        for a in d.extra:
            rows.append(("", act_summary(a), "➕"))
        if not rows:
            rows.append(("", "", "😴" if d.day < today else ""))
        for i, (pl, dn, st) in enumerate(rows):
            lines.append(f"| {label if i == 0 else ''} | {pl} | {dn} | {st} |")
    return "\n".join(lines)


def compliance(days: list[DayPlan]) -> tuple[int, int]:
    """(séances faites ou décalées, séances dues) sur les jours passés."""
    due = [p for d in days for p in d.planned if p["status"] in ("done", "moved", "missed")]
    ok = [p for p in due if p["status"] in ("done", "moved")]
    return len(ok), len(due)


# --- Signaux d'alerte ----------------------------------------------------------------------------


def flags(acts: pd.DataFrame, wellness: pd.DataFrame, checkins: pd.DataFrame, ref: date) -> list[str]:
    acts = ensure_columns(acts)
    out: list[str] = []
    wk = weekly(acts, ref, 3)
    prev2, prev1, cur = wk.iloc[0], wk.iloc[1], wk.iloc[2]
    for a, b, label in ((prev2, prev1, "S-1 vs S-2"), (prev1, cur, "S (en cours) vs S-1")):
        if a["run_km"] >= 5 and b["run_km"] > 1.3 * a["run_km"]:
            out.append(f"🟠 Volume course en hausse de {b['run_km'] / a['run_km'] * 100 - 100:.0f} % ({label}). "
                       "Au-delà de ~30 %, le risque de blessure augmente (Nielsen 2014).")

    runs = acts[acts["sport"] == "run"]
    for _, r in between(runs, ref - timedelta(days=13), ref).iterrows():
        before = between(runs, r["date"].date() - timedelta(days=30), r["date"].date() - timedelta(days=1))
        if len(before) and r["distance_km"] > 1.1 * before["distance_km"].max() and r["distance_km"] >= 8:
            out.append(f"🟠 Sortie du {r['date']:%d/%m} ({r['distance_km']:.1f} km) > 110 % de la plus longue des "
                       f"30 jours précédents ({before['distance_km'].max():.1f} km). Pic ponctuel à surveiller (Frandsen 2025).")

    ls, unit = load_series(acts, ref, days=7)
    if not ls.empty and pd.notna(ls["ratio"].iloc[-1]):
        ratio = ls["ratio"].iloc[-1]
        if ratio > 1.5:
            out.append(f"🟠 Charge aiguë/chronique = {ratio:.2f} ({unit}) : semaine nettement plus chargée que d'habitude.")
        elif ratio < 0.7:
            out.append(f"🔵 Charge aiguë/chronique = {ratio:.2f} : semaine allégée (normal en décharge ou en affûtage).")

    for i, (_, w) in enumerate(wk.tail(2).iterrows()):
        if w["zone_min"] >= 120 and w["z12_pct"] is not None and w["z12_pct"] < 75:
            out.append(f"🟠 Seulement {w['z12_pct']:.0f} % du temps en Z1-Z2 ({'S-1' if i == 0 else 'S'}). "
                       "Cible ~80 % : les footings sont-ils vraiment faciles ?")

    f = form(wellness, ref)
    if f.get("hrv_below_5d", 0) >= 3:
        out.append(f"🟠 HRV sous la baseline {f['hrv_below_5d']} nuits sur 5 : fatigue, stress ou maladie possible.")
    if f.get("rhr_7d") and f.get("rhr_28d") and f["rhr_7d"] >= f["rhr_28d"] + 5:
        out.append(f"🟠 FC de repos 7 j ({f['rhr_7d']:.0f}) > moyenne 28 j ({f['rhr_28d']:.0f}) de 5 bpm ou plus.")
    if f.get("sleep_7d") and f["sleep_7d"] < 7:
        out.append(f"🟠 Sommeil moyen 7 j : {f['sleep_7d']:.1f} h (< 7 h).")

    # Règle des 2 signaux sur 3 (HRV, FC repos, check-in) : voir knowledge/recuperation.md.
    signals = []
    hrv_7d, base_low = f.get("hrv_7d"), f.get("hrv_base_low")
    if hrv_7d and base_low and pd.notna(base_low) and hrv_7d < base_low:
        signals.append("HRV 7 j sous la baseline")
    if f.get("rhr_7d") and f.get("rhr_28d") and f["rhr_7d"] >= f["rhr_28d"] + 5:
        signals.append("FC de repos élevée")
    if not checkins.empty:
        last2 = between(checkins, ref - timedelta(days=1), ref)
        bad = last2[(last2.get("fatigue", pd.Series(dtype=float)) >= 4) | (last2.get("sommeil", pd.Series(dtype=float)) <= 2)]
        if not bad.empty:
            signals.append("check-in défavorable (fatigue ≥ 4 ou sommeil ≤ 2)")
    if len(signals) >= 2:
        out.append(f"🔴 {len(signals)} signaux de fatigue sur 3 ({', '.join(signals)}) : "
                   "la prochaine séance intense devient une sortie facile.")

    if not checkins.empty and "douleur" in checkins:
        recent = between(checkins, ref - timedelta(days=7), ref)
        for _, c in recent.iterrows():
            if pd.notna(c.get("douleur")) and c["douleur"] >= 1:
                zone = c.get("douleur_zone") if pd.notna(c.get("douleur_zone")) else "?"
                level = "🔴" if c["douleur"] > 3 else "🟠"
                out.append(f"{level} Douleur {c['douleur']:g}/10 ({zone}) signalée le {c['date']:%d/%m} : appliquer la règle de "
                           "douleur (≤ 3/10, stable, normale le lendemain matin) et vérifier l'évolution.")
    return out


# --- Totaux et régularité ----------------------------------------------------------------------


def totals(acts: pd.DataFrame, ref: date) -> dict[str, dict[str, float]]:
    acts = ensure_columns(acts)
    out = {}
    for label, df in (("year", acts[acts["date"].dt.year == ref.year]), ("all", acts)):
        run, bike = df[df["sport"] == "run"], df[df["sport"] == "bike"]
        out[label] = {
            "run_km": float(run["distance_km"].sum()), "run_h": float(run["duration_min"].sum() / 60),
            "run_n": len(run), "run_elev": float(run["elev_gain_m"].fillna(0).sum()),
            "bike_km": float(bike["distance_km"].sum()), "bike_h": float(bike["duration_min"].sum() / 60),
            "bike_n": len(bike), "strength_n": int((df["sport"] == "strength").sum()),
        }
    return out


def run_streak_weeks(acts: pd.DataFrame, ref: date, min_runs: int = 3) -> int:
    """Semaines consécutives avec au moins `min_runs` sorties, en comptant la semaine en cours si déjà atteinte."""
    wk = weekly(acts, ref, 104)
    ok = (wk["run_n"] >= min_runs).tolist()
    if ok and not ok[-1]:
        ok = ok[:-1]  # semaine en cours pas encore validée : on ne casse pas la série
    n = 0
    for v in reversed(ok):
        if not v:
            break
        n += 1
    return n
