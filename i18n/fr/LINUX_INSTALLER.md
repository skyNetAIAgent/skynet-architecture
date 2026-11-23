<!-- translation of installer/linux/README.md, source sha256: 7ece3bc522f30a5f0b62b4a6580a177b3d4725e5b1eaa5513e255f0772f27156 -->

# Installateur Linux

[English](../../installer/linux/README.md) · [中文](../zh/LINUX_INSTALLER.md) · [Español](../es/LINUX_INSTALLER.md) · **Français** · [Deutsch](../de/LINUX_INSTALLER.md) · [Italiano](../it/LINUX_INSTALLER.md) · [Русский](../ru/LINUX_INSTALLER.md) · [Português](../pt/LINUX_INSTALLER.md) · [العربية](../ar/LINUX_INSTALLER.md)

L'installateur hors ligne contient des exécutables Go signés pour amd64, arm64 et ARMv7. Exécutez-le avec le compte de l'utilisateur du bureau. Une nouvelle installation utilise le répertoire de données propre à l'utilisateur et place la commande dans `~/.local/bin`.

~~~sh
sh skynet-agent-install.sh --no-autostart
~/.local/bin/skynet-agent verify-install
~~~

Utilisez `--home DIR` pour un profil personnalisé. Par défaut, l'installation conserve le démarrage à l'ouverture de session. Utilisez `--autostart` pour démarrer le service utilisateur systemd maintenant et à l'ouverture de session, ou ajoutez `--linger` pour le maintenir en cours d'exécution hors des sessions de connexion. La suppression de l'agent conserve l'identité et les files d'attente. L'ajout de `--purge` supprime explicitement ses données enregistrées.

~~~sh
~/.local/bin/skynet-agent uninstall --yes
~~~

L'amorçage en ligne à `agent/install.sh` utilise curl, jq, xxd, sha256sum et OpenSSL avec prise en charge d'Ed25519. Obtenez le script depuis une version publiée de confiance. Il authentifie le manifeste avant d'exécuter le binaire propre à l'architecture.

Pour construire l'installateur hors ligne à partir d'artefacts signés, exécutez ce qui suit depuis la racine du dépôt. Le manifeste et la signature se trouvent dans `agent/v2`. Le constructeur vérifie chaque artefact avant de l'empaqueter.

~~~sh
sh installer/linux/build.sh --dir dist
~~~
