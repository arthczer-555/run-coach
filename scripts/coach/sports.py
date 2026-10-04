"""Classement des types d'activité Garmin en grandes familles."""

RUN_KEYS = {
    "running", "trail_running", "treadmill_running", "track_running", "indoor_running",
    "street_running", "ultra_run", "virtual_run", "obstacle_run",
}
BIKE_KEYS = {
    "cycling", "road_biking", "gravel_cycling", "mountain_biking", "indoor_cycling",
    "virtual_ride", "cyclocross", "track_cycling", "e_bike_fitness", "e_bike_mountain",
    "recumbent_cycling", "bmx", "commuting",
}
STRENGTH_KEYS = {"strength_training", "hiit", "indoor_cardio", "fitness_equipment"}
MOBILITY_KEYS = {"yoga", "pilates", "breathwork", "mobility", "stretching"}
SWIM_KEYS = {"lap_swimming", "open_water_swimming", "swimming"}

SPORT_LABELS = {
    "run": "🏃 Course",
    "bike": "🚴 Vélo",
    "strength": "🏋️ Renfo",
    "mobility": "🧘 Mobilité",
    "swim": "🏊 Natation",
    "race": "🏁 Course officielle",
    "other": "✨ Autre",
}
SPORT_EMOJI = {"run": "🏃", "bike": "🚴", "strength": "🏋️", "mobility": "🧘", "swim": "🏊", "race": "🏁", "other": "✨"}


def sport_of(type_key: str | None) -> str:
    k = (type_key or "").lower()
    if k in RUN_KEYS or k.endswith("_running"):
        return "run"
    if k in BIKE_KEYS or "cycling" in k or "biking" in k:
        return "bike"
    if k in STRENGTH_KEYS or "strength" in k:
        return "strength"
    if k in MOBILITY_KEYS:
        return "mobility"
    if k in SWIM_KEYS or "swim" in k:
        return "swim"
    return "other"
