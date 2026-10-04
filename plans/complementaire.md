# Programme complémentaire (vélo · renfo · mobilité)

> Construit par le coach **à la demande d'Arthur**, autour du plan Kiprun (qui reste prioritaire).
> Rien n'est actif tant qu'Arthur ne l'a pas validé. Chaque séance planifiée est aussi ajoutée
> à `data/planned_manual.csv` (source `coach`) pour apparaître dans le README et les bilans.

## Statut

**Programme actif : « Prévention semi »** (validé par Arthur le 03/10/2026).

## Programme « Prévention semi » · du 05/10 au 22/11/2026 · statut : actif

**Objectif** : rendre les tibias, chevilles et genoux plus solides pour arriver en bonne santé au semi du 22/11 (douleur au tibia
le 03/10, genoux sensibles sans échauffement, chevilles sensibles), entretenir le haut du corps, et installer le vélo 1x/semaine
(utile pour le triathlon visé ensuite). 7 semaines = familiarisation et robustesse ; le bloc de force lourde viendra après le semi.
**Validé par Arthur le** : 03/10/2026. **Contraintes** : aucun matériel, 20-25 min par séance, vélo de route, 3 sorties course/sem
à jours variables.

### Placement dans la semaine type

| Lu | Ma | Me | Je | Ve | Sa | Di |
|---|---|---|---|---|---|---|
| repos | Kiprun séance clé **+ 🏋️ A** (après) | repos | Kiprun **+ 🏋️ B** (après) | 🚴 vélo Z2 | repos | Kiprun sortie longue |

Règles si les jours bougent : **A** le jour de la séance dure, après la course · **B** au plus tard 48 h avant la sortie longue ·
**vélo** un jour sans course, jamais la veille de la sortie longue, au moins 24 h avant une séance clé.

### Progression

| Semaine | Dates | Renfo | Vélo | Note |
|---|---|---|---|---|
| S1 | 05/10 → 11/10 | A + B, 2 séries, RIR 3-4 | 45-60 min Z2 | Tibia : test de saut avant chaque sortie ; 7 × 400 du 08/10 → footing facile conseillé |
| S2 | 12/10 → 18/10 | A + B, 2 séries, RIR 3, mollets sur 1 pied | 45-60 min Z2 | |
| S3 | 19/10 → 25/10 | A + B, 3 séries, RIR 2 ; pogo 2 × 10 si 2 sem. sans douleur | 60-75 min Z2 | |
| S4 | 26/10 → 01/11 | A + B, 3 séries ; sac à dos lesté si facile ; pogo 3 × 10 | 60-75 min Z2 | |
| S5 | 02/11 → 08/11 | A + B, dernière semaine pleine | 60-75 min Z2 (ven. 06/11) | Sortie longue 17 km le 08/11 |
| S6 | 09/11 → 15/11 | **A allégé seulement** (mar. 10/11), pas de sauts | ≤ 60 min Z2 (mer. 11/11) | Affûtage |
| S7 | 16/11 → 22/11 | Activation 10 min facultative (mar. 17/11), rien dès le 19/11 | 20-30 min Z1 facultatif (mer. 18/11) | 🏁 Semi dim. 22/11 |

### Règles pour progresser / alléger

- **On progresse** si toutes les séries sont faites avec les reps en réserve visées, **aucune courbature au-delà de 48 h** et aucune
  douleur le lendemain matin.
- **On allège** (2 séries, ou séance B sautée) si jambes lourdes le jour de la sortie longue, tibia > 3/10, ou séance Kiprun dégradée.
- **La course passe avant le renfo**, toujours : en cas de conflit, on raccourcit ou on décale le renfo.
- **Tibia** : test de 10 sauts sur une jambe avant chaque sortie ; douleur → vélo facile à la place. Pas de sauts dans le renfo
  avant 2 semaines sans douleur. Douleur sur un point précis de l'os → arrêt et médecin.

### Séances

- 🏋️ [Renfo A · Jambes solides](renfo/prevention-A.md) (22-25 min)
- 🏋️ [Renfo B · Haut du corps + hanches + pieds](renfo/prevention-B.md) (21-23 min)
- 🚴 **Vélo endurance Z2** : 45-75 min sur le plat, conversation possible en phrases complètes (RPE 4-5/10), 85-95 rpm, assis et
  petit braquet en côte. Pas une séance d'intensité (la sortie du 29/09 était à 55 % en Z3-Z4 : trop dur pour ce rôle).
  Peut remplacer une sortie facile si le tibia fait mal ; ne remplace jamais la sortie longue.

Séances datées : `data/planned_manual.csv` (source `coach`). Après le semi : 1 semaine de repos relatif, puis bloc de force
(avec matériel ou salle, à discuter) et préparation marathon / triathlon.

## Format d'un programme (à respecter)

```markdown
## Programme « <nom> » · du JJ/MM au JJ/MM · statut : actif | terminé | abandonné

**Objectif** : ce qu'on cherche à améliorer et pourquoi (lien avec le semi / les points faibles).
**Validé par Arthur le** : JJ/MM.

### Placement dans la semaine type
| Lu | Ma | Me | Je | Ve | Sa | Di |
|---|---|---|---|---|---|---|
| repos | Kiprun EF | 🏋️ Renfo A | Kiprun fractionné | repos | 🚴 Vélo Z2 | Kiprun SL |

### Progression
| Semaine | Vélo | Renfo | Mobilité | Note |
|---|---|---|---|---|
| S1 | 45 min Z2 | A (familiarisation, RPE 6) | 10 min | |

### Règles pour progresser / régresser
- On progresse si : …
- On allège si : douleur > 3/10, HRV sous la baseline 3 nuits sur 5, semaine Kiprun chargée…

### Séances
(cartes au format ci-dessous, ou lien vers plans/renfo/<fichier>.md)
```

## Format d'une carte de séance (README et plans/renfo/)

```markdown
#### 🏋️ Renfo A · Force jambes · 35 min
> Quand : le jour d'une séance dure Kiprun, après la course (ou 6 h plus tard). Jamais la veille de la sortie longue.

| Exercice | Séries × reps | Charge / effort | Repos | Consigne clé |
|---|:-:|---|:-:|---|
| Squat goblet | 3 × 6 | RPE 7 (2-3 reps en réserve) | 2 min | Genoux dans l'axe des pieds |

**Progression** : +1 rep par série chaque semaine jusqu'à 8, puis charge + et retour à 6.
```

## Historique des programmes

| Période | Programme | Bilan |
|---|---|---|
| 05/10 → 22/11/2026 | Prévention semi (renfo A/B + vélo Z2) | en cours |
