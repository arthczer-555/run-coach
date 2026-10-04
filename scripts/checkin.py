"""Enregistre un check-in de ressenti dans data/checkins.csv (une ligne par jour, remplacée si elle existe).

Échelles 1 à 5 (inspirées de l'indice de Hooper) :
  sommeil : 1 très mauvais → 5 excellent      fatigue : 1 aucune → 5 épuisé
  courbatures : 1 aucune → 5 fortes          stress : 1 aucun → 5 très élevé
  motivation : 1 nulle → 5 à bloc            douleur : 0 à 10 (+ zone)

Usage (le coach le lance après avoir posé les questions) :
  uv run scripts/checkin.py --sommeil 4 --fatigue 2 --courbatures 2 --stress 3 --motivation 4 \
      --douleur 2 --douleur-zone "genou droit" --notes "partiels cette semaine"
"""

from __future__ import annotations

import argparse
import csv
from datetime import date

from coach.load import CHECKIN_COLUMNS
from coach.paths import CHECKINS_CSV


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--date", default=date.today().isoformat())
    for name in ("sommeil", "fatigue", "courbatures", "stress", "motivation"):
        p.add_argument(f"--{name}", type=int, choices=range(1, 6))
    p.add_argument("--douleur", type=float, help="0 à 10")
    p.add_argument("--douleur-zone", dest="douleur_zone", default="")
    p.add_argument("--notes", default="")
    args = vars(p.parse_args())

    rows: list[dict[str, str]] = []
    if CHECKINS_CSV.exists():
        with CHECKINS_CSV.open(encoding="utf-8") as f:
            rows = [r for r in csv.DictReader(f) if r["date"] != args["date"]]
    rows.append({c: "" if args.get(c) is None else str(args[c]) for c in CHECKIN_COLUMNS})
    rows.sort(key=lambda r: r["date"])
    CHECKINS_CSV.parent.mkdir(parents=True, exist_ok=True)
    with CHECKINS_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CHECKIN_COLUMNS)
        w.writeheader()
        w.writerows(rows)
    print(f"Check-in du {args['date']} enregistré.")


if __name__ == "__main__":
    main()
