"""Chemins et constantes partagés par tous les scripts."""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# Surchargeable pour tester sur des données factices sans toucher aux vraies.
DATA = Path(os.environ.get("RUN_COACH_DATA", ROOT / "data"))
RAW = DATA / "raw"
RAW_ACTIVITIES = RAW / "activities"
RAW_WORKOUTS = RAW / "workouts"
CHARTS = Path(os.environ.get("RUN_COACH_CHARTS", ROOT / "assets" / "charts"))
README = Path(os.environ.get("RUN_COACH_README", ROOT / "README.md"))

ACTIVITIES_CSV = DATA / "activities.csv"
WELLNESS_CSV = DATA / "wellness.csv"
METRICS_CSV = DATA / "metrics.csv"
RECORDS_JSON = DATA / "records.json"
PLANNED_JSON = DATA / "planned.json"
PLANNED_MANUAL_CSV = DATA / "planned_manual.csv"
CHECKINS_CSV = DATA / "checkins.csv"
GARMIN_PROFILE_JSON = DATA / "garmin_profile.json"
GOALS_JSON = DATA / "goals.json"
SYNC_STATE = DATA / ".sync_state.json"

# Jetons Garmin : hors du repo, dans le dossier par défaut de la lib.
TOKENSTORE = str(Path("~/.garminconnect").expanduser())

GARMIN_ACTIVITY_URL = "https://connect.garmin.com/modern/activity/{id}"
