<!-- translation of android/README.md, source sha256: 3fd07398dc6f1c3ed1d7c21b1315b13e43cdbf629cf72aab3887e8ebbd602e2b -->

# SkyNet-Forschungsagent für Android (experimentell)

[English](../../android/README.md) · [中文](../zh/ANDROID.md) · [Español](../es/ANDROID.md) · [Français](../fr/ANDROID.md) · **Deutsch** · [Italiano](../it/ANDROID.md) · [Русский](../ru/ANDROID.md) · [Português](../pt/ANDROID.md) · [العربية](../ar/ANDROID.md)

Eine Android-App, die denselben [Forschungsagenten](../../agent/README.md) wie die Desktop-Version enthält. Installieren Sie eine Datei und drücken Sie Start. Standardmäßig signiert der Agent jedes Ergebnis auf dem Gerät und veröffentlicht es ohne Konto oder Token. In dieser Phase gibt es keine Belohnungen.

**Experimentell.** Die vorherige Shell wurde am 22. November 2026 auf einem Android-14-Emulator getestet. Sie absolvierte alle sieben Testeinheiten, wartete auf das Laden und behielt ihren Zustand über Stopps und Starts hinweg. Shell 0.2.0 enthält Agent 0.2.2. Ihre Installations- und Neustartabläufe müssen noch unter Android getestet werden.

## Für Teilnehmer

1. Laden Sie `skynet-agent.apk` von der Seite [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) herunter.
2. Öffnen Sie die Datei. Android fragt Sie, ob Sie die Installation von Apps aus Ihrem Browser oder Dateimanager erlauben möchten.
3. Öffnen Sie „SkyNet Agent“ und drücken Sie **Start**. Eine dauerhafte Benachrichtigung zeigt, dass sie läuft.

- Sie arbeitet nur, während das Gerät geladen wird, außer Sie aktivieren „Auch im Akkubetrieb arbeiten“. Das Ladegerät wird zwischen den Arbeitsstücken geprüft: Ein begonnenes Stück (normalerweise unter einer Minute) wird auch dann zu Ende geführt, wenn Sie das Gerät vom Strom trennen.
- Um nach einem Neustart des Geräts fortzufahren, aktivieren Sie **Start after reboot**. Sie ist standardmäßig aus. Ein Druck auf **Stop** hält den Agenten über einen Neustart hinweg gestoppt.
- Unter Android 13 und neuer funktioniert die App auch dann, wenn Sie Benachrichtigungen ablehnen; Android zeigt sie dann nur in der Liste der laufenden Apps.
- Fortgeschrittene Benutzer, die `submit_via=github` auswählen, können auf dem Hauptbildschirm einen GitHub-Token eingeben.
- Android 7.0 oder neuer, ein 64-Bit-Gerät, etwa 40 MB.
- Der optionale KI-Modus ist in der App nicht verfügbar.
- Zum Entfernen deinstallieren Sie die App; sonst bleibt nichts auf dem Gerät zurück.

## Die App aktualisieren

Wenn Sie Version 0.1.0 haben, installieren Sie 0.2.0 aus Releases über die bestehende App, um Ihre Einstellungen und in der Warteschlange befindlichen Ergebnisse zu behalten. Ab 0.2.0 prüft das Öffnen des Bildschirms auf eine neue APK. Android plant außerdem eine tägliche Prüfung, wenn ein Netzwerk verfügbar ist, auch wenn der Agent gestoppt ist. Akkubeschränkungen können diese Prüfung verzögern.

Die App prüft das signierte Release-Manifest mit dem in der APK enthaltenen Schlüssel. Für eine neuere kompatible Version lädt sie das Release-Artefakt in den privaten Cache und prüft dessen Größe und SHA-256. Tippen Sie auf die Update-Schaltfläche oder die Benachrichtigung, um es zu installieren. Unter Android 8 und neuer erlauben Sie die Installation aus SkyNet Agent, wenn Sie dazu aufgefordert werden; kehren Sie dann zur App zurück und bestätigen Sie im Android-Installer. Bei deaktivierten Benachrichtigungen verwenden Sie die Schaltfläche auf dem Hauptbildschirm.

## Wie sie sich vom Desktop-Agenten unterscheidet

| | Desktop | Android-App |
|---|---|---|
| Agent-Code | `agent/skynet_agent` | dasselbe Paket, in die APK eingebaut |
| Arbeit | getrennte Prozesse mit niedriger Priorität | ein Stück nach dem anderen im Hintergrundprozess der App |
| Zeitlimit | der Arbeitsprozess wird beendet | ein Wächter beendet den Hintergrundprozess; Android startet ihn neu, und die Aufgabe bleibt schnelleren Geräten überlassen |
| Agent-Updates | signierte Version aus dem Repository | die APK prüft die signierten Dateien und die Release-Nummer. Ein neuer Agent erhält drei Starts, um eine lokale Selbstprüfung zu bestehen und einen Schleifenschritt abzuschließen |
| Die App selbst | Startprogramm und Installationsprogramm | eine verifizierte APK, die mit Ihrer Bestätigung installiert wird |
| Veröffentlichung | standardmäßig signierte Datensätze | standardmäßig signierte Datensätze |

Ehrliche Grenzen. Die APK ist mit einem Schlüssel signiert, den die Maintainer des Projekts besitzen; Android akzeptiert ein Update der App nur, wenn es mit demselben Schlüssel signiert ist. Der Release-Schlüssel (für Agent-Code und Aufgabenlisten) und dieser APK-Schlüssel sind zwei einzelne Vertrauenspunkte, die das Zielnetz SkyNet nicht haben darf. Die App lädt zur Laufzeit signierten Python-Code, was die Regeln von Google Play nicht erlauben; daher wird sie als Datei verteilt.

## Selbst bauen

Sie brauchen JDK 17, das Android SDK (platform 34, build-tools 34), Gradle 8.7 und Python 3.12 auf dem Build-Rechner.

```sh
cd android
gradle assembleRelease
```

Das Ergebnis ist `app/build/outputs/apk/release/app-release-unsigned.apk`. Signieren Sie es vor der Installation mit Ihrem eigenen Schlüssel (`zipalign`, dann `apksigner sign`). Eine selbst signierte APK kann nicht über die des Projekts installiert werden, und umgekehrt.

Bauen Sie die App nur aus einem Commit, in dem `agent/skynet_agent/trust.py` den Release-Schlüssel aufführt: Ein Agent ohne Release-Schlüssel nimmt keine Aufgaben an. Der Release-Build bricht in diesem Fall mit einem Fehler ab; `-PallowNoReleaseKey` baut eine solche APK trotzdem, nur für Tests.

Die Agent-Bridge und der APK-Prüfer haben separate Desktop-Python-Tests.
[Agent-Tests](../../agent/tests/test_android_glue.py) · [APK-Update-Tests](../../agent/tests/test_apk_update.py)
Python wird mit [Chaquopy](https://chaquo.com/chaquopy/) (MIT-Lizenz) eingebettet.

## Lizenz

MIT, wie der Agent: [agent/LICENSE](../../agent/LICENSE).
