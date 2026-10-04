"""Petits utilitaires : JSON, dates, accès tolérant aux champs Garmin, formats."""

from __future__ import annotations

import json
from collections.abc import Iterator
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default


def write_json(path: Path, obj: Any, *, compact: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if compact:
        text = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    else:
        text = json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True)
    path.write_text(text + "\n", encoding="utf-8")


def pick(obj: Any, *paths: str, default: Any = None) -> Any:
    """Renvoie la première valeur non nulle parmi des chemins pointés ("a.b.c").

    Garmin renomme parfois ses champs selon les appareils et les versions d'API :
    on essaie plusieurs noms plutôt que de casser.
    """
    for path in paths:
        cur = obj
        for part in path.split("."):
            if isinstance(cur, dict):
                cur = cur.get(part)
            else:
                cur = None
                break
        if cur is not None:
            return cur
    return default


def date_chunks(start: date, end: date, days: int) -> Iterator[tuple[str, str]]:
    cur = start
    while cur <= end:
        chunk_end = min(cur + timedelta(days=days - 1), end)
        yield cur.isoformat(), chunk_end.isoformat()
        cur = chunk_end + timedelta(days=1)


def days_between(start: date, end: date) -> Iterator[date]:
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=1)


def monday_of(d: date) -> date:
    return d - timedelta(days=d.weekday())


def parse_date(value: str) -> date:
    return datetime.strptime(value[:10], "%Y-%m-%d").date()


def fmt_duration(seconds: float | None) -> str:
    """3725 -> '1h02', 1500 -> '25:00' (min:s), None -> '-'."""
    if seconds is None or seconds != seconds:  # NaN
        return "-"
    seconds = int(round(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h{m:02d}"
    return f"{m}:{s:02d}"


def fmt_race_time(seconds: float | None) -> str:
    """Temps de course : 6600 -> '1:50:00', 1500 -> '25:00'."""
    if seconds is None or seconds != seconds:
        return "-"
    seconds = int(round(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def fmt_pace(min_per_km: float | None) -> str:
    """5.2167 -> '5:13'."""
    if min_per_km is None or min_per_km != min_per_km or min_per_km <= 0:
        return "-"
    total = int(round(min_per_km * 60))
    return f"{total // 60}:{total % 60:02d}"


def speed_to_pace(speed_ms: float | None) -> float | None:
    """m/s -> min/km."""
    if not speed_ms or speed_ms <= 0:
        return None
    return 1000 / speed_ms / 60


FR_DAYS = ["Lu", "Ma", "Me", "Je", "Ve", "Sa", "Di"]
FR_MONTHS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]


def fmt_date_fr(d: date) -> str:
    return f"{d.day} {FR_MONTHS[d.month - 1]}"


def df_to_md(df: Any) -> str:
    """DataFrame -> tableau markdown (sans dépendance à tabulate)."""
    cols = list(df.columns)
    lines = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
    for _, row in df.iterrows():
        cells = ["" if (v is None or v != v) else (f"{v:g}" if isinstance(v, float) else str(v)) for v in row]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)
