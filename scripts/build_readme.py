"""Régénère les graphs (assets/charts) et les blocs automatiques du README.

Seuls les blocs <!-- AUTO:nom:start --> ... <!-- AUTO:nom:end --> sont réécrits.
Les sections écrites par le coach (mot du coach, programmes, santé) ne sont jamais touchées.

Usage : uv run scripts/build_readme.py [--date AAAA-MM-JJ]
"""

from __future__ import annotations

import argparse
import re
from datetime import date, timedelta
from typing import Any

import pandas as pd

from coach import achievements, charts, load
from coach import metrics as m
from coach.paths import CHARTS, README
from coach.sports import SPORT_EMOJI
from coach.util import fmt_date_fr, fmt_duration, fmt_pace, fmt_race_time, monday_of

CHART_INFO = {
    "volume": ("📊 Volume hebdomadaire", "Kilomètres de course par semaine (semaine en cours en clair) et heures de vélo."),
    "prediction": ("🔮 Prédiction semi vs objectif", "Prédiction Garmin du temps sur semi. Vers le haut = plus rapide."),
    "intensite": ("🌡️ Distribution de l'intensité", "Part du temps passé par zone FC chaque semaine. Repère : ~80 % en facile."),
    "charge": ("⚖️ Charge aiguë vs chronique", "Charge des 7 derniers jours vs moyenne hebdo des 28 derniers. "
                                               "Hors de la bande = semaine inhabituelle (signal, pas verdict)."),
    "forme": ("🔋 Forme", "HRV nocturne (bande = baseline Garmin), FC de repos, sommeil. Points = nuits, ligne = moyenne 7 j."),
    "efficience": ("🫀 Efficience aérobie", "Mètres parcourus par battement sur les sorties faciles. Ça monte = le moteur progresse."),
    "regularite": ("🗓️ Régularité", "Minutes d'entraînement par jour sur un an (course, vélo, renfo)."),
}


def bar(progress: float, width: int = 12) -> str:
    full = int(max(0.0, min(progress, 1.0)) * width)  # arrondi inférieur : jamais « plein » avant 100 %
    return "█" * full + "░" * (width - full)


def picture(name: str, alt: str) -> str:
    return (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="assets/charts/{name}-dark.svg">\n'
            f'  <img alt="{alt}" src="assets/charts/{name}-light.svg" width="100%">\n</picture>')


# --- Blocs ---------------------------------------------------------------------------


def block_maj(acts: pd.DataFrame, today: date) -> str:
    last = ""
    if not acts.empty:
        a = acts.sort_values("start_local").iloc[-1]
        last = f" · dernière activité : {fmt_date_fr(a['date'].date())} ({m.act_summary(a)})"
    return f"<sub>Mis à jour le {today:%d/%m/%Y}{last}</sub>"


def block_objectif(acts: pd.DataFrame, planned: pd.DataFrame, metrics_df: pd.DataFrame, goals: dict[str, Any], today: date) -> str:
    race = goals.get("race") or {}
    if not race.get("date"):
        return "_Pas d'objectif daté. Le coach le renseignera dans `data/goals.json`._"
    rdate = date.fromisoformat(race["date"])
    days_left = (rdate - today).days
    target = race.get("target_s")
    dist = race.get("distance_km", 21.0975)
    head = [f"### {race.get('emoji', '🎯')} {race.get('name', 'Course')} · {rdate.day} {fmt_date_fr(rdate).split(' ', 1)[1]} {rdate.year}"]
    if days_left > 0:
        head.append(f"## J-{days_left}")
    elif days_left == 0:
        head.append("## C'est aujourd'hui ! 🔥")
    else:
        head.append(f"## Terminé il y a {-days_left} j")
    if target:
        head.append(f"**Objectif {fmt_race_time(target)}** · {fmt_pace(target / 60 / dist)}/km")

    pred, pred_sub = "-", ""
    if not metrics_df.empty and "pred_semi_s" in metrics_df and metrics_df["pred_semi_s"].notna().any():
        p = metrics_df.dropna(subset=["pred_semi_s"])
        last = p.iloc[-1]
        pred = f"**{fmt_race_time(last['pred_semi_s'])}**"
        old = p[p["date"] <= last["date"] - pd.Timedelta(days=28)]
        if not old.empty:
            delta = last["pred_semi_s"] - old.iloc[-1]["pred_semi_s"]
            arrow = "▼" if delta < 0 else "▲"
            pred_sub = f"<br><sub>{arrow} {fmt_duration(abs(delta))} en 4 sem.</sub>"
        if target:
            gap = last["pred_semi_s"] - target
            pred_sub += f"<br><sub>{'🟢 prédiction sous l\'objectif' if gap <= 0 else f'🟠 {fmt_duration(gap)} à gagner'}</sub>"
    vo2 = "-"
    if not metrics_df.empty and "vo2max_run" in metrics_df and metrics_df["vo2max_run"].notna().any():
        vo2 = f"**{metrics_df.dropna(subset=['vo2max_run']).iloc[-1]['vo2max_run']:.0f}**"
    streak = m.run_streak_weeks(acts, today)
    days = m.week_plan(acts, planned, monday_of(today), today)
    ok, due = m.compliance(days)
    plan_cell = f"**{ok}/{due}** {'✅' if ok == due else '⚠️'}" if due else "**-**"
    wk = m.weekly(acts, today, 1).iloc[0]

    lines = ['<div align="center">', "", *head, "",
             "| 🔮 Prédiction Garmin | 🫁 VO2max | 🔥 Série ≥ 3 sorties/sem. | ✅ Plan cette semaine | 🏃 Km cette semaine |",
             "|:-:|:-:|:-:|:-:|:-:|",
             f"| {pred}{pred_sub} | {vo2} | **{streak} sem.** | {plan_cell} | **{wk['run_km']:.1f}** |", ""]
    if goals.get("plan_start"):
        start = date.fromisoformat(goals["plan_start"])
        total = (rdate - start).days
        if total > 0:
            prog = (today - start).days / total
            lines += [f"`{bar(prog, 24)}` {max(0, min(prog, 1)) * 100:.0f} % de la prépa", ""]
    lines.append("</div>")
    return "\n".join(lines)


def block_semaine(acts: pd.DataFrame, planned: pd.DataFrame, today: date) -> str:
    mon = monday_of(today)
    out = []
    for title, monday in (("Cette semaine", mon), ("Semaine prochaine", mon + timedelta(weeks=1))):
        days = m.week_plan(acts, planned, monday, today)
        out += [f"#### {title} · {fmt_date_fr(monday)} → {fmt_date_fr(monday + timedelta(days=6))}", "",
                m.week_table_md(days, today), ""]
    if planned.empty or m.between(planned, mon + timedelta(weeks=1), mon + timedelta(days=13)).empty:
        out.append("> ⏳ Séances de la semaine prochaine pas encore connues (export Kiprun → Garmin ou capture du plan).\n")
    out.append("<sub>✅ fait · 🔄 décalé · ❌ manqué · ⏳ aujourd'hui · 🗓️ à venir · ➕ hors plan · 😴 repos</sub>")
    return "\n".join(out)


def _short(p: dict[str, Any]) -> str:
    """Libellé compact d'une séance prévue pour la grille du programme."""
    emo = SPORT_EMOJI.get(p["sport"], "✨")
    title = str(p["title"]).replace("allure de course", "allure course").replace("(R=", "(r ")
    if p.get("source") == "coach":
        title = title.split(" · ")[0]  # "Renfo A · Jambes solides" -> "Renfo A" : la grille reste lisible
    if p["sport"] == "run" and pd.notna(p.get("distance_km")) and p.get("distance_km") and "km" not in title.lower():
        title += f" · {p['distance_km']:g} km"
    elif p["sport"] in ("bike", "strength", "mobility") and pd.notna(p.get("duration_min")) and p.get("duration_min"):
        title += f" · {m.fmt_minutes(p['duration_min'])}"
    return f"{emo} {title}"


def block_programme(acts: pd.DataFrame, planned: pd.DataFrame, goals: dict[str, Any], today: date) -> str:
    """Grille semaine par semaine (course Kiprun + renfo + vélo) jusqu'à la course objectif."""
    race = goals.get("race") or {}
    if planned.empty or not race.get("date"):
        return "_Le calendrier apparaîtra quand des séances seront planifiées._"
    rdate = date.fromisoformat(race["date"])
    lines = ["| Semaine | Lu | Ma | Me | Je | Ve | Sa | Di |", "|---|---|---|---|---|---|---|---|"]
    mon = monday_of(today)
    race_mon = monday_of(rdate)
    while mon <= rdate:
        days = m.week_plan(acts, planned, mon, today)
        cells = []
        for d in days:
            items = []
            for p in d.planned:
                mark = {"done": " ✅", "moved": " 🔄", "missed": " ❌"}.get(p["status"], "")
                items.append(_short(p) + mark)
            if d.day == rdate:
                items.append(f"🏁 **{race.get('name', 'Course')}**")
            cell = "<br>".join(items)
            cells.append(f"**{cell}**" if d.day == today and cell else cell)
        left = (race_mon - mon).days // 7
        sub = "semaine de course" if left == 0 else f"course dans {left} sem."
        label = f"**{fmt_date_fr(mon)}**<br><sub>{sub}</sub>" + (" 👈" if mon == monday_of(today) else "")
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
        mon += timedelta(weeks=1)
    lines.append("")
    lines.append("<sub>🏃 Kiprun Pacer (synchronisé depuis Garmin) · 🏋️ renfo · 🚴 vélo · ✅ fait · 🔄 décalé · ❌ manqué. "
                 "👈 semaine en cours. Le plan Pacer s'adapte : cette grille est régénérée à chaque mise à jour.</sub>")
    return "\n".join(lines)


def block_graphs(produced: dict[str, bool]) -> str:
    out = []
    for name, (title, caption) in CHART_INFO.items():
        if not produced.get(name):
            continue
        out += [f"### {title}", f"<sub>{caption}</sub>", "", picture(name, title), ""]
    if not out:
        return "_Les graphs apparaîtront après la première synchronisation Garmin._"
    return "\n".join(out).rstrip()


def block_records(acts: pd.DataFrame, records: list[dict[str, Any]]) -> str:
    lines = ["| | Distance | Temps | Allure | Date | Séance |", "|:-:|---|--:|--:|---|---|"]
    medals = {1: "⚡", 3: "🥉", 4: "🥈", 5: "🥇", 6: "👑", 7: "📏"}
    for r in records:
        if r["type_id"] == 2:  # le mile n'intéresse pas grand monde ici
            continue
        dist_km = {1: 1, 3: 5, 4: 10, 5: 21.0975, 6: 42.195}.get(r["type_id"])
        if r["unit"] == "s":
            val, pace = fmt_race_time(r["value"]), fmt_pace(r["value"] / 60 / dist_km) + "/km" if dist_km else ""
        else:
            val, pace = f"{r['value'] / 1000:.1f} km", ""
        link = f"[{r['activity_name'] or 'voir'}]({r['url']})" if r.get("url") else ""
        when = pd.Timestamp(r["date"]).strftime("%d/%m/%Y") if r.get("date") else ""
        lines.append(f"| {medals.get(r['type_id'], '🏅')} | **{r['label']}** | {val} | {pace} | {when} | {link} |")
    acts = m.ensure_columns(acts)
    bikes = acts[acts["sport"] == "bike"]
    if not bikes.empty:
        b = bikes.loc[bikes["distance_km"].idxmax()]
        lines.append(f"| 🚴 | **Plus longue sortie vélo** | {b['distance_km']:.0f} km | {fmt_duration(b['duration_min'] * 60)} | "
                     f"{b['date']:%d/%m/%Y} | [{b['name']}]({b['url']}) |")
    if not acts.empty:
        wk = acts[acts["sport"] == "run"].groupby(acts["date"].dt.to_period("W-SUN"))["distance_km"].sum()
        if not wk.empty:
            lines.append(f"| 📈 | **Plus grosse semaine** | {wk.max():.1f} km | | sem. du {wk.idxmax().start_time:%d/%m/%Y} | |")
    if len(lines) == 2:
        return "_Les records Garmin apparaîtront après la première synchronisation._"
    return "\n".join(lines)


def block_achievements(acts: pd.DataFrame, records: list[dict[str, Any]], today: date) -> str:
    res = achievements.evaluate(acts, records, today)
    unlocked = sorted([(a, r) for a, r in res if r.unlocked], key=lambda x: x[1].when or "", reverse=True)
    locked = sorted([(a, r) for a, r in res if not r.unlocked], key=lambda x: -x[1].progress)

    def grid(items: list[tuple[Any, Any]], cols: int = 4) -> list[str]:
        cells = []
        for a, r in items:
            if r.unlocked:
                when = pd.Timestamp(r.when).strftime("%d/%m/%Y") if r.when else ""
                cells.append(f"{a.emoji}<br>**{a.name}**<br><sub>{a.desc}</sub><br><sub>✅ {when}</sub>")
            else:
                prog = f"<br><sub>`{bar(r.progress, 8)}` {r.label}</sub>" if r.label else ""
                cells.append(f"🔒<br>**{a.name}**<br><sub>{a.desc}</sub>{prog}")
        rows = ["|" + " |" * cols, "|" + ":-:|" * cols]
        for i in range(0, len(cells), cols):
            chunk = cells[i:i + cols] + [""] * (cols - len(cells[i:i + cols]))
            rows.append("| " + " | ".join(chunk) + " |")
        return rows

    out = [f"**{len(unlocked)} / {len(res)} débloqués** `{bar(len(unlocked) / len(res), 20)}`", ""]
    if unlocked:
        out += grid(unlocked) + [""]
    if locked:
        out += ["<details><summary>🔒 À débloquer</summary>", ""] + grid(locked) + ["", "</details>"]
    return "\n".join(out)


def block_totaux(acts: pd.DataFrame, today: date) -> str:
    t = m.totals(acts, today)
    y, a = t["year"], t["all"]
    return "\n".join([
        f"| | {today.year} | Depuis le début |", "|---|--:|--:|",
        f"| 🏃 Course | **{y['run_km']:.0f} km** · {y['run_n']} sorties · {y['run_h']:.0f} h | **{a['run_km']:.0f} km** · {a['run_n']} sorties · {a['run_h']:.0f} h |",
        f"| ⛰️ D+ course | {y['run_elev']:.0f} m | {a['run_elev']:.0f} m |",
        f"| 🚴 Vélo | {y['bike_km']:.0f} km · {y['bike_n']} sorties · {y['bike_h']:.0f} h | {a['bike_km']:.0f} km · {a['bike_n']} sorties · {a['bike_h']:.0f} h |",
        f"| 🏋️ Renfo | {y['strength_n']} séances | {a['strength_n']} séances |",
    ])


# --- Assemblage ---------------------------------------------------------------------------


def replace_block(text: str, name: str, content: str) -> str:
    pattern = re.compile(rf"(<!-- AUTO:{name}:start -->).*?(<!-- AUTO:{name}:end -->)", re.DOTALL)
    if not pattern.search(text):
        print(f"⚠️ Bloc AUTO:{name} absent du README, ignoré.")
        return text
    return pattern.sub(lambda mt: f"{mt.group(1)}\n{content}\n{mt.group(2)}", text)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", help="date de référence AAAA-MM-JJ (défaut : aujourd'hui)")
    args = parser.parse_args()
    today = date.fromisoformat(args.date) if args.date else date.today()

    acts, planned = load.activities(), load.planned()
    wellness, metrics_df = load.wellness(), load.metrics()
    records, goals = load.records(), load.goals()

    produced = charts.render_all(acts, wellness, metrics_df, goals.get("race") or {}, today, CHARTS)
    text = README.read_text(encoding="utf-8")
    blocks = {
        "maj": block_maj(acts, today),
        "objectif": block_objectif(acts, planned, metrics_df, goals, today),
        "semaine": block_semaine(acts, planned, today),
        "programme": block_programme(acts, planned, goals, today),
        "graphs": block_graphs(produced),
        "records": block_records(acts, records),
        "achievements": block_achievements(acts, records, today),
        "totaux": block_totaux(acts, today),
    }
    for name, content in blocks.items():
        text = replace_block(text, name, content)
    README.write_text(text, encoding="utf-8")
    print(f"README mis à jour ({sum(produced.values())} graphs).")


if __name__ == "__main__":
    main()
