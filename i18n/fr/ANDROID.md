<!-- translation of android/README.md, source sha256: dd56c64ec3931fa625cd383ec84dcdb5618d80f9faca47d3c9a52cd30294927e -->

# Agent de recherche SkyNet pour Android (expérimental)

[English](../../android/README.md) · [中文](../zh/ANDROID.md) · [Español](../es/ANDROID.md) · **Français** · [Deutsch](../de/ANDROID.md) · [Italiano](../it/ANDROID.md) · [Русский](../ru/ANDROID.md) · [Português](../pt/ANDROID.md) · [العربية](../ar/ANDROID.md)

Une application Android qui embarque le même [agent de recherche](../../agent/README.md) que la version de bureau. Elle s'adresse à ceux qui ne veulent pas installer Termux : installez un fichier, appuyez sur Démarrer. À ce stade, aucune récompense n'est fournie.

**Statut : expérimental.** Le 22 novembre 2026, l'application a été vérifiée sur un émulateur Android 14 (x86_64) face à un dépôt de test local signé avec une clé de test : elle s'est installée, a démarré, a vérifié les signatures, a calculé sans erreur les 7 portions des tâches de test, a attendu alors que l'émulateur n'était pas en charge, a continué à travailler en arrière-plan, a enregistré un jeton et atteint avec lui la véritable API GitHub, puis s'est arrêtée et relancée en conservant son état. Une version réservée à l'ARM (`arm64-v8a`) a fait de même sur cet émulateur grâce à sa traduction ARM. Sa partie Python réussit aussi les tests sur un ordinateur. **Elle n'a pas encore été vérifiée sur un vrai téléphone**, sur Android 7–13, lors de longues exécutions, ni face aux économiseurs de batterie des fabricants de téléphones. Faire tourner l'agent dans [Termux](../../agent/README.md#install) reste l'autre solution.

## Pour les participants

1. Téléchargez `skynet-agent.apk` depuis la page [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases).
2. Ouvrez le fichier. Android vous demande d'autoriser l'installation d'applications depuis votre navigateur ou votre gestionnaire de fichiers.
3. Ouvrez « SkyNet Agent » et appuyez sur **Démarrer**. Une notification permanente indique qu'elle est en cours d'exécution.

Ce qu'il faut savoir :

- Elle ne travaille que pendant que l'appareil est en charge, sauf si vous cochez « Travailler aussi sur batterie ». Le chargeur est vérifié entre les portions de travail : une portion déjà commencée (en général moins d'une minute) se termine même si vous débranchez l'appareil.
- Elle ne démarre pas d'elle-même après le redémarrage de l'appareil : ouvrez l'application et appuyez de nouveau sur Démarrer.
- Sur Android 13 et plus récent, si vous refusez les notifications, l'application fonctionne quand même ; Android ne l'affiche alors que dans la liste des applications en cours d'exécution.
- Pour publier les résultats, il lui faut un jeton GitHub : dans GitHub, ouvrez Paramètres → Paramètres de développement → Jetons d'accès personnel, créez un jeton pouvant écrire des tickets de dépôts publics et collez-le dans l'application. Le jeton n'est conservé qu'à l'intérieur de l'application. Sans jeton, les résultats attendent sur l'appareil (jusqu'à 300, puis l'application arrête de calculer).
- Android 7.0 ou plus récent, un appareil 64 bits, environ 40 Mo.
- Le mode IA facultatif n'est pas disponible dans l'application.
- Pour la supprimer, désinstallez l'application ; rien d'autre n'est laissé sur l'appareil.

## En quoi elle diffère de l'agent de bureau

| | Bureau | Application Android |
|---|---|---|
| Code de l'agent | `agent/skynet_agent` | le même paquet, intégré dans l'APK |
| Travail | processus séparés à basse priorité | une portion à la fois dans le processus d'arrière-plan de l'application |
| Limite de temps | le processus de travail est tué | un chien de garde met fin au processus d'arrière-plan ; Android le relance et la tâche est laissée aux appareils plus rapides |
| Mises à jour de l'agent | version signée provenant du dépôt | la même version signée, vérifiée par le code intégré dans l'APK : signature, chaque fichier, aucun fichier hors de la liste signée, jamais en dessous de la version la plus haute ayant déjà fonctionné ici. Une nouvelle version a droit à trois essais pour atteindre le dépôt ; sinon, l'application revient au code intégré |
| L'application elle-même | lanceur et installateur | ne change qu'avec un nouvel APK |
| Publication | connexion à GitHub CLI | un jeton collé dans l'application |

Limites, en toute franchise. L'APK est signé avec une clé détenue par les mainteneurs du projet ; Android n'accepte une mise à jour de l'application que si elle est signée avec la même clé. La clé de publication (pour le code de l'agent et les listes de tâches) et cette clé d'APK sont deux points de confiance uniques que le réseau SkyNet visé ne doit pas posséder. L'application charge du code Python signé à l'exécution, ce que les règles de Google Play interdisent ; elle est donc distribuée sous forme de fichier.

## Construire l'application vous-même

Il vous faut JDK 17, le SDK Android (plateforme 34, build-tools 34), Gradle 8.7 et Python 3.12 sur l'ordinateur de construction.

```sh
cd android
gradle assembleRelease
```

Le résultat est `app/build/outputs/apk/release/app-release-unsigned.apk`. Signez-le avec votre propre clé (`zipalign`, puis `apksigner sign`) avant de l'installer. Un APK signé par vous-même ne peut pas être installé par-dessus celui du projet, et inversement.

Ne construisez l'application qu'à partir d'un commit dans lequel `agent/skynet_agent/trust.py` mentionne la clé de publication : un agent sans clé de publication n'accepte aucune tâche. Dans ce cas, la construction de la version s'arrête avec une erreur ; `-PallowNoReleaseKey` construit quand même un tel APK, uniquement pour les tests.

La partie Python de l'application est [`app/src/main/python/skynet_android.py`](../../android/app/src/main/python/skynet_android.py). Elle est testée sur un ordinateur par [`agent/tests/test_android_glue.py`](../../agent/tests/test_android_glue.py). Python est intégré avec [Chaquopy](https://chaquo.com/chaquopy/) (licence MIT).

## Licence

MIT, comme l'agent : [agent/LICENSE](../../agent/LICENSE).
