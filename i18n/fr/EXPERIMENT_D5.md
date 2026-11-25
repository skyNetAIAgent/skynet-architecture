<!-- translation of docs/EXPERIMENT_D5.md, source sha256: a043f1ab15bdb60165b5430029b58928dbd99d6807c243175827dd51c9421af4 -->

# Expérience D5 : Qwen3.5-4B en arithmétique entière

[English](../../docs/EXPERIMENT_D5.en.md) · [中文](../zh/EXPERIMENT_D5.md) · [Español](../es/EXPERIMENT_D5.md) · **Français** · [Deutsch](../de/EXPERIMENT_D5.md) · [Italiano](../it/EXPERIMENT_D5.md) · [Русский](../../docs/EXPERIMENT_D5.md) · [Português](../pt/EXPERIMENT_D5.md) · [العربية](../ar/EXPERIMENT_D5.md)

État au 25 novembre 2026 : **les bits concordent sur six exécutants, y compris en contexte long ;
O3 et O4 ont été mesurés et n'ont pas satisfait aux seuils ; la qualité (O5) n'est pas encore mesurée** (section 7). L'expérience est autorisée par la décision D5
([ROADMAP](ROADMAP.md), section 3) et fait partie de l'étape 5 de la feuille de route. Elle vérifie la principale hypothèse non mesurée
du meilleur candidat de l'étape 4 — la vérification de la réponse par le payeur lui-même (PPS,
[VERIFICATION_SEARCH](VERIFICATION_SEARCH.md), sections 3.2 et 5.2).

## 1. Ce qui est vérifié

Le payeur qui dispose du modèle doit, en une seule passe, recalculer la requête et la réponse obtenue
et obtenir **les mêmes bits** que l'exécutant lors de la génération. Cela n'est possible que si toute
l'arithmétique du modèle est définie en nombres entiers avec un arrondi fixé : la somme d'entiers ne dépend pas
de l'ordre de l'addition tant qu'il n'y a pas de débordement. L'expérience répond à cinq questions ; les critères
de réfutation sont fixés avant le lancement :

| Expérience | Question | Ce qui la réfute |
|---|---|---|
| O1 | Les bits concordent-ils sur différentes cartes graphiques et sur le processeur ? | Au moins un bit différent des logits, du jeton choisi, de la raison d'arrêt ou des hachages de contrôle pour une même entrée. Avant la conclusion — la recherche de la première divergence et une répétition sur l'entrée la plus courte. La conclusion ne concerne que les appareils testés et la version de l'implémentation |
| O2 | Les bits concordent-ils entre la génération jeton par jeton et une passe sur la séquence prête sur une même carte ? | Tout bit différent, y compris le hachage de l'état récurrent des couches Gated DeltaNet aux points de contrôle |
| O3 | Combien coûte la vérification de la réponse par rapport à sa génération ? | La médiane de la part `ρ(1)` est supérieure à 5 % pour au moins une des quatre paires de longueurs de requête et de réponse nommées à l'avance avec un lot de 1. Les lots de 8 et de 32 sont mesurés séparément |
| O4 | De combien le profil entier est-il plus lent que le profil habituel en 8 bits sur la même carte ? | La médiane du ralentissement est supérieure à 1,25 fois dans une cellule comparable (seuil diagnostique : ce sont O3 et O5 qui décident) |
| O5 | Combien de qualité est perdue ? | Une perte de précision supérieure à 3 points de pourcentage sur 320 tâches choisies à l'avance (64 de chacune des quatre sections MMLU et du MGSM russe) par rapport au profil habituel en 8 bits du même modèle |

Les 1,2–3,8 % calculés de l'étape 4 ne sont pas considérés comme un résultat de O3 : seule cette expérience
les confirme ou les réfute.

## 2. Modèle et matériel

- **Modèle :** dépôt officiel Qwen/Qwen3.5-4B sur Hugging Face, révision fixée
  `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`. Deux fichiers de poids de 5 329 398 688 et 3 990 429 408
  octets, au total environ 9,3 Go. Après le téléchargement, les SHA-256 de l'inventaire du dépôt sont vérifiés.
- **Architecture** (d'après le `config.json` publié) : 32 blocs, vecteur caché 2560, MLP 9216.
  Un bloc sur quatre (indices 3, 7, …, 31) est une attention complète : 16 têtes de requête, 4 têtes
  de clés et de valeurs, taille de tête 256, gate de sortie, rotation des 64 premières coordonnées. Les autres
  24 blocs sont des Gated DeltaNet : état récurrent 32 × 128 × 128 par bloc, convolution causale
  de profondeur 4. Vocabulaire 248 320, matrices d'entrée et de sortie communes. Le « canon INT » de transformateur
  habituel de l'étape 4 ne lui suffit pas ; le profil est défini à nouveau (section 3).
- **Appareils :** RTX 2060 6 Go (Turing) sur le Linux domestique du superviseur ; RTX 4070 Laptop
  8 Go (Ada) sur l'ordinateur du propriétaire ; le processeur comme troisième exécutant indépendant. Avec accord —
  les appareils d'autres participants via un mini-agent.
- **Mémoire** [calcul] : les poids principaux en 8 bits — 4010 MiB. Avec un lot de 1 et une longueur jusqu'à 3000 jetons,
  tout tient dans 6 Go ; un lot de 32 à une longueur de 3000 exige environ 7064 MiB avant même les tampons de travail
  et n'est possible sur la RTX 2060 qu'avec un transfert de l'historique dans la mémoire vive.

## 3. Profil entier

Le profil reçoit un nom et une version distincts et est gelé avant O1–O5. La base est le graphe numérique
du projet ChatGPT avec les corrections des deux critiques :

1. **Poids et activations.** Poids en 8 bits ligne par ligne, l'échelle de la ligne est un nombre binaire exact.
   Activations en 16 bits à virgule fixe (1024 = unité). Un seul arrondi pour toutes les
   opérations : au plus proche, la moitié vers le pair, modulo avec restitution du signe.
2. **Normalisations et non-linéarités** (RMSNorm, L2, SiLU, sigmoïde, softplus, exponentielle) — formules
   entières avec racine carrée entière et tables. Les tables sont construites hors du programme avec un arrondi
   correct prouvé (MPFR) et publiées avec leur SHA-256.
3. **Attention complète.** Scores, exponentielle par table, parts en 16 bits. Le critique ChatGPT a trouvé
   dans le projet initial une erreur : à valeurs égales, l'ajout d'une clé supplémentaire identique
   changeait la sortie de 1365 à 683. Correction : diviser la somme pondérée par la somme des parts arrondies
   elles-mêmes ; alors une valeur constante est conservée exactement.
4. **Gated DeltaNet.** Décroissance, correction et mise à jour de l'état — cinq affectations entières
   par jeton dans un ordre chronologique canonique. La formule du projet DeepSeek
   décrivait une autre récurrence et est rejetée. La forme « par blocs » accélérée n'est admise que
   si elle reproduit les mêmes bits à chaque jeton.
5. **Choix du jeton.** Maximum sur le couple (score, −numéro) sur tout le vocabulaire, de façon gloutonne. Un mode séparé —
   le Gumbel-max canonique avec un pseudo-aléa HMAC-SHA256 à partir de la graine de la requête (D22).
   L'arrêt suit la première raison : EOS ou la limite.
6. **Bornes de débordement** définies pour chaque accumulateur ; là où 32 bits ne suffisent pas, 64 sont utilisés.
   Des tests séparés vérifient les valeurs extrêmes.

Tous les points ambigus (« bifurcations ») sont tranchés avant le premier lancement par la lecture du source du modèle
de la version fixée de Transformers ; le hachage de ce source entre dans le manifeste du profil.

## 4. Ordre des travaux

1. **P0, préparation (2–4 jours).** Téléchargement et vérification du modèle ; inventaire de tous les tenseurs ; résolution
   des ambiguïtés d'après le source ; tables ; vecteurs de contrôle avec des valeurs calculées à la main.
2. **Étape réduite (1–1,5 semaine).** Référence sur processeur pour tout le modèle sur des entrées courtes ;
   comparaison avec le calcul habituel en virgule flottante (seulement pour attraper une erreur d'importation,
   pas pour O1/O2). Version simple pour la carte graphique sans cœurs tensoriels. Réponses de O2 sur une même carte
   et de O1 « processeur contre RTX 2060 » sur un contexte court. Ensuite le même lot sur la RTX 4070
   Laptop — première réponse de O1 pour deux cartes graphiques différentes.
3. **Étape complète (3–4 semaines).** Multiplications rapides en 8 bits, noyau fusionné de la récurrence DeltaNet,
   lots 1/8/32, expériences O3, O4, O5, répétition sur un second appareil.

Tout le travail se fait dans un répertoire séparé sur le Linux domestique, avec un environnement Python
propre (CuPy avec les bibliothèques CUDA 12 des paquets pip, sans installation système). Les services en activité
et les répertoires des autres expériences ne sont pas touchés. Estimation globale — 4–6 semaines de travail d'un seul
développeur ; les principaux risques sont le coût de la récurrence DeltaNet (O3 le montrera), les ambiguïtés
avant P0 et la prise en charge de Qwen3.5 dans les moteurs habituels pour O4/O5.

## 5. Ce qui sera publié

Pour chaque lancement : le manifeste du profil et des versions, les entrées, les hachages des logits et des états par couche,
les temps bruts et les conditions de mesure, les défaillances initiales avec leurs corrections. La concordance des bits
ne concerne que les appareils et les versions testés. Le résultat de chaque expérience est inscrit dans la feuille de route
(étape 5) et dans ce document ; une expérience est considérée comme terminée quand un second participant l'a répétée.

## 6. Qui a fait quoi

- **Projets de l'expérience :** deux projets indépendants — ChatGPT et DeepSeek.
- **Critique croisée :** ChatGPT a analysé les deux projets, DeepSeek a analysé les deux projets ;
  recalculs de la mémoire et des bornes, vérification de la courte récurrence et des corrections d'attention sur de petites énumérations.
- **Synthèse et décisions sur le plan :** Claude.
- **Préparation, profils v1 et v2, référence sur processeur et version pour la carte graphique :** ChatGPT.
- **Vérifications indépendantes :** DeepSeek — importation du modèle avec le forward officiel, absence d'ambiguïté
  et bornes de débordement du profil v2.
- **Lancements sur cartes graphiques et vérification des résultats :** Claude (la carte graphique n'est pas accessible
  depuis le bac à sable des modèles).

## 7. Résultats

**24 novembre 2026, entrées courtes.** Entrées : deux historiques de 8 + 8 jetons et six textes courts
(russe, anglais, chinois, arithmétique, code, recette), profondeur 4 et 32 blocs ; lot de 1.

- **Importation du modèle.** Le calcul habituel en virgule flottante, écrit d'après le source, a coïncidé
  avec le forward officiel de Transformers 5.24.0 : le même jeton choisi dans 130 positions sur 130,
  un écart des logits ne dépassant pas 3,6·10⁻⁵ (vérifié par ChatGPT et indépendamment par DeepSeek).
- **Profil v1 rejeté.** Il était reproductible au bit près, mais l'échelle 1/1024 était trop grossière :
  la sortie de la récurrence DeltaNet était presque entièrement arrondie à zéro, la concordance du jeton choisi
  avec le modèle — 5 sur 8, la corrélation des logits environ 0,8.
- **Profil v2** (activations avec exposant binaire par vecteur et mantisse de 16 bits, reste
  et état de la récurrence avec un pas de 2⁻²⁰, clés et valeurs d'attention en 32 bits) : le même jeton que
  le modèle officiel dans 90 positions sur 90, corrélation moyenne des logits 0,9996, minimale
  0,998. L'état et le cache occupent 238 MiB à 3000 positions contre 95 pour v1 ; le nombre de multiplications
  par jeton est le même — 4,2 milliards.
- **O2 (un seul appareil).** La génération jeton par jeton et une passe sur la réponse prête avec un découpage
  en 1, 3 et 8 positions donnent les mêmes bits de tous les logits, des jetons choisis et des hachages d'états.
- **O1 (appareils différents).** Processeur (Xeon, Linux), RTX 2060 (Turing, Linux, CuPy) et RTX 4070
  Laptop (Ada, Windows, CuPy) : 88 comparaisons sur chaque carte, 242 360 320 logits par carte,
  976 jetons choisis et 37 152 hachages d'états — **aucune différence**.
- **25 novembre 2026, une autre architecture et un autre langage de noyaux.** Troisième implémentation en OpenCL
  (ChatGPT), mêmes entrées et 88 comparaisons : processeur via pocl, RTX 2060 via NVIDIA OpenCL
  et **AMD Radeon RX 580** (Polaris, Mesa rusticl, Linux) — de nouveau aucune différence dans aucun des
  242 360 320 logits, 976 jetons et 37 152 hachages. Au total, les mêmes bits sur six exécutants :
  processeur (NumPy), processeur (pocl), RTX 2060 (CUDA et OpenCL), RTX 4070 Laptop (CUDA),
  RX 580 (OpenCL).

**25 novembre 2026, contexte long.** Requête + réponse : 512 + 64, 2048 + 256 et 4096 + 64 jetons
(textes réels), les 32 blocs ; ont été comparés les hachages des logits de chaque position, les jetons
choisis et les hachages des états toutes les 64 positions. La RTX 2060 (CUDA), la RTX 2060 (OpenCL) et la RTX 4070 Laptop
(CUDA) ont concordé entre elles dans les trois cas, et sur chaque carte la génération jeton par jeton a concordé
avec une passe sur la réponse prête par tranches de 64 et 512 positions. Pour 512 + 64, la référence indépendante
sur processeur et la RX 580 ont donné le même résultat. Sur la RX 580, la génération jeton par jeton a concordé avec les autres cartes
pour 2048 + 256 et 4096 + 64 également, mais la passe sur la réponse prête sur des entrées longues est interrompue
par le pilote (réinitialisation d'une tâche de carte graphique trop longue) ; il faut découper le noyau d'attention en parties.
C'est une limite d'exécution, et non une divergence de bits.

**25 novembre 2026, noyaux rapides, O3 et O4.** ChatGPT a écrit des noyaux rapides pour NVIDIA
(DP4A pour les multiplications de poids en 8 bits par des activations en 16 bits, multiplications par tuiles pour la passe
sur la réponse prête, récurrence DeltaNet fusionnée). Sur la RTX 2060 et la RTX 4070 Laptop, chacune des quatre étapes
d'accélération a donné les mêmes bits : 88 comparaisons courtes sur 88 et le cas long 512 + 64 contre la référence
sur processeur.

O3 — le temps de vérification de la réponse en une seule passe, en fraction du temps de génération, médiane de neuf paires
après deux échauffements :

| Requête / réponse | RTX 2060, lot 1 | RTX 4070 Laptop, lot 1 | RTX 2060, lot 8 | RTX 4070 Laptop, lot 8 |
|---|---:|---:|---:|---:|
| 128 / 32 | 0,40 | 0,24 | 0,64 | 0,46 |
| 128 / 128 | 0,21 | 0,11 | 0,42 | 0,26 |
| 500 / 500 | 0,21 | 0,10 | 0,43 | 0,28 |
| 2000 / 1000 | 0,31 | 0,15 | ne tenait pas | 0,48 |

Avec un lot de 32 sur la RTX 4070 Laptop — 0,59–0,84 ; sur la RTX 2060, cela ne tenait pas en mémoire.
**Le seuil de 5 % est réfuté** pour cette implémentation sur les deux cartes (le critère avait été consigné avant l'expérience).
L'ancienne estimation de 1,2–3,8 % supposait des activations en 8 bits et des cœurs tensoriels ; le profil v2 exige
des activations en 16 bits, d'où environ deux fois plus de multiplications.

O4 — sur la RTX 2060, le profil entier est plus lent que llama.cpp Q8_0 (b11960, même modèle)
d'un facteur 1,52–1,78 avec un lot de 1 et de 2,47–2,79 avec un lot de 8. Le seuil de 1,25 n'est pas atteint.
Ce qu'il en découle pour le choix de la vérification a été examiné par le conseil des modèles :
[STRATEGY_SEARCH](STRATEGY_SEARCH.md).

Limites : entrées courtes et lot de 1 ; noyaux entiers simples sans blocs tensoriels ; le temps
de ces exécutions ne constitue pas une mesure de O3 et O4. Ensuite — le contexte long jusqu'à des milliers de jetons,
des noyaux rapides avec la même arithmétique, puis O3–O5.
