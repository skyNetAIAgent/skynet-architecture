<!-- translation of android/README.md, source sha256: dd56c64ec3931fa625cd383ec84dcdb5618d80f9faca47d3c9a52cd30294927e -->

# SkyNet-Forschungsagent für Android (experimentell)

[English](../../android/README.md) · [中文](../zh/ANDROID.md) · [Español](../es/ANDROID.md) · [Français](../fr/ANDROID.md) · **Deutsch** · [Italiano](../it/ANDROID.md) · [Русский](../ru/ANDROID.md) · [Português](../pt/ANDROID.md) · [العربية](../ar/ANDROID.md)

Eine Android-App, die denselben [Forschungsagenten](../../agent/README.md) wie die Desktop-Version enthält. Sie ist für Menschen gedacht, die Termux nicht einrichten möchten: eine Datei installieren, Start drücken. In dieser Phase gibt es keine Belohnungen.

**Status: experimentell.** Am 22. November 2026 wurde die App auf einem Android-14-Emulator (x86_64) gegen ein lokales Test-Repository geprüft, das mit einem Testschlüssel signiert ist: Sie installierte sich, startete, prüfte die Signaturen, berechnete alle 7 Stücke der Testaufgaben ohne Fehler, wartete, während der Emulator nicht am Ladegerät hing, arbeitete im Hintergrund weiter, speicherte einen Token und erreichte damit die echte GitHub-API, und sie wurde beendet und erneut gestartet, wobei ihr Zustand erhalten blieb. Ein reiner ARM-Build (`arm64-v8a`) tat auf diesem Emulator über dessen ARM-Übersetzung dasselbe. Der Python-Teil besteht die Tests auch auf einem Computer. **Auf einem echten Telefon wurde sie noch nicht überprüft**, nicht unter Android 7–13, nicht in langen Läufen und nicht gegen die Akkusparer der Telefonhersteller. Den Agenten in [Termux](../../agent/README.md#install) auszuführen, bleibt der andere Weg.

## Für Teilnehmer

1. Laden Sie `skynet-agent.apk` von der Seite [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) herunter.
2. Öffnen Sie die Datei. Android fragt Sie, ob Sie die Installation von Apps aus Ihrem Browser oder Dateimanager erlauben möchten.
3. Öffnen Sie „SkyNet Agent“ und drücken Sie **Start**. Eine dauerhafte Benachrichtigung zeigt, dass sie läuft.

Was Sie wissen sollten:

- Sie arbeitet nur, während das Gerät geladen wird, außer Sie aktivieren „Auch im Akkubetrieb arbeiten“. Das Ladegerät wird zwischen den Arbeitsstücken geprüft: Ein begonnenes Stück (normalerweise unter einer Minute) wird auch dann zu Ende geführt, wenn Sie das Gerät vom Strom trennen.
- Nach einem Neustart des Geräts startet sie nicht von selbst: Öffnen Sie die App und drücken Sie erneut Start.
- Unter Android 13 und neuer funktioniert die App auch dann, wenn Sie Benachrichtigungen ablehnen; Android zeigt sie dann nur in der Liste der laufenden Apps.
- Zum Veröffentlichen von Ergebnissen braucht sie einen GitHub-Token: Öffnen Sie in GitHub Einstellungen → Entwicklereinstellungen → Persönliche Zugriffstokens, erstellen Sie einen Token, der Issues öffentlicher Repositories schreiben darf, und fügen Sie ihn in die App ein. Der Token wird nur innerhalb der App gespeichert. Ohne Token warten die Ergebnisse auf dem Gerät (bis zu 300, dann hört die App auf zu rechnen).
- Android 7.0 oder neuer, ein 64-Bit-Gerät, etwa 40 MB.
- Der optionale KI-Modus ist in der App nicht verfügbar.
- Zum Entfernen deinstallieren Sie die App; sonst bleibt nichts auf dem Gerät zurück.

## Wie sie sich vom Desktop-Agenten unterscheidet

| | Desktop | Android-App |
|---|---|---|
| Agent-Code | `agent/skynet_agent` | dasselbe Paket, in die APK eingebaut |
| Arbeit | getrennte Prozesse mit niedriger Priorität | ein Stück nach dem anderen im Hintergrundprozess der App |
| Zeitlimit | der Arbeitsprozess wird beendet | ein Wächter beendet den Hintergrundprozess; Android startet ihn neu, und die Aufgabe bleibt schnelleren Geräten überlassen |
| Agent-Updates | signierte Version aus dem Repository | dieselbe signierte Version, geprüft vom in die APK eingebauten Code: Signatur, jede Datei, keine Datei außerhalb der signierten Liste, niemals unter der höchsten Version, die hier bereits funktioniert hat. Eine neue Version erhält drei Versuche, das Repository zu erreichen; andernfalls kehrt die App zum eingebauten Code zurück |
| Die App selbst | Startprogramm und Installationsprogramm | ändert sich nur mit einer neuen APK |
| Veröffentlichung | Anmeldung über die GitHub-CLI | ein in die App eingefügter Token |

Ehrliche Grenzen. Die APK ist mit einem Schlüssel signiert, den die Maintainer des Projekts besitzen; Android akzeptiert ein Update der App nur, wenn es mit demselben Schlüssel signiert ist. Der Release-Schlüssel (für Agent-Code und Aufgabenlisten) und dieser APK-Schlüssel sind zwei einzelne Vertrauenspunkte, die das Zielnetz SkyNet nicht haben darf. Die App lädt zur Laufzeit signierten Python-Code, was die Regeln von Google Play nicht erlauben; daher wird sie als Datei verteilt.

## Selbst bauen

Sie brauchen JDK 17, das Android SDK (platform 34, build-tools 34), Gradle 8.7 und Python 3.12 auf dem Build-Rechner.

```sh
cd android
gradle assembleRelease
```

Das Ergebnis ist `app/build/outputs/apk/release/app-release-unsigned.apk`. Signieren Sie es vor der Installation mit Ihrem eigenen Schlüssel (`zipalign`, dann `apksigner sign`). Eine selbst signierte APK kann nicht über die des Projekts installiert werden, und umgekehrt.

Bauen Sie die App nur aus einem Commit, in dem `agent/skynet_agent/trust.py` den Release-Schlüssel aufführt: Ein Agent ohne Release-Schlüssel nimmt keine Aufgaben an. Der Release-Build bricht in diesem Fall mit einem Fehler ab; `-PallowNoReleaseKey` baut eine solche APK trotzdem, nur für Tests.

Der Python-Teil der App ist [`app/src/main/python/skynet_android.py`](../../android/app/src/main/python/skynet_android.py). Er wird auf einem Computer von [`agent/tests/test_android_glue.py`](../../agent/tests/test_android_glue.py) getestet. Python wird mit [Chaquopy](https://chaquo.com/chaquopy/) (MIT-Lizenz) eingebettet.

## Lizenz

MIT, wie der Agent: [agent/LICENSE](../../agent/LICENSE).
