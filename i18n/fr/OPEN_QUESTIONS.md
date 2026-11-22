<!-- translation of docs/OPEN_QUESTIONS.md, source sha256: 399c8aa1465bb599179acb60130b35242d9b6d03a63de6f016bc462e968b83eb -->

# Questions ouvertes

[English](../../docs/OPEN_QUESTIONS.en.md) · [中文](../zh/OPEN_QUESTIONS.md) · [Español](../es/OPEN_QUESTIONS.md) · **Français** · [Deutsch](../de/OPEN_QUESTIONS.md) · [Italiano](../it/OPEN_QUESTIONS.md) · [Русский](../../docs/OPEN_QUESTIONS.md) · [Português](../pt/OPEN_QUESTIONS.md) · [العربية](../ar/OPEN_QUESTIONS.md)

Voici rassemblées les questions sans la résolution desquelles SkyNet ne fonctionnera pas. Elles sont
classées par importance. Pour chacune, il est indiqué ce qui est déjà connu et ce qui est **déjà
rejeté**, afin de ne pas tourner en rond.

Une bonne contribution : une construction concrète, des hypothèses énoncées explicitement, une
attaque contre elle analysée, un coût calculé (en calculs, mémoire, trafic, écritures dans la
blockchain). Encore plus précieuse : une faille trouvée dans le projet actuel avec un scénario
concret.

Une partie des questions peut avancer par le calcul. Ces calculs sont effectués par
l'[agent de recherche](RESEARCH_AGENT.md) sur les ordinateurs de bénévoles ; la liste des tâches et
leur sens sont décrits dans [tasks/README.md](../../tasks/README.md), un résumé des résultats apparaît
dans le dossier `results/`. Actuellement, les tâches se rapportent aux questions Q1, Q5 et Q9.

---

## Q1. Vérification bon marché où la triche est inutile, même en cas de collusion

**La question principale du projet.** Il faut qu'un résultat faux ne rapporte rien et que la
vérification coûte quelques pour cent du travail utile. Objectifs visés : environ 5% pour
l'inférence, environ 20% pour l'apprentissage (non confirmés).

Ce qui est connu :

- La vérification par sondage avec déduction, ou « le paiement du seul résultat vérifié », donne une
  garantie économique jusqu'au seuil de collusion (voir [CURRENT_DESIGN, section 3](CURRENT_DESIGN.md)).
  Elles ne donnent pas zéro lorsque tous les vérificateurs d'une tâche sont en collusion.
- Le zéro en cas de collusion est donné par la vérification de **chaque** résultat payé. Le recalcul
  coûte +100% de travail. Les preuves cryptographiques sont pour l'instant des centaines et des
  milliers de fois plus chères que le travail lui-même.

Mesures du pilote du projet (sur des CPU précis, voir [PILOT_RESULTS](PILOT_RESULTS.md)) :
la preuve RISC Zero d'une ligne de projection de Qwen prenait 22 minutes ; l'exécution d'un lot de
huit lignes dans la zkVM était ~17 700 fois plus longue que le natif ; la reprise complète de
l'arithmétique d'une ligne dans l'EVM coûte 14,1 millions de gas. Le travail publié FlashProve (2026)
rapporte 70–95× le temps GPU pour son profil d'inférence en entiers.

Ce que nous cherchons : un schéma de vérification de l'inférence d'un LLM et d'un pas
d'apprentissage (LoRA ou complet) dont le coût total (prover + verifier + données + blockchain)
tient dans le budget, ou une preuve que, pour cette classe de problèmes, c'est impossible.

## Q2. Concordance du résultat au bit près sur différentes cartes graphiques

Tout le schéma de vérification repose sur la comparaison exacte. En virgule flottante, différents
GPU additionnent dans des ordres différents et donnent des bits différents ; une tolérance ouvre la
porte à une triche « silencieuse » avec un modèle bon marché.

Candidat : un modèle entièrement entier (poids et activations int8, accumulation en int32, échelles
par facteur entier et décalage, non-linéarités entières ou tables). Pour l'apprentissage : une
décomposition en parties de huit bits (schéma d'Ozaki).

Ouvert : la qualité d'un Qwen entier, sa vitesse sur les GPU grand public (AMD, NVIDIA, Intel),
l'apprentissage entier. Il faut des noyaux concrets, une estimation de la perte de qualité, des
travaux connus.

## Q3. Litige avec recalcul dans la blockchain pour le modèle complet

Le litige se réduit par division en deux jusqu'à une seule opération, que le contrat recalcule
lui-même. Cela n'est construit que pour une seule ligne du modèle (contestation réussie ~14 millions
de gas, jeu de 93 transactions ~6 millions de gas). Il faut : une machine entière de référence pour
le modèle complet, une preuve que le jeu ne peut pas être détourné (substituer l'entrée, la longueur,
le chemin), des délais de coup, le coût sous charge, le choix d'une blockchain ou d'un L2.

## Q4. Quoi apprendre et comment ne pas laisser abîmer le modèle

- Comment le réseau choisit lui-même, sans personnes aux droits spéciaux, le plan d'apprentissage.
- Comment se protéger d'un saboteur prêt à perdre des crédits : les faux non détectés influencent
  aussitôt l'apprentissage.
- Comment attraper les portes dérobées de comportement cachées, que l'examen de qualité ne voit pas.
- Comment vérifier les jeux de données du catalogue : sur des données nuisibles, la vérification ne
  répare pas un calcul correct.

Garantie étroite connue : si le modèle de base est figé et que la partie apprenante modifie les
logits d'au plus `b`, alors là où l'écart entre les deux meilleurs jetons dépasse `2b`,
l'empoisonnement ne changera pas la réponse.

## Q5. Capture de la majorité

Le poids mesure le travail, pas l'indépendance. Le propriétaire de mille GPU loués ressemble à mille
participants. Un groupe détenant 3/4 du poids peut changer les règles. Il faut des mécanismes qui
limitent les dégâts d'une majorité honnêtement acquise : un noyau immuable, un seuil par modèle, des
règles de démarrage fermé et des conditions d'ouverture du réseau.

## Q6. Confidentialité des requêtes sur des appareils ordinaires

Le propriétaire de l'appareil peut lire la requête que celui-ci calcule. Le découpage des couches
n'aide pas : les vecteurs cachés se reconstituent. Il faut : des mesures partielles bon marché, des
règles d'accès aux requêtes d'autrui, un litige sur une requête privée sans publication des données
intermédiaires, un paiement que l'on ne peut pas relier au payeur.

## Q7. Disponibilité des données

Le vérificateur dit « on ne m'a pas donné les données », le détenteur dit « je les ai données », le
journal n'a pas vu la transmission. Pour de petites données, la publication dans la blockchain aide ;
pour de grandes (l'état du modèle), il n'y a pas de solution. Aussi : combien de copies indépendantes
sont nécessaires et comment s'assurer qu'elles sont chez des propriétaires différents.

## Q8. Résistance aux blocages et première installation

- Comment un nouveau venu obtient le programme authentique et l'adresse du journal si les principales
  plateformes sont bloquées.
- Quels « lieux de rencontre » publics indépendants utiliser, pour qu'ils ne puissent pas être
  bloqués par une seule décision.
- Comment fonctionner derrière NAT et par relais sans serveurs centraux.

## Q9. Économie

- L'unité de travail et le taux pour l'apprentissage auxquels l'émission de crédits ne les dévalue
  pas jusqu'à zéro.
- La participation est-elle rentable pour les propriétaires de grandes puissances aux prix réels de
  l'électricité.
- L'irrégularité du revenu lorsque seules les tâches vérifiées sont payées.
- L'achat et la vente de crédits contre de l'argent et des cryptomonnaies.

## Q10. Comment un modèle qui apprend tout seul suivra les lois de SkyNet

Le manifeste exige que le modèle ne nuise ni à l'humanité ni à l'être humain, qu'il exécute les
requêtes des gens dans les limites des lois supérieures et qu'il se préserve. Fixer de telles règles
de façon fiable dans un modèle est un problème scientifique non résolu, et dans un réseau sans
modérateurs et avec auto-apprentissage, il l'est encore plus. Il faut : comment les lois entrent dans
l'examen avant le remplacement d'une version du modèle, comment l'apprentissage ne les dilue pas, qui
et comment tranche les cas litigieux sans personnes aux droits spéciaux, comment ne pas transformer
les lois en censure des connaissances utiles.

---

## Ce qui a déjà été rejeté et pourquoi

| Idée | Pourquoi elle ne convient pas |
|---|---|
| Payer le temps de travail ou la puissance déclarée d'après des rapports et des signatures | Un agent et un vérificateur en collusion signeront n'importe quoi ; une carte au repos produit les mêmes messages |
| Des tâches courtes avec vérification de la réponse comme preuve de travail d'une carte graphique précise | La réponse peut être calculée sur l'ordinateur d'un autre ou prise dans le cache : le vérificateur voit des données identiques |
| Un dépôt de garantie ou un droit d'entrée | Interdit par l'exigence R5 |
| Des amendes prélevées sur le compte disponible | Interdit par l'exigence R5 |
| La confiance en un seul vérificateur honnête comme garantie en cas de collusion totale | Remplace l'exigence R4 par une hypothèse |
| Le vote de la majorité sur la justesse du résultat | La majorité peut être capturée ; c'est l'arithmétique qui doit trancher la justesse |

Principe général : **si le cas honnête et le cas fictif donnent au vérificateur des données
identiques, aucun algorithme sur ces données ne les distinguera.** Une nouvelle signature ou une
écriture dans la blockchain n'ajoute rien à de telles données. C'est pourquoi le réseau paie le
résultat vérifié, et non la ressource.
