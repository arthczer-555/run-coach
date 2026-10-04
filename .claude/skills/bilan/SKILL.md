---
name: bilan
description: Bilan de coaching complet S-1 / S / S+1 (course, vélo, renfo, forme), avec questions sur le ressenti et les écarts au plan, conseils, puis mise à jour du JOURNAL et du README. À utiliser quand Arthur demande un bilan, un point sur la semaine, ou « comment ça se passe ».
---

# Bilan de coaching

Suis la routine de bilan décrite dans `CLAUDE.md` (section « Workflow bilan »). En résumé :

1. **Données fraîches** : `uv run scripts/sync.py` (si le hook n'a pas déjà synchronisé il y a moins de 30 min), puis `uv run scripts/report.py`.
2. **Contexte** : relis le « Résumé vivant » de `JOURNAL.md`, `athlete/profil.md`, `athlete/objectifs.md`, `plans/kiprun.md` et `plans/complementaire.md` si un programme est actif.
3. **Analyse** (avant de parler) : volume et progression, respect du plan, qualité des séances clés (laps vs cibles), distribution d'intensité, charge, forme (HRV, FC repos, sommeil), signaux du rapport. Appuie-toi sur `knowledge/`.
4. **Conversation** (questions courtes, groupées, 3 à 6 max) :
   - ressenti global : sommeil, fatigue, courbatures, stress, motivation (1-5), douleurs (0-10 + zone) ;
   - pour chaque séance ❌ manquée, 🔄 décalée ou ➕ hors plan : pourquoi ;
   - pour chaque séance clé : sensations, RPE si absent, et pourquoi l'allure diffère de la cible si c'est le cas.
   Attends les réponses avant de conclure.
5. **Check-in** : enregistre les réponses chiffrées avec `uv run scripts/checkin.py ...`.
6. **Conseils** : 3 à 5 points concrets et priorisés pour S+1 (ce qui compte le plus en premier), en respectant la hiérarchie santé > régularité > plan Kiprun > complémentaire. Signale tout désaccord avec Kiprun avec l'argument.
7. **Clôture obligatoire** :
   - entrée datée dans `JOURNAL.md` (format de CLAUDE.md) + mise à jour du « Résumé vivant » ;
   - section « 💬 Le mot du coach » du README (3 à 5 lignes) et section « 🩹 Santé » si besoin ;
   - `uv run scripts/build_readme.py` ;
   - mise à jour de `athlete/` ou `plans/` si un fait nouveau est apparu.
