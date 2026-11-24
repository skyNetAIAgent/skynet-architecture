<!-- translation of docs/EXPERIMENT_D5.md, source sha256: 8c74b11b335ebd7a0797e908c40ed9e4c2b98395835bb319e3272b464224875d -->

# Expérience D5 : Qwen3.5-4B en arithmétique entière

[English](../../docs/EXPERIMENT_D5.en.md) · [中文](../zh/EXPERIMENT_D5.md) · [Español](../es/EXPERIMENT_D5.md) · **Français** · [Deutsch](../de/EXPERIMENT_D5.md) · [Italiano](../it/EXPERIMENT_D5.md) · [Русский](../../docs/EXPERIMENT_D5.md) · [Português](../pt/EXPERIMENT_D5.md) · [العربية](../ar/EXPERIMENT_D5.md)

État au 24 novembre 2026 : **plan de l'expérience, il n'y a pas encore de mesures.** L'expérience est autorisée par la décision D5
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
