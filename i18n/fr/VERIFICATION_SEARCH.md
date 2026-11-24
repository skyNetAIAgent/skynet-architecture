<!-- translation of docs/VERIFICATION_SEARCH.md, source sha256: cdf54a57e7747ae1f862b5b29fa7a53eee7fca80d8bae17a0cbc60f022cec00b -->

# Recherche d'une vérification indépendante de la part de collusion

[English](../../docs/VERIFICATION_SEARCH.en.md) · [中文](../zh/VERIFICATION_SEARCH.md) · [Español](../es/VERIFICATION_SEARCH.md) · **Français** · [Deutsch](../de/VERIFICATION_SEARCH.md) · [Italiano](../it/VERIFICATION_SEARCH.md) · [Русский](../../docs/VERIFICATION_SEARCH.md) · [Português](../pt/VERIFICATION_SEARCH.md) · [العربية](../ar/VERIFICATION_SEARCH.md)

État au 24 novembre 2026.

Ce document est le résultat du conseil de modèles pour l'étape 4 de la feuille de route (« Recherche d'une garantie indépendante
de la part de collusion », [ROADMAP](ROADMAP.md), section 4). Le conseil cherchait une vérification que chaque nœud
exécute lui-même, de sorte que l'accord ou la collusion d'autres vérificateurs ne décide de rien. La recherche portait sur deux
types de travail : la réponse du modèle Qwen à une requête d'utilisateur et l'étape de réentraînement.

**Statut du document.** C'est un résultat de raisonnement et de calcul par formules, non une mesure.
Il n'y a eu pour lui ni expériences avec le modèle, ni lancements de réseau, ni systèmes de preuve, ni model checking.
Les participants et les critiques n'ont exécuté que de courts programmes arithmétiques et de petites énumérations
sur processeur ; deux de ces énumérations des travaux ChatGPT ont été répétées par deux critiques, les hachages
de contrôle ont coïncidé. Les nombres marqués [calcul] sont obtenus par les formules à partir de paramètres nommés explicitement. Les paramètres
des modèles et des cartes graphiques ont été renseignés par les participants eux-mêmes ; aucun travail ne les a comparés à la configuration publiée
de Qwen3.5-4B ou d'un modèle d'environ 27 milliards de paramètres. **Seules les décisions D1–D25** de [ROADMAP](ROADMAP.md), section 3, sont des décisions acceptées. Tout le reste ici est
une évaluation du conseil. Là où les critiques ont divergé, la mention « contesté » figure.

**Comment lire.** La section 1 — ce qui est cherché et dans quelles conditions. La section 2 — ce qui est démontré impossible
et quelles affirmations d'impossibilité ont été réfutées. Les sections 3 et 4 — l'analyse des mécanismes pour la réponse
du modèle et pour l'étape d'apprentissage, avec le meilleur candidat et ses limites. La section 5 — ce qui reste
non démontré et quelles expériences et quels calculs le résoudront. La section 6 — les questions au propriétaire. La section 7 — qui
a participé.

**Bref bilan.**

1. **Réponse du modèle.** Une vérification indépendante de la part de collusion n'existe que là où toute la
   réponse est vérifiée par le payeur lui-même, dont l'argent est en jeu. Le meilleur candidat est « PPS » : le payeur
   recalcule en une passe la requête et la réponse prête dans un profil entier exact, le paiement provient
   uniquement de son prépaiement, et un litige fondé sur une preuve d'erreur est vérifié par chaque nœud. Le coût calculé est
   de 1,2–3,8 % du temps de génération, mais seulement avec une génération d'une réponse à la fois [calcul]. Le candidat
   ne couvre pas le consommateur sans équipement et dépend d'une concordance de bits non mesurée.
2. **Étape d'apprentissage.** Aucune vérification de l'étape elle-même dans une limite d'environ 20 %, indépendante de la part de collusion,
   n'a été trouvée. Les six travaux et les trois critiques sont d'accord.
3. **Le seul chemin survivant pour l'apprentissage** change ce qui est payé : le réseau paie
   pour une amélioration prouvée du modèle à un examen choisi après la fixation de la mise à jour. Selon la décision D18, ce chemin
   est étudié comme candidat à une nouvelle unité de paiement, mais n'est pas encore accepté ; des calculs, une expérience et les corrections
   trouvées par les critiques sont nécessaires.
4. **Ce qui décide, c'est l'expérience D5** (concordance des bits de Qwen3.5-4B en arithmétique entière sur deux cartes graphiques et entre
   deux modes de calcul, temps, qualité) **et les calculs des mini-agents** de la section 5.3 ; c'est sur eux que se prend
   la décision finale sur le paiement de l'apprentissage (D18).

Documents sources : décisions D1–D17 et étape 4 dans [ROADMAP](ROADMAP.md) ; modèle de l'adversaire
et formulation formelle de D1 dans [THREAT_MODEL](THREAT_MODEL.md), section 1.5 ; variantes A et B
dans [CURRENT_DESIGN](CURRENT_DESIGN.md) ; [OPEN_QUESTIONS](OPEN_QUESTIONS.md) ;
[PILOT_RESULTS](PILOT_RESULTS.md) ; [exigences obligatoires](../ru/REQUIREMENTS.md). Les participants
ont aussi lu les recherches antérieures du projet sur l'arithmétique exacte, sumcheck/GKR, Brakedown et le coût
du témoin pour LoRA (documents `LORA_*` et `HONESTY_RESEARCH_GATE` de l'archive de recherche ; ils ne font pas partie de ce
dépôt). Les participants ne disposaient pas encore des décisions D6–D17 : elles ont été adoptées le même jour.
Lors de la synthèse, ces décisions ont été appliquées aux conclusions des travaux ; là où une décision change le verdict, cela est dit explicitement.

---

## 1. Formulation

### 1.1. Ce qui est cherché

On cherche une procédure que le nœud exécute lui-même d'après des données que la coalition ne peut pas falsifier :
l'entrée de la tâche, le modèle fixé, les règles fixées et, éventuellement, une preuve
mathématique. La décision du nœud ne doit pas s'appuyer sur les signatures et les verdicts d'autres nœuds. Alors
la part `q` de vérificateurs en collusion, y compris `q = 1`, n'influence pas la décision.

Deux types de travail :

- **(a) réponse du modèle** Qwen de l'ordre de 4–27 milliards de paramètres à une requête d'utilisateur ;
- **(b) étape de réentraînement** (LoRA ou complet) sur un lot de données donné.

### 1.2. Conditions obligatoires

| Condition | Ce qui en découle pour la vérification |
|---|---|
| **D1** | Le gain attendu de toute fausse déclaration n'est pas supérieur à zéro, tant par rapport à l'inaction (`Δ₀ ≤ 0`) que par rapport au travail honnête (`Δч ≤ 0`), pour toute coalition, y compris un débutant au compte vide et tout nombre de clés. **Les deux** inégalités sont nécessaires ([THREAT_MODEL](THREAT_MODEL.md), section 1.5). Une fuite positive bornée comme `R·q^k` dans la variante B ne convient pas |
| **D2** | Seul un résultat vérifiable est payé. Le temps de travail, la puissance déclarée et l'équipement allumé ne servent pas de base. La manière dont l'exécutant a obtenu le résultat correct (cache, autre machine) n'importe pas |
| **D4** | La vérification est automatique, sans votes ; chaque nœud l'exécute lui-même d'après une empreinte fixée des règles |
| **D6** | Le dommage entre dans D1 : une réponse fausse ne doit pas être remise à l'utilisateur comme vérifiée, une étape fausse ne doit pas entrer dans le modèle. Le résultat n'est utilisé qu'après une vérification indépendante de la part de collusion, ou bien il est explicitement marqué comme non vérifié |
| **D7** | Une vérification indépendante de la part de collusion est exigée. Un affaiblissement de D1 jusqu'à « tant que les membres de la collusion sont moins de `q*` » n'est pas admis |
| **D8** | Seuls les vérificateurs de la tâche désignés par tirage au sort et l'utilisateur pour sa propre requête peuvent contester. Sans caution. Les autres signalent un soupçon sur le tableau sans droit d'arrêter le paiement |
| **D15** | Un simple recalcul qui peut être copié n'est pas payé |
| **R5** | Aucune caution, contribution ni amende. On ne peut perdre que des récompenses non arrivées à maturité (« somme en attente » `H`) |
| **Repères de prix** | Le supplément de vérification est d'environ 5 % du travail pour les requêtes et d'environ 20 % pour l'apprentissage. Ce sont des repères, non confirmés par les exigences |

Décisions liées : D9 (le plan d'apprentissage est déduit par une règle du catalogue et des résultats de l'examen,
les crédits sont émis une seule fois par contenu de tâche), D10 (l'échange passe par une seule écriture du journal),
D12 (les fenêtres sont comptées en temps actif du réseau), D14 (le prix du litige est celui du réseau de couche 2
le moins cher), D16 (une panne matérielle honnête n'est pas sanctionnée), D17 (les paiements pour les requêtes dans la variante B
proviennent uniquement des paiements des utilisateurs).

L'échantillonnage statistique, la confiance dans une enclave matérielle et une petite erreur cryptographique
selon les exigences sont des hypothèses : on peut les proposer, mais il faut les nommer explicitement.

### 1.3. Modèles et paramètres utilisés par les travaux

Il n'y avait pas de manifeste fixé de Qwen3.5-4B dans les matériaux. Chaque travail a pris sa propre configuration dense
conventionnelle, c'est pourquoi « 4B » désigne des nombres différents selon les travaux. Si Qwen3.5 comporte
des couches hybrides d'attention linéaire, toutes les parts d'attention et les conclusions sur la concordance des modes de calcul
changent (section 5).

| Travail | Réponse du modèle (a) | Étape d'apprentissage (b) |
|---|---|---|
| claude1 | « 4B » : 36 couches, largeur 2560, requêtes d'attention 4096, clés/valeurs 1024, MLP 9728, vocabulaire 151 936, entrée et tête communes (4,022 milliards de paramètres). « 27B » : 64 couches, 5120, 6144, 1024, 20 480, 151 936, séparées (26,386 milliards). Requêtes 500/500 et 2000/1000 jetons | LoRA de rang 16 sur les matrices des couches supérieures, examen `n = 10⁴–10⁶` positions |
| claude2 | Le même « 4B ». Requête de 1000 jetons, réponse de 500 ; travail de la requête 5,98·10¹² MAC [calcul] | LoRA de rang 16/64 sur les sept matrices, contexte 4096, lot de 64 ou 7680 séquences |
| gpt1 | « S » : 36 blocs, 2560, KV 640, MLP 11 008, 151 936. « Lg » : 48, 5120, 1024, 31 232. Entrée 128, sortie 32 jetons | 8 micro-lots de 512 jetons, LoRA de rang 8 sur Q, V |
| gpt2 | « Petit » : 36, 3072, KV 768, MLP 8192, vocabulaire 150 000. « Grand » : 60, 6144, 1024, 18 432. Entrée 128, sortie 128 | La même chose que gpt1 |
| ds1 | Classe Qwen3-4B : 4·10⁹ paramètres, 36 couches, 2560, MLP 9728 | Profil Qwen2.5-1.5B des recherches antérieures : 28 blocs, 1536, MLP 8960, LoRA de rang 8 sur q/v, 512 jetons × 8 micro-lots |
| ds2 | 36 couches, 2560, MLP 8960, 32/8 têtes ; contexte 2048, réponse 200 | Le même profil 1.5B |

Matériel (fiche technique de mémoire, non vérifiée) : classe RTX 2060 — 336 Go/s de mémoire, environ 103 TOPS
INT8, 6 Go ; classe RTX 4090 — 1008 Go/s, environ 660 TOPS, 24 Go. Les fractions du pic de 0,8 pour la mémoire et de 0,4
pour les calculs sont des scénarios. La seule mesure de vitesse est 73,8 jetons/s pour Qwen3-4B Q4_K_M
sur RTX 2060 dans le pilote ([PILOT_RESULTS](PILOT_RESULTS.md)). C'est un autre format de poids, et il ne
confirme ni ne réfute les modèles ci-dessus.

Formulation commune de D1 pour une fausse déclaration, sur laquelle les travaux se sont accordés : avec un prix de tâche `R`,
un coût de revient du travail honnête `c`, un coût de falsification `c_f` et une probabilité d'acceptation `ε`,
il faut `Δ₀ = εR − c_f ≤ 0` et `Δч = εR − c_f − (R − c) ≤ 0` [calcul].

---

## 2. Bornes inférieures : ce qui est démontré impossible

### 2.1. Bornes confirmées par les critiques

Ce sont des affirmations sur des **classes** de vérifications. Aucune d'elles n'exclut toutes les vérifications imaginables ;
personne n'a démontré de borne inférieure générale du coût pour tous les algorithmes.

1. **Indiscernabilité.** Si un nœud n'accepte un résultat que d'après les messages d'autres nœuds, alors, si tous leurs auteurs
   sont en collusion, il existe un résultat faux qu'il acceptera : la coalition enverra les mêmes
   signatures et empreintes que pour un résultat honnête. Pour `q = 1`, le nœud n'est protégé que par ce qu'il a
   vérifié lui-même. (claude1, lemme 1 ; claude2, 3.1 ; gpt2, 9.4 ; ds2, 6.1. Tous les critiques sont d'accord.)
2. **Échelle « chaque nœud lui-même ».** Si une modification de l'état commun (émission de crédits, poids) doit
   être protégée pour chacun des `N` nœuds complets, chacun d'eux vérifie chaque tel résultat,
   et le coût total n'est pas inférieur à `N·v`, où `v` est le coût d'une vérification. Pour tenir dans 5 % ou 20 %, avec
   `N = 1000`, il faut `v/W ≤ 5·10⁻⁵` ou `2·10⁻⁴` de travail [calcul]. D'où trois moyens d'obtenir
   l'indépendance vis-à-vis de la collusion : un unique participant dont l'argent est en jeu décide ; la vérification est compressée
   (preuve courte ou petit examen) ; le résultat ne modifie pas du tout l'état commun.
   (claude1, lemme 2 ; claude2, 3.4 ; gpt1, §2 ; ds2, 6.1. Tous les critiques sont d'accord ; le critique ChatGPT
   a corrigé la formule de ds2 en `1 + n·a` au lieu de `(1 + a)·n`.)
3. **Échantillonnage de cellules sans encodage.** Si un nœud lit en moyenne `s` cellules parmi `N` cellules remplaçables
   indépendamment (couches, positions, séquences), il existe une cellule qu'il vérifie
   avec une probabilité d'au plus `s/N` ; son remplacement passe avec une probabilité d'au moins `1 − s/N`.
   (claude2, 3.2 ; gpt2, 9.2 ; gpt1, 5.4 ; claude1, I2. Le critique Claude a relevé une lacune de rigueur pour
   un vérificateur dont les pièces dépendent de la racine de la trace ; la conclusion n'en change pas.)
4. **Vérification par échantillonnage et marge de l'exécutant.** Pour une fausse déclaration `σ` de coût `c_σ` et avec une somme
   en attente `H`, D1 par rapport à l'inaction exige `π(σ) ≥ (R − c_σ)/(R + H)`, où `π` est la probabilité
   de détection. Pour une falsification bon marché et un compte vide, il faut `π ≈ 1`, c'est-à-dire une vérification complète. Pour
   une falsification presque honnête, il faut une part de vérification d'au moins `m/(1 + m)` avec une marge `m`. Pour une clé
   avec `H > 0` et la vérification d'un bloc sur `L + 1`, il faut `H ≥ R·((L+1)/m_s − 1)` : 36R pour 36 couches
   et 64R pour 64 couches avec un seul bloc vérifié [calcul]. Un aléa frais du nœud rend `π`
   indépendant de la collusion, mais ne le rend pas égal à un. (claude1, lemme 3 ; claude2, 3.11, obtenu
   indépendamment. Tous les critiques sont d'accord. Le critique ChatGPT a précisé : avec vérification obligatoire du bloc
   de sortie, le seuil pour une tentative presque gratuite est de 35R.)
5. **Vérifications linéaires fixées sur un corps.** Pour `t < n` vérifications linéaires fixées à l'avance, il existe un noyau
   commun non nul : une erreur qui en fait partie leur échappe. Un vecteur uniforme frais,
   choisi après la fixation, laisse passer une erreur fixée non nulle avec une probabilité
   d'au plus `1/p`. Sur des entiers bornés, la borne ne s'applique pas (voir 2.2, point 3). (gpt1, 5.2 ;
   gpt2, 9.1 ; claude2, 3.5 ; ds2, 5.2 ; claude1, B4.)
6. **Une erreur nulle équivaut au déterminisme.** Une vérification sans aucune acceptation erronée, quelles que soient les pièces,
   devient déterministe par fixation des pièces. (claude2, 3.6.)
7. **Aléa commun en cas de collusion totale.** Pour `q = 1`, un aléa commun à tous les nœuds n'est possible
   que de l'extérieur du réseau (balise externe ou Fiat–Shamir) ; l'échange d'engagements entre nœuds SkyNet
   n'aide pas. Les pièces personnelles de différents nœuds donnent des décisions différentes, et un calcul unique n'en résulte pas.
   (claude2, 3.8 ; gpt2, 6.1. Le critique ChatGPT a ajouté : la balise doit être non biaisable, accessible
   et révélée strictement après l'acceptation définitive du bloc ; c'est déjà l'attaque 1.5 et N13
   dans [THREAT_MODEL](THREAT_MODEL.md).)
8. **Répétitions gratuites.** Si une tentative peut être répétée presque gratuitement (par exemple si l'aléa
   est dérivé du hachage de la déclaration elle-même), la probabilité de succès croît avec le nombre de tentatives. Fiat–Shamir
   ne doit pas être utilisé pour le choix des cellules. (claude2, 3.3 ; ds2, 5.1.)
9. **Vérificateur qui construit lui-même le résultat.** Si le nœud calcule lui-même tout l'état
   et ne lit la déclaration que pour comparer, alors, en supprimant la comparaison, on obtient un exécutant honnête
   avec le même travail. Une telle vérification coûte donc au moins 100 % du travail optimal. Seule une vérification
   avec indice peut être bon marché : réponse prête, trace ou preuve.
   (gpt2, 9.5. Les critiques Claude et DeepSeek ont appelé cela la meilleure formulation de la borne générale.)
10. **Certificat du jeton gagnant.** Pour un état caché en position générale, on ne peut pas certifier
    le gagnant sans obtenir d'informations sur chaque ligne du vocabulaire qui peut gagner. Dans le pire
    cas, tout le vocabulaire est vérifié. (claude1, B6 ; gpt2, 9.3.)
11. **Entrée privée.** Un nœud tiers sans la requête ne peut pas vérifier la réponse s'il n'existe pas
    de preuve à divulgation nulle de connaissance. Le critique ChatGPT a précisé la borne : un engagement masquant
    accompagné d'une telle preuve pourrait transmettre la propriété nécessaire, et le lemme
    ne l'exclut pas. (claude2, 3.7 ; ds2, 6.2 ; gpt1, §1.)

### 2.2. Affirmations d'impossibilité réfutées par les critiques

1. **« La lettre de D1 exige une erreur exactement nulle »** (ds1, F1). Vrai seulement si une tentative ne coûte
   rien. Si l'aléa est externe et imprévisible, et si chaque tentative exige une nouvelle fixation
   et coûte `c_min > 0`, alors `Δ₀ ≤ εR − c_min ≤ 0` pour `ε ≤ c_min/R` (claude1, lemme 4 ; ds2, 5.1).
   Le candidat propre de ds1 repose lui aussi sur un hachage avec une erreur supérieure à zéro. Les trois
   critiques l'ont réfuté. Réserve du critique ChatGPT : le projet n'a pas encore établi de borne inférieure du coût de la tentative la moins chère pour toute
   coalition ; une petite erreur n'est donc compatible avec D1 que conditionnellement
   (question 2 de la section 6).
2. **« La vérification d'une réponse prête coûte +100 % du temps par définition »** (ds1, F2). Faux pour
   une réponse prête : en vérifiant toutes les positions en une seule passe, les poids sont lus une fois, et non pour chaque
   jeton. En nombre d'opérations, la vérification égale bien la génération, mais en temps, avec une génération
   d'une réponse à la fois, elle peut être des dizaines de fois plus rapide. De plus, ds1 comparait
   des profils de poids incomparables. Les trois critiques l'ont réfuté.
3. **« Une vérification linéaire exacte exige au moins `N` formes et `N²` opérations »** (ds1, F3). Faux
   deux fois : des coefficients frais après la fixation donnent un passage avec une probabilité d'environ `Q^(−s)`, et sur
   des entiers bornés une seule forme avec empaquetage en base `Σ y_i·B^i` suffit pour `B > 2U`
   (gpt1, 5.3 ; gpt2, 6.2) ; la matrice identité lit les coordonnées en `O(N)`. Les trois
   critiques l'ont réfuté.
4. **« Le trafic minimal de vérification d'une réponse est égal à la taille de la trace de calcul »** (conclusion du lemme 5.3
   de ds2). La vérification d'une réponse prête n'a besoin que des jetons de la réponse, et le vérificateur d'une preuve courte
   lit la preuve et les racines, et non les données elles-mêmes. Les trois critiques l'ont réfuté.
5. **« Toute génération honnête doit exécuter autant d'opérations qu'une vérification en une
   passe »** (claude1, §4.1 et B5). C'est une borne supérieure du coût de vérification, non une borne inférieure (critique
   Claude), et elle ne tient pas si l'exécutant dispose d'un cache légitime du résultat prêt
   (critique ChatGPT).
6. **« Une vérification exacte bon marché est impossible sans aléa secret ou cryptographie »** (claude2, 3.5).
   Contre-exemple : l'équation normale exacte de la régression ridge sur les nombres rationnels
   se vérifie de manière déterministe (critique ChatGPT).

### 2.3. Bornes contestées ou conditionnelles

- **Taille de l'examen `n ≳ 2σ²·ln(1/ε)/δ²`** (claude2, 3.10). Les critiques Claude et DeepSeek l'utilisent
  comme estimation de travail. Le critique ChatGPT a montré qu'on ne peut pas déduire d'une seule variance le `n` nécessaire
  pour toute distribution : il faut des alternatives données et une unité d'échantillonnage indépendante.
  **Contesté** : convient comme estimation dans le modèle nommé, non comme théorème.
- **Barrière quantitative de la preuve complète** (claude2, 3.9) : un budget de 5 % laisse environ 1–5,
  un budget de 20 % — environ 6–18 opérations sur le corps par cellule non linéaire, alors que les constructions
  d'arrondi connues en coûtent des dizaines, softmax — des centaines [calcul avec les coûts admis]. Tous
  les critiques conviennent que c'est une borne des constructions connues, non un théorème.

---

## 3. Réponse du modèle (a)

### 3.1. Tous les mécanismes examinés

« Coût » est indiqué comme supplément au travail d'une exécution honnête ; tous les nombres sont [calcul] d'après les paramètres
des travaux. « Verdict » est le résultat après les trois critiques et compte tenu de D6–D17.

| Mécanisme (travaux) | Essence | Garantie et hypothèses | Données du nœud | Collusion et contre-exemple | Coût [calcul] | Verdict |
|---|---|---|---|---|---|---|
| **Répétition complète par chaque nœud**, passe causale sur la réponse prête (les six) | Le nœud disposant de l'entrée calcule lui-même toutes les positions et vérifie chaque jeton et la première raison d'arrêt | Erreur nulle avec un profil exact, une entrée authentique et un cœur sain | Requête, réponse, modèle, profil, graine | La collusion n'aide pas : c'est son propre recalcul qui décide | Environ 100 % des opérations pour chacun des `N` nœuds ; un nœud tiers ne voit pas la requête privée | **Tient** comme référence ; n'entre pas dans 5 % avec vérification par tous les nœuds |
| **I1 / PPS** (claude1) : vérifié par le payeur | Le payeur recalcule en une passe la requête et la réponse dans le profil entier « canon INT » ; le paiement provient uniquement de son prépaiement ; il n'y a ni émission ni poids pour une requête payée | Erreur nulle sous A1 (mêmes bits sur du matériel différent **et** en décodage jeton par jeton comme en passe sur toute la séquence sur une même carte), A2 (le journal conserve), A3 (hachage, chiffrement), A4 (le payeur publie à temps la preuve d'erreur), A5 (les données du litige sont disponibles) | Requête, réponse (`T·4` octets), empreintes du modèle et du profil, graine ; poids en mémoire 4,02 Go pour 4B W8, 12,8–25,6 Go pour 27B | Un unique participant dont l'argent est en jeu décide ; une collusion « payeur + exécutant » ne fait que déplacer leurs propres crédits | 4B, 500/500, RTX 2060 : 3,98·10¹² MAC, 0,19 s contre 7,5 s de génération — environ 2,5–2,6 % ; tous les scénarios 1,2–3,8 % avec génération d'une réponse à la fois ; 8–22 % avec un lot de 8 ; 21–48 % avec un lot de 32. Sans GPU environ 8 s pour 1000 jetons sur processeur — 100–300 % | **Tient avec corrections** (les trois critiques) ; corrections en 3.2 |
| **I8 — litige sur les racines des couches** (claude1) | L'exécutant fixe les empreintes du flux résiduel par couche. Le payeur trouve le premier bloc où le recalcul diverge et publie son entrée ; chaque nœud recalcule un bloc. Sans preuve dans la fenêtre, le paiement va à l'exécutant | Pas de fausse preuve d'erreur sous A1 ; un faux refus du payeur est impossible | Entrée du bloc (10–20 Mo pour 1000 positions), poids d'une couche (101–388 Mo) | Chaque nœud décide lui-même de la vérification. Contre-exemples : l'exécutant ne met dans le journal que l'empreinte du cryptogramme et ne remet pas la réponse elle-même ; le journal est identique que la réponse soit livrée ou retenue ; la censure d'un bloc dans la fenêtre repose sur des validateurs externes | Environ 1,0·10¹¹ MAC par nœud pour 4B, 3,9·10¹¹ pour 27B ; avec 1000 nœuds, un faux litige représente de l'ordre de 10–20 Go de trafic réseau (estimation du critique Claude) | **Tient avec corrections** : cryptogramme dans le journal, limite des faux litiges, actualité et censure comme hypothèses nommées |
| **M1 — Freivalds du payeur avec vecteur secret** (ds2) | Le payeur recalcule les opérations élément par élément et vérifie les multiplications matricielles par des produits scalaires sur son vecteur secret frais | Erreur d'au plus `N/p` sur toutes les égalités, négligeable pour `p ≈ 2⁶¹` ; il faut une vérification de plage et des sommes brutes avant arrondi | Trace de calcul fournie par l'exécutant | C'est le payeur lui-même qui vérifie. Contre-exemple au cache du vecteur : connaissant le vecteur d'une couche, l'exécutant contrôle la sortie de cette couche dans toutes les requêtes futures (critique DeepSeek) — le vecteur doit être frais à chaque requête | 2,7 % annoncés ; non reproduit : softmax 0,79 %, et non 2,45 %, et avec un coût de multiplication sur le corps de 10–100 MAC, les projections donnent +1,6–15,8 % (critique DeepSeek). Trafic — **contesté** : environ 14 Mo par jeton avec des int32 bruts et environ 15 Go de trace pour une requête de 1850 jetons (critique Claude) ; 7,419 Mo par jeton même en INT16 et 7,477 Go de prefill (critique ChatGPT) ; environ 2,4 Mo par jeton si les scores d'attention sont recalculés par le payeur lui-même (critique DeepSeek) | **Tient comme vérification** pour un payeur sans GPU, mais avec un canal rapide ; le coût annoncé est réfuté |
| **I2 — couches échantillonnées** avec un aléa frais du nœud (claude1 ; ds1, 3.1 ; gpt2, §8) | Le nœud vérifie `m_s` couches aléatoires sur `L` d'après les empreintes | Passage d'une erreur isolée avec une probabilité `1 − m_s/(L+1)` | Entrée de la couche, poids de la couche | Falsification : réponse d'un petit modèle plus trace honnête du grand ; une transition est faussée, puis continuation cohérente | Hachage de la trace 0,38–4 Go ; 1–8 % chez l'exécutant selon la vitesse de hachage | **Réfuté** pour un compte vide (borne 2.1, point 4) ; ne convient qu'aux clés avec `H ≥ 35–64R` |
| **PVYa** (claude2) : l'utilisateur vérifie un échantillon de cellules « bloc × jeton » avec son propre aléa secret | Choix d'une cellule proportionnellement à sa part d'opérations | Seulement un gain monétaire, pas le dommage | Cellules de la trace, chemin dans l'arbre des empreintes | Contre-exemple du critique Claude : réponse d'un petit modèle et trace prefill honnête ; une falsification bon marché en temps est détectée avec une probabilité d'environ 0,3–1 %, `Δч ≈ +0,94c`. Critique ChatGPT : dans le modèle de coûts égaux `Δ₀/c = +0,019` ; il faut aussi lier les clés et les valeurs d'attention au préfixe | Pour l'utilisateur de <0,001 % à 2,7 %, variante stricte environ 5,6 % ; pour l'exécutant, hachage d'environ 4 Go de trace — 2–4 s de processeur, 30–50 % du temps de la requête sur RTX 2060 | **Réfuté** (critiques Claude et ChatGPT). Le critique DeepSeek l'acceptait en séparant variante stricte et variante relative, mais la variante relative ne satisfait pas la formulation bilatérale de D1, et D6 exige aussi une garantie sur le dommage, que PVYa ne donne pas |
| **I3 — Freivalds sur la trace** par un nœud du réseau (claude1 ; ds1, 2.2 ; gpt1 ; gpt2, 6.1) | Vérification de chaque multiplication sur un vecteur aléatoire d'après la trace envoyée | `≤ 1/p` par erreur ; il faut les sorties brutes avant arrondi | Toute la trace | La collusion n'aide pas si le vecteur est frais | Trace de 4,4 Go par réponse (4B), 15,2 Go (27B) ; pour un prefill de 4096 positions, les seuls gate/up — 5,74 Go en INT16 contre 0,755 Go dans l'estimation de ds1 (critique ChatGPT) | **Réfuté comme vérification bon marché** : bute sur le trafic, non sur l'arithmétique |
| **I4 — tables de sommes partielles** (les six) | Le nœud construit à l'avance des tables de sorties de couche par groupes d'entrées | Exact avec des poids canoniques | Tables | — | Groupe 2 : 859 Go pour une matrice 4B, environ 476 To pour tout le corps ; plans binaires — au moins 128 tailles du modèle | **Réfuté par le calcul** (tous les critiques) |
| **I5 — certificat du jeton gagnant** (claude1 ; ds1, 2.5 ; gpt1, 4.3 ; gpt2, 5.3) | Arbre de clusters de lignes de la tête avec bornes supérieures prouvées | Exact pour le choix glouton avec couverture complète du vocabulaire et état caché vérifié | État caché de la dernière couche | Un état caché substitué certifie un autre jeton | Économise au plus la part de la tête : 2,10 % / 0,60 % (gpt1), 6,04 % / 1,76 % (gpt2), jusqu'à 9,67 % (claude1) ; dans le pire cas tout le vocabulaire | **Tient comme partie** de la vérification (choix glouton) |
| **Gumbel-max comme échantillonneur canonique** (claude1 ; claude2, 5.5) | Le choix avec température se ramène à `argmax(z/τ + g)` avec un bruit issu d'un PRF sur la graine | L'identité est vraie | Graine | La distribution diffère du top-p/top-k habituel — c'est un changement de produit | Bruit frais à chaque jeton : environ `V` valeurs de PRF et de maxima de groupe, 75,97 millions de valeurs de PRF pour 500 jetons | **Tient** comme moyen de fixer le choix ; l'économie du certificat pour l'échantillonnage **n'est pas justifiée** (critiques DeepSeek et ChatGPT) |
| **Certificat de Gumbel « avec marge »** (claude2, 5.5) | Un jeton presque gagnant est accepté dans les limites d'une tolérance | — | — | Contre-exemple : à logits égaux et avec une différence de bruit inférieure à `2η`, un jeton erroné passe (critique ChatGPT) ; toute tolérance ouvre une substitution (ds2, 6.4) | — | **Réfuté** |
| **Certificat par intervalles avec recalcul exact en cas d'ambiguïté** (gpt1, 4.4 ; gpt2, 5.4) | Approximation de rang faible d'une matrice gelée et borne prouvée du reste ; là où l'intervalle admet différents arrondis, le nœud recalcule exactement | Erreur nulle avec des normes du reste calculées indépendamment et un recalcul obligatoire | Ses propres facteurs et normes des restes | On ne peut pas prendre les clés et valeurs du message de l'exécutant | Passe rapide 0,521 % des opérations de la couche ; pour 5 %, la part de sorties ambiguës n'est pas supérieure à 4,479 % pour une couche préchauffée et à 1,342 % avec une préparation à froid (critique ChatGPT). Critique Claude : sur des poids proches du rang complet, les intervalles couvrent presque sûrement beaucoup de cellules, et le coût est proche de 100 % | **Tient** mathématiquement ; **coût contesté**, non démontré |
| **Empaquetage positionnel exact** (gpt1, 5.3 ; gpt2, 6.2) | Une seule forme linéaire `Σ y_i·B^i` sur les entiers | Exact pour `B > 2U` et des plages prouvées | Sommes brutes | Petite énumération : avec `B = 8`, 9 acceptations correctes et 0 fausse ; avec `B = 4`, 20 fausses sur 29 (répétée par deux critiques, hachages identiques) | Presque sans gain : pour W8A16 avec une largeur de 3072, un seul mot de 64 bits par sortie | **Tient** comme primitive exacte, n'apporte pas de réduction de coût |
| **Cache de préfixes vérifiés** (gpt2, 5.1) | Le nœud réutilise un état qu'il a lui-même produit | Exact pour la même position et la même version | Son propre cache | Une racine étrangère peut lier un état incorrect | Gain uniquement sur les répétitions ; le même cache est accessible à l'exécutant | **Tient**, ne réduit pas le coût en général |
| **Preuves courtes sumcheck/GKR** pour la réponse (claude1, I6 ; claude2, 4.9 et 5.7) | L'exécutant prouve toute la passe ; chaque nœud vérifie la preuve | Garantie calculatoire ; la borne d'erreur de bout en bout pour le graphe Qwen n'est pas dérivée | Preuve, poids pour l'évaluation en un point aléatoire | La collusion n'aide pas avec un schéma complet et des entrées vérifiées | Repère FlashProve 70–95× son propre profil (dénominateur incertain) ; estimation de claude2 — 6–20 fois plus cher que le travail avec un contexte de 2048 ; dans la meilleure lecture environ 16,8× (critique ChatGPT) | **Tient** comme garantie conditionnelle ; **n'entre pas** dans 5 % |
| **Changer la tâche : payer un résultat vérifiable** (claude1, I7 ; claude2, 5.4 ; gpt1, 3.1 ; gpt2, 4) | Par exemple, un vecteur satisfaisant une formule SAT, un code passant les tests, une solution à réponse vérifiable | Exact pour son propre prédicat | Tâche et résultat | L'exécutant peut envoyer un résultat correct que le modèle n'a pas produit ; selon D2, c'est admissible | Vérification SAT — au plus `3m` lectures | **Tient pour une classe étroite** ; la part de ces requêtes est inconnue ; le dialogue libre n'est pas couvert |
| **P0 / M4 — une requête payée ne donne ni émission ni poids** (claude1, claude2, ds2) | L'argent passe seulement du payeur à l'exécutant | Le transfert de ses propres crédits est neutre à l'intérieur de la coalition | — | Sans cette règle, la vérification par le payeur ne protège pas le réseau (borne 2.1, point 2) | 0 | **Tient** ; compatible avec D17 |
| **Vérificateur par lots d'un nœud dédié, paiement du seul prefill** (ds1, 3.3–3.4) | Un nœud vérifie un lot ; le prefill exact est payé | — | — | La signature du nœud dédié est identique pour une vérification réelle et une vérification simulée ; un prefill exact avec une réponse inventée passe | — | **Réfuté** (critique ChatGPT) |
| **Produit des probabilités d'erreur de différents nœuds** (ds1, 3.2) | Chaque nœud vérifie avec son propre aléa | — | — | Ne fonctionne que si tous les nœuds honnêtes acceptent obligatoirement ; pour `q = 1`, il n'y en a pas | — | **Réfuté** |
| **Litige ouvert dans la fenêtre** (les six) | Chacun peut objecter avant l'expiration de la fenêtre | Il faut un observateur honnête disposant des données et du temps | — | Si tous ceux qui ont vu les données se taisent, un résultat faux passe avec une probabilité de 1 ; le pilote l'a montré | Pilote : 93 transactions et 5,8–6,3 millions de gas dans un litige Cartesi | **Réfuté** comme vérification indépendante de la collusion ; D8 limite en outre le cercle des contestataires |
| **Délégation par un payeur faible** (claude1, 4.10) | Le payeur confie la vérification à son appareil ou à un nœud choisi | La confiance dans le nœud choisi est une hypothèse du payeur | — | Avec un choix aléatoire, la dépendance à `q` revient | — | **Hypothèse**, pas une solution |

### 3.2. Meilleur candidat pour la réponse du modèle et corrections des critiques

**Candidat.** Toute la réponse est vérifiée par le payeur lui-même. S'il dispose d'une carte graphique sur laquelle
le modèle tient, c'est PPS (claude1). S'il n'a pas de carte graphique mais dispose d'un canal rapide, c'est M1 (ds2)
avec un vecteur secret frais à chaque requête. Dans les deux cas, une requête payée ne donne ni émission
de crédits ni poids (P0 ; compatible avec D17), et chaque nœud décide du litige d'après la preuve d'erreur
(I8). Pourquoi la collusion n'aide pas : la décision est prise par l'unique participant dont l'argent est en jeu ;
il dispose de toutes les données — requête, réponse et modèle ; la vérification est complète, non par échantillonnage.

**Corrections sans lesquelles le candidat ne tient pas.**

1. **Rétention de la réponse.** Il faut mettre dans le journal le cryptogramme de la réponse lui-même, et non seulement son empreinte :
   environ 2–4 Ko par réponse (critique Claude). Cela coïncide avec D10 : échange par une seule écriture du journal.
2. **Faux litiges.** La coalition « payeur = exécutant » peut créer autant de petites requêtes qu'elle veut et déposer
   un litige pour chacune, litige que tous les nœuds téléchargent et recalculent. D8 limite le flux de litiges par le nombre de requêtes,
   mais les requêtes auto-payées ne sont pas limitées par ce plafond. Aucun travail n'a donné de solution
   (section 5, tâche M9).
3. **Actualité et censure.** Le payeur doit être en ligne et avoir le temps de publier
   la preuve dans la fenêtre, et le journal doit l'accepter. La censure d'un bloc dans la fenêtre repose sur l'honnêteté
   des validateurs externes du journal. C'est une hypothèse de collusion dans un autre ensemble, il faut la nommer
   explicitement. Pour le téléphone du payeur, elle est le plus souvent violée. La fenêtre est comptée, selon D12, en temps actif
   du réseau.
4. **Liaison des extrémités.** Un litige sur la première couche exige une liaison à la requête privée d'origine, un litige
   sur la dernière — au cryptogramme payé (critique ChatGPT).
5. **Arrêt.** Il faut vérifier la première raison d'arrêt. La condition « le dernier jeton est EOS ou
   la limite est atteinte » laisse passer une réponse complétée après un EOS précoce (critique ChatGPT).
6. **Arithmétique du canon INT.** Le produit des probabilités d'attention par les valeurs dans la spécification
   s'accumule en int64. S'il n'est pas exécuté sur les cœurs tensoriels, le coût du scénario long
   2000/1000 passe de 3,8 % à environ 8 % (estimation du critique Claude) ; issue — décomposer la probabilité de 16 bits
   en deux moitiés de 8 bits. Le critique ChatGPT a trouvé trois autres lacunes : avec une seule clé autorisée,
   softmax donne la valeur 65 536, qui ne tient pas dans 16 bits ; la somme des carrés
   dans RMSNorm peut déborder int64 (trois composantes de `2³¹−1` donnent déjà plus que `INT64_MAX`) ; il faut
   des largeurs explicites, des positions RoPE et un ordre d'arrondi. Le principe lui-même résiste à ces corrections.
7. **Diffusion en flux.** Selon D6, l'utilisateur ne doit pas voir un texte non vérifié comme vérifié.
   En diffusion en flux, chaque préfixe montré doit être vérifié, et la fréquence de ces vérifications
   entre dans le coût (gpt2, §1).

**Limites du candidat.**

- Le coût de 1,2–3,8 % n'est vrai qu'avec une génération d'une réponse à la fois. L'exécutant a intérêt à
  regrouper les requêtes en lots, et avec un lot de 8–32, la comparaison honnête donne 8–48 % [calcul].
- Le candidat ne couvre pas le consommateur sans équipement. Pour 27B, le payeur a besoin d'au moins
  13 Go de mémoire graphique. Le consommateur principal selon les exigences est un participant sans équipement. Selon D6, sa
  réponse ne peut être remise qu'avec la mention « non vérifié » ; aucun travail n'a résolu la question de savoir comment payer l'exécutant
  dans ce cas sans violer D1.
- Tout repose sur l'hypothèse non mesurée A1 : concordance des bits sur différentes cartes graphiques **et** entre
  le décodage jeton par jeton et la passe sur toute la séquence sur une même carte. Si Qwen3.5
  comporte des couches récurrentes d'attention linéaire, leur forme parallèle arrondit autrement, et le coût de
  vérification peut croître d'environ deux fois (claude1, 3.4, estimation avec 10 µs par étape admis).
- Le litige révèle la requête : l'entrée du bloc restaure presque réversiblement le texte. Il n'y a pas de litige sans révélation.
- L'énergie n'est pas mesurée : lorsque le calcul est le goulot, la carte graphique consomme plus que lorsque la mémoire est le goulot,
  la part énergétique peut donc être supérieure à la part temporelle.
- Les accélérateurs (certificat par intervalles, certificat du gagnant pour le choix glouton, cache de ses propres
  préfixes) ne sont admissibles que par-dessus une vérification complète, et non à sa place.

---

## 4. Étape d'apprentissage (b)

### 4.1. Tous les mécanismes examinés

La principale différence avec la réponse du modèle : l'étape d'apprentissage n'a pas de payeur dont l'argent est en jeu. Le paiement
se fait par émission de crédits, c'est pourquoi, selon la borne 2.1, point 2, la base doit être vérifiée par chaque nœud
complet. Selon D15, un tel simple recalcul n'est d'ailleurs pas payé.

| Mécanisme (travaux) | Essence | Garantie et hypothèses | Données du nœud | Collusion et contre-exemple | Coût [calcul] | Verdict |
|---|---|---|---|---|---|---|
| **T1 — répétition complète de la transition** par chaque nœud (les six) | Le nœud répète l'étape à partir du parent accepté et compare tout l'état suivant, y compris les poids master, les moments m, v de l'optimiseur et le numéro d'étape | Erreur nulle avec un profil exact et des données authentiques | Parent, lot de données, règles | Vérifier les seuls poids ne suffit pas : les mêmes poids avec v réinitialisé changent l'étape suivante (critique ChatGPT) | +100 % par nœud, au total `N × 100 %` ; par exemple environ 2,62·10¹⁵ MAC pour recalculer un lot de 64 × 4096 pour 4B | **Tient** comme référence ; n'entre pas dans 20 % |
| **T2 — couches, micro-lots, étapes échantillonnés** (claude1 ; ds1, 3.1) | Le nœud vérifie une partie aléatoire de l'étape | `1 − m_s/L` de passage | Une partie de la trace | Falsification : remettre une mise à jour aléatoire ou copiée ; remplacer un gradient frontière | Avec `N = 1000`, 36 couches et une couche vérifiée — environ 28 travaux par étape | **Réfuté** (borne 2.1, point 4) |
| **VYa-S** (claude2) : la balise choisit des cellules « bloc × séquence », chaque nœud vérifie leur preuve compressée | Probabilité de passer `(1 − f)^s` avec une part de falsification `f` | Balise externe, hachage, preuve de cellule ; seulement un gain monétaire, pas le dommage | Preuves des cellules choisies | Critique Claude : copier la trace d'une séquence sur tout le lot — seules les cellules de liaison sont incohérentes (environ 10,5 % du poids) ; avec `s = 30`, `Δ₀ ≈ +0,036R`, avec `s = 10`, `Δ₀ ≈ +0,33R` et `Δч ≈ +0,26c`. Critique ChatGPT : un gradient nul à la frontière du bloc rend toutes les cellules inférieures intérieurement correctes ; la formule utilise la part de travail économisé au lieu de la part d'égalités fausses ; même si elles étaient égales, `Δ₀/c ≈ +0,096`. Critique DeepSeek : seule `Δч ≤ 0` est satisfaite, alors que D1 exige aussi `Δ₀ ≤ 0` | Preuves 0,66 %, recalcul des entrées 0,39 %, hachage 3,7–10 % avec `s = 30` ; frontières des couches — 96,64 Go pour une tâche de 64 séquences et 11,60 To pour une tâche de 7680 | **Réfuté dans sa forme actuelle** (les trois critiques). Correctif proposé — vérification séparée de la liaison sur des séquences aléatoires ; non calculé |
| **T3 — preuve courte de l'étape** sumcheck/GKR avec engagements (claude1, T3 ; claude2, 4.9 ; ds1, 2.9 ; gpt1, 6.3 ; gpt2, 7.2) | L'exécutant prouve toute la transition, chaque nœud vérifie une seule preuve | Garantie calculatoire avec un schéma complet liant l'entrée, les arrondis, les plages et l'optimiseur ; la borne d'erreur de bout en bout n'est pas dérivée | Preuve, racines, une passe sur les poids par lot | La collusion n'aide pas avec un transcript commun | Repère VeriLoRA environ 137× (121,93 s de preuve pour 0,89 s d'apprentissage, autre modèle 3B) ; le budget laisse 11,43 % — écart d'environ 1200×. Pour le profil 1.5B, une seule division exacte de softmax — 11 973 394 432 cellules du corps et 10 998 054 912 vérifications de plage, 356,835 GiB avant alignement ; écriture de 3,067 To à 100 Go/s — 30,67 s contre 6,6 s de budget pour une étape de 60 s | **Tient comme direction** ; les dispositions concrètes sont réfutées, 20 % non démontrés. Le critique ChatGPT considère cela comme la branche de recherche la plus solide pour une étape inchangée |
| **M1 pour l'apprentissage** (ds2) | Vecteur secret plus recalcul des opérations élément par élément | Comme en 3.1 | Trace | Pas de lien entre la trace et le lot attribué : un calcul correct sur des données substituées passe (critique DeepSeek) | 1,5 % annoncés ; les opérations élémentaires inverses ne sont pas prises en compte (environ ×2–2,5), ni le coût de la multiplication sur le corps. Trafic 16,08 Go par étape en INT16, 64,318 Go en INT64 — au moins 514,5 s à 1 Gbit/s | **Réfuté** pour l'apprentissage, par le trafic et par la liaison |
| **Freivalds sur la trace de l'étape** (ds1, 2.2 ; gpt2, 6.1) | Vérification de chaque multiplication de l'étape | `≤ p^(−t)` | Toute la trace | — | 64,3 Go par étape (1.5B) ; 123,92–410,44 Go pour LoRA et 369,72–2073,34 Go pour l'apprentissage complet par étape (gpt2) ; au moins 991 s à 1 Gbit/s | **Réfuté** comme vérification bon marché |
| **T5 — l'étape comme formule de mise à jour** (les six) | Les nœuds vérifient les facteurs de mise à jour, et non la nouvelle matrice | Ne vérifie que la dernière addition | Facteurs | Contre-exemple : un gradient envoyé `G = 0` avec un vrai gradient non nul passe la vérification de la formule | Environ 10⁻⁶ du travail | **Réfuté** comme vérification de l'étape ; le recalcul de l'optimiseur et de l'addition fait partie du cœur |
| **Seulement le delta LoRA** (ds1, 3.5) | Vérifier uniquement l'adaptateur | — | — | La sortie de la partie gelée dépend de la nouvelle entrée | — | **Réfuté** |
| **T4 — paiement pour une amélioration** mesurée par chaque nœud sur un échantillon frais (claude1) | La mise à jour est fixée avant le tour ; une balise externe choisit `n` positions d'examen ; chaque nœud calcule lui-même la différence de pertes tronquée ; le dépassement du seuil de confiance est payé | Paiement d'une mise à jour sans amélioration avec une probabilité `≤ ε = 2⁻⁴⁰` avec une balise externe, un échantillonnage avec remise, un profil exact et une fixation avant la balise ; le coût d'une tentative doit être au moins `ε·κ·B/2` | Pool d'examen, toutes les `K` mises à jour du tour | Il n'y a pas de vérificateurs, chaque nœud calcule. Contre-exemples : (1) l'écrêtage des différences paie une mise à jour nuisible : +0,01 nat sur 99,5 % des positions et −20 sur 0,5 % donnent après écrêtage +0,005 pour un vrai −0,09 (critique Claude) ; +0,1 sur 99 % et −100 sur 1 % donnent +0,089 pour un vrai −0,901 (critique ChatGPT) ; (2) un pool public permet d'apprendre directement sur lui ; (3) un doublon avec bruit lors d'une fusion par somme apporte une contribution positive | Seuil pour `B = 2` : 0,0745 nat pour `n = 10⁴`, 0,0236 pour `n = 10⁵` (Hoeffding). Pour tenir dans 20 %, il faut `D ≥ n(1 + K·a)/0,6` jetons d'apprentissage par nœud et par tour ; avec `K = N = 10⁴`, cela fait 1,85·10⁸ jetons, environ 26 h. Cache d'états — 0,51 Go selon l'estimation de claude1 ou 524,3 Go en int16 si les positions sont prises dans différents préfixes de 1024 jetons (critique ChatGPT) | **Tient avec corrections** comme nouvelle unité de paiement ; ne vérifie pas l'étape. Contesté : la révélation échantillonnée des candidats après la balise est-elle dangereuse ? Critique Claude — non pour `ε = 2⁻⁴⁰`, critique ChatGPT — non pris en compte |
| **ODU** (claude2) : paiement pour une amélioration prouvée à un examen choisi par la balise après la fixation | Le soumissionnaire prouve l'examen ; chaque nœud vérifie la preuve au lieu de recalculer | Comme T4, mais supprime la croissance du coût avec le nombre de nœuds ; l'apprentissage peut se faire dans n'importe quelle arithmétique | Preuve de l'examen | Critique Claude : le soumissionnaire calcule gratuitement l'examen chez lui et ne prouve que les candidats gagnants, il faut donc `ε ≲ 0,23 %`, et non 10 %. Critique ChatGPT : même argument, plus la sélection adaptative sur un examen commun et le fait que le paiement selon la borne de confiance ne se compose pas télescopiquement (0,16 au lieu de 0,20 dans l'exemple). Critique DeepSeek : `ε = 10 %` passe formellement, mais au prix de tout le budget de 20 % | Preuve de l'examen environ 2,4 h par candidat, en séquentiel : avec 100 candidats, une époque ne dure pas moins de 10 jours (critique Claude). Part de l'examen 0,655 % des jetons d'apprentissage, 0,327 % si l'on prouve aussi le parent — environ 858 jetons, moins d'une séquence de 4096 (critique ChatGPT) | **Tient avec corrections** comme cadre ; `ε` — **contesté** (2 critiques sur 3 : il faut beaucoup moins de 10 %) ; l'attribution n'est pas résolue |
| **Examen ds1** (ds1, 2.8) : 20–82 jetons, « erreur nulle » | L'amélioration à un petit examen est payée | « Erreur nulle » seulement par définition | — | Bruit de la moyenne environ 0,28 nat sur 82 jetons pour une amélioration d'étape de 10⁻⁴–10⁻³ (critique DeepSeek) — c'est le bruit qui est payé ; la source d'aléa n'est pas nommée ; l'examen ne voit pas les moments substitués de l'optimiseur | Annoncé +1–3 % ; avec le contexte complet de chacun des 20 jetons évalués — 103,4 % de l'estimation matricielle de l'étape (critique ChatGPT) | **Réfuté** |
| **Étape de Gauss–Newton amortie avec certificat dual** (gpt1, 6.4) | Nouvel optimiseur ; l'exécutant donne un vecteur court, le nœud prouve chaque bit de l'étape arrondie pour `4λδ² > η²‖r‖²` | Erreur nulle pour la nouvelle étape avec un modèle linéaire donné | Forward exact et deux passes de dérivées | Une égalité à la borne d'arrondi exacte exige une solution exacte (critique ChatGPT) | `3N/(2k+2)` : 8,82 % pour `k = 16` et `N = 1`, 75 % pour `k = 1` ; pour `N = 100` — des centaines de pour cent | **Tient** comme contrat modifié ; le coût croît avec `N`, la qualité est inconnue |
| **Prédicat exact : régression ridge, tête linéaire** (claude1, T6 ; claude2, 4.1 ; gpt1, 3.2 ; gpt2, 4 ; ds1, 2.1 ; ds2, M2) | Le nœud vérifie la condition d'optimum `Xᵀ(Xw − y) + λw = 0` | Exact avec des caractéristiques authentiques | Caractéristiques, étiquettes | Les caractéristiques doivent être vérifiées séparément ; dans M2 de ds2, il manque le terme `λw`, et un optimum incorrect passe (critique ChatGPT) | 44,4 % avec un rang 8 et 12,1 % avec 32 par rapport à la construction de la matrice (gpt1) ; 0,390 % dans une autre disposition (gpt2) | **Tient pour une tâche étroite** ; ce n'est pas l'apprentissage de Qwen, la part d'un tel travail est inconnue |
| **Plusieurs premiers pas LoRA différents** (gpt2, 7.3) | Avec un adaptateur nul, les parties communes sont calculées une fois | Exact | Cache commun | Ne se transpose pas aux étapes suivantes | 16,70 % pour six débuts autorisés contre six lancements à froid | **Tient**, applicabilité étroite |
| **Apprentissage d'ordre zéro** (claude2, 5.8) ; **petit corps sur cœurs tensoriels** (claude2, 5.11) ; **cache du préfixe gelé et LoRA sur les blocs supérieurs** (claude1 ; claude2, 5.9) | Réductions de coût | — | — | L'ordre zéro change l'optimiseur ; un petit corps ne donne pas l'erreur annoncée sans bornes de plage | Cache du préfixe — environ 20,97 To pour un million de séquences de 4096 | Idées ; **non démontrées** |
| **T7 — litige ouvert** (les six) | — | Il faut un observateur | — | Pour l'apprentissage, il n'y a pas d'observateur intéressé | — | **Réfuté** |

### 4.2. Meilleur candidat pour l'étape d'apprentissage et ses limites

**Il n'existe pas de vérification de l'étape elle-même dans une limite de 20 %, indépendante de la part de collusion.** C'est un résultat négatif général,
confirmé de différents côtés : l'échelle `N·v`, une trace de 64 Go–2 To par étape,
des preuves des dizaines à des centaines de fois plus chères que le travail, le budget des opérations élément par élément.

**Avec une base de paiement inchangée**, deux voies restent : la répétition complète de la transition (référence, +100 %
par nœud) et, à long terme, la preuve obligatoire de toute l'étape (T3). Pour T3, il faut un
graphe concret, une robustesse prouvée de la composition et une estimation complète ; elle n'existe pas aujourd'hui.

**Avec un changement de base de paiement** (décision du propriétaire, section 6, question 1), le meilleur candidat est
la combinaison de T4 et d'ODU avec les corrections des critiques :

1. L'examen est choisi par une balise externe strictement après la fixation de toutes les mises à jour et l'acceptation définitive
   du bloc.
2. Le seuil est tiré d'une borne statistique avec une `ε` cryptographiquement petite (comme dans T4), et non de 10 %.
3. L'examen est vérifié par preuve (cadre ODU), afin que le coût ne croisse pas avec le nombre de nœuds.
4. Les pertes sont limitées par l'arithmétique elle-même (probabilité minimale dans le profil) et ne sont pas écrêtées,
   sinon des mises à jour nuisibles sont payées.
5. L'attribution des doublons doit être résolue sans chaîne séquentielle de preuves. Aucun travail ne l'a résolue.

**Limites.**

- Ce n'est pas une vérification de l'étape. L'examen ne voit pas les moments de l'optimiseur, ne certifie pas l'origine
  de la mise à jour et n'exclut pas l'apprentissage sur l'examen lui-même.
- Selon D6, une étape fausse ne doit pas entrer dans le modèle. Une amélioration à l'examen ne prouve pas l'absence de dommage
  sur des requêtes rares ni de portes dérobées (Q4 dans [OPEN_QUESTIONS](OPEN_QUESTIONS.md)). Le candidat limite
  le gain monétaire, mais pas le dommage.
- On ne sait pas si l'amélioration honnête d'une mise à jour dépasse le seuil : le bruit de la différence de pertes `σ`
  n'est pas mesuré. Si elle ne le dépasse pas, les participants honnêtes ne sont pas payés, et R6 est violé.
- Les appareils faibles avec une petite mise à jour ne passent pas le seuil ; « toute la puissance libre apprend »
  ne vaut que comme « apprend », non comme « est payée ».
- Lien avec D9 : le plan d'apprentissage est déjà déduit des résultats de l'examen. Cela fait de l'examen une partie
  du cœur, mais ne résout pas la question de savoir si l'on peut payer pour l'amélioration au lieu de l'étape.

---

## 5. Ce qui n'est pas démontré et comment le vérifier

### 5.1. Ce qui n'est pas démontré

1. Concordance des bits du profil entier sur différentes cartes graphiques et entre le décodage jeton par jeton
   et la passe sur toute la séquence sur une même carte (A1, question Q2). En dépendent PPS, M1,
   le certificat par intervalles et toute répétition exacte.
2. Temps de vérification d'une réponse prête par rapport à la génération sur des cartes réelles avec des lots de 1, 8, 32 ;
   énergie ; comportement des couches hybrides d'attention linéaire.
3. Qualité et vitesse du profil entier de Qwen3.5-4B par rapport au profil habituel.
4. Coût du certificat par intervalles et du certificat du gagnant sur des poids réels.
5. Disponibilité des données du litige, limite des faux litiges sans caution, actualité et censure du journal.
6. Pour le paiement de l'amélioration : amplitude de l'amélioration honnête par rapport au seuil, règle d'attribution sans
   gain des doublons, borne des pertes sans écrêtage, coût de la preuve de l'examen.
7. Pour la preuve courte de l'étape : estimation complète d'une étape et borne d'erreur de bout en bout.
8. Configuration exacte de Qwen3.5-4B et du modèle d'environ 27B : tous les nombres des travaux ont été renseignés à la main.

### 5.2. Expériences minimales

La décision D5 autorise la première expérience : Qwen3.5-4B en arithmétique entière sur la RTX 2060 du Linux domestique
du superviseur, sur son ordinateur et, avec accord, sur les appareils d'autres participants via
des mini-agents, après l'étape 0. Les profils, métriques et seuils sont fixés avant la mesure. La concordance des bits
ne concerne que les configurations testées.

| N° | Expérience | Ce qui est mesuré | Réfute le candidat si |
|---|---|---|---|
| O1 (D5) | Qwen3.5-4B en arithmétique entière sur deux cartes graphiques différentes | Hachages des logits et des jetons sur un même jeu de requêtes ; premier jeton divergent, EOS, égalités, contexte long, requêtes à logits proches | Un seul bit diffère pour la même spécification |
| O2 (D5) | Passe sur toute la séquence contre décodage jeton par jeton sur une même carte | La même comparaison de bits ; séparément pour les couches hybrides, si elles existent | Un seul bit diffère |
| O3 (D5) | Vitesse : vérification d'une réponse prête contre génération | Temps avec des lots de 1, 8, 32 et des combinaisons entrée/sortie 128/32, 128/128, 500/500, 2000/1000 ; implémentation du produit d'attention en 16 et 8 bits ; mémoire, trafic | Part de vérification avec un lot de 1 supérieure à 5 % |
| O4 (D5) | Vitesse du profil entier contre le profil habituel sur les mêmes cartes | Jetons par seconde, mémoire | Le ralentissement rend le service non rentable (fixer le seuil avant l'expérience) |
| O5 (D5) | Qualité du profil entier contre le profil habituel | Le même jeu de tâches | Perte de qualité supérieure à un seuil fixé à l'avance |
| O6 (hors D5, autorisation séparée nécessaire) | Bruit de l'amélioration d'un seul adaptateur LoRA | Distribution de la différence de pertes base/adaptateur de rang 16 après un jour d'apprentissage, `σ` et `δ/σ` | L'amélioration honnête est typiquement inférieure au seuil pour une taille d'examen admissible |
| O7 (hors D5 ; le lancement de systèmes de preuve est actuellement interdit par une restriction de recherche) | Coût de la preuve d'un bloc forward sur 4096 jetons | Coefficient `P` | `P` supérieur à environ 300 — alors ODU et VYa-S ne tiennent pas (estimation de claude2) |
| O8 (hors D5) | Rapport du coût d'une multiplication sur le corps au MAC tensoriel sur RTX 2060 et RTX 4090 | Coefficient `R_f` | Décide de toutes les estimations de Freivalds et GKR |
| O9 (hors D5) | Énergie de la vérification | Joules par vérification et par génération | Part énergétique supérieure au repère |

### 5.3. Calculs exacts pouvant être confiés à des mini-agents

Ce sont des calculs déterministes sans mesures. Pour chaque tâche sont fixés la version de la procédure,
les octets d'entrée ou le générateur avec les bornes d'énumération, les entiers ou fractions exacts, la sérialisation de la réponse
et le SHA-256 ; le résultat est répété sur un second appareil. La concordance confirme le calcul, mais ni
la sémantique ni l'inégalité économique.

| N° | Tâche | Paramètres | Ce que cela décide |
|---|---|---|---|
| M1 | Inventaire du graphe selon le manifeste fixé de Qwen3.5-4B et du modèle d'environ 27B (`config.json` publié avec hachage) | Formes et types de toutes les opérations de remplissage du contexte, de génération, de vérification de la réponse et de l'étape d'apprentissage ; MAC, octets des sommes brutes, durée de vie des tampons ; couches hybrides ; LoRA et apprentissage complet | Précise les numérateurs et dénominateurs de toutes les estimations |
| M2 | Table de la part de vérification `ρ(B)` selon le modèle « toit » | `L, d`, largeurs d'attention et MLP, vocabulaire, `P, T`, lot `B ∈ {1, 8, 32}`, bande passante mémoire, TOPS, fractions du pic | Prédiction pour l'expérience O3 |
| M3 | Bornes de débordement du canon INT | Tous les accumulateurs selon la spécification, y compris le produit d'attention jusqu'à `T ≤ 32 768`, la somme des carrés de RMSNorm, la taille de la probabilité dans softmax ; variante à deux moitiés de 8 bits | Trouve une entrée avec débordement ou prouve son absence |
| M4 | Trafic exact de M1 | int32 bruts et trace de la requête sur la grille (entrée, sortie, modèle) ; avec et sans recalcul des scores d'attention par le payeur | Lève le désaccord des critiques sur le trafic de M1 |
| M5 | Vague de falsifications pour les schémas d'échantillonnage avec `H > 0` | `π = m_s/(L+1)`, `H₀` initial, `R`, plafond des tâches ouvertes ; énumération de la taille et du nombre de vagues | `H*` minimal pour lequel une falsification avant départ n'est pas rentable |
| M6 | VYa-S : énumération des stratégies de copie et des entrées dégénérées | Part `f`, nombre de cellules `s`, poids des cellules, nombre de vérifications de liaison `s'` ; avant et après le correctif | `Δ₀` maximale ; le correctif tient-il |
| M7 | Économie de la preuve échantillonnée et de la révélation dans ODU et T4 | `e/R`, `P`, marge `m`, nombre de clés et de candidats | `ε` maximale admissible |
| M8 | Échelle de T4 | `D(N)` avec `K = N`, `n`, `a`, `ε` | Limite du nombre de soumissionnaires pour 20 % |
| M9 | Coût d'un faux litige I8 | Trafic et calculs du réseau en fonction de `N`, `P + T`, pas des empreintes `k` | Faut-il une limite des faux litiges, et laquelle |
| M10 | Tables du seuil `t(n, ε, V̂)` | Hoeffding et Bernstein empirique avec le terme `B` ; grille `n, ε, B` | Examen minimal |
| M11 | Écrêtage des pertes | Part maximale payée de mises à jour nuisibles pour `B, n, ε` ; borne des pertes du canon INT en fonction de la probabilité minimale | Choix de `B` sans payer le dommage |
| M12 | Attribution sur un modèle de fusion jouet | Pertes linéaires-quadratiques, gradients connus ; règles « séparément », « garder un seul », Shapley ; doublons et doublons avec bruit ; fractions exactes | Existe-t-il une règle sans gain des doublons |
| M13 | Indices et gadgets de la preuve courte | Nombre de valeurs avec arrondi, division et tables par jeton et par couche ; cellules, accès aux tables et engagements pour une opération d'arrondi et de softmax | Barrière 2.3 et estimation de T3 |
| M14 | Petites énumérations pour vérifier les formules | Empaquetage positionnel avec `B = 8` et `B = 4` (répétition des hachages) ; chaîne de 8 transitions avec choix 2 : 224 paires, 56 attrapées, 168 manquées ; corps F₅ et erreur (1, −1) : 5 manques sur 25 | Vérification de l'implémentation des modèles probabilistes |
| M15 | Certificat du gagnant sur des matrices structurées synthétiques | Lignes regroupées, écart de logits donné, égalités, échelle commune | Économie selon différentes distributions ; sur des poids réels — après O1 |
| M16 | Certificat par intervalles sur des préfixes fixés | Part de sorties ambiguës `u`, nombre de recalculs complets, coût de préparation par nombre de requêtes | L'accélération tient-elle dans 5 % (une fois les poids disponibles) |
| M17 | Étape de Gauss–Newton sur un petit bloc | Matrice rationnelle explicite `J`, identité `⟨Jx, z⟩ = ⟨x, Jᵀz⟩`, longueurs des entiers, nombre de raffinements, égalités | Coût du nouveau contrat |
| M18 | Calcul des paiements et récupération | Énumération finie : un numéro de tâche, deux parents, bifurcation, perte de l'entrée, collusion de tous les désignés, compte vide | Pas plus d'un paiement par résultat ; rien n'est appliqué avant l'acceptation |

---

## 6. Décisions qu'exige cette étape

Le conseil ne prend pas de décisions. Ci-dessous — les questions avec la recommandation du conseil. Le propriétaire a chargé
le superviseur de les trancher ; les décisions D18–D25 ont été adoptées le 24 novembre 2026 et consignées dans [ROADMAP](ROADMAP.md),
section 3. Chaque décision est indiquée après la question.

1. **Faut-il changer la base du paiement de l'apprentissage pour un « paiement pour une amélioration prouvée » ?** Selon D2,
   c'est un résultat vérifiable qui est payé ; une amélioration à l'examen en est formellement un, mais c'est un autre
   objet que l'étape exécutée. Trois travaux (claude1, claude2, ds1) le considèrent comme le candidat principal,
   trois (gpt1, gpt2, ds2) — comme un autre contrat, et non comme une vérification de l'étape. *Recommandation du conseil :* autoriser
   l'étude de cette voie comme candidat à une nouvelle unité de paiement de l'apprentissage, sans l'appeler vérification de l'étape.
   Décider définitivement après les calculs M7, M8, M10–M12 et l'expérience O6. Conditions : balise externe après
   fixation, `ε` cryptographiquement petite, pertes sans écrêtage, preuve de l'examen, règle
   d'attribution sans gain des doublons. Selon D6, consigner que l'amélioration ne prouve pas l'absence de dommage.
   **Décidé — D18 :** la voie est étudiée comme candidat à une nouvelle unité de paiement de l'apprentissage, mais n'est pas acceptée et n'est pas
   appelée vérification de l'étape. La décision d'acceptation — après M7, M8, M10–M12 et l'expérience O6 (elle est hors D5
   et exige l'autorisation du propriétaire). Le modèle
   n'est émis que selon la règle D9. La recherche d'une vérification de l'étape elle-même (T3) continue.
2. **Une petite erreur cryptographique est-elle admissible ?** Les exigences la qualifient d'hypothèse. Les travaux
   claude1, claude2, ds2 et les critiques Claude et DeepSeek considèrent qu'une erreur `2⁻⁴⁰…2⁻¹²⁸` est compatible
   avec D1 comme espérance, si l'aléa est externe et imprévisible et si chaque tentative coûte
   plus de `ε·R`. Travaux gpt1, gpt2 et critique ChatGPT : une petite erreur ne suffit pas pour D1, il faut
   une borne inférieure prouvée du coût de la tentative la moins chère. ds1 considère qu'il faut exactement zéro.
   *Recommandation du conseil :* accepter une petite erreur comme hypothèse nommée explicitement à trois conditions —
   balise externe strictement après l'acceptation définitive du bloc, interdiction de Fiat–Shamir pour l'échantillonnage,
   borne inférieure consignée du coût d'une tentative. Sans cette décision, ni le paiement de l'amélioration
   ni les preuves courtes ne sont possibles.
   **Décidé — D19 :** une petite erreur est admise comme hypothèse explicite à ces trois conditions,
   pas plus de `2⁻⁸⁰` par tentative et avec `ε·R` inférieur à la borne inférieure consignée du coût d'une tentative. Une vérification
   par échantillonnage ordinaire avec une erreur `q^k` n'est pas autorisée par cela.
3. **Quelle balise externe et quelle confiance sont admissibles ?** Sans source externe d'aléa commun, pour
   `q = 1`, aucun schéma avec échantillonnage après fixation ne fonctionne (borne 2.1, point 7). Les sources ne sont pas encore
   choisies (attaque 1.5 et N13). *Recommandation du conseil :* choisir plusieurs sources indépendantes
   et consigner la confiance en elles comme hypothèse.
   **Décidé — D20 :** au moins deux sources publiques indépendantes, la valeur est prise à un moment fixé
   à l'avance après la fixation définitive, sans droit de l'omettre. Les sources concrètes
   et le coût de l'influence sur elles — à l'étape 2. Elles ne sont pas incluses avant le choix d'un schéma avec échantillonnage.
4. **Faut-il accepter que, pour la réponse du modèle, la vérification indépendante de la collusion n'existe que chez le payeur
   qui vérifie lui-même ?** *Recommandation du conseil :* oui. Pour le consommateur sans équipement, la réponse
   est remise avec la mention « non vérifié » (D6 le permet), et la délégation de la vérification est sa propre
   hypothèse. Décider séparément comment payer l'exécutant pour une telle réponse sans violer D1 : il n'y a pas de solution.
   **Décidé — D21 :** oui. Le réseau ne paie pas une réponse sans vérification. Un utilisateur sans équipement peut
   désigner lui-même un vérificateur ; c'est sa propre hypothèse, et le réseau ne lui promet pas D1.
   La garantie D1 pour un tel utilisateur reste une question ouverte.
5. **Faut-il autoriser des changements de produit pour une vérification exacte bon marché ?** Cela inclut le choix canonique
   du jeton par Gumbel-max (change la distribution par rapport à l'échantillonnage habituel top-p/top-k),
   le profil entier exact (peut dégrader la qualité), les tâches à issue vérifiable (formules,
   tests) et de nouveaux optimiseurs avec un certificat exact (Gauss–Newton, régression ridge).
   *Recommandation du conseil :* autoriser comme types de tâches séparés du plan avec un contrat explicite, après
   les expériences O5 et le calcul M17.
   **Décidé — D22 :** autoriser comme types de tâches séparés du plan avec un contrat explicite, après O5 et M17.
   L'échantillonnage habituel reste disponible avec la mention « non vérifié ».
6. **Comment limiter les faux litiges du payeur sans caution ?** D8 limite les litiges par le nombre de
   requêtes, mais une coalition qui paie ses propres requêtes contourne cette limite. *Recommandation
   du conseil :* calculer le coût d'un faux litige (M9) avant de décider ; le conseil n'a pas trouvé de règle qui n'exige pas
   de caution.
   **Décidé — D23 :** d'abord le calcul M9. PPS n'est pas inclus tant qu'une règle
   de limitation des faux litiges sans caution n'a pas été choisie pour lui.
7. **Faut-il conserver le cryptogramme de la réponse dans le journal ?** Sans cela, l'exécutant peut retenir la réponse.
   *Recommandation du conseil :* oui, environ 2–4 Ko par réponse ; c'est compatible avec D10.
   **Décidé — D24 :** oui, le cryptogramme est inscrit au journal en une seule écriture avec l'acceptation.
8. **La formulation bilatérale de D1 est-elle nécessaire aussi pour une falsification partielle ?** Le travail claude2 demandait
   si une falsification pire que le travail honnête mais meilleure que l'inaction est admissible. La formulation formelle
   de D1 dans [THREAT_MODEL](THREAT_MODEL.md), section 1.5, exige déjà les deux inégalités. *Recommandation
   du conseil :* ne pas changer ; c'est pourquoi VYa-S et PVYa dans leur variante relative sont rejetés.
   **Décidé — D25 :** ne pas changer.

---

## 7. Qui a fait quoi

Le conseil de modèles a travaillé à partir des matériaux du projet, sans accès au réseau et sans expériences.

- **Tour 1, six travaux indépendants :** deux travaux ChatGPT (gpt1, gpt2), deux travaux DeepSeek
  (ds1, ds2), deux travaux Claude (claude1, claude2). Chacun a analysé les directions de l'étape 4
  de la feuille de route, proposé ses propres mécanismes et calculé leur coût. De courts programmes arithmétiques
  ont été exécutés par claude1, claude2, gpt1 et gpt2 ; gpt1 et gpt2 ont joint de petites énumérations
  avec hachages de contrôle.
- **Tour 2, trois critiques :** une de ChatGPT, une de DeepSeek et une de Claude. Chaque critique a lu les six
  travaux, cherché des contre-exemples et recalculé les nombres clés. Les critiques ChatGPT et DeepSeek ont répété les petites
  énumérations de gpt1 et gpt2 sur processeur ; les hachages ont coïncidé.
- **Synthèse :** ce document a été rédigé par Claude d'après les travaux et les critiques. Là où les critiques ont divergé, la mention
  « contesté » figure. Lors de la synthèse, les décisions D6–D17, que les participants n'avaient pas, ont été appliquées aux conclusions ; aucune nouvelle
  estimation ni aucun nouveau nombre au-delà des travaux et des critiques n'a été ajouté.
