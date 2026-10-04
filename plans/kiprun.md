# Plan Kiprun Pacer

> Plan principal, adaptatif (Pacer ajuste les séances selon les sorties réalisées).
> **Sources** : séances exportées vers le calendrier Garmin (automatique via `sync.py` → `data/planned.json`)
> et captures d'écran déposées dans `plans/kiprun/captures/` (transcrites ici et dans `data/planned_manual.csv`, source `kiprun`).
> Si Garmin et une transcription donnent une séance le même jour pour le même sport, Garmin l'emporte.

## Infos du plan

| | |
|---|---|
| Objectif dans Pacer | Semi du 22/11/2026 (allure « course » recalée à **5:06-5:18/km** après le test VMA du 19/09, cohérent avec 1h50) |
| Début du plan | ~02/09/2026 (première séance Kiprun visible dans Garmin ; à confirmer avec Arthur) |
| Séances par semaine | **3** (en général mardi, jeudi, dimanche à partir d'octobre) |
| Phase actuelle | Spécifique (allure course + VMA courte + sortie longue avec bloc à allure semi) |
| Sortie longue max prévue | **17 km le 08/11** (puis 13 km, et affûtage à partir du 10/11) |
| Export vers Garmin | ✅ **Tout le plan jusqu'au 21/11 est dans le calendrier Garmin** (vérifié le 03/10/2026) : récupération automatique, pas besoin de captures |

> Évolution notable : début septembre, l'allure « course » de Pacer était 5:36-5:50/km (≈ 2h00). Après le **test VMA du 19/09**,
> Pacer l'a recalée à 5:06-5:18/km (≈ 1h50). Les allures d'endurance sont passées de 6:13-6:30 à 5:48-6:03 sur les sorties « endurance ».

## Semaines

> Extrait du calendrier Garmin le 03/10/2026. Pacer adapte le plan : la source à jour reste `data/planned.json` (régénéré à chaque sync)
> et le rapport `scripts/report.py`. Ce tableau sert d'historique lisible et sera rafraîchi aux bilans.

### Semaine du 31/08
| Jour | Séance | Contenu |
|---|---|---|
| Me 02/09 | 2 x 2000m allure spé | Échauffement 25 min @ 6:42-7:02/km · 2 × (2 km @ 5:36-5:50/km + Repos 400 m @ 6:58-7:21/km) · Récup 10 min @ 6:58-7:21/km |
| Ve 04/09 | 11km endurance | 11 km @ 6:13-6:30/km |

### Semaine du 07/09
| Jour | Séance | Contenu |
|---|---|---|
| Lu 07/09 | 1 h endurance | 60 min @ 6:13-6:30/km |
| Je 10/09 | 4 x 600m (R=200m) | Échauffement 30 min @ 6:42-7:02/km · 4 × (600 m @ 4:30-4:39/km + Repos 200 m @ 6:58-7:21/km) · Récup 10 min @ 6:58-7:21/km |

### Semaine du 14/09
| Jour | Séance | Contenu |
|---|---|---|
| Lu 14/09 | 13km endurance | 13 km @ 6:13-6:30/km |
| Je 17/09 | 2 x 3000m allure de course | Échauffement 25 min @ 6:42-7:02/km · 2 × (3 km @ 5:36-5:50/km + Repos 500 m @ 6:58-7:21/km) · Récup 10 min @ 6:58-7:21/km |
| Sa 19/09 | Test VMA | Échauffement 30 min @ 6:27-6:46/km · 6 min @ 4:14-4:22/km · Récup 10 min @ 6:27-6:46/km |

### Semaine du 21/09
| Jour | Séance | Contenu |
|---|---|---|
| Me 23/09 | 15 x 1'/1' avec récupération active | Échauffement 30 min @ 6:15-6:33/km · 15 × (1 min @ 5:21-5:34/km + Repos 1 min @ 5:25-5:38/km) · Récup 10 min @ 6:31-6:50/km |
| Ve 25/09 | 45 min footing lent | 45 min @ 6:31-6:50/km |
| Di 27/09 | 13km endurance | 13 km @ 5:48-6:03/km |

### Semaine du 28/09
| Jour | Séance | Contenu |
|---|---|---|
| Me 30/09 | 50 min footing lent | 50 min @ 6:31-6:50/km |
| Je 01/10 | 50 min footing lent | 50 min @ 6:31-6:50/km |
| Sa 03/10 | 2 x 2000m allure spé | Échauffement 25 min @ 6:15-6:33/km · 2 × (2 km @ 5:06-5:18/km + Repos 400 m @ 6:31-6:50/km) · Récup 10 min @ 6:31-6:50/km |

### Semaine du 05/10
| Jour | Séance | Contenu |
|---|---|---|
| Ma 06/10 | 2 x 3000m allure de course | Échauffement 25 min @ 6:15-6:33/km · 2 × (3 km @ 5:06-5:18/km + Repos 500 m @ 6:31-6:50/km) · Récup 10 min @ 6:31-6:50/km |
| Je 08/10 | 7 x 400m (R=1 min) | Échauffement 20 min @ 6:15-6:33/km · 7 × (400 m @ 3:57-4:04/km + Repos 1 min @ 6:31-6:50/km) · Récup 10 min @ 6:31-6:50/km |
| Di 11/10 | 15km endurance | 6 km @ 6:15-6:33/km · 3 km @ 5:06-5:18/km · 6 km @ 6:15-6:33/km |

### Semaine du 12/10
| Jour | Séance | Contenu |
|---|---|---|
| Ma 13/10 | 15KM Progressifs | Échauffement 10 min @ 6:15-6:33/km · 5 km @ 5:36-5:50/km · 5 km @ 5:14-5:26/km · 5 km @ 4:55-5:05/km · Récup 10 min @ 6:31-6:50/km |
| Je 15/10 | 1 h endurance | 60 min @ 5:48-6:03/km |
| Di 18/10 | 15km endurance | 6 km @ 6:15-6:33/km · 3 km @ 5:06-5:18/km · 6 km @ 6:15-6:33/km |

### Semaine du 19/10
| Jour | Séance | Contenu |
|---|---|---|
| Ma 20/10 | 5000m allure course | Échauffement 25 min @ 6:15-6:33/km · 5 km @ 5:06-5:18/km · Récup 10 min @ 6:31-6:50/km |
| Je 22/10 | 55 min endurance | 55 min @ 5:48-6:03/km |
| Di 25/10 | 12km endurance | 12 km @ 5:48-6:03/km |

### Semaine du 26/10
| Jour | Séance | Contenu |
|---|---|---|
| Ma 27/10 | 5 x 1500m 90% VMA (R=2 min) | Échauffement 20 min @ 6:15-6:33/km · 5 × (1.5 km @ 4:22-4:31/km + Repos 2 min @ 6:31-6:50/km) · Récup 10 min @ 6:31-6:50/km |
| Je 29/10 | 8 x 500m (R=200m) | Échauffement 20 min @ 6:15-6:33/km · 8 × (500 m @ 4:03-4:10/km + Repos 200 m @ 6:31-6:50/km) · Récup 10 min @ 6:31-6:50/km |
| Di 01/11 | 16km endurance | 6 km @ 6:15-6:33/km · 3 km @ 5:06-5:18/km · 7 km @ 6:15-6:33/km |

### Semaine du 02/11
| Jour | Séance | Contenu |
|---|---|---|
| Ma 03/11 | 30' actives | Échauffement 20 min @ 6:15-6:33/km · 15 min @ 5:14-5:26/km · 15 min @ 4:55-5:05/km · Récup 10 min @ 6:31-6:50/km |
| Je 05/11 | Footing pyramidal | Échauffement 15 min @ 6:31-6:50/km · 20 min @ 6:01-6:18/km · Récup 10 min @ 6:31-6:50/km |
| Di 08/11 | 17km endurance | 6 km @ 6:15-6:33/km · 4 km @ 5:06-5:18/km · 7 km @ 6:15-6:33/km |

### Semaine du 09/11
| Jour | Séance | Contenu |
|---|---|---|
| Ma 10/11 | 8 x (30"/30") | Échauffement 30 min @ 6:15-6:33/km · 8 × (0:30 @ 3:35-3:41/km + Repos 0:30 @ 6:31-6:50/km) · Récup 10 min @ 6:31-6:50/km |
| Je 12/11 | 13km endurance | 13 km @ 5:48-6:03/km |
| Di 15/11 | 2500m allure SPE | Échauffement 30 min @ 6:15-6:33/km · 2.5 km @ 5:06-5:18/km · Récup 10 min @ 6:31-6:50/km |

### Semaine du 16/11
| Jour | Séance | Contenu |
|---|---|---|
| Ma 17/11 | 8km endurance | 8 km @ 5:48-6:03/km |
| Je 19/11 | 2000m allure SPE | Échauffement 30 min @ 6:01-6:18/km · 2 km @ 5:06-5:18/km · Récup 10 min @ 6:31-6:50/km |
| Sa 21/11 | 20 min footing lent | 20 min @ 6:31-6:50/km |

