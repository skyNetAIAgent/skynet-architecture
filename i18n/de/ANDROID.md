<!-- translation of android/README.md, source sha256: f39e5a1b5b61d6be25ac07b2c69e9f4af5a9bca2ee2ff7cb9610398aebe13e0c -->

# SkyNet-Forschungsagent für Android (experimentell)

[English](../../android/README.md) · [中文](../zh/ANDROID.md) · [Español](../es/ANDROID.md) · [Français](../fr/ANDROID.md) · **Deutsch** · [Italiano](../it/ANDROID.md) · [Русский](../ru/ANDROID.md) · [Português](../pt/ANDROID.md) · [العربية](../ar/ANDROID.md)

Eine Android-App, die dieselben [Go-Rechenkerne](../../agent-go/README.md) wie die Desktop-
Version enthält. Installieren Sie eine Datei und drücken Sie Start. Standardmäßig signiert der Agent jedes Ergebnis auf dem
Gerät und veröffentlicht es ohne Konto oder Token.
In dieser Phase gibt es keine Belohnungen.

**Experimentell.** Shell 0.3.0 enthält Go-Agent 1.0.0 (Engine-Release 7) in der APK. Die Installation
über 0.2.0, der Dienstlebenszyklus und der Neustart müssen unter Android noch getestet werden.

## Für Teilnehmer

1. Laden Sie `skynet-agent.apk` von der Seite
   [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) herunter.
2. Öffnen Sie die Datei. Android fragt Sie, ob Sie die Installation von Apps aus Ihrem Browser oder Dateimanager erlauben möchten.
3. Öffnen Sie „SkyNet Agent“ und drücken Sie **Start**. Eine dauerhafte Benachrichtigung zeigt, dass sie läuft.

- Sie arbeitet nur, während das Gerät geladen wird, außer Sie aktivieren „Auch im Akkubetrieb arbeiten“.
  Das Trennen vom Strom bricht das aktuelle Arbeitsstück ab und lässt es für einen späteren Lauf verfügbar.
- Nachdem Sie einmal **Start** gedrückt haben, startet der Agent auch nach einem Neustart des Geräts erneut
  (**Start after reboot** ist standardmäßig aktiviert; deaktivieren Sie das Kontrollkästchen, um dies auszuschalten). Ein Druck auf **Stop** hält
  den Agenten über einen Neustart hinweg gestoppt.
- Unter Android 13 und neuer funktioniert die App auch dann, wenn Sie Benachrichtigungen ablehnen; Android zeigt sie dann
  nur in der Liste der laufenden Apps.
- Wenn ein vorhandenes Profil `submit_via=github` verwendet, bleiben seine Ergebnisse in der Warteschlange. Diese Version
  unterstützt die Veröffentlichung über signierte Netzwerk-Datensätze.
- Android 7.0 oder neuer auf arm64-v8a oder x86_64.
- Der optionale KI-Modus ist in der App nicht verfügbar.
- Zum Entfernen deinstallieren Sie die App; sonst bleibt nichts auf dem Gerät zurück.

## Die App aktualisieren

Installieren Sie 0.3.0 mit derselben Paketsignatur über die bestehende App, um Ihre Geräteidentität,
Einstellungen, Fortschritt und in der Warteschlange befindlichen Ergebnisse zu behalten. Ab 0.2.0 prüft das Öffnen des Bildschirms auf eine neue APK.
Android plant außerdem eine tägliche Prüfung, wenn ein Netzwerk verfügbar ist, auch wenn der Agent gestoppt ist. Akkubeschränkungen können diese Prüfung verzögern.

Die App prüft das signierte Release-Manifest mit dem in der APK enthaltenen Schlüssel. Für eine neuere kompatible Version lädt sie das Release-Artefakt in den privaten Cache und prüft dessen Größe und SHA-256. Tippen Sie auf die Update-Schaltfläche oder die Benachrichtigung, um es zu installieren. Unter Android 8 und neuer erlauben Sie die Installation aus SkyNet Agent, wenn Sie dazu aufgefordert werden; kehren Sie dann zur App zurück und bestätigen Sie im Android-Installer. Bei deaktivierten Benachrichtigungen verwenden Sie die Schaltfläche auf dem Hauptbildschirm.

## Agent und Aktualisierungen

Der Vordergrunddienst startet die extrahierte ausführbare Datei im Verzeichnis der nativen Bibliotheken.
Er führt jeweils einen Worker mit niedriger Priorität aus und hält während der Berechnung einen Wake-Lock. Ein
Worker, der das Zeitlimit überschreitet, wird beendet, und der Agent überspringt diese Aufgabe vorübergehend. Neue Aufgaben kommen
über den signierten Aufgabenindex. Neuer ausführbarer Code kommt mit einem App-Update.

Android prüft bei der Installation das Signaturzertifikat der APK. Der separate Release-Schlüssel
authentifiziert den Aufgabenindex und das Download-Manifest der APK. Die App prüft Größe, SHA-256, Paketnamen und Versionscode
der APK, bevor sie den Installer öffnet.

## Selbst bauen

Unter Linux installieren Sie Go 1.27.4 mit Quellen, Bash, GNU patch, coreutils, file und readelf
(binutils). Zum Bauen der APK brauchen Sie außerdem JDK 17, Gradle 8.7 und Android SDK 34.

```sh
cd android
gradle assembleRelease
```

Gradle ruft `./build-go.sh` auf. Führen Sie dieses Skript direkt aus, um nur die beiden
ausführbaren Dateien `app/src/main/jniLibs/<abi>/libskynet.so` zu bauen. Es verwendet `GOOS=android`,
`CGO_ENABLED=0` und PIE für beide ABIs. Der arm64-Build verwendet das unveränderte Go. Für den
x86_64-Emulator-Build aktiviert das Skript internes Linken in einer temporären Kopie der
Host-Build-Tools von Go 1.27.4. Es prüft die Architektur, den Einstiegspunkt und den
Interpreter `/system/bin/linker64`, bevor es eine der beiden Dateien installiert.

Die Release-APK ist `app/build/outputs/apk/release/app-release-unsigned.apk`. Verwenden Sie
`zipalign`, dann `apksigner sign` mit demselben Schlüssel wie bei der vorherigen APK für Upgrades an Ort und Stelle. Erzeugen und signieren Sie `android/latest.json` aus der final signierten APK mit
`tools/make_apk_manifest.py`.

## Lizenz

MIT, wie der Agent: [agent/LICENSE](../../agent/LICENSE).
