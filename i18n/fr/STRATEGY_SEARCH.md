<!-- translation of docs/STRATEGY_SEARCH.md, source sha256: 9c3fdac8710ac98433828b793ab6aad7fd31da5661c1fecb590bb7c63a2cdd26 -->

# Vérification « sans y aller frontalement » : ce que les mathématiques apportent à la place du recalcul complet

[English](../../docs/STRATEGY_SEARCH.en.md) · [中文](../zh/STRATEGY_SEARCH.md) · [Español](../es/STRATEGY_SEARCH.md) · **Français** · [Deutsch](../de/STRATEGY_SEARCH.md) · [Italiano](../it/STRATEGY_SEARCH.md) · [Русский](../../docs/STRATEGY_SEARCH.md) · [Português](../pt/STRATEGY_SEARCH.md) · [العربية](../ar/STRATEGY_SEARCH.md)

État au 25 novembre 2026.

Ce document est le résultat du cinquième conseil de modèles. Le propriétaire du projet a demandé mot pour mot :

> « Peut-être aurait-il du sens de choisir une autre stratégie ? Par exemple, brancher un peu de
> mathématiques ? Pour ne pas tout vérifier à la suite, mais prédire une tentative de tromperie et vérifier
> seulement dans ce cas ? Ou faire une analyse intelligente du travail du réseau skynet et trouver un
> comportement suspect ? Réfléchissez dans cette direction, à ce que la science offre encore qui puisse
> aider à ne pas résoudre frontalement. »

Le conseil a examiné la théorie des jeux d'inspection, la vérification selon le risque, la recherche
d'anomalies, les pièges, la vérification par échantillonnage, les mécanismes sans vérification, la
cryptographie et l'économie sans cautions, puis a proposé une stratégie et des versions révisées des
décisions.

**Statut du document.** C'est un résultat de raisonnement et de calcul par formules, non une mesure.
Il n'y a eu pour lui ni expériences, ni lancements de réseau, ni installations. Les participants et les
critiques n'ont exécuté que de courts programmes arithmétiques et de petites énumérations sur processeur.
Les nombres mesurés proviennent uniquement des [résultats de l'expérience D5](EXPERIMENT_D5.md) (synthèse
D5_RESULTS au 25 novembre 2026) et sont marqués [mesuré] ; les nombres obtenus par les formules à partir de
paramètres nommés explicitement sont marqués [calcul]. Les travaux des chercheurs sont cités **de mémoire** :
il n'y avait pas de réseau, les textes des sources primaires n'ont pas été vérifiés. **Seules les décisions
D1–D25** de [ROADMAP](ROADMAP.md), section 3, sont des décisions acceptées. Tout le reste ici est une
évaluation et des recommandations du conseil. Là où les critiques ont divergé, cela est dit directement.

## 1. Bref bilan

1. **« Prédire la tromperie et ne vérifier que les suspects » n'économise pas de vérifications lorsque les
   règles sont ouvertes.** Les règles de vérification sont identiques pour tous les nœuds et connues du
   trompeur (D4). Il ne soumet une falsification que là où le détecteur dit « sans risque », et jusqu'au
   moment de la tromperie il se comporte comme un honnête. Il est strictement démontré que le détecteur
   n'élève la probabilité de vérification d'une falsification au-dessus de la vérification moyenne du
   travail honnête que d'au plus la distance entre leurs distributions observables (section 2). Par
   conséquent, la prédiction, les anomalies, la confiance fondée sur l'historique et les graphes ne peuvent
   qu'**ajouter** des vérifications au-delà de la borne inférieure, mais non descendre la fréquence sous
   celle-ci. Les six travaux et les trois critiques sont d'accord.
2. **Il y a exactement deux signes infalsifiables :** le résultat d'un recalcul exact après que la réponse a
   été irrévocablement fixée, et la somme en attente brûlable — les récompenses de la clé pas encore payées,
   qui disparaîtront en cas de prise. Toute l'économie réelle vient du second signe, et non de
   « l'intelligence ».
3. **La meilleure stratégie trouvée pour les réponses du modèle :** le payeur vérifie lui-même sa réponse en
   une passe, et prend la décision « vérifier ou non » **par sa pièce secrète** après la fixation de la
   réponse, avec une probabilité non inférieure à `R/(R + H_lock)`. Ici `R` est le prix de la tâche,
   et `H_lock` — la partie des récompenses non arrivées à maturité de l'exécutant qui n'aura pas le temps
   d'arriver à maturité avant la fin de la vérification. La réponse d'un débutant au compte vide est toujours
   vérifiée. Alors, sous les conditions de la section 4, la falsification n'est rentable pour aucune part de
   collusion des autres, y compris en cas de collusion totale. Deux critiques sur trois soutiennent cette
   stratégie ; le critique ChatGPT préfère la vérification complète de chaque réponse (section 6).
4. **Le coût de la vérification elle-même est alors de fractions de pour cent :** environ 0,005–2 % du
   travail selon le calendrier et la charge de la clé, chez les clés peu actives avec limitation du dommage —
   jusqu'à 6,7 % [calcul]. Le coût principal passe dans le profil exact : il est 1,5–1,8 fois plus lent
   qu'une génération 8 bits ordinaire avec un lot de 1 et 2,5–2,8 fois avec un lot de 8 [mesuré]. Ensemble,
   cela fait +50…+82 % par rapport à la génération ordinaire avec un lot de 1 [calcul]. Le repère de 5 %
   bute sur la vitesse du profil exact, non sur la vérification.
5. **Le dommage n'est pas couvert par l'économie.** Le saboteur n'a pas besoin de gain : avec une
   vérification par échantillonnage, une partie de ses falsifications passe (environ la moitié avec le
   calendrier le moins cher, section 4). C'est pourquoi une réponse non vérifiée doit porter la mention
   « non vérifié », et « vérifié » n'est mis qu'après une vérification complète avant l'affichage. Pour
   l'étape d'apprentissage, le conseil n'a trouvé aucune nouvelle garantie.
6. **L'utilisateur sans équipement** n'est pas protégé par cette stratégie : si des nœuds étrangers aléatoires
   vérifient à sa place, la fuite est égale à `R·q^k` et, en cas de collusion totale, à tout le prix
   (section 5). Cela reste la question ouverte D21.
7. **Ce que le propriétaire doit décider :** autoriser ou non le paiement de ce qui n'est pas vérifié selon
   la règle de la pièce (D21, D11, D7) ; que faire des pannes honnêtes gratuites (D16), incompatibles avec la
   vérification par échantillonnage ; accepter ou non la nouvelle décision D26 sur le « verrou » de la somme
   en attente et la limite du remboursement à la victime ; la règle des litiges fallacieux (D23, calcul M9)
   reste une condition d'activation. Les questions sont formulées à la section 6.

**Notations.** `R` — prix de la tâche ; `c` — coût de revient du travail honnête ; `c_f` — coût de la
falsification (pire cas — presque nul) ; `H` — somme en attente de la clé de l'exécutant ; `H_lock` — sa
partie qui n'arrivera pas à maturité avant le résultat définitif de la vérification de cette tâche ; `p` —
probabilité de vérification de la tâche ; `q` — part de collusion parmi les vérificateurs ; `k` — nombre de
vérificateurs désignés ; `n_w` — nombre de tâches de la clé par fenêtre de maturation ; `ρ` — temps de
vérification d'une réponse en une passe divisé par le temps de sa génération (0,10–0,40 avec un lot de 1,
0,26–0,64 avec un lot de 8 [mesuré]) ; `γ` — ralentissement du profil exact par rapport à llama.cpp Q8_0
(1,5–1,8 avec un lot de 1, 2,5–2,8 avec un lot de 8 [mesuré]) ; PPS — vérification par le payeur lui-même.
`Δ₀` et `Δч` — différence attendue du gain de la falsification par rapport à l'inaction et par rapport au
travail honnête ; D1 et D25 exigent que les deux soient inférieures ou égales à zéro.

**Comment lire.** La section 2 — pourquoi la prédiction de la tromperie ne fonctionne pas. La section 3 —
tableau de toutes les approches. La section 4 — formules ayant résisté à la critique et erreurs trouvées. La
section 5 — stratégie recommandée, son coût et le risque résiduel. La section 6 — questions-décisions. La
section 7 — calculs et expériences. La section 8 — divergences non résolues et références douteuses. La
section 9 — qui a fait quoi.

## 2. Pourquoi « prédire la tromperie » ne fonctionne pas lorsque les règles sont ouvertes

### 2.1. Borne via la variation totale

Soit la décision de vérifier prise par une règle quelconque `π(x)` à valeurs de 0 à 1, où `x` est tout ce que
le réseau ou le payeur voient avant la décision : temps de réponse, texte, statistiques, historique de la
clé, graphe des liens. Le travail honnête donne des observations de distribution `P`, la falsification — de
distribution `F`. Alors

`E_F[π] − E_P[π] = Σ_x π(x)·(F(x) − P(x)) ≤ Σ_{x: F(x) > P(x)} (F(x) − P(x)) = TV(F, P)`.

L'inégalité est vraie parce que `π ≤ 1` là où `F > P`, et `π ≥ 0` là où `F < P`. La quantité `TV` est la
distance de variation totale : à quel point deux distributions sont en général distinguables. D'où
(théorème T4 du travail claude2 ; la même inégalité chez gpt1 et gpt2) :

1. **Une falsification n'est pas vérifiée plus souvent que le travail honnête en moyenne, plus `TV`.** Si la
   falsification est difficile à distinguer par les observations (`TV ≈ 0`), le détecteur la vérifie aussi
   rarement que le travail honnête.
2. **Contre un adversaire informé, c'est encore pire.** Les règles sont ouvertes (D4), donc l'adversaire
   calcule lui-même `π` et choisit l'observation pour laquelle la vérification est la moins probable. La
   probabilité de détection de sa meilleure falsification est égale au plus petit `π(x)` parmi les
   observations qu'il peut créer à bon marché.
3. **Conséquence pour l'économie.** Pour que la falsification soit déficitaire, elle doit être vérifiée avec
   une probabilité non inférieure à `R/(R + H_lock)` (section 4). Avec `TV ≈ 0`, il faudra tenir la même
   fréquence pour le travail honnête aussi, c'est-à-dire qu'il n'y a pas d'économie. Selon l'estimation de
   claude2, le gain de « l'intelligence » ne dépasse pas le facteur `R/(R − c*)`, où `c*` est le prix de la
   falsification indiscernable la moins chère ; avec un `c* ≈ 0,5R` plausible, cela ne dépasse pas un facteur
   deux, mais `c*` est choisi par l'adversaire et n'est pas mesuré.
4. **L'historique de la clé ne dit rien du moment de la tromperie.** Une clé qui décidera de tromper à la
   tâche suivante a, avant cette tâche, le même historique qu'une clé honnête (rapport de vraisemblance
   exactement 1 ; théorème T5 de claude2, contre-exemple de gpt1). C'est pourquoi les tests séquentiels
   (SPRT de Wald, CUSUM de Page), les algorithmes de bandit et la « confiance » bayésienne ne l'apprennent
   qu'après la tromperie. Une petite énumération de claude1 a montré : si l'on abaisse de 10 % sous le seuil
   la fréquence de vérification fondée sur la confiance, apparaît une stratégie rentable « accumuler la
   confiance et tromper » (+1,7R…+2,5R pour 60 tâches), et en la réduisant de moitié — +14,4R…+19,4R
   [calcul]. Le critique Claude a reproduit ces nombres, le critique DeepSeek a obtenu dans le modèle le plus
   proche une autre valeur (+0,085R), mais le même signe (section 8).

### 2.2. Exemple sur les mesures D5

La falsification bon marché la plus naturelle est **le même Qwen lancé dans llama.cpp Q8_0**. Le profil
exact est 1,5–1,8 fois plus lent qu'elle avec un lot de 1 et 2,5–2,8 fois avec un lot de 8 [mesuré], donc la
falsification est sensiblement moins chère que le travail honnête. Pourtant c'est la réponse du même modèle :
le temps, le style, la perplexité sous un petit modèle sont les mêmes que ceux d'une réponse honnête, et le
délai, l'exécutant peut l'ajouter lui-même. Si la réponse Q8_0 coïncide avec la réponse exacte jeton pour
jeton, ce n'est pas une falsification : selon D2, c'est le résultat qui compte. Si elle diverge ne serait-ce
qu'en un jeton, seul un recalcul exact le détectera, parce que les bits du profil exact coïncident sur tout
appareil testé [mesuré].

Réserve du critique ChatGPT : dans D5 est mesurée la proximité du profil exact avec le modèle officiel (le
même jeton à 90 positions sur 90, corrélation des logits 0,9996 [mesuré]), mais la proximité de la
falsification Q8_0 avec le profil exact selon des signes bon marché n'a pas été mesurée. Pour la garantie,
cela n'importe pas : il suffit que personne n'ait montré de signe distinguant chaque falsification
disponible d'une réponse honnête.

### 2.3. Où les détecteurs restent néanmoins utiles

Les détecteurs, les pièges et l'analyse du réseau sont admissibles s'ils **ne font qu'augmenter** la fréquence
de vérification :

- comme file de vérifications volontaires supplémentaires du payeur, qui ne comptent pas dans la garantie
  mais augmentent la détection réelle ;
- contre les saboteurs négligents qui n'optimisent pas leur comportement ;
- pour diagnostiquer les pannes de matériel et de pilotes ; un participant peut tenir un CUSUM sur ses
  auto-vérifications et s'arrêter avant de perdre la somme en attente ;
- sur un flux d'erreurs non adaptatif, ils trouvent plus d'erreurs par heure de vérification. Exemple de
  gpt1 [calcul] : avec une part de falsifications de 2 %, une sensibilité de 90 % et 5 % de fausses alarmes,
  8,57 % des tâches sont vérifiées, 90,2 % de cette famille de falsifications est détectée, coût 1,80 %
  contre 18,94 % pour une vérification uniforme. Mais une famille de falsifications que le détecteur ne
  signale pas passe dans 98 % des cas.

Il existe aussi une attaque inverse (claude2) : des requêtes pour lesquelles la réponse honnête paraît
« anormale » font dépenser des vérifications sur des honnêtes. Si c'est celui qui l'a provoquée qui paie la
vérification, cela se limite de soi-même ; si c'est le réseau, c'est un transfert de charge.

## 3. Analyse des approches

Dans le tableau, « garantit » — ce qui découle strictement sous les hypothèses nommées ; « avec `q` » — le
comportement selon la part de collusion des vérificateurs ; « compte vide » — un débutant avec `H = 0` et
beaucoup de clés gratuites ; « verdict » — le résultat après les trois critiques.

| Approche | Essence | Ce que cela garantit | Avec `q` et avec `q = 1` | Compte vide, plusieurs clés | Coût | Verdict après critique |
|---|---|---|---|---|---|---|
| Jeux d'inspection (Dresher, Maschler, la synthèse d'Avenhaus–von Stengel–Zamir ; jeux de sécurité de Tambe et al. — de mémoire) | Vérification aléatoire annoncée à l'avance, à une fréquence où la tromperie n'est pas rentable | `Δ₀ ≤ 0` pour `p ≥ (R − c_f)/(R + H_lock)`, y compris pour une vague de falsifications avant le départ (sous les conditions de la section 4) | Si c'est le payeur qui vérifie, cela ne dépend pas de `q`, y compris `q = 1`. Si ce sont des vérificateurs désignés — détection `p·(1 − q^k)`, nulle pour `q = 1` | `H = 0` ⇒ `p = 1` ; chaque clé répond sur sa propre somme, Sybil n'aide pas | `p·ρ` : centièmes à dixièmes de pour cent chez les clés actives ; vérification complète chez le débutant [calcul] | **Base de la stratégie**, si la fréquence est appliquée par celui dont l'argent est en jeu |
| Vérification selon le risque : SPRT, CUSUM, bandits, confiance bayésienne | Vérifier plus souvent les débutants et les suspects, moins souvent les anciens | Attrape vite un trompeur bruyant permanent ; rien contre un stratège | Le verdict fondé sur les opinions des vérificateurs se casse en cas de collusion ; nul pour `q = 1` | Les nouvelles clés sont gratuites ; une clé « ancienne » accumule la confiance et trompe à la fin | L'économie de 40–70 % (ds1) concerne un adversaire bruyant, pas SkyNet | Il est **interdit** de descendre la fréquence sous le seuil (contre-exemple de la section 2.1) ; on peut répartir des vérifications supplémentaires |
| Anomalies, graphes, Sybil (temps, logits, entropie, perplexité d'un petit modèle, filigranes, cohérence des répétitions, graphes de collusion, SybilGuard/SybilLimit/SybilRank) | Chercher un comportement et des liens suspects | Rien contre un adversaire qui connaît le détecteur (borne de la section 2.1) | Une falsification concertée ressemble à un accord honnête ; pour `q = 1`, il n'y a pas de protection | SybilRank exige des nœuds initiaux de confiance et un petit nombre de liens « attaquants » ; les liens, la coalition les achète par un travail honnête | La perplexité d'un petit modèle coûte environ 1,3–5 % de **chaque** réponse selon l'estimation de claude1 (critique ChatGPT : aux extrémités, ds2 1,875–9 %) [calcul], plus cher que la vérification selon la règle ; un filigrane n'atteste que l'échantillonneur | Seulement un **signal pour des vérifications supplémentaires** et un diagnostic des pannes |
| Pièges, gold questions, modèle de Dawid–Skene | Tâches à réponse connue, indiscernables des vraies | Seulement si le piège est indiscernable et la réponse secrète. Dans un réseau public, seul le payeur peut garder un secret, et le piège coïncide avec sa vérification (T9 de claude2) | La collusion partage instantanément les pièges ; Dawid–Skene suppose des erreurs indépendantes | Les clés à usage unique étudient les pièges par essais ; le type de tâche (D22) est visible pour l'exécutant | Une référence fraîche de texte libre coûte une génération complète, plus cher que la vérification (`ρ < 1`) ; pour le niveau `2⁻⁸⁰` avec une part de pièges de 10 %, il faut 526–527 désignations [calcul] | Pas moins cher que la vérification par le payeur ; forme admissible — la répétition d'une requête déjà vérifiée du payeur |
| Vérification par échantillonnage et loterie (partie des jetons ou des couches après fixation ; BOINC, TrueBit, opML, proof of sampling — de mémoire) | Vérifier une petite partie du calcul ; ou ne payer que ce qui est choisi par tirage au sort (loterie B) | Jetons : un défaut passe avec la probabilité `1 − s/N` (99,2 % pour 8 positions sur 1000 [calcul]). Loterie B avec vérification de la sélection par le payeur : `Δ₀ = −c_f` pour tout `p` | La loterie avec comité donne au débutant `R·q^k` : 0,001R / 0,027R / 0,125R / R pour `q` = 0,1 / 0,3 / 0,5 / 1, `k = 3` [calcul] | La loterie B avec le payeur convient au débutant ; l'échantillonnage de jetons — non | État de Qwen3.5-4B : 48 MiB + 64 KiB par position, un échantillon à la position 500/1500/4000 — 79/142/298 MiB [calcul] ; la loterie donne un revenu irrégulier et exige un prépaiement `R/p` | Les jetons et les couches sont **pires** que la passe complète, tant en trafic qu'en garantie ; la loterie B avec le payeur est une variante admissible. Les systèmes externes reposent sur une caution ou sur « un honnête sur N » |
| Peer prediction (Bayesian Truth Serum de Prelec, peer truth serum, DMI — de mémoire) | Payer la cohérence des rapports sans vérification | La sincérité n'est un équilibre que sans collusion ; il existe des équilibres non informatifs | Pour `q > 0`, le groupe se met d'accord ; pour `q = 1`, le mécanisme paie n'importe quoi | Billets gratuits pour chaque clé | Pas de vérification, mais on paie on ne sait quoi | **Inapplicables** à un calcul déterministe ; payer la coïncidence, c'est payer la copie, ce que D15 interdit |
| Cryptographie sans preuve complète, TEE, graine | Engagements et révélations échantillonnées, litige par division en deux, sumcheck/GKR, attestation TEE, génération déterministe | L'échantillonnage sans encodage — la même borne `1 − s/N` ; la preuve complète — oui sous D19, mais selon l'estimation de l'étape 4, 16,8 fois plus cher, et plus cher encore pour la réponse ; TEE — confiance au fabricant | Le litige et le déterminisme ne dépendent pas de `q` ; avec TEE, une clé extraite frappe tout le parc | Réduire la fréquence selon l'attestation donnerait la fréquence réduite à toutes les clés de l'adversaire | Engagement sur la réponse — 2–4 Ko dans le journal (D24) | Il faut un engagement sur la réponse, une pièce secrète et un litige par moitié ; TEE — seulement pour augmenter la vérification ou la confidentialité. La proposition de ds1 de réduire la fréquence selon TEE a été rejetée par tous les critiques |
| Économie sans cautions (paiements différés, réputation comme capital, assurance, prix de la clé payé par le travail) | Punir par la perte des récompenses non arrivées à maturité et du revenu futur | La somme en attente est le seul levier compatible avec R5. Le revenu futur en cas de départ est nul. L'assurance indemnise la victime mais ne réduit pas le gain du trompeur | Fonctionne si la fréquence est appliquée par le payeur | `H = 0` ⇒ vérification complète. L'entrée par le travail est une caution cachée, inutile en cas de départ ; avec une fuite par comité `R·q³` et `q = 0,3`, un prix d'entrée de `10R` est amorti en environ 370 tentatives (ds1) [calcul] | Report du paiement d'une fenêtre de maturation | `H_lock` est une partie obligatoire de la stratégie ; le reste ne sert pas de base à une garantie |

## 4. Bornes inférieures et formules ayant résisté à la critique

### 4.1. Falsification isolée : le seuil `R/(R + H_lock)`, et non `R/H`

Une falsification détectée n'est pas payée et brûle la somme en attente (rien d'autre ne peut être débité
selon R5). Alors

`Δ₀ = (1 − p)·R − p·H_lock − c_f ≤ 0  ⇔  p ≥ (R − c_f)/(R + H_lock)`,

et pour une falsification presque gratuite — `p ≥ R/(R + H_lock)`. Par rapport au travail honnête
`Δч = Δ₀ − (R − c) ≤ Δ₀`, donc la seconde condition de D25 est satisfaite d'elle-même. Chez le débutant
`H_lock = 0`, et `p = 1`. Fréquence minimale [calcul, claude2] : 0,5 pour `H_lock = R` ; 0,25 pour `3R` ;
0,0909 pour `10R` ; 0,01 pour `99R` ; 0,000231 pour `4320R`.

Le travail claude1 a proposé la règle `p = min(1, R/H)` et l'a dite exacte. Le critique Claude a montré par
énumération que le seuil exact est `R/(R + H)` : avec lui, le plus grand gain de la falsification est
exactement 0, et déjà avec `0,99·R/(R + H)` — de +0,225R à +0,299R [calcul]. La règle `R/H` contient une
marge. Le critique DeepSeek a noté que cette marge est utile contre le dommage : avec `R/H`, le nombre
attendu de falsifications avant la prise est fini (environ `H/R + 1`), avec `R/(R + H)` — infini (section
4.4). Quelle formule prendre dans le noyau n'est pas décidée (section 8).

### 4.2. Condition : la somme n'arrive pas à maturité avant le résultat de la vérification

On ne peut brûler que ce qui n'est pas encore payé au moment du litige prouvé. Si une partie de `H` arrive à
maturité plus tôt, la règle se casse. Contre-exemples [calcul] :

- claude2 : une clé avec `H = 99R` arrivant à maturité avant le résultat soumet `n` falsifications à
  `p = 1 %` ; gain 0,99R pour `n = 1`, 9,04R pour 10, 36,6R pour 100 ;
- critique Claude : une clé avec `H₀ = 100R` cesse le travail honnête et soumet des falsifications, et les
  payeurs vérifient tard ; gain +0,99R, +9,1R, +49,7R, +74,4R pour `n` = 1, 10, 100, 300. Avec le « verrou »
  (tout brûle), les mêmes stratégies donnent de −0,01R à −0,75R.

C'est pourquoi le dénominateur de la fréquence pour la tâche `i` ne contient que la partie de la somme qui
arrivera à maturité **après** le délai extrême de litige sur `i`, et le délai de vérification par le payeur
`δ` doit être beaucoup plus petit que la fenêtre de maturation `W` ; les deux délais sont comptés en temps
actif (D12). C'est l'hypothèse de « vérification en temps utile » ; pour un téléphone qui se connecte
rarement au réseau, elle est violée la première.

### 4.3. Vagues de falsifications avant le départ

Une vague de falsifications avant le départ n'est couverte par la formule de la falsification isolée que sous
la règle **« la première prise prouvée brûle toute la somme non arrivée à maturité de la clé, y compris les
récompenses de la même vague »**.

- Sans cette règle (gpt1) : 10 falsifications parallèles avec `R = 1`, `B = 4R`, `d = 0,2`, lorsque chaque
  falsification non détectée est payée et que l'ancienne somme n'est perdue qu'une fois, donnent
  `10·0,8 − 4·(1 − 0,8¹⁰) = +4,4295R`, alors qu'une seule falsification donne zéro. Si la prise annule toute
  la vague, la même stratégie donne −2,49676R [calcul ; répété par les critiques].
- Le critique ChatGPT a ajouté un second exemple : avec `H = R`, `p = 1/2`, deux falsifications à pièces
  indépendantes et un débit unique de l'ancienne somme, le gain est `R/4` [calcul]. Donc le protocole doit
  lier atomiquement tous les engagements ouverts de la clé à toute sa recette non arrivée à maturité.

Sous cette règle, la démonstration de claude2 (T2) est correcte : chaque nouvelle falsification multiplie le
résultat attendu par `(1 − p_j)·(1 + α_j/(H_lock + A)) ≤ 1`, où `α_j` est le paiement pour le non-vérifié, et
`A` — ce qui est déjà accumulé de brûlable. L'induction sur le nombre de falsifications donne
`E[résultat] ≤ H_lock` pour toute vague et toute suite adaptative. Pour une vague homogène, la même chose
découle de `(1 + R/H)ⁿ ≥ 1 + nR/H`. La vérification sur une grille de fractions exactes a donné un
dépassement maximal exactement 0 [calcul].

### 4.4. Vérification par comité : le facteur `1 − q^k`

Si la prise doit être constatée par au moins un des `k` vérificateurs désignés, et si chacun appartient à la
coalition avec la probabilité `q`, la probabilité de prise tombe à `p·(1 − q^k)`, et le seuil devient
`p ≥ R/((R + H_lock)·(1 − q^k))`. Il est irréalisable lorsque `1 − q^k < R/(R + H_lock)` et toujours
irréalisable pour `q = 1`. Dans la loterie B avec comité, le débutant reçoit `R·q^k` par tentative :
0,001R / 0,027R / 0,125R / R pour `q` = 0,1 / 0,3 / 0,5 / 1 et `k = 3` [calcul]. Cela coïncide avec le modèle
de l'adversaire. L'indépendance des choix est aussi une hypothèse : en choisissant `k` différents parmi `N`
participants dont `C` sont en collusion, la probabilité de collusion totale est `C(C,k)/C(N,k)` ; en cas
d'indisponibilité générale des données ou de délivrance sélective, elle peut atteindre `q` ou 1 (critique
ChatGPT selon le modèle de l'adversaire). Conclusion de tous les travaux : **la fréquence doit être appliquée
par celui dont la décision est protégée** — le payeur pour son argent, chaque nœud pour sa propre comptabilité.

### 4.5. Dommage : la part non détectée

Le saboteur n'a pas besoin de gain, c'est pourquoi le dommage est évalué par la part de ses falsifications
passées sans prise.

- **Le calendrier le moins cher rend le dommage illimité.** Avec `p = R/(R + H)`, les falsifications non
  vérifiées augmentent elles-mêmes `H`, et la fréquence baisse. La probabilité de survivre à `n`
  falsifications depuis le départ `h = H/R` est égale à `h/(h + n)` ; le nombre attendu de falsifications
  avant la prise est infini (T8 de claude2). L'estimation de claude1 « `e^{−m}` » sous-estime le passage :
  avec `H₀ = 4320R` et 4320 falsifications, le passage exact est 0,50 au lieu de 0,37 à la fréquence
  `m·R/H` avec `m = 1` ; 0,125 au lieu de 0,050 avec `m = 3` ; 0,0078 au lieu de 0,0009 avec `m = 7`
  [calcul, critique Claude].
- **Une falsification ciblée** passe avec la probabilité `1 − p` : chez une clé mûre avec `n_w = 4320`,
  environ 99,977 % (critique ChatGPT) [calcul].
- **La correction selon la partie vérifiée de la somme n'a pas tenu.** claude2 a proposé de calculer la
  fréquence selon `H_ver` — les récompenses des seules tâches vérifiées ; alors, chez une clé honnête
  `p ≈ 1/√n_w` (point fixe `p²·n_w + p − 1 = 0`) et la part de falsifications du saboteur est d'environ `p` :
  5,6 % avec `n_w = 300`, 1,8 % avec 3000, 0,58 % avec 30 000 [calcul]. Le critique Claude a montré que
  `H_ver` est gonflé par les requêtes auto-payées de la coalition ; le critique ChatGPT — qu'un saboteur avec
  une nouvelle clé, après une réponse vérifiée à `p = 1/2`, obtient qu'environ la moitié de ses réponses
  livrées soient fausses. Aucun travail n'a trouvé de borne économique du dommage qui résiste à
  l'auto-paiement et aux nouvelles clés.

Conclusion : pour tout `p < 1`, une partie des réponses du saboteur est fausse. Pour les requêtes, cela n'est
admissible qu'avec la mention « non vérifié » (texte D6), pour l'étape d'apprentissage — non.

### 4.6. Autres formules ayant résisté à la critique

- **Les pannes gratuites sont incompatibles avec la vérification par échantillonnage** (claude1). Si une
  panne honnête ne brûle pas la somme (D16), un trompeur pris appelle sa falsification une panne, et
  `Δ₀ = (1 − p)·R − c_f > 0`. Avec `b` pannes gratuites par fenêtre, la fuite est de l'ordre de `b·H` par
  fenêtre [calcul].
- **Les payeurs paresseux** (claude2). Si une part `λ` des payeurs ne vérifie pas et que l'exécutant ne les
  distingue pas, il faut `p·(1 − λ) ≥ R/(R + H_lock)`. S'il les distingue — la falsification contre eux
  rapporte jusqu'à `R` sans risque. La dissuasion est un bien commun : un payeur qui coupe la vérification
  économise des fractions de pour cent et ne perd rien. C'est l'hypothèse « les payeurs appliquent en moyenne
  la pièce du noyau ».
- **Coût et irrégularité de la loterie B** (claude2, T7, avec la correction du critique ChatGPT). Le paiement
  `R/p` avec la probabilité `p` donne un coefficient de variation du revenu `√((1 − p)/(pT))` pour `T`
  tâches. Pour un écart donné `v`, il faut `p ≥ 1/(1 + T·v²)` ; avec `T = 6000`, `v = 10 %`, `ρ = 0,21`, le
  coût minimal de vérification est 0,3443 % [calcul]. Avec une vérification « par chacun des 1000 nœuds », le
  même coût est multiplié par le nombre de nœuds, c'est pourquoi la loterie avec vérification par tous les
  nœuds est inutilisable pour l'émission de crédits.
- **La collusion du payeur et de l'exécutant** se réduit à un transfert de leur propre argent à l'intérieur
  de la coalition, tant que la requête payée ne crée pas d'émission de crédits, de poids et de droit à
  indemnisation sur la caisse commune.

### 4.7. Erreurs dans les formules des travaux (brièvement)

| Travail | Erreur | Correction |
|---|---|---|
| ds2 | Le second seuil est écrit `(c − c_f)/R` | Il faut `(c − c_f)/(R + H)` ; ce seuil n'est jamais contraignant. Ne transmettre aux mini-agents que la version corrigée |
| ds1 | Dans le jeu, la perte est prise `L = H + V` sans tenir compte de `c_f` déjà dépensé | Seuil `(R − c_f)/(R + H + V)` ; pour `H = 0`, `c_f = 0,1R` — 90 %, et non 100 % |
| claude1 | Équilibre du jeu d'inspection avec `L = H + R` (double comptage de `R`) | Point d'indifférence `(R − c_f)/(R + H)` : pour `H = R`, `c_f = 0` — 1/2, et non 1/3 |
| claude1 | « La règle `R/H` est exacte » ; dommage `e^{−m}` | Seuil exact `R/(R + H)` ; le passage est plus élevé (section 4.5) |
| claude1 | Génération spéculative « environ `1 + ρ·s` » | Non dérivé ; selon le critique DeepSeek — double comptage ; avec un lot de 8, on obtient 1,65–2,79 |
| claude2 | T7 : « `κ·CV²` ne dépend pas de `p` » | Il y a un facteur `1 − p` ; seuil exact `p ≥ 1/(1 + T·v²)` |
| claude2 | Le coût synthétique 0,2–1,2 % est pris pour `n_w = 3000` | Pour `n_w = 300` — 0,56–2,24 % (jusqu'à 3,6 % avec un lot de 8), pour `n_w = 30` — 1,7–6,7 % [calcul] |
| claude2 | Instantanés d'état de 0,33 et 2,9 GiB par réponse | Avec un cache d'attention de 0,651 GiB (500/500, pas 64) et 12,38 GiB (2000/1000, pas 16) [calcul, critique ChatGPT] |
| claude2 | Dans S1, le paiement du non-vérifié `α` avec la règle selon `H_ver` est toujours égal à `R` | Il n'y a pas de transition progressive A/B dans S1 ; une balise commune pour la décision de vérification n'est pas nécessaire |
| ds1, gpt1, gpt2 | Estimations de stratégies sans le ralentissement du profil exact | Le coût complet est 1,5–1,8 fois plus élevé dès le lot de 1 (section 5.2) |
| ds1 | « La vérification de `k` jetons n'est pas moins chère qu'une passe complète » | En calculs, elle est moins chère ; elle perd en trafic d'état et en garantie |
| gpt2 | Certificat par bornes de logits : 6,25 % | Les bornes exigent l'état vrai de la dernière couche ; la tête représente environ 15 % des multiplications, l'économie ne dépasse pas sa part |
| ds2 | Part stable de tromperie contre CUSUM `θ = d_h/(d_h + d_f)` | C'est une approximation par dérive moyenne, non un théorème |
| ds1 | SPRT : 65 et 133 observations | Recalcul exact du critique ChatGPT : 132,73 et 76,70, test fixe — 229 [calcul] ; ne concerne pas un adversaire stratégique |

## 5. Stratégie recommandée

### 5.1. Réponses du modèle : « le payeur-inspecteur avec mise »

Le noyau est tiré des travaux claude1 et claude2, les corrections — de gpt1 et des trois critiques.

1. **Profil exact.** Chaque réponse payée est générée dans le profil exact v2 (choix glouton ou Gumbel-max
   canonique), le cryptogramme de la réponse est inscrit au journal en une seule écriture avec l'acceptation
   (D24).
2. **Pièce secrète du payeur.** Une fois la réponse irrévocablement fixée, le programme du payeur décide, par
   son aléa secret, s'il la vérifie en une passe, avec la probabilité
   `p_i = max(p_user, R_i/(R_i + H_lock))`. `p_user` est choisi par l'utilisateur lui-même ; avec
   `p_user = 1`, il ne voit que des réponses vérifiées. Avec `H_lock = 0` (débutant), la vérification est
   toujours faite. Une balise commune n'est pas nécessaire pour cela tant que le paiement ne dépend pas du
   résultat de la pièce ; la décision n'attend pas de bloc public.
3. **Verrou de la somme.** `H_lock` pour la tâche `i` — les récompenses non arrivées à maturité de la clé qui
   arriveront à maturité après le délai extrême de litige sur `i` ; le délai de vérification `δ` est bien plus
   petit que la fenêtre de maturation (section 4.2).
4. **Brûlage.** Toute divergence prouvée brûle **toute** la somme non arrivée à maturité de la clé, y
   compris les récompenses de la même vague. À la victime n'est rendu que son paiement `R` au plus, le reste
   est détruit. Sinon une attaque « d'auto-litige » est possible : la coalition attrape avec sa clé-payeur une
   requête auto-payée falsifiée exprès et prend les sommes d'autrui en contournant la fenêtre de maturation
   (critique Claude).
5. **Mentions.** « Vérifié » — seulement une réponse entièrement vérifiée avant l'affichage. Tout le reste est
   par défaut « non vérifié ». La mention « vérifié par échantillonnage » (claude1) a été rejetée par tous les
   critiques comme trompeuse.
6. **Signaux seulement vers le haut.** Les anomalies, la perplexité, les graphes, les répétitions de requêtes
   vérifiées (pièges) ne déclenchent que des vérifications volontaires supplémentaires. Il est interdit de
   réduire la fréquence selon l'historique, la réputation, les anomalies, l'attestation ou le nombre de clés.
7. **Litiges** — seulement par preuve de divergence, que chaque nœud vérifie lui-même (I8). La stratégie n'est
   pas activée sans règle des litiges fallacieux (D23, calcul M9).
8. **Variante pour les clés à petite somme.** Là où une vérification fréquente coûte cher au payeur, la
   loterie B est admissible : seule la réponse choisie par tirage au sort est payée, son payeur la vérifie
   entièrement (gpt1, claude2). En elle, la panne honnête gratuite (D16) est conservée sans changement, mais
   le revenu de l'exécutant est irrégulier, et le payeur garde un prépaiement `R/p`.

La stratégie exige de modifier D16 et D21 (section 6). Tous les zéros de la garantie sont conditionnels :
coïncidence des bits sur les appareils testés, et non sur tout appareil ; vérification en temps utile ;
vivacité du journal et absence de censure de la preuve ; correction du noyau ; exécution honnête de la pièce
par le programme du payeur ; règle des litiges fallacieux.

### 5.2. Coût

Paramètres : `p = R/(R + H)` avec `H ≈ n_w·R` établi ; `ρ` = 0,10 / 0,21 / 0,40 (lot de 1) ; `γ` = 1,5–1,8
(lot de 1) et 2,5–2,8 (lot de 8). Coût complet contre Q8_0 — `γ·(1 + p·ρ) − 1`. Tableau du critique Claude
[calcul] :

| `n_w` (tâches de la clé par fenêtre) | `p` stable | Vérification pour `ρ` = 0,10 / 0,21 / 0,40 | Total contre Q8_0, lot de 1 | Total, lot de 8 | Vérifications dans la première fenêtre d'une nouvelle clé |
|---|---|---|---|---|---|
| 30 | 3,23% | 0,32% / 0,68% / 1,29% | +50,5% … +82,3% | +152% … +186% | environ 4,0 |
| 300 | 0,33% | 0,033% / 0,070% / 0,133% | +50,0% … +80,2% | +150% … +181% | environ 6,3 |
| 4320 | 0,023% | 0,002% / 0,005% / 0,009% | +50,0% … +80,0% | +150% … +180% | environ 9,0 |

Autres calendriers [calcul] : à la fréquence minimale en argent `p ≈ t_task/t_lock ≈ 2,3·10⁻⁴`, la
vérification coûte environ 0,005 % du travail (critique DeepSeek) ; à la fréquence avec limitation du dommage
`p ≈ 1/√n_w` — 0,18–0,72 % avec `n_w = 3000` et 0,56–2,2 % avec `n_w = 300` ; avec la loterie B à `p = 5 %` —
0,5–2,0 % avec un lot de 1. Si l'on ajoute à la règle monétaire un plancher contre le dommage selon `H_ver`,
la vérification monte à 0,15–2,2 % avec `n_w` = 300–4320 et à 6,7 % avec `n_w = 30` (critique Claude). La
première tâche du débutant coûte une vérification complète, 10–40 % de sa génération.
Pour comparaison : la vérification complète de chaque réponse (contrat principal de gpt1, gpt2, ds2) coûte
`γ·(1 + ρ) − 1` = +65…+152 % contre Q8_0, avec `γ = 1,65`, `ρ = 0,21` — +99,65 % [calcul].

Non comptés : l'écriture de 2–4 Ko par réponse dans le journal, les litiges fallacieux (M9), l'énergie, la
vérification sur les appareils des payeurs. **Le goulot d'étranglement du repère de 5 % est le ralentissement du profil
exact, non la vérification.** Peuvent le réduire des noyaux rapides à bits égaux et le décodage spéculatif
exact : le brouillon est généré par le Q8_0 rapide, et le profil exact accepte le préfixe jusqu'à la première
divergence. Estimation de claude2 avec 99 % de jetons coïncidents et un bloc de 32 — environ 0,78 du temps du
jeton exact, soit +28 % au-dessus de Q8_0 au lieu de +65 % ; avec 95 % de coïncidence — 1,33 du temps du jeton
exact, pire que la génération directe (critique Claude) [calcul ; la coïncidence n'est pas mesurée].

### 5.3. Risque résiduel

Gain attendu par falsification ; « dommage » — la part de falsifications non détectées du saboteur, toutes
avec la mention « non vérifié ». Synthèse du critique Claude et du critique DeepSeek [calcul].

| Cas | `q = 0,1` | `q = 0,3` | `q = 0,5` | `q = 1` | Débutant, `H = 0` |
|---|---|---|---|---|---|
| Argent, le payeur vérifie lui-même | ≤ 0 | ≤ 0 | ≤ 0 | ≤ 0 | `−c_f` (vérification toujours) |
| Réponse fausse présentée comme « vérifiée » | 0 | 0 | 0 | 0 | 0 |
| Dommage pour `p = R/(R + H)` : non détecté après `n_w` falsifications | environ 50% | environ 50% | environ 50% | environ 50% | 0 (les premières sont vérifiées) |
| Idem pour `p = 3R/(R + H)` | environ 12,5% | de même | de même | de même | 0 |
| Payeur sans équipement confie la vérification à un groupe aléatoire de trois nœuds | +0,001R | +0,027R | +0,125R | +R | de même |
| Le payeur ne vérifie pas, l'exécutant le distingue | jusqu'à +R | jusqu'à +R | jusqu'à +R | jusqu'à +R | 0 |
| Apprentissage, il existe un auditeur honnête de pleine fréquence | ≤ 0 | ≤ 0 | ≤ 0 | — | `−c_f` |
| Apprentissage, pas d'auditeur honnête | jusqu'à +R | jusqu'à +R | jusqu'à +R | jusqu'à +R | jusqu'à +R |

Les lignes « le payeur vérifie lui-même » ne dépendent pas de `q`. C'est là le résultat principal du conseil :
une vérification indépendante de la part de collusion est peu coûteuse chez le payeur s'il vérifie par
échantillonnage, et la somme brûlable de l'exécutant est verrouillée jusqu'à la fin de la vérification.

### 5.4. Débutant

Une clé au compte vide est toujours vérifiée, c'est pourquoi une falsification chez elle donne `−c_f`. À
mesure que la somme verrouillée s'accumule, la fréquence baisse : avec la règle `R/(R + H)`, dans la première
fenêtre, environ 4,0 / 6,3 / 9,0 vérifications complètes avec `n_w` = 30 / 300 / 4320 (critique Claude), avec
la règle `R/H` — 5,0 / 7,3 / 10,0 (claude1) [calcul]. Le coût de la première fenêtre avec `n_w = 30` —
1,7 / 3,5 / 6,6 % avec `ρ` = 0,10 / 0,21 / 0,40 (claude1) [calcul]. Le « prix d'entrée » est un travail utile
vérifié entièrement, non une contribution d'entrée. Le revers — la charge : une coalition de nouvelles clés
oblige les payeurs à vérifier chacune de leurs réponses. Cela frappe le coût (R6), mais non D1 ; la grandeur
doit être calculée (section 7).

### 5.5. Utilisateur sans équipement

La stratégie ne le protège pas. S'il confie la vérification à un groupe aléatoire de trois nœuds étrangers,
la fuite attendue est `R·q³` : 0,001R / 0,027R / 0,125R / R pour `q` = 0,1 / 0,3 / 0,5 / 1 [calcul]. S'il la
confie à son appareil ou à un nœud de connaissance, c'est son hypothèse selon D21 ; en cas de collusion de
l'auxiliaire avec l'exécutant, une fausse attestation est possible avec la probabilité 1. Le critique Claude
propose de vérifier par l'expérience combien coûte une vérification en une passe sur le processeur d'un
ordinateur portable et d'un téléphone : à une fréquence d'environ une vérification par fenêtre de clé, une
vérification rare et lente peut s'avérer acceptable. La garantie pour un tel utilisateur reste la question
ouverte D21.

### 5.6. Apprentissage

Pour l'étape d'apprentissage, le conseil n'a trouvé aucune nouvelle garantie. L'étape n'a pas de payeur dont
l'argent est en jeu, c'est pourquoi la vérification par échantillonnage doit être appliquée par chaque nœud
qui a besoin de la garantie, et le coût est multiplié par le nombre de ces nœuds. Variantes :

- **Répétition complète de l'étape** depuis le parent accepté — environ 100 % du travail de l'étape pour
  chaque nœud vérificateur. Exemple du critique ChatGPT : si l'inférence représente 80 % du travail de base,
  `ρ = 0,21` et chaque étape est répétée une fois, on obtient 0,8·0,21 + 0,2·1 = 36,8 % au-delà du travail de
  base [calcul] ; avec `N` nœuds vérifiant eux-mêmes, le second terme est multiplié par `N`.
- **Vérification par échantillonnage de l'étape par tous les nœuds complets** (claude2, S2) : seulement pour
  l'argent avec une fenêtre de 3 jours — 0,23 % / 2,3 % / 23 % du travail du réseau avec 10 / 100 / 1000 nœuds
  vérificateurs ; avec une limitation du dommage de 10 % — 10 fois plus cher [calcul ; la colonne du dommage
  n'est pas dérivée strictement]. Exige un apprentissage en arithmétique entière exacte, qui n'est ni construit ni mesuré.
- **Audit « un honnête sur N »** (claude1, S2) — c'est une hypothèse que l'étape 4 a déjà rejetée pour
  l'apprentissage ; sans audit payé, l'équilibre est « il n'y a pas d'auditeurs ».
- **Paiement pour une amélioration prouvée (D18)** — ce n'est pas une vérification de l'étape ; le calcul M12
  a déjà montré qu'un doublon exact de la candidature augmente l'attribution du propriétaire selon les trois
  règles d'attribution (calcul des mini-agents, synthèse D5_RESULTS).

L'addition stable des contributions (Krum, médiane, moyenne tronquée — de mémoire) limite le dommage de la
part non détectée, mais ne protège pas contre des saboteurs concertés ayant une part de poids notable et ne
satisfait pas D1. Une étape non vérifiée ne doit pas entrer dans la version publiée du modèle (D6).

## 6. Décisions à modifier ou à prendre

Les formulations ci-dessous sont des **recommandations du conseil**, non des décisions acceptées. Chaque
question doit être acceptée ou rejetée explicitement. Les exigences immuables R1–R6 ne changent pas par la
modification d'une ligne de la feuille de route (rappel de gpt1).

**Question 1 (D21, ainsi que D11 et D2). Faut-il autoriser le payeur à payer, sur son prépaiement, une
réponse que son programme, selon la règle du noyau, n'a pas vérifiée ?** Actuellement D21 dit : « Le réseau
ne paie pas une réponse sans vérification », et D11 — « seul ce qui est vérifié est payé ».
*Recommandation (critique Claude, d'après les travaux claude1 et claude2) :* oui. Deuxième phrase proposée
pour D21 : « Le payeur paie sur son prépaiement la réponse qu'il a vérifiée, ou laissée passer selon la règle
D7 au moyen de sa pièce secrète ; une réponse laissée passer porte la mention « non vérifié ». Une requête payée ne
donne ni émission de crédits ni poids ». Il faut en même temps préciser D11 (et, selon la remarque du critique
DeepSeek, D2), sinon les modifications se contredisent.
*Où ils ont divergé :* le critique DeepSeek — ne pas changer D21 pour l'instant (la stratégie est de toute
façon bloquée par D23) et utiliser la loterie B (`α = 0`, paiement `R/p` à la réponse choisie), compatible avec les D2,
D11, D21 actuels. Le critique ChatGPT — garder comme contrat principal la vérification complète de chaque
réponse par le payeur, et introduire le paiement de celles choisies dans un lot par un contrat séparé ; sans
vérification autonome, il n'y a pas de paiement réseau.

**Question 2 (D7). Comment écrire quelle vérification est admissible pour le paiement ?**
*Recommandation (critique Claude) :* « La vérification indépendante de la part de collusion est obligatoire
pour la mention « vérifié », pour l'émission de crédits et pour le poids. Le paiement d'une requête sur les
fonds du payeur est admis après vérification par le payeur ou après un passage de vérification selon la règle
du noyau : pièce secrète du payeur, lancée après la fixation de la réponse, probabilité non inférieure à
`R_i/(R_i + H_lock)`. Il est interdit de réduire cette probabilité selon l'historique, la réputation, les
anomalies, l'attestation ou le nombre de clés ; l'augmenter est permis. La vérification par des vérificateurs
désignés ne sert pas de base au paiement. D1 n'est pas affaibli jusqu'à `q < q*` ». Il faut choisir séparément
`R/(R + H_lock)` (seuil exact) ou `R/H` (avec marge, nombre fini de falsifications du saboteur avant la
prise).
*Où ils ont divergé :* les critiques DeepSeek et ChatGPT proposent de ne pas changer le texte de D7, mais
d'ajouter un domaine d'application : la garantie à la partie qui exécute elle-même la vérification ne dépend
pas de `q` ; la partie qui a délégué la vérification n'est protégée que si la part de collusion des désignés
est inférieure à `q*`, et cela lui est montré (critique DeepSeek). Le critique ChatGPT ajoute : le
classement, le quorum, l'expiration du délai et l'hypothèse `q_eff < q*` ne donnent pas droit à un statut
indépendant.

**Question 3 (D6). Faut-il préciser les mentions du résultat ?**
*Recommandation (commune aux critiques, formulation d'après ds1) :* « Une réponse fausse n'est pas remise
comme « vérifiée ». Il y a deux mentions : « vérifié » — vérification complète avant l'affichage, par un
moyen indépendant de la part de collusion (pour une requête — par le payeur en personne, ou par une preuve
acceptée par le noyau) ; « non vérifié » — par défaut, mise automatiquement, seule une telle vérification peut
la retirer. La délivrance en flux — par blocs vérifiés ou avec cette mention. Une étape d'apprentissage non
vérifiée n'entre pas dans la version publiée du modèle ». Le critique ChatGPT précise : une étape non vérifiée
et ses descendants ne peuvent être que dans une branche de recherche isolée, sans paiement pour la transition.
*Où ils ont divergé :* au fond, ils n'ont pas divergé ; claude1 proposait une troisième mention « vérifié par
échantillonnage » — elle a été rejetée par les trois critiques.

**Question 4 (D16). Que faire d'une panne matérielle honnête ?** Actuellement une panne n'est pas sanctionnée,
et la somme en attente ne brûle pas. Avec la vérification par échantillonnage et le paiement du non-vérifié,
c'est une fuite directe (section 4.6).
*Recommandation (critiques Claude et DeepSeek, d'après claude1) :* « Avec la vérification complète ou la
loterie B, une panne honnête n'est pas sanctionnée (règle précédente). Avec la vérification par
échantillonnage et le paiement du non-vérifié, toute divergence prouvée brûle le `H_lock` de la clé
indépendamment de la cause, car la cause ne peut pas être établie d'après une sortie erronée identique. La
perte attendue de l'honnête (environ `P_f·R` par tâche, où `P_f` est la probabilité d'une panne silencieuse)
est indemnisée par une majoration inconditionnelle prélevée sur la redevance du réseau. La règle n'est activée
qu'après la mesure de `P_f` ».
*Où ils ont divergé :* le critique ChatGPT — conserver la protection contre une panne honnête : la panne
laisse le résultat sans paiement, les récompenses antérieures sont conservées, le nombre de pannes par clé est
limité, et la fiabilité du calcul ne doit pas dépendre du débit des récompenses antérieures. Il note aussi que
la majoration prélevée sur la redevance d'autrui pour chaque tâche augmente le paiement de la falsification
aussi et change le seuil. Le critique Claude ajoute : brûler une fenêtre de revenu pour une instabilité non
mesurée frappe les nœuds faibles (R6), la majoration indemnise la moyenne, non le risque de ruine. Le
différend se résout par le choix de la structure de paiement (la loterie B conserve D16, le paiement du
non-vérifié — non) et par la mesure de `P_f`.

**Question 5 (D8). Comment organiser le délai et les droits de litige ?**
*Recommandation (critique Claude) :* « Le payeur soumet une preuve de divergence au plus tard dans le délai `δ` de
temps actif après la réception de la réponse ; le litige n'est tranché que par une preuve que chaque nœud
vérifie lui-même ». *Complément (critique ChatGPT) :* l'exécutant a le droit d'exiger le règlement de sa
commande fixée en cas de refus injustifié ou de silence de l'acheteur ; les deux parties plaident à partir
d'un compte nul sans caution ; un doublon ne déclenche pas une nouvelle vérification coûteuse ; jusqu'à la
décision, la somme litigieuse reste en attente. Il y a ici une bifurcation ouverte : si l'on paie à
l'expiration du délai sans objection, l'absence du payeur fait payer la falsification ; si l'on refuse en cas de
silence, un payeur malhonnête obtient gratuitement une réponse correcte.
*Où ils ont divergé :* claude2 et le critique DeepSeek proposent, après M9, d'autoriser tout nœud à contester
une tâche choisie par la balise, avec un quota de litiges fallacieux ; le critique Claude considère cela vide
pour une requête privée (un nœud étranger n'a pas de requête) et utile seulement pour l'apprentissage.

**Question 6 (D23). Faut-il maintenir le blocage jusqu'au calcul M9 ?**
*Recommandation (les trois critiques) :* le maintenir. Compléter (critique Claude) : « M9 est calculé pour la
règle D7 : les litiges sont rares à l'équilibre, mais la coalition « payeur = exécutant » peut en soumettre
autant qu'elle veut sur des requêtes auto-payées ; la somme brûlée est détruite, à la victime n'est rendu que
son paiement au plus ». Le critique ChatGPT propose d'écrire le critère de levée du blocage : bornes
supérieures d'octets, de calculs, de messages et de délais par affaire, limite des affaires ouvertes
simultanément, source de couverture de la charge, vérification du format et de l'unicité avant le recalcul
coûteux, résistance aux requêtes auto-payées, à la collusion des deux parties, au refus fallacieux de
l'acheteur, à la partition du réseau et à l'indisponibilité des données.

**Question 7 (nouvelle D26). Faut-il adopter une décision sur le verrou de la somme en attente et la limite
du remboursement ?**
*Recommandation (critique Claude, avec les corrections de la section 4) :* « `H_lock` de la tâche `i` — les
récompenses non arrivées à maturité de la clé qui arriveront à maturité après le délai extrême de litige sur
`i` ; le délai de vérification par le payeur est bien plus petit que la fenêtre de maturation. Une divergence
prouvée brûle toute la somme non arrivée à maturité de la clé, y compris les récompenses des tâches soumises
après la tâche litigieuse et dans la même vague. Au payeur victime n'est rendu que son paiement pour la
réponse litigieuse au plus ; le reste est détruit ; le premier litige ne prend pas les sommes dues aux autres
payeurs ». Sans cette règle, la stratégie des sections 5.1–5.3 ne tient pas (contre-exemples +4,4295R et
jusqu'à +74,4R aux sections 4.2–4.3).
*Où ils ont divergé :* le critique ChatGPT ne discute pas le verrou sous cette forme, car il ne soutient pas
le paiement du non-vérifié ; mais il exige lui-même de lier atomiquement les engagements ouverts à toute la
recette non arrivée à maturité.

**Question 8 (D1). Faut-il changer D1 ?**
*Recommandation (les trois critiques) :* ne pas affaiblir le texte. Les variantes « D1 lorsque la part de
collusion est inférieure à `q*` » et « la fuite ne dépasse pas `ε` du chiffre d'affaires » (claude1, ds1,
ds2, gpt1) sont rejetées : pour `q = 1`, elles livrent à la coalition toute l'émission non vérifiée,
contredisent D19 et R4 immuable, et le « chiffre d'affaires » est gonflé par des auto-transactions. Le
critique Claude propose une note : pour la réponse du modèle, D1 est assuré à l'égard du payeur qui applique
la vérification du noyau ; la vérification par échantillonnage par sa pièce secrète satisfait D1 comme
espérance et est consignée comme hypothèse d'un adversaire rationnel (selon R4, l'échantillonnage
statistique est une hypothèse) ; pour un consommateur qui ne vérifie pas, le réseau ne promet pas D1. Le
critique DeepSeek — une note disant que la garantie D1 concerne chaque résultat portant la mention
« vérifié » et chaque émission de crédits.

## 7. Ce qu'il faut calculer par les mini-agents et ce qu'il faut vérifier par l'expérience

### 7.1. Calculs exacts (fractions, hachage de contrôle, répétition sur un second appareil)

1. Énumération complète de la règle D7 avec maturation de la somme, vagues, plusieurs clés, prix différents
   dans la vague et vérifications rétroactives. Valeurs de référence : `κ = 1` → 0 ; `κ = 0,9` avec `H₀ = 0` → +1,734R
   (reproduit par le critique Claude, non reproduit par le critique DeepSeek — l'énumération doit trancher) ;
   `0,99·R/(R + H)` → +0,225R ; contre-exemple de maturation +0,99R / +9,08R / +49,7R / +74,4R.
2. Formule de vague de gpt1 : +4,4295R avec débit séparé et −2,49676R avec combustion de toute la vague.
3. Attaque « d'auto-litige » : pour quelle part de remboursement à la victime le gain devient positif.
4. Fuite des pannes gratuites (`b` par fenêtre) et majoration `P_f·R` avec dispersion des pertes de l'honnête.
5. Dommage avec les calendriers `H_lock`, `H_old`, `H_ver`, `m·R/(R + H)` avec auto-paiement et nouvelles
   clés ; valeurs de référence 0,50 / 0,125 / 0,0078 avec `n_w = 4320`.
6. Payeurs paresseux : part `λ` et distinction pour lesquelles la dissuasion disparaît.
7. Charge de la coalition de nouvelles clés sur les payeurs avec `p = 1` pour les débutants.
8. M9 (litiges fallacieux) pour la règle D7 — condition de D23.
9. Coût synthétique `γ·(1 + p·ρ)` sur la grille des `γ`, `ρ` mesurés et de la distribution de `n_w`.
10. Probabilité de collusion totale lors d'un choix sans remise (`C(C,k)/C(N,k)`) et lors de tours de tirage
    au sort.
11. Tailles des instantanés d'état selon la configuration fixée du modèle (M1) — différend sur le coût des
    jetons échantillonnés et des instantanés.
12. Seuil corrigé de ds2 et script de contrôle de gpt2 (SHA-256 commence par `58aec3b0` et se termine par
    `cd07ba` ; a coïncidé chez les critiques Claude et DeepSeek).
13. Chaînes exactes SPRT et CUSUM sur des grilles finies, y compris le changement de comportement après un bon
    historique.
14. Tables de pièges `(1 − g·θ·d)^m` pour les niveaux `10⁻³`, `10⁻⁹`, `2⁻⁸⁰`.

### 7.2. Uniquement par l'expérience

L'expérience D5 autorise le travail avec le Qwen3.5-4B en arithmétique entière dans le volume de O1–O5 de son protocole. **Tout
le reste — seulement avec une autorisation séparée du propriétaire.**

1. Dans le cadre de D5 : noyaux rapides à bits égaux (O3, O4) — la seule voie pour s'approcher de 5 % ; part
   de vérification sur les appareils des payeurs et avec des lots de 1, 8, 32 ; O5 — la qualité sur 320
   tâches.
2. Hors D5 : décodage spéculatif exact — distribution de la longueur du préfixe coïncident de Q8_0 et du
   profil exact sur de longues réponses.
3. Hors D5 : fréquence des divergences silencieuses `P_f` lors d'un travail long sur des appareils
   volontaires — avant tout changement de D16.
4. Hors D5 : temps et mémoire d'une vérification en une passe sur le processeur d'un ordinateur portable et
   d'un téléphone.
5. Coïncidence des bits sur les entrées aux limites (dépassement, égalités, fin précoce de la réponse) et sur de
   nouveaux pilotes ; sur RX 580, une longue passe sur une réponse prête a été interrompue par le pilote
   [mesuré].
6. Hors D5 : O9 (énergie), O6 (bruit de l'amélioration LoRA), O7 (coût de la preuve d'un bloc), apprentissage
   en arithmétique entière — condition préalable de tout schéma de vérification de l'étape.
7. Hors D5, facultatif : à quel point des falsifications bon marché sont distinguables par des signes. Cela
   ne donne aucune garantie quel que soit le résultat, mais précise seulement le plafond de la section 2.1.

## 8. Divergences non résolues et références douteuses

### 8.1. Divergences

1. **La vérification par échantillonnage effectuée par le payeur satisfait-elle littéralement D1.** claude1, claude2,
   les critiques Claude et DeepSeek — oui pour l'argent, non pour le dommage. ds1 et ds2 — une vérification
   complète est nécessaire (les critiques estiment qu'ils n'ont pas remarqué la vérification par le payeur à
   une fréquence fondée sur la somme verrouillée). gpt1, gpt2 et le critique ChatGPT — vérification complète
   de chaque réponse, et le paiement des réponses choisies — seulement par un contrat séparé pour les lots. La décision
   de savoir si le gain attendu suffit à la première phrase de R4 appartient au propriétaire.
2. **`R/(R + H_lock)` ou `R/H`.** Le premier est exact pour l'argent, le second donne une marge et un nombre
   attendu fini de falsifications avant la prise ; la différence de coût est d'environ un facteur deux pour
   une petite somme.
3. **Payer le non-vérifié** (`α = R` ou G(α) progressif chez claude2) **ou seulement ce qui est choisi** (`α = 0`, loterie
   B). Cela dépend de la modification de D2, D11, D21 et de l'irrégularité non mesurée du revenu.
4. **Balise ou pièce secrète.** claude2 — balise commune (D20) ; claude1 et les critiques Claude et DeepSeek —
   pièce secrète du payeur, la balise n'est nécessaire que pour `α < R` et pour les litiges de nœuds tiers.
   Critique ChatGPT : la pièce secrète convient à une vérification personnelle, mais ne peut pas disposer du
   lot commun ; si l'on choisit le plus commode de deux résultats indépendants de la balise, la prise tombe
   de `p` à `p²`.
5. **D16** — section 6, question 4.
6. **Borne du dommage** — aucun schéma n'a résisté à l'auto-paiement et aux nouvelles clés.
7. **Apprentissage** — audit « un sur N » (claude1), vérification par chaque nœud complet avec retour en
   arrière de la branche (claude2), D18 ou répétition complète (ds1, ds2, gpt1, gpt2) ; aucun schéma ne
   satisfait D7 pour `q = 1`.
8. **Grandeurs de l'énumération de claude1** (+1,73R avec `κ = 0,9`) : reproduites par le critique Claude, non
   reproduites par le critique DeepSeek (+0,085R dans le modèle le plus proche) ; le signe est le même chez
   les deux.
9. **Décodage spéculatif :** 1,15–1,38 (claude1) contre environ 0,78 du temps du jeton exact (claude2) ; les
   deux ne sont pas mesurés.
10. **Pièges :** ds2 calcule le nombre nécessaire de pièges, claude1 et claude2 démontrent que dans un réseau
    public le piège coïncide avec la vérification par le payeur. Les conclusions sont compatibles.

### 8.2. Références bibliographiques signalées comme douteuses par les critiques

Toutes les références sont données de mémoire, sans vérification des textes.

- SybilGuard et SybilRank sous le nom commun « Yu et al. » (ds1) : de mémoire des critiques, SybilGuard et
  SybilLimit — Yu et al. (2006, 2008), SybilRank — Cao et al. (2012) ; l'année de SybilRank elle-même est
  signalée par le critique Claude comme incertaine.
- « Proof of Sampling (2024) » et « Verde (Gensyn, 2025) » (claude1, claude2) — les travaux eux-mêmes écrivent
  « pas sûr » ; la structure du mécanisme n'est pas confirmée.
- Peer Truth Serum comme travail de Witkowski et Parks (2012) (ds2) : le critique Claude juge cela douteux
  (de sa mémoire, ils ont une « BTS robuste », et le nom appartient à Radanovic et Faltings), le critique
  DeepSeek — correct. Divergence.
- DMI comme travail de Kong et Schönbeck (2019) (ds1, ds2) : douteux de mémoire des critiques Claude et
  ChatGPT (DMI — travail de Kong vers 2020) ; le critique DeepSeek considère l'attribution correcte.
- « Attaques par auto-prédiction sur BTS chez Radanovic et Faltings » (ds1) — douteux.
- « Gao, Wright et Leyton-Brown (2016) » sur la supériorité de la vérification par échantillonnage sur la peer
  prediction (claude2) — année non confirmée (critique DeepSeek), caractère inconditionnel de la conclusion
  douteux selon le critique ChatGPT.
- Kreps et Wilson (1982) comme fondement de « la réputation ne fonctionne qu'à long horizon » (claude1) —
  douteux (critique ChatGPT).
- DetectGPT comme justification du seuil de perplexité d'un petit modèle (ds1) — incorrect : il étudie une
  autre propriété (critique ChatGPT).
- La formule générale de passage `(1 − f)^s` comme propriété de BOINC, TrueBit, opML (ds1, ds2) — elle ne
  découle pas de leurs protocoles.
- Les références de ds1 et ds2 à « 0,3–0,7 % / 0,33–0,66 % de jetons d'examen » et « environ 2,4 heures par
  candidat » n'ont pas été trouvées dans les documents d'entrée.

## 9. Qui a fait quoi

Le conseil de modèles a travaillé sur les matériaux du projet, sans accès au réseau et sans expériences.

- **Six travaux indépendants :** deux travaux ChatGPT (gpt1, gpt2), deux travaux DeepSeek (ds1, ds2), deux
  travaux Claude (claude1, claude2). Chacun a analysé les sept directions de la consigne, en a ajouté
  d'autres, les a vérifiées par rapport aux décisions D1, D6, D7 et a proposé des stratégies avec coût et risque
  résiduel. De courts programmes arithmétiques et de petites énumérations ont été exécutés par claude1
  (énumération de stratégies contre la règle de fréquence), claude2 (grille de fractions exactes), gpt1 et gpt2
  (gpt2 a joint un script de contrôle avec hachage).
- **Trois critiques :** une pour chacun de ChatGPT, DeepSeek et Claude. Chaque critique a lu les six travaux,
  cherché des erreurs et des contre-exemples, recalculé les nombres clés. Les critiques Claude et DeepSeek ont
  répété le script de contrôle de gpt2, le hachage a coïncidé ; le critique Claude a répété l'énumération de
  claude1, le critique DeepSeek n'a pas reproduit ses grandeurs.
- **Synthèse :** ce document a été composé par Claude d'après les travaux et les critiques. Aucune évaluation
  ni aucun nombre nouveau au-delà des travaux, des critiques et des mesures D5 n'a été ajouté ; là où les
  critiques ont divergé, cela est indiqué.
