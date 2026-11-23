<!-- translation of installer/windows/README.md, source sha256: 95e38378255edcbcadd409d118146850d8282a8a66501bbe40381b095e4893d7 -->

# Programma di installazione per Windows x64

[English](../../installer/windows/README.md) · [中文](../zh/WINDOWS_INSTALLER.md) · [Español](../es/WINDOWS_INSTALLER.md) · [Français](../fr/WINDOWS_INSTALLER.md) · [Deutsch](../de/WINDOWS_INSTALLER.md) · **Italiano** · [Русский](../ru/WINDOWS_INSTALLER.md) · [Português](../pt/WINDOWS_INSTALLER.md) · [العربية](../ar/WINDOWS_INSTALLER.md)

Scaricate l'EXE e il file `.exe.sha256` corrispondente dallo stesso rilascio del
progetto. In PowerShell, aprite la cartella dei download e confrontate l'impronta di
controllo. [Releases di GitHub](https://github.com/skyNetAIAgent/skynet-architecture/releases)

```powershell
$file = 'SkyNetAgentSetup-0.2.2.exe'
$expected = ((Get-Content -Raw "$file.sha256") -split '\s+')[0]
if ((Get-FileHash $file -Algorithm SHA256).Hash -ne $expected) { throw 'Checksum mismatch.' }
```

Aprite l'EXE verificato. SmartScreen potrebbe mostrare **Windows ha protetto il PC**
perché il programma di installazione non ha una firma del codice. Scegliete
**Ulteriori informazioni**, confermate il nome del file, quindi scegliete
**Esegui comunque**. L'installazione vale per l'utente corrente. Deselezionate l'una o
l'altra casella di avvio automatico per cambiare quando viene eseguito l'agente.

L'agente accetta aggiornamenti firmati dei propri file. Un programma di installazione
più recente aggiorna il Python incluso. Installate sopra la copia esistente per
conservare l'identità del dispositivo e i risultati in attesa. Anche il programma di
disinstallazione del menu Start li conserva per impostazione predefinita. La sua casella
facoltativa per l'eliminazione dei dati comprende la posta in uscita e i record firmati
in attesa.

## Compilazione e test

Partite da una copia del repository appena scaricata e pulita, con terminazioni di riga
LF per i file firmati. Dalla radice del repository su Windows x64, eseguite PowerShell 7
con una cartella di compilazione nuova. La compilazione cerca Inno Setup 6.3.3 o
successivo nel PATH o nella sua posizione abituale. Se il compilatore manca, usa
Chocolatey per installare la 6.3.3.

```powershell
./installer/windows/build.ps1 -BuildDir build
```

`python.lock` deve contenere la versione di patch 3.12 esatta e lo SHA-256 di 64 cifre
del suo `python-<version>-embed-amd64.zip` ufficiale. Per un nuovo pin, autenticate
l'archivio con le istruzioni e il bundle Sigstore collegati dalla pagina di rilascio di
Python, poi registratene lo SHA-256. Un pin vuoto o non valido ferma la compilazione
prima del download. [Rilascio di Python 3.12.10](https://www.python.org/downloads/release/python-31210/)

La compilazione verifica l'archivio prima dell'estrazione. L'interprete incorporato
prepara solo i file del manifesto di rilascio autenticato. Al momento dell'installazione
controlla di nuovo il bundle, compreso l'elenco dei file, prima di eseguire il candidato.
Il file `python312._pth` in dotazione fornisce la libreria standard. Il programma di
avvio e il controllo del candidato aggiungono la cartella del rilascio scelto a
`sys.path` con `-I`.

Su un profilo Windows usa e getta, senza alcuna installazione di SkyNet esistente,
eseguite il test rapido. Installa in silenzio, controlla la registrazione per l'avvio
all'accesso e la CLI senza Python di sistema nel PATH, poi disinstalla e controlla i dati
conservati.

```powershell
./installer/windows/smoke.ps1 -BuildDir build
```

In alternativa, eseguite **Actions → Windows installer → Esegui flusso di lavoro**. Dopo
che il test rapido è superato, scaricate l'artefatto `SkyNetAgentSetup-x64`. Il suo
`SkyNetAgentSetup-<version>.exe` e il relativo `.exe.sha256` sono i due file da allegare
manualmente al rilascio GitHub corrispondente.
