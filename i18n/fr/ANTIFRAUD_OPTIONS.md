<!-- translation of docs/ANTIFRAUD_OPTIONS.md, source sha256: 63c43d6864c5cccb6fa61953c9ba9594e26e3dba1a4c8241129e6f346bc08f20 -->

# Options de lutte contre la tromperie : bilan des audits et du conseil des modèles

[English](../../docs/ANTIFRAUD_OPTIONS.en.md) · [中文](../zh/ANTIFRAUD_OPTIONS.md) · [Español](../es/ANTIFRAUD_OPTIONS.md) · **Français** · [Deutsch](../de/ANTIFRAUD_OPTIONS.md) · [Italiano](../it/ANTIFRAUD_OPTIONS.md) · [Русский](../../docs/ANTIFRAUD_OPTIONS.md) · [Português](../pt/ANTIFRAUD_OPTIONS.md) · [العربية](../ar/ANTIFRAUD_OPTIONS.md)

État au 27 novembre 2026.

**Ce qui a été fait.** Le propriétaire du projet a réuni six audits indépendants de complétude et deux cartes
des mécanismes de protection contre la tromperie, et a proposé trois idées personnelles : intégrer la
vérifiabilité dans le modèle lui-même, reprendre des procédés issus des jeux et « croiser » les voies de
contournement de la vérification avec un travail utile. Le conseil des modèles a rédigé onze travaux
indépendants et quatre critiques croisées, et a consolidé tout cela en variantes décrites ci-dessous.

**Statut.** Ce document est un raisonnement et un calcul. Les grandeurs mesurées proviennent uniquement de
l'expérience D5 ([EXPERIMENT_D5](EXPERIMENT_D5.md)) et sont marquées [mesuré]. Tout le reste est marqué
[calcul] ou appelé hypothèse. Seules les décisions D1–D25 restent des décisions acceptées ([ROADMAP](ROADMAP.md),
section 3) ; tout ce que l'on propose ici de changer est une proposition du conseil, non une décision. Le
conseil n'a réalisé ni nouvelles expériences, ni prototypes, ni installations. La littérature est citée de
mémoire des modèles ou d'après les données des audits et n'a pas été confrontée aux sources primaires.
Synthèses précédentes : [STRATEGY_SEARCH](STRATEGY_SEARCH.md) et [HIDDEN_DETECTOR](HIDDEN_DETECTOR.md).

**Notations.** `R` — prix de la tâche ; `c` — coût de revient du travail honnête dans le profil exact
(entier) ; `c_f` — coût de la falsification pour le trompeur ; `H_lock` — somme verrouillée non arrivée à
maturité de la clé ; `p` — probabilité de vérification de la réponse ; `q` — part de poids de la coalition
parmi les vérificateurs désignés ; `ρ` — temps de vérification d'une réponse prête en une passe, en fractions
du temps de sa génération exacte : 0,10–0,40 avec un lot de 1 et 0,26–0,64 avec un lot de 8 [mesuré] ; `γ` —
ralentissement du profil exact par rapport au Q8_0 ordinaire : 1,52–1,78 avec un lot de 1 et 2,47–2,79 avec
un lot de 8 [mesuré, seulement RTX 2060].

## Bref bilan

1. **Ce qui coûte cher n'est pas de vérifier, mais de calculer exactement.** La vérification d'une réponse
   coûte 10–40 % de sa génération [mesuré], mais la surcharge principale est le ralentissement du profil exact
   d'un facteur 1,52–1,78 [mesuré]. Le repère « environ 5 % » est, avec les noyaux actuels, inatteignable dans
   aucune variante, aussi rare que soit la vérification [calcul].
2. **L'idée « empreintes et recalcul d'un morceau aléatoire » fonctionne, mais non comme un allègement du coût
   de la garantie.** Si l'on ouvre `s` morceaux sur `N`, une cellule substituée de manière ciblée passe avec
   une probabilité d'au moins `1 − s/N`. L'estimation « 30 fois moins cher, et la tromperie est toujours
   détectée » signifie en réalité « 30 fois moins de détections ». Les empreintes sont utiles dans un autre
   rôle : une courte racine de trace permet de résoudre un litige par division en deux jusqu'à une seule étape
   et donne à un appareil faible une vérification partielle avec une mention honnête.
3. **L'idée de « vérifiabilité à l'intérieur du modèle » fonctionne sous une seule forme :** réentraîner ou
   réécrire les noyaux pour que le profil exact devienne rapide. Cela réduit `γ` et n'affaiblit pas la
   garantie. Les empreintes sont écrites par un programme, non par le modèle, et le réentraînement n'est pas
   nécessaire pour elles. Les sommes de contrôle dans les couches protègent l'exécutant honnête contre les
   défaillances matérielles, mais non contre l'intention malveillante.
4. **Des jeux, seul l'ordre des coups se transpose :** « scellé → fixation définitive → choix secret →
   ouverture → recalcul ». Deux coups seulement sont liés au calcul : le recalcul du morceau ouvert et la
   vérification du témoin de la tâche. Un jeu séparé à côté du travail utile ne prouve rien.
5. **Il y a quatre variantes et une surcouche :** vérification complète de chaque réponse par le payeur ;
   loterie sur des commandes entières ; pièce secrète du payeur avec somme verrouillée ; tâches à résultat
   vérifiable ; et décodage spéculatif exact comme moyen possible de rendre moins chers la première et la
   troisième variantes.
6. **Recommandation.** Le contrat principal est la vérification complète de chaque réponse par le payeur dans
   le profil exact. Il est le seul à satisfaire les décisions acceptées sans les modifier. Les tâches à
   résultat vérifiable constituent un type de tâche distinct et, pour l'instant, la seule garantie stricte
   pour l'apprentissage. La loterie est un tarif pour les lots. La pièce avec somme verrouillée reste
   candidate jusqu'au calcul M9 et aux décisions du propriétaire.
7. **Première étape.** Un calcul : M9 — litiges fallacieux sans caution, toutes les branches de silence et de
   refus. Une expérience (avec l'autorisation du propriétaire) : sur le profil v2 et llama.cpp Q8_0 déjà
   assemblés, mesurer la coïncidence des jetons avec un préfixe commun. Elle tranche trois questions d'un coup
   (section 5).
8. **Littéralement irréalisable :** protéger le consommateur sans équipement en cas de collusion totale des
   vérificateurs ; vérifier une étape d'apprentissage en cas de collusion totale dans la limite d'une surcharge
   de 20 % ; faire tenir une réponse vérifiée dans 5 % avec le `γ` mesuré. Les assouplissements minimaux sont
   formulés comme questions au propriétaire à la section 7.

## 1. Ce que les audits ont trouvé

Étiquettes des audits : RU — `SkyNet_audit_completeness_RU` ; SC — `skynet_completeness_audit` ; GPT —
`gpt-SkyNet-audit` ; DS — `deepseek-AUDIT_REPORT` ; GEM — `gemini_report` ; CR — `chat_responses` ; cartes —
`mehanizmy-anti-obman` (MEH) et `mechanisms_map_report` (MAP). Là où les travaux du conseil ont lu
différemment qui a nommé quoi, cela est signalé par le mot « contesté ».

### 1.1. Approches omises

| Approche | Qui, parmi les audits, l'a nommée | Évaluation du conseil |
|---|---|---|
| Empreintes d'activations, TOPLOC | SC, GPT, GEM, CR, DS (en une ligne), MAP ; MEH — contesté | Pas une base de paiement ; seulement un signal pour une vérification exacte supplémentaire (section 2.4) |
| Schémas optimistes, litige avec arbitre, division en deux | Les six et les deux cartes | Couche de litige nécessaire ; en cas de collusion totale, il n'y a personne pour disputer, donc ce n'est pas un substitut à la vérification par le payeur |
| Tests statistiques de substitution de modèle | GPT, DS, GEM, CR, MAP ; SC et RU — contesté | Seulement un signal pour augmenter la fréquence de vérification ; n'entre pas dans le noyau |
| Arithmétique flottante reproductible, noyaux entiers de type Ozaki | SC, GEM, DS, GPT, RU ; CR cite RepOps | L'arithmétique flottante ne remplace pas le profil entier ; l'accélération des noyaux est une hypothèse à tester par l'expérience |
| Sommes de contrôle ABFT | SC, GEM, DS, GPT, RU | Auto-contrôle d'un nœud honnête contre les défaillances ; ne couvre que les multiplications linéaires |
| Vérification de Freivalds | SC, CR, GPT, GEM, cartes | Fonctionne pour la partie linéaire de l'arithmétique exacte avec un vecteur secret frais après la fixation |
| Disponibilité des données | SC, DS, GPT ; GEM — contre ; RU et cartes — contesté | Ingénierie du litige et de l'apprentissage, non une garantie de R4 |
| Conception de mécanismes avec vérification coûteuse | GEM, DS, GPT, SC | Confirme le seuil `R/(R + H_lock)` ; n'apporte pas de nouveau levier |
| Attestation matérielle GPU, TEE | Presque tous | Signal supplémentaire et mode de confidentialité ; il est interdit d'en déduire une réduction de la fréquence de vérification |
| Cautionnement et assurance sans dépôt de garantie du participant | SC, GEM, DS, GPT, RU | Le verrou d'autrui est essentiellement un dépôt de garantie d'un tiers, question pour R5 ; le fonds d'assurance ouvre l'auto-litige |
| Expérience de Bittensor, Gensyn, Prime Intellect, Hyperbolic, Ritual, Atoma, Golem | Les six et les cartes | Tous reposent sur un dépôt de garantie, des validateurs de confiance, TEE ou « un seul honnête » ; certaines techniques sont transposables |

Un seul audit a nommé : les preuves échantillonnées par couches comme base (RU), la liaison du cryptogramme
de la réponse à un engagement via DLEQ (SC), le pool de coupons (SC ; selon l'un des travaux — aussi GEM et
GPT).

### 1.2. Points faibles des conclusions précédentes

- Le seuil `p ≥ R/(R + H_lock)` est correct sous trois conditions qui n'avaient pas été nommées auparavant :
  le prix n'est pas inférieur au coût de revient, la pièce est réellement lancée, la somme peut être brûlée
  (GPT, SC, GEM, RU).
- La conclusion « le repère de 5 % est réfuté » concerne une seule implémentation des noyaux (GEM, SC, DS).
- La barrière des preuves succinctes est calculée pour une seule configuration (SC, GEM, DS, GPT).
- La coïncidence des bits est montrée sur six configurations, non « sur n'importe quel matériel » (DS, GEM,
  SC, GPT). Les critiques ont précisé : pour une longue passe sur une réponse prête — sur trois.
- L'affirmation « un payeur paresseux et un débutant donnent ensemble zéro » était une erreur : le gain va
  jusqu'à `+R`.
- L'énumération de « 92 millions de stratégies » ne prouve pas la complétude (RU).
- La littérature des conseils précédents est citée de mémoire (RU, GEM, DS, GPT).

### 1.3. Contradictions entre exigences et décisions

- **D16 contre la vérification par échantillonnage.** Si une défaillance honnête n'est pas sanctionnée, le
  trompeur déclare sa falsification une défaillance et obtient `(1 − p)·R − c_f` (DS, GEM, RU, SC).
- **D19.** La troisième condition — « l'erreur multipliée par `R` est inférieure au prix de la tentative » —
  est inapplicable lorsque la tentative est gratuite (DS, RU ; au conseil — ChatGPT).
- **L'émission de crédits pour l'apprentissage à demande nulle**, la collusion totale, la surcharge de 20 % et
  la vérification par chaque nœud ne sont pas satisfaites ensemble (DS, SC, GEM, GPT, CR, MEH).
- **Le consommateur sans équipement et R4** (SC, GEM, RU, CR).
- **Le D1 littéral exclut tout échantillonnage** (RU, DS).
- **Litige sans caution et fonds de litiges fini** (SC, GEM, GPT, RU).
- **« D'abord la pleine certitude, ensuite les expériences »** est qualifié de cercle vicieux : `γ`, `ρ`, la
  qualité et la fréquence des défaillances ne s'établissent que par la mesure (DS, GPT). C'est l'avis des
  audits et d'un critique ; le conseil n'a pas enfreint et ne lève pas la restriction en vigueur sur les
  expériences.

### 1.4. Nouvelles attaques

- **Payeur paresseux.** Si une part `λ` des payeurs ne vérifie pas, le seuil devient
  `R/((1 − λ)(R + H_lock))` ; avec un compte vide, il est supérieur à un, et le trompeur qui a reconnu un
  payeur paresseux obtient jusqu'à `+R` (SC) [calcul].
- **La pièce n'est pas contrainte :** on peut recompiler le programme du payeur avec `p = 0` (GEM, SC).
- **Revente d'une réponse entre sessions** (« attaque de la mafia ») : un intermédiaire prend la commande,
  achète la réponse à un exécutant honnête et ne paie pas. Fonctionne sans collusion des vérificateurs ; se
  soigne par l'ordre « prépaiement verrouillé → réponse → vérification dans le délai → paiement » (GEM ;
  développé au conseil).
- **Vente d'une somme non arrivée à maturité** avant le départ (RU). Se soigne par l'interdiction de cession.
- **L'auto-paiement** accroît la somme verrouillée et abaisse la fréquence de vérification. La critique a
  montré que cela n'ouvre pas l'argent (l'argent propre du trompeur brûle lors de la prise), mais rend moins
  coûteux le dommage ciblé.
- **Inondation de clés gratuites :** chaque nouvelle clé exige une vérification complète et charge le payeur ;
  c'est un déni de service, non un vol.
- **Substitution d'un ou deux jetons à l'intérieur de la fenêtre d'empreinte TOPLOC** (SC).

### 1.5. Ce qui est douteux dans les références et les chiffres des audits

- **Accélération des noyaux selon Ozaki jusqu'à `γ` = 1,05–1,20.** Douteux : les noyaux rapides de D5
  utilisent déjà les mêmes instructions 8 bits, et avec eux on a mesuré 1,52–1,78 ; 24 blocs sur 32 sont une
  récursion que la décomposition n'accélère pas. On ne peut pas mettre ce chiffre dans les estimations à côté
  des chiffres mesurés.
- **TOPLOC :** « 258 octets pour 32 jetons », « 10 à 100 fois plus rapide », « surcharge 1–3 % ». Deux travaux
  le confirment de mémoire, trois — « je ne peux pas vérifier » ; pour SkyNet, rien de tout cela n'est mesuré.
- **N'ont pas pu être vérifiés :** les chiffres de DeepProve et FlashProve, Verde (dans les audits, trois
  ensembles différents de surcharges), les pertes TEE sur H100, le prix de DLEQ en gaz, les statuts et
  incidents de Bittensor et d'autres réseaux, plusieurs numéros arXiv.
- **Attributions erronées :** l'algorithme Krum est attribué aux mauvais auteurs (MEH) ; un audit comporte une
  erreur arithmétique dans le seuil (`c_f ≈ 0,3c`, `p ≥ 0,73`).
- Un même chiffre dans deux audits ne fait pas deux mesures indépendantes : les deux peuvent reprendre une
  seule source.

## 2. Les idées du propriétaire menées jusqu'à des constructions

### 2.1. Vérifiabilité à l'intérieur du modèle et réentraînement

- **« Le modèle se protège lui-même » ne fonctionne pas.** Les poids et le code sont ouverts ; le trompeur
  n'est pas obligé de lancer le modèle. Les onze travaux l'ont confirmé.
- **« Le modèle écrit des empreintes »** — c'est un programme de hachage autour de poids inchangés. Le
  réentraînement n'est pas nécessaire et n'ajoute rien.
- **Les sommes de contrôle dans les couches (ABFT)** détectent une défaillance aléatoire. Un adversaire
  informé choisit une erreur qui conserve la somme. La récursion, les tables et la division dans l'attention ne
  sont pas couvertes par les sommes. La thèse de plusieurs travaux « ABFT lève le conflit D16 » a été jugée
  exagérée par les critiques.
- **Le réentraînement n'a de sens que pour réduire `γ` :** faire en sorte que le profil exact coïncide avec les
  noyaux 8 bits rapides (« canon grossier », proposition de DeepSeek). Les bits restent des bits, la garantie
  ne change pas. Risque : le premier profil 8 bits de D5 a déjà été rejeté pour sa qualité [mesuré] ; le coût
  de l'apprentissage et la perte de qualité ne sont pas mesurés, les heures GPU citées dans les travaux sont
  des hypothèses.
- **Le réentraînement « pour la robustesse à l'arrondi »**, afin que le profil rapide soit vérifié par
  tolérance, ramène au contrat avec tolérance (section 2.4) et ne donne pas de borne démontrable.
- **Un modèle à état plus petit** réduit le trafic de vérification d'un morceau, mais n'augmente pas la part des
  substitutions détectables.

**Verdict :** une seule forme fonctionne — l'accélération du profil exact. Elle se tranche par l'expérience.

### 2.2. Empreintes et recalcul d'un morceau aléatoire

**Construction.** Avant le choix du vérificateur, l'exécutant scelle d'une seule racine les jetons et les
états intermédiaires. Le vérificateur choisit secrètement un morceau, reçoit l'entrée scellée du morceau et le
recalcule dans le profil exact. Un morceau peut être vérifié sans recalculer tout le début de la réponse : D5
le confirme aussi, où un passage par morceaux donne les mêmes hachages d'états [mesuré]. L'affirmation de
plusieurs travaux « on ne peut pas recalculer un morceau sans le préfixe » a été rejetée par la critique.

**Pourquoi la borne `1 − s/N` n'est pas contournée.** Le trompeur calcule honnêtement tout sauf une cellule,
et continue honnêtement à partir de la valeur substituée. La trace est cohérente partout sauf en une
transition. Si l'on ouvre `s` transitions sur `N`, il existe une transition qui est vérifiée avec une
probabilité d'au plus `s/N`. Les empreintes rendent le mensonge détectable, mais ne le multiplient pas. Seule
une vérification où tout mensonge viole une grande part des égalités (preuves succinctes) peut contourner la
borne, et son prix reste le même.

**Deux types de coupes** [calcul d'après la configuration D5] :

| Coupe | Ce qu'elle certifie | Ce qu'il faut transmettre | Ce qu'elle ne détecte pas |
|---|---|---|---|
| Par couches : un bloc sur toute la séquence | Une transition de bloc à partir de l'entrée présentée ; le bloc représente environ 2,65 % de la passe, la tête de sortie environ 15,1 % | 0,78 / 4,9 / 14,6 MiB pour 160 / 1000 / 3000 positions | Une substitution assemblée dans une autre couche : une chance sur 32–33 |
| Par positions : toutes les couches sur un segment de 64 positions | Les jetons du segment sont égaux au choix exact avec l'état scellé de la frontière gauche | 48 MiB d'état et 64 KiB par position précédente : 58 / 110 / 236 MiB | Une position substituée hors du segment : passe avec la probabilité `1 − L/T`, par exemple 93,6 % pour 500 + 500 jetons |

L'exécutant doit alors conserver 0,13–2,38 GiB de points de contrôle par réponse pendant la fenêtre de litige
[calcul]. Seule une racine de 32 octets peut aller au journal : l'état lui-même est de 3 à 5 ordres de grandeur
plus grand que l'entrée D24.

**Falsification « brouillon par profil rapide + passe exacte ».** Elle a été trouvée par le critique Claude.
Le trompeur génère la réponse en Q8_0, puis fait une passe exacte sur les jetons prêts et imprime la trace.
Dans une telle trace, toutes les transitions de tous les blocs sont cohérentes ; seules ne coïncident pas les
positions où le jeton du brouillon diffère du choix exact.

- Le coût de la falsification est `c·(1/γ + ρ)`, l'économie par rapport au travail honnête `1 − 1/γ − ρ` :
  18,4 % avec `γ = 1,65`, `ρ = 0,21` ; la falsification est rentable lorsque `ρ < 1 − 1/γ` (0,34 / 0,39 / 0,44
  pour `γ` = 1,52 / 1,65 / 1,78) [calcul].
- La coupe par couches ne la détecte pas (sauf une chance sur 32–33 sur la tête de sortie).
- La coupe par positions de longueur 64 la détecte avec une probabilité de 97 % si les jetons de Q8_0 et du
  profil exact coïncident sur 95 % des positions ; 49 % avec une coïncidence de 99 % ; 29 % avec 99,5 % ;
  6,5 % avec 99,9 % [calcul]. La part de coïncidence n'est pas mesurée.
- La vérification complète la détecte toujours. La faille ne concerne que les schémas où la coupe **remplace**
  la passe complète.

Conséquence : la coupe certifie « l'exécutant a payé au moins une passe exacte », non « la réponse a été
générée par le profil exact ». Les critiques ont divergé ici : DeepSeek estime que la coupe par positions
détecte la substitution de toute la réponse par du Q8_0 avec une probabilité de 1 ; MiniMax — que cette
probabilité n'est pas mesurée ; Claude a donné le calcul ci-dessus. C'est la mesure de la coïncidence des
jetons qui tranche.

Le critique MiniMax a ajouté : la falsification gratuite « interrompre la réponse plus tôt » ne crée aucune
cellule fausse. La longueur de la réponse et la raison de l'arrêt doivent faire partie de l'objet de la
vérification.

**Ce que la racine de trace apporte néanmoins :**

- **Litige par division en deux.** Deux parties ayant des traces différentes convergent, en un nombre
  logarithmique de coups, vers une seule étape que chaque nœud recalcule lui-même. La critique a précisé : les
  15–23 coups annoncés ne suffisent que jusqu'à la cellule, à l'intérieur du bloc il faut encore environ 27
  divisions ; la règle « le silence est une perte » exige le calcul M9.
- **Appareil faible.** Un payeur sans carte graphique peut vérifier un segment par réponse. Cela donne la
  mention « vérifié partiellement », non « vérifié ». Le prix pour lui est un trafic de 52–300 MiB par réponse
  et du temps processeur ; sur téléphone, ce n'est pas mesuré.
- **L'immuabilité de l'historique de l'exécutant** et le litige sur une requête privée avec révélation d'une
  cellule.

**Verdict :** la construction est possible et utile pour le litige et l'appareil faible, mais elle n'allège pas
la garantie D1 et D25. Pour qu'une substitution ciblée devienne moins avantageuse que l'inaction, avec 32
blocs il faut ouvrir 2 / 4 / 7 / 10 blocs avec une marge de 5 / 10 / 20 / 30 % [calcul], et contre le dommage
(D6), cela n'aide pas non plus.

### 2.3. Procédés issus des jeux

| Procédé | Où le coup est lié au calcul | Où il ne l'est pas |
|---|---|---|
| « Sceller — ouvrir » | Le morceau ouvert doit coïncider avec le recalcul à partir de l'entrée scellée | Le scellement lui-même ne prouve rien : on peut aussi sceller un mensonge concerté |
| « L'un coupe — l'autre choisit » | Le choix est fait après la fixation, par la pièce secrète du vérificateur | Celui qui coupe abîme une partie sur `N` ; il n'y a pas d'économie par rapport à la vérification complète |
| Pièce commune de deux parties | Inutile lorsque l'argent d'un seul payeur est en jeu : sa pièce secrète suffit | Celui qui se révèle le dernier fait échouer une issue défavorable ; en cas de collusion totale, tous les apports sont connus de la coalition |
| Cartes sans croupier (mental poker) | — | Superflu pour choisir le numéro du morceau : une seule fonction aléatoire vérifiable fait la même chose |
| « Chacun surveille son adversaire » | Le payeur vérifie sa réponse — toutes les variantes de la section 3 reposent là-dessus | L'exécutant ne peut pas punir un payeur malhonnête sans caution (calcul M9) |
| Cartes marquées, acheteur secret | — | Dans un réseau ouvert, seul le payeur garde le secret du piège ; le piège coïncide donc avec sa vérification et coûte plus cher |

Une source publique commune d'aléa n'est nécessaire que là où l'on vérifie l'argent d'autrui ; alors D20
s'applique (au moins deux sources indépendantes).

**Verdict :** des jeux, on a retenu l'ordre des coups et le principe principal « vérifie celui dont l'argent
est en jeu ». Le jeu ne transforme pas un échantillon en vérification complète.

### 2.4. Exécutant rapide et juge exact

**Contrat avec tolérance.** L'exécutant calcule dans le Q8_0 rapide, le payeur fait une passe exacte et
accepte la réponse si, à chaque position, le score du jeton choisi est inférieur au maximum de pas plus de `m`.
L'avantage par rapport au « certificat avec marge » rejeté auparavant : le verdict se calcule en nombres
entiers et est identique sur tout appareil. Mais la critique a trouvé quatre défauts.

- **La tolérance légitime les réponses d'autrui.** N'importe quel brouillon plus une passe exacte montre à
  l'exécutant tous les scores ; il corrige les positions hors tolérance et obtient une réponse admissible. Le
  producteur le moins cher d'une telle réponse est le modèle-brouillon le moins cher, non le Q8_0 du même
  modèle.
- **La liberté de choix est un canal de dommage.** Aux positions où l'écart est inférieur à `m`, le jeton est
  choisi par l'exécutant, y compris l'arrêt précoce. Exemple : les scores « continuer » et « s'arrêter » valent
  100 et 99 ; avec `m = 1`, une réponse interrompue passe la vérification complète. Un tel texte recevrait la
  mention « vérifié avec tolérance » — c'est au fond une violation de D6. Le conseil précédent a déjà rejeté
  une mention semblable.
- **L'exécutant honnête est contraint de se vérifier lui-même**, sinon il perd la somme sur un seul écart,
  y compris sur une entrée choisie par le payeur. Le prix est alors `1 + ρ·γ` : +15…+71 % avec un lot de 1,
  et avec un lot de 8 il n'y a pas de gain par rapport à la génération exacte [calcul].
- **Le prix annoncé « +0,01…+2,3 % » n'a pas tenu :** pour ouvrir des morceaux, l'exécutant a besoin des
  hachages d'états du profil exact, c'est-à-dire d'une passe exacte à chaque génération [calcul].

Même avec un exécutant rapide, la passe exacte complète du juge coûte sur RTX 2060 au moins 31,9 % du temps
d'une génération ordinaire [calcul], si bien que ce contrat ne fait tenir aucune réponse dans 5 %.

**Le décodage spéculatif exact** — le même contrat avec `m = 0`. Le brouillon est obtenu par n'importe quel
moyen, seule est payée la réponse bit à bit égale à l'exacte. Le contrat et la garantie ne changent pas, D6
n'est pas touché. Le prix dépend de la part de coïncidence des jetons et de la longueur des séries
coïncidentes ; estimation inférieure `1 + ρ·γ`. Non mesuré ; avec une coïncidence inférieure à environ 95 %,
le résultat est pire que la génération exacte directe.

**TOPLOC et empreintes avec tolérance en arithmétique flottante.** L'empreinte certifie que les activations
sont cohérentes avec le texte, non d'où vient le texte. Falsification : un texte par n'importe quel modèle,
puis une passe du modèle déclaré sur ce texte — les empreintes sont authentiques. Le verdict avec tolérance
dépend du matériel : deux nœuds honnêtes peuvent diverger, on ne peut donc pas brûler la somme sur cette base,
et D4 est violé littéralement. Pour que le tarif avec tolérance soit bon marché, le vérificateur a besoin d'une
référence qu'il n'a pas tant qu'il n'a pas lui-même calculé la passe exacte.

**Verdict :** le contrat avec tolérance et les empreintes avec tolérance n'entrent pas dans la liste des
variantes : ils changent le produit et apposent une mention sur un texte choisi par l'exécutant. Ils ne sont
admissibles que comme signal pour une vérification exacte supplémentaire. Le décodage spéculatif exact est un
candidat à l'allègement du coût, tranché par une seule mesure.

## 3. Variantes intégrales

Le prix est la surcharge de calcul complète par rapport à une génération Q8_0 ordinaire sans vérification
[calcul d'après les mesures D5]. Il n'inclut pas le journal, les litiges, le stockage, le trafic et l'énergie :
ils ne sont pas mesurés. Le gain est attendu, pour une seule falsification soumise. Le bord inférieur
« +67 % » combine le `ρ` de la carte RTX 4070 Laptop avec le `γ` de la carte RTX 2060 ; sur une seule RTX 2060,
la plage commence à +84 %.

| № | Variante | Prix avec un lot de 1 | Argent du trompeur pour `q` = 0,1 / 0,3 / 0,5 / 1 | Débutant à compte vide | Saboteur sans gain | Principal risque résiduel |
|---|---|---|---|---|---|---|
| V1 | Vérification complète de chaque réponse par le payeur | +67…+149 % (sur une seule RTX 2060 +84…+149 %) | `−c_f` pour tous les `q` | `−c_f` | Pas de fausse mention « vérifié » ; peut faire échouer la livraison | Payeur paresseux ; faux refus du payeur (M9) |
| V2 | Loterie sur des commandes entières | +53…+82 % et réserve de l'acheteur `R/p` | `−c_f` pour tous les `q` | 0 | Une part `1 − p` des réponses n'est pas vérifiée et n'est retenue par rien | Revenu irrégulier ; la réserve est une question pour R5 |
| V3 | Pièce secrète du payeur et somme verrouillée | +50…+82 % ; la vérification elle-même 0,005–3,6 % | Au plus zéro pour tous les `q`, si le payeur lance la pièce à temps | `−c_f` (vérification toujours) | Une part `1 − p` passe : jusqu'à 99,98 % | Payeur paresseux reconnu — jusqu'à `+R` ; une défaillance honnête brûle la somme |
| V4 | Tâches à résultat vérifiable | `(N − 1)·v/w`, non mesuré | `−c_f` pour tous les `q` | 0 | Un témoin erroné ne passe pas | Ce n'est ni une réponse du modèle ni une étape d'apprentissage |
| V5 | Surcouche : décodage spéculatif exact par-dessus V1 ou V3 | Non mesuré ; estimation inférieure +15…+71 % | Comme pour la variante porteuse | Idem | Idem | La coïncidence des jetons n'est pas mesurée |

**Le payeur sans équipement** n'a de garantie dans aucune variante. S'il confie la vérification à un trio de
nœuds désignés, le faux paiement attendu est `R·q³` : 0,001`R` / 0,027`R` / 0,125`R` / `R` pour `q` = 0,1 /
0,3 / 0,5 / 1 [calcul]. C'est déjà écrit dans D21.

### V1. Vérification complète de chaque réponse par le payeur

**Étapes.** La commande fixe le modèle, le profil, la graine, les limites de longueur et la condition
d'acceptation. L'exécutant calcule la réponse dans le profil exact et fixe en une seule écriture le
cryptogramme et la racine de trace. Avant l'affichage, le payeur recalcule toute la réponse en une passe, y
compris la longueur et la raison de l'arrêt. Une divergence signifie non-paiement ; la somme en attente ne
brûle pas. La mention « vérifié » n'est mise qu'après la passe.

**Garantie et hypothèses.** Une réponse fausse n'est ni payée ni marquée, pour toute part de collusion, pour un
débutant et pour tout nombre de clés. Hypothèses : les bits coïncident sur l'appareil du payeur (montré sur six
exécutants [mesuré], pas sur téléphones) ; le noyau de vérification est correct ; le payeur vérifie réellement.

**Prix.** `γ·(1 + ρ) − 1` : +67…+149 % avec un lot de 1 ; +211…+358 % avec un lot de 8 (sur une seule
RTX 2060 +251…+358 %). Exemple `γ = 1,65`, `ρ = 0,21` : +99,65 %. Pour le payeur, la vérification coûte
15–71 % du temps de sa propre génération ordinaire [calcul].

**Ce qu'il faut changer dans les décisions.** Rien ; des précisions sont nécessaires pour D6 (deux mentions,
aucune intermédiaire), D16 (avec vérification complète, une divergence n'entraîne que le non-paiement) et D22
(section 4).

**Non mesuré.** La qualité du profil exact (expérience O5) ; `γ` sur d'autres cartes ; le temps et la mémoire
sur ordinateur portable et téléphone ; le coût du litige ; le comportement en cas de faux refus du payeur.

### V2. Loterie sur des commandes entières

**Étapes.** L'acheteur réserve à l'avance la cagnotte. Tous les résultats du lot sont fixés avant le tirage.
Le tirage choisit une fraction `p` des commandes ; le payeur vérifie entièrement les commandes choisies et paie
`R/p` ; les autres ne sont pas payées et sont marquées « non vérifié ».

**Garantie et hypothèses.** Un faux paiement est impossible même avec un compte vide et sans combustion des
sommes ; D16 n'a pas besoin d'être modifié. Hypothèses : tirage selon D20 ; la réserve de l'acheteur n'est pas
considérée comme un dépôt de garantie.

**Prix.** `γ·(1 + p·ρ) − 1` : +53…+82 % avec un lot de 1 ; exemple `p = 0,05`, `γ = 1,65`, `ρ = 0,21` :
+66,73 %. Mais pour un résultat **vérifié**, il y a `1/p` fois plus de travail.

**Points faibles.** Le revenu est irrégulier : avec `p = 0,1`, un débutant honnête a une probabilité de 34,87 %
de ne rien recevoir pour les dix premières commandes ; avec 6000 tâches par mois, `p = 0,01` et un coût de
revient de 95 % du prix, la probabilité d'un mois déficitaire est de 33,10 % [calcul]. Les réponses non
vérifiées ne sont retenues par rien : un saboteur avec des clés gratuites fournit des déchets gratuitement.

**Ce qu'il faut changer.** Répondre si la réserve `R/p` constitue des « fonds d'avance » au sens de R5 ;
choisir les sources d'aléa selon D20.

**Non mesuré.** La probabilité exacte de ruine en cours de route, la taille de la réserve, la demande pour un
tel tarif.

### V3. Pièce secrète du payeur et somme verrouillée

C'est la stratégie du conseil 5 ([STRATEGY_SEARCH](STRATEGY_SEARCH.md)) avec des corrections.

**Étapes.** La réponse est fixée dans le profil exact. Après la fixation, le programme du payeur lance sa pièce
secrète et vérifie la réponse complète avec une probabilité non inférieure à `R/(R + H_lock)` ; chez un
débutant — toujours. Une divergence prouvée brûle en une seule action toute la somme non arrivée à maturité de
la clé, y compris les récompenses de la même vague ; à la victime est rendu au plus `R`. La somme non arrivée à
maturité ne peut être ni cédée, ni vendue, ni mise en gage. Une réponse laissée passer par la pièce est payée
et marquée « non vérifié ».

**Garantie et hypothèses.** Le résultat attendu de toute série de falsifications ne dépasse pas la somme
verrouillée pour toute part de collusion : exemple de contrôle — une vague de dix falsifications donne
+4,4295`R` sans combustion et −2,49676`R` avec elle [calcul, reproduit par les critiques]. Hypothèses : le
payeur lance réellement la pièce et vérifie à temps ; le journal est accessible ; la somme est réellement
perdue.

**Prix.** +50…+82 % avec un lot de 1 ; la vérification elle-même chez les clés mûres — 0,005–3,6 % du travail.
La première fenêtre d'un débutant coûte 1,3–5,3 % du travail de la fenêtre en unités de génération exacte
[calcul].

**Points faibles.** La faille du payeur paresseux n'est fermée par aucune réparation : avec un compte vide et
`λ > 0`, le seuil est irréalisable. Avec D16 en vigueur, le trompeur déclare sa falsification une défaillance
et obtient `(1 − p)·R − c_f`. Le saboteur passe avec la probabilité `1 − p`. Un ajout bon marché — un plancher
de fréquence (par exemple `p ≥ 1/11` coûte 0,9–3,6 % du travail), mais même alors 90,9 % des falsifications du
saboteur passent [calcul].

**Ce qu'il faut changer.** D2, D11 et D21 (paiement d'une réponse laissée passer par la pièce) ; D7 ; l'annulation
de D16 pour une divergence publiée ; une nouvelle décision sur la somme verrouillée ; la réponse à la question
de savoir si la combustion est une sanction au sens de R5 ; le calcul M9.

**Non mesuré.** La fréquence des défaillances matérielles silencieuses — elle détermine combien de participants
honnêtes perdront la somme ; la part des payeurs qui exécutent réellement la vérification.

### V4. Tâches à résultat vérifiable

**Étapes.** Le plan (D9) autorise à l'avance une tâche dont le résultat est accompagné d'un témoin vérifiable
par machine : tests, preuve formelle, solution d'un problème avec certificat d'optimalité. La candidature est
scellée avant la révélation du témoin, afin qu'il ne puisse pas être intercepté. Chaque nœud vérifie lui-même
le témoin ; le paiement — une fois pour le contenu de la tâche.

**Garantie.** Un témoin erroné ne passe pas en cas de collusion totale, de compte vide et pour tout nombre de
clés.

**Prix.** Si `N − 1` nœuds vérifient pour `v` avec un coût de génération `w`, la surcharge est `(N − 1)·v/w`.
Avec `N = 1000`, elle tient dans 20 % seulement si `v/w ≤ 2·10⁻⁴` ; avec `v/w = 10⁻³`, c'est déjà 99,9 %
[calcul]. Le rapport `v/w` est tiré des audits et n'est pas mesuré.

**Points faibles.** C'est un autre produit : ni une réponse libre du modèle, ni une étape de gradient. La tâche
peut être résolue sans modèle et sans carte graphique. La règle qui engendre des tâches difficiles utiles n'est
pas présentée. La vérification d'un témoin est copiable, donc non payée selon D15 : l'idée « le téléphone gagne
en vérifiant des certificats » y contredit.

**Ce qu'il faut changer.** Compléter D9 et D15 ; D18 reste une recherche.

**Non mesuré.** Quelle part du travail du réseau entre dans cette classe.

### V5. Surcouche : décodage spéculatif exact

Le brouillon est obtenu par n'importe quel moyen rapide ; l'exécutant le compare lui-même par une passe exacte
et corrige les divergences ; seule une réponse exacte bit à bit est payée. La garantie est la même que pour la
variante porteuse V1 ou V3 ; les décisions, hormis la précision de D22, ne changent pas. Un gain n'est possible
que si les jetons des profils rapide et exact coïncident souvent et en longues séries. Rien de tout cela n'est
mesuré.

## 4. Recommandation du conseil et première étape

**Recommandation (synthèse).** Le contrat principal est **V1**. Il est le seul à satisfaire D1, D6, D7 et D25
pour la réponse sans nouvelles hypothèses sur la fréquence, la somme verrouillée et la combustion, et ne
demande pas de modifier les décisions acceptées. Les onze travaux en donnent la même formule de prix. **V4** —
un type de tâche distinct du plan. **V2** — un tarif pour les lots concertés. **V3** — un candidat : à inclure
seulement après le calcul M9 et des décisions explicites du propriétaire. **V5** et l'accélération des noyaux
exacts sont des voies de réduction du prix, non des contrats distincts.

**Précisions des décisions pour V1** (des propositions, non des décisions) :

- D6 : deux mentions — « vérifié » après une vérification complète bit à bit avant l'affichage, et
  « non vérifié ».
- D16 : lorsque le payeur vérifie chaque réponse, une divergence n'entraîne que le non-paiement.
- D19 : si la tentative est gratuite, l'hypothèse D19 ne s'applique pas.
- D22 : le brouillon peut être obtenu par n'importe quel moyen ; seule est payée la réponse bit à bit égale à
  l'exacte. La longueur de la réponse et la raison de l'arrêt font partie de l'objet de la vérification.
- D12 : ne pas changer : remplacer le temps actif par la hauteur des blocs d'une chaîne externe permet aux
  sommes non arrivées à maturité de mûrir pendant que le réseau est indisponible.
- Nouvelle décision sur le prix : dans quel profil se compte le volume de calculs. Avec un prix de 1,10 du
  coût de revient du profil ordinaire, le travail honnête dans le profil exact est déficitaire de 42–68 % du
  coût de revient [calcul] ; cette prémisse elle-même n'est pas approuvée dans le projet.

**Un calcul.** M9 : litiges fallacieux sans caution pour une commande à usage unique — silence de chaque
partie, auto-litige, auto-commande avec litige fallacieux, limites d'octets et de calculs par affaire, source
des fonds. Sans lui, aucune variante n'est activée (D23).

**Une expérience** (l'autorisation du propriétaire est nécessaire ; extension des O3 et O4 déjà réalisées). Sur
le profil v2 et llama.cpp Q8_0 assemblés, avec un préfixe commun, mesurer la part de coïncidence des jetons, la
distribution de l'écart du score du jeton choisi et les longueurs des séries de coïncidence. Elle tranche trois
questions : V5 est-elle rentable ; le contrat avec tolérance est-il viable ; la coupe par positions détecte-t-elle
la falsification « brouillon + passe exacte », c'est-à-dire le payeur sans carte graphique dispose-t-il d'une
protection quelconque. Il faut d'abord vérifier si les enregistrements D5 ont conservé les scores complets des
deux profils.

**Où les critiques et les travaux ont divergé.**

1. **Quel contrat est principal.** Les critiques Claude et ChatGPT — V1. Le critique DeepSeek — V3 avec des
   réparations, et V1 comme tarif coûteux et mode débutant. Le critique MiniMax — V1 comme tarif de base et la
   pièce pour les clés mûres, mais le réseau ne paie que le vérifié.
2. **Faut-il payer une réponse laissée passer par la pièce.** Pour — la majorité des travaux ; contre — les deux
   travaux ChatGPT et un travail MiniMax. Si l'on ne paie pas, l'exécutant honnête reçoit `p·R` par tâche, et
   c'est une loterie sans multiplicateur `1/p`. Il n'y a pas de troisième voie ; c'est le choix du propriétaire.
3. **Quelle expérience est la première.** Les critiques Claude et ChatGPT — la coïncidence des jetons des deux
   profils. Les critiques DeepSeek et MiniMax — un microbenchmark de noyaux 8 bits de type Ozaki avec
   vérification bit à bit : il montre si le repère de 5 % est atteignable en général. La synthèse le place en
   second.
4. **Le `γ` atteignable.** 1,05–1,20, 1,1–1,3 ou « ne baissera pas ». Non mesuré.
5. **Constituent-ils un dépôt de garantie au sens de R5** la combustion d'une somme non arrivée à maturité, la
   réserve de litige, la réserve de loterie, le long délai de maturation et le cautionnement.
6. **Faut-il plafonner la somme verrouillée.** Un plafond de 10`R` limite le nombre attendu de falsifications,
   mais rend la vérification des clés mûres environ 400 fois plus chère [calcul d'un critique, non revérifié].
7. **La troisième mention.** Le critique MiniMax propose « vérifié partiellement » ; le critique Claude —
   seulement deux mentions.

## 5. Apprentissage : ce qui existe et ce qui n'existe pas

**Ce qui n'existe pas.** Aucun travail ne donne de garantie pour une étape d'apprentissage. L'apprentissage
n'a pas de payeur : la base de l'émission de crédits doit être vérifiée par chaque nœud complet. L'apprentissage
en arithmétique entière n'est ni construit ni mesuré ; les mesures D5 ne concernent que la passe directe et ne
se transposent ni à la passe inverse ni à l'optimiseur.

**Ce qui existe.**

- **La répétition complète de l'étape par chaque nœud** — rigoureuse, mais coûte `N` étapes supplémentaires :
  avec dix nœuds, environ 1000 % [calcul].
- **Coupes de l'étape :** un nœud vérifie une cellule sur environ quatre mille. Coût 0,24 % / 2,4 % / 24 %
  avec 10 / 100 / 1000 nœuds [calcul], mais en cas de collusion totale la détection est nulle.
- **Paiement d'un résultat vérifiable** (V4) : garantie stricte pour une affirmation étroite. On vérifie le
  témoin de la tâche, non l'étape de gradient ; les formulations des travaux « l'apprentissage est résolu » et
  « le dommage est exclu » ont été jugées exagérées par la critique.
- **Le paiement pour une amélioration prouvée à l'examen** (D18) reste une recherche : l'examen certifie un
  score sur un ensemble donné, mais non l'absence de porte dérobée dans les poids.

**Limite.** Avec 1000 nœuds et une surcharge de 20 %, toute la vérification indépendante d'un nœud doit coûter
au plus 0,0002 du travail de l'étape [calcul]. Une preuve succincte de l'étape, selon toutes les estimations du
projet, est de plusieurs ordres de grandeur plus chère.

**Recommandation du conseil.** N'émettre des crédits que pour les résultats que chaque nœud vérifie lui-même ;
ne pas inclure une étape non vérifiée dans la version du modèle (c'est déjà D6).

## 6. Ce qui est littéralement irréalisable : questions au propriétaire

Le conseil ne propose pas de modifier les textes R1–R6. Les propositions de deux travaux de modifier R4 et R6
ont été rejetées par la critique : c'est une base immuable. L'impossibilité générale de concilier R4 et R6 pour
tous les algorithmes imaginables n'est pas démontrée ; ci-dessous — ce qui est irréalisable avec les
constructions trouvées.

| № | Ce qui est irréalisable | Assouplissement minimal | Recommandation du conseil |
|---|---|---|---|
| 1 | Protéger le consommateur sans équipement en cas de collusion totale des vérificateurs : les cas honnête et faux lui donnent les mêmes messages | La garantie n'est promise qu'à la partie qui vérifie elle-même ; aux autres, la réponse est montrée avec la mention « non vérifié », et l'ampleur du risque `R·q³` est nommée explicitement | Accepter : c'est déjà écrit dans D21, il suffit de le reporter dans la description destinée à l'utilisateur |
| 2 | Vérifier une étape d'apprentissage en cas de collusion totale dans la limite de 20 % | (a) payer pour un résultat vérifiable, non pour l'étape ; (b) admettre « au moins un nœud complet honnête » ; (c) retirer le repère de 20 % pour un petit réseau | (a) : la seule voie avec une garantie stricte ; une partie de la puissance libre reste alors sans apprentissage rémunéré |
| 3 | Faire tenir une réponse vérifiée dans 5 % avec le `γ` mesuré = 1,52–1,78 | Considérer le repère de 5 % comme un objectif d'ingénierie, publier le prix réel et mener la réduction de `γ` comme une tâche distincte | Accepter ; 5 % est un repère de la feuille de route, non le texte de R6 |
| 4 | Retenir par l'économie un saboteur qui n'a pas besoin de gain, avec `p < 1` | Seulement les mentions et l'interdiction d'utiliser le non-vérifié (D6) | Déjà accepté ; il n'y a pas de nouvelles mesures |
| 5 | Litige sans caution avec un fonds de litiges fini | Décider si le prépaiement verrouillé de l'acheteur est considéré comme un dépôt de garantie au sens de R5 | Décider après le calcul M9 |
| 6 | Être pleinement certain d'une décision avant toute mesure | Autoriser une liste limitée de mesures dont dépend le choix | Décision du propriétaire ; le conseil nomme deux mesures de la section 4 et l'expérience O5 |

Questions supplémentaires : faut-il payer une réponse laissée passer par la pièce (section 4, point 2) ; dans
quel profil se compte le prix de la tâche ; faut-il admettre le cautionnement d'un tiers.

## 7. Ce qu'il faut calculer par des mini-agents et ce qu'il faut vérifier par l'expérience

**Calculs** (fractions exactes, hachage de contrôle, répétition sur un second appareil ; ce ne sont pas des
expériences sur le protocole) :

1. M9 pour toutes les branches d'une commande à usage unique.
2. Le gain de la falsification « brouillon + passe exacte » sous les coupes, sur une grille de `γ`, `ρ`, de la
   part de coïncidence, de la longueur du segment et de la réponse, de la marge.
3. La pièce avec un plancher de fréquence et une part de payeurs paresseux, y compris le compte vide.
4. La falsification mixte « tout est honnête sauf une colonne » et la falsification par interruption de la
   réponse.
5. Loterie : probabilité exacte de ruine en cours de route et taille de la réserve de l'acheteur.
6. Les tailles exactes de l'entrée d'une cellule et de l'étape de litige selon la nomenclature du profil v2
   (vérifier 48 MiB et 64 KiB).
7. Inondation de nouvelles clés : charge sur le payeur et conclusion sur le quota de nouvelles clés.
8. Énumération des plus petits ensembles faux de cellules sur un petit modèle.
9. Comparaison de `ρ` et `γ` sur une même carte et à longueurs égales ; prix par résultat vérifié.

**Expériences.** O5 est autorisée par la décision D5. Les autres sont hors D5 et exigent l'autorisation du
propriétaire :

1. Coïncidence des jetons et écart des scores Q8_0 contre v2 — la première expérience.
2. O5 — la qualité du profil v2 sur 320 tâches.
3. Microbenchmark de noyaux 8 bits avec vérification bit à bit — vérification de l'estimation d'Ozaki.
4. `γ` et `ρ` par paires sur une même carte, y compris RTX 4070 Laptop.
5. Temps et mémoire d'une passe et d'un segment sur le processeur d'un ordinateur portable et d'un téléphone.
6. Coût de l'impression de la trace, couverture ABFT et fréquence des défaillances silencieuses.
7. Expériences sur l'apprentissage O6 et O7 — séparément, après la décision sur D18.

## 8. Qui a fait quoi

- **ChatGPT :** deux travaux indépendants et une critique de tous les travaux.
- **DeepSeek :** deux travaux indépendants et une critique avec recalcul des chiffres en arithmétique exacte.
- **Claude :** deux travaux indépendants, une critique et cette synthèse.
- **MiniMax :** cinq travaux indépendants et une critique.
- **Gemini** n'a pas participé au conseil : il n'y avait pas de clé dans le hub des modèles ; son audit
  figurait parmi les données d'entrée.
- **Les audits externes et les cartes des mécanismes** — des données d'entrée réunies par le propriétaire ; le
  conseil ne les a pas revérifiés sur les sources primaires.

Limites de la synthèse : le critique ChatGPT a analysé dix travaux sur onze ; le critique Claude n'a pas lu un
des travaux en entier ; les calculs des critiques ont été effectués chacun sur un seul ordinateur et attendent
une répétition par des mini-agents.
