---
name: programme
description: Créer, ajuster ou arrêter un programme complémentaire au plan Kiprun (vélo 1x/semaine, renforcement, mobilité), sans risque de blessure. À utiliser quand Arthur demande un programme de renfo, de vélo, de prévention ou veut améliorer un point précis.
---

# Créer ou ajuster un programme complémentaire

Le plan Kiprun reste la colonne vertébrale. Le programme complémentaire s'y adapte, jamais l'inverse.

1. **Comprendre la demande** : objectif (quoi améliorer et pourquoi), matériel (maison, élastique, haltères, salle), vélo dispo (route, home trainer), créneaux, temps par séance, douleurs ou antécédents. Pose les questions manquantes avant de proposer quoi que ce soit (regarde d'abord `athlete/profil.md`).
2. **Lire** : `plans/kiprun.md` + `uv run scripts/report.py` (semaines S et S+1, charge actuelle), `knowledge/renforcement.md`, `knowledge/velo-cross-training.md`, `knowledge/charge-blessures.md`, et `knowledge/semi-marathon.md` si on approche d'une course (affûtage).
3. **Concevoir** en appliquant les règles d'or de `CLAUDE.md` :
   - placement : renfo les jours durs (après la course), vélo facile sur un jour facile, jamais de charge supplémentaire la veille d'une séance clé ou de la sortie longue ;
   - familiarisation d'abord, progression lente et explicite, critères pour progresser et pour alléger ;
   - affûtage : allègement puis arrêt du renfo avant une course (dates précises) ;
   - une seule nouveauté à la fois si Arthur débute (vélo OU renfo, puis l'autre).
4. **Proposer** à Arthur une version courte (semaine type + progression + 1 carte de séance) et **attendre sa validation**. Explique les choix en 2-3 phrases.
5. **Une fois validé** :
   - écris le programme dans `plans/complementaire.md` (format défini dans ce fichier) et les séances détaillées dans `plans/renfo/<nom>.md` (gabarit `plans/renfo/_gabarit.md`) ;
   - ajoute les séances datées des prochaines semaines dans `data/planned_manual.csv` (source `coach`, sport `bike` / `strength` / `mobility`) ;
   - mets à jour la section « 🟧 Programme complémentaire » du README en cartes lisibles (semaine type + cartes de séances) ;
   - entrée dans `JOURNAL.md` (pourquoi ce programme, ce qui a été décidé) ;
   - `uv run scripts/build_readme.py`.
6. **Ajuster** ensuite à chaque bilan : selon le ressenti, la charge et les douleurs. Toute modification est tracée dans le JOURNAL.
