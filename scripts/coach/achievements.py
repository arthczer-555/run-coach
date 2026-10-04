"""Achievements : règles déclaratives évaluées sur l'historique complet.

Chaque règle renvoie (débloqué, date de déblocage, progression 0..1, libellé de progression).
Pour ajouter un badge : écrire une fonction `_xxx(ctx)` et l'ajouter à ACHIEVEMENTS.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from typing import Any

import pandas as pd

from coach import metrics as m
from coach.util import fmt_race_time


@dataclass
class Ctx:
    acts: pd.DataFrame
    runs: pd.DataFrame
    records: list[dict[str, Any]]
    weekly: pd.DataFrame  # toutes les semaines depuis la première activité
    ref: date


@dataclass
class Result:
    unlocked: bool
    when: str | None
    progress: float
    label: str


@dataclass
class Achievement:
    id: str
    emoji: str
    name: str
    desc: str
    rule: Callable[[Ctx], Result]


def _first_date(df: pd.DataFrame) -> str | None:
    return None if df.empty else f"{df['date'].min():%Y-%m-%d}"


def _distance(km: float) -> Callable[[Ctx], Result]:
    def rule(c: Ctx) -> Result:
        hit = c.runs[c.runs["distance_km"] >= km * 0.995]
        best = float(c.runs["distance_km"].max()) if not c.runs.empty else 0.0
        return Result(not hit.empty, _first_date(hit), min(best / km, 1), f"{best:.1f} / {km:.1f} km")
    return rule


def _record_under(type_id: int, seconds: int, label: str) -> Callable[[Ctx], Result]:
    def rule(c: Ctx) -> Result:
        rec = next((r for r in c.records if r.get("type_id") == type_id), None)
        if rec is None or rec.get("value") is None:
            return Result(False, None, 0.0, f"pas encore de {label}")
        v = float(rec["value"])
        return Result(v <= seconds, rec.get("date") if v <= seconds else None, min(seconds / v, 1), f"record {fmt_race_time(v)}")
    return rule


def _streak(weeks_needed: int, col: str, min_value: int, unit: str) -> Callable[[Ctx], Result]:
    def rule(c: Ctx) -> Result:
        best, cur, when = 0, 0, None
        for _, w in c.weekly.iterrows():
            cur = cur + 1 if w[col] >= min_value else 0
            if cur > best:
                best = cur
            if cur >= weeks_needed and when is None:
                when = f"{w['monday'] + pd.Timedelta(days=6):%Y-%m-%d}"
        return Result(best >= weeks_needed, when, min(best / weeks_needed, 1), f"meilleure série {best} / {weeks_needed} {unit}")
    return rule


def _cumulative(km: float) -> Callable[[Ctx], Result]:
    def rule(c: Ctx) -> Result:
        runs = c.runs.sort_values("date")
        cum = runs["distance_km"].cumsum()
        hit = runs[cum >= km]
        total = float(cum.iloc[-1]) if len(cum) else 0.0
        return Result(not hit.empty, _first_date(hit.head(1)), min(total / km, 1), f"{total:.0f} / {km:g} km")
    return rule


def _month_km(km: float) -> Callable[[Ctx], Result]:
    def rule(c: Ctx) -> Result:
        if c.runs.empty:
            return Result(False, None, 0.0, f"0 / {km:g} km")
        by_month = c.runs.groupby(c.runs["date"].dt.to_period("M"))["distance_km"].sum()
        hit = by_month[by_month >= km]
        best = float(by_month.max())
        when = f"{hit.index[0].end_time:%Y-%m-%d}" if not hit.empty else None
        return Result(not hit.empty, when, min(best / km, 1), f"meilleur mois {best:.0f} / {km:g} km")
    return rule


def _first_of(sport: str) -> Callable[[Ctx], Result]:
    def rule(c: Ctx) -> Result:
        df = c.acts[c.acts["sport"] == sport]
        return Result(not df.empty, _first_date(df), 1.0 if not df.empty else 0.0, "")
    return rule


def _polarized_week(c: Ctx) -> Result:
    ok = c.weekly[(c.weekly["run_n"] >= 3) & (c.weekly["z12_pct"].fillna(0) >= 80)]
    when = f"{ok['monday'].iloc[0] + pd.Timedelta(days=6):%Y-%m-%d}" if not ok.empty else None
    best = c.weekly.loc[c.weekly["run_n"] >= 3, "z12_pct"].max() if (c.weekly["run_n"] >= 3).any() else 0
    best = 0.0 if pd.isna(best) else float(best)
    return Result(not ok.empty, when, min(best / 80, 1), f"meilleure semaine {best:.0f} % en Z1-Z2")


def _hour(before: int | None = None, after: int | None = None) -> Callable[[Ctx], Result]:
    def rule(c: Ctx) -> Result:
        h = c.runs["start_local"].dt.hour
        hit = c.runs[h < before] if before is not None else c.runs[h >= after]
        return Result(not hit.empty, _first_date(hit), 1.0 if not hit.empty else 0.0, "")
    return rule


def _week_elev(meters: float) -> Callable[[Ctx], Result]:
    def rule(c: Ctx) -> Result:
        best = float(c.weekly["elev_m"].max()) if not c.weekly.empty else 0.0
        hit = c.weekly[c.weekly["elev_m"] >= meters]
        when = f"{hit['monday'].iloc[0] + pd.Timedelta(days=6):%Y-%m-%d}" if not hit.empty else None
        return Result(not hit.empty, when, min(best / meters, 1), f"meilleure semaine {best:.0f} / {meters:g} m D+")
    return rule


ACHIEVEMENTS: list[Achievement] = [
    Achievement("first-run", "👟", "Premiers pas", "Première sortie enregistrée", _distance(0.5)),
    Achievement("10k", "🔟", "Cap des 10 km", "Une sortie de 10 km ou plus", _distance(10)),
    Achievement("15k", "🌉", "15 bornes", "Une sortie de 15 km ou plus", _distance(15)),
    Achievement("18k", "🏔️", "18 bornes", "Une sortie de 18 km ou plus", _distance(18)),
    Achievement("semi-distance", "🥇", "Distance semi", "Courir 21,1 km d'une traite", _distance(21.0975)),
    Achievement("sub-25-5k", "⚡", "Sub 25 au 5 km", "Record 5 km sous 25:00", _record_under(3, 25 * 60, "5 km")),
    Achievement("sub-50-10k", "🚀", "Sub 50 au 10 km", "Record 10 km sous 50:00", _record_under(4, 50 * 60, "10 km")),
    Achievement("sub-150-semi", "🎯", "Sub 1h50 au semi", "L'objectif du 22/11/2026", _record_under(5, 110 * 60, "semi")),
    Achievement("streak-4", "📅", "Régulier", "4 semaines d'affilée avec 3 sorties ou plus", _streak(4, "run_n", 3, "sem.")),
    Achievement("streak-8", "🔥", "Machine", "8 semaines d'affilée avec 3 sorties ou plus", _streak(8, "run_n", 3, "sem.")),
    Achievement("streak-16", "🦾", "Inarrêtable", "16 semaines d'affilée avec 3 sorties ou plus", _streak(16, "run_n", 3, "sem.")),
    Achievement("month-100", "💯", "Mois à 100 km", "100 km de course dans un mois", _month_km(100)),
    Achievement("cum-500", "🌍", "500 km", "500 km de course cumulés", _cumulative(500)),
    Achievement("cum-1000", "🪐", "1000 km", "1000 km de course cumulés", _cumulative(1000)),
    Achievement("polarized", "🧊", "Semaine polarisée", "Une semaine à 3 sorties ou plus avec 80 % du temps en Z1-Z2", _polarized_week),
    Achievement("first-bike", "🚴", "En selle", "Première sortie vélo", _first_of("bike")),
    Achievement("bike-4", "🛞", "Rouleur régulier", "4 semaines d'affilée avec une sortie vélo", _streak(4, "bike_n", 1, "sem.")),
    Achievement("first-strength", "🏋️", "Premier renfo", "Première séance de renforcement", _first_of("strength")),
    Achievement("strength-6", "🦵", "Jambes d'acier", "6 semaines d'affilée avec du renfo", _streak(6, "strength_n", 1, "sem.")),
    Achievement("early", "🌅", "Lève-tôt", "Une sortie commencée avant 7 h", _hour(before=7)),
    Achievement("night", "🌙", "Noctambule", "Une sortie commencée après 21 h", _hour(after=21)),
    Achievement("elev-500", "⛰️", "Grimpeur", "500 m de D+ en course sur une semaine", _week_elev(500)),
]


def evaluate(acts: pd.DataFrame, records: list[dict[str, Any]], ref: date) -> list[tuple[Achievement, Result]]:
    acts = m.ensure_columns(acts)
    runs = acts[acts["sport"] == "run"]
    if acts.empty:
        weekly = m.weekly(acts, ref, 1)
    else:
        n_weeks = (m.monday_of(ref) - m.monday_of(acts["date"].min().date())).days // 7 + 1
        weekly = m.weekly(acts, ref, n_weeks)
    ctx = Ctx(acts, runs, records, weekly, ref)
    return [(a, a.rule(ctx)) for a in ACHIEVEMENTS]
