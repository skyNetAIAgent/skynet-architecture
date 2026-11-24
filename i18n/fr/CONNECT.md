<!-- translation of docs/CONNECT.md, source sha256: 125af61335dde49176b5b023903489a40b1792ebe8e8eb04a960681206774db9 -->

# Comment participer

[English](../../docs/CONNECT.md) · [中文](../zh/CONNECT.md) · [Español](../es/CONNECT.md) · **Français** · [Deutsch](../de/CONNECT.md) · [Italiano](../it/CONNECT.md) · [Русский](../ru/CONNECT.md) · [Português](../pt/CONNECT.md) · [العربية](../ar/CONNECT.md)

Vous pouvez aider à concevoir SkyNet avec votre ordinateur ou votre téléphone. L'agent de recherche
est un petit programme libre : il prend des calculs de recherche signés, les exécute pendant le temps
libre de votre appareil et publie les résultats. Aucun compte n'est nécessaire, où que ce soit.
**À ce stade, aucune récompense n'est fournie** : c'est une aide bénévole pour la recherche, et non
le réseau SkyNet lui-même.

## Installation

| Votre appareil | Ce qu'il faut faire |
|---|---|
| **Windows 10/11** (64 bits) | Téléchargez `SkyNetAgentSetup-<version>-amd64.exe` depuis la [dernière version publiée](https://github.com/skyNetAIAgent/skynet-architecture/releases/latest) et exécutez-le. Windows affiche « Windows a protégé votre PC » car le fichier n'a pas de signature de code : choisissez **Informations complémentaires**, puis **Exécuter quand même**. |
| **Linux** (x86_64 ou ARM64) | Téléchargez `skynet-agent-linux-install-<version>.sh` depuis la [dernière version publiée](https://github.com/skyNetAIAgent/skynet-architecture/releases/latest) et exécutez `sh skynet-agent-linux-install-<version>.sh`. |
| **Android 7.0+** (64 bits) | Téléchargez `skynet-agent.apk` depuis la page des versions publiées, ouvrez-le et autorisez l'installation depuis cette source. L'application ne fonctionne que pendant que le téléphone charge. |

macOS et iPhone ne sont pas pris en charge.

L'installateur démarre l'agent immédiatement et le configure pour qu'il se lance à nouveau après un
redémarrage (sous Windows, vous pouvez décocher cette option ; sous Android, appuyez une fois sur
**Start**). Ensuite, il n'y a rien d'autre à faire : l'agent se met à jour tout seul (uniquement vers
des versions signées par le projet), prend des tâches et publie les résultats de lui-même. Il trouve
tout seul un nœud complet sur votre réseau local s'il y en a un.

Les agents actuellement en ligne sont listés à l'adresse http://62.213.14.254:8790/agents : système,
processeur, mémoire, carte graphique, version et unités calculées. Aucune adresse IP ni nom
d'ordinateur n'est affiché.

## Ce qu'il utilise et ce qu'il ne fait jamais

- Un cœur de processeur, à la priorité la plus basse par défaut, pour que vos propres programmes ne
  ralentissent pas. Sur un ordinateur portable, il ne calcule pas sur batterie, sauf si vous
  l'autorisez.
- Il n'exécute jamais de code provenant d'une tâche, n'envoie jamais vos fichiers et ne nécessite
  aucun droit d'administrateur. Chaque résultat est un petit enregistrement public signé avec la clé
  de votre appareil.
- Pour mettre en pause ou arrêter : le dossier **SkyNet Agent** du menu Démarrer sous Windows,
  `skynet-agent pause` / `stop` sous Linux, le bouton **Stop** dans l'application.
- Pour le supprimer : **SkyNet Agent → Uninstall** sous Windows, `skynet-agent uninstall --yes` sous
  Linux, désinstallez l'application sur Android.

Détails : [le guide de l'agent](AGENT.md).

## Aider avec des idées, pas seulement avec du calcul

Le principal problème ouvert du projet est de savoir comment vérifier les calculs pour que la triche
ne soit jamais rentable, à faible coût, sans dépôt ni amende. Si vous, ou votre assistant d'IA, avez
une idée ou avez trouvé une faille, consultez le [tableau des tâches](BOARD.md), la
[feuille de route](ROADMAP.md) et les [questions ouvertes](OPEN_QUESTIONS.md).
