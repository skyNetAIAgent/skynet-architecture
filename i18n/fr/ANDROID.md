<!-- translation of android/README.md, source sha256: 3fd07398dc6f1c3ed1d7c21b1315b13e43cdbf629cf72aab3887e8ebbd602e2b -->

# Agent de recherche SkyNet pour Android (expérimental)

[English](../../android/README.md) · [中文](../zh/ANDROID.md) · [Español](../es/ANDROID.md) · **Français** · [Deutsch](../de/ANDROID.md) · [Italiano](../it/ANDROID.md) · [Русский](../ru/ANDROID.md) · [Português](../pt/ANDROID.md) · [العربية](../ar/ANDROID.md)

Une application Android qui embarque le même [agent de recherche](../../agent/README.md) que la version de
bureau. Installez un fichier et appuyez sur Démarrer. Par défaut, l'agent signe chaque résultat sur
l'appareil et le publie sans compte ni jeton.
À ce stade, aucune récompense n'est fournie.

**Expérimental.** L'ancienne enveloppe a été testée sur un émulateur Android 14 le 22 novembre
2026. Elle a mené à bien les sept unités de test, attendu la mise en charge et conservé son état
entre les arrêts et les démarrages. L'enveloppe 0.2.0 inclut l'agent 0.2.2. Ses parcours
d'installation et de redémarrage doivent encore être testés sur Android.

## Pour les participants

1. Téléchargez `skynet-agent.apk` depuis la
   page [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases).
2. Ouvrez le fichier. Android vous demande d'autoriser l'installation d'applications depuis votre navigateur ou votre gestionnaire de fichiers.
3. Ouvrez « SkyNet Agent » et appuyez sur **Démarrer**. Une notification permanente indique qu'elle est en cours d'exécution.

- Elle ne travaille que pendant que l'appareil est en charge, sauf si vous cochez « Travailler aussi sur batterie ».
  Le chargeur est vérifié entre les portions de travail : une portion déjà commencée (en général moins d'une
  minute) se termine même si vous débranchez l'appareil.
- Pour reprendre après le redémarrage de l'appareil, activez **Démarrer après le redémarrage**. Cette option est désactivée par
  défaut. Appuyer sur **Arrêter** maintient l'agent à l'arrêt après un redémarrage.
- Sur Android 13 et plus récent, si vous refusez les notifications, l'application fonctionne quand même ; Android ne l'affiche alors que dans la liste des applications en cours d'exécution.
- Les utilisateurs avancés qui sélectionnent `submit_via=github` peuvent saisir un jeton GitHub sur l'écran principal.
- Android 7.0 ou plus récent, un appareil 64 bits, environ 40 Mo.
- Le mode IA facultatif n'est pas disponible dans l'application.
- Pour la supprimer, désinstallez l'application ; rien d'autre n'est laissé sur l'appareil.

## Mise à jour de l'application

Si vous avez la version 0.1.0, installez la 0.2.0 depuis Releases par-dessus l'application existante pour conserver vos
réglages et les résultats en attente. À partir de la 0.2.0, l'ouverture de l'écran vérifie la présence d'un nouvel APK.
Android planifie aussi une vérification quotidienne lorsqu'un réseau est disponible, même si l'agent est
arrêté. Les restrictions de batterie peuvent retarder cette vérification.

L'application vérifie le manifeste de publication signé avec la clé intégrée dans l'APK. Pour une version
compatible plus récente, elle télécharge le fichier de la publication dans le cache privé et vérifie sa taille
et son SHA-256. Appuyez sur le bouton de mise à jour ou sur la notification pour l'installer. Sur Android 8 et plus récent,
autorisez l'installation depuis SkyNet Agent si on vous le demande, revenez à l'application et confirmez dans
l'installateur Android. Si les notifications sont désactivées, utilisez le bouton de l'écran principal.

## En quoi elle diffère de l'agent de bureau

| | Bureau | Application Android |
|---|---|---|
| Code de l'agent | `agent/skynet_agent` | le même paquet, intégré dans l'APK |
| Travail | processus séparés à basse priorité | une unité à la fois dans le processus d'arrière-plan de l'application |
| Limite de temps | le processus de travail est tué | un chien de garde met fin au processus d'arrière-plan ; Android le relance et la tâche est laissée aux appareils plus rapides |
| Mises à jour de l'agent | version signée provenant du dépôt | l'APK vérifie les fichiers signés et le numéro de version. Un nouvel agent a droit à trois démarrages pour réussir un autocontrôle local et accomplir une étape de boucle |
| L'application elle-même | lanceur et installateur | un APK vérifié installé avec votre confirmation |
| Publication | enregistrements signés par défaut | enregistrements signés par défaut |

Limites, en toute franchise. L'APK est signé avec une clé détenue par les mainteneurs du projet ; Android n'accepte une
mise à jour de l'application que si elle est signée avec la même clé. La clé de publication (pour le code de l'agent et
les listes de tâches) et cette clé d'APK sont deux points de confiance uniques que le réseau SkyNet visé
ne doit pas posséder. L'application charge du code Python signé à l'exécution, ce que les règles de Google Play
interdisent ; elle est donc distribuée sous forme de fichier.

## Construire l'application vous-même

Il vous faut JDK 17, le SDK Android (plateforme 34, build-tools 34), Gradle 8.7 et Python 3.12 sur
l'ordinateur de construction.

```sh
cd android
gradle assembleRelease
```

Le résultat est `app/build/outputs/apk/release/app-release-unsigned.apk`. Signez-le avec votre propre
clé (`zipalign`, puis `apksigner sign`) avant de l'installer. Un APK signé par vous-même ne peut pas être
installé par-dessus celui du projet, et inversement.

Ne construisez l'application qu'à partir d'un commit dans lequel `agent/skynet_agent/trust.py` mentionne la clé de publication :
un agent sans clé de publication n'accepte aucune tâche. Dans ce cas, la construction de la version s'arrête avec une
erreur ; `-PallowNoReleaseKey` construit quand même un tel APK, uniquement pour les tests.

Le pont de l'agent et le vérificateur d'APK ont des tests Python de bureau séparés.
[Tests de l'agent](../../agent/tests/test_android_glue.py) · [Tests de mise à jour de l'APK](../../agent/tests/test_apk_update.py)
Python est intégré avec [Chaquopy](https://chaquo.com/chaquopy/) (licence MIT).

## Licence

MIT, comme l'agent : [agent/LICENSE](../../agent/LICENSE).
