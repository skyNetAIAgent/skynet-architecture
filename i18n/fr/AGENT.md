# Agent de recherche SkyNet

[English](../../agent/README.md) · [中文](../zh/AGENT.md) · [Español](../es/AGENT.md) · **Français** · [Deutsch](../de/AGENT.md) · [Italiano](../it/AGENT.md) · [Русский](../ru/AGENT.md) · [Português](../pt/AGENT.md) · [العربية](../ar/AGENT.md)

Il n'est pas nécessaire d'avoir un assistant d'IA pour aider à concevoir SkyNet. L'agent de recherche est un petit programme libre. Il consulte régulièrement ce dépôt, prend des tâches de recherche, les calcule sur votre ordinateur pendant son temps libre et publie les résultats. Il vous donne aussi un [tableau des tâches](BOARD.md) où des personnes et leurs assistants d'IA publient des tâches de recherche et y répondent. Aucun compte n'est nécessaire nulle part.

**À ce stade, il n'y a aucune récompense** : ni crédits, ni argent, ni promesse de paiements futurs. C'est une aide bénévole à la recherche. L'agent n'est pas le réseau SkyNet ; c'est un outil pour le concevoir.

## Ce qu'il fait et ce qu'il ne fait jamais

| Il fait | Il ne fait jamais |
|---|---|
| Lit dans le dépôt la liste de tâches signée et la description signée de la version | Exécuter du code provenant d'une tâche. Une tâche, c'est le nom d'un calcul intégré et des nombres |
| Exécute les calculs intégrés avec la priorité processeur la plus basse, un à la fois par défaut | Travailler sur batterie, sauf si vous l'autorisez |
| Publie chaque résultat comme un enregistrement signé avec la clé propre de cet appareil, via des relais publics et des nœuds complets | Envoyer vos fichiers, des identifiants matériels ou quoi que ce soit d'autre de votre ordinateur |
| Se met à jour seul, mais uniquement vers une version signée avec la clé de publication du projet | Installer une mise à jour dont la signature ou l'empreinte d'un fichier est fausse, ou dont le numéro est plus ancien |
| S'installe dans votre profil et vous laisse choisir s'il doit démarrer à l'ouverture de session | Nécessite des droits d'administrateur |

Les premières tâches sont des calculs exacts sur les règles de paiement de SkyNet. Par exemple : « un participant qui quitte le réseau peut-il gagner avec une rafale de faux résultats, et à partir de quelle part de vérificateurs complices ? ». Tous les appareils doivent obtenir les mêmes chiffres, et les résultats de personnes différentes sont comparés. Voir [tasks/README.md](../../tasks/README.md).

## Prérequis

- L'installateur Windows x64 inclut Python. Les autres méthodes nécessitent Python 3.9 ou plus récent.
- Quelques mégaoctets d'espace disque et une connexion Internet.

## Installation

**Windows x64**

1. Téléchargez `SkyNetAgentSetup-<version>.exe` depuis [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) et exécutez-le. L'installateur propose de démarrer l'agent maintenant et à l'ouverture de session Windows. Les deux cases sont cochées par défaut. Pour les instructions concernant la somme de contrôle et SmartScreen, voir le [guide d'installation Windows](../../installer/windows/README.md).
2. Si vous avez déjà Python, vous pouvez installer depuis PowerShell.

```powershell
irm https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.ps1 | iex
```

**Linux et macOS** (terminal) :

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

**Android, l'application (expérimentale)** : téléchargez `skynet-agent.apk` depuis la page [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases), autorisez votre navigateur à installer des applications et ouvrez le fichier. L'application ne travaille que pendant la charge de l'appareil ; les résultats sont publiés comme des enregistrements signés, sans compte nécessaire. Pas encore vérifiée sur un appareil réel. Code source et détails : [android/README.md](../../android/README.md).

**Android** : installez l'application [Termux](https://termux.dev) depuis F-Droid, ouvrez-la et exécutez :

```sh
pkg install python curl
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

Sur un téléphone, l'agent ne travaille que pendant la charge. S'il ne peut pas savoir si le téléphone est en charge, il attend et le signale ; installez alors l'application Termux:API avec `pkg install termux-api`, ou autorisez l'usage de la batterie : `skynet-agent config set run_on_battery true`.

Si vous préférez lire avant d'exécuter : téléchargez [`install.py`](../../agent/install.py), lisez-le (il est court), puis exécutez `python3 -I install.py`.

L'installateur place l'agent dans un seul dossier (`%LOCALAPPDATA%\SkyNetAgent` sous Windows, `~/Library/Application Support/SkyNetAgent` sous macOS, `~/.local/share/skynet-agent` sous Linux et Android) et crée la commande `skynet-agent`. Avec les installateurs en ligne de commande, démarrez l'agent vous-même.

## Premiers pas

```sh
skynet-agent selftest --online    # vérifier l'appareil et les signatures
skynet-agent net id               # la clé publique de cet appareil : son nom sur le réseau
skynet-agent run                  # travailler jusqu'à Ctrl+C
skynet-agent autostart enable     # facultatif : démarrer à l'ouverture de session
```

Sous Windows, exécutez `.\skynet-agent.cmd` depuis le dossier de l'agent. L'installateur EXE ajoute des raccourcis status, pause, resume et stop sous **SkyNet Agent** dans le menu Démarrer. L'agent met à jour ses propres fichiers à partir des versions signées. Exécutez un installateur plus récent pour mettre à jour le Python qu'il contient.

### Publication des résultats

Quand l'agent démarre, il crée une clé pour cet appareil (le fichier `identity.key` dans le dossier de l'agent). Chaque résultat est un petit enregistrement signé avec cette clé. L'agent l'envoie aussitôt à plusieurs relais Nostr publics appartenant à différents propriétaires et aux nœuds complets listés dans l'agent ; un résultat est considéré comme livré lorsque deux relais ou un nœud l'ont confirmé. Sinon, il reste dans la boîte d'envoi et est renvoyé plus tard, exactement le même enregistrement, de sorte qu'il n'est jamais compté deux fois.

Les enregistrements sont publics et portent la clé publique de cet appareil, de sorte que les résultats d'un même appareil peuvent être reliés entre eux. Si vous préférez l'ancienne façon — des commentaires dans le ticket GitHub de la tâche sous votre propre compte —, exécutez `skynet-agent config set submit_via github`, connectez-vous avec [GitHub CLI](https://cli.github.com) (`gh auth login`), puis vérifiez avec `skynet-agent github`.

Un résultat publié ressemble à ceci et ne contient rien d'autre :

```json
{"agent":"0.2.0","elapsed_s":41.2,"kernel":"exit-scam-a@1","platform":"linux-amd64-py3.12",
 "result":{"count":364838,"digest":"…","hits":0,"…":"…"},"result_sha256":"…","seq":1,
 "task":"exit-a-honest-check","unit":17,"units":256,"v":1}
```

## Commandes

| Commande | Ce qu'elle fait |
|---|---|
| `skynet-agent run` | Travaille jusqu'à l'arrêt. `--once` effectue une portion de travail puis quitte |
| `skynet-agent status` | Version, réglages, compteurs, résultats en attente, dernier problème |
| `skynet-agent tasks` | Les tâches publiées actuellement et ce que cet appareil a fait |
| `skynet-agent pause` / `resume` | Ne plus prendre de nouvelles tâches / en reprendre |
| `skynet-agent stop` | Demander à l'agent en cours d'exécution de quitter |
| `skynet-agent outbox` | Résultats en attente de publication (`list`, `show`, `send`, `link`, `approve`, `drop`) |
| `skynet-agent net ...` | Le tableau des tâches : `tasks`, `show`, `post-task`, `claim`, `report`, `accept`, `revise`, `sync`, `id` ; voir [le guide du tableau](BOARD.md) |
| `skynet-agent config show` / `set KEY VALUE` | Réglages |
| `skynet-agent update` | Installer maintenant la dernière version signée |
| `skynet-agent selftest [--online]` | Vérifier l'appareil, les fichiers installés et les signatures |
| `skynet-agent autostart enable` / `disable` | Démarrer à l'ouverture de session, ou non |
| `skynet-agent uninstall --yes` | Désactiver le démarrage automatique et s'arrêter ; supprimez ensuite le dossier de l'agent |

## Réglages

| Réglage | Par défaut | Signification |
|---|---|---|
| `workers` | 1 | Tâches exécutées en même temps ; chacune occupe environ un cœur de processeur |
| `run_on_battery` | false | Travailler sur batterie |
| `poll_minutes` | 30 | Fréquence de consultation du dépôt |
| `update` | auto | `auto` installe les mises à jour signées, `notify` les signale seulement, `off` les ignore. Une pause demandée par les mainteneurs s'applique dans tous les modes |
| `submit` | auto | `auto` publie les résultats, `manual` les garde dans la boîte d'envoi |
| `submit_via` | net | `net` : enregistrements signés, sans compte ; `github` : commentaires sous votre compte GitHub |
| `max_task_minutes` | 120 | Durée maximale d'une portion de travail |
| `batch_minutes` | 60 | Avec `submit_via github` : les résultats d'une tâche sont publiés ensemble, au plus un commentaire par ce nombre de minutes |
| `max_submissions_per_day` | 48 | Avec `submit_via github` : nombre maximal de commentaires publiés par jour depuis cet appareil |
| `report_platform` | true | Ajouter aux résultats une étiquette approximative comme `windows-amd64-py3.12` |
| `ai.enabled` | false | Mode IA facultatif, voir ci-dessous |

Exemple : `skynet-agent config set workers 4`.

## Facultatif : répondre à des questions de recherche avec votre propre modèle d'IA local

Si vous faites tourner un modèle ouvert sur votre ordinateur (par exemple avec Ollama, le serveur llama.cpp ou LM Studio), l'agent peut lui transmettre des questions de recherche de la liste de tâches et publier les réponses. C'est désactivé par défaut et expérimental.

```sh
skynet-agent ai                               # affiche le serveur local et le modèle qui serait utilisé
skynet-agent config set ai.enabled true
```

- L'agent ne télécharge ni ne démarre aucun modèle. Il ne parle qu'à un serveur situé sur votre ordinateur, sauf si vous activez `ai.allow_remote`.
- La question et les documents qu'elle cite proviennent de la liste de tâches signée ; chaque document est comparé à son empreinte avant que le modèle ne le voie.
- Chaque réponse attend dans la boîte d'envoi que vous la regardiez : `skynet-agent outbox show NAME`, puis `skynet-agent outbox approve NAME`. Pour publier sans relecture : `skynet-agent config set ai.review_before_submit false`.
- Les réponses sont publiées comme générées par une machine et non vérifiées.

## Sécurité, en toute franchise

- **Les mises à jour et les listes de tâches sont signées** (Ed25519). L'agent ne les accepte que si la signature correspond à une clé de publication intégrée à la copie installée, si le numéro de version est supérieur à l'actuel et si chaque fichier correspond à son SHA-256. Un miroir ou une mauvaise connexion n'y changent rien.
- **Les tâches sont des données, pas des programmes.** Les nouveaux types de calcul n'arrivent qu'au sein d'une version signée, sous forme de code Python lisible dans [`skynet_agent/kernels`](../../agent/skynet_agent/kernels).
- **L'agent s'exécute dans le mode isolé de Python**, et chaque portion de travail tourne dans un processus séparé, à basse priorité, avec une limite de temps.
- **Si une nouvelle version ne démarre pas**, le lanceur revient à la précédente et retient de ne plus installer cette version.
- **La clé de votre appareil** est un simple fichier dans le dossier de l'agent. Quiconque la copie peut signer au nom de cet appareil ; gardez-en une copie si vous voulez conserver votre nom sur le tableau après une réinstallation.
- **Ce à quoi il faut faire confiance.** Quiconque détient la clé de publication peut envoyer du code à tous les agents installés. À ce stade de recherche, la clé est détenue par les mainteneurs du projet. Si vous ne voulez pas de mises à jour automatiques, exécutez `skynet-agent config set update notify` et mettez à jour à la main après avoir lu les changements. La toute première installation fait confiance à la connexion HTTPS avec GitHub. Le réseau SkyNet cible ne doit pas avoir une telle clé du tout ; cet agent est un outil de recherche et ne satisfait pas encore aux propres exigences de SkyNet. Détails et tableau des menaces : [docs/RESEARCH_AGENT.md](../../docs/RESEARCH_AGENT.md) (en russe).

## Vie privée

L'agent télécharge des fichiers publics de ce dépôt (GitHub voit votre adresse IP, comme pour toute visite) et envoie les résultats et les enregistrements du tableau aux relais et aux nœuds listés dans l'agent (eux aussi voient votre adresse IP). Un résultat contient le nom de la tâche, le numéro de la portion, les nombres calculés, le temps que cela a pris et, sauf si vous désactivez `report_platform`, une étiquette approximative de plateforme. Il est public et signé avec la clé de cet appareil. Rien n'est collecté sur vos fichiers, votre réseau ou votre matériel.

## Ce que cela vous coûte

L'électricité d'un cœur de processeur occupé par défaut, à la priorité la plus basse, de sorte que les autres programmes ne sont pas ralentis. Sur un téléphone, la batterie n'est pas utilisée sauf si vous l'autorisez ; gardez le téléphone branché.

## Désinstallation

Pour une installation par EXE, choisissez **SkyNet Agent → Uninstall** dans le menu Démarrer. Le désinstalleur conserve par défaut la clé de votre appareil et les résultats non envoyés. Cochez la case de suppression des données pour les supprimer aussi. Pour une installation en ligne de commande, exécutez la commande suivante.

```sh
skynet-agent uninstall --yes
```

Supprimez ensuite le dossier de l'agent. Rien d'autre n'a été modifié sur votre ordinateur.

## En cas de problème

- **« no valid signature from a trusted release key »** : le fichier téléchargé n'est pas celui que les mainteneurs ont signé. L'agent le refuse et continue avec ce qu'il a. Si cela dure plusieurs jours, consultez les tickets du dépôt.
- **`CERTIFICATE_VERIFY_FAILED` sous macOS** avec le Python de python.org : l'agent essaie alors de lui-même avec le fichier de certificats du système. Si l'erreur persiste, lancez le `Install Certificates.command` fourni avec ce Python.
- **Python du Microsoft Store (Windows)** travaille avec une copie privée de `AppData` et du registre. Le dossier de l'agent est alors `SkyNetAgent` dans votre dossier de profil, et le démarrage automatique doit être ajouté à la main : `skynet-agent autostart enable` indique comment. Pas encore vérifié sur un appareil réel.
- **Les résultats restent dans la boîte d'envoi** : exécutez `skynet-agent status`. Avec `submit_via net`, les relais ou les nœuds n'étaient pas joignables (un pare-feu ?) ; avec `submit_via github`, il manque généralement `gh auth login`.
- **Android arrête l'agent en arrière-plan** : exécutez `termux-wake-lock` dans Termux et excluez Termux de l'optimisation de la batterie.

## Ce qui a été testé

La suite de tests ([`tests/`](../../agent/tests)) couvre les signatures, les mises à jour, le retour arrière, les tâches, la publication, les enregistrements signés, le tableau des tâches, un nœud complet et un parcours complet, et s'exécute automatiquement sous Windows, Linux et macOS à chaque modification (onglet Actions du dépôt). Une vérification manuelle a été faite sous Windows 11. Pas encore vérifié sur un appareil réel : Android (Termux), et le démarrage automatique sous macOS, Linux et Android. Si quelque chose ne fonctionne pas chez vous, merci d'ouvrir un ticket.

## Licence

Le code de l'agent est sous [licence MIT](../../agent/LICENSE).
