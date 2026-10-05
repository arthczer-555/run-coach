# Journal du coach

> **TOUT ce qui s'est passé**, dans l'ordre chronologique : sessions de coaching, ressentis, réponses d'Arthur,
> décisions et leurs raisons, changements de plan, blessures, courses, évolutions du projet.
> Le coach relit le **Résumé vivant** au début de chaque session, puis les dernières entrées si besoin.
> Règles d'écriture : voir `CLAUDE.md` § « Journal ». Archivage : quand ce fichier dépasse ~2000 lignes,
> les années closes partent dans `journal/AAAA.md` (le résumé vivant reste ici, avec un lien).

---

## 📌 Résumé vivant

<!-- Tenu à jour à chaque session. ~40 lignes max. C'est la mémoire de travail du coach. -->

**Mis à jour le** : 2026-10-05 (2 × 2000 m au chaud, tibia revenu à km 2, semaine allégée, règle « 1 qualité/sem » à trancher au bilan)

- **Athlète** : Arthur, 24 ans, 65 kg, Forerunner 165. **Débutant** : court régulièrement depuis ~août, **aucune course officielle**.
  VMA **15 km/h** (test Pacer du 19/09). FC max Garmin 197 = auto-détection, jamais atteinte (max observé 178) → zones FC incertaines.
  Montre **portée la nuit depuis le 03-04/10** (1re nuit : sommeil 7h33, FC repos 47, HRV 79 ms) ; baseline HRV Garmin d'ici ~3 semaines.
- **Objectif** : semi le **22/11/2026**, visé en **1h50** (77 % de VMA ; prédiction Garmin 1:49:42). Jugé ambitieux mais plausible ;
  le risque principal est la blessure. Proposé : A < 1h50 · B < 1h55 bien géré · C finir sans blessure. À réévaluer fin octobre.
- **Après** : marathon, puis triathlon (M puis half), peut-être trail.
- **Plan** : Kiprun Pacer, 3 séances/sem (jours variables), phase spécifique, allure course 5:06-5:18. Tout le plan est dans Garmin.
- **Rugby tous les lundis soir** (+ foot en fin d'entraînement), découvert le 04/10, jamais enregistré dans Garmin : charge intense cachée.
  Règle : **jamais de séance clé le lendemain du rugby** (mardi). Pacer met ses séances clés le mardi → jours à changer.
- **Santé** : 🟠 **tibia** : douleur diffuse le long de l'os le 03/10 (2 × 2000 m, arrêt après 1 rép.), test RAS le 04/10, **revenue le
  05/10 vers km 2** (échauffement), calmée après une pause, séance finie. 2 alertes en 3 jours, plus tôt dans la sortie : à surveiller.
  **Si elle revient à la prochaine sortie → kiné / médecin du sport**, vélo en attendant. Test du tibia avant chaque sortie. Arthur
  l'attribuait au vélo ; le coach pense à la charge (volume de septembre +72 % + rugby invisible + densité d'intensité).
  Genoux (si pas échauffé) et chevilles : récurrent léger.
- **Diagnostic « jambes » (03/10)** : le cœur a de la marge à allure semi (FC ~135-150 au frais), ce sont les jambes qui limitent
  (endurance musculaire, mollets, tissus). Moteur VDOT ~45 vs objectif 40. Cadence fixe ~167, tout passe par la foulée. Chaleur : +1,4 bpm/°C.
  Leviers : volume facile + SL par paliers, blocs Kiprun à allure semi, renfo A (mollets), cadence +3-5 % plus tard si tibia calme.
- **Programme complémentaire** : vélo 1x/sem voulu (facile !) ; **renfo de prévention demandé** (tibia, chevilles, genoux + haut du corps).
  ✅ **Programme « Prévention semi » actif** (validé le 03/10, 05/10 → 22/11) : renfo A (jambes, après la séance clé) + renfo B
  (haut du corps + hanches + pieds, ≥ 48 h avant la sortie longue), sans matériel, 2 × 20-25 min/sem + vélo route Z2 1x/sem.
  Détail : `plans/complementaire.md`, `plans/renfo/prevention-A.md` / `-B.md` ; séances datées dans `data/planned_manual.csv`.
- **Intensité** (analyse du 05/10) : depuis juillet 45 % Z1-2 / 43 % Z3 / 12 % Z4 (zones Garmin sur FCmax 197, Z3 = 138-158). Footings
  lents OK (126-132 bpm). Problème = **densité** : 7 sorties sur 13 en qualité depuis le 01/09 + rugby. Pacer met 2 qualités + bloc allure
  semi dans la SL chaque semaine : trop pour lui aujourd'hui. Volume du plan : OK.
- **Proposé le 05/10 (en attente)** : 1 seule qualité/sem (allure semi/seuil Pacer à 5:13-5:18, jamais plus vite), VMA → footing + lignes
  droites, SL en facile (bloc allure semi après 2 sem. sans douleur), « endurance » au test de la parole (≤ ~150 bpm au frais), rugby = la
  2e séance dure, séances clés au frais. Décision 1h50 / 1h55 fin octobre sur un test au frais.
- **Semaine 05-11/10 (allégée, décidé le 05/10)** : Lu 2 × 2000 m + foot tranquille le soir (pas le rugby) · Ma repos + test tibia ·
  Me renfo A sans saut · Je footing facile 30-35 min (au lieu de 7 × 400 m) + renfo B · Ve-Sa repos (pas de vélo) · Di sortie longue
  **10 km max tout en facile** (au lieu de 15 km avec 3 km allure semi). ~24 km au lieu des ~35 de Pacer. Tibia douloureux → vélo facile.
- **En attente de validation** : semaine type Lu rugby · Ma repos · Me clé + renfo A · Je renfo B · Ve footing · Sa repos · Di SL ;
  vélo retiré jusqu'au semi. Puis mettre à jour `plans/complementaire.md`, `data/planned_manual.csv`, README.
- **Prochaine étape** : réponses d'Arthur (tibia : jambe, /10, bande ou point ; rugby ce soir et jusqu'au semi ; souffle /10 et jambes /10
  sur la rép. 2 ; priorité 1h50 ou arriver en forme), test du tibia le 06/10, règle « 1 qualité/sem » et semaine type à trancher au bilan du 11-12/10 (choix d'Arthur : aviser la semaine prochaine).

---

## Entrées

### 2026-10-03 · Création du projet et choix d'architecture

**Contexte.** Arthur veut un coach running perso qui tourne en local dans Claude Code. Sa demande d'origine :
- lui poser des questions ici, en local ;
- à chaque question, récupérer toutes ses séances (il pensait à **Strava**) ;
- récupérer son programme **Kiprun** ;
- faire un bilan de la semaine en cours, de la précédente et de la suivante, voir aussi ses **sorties vélo**, lui demander
  comment il se sent et pourquoi il a fait ci ou ça, le conseiller, répondre sur le renfo et ses objectifs ;
- être documenté comme un expert (recherche de doc sur le coaching running) ;
- **tout documenter** : instructions dans `CLAUDE.md`, historique complet dans un autre fichier (celui-ci), même si le dossier vit 2 ans ;
- un **README soigné** qu'il consulte comme un dashboard : graphs, progression, achievements, programmes ;
- pouvoir créer un programme en plus de Kiprun (renfo, vélo 1x/semaine) sans blessure. Pour le renfo : « pour l'instant fais rien
  mais il doit être capable ».

**Réponses d'Arthur pendant le cadrage.**
- Montre : **Garmin** (course et vélo enregistrés avec, vélo via montre ou compteur Garmin).
- README : consulté sur un **repo GitHub privé** (lisible sur mobile).
- Kiprun : il utilise l'app **Kiprun Pacer** et les séances sont **envoyées sur sa montre**.
- Objectif : **semi le 22/11/2026, visé en 1h50**. Il a demandé s'il existe une API Kiprun pour tout récupérer.

**Recherches et constats.**
- **Strava** : la politique API en vigueur depuis le **01/06/2026** (§5.3) interdit d'utiliser les données Strava « in connection with
  the development, training, evaluation, or operation of any AI Application », y compris l'ingestion dans une fenêtre de contexte.
  Seule exception : le **MCP Strava officiel**, réservé aux abonnés payants (§3.5). Les serveurs MCP tiers sont interdits (§5.16).
  Vérifié directement sur https://www.strava.com/legal/api_policy le 2026-10-03.
- **Kiprun Pacer** : pas d'API publique, pas d'export CSV/ICS. Pacer peut **exporter une séance vers le calendrier Garmin**
  (Garmin Connect → Applications connectées → Decathlon → autoriser « Entraînement »). À tester : export de la séance du jour seulement,
  ou de plusieurs jours ? Les cibles d'allure sont-elles conservées ?
- **Garmin** : lib Python non officielle `garminconnect` 0.3.17 (login façon appli mobile, MFA, jetons dans `~/.garminconnect/`).
  Donne activités, laps, zones FC, RPE saisi sur la montre, HRV, sommeil, FC repos, Body Battery, Training Readiness, VO2max,
  prédictions de course, records, séances planifiées du calendrier. Peut casser quand Garmin change son login.

**Décisions (validées par Arthur).**
1. **Source de données = Garmin Connect** (pas Strava). Raison : conformité + Garmin est la source d'origine et donne beaucoup plus
   (HRV, sommeil, prédictions, calendrier Kiprun).
2. **Kiprun** : sync automatique du calendrier Garmin ; en secours, captures d'écran du plan dans `plans/kiprun/captures/`,
   transcrites par le coach dans `plans/kiprun.md` et `data/planned_manual.csv`.
3. **Stack** : Python + uv, scripts dans `scripts/`, données normalisées dans `data/` (brut Garmin dans `data/raw/`, gitignored).
4. **Sync automatique** par un hook Claude Code (`UserPromptSubmit`) : au plus une fois toutes les 30 minutes, jamais bloquant.
5. **README dashboard** : blocs générés par `scripts/build_readme.py` (objectif, semaine, 7 graphs SVG clair/sombre, records,
   achievements, totaux) + sections écrites par le coach (mot du coach, programmes, santé).
6. **Repo GitHub privé** : `git init` fait, aucun commit ni push sans demande explicite d'Arthur.
7. **Programmes** : la capacité est construite (format, skill `/programme`, base de connaissances renfo et vélo), **aucun programme
   généré** tant qu'Arthur ne le demande pas.

**Ce qui a été construit.**
- Scripts : `garmin_login.py`, `sync.py` (incrémental, `--full`, `--hook`, `--normalize-only`), `report.py` (bilan S-1/S/S+1),
  `checkin.py` (ressentis), `build_readme.py` ; package `scripts/coach/` (normalisation, métriques, achievements, graphs).
- Base de connaissances `knowledge/` (3 agents de recherche, **210 sources**, DOI contrôlés ; contre-vérification par sondage de
  11 DOI via Crossref, tous réels) : méthode et intensité, semi-marathon (allures 1h50, grille « réaliste ? », trame 7 semaines
  à confronter au plan Kiprun), charge et blessures, récupération, renforcement (bibliothèque d'exercices), vélo. Règles d'or
  reprises dans `CLAUDE.md` § 6.
- Points incertains signalés par la recherche : seuil de douleur 3/10 = consensus de terrain (Silbernagel tolérait 5/10 pour une
  tendinopathie suivie) ; Nielsen 2014 non significatif ; Frandsen 2025 observationnel ; prédicteur Garmin sans validation
  indépendante ; équivalences vélo/course = consensus très individuel.
- `CLAUDE.md` (instructions du coach), `athlete/` (profil, objectifs), `plans/` (Kiprun, complémentaire, gabarit renfo),
  skills `/bilan` et `/programme`.
- Testé de bout en bout sur des données factices au format Garmin (sync normalisée, rapport, graphs, README idempotent).
  Pas encore testé sur les vraies données : il faut le login Garmin d'Arthur.

**Reste à faire.**
- Arthur : login Garmin (`uv run scripts/garmin_login.py` dans un terminal), export des séances Kiprun vers Garmin, capture du plan.
- Coach : `sync.py --full`, vérifier les parseurs sur les vraies réponses Garmin (sommeil, HRV, records, calendrier, unité du seuil
  lactique), onboarding, premier bilan.

### 2026-10-03 · Projet · Connexion Garmin, première sync complète, corrections

- **Contexte** : Arthur s'est connecté à Garmin (`garmin_login.py`). Le hook a fait une 1re sync (6 semaines, 16 activités), puis
  `sync.py --full` a rapatrié tout l'historique : **39 activités depuis le 06/08/2025** (30 course, 5 natation, 2 vélo, 1 renfo, 1 autre).
- **Découvertes** :
  - **Kiprun Pacer exporte tout le plan jusqu'au 21/11 dans le calendrier Garmin** (46 séances visibles, cibles d'allure incluses).
    Les captures d'écran deviennent inutiles. Plan transcrit dans `plans/kiprun.md`.
  - Montre : **Forerunner 165**. Pas de training load ni de training status Garmin. Une seule nuit mesurée (15/07) : la montre n'est
    pas portée la nuit, donc la « FC de repos » Garmin (85-110 bpm) était en fait la FC minimale des séances.
  - Garmin : 24 ans, 171 cm, 65 kg, FCmax 197, VO2max 55,4, prédiction semi 1:49:42. Records pris à l'entraînement (pas de course).
- **Corrections du code** : doublons du calendrier (mois qui se chevauchent) ; FC de repos et Body Battery gardées seulement les jours
  avec une nuit mesurée ; **TRIMP d'Edwards** (minutes en zone × numéro de zone) comme charge quand la montre n'en calcule pas ;
  profil lu via `get_user_profile` ; appareil enregistré ; natation reconnue ; section « Forme » du rapport explicite sans données de nuit ;
  graph d'efficience affiché seulement à partir de 10 sorties faciles.
- **README** régénéré sur les vraies données (5 graphs : volume, prédiction, intensité, charge, régularité).
- **À suivre** : onboarding et premier bilan (points d'attention listés dans le résumé vivant).

### 2026-10-03 · Projet · Correction du prénom

- **Correction** : l'athlète s'appelle **Arthur**, pas Arthur. Prénom corrigé partout (CLAUDE.md, skills, journal, athlete/, plans/,
  knowledge/, `report.py`), y compris dans les entrées précédentes à sa demande explicite.

### 2026-10-03 · Bilan · Onboarding et premier bilan (S-1 / S / S+1)

- **Contexte** : premier bilan après la sync complète. S-1 : 30,8 km en 3 sorties + 1 vélo, 3/3 séances Kiprun faites, 46 % du temps en Z1-Z2.
  S : 10,9 km en 2 sorties + 1 vélo (1h29, 55 % en Z3-Z4) ; 2 × 2000 m du 03/10 arrêté après 1 répétition (5:07 et 5:13/km), ressenti « mal ».
  Charge aiguë/chronique (TRIMP) 1,33. Volume : 17,5 → 30,1 km/sem entre les semaines du 07/09 et du 14/09 (+72 %).
- **Réponses d'Arthur** :
  1. Court « depuis août en gros », jamais fait de course.
  2. Petites douleurs aux genoux quand il ne s'échauffe pas assez, aux chevilles de temps en temps. **Aujourd'hui : douleur tout le long du
     tibia**, qu'il attribue à la sortie vélo trop intense (29/09).
  3. Ne porte pas la montre la nuit, « pourquoi pas ».
  4. FC max 197 = valeur donnée par Garmin d'après ses activités.
  5. VMA Pacer : **15 km/h**.
  6. 3 sorties/sem, dispos variables ; veut ajouter du vélo 1x/sem.
  7. Après le semi : marathon, puis triathlon (M puis half), peut-être trail.
  8. 2 × 2000 m : arrêt à cause du tibia ; jambes lourdes cette semaine ; pense sauter « la séance de demain » pour récupérer.
  9. Footing du 30/09 : séance exportée puis déplacée dans Pacer (doublon fantôme dans Garmin, désormais masqué via
     `data/planned_manual.csv`, source `annule`). Le 01/10 : footing raccourci (33 min au lieu de 50), mal à la cheville et fatigué.
  10. Ressenti : jambes lourdes, fatigué, douleur tibia (check-in enregistré : fatigue 4, courbatures 4, douleur à noter).
  - **Demande** : ajouter du renfo pour éviter les douleurs (tibia, cheville, genou) et garder un peu de muscle au haut du corps.
- **Analyse du coach** :
  - Tibia : douleur diffuse le long de l'os = tableau compatible avec un **syndrome de stress tibial médial** (MTSS, « périostite »),
    blessure « de distance » typique du débutant [Nielsen 2014, Winters 2018]. Le vélo n'a pas d'impact : il peut expliquer les jambes
    lourdes, pas vraiment le tibia. Cause probable : la **hausse de volume de septembre** sur des tissus qui ne courent que depuis l'été
    (le cardio, VMA 15, progresse plus vite que les os et les tendons). Point précis, douleur au saut, à la marche ou la nuit = drapeau rouge
    (fracture de fatigue) → arrêt et médecin [Warden 2014].
  - Intensité : beaucoup de Z3, mais zones FC peu fiables (FC max 197 jamais approchée). Conclusion pratique : footings au **test de la
    parole**, quitte à courir plus lentement que la fourchette Kiprun « endurance » (5:48-6:03).
  - 1h50 : plausible physiologiquement (77 % de VMA), mais premier semi, débutant, 13 km max. Objectif A/B/C proposé.
- **Décisions / conseils (provisoires, selon le triage du tibia)** : repos le 04/10 (Kiprun n'a rien de prévu avant mardi) ; mardi
  2 × 3000 m seulement si marche et saut unipodal indolores, sinon 45 min de vélo facile ; jeudi 7 × 400 m → facile cette semaine ;
  sortie longue du 11/10 plafonnée à 13 km ; vélo 1x/sem en Z1-Z2 (45-60 min) ; porter la montre la nuit ; renfo de prévention
  2 × 20-25 min/sem, sans pliométrie tant que le tibia n'est pas indolore.
- **À suivre** : triage du tibia (note, localisation, saut, nuit), matériel et durée pour le renfo, validation du programme, test de
  réalisme 1h50 fin octobre.

### 2026-10-03 · Programme · Proposition renfo de prévention + vélo

- **Contexte** : réponses d'Arthur : **aucun matériel**, OK pour **20-25 min par séance**, **vélo de route**. Tibia : plus de douleur
  au repos, douleur seulement pendant la course du matin, « occasionnelle ».
- **Proposition** (programme « Prévention semi », 05/10 → 22/11) : séance A « jambes solides » (mollets jambe tendue et genou fléchi,
  tibial raises, fente bulgare, pont fessier unipodal, équilibre, gainage) après la 1re séance clé Kiprun ; séance B « haut du corps +
  hanches + pieds » (pompes, rowing sous une table, dips sur chaise, step-down, abduction de hanche, isométrie mollet, dead bug, short foot)
  après la 2e sortie, à ≥ 48 h de la sortie longue ; vélo route 1x/sem 45-75 min en Z2 un jour sans course, pas la veille de la sortie longue.
  Familiarisation S1-S2 (2 séries, 3-4 reps en réserve), développement S3-S5, une seule séance allégée en S6 (dernière le 12/11, J-10),
  activation facultative le 17/11, rien à partir du 19/11. Pas de sauts avant 2 semaines sans douleur au tibia.
- **Pourquoi** : MTSS probable + genoux et chevilles sensibles → priorité mollets (soléaire), hanches, contrôle du genou et cheville
  [knowledge/renforcement.md] ; 7 semaines = familiarisation et robustesse, le bloc de force lourde viendra après le semi (avec du matériel).
  Le renfo ne remplace pas la gestion du volume, facteur n°1 [Wu 2024].
- **À suivre** : validation d'Arthur, puis écriture du programme (plans/, data/planned_manual.csv, README).

### 2026-10-03 · Programme · « Prévention semi » validé et publié

- **Contexte** : Arthur valide la proposition (« oui go ») et demande le programme dans le README avec les séances de renfo et de course.
- **Fait** :
  - `plans/complementaire.md` (programme actif, semaine type, progression S1-S7, règles), `plans/renfo/prevention-A.md` et
    `prevention-B.md` (fiches complètes : échauffement, séance, progression, régressions).
  - 19 séances datées dans `data/planned_manual.csv` (source `coach`) : renfo A les mardis, B les jeudis, vélo les vendredis ;
    S6 : A allégé le 10/11 et vélo le 11/11 ; S7 : activation facultative le 17/11 et vélo facultatif le 18/11.
  - README : nouveau bloc automatique **« 📆 Calendrier jusqu'au semi »** (grille semaine par semaine qui fusionne Kiprun, renfo et
    vélo, régénérée à chaque sync), section « 🟧 Programme complémentaire » avec semaine type, progression et cartes des séances A, B et vélo.
- **Rappels donnés** : test de 10 sauts sur une jambe avant chaque sortie ; lancer l'activité « Musculation » sur la montre ;
  la course passe avant le renfo ; 7 × 400 m du 08/10 → footing facile conseillé (tibia).
- **À suivre** : courbatures après la 1re séance A (mardi 06/10), tibia, ressenti du vélo Z2.

### 2026-10-03 · Programme · Explications des exercices réécrites

- **Contexte** : Arthur ne comprenait pas quoi faire avec les consignes courtes des tableaux.
- **Fait** : chaque exercice des séances A et B (plus le pogo) a maintenant un pas à pas (départ, mouvement, ce qu'il doit sentir,
  erreur à éviter, version plus facile ou plus dure) et un lien de recherche vidéo YouTube. Ajouté dans `plans/renfo/prevention-A.md`,
  `prevention-B.md` et dans le README (blocs dépliables « 📖 Comment faire chaque exercice » sous chaque carte). L'exercice 2 de la
  séance A se fait désormais **face au mur** (plus simple que dos au mur).
- **À retenir pour le coach** : Arthur débute en renfo. Toujours décrire un exercice en pas à pas, pas seulement en consigne courte.

### 2026-10-03 · Question · Cœur ou jambes : étude des séances depuis juillet

- **Contexte** : Arthur sent que « c'est les jambes » qui doivent progresser : ce matin, sur le 2 × 2000 m (1 seule répétition faite, tibia),
  FC basse à allure course (5:07 puis 5:13/km, FC 142 puis 135) mais dur dans les jambes. Demande : ce que ça signifie, comment le travailler,
  avec une étude de ses séances. Analyse de 121 laps de 1 km (juillet → 03/10), FC, température montre, cadence, foulée, temps de contact.
- **Analyse du coach** :
  - **Le cœur a de la marge à allure semi** : ~135-150 bpm au frais (17/08 km 3-5 à 5:12-5:17 : 145-149 ; 14/09 dernier km à 5:06 : 147 ;
    03/10 : 135-142), soit ~80-84 % de la FC max observée (178). La FC de ce matin est 6 bpm sous son modèle, dans sa variation habituelle :
    pas un signal de fatigue exploitable seul (mais FC basse + jambes lourdes peut être de la fatigue [Le Meur 2013]).
  - **La chaleur explique la plupart des FC hautes** : +1,4 bpm par °C à allure égale (régression FC ~ vitesse + température, R² 0,51).
    22/07, 07/09, 23/09 (27-34 °C) = jours où le cardio montait. Le 22/11 il fera frais : le cœur ne sera pas le facteur limitant.
  - **Les jambes lâchent avant le cœur** : test VMA 19/09 (FC max 168 alors qu'il est déjà monté à 177-178, allure 3:54 → 4:00) ;
    02/09 (2e fraction à 6:00 pour une cible 5:36-5:50, FC 148-156) ; 17/08 (cassure au km 6, foulée 111 → 90 cm, FC qui baisse).
  - **Moteur en avance sur le châssis** : test 6 min = VDOT ~45 (semi théorique ~1h40) contre 1h50 visé (VDOT 40,4). VO2max progresse vite,
    l'endurance musculaire (mitochondries, capillaires), les tendons et les os prennent des mois [Joyner & Coyle 2008, Holloszy & Coyle 1984, Bohm 2015].
  - **Mécanique** : cadence quasi fixe (165-170 pas/min de 6:50 à 3:54/km), toute l'accélération vient de la foulée (+10 cm par km/h :
    92 cm en footing, ~115 cm à allure semi). Stratégie normale à ces vitesses mais poussée à l'extrême : ce sont les mollets qui paient
    [Dorn 2012], et une foulée longue charge plus le tibia par appui [Edwards 2009, modèle].
  - **Ce matin en plus** : jambes pré-fatiguées (13 km à 5:52 le 27/09, vélo 1h29 avec 459 m D+ et 18 min en Z4 le 29/09, check-in fatigue 4 et
    courbatures 4, tibia). La sensation mélange manque de capacité et fatigue.
- **Conseils** : (1) récupérer d'abord (plan de la semaine inchangé) ; (2) volume facile régulier et sortie longue par paliers = levier n°1 ;
  (3) blocs Kiprun à allure semi, viser le milieu de la fourchette (5:12) et la régularité ; (4) renfo A, mollets en priorité, puis force lourde
  + pliométrie après le semi ; (5) plus tard, si tibia calme : +3-5 % de cadence à allure semi (~172-175 pas/min), un seul changement à la fois ;
  vélo à plat, vélocité ≥ 85 rpm. Jour J : courir à l'allure, pas à la FC (une FC basse n'autorise pas à accélérer).
- **Savoir ajouté** : `knowledge/cardio-vs-jambes.md` (7 sources, DOI vérifiés Crossref) ; faits stables dans `athlete/profil.md`.
- **À suivre** : réponses d'Arthur (type de sensation, où, frais ou fatigué, repas et sommeil avant la séance) ; refaire l'étude fin octobre
  (FC à allure semi, cadence, tenue des blocs de 5 km et des 15 km progressifs) ; décision cadence au bilan du 11-12/10.

### 2026-10-04 · Question · Prochaine sortie et retour sur les jambes

- **Contexte** : Arthur court le 05 ou le 06/10 et fera un retour sur l'état de ses jambes.
- **Conseil** : de préférence le mardi 06/10 (le 2 × 3000 m prévu, 3 jours après le 03/10, renfo A le même jour), seulement si le test de
  saut est indolore. Retour demandé : souffle /10 et jambes /10 séparément pendant les fractions, type et lieu de la sensation, tibia
  pendant et le lendemain matin, sommeil et repas avant la séance.
- **Ajout** : Arthur a **rugby lundi soir (05/10)**, jamais signalé jusqu'ici et absent de Garmin. Un 2 × 3000 m le mardi, moins de 24 h
  après sprints, appuis et contacts, avec un tibia sensible : non. Proposition en attente de validation : rugby lundi (si saut indolore,
  stop si tibia > 3/10), repos mardi, 2 × 3000 m + renfo A mercredi, renfo B jeudi, footing facile vendredi (à la place du 7 × 400 m),
  sortie longue dimanche plafonnée à 13 km, **pas de vélo cette semaine** (le rugby le remplace). Questions posées : rugby chaque semaine ?
  depuis quand ? joué le 28/09 (ce qui expliquerait en partie les jambes lourdes et le tibia) ?
- **Option lundi** (question d'Arthur) : 2 × 3000 m lundi matin ou midi (≥ 6 h avant le rugby, repas entre les deux), rugby le soir, puis
  repos mardi ; renfo A mercredi, footing facile + renfo B jeudi, sortie longue dimanche ≤ 13 km. Jugée **plutôt meilleure** que mercredi :
  séance clé sur jambes fraîches au lieu de jambes courbaturées 40 h après le rugby, puis 2 jours pour récupérer. Contrepartie : jambes
  entamées au rugby (risque musculaire), et grosse journée pour le tibia. En attente : validation, et rugby hebdomadaire ou non, joué le 28/09 ?
- **1re nuit avec la montre (03-04/10)** : coucher 23:57, lever 08:12, 7h33 de sommeil (profond 1h29, paradoxal 1h04, 1 réveil), score 84,
  FC repos 47 (réglage Garmin 50 ; 55 la seule autre nuit, le 15/07), HRV 79 ms (64 le 15/07), Body Battery +74. Nuit de bonne récupération
  après le jour de repos, mais **une nuit seule ne s'interprète pas** : il faut ~3 semaines pour une baseline. Lecture du sommeil et de la
  HRV par la sync vérifiée sur les vraies données (point « à vérifier » de CLAUDE.md § 13).
- **Test du tibia expliqué** (Arthur ne savait pas ce que c'était) : palpation du bord interne (bande ou point précis), marche + escalier,
  10 sauts sur une jambe en comparant les deux côtés. Vert → course ; douleur aux sauts → vélo (kiné/médecin si > 3 jours) ; point précis,
  marche, nuit → arrêt et médecin. Pas à pas ajouté dans le README (🩹 Santé), qui harmonise la règle (avant : « douleur au saut → médecin »
  dans Santé, « → vélo » dans le programme). À demander : quelle jambe, résultat du test ce matin.
- **Test du tibia du 04/10 au matin : RAS** (palpation, marche, sauts indolores). Check-in enregistré (douleur 0). Tibia passé en 🟡 :
  feu vert pour courir lundi, règle des 3/10 pendant la séance et test à refaire avant chaque sortie.
- **Réponses d'Arthur** : la séance clé sera lundi s'il a le temps, sinon mardi ou mercredi selon ses sensations. **Rugby tous les lundis
  soir, avec du foot en fin d'entraînement.**
- **Analyse** : mardi = le pire choix (moins de 24 h après sprints et appuis, courbatures qui arrivent à 24-48 h : la sensation du mardi matin
  trompe). Règle donnée : lundi (≥ 6 h avant le rugby) sinon mercredi, jamais mardi. Le rugby hebdomadaire est une séance intense invisible
  dans Garmin : la charge de septembre était plus haute que les +72 % calculés (course seule), ce qui renforce l'hypothèse « charge » pour le
  tibia. Pacer place ses séances clés le mardi (06, 13, 20/10…) : chaque semaine, le lendemain du rugby.
- **Proposition (en attente de validation)** : semaine type Lu rugby · Ma repos · Me séance clé Kiprun + renfo A · Je renfo B ·
  Ve footing Kiprun · Sa repos · Di sortie longue ; vélo retiré jusqu'au semi (le rugby fait office de sport complémentaire) ; jours à changer
  dans Pacer ; enregistrer le rugby sur la montre.

### 2026-10-05 · Séance clé · 2 × 2000 m au chaud, tibia de retour, zones et densité du plan

- **Contexte** : séance à 14:47 (Caluire), 9,0 km en 54:24, RPE 6. Prévu 2 × 3000 m allure course, fait **2 × 2000 m**. Laps auto au km :
  échauffement 6:12 · 6:12 · **6:38 (FC 122 : pause tibia)** · 6:33 ; rép. 1 **5:14 / 5:08** (FC 153 / 161) ; rép. 2 estimée ~5:20-5:30
  (km 8 à 5:23, FC 164, max 166 ; laps auto non alignés sur les fractions). Température montre 27-31 °C. Semaine précédente : 10,9 km.
- **Ressenti / réponses d'Arthur** : a allégé à 2 × 2000 m parce qu'il faisait très chaud et qu'il avait levé le pied la semaine dernière.
  Vers 2 km, **même douleur le long du tibia**, qui monte doucement ; il s'est arrêté, a repris, ça allait mieux. 2e 2000 m dur, n'a pas
  tenu l'allure, a ralenti. Questions : court-il trop en zones 3-4, devrait-il courir plus en zone 1 ? Le programme est-il trop gros pour
  son objectif et son niveau ?
- **Analyse du coach** :
  - Séance : rép. 1 pile dans la cible (5:11 de moyenne). Même allure le 03/10 à 18-19 °C : FC 135-142 ; aujourd'hui 153-161 à 28 °C
    → +18-20 bpm, cohérent avec l'effet chaleur mesuré (+1,4 bpm/°C). Rép. 2 à 164-166 bpm (~92 % de la FC max observée) = effort
    seuil / 10 km, pas semi. Ralentir était la bonne décision ; ce n'est pas un manque de niveau.
  - Tibia : **2e alerte en 3 jours**, même tableau diffus, apparue **plus tôt** (km 2 à l'échauffement contre km 5 le 03/10) mais calmée
    après une pause et séance terminée. Toujours compatible avec un MTSS ; une douleur qui arrive « de plus en plus tôt » est un signe à
    surveiller [Warden 2014]. Rugby prévu le soir même (~4 h après).
  - Zones : depuis juillet, **45 % Z1-2 / 43 % Z3 / 12 % Z4** (zones Garmin sur FCmax 197 jamais atteinte : Z3 = 138-158 bpm, à cheval
    entre facile et modéré). Les footings lents sont bien faits (126-132 bpm). Garmin Z1 (< 118 bpm) ≈ marche : pas une cible.
    Le vrai problème est la **densité** : depuis le 01/09, **7 sorties sur 13** en qualité ou test, sorties « endurance » Pacer
    (5:48-6:03) à ~145-150 bpm, et le **rugby du lundi** que Pacer ne voit pas. Environ 1 séance sur 2 est dure, contre 1 sur 4-5 visé.
  - Plan : le **volume** est raisonnable (25-35 km/sem, sortie longue max 17 km, minimum utile pour un semi [Fokkema 2020]). La **densité
    d'intensité** est trop forte pour lui aujourd'hui : chaque semaine 2 séances dures + bloc allure semi dans la sortie longue (13/10 :
    15 km progressifs finis à 4:55-5:05 ; semaine du 26/10 : 5 × 1500 m à 90 % VMA + 8 × 500 m). Plan pensé pour un coureur avec une base,
    sans rugby. 1h50 : moteur OK (VMA 15, 5:11 à 135-142 bpm au frais), châssis pas encore (sortie longue max 13 km, ~24 km/sem sur les
    3 dernières semaines complètes, aucune course, tibia).
- **Décisions / conseils** (proposés, en attente des réponses d'Arthur) :
  1. **Rugby ce soir : le zapper** (ou version très légère : pas de sprint, pas de foot, stop à la 1re douleur). Sprints, appuis et
     changements de direction = la charge la plus agressive pour un tibia qui a parlé 2 fois en 3 jours, avec 9 km au chaud dans les jambes.
  2. Test du tibia demain matin. 🟢 → renfo A (familiarisation) ; 🟠 → pas de course, vélo facile ; 🔴 → médecin.
  3. Reste de la semaine : 7 × 400 m → footing facile 40 min (+ renfo B) ; sortie longue du 11/10 → **10-12 km tout en facile**, sans bloc
     allure semi.
  4. **Seuil de consultation** : si la douleur revient à la prochaine sortie (3e fois) → kiné ou médecin du sport, vélo en attendant.
  5. Jusqu'au semi (si validé) : **1 seule séance de qualité par semaine** (allure semi / seuil de Pacer, à 5:13-5:18, jamais plus vite) ;
     séances VMA (7 × 400, 5 × 1500, 8 × 500, 30/30) → footing + 4-6 lignes droites ; sortie longue en facile, bloc allure semi seulement
     après 2 semaines sans douleur ; sorties « endurance » au test de la parole (≤ ~150 bpm au frais) même si plus lent que Pacer.
     Le rugby compte comme la 2e séance dure. Séances clés aux heures fraîches ; au chaud, courir à l'effort, pas à l'allure.
     Pacer s'adapte aux séances réalisées : remplacer une séance change la suite du plan.
  6. Objectif : 1h50 reste l'objectif A, décision 1h50 / 1h55 fin octobre sur un test au frais (8-10 km ou 2 × 5 km à 5:13).
- **À suivre** : note du tibia (jambe, /10, bande ou point, pendant les fractions, à la marche ce soir), rugby ce soir et jusqu'au semi
  (pause possible ?), souffle /10 et jambes /10 sur la rép. 2, priorité d'Arthur (1h50 à tout prix ou arriver en forme), validation de la
  semaine type et de la règle « 1 qualité par semaine ».

### 2026-10-05 · Programme · Semaine allégée, décision sur le plan reportée

- **Réponse d'Arthur** : il veut alléger un peu la semaine et aviser la semaine prochaine pour le reste. Ce soir : pas le rugby, **foot
  tranquille** à la place.
- **Analyse du coach** : bon compromis par rapport au rugby, mais le foot reste des appuis et des changements de direction ; c'est le tibia
  qui fixe la limite. Semaine précédente 10,9 km : viser ~24 km cette semaine (contre ~35 prévus par Pacer) reste sous les 30 km de septembre.
- **Décisions** : foot sans sprint à fond ni duel, 1 h max, sortie à la 1re sensation au tibia. Ma repos + test du tibia ; Me renfo A sans saut
  (déplacé du mardi) ; Je footing facile 30-35 min + renfo B ; Ve-Sa repos, **vélo du 09/10 retiré** ; Di sortie longue 10 km max tout en facile.
  Tibia douloureux au test ou pendant le footing → vélo facile à la place, et kiné / médecin du sport si la douleur revient en courant.
  `data/planned_manual.csv` mis à jour (renfo A au 07/10, vélo du 09/10 supprimé). Pacer recalculera la suite selon les séances faites.
- **À suivre** : test du tibia du 06/10 au matin (jambe, /10, bande ou point, effet du foot) ; règle « 1 qualité par semaine », semaine type
  et place du rugby à trancher au bilan du 11-12/10.
