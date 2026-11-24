<!-- translation of docs/THREAT_MODEL.md, source sha256: ad971a2fe29f57d18ba6e2f6d8b4b6eedb8fb813c17a1cd1343ca6b141c990a8 -->

# Modèle de l'adversaire et tableau des attaques

[English](../../docs/THREAT_MODEL.en.md) · [中文](../zh/THREAT_MODEL.md) · [Español](../es/THREAT_MODEL.md) · **Français** · [Deutsch](../de/THREAT_MODEL.md) · [Italiano](../it/THREAT_MODEL.md) · [Русский](../../docs/THREAT_MODEL.md) · [Português](../pt/THREAT_MODEL.md) · [العربية](../ar/THREAT_MODEL.md)

État au 24 novembre 2026.

Ce document est le résultat du conseil de modèles pour l'étape 1 de la feuille de route (« Formulation précise »,
[ROADMAP](ROADMAP.md), section 4). Il rassemble le modèle de l'adversaire, le rapprochement du nombre d'attaques,
le statut de chacune des 60 attaques de la spécification pour les variantes A et B, les nouvelles attaques trouvées
par le conseil, et les questions que seul le propriétaire du projet peut trancher.

**Statut du document.** C'est un résultat de raisonnement et de calcul par formules, non une mesure.
Il n'y a eu pour lui ni expériences, ni lancements de réseau, ni recalculs logiciels. Les nombres marqués
[calcul] sont obtenus par les formules des travaux du conseil et vérifiés à la main par les critiques ; ils ne sont
pas répétés sur un second appareil. Seul ce que le propriétaire du projet approuvera deviendra une décision
acceptée. Tout le reste ici est une évaluation du conseil, et en cas de désaccord elle porte la mention « contesté ».

**Comment lire.** La section 1 définit qui attaque et ce qui compte comme gain. La section 2 explique
l'écart entre 59 et 60. La section 3 est le tableau principal : tout participant peut y nommer
une attaque non fermée et le vérifier dans les documents sources. La section 4 est un bref bilan, la section 5 —
les questions au propriétaire, la section 6 — qui a participé.

Documents sources : décisions D1–D5 dans [ROADMAP](ROADMAP.md), section 3 ; variantes A et B dans
[CURRENT_DESIGN](CURRENT_DESIGN.md), section 3 ; [OPEN_QUESTIONS](OPEN_QUESTIONS.md) ;
[PILOT_RESULTS](PILOT_RESULTS.md) ; première exécution [FIRST_RUN](FIRST_RUN.md) ;
exigences obligatoires [REQUIREMENTS](REQUIREMENTS.md). Le tableau des 60 attaques est tiré
de la spécification du réseau sans coordinateurs du 20 novembre 2026 (ci-après SPEC) ; les numéros de lignes
1.1–7.4 sont ses numéros.

---

## 1. Modèle de l'adversaire

### 1.1. Notations et variantes

| Symbole | Sens |
|---|---|
| `R`, `c` | Prix de la tâche et coût de revient d'une exécution honnête, `c ≤ R` |
| `H` | Somme en attente : récompenses non arrivées à maturité de la clé pour les trois derniers jours. Seule celle-ci peut être annulée (ni cautions ni amendes, exigence R5) |
| `p` | Part de vérification : en A `p = 4R/(R+H)`, mais pas moins de 1% ; en B elle est constante, par exemple 1% |
| `B` | Annulation en A : `B = 4R/p − R`, pas plus de `H` ; si `p > 1%` c'est `B = H`, sinon `B = 399R` |
| `k` | Nombre de vérificateurs de la tâche, 3 (avec les tours de tirage au sort, en moyenne 3,5–4,5) |
| `q`, `q_eff` | Part de la coalition dans tout le poids des vérificateurs du modèle et parmi ceux qui vérifient réellement la tâche (section 1.7) |
| `G` | Coût complet du litige dans le journal |

**Variante A** (spécification actuelle) : vérification par échantillonnage avec annulation sur `H` ; une soumission
non vérifiée et non contestée est payée. **Variante B** (proposition) : seules les tâches tirées au sort et
confirmées sont payées, au prix `R/p` ; ce qui n'est pas tiré n'est payé à personne ; un faux attrapé brûle tout
le `H` de la clé. B est décrite par une esquisse, et le conseil a analysé « B telle que décrite » : le chemin du débutant,
l'admission des vérificateurs selon `H`, le tarif des vérificateurs et la source de `R/p` pour les requêtes
ne figurent pas dans la description.

### 1.2. Qui attaque

Les profils sont regroupés pour les six travaux. Les combinaisons sont obligatoires : coalition avec des clés gratuites,
locataire devenu coalition, participant longtemps honnête en cas de collusion, utilisateur en collusion
avec les vérificateurs, saboteur avec des clés gratuites.

| Profil | Ce dont il dispose | Ce qu'il veut |
|---|---|---|
| Solitaire | Ses propres clés, son propre appareil, un programme modifié | Des crédits sans travail ou au-delà du travail |
| Coalition de part `q` | Des clés sous gestion commune ; transmission instantanée des résultats, des étapes de calcul, des états et des requêtes ; une caisse commune | Faire passer un faux, être payée pour des vérifications sans recalcul, gagner des votes |
| Propriétaire de nombreuses clés | Autant de clés qu'il veut presque gratuitement ; poids et `H` des nouvelles clés nuls | Des files d'attente, des places d'apprenti, la distribution de données, des attributions, des billets B |
| Locataire de puissance | Des heures de GPU au prix du marché, un travail honnête et payé par le réseau | Une part de poids, puis la collusion, un modèle rare ou les règles |
| Saboteur sans profit | Prêt à perdre toutes les récompenses non arrivées à maturité | Le mal lui-même : le modèle, les réponses, une porte dérobée, l'arrêt |
| Participant au compte vide | `H = 0`, pas de poids | N'importe quel paiement sans travail |
| Longtemps honnête, puis départ | Un grand `H` et du poids ; choisit le moment, la taille et le nombre de vagues | Plus que `H` plus le paiement honnête des dernières tâches |
| Utilisateur | Sa requête, ses crédits, le droit au litige, une collusion avec l'exécutant ou les vérificateurs | Une réponse gratuite, un remboursement pour une réponse correcte, les données d'autrui |
| Opérateurs de relais, de points de rencontre, de nœuds d'enregistrement, de points d'accès à la blockchain, gardiens des données | Voient les adresses et l'heure, retardent, ne transmettent pas, montrent un faux environnement | La censure, l'isolement d'un nœud, la révélation d'identité, le paiement pour les enregistrements |
| Parties externes | La balise d'aléa, le producteur de bloc, les fournisseurs de points de contrôle, le fabricant du mode protégé, le diffuseur du programme | Décaler l'échantillon, glisser un faux historique ou un faux programme |
| Propriétaire d'appareils d'autrui | Des clés de travail volées ou infectées | Confirmer des faux en risquant le `H` d'autrui |

### 1.3. Ce que l'adversaire peut et ne peut pas

**Peut :** créer autant de clés qu'il veut ; lancer un programme modifié et lire tout sur son
appareil, y compris des requêtes privées en mode ordinaire ; transmettre au sein de la coalition n'importe quelles données ;
s'éteindre, choisir le moment de la soumission, se taire, donner des données à certains nœuds et pas à d'autres,
garder un seul exemplaire ; louer de la puissance ; voter et acheter des voix ; proposer ouvertement
un pot-de-vin via un contrat intelligent (les confirmations sont dans le journal, le paiement peut être exécuté sans confiance) ;
en tant que producteur de bloc — ne pas publier un bloc et choisir l'une des deux valeurs d'aléa ;
détenir une partie des relais et encercler un nœud ; avoir un bénéfice externe ou apprécier le mal lui-même.

**Ne peut pas** (ce sont des hypothèses, il faut les nommer clairement) : falsifier la signature d'une clé d'autrui non volée,
trouver une collision de hachage, ouvrir un engagement de deux manières, falsifier un tirage au sort secret (VRF) ;
réécrire les blocs définitifs d'une blockchain publique, le journal n'a pas de clé d'administrateur et il
est correct (prémisse 1 de la SPEC ; le programme n'est pas écrit) ; prédire ou décaler l'aléa après
la fixation du lot (prémisse 2 ; les sources ne sont pas choisies ; le mélange protège de la prédiction,
mais pas du choix par la dernière source, N13) ; obtenir une concordance au bit près sans calcul
(prémisse 3 ; non vérifié) ; modifier l'issue du recalcul d'une étape dans le journal (prémisse 4 ; pour le modèle complet
non construit) ; modifier le programme du nœud d'autrui (D4) ; annuler les crédits disponibles d'autrui,
obtenir un second paiement pour le même numéro, révoquer un lot soumis.

**Ce que le réseau ne voit pas par principe :** à qui appartiennent les clés et si les participants sont indépendants ; si le
nœud a donné les données à un autre ; ce qui tourne sur l'ordinateur d'autrui ; en quoi le recalcul diffère d'une copie de l'état
d'autrui. Si le cas honnête et le cas faux donnent au nœud des données identiques, aucune règle ne les
distinguera ([OPEN_QUESTIONS](OPEN_QUESTIONS.md)).

### 1.4. Gain de l'adversaire et dommage au réseau

Le gain est calculé pour toute la coalition à partir d'un même état initial, avec les mêmes droits, tâches
et horizon jusqu'au règlement final, y compris le départ. Sont additionnés les crédits arrivés à maturité, les indemnisations,
la valeur du service obtenu et des nouveaux droits ; sont soustraits les coûts réels (travail, énergie, location, gas,
paiements externes). Les transferts au sein de la coalition sont compensés, un même crédit n'est pas compté deux fois, la perte
de la victime n'est pas en soi un revenu de la coalition. Types de gain : crédits pour une fausse déclaration (faux, copie,
confirmation sans recalcul, ligne d'autrui) ; coûts économisés à paiement égal ; poids et places
dans le tirage au sort ; remboursement pour une réponse correcte ou partie de données non payée ; gain par effet — influence sur la
réponse ou le modèle, lecture de la requête d'autrui, contrôle des règles, de l'émission, du catalogue, du plan, le mal lui-même.

Le dommage au réseau est calculé séparément, dans ses propres unités : un résultat erroné est accepté ; le résultat est utilisé
avant vérification ; des crédits sont émis sans travail ; un honnête a perdu `H` ; les paiements ou l'entrée des
débutants sont gelés ; des données privées sont révélées ; l'historique, les règles, le programme ou la version du modèle sont substitués ; le réseau a
dépensé du travail pour des vérifications et des litiges imposés. Un dommage sans gain ne viole pas D1, mais peut
violer d'autres exigences ; dans le tableau c'est « s.o. » avec le nom de l'exigence.

### 1.5. Formulation formelle de D1

D1 (adopté le 23 novembre 2026) : « le fraudeur n'obtient pas ce qu'il veut » ; le gain attendu d'un faux
n'est pas supérieur à zéro par rapport au travail honnête et par rapport à l'inaction, pour toute coalition, y compris un débutant
au compte vide et un nombre quelconque de clés ; une fuite positive limitée ne satisfait pas au critère.

Soit `U(σ)` — l'utilité attendue de la coalition sous la stratégie `σ`. Pour chaque stratégie avec une fausse
déclaration, il faut **les deux** inégalités :

- `Δ₀ = E[U(σ) − U(inaction)] ≤ 0` — chaque fausse déclaration est remplacée par un refus de la tâche
  (le `H₀` déjà gagné arrive alors à maturité) ;
- `Δч = E[U(σ) − U(travail honnête)] ≤ 0` — chaque fausse déclaration est remplacée par une exécution honnête.

L'exigence s'applique pour tout `q` de 0 à 1, pour `H = 0` et un nombre quelconque de clés. Pour la réfuter
il suffit d'un seul état admissible et d'une seule différence positive. Il ne faut pas comparer à la plus grande
des deux bases : avec l'inaction à 0, un gain honnête de 0,60 et une fausse déclaration de 0,20, une telle comparaison
donne « pas de violation », alors que `Δ₀ = +0,20` [calcul].

Un travail a proposé de diviser D1 en niveau économique (crédits seulement) et niveau par effet
(influence sur la réponse et le modèle, lecture de la requête, mal). Le conseil ne l'adopte pas lui-même : la question est portée au
propriétaire (section 5, question 1). Dans le tableau, un gain uniquement par effet est marqué « non (eff.) ».

### 1.6. Principe général de la colonne « données pour le refus »

En cas de collusion de l'exécutant avec tous les vérificateurs désignés, le nœud ne voit que des données concertées :
les empreintes du résultat et de l'étape, les états révélés avec les preuves d'inclusion. Toutes sont compatibles
avec un faux. Seuls l'entrée et le modèle fixé restent vérifiables indépendamment, à partir desquels le nœud
peut recalculer lui-même la tâche — environ +100% de travail [calcul] ; ni A ni B ne l'exigent, et pour une
requête privée le nœud tiers n'a même pas l'entrée. C'est pourquoi le tableau porte souvent « non, sauf recalcul
complet ».

### 1.7. Part de collusion `q_eff`

Tous les seuils du type « jusqu'à 91% » se rapportent à la part de la coalition parmi ceux qui vérifient réellement la tâche.
`q_eff` est la part de la coalition parmi les vérificateurs qui (1) sont admis à la tâche (selon la règle 2.6 de la SPEC,
pour une tâche d'un exécutant ancien il faut `H_v ≥ B`, jusqu'à `399R`), (2) ont répondu dans le délai du tour et (3) ont reçu
les données pour la vérification. Exemple [calcul] : 3000 appareils domestiques honnêtes à 8 heures et 100 appareils honnêtes
fonctionnant 24 h sur 24 contre 800 appareils loués fonctionnant 24 h sur 24. La part de l'adversaire dans tout le poids est de 42,1%
(19 200 sur 45 600 heures-appareil par jour) ; un appareil domestique accumule environ `144R < 399R`
et n'est pas admis aux tâches d'exécutants anciens ; parmi les admis `q_eff = 800/900 = 88,9%`,
`q_eff³ ≈ 0,70`. Réserve des critiques : cela concerne les tâches avec `B = 399R`. La condition (3) peut porter
`q_eff` jusqu'à un pour toute part globale (N2). La formule `q^k` n'est valable que pour des choix indépendants ;
dans la SPEC les tours vont jusqu'à trois réponses, et pour une collusion partielle il faut la distribution des répondants.

### 1.8. Formules de base [calcul]

- **A, un seul faux :** gain `R − 4R(1 − q³)` ; déficitaire pour `q < 0,9086`. **Débutant A :**
  `p = 1`, `B = H = 3R`, gain `R(4q³ − 3)`.
- **A, départ avec des faux** (énumération FIRST_RUN sur un seul appareil, non confirmée) : rentable à partir de
  `q = 0,875` (tailles quelconques, trois vagues, règle « pas plus d'un tiers de `H` en cours » ; 1,00004·H₀ à
  0,875, 1,034·H₀ à 0,880), à partir de 0,890 (tâches identiques), à partir de 0,800 sans la règle du tiers ; sans collusion
  sur 92 millions de stratégies il n'y a pas de départ rentable (le meilleur 0,980·H₀). C'est une énumération de familles, non une preuve.
- **B, un seul faux** est rentable pour `q^k > pH/(R + pH)` ; avec `p = 1%`, `k = 3` : `q ≈ 0,928` pour
  `H = 400R`, `0,659` pour `40R`, tout `q > 0` pour `H = 0`. Le paiement brut moyen pour un faux
  `R·q^k` ne dépend pas de `p`.
- **B, vague de `N` faux :** `E = a^N·H₀ + N·a^(N−1)·q^k·R`, `a = 1 − p(1 − q^k)`. Le premier
  faux est rentable pour `H₀` inférieur à 2,8R / 14,3R / 52R / 105R / 269R pour `q` = 0,3 / 0,5 / 0,7 /
  0,8 / 0,9. Pour `H₀ = 0`, le plus grand gain par clé est d'environ `q^k·R/(e·p·(1 − q^k))` : 0,037R / 1,0R /
  5,3R / 19R pour `q` = 0,1 / 0,3 / 0,5 / 0,7. Une seule vague sans énumération — borne inférieure.
- **Probabilité d'un paiement indu** pour une tâche sans litige externe : en A `1 − p + p·s`, en B `p·s`
  (`s` — probabilité d'une collusion totale lors du choix) ; avec `p = 0,01`, `s = 0,125` — 0,99125 et 0,00125,
  et le paiement indu brut pour `R = 1` — 0,99125 et 0,125. On ne peut pas comparer les variantes uniquement par la fréquence
  du paiement indu.

---

## 2. Rapprochement « 60 et 59 »

Dans la SPEC il y a exactement 60 lignes (12 + 12 + 10 + 5 + 11 + 6 + 4) : 18 fermées, 6 déficitaires, 19 limitées,
16 ouvertes et **une « non-attaque » — la ligne 1.9** (soumettre un résultat correct calculé sur le matériel
d'autrui est autorisé par la décision D2) ; le résumé de CURRENT_DESIGN, section 9, et le paragraphe « En bref » de la SPEC
n'ont additionné que quatre catégories et ont perdu la cinquième, d'où 59. Les six travaux et les trois critiques
y sont arrivés indépendamment. L'écriture correcte : 60 = 18 + 6 + 19 + 16 + 1.

---

## 3. Tableau des attaques

### 3.1. Notations

**Statut :** ferm. — le nœud rejette l'attaque d'après les données du journal sous les prémisses nommées ;
déf. — l'attaque est possible, en moyenne déficitaire jusqu'à la limite indiquée ; lim. — possible, le dommage ou
le gain sont limités par une règle ; ouv. — pas de solution ; non-attaque.

**D1 :** oui — gain non supérieur à zéro pour toute coalition ; **non** — il existe une stratégie à
gain positif au moins contre une base ; cond. — satisfait seulement sous les prémisses nommées,
indépendantes de la part de collusion (prémisses 1–4 de la SPEC, pas encore construites) ;
non (eff.) — il n'y a pas de gain monétaire ou il n'est pas établi, mais un gain par effet est atteint
(section 1.5) ; s.o. — l'attaque ne comporte pas de fausse déclaration en vue d'un gain, l'exigence indiquée est touchée ;
? — la règle n'est pas définie, le signe du gain n'est pas établi.

**Données** — d'après quelles données vérifiables indépendamment le nœud rejettera une fausse déclaration en cas de collusion
de l'exécutant avec tous les vérificateurs. « contesté » — les travaux ou les critiques ont divergé et le désaccord n'est pas tranché.
Les renvois « N… » mènent aux nouvelles attaques de la section 3.9.

### 3.2. Exécutant

| № | En bref | A | D1 en A | B | D1 en B | Données pour le refus en cas de collusion | Ce qu'il faut pour fermer |
|---|---|---|---|---|---|---|---|
| 1.1 | Débutant au compte vide soumet un faux | déf. jusqu'à `q ≈ 0,909` : les premières tâches sont toujours vérifiées, gain `R(4q³−3)`. Contesté : le critique ChatGPT considère la ligne ouverte, car les `3R` de départ peuvent être obtenus par copie (2.2, N1) | **non** pour `q ≥ 0,909`, et pour tout `q > 0` — via le paiement de revérifications d'apprenti | ouv. : `R·q^k` par tentative sans pertes, autant de clés qu'on veut | **non** pour tout `q > 0` | Non, sauf recalcul complet d'après l'entrée ouverte ; pour une requête — seulement chez l'utilisateur | Vérifier les premiers résultats payés d'une manière que chaque nœud exécute lui-même ; avant cela — seulement un travail non payé. En B — admission selon `H` (N16) |
| 1.2 | Un participant ancien falsifie une partie des tâches | déf. jusqu'à `q ≈ 0,909` ; 99% des faux ne sont pas vérifiés et restent dans le réseau | **non** pour un `q` élevé | déf. pour `q^k R < p(1−q^k)H` : 0,928 pour `H = 400R`, 0,659 pour `40R`, tout `q` pour `H = 0` ou depuis une clé vide (N16) | **non** | Non, sauf recalcul complet | Vérification du résultat payé indépendante de la part de collusion (étape 4). En B — `p` et admission en fonction de `H` |
| 1.3 | Honnête longtemps, puis grosse fraude et départ | déf. seulement dans les familles énumérées sous 0,875 / 0,890 / 0,800 (section 1.8) | **non** pour `q ≥ 0,875` ; en dessous non démontré | ouv. : la campagne de sortie n'est pas calculée ; pour un petit `H` rentable depuis tout `q > 0` | **non** | Non, sauf recalcul | Preuve pour toutes les stratégies en A ; calcul de la campagne de sortie de B, y compris `H₀ = 0` (étape 2) |
| 1.4 | Soumet un faux et disparaît après avoir vu l'échantillon | ferm. : le lot n'est pas révocable, la disparition après l'échantillon — résultat erroné | cond. | de même | cond. | La ligne du lot et l'absence de révélation à échéance | Une panne de communication honnête est indiscernable (coût pour les honnêtes) ; pour une requête privée — disponibilité de l'entrée |
| 1.5 | Apprend à l'avance ou choisit l'échantillon | ouv. aujourd'hui : fermé seulement sous la prémisse 2, et les sources ne sont pas choisies (ainsi l'ont évalué les travaux ChatGPT ; les critiques Claude et ChatGPT sont d'accord) | cond. ; **non** en cas de choix par la dernière source (N13) | de même | de même | Valeurs publiques de la balise et du bloc ; une collusion sur le seuil de la balise ou une rétention du bloc ne s'y voient pas | Choisir les sources ; tour de balise strictement après l'acceptation définitive du bloc ; consigner la confiance dans les parties externes comme hypothèse |
| 1.6 | Double paiement ou tâche d'autrui | lim. : le numéro est unique, mais une ligne avec la tâche d'autrui n'est rejetée par le journal que sur objection ; si l'exécutant est éteint pendant toute la fenêtre, la ligne arrive à maturité. Confirmé par les trois critiques | **non** : paiement de `R` à une clé d'autrui | de même | **non** | L'attribution est calculable si la liste des admis au tirage au sort se trouve dans le journal | Le journal vérifie lui-même l'attribution à la réception de la ligne (bon marché) |
| 1.7 | S'attribue des tâches, invente du travail | ouv. : l'exécutant est choisi par tirage au sort (cette partie est fermée), mais la règle d'approbation du plan d'apprentissage n'est pas adoptée (ROADMAP, « Ce qui n'est pas résolu », point 5) ; la répétition du contenu donne plusieurs paiements (N22). Critique DeepSeek : « fermé pour un plan fixe, ouvert pour le plan » | **non** | de même | **non** | Le nœud vérifie que la tâche figure dans le plan ; le droit d'émission et la non-répétition — non | Règle du plan dans le noyau immuable ; émission uniquement selon une place autorisée du plan ; crédit une seule fois par contenu |
| 1.8 | Prend les tâches avantageuses, abandonne les autres | lim. : une tâche abandonnée va à un autre | oui à coûts égaux ; contesté : un petit gain dû à la sélection à coûts inégaux viole-t-il D1 | lim. ; la sélection après le tirage au sort est impossible | de même | Attribution et délai dans le journal | Coût de revient égal des tâches ; le quota diminue après des abandons |
| 1.9 | Résultat calculé sur le matériel d'autrui | non-attaque (D2) | s.o. | non-attaque | s.o. | — | Distinguer de la soumission répétée du même résultat (N1, N22) |
| 1.10 | Traîne le litige ou se tait | lim. : le silence — défaite ; pour un petit `H`, la différence de frais de litige est payée par le réseau | s.o. ; contesté en cas de litige coûteux (N3) | lim. ; `H` souvent proche de zéro | de même | Minuteries des étapes dans le journal | Délais des étapes ; estimation du prix du litige |
| 1.11 | Faux avant l'arrêt du réseau | ferm. : la fenêtre n'avance pas tant que le réseau est arrêté ; le seuil n'est pas choisi | cond. | de même | cond. | Temps de la fenêtre selon les lots dont la part de poids n'est pas inférieure au seuil | Choisir le seuil (3.10) ; conserver les lignes pendant l'indisponibilité (N7) |
| 1.12 | Cache un faux en ne fournissant pas les données | ouv. pour les grandes données : « a donné ou non » le journal ne le voit pas ; pour l'apprentissage il faut l'état de l'étape précédente | **non** | ouv. ; non payé, mais déjà utilisé | **non** | Pour de petites données — publication dans la blockchain ; pour de grandes — non | Disponibilité des données avant le tirage au sort ; « pas de données dans les délais — erroné » aussi pour l'état d'apprentissage (N2, M3) |

### 3.3. Vérificateur

| № | En bref | A | D1 en A | B | D1 en B | Données pour le refus en cas de collusion | Ce qu'il faut pour fermer |
|---|---|---|---|---|---|---|---|
| 2.1 | Confirme sans recalculer | Contesté. ferm. pour un vérificateur hors coalition (quatre travaux, critiques Claude et DeepSeek) ; ouv. selon l'évaluation des travaux ChatGPT et du critique ChatGPT : au sein de la coalition, les mêmes données sont compatibles avec l'absence de recalcul | oui pour un vérificateur non lié ; au sein de la coalition — 2.2 | de même | de même | Son propre état en un point aléatoire et preuve d'inclusion ; l'origine du calcul n'est pas vérifiable | Ne pas publier les états intermédiaires au nom de la disponibilité (N11) |
| 2.2 | Paiement de la vérification de son groupe sans recalcul | lim. : environ 0,3% du revenu avec 10% de poids [calcul : 0,01·3·0,1] | **non** pour tout `q > 0` : économie du recalcul (cinq travaux, les trois critiques) | lim. si la vérification en B est payée comme en A (tarif non défini) | **non** pour le même paiement | Non : le recalcul et la copie donnent des données identiques | Ne pas payer pour une répétition ; le correctif « payer sur la récompense de la tâche vérifiée » n'annule pas le gain (section 4.5) |
| 2.3 | Collusion de l'exécutant avec tous les vérificateurs | déf. jusqu'à `q_eff ≈ 0,909` (départ — 0,875) | **non** | déf. selon la formule de la section 1.8 | **non** | Non, sauf recalcul complet ; requête privée — seulement chez l'utilisateur | Vérification indépendante de la part de collusion (étape 4), ou affaiblissement explicite de D1 (question 2) |
| 2.4 | Corruption ou pression après l'échantillon | ouv. : le vérificateur d'une requête se révèle à l'exécutant ; pot-de-vin via un contrat (N4) ; avec M1, le corrompu ne risque rien. L'abaissement a été confirmé par les trois critiques | **non** | de même ; pour `H = 0` la corruption est moins chère | **non** | Non | Requête aux vérificateurs sans contact avec l'exécutant ; conséquences de la non-révélation (M1) |
| 2.5 | Le groupe répond le premier et occupe les places | ferm. : toutes les réponses dans les délais sont comptées ; le délai n'est pas choisi | cond. | de même | cond. | Heure des réponses dans le journal | Délai du tour non plus court que le cycle journalier ; tenir compte de la croissance de `q_eff` |
| 2.6 | Un enregistrement avec du poids sans `H` confirme des faux | ferm. : admission seulement pour `H_v ≥ B` ; effet secondaire — croissance de `q_eff` (N5) | oui | ouv. : pas de règle d'admission en B | **non** : la coalition obtient `R/p` sans risque | `H` du vérificateur dans le journal (en A) | Une mesure propre de la responsabilité du vérificateur en B |
| 2.7 | Accuse faussement un exécutant honnête | ferm. sous la prémisse 4 (non construite) | cond. | de même | cond. | Recalcul de l'étape dans le journal | Machine de référence du modèle complet ; remboursement sur expiration — 2.8, 4.2 |
| 2.8 | Accuse un exécutant éteint | lim. : pour une requête privée il n'y a pas de défenseur, le `H` de l'honnête est brûlé | **non** pour la paire « utilisateur + vérificateurs » (remboursement pour une réponse correcte obtenue) ; s.o. pour un dommage pur | de même | de même | Pour l'apprentissage, tout défenseur protégera d'après l'entrée ouverte ; pour une requête privée il n'y a pas de données | Copie de la requête accessible au défenseur sans révélation |
| 2.9 | Flux de faux litiges | lim. par le coût `H` de l'attaquant | s.o. (vérification bon marché) | lim. ; en B `H` souvent 0 | s.o. | Issue du litige dans le journal | Trancher la contradiction N23 |
| 2.10 | Interception de la trouvaille d'autrui | ouv. : l'ordre n'est pas élaboré | **non** : part de l'annulation pour l'intercepteur | ouv. ; la prime en B n'est pas définie | ? | Objection cachée `hash(trouvaille ‖ clé)` avec marque du bloc | Soumission cachée avec révélation et liaison à la clé (bon marché) ; atteste la priorité de la fixation, non le moment de l'ouverture |
| 2.11 | Dénonce son propre faux pour une part de l'annulation | ferm. pour la tâche choisie ; une auto-dénonciation séparée est déficitaire | oui | prime en B non définie | ? | Le journal ne paie pas celui qui a trouvé avant la fin de la vérification désignée | Règle de prime pour B |
| 2.12 | Refuse les vérifications | lim. : le tirage au sort passe au tour suivant | s.o. ; contesté : pour `G > B` il est plus avantageux pour le désaccord de se taire (N3), dépend de l'estimation `G` | de même | de même | — | Estimation `G` ; conséquences d'une absence sans cautions |

### 3.4. Ensemble des enregistrements, poids et votes

| № | En bref | A | D1 en A | B | D1 en B | Données pour le refus en cas de collusion | Ce qu'il faut pour fermer |
|---|---|---|---|---|---|---|---|
| 3.1 | Des milliers de comptes | ferm. pour le poids et les votes ; lim. dans l'ensemble : paiements d'apprenti, distribution et attributions croissent avec le nombre de clés (critiques Claude et DeepSeek). Critique ChatGPT : le nombre de tentatives payées dépend des places attribuées, non des inscriptions | **non** | ouv. : chaque clé avec une attribution — un billet d'espérance `R·q^k` | **non** | Aucune donnée reliant les clés | Entrée sans paiements avant une vérification indépendante ; en B — admission selon `H` (N16) |
| 3.2 | Gonfle son poids par des faux ou des requêtes à soi-même | déf. jusqu'au seuil ; des faux non vérifiés ayant passé la fenêtre reçoivent du poids | **non** à la limite | ouv. : pour `H = 0` un faux choisi donne du poids presque gratuitement | **non** | Non, sauf recalcul | Poids seulement pour ce qui est vérifié indépendamment ; concilier « a passé la fenêtre » (SPEC) et « a passé la vérification » (CURRENT_DESIGN) |
| 3.3 | Loue de la puissance et accumule honnêtement du poids | ouv. dans un petit réseau : pour ¾ du poids — un mois et demi à travailler trois fois plus que les autres, pour 91% — dix fois plus [calcul SPEC] | s.o. (la location est autorisée par D2) ; mène à 2.3 et 3.7 | de même | s.o. | Non : le travail est honnête | Vérification indépendante de la part de poids ; noyau immuable (D4) |
| 3.4 | De grosses tâches que lui seul vérifiera | ferm. par la règle d'une même petite taille ; la capture de petites tâches d'un modèle rare — ligne 3.5 | oui | de même | oui | La taille de la tâche — règle du noyau | — |
| 3.5 | Capture des vérifications d'un modèle rare | ouv. : `q_eff ≈ 1` est atteignable | **non** | de même | **non** | Non | Ne pas payer pour un modèle sans seuil de vérificateurs indépendants sur un autre matériel |
| 3.6 | Enregistrements vides aux places d'apprenti | ouv. : file d'attente de débutants honnêtes ; paiement de l'apprenti pour une copie (2.2) | **non** via la copie ; s.o. pour la file d'attente | ouv. ; le budget des places est pris par celui qui a le plus de clés | **non** | Non | Ne pas payer pour une revérification d'apprenti ; délai de libération d'une place (N28) |
| 3.7 | ¾ du poids changent les règles à leur avantage | Contesté. Critiques Claude et DeepSeek : ouv. — D4 protège le noyau de vérification, mais pas l'émission, le taux, le prélèvement, le frein et le catalogue. Critique ChatGPT : lim. — D4 est prioritaire sur l'ancienne SPEC, le profit exige un changement concret | **non** (capture de l'émission), contesté | de même | de même | Empreinte du noyau : le nœud refuse une version qui modifie le noyau | Énumérer la composition du noyau (question 5) |
| 3.8 | Bloque des décisions (½ — modèle, ¼ — règles) | lim. : réversible, mais l'erreur ne peut pas être corrigée | s.o. (vivacité) | de même | s.o. | — | — |
| 3.9 | Achète des voix | lim. : il faut ¾ de tout le poids ; le pot-de-vin est exécuté par un contrat | comme 3.7 : **non** si la majorité modifie l'émission ; contesté | de même | de même | Non | Comme 3.7 |
| 3.10 | Cesse de soumettre des lots pour geler la fenêtre | ouv. : seuil élevé — gel des paiements ; seuil bas — la coalition tient la fenêtre avec ses lots, les faux arrivent à maturité (N14) | **non** (branche du seuil bas) | de même ; un faux choisi obtient `R/p` | **non** | Temps et parts de poids des lots | Seuil avec preuve des deux bornes ; distinguer le poids actif du réseau et la composition des vérificateurs |

### 3.5. Utilisateur

| № | En bref | A | D1 en A | B | D1 en B | Données pour le refus en cas de collusion | Ce qu'il faut pour fermer |
|---|---|---|---|---|---|---|---|
| 4.1 | Ne paie pas la réponse, dépense deux fois les crédits | lim. par une partie de la réponse ; la double dépense est fermée | **non** : la partie non payée — fuite positive (question 3) | de même | **non** | Fixation des crédits ; le transfert d'une partie, le journal ne le voit pas | Un échange honnête sans partie de confiance est en général impossible : réduire la partie ou reconnaître une hypothèse |
| 4.2 | Conteste une réponse correcte pour un remboursement | ouv. par deux chemins : le litige se ferme par la concordance des vérificateurs tirés au sort (N17) ; remboursement sur expiration quand l'exécutant est éteint. L'évaluation « fermé » dans trois travaux a été jugée exagérée par les trois critiques | **non** | de même | **non** | Recalcul dans le journal — seulement si le litige y est parvenu | Droit de porter le litige jusqu'au recalcul ; règle d'expiration ; défenseur avec les données |
| 4.3 | L'utilisateur et l'exécutant émettent des crédits par des requêtes | ferm. : les requêtes n'émettent pas de crédits | oui | ferm. si `R/p` est payé seulement sur les paiements des utilisateurs ; la source n'est pas consignée | cond. | Règle d'émission | Consigner la source de `R/p` en B (question 12) |
| 4.4 | Inonde le réseau de requêtes | lim. par le portefeuille | s.o. | de même | s.o. | — | — |
| 4.5 | Copie le modèle et sert hors du réseau | ouv. dans le décompte de la SPEC (fait partie des 16) | s.o. : risque pour la demande | de même | s.o. | — | — |

### 3.6. Journal, programme et communication

| № | En bref | A | D1 en A | B | D1 en B | Données pour le refus en cas de collusion | Ce qu'il faut pour fermer |
|---|---|---|---|---|---|---|---|
| 5.1 | Réécrit l'historique ou les comptes | ferm. sous la prémisse 1 | cond. | de même | cond. | Blocs définitifs via des points indépendants | Vérification formelle du programme du journal |
| 5.2 | Le nœud d'enregistrement ne transmet pas ou déforme les enregistrements | lim. pour la censure (son propre enregistrement coûte des coins de la blockchain, inaccessible à un compte vide) ; ouv. pour une ligne avec un prix ou un destinataire erroné sans objection (critiques DeepSeek et ChatGPT) | **non** | de même | **non** | Le prix et le destinataire sont vérifiables, mais pour l'instant seulement sur objection | Vérification de la ligne à la réception ; indemnisation des enregistrements sans émission (N12) |
| 5.3 | Programme falsifié pour un débutant | ouv. : adresse et référence issues d'une même source | s.o. (authenticité) | de même | s.o. | Rien avant la première installation | Sources indépendantes de l'adresse et de l'empreinte ; construction reproductible |
| 5.4 | Mise à jour malveillante | lim. : D4 permet de refuser une empreinte de noyau étrangère ; il n'y a pas de construction reproductible du programme du nœud, donc le « fermé » de la SPEC ne tient pas ; pour le reste du programme — ouv. | s.o. | de même | s.o. | Empreinte dans le journal sans lien vérifiable avec la source | Construction reproductible ; la concordance avec le texte approuvé ne prouve pas sa sûreté |
| 5.5 | Paiement d'un stockage inexistant ou d'une distribution à soi-même | ferm. : rien n'est émis pour le stockage | oui | de même | oui | Règle d'émission | — |
| 5.6 | Prend le paiement, ne livre pas les données | lim. par une partie | **non** : fuite d'une partie chez le destinataire sans reçu (question 3) | de même | **non** | Empreinte de la partie ; le reçu confirme le paiement, non la livraison | Comme 4.1 |
| 5.7 | Bloque tous les chemins de rencontre | ouv. en cas de blocage de tous les chemins | s.o. (distribution) | de même | s.o. | — | — |
| 5.8 | Encercle le nœud d'un faux état | lim. par la confiance en deux fournisseurs sur trois ; en cas de leur collusion — ouv. (N29) | cond. | de même | cond. | Bloc définitif via des points indépendants | Client léger avec vérification du consensus |
| 5.9 | Divise le réseau pour deux paiements | ferm. : un seul journal | oui | de même | oui | Numéro de la tâche dans un seul journal | Scission des règles — N15 |
| 5.10 | Vole une clé de travail | lim. : la clé ne dépense pas les crédits du portefeuille | Contesté : s.o. (dommage à la victime) ou **non** — les clés volées confirment des faux au détriment du `H` d'autrui (N9, soutenu par le critique Claude) | de même | de même | La signature ne montre pas l'opérateur | Révocation de la clé ; stockage matériel |
| 5.11 | Épuise la distribution gratuite | ouv. : si cela suffira aux débutants, non vérifié | s.o. (refus de service) ; contesté si l'avantage est défini comme « au premier arrivé » | de même | de même | Un nouveau propriétaire est indiscernable d'une nouvelle clé de l'ancien | Distribution seulement selon des tâches déjà attribuées |

### 3.7. Modèle et apprentissage

| № | En bref | A | D1 en A | B | D1 en B | Données pour le refus en cas de collusion | Ce qu'il faut pour fermer |
|---|---|---|---|---|---|---|---|
| 6.1 | Un saboteur soumet des contributions erronées | lim. : environ `x/3` contributions pour une part de travail `x` [calcul SPEC] ; en cas de collusion totale non démontré ; la contribution agit immédiatement (N21) | s.o. pour les crédits ; non (eff.) | ouv. : un faux non choisi est gratuit, la limite `x/3` ne s'applique pas (critiques Claude et ChatGPT) | **non** | Non, sauf recalcul | Ne promouvoir que des contributions vérifiées (coût — latence et mémoire) |
| 6.2 | Comportement caché | ouv. : l'examen attrape une dégradation, pas une porte dérobée | non (eff.) | de même | non (eff.) | Non ; une porte dérobée est possible même avec une étape correcte | Tâche de recherche |
| 6.3 | Jeu de données nuisible ou licence d'autrui | ouv. : un calcul correct sur des données nuisibles ne se corrige pas | s.o. ; non (eff.) | de même | de même | Non : le hachage et la mention sont identiques chez le titulaire des droits et chez un tiers | Limiter le catalogue à des sources vérifiables |
| 6.4 | Ajustement à l'examen | lim. : les tâches sont choisies après la fixation | non (eff.) dans les limites de ce qui n'est pas mesurable | de même | de même | Moment du choix des tâches | — |
| 6.5 | Falsification des résultats de l'examen | déf. jusqu'au seuil 2.3 ; l'examen est toujours vérifié, sans loterie | **non** pour un `q` élevé | comme en A ; la formule `R·q^k` n'est pas applicable à l'examen (section 4.5) | **non** | L'examen est petit et ouvert : chaque nœud peut le recalculer lui-même | Recalcul de l'examen par chaque nœud (recommandé par le critique DeepSeek ; critique ChatGPT : prix et caractère obligatoire non établis) |
| 6.6 | Capture du vote sur le plan | lim. : propriété du schéma | s.o. ; **non** en liaison avec 1.7 | de même | de même | Non | Voir 1.7 |

### 3.8. Confidentialité

| № | En bref | A | D1 en A | B | D1 en B | Données pour le refus en cas de collusion | Ce qu'il faut pour fermer |
|---|---|---|---|---|---|---|---|
| 7.1 | Le propriétaire de l'appareil lit les requêtes | ouv. en mode ordinaire | s.o. ; non (eff.) — atteinte à la vie privée | de même | de même | Non | Mode protégé au prix de la confiance dans le fabricant (N25) |
| 7.2 | Collecte massive des requêtes d'autrui | lim. par la part des attributions et des places de vérification | s.o. ; non (eff.) | de même | de même | — | — |
| 7.3 | Liaison des requêtes de l'utilisateur | ouv. : pseudonyme et adresses chez le relais | s.o. | de même | s.o. | — | Paiement non liable |
| 7.4 | Lecture d'une requête via la vérification ou le litige | ouv. : environ 1% des requêtes sont vues par trois appareils de plus ; un faux litige publie un fragment | s.o. ; non (eff.) | de même ; la part `p` ne limite pas la révélation — le litige est ouvert par l'utilisateur | de même | — | Litige sans révélation (preuve à divulgation nulle de l'étape) |

### 3.9. Nouvelles attaques trouvées par le conseil

Les doublons de différents travaux sont fusionnés. « Travaux » — combien des six travaux du tour 1 ont identifié l'attaque ;
« Critiques » — conclusion du tour 2. Les numéros N1… sont propres à ce document et ne coïncident pas avec les numéros locaux
des travaux. Il n'y a pas de nouvelles attaques réfutées ; là où la justification est réfutée, cela est dit.

| № | Attaque | Travaux | Critiques | A · D1 | B · D1 | Ce qu'il faut pour fermer |
|---|---|---|---|---|---|---|
| N1 | **Un calcul — plusieurs paiements.** La clé de la coalition recalcule une fois la tâche d'autrui (même honnête) et distribue l'étape à toutes ses clés tirées comme vérificateurs ou apprentis pour cette tâche. Généralise 2.2 : la collusion avec l'exécutant n'est pas nécessaire | 1 | Confirmé par les trois ; l'avantage croît avec le nombre de places payées attribuées, non avec les clés | ouv. · **non** | ouv. · **non** | Pas de données. Aucun paiement ne doit dépendre de la répétition d'un travail déjà fait |
| N2 | **Famine des vérificateurs honnêtes en données.** Le vérificateur prend la requête chez l'exécutant et se révèle ; l'exécutant de la coalition ne donne la requête qu'aux siens ; l'honnête « n'a pas reçu » ne répond pas et ne perd rien ; les tours vont jusqu'à ce que trois réponses de la coalition soient réunies | 1 (partiellement aussi 3) | Exact avec réserve : il faut environ `3/(λ·q)` tours journaliers — environ 15 jours pour `q = 5%`, `λ ≈ 4`, environ 75 jours pour `q = 1%` [calcul], l'attaque se remarque dans le journal. Le mécanisme « publication d'une copie chiffrée » est nommé dans la SPEC, mais non défini. Pour l'apprentissage — seulement avec un unique exemplaire de l'entrée | ouv. · **non** pour les requêtes | ouv. · **non** | Le journal ne voit pas la transmission. Disponibilité des entrées avant le tirage au sort ; pour une requête privée il n'y a pas de solution ; voir M3 |
| N3 | **Litige plus cher que l'enjeu.** Le jeu du litige dans le pilote — 93 transactions, 5,8–6,3 millions de gas : environ 18 $ à 1 gwei et 3000 $ par ETH, environ 360 $ à 20 gwei [calcul ; les prix sont des hypothèses]. La répétition de la ligne — 14,1 millions de gas, autre prototype, on ne peut pas additionner | 1 (aussi 3 de façon proche) | Exact comme dilemme, les nombres sont conditionnels : soit la partie de droite supporte `G − B`, et l'honnête en désaccord se tait ; soit le réseau rembourse `G` (ainsi se lit 1.10 de la SPEC), et le saboteur force le réseau à payer `G` pour chaque faux attrapé | ouv. · **non** | ouv. · **non** | Estimation `G` pour la chaîne choisie ; tâches dont une erreur exige un litige — seulement pour `H ≥ G` |
| N4 | **Pot-de-vin « P+ε » :** le contrat paie ε au vérificateur pour une confirmation et promet de rembourser `H_v` en cas de prise. Sous-variante de 2.4 | 1 | Critique DeepSeek : substantielle ; critique ChatGPT : exécutabilité et équilibre non démontrés | ouv. · **non** | ouv. · **non** | Une vérification où l'accord ne décide rien ; voir M1 |
| N5 | **Croissance de `q_eff` via l'admission `H_v ≥ B` :** 42,1% du poids global donnent 88,9% parmi les admis (section 1.7) | 2 | Confirmé ; seulement pour les tâches avec `B = 399R` | lim. · **non** en cas de capture | ouv. (2.6) | Calculer les bornes selon `q_eff` ; calculer le compromis entre la taille de l'annulation et la largeur du tour |
| N6 | **Le poids disparaît après 30 jours calendaires d'arrêt :** la fenêtre est à l'arrêt, le poids est calculé « sur 30 jours » ; le premier groupe revenu obtient tout le poids | 1 | Exact selon la lettre de la SPEC, mais conditionnel : temps calendaire ou actif n'est pas dit ; à poids nul de tous le tirage au sort n'est pas défini | ouv. · **non** | ouv. · **non** | Calculer le poids selon le temps actif du réseau (bon marché) et définir l'attribution initiale |
| N7 | **Les lignes des lots vivent environ 18 jours, la fenêtre peut rester plus longtemps :** après l'indisponibilité il reste une racine sans lignes, il n'y a rien pour contester | 3 | Confirmé par tous | ouv. · ? | ouv. · ? | Conserver les lignes et les motifs de transition pendant toute la durée de la vérification et du litige ; sans données, l'écriture contestée attend |
| N8 | **Son propre modèle dans le catalogue donne `q = 1` :** un modèle que seul le matériel de la coalition utilise | 1 | Critique ChatGPT : c'est une combinaison de 1.7, 3.5 et 6.6 ; que une petite part de poids fasse entrer un modèle dans le catalogue n'est pas démontré | ouv. · **non** | ouv. · **non** | Ne pas payer pour un modèle sans cercle minimal de vérificateurs sur un autre matériel |
| N9 | **Les appareils d'autrui comme poids de vérificateurs gratuit :** des clés de travail volées confirment des faux, le `H` des victimes brûle. Extension de 5.10 | 1 | Confirmé ; l'accroissement de `q` — selon le poids des clés capturées, non le nombre d'appareils | ouv. · **non** | ouv. · **non** | Stockage matériel de la clé ; prise en compte du piratage dans le `q` admissible |
| N10 | **La soumission instantanée de faux augmente le flux d'attributions** (B) | 1 | Conditionnel : une croissance de 10 à 100 fois ne découle pas des règles de la SPEC | lim. · oui | ouv. · **non** | Rythme des attributions seulement selon le travail vérifié |
| N11 | **Disponibilité contre 2.1 :** la publication d'états intermédiaires pour N2 permet de confirmer sans recalcul | 1 | Limitation du changement proposé, non attaque autonome | — | — | Publier seulement les entrées, les intermédiaires — dans le litige |
| N12 | **Paiement pour l'enregistrement dans le journal au-delà des coûts :** indemnisation d'enregistrements inutiles ou cartel de nœuds d'enregistrement | 2 | La règle d'indemnisation n'est pas définie dans la SPEC ; le revenu ordinaire d'un intermédiaire ne viole pas D1 | ouv. · cond. | ouv. · cond. | Indemniser seulement les enregistrements avec des résultats acceptés et pas au-delà de la commission réelle |
| N13 | **Choix par la dernière source d'aléa :** si le tour de la balise est connu avant le bloc décisif, son producteur choisit entre deux valeurs ; en A `p → p²`, gain d'environ +0,96R par faux [calcul]. Critique Claude : avec un calendrier de producteurs connu à l'avance, la coalition soumet des lots pour ses propres blocs | 4 | Confirmé par tous ; les nombres — seulement en cas d'ordre erroné des sources | ouv. · **non** en cas d'ordre erroné | de même | Tour de balise strictement après l'acceptation définitive du bloc |
| N14 | **La fenêtre avance sans majorité :** une coalition de 40%, avec la coupure de la moitié des honnêtes, obtient 40/70 = 57% parmi les actifs [calcul]. Sous-variante de 3.10 | 2 | Confirmé comme sous-variante de 3.10 | déf. · **non** pour les fuites de type B | ouv. · **non** | Voir 3.10 |
| N15 | **Scission des règles :** les sommes non arrivées à maturité arrivent à maturité dans deux branches | 1 | Conditionnel : le doublement d'un même engagement n'est pas démontré | ouv. · ? | ouv. · ? | Contrat séparé avec séparation des soldes |
| N16 | **En B, la retenue est liée à la clé, mais l'accès aux tâches ne l'est pas :** des faux depuis une clé vide séparée donnent `R·q^k` sans pertes. Racine commune 1.1-B, 1.2-B, 1.3-B, 3.1-B | 2 + critique Claude | Deux travaux ont justifié la faille par le fait que, chez un participant ordinaire de B, `H = 0` dans 23,5–54,7% des fenêtres ; cet argument a été réfuté (section 4.5). La forme correcte a été donnée par le critique Claude | — | ouv. · **non** | Admission aux billets pour `H` non inférieur au paiement attendu pour un faux ; alors B perd la part de vérification constante et basse (question 8) |
| N17 | **Le litige de l'utilisateur est tranché par l'échantillon, non par l'arithmétique :** le litige est fermé si les vérificateurs tirés au sort ont concordé avec l'exécutant | 1 | Confirmé par les critiques Claude et DeepSeek ; critique ChatGPT : exact, mais 4.2 porte sur une prétention opposée | ouv. · **non** | ouv. · **non** | Droit de porter le litige jusqu'au recalcul dans le journal |
| N18 | **Faux → poids → `q`.** Extension de 3.2 | 1 | Confirmé ; la conclusion monétaire exige la prise en compte des paiements futurs | lim. · **non** à la limite | ouv. · **non** | Poids seulement pour ce qui est vérifié indépendamment |
| N19 | **Déchets de clés gratuites avant l'attribution** surchargent les nœuds et les files d'attente | 4 | Confirmé ; une place pour un débutant honnête n'est garantie dans aucune variante. L'évaluation « les déchets coûtent au réseau 3–4,5 de travail pour des coûts presque nuls en A » a été réfutée par le critique Claude | ouv. · s.o. | ouv. · **non** en liaison avec des billets gratuits | Rejeter les messages sans attribution avant un traitement coûteux ; le chemin depuis un compte vide est obligatoire |
| N20 | **Divergence imposée des arithmétiques** de l'exécutant et de l'arbitre | 2 | Confirmé ; la divergence elle-même ne prouve pas un gain | ouv. · ? | ouv. · ? | Sémantique exécutable unique des opérations et vérification des implémentations d'après la référence |
| N21 | **Utilisation du résultat avant vérification :** la réponse est lue, l'étape est prise comme étape suivante et reste dans la généalogie du modèle | 5 (+1 en 6.1) | Confirmé par tous ; le dommage est possible même pour `q = 0` ; `1 − p` — part des non choisis, non des appliqués | ouv. · non (eff.) | ouv. · non (eff.) | Vérifier le bloc avant de le délivrer ; ne promouvoir qu'un descendant vérifié (coût — latence et mémoire) |
| N22 | **Un même droit d'émission sous différents numéros** (courses d'essai identiques, répétition d'une étape après redémarrage) | 3 | Confirmé ; deux commandes légitimes peuvent avoir une sortie identique | ouv. · **non** | ouv. · **non** | Crédit une seule fois par droit canonique à une place du plan |
| N23 | **Contradiction des règles de litige depuis un compte vide** (ROADMAP l'exige, SPEC — non) | 1 | Confirmé par les critiques DeepSeek et ChatGPT | ouv. · s.o. | ouv. · s.o. | Décision du propriétaire (question 4) |
| N24 | **Attribution de la tâche d'un exécutant éteint** — dépliage de 1.6 | 2 | Confirmé | voir 1.6 | voir 1.6 | Vérification de l'attribution à la réception de la ligne |
| N25 | **Collusion avec le fabricant du mode protégé** | 1 | Exact dans les limites de 7.1 | ouv. · s.o. | ouv. · s.o. | Consigner l'hypothèse de confiance dans le fabricant |
| N26 | **Faux reçus de transmission de données** | 1 | Pas de revenu externe : la coalition se paie elle-même | ouv. · s.o. | ouv. · s.o. | Il n'y a pas d'indice de livraison de grandes données |
| N27 | **Livraison sélective par un relais** | 1 | Confirmé pour la disponibilité | lim. · s.o. | lim. · s.o. | Plusieurs relais, chemins de secours |
| N28 | **« L'apprenti éternel »** occupe une place et n'achève pas la revérification (vers 3.6) | 1 | Confirmé | ouv. · s.o. | ouv. · s.o. | Délai et libération automatique de la place |
| N29 | **Collusion de deux fournisseurs de point de contrôle sur trois** (vers 5.8) | 1 | Confirmé ; « plus de fournisseurs » ne résout pas la collusion de la majorité requise | lim. · cond. | lim. · cond. | Client léger avec vérification du consensus |
| N30 | **Un bloc différent du bloc fixé est délivré à l'utilisateur** | 1 | Confirmé | ouv. · ? | ouv. · ? | Lier le bloc délivré à l'engagement et le vérifier avant usage |
| N31 | **Une erreur commune dans le noyau lui-même** fait accepter une transition erronée par tous les nœuds | 1 | Confirmé ; différent de N20 | ouv. · ? | ouv. · ? | Spécification indépendante de la transition ; selon D4 la correction — seulement par passage à un nouveau réseau |
| N32 | **Reconnaissance d'une courte requête privée par son empreinte publique** | 2 | Confirmé conditionnellement : hachage déterministe et petit ensemble de textes | ouv. · non (eff.) | de même | Engagements masquants avec aléa frais |

**Trouvées seulement par les critiques** (non vérifiées par d'autres participants) :

| № | Attaque | Qui | A · D1 | B · D1 | Ce qu'il faut pour fermer |
|---|---|---|---|---|---|
| M1 | **Refus gratuit de révélation.** Les vérificateurs de la coalition soumettent un « je confirme » caché et ne le révèlent que si toutes les réponses soumises sont les leurs ; sinon ils se taisent et ne perdent rien. La corruption d'un vérificateur extérieur devient sans risque : au lieu du risque `399R` — zéro [calcul]. Condition : si les réponses cachées sont visibles avant révélation — non défini dans la SPEC | critique Claude | ouv. · **non** | ouv. · **non** | Conséquences de la non-révélation sans cautions (perte du paiement et du poids pour le tour) ou masquage du nombre et de l'auteur des réponses ; le coût pour les honnêtes éteints n'est pas calculé |
| M3 | **Charge via le mécanisme de disponibilité.** Si à « n'a pas reçu » on répond par une publication obligatoire d'une copie, le vérificateur de la coalition déclare toujours « n'a pas reçu » ; pour `q = 10%`, `λ ≈ 4` cela fait environ 34% des tâches choisies [calcul] | critique Claude | ouv. · s.o. | de même | La déclaration de non-livraison doit coûter au déclarant au moins la publication provoquée (sur son `H`) |
| M4 | **Panne et tromperie sous une même règle d'annulation :** la cause d'une même sortie erronée ne se vérifie pas | critique ChatGPT | ? | ? | Une règle équitable pour les deux parties n'est pas présentée (question 11) |

(M2 du critique Claude — c'est N16.)

---

## 4. Bilan

### 4.1. Combien d'attaques violent D1

Décompte selon le tableau des sections 3.2–3.8 [calcul d'après le tableau]. Les lignes marquées « contesté » sont incluses
et nommées séparément.

| | Variante A | Variante B |
|---|---|---|
| Gain monétaire (« **non** »), sur 60 lignes | 24 (et encore 2 conditionnellement : 1.5 en cas d'ordre erroné des sources, 6.6 en liaison avec 1.7) : 1.1, 1.2, 1.3, 1.6, 1.7, 1.12, 2.2, 2.3, 2.4, 2.8, 2.10, 3.1, 3.2, 3.5, 3.6, 3.7*, 3.9*, 3.10, 4.1, 4.2, 5.2, 5.6, 5.10*, 6.5 | 25 : les mêmes sans 2.10 (en B « ? »), plus 2.6 et 6.1 (et les mêmes 2 conditionnellement) |
| Gain uniquement par effet (« non (eff.) ») | 7 : 6.1, 6.2, 6.3, 6.4, 7.1, 7.2, 7.4 | 6 : les mêmes sans 6.1 |
| Nouvelles attaques avec un « **non** » monétaire (N1–N32, M1) | 14 | 16 |

Les lignes contestées sont marquées d'un astérisque (3.7, 3.9, 5.10). Sans elles, il reste 21 en A, 22 en B.
Le nombre de lignes ne peut pas être additionné comme un nombre de façons indépendantes de tromper : un même schéma est souvent décrit
par plusieurs lignes. La conclusion principale ne dépend pas du décompte : **D1 dans sa forme littérale n'est satisfait
ni par la variante A ni par la variante B**, et les six travaux et les trois critiques en conviennent.

**Comparaison de A et B.** B telle que décrite est pire que A pour des `H` vides et bas avec `0 < q < 0,909` :
une clé vide obtient `R·q^k` par tentative sans pertes (N16). Pour `q = 0`, B est meilleure : un faux non choisi
ne rapporte rien, même en cas de départ. Pour `q ≥ 0,909`, les deux perdent. Si l'on transfère en B
le chemin du débutant de A (vérification complète des premières tâches), la différence sur les clés vides disparaît
(`q^k R − (1 − q^k)·3R`, comme en A [calcul]), mais B perd la part de vérification constante et basse.
C'est une entrée pour la décision D3 à l'étape 2, non la décision elle-même.

### 4.2. Points critiques pour le lancement du réseau avec de vrais crédits

Résumé des évaluations des travaux et des critiques. Un démarrage fermé sur des crédits d'apprentissage ne bloque pas ces points,
sauf la vie privée, la restauration (N6, N7) et les points sans lesquels le pilote ne vérifie pas ce qu'il
doit vérifier (N2, N3).

1. **Collusion selon `q_eff` :** 1.1, 1.2, 1.3, 2.3, 3.2, 3.5, 6.5 et N5. Dans les deux variantes l'acceptation
   repose sur l'accord de l'échantillon des participants.
2. **Paiement de la répétition :** 2.2, 3.6, N1. Viole D1 pour tout `q > 0` ; aucun correctif bon marché n'a été trouvé.
3. **Clés vides en B :** N16, 1.1-B, 3.1-B.
4. **Droit d'émission et destinataire :** 1.7, 1.6, 5.2, N22, ainsi que 3.7 pour l'émission hors du noyau.
5. **Disponibilité des données :** 1.12, N2, N7.
6. **Litiges :** 4.2 et N17 ; prix du litige N3, lié à lui 2.12 ; contradiction N23 ; M1.
7. **Utilisation avant vérification :** N21, 6.1, N30 (si le propriétaire inclut l'effet dans D1).
8. **Restauration :** N6 (poids après l'arrêt) et N7 (lignes des lots).
9. **Entrée et programme :** 5.3, 5.4, N19.
10. **Vie privée :** 7.1, 7.4, N32 — violent une condition obligatoire indépendamment de l'argent.

### 4.3. Racine commune

Dans les deux variantes, l'acceptation ordinaire d'un résultat repose sur l'accord d'un échantillon aléatoire de participants,
c'est-à-dire sur des signatures qui, en cas de collusion, ne prouvent rien. C'est pourquoi la limite de protection s'exprime toujours
par la part de collusion `q_eff`, et `q_eff` peut être augmenté par la location de puissance, la capture d'un modèle
rare, la règle d'admission selon `H` (N5), la famine en données (N2), des clés volées (N9) ou
un long arrêt (N6). Les données vérifiables indépendamment en cas de collusion totale — seulement l'entrée et le modèle,
d'après lesquels le nœud peut recalculer lui-même la tâche ; ni A ni B ne l'exigent, et pour une requête privée
le nœud n'a même pas l'entrée. D1 n'est atteignable que par une vérification qui ne dépend pas de la part de collusion
(étape 4 [ROADMAP](ROADMAP.md)), ou par un affaiblissement explicite de D1 jusqu'à « pour `q < q*` » décidé par le propriétaire.

### 4.4. Correctifs bon marché confirmés par les critiques

| Correctif | Ferme | Réserve |
|---|---|---|
| Le journal vérifie lui-même l'attribution, le prix et le destinataire de la ligne à la réception, et non sur objection | 1.6, 5.2, N24 | La liste des admis au tirage au sort doit se trouver dans le journal |
| Crédit une seule fois par droit canonique à une place du plan et par empreinte du contenu | N22, partie de 1.7 | Deux commandes légitimes peuvent donner une sortie identique ; la faille principale de 1.7 — la règle du plan — reste |
| Soumission cachée de l'objection avec révélation et liaison à la clé | 2.10 | Atteste la priorité de la fixation, non le moment de l'ouverture |
| Calculer le poids et la fenêtre selon le temps actif du réseau, non selon le calendrier | N6 | Il faut une règle d'attribution initiale après l'arrêt |
| Tour de balise strictement après l'acceptation définitive du bloc | 1.5 (partie), N13 | Les sources ne sont pas encore choisies |
| Chaque nœud recalcule lui-même l'examen avant d'accepter la version | 6.5 | Recommandé par un critique ; prix et caractère obligatoire pas encore établis |
| Corriger le résumé de CURRENT_DESIGN : 60 = 18 + 6 + 19 + 16 + 1 | Rapprochement 59/60 | — |

### 4.5. Conclusions réfutées

Ces affirmations des travaux du tour 1 ont été reconnues erronées par les critiques ; elles n'ont pas été reportées dans le tableau.

| Affirmation | Où | Pourquoi c'est faux |
|---|---|---|
| Seuil de rentabilité d'un faux en B `q^k > H/(H+R)` | un travail DeepSeek | Le facteur `p` est perdu. Correct : `q^k > pH/(R+pH)`. Pour `p = 1%`, `H = 400R`, `q = 0,95` : gain `0,857R`, perte attendue `0,01·0,143·400R = 0,572R`, total +0,285R par faux, alors que selon la formule erronée — une perte [calcul]. L'erreur surestime la protection presque jusqu'au maximum (0,999 au lieu de 0,93) |
| Le seuil de 90,9% du débutant A « est correct sous l'hypothèse que les 3R ont été accumulés par la collusion » | le même travail | Le seuil ne dépend pas de la manière dont les `3R` ont été obtenus |
| La falsification de l'examen en B donne `R·q^k` | les deux travaux DeepSeek | L'examen est toujours vérifié, sans loterie ; la formule de loterie ne lui est pas applicable |
| Le correctif 2.2 « payer les vérificateurs sur la récompense de la tâche vérifiée » annule le gain | un travail Claude | Celui qui copie économise toujours le recalcul ; contre l'inaction le gain est aussi positif ; la copie sur une tâche honnête d'autrui (N1) n'est pas touchée par le correctif. Il ne supprime que l'émission de crédits pour une vérification vide |
| « Chez un participant ordinaire de B, `H = 0` dans 23,5–54,7% des fenêtres, et pendant ce temps un faux ne menace rien » | les deux travaux Claude | Les nombres `0,99^60 ≈ 54,7%`, `0,99^144 ≈ 23,5%`, `0,99^432 ≈ 1,3%` sont exacts, mais c'est la part des fenêtres après le fait. Le `H` brûle au moment de la prise, y compris les gains arrivés après la soumission. La conclusion sur la faille est exacte pour une autre raison — via la clé vide (N16) |
| D1 se vérifie en comparant à la plus grande des deux bases | un travail Claude | Manque le cas d'un gain positif contre l'inaction (exemple section 1.5) |
| « Les déchets coûtent au réseau 3–4,5 de travail pour des coûts presque nuls de l'attaquant » (variante A) | un travail Claude | En A la clé ne reçoit des tâches que pour `H ≥ 3R`, et chaque résultat inutile brûle ces `3R` ; il n'y a pas d'amplification multiple. L'amplification n'existe qu'en B sans admission selon `H` |
| Statuts corrigés dans le tableau : 2.6-B « fermée » (travaux DeepSeek et Claude) ; 1.7 « fermée / oui », 1.6 et 4.2 « fermées / oui », 4.1 et 5.6 « D1 oui », 2.2 « ne viole pas D1 » (travaux DeepSeek, en partie Claude) ; 3.4 « non », 2.7 « ouverte / non », 5.11 « non » (travaux ChatGPT) | différents | Justifications — dans les lignes correspondantes du tableau : il n'y a pas de règle d'admission en B ; la règle du plan est ouverte ; la vérification de l'attribution et le litige de l'utilisateur donnent un gain ; D1 interdit une fuite limitée ; le gain en 3.4 et 2.7 est pris aux lignes voisines ; il n'y a pas d'avantage personnel dans la SPEC |
| 1.3 : gain 1,034·H₀ au point 0,875 | un travail Claude | 1,034·H₀ se rapporte au point 0,880 ; en 0,875 — 1,00004·H₀ |

Restent contestées (non réfutées) les évaluations 2.1 « ouverte » dans les deux travaux ChatGPT et 3.7
« limitée » : les critiques ont divergé (lignes 2.1 et 3.7 du tableau).

---

## 5. Questions au propriétaire

Décisions sans lesquelles l'étape 1 ne peut pas être fermée. Le conseil ne les prend pas. Les douze questions ont toutes été tranchées le 24 novembre 2026 sur instruction du propriétaire (décisions D6–D17 dans [ROADMAP](ROADMAP.md), section 3).

1. **L'effet entre-t-il dans D1 ?** *(Tranché — D6 : oui.)* Un travail a proposé de distinguer D1 économique (crédits seulement)
   et D1 par effet (influence sur la réponse et le modèle, lecture de la requête, le mal lui-même). Les mots « le fraudeur
   n'obtient pas ce qu'il veut » au sens littéral incluent l'effet ; alors l'utilisation du résultat
   avant vérification (N21) viole D1 dans les deux variantes pour tout `q`, et on ne peut la fermer que par une
   vérification avant délivrance et promotion (coût — latence et mémoire).
2. **Exiger une vérification indépendante de la part de collusion, ou affaiblir D1 jusqu'à « pour `q < q*` » ?** *(Tranché — D7 : une vérification indépendante de la part de collusion est exigée.)*
   Sans l'un des deux, D1 est inatteignable ni en A ni en B.
3. **Fuite d'une partie lors de l'échange** *(Tranché — D10 : violation de D1 ; échange d'une seule entrée du journal.)* (4.1, 5.6) : un échange honnête sans partie de confiance en général
   est impossible. La reconnaître comme hypothèse explicite ou la considérer comme une violation de D1 ?
4. **Litige depuis un compte vide** *(Tranché — D8 : seulement les vérificateurs désignés et l'utilisateur pour sa propre requête.)* (N23) : ROADMAP l'exige, SPEC — non. Par quoi alors limiter le flux
   de faux litiges sans cautions ?
5. **Composition du noyau immuable** *(Tranché — D11 : vérification, paiement de ce qui est vérifié, émission, litige et règles du journal ; le reste dans les limites.)* (3.7) : y entrent la règle d'émission, le taux, le prélèvement réseau,
   le frein et le catalogue, ou seulement la vérification ?
6. **Règle d'approbation du plan d'apprentissage** *(Tranché — D9 : le plan est dérivé par une règle du catalogue et de l'examen.)* (1.7, ROADMAP « Ce qui n'est pas résolu », point 5) : qui et comment
   autorise une tâche à émettre des crédits.
7. **Temps pour le poids et la fenêtre** *(Tranché — D12 : temps actif du réseau.)* (N6) : temps calendaire ou temps actif du réseau.
8. **Admission aux tâches en B** *(Tranché — D13 : oui, le chemin du débutant de la variante A.)* (N16) : introduire en B une dépendance de l'accès à `H`, en sachant qu'alors
   B perd la part de vérification constante et basse. C'est une entrée pour D3.
9. **Prix du litige** *(Tranché — D14 : le réseau de second niveau le moins cher ; la différence est payée par le prélèvement réseau.)* (N3) : quelle chaîne considérer pour l'estimation `G` et qui supporte la différence `G − B` —
   la partie de droite ou le réseau.
10. **Faut-il payer pour une revérification répétée et pour les revérifications d'apprenti** *(Tranché — D15 : un simple recalcul, qui peut être copié, n'est pas payé.)* (2.2, N1), si une copie est indiscernable
    d'un recalcul ?
11. **Panne matérielle honnête :** *(Tranché — D16 : non ; la tâche n'est pas payée, la somme en attente ne brûle pas.)* l'annuler comme une tromperie.
12. **Source du paiement `R/p` en B pour les requêtes** *(Tranché — D17 : seulement sur les paiements des utilisateurs.)* (4.3) : seulement sur les paiements des utilisateurs ou avec émission.

---

## 6. Qui a fait quoi

Le conseil de modèles a travaillé sur les matériaux du projet, sans accès au réseau et sans expériences.

- **Tour 1, six travaux indépendants :** deux travaux ChatGPT, deux travaux DeepSeek, deux travaux
  Claude. Chacun a établi un modèle de l'adversaire, un rapprochement des 60 lignes, les statuts pour les variantes A et B,
  les données pour le refus et de nouvelles attaques.
- **Tour 2, trois critiques :** un de ChatGPT, un de DeepSeek et un de Claude. Chaque critique a lu les six
  travaux, vérifié les affirmations avec les documents sources, recalculé les formules à la main et indiqué
  les divergences et les erreurs.
**Synthèse :** ce document a été établi par Claude d'après les travaux et les critiques. Là où les critiques divergeaient,
  le tableau porte « contesté » ; aucune évaluation nouvelle propre n'a été ajoutée lors de la synthèse.
