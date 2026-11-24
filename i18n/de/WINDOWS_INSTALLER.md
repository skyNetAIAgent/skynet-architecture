<!-- translation of installer/windows/README.md, source sha256: ea7cbbbfeb25d77b3a5b0c8e09d4f0869dfa666efd0d84e0755573b22c5206ae -->

# Windows-Desktop-Installationsprogramm

[English](../../installer/windows/README.md) · [中文](../zh/WINDOWS_INSTALLER.md) · [Español](../es/WINDOWS_INSTALLER.md) · [Français](../fr/WINDOWS_INSTALLER.md) · **Deutsch** · [Italiano](../it/WINDOWS_INSTALLER.md) · [Русский](../ru/WINDOWS_INSTALLER.md) · [Português](../pt/WINDOWS_INSTALLER.md) · [العربية](../ar/WINDOWS_INSTALLER.md)

Wählen Sie das amd64- oder arm64-Installationsprogramm für Ihren Computer. Prüfen Sie dessen SHA-256-Wert anhand einer über einen vertrauenswürdigen Kanal bezogenen Prüfsumme. Das Setup installiert das signierte native Release im Profil des aktuellen Benutzers. Das Setup startet den Agenten sofort und bei jeder Windows-Anmeldung; beides kann auf der Seite „Aufgaben“ abgewählt werden. Startmenü-Verknüpfungen rufen den permanenten Launcher auf.

Das Deinstallationsprogramm behält standardmäßig die Identität, die Warteschlangen und den Release-Verlauf. Wählen Sie die Option zum Löschen der Daten, um sie zu entfernen. Während der Migration werden die vorherige signierte Python-Bridge und ihr Interpreter für einen Rollback beibehalten.

## Erstellen und testen

Verwenden Sie Python 3.9+ und Inno Setup 6 auf dem Build-Rechner. Legen Sie das Release-Manifest und die abgetrennte Signatur unter `agent/v2` sowie die zugehörigen Release-Binärdateien unter `dist` ab. Verwenden Sie ein neues Build-Verzeichnis. Der Smoke-Test benötigt ein Wegwerf-Windows-Konto.

~~~powershell
./installer/windows/build.ps1 -BuildDir build -AssetDir dist -Arch amd64
./installer/windows/smoke.ps1 -BuildDir build
~~~
