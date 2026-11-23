<!-- translation of installer/windows/README.md, source sha256: 95e38378255edcbcadd409d118146850d8282a8a66501bbe40381b095e4893d7 -->

# Windows-x64-Installationsprogramm

[English](../../installer/windows/README.md) · [中文](../zh/WINDOWS_INSTALLER.md) · [Español](../es/WINDOWS_INSTALLER.md) · [Français](../fr/WINDOWS_INSTALLER.md) · **Deutsch** · [Italiano](../it/WINDOWS_INSTALLER.md) · [Русский](../ru/WINDOWS_INSTALLER.md) · [Português](../pt/WINDOWS_INSTALLER.md) · [العربية](../ar/WINDOWS_INSTALLER.md)

Laden Sie die EXE und die passende Datei `.exe.sha256` aus demselben Release des Projekts herunter. Öffnen Sie in PowerShell den Download-Ordner und vergleichen Sie die Prüfsumme. [GitHub-Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases)

```powershell
$file = 'SkyNetAgentSetup-0.2.2.exe'
$expected = ((Get-Content -Raw "$file.sha256") -split '\s+')[0]
if ((Get-FileHash $file -Algorithm SHA256).Hash -ne $expected) { throw 'Checksum mismatch.' }
```

Öffnen Sie die geprüfte EXE. SmartScreen zeigt möglicherweise **Windows hat den Start dieser App verhindert** an, weil das Installationsprogramm keine Codesignatur hat. Wählen Sie **Weitere Informationen**, bestätigen Sie den Dateinamen und wählen Sie dann **Trotzdem ausführen**. Das Setup installiert für den aktuellen Benutzer. Entfernen Sie das Häkchen in einem der beiden Autostart-Kontrollkästchen, um zu ändern, wann der Agent läuft.

Der Agent akzeptiert signierte Updates für seine eigenen Dateien. Ein neueres Installationsprogramm aktualisiert das mitgelieferte Python. Installieren Sie über die vorhandene Kopie, um die Geräteidentität und wartende Ergebnisse zu behalten. Das Deinstallationsprogramm im Startmenü behält diese standardmäßig ebenfalls. Sein optionales Kontrollkästchen zum Löschen der Daten umfasst den Postausgang und wartende signierte Datensätze.

## Erstellen und testen

Verwenden Sie einen sauberen Checkout mit LF-Zeilenenden für die signierten Dateien. Führen Sie im Stammordner des Repositorys unter Windows x64 PowerShell 7 mit einem neuen Build-Verzeichnis aus. Der Build prüft, ob Inno Setup 6.3.3 oder neuer im PATH oder am üblichen Ort vorhanden ist. Fehlt der Compiler, wird 6.3.3 mit Chocolatey installiert.

```powershell
./installer/windows/build.ps1 -BuildDir build
```

`python.lock` muss die genaue Patch-Version von 3.12 und den 64-stelligen SHA-256-Wert der offiziellen Datei `python-<version>-embed-amd64.zip` enthalten. Für eine neue Festlegung authentifizieren Sie das Archiv mit den Anweisungen und dem Sigstore-Bundle, die auf der Python-Release-Seite verlinkt sind, und tragen Sie dann seinen SHA-256-Wert ein. Eine leere oder ungültige Festlegung stoppt den Build vor dem Download. [Python-Release 3.12.10](https://www.python.org/downloads/release/python-31210/)

Der Build prüft das Archiv vor dem Entpacken. Der eingebettete Interpreter übernimmt nur Dateien aus dem authentifizierten Release-Manifest. Bei der Installation prüft er das Bundle erneut, einschließlich seiner Dateiliste, bevor er den Kandidaten ausführt. Die mitgelieferte `python312._pth` liefert die Standardbibliothek. Starter und Kandidatenprüfung fügen das ausgewählte Release-Verzeichnis unter `-I` zu `sys.path` hinzu.

Führen Sie den Smoke-Test in einem Wegwerf-Windows-Profil ohne vorhandene SkyNet-Installation aus. Er installiert still, prüft die Anmeldung und die CLI ohne System-Python im PATH, deinstalliert danach und prüft die behaltenen Daten.

```powershell
./installer/windows/smoke.ps1 -BuildDir build
```

Alternativ führen Sie **Actions → Windows installer → Run workflow** aus. Laden Sie nach erfolgreichem Smoke-Test das Artefakt `SkyNetAgentSetup-x64` herunter. Seine Dateien `SkyNetAgentSetup-<version>.exe` und `.exe.sha256` sind die beiden Assets, die von Hand an das passende GitHub-Release angehängt werden müssen.
