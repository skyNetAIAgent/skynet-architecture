<!-- translation of installer/linux/README.md, source sha256: abf22229c4680552dec4357a2de39a59a6c18c9238e2ff76b46a2952e7d8f0b0 -->

# Installateur Linux

[English](../../installer/linux/README.md) · [中文](../zh/LINUX_INSTALLER.md) · [Español](../es/LINUX_INSTALLER.md) · **Français** · [Deutsch](../de/LINUX_INSTALLER.md) · [Italiano](../it/LINUX_INSTALLER.md) · [Русский](../ru/LINUX_INSTALLER.md) · [Português](../pt/LINUX_INSTALLER.md) · [العربية](../ar/LINUX_INSTALLER.md)

Exécutez le fichier unique depuis la page Releases du projet, avec votre propre compte.

```sh
sh skynet-agent-install.sh
```

Le fichier porte la version signée de l'agent. L'installation vérifie sa signature Ed25519 et les empreintes des fichiers hors ligne. Si Python 3.9 ou plus récent est dans votre PATH, l'installation utilise cet interpréteur. Sinon, il lui faut une compilation épinglée de CPython basée sur glibc, pour x86_64 ou aarch64. **Les deux empreintes sont actuellement en attente. Cette compilation exige le Python du système.**

L'installateur en ligne utilise la même procédure d'installation. Avec une version épinglée vérifiée, il peut récupérer l'environnement d'exécution correspondant depuis python-build-standalone et vérifier son SHA-256 avant l'extraction. Les interpréteurs portables se trouvent sous `$XDG_DATA_HOME/skynet-agent/python/<sha256>`, normalement `~/.local/share/skynet-agent/python/<sha256>`. La commande dans `~/.local/bin` et le service utilisateur systemd utilisent l'exécutable choisi.

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

## Démarrage et suppression

Dans un terminal, appuyer sur Entrée à la première question démarre le service maintenant et à l'ouverture de session. Appuyer sur Entrée à la seconde le maintient lié aux sessions de connexion. Sans terminal, l'installation saute les questions. Ces commandes expriment ces choix explicitement.

```sh
sh skynet-agent-install.sh --autostart           # Exécuter maintenant et à l'ouverture de session
sh skynet-agent-install.sh --autostart --linger  # Exécuter aussi avant l'ouverture de session et après la fermeture de session
sh skynet-agent-install.sh --no-autostart        # Installer pour un usage manuel
```

Le service a besoin d'un gestionnaire utilisateur systemd en cours d'exécution. Le générateur de service signé 0.2.2 prend en charge les chemins contenant des espaces. L'installation demande un démarrage manuel si le chemin d'un interpréteur ou de l'agent contient un guillemet double, une barre oblique inverse, un signe dollar, un signe pour cent ou un saut de ligne. Si une règle locale interdit le maintien après déconnexion, l'installation le signale et le service fonctionne quand même pendant les sessions de connexion. Le maintien après déconnexion, qui vaut pour tout le compte, peut être modifié séparément avec `loginctl disable-linger "$(id -un)"`. Pour une installation manuelle, commencez le travail avec `~/.local/bin/skynet-agent run`.

```sh
~/.local/bin/skynet-agent selftest
~/.local/bin/skynet-agent version
~/.local/bin/skynet-agent uninstall --yes
```

La désinstallation désactive le service, demande son arrêt et attend le verrou de l'agent. Votre clé d'identité, votre boîte d'envoi, les enregistrements de relais en attente et vos réglages restent dans le dossier de l'agent pour une réinstallation. Pour effacer aussi les données enregistrées de l'agent, utilisez `uninstall --yes --purge`. Le maintien après déconnexion est un réglage propre à tout le compte et il subsiste après la désinstallation.

## Compilation et vérification

Depuis la racine du dépôt, utilisez Python 3.9 ou plus récent sur la machine de compilation.

```sh
sh installer/linux/build.sh
shellcheck -s sh agent/install.sh installer/linux/build.sh installer/linux/smoke.sh
dash -n installer/linux/skynet-agent-install.sh
python3 -I -m unittest discover -s agent/tests -t agent/tests
```

Le constructeur authentifie la version avec la clé publique dans `agent/install.py` et produit `installer/linux/skynet-agent-install.sh`. Pour activer le Python portable, vérifiez chaque archive amont de façon indépendante et inscrivez son SHA-256 dans `python.lock` (un champ par ligne). Pour une entrée vide uniquement, CI peut fournir une empreinte vérifiée via `SKYNET_PYTHON_SHA256_X86_64` ou `SKYNET_PYTHON_SHA256_AARCH64`. Ce sont des réglages de compilation. Le constructeur vérifie et intègre chaque archive épinglée. Pour compiler hors ligne avec des versions épinglées, utilisez `sh installer/linux/build.sh --runtime-dir /path/to/archives`.

Le workflow de l'installateur Linux exécute le paquet avec un utilisateur non privilégié et sans réseau. Ubuntu 24.04 teste le Python du système. Debian 12 slim teste l'interpréteur portable lorsque l'empreinte x86_64 est disponible, et vérifie le refus lorsqu'elle est en attente. Les installations réussies exécutent l'auto-test, indiquent la version et testent les deux modes de désinstallation. Le workflow téléverse le script comme artefact de compilation pour une distribution manuelle.
