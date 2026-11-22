<!-- translation of docs/RESEARCH_AGENT.md, source sha256: be3193497fd35b1568b634f7647119965e68e6e665fea52b5a8ecb8aa477aa9e -->

# Programme-agent : comment aider le projet sans assistant d'IA

[English](../../docs/RESEARCH_AGENT.en.md) · [中文](../zh/RESEARCH_AGENT.md) · [Español](../es/RESEARCH_AGENT.md) · **Français** · [Deutsch](../de/RESEARCH_AGENT.md) · [Italiano](../it/RESEARCH_AGENT.md) · [Русский](../../docs/RESEARCH_AGENT.md) · [Português](../pt/RESEARCH_AGENT.md) · [العربية](../ar/RESEARCH_AGENT.md)

État au 22 novembre 2026. Version de l'agent 0.1.0. Instructions pour le participant :
[agent/README.md](../../agent/README.md) ([en russe](../ru/AGENT.md)).

## Pourquoi

Le dépôt est conçu pour les personnes qui disposent d'un assistant d'IA : il lit les documents
et aide à concevoir. La plupart des gens n'ont pas un tel assistant, mais ont un ordinateur ou
un téléphone. L'agent leur donne un moyen de participer : il consulte régulièrement ce dépôt,
prend des tâches, les exécute sur l'appareil du participant et publie les résultats.

À ce stade, **il n'y a aucune récompense** : ni crédits, ni argent, ni promesse de paiements
futurs. Le but est d'attirer vers la conception de l'architecture le plus possible de ressources
de calcul et de vérificateurs indépendants.

L'agent est **un outil de recherche, pas le réseau SkyNet**. Il est plus simple et plus
centralisé que le réseau ne doit l'être, et il ne satisfait pas lui-même aux exigences
obligatoires du réseau. Cela est dit explicitement à chaque endroit ci-dessous.

## Comment c'est fait

| Élément | Où il se trouve | Ce qu'il fait |
|---|---|---|
| Liste des tâches | `tasks/index.json` et la signature `tasks/index.json.sig` | Nomme le calcul intégré, ses paramètres et le nombre de portions indépendantes |
| Agent | `agent/skynet_agent/`, uniquement la bibliothèque standard Python 3.9+ | Vérifie les signatures, choisit une portion, calcule, publie, se met à jour |
| Description de la version | `agent/release.json` et la signature | Énumère les fichiers de l'agent avec leur taille et leur SHA-256 |
| Lanceur | `agent/launcher.py` | Lance la version actuelle, passe à la nouvelle, revient en arrière depuis une version cassée |
| Résultats | Commentaires dans le ticket GitHub au nom du participant | Enregistrement lisible par machine avec l'empreinte du résultat |
| Synthèse | `results/`, construite par `tools/collect_results.py` | Compare les résultats de différentes personnes et revérifie les trouvailles |

Un cycle de travail de l'agent :

1. Toutes les 30 minutes (avec une dispersion), il télécharge la description de la version et
   la liste des tâches.
2. Il vérifie la signature de chacune d'elles avec la clé de publication intégrée à la copie
   installée.
3. S'il existe une version au numéro plus élevé, il télécharge ses fichiers, compare chacun avec
   son empreinte, l'installe à côté de la version actuelle et redémarre.
4. Il choisit une portion aléatoire d'une tâche qu'il n'a pas encore calculée.
5. Il la calcule dans un processus séparé, avec la priorité la plus basse et une limite de temps.
6. Il met le résultat dans la « boîte d'envoi » et le publie comme commentaire dans le ticket
   GitHub. Les résultats d'une même tâche sont publiés en lot, au plus un commentaire par heure,
   pour ne pas submerger le ticket et ses abonnés de notifications. Après une tentative échouée,
   la suivante est reportée : d'une minute, puis deux fois plus, mais jamais plus d'une heure.
   S'il est impossible de publier (pas de connexion à GitHub), l'agent, après trois cents
   résultats non publiés, cesse de prendre du travail et le signale.

Il n'y a pas d'ordonnanceur : chaque agent choisit sa portion lui-même. Le chevauchement des
portions entre différents participants est voulu : toutes les tâches de calcul sont entières, de
sorte que n'importe quel appareil obtient les mêmes chiffres, et une portion est considérée
comme confirmée quand la même empreinte a été publiée par autant de comptes différents que la
tâche l'exige.

## Une tâche est une donnée, pas un programme

L'agent ne télécharge et n'exécute jamais de code provenant d'une tâche. Une tâche nomme l'un
des calculs intégrés à l'agent (« noyau ») et lui transmet des nombres. Chaque noyau vérifie
les paramètres et limite le volume de travail. Un nouveau type de calcul n'apparaît qu'avec une
nouvelle version signée de l'agent, dont le code source se trouve dans le dépôt et se lit
directement.

Noyaux de la version 0.1 :

| Noyau | Ce qu'il calcule |
|---|---|
| `selftest` | Calcul entier de contrôle : l'empreinte doit être identique sur tous les appareils |
| `exit-scam-a` | L'espérance exacte de paiement d'un participant qui, avant de partir, soumet des faux (variante A de [CURRENT_DESIGN](CURRENT_DESIGN.md)) ; énumère une famille de stratégies et signale celles qui sont plus avantageuses qu'un départ honnête |
| `lottery-b` | La probabilité exacte d'un mois ou d'un trimestre déficitaire si l'on ne paie que pour les tâches vérifiées (variante B) |
| `ai-answer` | Au choix du participant : une question pour le modèle d'IA local qu'il fait tourner lui-même |

Le modèle exact de chaque calcul est écrit en tête du fichier source du noyau, afin que
n'importe qui puisse recalculer le résultat de façon indépendante. Les tâches et leur sens :
[tasks/README.md](../../tasks/README.md).

**Limite par rapport à la règle du projet sur les expériences.** Les premières tâches sont des
calculs d'après les formules des documents (analyse de coût et recherche de contre-exemples) et
des questions aux modèles de langage. Ce ne sont ni des mesures sur le matériel ni des
expériences sur le réseau. Les tâches de mesure (par exemple, les bits de la sortie entière
coïncident-ils sur différentes cartes graphiques) ne sont publiées qu'après la décision du
propriétaire du projet d'ouvrir les expériences.

## Mode IA (facultatif, expérimental)

Un participant qui fait tourner chez lui un modèle ouvert (Ollama, le serveur llama.cpp,
LM Studio et équivalents avec une interface compatible OpenAI) peut activer `ai.enabled`.
L'agent transmet alors au modèle des questions de la liste signée et publie les réponses.
Ainsi, des personnes sans abonnement à une IA mais avec une carte graphique deviennent des
participants du « conseil des modèles ».

- L'agent ne télécharge et ne démarre pas de modèle et, par défaut, ne s'adresse qu'à un
  serveur situé sur le même ordinateur.
- La question et les documents qu'il cite sont définis par la liste signée. Chaque document est
  comparé à son empreinte, de sorte qu'on ne peut pas faire lire un autre texte au modèle.
- Par défaut, la réponse attend dans la « boîte d'envoi » que le participant l'approuve : le
  texte est publié en son nom.
- La réponse est marquée comme générée par une machine et vérifiée par personne. Le nombre de
  réponses par question est limité.

Vérifié seulement sur un serveur factice dans les tests automatiques. Avec de véritables
environnements d'exécution de modèles, le mode n'a pas encore été testé.

## Application Android (expérimentale)

Pour ceux qui ne veulent pas configurer Termux, il existe une application : un seul fichier
APK, un bouton « Start ». Code source et instructions : [android/README.md](ANDROID.md).
Le même paquet `skynet_agent` et Python (via Chaquopy) sont intégrés à l'application.
Différences par rapport à l'agent sur ordinateur :

- Android ne permet pas de lancer des processus Python séparés ; la portion est donc calculée
  dans le processus d'arrière-plan de l'application elle-même, une à la fois. Si une portion
  dépasse la limite, le chien de garde met fin à ce processus, Android relance le service et la
  tâche reste aux appareils plus rapides.
- La nouvelle version de l'agent est prise depuis le dépôt avec la même signature de clé de
  publication. C'est la copie intégrée qui la vérifie ; si la nouvelle version ne démarre pas
  ici ou si ses fichiers ont été modifiés, l'application revient à la version intégrée.
- L'application elle-même (écran, service, chien de garde) ne change qu'avec un nouvel APK.
  L'APK est signé avec une clé distincte des mainteneurs du projet : c'est un second point de
  confiance unique, qui ne doit pas exister dans le réseau.
- Les résultats sont publiés avec un jeton GitHub que le participant colle dans l'application.
- Elle ne travaille que pendant la charge, sauf si le participant l'a autorisé autrement. Pas de
  mode IA.

État au 22 novembre 2026 : l'application se compile, sa partie Python passe les tests sur
ordinateur (`agent/tests/test_android_glue.py`). Une compilation de vérification avec une clé de
test a réussi sur l'émulateur Android 14 (x86_64) avec un dépôt de test local : installation,
vérification des signatures, calcul des 7 portions de test sans erreur, attente sans charge,
travail en arrière-plan, conservation du jeton et son utilisation avec la vraie API GitHub,
arrêt et redémarrage avec l'état conservé. Sur un vrai téléphone, l'application n'a pas encore
été lancée, la compilation pour ARM (`arm64-v8a`) n'a pas été vérifiée. Elle n'est pas distribuée
via Google Play : ses règles interdisent les applications qui téléchargent du code exécutable.

## À quoi l'agent fait confiance

| Quoi | Confiance |
|---|---|
| Signature Ed25519 par la clé de publication | Oui. Sans elle, ni la version ni la liste des tâches ne sont acceptées |
| Canal (HTTPS, miroir, GitHub lui-même) | Non pour l'intégrité : la substitution d'un fichier casse la signature ou l'empreinte |
| Contenu de la tâche | Non : les paramètres sont vérifiés, le volume de travail est limité, il n'y a pas de code dans la tâche |
| Réponse du modèle local | Non : c'est du texte, il est publié comme non vérifié |
| Première installation | Oui, au canal HTTPS vers GitHub. On peut vérifier l'installation avec la commande `selftest --online` |

**Limite honnête.** Le détenteur de la clé de publication peut livrer le programme à tous les
agents installés. Actuellement, la clé est détenue par les mainteneurs du projet. C'est un point de
confiance unique qui ne doit pas exister dans le réseau SkyNet : dans le projet cible, le
programme n'est mis à jour que vers une version dont l'empreinte a été acceptée par un vote des
participants dans le journal commun, et une signature par la clé de quelqu'un ne suffit pas
([CURRENT_DESIGN, section 8](CURRENT_DESIGN.md)). Un participant qui ne veut pas faire confiance
à la clé met `update` à `notify` et se met à jour manuellement après avoir lu les changements.

## Tableau des menaces

| Menace | Par quoi elle est couverte | Ce qui reste |
|---|---|---|
| Compromission du dépôt ou d'un compte avec droit d'écriture : substitution de l'agent | La version n'est acceptée qu'avec la signature d'une clé qui n'est pas dans le dépôt | Couvert, tant que la clé n'est pas volée |
| Substitution d'un fichier en transit ou sur un miroir | Signature de la description de version et SHA-256 de chaque fichier | Couvert |
| Retour à une ancienne version vulnérable | Le numéro de version doit être supérieur à l'actuel | Couvert pour les agents installés. Une nouvelle installation prend ce qui se trouve dans le dépôt |
| Tâche nuisible | La tâche ne contient pas de code ; le noyau vérifie les paramètres et limite le volume de travail et de mémoire ; il y a une limite de temps | Limité : une tâche signée peut occuper le processeur jusqu'à la limite de temps |
| Rejeu d'une ancienne liste de tâches signée | Le numéro de la liste doit être au moins celui déjà vu ; la liste peut avoir une date d'expiration | Limité : une installation fraîche peut recevoir une ancienne liste et calculer en vain des tâches fermées |
| Version cassée | Le lanceur revient à la version précédente après trois plantages rapides ou si les fichiers de la nouvelle version ont disparu, et mémorise le numéro inutilisable. Les demandes répétées de redémarrage sont exécutées avec une pause croissante | Couvert pour les plantages au démarrage. Une erreur silencieuse dans le calcul est attrapée par la comparaison des résultats |
| Vol de la clé de publication | La clé se trouve hors du dépôt ; sous Windows, elle est chiffrée pour le compte du propriétaire | **Ouvert.** Le voleur peut publier une version nuisible. Le remplacement de la clé se fait par une nouvelle version signée avec l'ancienne clé, et le voleur y a également accès |
| Perte de la clé de publication | Copie de secours chez le propriétaire | Sans la clé, les agents installés ne peuvent pas être mis à jour : les participants devront réinstaller l'agent |
| Falsification d'un résultat | Le calcul entier est comparé entre différents comptes ; les trouvailles sont recalculées lors de la collecte | Limité : une personne avec deux comptes se « confirmera » elle-même. Comme il n'y a pas de récompenses, il n'y a aucun avantage, mais un saboteur est possible. Les mainteneurs recalculent de façon sélective |
| Flux de commentaires indésirables venant de comptes étrangers | Le collecteur n'accepte que les enregistrements avec une empreinte correcte et une tâche connue | Limité par les moyens de GitHub |
| Fuite du jeton GitHub | L'agent ne stocke pas le jeton, le prend chez `gh` ou dans une variable et ne l'envoie nulle part ailleurs qu'à GitHub par HTTPS, sans redirections | Un jeton avec droit d'écriture dans les dépôts publics reste la responsabilité du participant |
| Code étranger à côté de l'agent (module glissé dans le dossier courant) | Mode isolé de Python (`-I`) | Couvert. Il n'y a pas de protection contre un programme ayant les droits du même utilisateur sur le même ordinateur |
| Consommation des ressources du participant | Un processus par défaut, priorité la plus basse, pause sur batterie, limite de temps, commandes `pause` et `stop` | L'électricité, le participant la dépense lui-même et gratuitement |
| Arrêt de tous les agents par les mainteneurs | Marque signée `halt` dans la description de version ; elle agit même avec les mises à jour désactivées | C'est un levier intentionnel : uniquement l'arrêt, sans lancer quoi que ce soit |

## Ce que l'agent dit de lui-même

Uniquement le contenu de l'enregistrement publié : le nom de la tâche, le numéro de portion,
les nombres du résultat, le temps de calcul et, s'il n'est pas désactivé, une étiquette
approximative de plateforme du type `linux-amd64-py3.12`. Les requêtes ne vont que vers GitHub.
Rien n'est collecté sur les fichiers, le réseau ou le matériel du participant.

## Procédure pour les mainteneurs

La clé de publication est créée une seule fois et conservée hors du dépôt :

```
python tools/keytool.py generate
```

La copie de secours du secret, le propriétaire la fait lui-même, à la main, avec la commande
`python tools/keytool.py backup`, et la conserve hors de l'ordinateur. Le secret ne doit pas
être montré aux assistants, ni collé dans des chats ou des fichiers.

Nouvelle version de l'agent :

```
python tools/make_release.py --seq <numéro suivant> --version <x.y.z>
```

puis chargement des fichiers modifiés `agent/` dans le dépôt. Nouvelle liste de tâches :

```
python tools/sign_tasks.py
```

puis chargement de `tasks/index.json` et de `tasks/index.json.sig`. Collecte des résultats :

```
python tools/collect_results.py
```

Arrêter le travail de tous les agents jusqu'à la correction de l'erreur : publier une
description de version avec `--halt-through <numéro>` et la raison.

## Ce qui manque ici et pourquoi il est honnête de le dire

- **Ce n'est pas un réseau distribué.** Les tâches et les versions sont distribuées par un seul
  dépôt, signées par une seule clé, et les résultats sont reçus par une seule plateforme. Les
  exigences R1–R4 des [exigences obligatoires](../ru/REQUIREMENTS.md) ne s'appliquent pas à
  l'agent et ne sont pas satisfaites par lui.
- **Un compte GitHub est nécessaire.** Sans lui, les résultats ne sont publiés qu'à la main, par
  un lien.
- **Pas de protection contre de multiples comptes.** Pour une étape bénévole, c'est acceptable.
- **Android n'est pas vérifié sur un appareil réel** ; le démarrage automatique sur macOS, Linux
  et Android n'est vérifié qu'au niveau des fichiers créés. Deux cas sont pris en compte d'après
  la documentation et ne sont pas non plus vérifiés sur de vrais appareils : Python du Microsoft
  Store sous Windows (il voit sa propre copie d'`AppData` et du registre, c'est pourquoi le
  dossier de l'agent se trouve dans le profil et le démarrage automatique est ajouté à la main)
  et Python de python.org sous macOS sans certificats installés (l'agent répète la requête avec
  le fichier de certificats du système).
- **Les premières tâches sont faciles.** Toute la première fournée (702 portions) a pris sur un
  seul ordinateur de bureau 15,5 heures de temps processeur avec 16 processus simultanés à la
  priorité la plus basse, soit environ une heure en temps réel [mesuré sur un seul PC, le
  22 novembre 2026]. Le mécanisme est prêt à accepter des tâches lourdes. Le résultat obtenu :
  [results/FIRST_RUN.md](../../results/FIRST_RUN.md).

## Prochaines étapes

1. Des tâches de mesure sur différents appareils : la principale inconnue du projet est la
   coïncidence du résultat au bit près sur différentes cartes graphiques. Ce sont des
   expériences ; elles attendent la décision du propriétaire.
2. Abandon du compte GitHub : réception des résultats via plusieurs plateformes publiques
   indépendantes, comme dans le projet cible du réseau.
3. Abandon de la clé unique : plusieurs signatures indépendantes, puis acceptation des versions
   selon les règles du réseau lui-même.
4. Gestion du modèle local : téléchargement d'un modèle ouvert avec vérification de l'empreinte,
   pour que le mode IA s'active par une seule commande.
