# Agente di ricerca SkyNet

[English](../../agent/README.md) · [中文](../zh/AGENT.md) · [Español](../es/AGENT.md) · [Français](../fr/AGENT.md) · [Deutsch](../de/AGENT.md) · **Italiano** · [Русский](../ru/AGENT.md) · [Português](../pt/AGENT.md) · [العربية](../ar/AGENT.md)

Per aiutare a progettare SkyNet non serve un assistente di IA. L'agente di ricerca è un piccolo programma open source. Controlla periodicamente questo repository, prende compiti di ricerca, li calcola sul vostro computer nel tempo libero e pubblica i risultati.

**In questa fase non sono previste ricompense**: né crediti, né denaro, né promesse di pagamenti futuri. È un aiuto volontario alla ricerca. L'agente non è la rete SkyNet; è uno strumento per progettarla.

## Cosa fa e cosa non fa mai

| Fa | Non fa mai |
|---|---|
| Legge dal repository l'elenco firmato dei compiti e la descrizione firmata della versione | Eseguire codice proveniente da un compito. Un compito è il nome di un calcolo incorporato più dei numeri |
| Esegue i calcoli incorporati con la priorità di CPU più bassa, uno alla volta per impostazione predefinita | Lavorare a batteria, a meno che non lo permettiate |
| Pubblica ogni risultato come commento su GitHub con il vostro account | Inviare i vostri file, identificativi hardware o altro dal vostro computer |
| Si aggiorna da solo, ma solo a una versione firmata con la chiave di rilascio del progetto | Installare un aggiornamento con firma errata, impronta di un file errata o numero più vecchio |
| Tiene tutto in un'unica cartella del vostro profilo | Richiedere diritti di amministratore o avviarsi da solo se non attivate l'avvio automatico |

I primi compiti sono calcoli esatti sulle regole di pagamento di SkyNet. Per esempio: «un partecipante che lascia la rete può guadagnare con una raffica di risultati falsi, e a partire da quale quota di verificatori in collusione?». Ogni dispositivo deve ottenere le stesse cifre, e i risultati di persone diverse vengono confrontati. Vedere [tasks/README.md](../../tasks/README.md).

## Requisiti

- Python 3.9 o successivo. Nient'altro: l'agente usa solo la libreria standard di Python.
- Un account GitHub per pubblicare i risultati (gratuito). Senza account potete comunque calcolare e pubblicare a mano tramite un link.
- Qualche megabyte di spazio su disco e una connessione a internet.

## Installazione

**Windows** (PowerShell):

```powershell
irm https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.ps1 | iex
```

**Linux e macOS** (terminale):

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

**Android, l'app (sperimentale)**: scaricate `skynet-agent.apk` dalla pagina [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases), consentite al browser di installare app e aprite il file. L'app lavora solo mentre il dispositivo è in carica; i risultati vengono pubblicati con un token GitHub che incollate nell'app. Non ancora verificata su un dispositivo reale. Codice sorgente e dettagli: [android/README.md](../../android/README.md).

**Android**: installate l'app [Termux](https://termux.dev) da F-Droid, apritela ed eseguite:

```sh
pkg install python curl
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

Su un telefono l'agente lavora solo mentre il telefono è in carica. Se non riesce a capire se il telefono è in carica, attende e lo segnala; in tal caso installate l'app Termux:API insieme a `pkg install termux-api`, oppure consentite l'uso della batteria: `skynet-agent config set run_on_battery true`.

Se preferite leggere prima di eseguire: scaricate [`install.py`](../../agent/install.py), leggetelo (è breve) ed eseguite `python3 -I install.py`.

Il programma di installazione mette l'agente in una cartella (`%LOCALAPPDATA%\SkyNetAgent` su Windows, `~/Library/Application Support/SkyNetAgent` su macOS, `~/.local/share/skynet-agent` su Linux e Android) e crea il comando `skynet-agent`. Non avvia nulla.

## Primi passi

```sh
skynet-agent selftest --online    # controllare il dispositivo e le firme
skynet-agent github               # vedere con quale account GitHub saranno pubblicati i risultati
skynet-agent run                  # lavorare finché non premete Ctrl+C
skynet-agent autostart enable     # facoltativo: avviarsi all'accesso
```

Su Windows il comando è il file `skynet-agent.cmd` nella cartella dell'agente; il programma di installazione stampa la riga esatta.

### Pubblicazione dei risultati

I risultati sono commenti nella issue di tracciamento del compito in questo repository, pubblicati dal vostro account GitHub. Il modo più semplice per accedere è lo strumento a riga di comando di GitHub:

1. Installate [GitHub CLI](https://cli.github.com) (`winget install GitHub.cli`, `brew install gh`, `pkg install gh` in Termux, o il gestore di pacchetti del vostro Linux).
2. Eseguite `gh auth login` e seguite le istruzioni nel browser.
3. Eseguite `skynet-agent github`. Stampa il nome dell'account.

L'agente chiede l'accesso a `gh` quando gli serve e non conserva né password né token. Alternative: mettere un token nella variabile d'ambiente `SKYNET_GITHUB_TOKEN`, oppure pubblicare a mano: `skynet-agent outbox link` stampa dei link che aprono una pagina GitHub già compilata in cui basta premere un pulsante.

Perché le issue restino leggibili, i risultati di un compito vengono pubblicati insieme: al massimo un commento all'ora, ciascuno con più risultati.

Un risultato pubblicato ha questo aspetto e non contiene altro:

```json
{"agent":"0.1.0","elapsed_s":41.2,"kernel":"exit-scam-a@1","platform":"linux-amd64-py3.12",
 "result":{"count":364838,"digest":"…","hits":0,"…":"…"},"result_sha256":"…","seq":1,
 "task":"exit-a-honest-check","unit":17,"units":256,"v":1}
```

## Comandi

| Comando | Cosa fa |
|---|---|
| `skynet-agent run` | Lavora finché non viene fermato. `--once` esegue una porzione di lavoro ed esce |
| `skynet-agent status` | Versione, impostazioni, contatori, risultati in attesa, ultimo problema |
| `skynet-agent tasks` | I compiti pubblicati ora e ciò che questo dispositivo ha fatto |
| `skynet-agent pause` / `resume` | Non prendere nuovi compiti / riprenderli |
| `skynet-agent stop` | Chiedere all'agente in esecuzione di uscire |
| `skynet-agent outbox` | Risultati in attesa di pubblicazione (`list`, `show`, `send`, `link`, `approve`, `drop`) |
| `skynet-agent config show` / `set CHIAVE VALORE` | Impostazioni |
| `skynet-agent update` | Installare subito l'ultima versione firmata |
| `skynet-agent selftest [--online]` | Controllare il dispositivo, i file installati e le firme |
| `skynet-agent autostart enable` / `disable` | Avviarsi all'accesso oppure no |
| `skynet-agent uninstall --yes` | Disattivare l'avvio automatico e fermarsi; poi eliminate la cartella dell'agente |

## Impostazioni

| Impostazione | Predefinito | Significato |
|---|---|---|
| `workers` | 1 | Compiti eseguiti contemporaneamente; ciascuno usa circa un core della CPU |
| `run_on_battery` | false | Lavorare a batteria |
| `poll_minutes` | 30 | Ogni quanto controllare il repository |
| `update` | auto | `auto` installa gli aggiornamenti firmati, `notify` li segnala soltanto, `off` li ignora. Una pausa chiesta dai responsabili vale in ogni modalità |
| `submit` | auto | `auto` pubblica i risultati, `manual` li tiene nella posta in uscita |
| `max_task_minutes` | 120 | Durata massima di una porzione di lavoro |
| `batch_minutes` | 60 | I risultati di un compito sono pubblicati insieme, al massimo un commento ogni tanti minuti |
| `max_submissions_per_day` | 48 | Massimo di commenti pubblicati al giorno da questo dispositivo |
| `report_platform` | true | Aggiungere ai risultati un'etichetta approssimativa come `windows-amd64-py3.12` |
| `ai.enabled` | false | Modalità IA facoltativa, vedere sotto |

Esempio: `skynet-agent config set workers 4`.

## Facoltativo: rispondere a domande di ricerca con il proprio modello di IA locale

Se sul vostro computer fate girare un modello aperto (per esempio con Ollama, il server llama.cpp o LM Studio), l'agente può passargli le domande di ricerca dell'elenco dei compiti e pubblicare le risposte. È disattivato per impostazione predefinita ed è sperimentale.

```sh
skynet-agent ai                               # mostra il server locale e il modello che userebbe
skynet-agent config set ai.enabled true
```

- L'agente non scarica e non avvia alcun modello. Parla solo con un server sul vostro computer, a meno che non impostiate `ai.allow_remote`.
- La domanda e i documenti che cita provengono dall'elenco firmato dei compiti; ogni documento viene confrontato con la sua impronta prima che il modello lo veda.
- Ogni risposta attende nella posta in uscita finché non la guardate: `skynet-agent outbox show NOME`, poi `skynet-agent outbox approve NOME`. Per pubblicare senza revisione: `skynet-agent config set ai.review_before_submit false`.
- Le risposte sono pubblicate come generate da una macchina e non verificate.

## Sicurezza, onestamente

- **Gli aggiornamenti e gli elenchi dei compiti sono firmati** (Ed25519). L'agente li accetta solo se la firma corrisponde a una chiave di rilascio incorporata nella copia installata, il numero di versione è superiore a quello attuale e ogni file corrisponde al suo SHA-256. Un mirror o una cattiva connessione non cambiano nulla.
- **I compiti sono dati, non programmi.** I nuovi tipi di calcolo arrivano solo dentro una versione firmata, come codice Python leggibile in [`skynet_agent/kernels`](../../agent/skynet_agent/kernels).
- **L'agente gira nella modalità isolata di Python**, e ogni porzione di lavoro va in un processo separato a bassa priorità con un limite di tempo.
- **Se una nuova versione non parte**, il programma di avvio torna alla precedente e ricorda di non installare più quella versione.
- **Di cosa bisogna fidarsi.** Chi possiede la chiave di rilascio può distribuire codice a tutti gli agenti installati. In questa fase di ricerca la chiave è detenuta dai responsabili del progetto. Se non volete aggiornamenti automatici, eseguite `skynet-agent config set update notify` e aggiornate a mano dopo aver letto le modifiche. La primissima installazione si fida della connessione HTTPS con GitHub. Nella rete SkyNet una chiave simile non deve esistere; questo agente è uno strumento di ricerca e non soddisfa ancora i requisiti di SkyNet. Dettagli e tabella delle minacce: [docs/RESEARCH_AGENT.md](../../docs/RESEARCH_AGENT.md) (in russo).

## Riservatezza

L'agente contatta solo GitHub: scarica file pubblici di questo repository (GitHub vede il vostro indirizzo IP, come per qualsiasi visita) e, se avete effettuato l'accesso, pubblica i risultati con il vostro account. Un risultato contiene il nome del compito, il numero della porzione, i numeri calcolati, il tempo impiegato e, a meno che non disattiviate `report_platform`, un'etichetta approssimativa della piattaforma. Non viene raccolto nulla sui vostri file, sulla vostra rete o sul vostro hardware.

## Quanto vi costa

L'elettricità di un core della CPU occupato per impostazione predefinita, alla priorità più bassa, così gli altri programmi non rallentano. Su un telefono la batteria non viene usata a meno che non lo permettiate; tenete il telefono in carica.

## Rimozione

```sh
skynet-agent uninstall --yes
```

Poi eliminate la cartella dell'agente. Sul vostro computer non è stato cambiato altro.

## Se qualcosa non va

- **«no valid signature from a trusted release key»**: il file scaricato non è quello firmato dai responsabili. L'agente lo rifiuta e continua a lavorare con ciò che ha. Se si ripete per giorni, guardate le issue del repository.
- **`CERTIFICATE_VERIFY_FAILED` su macOS** con Python di python.org: l'agente prova allora da solo con il file dei certificati del sistema. Se l'errore resta, eseguite l'`Install Certificates.command` fornito con quel Python.
- **Python del Microsoft Store (Windows)** lavora con una copia privata di `AppData` e del registro. In questo caso la cartella dell'agente è `SkyNetAgent` nella vostra cartella del profilo, e l'avvio automatico va aggiunto a mano: `skynet-agent autostart enable` spiega come. Non ancora verificato su un dispositivo reale.
- **I risultati restano nella posta in uscita**: eseguite `skynet-agent github`; di solito manca `gh auth login`.
- **Android ferma l'agente in background**: eseguite `termux-wake-lock` in Termux ed escludete Termux dall'ottimizzazione della batteria.

## Cosa è stato provato

La suite di test ([`tests/`](../../agent/tests)) copre firme, aggiornamenti, ritorno alla versione precedente, compiti, pubblicazione e un percorso completo, e viene eseguita automaticamente su Windows, Linux e macOS a ogni modifica (scheda Actions del repository). A mano è stato verificato su Windows 11. Non ancora verificato su un dispositivo reale: Android (Termux) e l'avvio automatico su macOS, Linux e Android. Se qualcosa non funziona sul vostro sistema, aprite una issue.

## Licenza

Il codice dell'agente è sotto [licenza MIT](../../agent/LICENSE).
