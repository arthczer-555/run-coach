"""Chargement des fichiers propres de data/ en DataFrames prêts à l'analyse."""

from __future__ import annotations

from typing import Any

import pandas as pd

from coach.paths import (
    ACTIVITIES_CSV, CHECKINS_CSV, GARMIN_PROFILE_JSON, GOALS_JSON, METRICS_CSV, PLANNED_JSON,
    PLANNED_MANUAL_CSV, RECORDS_JSON, WELLNESS_CSV,
)
from coach.util import read_json

PLANNED_COLUMNS = ["date", "sport", "title", "details", "description", "duration_min", "distance_km", "source"]
CHECKIN_COLUMNS = ["date", "sommeil", "fatigue", "courbatures", "stress", "motivation", "douleur_zone", "douleur", "notes"]


def _csv(path: Any, date_cols: tuple[str, ...] = ("date",)) -> pd.DataFrame:
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame()
    df = pd.read_csv(path)
    for c in date_cols:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    return df


def activities() -> pd.DataFrame:
    df = _csv(ACTIVITIES_CSV)
    if not df.empty:
        df["start_local"] = pd.to_datetime(df["start_local"], errors="coerce")
        df["description"] = df["description"].fillna("")
    return df


def wellness() -> pd.DataFrame:
    return _csv(WELLNESS_CSV)


def metrics() -> pd.DataFrame:
    return _csv(METRICS_CSV)


def checkins() -> pd.DataFrame:
    return _csv(CHECKINS_CSV)


def planned() -> pd.DataFrame:
    """Séances prévues : calendrier Garmin (Kiprun exporté) + saisies manuelles.

    Sources manuelles (data/planned_manual.csv) : "kiprun" (transcription de captures),
    "coach" (programme complémentaire vélo / renfo / mobilité) et "annule" (masque une
    séance Garmin de même date et même titre). Une transcription
    "kiprun" est ignorée si Garmin a déjà une séance du même sport ce jour-là, car
    l'export Garmin est plus frais (le plan Pacer s'adapte).
    """
    rows = read_json(PLANNED_JSON, {}).get("items", [])
    garmin = pd.DataFrame(rows).reindex(columns=PLANNED_COLUMNS)
    manual = _csv(PLANNED_MANUAL_CSV, date_cols=()).reindex(columns=PLANNED_COLUMNS)
    garmin["date"] = pd.to_datetime(garmin["date"], errors="coerce")
    manual["date"] = pd.to_datetime(manual["date"], errors="coerce")
    # Source "annule" : séance fantôme du calendrier Garmin à ignorer (ex. séance Pacer exportée puis déplacée).
    cancel = manual[manual["source"] == "annule"]
    manual = manual[manual["source"] != "annule"]
    if not cancel.empty and not garmin.empty:
        drop = set(zip(cancel["date"], cancel["title"]))
        garmin = garmin[~garmin.apply(lambda r: (r["date"], r["title"]) in drop, axis=1)]
    if not manual.empty and not garmin.empty:
        covered = set(zip(garmin["date"], garmin["sport"]))
        dup = manual.apply(lambda r: r["source"] == "kiprun" and (r["date"], r["sport"]) in covered, axis=1)
        manual = manual[~dup]
    frames = [f for f in (garmin, manual) if not f.empty]
    if not frames:
        return pd.DataFrame(columns=PLANNED_COLUMNS)
    df = pd.concat(frames, ignore_index=True).sort_values(["date", "sport"])
    for c in ("details", "description", "title"):
        df[c] = df[c].fillna("")
    return df.reset_index(drop=True)


def records() -> list[dict[str, Any]]:
    return read_json(RECORDS_JSON, [])


def garmin_profile() -> dict[str, Any]:
    return read_json(GARMIN_PROFILE_JSON, {})


def goals() -> dict[str, Any]:
    return read_json(GOALS_JSON, {})
