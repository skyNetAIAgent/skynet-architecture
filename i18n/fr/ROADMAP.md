<!-- translation of docs/ROADMAP.md, source sha256: 4cd77f720933922c55c4d78c3e761ca614215cc0ed8610b0fb2ae2e3fbee22e2 -->

# Feuille de route : protection contre la fraude

[English](../../docs/ROADMAP.en.md) · [中文](../zh/ROADMAP.md) · [Español](../es/ROADMAP.md) · **Français** · [Deutsch](../de/ROADMAP.md) · [Italiano](../it/ROADMAP.md) · [Русский](../../docs/ROADMAP.md) · [Português](../pt/ROADMAP.md) · [العربية](../ar/ROADMAP.md)

État au 23 novembre 2026. Ceci est un **plan de travail, pas une promesse de résultat**. La marque `[x]`
signifie « fait, et c'est vérifiable dans le dépôt ou dans les enregistrements du réseau » ; `[ ]` signifie
« pas fait ». Les nombres marqués [calcul] sont obtenus par une formule, pas mesurés. La feuille de route
est mise à jour à chaque changement de statut.

## 1. Objectif et critères d'achèvement

**Objectif de l'étape actuelle du projet :** trouver un moyen de vérifier l'honnêteté qui satisfasse en
même temps les exigences obligatoires ([REQUIREMENTS](REQUIREMENTS.md)) :

- il est impossible de tromper le réseau : la fraude est inutile ou déficitaire, y compris pour un débutant
  avec un compte vide, en cas de collusion et avec de nombreuses clés ;
- aucun paiement à l'avance : ni cautions, ni cotisations, ni amendes ;
- la participation est rentable, la vérification de l'honnêteté est bon marché. Repères pour le surcoût de la
  vérification : environ 5% du travail pour les requêtes au modèle et environ 20% pour l'apprentissage
  (non confirmés).

**Le travail est considéré comme terminé lorsque tout ce qui suit est présent :**

1. **Il est écrit ce qui est exactement garanti** (décision D1) : pour le résultat d'une requête, une étape
   d'apprentissage, un paiement et l'historique ; pour un compte vide, un nombre quelconque de clés, le
   départ et la collusion totale des vérificateurs de la tâche. L'exigence admet « la fraude est inutile » ;
   il n'est pas obligatoire de prouver une perte stricte à chaque tentative.
2. **Pour chaque attaque du tableau des attaques, il est écrit la règle par laquelle un nœud rejette la
   fausse déclaration, et à partir de quelles données il le fait.** Sont indiqués séparément la probabilité
   de fausse acceptation, le dommage au réseau et le gain net de la coalition par rapport à l'inaction et
   par rapport au travail honnête. Contre-exemple de la règle : un cas honnête et un cas faux dans lesquels
   le nœud voit des données identiques. L'échantillonnage, la faible probabilité d'erreur et « il existe un
   observateur honnête » sont consignés comme hypothèses.
3. **Le coût complet de la vérification est calculé** par rapport à la même tâche sans vérification : le
   travail de l'exécutant et des vérificateurs, la mémoire, le trafic, le stockage, l'écriture dans le
   journal, les litiges, les reprises après incident. Sont déduits le revenu net d'un participant avec de
   grandes ressources à une électricité chère, le supplément d'un participant avec un matériel faible et le
   coût pour un consommateur sans matériel. L'écriture et le litige sont accessibles depuis un compte à
   zéro ; on ne peut perdre que les récompenses non arrivées à maturité.
4. **Les calculs sont reproductibles :** la version des règles et du noyau, les entrées, les bornes de
   l'énumération, la sortie et l'empreinte sont jointes ; le calcul est répété sur un second appareil. La
   répétition confirme le calcul, mais pas la justesse du modèle lui-même : celle-ci est justifiée séparément.
5. **Est mesuré ce qui ne peut pas être établi par le raisonnement :** la concordance du résultat bit à bit
   sur différentes cartes graphiques, la vitesse et la qualité du modèle en arithmétique entière, le coût du
   litige. Les profils, les métriques et les seuils sont fixés avant la mesure.
6. **Les autres exigences ne sont pas violées :** le réseau reste opérationnel même si l’un des nœuds ou l’une des plateformes est indisponible et, après un arrêt complet, ses nœuds peuvent se retrouver, les fondements des crédits sont reconstituables ; en
   cas de partition du réseau, le paiement litigieux attend l'historique commun, la reprise n'est pas payée
   deux fois.

Une issue honnête est aussi un résultat : si pour une certaine classe de tâches la vérification bon marché
est impossible, cela est montré par une preuve avec la classe de tâches nommée et les données nommées du
vérificateur, et non par l'absence d'idées.

## 2. Où nous en sommes

| Quoi | Statut | Où c'est consigné |
|---|---|---|
| À partir des signatures et des réponses courtes, on ne peut pas établir quel appareil a travaillé ni pendant combien de temps : un intermédiaire, un cache et une carte au repos donnent les mêmes données | Établi par le raisonnement | [OPEN_QUESTIONS](OPEN_QUESTIONS.md), « Ce qui a déjà été écarté » |
| Le réseau paie pour le résultat vérifiable, et non pour la ressource | Base du projet ; l'unité de résultat et la condition d'acceptation attendent d'être fixées (D2) | [CURRENT_DESIGN](CURRENT_DESIGN.md), section 1 |
| Paiement différé au lieu d'une caution : le participant ne répond qu'à hauteur de la somme en attente | Accepté | CURRENT_DESIGN, section 2 |
| Variante A : vérification par échantillonnage avec annulation des récompenses en attente en cas de fraude détectée | Spécification actuelle | CURRENT_DESIGN, section 3 |
| Variante B : le réseau ne paie que les tâches vérifiées, `1/p` fois plus cher | Proposition (D3) | CURRENT_DESIGN, section 3 |
| Concordance du résultat bit à bit par l'arithmétique entière | Candidat, pas mesuré | OPEN_QUESTIONS, Q2 |
| Litige par division en deux avec recalcul d'une étape dans le journal | Mesuré pour une ligne du modèle ; pas construit pour le modèle complet | [PILOT_RESULTS](PILOT_RESULTS.md) |
| Utilisation d’un vecteur aléatoire pour vérifier le produit de deux matrices dans le litige | Candidat, il n'existe qu'une estimation calculée | CURRENT_DESIGN, section 3 |
| Noyau de vérification immuable, qu'aucun vote ne peut annuler | Proposition (D4) | CURRENT_DESIGN, section 8 |

**Ce que l'on sait de la force de la protection.**

- Variante A, sans collusion : dans la famille énumérée (deux rafales de faux, 92 millions de stratégies),
  soumettre des résultats falsifiés puis quitter le réseau ne rapporte pas plus qu'un départ ordinaire [calcul].
- Variante A, collusion : les premiers points de la grille où soumettre des résultats falsifiés puis quitter le réseau devient rentable — une
  part de collusion de 87,5% (tâches de taille quelconque) et 89,0% (tâches identiques) avec la règle « pas
  plus d'un tiers en cours », 80% sans cette règle. Pas de la grille 0,002–0,02 ; d'autres familles de
  stratégies n'ont pas été énumérées [calcul, [FIRST_RUN](FIRST_RUN.md)].
- Variante B, sans collusion : avec une comparaison exacte, un faux n'est pas payé.
- Variante B, collusion : `q` est la fraction du poids total des vérificateurs de ce modèle que détient la coalition.
  Un faux n'est payé que si la tâche est choisie et que tous les `k` vérificateurs sont en collusion. Le
  paiement moyen pour un faux soumis est égal à `R·q^k` (`R` est le prix de la tâche) et ne dépend pas de
  `p` [calcul]. Pour `q = 1`, c'est le prix complet. Un débutant dont le compte est vide n’a aucune récompense en attente à perdre.
- Si tous les vérificateurs s’entendent, l’absence de paiements pour des résultats falsifiés n’a été démontrée pour aucune des deux variantes. On obtient cette garantie en vérifiant chaque résultat rémunéré à partir de données que tout nœud peut contrôler lui-même. Le recalcul complet ajoute environ 100% de travail. Mesures du pilote : la preuve
  RISC Zero pour une ligne du modèle a mis 22 min 10 s à être construite ; l'exécution de huit lignes dans
  la zkVM a duré environ 17 700 fois plus longtemps que la normale, sans construction de preuve. Ces mesures
  ne donnent pas de borne inférieure générale du coût.
- Irrégularité du revenu dans la variante B : à 6 000 tâches par mois, une vérification d'une tâche sur 100
  et un coût de revient de 95% du prix, la probabilité d'un mois déficitaire est de 33,10% [calcul, FIRST_RUN].
- La première exécution des calculs (702 portions) a été faite sur un seul ordinateur. Au 22 novembre, un second appareil avait recalculé 40 portions ; toutes ont coïncidé. Ses enregistrements sont signés par la
  clé `46000d30…` et sont accessibles sur un nœud complet. Les 662 autres portions ne sont pas confirmées
  indépendamment.

**Ce qui n'est pas résolu.**

1. Un débutant avec un compte vide en collusion (variante B) : gain moyen `R·q^k` par tentative, aucune perte.
2. « Honnête longtemps, puis une grosse fraude et le départ » : la perte est limitée à la somme en attente,
   le gain croît avec le nombre de faux. Des correctifs pour la variante B sont proposés, pas calculés.
3. Le flux de déchets depuis des clés gratuites. Une clé ne coûte rien ; le paiement par le travail du
   processeur place les appareils faibles dans une situation pire.
4. Un résultat utilisé avant la vérification. La réponse a déjà été lue par l'utilisateur, l'étape est déjà
   entrée dans l'apprentissage ; la limitation des paiements ne corrige pas cela. Dans la variante B, cela
   vaut aussi pour les tâches non choisies.
5. Les tâches d'apprentissage payées par l'émission de crédits : qui les approuve et selon quelle règle. Une
   tâche correctement exécutée mais auto-attribuée ne doit pas donner de crédits.
6. Un modèle rare : le cercle des vérificateurs est petit, et `q` pour lui peut être proche de 1.
7. La disponibilité des données et le litige sur une requête privée sans révéler la requête.
8. La concordance bit à bit et la vitesse du modèle en arithmétique entière ne sont pas mesurées.
9. Un saboteur qui n'a pas besoin de profit, et l'empoisonnement des données d'apprentissage. La protection
   économique n'agit pas contre eux.

## 3. Décisions en attente d'approbation

Tant qu'une décision n'est pas prise, les points du plan qui en dépendent restent des propositions.

| N° | Question | Ce qui en dépend |
|---|---|---|
| D1 | Ce qui est accepté comme garantie. « La fraude ne rapporte rien, ce qui est dépensé est perdu, le travail honnête est plus rentable » suffit-il ? Une fuite limitée en cas de collusion est-elle admissible, ou le paiement faux doit-il être exclu même en cas de collusion totale des vérificateurs | Critères d'achèvement, étapes 3 et 4 |
| D2 | Fixer le paiement pour le résultat vérifiable au lieu de la puissance et du temps ; définir l'unité de résultat et la condition d'acceptation | Étapes 2–6 |
| D3 | La variante A, la variante B ou aucune. Se décide après comparaison sur les mêmes attaques et au même coût (étape 2) | Étapes 3 et 6 |
| D4 | Le noyau de vérification immuable et ce qu'il contient | Étape 6 |
| D5 | La première expérience : Qwen3.5-4B en arithmétique entière sur deux cartes graphiques différentes (les bits coïncident-ils, vitesse, qualité) | Étape 5 |

## 4. Étapes et liste de contrôle

Les étapes 1–4 avancent en même temps : ce sont des calculs et des raisonnements. La recherche de nouveaux
algorithmes (étape 4) n'attend pas les autres. L'étape 5 exige la décision D5. L'étape 6 rassemble les
résultats.

### Étape 0. Outils de collaboration

- [x] Dépôt public, base immuable en neuf langues (étiquette `core-v1`).
- [x] Programme agent pour Windows, Linux et macOS : tâches et mises à jour signées, vérifications
      automatiques sur trois systèmes (version 0.2.0).
- [x] Résultats et [tableau des tâches](BOARD.md) sans compte utilisateur.
- [x] Premier nœud complet, conservant l'historique des enregistrements.
- [x] Première tâche de recherche « Protection contre les fraudeurs » sur le tableau, en neuf langues.
- [ ] Rapport sur une tâche du tableau remis par un participant sans lien avec les mainteneurs, indiquant par
      qui et comment il a été obtenu. Actuellement, tous les enregistrements du réseau sont faits par les
      appareils des mainteneurs. Des clés différentes ne prouvent pas des propriétaires différents.
- [ ] Confirmation indépendante des 702 portions de la première liste de tâches (40 actuellement).
- [ ] Mise à jour de l'agent d'une version publiée à la suivante, observée sur une installation réelle
      (actuellement vérifiée uniquement par des tests).
- [ ] Application Android : vérification sur un vrai téléphone, publication des résultats sans jeton.
- [ ] Installation sans Python préinstallé : un seul fichier pour Windows, macOS et Linux.
- [ ] Instructions pour un assistant IA : comment prendre une tâche du tableau, remettre un rapport et
      vérifier celui d'un autre.
- [ ] Boucle automatique pour les assistants IA : l'agent récupère lui-même les nouvelles tâches du tableau
      et les transmet au modèle local du participant. Actuellement, cela se fait par des commandes manuelles.
- [ ] Deuxième et troisième nœuds complets chez des propriétaires différents.
- [ ] Corriger la ligne obsolète dans BOARD (« l'agent 0.2.0 n'est pas encore publié »).

### Étape 1. Formulation précise

- [ ] Les décisions D1 et D2 sont prises et consignées.
- [ ] Pour une requête ouverte et une étape d'apprentissage sont consignés : la règle d'acceptation,
      l'arithmétique, le fondement de l'émission de crédits, le moment de fixation du résultat par rapport au
      tirage au sort et le moment où le résultat peut être utilisé.
- [ ] Le modèle de l'adversaire en un seul document : collusion, nombreuses clés, départ, location de
      puissance ; ce qui compte comme gain du fraudeur et ce qui compte comme dommage au réseau.
- [ ] Le tableau des attaques analysées est publié dans le dépôt en neuf langues avec le statut de chaque
      attaque pour les variantes A et B. Avant publication, vérifier les lignes : dans le résumé de
      CURRENT_DESIGN, la somme des catégories 18 + 6 + 19 + 16 = 59 alors que 60 sont annoncées.
- [ ] Pour chaque attaque, il est consigné à partir de quelles données vérifiables indépendamment le nœud
      rejettera la fausse déclaration en cas de collusion de l'exécutant et des vérificateurs.

Terminé quand : tout participant peut, à l'aide du tableau, identifier une attaque qui reste sans parade et vérifier que c’est bien le cas.

### Étape 2. Économie : les calculs exécutés par les mini-agents

Chaque tâche est un modèle exact avec une grille finie d'entrées ; les probabilités et les sommes sont
calculées en fractions exactes, l'empreinte de chaque portion est comparée entre les appareils.

- [x] Variante A, soumission de résultats falsifiés suivie d’un départ du réseau : première exécution.
- [x] Variante B, irrégularité du revenu à part de vérification constante : première exécution.
- [ ] Confirmation indépendante des deux calculs (voir étape 0).
- [ ] **Campagne de sortie dans la variante B.** Entrées : la somme en attente `H₀`, le prix `R`, la part de
      vérification `p`, la collusion `q` et `k`, le plafond des tâches simultanées `C`, le nombre de rafales
      `T`. Un seul faux attrapé remet à zéro toute la somme en attente, y compris les gains de la rafale.
      Trouver le plus grand paiement attendu au-delà de `H₀`, y compris pour `H₀ = 0`, `q = 0` et `q = 1`.
- [ ] **Places d'apprenti.** Par époque, `S` places sont distribuées entre `n` clés honnêtes et `m` clés de
      la coalition. Trouver la fuite attendue sur `E` époques et la part des places qui revient aux débutants
      honnêtes, lorsque `m` croît.
- [ ] **Loterie avec une part de vérification choisie.** Pour `N` tâches par mois, prendre le plus petit `p`
      pour lequel au moins 60 tâches sont payées en moyenne. Trouver la probabilité d'un mois et d'un
      trimestre déficitaires, la probabilité d'un mois sans aucun paiement et le nombre de recalculs pour le
      réseau.
- [ ] **Certificat du jeton gagnant** (voir étape 4) : le nombre d'opérations de vérification par rapport au
      recalcul complet de la couche de sortie sur un ensemble d'entrées donné.
- [ ] La formule du coût complet de la vérification pour trois types de participants ; après l'étape 5, les
      mesures y sont substituées.
- [ ] Comparaison des variantes A et B sur les mêmes attaques et au même coût, puis la décision D3. Issue
      possible : les deux variantes restent des pistes de recherche.

Terminé quand : pour chaque variante, il existe un tableau « part de collusion → plus grand gain attendu du
fraudeur », recalculé sur au moins deux appareils indépendants.

### Étape 3. Fermer les failles connues

- [ ] **Débutant avec un compte vide.** Candidat : les premières tâches du débutant sont telles que tout nœud
      les vérifie exactement lui-même, et ce n'est qu'ensuite que la récompense et le poids sont crédités.
      Solution de repli : un budget commun de paiements d'apprenti par époque ; il limite la fuite sans la
      rendre nulle, et la collusion peut occuper toutes les places.
- [ ] **« Honnête longtemps, puis une grosse fraude ».** Candidat : un plafond sur la somme de tous les
      engagements ouverts de la clé, en comptant les plus grands gains possibles. C'est une borne d'une seule
      rafale, pas une fuite nulle.
- [ ] **Déchets depuis des clés gratuites.** Candidat : le nœud n'accepte les données que pour les numéros de
      tâches autorisés, limite la taille, la file d'attente et le travail par époque. Le canal peut tout de
      même être saturé ; une place garantie pour un débutant honnête avec un nombre quelconque de clés n'est
      pas obtenue.
- [ ] **Résultat utilisé avant la vérification.** Candidat : vérifier le bloc de réponse avant de le
      remettre ; conserver l'étape d'apprentissage dans une branche séparée et ne promouvoir que le
      descendant vérifié. Coût : latence et mémoire.
- [ ] Tâches d'apprentissage : une règle d'approbation sans participant doté de droits spéciaux.
- [ ] Modèle rare : un seuil, déduit de la distribution du poids, en dessous duquel le réseau ne paie pas
      pour le modèle.
- [ ] Vérificateur paresseux et nouvelle soumission d'un résultat connu : des engagements masquants avec
      révélation, un crédit unique selon le contenu.
- [ ] Panne de matériel chez un participant honnête : une règle qui ne donne pas de gain au fraudeur.
- [ ] Disponibilité des données et litige sur une requête privée sans révélation.
- [ ] Fenêtre de litige à l'arrêt du réseau, protection contre un historique périmé, partition du réseau.

Terminé quand : pour chaque point sont publiés une construction avec ses hypothèses, une attaque contre elle
et son coût, soit un contre-exemple, soit le statut « ouvert » avec la raison.

### Étape 4. Recherche d'une garantie indépendante de la part de collusion

On cherche une vérification que chaque nœud exécute lui-même, de sorte que l'accord des vérificateurs ne
décide rien. Les directions ne sont pas approuvées. Pour chacune, il faut indiquer les opérations vérifiées,
les données, la probabilité d'erreur et le coût d'une requête ou d'une étape entière ; puis la mener jusqu'à
une construction ou la fermer par un contre-exemple.

- [ ] **Tâches pour lesquelles un critère exact permet de vérifier le résultat à faible coût.** Exemple : pour la régression ridge, le nœud
      vérifie la condition d'optimalité en un seul passage sur les données. Question : quelle part du travail
      du réseau tient dans de telles tâches. Commencer par cette direction : elle garantit qu’aucun résultat falsifié n’est rémunéré.
- [ ] **Utilisation d’un vecteur aléatoire pour vérifier chaque produit de matrices** au lieu du recalcul. Le
      vecteur est choisi après la fixation du résultat ; la probabilité de laisser passer une erreur ne
      dépend pas de la collusion. Rentable pour les grands lots ; pour la génération jeton par jeton, aucun
      gain. Les autres opérations (arrondi, activations, cache, optimiseur) doivent être vérifiées séparément.
- [ ] **Vérification de la réponse finie par un seul passage du modèle** avec un profil exact et l'aléa fixé
      dans la tâche. Le nombre d'opérations est du même ordre que la génération ; on ne sait pas si cela
      tient dans 5%.
- [ ] **Tables de sommes partielles exactes pour les couches immuables :** le nœud déduit une fois les tables
      des poids, puis obtient la sortie de la couche par des lectures et des additions. Applicable aussi à un
      seul jeton ; bute sur le volume de mémoire.
- [ ] **Certificat du jeton gagnant** pour un grand vocabulaire : l'exécutant transmet la couverture du
      vocabulaire par groupes, le nœud vérifie les bornes supérieures et ne descend vers les jetons
      individuels que là où la borne ne sépare pas le gagnant. Dans le pire des cas, tout le vocabulaire est
      vérifié.
- [ ] **Étape d'apprentissage comme formule exacte de mise à jour :** les nœuds stockent et vérifient non la
      nouvelle matrice de poids, mais les facteurs de mise à jour. Dérivé uniquement pour une couche linéaire
      avec un SGD simple.
- [ ] **Litige ouvert à tout participant pendant la fenêtre.** La garantie est conditionnelle : il faut au
      moins un observateur qui a reçu les données et a eu le temps d'objecter. Qui paie l'observation avec un
      compte vide n'est pas résolu. Garder en solution de repli.
- [ ] **Paiement pour l'amélioration mesurée du modèle** sur des tâches choisies après la fixation des poids.
      Change le fondement du paiement et exige une décision séparée. Convient à la sélection des versions du
      modèle.
- [ ] **Preuves de calcul pour l'apprentissage (sumcheck, GKR)** pour une étape définie : une estimation complète du coût de calcul
      avec les plages, l'arrondi et le rattachement de l'entrée à la tâche.
- [ ] **Borne inférieure :** montrer quelles classes de vérifications ne peuvent pas être sans erreur. Début :
      un ensemble fixe de vérifications linéaires dont le nombre est inférieur à la taille du résultat laisse
      toujours passer une certaine erreur ; restent ouverts l'aléa frais et les entrées à structure connue.
- [ ] Les idées des participants et des assistants IA venant du tableau : chacune passe par la même analyse,
      y compris le cas `q = 1`.

Terminé quand : pour chaque direction sont publiées une construction accompagnée d’une estimation de son coût, un contre-exemple ou une
borne prouvée. Est considérée comme trouvée la construction qui remplit tous les critères de la section 1.

### Étape 5. Les fondements qui ne s'établissent que par l'expérience (exige D5)

- [ ] Qwen3.5-4B en arithmétique entière sur deux cartes graphiques différentes : les bits coïncident-ils.
- [ ] Sa vitesse par rapport au profil ordinaire sur les mêmes cartes.
- [ ] Sa qualité par rapport au profil ordinaire sur le même ensemble de tâches.
- [ ] Des plans de mesure séparés (hors D5) : l'énergie de la vérification, l'apprentissage en arithmétique
      entière.
- [ ] Le coût du litige dans le journal pour le modèle complet. Avant lui, il faut le choix de la blockchain,
      une machine de référence du modèle complet, le rattachement de l'entrée, les longueurs et les chemins
      de calcul.

Terminé quand : chaque nombre est mesuré, les conditions de la mesure sont consignées, la mesure a été
répétée par un second participant. La concordance des bits ne vaut que pour les configurations testées.

### Étape 6. Synthèse et acceptation

- [ ] La décision D4 sur le noyau immuable — avant la vérification finale de la résistance à la prise de contrôle de la majorité des voix.
- [ ] Mettre à jour CURRENT_DESIGN et le tableau des attaques d'après les résultats des étapes 1–5.
- [ ] Une déclaration est suivie sur le papier, de l'autorisation de la tâche jusqu'à l'utilisation du
      résultat, y compris le refus, la reprise et la partition du réseau.
- [ ] Revue ouverte de la construction finale : un conseil de modèles et une tâche sur le tableau.
- [ ] Pour chaque exigence est publiée une preuve, une mesure, un contre-exemple ou le statut « ouvert ».
      Vérification selon les six critères de la section 1.

## 5. Comment avance le travail

1. Un point de la liste de contrôle devient une tâche : de calcul (elle est calculée par les mini-agents, le résultat est vérifié par concordance) ou de recherche (elle est publiée sur le tableau).
2. Les participants et leurs assistants IA remettent des rapports. Un rapport n'est accepté que s'il peut
   être vérifié : par recalcul, par contre-exemple ou par une référence à la source. Le nombre de clés
   d'accord ne prouve rien ; la décision de l'auteur de la tâche sur le tableau ne confirme pas le calcul.
3. Selon l'issue de la vérification, la tâche est fermée, précisée ou donne naissance à de nouvelles tâches.
4. Le changement de statut est reporté dans cette feuille de route et dans CURRENT_DESIGN par une seule
   modification, avec la date.

## 6. Ce que cette feuille de route ne promet pas

- Qu'une solution existe dans les conditions fixées. C'est l'objet de la recherche.
- Des délais. Le projet n'a pas d'exécutants payés ; la vitesse dépend des participants.
- Des récompenses pour la participation à la conception.
