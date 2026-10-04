"""Connexion unique à Garmin Connect.

Demande email + mot de passe (+ code MFA si activé), puis enregistre les jetons
dans ~/.garminconnect/. Le mot de passe n'est jamais stocké. Les syncs suivantes
réutilisent et rafraîchissent les jetons automatiquement.

Usage : uv run scripts/garmin_login.py
"""

import getpass
import sys

from garminconnect import Garmin

from coach.paths import SYNC_STATE, TOKENSTORE
from coach.util import read_json, write_json


def main() -> int:
    print("Connexion à Garmin Connect (les jetons seront stockés dans ~/.garminconnect/)")
    email = input("Email Garmin : ").strip()
    password = getpass.getpass("Mot de passe Garmin : ")
    api = Garmin(email, password, prompt_mfa=lambda: input("Code MFA : ").strip())
    try:
        api.login(TOKENSTORE)
    except Exception as e:  # noqa: BLE001 - on veut un message clair, quelle que soit l'erreur
        print(f"Échec de connexion : {e}", file=sys.stderr)
        return 1
    print(f"Connecté en tant que {api.get_full_name()}. Jetons enregistrés.")
    # Lève le throttle du hook : la prochaine question déclenchera une sync immédiate.
    state = read_json(SYNC_STATE, {})
    state.pop("last_attempt", None)
    write_json(SYNC_STATE, state)
    print("Prochaine étape : uv run scripts/sync.py --full")
    return 0


if __name__ == "__main__":
    sys.exit(main())
