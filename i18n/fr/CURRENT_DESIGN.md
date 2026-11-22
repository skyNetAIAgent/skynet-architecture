<!-- translation of docs/CURRENT_DESIGN.md, source sha256: a4c162fa040254e708d1d2a816f908416be83f27576a99e7dd1174c85218fced -->

# Projet actuel de l'architecture

[English](../../docs/CURRENT_DESIGN.en.md) · [中文](../zh/CURRENT_DESIGN.md) · [Español](../es/CURRENT_DESIGN.md) · **Français** · [Deutsch](../de/CURRENT_DESIGN.md) · [Italiano](../it/CURRENT_DESIGN.md) · [Русский](../../docs/CURRENT_DESIGN.md) · [Português](../pt/CURRENT_DESIGN.md) · [العربية](../ar/CURRENT_DESIGN.md)

État au 22 novembre 2026. Ceci est un **projet, pas une implémentation**. Aucune
expérience n'a été menée sur ce projet. Les nombres marqués [calcul] sont obtenus par
une formule, pas mesurés.

## Où nous en sommes

L'idée est formulée dans le [manifeste](MANIFESTO.md), les exigences obligatoires sont
approuvées, la base de l'architecture est choisie : un réseau sans coordinateurs, un
journal commun sur une blockchain publique, le paiement du travail vérifié et le
paiement différé au lieu d'une caution. Un petit pilote de confiance a déjà fait
tourner le modèle Qwen sur plusieurs ordinateurs ([résultats du
pilote](../../docs/PILOT_RESULTS.md)).

Le plus difficile reste à venir. Un moyen bon marché de vérifier le travail de sorte
que la fraude soit inutile même en cas de collusion n'a pas encore été trouvé. Un
modèle qui s'améliore lui-même de façon fiable et suit les Lois de SkyNet reste pour
l'instant un objectif de recherche. Les tâches pour les coauteurs se trouvent dans les
[questions ouvertes](OPEN_QUESTIONS.md).

Mentions de statut :

| Mention | Signification |
|---|---|
| **Accepté** | Approuvé dans le projet comme décision |
| **Candidat** | Variante choisie, pas encore approuvée ni construite |
| **Proposition** | Soumise à décision, pas approuvée |
| **Ouvert** | Pas de décision |

## 1. Schéma général (accepté comme base)

Le réseau **n'a pas de coordinateurs** et aucun rôle doté de droits spéciaux. Tous les
participants ont le même programme. Dans les limites des curseurs de ressources, il fait
de lui-même :

| Activité | Ce qu'il fait | Ce qui est payé |
|---|---|---|
| Calcule | Exécute une étape d'apprentissage ou une requête d'utilisateur | Pour le résultat accepté |
| Vérifie | Recalcule le résultat d'autrui si le tirage au sort l'a choisie | Pour la vérification effectuée |
| Surveille | Peut recalculer n'importe quel résultat et le contester | Une part du prélèvement lorsqu'un faux est découvert |
| Stocke et distribue | Garde les données avec lesquelles il travaille | Le destinataire des données paie |
| Écrit dans le journal | Rassemble les enregistrements des participants dans la blockchain | Remboursement des frais |
| Aide à se retrouver | Relaie les connexions pour les appareils derrière un routeur | Compris dans le paiement de la livraison |

**Le journal commun** est un contrat sur une blockchain publique existante, sans clé
d'administrateur. Il conserve les règles et l'empreinte du programme, les comptes
(crédits disponibles, somme en attente, poids du travail vérifié), les empreintes des
résultats remis, les litiges, les votes, le catalogue des modèles et le plan
d'apprentissage. Le journal fonctionne même lorsque tous les nœuds SkyNet sont éteints.
La blockchain **n'est pas choisie** (Ouvert).

**L'aléa public** décide à qui revient la tâche, ce qui est vérifié et qui vérifie. Il
apparaît après que le résultat a été fixé. Candidat : un mélange de la balise drand et
de l'aléa de la blockchain (Candidat, sources non choisies).

## 2. Vie d'une tâche (candidat)

1. La tâche d'apprentissage est dérivée du plan général du réseau ; la requête vient
   d'un utilisateur avec paiement.
2. L'exécutant est désigné par l'aléa parmi les appareils aux ressources adaptées.
3. Le programme calcule et consigne les empreintes des états intermédiaires.
4. L'empreinte du résultat entre dans un paquet, le paquet dans le journal. La
   récompense va dans la somme « en attente ».
5. L'aléa après la remise décide si la tâche est vérifiée.
6. La tâche choisie est recalculée indépendamment par trois participants aléatoires, en
   aveugle.
7. Correspondance bit à bit : confirmé. Différence : litige, tranché par le recalcul de
   l'étape élémentaire litigieuse **dans le journal lui-même**, et non par un vote.
8. La fenêtre de vérification dure trois jours : n'importe qui peut contester le
   résultat.
9. Après la fenêtre, la récompense devient disponible.

**Paiement différé au lieu d'une caution (accepté).** Pour un résultat, le participant
ne répond qu'à hauteur de la somme en attente — ses récompenses des trois derniers
jours. Rien n'est pris à l'avance, les crédits déjà disponibles ne sont jamais prélevés.

## 3. Comment rendre la fraude déficitaire : deux variantes

### Variante A. Vérification par échantillonnage avec prélèvement (spécification actuelle)

La part de vérification `p = 4R / (R + H)`, mais pas moins de 1% ; le prélèvement pour
un résultat incorrect `B = 4R/p − R`, pas plus que la somme en attente `H` (`R` est le
prix de la tâche). Alors chaque faux coûte en moyenne quatre fois le prix de la tâche,
quelle que soit la fréquence de vérification [calcul]. Un faux ne passe que si les trois
vérificateurs sont complices : avec une part de collusion `q`, la probabilité est `q³`.
La fraude est déficitaire tant que le groupe complice détient moins de ~91% du poids des
vérificateurs [calcul].

**Faiblesse.** Un faux non vérifié est payé et reste dans le réseau. C'est un pari qui a
des issues gagnantes pour le fraudeur.

**Calcul préliminaire (22 novembre 2026, un seul ordinateur, non confirmé par d'autres
participants).** L'estimation «91%» est obtenue à partir de la moyenne sur un seul faux.
Elle ne tient pas compte du fait qu'un participant ne peut pas perdre plus que la somme
en attente : il n'y a ni caution ni amende. Pour un participant qui part et soumet des
faux par rafales avant la fin des vérifications, l'énumération exacte des stratégies
dans le modèle `exit-scam-a` donne une borne plus basse [calcul] :

| Règles | Partir avec des faux devient rentable à partir de la part de collusion |
|---|---|
| Petites tâches identiques, 399 prix en attente, une seule rafale | 89,2% |
| Petites tâches identiques, 1200 prix en attente, une seule rafale | 90,8% |
| Petites tâches identiques, trois rafales, règle « pas plus d'un tiers en cours » | 89,0% |
| Tâches de taille quelconque, trois rafales, règle « pas plus d'un tiers » | 87,5% |
| Tâches de taille quelconque, deux rafales jusqu'à 100 tâches, sans la règle « pas plus d'un tiers » | 80% |
| Sans collusion, tâches de taille quelconque, deux rafales (92 millions de stratégies) | non rentable |

Sans la règle « pas plus d'un tiers », les récompenses non vérifiées de la première
rafale augmentent la somme en attente et la taille admissible des tâches de la seconde,
c'est pourquoi cette règle est obligatoire. Le modèle est consigné au début du fichier du
noyau [exit_scam_a.py](../../agent/skynet_agent/kernels/exit_scam_a.py) et reproduit les
nombres de l'exemple de la spécification (« environ 78, 107 et 17 »). Les tâches sont
décrites dans [tasks/README.md](../../tasks/README.md), la première exécution dans
[results/FIRST_RUN.md](../../results/FIRST_RUN.md). Ces nombres deviendront un résultat du
projet après confirmation indépendante par d'autres participants.

### Variante B. Le réseau ne paie que ce qui est vérifié (proposition, en attente de décision)

La tâche devient un billet de loterie. Le tirage au sort choisit une part `p` des tâches
(par exemple, 1%), seules celles-ci sont vérifiées et **seules celles-ci sont payées,
mais `1/p` fois plus cher**. En moyenne, un participant honnête reçoit autant, et un faux
non sélectionné ne rapporte **rien**.

- Sans collusion, un faux rapporte exactement zéro.
- En cas de collusion, le paiement frauduleux ne dépasse pas `q^k` par tâche vérifiée
  (k est le nombre de vérificateurs) : 0,1% pour q = 10% et k = 3 [calcul]. Chaque
  tentative ratée brûle toute la somme en attente.
- Failles trouvées : un débutant complice reçoit en moyenne `q^k` fois le prix par
  tentative et ne perd rien ; une « campagne de sortie » composée de nombreux faux d'un
  coup. Des correctifs sont proposés : des places d'apprenti financées par un budget
  limité, l'annulation de tous les gains non arrivés à maturité de la clé lorsqu'un faux
  est attrapé, un plafond des tâches ouvertes.
- Le coût : le revenu devient irrégulier. Pour un appareil faible, environ ±13% par mois
  [calcul].

Les deux schémas exigent une **concordance du résultat bit à bit** sur des appareils
différents. Voie proposée : une arithmétique entière (int8/int32) du modèle, où l'ordre
des additions n'influence pas le résultat. **La vitesse et la qualité du Qwen en
arithmétique entière ne sont pas mesurées** ; un profil int8 reproductible connu était
5,2 fois plus lent que le profil ordinaire (Ouvert).

Litige bon marché : division du calcul en deux jusqu'à une seule opération, puis
vérification de la multiplication de matrices par un vecteur aléatoire (algorithme de
Freivalds). Économie d'environ 100 fois sur le nombre de multiplications pour les grandes
matrices, 2,6 fois sur LoRA, aucun gain pour la génération jeton par jeton [calcul]
(Candidat).

## 4. Poids et nouveaux participants (candidat)

- **Le poids** est la somme des prix des résultats ayant passé la vérification sur
  30 jours. Il ne peut pas être acheté, transféré ni accumulé. Le nombre de comptes ne
  donne rien : les chances et les votes sont proportionnels au poids.
- **Le débutant** fait d'abord des re-vérifications « d'apprenti » des tâches d'autrui :
  sa réponse ne décide rien et n'est payée que si elle correspond au résultat accepté.
  Ensuite, il reçoit des tâches qui sont toujours vérifiées, puis de moins en moins
  souvent.
- Le poids est calculé séparément pour chaque modèle. Pour un modèle sur lequel peu de
  gens travaillent, le cercle des vérificateurs est petit et plus facile à capturer
  (Ouvert).

## 5. Se retrouver et reprendre (candidat)

| Où | Ce qui survit à un arrêt complet |
|---|---|
| Le journal dans la blockchain publique | Les règles, les comptes, le poids, l'empreinte du modèle, le plan d'apprentissage, les litiges, les adresses des nœuds qui ont écrit |
| Les disques des participants et les miroirs publics | Les poids du modèle, l'état de l'apprentissage, les données ; toute copie est comparée à l'empreinte du journal |
| La distribution du programme | L'identifiant du réseau, l'adresse du journal, la liste initiale des points de rendez-vous |

Trois façons indépendantes de se retrouver, une seule suffit : des annonces signées sur
des plateformes externes (« points de rendez-vous »), des réseaux ouverts de découverte
de nœuds (par exemple, la DHT de libp2p), les adresses dans le journal lui-même. La
fenêtre de vérification ne s'écoule pas tant que le réseau est arrêté, sinon un faux
pourrait être soumis juste avant l'arrêt.

Points faibles : l'authenticité de la première installation (le débutant apprend
l'adresse du journal de l'extérieur) ; le blocage complet de toutes les voies à la fois ;
la confiance envers deux des trois fournisseurs du point de contrôle après une longue
période d'arrêt.

## 6. Requêtes et vie privée (candidat)

La requête est chiffrée pour l'appareil de l'exécutant et passe directement ou par un
relais sous pseudonyme. Le journal ne contient que des empreintes. Environ 1% des
requêtes sont vues en plus par trois vérificateurs.

**Réserve honnête.** Sur un ordinateur ordinaire, le propriétaire de l'appareil avec un
programme modifié peut lire la requête que celui-ci calcule. Le calcul entièrement
homomorphe pour de tels modèles est des milliers de fois plus lent. D'où deux modes : le
mode ordinaire (bon marché) et le mode protégé (uniquement sur du matériel qui prouve que
le propriétaire ne regardera pas à l'intérieur, plus cher, fondé sur la confiance envers
le fabricant).

## 7. Apprentissage et choix du plan (proposition)

Un catalogue ouvert de modèles et de jeux de données sous licences libres, fixés par des
empreintes. Le réseau compose selon la règle des variantes d'apprentissage, donne à
chacune un essai, répartit la puissance libre selon les résultats et le vote au poids.
Une nouvelle version du modèle ne remplace l'ancienne que si elle a mieux réussi
l'examen, dont les épreuves sont choisies par l'aléa après la fixation des poids. La
contribution d'une seule tâche à la mise à jour des poids est limitée ; la partie
« légère » de l'étape (l'addition des contributions) est toujours recalculée.

Un modèle qui **s'améliore lui-même de façon fiable et sans fin** est un objectif de
recherche, pas une technologie prête. Une première étape réaliste : le réapprentissage
automatique et la sélection par l'examen.

## 8. Changement des règles (candidat)

Les règles ne sont modifiées que par une nouvelle version du programme, acceptée par les
3/4 de **tout** le poids après un vote d'au moins 14 jours et un délai annoncé de
30 jours. Le frein général (plus de la moitié du poids) ne peut qu'arrêter une nouvelle
version du modèle. Proposition : un noyau de vérification immuable, qu'aucun vote ne peut
annuler (en attente de décision).

## 9. Résumé des attaques

Sur 60 façons de frauder analysées : 18 sont fermées, 6 sont déficitaires, 19 sont
limitées, 16 sont ouvertes (pour la variante A). Principaux points ouverts :

1. **Majorité au poids.** Un groupe détenant les 3/4 du poids peut changer les règles ;
   dans un petit réseau, une telle part peut être accumulée par un travail honnête sur de
   la puissance louée. C'est pourquoi le démarrage est fermé, sur des crédits
   d'apprentissage.
2. **Fondations non construites.** La concordance bit à bit et le recalcul du litige dans
   le journal pour le modèle complet ne sont pas construits.
3. **Un saboteur qui ne cherche aucun profit.** Il peut dégrader l'apprentissage dans la
   limite de sa part de travail ; les portes dérobées cachées échappent à l'examen.
4. **Les requêtes d'autrui** en mode ordinaire et lors des litiges.
5. **Disponibilité des données.** Le litige « a-t-il fourni ou non les grosses données »
   ne peut pas être tranché.
6. **Entrée dans le réseau.** La file d'attente pour les places d'apprenti et
   l'authenticité de la première installation.

Détails et tâches pour les coauteurs : voir [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md).
