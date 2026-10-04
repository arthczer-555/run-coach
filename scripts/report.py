"""Bilan brut S-1 / S / S+1 en markdown, lu par le coach avant chaque conversation.

Usage :
  uv run scripts/report.py                  # référence = aujourd'hui
  uv run scripts/report.py --date 2026-10-12
  uv run scripts/report.py --trend 12       # nombre de semaines dans le tableau de tendance
"""

from __future__ import annotations

import argparse
from datetime import date, timedelta
from typing import Any

import pandas as pd

from coach import load
from coach import metrics as m
from coach.paths import RAW_ACTIVITIES
from coach.util import FR_DAYS, df_to_md, fmt_date_fr, fmt_duration, fmt_pace, fmt_race_time, monday_of, read_json


def laps_line(activity_id: Any) -> str:
    """Résumé compact des laps d'une course (utile pour juger une séance de fractionné)."""
    detail = read_json(RAW_ACTIVITIES / f"{activity_id}.json", {})
    laps = ((detail.get("splits") or {}).get("lapDTOs")) or []
    if len(laps) < 3:
        return ""
    paces = [1000 / lap["averageSpeed"] / 60 for lap in laps if lap.get("averageSpeed") and (lap.get("distance") or 0) >= 150]
    if paces and max(paces) - min(paces) < 0.4:
        return ""  # allure régulière (auto-lap d'un footing) : les laps n'apportent rien
    parts = []
    for lap in laps[:30]:
        dist = (lap.get("distance") or 0) / 1000
        speed = lap.get("averageSpeed")
        pace = fmt_pace(1000 / speed / 60) if speed else "-"
        hr = lap.get("averageHR")
        parts.append(f"{dist:.2f} km {pace}" + (f" {int(hr)}" if hr else ""))
    return "Laps (km allure FC) : " + " | ".join(parts)


def section_week(title: str, acts: pd.DataFrame, planned: pd.DataFrame, monday: date, today: date) -> list[str]:
    sunday = monday + timedelta(days=6)
    days = m.week_plan(acts, planned, monday, today)
    wk = m.weekly(acts, sunday, 1).iloc[0]
    ok, due = m.compliance(days)
    out = [f"## {title} : {fmt_date_fr(monday)} → {fmt_date_fr(sunday)}", ""]
    if monday <= today:
        z = f"{wk['z12_pct']:.0f} % Z1-2 / {wk['z3_pct']:.0f} % Z3 / {wk['z45_pct']:.0f} % Z4-5" if wk["z12_pct"] is not None else "zones FC indisponibles"
        out += [
            f"- Course : **{wk['run_km']:.1f} km** en {wk['run_n']} sortie(s), {fmt_duration(wk['run_min'] * 60)}, "
            f"plus longue {wk['long_run_km']:.1f} km, D+ {wk['elev_m']:.0f} m",
            f"- Vélo : {wk['bike_n']} sortie(s), {fmt_duration(wk['bike_min'] * 60)} ; renfo : {wk['strength_n']} séance(s)",
            f"- Intensité (temps en zones FC, course + vélo) : {z} ; charge {wk['load']:.0f}",
            f"- Plan : {ok}/{due} séances dues réalisées" if due else "- Plan : aucune séance due",
            "",
        ]
    out += [m.week_table_md(days, today), ""]

    done = m.between(m.ensure_columns(acts), monday, sunday)
    if not done.empty:
        out.append("**Détail des séances réalisées**")
        out.append("")
        for _, a in done.sort_values("start_local").iterrows():
            zones = a[m.ZONE_COLS].fillna(0)
            tz = zones.sum()
            zpct = " / ".join(f"Z{i + 1} {v / tz * 100:.0f}%" for i, v in enumerate(zones)) if tz > 0 else ""
            line = f"- {FR_DAYS[a['date'].weekday()]} {a['date']:%d/%m} {a['start_local']:%H:%M} · « {a['name']} » · {m.act_summary(a)}"
            if pd.notna(a.get("max_hr")):
                line += f" · FC max {int(a['max_hr'])}"
            if pd.notna(a.get("feel")) and a.get("feel"):
                line += f" · ressenti montre : {a['feel']}"
            out.append(line)
            if zpct:
                out.append(f"  - Zones : {zpct}")
            if a.get("description"):
                out.append(f"  - Note : {a['description']}")
            if a["sport"] == "run":
                lp = laps_line(a["id"])
                if lp:
                    out.append(f"  - {lp}")
        out.append("")

    plan_w = m.between(planned, monday, sunday) if not planned.empty else planned
    detailed = plan_w[plan_w["details"].astype(bool) | plan_w["description"].astype(bool)] if not plan_w.empty else plan_w
    if not detailed.empty:
        out.append("**Contenu des séances prévues**")
        out.append("")
        for _, p in detailed.iterrows():
            txt = p["details"] or p["description"]
            out.append(f"- {FR_DAYS[p['date'].weekday()]} {p['date']:%d/%m} · {p['title']} ({p['source']}) : {txt}")
        out.append("")
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="date de référence AAAA-MM-JJ (défaut : aujourd'hui)")
    parser.add_argument("--trend", type=int, default=8, help="semaines dans le tableau de tendance")
    args = parser.parse_args()
    today = date.fromisoformat(args.date) if args.date else date.today()

    acts, planned = load.activities(), load.planned()
    wellness, checkins, metrics_df = load.wellness(), load.checkins(), load.metrics()
    goals = load.goals()
    mon = monday_of(today)

    out = [f"# Bilan coach, généré pour le {FR_DAYS[today.weekday()]} {today:%d/%m/%Y}", ""]
    if acts.empty:
        out += ["⚠️ Aucune activité dans data/. Lancer `uv run scripts/sync.py --full`.", ""]

    # Objectif
    race = goals.get("race") or {}
    if race.get("date"):
        rdate = date.fromisoformat(race["date"])
        target = race.get("target_s")
        line = f"## Objectif : {race.get('name', 'course')} le {rdate:%d/%m/%Y} (J-{(rdate - today).days})"
        if target:
            line += f", visé en {fmt_race_time(target)} ({fmt_pace(target / 60 / race.get('distance_km', 21.0975))}/km)"
        out += [line, ""]
        if not metrics_df.empty and "pred_semi_s" in metrics_df and metrics_df["pred_semi_s"].notna().any():
            last = metrics_df.dropna(subset=["pred_semi_s"]).iloc[-1]
            month_ago = metrics_df[(metrics_df["date"] <= last["date"] - pd.Timedelta(days=28))].dropna(subset=["pred_semi_s"])
            trend = f" (il y a 4 sem. : {fmt_race_time(month_ago.iloc[-1]['pred_semi_s'])})" if not month_ago.empty else ""
            out.append(f"- Prédiction Garmin semi : **{fmt_race_time(last['pred_semi_s'])}** au {last['date']:%d/%m}{trend}")
        if not metrics_df.empty and "vo2max_run" in metrics_df and metrics_df["vo2max_run"].notna().any():
            out.append(f"- VO2max Garmin : {metrics_df.dropna(subset=['vo2max_run']).iloc[-1]['vo2max_run']:.1f}")
        if not metrics_df.empty and "training_status" in metrics_df and metrics_df["training_status"].notna().any():
            out.append(f"- Training status Garmin : {metrics_df.dropna(subset=['training_status']).iloc[-1]['training_status']}")
        out.append("")

    out += section_week("Semaine S-1", acts, planned, mon - timedelta(weeks=1), today)
    out += section_week("Semaine S (en cours)", acts, planned, mon, today)
    out += section_week("Semaine S+1 (à venir)", acts, planned, mon + timedelta(weeks=1), today)
    if planned.empty or m.between(planned, mon + timedelta(weeks=1), mon + timedelta(days=13)).empty:
        out += ["⚠️ Aucune séance prévue en S+1 : demander à Arthur d'exporter ses séances Kiprun vers Garmin "
                "ou une capture du plan (plans/kiprun/captures/).", ""]

    # Tendance
    wk = m.weekly(acts, today, args.trend)
    out += [f"## Tendance ({args.trend} semaines)", "",
            "| Semaine | Course km | Sorties | Plus longue | Vélo | Renfo | % Z1-2 | Charge |",
            "|---|--:|--:|--:|--:|--:|--:|--:|"]
    for _, w in wk.iterrows():
        z = f"{w['z12_pct']:.0f}" if w["z12_pct"] is not None and pd.notna(w["z12_pct"]) else "-"
        out.append(f"| {fmt_date_fr(w['monday'])} | {w['run_km']:.1f} | {w['run_n']} | {w['long_run_km']:.1f} | "
                   f"{fmt_duration(w['bike_min'] * 60) if w['bike_min'] else '-'} | {w['strength_n'] or '-'} | {z} | {w['load']:.0f} |")
    ls, unit = m.load_series(acts, today, days=28)
    if not ls.empty and pd.notna(ls["ratio"].iloc[-1]):
        out.append(f"\nCharge aiguë 7 j / chronique 28 j ({unit}) : {ls['acute'].iloc[-1]:.0f} / {ls['chronic'].iloc[-1]:.0f} "
                   f"= **{ls['ratio'].iloc[-1]:.2f}**")
    out.append(f"\nSérie en cours : {m.run_streak_weeks(acts, today)} semaine(s) d'affilée avec 3 sorties ou plus.")
    out.append("")

    # Forme
    f = m.form(wellness, today)
    night_keys = ("hrv_7d", "rhr_7d", "sleep_7d", "readiness_7d")
    if not any(f.get(k) is not None and pd.notna(f.get(k)) for k in night_keys):
        out += ["## Forme (Garmin)", "",
                "- Aucune donnée de nuit sur 7 jours (HRV, sommeil, FC de repos) : montre non portée la nuit ? "
                "Sans elle, la forme se juge au check-in et aux sensations.", ""]
    elif f:
        def v(key: str, fmt: str = "{:.0f}") -> str:
            val = f.get(key)
            return fmt.format(val) if val is not None and pd.notna(val) else "-"
        out += ["## Forme (Garmin)", "",
                f"- HRV nocturne : 7 j {v('hrv_7d')} ms vs 28 j {v('hrv_28d')} ms, baseline {v('hrv_base_low')}-{v('hrv_base_high')}, "
                f"statut {f.get('hrv_status') or '-'}, nuits sous baseline (5 j) : {v('hrv_below_5d')}",
                f"- FC de repos : 7 j {v('rhr_7d')} vs 28 j {v('rhr_28d')} bpm",
                f"- Sommeil 7 j : {v('sleep_7d', '{:.1f}')} h, score {v('sleep_score_7d')}",
                f"- Training Readiness : dernier {v('readiness_last')}, moyenne 7 j {v('readiness_7d')}", ""]

    # Check-ins
    if not checkins.empty:
        recent = m.between(checkins, today - timedelta(days=14), today)
        if not recent.empty:
            out += ["## Check-ins récents (1-5, douleur /10)", "", df_to_md(recent.assign(date=recent["date"].dt.strftime("%d/%m"))), ""]

    # Signaux
    fl = m.flags(acts, wellness, checkins, today)
    out += ["## Signaux", ""] + ([f"- {x}" for x in fl] if fl else ["- RAS"]) + [""]

    out += ["## À faire par le coach", "",
            "- Demander le ressenti global (sommeil, fatigue, motivation, douleurs) et l'enregistrer : `uv run scripts/checkin.py`.",
            "- Pour chaque ❌ / 🔄 / ➕ : demander pourquoi (contrainte, fatigue, envie, météo…).",
            "- Pour chaque séance de qualité : comparer laps vs cibles prévues, demander le RPE si absent.",
            "- Traiter chaque signal ci-dessus, puis conseiller pour S+1.",
            "- Fin de session : entrée JOURNAL.md + `uv run scripts/build_readme.py` + mot du coach."]
    print("\n".join(out))


if __name__ == "__main__":
    main()
