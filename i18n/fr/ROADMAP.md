<!-- translation of docs/ROADMAP.md, source sha256: 6f12143662929b719966cb992e7a2cc7227ba4d97d49e226216546d18695a246 -->

# Feuille de route : protection contre la fraude

[English](../../docs/ROADMAP.en.md) · [中文](../zh/ROADMAP.md) · [Español](../es/ROADMAP.md) · **Français** · [Deutsch](../de/ROADMAP.md) · [Italiano](../it/ROADMAP.md) · [Русский](../../docs/ROADMAP.md) · [Português](../pt/ROADMAP.md) · [العربية](../ar/ROADMAP.md)

État au 23 novembre 2026 (mis à jour après la version v0.2.2). Ceci est un **plan de travail, pas une promesse de résultat**. La marque `[x]`
signifie « fait, et c'est vérifiable dans le dépôt ou dans les enregistrements du réseau » ; `[ ]` signifie
« pas fait ». Les nombres marqués [calcul] sont obtenus par une formule, pas mesurés. La feuille de route
est mise à jour à chaque changement de statut.

## 1. Objectif et critères d'achèvement

**Objectif de l'étape actuelle du projet :** trouver un moyen de vérifier l'honnêteté qui satisfasse en
même temps les exigences obligatoires ([REQUIREMENTS](REQUIREMENTS.md)) :

- il est impossible de tromper le réseau : la fraude est inutile ou déficitaire, y compris pour un débutant
  avec un compte vide, en cas de collusion et avec de nombreuses clés ;
- aucun paiement à l'avance : ni cautions, ni cotisations, ni amendes ;
- la participation est rentable, la vérification de l'honnêteté est bon marché. Repères pour le surcoût de la
  vérification : environ 5% du travail pour les requêtes au modèle et environ 20% pour l'apprentissage
  (non confirmés).

**Le travail est considéré comme terminé lorsque tout ce qui suit est présent :**

1. **Il est écrit ce qui est exactement garanti** (décision D1) : pour le résultat d'une requête, une étape
   d'apprentissage, un paiement et l'historique ; pour un compte vide, un nombre quelconque de clés, le
   départ et la collusion totale des vérificateurs de la tâche. L'exigence admet « la fraude est inutile » ;
   il n'est pas obligatoire de prouver une perte stricte à chaque tentative.
2. **Pour chaque attaque du tableau des attaques, il est écrit la règle par laquelle un nœud rejette la
   fausse déclaration, et à partir de quelles données il le fait.** Sont indiqués séparément la probabilité
   de fausse acceptation, le dommage au réseau et le gain net de la coalition par rapport à l'inaction et
   par rapport au travail honnête. Contre-exemple de la règle : un cas honnête et un cas faux dans lesquels
   le nœud voit des données identiques. L'échantillonnage, la faible probabilité d'erreur et « il existe un
   observateur honnête » sont consignés comme hypothèses.
3. **Le coût complet de la vérification est calculé** par rapport à la même tâche sans vérification : le
   travail de l'exécutant et des vérificateurs, la mémoire, le trafic, le stockage, l'écriture dans le
   journal, les litiges, les reprises après incident. Sont déduits le revenu net d'un participant avec de
   grandes ressources à une électricité chère, le supplément d'un participant avec un matériel faible et le
   coût pour un consommateur sans matériel. L'écriture et le litige sont accessibles depuis un compte à
   zéro ; on ne peut perdre que les récompenses non arrivées à maturité.
4. **Les calculs sont reproductibles :** la version des règles et du noyau, les entrées, les bornes de
   l'énumération, la sortie et l'empreinte sont jointes ; le calcul est répété sur un second appareil. La
   répétition confirme le calcul, mais pas la justesse du modèle lui-même : celle-ci est justifiée séparément.
5. **Est mesuré ce qui ne peut pas être établi par le raisonnement :** la concordance du résultat bit à bit
   sur différentes cartes graphiques, la vitesse et la qualité du modèle en arithmétique entière, le coût du
   litige. Les profils, les métriques et les seuils sont fixés avant la mesure.
6. **Les autres exigences ne sont pas violées :** le réseau reste opérationnel même si l’un des nœuds ou l’une des plateformes est indisponible et, après un arrêt complet, ses nœuds peuvent se retrouver, les fondements des crédits sont reconstituables ; en
   cas de partition du réseau, le paiement litigieux attend l'historique commun, la reprise n'est pas payée
   deux fois.

Une issue honnête est aussi un résultat : si pour une certaine classe de tâches la vérification bon marché
est impossible, cela est montré par une preuve avec la classe de tâches nommée et les données nommées du
vérificateur, et non par l'absence d'idées.

## 2. Où nous en sommes

| Quoi | Statut | Où c'est consigné |
|---|---|---|
| À partir des signatures et des réponses courtes, on ne peut pas établir quel appareil a travaillé ni pendant combien de temps : un intermédiaire, un cache et une carte au repos donnent les mêmes données | Établi par le raisonnement | [OPEN_QUESTIONS](OPEN_QUESTIONS.md), « Ce qui a déjà été écarté » |
| Le réseau paie pour le résultat vérifiable, et non pour la ressource | Accepté (D2) ; l'unité de résultat et la condition d'acceptation ne sont pas encore définies | [CURRENT_DESIGN](CURRENT_DESIGN.md), section 1 |
| Paiement différé au lieu d'une caution : le participant ne répond qu'à hauteur de la somme en attente | Accepté | CURRENT_DESIGN, section 2 |
| Variante A : vérification par échantillonnage avec annulation | Spécification actuelle | CURRENT_DESIGN, section 3 |
| Variante B : le réseau ne paie que les tâches vérifiées, `1/p` fois plus cher | Candidat principal ; choix après comparaison (D3) | CURRENT_DESIGN, section 3 |
| Concordance du résultat bit à bit par l'arithmétique entière | Candidat, pas mesuré | OPEN_QUESTIONS, Q2 |
| Litige par division en deux avec recalcul d'une étape dans le journal | Mesuré pour une ligne du modèle ; pas construit pour le modèle complet | [PILOT_RESULTS](PILOT_RESULTS.md) |
| Utilisation d’un vecteur aléatoire pour vérifier le produit de deux matrices dans le litige | Candidat, il n'existe qu'une estimation calculée | CURRENT_DESIGN, section 3 |
| Noyau de vérification immuable, qu'aucun vote ne peut annuler | Accepté (D4) | CURRENT_DESIGN, section 8 |

**Ce que l'on sait de la force de la protection.**

- Variante A, sans collusion : dans la famille énumérée (deux rafales de faux, 92 millions de stratégies),
  soumettre des résultats falsifiés puis quitter le réseau ne rapporte pas plus qu'un départ ordinaire [calcul].
- Variante A, collusion : les premiers points de la grille où soumettre des résultats falsifiés puis quitter le réseau devient rentable — une
  part de collusion de 87,5% (tâches de taille quelconque) et 89,0% (tâches identiques) avec la règle « pas
  plus d'un tiers en cours », 80% sans cette règle. Pas de la grille 0,002–0,02 ; d'autres familles de
  stratégies n'ont pas été énumérées [calcul, [FIRST_RUN](FIRST_RUN.md)].
- Variante B, sans collusion : avec une comparaison exacte, un faux n'est pas payé.
- Variante B, collusion : `q` est la fraction du poids total des vérificateurs de ce modèle que détient la coalition.
  Un faux n'est payé que si la tâche est choisie et que tous les `k` vérificateurs sont en collusion. Le
  paiement moyen pour un faux soumis est égal à `R·q^k` (`R` est le prix de la tâche) et ne dépend pas de
  `p` [calcul]. Pour `q = 1`, c'est le prix complet. Sur le compte vide d'un débutant, il n'y a rien à débiter.
- L'absence de paiement indu en cas de collusion totale des vérificateurs n'est démontrée ni pour la variante A
  ni pour la variante B. Elle s'obtient en vérifiant chaque résultat rémunéré à partir de données que tout
  nœud vérifie lui-même. Le recalcul complet ajoute environ 100% de travail. Mesures du pilote : la preuve
  RISC Zero pour une ligne du modèle a mis 22 min 10 s à être construite ; l'exécution de huit lignes dans
  la zkVM a duré environ 17 700 fois plus longtemps que la normale, sans construction de preuve. Ces mesures
  ne donnent pas de borne inférieure générale du coût.
- Irrégularité du revenu dans la variante B : à 6 000 tâches par mois, une vérification d'une tâche sur 100
  et un coût de revient de 95% du prix, la probabilité d'un mois déficitaire est de 33,10% [calcul, FIRST_RUN].
- La première exécution des calculs (702 portions) a été faite sur un seul ordinateur. Au 23 novembre, un
  second appareil avait recalculé les 702 portions ; toutes ont coïncidé. Ses enregistrements sont signés
  par la clé `46000d30…` et sont accessibles sur un nœud complet. Les deux appareils appartiennent aux
  mainteneurs, ce n'est donc pas encore une confirmation par un participant indépendant.

**Ce qui n'est pas résolu.**

1. Un débutant avec un compte vide en collusion (variante B) : gain moyen `R·q^k` par tentative, aucune perte.
2. « Honnête longtemps, puis une grosse fraude et le départ » : la perte est limitée à la somme en attente,
   le gain croît avec le nombre de faux. Des correctifs pour la variante B sont proposés, pas calculés.
3. Le flux de déchets depuis des clés gratuites. Une clé ne coûte rien ; le paiement par le travail du
   processeur place les appareils faibles dans une situation pire.
4. Un résultat utilisé avant la vérification. La réponse a déjà été lue par l'utilisateur, l'étape est déjà
   entrée dans l'apprentissage ; la limitation des paiements ne corrige pas cela. Dans la variante B, cela
   vaut aussi pour les tâches non choisies.
5. Les tâches d'apprentissage payées par l'émission de crédits : qui les approuve et selon quelle règle. Une
   tâche correctement exécutée mais auto-attribuée ne doit pas donner de crédits.
6. Un modèle rare : le cercle des vérificateurs est petit, et `q` pour lui peut être proche de 1.
7. La disponibilité des données et le litige sur une requête privée sans révéler la requête.
8. La concordance bit à bit et la vitesse du modèle en arithmétique entière ne sont pas mesurées.
9. Un saboteur qui n'a pas besoin de profit, et l'empoisonnement des données d'apprentissage. La protection
   économique n'agit pas contre eux.

## 3. Décisions

Les décisions D1–D5 sont prises le 23 novembre 2026, D6–D17 le 24 novembre 2026 (sur instruction du propriétaire).

| N° | Question | Décision |
|---|---|---|
| D1 | Ce qui est accepté comme garantie | **Le fraudeur n'obtient pas ce qu'il veut.** On ne peut pas exclure les tentatives de fraude, mais toute tentative doit être inutile pour celui qui la fait : le gain attendu d'un faux n'est pas supérieur à zéro par rapport au travail honnête et par rapport à l'inaction, pour toute coalition, y compris un débutant avec un compte vide et un nombre quelconque de clés. Le but est que le résultat faux ne soit pas payé du tout. Une perte stricte à chaque tentative n'est pas exigée. Une fuite limitée mais positive (par exemple `R·q^k` chez le débutant dans la variante B) **ne satisfait pas** au critère et reste une faille ouverte |
| D2 | Le fondement du paiement | **Accepté : seul le résultat vérifiable est payé.** Le matériel allumé, le temps de travail et la puissance déclarée ne sont pas un fondement du paiement : on peut charger la carte graphique avec n'importe quoi d'autre |
| D3 | Variante A ou B | **La décision est prise après comparaison sur les mêmes attaques et au même coût (étape 2).** Le candidat principal est la variante B |
| D4 | Le noyau de vérification immuable | **Accepté sous une forme renforcée.** La vérification se déroule automatiquement, sans intervention humaine et sans votes. Les règles de vérification ne sont pas modifiées par un vote. Chaque nœud exécute lui-même la vérification d'après l'empreinte fixée des règles, c'est pourquoi la substitution de l'algorithme sur un nœud ou chez un fournisseur du programme ne change pas la décision des autres. Ouvert : comment corriger une erreur dans le noyau lui-même (uniquement par le passage à un nouveau réseau) et comment un participant s'assure que son programme correspond à l'empreinte publiée (construction reproductible). La clé de publication, avec laquelle les mini-agents sont actuellement signés, est un outil de recherche ; elle ne doit pas exister dans le réseau cible |
| D5 | La première expérience avec Qwen3.5-4B en arithmétique entière | **Autorisée :** la carte graphique RTX 2060 sur le Linux domestique du mainteneur, son ordinateur et, avec l'accord, les appareils d'autres participants via les mini-agents. S'exécute après l'étape 0 |
| D6 | Le préjudice entre-t-il dans D1 | **Oui** (décidé le 24 novembre 2026 sur instruction du propriétaire). « Le fraudeur n'obtient pas ce qu'il veut » ne concerne pas seulement les crédits, mais aussi le résultat : une réponse fausse ne doit pas être remise à l'utilisateur comme vérifiée, une fausse étape ne doit pas entrer dans le modèle. C'est pourquoi le résultat n'est utilisé qu'après une vérification indépendante de la part de collusion, ou bien il est explicitement marqué comme non vérifié |
| D7 | Vérification indépendante de la part de collusion ou affaiblissement de D1 | **Une vérification indépendante de la part de collusion est exigée** (24 novembre 2026). D1 n'est pas affaibli jusqu'à « tant que les collusionnés sont moins de q\* ». L'étape 4 devient principale |
| D8 | Litige depuis un compte à zéro | **Seuls les vérificateurs désignés par tirage au sort pour cette tâche et l'utilisateur, pour sa propre requête, peuvent ouvrir un litige** (24 novembre 2026). Sans caution ; le flux de litiges est limité par le nombre de vérifications et de requêtes. Les autres signalent un soupçon sur le tableau, sans droit d'arrêter le paiement |
| D9 | Qui approuve le plan d'apprentissage | **Personne en particulier : le plan est déduit par une règle fixée à partir du catalogue ouvert et des résultats de l'examen** (24 novembre 2026). Sans votes. Les crédits ne sont émis que pour les tâches du plan, une seule fois par contenu de tâche |
| D10 | Fuite d'une seule partie lors d'un échange | **Est considérée comme une violation de D1.** L'échange de crédits et d'autres valeurs passe uniquement par le journal, par un seul enregistrement pour les deux parties, sans tiers de confiance hors du journal |
| D11 | Composition du noyau immuable | **La vérification, la règle « seul ce qui est vérifié est payé », la règle d'émission des crédits, le litige et les règles du journal.** Les taux, le prélèvement du réseau et le catalogue de modèles ne changent que dans les limites fixées dans le noyau |
| D12 | Temps pour le poids et fenêtres de vérification | **Le temps actif du réseau**, et non le calendrier : tant que le réseau est arrêté, le poids ne vieillit pas et la fenêtre de vérification ne court pas |
| D13 | Accès aux tâches dans la variante B | **On introduit le parcours du débutant de la variante A :** l'accès aux tâches dépend de la somme en attente de la clé. Le choix définitif entre A et B (D3) intervient après la comparaison |
| D14 | Coût du litige | **Pour l'estimation, on prend un réseau de second niveau avec l'enregistrement le moins cher.** La différence entre le coût du litige et la somme qui peut être débitée de la partie perdante est payée par le prélèvement du réseau sur les consommateurs, et non par l'émission de crédits |
| D15 | Vérifications répétées et vérifications d'apprenti | **Un simple recalcul, qui peut être copié, n'est pas payé.** Une vérification n'est payée que là où son résultat ne peut pas être obtenu en copiant la réponse d'un autre |
| D16 | Panne matérielle honnête | **N'est pas punie comme une fraude :** la tâche n'est pas payée, la somme en attente n'est pas perdue ; le nombre de telles pannes par clé est limité |
| D17 | Source du paiement des requêtes dans la variante B | **Uniquement à partir des paiements des utilisateurs**, sans émission de crédits |

**Ordre du travail.** D'abord l'étape 0 est menée à terme — les mini-agents et les applications pour smartphones, afin que d'autres personnes puissent rejoindre le travail. Ensuite les étapes 1–5 selon cette feuille de route.

## 4. Étapes et liste de contrôle

L'étape 0 est menée à terme en premier. Ensuite les étapes 1–4 avancent en même temps : ce sont des calculs et des raisonnements. L'étape 5 (l'expérience est autorisée par la décision D5) vient après l'étape 0. L'étape 6 rassemble les résultats.

### Étape 0. Mini-agents et applications pour smartphones (exécutée en premier)

**Objectif de l'étape.** Sur chaque plateforme prise en charge, une personne parcourt le chemin
« téléchargé → installé → lancé », et ensuite le mini-agent, sans intervention humaine, se met à jour,
prend des tâches et rend le résultat. Sans compte utilisateur, sans droits d'administrateur, sans Python
préinstallé. Chaque étape est vérifiée sur un appareil réel, et pas seulement par des tests automatiques.

**Terminé quand** pour chaque plateforme de la liste ci-dessous : une personne sans expérience a parcouru
le chemin en une seule page d'instructions ; l'agent sur cet appareil a reçu lui-même une nouvelle
version, a pris lui-même une tâche de la nouvelle liste, son résultat est apparu sur le nœud complet et a
coïncidé avec le résultat d'un autre appareil. Sont consignés le système, l'architecture, les versions
avant et après et l'identifiant de l'enregistrement sur le nœud.

Plateformes : Windows, Linux, Android (décision du 23 novembre 2026). Pour macOS et iOS, les mini-agents
ne sont pas faits et ne sont pas vérifiés. La commande d'installation pour Linux fonctionne peut-être
aussi sur macOS, mais ce n'est pas pris en charge. La version Windows est publiée sans signature de
code : à l'installation, Windows affiche l'avertissement SmartScreen, qu'il faut confirmer manuellement ;
l'authenticité du fichier est vérifiée par l'empreinte publiée et la signature du projet.

Déjà fait :

- [x] Dépôt public, base immuable en neuf langues (étiquette `core-v1`).
- [x] Programme agent pour Windows et Linux : tâches et mises à jour signées, vérifications
      automatiques dans la CI (version 0.2.0). Installation par une seule commande dans le
      terminal ; Python 3.9+ est requis.
- [x] Résultats et [tableau des tâches](BOARD.md) sans compte utilisateur.
- [x] Premier nœud complet, conservant l'historique des enregistrements.
- [x] Première tâche de recherche « Protection contre les fraudeurs » sur le tableau, en neuf langues.
- [x] Application Android d'essai 0.1.0 (vérifiée uniquement sur l'émulateur).

**Point 1. Fiabilité de la mise à jour (version 0.2.1, sans nouvelles tâches)**

- [x] La première installation vérifie la signature de la version avec la clé intégrée dans
      l'installateur lui-même, **avant** l'exécution du code téléchargé (précédemment, l'agent téléchargé
      se vérifiait lui-même).
- [x] Le passage à la nouvelle version en une seule opération atomique : d'abord le nouveau répertoire
      est préparé et vérifié, puis un seul pointeur est changé ; l'ensemble fonctionnel précédent est
      conservé.
- [x] Le plus grand numéro de version accepté est stocké hors des répertoires de versions et est aussi
      vérifié lors de la réinstallation (protection contre le retour à une ancienne version).
- [x] La clé de l'appareil, les réglages, la progression et les résultats non envoyés sont stockés hors
      des répertoires de versions et survivent à la mise à jour et à la réinstallation.
- [x] Sans réseau, l'agent continue de travailler sur la dernière version fonctionnelle et réessaie la
      connexion avec un intervalle croissant.
- [x] Vérification automatique dans la CI : un fichier substitué, une clé étrangère, un ancien numéro,
      un fichier en trop, un téléchargement interrompu et un Python incompatible sont rejetés, la version
      fonctionnelle reste.
- [x] **Vérification en conditions réelles sur le serveur :** l'installation 0.2.0 est passée d'elle-même
      à 0.2.2 le 23 novembre 2026, la clé de l'appareil et la progression sont conservées. Sur le Linux
      domestique, l'agent a été réinstallé avec le nouvel installateur (0.2.2) ; sa mise à jour
      automatique sera vérifiée par la prochaine version.
- [x] Vérification en conditions réelles de la mise à jour automatique sous Windows : l'installation du
      propriétaire est passée d'elle-même 0.2.2 → 0.3.0 → Go 1.0.1 (23 novembre 2026).

**Point 2. Android : application sans jeton**

- [x] Nouvel APK 0.2.0 avec l'agent 0.2.2 intégré : publication par des enregistrements signés, l'écran du
      jeton et les conseils sur le jeton sont supprimés.
- [x] Corriger le faux retour en arrière sans réseau : auparavant, trois lancements sans connexion
      marquaient la nouvelle version fonctionnelle comme défaillante. Désormais, la version est confirmée
      par une auto-vérification locale.
- [x] Une fois par jour, l'application vérifie les nouvelles versions de l'APK, compare l'empreinte et
      la signature du projet et propose l'installation ; l'installation est confirmée par une personne
      (c'est ainsi qu'Android fonctionne hors du magasin).
- [x] Lancement après le redémarrage selon l'interrupteur de l'utilisateur (vérifié sur l'émulateur).
- [x] Vérification de la mise à jour par-dessus l'APK 0.1.0 sur l'émulateur Android 14 : les données
      sont conservées.
- [ ] Vérification de la proposition d'un nouvel APK par l'application elle-même (fonctionnera avec la
      prochaine version de l'APK).
- [ ] **Vérification en conditions réelles sur un vrai téléphone** (il faut un participant avec un
      téléphone) : installation, fonctionnement pendant la charge, redémarrage, économie d'énergie du
      fabricant.

**Point 3. Windows : installateur en un seul fichier**

- [x] `SkyNetAgentSetup.exe` est assemblé dans GitHub Actions, sans signature de code ; à l'intérieur,
      un Python embarqué de python.org, l'agent et la version signée. À côté sont publiés son empreinte
      et la signature du projet. Installation dans le profil de l'utilisateur, sans droits
      d'administrateur, fonctionne sans réseau.
- [x] Raccourcis dans le menu « Démarrer » : état de l'agent, pause, reprise, arrêt, désinstallation.
- [x] Case « lancer à la connexion » dans l'installateur ; le choix est conservé lors de la mise à jour.
- [x] Désinstallation via « Applications » ; lors de la désinstallation, on peut conserver la clé de
      l'appareil.
- [x] Vérification automatique dans la CI sur un Windows propre sans Python : installation,
      auto-vérification, désinstallation.
- [x] Vérification en conditions réelles sur l'ordinateur d'une personne : le propriétaire a installé
      l'agent depuis les Releases (version v0.2.2).

**Point 4. Linux**

- [x] L'installateur utilise le Python système 3.9+, et s'il n'y en a pas, installe un Python portable et
      vérifie son empreinte. Il existe aussi un installateur en un seul fichier, sans réseau (version
      v0.2.2).
- [x] Service utilisateur systemd avec l'accord de l'utilisateur ; le fonctionnement sans ouverture de
      session est une case séparée.
- [x] Vérification dans la CI : Debian 12 sans Python et Ubuntu 24.04 avec Python ; installation en
      conditions réelles sur Linux Mint.
- [ ] Vérification en conditions réelles chez un participant sans lien avec les mainteneurs.

**Point 5. Agent en Go au lieu de Python (décision du propriétaire du 23 novembre 2026)**

L'agent est réécrit en Go : un seul petit programme, Python n'est pas nécessaire. Le Python embarqué et sa
mise à jour ne sont plus requis, c'est pourquoi l'ancien point « mise à jour du Python embarqué » est retiré.

- [x] Signatures, tâches, sept noyaux de calcul, enregistrements, Nostr, tableau, cycle de travail, mise à
      jour par le second canal (`agent/v2/release.json`), lanceur, démarrage automatique — en Go, uniquement
      la bibliothèque standard (code écrit par ChatGPT, vérifié par DeepSeek).
- [x] Les résultats Go coïncident avec Python bit à bit sur toutes les portions rapides de la référence et
      sur toutes les portions lourdes vérifiées ; la comparaison des 1 199 portions se poursuit.
- [x] Construction reproductible : empreintes identiques des programmes lors d'une construction sous
      Windows et Linux.
- [x] Le pont en Python 0.4.0 transfère lui-même les agents installés vers Go en conservant la clé de
      l'appareil, la progression et la file d'attente. Transition en conditions réelles : le serveur, le
      Linux domestique et le Windows du propriétaire sont passés d'eux-mêmes à Go 1.0.1.
- [x] Installateurs en Go : Windows 4,7 Mo, Linux en un seul fichier ; application Android 0.3.0 avec
      moteur Go, environ 8 Mo au lieu de 40 (vérifié sur l'émulateur Android 14).
- [ ] Supprimer le pont et les copies Python après deux versions Go vérifiées.

**Point 6. Flux des tâches**

- [x] Quatre nouvelles tâches de calcul de l'étape 2 (la campagne de sortie de la variante B, les places
      d'apprenti, la loterie avec une part de vérification choisie, le certificat du jeton gagnant) — de
      nouveaux noyaux intégrés de l'agent 0.3.0, 515 portions dans la liste de tâches n° 2. Les
      mathématiques ont été vérifiées indépendamment par une autre méthode sur 111 points. Le certificat
      n'apporte pas d'économie sur des matrices aléatoires (environ 0,8% de travail supplémentaire), c'est
      pourquoi 20 portions ont été conservées comme base de comparaison avec les poids du modèle réel.
- [x] Les nouvelles tâches exigent l'agent 0.3.0 ou une version supérieure ; l'ancien agent saute la tâche
      incompatible et continue de travailler (vérifié par un test).
- [ ] Quand toutes les tâches sont calculées, l'agent attend et reprend lui-même la liste suivante.
- [ ] Le collecteur de résultats fonctionne selon un planning sur le nœud complet et publie un
      récapitulatif.
- [ ] Confirmation indépendante de toutes les 702 portions de la première liste. Un second appareil
      (serveur des mainteneurs) a recalculé les 702, toutes ont coïncidé ; il n'y a pas encore de
      participant sans lien avec les mainteneurs.

**Point 7. Pilote avec d'autres personnes**

- [ ] Page « Comment se connecter » en neuf langues : un lien pour chaque système.
- [ ] Un participant sans lien avec les mainteneurs sur chaque plateforme ; les critères d'achèvement de
      l'étape sont remplis.
- [ ] Deuxième et troisième nœuds complets chez des propriétaires différents.

**Point 8. Agents IA**

- [ ] L'agent récupère lui-même les nouvelles tâches du tableau et les transmet au modèle local du
      participant ; la réponse n'est envoyée qu'après l'approbation d'une personne. Le texte de la tâche
      est considéré comme non fiable.
- [ ] Instructions pour un assistant IA : comment prendre une tâche du tableau, remettre un rapport et
      vérifier celui d'un autre.
- [ ] Rapport sur une tâche du tableau remis par un participant sans lien avec les mainteneurs.

**Décisions du propriétaire sur l'étape 0** (23 novembre 2026) : macOS et iOS ne sont pas faits ; la
version Windows est publiée sans signature de code.

### Étape 1. Formulation précise

- [x] Les décisions D1 et D2 sont prises et consignées (section 3).
- [ ] Pour une requête ouverte et une étape d'apprentissage sont consignés : la règle d'acceptation,
      l'arithmétique, le fondement de l'émission de crédits, le moment de fixation du résultat par rapport au
      tirage au sort et le moment où le résultat peut être utilisé.
- [x] Le modèle de l'adversaire en un seul document : [THREAT_MODEL](THREAT_MODEL.md), section 1 (conseil
      de six modèles et de trois critiques, 24 novembre 2026).
- [x] Le tableau des attaques analysées est publié en neuf langues avec le statut de chaque attaque pour
      les variantes A et B : 60 attaques de la spécification et 32 nouvelles. L'écart entre 59 et 60 est
      expliqué : la ligne 1.9 (« pas une attaque ») a été omise dans le résumé.
- [x] Pour chaque attaque, il est consigné à partir de quelles données vérifiables indépendamment le nœud
      rejettera la fausse déclaration en cas de collusion de l'exécutant et des vérificateurs. Bilan : ni la
      variante A ni la variante B ne satisfont D1 littéralement ; un gain pécuniaire est possible dans
      24 lignes de A et 25 lignes de B [calcul].
- [x] Les décisions sur les douze questions de la section 5 de [THREAT_MODEL](THREAT_MODEL.md) : D6–D17.

Terminé quand : tout participant peut, à l'aide du tableau, identifier une attaque qui reste sans parade et vérifier que c’est bien le cas.

### Étape 2. Économie : les calculs exécutés par les mini-agents

Chaque tâche est un modèle exact avec une grille finie d'entrées ; les probabilités et les sommes sont
calculées en fractions exactes, l'empreinte de chaque portion est comparée entre les appareils.

- [x] Variante A, soumission de résultats falsifiés suivie d’un départ du réseau : première exécution.
- [x] Variante B, irrégularité du revenu à part de vérification constante : première exécution.
- [ ] Confirmation indépendante des deux calculs (voir étape 0).
- [ ] **Campagne de sortie dans la variante B.** Entrées : la somme en attente `H₀`, le prix `R`, la part de
      vérification `p`, la collusion `q` et `k`, le plafond des tâches simultanées `C`, le nombre de rafales
      `T`. Un seul faux attrapé remet à zéro toute la somme en attente, y compris les gains de la rafale.
      Trouver le plus grand paiement attendu au-delà de `H₀`, y compris pour `H₀ = 0`, `q = 0` et `q = 1`.
- [ ] **Places d'apprenti.** Par époque, `S` places sont distribuées entre `n` clés honnêtes et `m` clés de
      la coalition. Trouver la fuite attendue sur `E` époques et la part des places qui revient aux débutants
      honnêtes, lorsque `m` croît.
- [ ] **Loterie avec une part de vérification choisie.** Pour `N` tâches par mois, prendre le plus petit `p`
      pour lequel au moins 60 tâches sont payées en moyenne. Trouver la probabilité d'un mois et d'un
      trimestre déficitaires, la probabilité d'un mois sans aucun paiement et le nombre de recalculs pour le
      réseau.
- [ ] **Certificat du jeton gagnant** (voir étape 4) : le nombre d'opérations de vérification par rapport au
      recalcul complet de la couche de sortie sur un ensemble d'entrées donné.
- [ ] La formule du coût complet de la vérification pour trois types de participants ; après l'étape 5, les
      mesures y sont substituées.
- [ ] Comparaison des variantes A et B sur les mêmes attaques et au même coût, puis la décision D3. Issue
      possible : les deux variantes restent des pistes de recherche.

Terminé quand : pour chaque variante, il existe un tableau « part de collusion → plus grand gain attendu du
fraudeur », recalculé sur au moins deux appareils indépendants.

### Étape 3. Fermer les failles connues

- [ ] **Débutant avec un compte vide.** Candidat : les premières tâches du débutant sont telles que tout nœud
      les vérifie exactement lui-même, et ce n'est qu'ensuite que la récompense et le poids sont crédités.
      Solution de repli : un budget commun de paiements d'apprenti par époque ; il limite la fuite sans la
      rendre nulle, et la collusion peut occuper toutes les places.
- [ ] **« Honnête longtemps, puis une grosse fraude ».** Candidat : un plafond sur la somme de tous les
      engagements ouverts de la clé, en comptant les plus grands gains possibles. C'est une borne d'une seule
      rafale, pas une fuite nulle.
- [ ] **Déchets depuis des clés gratuites.** Candidat : le nœud n'accepte les données que pour les numéros de
      tâches autorisés, limite la taille, la file d'attente et le travail par époque. Le canal peut tout de
      même être saturé ; une place garantie pour un débutant honnête avec un nombre quelconque de clés n'est
      pas obtenue.
- [ ] **Résultat utilisé avant la vérification.** Candidat : vérifier le bloc de réponse avant de le
      remettre ; conserver l'étape d'apprentissage dans une branche séparée et ne promouvoir que le
      descendant vérifié. Coût : latence et mémoire.
- [ ] Tâches d'apprentissage : une règle d'approbation sans participant doté de droits spéciaux.
- [ ] Modèle rare : un seuil, déduit de la distribution du poids, en dessous duquel le réseau ne paie pas
      pour le modèle.
- [ ] Vérificateur paresseux et nouvelle soumission d'un résultat connu : des engagements masquants avec
      révélation, un crédit unique selon le contenu.
- [ ] Panne de matériel chez un participant honnête : une règle qui ne donne pas de gain au fraudeur.
- [ ] Disponibilité des données et litige sur une requête privée sans révélation.
- [ ] Fenêtre de litige à l'arrêt du réseau, protection contre un historique périmé, partition du réseau.

Terminé quand : pour chaque point sont publiés une construction avec ses hypothèses, une attaque contre elle
et son coût, soit un contre-exemple, soit le statut « ouvert » avec la raison.

### Étape 4. Recherche d'une garantie indépendante de la part de collusion

On cherche une vérification que chaque nœud exécute lui-même, de sorte que l'accord des vérificateurs ne
décide rien. Les directions ne sont pas approuvées. Pour chacune, il faut indiquer les opérations vérifiées,
les données, la probabilité d'erreur et le coût d'une requête ou d'une étape entière ; puis la mener jusqu'à
une construction ou la fermer par un contre-exemple.

- [ ] **Tâches pour lesquelles un critère exact permet de vérifier le résultat à faible coût.** Exemple : pour la régression ridge, le nœud
      vérifie la condition d'optimalité en un seul passage sur les données. Question : quelle part du travail
      du réseau tient dans de telles tâches. Commencer par cette direction : elle garantit qu’aucun résultat falsifié n’est rémunéré.
- [ ] **Utilisation d’un vecteur aléatoire pour vérifier chaque produit de matrices** au lieu du recalcul. Le
      vecteur est choisi après la fixation du résultat ; la probabilité de laisser passer une erreur ne
      dépend pas de la collusion. Rentable pour les grands lots ; pour la génération jeton par jeton, aucun
      gain. Les autres opérations (arrondi, activations, cache, optimiseur) doivent être vérifiées séparément.
- [ ] **Vérification de la réponse finie par un seul passage du modèle** avec un profil exact et l'aléa fixé
      dans la tâche. Le nombre d'opérations est du même ordre que la génération ; on ne sait pas si cela
      tient dans 5%.
- [ ] **Tables de sommes partielles exactes pour les couches immuables :** le nœud déduit une fois les tables
      des poids, puis obtient la sortie de la couche par des lectures et des additions. Applicable aussi à un
      seul jeton ; bute sur le volume de mémoire.
- [ ] **Certificat du jeton gagnant** pour un grand vocabulaire : l'exécutant transmet la couverture du
      vocabulaire par groupes, le nœud vérifie les bornes supérieures et ne descend vers les jetons
      individuels que là où la borne ne sépare pas le gagnant. Dans le pire des cas, tout le vocabulaire est
      vérifié.
- [ ] **Étape d'apprentissage comme formule exacte de mise à jour :** les nœuds stockent et vérifient non la
      nouvelle matrice de poids, mais les facteurs de mise à jour. Dérivé uniquement pour une couche linéaire
      avec un SGD simple.
- [ ] **Litige ouvert à tout participant pendant la fenêtre.** La garantie est conditionnelle : il faut au
      moins un observateur qui a reçu les données et a eu le temps d'objecter. Qui paie l'observation avec un
      compte vide n'est pas résolu. Garder en solution de repli.
- [ ] **Paiement pour l'amélioration mesurée du modèle** sur des tâches choisies après la fixation des poids.
      Change le fondement du paiement et exige une décision séparée. Convient à la sélection des versions du
      modèle.
- [ ] **Preuves de calcul pour l'apprentissage (sumcheck, GKR)** pour une étape définie : une estimation complète du coût de calcul
      avec les plages, l'arrondi et le rattachement de l'entrée à la tâche.
- [ ] **Borne inférieure :** montrer quelles classes de vérifications ne peuvent pas être sans erreur. Début :
      un ensemble fixe de vérifications linéaires dont le nombre est inférieur à la taille du résultat laisse
      toujours passer une certaine erreur ; restent ouverts l'aléa frais et les entrées à structure connue.
- [ ] Les idées des participants et des assistants IA venant du tableau : chacune passe par la même analyse,
      y compris le cas `q = 1`.

Terminé quand : pour chaque direction sont publiées une construction accompagnée d’une estimation de son coût, un contre-exemple ou une
borne prouvée. Est considérée comme trouvée la construction qui remplit tous les critères de la section 1.

### Étape 5. Les fondements qui ne s'établissent que par l'expérience (autorisée par D5)

- [ ] Qwen3.5-4B en arithmétique entière sur deux cartes graphiques différentes : les bits coïncident-ils.
- [ ] Sa vitesse par rapport au profil ordinaire sur les mêmes cartes.
- [ ] Sa qualité par rapport au profil ordinaire sur le même ensemble de tâches.
- [ ] Des plans de mesure séparés (hors D5) : l'énergie de la vérification, l'apprentissage en arithmétique
      entière.
- [ ] Le coût du litige dans le journal pour le modèle complet. Avant lui, il faut le choix de la blockchain,
      une machine de référence du modèle complet, le rattachement de l'entrée, les longueurs et les chemins
      de calcul.

Terminé quand : chaque nombre est mesuré, les conditions de la mesure sont consignées, la mesure a été
répétée par un second participant. La concordance des bits ne vaut que pour les configurations testées.

### Étape 6. Synthèse et acceptation

- [x] La décision D4 sur le noyau immuable (section 3).
- [ ] La composition du noyau et la manière dont un participant s'assure que son programme correspond à
      l'empreinte publiée.
- [ ] Mettre à jour CURRENT_DESIGN et le tableau des attaques d'après les résultats des étapes 1–5.
- [ ] Une déclaration est suivie sur le papier, de l'autorisation de la tâche jusqu'à l'utilisation du
      résultat, y compris le refus, la reprise et la partition du réseau.
- [ ] Revue ouverte de la construction finale : un conseil de modèles et une tâche sur le tableau.
- [ ] Pour chaque exigence est publiée une preuve, une mesure, un contre-exemple ou le statut « ouvert ».
      Vérification selon les six critères de la section 1.

## 5. Comment avance le travail

1. Un point de la liste de contrôle devient une tâche : de calcul (elle est calculée par les mini-agents, le résultat est vérifié par concordance) ou de recherche (elle est publiée sur le tableau).
2. Les participants et leurs assistants IA remettent des rapports. Un rapport n'est accepté que s'il peut
   être vérifié : par recalcul, par contre-exemple ou par une référence à la source. Le nombre de clés
   d'accord ne prouve rien ; la décision de l'auteur de la tâche sur le tableau ne confirme pas le calcul.
3. Selon l'issue de la vérification, la tâche est fermée, précisée ou donne naissance à de nouvelles tâches.
4. Le changement de statut est reporté dans cette feuille de route et dans CURRENT_DESIGN par une seule
   modification, avec la date.

## 6. Ce que cette feuille de route ne promet pas

- Qu'une solution existe dans les conditions fixées. C'est l'objet de la recherche.
- Des délais. Le projet n'a pas d'exécutants payés ; la vitesse dépend des participants.
- Des récompenses pour la participation à la conception.
