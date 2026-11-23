<!-- translation of installer/linux/README.md, source sha256: abf22229c4680552dec4357a2de39a59a6c18c9238e2ff76b46a2952e7d8f0b0 -->

# Programma di installazione per Linux

[English](../../installer/linux/README.md) · [中文](../zh/LINUX_INSTALLER.md) · [Español](../es/LINUX_INSTALLER.md) · [Français](../fr/LINUX_INSTALLER.md) · [Deutsch](../de/LINUX_INSTALLER.md) · **Italiano** · [Русский](../ru/LINUX_INSTALLER.md) · [Português](../pt/LINUX_INSTALLER.md) · [العربية](../ar/LINUX_INSTALLER.md)

Eseguite il singolo file dalla pagina Releases del progetto con il vostro account.

```sh
sh skynet-agent-install.sh
```

Il file contiene la versione firmata dell'agente. L'installazione verifica offline la firma Ed25519 e le impronte dei file. Se Python 3.9 o successivo è nel PATH, il programma di installazione usa quell'interprete. Altrimenti serve una build di CPython con una glibc bloccata per x86_64 o aarch64. **Al momento entrambe le impronte sono in sospeso. Questa build richiede il Python di sistema.**

Il programma di installazione online usa la stessa procedura. Con un valore bloccato e verificato può scaricare il runtime corrispondente da python-build-standalone e controllare lo SHA-256 prima dell'estrazione. Gli interpreti portatili si trovano in `$XDG_DATA_HOME/skynet-agent/python/<sha256>`, normalmente `~/.local/share/skynet-agent/python/<sha256>`. Il comando in `~/.local/bin` e il servizio utente systemd usano l'eseguibile scelto.

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

## Avvio e rimozione

In un terminale, se premete Invio al primo prompt, il servizio parte subito e all'accesso. Se premete Invio al secondo, resta legato alle sessioni di accesso. Senza un terminale, il programma di installazione salta i prompt. Questi comandi rendono le scelte esplicite.

```sh
sh skynet-agent-install.sh --autostart           # Run now and at sign-in
sh skynet-agent-install.sh --autostart --linger  # Also run before login and after logout
sh skynet-agent-install.sh --no-autostart        # Install for manual use
```

Il servizio richiede un gestore utente systemd in esecuzione. Il generatore di servizi firmato 0.2.2 supporta i percorsi con spazi. Il programma di installazione chiede un avvio manuale se un percorso dell'interprete o dell'agente contiene virgolette doppie, una barra rovesciata, un simbolo del dollaro, un segno di percentuale o un'interruzione di riga. Se la politica locale nega la persistenza, il programma di installazione lo segnala e il servizio funziona comunque durante le sessioni di accesso. La persistenza a livello di account può essere modificata separatamente con `loginctl disable-linger "$(id -un)"`. Per un'installazione manuale, iniziate il lavoro con `~/.local/bin/skynet-agent run`.

```sh
~/.local/bin/skynet-agent selftest
~/.local/bin/skynet-agent version
~/.local/bin/skynet-agent uninstall --yes
```

La rimozione disattiva il servizio, ne richiede l'arresto e attende il blocco dell'agente. La chiave di identità, la posta in uscita, i record dei relay in attesa e le impostazioni restano nella cartella dell'agente per la reinstallazione. Per cancellare anche i dati salvati dall'agente, usate `uninstall --yes --purge`. La persistenza è un'impostazione per l'intero account e sopravvive alla rimozione.

## Compilazione e verifica

Dalla radice del repository, usate Python 3.9 o successivo sulla macchina di compilazione.

```sh
sh installer/linux/build.sh
shellcheck -s sh agent/install.sh installer/linux/build.sh installer/linux/smoke.sh
dash -n installer/linux/skynet-agent-install.sh
python3 -I -m unittest discover -s agent/tests -t agent/tests
```

Lo strumento di compilazione autentica la versione con la chiave pubblica in `agent/install.py` e produce `installer/linux/skynet-agent-install.sh`. Per abilitare Python portatile, verificate separatamente ogni archivio upstream e registrate il suo SHA-256 in `python.lock` (un campo per riga). Solo se una voce è nulla, la CI può fornire un digest verificato tramite `SKYNET_PYTHON_SHA256_X86_64` o `SKYNET_PYTHON_SHA256_AARCH64`. Queste sono impostazioni del momento della compilazione. Lo strumento di compilazione verifica e incorpora ogni archivio bloccato. Per compilare offline con valori bloccati, usate `sh installer/linux/build.sh --runtime-dir /path/to/archives`.

Il flusso di lavoro del programma di installazione per Linux esegue il pacchetto come utente senza privilegi e con la rete disattivata. Ubuntu 24.04 mette alla prova il Python di sistema. Debian 12 slim mette alla prova l'interprete portatile quando il digest x86_64 è disponibile e verifica il rifiuto quando è in sospeso. Le installazioni riuscite eseguono l'autotest, riportano la versione e mettono alla prova entrambe le modalità di rimozione. Il flusso di lavoro carica lo script come artefatto di compilazione per la distribuzione manuale.
