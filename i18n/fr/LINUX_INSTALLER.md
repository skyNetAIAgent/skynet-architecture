<!-- translation of installer/linux/README.md, source sha256: cabcf2237fcb61f3ccddb3e461306c5030f018a0db5353bfe00e7a5f55dd389f -->

# Installateur Linux

[English](../../installer/linux/README.md) · [中文](../zh/LINUX_INSTALLER.md) · [Español](../es/LINUX_INSTALLER.md) · **Français** · [Deutsch](../de/LINUX_INSTALLER.md) · [Italiano](../it/LINUX_INSTALLER.md) · [Русский](../ru/LINUX_INSTALLER.md) · [Português](../pt/LINUX_INSTALLER.md) · [العربية](../ar/LINUX_INSTALLER.md)

L'installateur hors ligne contient des exécutables Go signés pour amd64, arm64 et ARMv7. Exécutez-le avec le compte de l'utilisateur du bureau. Une nouvelle installation utilise le répertoire de données propre à l'utilisateur et place la commande dans `~/.local/bin`.

~~~sh
sh skynet-agent-install.sh
~/.local/bin/skynet-agent verify-install
~~~

Utilisez `--home DIR` pour un profil personnalisé. L'installation démarre immédiatement l'agent et l'enregistre comme service utilisateur systemd, de sorte qu'il redémarre après un redémarrage de la machine ; elle tente aussi de le maintenir en cours d'exécution après la déconnexion (linger). Utilisez `--no-autostart` pour installer uniquement, ou `--linger` pour exiger linger. La suppression de l'agent conserve l'identité et les files d'attente. L'ajout de `--purge` supprime explicitement ses données enregistrées.

~~~sh
~/.local/bin/skynet-agent uninstall --yes
~~~

L'amorçage en ligne à `agent/install.sh` utilise curl, jq, xxd, sha256sum et OpenSSL avec prise en charge d'Ed25519. Obtenez le script depuis une version publiée de confiance. Il authentifie le manifeste avant d'exécuter le binaire propre à l'architecture.

Pour construire l'installateur hors ligne à partir d'artefacts signés, exécutez ce qui suit depuis la racine du dépôt. Le manifeste et la signature se trouvent dans `agent/v2`. Le constructeur vérifie chaque artefact avant de l'empaqueter.

~~~sh
sh installer/linux/build.sh --dir dist
~~~
