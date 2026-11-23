<!-- translation of android/README.md, source sha256: e6e5eb4a3358a14712c3c5b2e0efee2cd483b0009e7378ef16b31cc789c0d054 -->

# Agent de recherche SkyNet pour Android (expérimental)

[English](../../android/README.md) · [中文](../zh/ANDROID.md) · [Español](../es/ANDROID.md) · **Français** · [Deutsch](../de/ANDROID.md) · [Italiano](../it/ANDROID.md) · [Русский](../ru/ANDROID.md) · [Português](../pt/ANDROID.md) · [العربية](../ar/ANDROID.md)

Une application Android qui embarque les mêmes [noyaux de calcul Go](../../agent-go/README.md) que la version de
bureau. Installez un fichier et appuyez sur Démarrer. Par défaut, l'agent signe chaque résultat sur
l'appareil et le publie sans compte ni jeton.
À ce stade, aucune récompense n'est fournie.

**Expérimental.** L'enveloppe 0.3.0 inclut l'agent Go 1.0.0 (version 7 du moteur) dans l'APK. L'installation par-dessus la 0.2.0,
le cycle de vie du service et le redémarrage doivent encore être testés sur Android.

## Pour les participants

1. Téléchargez `skynet-agent.apk` depuis la
   page [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases).
2. Ouvrez le fichier. Android vous demande d'autoriser l'installation d'applications depuis votre navigateur ou votre gestionnaire de fichiers.
3. Ouvrez « SkyNet Agent » et appuyez sur **Démarrer**. Une notification permanente indique qu'elle est en cours d'exécution.

- Elle ne travaille que pendant que l'appareil est en charge, sauf si vous cochez « Travailler aussi sur batterie ».
  Débrancher l'appareil annule l'unité en cours et la laisse disponible pour une exécution ultérieure.
- Pour reprendre après le redémarrage de l'appareil, activez **Démarrer après le redémarrage**. Cette option est désactivée par
  défaut. Appuyer sur **Arrêter** maintient l'agent à l'arrêt après un redémarrage.
- Sur Android 13 et plus récent, si vous refusez les notifications, l'application fonctionne quand même ; Android ne l'affiche alors que dans la liste des applications en cours d'exécution.
- Si un profil existant utilise `submit_via=github`, ses résultats restent en file d'attente. Cette version
  prend en charge la publication via des enregistrements réseau signés.
- Android 7.0 ou plus récent sur arm64-v8a ou x86_64.
- Le mode IA facultatif n'est pas disponible dans l'application.
- Pour la supprimer, désinstallez l'application ; rien d'autre n'est laissé sur l'appareil.

## Mise à jour de l'application

Installez la 0.3.0 par-dessus l'application existante avec la même signature de paquet pour conserver
l'identité de votre appareil, vos réglages, votre progression et les résultats en file d'attente. À partir de la 0.2.0, l'ouverture de l'écran vérifie la présence d'un nouvel APK.
Android planifie aussi une vérification quotidienne lorsqu'un réseau est disponible, même si l'agent est
arrêté. Les restrictions de batterie peuvent retarder cette vérification.

L'application vérifie le manifeste de publication signé avec la clé intégrée dans l'APK. Pour une version
compatible plus récente, elle télécharge le fichier de la publication dans le cache privé et vérifie sa taille
et son SHA-256. Appuyez sur le bouton de mise à jour ou sur la notification pour l'installer. Sur Android 8 et plus récent,
autorisez l'installation depuis SkyNet Agent si on vous le demande, revenez à l'application et confirmez dans
l'installateur Android. Si les notifications sont désactivées, utilisez le bouton de l'écran principal.

## Agent et mises à jour

Le service de premier plan lance l'exécutable extrait dans le répertoire des bibliothèques natives.
Il exécute un seul processus de travail à basse priorité à la fois et maintient un verrou de réveil pendant le calcul. Un
processus de travail arrivé à expiration est arrêté et l'agent ignore temporairement cette tâche. Les nouvelles tâches arrivent
via l'index de tâches signé. Le nouveau code exécutable arrive avec une mise à jour de l'application.

Android vérifie le certificat de signature de l'APK lors de l'installation. La clé de publication distincte
authentifie l'index de tâches et le manifeste de téléchargement de l'APK. L'application vérifie la taille, le SHA-256, le nom de paquet et le code de version de l'APK avant d'ouvrir l'installateur.

## Construire l'application vous-même

Sous Linux, installez Go 1.27.4 avec ses sources, Bash, GNU patch, coreutils, file et readelf
(binutils). La construction de l'APK nécessite aussi JDK 17, Gradle 8.7 et le SDK Android 34.

```sh
cd android
gradle assembleRelease
```

Gradle appelle `./build-go.sh`. Exécutez ce script directement pour construire uniquement les deux
exécutables `app/src/main/jniLibs/<abi>/libskynet.so`. Il utilise `GOOS=android`,
`CGO_ENABLED=0` et PIE pour les deux ABI. La construction arm64 utilise Go standard. Pour la
construction de l'émulateur x86_64, le script active l'édition de liens interne dans une copie temporaire des
outils de construction hôtes de Go 1.27.4. Il vérifie l'architecture, le point d'entrée et
l'interpréteur `/system/bin/linker64` avant d'installer l'un ou l'autre fichier.

L'APK de publication est `app/build/outputs/apk/release/app-release-unsigned.apk`. Utilisez
`zipalign`, puis `apksigner sign` avec la même clé que l'APK précédent pour les mises à jour sur place. Générez et signez `android/latest.json` à partir de l'APK signé final avec
`tools/make_apk_manifest.py`.

## Licence

MIT, comme l'agent : [agent/LICENSE](../../agent/LICENSE).
