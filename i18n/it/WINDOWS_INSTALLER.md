<!-- translation of installer/windows/README.md, source sha256: ea7cbbbfeb25d77b3a5b0c8e09d4f0869dfa666efd0d84e0755573b22c5206ae -->

# Programma di installazione desktop per Windows

[English](../../installer/windows/README.md) · [中文](../zh/WINDOWS_INSTALLER.md) · [Español](../es/WINDOWS_INSTALLER.md) · [Français](../fr/WINDOWS_INSTALLER.md) · [Deutsch](../de/WINDOWS_INSTALLER.md) · **Italiano** · [Русский](../ru/WINDOWS_INSTALLER.md) · [Português](../pt/WINDOWS_INSTALLER.md) · [العربية](../ar/WINDOWS_INSTALLER.md)

Scegliete il programma di installazione amd64 o arm64 per il vostro computer.
Verificate il suo SHA-256 usando un'impronta di controllo ottenuta tramite un canale
attendibile. L'installazione colloca il rilascio nativo firmato nel profilo dell'utente
corrente. L'installazione avvia subito l'agente e a ogni accesso a Windows; entrambe le
opzioni possono essere deselezionate nella pagina delle attività.
I collegamenti nel menu Start richiamano il programma di avvio permanente.

Il programma di disinstallazione conserva per impostazione predefinita identità, code e
cronologia dei rilasci. Selezionate l'opzione di eliminazione dei dati per rimuoverli.
Durante la migrazione il precedente bridge Python firmato e il suo interprete vengono
conservati per il rollback.

## Compilazione e test

Usate Python 3.9+ e Inno Setup 6 sulla macchina di compilazione. Preparate il manifesto
di rilascio e la firma separata sotto `agent/v2` e i binari di rilascio corrispondenti
sotto `dist`. Usate una cartella di compilazione nuova. Il test rapido richiede un
account Windows usa e getta.

~~~powershell
./installer/windows/build.ps1 -BuildDir build -AssetDir dist -Arch amd64
./installer/windows/smoke.ps1 -BuildDir build
~~~
