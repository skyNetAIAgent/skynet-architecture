<!-- translation of docs/HIDDEN_DETECTOR.md, source sha256: a695d12d2972002373f749a618c390c3e937e344afd1e816d8c46319fe1127cb -->

# Détecteur caché et changeant : ce qu'apporte le secret des règles

[English](../../docs/HIDDEN_DETECTOR.en.md) · [中文](../zh/HIDDEN_DETECTOR.md) · [Español](../es/HIDDEN_DETECTOR.md) · **Français** · [Deutsch](../de/HIDDEN_DETECTOR.md) · [Italiano](../it/HIDDEN_DETECTOR.md) · [Русский](../../docs/HIDDEN_DETECTOR.md) · [Português](../pt/HIDDEN_DETECTOR.md) · [العربية](../ar/HIDDEN_DETECTOR.md)

État au 25 novembre 2026. Résultat du sixième conseil de modèles.

## 1. Question et bref bilan

Le propriétaire du projet a demandé mot pour mot :

> « Avec des règles ouvertes (D4), le trompeur connaît le détecteur et falsifie précisément là où celui-ci
> est tranquille. Et si l'on cachait le détecteur ? Par exemple, le réseau générerait à un moment aléatoire
> de nouvelles règles de vérification de l'honnêteté, et les agents vérifieraient selon elles. Compte tenu
> de l'architecture distribuée et ouverte du réseau skynet, les règles de vérification ne doivent être
> connues de personne et doivent être chiffrées, la clé du chiffrement doit changer. Réfléchissez en conseil
> de modèles dans cette direction. J'ai déjà soulevé la question de l'utilisation de la blockchain — existe-t-il
> une variante de détecteur dynamique fondé sur la blockchain ? Peut-être existe-t-il d'autres technologies
> ou algorithmes que la blockchain ? »

**Statut du document.** C'est un raisonnement et un calcul, non une mesure. Le réseau n'était pas disponible
pendant le travail du conseil, aucune expérience n'a été menée ; les travaux scientifiques sont cités de
mémoire et n'ont pas été vérifiés. Les mesures proviennent uniquement des résultats de l'expérience D5 au
25 novembre ([EXPERIMENT_D5](EXPERIMENT_D5.md), section 7) et du précédent recueil
[STRATEGY_SEARCH](STRATEGY_SEARCH.md). Seules D1–D25 ([ROADMAP](ROADMAP.md)) restent des décisions acceptées
du projet ; tout ce qui est appelé ci-dessous « recommandation », le propriétaire doit l'accepter ou le
rejeter explicitement. Marques : [mesuré] — mesuré dans D5 ; [calcul] — découle d'une formule avec des
paramètres nommés ; [hypothèse] — valeur prise pour l'estimation et non mesurée.

Notations rencontrées ci-dessous : `R` — paiement d'une tâche ; `H_lock` — somme non arrivée à maturité de
l'exécutant, qui brûle en cas de falsification prouvée ; `c_f` — coût de la falsification ; `p` —
probabilité de vérification complète de la tâche ; `ρ` — temps de vérification d'une réponse prête en une
passe, divisé par le temps de génération ; `γ` — combien de fois le profil exact en nombres entiers est plus
lent qu'une génération ordinaire llama.cpp Q8_0 ; `q` — part de collusion ; `n_w` — nombre de tâches de la
clé par fenêtre de maturation.

**Bref bilan.**

1. **Un détecteur caché n'apporte pas plus qu'une vérification ouverte avec un hasard secret du même coût.**
   Si le trompeur connaît la loi selon laquelle les règles sont choisies (et selon D4 le code de l'agent est
   ouvert, donc il la connaît), alors la probabilité d'attraper l'une quelconque de ses falsifications avec
   une règle cachée est égale à la probabilité de prise avec le programme ouvert « après fixation de la
   réponse, lancer une pièce et appliquer la règle tombée ». Les onze travaux l'ont obtenu indépendamment,
   les quatre critiques l'ont confirmé. Donc le caractère caché ne permet pas d'abaisser la fréquence de
   vérification sous le seuil antérieur `R/(R + H_lock)`.
2. **Une règle qui vit plus longtemps qu'une tâche est pire qu'une pièce fraîche.** Le trompeur apprend de
   ses issues (« attrapé / non attrapé »), essaie le détecteur avec de nouvelles clés gratuites, découvre la
   règle par n'importe quel complice à qui on l'a donné à appliquer. Même sans aucune fuite, une règle
   commune à une époque est plus dangereuse : dans l'exemple de ChatGPT, une vague de dix falsifications
   donne `+8,1R` contre `−2,38R` avec des pièces indépendantes [calcul]. « Changer les règles à un moment
   aléatoire » est donc pire que changer le choix à chaque tâche.
3. **Exactement une forme de dissimulation est utile :** le secret du choix aléatoire *avant* que l'exécutant
   ait irrévocablement fixé la réponse, et le secret du *rôle* — si ce payeur donné vérifie et qui est désigné
   vérificateur. Les règles, la famille de vérifications et la loi de choix restent ouvertes. Cette forme
   existe déjà dans la stratégie du conseil précédent (« pièce secrète du payeur »).
4. **Ce qu'il faut retenir de la blockchain et de la cryptographie.** La blockchain est un journal de
   fixations, d'ordre, de révélations et de brûlage de sommes ; elle ne contient pas de secrets et ne peut
   pas en contenir. Une balise de hasard externe à seuil et le délai VDF depuis le bloc final sont des
   sources de hasard pour les échantillons communs selon D20 (audit d'apprentissage, examen, désignation des
   vérificateurs), mélangées par hachage. VRF et engagement sur un sel avant fixation — là où l'issue de la
   pièce influence l'argent d'autrui. Un « détecteur dynamique sur blockchain » sous sa forme correcte,
   c'est **un générateur ouvert de règles dans le noyau plus un hasard frais après fixation**, et non des
   règles chiffrées.
5. **Ce qu'il faut rejeter comme fondement de garantie.** Stockage à seuil de règles secrètes par les
   participants (révélé ou bloqué par collusion, aucune protection pour `q = 1` — violation de D7),
   environnements d'exécution de confiance TEE (confiance au fabricant, absents sur les cartes de l'expérience
   D5), chiffrement homomorphe FHE (selon l'estimation des critiques, de 19 heures à 15 jours de calcul pour
   une réponse), calcul multipartite MPC (des centaines de mégaoctets et plus de trafic par jeton et de
   nouveau la dépendance à `q`), obfuscation indistinguable iO (impraticable et laissant de toute façon au
   trompeur un « essai »), chiffrement fonctionnel et PIR (résolvent d'autres problèmes). Pièges, seuils
   secrets et statistiques ne sont admissibles que comme signal pour une vérification *supplémentaire*.
6. **Une erreur a été trouvée dans les tableaux précédents.** Dans STRATEGY_SEARCH 5.3 et dans la plupart des
   travaux de ce conseil, la cellule « payeur paresseux, l'exécutant le distingue » × « débutant » contient
   0. Correct — **jusqu'à `+R`** : la règle « un débutant est toujours vérifié » est exécutée par le programme
   du payeur, et un payeur paresseux ne l'exécute pas. Pire, de nouvelles clés permettent de déterminer
   gratuitement quel payeur est paresseux. Seule la non-liabilité des payeurs entre les requêtes protège de
   cela, et elle reste encore à construire.
7. **Le conseil ne propose pas de nouvelles décisions sur la garantie.** Sont proposés une précision de D4
   (« le noyau accepte un hasard futur, mais pas un secret de longue durée ») et une précision de D20 (« les
   sources sont mélangées par hachage, et non par choix ; la balise — pour les décisions communes, non pour
   l'argent du payeur »). Le coût de la vérification ne change pas à cause de la dissimulation : le principal
   poste reste le ralentissement du profil exact `γ` (+50…+82 % par rapport à Q8_0 avec un lot de 1
   [mesuré γ, calcul]), et non la vérification elle-même.

---

## 2. Pourquoi le secret des règles n'aide pas : affirmations et contre-exemples

### 2.1. Une règle cachée équivaut à une règle ouverte avec une pièce secrète

**Modèle.** Le défenseur choisit une règle de vérification `r` dans une distribution `D`. La règle `r`
attrape la falsification `x` avec la probabilité `π_r(x)`. Le trompeur connaît la distribution `D` (selon D4,
le générateur de règles fait partie du noyau ouvert), mais ne connaît pas le `r` tombé, et choisit la
falsification avant que `r` ne tombe.

**Affirmation 1 (équivalence).** La probabilité d'attraper la falsification `x` est égale à
`π̄(x) = E_{r~D}[π_r(x)]`, le coût moyen de la vérification est égal au coût moyen des règles. Le programme
ouvert « après fixation irrévocable de la réponse, prendre un hasard frais, choisir `r` selon la loi `D`
et l'appliquer » donne pour **chaque** falsification la même probabilité de prise et le même coût. Donc la
dissimulation de l'implémentation n'ajoute rien à la protection.

Preuve — moyenne sur `r` : les issues des deux expériences coïncident pour chaque valeur du hasard. gpt1,
gpt2, ds1, ds2, claude1, claude2, mm1–mm5 l'ont menée indépendamment ; les critiques ChatGPT, DeepSeek,
Claude et MiniMax l'ont confirmée. C'est le même résultat que la borne du conseil précédent
`E_F[π] − E_P[π] ≤ TV(F, P)` ([STRATEGY_SEARCH](STRATEGY_SEARCH.md), section 2.1) : la quantité `π̄` est une
fonction ordinaire des observations à valeurs de 0 à 1, et le secret ne la change pas.

**Affirmation 2 (les informations sur le secret ne nuisent qu'au défenseur).** Si le trompeur reçoit avant la
falsification n'importe quel signal `Z` sur la règle tombée — par un litige passé, un essai, via une part de
clé, par une fuite de l'enclave —, son meilleur résultat ne se dégrade pas : `E_Z[min_x E[π_r(x) | Z]] ≤ min_x π̄(x)`.
Il peut toujours ignorer le signal (claude1, claude2 ; confirmé par les critiques).

Le critique ChatGPT a précisé la limite de cette affirmation : l'inégalité est non stricte. Si toutes les
règles ont la même falsification « la pire pour le défenseur », la révélation de la règle peut ne rien
changer. La phrase de claude1 « toute fuite aggrave strictement » est donc fausse ; ce qui est vrai, c'est
« elle n'améliore jamais ».

**En quoi cela diffère de la randomisation.** Plusieurs travaux (ds1, ds2, mm2) ont consigné la conséquence
comme « un détecteur caché équivaut à vérifier toute la réponse avec probabilité `p` ». C'est inexact.
L'équivalent d'un détecteur caché est *un mélange des mêmes règles*. Un mélange de vérifications partielles
est parfois plus fort qu'une vérification complète au même coût, mais le gain vient de la randomisation, non
du secret, et il se conserve avec un algorithme ouvert :

- **Contre-exemple gpt1.** Le résultat a trois parties vérifiables indépendamment d'un même coût, et par la
  structure de la tâche toute falsification admissible en abîme au moins deux. La vérification d'une partie
  aléatoire pour un tiers du coût complet attrape au moins 2/3 des falsifications ; un recalcul complet avec
  probabilité 1/3 — seulement 1/3.
- **Variante gpt2.** Trois tests pour la moitié du coût d'un recalcul complet, chacun attrape deux classes
  d'erreurs sur trois : le mélange attrape 2/3, le recalcul complet de la moitié des tâches — 1/2. Si l'on
  ajoute une quatrième classe, qu'aucun test n'attrape, la garantie du mélange tombe à 0.

Pour Qwen, une telle couverture des classes d'erreurs n'est pas démontrée : une seule position erronée de la
réponse est déjà une falsification, et pour elle toute vérification partielle n'attrape pas plus que sa part.
C'est pourquoi le gain pratique du mélange est actuellement nul (critiques Claude et ChatGPT). L'affirmation
de mm2 « un mélange est toujours plus cher qu'un type décisif » est fausse en général ; dans sa formule il y
a en outre un facteur superflu (les nombres 0,2111 / 0,22 / 0,2333 sont calculés selon la formule correcte,
une formule incorrecte est écrite — critiques Claude et DeepSeek).

**Où le secret ne se réduit pas à une pièce.** C'est une marque privée du défenseur, liée à la réponse
correcte : la référence du piège, que seul le payeur connaît (gpt1, gpt2). On ne peut pas la remplacer par un
bit aléatoire. Mais, comme le montre la section 3, elle coûte au moins une génération et ne rend donc pas la
vérification moins chère.

**Contre une règle « fixe », le caché est effectivement meilleur.** claude1 donne un exemple : si la règle
ouverte regarde toujours les positions 1–8, une falsification à la position 9 n'est jamais attrapée. Mais le
même gain est donné par la règle ouverte « choisir 8 positions uniformément après fixation » (mm3,
théorème 2 : une position fraîche attrape `e/N` falsifications, où `e` est le nombre de positions corrompues
sur `N`, indépendamment du fait que le trompeur connaisse la règle). Le critique MiniMax a appelé cela
l'erreur principale du tour : beaucoup de travaux ont comparé le détecteur caché à une règle ouverte fixe et
ont attribué au secret un gain qui appartient au hasard.

### 2.2. Apprentissage du trompeur par les issues et essais avec de nouvelles clés

Un secret utilisé plus d'une fois s'apprend. Pour cela, l'adversaire n'a pas besoin de connaître la règle en
entier — il suffit de trouver un endroit sûr.

- **Deux positions sur dix (claude1).** La règle cachée vérifie 2 positions sur 10, la prise d'une
  falsification à une position — 1/5. Après qu'un litige a révélé une position vérifiable, la prise tombe à
  1/9, après la révélation de la seconde — à 0. Si la règle est révélée dès le premier litige, le nombre
  attendu d'attrapées sur 100 falsifications est `1 − 0,8¹⁰⁰ = 0,9999999998`, c'est-à-dire pratiquement une,
  alors qu'une pièce fraîche en aurait attrapé en moyenne 20 [calcul, confirmé par les critiques]. Le
  critique ChatGPT a noté que cela est vrai pour un ordre d'essais concret et une révélation complète à la
  première prise ; en général, un litige révèle au moins la position vérifiée, mais pas nécessairement tout
  l'ensemble.
- **Huit positions sur mille (ds2).** Avec un sous-ensemble constant caché de 8 positions sur 1000, la
  première falsification à une position passe avec probabilité 0,992, comme avec un échantillon frais public
  de la même part. La différence est qu'avec un sous-ensemble constant caché, la position passée reste sûre
  pour toujours. Le nombre de ds2 « ≈ 2718 tentatives pour restaurer tout l'ensemble » est calculé selon un
  modèle incorrect (avec remise) ; sans remise il faut environ 890 tentatives, et surtout, une seule position
  sûre suffit à l'adversaire (critiques Claude, DeepSeek et ChatGPT).
- **Règle d'époque et clé mûre (claude2).** Règle déterministe par époque de 100 tâches, `p = 1%`,
  `H_lock = 99R` : le trompeur qui a trouvé une zone sûre par essai obtient environ
  `0,99·100R − 0,01·99R = 98,01R` par époque contre `≤ 0` avec une pièce fraîche [calcul, confirmé].
- **Bit commun d'époque (gpt2).** `R = 1`, verrouillé `9R`, dix falsifications d'une même vague, la première
  falsification prouvée annule la vague et `9R`, fréquence de vérification d'une demande séparée 1/10. Si un
  bit caché d'époque décide « tout vérifier » ou « tout sauter », le gain de la vague est
  `0,9·10R − 0,1·9R = +8,1R` — une violation de D1 **avant toute fuite**. Avec dix pièces indépendantes aux
  mêmes coûts `(0,9¹⁰·10 − (1 − 0,9¹⁰)·9)R = −2,3751096381R` [calcul, répété par tous les critiques]. De même
  chez le critique ChatGPT : avec `R = 1`, `H = 4`, `p = 0,2` et dix falsifications, une pièce commune pour
  toute la vague donne `+7,2R` même avec l'annulation de toute la vague.

**Clés Sybil.** Les nouvelles clés sont gratuites. Une clé à compte vide ne perd rien en cas de prise, donc
les essais du détecteur avec elle ne coûtent presque rien. La protection ne tient que là où le débutant est
réellement toujours vérifié (`p = 1`). Le critique ChatGPT a précisé que la gratuité des clés n'implique pas
que l'adaptation soit instantanée : chaque issue informative exige une tâche payante et du temps, et avec un
retour bruité — plusieurs tentatives. La conclusion n'en change pas : un secret qui vit longtemps finit tôt
ou tard par s'apprendre, et une pièce fraîche n'apprend rien, parce que le lancer suivant est indépendant des
précédents.

**Conclusion.** Le choix doit être refait à chaque tâche, et non selon un calendrier. C'est précisément
pourquoi « le réseau génère de nouvelles règles à un moment aléatoire » est pire que « une pièce fraîche à
chaque tâche », qui se régénère d'elle-même et gratuitement (ds1).

### 2.3. La règle fuit par ceux qui l'appliquent

« Une règle que personne ne connaît mais que tous exécutent » est impossible dans un réseau ouvert. Le nœud
qui applique la règle la connaît au moment de l'application : le code et les clés sont dans la mémoire de la
machine, et le propriétaire de la machine, selon le modèle d'adversaire, peut les lire
([THREAT_MODEL](THREAT_MODEL.md), section 1.3). claude1 a formulé la liste complète des porteurs du secret :

1. la règle n'existe pas encore — elle sera dérivée d'un hasard futur (balise, VDF) ;
2. la règle est exécutée dans du matériel que le propriétaire ne peut pas ouvrir (TEE) — alors la confiance
   se transfère au fabricant, et R4 appelle cela une hypothèse ;
3. la règle est chiffrée de façon à pouvoir être exécutée sans être connue (iO, FHE, MPC) — voir section 3 ;
4. la règle est connue d'un comité de participants — alors elle est révélée ou bloquée par collusion.

Le critique ChatGPT a complété la liste : MPC sur des parts et le calcul d'un schéma ouvert sur un paramètre
chiffré permettent à l'opérateur de ne pas voir du tout le résultat. Cela ne change pas la conclusion, parce
que de tels schémas reposent de nouveau sur une part de participants honnêtes ou sur le détenteur de la clé.

**Une clé à seuil protège le stockage, mais pas l'application** (claude2, l'argument le plus fort du conseil
contre une règle secrète chez un comité). Même si la clé est partagée de manière fiable, la règle d'époque
déchiffrée est exécutée par un nœud concret. Pour `m` applications indépendantes, la probabilité qu'au moins
un nœud appliquant fasse partie de la coalition est `1 − (1 − q)^m` : pour 10 applications, c'est
0,65 / 0,97 / 0,999 pour `q` = 0,1 / 0,3 / 0,5. La probabilité que la règle d'époque *ne soit pas* connue de
la coalition après 100 applications avec `q = 0,1` est `0,9¹⁰⁰ ≈ 2,7·10⁻⁵` [calcul, confirmé par les
critiques].

**Cacher au vérificateur n'a pas de sens** (claude2, corollaire 4.2). Un vérificateur de la coalition peut
ne pas vérifier du tout et dire « propre » ; l'honnête n'a rien à cacher. Le seul à qui la décision doit être
cachée, c'est l'exécutant avant la fixation de la réponse. claude2 a ajouté le théorème 4 : si le
vérificateur ne doit pas savoir quelles positions il vérifie, il doit « toucher » toutes les positions, et
l'économie de l'échantillon disparaît. Le critique ChatGPT a noté que cette conclusion est vraie dans un
modèle spécial (un seul serveur, pas de prétraitement), et que dans d'autres modèles d'accès à la mémoire
elle peut changer ; le critique Claude — que le théorème réfute une variante que personne ne défendait.

**Un secret caché ne donne pas de verdict vérifiable.** mm2 a remarqué que l'affirmation « il existe une
règle secrète qui a accepté le résultat » est toujours vraie pour la règle « tout accepter ». Les critiques
Claude et ChatGPT ont précisé : une preuve à divulgation nulle de connaissance peut attester une affirmation
substantielle « la règle est dérivée d'un engagement inscrit avant la fixation, et elle a accepté le
résultat ». Mais une telle preuve exige une relation ouverte dans le noyau, c'est-à-dire nous ramène au
générateur ouvert, et son coût pour Qwen n'est pas calculé.

### 2.4. Clé à seuil avec part de collusion q

Soit une clé partagée entre `n` détenteurs, et `t` parts nécessaires pour le déchiffrement. Alors la coalition
découvre le secret par avance si elle a `t` places ou plus, et peut arrêter le travail si elle a `n − t + 1`
places ou plus. Si les places sont choisies indépendamment et chacune appartient à la coalition avec
probabilité `q`, ce sont des queues binomiales. Tableau du critique Claude, vérifié par les critiques ChatGPT
et DeepSeek ; dans chaque cellule « révélation / arrêt » [calcul] :

| `n`, `t` | `q = 0,1` | `q = 0,3` | `q = 0,5` | `q = 1` |
|---|---|---|---|---|
| 5, 3 | 0,856% / 0,856% | 16,3% / 16,3% | 50% / 50% | 1 / 1 |
| 7, 5 | 0,0177% / 2,57% | 2,88% / 35,3% | 22,7% / 77,3% | 1 / 1 |
| 16, 11 | 2,7·10⁻⁸ / 0,33% | 0,157% / 34,0% | 10,5% / 89,5% | 1 / 1 |
| 30, 16 | 3,66·10⁻⁹ / 3,56·10⁻⁸ | 0,637% / 1,69% | 42,8% / 57,2% | 1 / 1 |
| 64, 43 | 4,75·10⁻²⁸ / 1,20·10⁻⁷ | 9,43·10⁻¹⁰ / 26,2% | 0,41% / 99,6% | 1 / 1 |
| 100, 51 | 6,3·10⁻²⁵ / 5,8·10⁻²⁴ | 9,0·10⁻⁶ / 2,2·10⁻⁵ | 46,0% / 54,0% | 1 / 1 |
| 100, 67 | 9,6·10⁻⁴³ / 7,0·10⁻¹¹ | 2,7·10⁻¹⁴ / 22,1% | 0,044% / ≈1 | 1 / 1 |

Ce qui en découle :

1. **Aucune ligne ne donne de protection pour `q = 1`.** D7 exige une vérification indépendante de la part de
   collusion, donc le secret chez un comité ne satisfait pas D7 pour aucun seuil.
2. **Un seuil élevé garde bien le secret, mais se bloque facilement.** Ligne 16/11 : avec `q = 0,3`,
   révélation 0,157 %, mais avec probabilité 34 % la coalition arrête l'émission en ne fournissant simplement
   pas ses parts.
3. **Les époques s'additionnent.** Avec une probabilité de révélation de 0,856 % par époque (3 sur 5,
   `q = 0,1`), sur 30 époques indépendantes au moins une révélation se produira avec probabilité 22,7 %
   (gpt1) [calcul].
4. **Le tableau est optimiste.** Le choix indépendant des places est une hypothèse. Elle se casse si les
   détenteurs sont sélectionnés par poids, et que le poids peut être acquis par des requêtes vérifiées
   auto-payées ; si un modèle rare a une part de collusion supérieure à la moyenne ; en cas de corruption
   après la désignation ; en cas de propriétaires communs des places. Dans [THREAT_MODEL](THREAT_MODEL.md)
   (section 1.7), il y a déjà un exemple : 42,1 % du poids total donnent `q_eff = 88,9 %` parmi ceux admis à
   la tâche (le critique MiniMax y a attiré l'attention).
5. **Erreurs dans les travaux.** claude1 a consigné la condition « `q < min(t/n, 1 − t/n) ≤ 1/2` » comme
   théorème ; ce n'est pas un théorème : avec `t = n`, le secret tient tant qu'il y a au moins un honnête dans
   le comité, et le blocage peut avoir une issue de secours sûre (critique Claude). mm4 a confondu les seuils
   de révélation et de blocage ; mm2 croyait à tort que le déchiffrement à seuil exige tous les détenteurs ;
   ds1 a consigné de façon contradictoire « on restaure avec `t + 1` parts ». L'affirmation de mm3 « avec
   `q ≥ t`, la coalition falsifie la règle » n'est vraie que là où le verdict est une signature à seuil sans
   contenu vérifiable ; si l'on déchiffre un chiffré fixé d'avance, la coalition découvre la règle, mais ne
   peut pas la remplacer.

**Comment lire les exigences R2/R3.** ds1, mm1, mm3 et mm4 ont écrit que l'exigence de restauration après un
arrêt complet « interdit par principe » les secrets communs. Les critiques Claude et ChatGPT considèrent cela
comme excessif : les parts des détenteurs peuvent survivre à l'arrêt sur leurs disques ; R2/R3 interdisent de
dépendre de l'adresse d'un coordinateur vivant, et non du retour d'une partie des participants. La limite
exacte (claude2) : un secret sans lequel on ne peut pas vérifier le fondement d'une décision **passée** est
incompatible avec la vérifiabilité après redémarrage. Donc toute règle secrète doit être révélée au plus tard
au paiement, et son secret ne vit pas plus longtemps que le secret de la pièce. La conclusion sur
l'inaptitude des règles secrètes est la même, le fondement de ds1, mm1, mm3 était surestimé.

### 2.5. Principe de Kerckhoffs, jeux de sécurité, banques et CAPTCHA

**Kerckhoffs.** Le principe de Kerckhoffs (de mémoire) admet un algorithme ouvert avec une clé secrète. Dans
ce jeu, la « clé » secrète doit être la réalisation imprévisible avant fixation de l'appel de vérification, et
non l'algorithme. Le changement d'une clé de longue durée est utile après une compromission, mais n'efface
pas ce que le trompeur a déjà appris sur la fonction que cette clé déchiffrait (critique ChatGPT).

**Jeux de sécurité.** Le défenseur à budget limité randomise — c'est classique dans les jeux de Stackelberg et
les jeux d'inspection (de mémoire). Mais là, la distribution du défenseur est généralement considérée comme
connue de l'attaquant, et tout le bénéfice vient du hasard, non du secret de la distribution. Le critique
DeepSeek a corrigé mm3 : la méconnaissance par le trompeur de la distribution ne peut pas élever son gain
au-dessus de la meilleure réponse à la distribution véritable, et selon D4 il est de toute façon tenu de
connaître cette distribution. Pour un mélange de tests différents, gpt1 a consigné un problème de
programmation linéaire : maximiser la plus petite probabilité de prise sur les falsifications
`min_f Σ w_j D(j,f)` sous le budget `Σ w_j c_j ≤ B`.

**« Cible mouvante ».** L'idée de moving target defense (de mémoire) est précieuse lorsque l'observateur a
besoin de temps pour s'adapter à une nouvelle configuration. Dans SkyNet, la meilleure « cible mouvante » est
une nouvelle configuration à chaque tâche, c'est-à-dire une pièce fraîche (mm4, mm5).

**Pourquoi la dissimulation fonctionne dans une banque et dans un CAPTCHA, mais pas dans SkyNet.** Les travaux
et les critiques se sont accordés sur les différences suivantes (claude2, ds2, mm3, mm5, critique ChatGPT) :

| | Antifraude bancaire, CAPTCHA | SkyNet |
|---|---|---|
| Qui détient le modèle de vérification | Une organisation sur son serveur | Pas de centre ; le code de l'agent est ouvert (D4) |
| Retour à l'attaquant | Souvent non attribuable, avec délai | L'issue est visible immédiatement et liée à la tâche |
| Coût de la tentative | Ouverture d'un compte, documents, limitation des répétitions | La clé est gratuite (Sybil) |
| Sanctions | Non monétaires : blocage, tribunal, informations externes | Seulement le brûlage de la somme non arrivée à maturité (R5) |
| But de la protection | Réduire les pertes en moyenne | Le gain attendu de toute coalition n'est pas supérieur à zéro (D1) |
| Vérifiabilité de la décision | Non exigée par des tiers | Chaque nœud vérifie lui-même le fondement |

La banque dispose de marques privées des issues, du coût d'ouverture d'un compte et d'une limitation des
répétitions ; le CAPTCHA — d'un vérificateur externe. Ce sont des informations supplémentaires et des coûts
pour l'attaquant. Ils n'apparaissent pas dans SkyNet par le changement d'un fichier chiffré de règles. ds2 et
mm5 ont bien nommé l'essentiel : là où la dissimulation fonctionne, le secret est en fait à usage unique,
c'est-à-dire la même pièce.

**La prémisse principale de la question pour SkyNet est en partie fausse** (mm3). La vérification principale
du projet est une comparaison bit à bit avec un recalcul exact. Elle n'a pas d'« endroit où le détecteur est
tranquille » : la réponse honnête coïncide partout, la falsification diverge là où elle est falsifiée. Les
« zones calmes » n'existent que chez les détecteurs statistiques et les vérifications partielles. Les
détecteurs statistiques contre la falsification principale (génération Q8_0 ordinaire au lieu du profil
exact) sont presque inutiles, et pour les vérifications partielles, un choix frais après fixation aide.

---

## 3. Analyse des technologies

Les coûts ci-dessous sont [calcul] selon des paramètres explicitement nommés et [hypothèse] sur la vitesse de
la cryptographie de mémoire ; aucune de ces technologies n'a été mesurée dans le projet. Mesures de base :
`ρ = 0,10–0,40` avec un lot de 1 et `0,26–0,64` avec un lot de 8 ; `γ = 1,5–1,8` avec un lot de 1 et
`2,5–2,8` avec un lot de 8 [mesuré, O3 et O4]. Modèle D5 : 32 blocs, taille cachée 2560, MLP 9216, 24 blocs
Gated DeltaNet avec état `32×128×128`, vocabulaire 248 320, environ 4,2·10⁹ multiplications-additions par
jeton.

| Technologie | Ce qu'elle apporte | Ce qu'elle n'apporte pas | Coût [calcul / hypothèse] | Verdict |
|---|---|---|---|---|
| **Journal blockchain** | Ordre, fixation définitive de la réponse (D24, 2–4 Ko de chiffré), engagements, révélations, calcul unique, brûlage | Pas de confidentialité : tout le monde voit tout dans le bloc. Pas de hasard non biaisable : le producteur du bloc peut retenir un bloc gênant (N13) | Litige pilote : 93 transactions, 5,8–6,3 millions de gas, à 1 gwei et 3000 $/ETH — 17,4–18,9 $, à 20 gwei — 348–378 $ (critique ChatGPT d'après THREAT_MODEL, N3) | **À prendre comme journal** |
| **Contrat intelligent comme détecteur** | Calcul automatique sur un fondement déjà vérifié | Ni stockage de secret, ni calcul du modèle | Recalcul d'un jeton dans le contrat : `4,2·10⁹ × 3 gas ≈ 1,26·10¹⁰ gas` ≈ 37 800 $ par jeton à 1 gwei et 3000 $/ETH (ds1, confirmé). Critique Claude : cela fait environ 420 blocs de 30 millions de gas (limite de mémoire). Critique ChatGPT : une simple opération MUL coûte 5 gas de mémoire, donc c'est un scénario, non une borne inférieure stricte | **À rejeter comme détecteur** |
| **Balise externe à seuil** (classe drand, de mémoire) | Un hasard public que personne ne connaît d'avance, si le seuil de son comité est honnête | Le secret : le tour est publié pour tous. Une coalition à l'intérieur du comité de la balise découvre le tour plus tôt ou peut ne pas le publier | Des centaines d'octets par tour par lot et l'attente d'un tour (de mémoire, 30 s pour la chaîne principale et environ 3 s pour une rapide) | **À prendre comme l'une des deux sources de D20** pour les échantillons communs |
| **VDF depuis le bloc final** | Un délai pendant lequel le producteur du bloc n'a pas le temps de choisir un bloc commode | Une entropie indépendante : un VDF du même bloc n'est pas une seconde source indépendante (critique ChatGPT) | Travail séquentiel du calculateur ; vérification rapide | **À prendre comme complément à la balise**, consigner l'hypothèse sur la supériorité du matériel rapide |
| **Chiffrement à verrou temporel via la balise** | Révélation différée de références communes, tâches d'examen | Le secret au-delà d'un tour ; hérite du seuil de la balise | Comme pour la balise | **Uniquement pour la révélation différée de données communes** ; ne pas révéler ainsi des données privées |
| **Puzzle à verrouillage temporel** (Rivest–Shamir–Wagner, de mémoire) | Un délai de révélation | Le créateur connaît la réponse immédiatement ; une pièce est plus simple | Travail séquentiel | **À rejeter** |
| **VRF** | Une valeur univoque et vérifiable pour une clé et une entrée enregistrées d'avance | Le secret vis-à-vis du détenteur de la clé : il calcule la valeur quand il veut. La vérification de la preuve VRF révèle la valeur (erreur de mm4). Elle ne prouve pas le fait du recalcul VRF | Un appel et des centaines d'octets par réponse | **À prendre** : pour la désignation des vérificateurs (contre la corruption après désignation) et comme pièce du payeur là où l'issue influence le paiement d'autrui ; la clé est enregistrée pour la commande avant fixation |
| **Commit–reveal** | La liaison d'un sel à une seule commande avant la fixation de la réponse | La protection contre le « dernier à révéler », qui peut se taire | gpt2 : 448 octets par schéma | **À prendre de façon étroite** : engagement avant fixation, sans droit de choisir l'issue |
| **Cryptographie à seuil** (Shamir, DKG, déchiffrement à seuil) | Le stockage d'une clé sans un seul détenteur | L'indépendance vis-à-vis de `q` (section 2.4) ; la protection lors de l'application de la règle (section 2.3) | DKG avec `n = 7`, `t = 5` : `7·6·32 + 7·5·48 = 3024` octets de charge utile (gpt2), signature à seuil BLS — 288 octets ; sans réplication ni plaintes | **À rejeter pour les règles secrètes** ; une balise interne à seuil des participants — seulement comme l'une des sources, pas comme l'unique |
| **TEE** (SGX, SEV, TDX, GPU protégés) | L'exécution d'un code caché au propriétaire de la machine, avec confiance au fabricant | L'indépendance vis-à-vis du fabricant et de sa chaîne d'attestation ; il n'y a pas de GPU protégés dans le parc D5 (RTX 2060, RTX 4070 Laptop, RX 580) | Scénario du critique ChatGPT : une vérification protégée 1,2 fois plus longue que l'ouverte, `p = 0,1` — environ 3,20 % du temps de génération avec chargement des poids ; un modèle sur CPU — environ 50–100 ms par jeton contre 15–50 ms sur GPU (critique Claude) [hypothèse]. Critique MiniMax : le propriétaire peut utiliser l'enclave comme oracle, le secret tient à la limitation du nombre de requêtes | **Uniquement comme mode de confidentialité au choix de l'utilisateur**, pas comme fondement de garantie |
| **FHE** | Le calcul sur des données chiffrées et, via un schéma universel, sur un programme chiffré | La vérification de la correction du calcul ; le résultat est ouvert par le détenteur de la clé (de nouveau `q`). Le schéma approximatif CKKS ne reproduit pas les bits du profil v2 | 1,4·10⁷–2,6·10⁷ bootstraps par jeton, à 10⁴–10⁵ bootstraps par seconde [hypothèse] — 140–2600 s par jeton, de 19 heures à 15 jours pour une réponse de 500 jetons ; multiplicateur par rapport à la vérification ouverte `Φ ≈ 3·10³…2·10⁵` (claude2, critiques Claude, ChatGPT, MiniMax). Supplément `p·ρ·Φ` avec `n_w = 300` : de 2,1 à 139 générations par réponse | **À rejeter pour la vérification** ; à étudier uniquement pour la confidentialité |
| **MPC** | Le calcul sans rassembler le secret en un seul endroit | L'indépendance vis-à-vis de `q` : la protection tient à une majorité honnête ou à « au moins un honnête » avec le droit de faire échouer le travail ; avec `q = 1`, il n'y a pas de protection | Pour cacher le *choix* de la vérification, il faut tout traiter — en `1/p` = 31 / 303 / 4329 fois plus cher qu'une pièce avec `n_w` = 30 / 300 / 4320 (critique Claude). Cacher la *requête* : critique Claude — d'une borne inférieure de 151 Mo par jeton à 0,15–1 Go, 10–67 minutes par réponse à 1 Gbit/s ; critique ChatGPT — 448 Mo par position, 224 Go pour 500 positions ; critique MiniMax — jusqu'à 180 To par réponse (les estimations divergent de plusieurs ordres de grandeur, voir section 7) | **À rejeter pour la vérification** |
| **iO** (obfuscation indistinguable) | En théorie — l'exécution d'un programme sans révéler sa structure | Il n'existe pas d'implémentation pratique pour le modèle ; même une iO idéale laisse au trompeur un « essai » de sa falsification à travers le détecteur | Non évalué | **À rejeter** |
| **Obfuscation de fonctions ponctuelles** | La vérification « est-ce identique à la référence » sans révéler la référence | La protection quand l'espace des réponses est petit : énumération ; c'est le même piège | Hachage | Uniquement comme partie du piège |
| **Chiffrement fonctionnel** | L'obtention de la valeur d'une fonction par le détenteur d'une clé fonctionnelle | La dissimulation de la fonction au détenteur de la clé (un schéma séparé est nécessaire) ; un émetteur de clés est nécessaire | Non évalué | **À rejeter** pour cette tâche |
| **PIR, ORAM** | La dissimulation de l'indice de lecture au serveur | La dissimulation de la règle ; une preuve de provenance des données | Critique ChatGPT : en PIR à deux serveurs sur 10 000 enregistrements de 32 octets — une consultation d'environ 320 Ko par serveur et la non-collusion des serveurs | **À rejeter** pour cette tâche |
| **Pièges** (requête à réponse connue d'avance) | Des informations nouvelles : une référence corrélée à la vérité | Un abaissement du coût. Un piège de même force qu'une pièce coûte le travail de l'exécutant (≈ une génération, payée et inutile à quiconque) et la référence (une génération, si elle est fraîche). La répétition d'une ancienne requête, la coalition la reconnaît | Le rapport du prix du piège au prix de la pièce `≥ 1/((1 − σ)ρ)`, où `σ` est la probabilité de reconnaître le piège : avec `ρ = 0,21` — 5,3 / 6,8 / 9,5 / ∞ fois pour `σ = q` = 0,1 / 0,3 / 0,5 / 1 ; avec `ρ = 0,40` — 2,8 / 3,6 / 5,0 / ∞ (claude2). gpt2 : des pièges à usage unique sur 1 % des travaux avec deux générations ajoutent 2,02 % | **Uniquement « signal vers le haut »**, sans réduire la fréquence et sans mention « vérifié » |
| **Tests et seuils statistiques secrets** | Le diagnostic de pannes massives et d'erreurs d'implémentation | Un abaissement de la fréquence : borne `TV` ; le seuil s'apprend par essais | Peu | **Uniquement « signal vers le haut »** |
| **Vérificateur caché, payeurs non liables** | Contre la corruption après désignation (désignation VRF) et contre la distinction des payeurs paresseux (clés de payeur à usage unique, claude1) | L'indépendance vis-à-vis de `q` lors d'une vérification par comité. Pour un paiement non liable, il faut un émetteur ou un autre mécanisme sans privilèges particuliers — non construit | Kilooctets et secondes (claude1), non évalué complètement | **Prendre la désignation VRF ; étudier les payeurs non liables** |
| **Preuve ZK de calcul** | La seule voie vers un verdict vérifiable publiquement sur un témoin fermé | Rien sur le secret des règles ; le coût pour Qwen n'est pas calculé. Expérience du pilote : l'exécution d'une zkVM est 17 700 fois plus lente, même sans construire la preuve | Non évalué | **À étudier** séparément |
| **« Moving target defense »** | La valeur du changement de configuration tant que l'observateur ne s'est pas adapté | Dans SkyNet, le meilleur changement est à chaque tâche, c'est-à-dire une pièce fraîche | Zéro au-delà de la pièce | Se ramener à la pièce fraîche |
| **Antifraude bancaire, CAPTCHA** | Fonctionnent grâce à un serveur fermé, au coût de la tentative, à des sanctions non monétaires et à des appels à usage unique | Rien de tout cela n'apparaît dans SkyNet par le changement d'un fichier de règles (section 2.5) | — | Ne pas transposer |

**Trouvaille séparée de claude1 (pas sur le secret) : la vérification de Freivalds.** Vérifier la
multiplication d'une matrice par un vecteur par une projection aléatoire peut être moins cher que la
multiplication elle-même : rapport d'environ 1740 par jeton et par bloc [calcul, confirmé par le critique
Claude]. Mais le critique ChatGPT a noté que ce n'est pas une accélération de la réponse : il faut transmettre
les activations intermédiaires, tenir compte des non-linéarités, des arrondis du profil v2 et de la fraîcheur
du vecteur à chaque requête. La conclusion de claude1 « le trafic des activations rend cela pire qu'une passe
complète » est vraie. On ne peut pas déclarer tout Qwen vérifié par une seule multiplication.

---

## 4. Stratégie recommandée

### 4.1. Étapes

C'est la stratégie du conseil précédent (« payeur-inspecteur »), précisée par les travaux et les critiques de
ce conseil. Aucune étape n'exige de règles secrètes. Les étapes 3, 4 et 9 dépendent de décisions non encore
adoptées (section 5).

1. **Noyau ouvert.** Le générateur d'une instance de vérification, la famille de vérifications admissibles et
   la loi de choix sont la partie ouverte du noyau avec une empreinte figée (D4). « De nouvelles règles à un
   moment aléatoire » — ce sont de nouvelles valeurs de hasard, et non de nouveaux algorithmes.
2. **Fixation.** L'exécutant calcule dans le profil exact v2 et dépose en une seule écriture avec accusé de
   réception le chiffré de la réponse dans le journal (D24). Jusqu'à ce moment, aucun choix de vérification
   n'est fait.
3. **Pièce secrète du payeur.** Après la fixation irrévocable, le programme du payeur prend un hasard frais et
   décide s'il faut vérifier la réponse, avec probabilité
   `p = max(p_util, (R − c_f)/(R + H_lock))` ; avec `c_f ≈ 0`, c'est `R/(R + H_lock)` ; avec `H_lock = 0`
   (débutant) — toujours. Pour l'argent du payeur lui-même, la balise n'est pas nécessaire.
4. **Pièce vérifiable là où l'argent d'autrui en dépend.** Si l'issue de la pièce influence le paiement
   d'autrui (loterie à prix commun, litiges de nœuds tiers), la pièce doit être vérifiable : VRF d'une clé
   enregistrée pour la commande avant fixation, ou engagement sur un sel publié avant fixation (gpt2,
   claude2). Un engagement fait après fixation est vide de sens : le payeur choisit l'issue en voyant déjà la
   réponse (erreur de mm5 dans la proposition D28).
5. **Verrou de la somme.** `H_lock` — seulement la somme qui arrive à maturité après le délai de litige ; le
   délai de vérification `δ` est bien inférieur à la fenêtre de maturation `W` (en temps actif, D12). La
   première falsification prouvée brûle atomiquement toute la somme non arrivée à maturité de la clé, y
   compris les récompenses de la même vague ; la victime ne récupère pas plus que son paiement (candidat D26).
   Sans atomicité, les formules ne tiennent pas la vague : 10 falsifications parallèles avec `R = 1`, `H = 4`,
   `p = 0,2` donnent `+4,4295R` au lieu de `−2,49676R` [calcul].
6. **Mentions.** « Vérifié » — uniquement une réponse entièrement vérifiée avant l'affichage ; tout le reste —
   « non vérifié » par défaut. Une étape d'apprentissage non vérifiée n'entre pas dans le modèle publié (D6).
7. **Échantillons communs selon D20.** L'audit d'apprentissage, l'examen, la loterie à prix commun et la
   désignation des vérificateurs prennent le hasard dans au moins deux sources indépendantes (balise externe à
   seuil et VDF depuis le bloc final), mélangées par hachage ; le tour est désigné avant fixation et commence
   après elle. Les nœuds désignés apprennent le choix via VRF.
8. **Signaux uniquement vers le haut.** Pièges, anomalies, tests statistiques peuvent désigner une vérification
   supplémentaire, mais ne réduisent pas la fréquence et ne donnent pas la mention « vérifié ».
9. **Non-liabilité du payeur** (élément de recherche). Clés de payeur à usage unique et relais, pour que
   l'exécutant ne puisse pas distinguer un payeur vérificateur d'un paresseux (claude1). Tant que le
   mécanisme n'est pas construit, le tableau de risque contient la ligne « les paresseux sont distinguables :
   jusqu'à `+R`, y compris pour un débutant ».
10. **Ce qui n'est pas dans le fondement.** Règles secrètes, clés de vérification réseau, comités à seuil de
    gardiens, TEE, FHE, MPC, iO.

### 4.2. Rôle de la blockchain et de la balise : le « détecteur dynamique sur blockchain » sous sa forme correcte

La question du propriétaire sur un détecteur dynamique sur blockchain reçoit la réponse suivante. La
blockchain fait bien ce qui est exigé d'un détecteur, *sauf* le secret :

- **elle fixe la réponse avant le choix de la vérification** — sans cela, aucun hasard n'aide ;
- **elle stocke les engagements** envers de futurs tours et des sels, pour que personne ne puisse choisir une
  issue commode ;
- **elle rend le choix reproductible** : tout nœud après le tour calcule lui-même ce qui a été choisi et
  vérifie le fondement de la décision même après un arrêt complet du réseau ;
- **elle exécute le brûlage et le calcul unique**.

La « dynamicité » n'est pas donnée par le chiffrement des règles, mais par le fait que l'instance de
vérification est chaque fois dérivée d'un hasard qui n'existait pas encore au moment de la fixation de la
réponse. Pour une réponse privée, ce hasard est la pièce du payeur ; pour les décisions communes — la balise
selon D20. Les travaux l'ont formulé ainsi : « générateur ouvert de règles dans le noyau plus une instance de
règle dérivée de la balise, dont le tour est désigné avant fixation » (claude1) ; « les règles sont ouvertes,
le secret seulement dans le choix : qui, quand et quelle règle appliquer » (mm4) ; « imprévisible, et non
secret » (mm3).

Deux erreurs à éviter :

- **La balise dans la décision monétaire du payeur** (mm3, mm4). Le tirage public dit *quoi* vérifier, mais
  c'est le même payeur qui vérifie ; un payeur paresseux ne vérifiera pas non plus selon un tirage public, et
  il n'y a pas de sanction pour non-vérification sans caution (R5). Le tirage public ici ne fait qu'ajouter
  une hypothèse sur l'honnêteté de la balise et un délai de tour (critiques Claude, DeepSeek ; mm2 et claude2
  disent la même chose). mm3 et mm4 ne sont pas d'accord (section 7).
- **Le mode de secours « selon la dernière valeur disponible »** (mm3). Si la balise est indisponible et que
  les vérifications d'époque se font selon une valeur déjà connue, le trompeur sait d'avance ce qui ne sera
  pas vérifié. Cela viole directement D20. En cas d'indisponibilité du tour, le câblage contesté attend ou la
  vérification est obligatoire.

Encore une précision : « choisir le commode de deux bits indépendants » réduit la probabilité de vérification
obligatoire de `p` à `p²` (critique ChatGPT), tandis que *mélanger* deux sources par un hachage univoque —
c'est exactement ce qu'exige D20. Le complément proposé par mm5 à D19 « la pièce secrète et la balise ne se
mélangent pas » confond ces deux actions et contredirait D20 (critique Claude).

### 4.3. Coût

Le secret des règles ne change pas le coût : il ne touche ni `ρ` ni `γ`.

| `n_w` | `p = R/(R + H_lock)` | Vérification `p·ρ` avec `ρ` = 0,10 / 0,21 / 0,40 | Total contre Q8_0, lot 1 | Lot 8 |
|---|---|---|---|---|
| 30 | 3,23% | 0,32% / 0,68% / 1,29% | +50,5…+82,3% | +152…+186% |
| 300 | 0,33% | 0,033% / 0,070% / 0,133% | +50,0…+80,2% | +150…+181% |
| 4320 | 0,023% | 0,0023% / 0,0049% / 0,0093% | +50,0…+80,0% | +150…+180% |

Tableau — [calcul] selon la formule `γ(1 + pρ) − 1` et les `ρ`, `γ` mesurés (critique MiniMax, vérifié par
les critiques DeepSeek et Claude). Le critique ChatGPT rappelle que les points extrêmes de la plage `γ` et `ρ`
sont pris sur des cartes différentes et n'ont pas été mesurés ensemble ; c'est une enveloppe, non une mesure.

- **Débutant.** La première réponse — vérification complète, 10–40 % de sa génération. Avec un travail honnête
  strictement séquentiel et une croissance de `H_lock` de `R` par tâche, le nombre attendu de vérifications
  complètes pour les 30 premières tâches est `1 + 1/2 + … + 1/30 ≈ 3,995` ; cela fait
  1,33 % / 2,80 % / 5,33 % du travail de la fenêtre avec `ρ` = 0,10 / 0,21 / 0,40 (mm1, critique ChatGPT)
  [calcul]. Avec un démarrage parallèle à compte vide, chaque demande subit une vérification complète.
- **Repère de 5 %.** Comme supplément pour la vérification, il est atteignable : `p·ρ ≤ 0,05` exige `p` au
  plus 50 % / 23,81 % / 12,5 %, c'est-à-dire `H_lock/R ≥ ρ/0,05 − 1` = 1 / 3,2 / 7 (gpt1, gpt2) [calcul].
  Comme « 5 % au-delà de la génération ordinaire » — non : le profil exact lui-même coûte +50…+80 %
  [mesuré γ]. La seule voie vers 5 % — des noyaux plus rapides et bit à bit égaux.
- **Suppléments de la stratégie.** 32–64 octets d'engagement ou des centaines d'octets de VRF par réponse là
  où la vérifiabilité de la pièce est nécessaire ; la balise — des centaines d'octets par tour par lot et un
  délai d'un tour uniquement pour les échantillons communs (critique Claude) [calcul].
- **Qui paie** (mm4, critique MiniMax). La majoration du profil exact `γ − 1` est supportée par l'exécutant sur
  chaque réponse payée ; la vérification `p·ρ` — par le payeur sur son prépaiement. Le transfert de la
  vérification au payeur supprime le rôle de « vérificateur payé pour la vérification » de
  [CURRENT_DESIGN](CURRENT_DESIGN.md), section 1. Alors soit le prix `R` augmente de 50–80 %, soit la marge de
  l'exécutant tend vers zéro. C'est une question séparée du propriétaire (section 5).
- **Loterie B** (seules les réponses choisies et entièrement vérifiées sont payées, variante de gpt1, gpt2 et
  du critique ChatGPT). Avec une part de choix de 5 %, les vérifications coûtent en moyenne 0,5 / 1,05 / 2 %
  du temps de génération exacte, mais 95 % des réponses restent non vérifiées et non payées ; la variance d'un
  paiement séparé `19R²` ; la probabilité de ne recevoir aucun paiement pour 20 demandes indépendantes
  `0,95²⁰ ≈ 35,85 %`, pour 30 — 21,46 % [calcul].
- **Apprentissage.** Une répétition complète d'une étape coûte environ 100 % de l'étape pour chaque nœud
  vérificateur ; le repère de 20 % n'est montré par aucun schéma. Avec `N = 1000` nœuds récepteurs, même à
  coût nul des autres dépenses, il reste au plus 0,0002 du travail de l'étape pour une vérification (critique
  ChatGPT) [calcul].

### 4.4. Risque résiduel

Le gain attendu d'une falsification contre l'inaction ; le « dommage » — la part des falsifications non
détectées du saboteur, toutes avec la mention « non vérifié ». Le tableau est assemblé à partir des tableaux
des critiques Claude, DeepSeek, ChatGPT et MiniMax et de STRATEGY_SEARCH 5.3 ; **les cellules corrigées par ce
conseil sont en gras**. Le détecteur caché n'améliore aucune ligne [calcul].

| Cas | `q = 0,1` | `q = 0,3` | `q = 0,5` | `q = 1` | Débutant, `H = 0` |
|---|---|---|---|---|---|
| Argent, le payeur vérifie lui-même ; journal vivant, D26 et D23 résolues | ≤ 0 | ≤ 0 | ≤ 0 | ≤ 0 | `−c_f` (vérification toujours) |
| Idem, mais la coalition `q = 1` inclut les producteurs de blocs et censure le litige | — | — | — | jusqu'à `+R` | jusqu'à `+R` |
| Fausse réponse avec la mention « vérifié » | 0 | 0 | 0 | 0 | 0 |
| Dommage avec `p = R/(R + H)` : toute la série de `n_w` falsifications passe | ≈ 50% | ≈ 50% | ≈ 50% | ≈ 50% | 0 chez un payeur honnête |
| Dommage avec `p = 3R/(R + H)` | ≈ 12,5% | idem | idem | idem | 0 |
| Payeurs paresseux de part `λ`, l'exécutant ne les distingue pas | ≤ 0 avec `p(1 − λ) ≥ R/(R + H)` | idem | idem | idem | **`+λR`** |
| Payeurs paresseux distinguables (par essais avec de nouvelles clés — gratuitement) | jusqu'à `+R` | jusqu'à `+R` | jusqu'à `+R` | jusqu'à `+R` | **jusqu'à `+R`** |
| Payeur sans équipement ayant confié la vérification à un trio aléatoire | +0,001R | +0,027R | +0,125R | +R | idem |
| Échantillon commun selon D20, au moins une source honnête | ≤ 0 | ≤ 0 | ≤ 0 | ≤ 0 avec une source externe honnête ; sinon jusqu'à `+R` | idem |
| Uniquement balise interne des participants 64/43 | ≤ 0 sauf 4,8·10⁻²⁸ | sauf 9,4·10⁻¹⁰ | sauf 0,41% | jusqu'à `+R` | idem |
| Pour comparaison : règle d'époque secrète chez un comité | fuit en 10 applications avec probabilité 0,65 ; ensuite environ `(1 − p)·E·R` par époque | 0,97 | 0,999 | jusqu'à `+R` par falsification | les essais sont gratuits : jusqu'à `+R` |
| Apprentissage sans nœud auto-vérificateur | jusqu'à `+R` | jusqu'à `+R` | jusqu'à `+R` | jusqu'à `+R` | jusqu'à `+R` |

Comment lire le tableau :

- **La ligne « ≤ 0 pour tout `q` »** n'est vraie que sous les conditions nommées : `q` est la part de collusion
  parmi les vérificateurs extérieurs ; si la même coalition contrôle la production des blocs ou la balise,
  elle peut retarder ou censurer la preuve (cela a été dit directement par gpt1 et gpt2). Il faut aussi
  `δ ≪ W`, un brûlage atomique (D26), la résolution du conflit avec D16 et la règle des litiges fallacieux
  (D23, calcul M9).
- **L'exécution de la vérification importe autant que la fréquence.** Exemple du critique ChatGPT : `R = 1`,
  `H = 3`, `p = 1/4`, `c_f = 0` donnent exactement une espérance nulle ; si le payeur n'exécute que 90 % des
  vérifications désignées, la probabilité de prise est 0,225 et le gain `+0,1R` [calcul]. Si la première
  falsification peut être expliquée par une panne selon le D16 actuel et conserver `H`, l'espérance
  `(1 − p)R − c_f` est positive.
- **« ≈ 50 % »** — c'est la probabilité que passe *toute la série* de `n_w = H/R` falsifications avec
  croissance de `H` après chaque saut (`h/(h + n)` avec `n = h`). Une falsification ciblée d'une clé mûre
  passe avec probabilité `1 − p` : avec `H = 4320R`, cela fait environ 99,977 % (critique ChatGPT d'après
  ds2).
- **Les lignes « paresseux »** sont corrigées : l'ancienne valeur 0 pour un débutant est fausse (section 1,
  point 6). Scénario : une clé fraîche soumet une falsification au payeur `X` ; si `X` vérifie, seul `c_f`
  est perdu, il n'y a rien à brûler ; si `X` est paresseux, la clé obtient `R` et le savoir « `X` est
  paresseux » ; ensuite les clés mûres de la coalition ne soumettent des falsifications qu'aux paresseux
  (critique Claude). Le critique ChatGPT a ajouté que même avec une non-liabilité complète, la condition
  `p(1 − λ) ≥ 1` pour un débutant est irréalisable avec `λ > 0`, et que les clés non liables ne ferment qu'un
  canal de distinction : le texte, le temps, la taille de la requête et le paiement associé restent.

### 4.5. Débutant

Un débutant à compte vide (`H_lock = 0`) contre un payeur honnête est toujours vérifié et perd `c_f`. La
dissimulation des règles n'ajoute rien ici. Deux réserves de ce conseil : contre un payeur paresseux, un
débutant obtient jusqu'à `+R` (section 4.4), et de nouvelles clés gratuites peuvent élever la part des demandes
entièrement vérifiées : si la part du travail pour les premières commandes de clés vides est `f`, et sur les
autres `p = 0,1`, le supplément est `ρ[f + 0,1(1 − f)]`, et la condition de 5 % avec `ρ = 0,21` donne
`f ≤ 0,1534` (critique ChatGPT) [calcul]. Aucun schéma du conseil ne supporte encore simultanément le flux de
nouvelles clés et l'auto-paiement.

### 4.6. Payeur paresseux

La stratégie tient au fait que le payeur lance réellement la pièce et vérifie. Un payeur paresseux, que
l'exécutant peut distinguer, donne jusqu'à `+R` à n'importe quelle clé. Moyens par ordre décroissant de force :
(a) le programme du payeur exécute par défaut la règle du noyau, et la désactivation de la vérification retire
de la réponse la mention « vérifié » ; (b) clés de payeur non liables (claude1) — il faut un mécanisme de
paiement sans émetteur à privilèges particuliers : une signature aveugle a besoin d'un émetteur, Privacy Pass
(de mémoire) — un schéma à émetteur serveur ; un émetteur à seuil réintroduit `q` (critique Claude) ; (c) le
tirage public de la balise *ne* corrige *pas* un payeur paresseux (section 4.2). Comment concilier la
non-liabilité avec la règle des litiges fallacieux sans caution (D23), n'est pas résolu.

### 4.7. Utilisateur sans équipement

Un utilisateur qui ne peut pas recalculer lui-même la réponse n'est pas protégé par cette stratégie. S'il
confie la vérification à un trio aléatoire, la coalition obtient `q³R` : +0,001R / +0,027R / +0,125R / +R ;
avec un seul assistant — `qR`, et avec un complice choisi intentionnellement — jusqu'à `+R` pour toute part
moyenne (critique ChatGPT) [calcul]. Une fuite positive limitée est directement interdite par D1, donc c'est
un trou ouvert de D21. Un détecteur caché ne le ferme pas : claude1 a montré un contre-exemple avec des
« canaris secrets » — un vérificateur de la coalition passe honnêtement tous les contrôles d'autrui et ne ment
que sur ses propres falsifications, qu'il reconnaît par la clé de l'exécutant ou par la liberté de choix (la
falsification n'est pas obligée d'être déterministe, la réponse exacte est déterministe). La variante honnête
— vendre deux niveaux de service avec une différence clairement écrite : « vérifié par moi » et « vérifié par
des désignés, fuite `R·q^k` » (mm1).

### 4.8. Dommage

Le saboteur n'a pas besoin de gain. Pour toute fréquence `p < 1`, une partie de ses falsifications passe. La
seule protection — la mention « non vérifié » par défaut et « vérifié » seulement après une vérification
complète avant affichage. Le détecteur caché ne change pas la ligne du dommage (tous les travaux). mm1 a
trouvé le seul endroit où un *choix frais* change sensiblement le tableau du dommage : avec une vérification
partielle (surtout l'étape d'apprentissage), contre une sonde ouverte fixe, le trompeur trouve par une seule
passe exacte les cellules non vérifiables et ne falsifie qu'elles, la prise est 0 ; un choix frais de la sonde
après fixation donne une prise `s` (part de la partie vérifiée) pour un écart et `1 − (1 − s)^m` pour `m`
écarts. Les critiques DeepSeek et Claude ont précisé : c'est un hasard frais, non un secret des règles ; le
motif d'une telle falsification est le dommage, non l'argent (contre un travail honnête, une falsification
exacte gagne environ zéro) ; et la conclusion tient à une hypothèse non établie, que les cellules de l'étape
d'apprentissage peuvent être falsifiées indépendamment.

---

## 5. Décisions

Les formulations ci-dessous sont des **recommandations**, non des décisions adoptées. Les exigences immuables
R1–R6 ne changent pas par modification des lignes de la feuille de route. Selon D4, après le lancement avec
une empreinte figée, modifier l'ensemble des transitions admissibles exige de passer à un nouveau réseau ; le
changement de clé ne donne pas ce droit (critique ChatGPT).

### 5.1. D4 — compléter, sans changer le sens

D4 actuel : la vérification est automatique, sans votes ; chaque nœud exécute lui-même la vérification selon
l'empreinte figée des règles. Le conseil est unanime contre l'affaiblissement de D4 au profit de règles
secrètes : une règle secrète exige d'accepter le verdict des détenteurs de la clé, de l'enclave ou d'un
groupe, que le nœud ne peut pas vérifier lui-même. Le critique ChatGPT a montré à quoi ressemblerait un tel
affaiblissement : « le nœud accepte le verdict du programme courant choisi par les détenteurs de la clé de
l'époque », « le nœud accepte le rapport d'un programme mesuré selon la chaîne de confiance du fabricant » ou
« le nœud accepte un bit délivré par le groupe ».

**Complément proposé** (fusion des variantes des critiques Claude et ChatGPT, claude1, claude2, gpt1,
proposition D27 de mm5) :

> « Le noyau peut recevoir en entrée un hasard inconnu de l'exécutant avant la fixation définitive du
> résultat : (a) la pièce secrète de la partie dont la propre décision est protégée, lancée après fixation ;
> (b) les valeurs des sources D20 dans des tours désignés avant fixation et commençant après elle. Le
> générateur d'instance de vérification, la famille de vérifications admissibles et la loi de choix sont la
> partie ouverte du noyau avec une empreinte figée ; de nouvelles règles à un moment aléatoire sont de
> nouvelles valeurs de hasard, non de nouveaux algorithmes. L'instance réalisée, influençant les droits
> d'autrui, est publiée au plus tard au paiement et recalculée par chaque nœud. La mention locale du payeur ne
> crée pas en soi de témoignage réseau sur le travail. Le fondement d'une décision commune ne contient pas de
> règles secrètes de longue durée ni de clés de vérification, de comités à seuil, d'attestations TEE ni de
> verdicts fermés ; ils ne sont admissibles que comme vérifications supplémentaires augmentant la fréquence. »

**Ce qui ne change pas :** l'immuabilité du noyau, l'absence de votes, la vérification autonome par chaque
nœud. **Ce qui casse :** rien ; le complément ferme la direction des « détecteurs secrets » comme fondement de
garantie. La possibilité d'une preuve publiquement vérifiable d'une relation figée (ZK) reste ouverte et ne
requiert pas de modification de D4 (critique ChatGPT).

### 5.2. D20 — préciser

D20 actuel : au moins deux sources publiques indépendantes, une valeur à un moment désigné d'avance après la
fixation définitive, sans droit de sauter.

**Précision proposée** (critique Claude avec compléments du critique ChatGPT) :

> « Au moins deux sources publiques indépendantes ; leurs valeurs sont combinées par une fonction de hachage
> univoque avec une étiquette de domaine et un identifiant de lot, et non par choix de l'une des valeurs. Le
> tour de chaque source est désigné avant la fixation définitive et commence après l'acceptation définitive du
> bloc avec fixation. Le saut, le tirage répété, le remplacement de source ou le passage à une valeur connue
> d'avance sont interdits ; en cas d'indisponibilité du tour, le câblage contesté attend, une nouvelle demande
> ne reçoit pas de billet pour ce tour. La balise est utilisée pour les échantillons influençant les droits
> d'autrui (apprentissage, examen, loterie à prix commun, désignation des vérificateurs) ; pour la vérification
> privée par le payeur de son propre argent, elle n'est pas nécessaire. Une balise interne à seuil des
> participants peut être l'une des sources seulement avec une hypothèse consignée sur la part de collusion de
> ses détenteurs, et ne peut pas être l'unique. Un VDF du même bloc n'est pas considéré comme une source
> indépendante. La confiance dans les sources est une hypothèse selon R4. »

**Ce qui exclut :** le mode de secours « dernière valeur disponible » (mm3), la correction de mm5 à D19
(« ne pas mélanger les sources »), la balise dans la décision monétaire du payeur (mm3, mm4). **Risque
ouvert :** si « attendre le tour » signifie un délai infini, c'est un risque R1/R6 non fermé (critique
ChatGPT) ; le critique MiniMax propose, au lieu d'attendre, de considérer la vérification comme obligatoire.

### 5.3. Ce qui ne change pas

- **D1** — ne pas changer et ne pas affaiblir jusqu'à « tant que `q` est petit » ; une fuite positive limitée
  reste une violation (tous les travaux et critiques).
- **D7** — une règle secrète ne le satisfait pour aucun seuil (section 2.4).
- **D19** — ne pas changer : le complément de mm5 est erroné (section 4.2).
- **D6** — la dissimulation ne change pas la ligne du dommage ; les mentions sont précisées selon la question 3
  du recueil précédent.

### 5.4. Lien avec les huit questions du recueil précédent

Les huit questions de [STRATEGY_SEARCH](STRATEGY_SEARCH.md), section 6, restent ouvertes. Ce conseil y a
ajouté :

| Question du recueil précédent | Ce qu'a ajouté le sixième conseil |
|---|---|
| 1. D21, D11, D2 : faut-il payer une réponse sautée par la pièce | Pas de nouveaux arguments. La cellule « payeur paresseux × débutant » est corrigée (jusqu'à `+R`) : si le paiement du sauté est autorisé, il faut une protection contre la distinction des paresseux. Le critique ChatGPT reste pour la vérification complète comme contrat principal et la loterie B comme séparée |
| 2. D7 : quelle vérification est admissible pour le paiement | Il est confirmé que ni la dissimulation, ni l'attestation, ni le comité ne peuvent abaisser la fréquence minimale ; on peut l'augmenter. Ajouté : la part des vérifications *exécutées* importe, pas seulement la fréquence (exemple `+0,1R`) |
| 3. D6 : mentions | Un piège, une statistique et un détecteur caché ne donnent pas la mention « vérifié » |
| 4. D16 : panne honnête | Si la première falsification peut être déclarée panne et `H` conservé, la pièce ne dissuade pas : `(1 − p)R − c_f > 0`. La décision sur D16 est nécessaire avant toute activation du paiement du sauté |
| 5. D8 : délai et droits de litige | La condition `δ ≪ W` et la vivacité du journal entrent dans la ligne « ≤ 0 » (section 4.4) |
| 6. D23 : blocage jusqu'à M9 | Aucun des onze travaux n'a calculé M9 ; le blocage est conservé. La non-liabilité des payeurs ajoute à M9 une nouvelle question |
| 7. Nouvelle D26 : verrou de la somme | La nécessité d'un brûlage atomique de la vague est confirmée ; le bit commun d'époque est un nouveau contre-exemple (`+8,1R`) |
| 8. D1 : faut-il changer | Ne pas changer |

### 5.5. Nouvelles questions-décisions de ce conseil

**Question A (D4).** Faut-il adopter le complément de D4 de la section 5.1 ? *Recommandation des critiques
Claude, ChatGPT et DeepSeek :* oui ; le sens de D4 ne change pas. *Où ils ont divergé :* le critique ChatGPT
propose une rédaction plus détaillée, qui parle explicitement de la vérification « par une preuve
publiquement vérifiable de l'affirmation figée » ; le critique DeepSeek juge suffisante une courte note sur le
hasard après fixation ; le critique MiniMax (comme mm2 et mm5) estime que D4 n'a pas besoin d'être changé du
tout, parce que la règle de vérification est déjà ouverte.

**Question B (D20).** Faut-il adopter la précision de D20 de la section 5.2 ? *Recommandation :* oui. *Où ils
ont divergé :* que faire en cas d'indisponibilité du tour — attendre (critiques Claude et ChatGPT) ou
considérer la vérification comme obligatoire (critiques DeepSeek et MiniMax). L'attente peut devenir un délai
infini ; la vérification obligatoire change le prix et, dans la loterie, la composition des gagnants.

**Question C (balise ou pièce dans la décision monétaire).** Faut-il consigner que, pour la vérification privée
par le payeur de son propre argent, la balise n'est pas utilisée ? *Recommandation* des critiques Claude et
DeepSeek, ainsi que de claude1, gpt1, gpt2, ds1, ds2, mm1, mm2 : oui. *Contre :* mm3, mm4, mm5 (tirage public
au lieu de la pièce), claude2 (VRF du payeur plus balise pour les affaires communes). Le critique DeepSeek
propose de comparer d'abord les deux schémas par un mini-agent sur les mêmes attaques (section 6).

**Question D (payeurs non liables).** Faut-il inclure dans le programme de recherche un mécanisme où
l'exécutant ne peut pas lier les requêtes d'un même payeur ? *Recommandation* du critique Claude : oui, comme
recherche ; avant sa construction, le tableau de risque contient la ligne « les paresseux sont
distinguables : jusqu'à `+R` ». *Ouvert :* paiement sans émetteur à privilèges particuliers, compatibilité
avec D23, distinction par le texte et le temps.

**Question E (poids).** Faut-il consigner dans la spécification du poids ([CURRENT_DESIGN](CURRENT_DESIGN.md),
section 4) que le poids selon lequel sont sélectionnés les détenteurs ou les vérificateurs ne croît pas du fait
des requêtes auto-payées ? *Recommandation* du critique Claude : oui. claude2 proposait une sélection « selon
le poids du travail vérifié » sans cette réserve.

**Question F (qui paie le profil exact).** Comment répartir la majoration `γ − 1` si le rôle du vérificateur
payant disparaît ? *Posée par* mm4 et le critique MiniMax ; aucune solution proposée.

**Question G (nouvelles décisions de mm5).** Faut-il adopter D27 (« secret du choix, et non secret de la
vérification ») et D28 (« pièce à révélation différée ») ? *Recommandation des critiques :* D27 entre par son
sens dans le complément de D4 (section 5.1) ; D28 duplique l'engagement de pièce de gpt2 et claude1 et n'a de
sens que si l'engagement est publié *avant* la fixation de la réponse.

---

## 6. Ce qu'il faut calculer par mini-agents et ce qu'il faut vérifier par l'expérience

### 6.1. Mini-agents (fractions exactes, hachage de contrôle, répétition sur un second appareil)

Liste commune des quatre critiques. Pour chaque calcul, conserver la description des règles, les entrées, les
fractions exactes, la pire histoire, la version et le hachage de contrôle (critique ChatGPT).

1. **Règle d'époque contre pièce fraîche.** Vague, `H_lock`, brûlage de toute la somme, séquence adaptative.
   Références : `+8,1R` / `−2,3751096381R` (gpt2), `98,01R` (claude2), 1/5 → 1/9 → 0 (claude1),
   `+4,4295R` / `−2,49676R` / `+7,2R` (conseil précédent et critique ChatGPT).
2. **Essais de payeurs paresseux avec de nouvelles clés.** Espérance de l'essai, temps jusqu'à la
   reconnaissance du payeur, gain des clés mûres ; avec des payeurs liables et non liables. Espérance du
   critique Claude : avec liabilité, la dissuasion contre les paresseux est nulle.
3. **Pièce secrète contre tirage public de la balise** sur les mêmes attaques (critique DeepSeek). Attendu :
   des issues monétaires égales et un prix plus élevé pour le tirage public.
4. **Programme linéaire de mélange de tests** (gpt1, gpt2) : référence « trois classes → 2/3 contre 1/2 »,
   ajout d'une classe non couverte → 0 ; minimax sur la matrice « test × falsification ».
5. **Queues de seuil :** binomiales, sans remise, par poids avec auto-paiement, avec corruption après
   désignation. Référence « 3 sur 5 » : `107/12500`, `4077/25000`, `1/2`, `1` ; hachage de contrôle SHA-256
   des quatre lignes de gpt1, répété par le critique ChatGPT :
   `fd83fbdd42baa56d982eba3be90888cf3ec5a6261b5daa53d42fdc42b99c8323`.
6. **Pièges :** `1/((1 − σ)ρ)` sur une grille de `ρ` et `σ` ; reconnaissance de la répétition ; amortissement
   d'une banque de références contre le recalcul ; vérification de l'affirmation de mm2 sur le prix presque
   nul de la répétition d'une requête vérifiée.
7. **Écarts dans la VRF et l'engagement du payeur :** refus de révéler, plusieurs clés, interruption après
   révélation, loterie à prix commun.
8. **Mélange des sources D20 :** biais avec une source honnête, avec rétention d'un bloc, avec indisponibilité
   du tour ; interdiction de la « dernière valeur ».
9. **Falsification « chirurgicale » de mm1** contre une sonde ouverte fixe et une sonde fraîche : prise 0
   contre `s` ; seuil `p·s ≥ (R − c)/(R + H_lock)`.
10. **Comptage des opérations non linéaires par jeton** selon la configuration figée D5 pour les estimations
    FHE et MPC (actuellement 1,4·10⁷–2,6·10⁷ approximativement) ; estimations DKG, commit–reveal, VRF en
    octets et messages.
11. **Lot 8 chez le payeur** (mm3) : `ρ` est mesuré par rapport à la génération par lots, et le recalcul d'une
    réponse par le payeur ne devient pas moins cher ainsi.
12. **Correction des tableaux :** mm1 (`k = 10`, `H_lock = 10R`), mm5 (`p·ρ`), cellule « paresseux × débutant »
    dans STRATEGY_SEARCH 5.3.
13. **M9** — prix du litige pour la règle D7 et condition de levée du blocage D23 ; auto-litige, limite du
    remboursement, flux de nouvelles clés.

### 6.2. Expériences

**Pour la conclusion sur le détecteur caché, aucune expérience n'est nécessaire :** ce sont des théorèmes, la
mesure ne les réfute pas (claude1, claude2, ds2, critiques Claude et DeepSeek). Les expériences avec FHE, MPC
et TEE ne sont pas non plus nécessaires : leur meilleure issue ne change pas les théorèmes.

**Dans le cadre de D5 (autorisé) :** O5 — qualité sur 320 tâches ; O3 et O4 avec des noyaux plus rapides et
bit à bit égaux — la seule voie vers le repère de 5 %.

**Hors D5 — seulement avec une autorisation séparée du propriétaire :**

- temps d'une passe de vérification sur le CPU d'un ordinateur portable et sur un téléphone, démarrage à froid
  et à chaud, énergie ;
- dans quelle mesure les métadonnées de la requête (temps, taille, texte) permettent à l'exécutant de
  distinguer un payeur vérificateur — le prix des clés non liables en dépend ;
- fréquence des écarts matériels silencieux `P_f` — avant toute modification de D16 ;
- part de coïncidence des jetons Q8_0 et du profil exact (pour l'estimation d'une falsification bon marché et
  pour un décodage spéculatif exact) ;
- délai et coût d'un tour d'une balise réelle, comportement en cas de source silencieuse ;
- pour les pièges — si la vérification est reconnue et combien coûtent les références ;
- la répétition exacte d'une étape d'apprentissage comme condition préalable à toute vérification de celle-ci.

---

## 7. Divergences non résolues par le conseil et références douteuses

### 7.1. Divergences

1. **Paiement du sauté par la pièce contre vérification complète de chaque réponse payée.** claude1, claude2,
   ds1, ds2 et mm1–mm5 s'appuient sur le paiement du sauté sous risque de brûlage de la somme non arrivée à
   maturité ; gpt1, gpt2 et le critique ChatGPT — sur la vérification complète comme contrat principal et la
   loterie B comme séparée. Hérité du conseil précédent ; décision du propriétaire sur D21, D11, D7.
2. **Balise ou pièce dans la décision monétaire du payeur** — section 5.5, question C. mm3 et mm4 estiment que
   le tirage public supprime l'hypothèse d'un payeur honnête ; les critiques Claude et DeepSeek considèrent
   cela comme une erreur (un payeur paresseux ne vérifiera pas non plus selon un tirage public). Non calculé.
3. **`R/(R + H_lock)` ou `R/H`.** Le premier est exact pour l'argent ; le second donne une marge et un nombre
   attendu fini de falsifications avant la prise à `H` fixe, mais coûte environ deux fois plus cher avec un
   petit `H`. Le critique ChatGPT a montré qu'avec une croissance de `H` après chaque saut, le nombre moyen de
   sauts jusqu'à la première prise est infini pour les deux règles. Le conseil n'a pas donné de nouveaux
   arguments.
4. **Le piège comme gain autonome.** mm2 (référence secrète — le seul gain véritable) et ds1 (économie d'une
   référence mise en cache) contre claude2, mm4, mm5, gpt1 et les critiques Claude et DeepSeek. Le critique
   ChatGPT a pris une position intermédiaire : une référence déjà connue d'un payeur honnête peut réduire le
   coût marginal, et pour des pièges frais indiscernables, `σ` peut être 0 même avec `q = 1` parmi les
   exécutants extérieurs. Calcul non effectué.
5. **Mélange de types de vérification comme moyen d'économie.** gpt1, gpt2, claude2 — possible avec une
   couverture démontrée des classes d'erreurs ; mm2 — jamais. Pour Qwen, la couverture n'est pas démontrée.
6. **Balise interne à seuil des participants.** mm3 — le meilleur primitif ; mm5 — uniquement externe ;
   claude1, claude2 et le critique Claude — admissible seulement comme l'une des sources.
7. **Dans quelle mesure R2/R3 interdisent les secrets communs.** ds1, mm1, mm3 — par principe ; claude2,
   critiques Claude et ChatGPT — seulement les secrets nécessaires pour vérifier les décisions passées.
8. **Coût du MPC.** Les estimations divergent de plusieurs ordres de grandeur : ds1 — 2,4–14 Mo par jeton (les
   critiques estiment que c'est le prix de la trace de vérification, non du MPC) ; critique Claude —
   0,15–1 Go par jeton ; critique ChatGPT — 448 Mo par position ; critique MiniMax — jusqu'à 180 To par
   réponse (il considère toutes les multiplications comme effectuées sur le réseau, et le critique ChatGPT remarque que la
   multiplication d'un poids ouvert par une activation partagée s'effectue localement dans beaucoup de
   protocoles). La conclusion « MPC hors budget et dépendant de `q` » n'en change pas.
9. **Multiplicateurs FHE :** ds1 `10³–10⁶`, claude2 `3·10³–2·10⁵` ; le critique ChatGPT estime qu'il est
   incorrect de multiplier l'estimation par bootstraps par `ρ` d'une passe prête, et qu'il faut une estimation
   d'une même passe sous un schéma concret. Les conclusions n'en dépendent pas.
10. **Sonde cachée lors d'une vérification partielle** (mm1) : « détecteur secret » ou pièce fraîche —
    divergence de mots ; l'applicabilité à l'étape d'apprentissage dépend de l'indépendance non mesurée des
    cellules.
11. **D16.** Brûler `H_lock` pour tout écart prouvé avec indemnisation des honnêtes sur un prélèvement réseau
    (ligne de claude1 et des critiques Claude et DeepSeek) contre la conservation des récompenses précédentes
    en cas de panne honnête (gpt1, gpt2, critique ChatGPT). Une mesure de `P_f` est nécessaire.
12. **Apprentissage.** Aucun schéma ne satisfait D7 avec `q = 1` dans la limite de 20 %.
13. **Classe principale de falsifications :** la « chirurgicale » coûteuse (mm1) ou la Q8_0 bon marché (mm3,
    mm4). Non mesuré.

### 7.2. Erreurs trouvées dans les nombres des travaux

Pour que les nombres erronés n'entrent pas dans d'autres documents :

| Travail | Affirmation | Correct [calcul des critiques] |
|---|---|---|
| mm1 | Avec `H_lock = 10R`, fréquence 0,0909 et coût de vérification 0,005–0,009% | `0,0909·ρ` = 0,91–3,64% |
| mm1 | Fuite des « dizaines » avec `q = 0,1` : `1·10⁻⁵R` | `10⁻¹⁰R` |
| mm1 | Seuil 25% avec `H_lock = R` | 29,29% avec les propres paramètres de mm1 |
| mm5 | `p·ρ` = 0,021–0,042% avec `p = 0,1` | 2,1–4,0% (le propre tableau de mm5 est correct) |
| mm5 | « FHE est déterministe, l'observateur construit un dictionnaire » | Les schémas FHE robustes sont probabilistes |
| mm5 | « VRF imprévisible pour le détenteur » | Le détenteur calcule la VRF quand il veut |
| mm5 | Répétition complète d'une étape d'apprentissage ≈ 36,8% | 36,8% — exemple de charge mixte ; la répétition de l'étape ≈ 100% |
| mm2 | « 5% atteignables avec `p ≤ 0,33%` » | Avec `ρ = 0,21`, `p ≤ 23,8%` est admissible |
| mm4 | « VRF ne révèle pas le choix » | La vérification de la preuve VRF révèle la valeur |
| ds2 | `N·H_s ≈ 2718` tentatives | Environ 890 sans remise ; une seule position sûre suffit |
| ds1 | Un piège coûte `φ·ρ`, une référence en cache économise | Un piège coûte au moins une génération de l'exécutant ; il faut d'abord obtenir le cache |
| ds1, ds2 | Les pièges ajoutent une prise `φ` pour tout `q` | Pas plus de `φ(1 − q)` en cas de répétition ; avec `q = 1` — 0 |
| claude1, claude2, mm3, mm4, STRATEGY_SEARCH | Payeur paresseux × débutant = 0 | Jusqu'à `+R` |
| claude2 | Formule de l'exemple d'époque `(1 − p)(E − 1)R` | `(1 − p)·E·R − p·H_lock = 98,01R` ; coïncidence fortuite |

### 7.3. Références douteuses (estimations des critiques de mémoire, sans vérification)

| Travail | Affirmation | Évaluation |
|---|---|---|
| mm5 | « RandAILight » comme balise | Douteux ; nom inconnu des critiques |
| mm5 | « iO théoriquement possible, Barak et coauteurs ~2001 » | Confondu : Barak et coauteurs 2001 — impossibilité de l'obfuscation « boîte noire » ; candidats iO — Garg et coauteurs 2013 |
| mm1 | « Feuille de route iO de Barak et coauteurs, 2019 » | Douteux |
| mm2 | Annexe F : « Ben-Or et coauteurs », « Allingham, Melvin, Temple 1992 », « Dwork ~1999 », « Hashcash — HomeStein », « Awasthi », « Randcast Bader ~2020 » | Douteux sur presque tous les points ; ne pas transférer dans le recueil |
| mm3 | « Cui, Wang et al., Skoglid et al. » sur moving target defense | Douteux |
| ds1 | « Canetti 1997 — fonctions ponctuelles dans le modèle d'oracle aléatoire » | Douteux (de mémoire — hypothèse de type DDH) |
| ds1 | « Bishop–Jain–Kowalczyk 2018 » | Douteux quant à l'année (de mémoire 2015) |
| ds1, ds2 | « drand ~30 s » | Partiellement : de mémoire, 30 s et 3 s selon les chaînes |
| ds2 | « MPC 5,98·10¹² MAC (claude2) » | Référence imprécise |
| claude1 | « SGX.Fail, clé maîtresse Secret Network, 2022 » | Douteux dans les détails (l'auteur lui-même l'a marqué) |
| claude1 | Privacy Pass comme exemple d'émission sans partie particulière | De mémoire — schéma à émetteur serveur |
| claude2 | Borne inférieure PIR — Beimel, Ishai, Malkin | Douteux : leurs travaux portent sur le PIR avec prétraitement ; la borne classique, de mémoire, est chez Chor et coauteurs |
| claude2 | Lowd–Meek, Tramèr : `d` requêtes binaires suffisent pour tout classifieur | Douteux en général |

Les autres références des travaux (Shamir, Feldman, Pedersen, Gennaro–Jarecki–Krawczyk–Rabin,
Micciancio–Rabin–Vadhan, Boneh et coauteurs sur VDF, Rivest–Shamir–Wagner, Aumann–Lindell, Asharov–Orlandi,
jeux d'inspection, Barak et coauteurs sur l'impossibilité de la « boîte noire ») paraissent aux critiques
correctement attribuées quant à la direction ; les sources primaires n'ont pas été vérifiées.

---

## 8. Qui a fait quoi

Le conseil a travaillé sur les matériaux du projet, sans accès au réseau et sans expériences.

- **Onze travaux indépendants :** ChatGPT — deux (gpt1, gpt2), DeepSeek — deux (ds1, ds2), Claude — deux
  (claude1, claude2), MiniMax — cinq (mm1 axé sur l'économie, mm2 — sur la protection contre la tromperie,
  mm3 — sur la distribution et la restauration, mm4 — sur les contre-exemples, mm5 — sur les solutions non
  standard). Chaque travail a analysé six directions de la mission : qui détient la clé, comment vérifier
  selon une règle inconnue, ce qui peut être un détecteur secret, la théorie, le prix et la compatibilité
  avec les décisions.
- **Quatre critiques :** une de ChatGPT, DeepSeek, Claude et MiniMax (la critique MiniMax est rédigée comme
  une proposition avec critique). Chaque critique a lu les onze travaux, cherché des erreurs et des
  contre-exemples et recalculé les nombres clés. Le critique DeepSeek vérifiait l'arithmétique par des
  programmes locaux sur des fractions exactes, le critique Claude — par de courts calculs en Python, le
  critique ChatGPT a reproduit le hachage de contrôle du tableau de gpt1.
- **Recueil :** ce document a été composé par Claude d'après les travaux et les critiques. Aucune nouvelle
  évaluation ni nombre au-delà des travaux, des critiques, des résultats D5 et de STRATEGY_SEARCH n'a été
  ajouté ; là où les critiques ont divergé, cela est indiqué.
