<!-- translation of docs/STAGE4_KERNELS.md, source sha256: e81d4e27191f3ce009ea9b71602c58405e742a7229fc972d8c69ae520e675812 -->

# Étape 4. Contrat à l'octet près des calculs intégrés

[English](../../docs/STAGE4_KERNELS.en.md) · [中文](../zh/STAGE4_KERNELS.md) · [Español](../es/STAGE4_KERNELS.md) · **Français** · [Deutsch](../de/STAGE4_KERNELS.md) · [Italiano](../it/STAGE4_KERNELS.md) · [Русский](../../docs/STAGE4_KERNELS.md) · [Português](../pt/STAGE4_KERNELS.md) · [العربية](../ar/STAGE4_KERNELS.md)

État au 24 novembre 2026. Le document fixe les règles exactes de quatre nouveaux calculs intégrés du mini-agent (depuis la version 1.2.0 de l'agent) pour les calculs M8, M10, M12 et M14 de [VERIFICATION_SEARCH](VERIFICATION_SEARCH.md), section 5.3. ChatGPT a écrit la spécification et l'implémentation en Go ; DeepSeek a vérifié indépendamment la spécification d'après les travaux d'origine du conseil et, à partir de celle-ci seule, a écrit une seconde implémentation en Python ([tools/reference_stage4.py](../../tools/reference_stage4.py)) ; les 73 résultats des tâches ont coïncidé à l'octet près ; Claude a vérifié le code et la comparaison. Les références du type « claude1, §5.4 » renvoient aux travaux du conseil de modèles réunis dans VERIFICATION_SEARCH. C'est un décompte exact par formules, et non une mesure : la coïncidence confirme l'arithmétique, mais pas les hypothèses des modèles. Les calculs M5, M7 et M18 sont reportés : les travaux manquent de règles pour les définir sans ambiguïté (section « Calculs reportés »).

| Calcul du §5.3 | Noyau de version 1 | Ce que l'on peut apprendre d'une seule unit |
|---|---|---|
| M8 | `t4-scale` | Combien de jetons d'apprentissage par nœud sont nécessaires pour un nombre donné de soumissionnaires, et combien de soumissionnaires le budget autorise |
| M10 | `exam-thresholds` | Dans quel intervalle rationnel se situe chacun des deux seuils de l'examen |
| M12 | `merge-attribution` | Comment varie la somme des crédits d'un participant lors de l'ajout de copies exactes ou bruitées |
| M14 | `verification-enumerations` | Quels cas ont réussi ou échoué de manière exhaustive à la vérification de l'empaquetage, de la chaîne ou de l'égalité sur le corps |

Le choix découle du tableau du conseil au §5.3. Selon D18, le paiement pour une amélioration reste une hypothèse de recherche. Les paramètres d'entrée suffisent à reproduire les quatre calculs. [Résultat du conseil](VERIFICATION_SEARCH.md) · [Décisions D18–D20](ROADMAP.md)

## Règles communes de la version 1

Dans la tâche à signer, le nom du noyau et l'entier `kernel_version: 1` sont stockés séparément. L'entrée `params` est un objet contenant tous les champs énumérés pour le noyau. Les champs superflus ou manquants, la répétition d'une clé JSON, les valeurs hors plage et les types incorrects provoquent une erreur. Un entier s'écrit comme un littéral JSON entier, sans point décimal ni exposant. Les chaînes et les valeurs booléennes à la place de nombres sont interdites. Les bornes sont incluses. Les axes de la grille conservent l'ordre d'entrée. Le nombre d'units est exactement égal à la taille de grille indiquée pour le noyau, de 1 à 1 000 000. La numérotation des units commence à zéro. Dans le produit cartésien, le dernier axe varie le plus vite.

Pour la comparaison, on prend l'objet résultat entier. En Python, les octets canoniques sont égaux à `json.dumps(result, sort_keys=True, ensure_ascii=True, separators=(',', ':')).encode('ascii')`, sans saut de ligne final. Le hachage du résultat est le SHA-256 de ces octets, soit 64 chiffres hexadécimaux minuscules. L'ordre des éléments des tableaux est significatif. Une fraction sous forme de chaîne s'écrit en base dix comme `p/q` avec un dénominateur positif après réduction, y compris `0/1` et les entiers avec `/1`. Il n'y a ni signes plus ni zéros de tête. Pour M14, le hachage des octets *à l'intérieur* du résultat d'empaquetage est défini séparément. [Encodeur canonique de l'agent](../../agent-go/canon/canon.go)

## M8. Échelle de T4 avec une mise à jour de chaque participant

`t4-scale@1` calcule le nombre entier minimal de jetons d'apprentissage propre par tour pour lequel l'examen ajoute au plus 20 % de calculs. Pour un budget de jetons donné, le noyau trouve aussi le nombre limite de soumissionnaires. Dans le modèle, chaque nœud vérifie toutes les `K=N` mises à jour. La base coûte une passe directe par position, chaque mise à jour des couches supérieures — une fraction `a=L_a/L` d'une passe, et l'apprentissage d'un jeton coûte trois passes. Ces rapports sont fixés par la proposition. claude1, §5.4 « Prix » et §7.5, point 4 · critic_claude, §1.8 et §10.4, point 3 · [VERIFICATION_SEARCH, §5.3, M8](VERIFICATION_SEARCH.md)

| Champ `params` | Valeurs autorisées |
|---|---|
| `N` | Axe d'entiers de 1 à 1 000 000. Nombre de soumissionnaires dans le tour |
| `n` | Axe d'entiers de 1 à 1 000 000. Nombre de positions d'examen |
| `a` | Axe de paires d'entiers `[p,q]`, où `1 ≤ p ≤ q ≤ 1 000 000`. Fraction de passe par mise à jour |
| `D_budget` | Axe d'entiers de 1 à 1 000 000 000 000. Budget de jetons d'apprentissage par nœud et par tour |
| `epsilon_bits` | Un entier de 1 à 256. Fixe `ε=1/2^epsilon_bits` pour un examen fixé. Pour un `n` donné, le coût est le même pour tous les `ε` |

Les cinq champs sont obligatoires. Chaque axe est un tableau de longueur 1…32, les valeurs sont uniques compte tenu de la réduction des fractions, l'ordre du tableau d'entrée est conservé. Le nombre d'units est égal au produit des longueurs des axes et ne dépasse pas 1 000 000. Numérotation à partir de zéro selon le produit cartésien `N, n, a, D_budget` dans l'ordre des boucles imbriquées, le budget variant le plus vite. Une unit produit un objet.

Pour le point choisi, posons `D=D_budget` et réduisons `a=p/q`. Mesurons les calculs en unités de `1/q` de passe directe par position. Alors l'examen exige `E=n(q+Np)`, l'apprentissage exige `W=3Dq`, la fraction de surcoût est `E/W`. La division par le volume de l'apprentissage propre découle de la formulation « supplément » au §5.4. La condition de 20 % équivaut à `5E ≤ W`.

| Champ du résultat | Valeur |
|---|---|
| `kernel` | Chaîne `t4-scale@1` |
| `N`, `n`, `D_budget` | Entiers du point d'entrée |
| `a`, `epsilon` | Chaînes réduites `p/q` ; `epsilon` s'écrit `1/q`, où `q = 2^epsilon_bits` est un entier décimal (par exemple, `"1/4"` pour `epsilon_bits = 2`) |
| `D_min` | Entier `(5E + 3q − 1) // (3q)`, où `//` est la division entière vers le bas. C'est l'arrondi du seuil vers le haut jusqu'à un jeton entier |
| `fits` | Valeur booléenne `D_budget ≥ D_min`. L'égalité compte |
| `N_max` | `null` si `W < 5nq` et que même la passe de base dépasse le budget. Sinon l'entier `(W − 5nq) // (5np)`. Zéro signifie que seule la base tient. La limite peut dépasser l'axe d'entrée `N` |
| `overhead` | `E/W` sous la forme d'une chaîne réduite `numerator/denominator` |

La borne inverse découle de l'inégalité linéaire `5npN ≤ W − 5nq` pour `p` positif. Avec les paramètres autorisés, `5E+3q−1 ≤ 5 000 005 000 002 999 999`, `W ≤ 3·10^18`. Les dénominateurs sont positifs. Des entiers signés de 64 bits et la réduction des fractions par le PGCD suffisent. En Go, `big.Rat` est utilisé pour `overhead`, et `big.Int` pour `2^epsilon_bits`. Une unit comporte l'analyse d'au plus 128 éléments d'axes et un nombre constant d'opérations arithmétiques.

Pour `n=3, N=4, a=1/2`, l'examen coûte 9 passes ; avec 15 jetons d'apprentissage, il occupe exactement un cinquième. Avec 14 jetons, la limite tombe à trois soumissionnaires. Avec `epsilon_bits=2`, on obtient les octets canoniques suivants.

```json
{"D_budget":15,"D_min":15,"N":4,"N_max":4,"a":"1/2","epsilon":"1/4","fits":true,"kernel":"t4-scale@1","n":3,"overhead":"1/5"}
```

Pour le repère du §5.4, avec `n=100000, N=10000, a=4/36`, le minimum exact est de 185 351 852 jetons. Le coût physique dépend de la réutilisation des préfixes, du volume du cache, de la tête de sortie, de la normalisation, du trafic et du coût réel de l'apprentissage des couches supérieures. La formule ne couvre que le décompte de passes décrit au §5.4. M10 sert à estimer le seuil statistique lorsque `ε` change. La tâche proposée fixe `ε=2^-80` conformément au repère numérique D19. critic_gpt, section sur claude1, « Le prix caché de T4 » · [ROADMAP, D18–D19](ROADMAP.md)

## M10. Seuil de l'examen T4 — `exam-thresholds@1`

M10 détermine quelle doit être l'ampleur de l'amélioration moyenne observée à l'examen pour qu'elle dépasse le seuil statistique. Pour un candidat fixé à l'avance, on prend `n` positions indépendantes avec remise. La différence de pertes à chaque position est écrêtée à `[−B/2, B/2]`. L'entrée `V` est la variance d'échantillon des différences écrêtées avec le diviseur `n−1` (le carré de l'écart type). Les bornes en nats par position proviennent de l'étape 6 de la description de T4. claude1, §5.4 · critique Claude, §1.8

| Méthode | Seuil exact `t` |
|---|---|
| Hoeffding | `B·√(ln(1/ε)/(2n))` |
| Bernstein empirique | `√(2V·ln(2/ε)/n) + 7B·ln(2/ε)/(3(n−1))` |

**Paramètres et units.** Cinq champs sont obligatoires. Les champs `n`, `epsilon_bits`, `B`, `variance` sont des axes de longueur 1 à 32, chacun dans l'ordre du tableau d'entrée. Les valeurs d'un axe sont distinctes, les fractions sont comparées après réduction.

| Champ | Valeurs autorisées |
|---|---|
| `n` | Nombre de positions, entier de 2 à 1 000 000 |
| `epsilon_bits` | Entier `k` de 1 à 128, `ε = 2⁻ᵏ` par comparaison |
| `B` | Largeur de la plage d'écrêtage, entier de 1 à 64 |
| `variance` | Fraction `[p,q]`, entiers `0 ≤ p ≤ 10⁶` et `1 ≤ q ≤ 10⁶`. En tous les points de la grille `V=p/q ≤ B²·floor(n/2)·ceil(n/2)/(n(n−1))` |
| `digits` | Un entier `d` de 1 à 9. La largeur absolue garantie de chaque intervalle est inférieure à `10⁻ᵈ` |

Le maximum de variance est atteint aux extrémités de la plage, car la variance est convexe par rapport à chaque observation. Pour `j` valeurs à une extrémité, son numérateur est proportionnel à `j(n−j)`, ce qui donne la borne indiquée. Le nombre d'units est égal au produit des longueurs des quatre axes et ne dépasse pas 1 000 000. La numérotation coïncide avec `itertools.product(n, epsilon_bits, B, variance)`, à partir de zéro.

**Algorithme de reproduction à l'octet près.** Pour les deux méthodes, écrire `t = √(A·ln 2) + C·ln 2`. Pour Hoeffding `A=B²k/(2n), C=0`. Pour Bernstein `A=2V(k+1)/n, C=7B(k+1)/(3(n−1))`. Toutes les divisions ici sont rationnelles.

1. Prendre `S=10^(d+1)`, `l=693147180559945309/10¹⁸`, `h=693147180559945310/10¹⁸`.
2. La borne inférieure vaut `(floor(√(S²Al)) + floor(SCl))/S`. La borne supérieure vaut `(ceil(√(S²Ah)) + ceil(SCh))/S`. Les deux termes sont arrondis **séparément**.
3. Pour une fraction non négative `x=p/q`, calculer `r=isqrt(p//q)`. C'est `floor(√x)`. Pour la borne supérieure, ajouter un à `r` exactement lorsque `r²q < p`. Les `floor` et `ceil` ordinaires s'effectuent aussi par division entière. Toutes les fractions obtenues sont réduites.

**Certificat de précision.** Dans la série pour `2·atanh(1/3)=ln 2`, nous prenons `T=2·Σ 1/(j·3ʲ)` pour les j impairs `j=1,3,…,39`. Le reste est positif et majoré par le premier terme omis multiplié par `1/(1−1/9)`. Par comparaison entière, nous obtenons `l < T < ln 2 ≤ T + 9/(4·41·3⁴¹) < h`. La monotonie des deux termes et l'arrondi dirigé assurent l'encadrement du seuil vrai. Dans la plage indiquée, `A ≤ 264192` et `C ≤ 19264`. Comme `√h+√l > 1`, le remplacement de `l` par `h` modifie le seuil non arrondi de moins de `(515+19264)·10⁻¹⁸`. L'arrondi élargit l'intervalle de moins de `4/S`. La somme est inférieure à `10⁻ᵈ` même pour `d=9`. Par unit, quatre racines carrées entières et un nombre constant d'opérations sur des entiers et des fractions de quelques centaines de bits suffisent, indépendamment de `n`.

**Réponse.** Les champs `n`, `epsilon_bits`, `B` et `digits` sont les coordonnées entières et la précision. `variance` est une chaîne contenant une fraction réduite. `hoeffding` et `bernstein` sont des tableaux de deux telles chaînes, la borne inférieure en premier. Pour `n=2, k=1, B=2, V=0, d=1`, le noyau produit les octets canoniques suivants.

```json
{"B":2,"bernstein":["323/50","647/100"],"digits":1,"epsilon_bits":1,"hoeffding":["83/100","21/25"],"kernel":"exam-thresholds@1","n":2,"variance":"0/1"}
```

Pour un seuil limite `τ` donné, la taille minimale d'examen **sur la grille** est établie lorsque, au point choisi, la borne supérieure est `≤ τ`, et que pour tous les `n` plus petits, avec les mêmes paramètres, la borne inférieure est `> τ`. Si l'intervalle croise la cible, une précision plus grande peut être nécessaire. Les nombres caractérisent une comparaison unilatérale de la moyenne tronquée avec fixation avant la balise externe. La correction pour le choix parmi plusieurs candidats, la qualité hors examen, le choix de `τ` et l'ampleur de l'effet réel exigent des données ou des règles séparées. Le paiement pour une amélioration reste une variante de recherche selon D18. [ROADMAP, D18–D20](ROADMAP.md) · critique GPT, estimation de T4

## M12. Comment varie le crédit du propriétaire des doublons lors d'une fusion par somme

Le travail pour M12 indique des pertes linéaires-quadratiques avec gradient et hessien connus, trois règles d'attribution, des doublons exacts et des doublons avec bruit. Nous choisissons la variante explicitement analysée au §5.4 `merge = sum`. Le critique cite un cas où même l'ajout répété de la même étape améliore la fonction de pertes. Le noyau `merge-attribution@1` vérifie cela sur des coefficients d'entrée explicites. claude1, §5.4, étapes 6–7 et point 2 « Attribution et doublons », §7.5, point 7 · critic_gpt, tableau sur claude1, ligne T4

| Champ `params` | Sens et bornes incluses |
|---|---|
| `scale` | Dénominateur commun `s`, entier 1…10 000 |
| `g` | Vecteur des numérateurs du gradient au point de base. Sa longueur fixe la dimension `d`, 1…8 |
| `hessian` | Matrice symétrique des numérateurs du hessien, tableau de `d` lignes de `d` composantes |
| `updates` | Tableau de `b=1…8` vecteurs de numérateurs initiaux de longueur `d`, dans l'ordre de soumission. Les vecteurs identiques sont autorisés |
| `owner` | Index entier de la soumission initiale du participant vérifié, de 0 à `b−1`. Les autres soumissions initiales appartiennent à d'autres participants |
| `copies` | Axe de 1…8 entiers distincts 1…8. Le `c` choisi fixe le nombre de soumissions ajoutées du même participant |
| `noise` | Axe de 1…32 vecteurs de numérateurs de longueur `d` deux à deux distincts. Le vecteur nul donne un doublon exact |
| `threshold` | Numérateur entier 0…10 000 pour la déduction `t=threshold/s` de l'évaluation de chaque soumission |

Chaque composante de `g`, `hessian`, `updates` et `noise` est un entier de −10 000 à 10 000. Pour obtenir la valeur mathématique de chaque composante, la diviser par `s` **une seule fois**, y compris pour la matrice. La version prend en charge des coefficients rationnels de dénominateur commun dans la plage indiquée. La symétrie est obligatoire, le signe de la courbure est arbitraire. Les axes d'entrée `copies, noise` forment une grille. Pour l'unit `u`, prendre les indices `divmod(u,len(noise))` respectivement. Après les `b` soumissions initiales, ajouter `c` vecteurs, chacun égal à `updates[owner] + noise[j]` en numérateurs. Les vecteurs initiaux sont conservés. Les groupes de soumissions avant et après l'ajout sont examinés séparément.

**Calcul.** Soit `U` l'ensemble des indices des soumissions d'un même groupe, et `x(S)` la somme de leurs vecteurs de mise à jour **mathématiques** sur le sous-ensemble `S`. Le gain en pertes est défini comme la réduction par rapport à la base commune,

```text
v(S) = −gᵀx(S) − x(S)ᵀ H x(S)/2,     v(∅) = 0.
```

Pour chaque indice `i`, calculer trois évaluations **signées**. `separate[i]=v({i})`. La règle d'exclusion d'un élément, `loo[i]=v(U)−v(U без i)`. L'évaluation `shapley[i]` est égale à l'accroissement moyen `v(S∪{i})−v(S)` sur toutes les permutations des indices, où `S` est constitué des prédécesseurs de `i`. Cette règle s'applique à la fonction complète de réduction des pertes. Pour calculer sans énumération factorielle, posons `q_i=v({i})`, `h_ij=−x_iᵀ H x_j`. La symétrie donne `v(S)=Σ q_i + Σ_{i<j} h_ij` sur les participants de `S`. Lors de l'exclusion d'un participant, tous ses termes croisés disparaissent. Dans une permutation uniforme, chaque autre participant le précède exactement dans la moitié des cas. C'est pourquoi

```text
loo[i]     = q_i + Σ_{j≠i} h_ij
shapley[i] = q_i + (Σ_{j≠i} h_ij)/2
v(U)       = Σ shapley[i].
```

Ensuite, séparément pour chaque règle, l'évaluation `z` est convertie en crédit `max(0,z−t)` en unités d'amélioration (le coefficient de paiement κ est pris égal à un). On crédite d'abord chaque soumission, puis on additionne les crédits du propriétaire. `gain` — le crédit au propriétaire pour sa soumission initiale et toutes ses soumissions ajoutées après l'ajout, moins le crédit pour son unique soumission avant l'ajout. Le signe positif signifie un gain dû aux soumissions supplémentaires dans cet exemple.

**Format de la réponse.** Les clés `kernel` (chaîne `merge-attribution@1`), `owner`, `scale`, `copies` (l'entier choisi dans l'axe), `noise` (le vecteur choisi d'entiers numérateurs), `baseline`, `with_copies` et `gain`. Chacun des objets `baseline` et `with_copies` contient `value` — la fraction `v(U)` — et les champs `separate`, `loo`, `shapley` — des tableaux de fractions dans l'ordre des indices de soumissions. L'objet `gain` contient une fraction sous chacun des trois noms de règles. Toutes les fractions de sortie sont des chaînes canoniques.

**Arithmétique et limites.** Le dénominateur commun des évaluations intermédiaires est `2s³`. Si `G, A, z_i` sont les numérateurs entiers d'entrée du gradient, du hessien et du pas, le numérateur `q_i` vaut `−2s Gᵀz_i−z_iᵀAz_i`. À la moitié du terme croisé correspond le numérateur entier `−z_iᵀAz_j`. Le numérateur de la déduction vaut `2s²·threshold`. Après ajout, on a jusqu'à 16 soumissions et `|z_ij| ≤ 20 000`. D'où `|z_iᵀAz_j| ≤ 8²·20 000²·10 000 = 2,56·10¹⁴`, la partie linéaire ne dépassant pas `3,2·10¹³` en module. Même la somme de 16 évaluations LOO complètes et des déductions est inférieure à `1,3·10¹⁷` en module. Toutes les multiplications et sommes partielles tiennent dans 64 bits signés. L'implémentation réduit les fractions via `big.Rat`. Temps `O(k d²+k²d)` pour `k ≤ 16`, sans table de sous-ensembles. La mémoire est limitée aux vecteurs d'entrée, à la matrice, à trois évaluations par soumission et au résultat.

**Vérification manuelle.** Avec `v(x)=3x−x²/2`, une seule soumission `x=1` et un seuil nul, l'évaluation initiale vaut `5/2` selon toutes les règles. Après un doublon exact, `v(2)=4`. Les règles donnent, pour chaque soumission, `5/2` séparément, `3/2` par exclusion et `2/1` selon Shapley. Le gain total du propriétaire vaut respectivement `5/2`, `1/2`, `3/2`. Cet exemple suffit à réfuter l'absence de gain pour chacune des trois règles sur toute la famille de tels modèles à seuil nul.

**Portée de la conclusion.** L'ensemble des participants de la comparaison est fixé. Le bruit est donné par un vecteur explicite, le seuil est donné par l'entrée. L'acceptation, la re-sélection de la composition après déduction du seuil, les coûts de soumission, l'apprentissage des paramètres, les effets externes et l'examen empirique sont hors de ce modèle. Le gain numérique concerne la somme des crédits selon la règle choisie. La vérification complète de D1 exige de comparer les utilités de la coalition aussi avec le travail honnête et avec l'inaction. [THREAT_MODEL, §§1.4–1.5](THREAT_MODEL.md) · [ROADMAP, D18 et D25](ROADMAP.md)

## M14. Vérification des formules par énumération finie

Le noyau `verification-enumerations@1` reproduit trois petites expériences. Il permet de vérifier si l'empaquetage conserve la distinction entre les vecteurs autorisés, et combien d'erreurs laissent passer deux types de vérification par échantillonnage. Les données d'entrée, l'ordre d'énumération et les hachages de référence sont publiés dans GPT2, §6.2 et « Code de contrôle pour la première répétition ». La chaîne est définie dans le tableau « Ce qu'il faut confier aux mini-agents », la condition d'un manque dans le corps — au §6.1. Travail GPT2 · [Récapitulatif, §5.3](VERIFICATION_SEARCH.md)

Le seul paramètre `cases` est un tableau de 1 à 4 chaînes distinctes du tableau ci-dessous. `units = len(cases)`. Numérotation à partir de zéro, l'unit `u` calcule toute l'expérience `cases[u]`. La clé `case` du résultat contient cette même chaîne, `kernel` vaut `"verification-enumerations@1"`. Le format des autres champs dépend de l'expérience.

| `case` | Champs du résultat en plus de `case` et `kernel` | Valeurs de contrôle |
|---|---|---|
| `packing-8` | Entiers `total`, `true_accepts`, `false_accepts`, chaîne `verdict_sha256` | 441, 9, 0, `a5c8a8d715fb5293a4dd12753d3483e848f63cb24891a3e584bfdc81954f377c` |
| `packing-4` | Les mêmes champs | 441, 9, 20, `fca92fea5a3148177517b737591e499ed021432078bd9803578a2eaad4074fc9` |
| `chain-8-2` | Entiers `total`, `caught`, `missed` | 224, 56, 168 |
| `field-5` | Entiers `total`, `caught`, `missed` | 25, 20, 5 |

**Empaquetage positionnel.** Prendre la base `B` dans l'étiquette de l'expérience. Énumérer `(x,y,c,d)` par ordre lexicographique croissant, avec `x,y ∈ {−1,0,1}`, `c,d ∈ {−3,…,3}`. La boucle interne fait varier `d`. Le résultat vrai est `(s,t)=(2x−y,−x−y)`. Le critère d'acceptation est la divisibilité de `(c−s)+B(d−t)` par `B²` sur les entiers. En cas de coïncidence `(c,d)=(s,t)`, l'acceptation incrémente `true_accepts`, dans les autres cas d'acceptation — `false_accepts`. Écrire, dans l'ordre d'énumération, exactement 441 octets, chacun valant 1 en cas d'acceptation et 0 en cas de refus. `verdict_sha256` est le SHA-256 de ces octets bruts sous la forme de 64 chiffres hexadécimaux minuscules. Le hachage habituel du résultat de l'unit est calculé séparément de tout le JSON canonique. Pour la vérification manuelle, avec `B=4`, `x=−1`, `y=1`, la réponse vraie `(−3,0)` et la soumission `(1,−1)` donnent une différence nulle.

**Chaîne.** Pour chaque défaut unique `h=0,…,7`, énumérer toutes les paires non ordonnées sans remise comme `0 ≤ i < j < 8`. Incrémenter `total` de 1 pour chaque triplet, `caught` — si `h=i` ou `h=j`. Le nombre de manques est `missed=total−caught`. Pour chaque `h`, il y a 28 paires, dont exactement 7 contiennent `h`.

**Corps.** Énumérer les vecteurs `(x,y)∈{0,…,4}²`, y compris le vecteur nul. L'erreur `(1,−1)` est manquée exactement lorsque `(x−y) mod 5 = 0`. `total` compte tous les vecteurs, `missed` compte les manques, `caught=total−missed`. Cinq paires diagonales donnent cinq manques.

L'unit la plus longue vérifie 441 combinaisons et stocke 441 octets de verdicts pour un seul SHA-256. Les compteurs ne dépassent pas 441, le module de l'expression d'empaquetage ne dépasse pas 46, le plus grand module de division vaut 64. Des entiers signés de 32 bits suffisent. Les résultats concernent les plages indiquées, une erreur fixée et l'énumération complète de variantes équiprobables. La généralisation à un protocole réel exigerait de justifier la distribution des appels et l'indépendance des vérifications.

## Calculs reportés


| Calcul | Ce qui est déjà défini | Quelles données permettront d'obtenir un résultat univoque |
|---|---|---|
| M5. Vagues de falsifications | Pour une falsification bon marché à coût nul, `π=m_s/(L+1)` et `H*=R(1/π−1)`. Par exemple, avec `L=36, m_s=2`, le seuil est de 17,5R | Pour une vague, il faut fixer la distribution conjointe des vérifications et l'évolution du solde lors de plusieurs détections simultanées, y compris le moment du débit et la disponibilité des récompenses de la vague précédente. Avec `π=1/2`, un échantillon commun pour deux erreurs identiques manque les deux avec une probabilité de 1/2, des échantillons indépendants — avec une probabilité de 1/4. L'analogie proposée avec `exit-scam-a` exige aussi de préciser si sa probabilité séparée d'assignation d'une vérification est conservée. (claude1, §1.3, §4.2 et §7.5, point 3) (THREAT_MODEL, §1.8) |
| M7. Économie de la révélation | Pour un paiement fixe R et un paiement de la preuve seulement dans la branche réussie, le revenu d'une tentative `p(R−Pe)−c_view−c_commit` est connu | Pour la limite générale ε, il faut le prix d'une tentative rejetée, la règle de paiement en cas de plusieurs succès et la loi conjointe des issues des candidats à un examen commun. Le nombre de clés ne détermine pas à lui seul ces grandeurs. ODU avec preuve obligatoire de chaque tentative donne un autre budget, et pour T4 le paiement dépend en plus de l'ampleur de l'amélioration. (claude2, §5.3) (critic_claude, §2.4) (critic_gpt, analyse d'ODU) |
| M18. Paiements et récupération | Sont définis l'atomicité de l'acceptation, l'unicité de l'extinction du droit dans l'historique canonique et la liste des scénarios | Pour compter les chemins, il faut une table de transitions lors du changement de branche, un critère de finalité, des règles de récupération en cas de disparition et de retour des données, et une borne finie du nombre de présentations répétées. Différents automates peuvent satisfaire les mêmes invariants et donner des nombres de paiements différents selon les histoires intermédiaires. (gpt1, §1 et §7) (critic_gpt, « Complétude, récupération et prix ») |
