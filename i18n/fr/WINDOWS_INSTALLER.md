<!-- translation of installer/windows/README.md, source sha256: ea7cbbbfeb25d77b3a5b0c8e09d4f0869dfa666efd0d84e0755573b22c5206ae -->

# Installateur de bureau Windows

[English](../../installer/windows/README.md) · [中文](../zh/WINDOWS_INSTALLER.md) · [Español](../es/WINDOWS_INSTALLER.md) · **Français** · [Deutsch](../de/WINDOWS_INSTALLER.md) · [Italiano](../it/WINDOWS_INSTALLER.md) · [Русский](../ru/WINDOWS_INSTALLER.md) · [Português](../pt/WINDOWS_INSTALLER.md) · [العربية](../ar/WINDOWS_INSTALLER.md)

Choisissez l'installateur amd64 ou arm64 correspondant à votre ordinateur. Vérifiez son SHA-256 à l'aide d'une somme de contrôle obtenue par un canal fiable. Le programme d'installation installe la version native signée dans le profil de l'utilisateur actuel. Le programme d'installation démarre l'agent immédiatement et à chaque ouverture de session Windows ; ces deux options peuvent être décochées sur la page des tâches. Les raccourcis du menu Démarrer lancent le lanceur permanent.

Le désinstallateur conserve par défaut l'identité, les files d'attente et l'historique des versions. Sélectionnez l'option de suppression des données pour les supprimer. Pendant la migration, le pont Python signé précédent et son interpréteur sont conservés pour permettre un retour arrière.

## Compilation et test

Utilisez Python 3.9+ et Inno Setup 6 sur la machine de compilation. Placez le manifeste de publication et sa signature détachée sous `agent/v2`, ainsi que les binaires de publication correspondants sous `dist`. Utilisez un nouveau dossier de compilation. Le test de fumée nécessite un compte Windows jetable.

~~~powershell
./installer/windows/build.ps1 -BuildDir build -AssetDir dist -Arch amd64
./installer/windows/smoke.ps1 -BuildDir build
~~~
