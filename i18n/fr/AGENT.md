# Agent de recherche SkyNet

[English](../../agent/README.md) · [中文](../zh/AGENT.md) · [Español](../es/AGENT.md) · **Français** · [Deutsch](../de/AGENT.md) · [Italiano](../it/AGENT.md) · [Русский](../ru/AGENT.md) · [Português](../pt/AGENT.md) · [العربية](../ar/AGENT.md)

Vous pouvez aider à concevoir SkyNet en laissant votre ordinateur effectuer une partie de la recherche. L'agent est un petit programme libre. Il consulte ce dépôt à la recherche de tâches, effectue une portion de calcul et partage le résultat. Vous pouvez aussi publier une question de recherche ou répondre à celle de quelqu'un d'autre sur le tableau des tâches. Vous n'avez besoin ni d'un compte ni d'un assistant d'IA. [Guide du tableau des tâches](BOARD.md)

**À ce stade, il n'y a aucune récompense.** Il n'y a ni crédits, ni argent, ni promesse de paiements futurs. C'est une recherche bénévole pour aider à concevoir le réseau SkyNet.

## Ce qu'il fait et ce qu'il ne fait jamais

| Il fait | Il ne fait jamais |
|---|---|
| Lit une liste de tâches signée. Chaque tâche nomme un calcul intégré et fournit ses entrées | Exécute du code provenant d'une tâche ou d'une publication du tableau |
| Exécute une portion de travail à la fois par défaut, avec la priorité processeur la plus basse | Démarre par défaut une nouvelle portion lorsque la batterie est détectée |
| Signe les résultats avec la clé de cet appareil et, par défaut, les envoie à des relais publics et à un nœud complet | Inclut vos fichiers personnels ou des identifiants matériels dans un résultat automatique |
| Vérifie la signature du projet avant d'installer une mise à jour de bureau | Accepte une mise à jour téléchargée dont la signature est invalide, dont l'empreinte de fichier est fausse ou dont le numéro de version est plus ancien |
| S'installe dans votre profil et vous laisse choisir s'il doit démarrer à l'ouverture de session | Nécessite des droits d'administrateur pour une installation de bureau normale |

L'une des questions de recherche est de savoir si un participant qui s'apprête à quitter le réseau peut tirer profit d'une rafale de faux résultats. Combien de vérificateurs devraient être complices ? Des appareils différents recevant la même portion de ce calcul doivent obtenir exactement la même réponse, afin que leurs résultats puissent être comparés. [Tâches de recherche](../../tasks/README.md)

## Prérequis

- Windows sur x64 (amd64) ou ARM64, ou Linux sur amd64, arm64 ou ARMv7. L'agent de bureau en 1.0.1 est un seul programme Go. Les installateurs de Releases incluent l'exécutable, prêt à l'emploi. macOS n'est pas pris en charge.
- Pour l'application Android expérimentale, Android 7.0 ou une version plus récente sur arm64-v8a ou x86_64.
- Une connexion Internet pour recevoir les nouvelles tâches et publier les résultats. L'installateur Linux de Releases peut effectuer l'installation hors ligne.

## Installation

**Windows**

1. Choisissez l'installateur Windows (`.exe`) correspondant à votre ordinateur, amd64 ou arm64, dans [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases).
2. Comparez la somme de contrôle SHA-256 du fichier avec la somme de contrôle provenant d'une source de confiance, puis exécutez l'installateur. Vous pouvez choisir de démarrer l'agent maintenant et de le démarrer à l'ouverture de session. L'installation ajoute des raccourcis au menu Démarrer. [Guide d'installation Windows](../../installer/windows/README.md)

**Linux**

Téléchargez `skynet-agent-install.sh` depuis la page [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) du projet et exécutez `sh skynet-agent-install.sh` en tant qu'utilisateur ordinaire. Le fichier inclut les exécutables pour les trois architectures Linux prises en charge.

Vous pouvez aussi installer par le réseau avec la commande ci-dessous. Elle nécessite `curl`, `jq`, `xxd`, `sha256sum` et OpenSSL avec prise en charge d'Ed25519.

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

Par défaut, l'installation conserve votre réglage existant de démarrage à l'ouverture de session. Lors d'une nouvelle installation, démarrez l'agent vous-même avec `skynet-agent run`. Pour le démarrer maintenant et à l'ouverture de session, exécutez `sh skynet-agent-install.sh --autostart`. Cela utilise votre service utilisateur systemd. Ajoutez `--linger` pour qu'il tourne dès le démarrage et après la déconnexion, ou utilisez `--no-autostart` pour désactiver le service. Si votre shell ne trouve pas la commande, utilisez `~/.local/bin/skynet-agent`. [Guide d'installation Linux](../../installer/linux/README.md)

**Android (expérimental)**

Téléchargez `skynet-agent.apk` depuis la page [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases). Ouvrez le fichier et autorisez l'installation depuis votre navigateur ou votre gestionnaire de fichiers lorsque Android le demande. Ouvrez **SkyNet Agent** et appuyez sur **Start**. Par défaut, il ne calcule que pendant la charge. **Start after reboot** est désactivé par défaut.

L'APK a son propre numéro de version. La version 0.3.0 de l'application inclut l'agent Go 1.0.0. L'application propose des mises à jour sur son écran ou dans une notification. Elle vérifie la description de version signée ainsi que la taille et le SHA-256 de l'APK avant de vous demander de confirmer l'installation dans Android. [Guide Android](../../android/README.md)

Votre clé d'appareil, vos réglages et vos résultats se trouvent dans le dossier de l'agent. Par défaut, ce dossier est `%LOCALAPPDATA%\SkyNetAgent` sous Windows et `~/.local/share/skynet-agent` sous Linux (ou `$XDG_DATA_HOME/skynet-agent` s'il est défini). L'installateur Linux accepte aussi `SKYNET_AGENT_HOME` ou `--home DIR` pour choisir un autre dossier. Android conserve son profil dans le stockage privé de l'application.

Si vous exécutez déjà l'agent Python sur un bureau pris en charge avec les mises à jour automatiques activées, il passe de lui-même à Go via la version passerelle signée **0.4.0**. Il conserve votre clé d'appareil, votre progression et les résultats non envoyés. La passerelle précédente et son interpréteur sont conservés pour le retour arrière.

## Premiers pas

Sous Linux, utilisez les commandes ci-dessous. Sous Windows, ouvrez PowerShell dans le dossier de l'agent et utilisez `.\skynet-agent.exe launch` à la place de `skynet-agent`. Par exemple, `.\skynet-agent.exe launch status` affiche votre état via le lanceur permanent.

```sh
skynet-agent verify-install       # vérifier les fichiers de la version installée et exécuter un calcul de test
skynet-agent selftest --online    # exécuter le calcul et vérifier les documents signés en ligne
skynet-agent net id               # afficher la clé publique de cet appareil, son nom sur le tableau
skynet-agent run                  # s'il ne tourne pas déjà, travailler jusqu'à Ctrl+C
```

Utilisez `skynet-agent autostart status` pour voir si le démarrage à l'ouverture de session est activé. Pour l'activer, utilisez `skynet-agent autostart enable`.

### Publication des résultats

L'agent enregistre chaque résultat terminé dans la boîte d'envoi. Il utilise la clé de signature dans `identity.key`, dans le dossier de l'agent, et en crée une à la première utilisation si le fichier est absent. Par défaut, il envoie le résultat signé à des relais Nostr publics et à un nœud complet. Un nœud ou deux relais distincts doivent confirmer la réception avant que l'agent ne déplace le résultat vers `sent`. Sinon, il reste dans la boîte d'envoi. Chaque nouvelle tentative utilise le même enregistrement signé, avec le même ID.

Voici une partie d'un résultat pour une tâche qui utilise le calcul de test intégré. Le résultat complet indique aussi le nom de la tâche, le nombre de secondes écoulées, la version du format, le numéro de version de l'agent et, par défaut, une étiquette de plateforme. L'enregistrement signé qui l'entoure porte la clé publique de l'appareil, un horodatage, l'ID de l'enregistrement et la signature.

```json
{
  "agent": "1.0.1", "kernel": "selftest@1", "unit": 0, "units": 1,
  "result": {
    "kernel": "selftest@1", "rounds": 8, "ok": true,
    "digest": "a2e8f2c45179bfccb6a01d61ab527a86277215a6ee85ff824910fe27d3e9fe26"
  },
  "result_sha256": "7823a03918e86a7046e437fdf001dc40ff05fb1d241a8917baeae4d88b5629fa"
}
```

## Commandes

| Commande de bureau | Ce qu'elle fait |
|---|---|
| `skynet-agent run` | Travaille jusqu'à l'arrêt. `--once` effectue au plus une portion de travail. `--no-submit` garde les résultats en local pour cette exécution. `--no-update` ignore l'installation des mises à jour. `--verbose` ajoute des détails au journal. |
| `skynet-agent status` | Affiche la version, le dossier de l'agent, l'état de l'alimentation, les compteurs de travail, les résultats en attente et les problèmes récents. |
| `skynet-agent tasks` | Liste les tâches de recherche automatiques, celles qui sont prêtes et combien de portions cet appareil a terminées. |
| `skynet-agent pause` / `resume` | Laisse les portions actives se terminer et arrête d'en démarrer de nouvelles, ou autorise de nouveau de nouvelles portions. |
| `skynet-agent stop` | Demander à l'agent en cours d'exécution de quitter |
| `skynet-agent outbox` | `list` affiche les résultats en attente, `show NAME` en affiche un, `send` tente de publier les résultats éligibles et `drop NAME` supprime un résultat en file d'attente. |
| `skynet-agent net` | Parcourez le tableau avec `tasks` ou `show`. Utilisez `post-task`, `claim`, `report`, `accept` ou `revise` pour participer. `sync` réessaie les publications en attente sur le tableau et récupère les enregistrements. `id` affiche votre clé publique. [Guide du tableau](BOARD.md) |
| `skynet-agent config` | `show` liste les réglages, `get KEY` en affiche un et `set KEY VALUE` le modifie. |
| `skynet-agent update` | Recherche une version de bureau signée plus récente et l'installe si elle est éligible pour cet appareil. |
| `skynet-agent selftest [--online]` | Vérifie un calcul par rapport à sa réponse connue. Ajoutez `--online` pour vérifier les signatures de la liste de tâches et de l'ancienne description de version du projet. |
| `skynet-agent verify-install` | Vérifie les fichiers de la version installée et exécute le calcul de test. |
| `skynet-agent version` | Affiche la version de l'agent, le numéro de version, la version de Go et la plateforme. |
| `skynet-agent autostart` | `status` indique si le démarrage à l'ouverture de session est activé. `enable` l'active et `disable` le désactive. |
| `skynet-agent uninstall --yes` | Supprime une installation Linux. Ajoutez `--purge` pour supprimer aussi les données enregistrées. |

## Réglages

| Réglage | Par défaut | Signification |
|---|---|---|
| `workers` | 1 | Nombre de portions que l'agent de bureau peut exécuter en même temps, de 1 à 256. Android en exécute une. |
| `run_on_battery` | false | Autoriser le calcul sur batterie. |
| `paused` | false | Attendre avant de démarrer de nouvelles portions. Les commandes `pause` et `resume` modifient ce réglage. |
| `poll_minutes` | 30 | Intervalle approximatif entre les consultations du dépôt, de 5 à 1440 minutes. Les consultations échouées ont leur propre calendrier de nouvelles tentatives. |
| `update` | auto | Sur un ordinateur de bureau, `auto` installe les mises à jour signées éligibles, `notify` journalise lorsqu'une mise à jour est disponible et `off` ignore l'installation et les notifications. Les trois vérifient toujours si les mainteneurs ont signé une pause. |
| `submit` | auto | `auto` envoie les résultats au fil du travail. `manual` les garde dans la boîte d'envoi jusqu'à ce que vous exécutiez `skynet-agent outbox send`. |
| `submit_via` | net | Publier des enregistrements signés via des relais et des nœuds. C'est le seul canal fonctionnel en 1.0. |
| `max_task_minutes` | 120 | Durée maximale par portion, de 1 à 1440 minutes. Une limite plus courte dans la tâche a la priorité. |
| `report_platform` | true | Inclure le système d'exploitation, l'architecture du processeur et la version de Go dans les nouveaux résultats, par exemple `linux-amd64-` suivi de la version de Go. |

Par exemple, `skynet-agent config set workers 4` autorise jusqu'à quatre workers de bureau. Pour rester compatible avec les anciennes installations, `skynet-agent config show` liste aussi les anciennes limites de commentaires et les réglages d'IA. Ces éléments n'ont aucun effet sur les calculs Go ni sur la publication sur le réseau.

## Facultatif : répondre à des questions de recherche avec votre propre modèle d'IA local

Le mode IA local n'est pas disponible en 1.0. Vous pouvez toujours rédiger et publier votre propre réponse sur le tableau des tâches.

## Sécurité, en toute franchise

- **Les mises à jour et les listes de tâches sont signées.** L'agent vérifie leurs signatures Ed25519 par rapport à la clé de publication du projet intégrée au programme. Avant de passer à une mise à jour de bureau, il vérifie le numéro de version, la taille et le SHA-256 de l'exécutable, et exécute un calcul de test. Il refuse les listes de tâches plus anciennes et cesse de démarrer du travail à partir d'une liste expirée.
- **Les tâches fournissent des données.** Les seuls calculs qu'une tâche peut sélectionner sont intégrés à l'exécutable. Ajouter un nouveau type de calcul nécessite une nouvelle version de bureau ou une mise à jour de l'application Android. [Code source Go des calculs](../../agent-go/kernels)
- **Chaque portion s'exécute dans un processus séparé** sous votre compte. Le worker demande une priorité processeur basse. L'agent arrête le worker s'il atteint la limite de temps.
- **Une mise à jour de bureau peut être annulée par un retour arrière.** Le lanceur vérifie la version active avant de la démarrer. Si cette vérification échoue, ou si trois tentatives consécutives d'exécution de l'agent plantent dans leur première minute, le lanceur peut restaurer une version précédente vérifiée si elle est disponible. Il retient le numéro de la version défaillante.
- **La clé de votre appareil est un fichier non chiffré.** Quiconque copie `identity.key` peut signer au nom de cet appareil. Une sauvegarde privée vous permet de conserver votre nom sur le tableau après une réinstallation.
- **La première installation dépend de l'endroit où vous obtenez l'installateur ou le script.** Après l'installation, quiconque contrôle la clé de publication du projet peut signer du nouveau code qui s'exécute avec vos permissions d'utilisateur. Les mainteneurs détiennent cette clé pendant cette phase de recherche. Pour examiner les mises à jour de bureau au préalable, utilisez `skynet-agent config set update notify` et exécutez `skynet-agent update` quand vous êtes prêt. Le réseau SkyNet proposé est censé fonctionner sans clé de publication centrale. [Conception de l'agent de recherche et tableau des menaces, en russe](../../docs/RESEARCH_AGENT.md)

## Vie privée

GitHub voit votre adresse IP lorsque vous téléchargez des tâches ou des mises à jour. Les relais et les nœuds complets que vous contactez voient aussi votre adresse IP. Le nœud complet intégré utilise HTTP non chiffré. Les résultats et les publications du tableau sont publics. Leur clé publique permet aux lecteurs de relier les enregistrements d'un même appareil.

Les résultats automatiques contiennent les données de calcul et les champs décrits ci-dessus. Utilisez `skynet-agent config set report_platform false` pour omettre l'étiquette de plateforme des résultats futurs. L'agent ne scanne pas vos fichiers personnels et n'inclut pas de numéros de série matériels. Lorsque vous publiez une tâche ou un rapport sur le tableau, le texte que vous choisissez d'envoyer devient public.

## Ce que cela vous coûte

Un worker occupé peut utiliser environ un cœur de processeur. La priorité basse aide les autres programmes à obtenir du temps processeur lorsqu'ils en ont besoin. Le travail consomme tout de même de l'électricité et peut produire de la chaleur. Sur un ordinateur portable, l'agent vérifie l'alimentation environ une fois par minute. Par défaut, il attend pour démarrer de nouvelles portions lorsqu'il détecte la batterie. Une portion déjà en cours peut se terminer, et l'agent de bureau peut démarrer du travail si la source d'alimentation est inconnue.

Sur Android, débrancher annule la portion en cours et la laisse disponible pour une nouvelle tentative. Sélectionnez **Also work on battery power** dans l'application si vous voulez qu'elle continue à calculer une fois débranchée.

## Désinstallation

Sous Windows, utilisez le désinstalleur **SkyNet Agent**. Il conserve par défaut votre clé d'appareil, les files d'attente et l'historique des versions. Choisissez l'option de suppression des données pendant la désinstallation pour les supprimer aussi.

Sous Linux, exécutez la commande suivante. Elle désactive le service utilisateur, arrête l'agent et supprime les programmes installés. Votre clé, vos réglages, votre progression et vos files d'attente sont conservés.

```sh
skynet-agent uninstall --yes
```

Pour supprimer aussi les données enregistrées de l'agent, utilisez `skynet-agent uninstall --yes --purge` lors de la désinstallation. Sur Android, désinstallez **SkyNet Agent** via les réglages d'Android pour supprimer l'application et ses données locales. Les enregistrements publiés restent publics.

## En cas de problème

- **« no valid signature from a trusted key »** signifie que le document téléchargé n'a pas passé la vérification. L'agent le refuse. Il peut encore utiliser une liste de tâches précédemment vérifiée jusqu'à ce que cette liste expire. Sur un bureau, `skynet-agent status` affiche la dernière erreur du dépôt. Le journal d'exécution est `logs/agent.log` dans le dossier de l'agent.
- **Les résultats restent dans la boîte d'envoi.** Utilisez `skynet-agent status` ou `skynet-agent outbox list` pour voir ce qui est en attente. En mode manuel, exécutez `skynet-agent outbox send`. Si trop peu de relais ou de nœuds répondent, le résultat reste en file d'attente pour une nouvelle tentative.
- **Une ancienne installation affiche « GitHub submission is unsupported ».** Exécutez `skynet-agent config set submit_via net` pour utiliser des enregistrements signés pour les nouveaux résultats. Les entrées déjà marquées pour GitHub et les anciennes réponses d'IA restent dans la boîte d'envoi pour inspection.
- **L'agent tourne mais aucun nouveau travail ne démarre.** Vérifiez `skynet-agent tasks` et le journal d'exécution. Il est peut-être en pause, en attente d'alimentation, à court de tâches éligibles ou en attente de place dans sa boîte d'envoi. Sur Android, branchez le chargeur et appuyez sur **Start** si vous avez arrêté l'application auparavant.

## Ce qui a été testé

Les tests de l'agent s'exécutent automatiquement sous Windows et Linux. Ils couvrent les listes de tâches signées, les calculs à réponse connue, les mises à jour et le retour arrière, les enregistrements signés, la livraison, le tableau des tâches et une exécution qui démarre un worker et livre son résultat à un nœud simulé.

Des installations réelles ont été essayées sous Windows 11, Linux Mint, Ubuntu Server et sur un émulateur Android 14. L'application Android n'a pas encore été vérifiée sur un appareil physique. Si quelque chose ne fonctionne pas sur votre système, merci d'ouvrir un ticket.

## Licence

Le code de l'agent est sous [licence MIT](../../agent-go/LICENSE).
