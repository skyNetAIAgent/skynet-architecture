# Agente di ricerca SkyNet

[English](../../agent/README.md) · [中文](../zh/AGENT.md) · [Español](../es/AGENT.md) · [Français](../fr/AGENT.md) · [Deutsch](../de/AGENT.md) · **Italiano** · [Русский](../ru/AGENT.md) · [Português](../pt/AGENT.md) · [العربية](../ar/AGENT.md)

Potete aiutare a progettare SkyNet facendo fare al vostro computer una parte della ricerca. L'agente è un piccolo programma open source. Controlla questo repository alla ricerca di compiti, esegue una porzione di un calcolo e condivide il risultato. Potete anche pubblicare una domanda di ricerca o rispondere a quella di qualcun altro sulla bacheca dei compiti. Non serve alcun account né un assistente di IA. [Guida della bacheca dei compiti](BOARD.md)

**In questa fase non sono previste ricompense.** Non ci sono crediti, pagamenti né promesse di pagamenti futuri. È ricerca volontaria per aiutare a progettare la rete SkyNet.

## Cosa fa e cosa non fa mai

| Fa | Non fa mai |
|---|---|
| Legge un elenco firmato di compiti. Ogni compito indica un calcolo incorporato e fornisce i suoi dati di input | Esegue codice proveniente da un compito o da un post della bacheca |
| Per impostazione predefinita esegue una porzione di lavoro alla volta, con priorità di CPU bassa | Avvia una nuova porzione quando rileva l'alimentazione a batteria, per impostazione predefinita |
| Firma i risultati con la chiave di questo dispositivo e, per impostazione predefinita, li invia a relay pubblici e a un nodo completo | Include i vostri file personali o identificativi hardware in un risultato automatico |
| Controlla la firma del progetto prima di installare un aggiornamento desktop | Accetta un aggiornamento scaricato con una firma non valida, un'impronta del file errata o un numero di versione più vecchio |
| Si installa nel vostro account utente e vi lascia scegliere se avviarsi all'accesso | Richiede diritti di amministratore per una normale installazione desktop |

Una domanda di ricerca è se un partecipante che sta per andarsene possa trarre profitto da una raffica di risultati falsi. Quanti verificatori dovrebbero essere in collusione? Dispositivi diversi a cui viene data la stessa porzione di quel calcolo devono ottenere esattamente la stessa risposta, così i loro risultati possono essere confrontati. [Compiti di ricerca](../../tasks/README.md)

## Requisiti

- Windows su x64 (amd64) o ARM64, oppure Linux su amd64, arm64 o ARMv7. L'agente desktop nella versione 1.0.1 è un singolo programma Go. I programmi di installazione della pagina Releases includono l'eseguibile, pronto da eseguire. macOS non è supportato.
- Per l'app Android sperimentale, Android 7.0 o successivo su arm64-v8a o x86_64.
- Una connessione a internet per ricevere nuovi compiti e pubblicare i risultati. Il programma di installazione Linux della pagina Releases può installare offline.

## Installazione

**Windows**

1. Scegliete dalla pagina [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) il programma di installazione per Windows (`.exe`) adatto al vostro computer, amd64 o arm64.
2. Confrontate il checksum SHA-256 del file con quello proveniente da una fonte di cui vi fidate, poi eseguite il programma di installazione. Potete scegliere di avviare l'agente subito e di avviarlo all'accesso. Il programma di installazione aggiunge scorciatoie al menu Start. [Guida del programma di installazione per Windows](../../installer/windows/README.md)

**Linux**

Scaricate `skynet-agent-install.sh` dalla pagina [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) ed eseguite `sh skynet-agent-install.sh` come utente normale. Il file include gli eseguibili per tutte e tre le architetture Linux supportate.

Potete anche installare dalla rete con il comando seguente. Richiede `curl`, `jq`, `xxd`, `sha256sum` e OpenSSL con supporto Ed25519.

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

Per impostazione predefinita, il programma di installazione mantiene l'impostazione di avvio all'accesso esistente. In una nuova installazione, avviate voi stessi l'agente con `skynet-agent run`. Per avviarlo subito e all'accesso, eseguite `sh skynet-agent-install.sh --autostart`. Questo usa il vostro servizio utente systemd. Aggiungete `--linger` per l'avvio dall'accensione e dopo la disconnessione, oppure usate `--no-autostart` per disattivare il servizio. Se la vostra shell non trova il comando, usate `~/.local/bin/skynet-agent`. [Guida del programma di installazione per Linux](../../installer/linux/README.md)

**Android (sperimentale)**

Scaricate `skynet-agent.apk` dalla pagina [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases). Aprite il file e consentite l'installazione dal browser o dal gestore file quando Android lo chiede. Aprite **SkyNet Agent** e toccate **Avvia**. Per impostazione predefinita calcola solo mentre è in carica. **Avvia dopo il riavvio** è disattivato per impostazione predefinita.

L'APK ha un proprio numero di versione. La versione 0.3.0 dell'app include l'agente Go 1.0.0. L'app propone gli aggiornamenti sulla sua schermata o in una notifica. Controlla la descrizione firmata della versione e le dimensioni e lo SHA-256 dell'APK prima di chiedervi di confermare l'installazione in Android. [Guida Android](../../android/README.md)

La chiave del dispositivo, le impostazioni e i risultati si trovano nella cartella dell'agente. Il percorso predefinito è `%LOCALAPPDATA%\SkyNetAgent` su Windows e `~/.local/share/skynet-agent` su Linux (oppure `$XDG_DATA_HOME/skynet-agent` se impostata). Il programma di installazione Linux accetta anche `SKYNET_AGENT_HOME` o `--home DIR` per scegliere un'altra cartella. Android conserva il proprio profilo nello spazio privato dell'app.

Se eseguite già l'agente Python su un desktop supportato con gli aggiornamenti automatici attivi, passa da solo a Go tramite la versione ponte firmata **0.4.0**. Conserva la chiave del dispositivo, i progressi e i risultati non inviati. La versione ponte precedente e il suo interprete vengono conservati per il ritorno alla versione precedente.

## Primi passi

Su Linux, usate i comandi seguenti. Su Windows, aprite PowerShell nella cartella dell'agente e usate `.\skynet-agent.exe launch` al posto di `skynet-agent`. Per esempio, `.\skynet-agent.exe launch status` mostra il vostro stato tramite il programma di avvio permanente.

```sh
skynet-agent verify-install       # controllare i file della versione installata ed eseguire un calcolo di prova
skynet-agent selftest --online    # eseguire il calcolo e controllare online i documenti firmati
skynet-agent net id               # mostrare la chiave pubblica di questo dispositivo, il suo nome sulla bacheca
skynet-agent run                  # se non è già in esecuzione, lavorare finché non premete Ctrl+C
```

Usate `skynet-agent autostart status` per vedere se l'avvio all'accesso è attivo. Per attivarlo, usate `skynet-agent autostart enable`.

### Pubblicazione dei risultati

L'agente salva ogni risultato completato nella posta in uscita. Usa la chiave di firma nel file `identity.key` nella cartella dell'agente e ne crea una al primo uso se il file manca. Per impostazione predefinita invia il risultato firmato a relay Nostr pubblici e a un nodo completo. Un nodo o due relay distinti devono confermare la ricezione prima che l'agente sposti il risultato in `sent`. Altrimenti resta nella posta in uscita. Ogni nuovo tentativo usa lo stesso record firmato con lo stesso ID.

Ecco una parte di un risultato per un compito che usa il calcolo di prova incorporato. Il risultato completo fornisce anche il nome del compito, i secondi trascorsi, la versione del formato, il numero di versione dell'agente e, per impostazione predefinita, un'etichetta della piattaforma. Il record firmato che lo contiene porta la chiave pubblica del dispositivo, un timestamp, l'ID del record e la firma.

```json
{
  "agent": "1.0.1", "kernel": "selftest@1", "unit": 0, "units": 1,
  "result": {
    "kernel": "selftest@1", "rounds": 8, "ok": true,
    "digest": "a2e8f2c45179bfccb6a01d61ab527a86277215a6ee85ff824910fe27d3e9fe26"
  },
  "result_sha256": "7823a03918e86a7046e437fdf001dc40ff05fb1d241a8917baeae4d88b5629fa"
}
```

## Comandi

| Comando desktop | Cosa fa |
|---|---|
| `skynet-agent run` | Lavora finché non viene fermato. `--once` tenta al massimo una porzione di lavoro. `--no-submit` mantiene i risultati in locale per questa esecuzione. `--no-update` salta l'installazione degli aggiornamenti. `--verbose` aggiunge dettagli al registro. |
| `skynet-agent status` | Mostra la versione, la cartella dell'agente, lo stato dell'alimentazione, i contatori del lavoro, i risultati in attesa e i problemi recenti. |
| `skynet-agent tasks` | Elenca i compiti di ricerca automatici, quali sono pronti e quante porzioni di lavoro ha completato questo dispositivo. |
| `skynet-agent pause` / `resume` | Lasciano terminare le porzioni di lavoro attive e smettono di avviarne di nuove, oppure consentono di nuovo nuove porzioni di lavoro. |
| `skynet-agent stop` | Chiedere all'agente in esecuzione di uscire. |
| `skynet-agent outbox` | `list` mostra i risultati in attesa, `show NAME` ne visualizza uno, `send` tenta di pubblicare i risultati idonei e `drop NAME` elimina un risultato in coda. |
| `skynet-agent net` | Esplorate la bacheca con `tasks` o `show`. Usate `post-task`, `claim`, `report`, `accept` o `revise` per partecipare. `sync` ritenta i post della bacheca in sospeso e recupera i record. `id` mostra la vostra chiave pubblica. [Guida della bacheca](BOARD.md) |
| `skynet-agent config` | `show` elenca le impostazioni, `get KEY` ne mostra una e `set KEY VALUE` la modifica. |
| `skynet-agent update` | Controlla se esiste una versione desktop firmata più recente e la installa se è idonea per questo dispositivo. |
| `skynet-agent selftest [--online]` | Controlla un calcolo rispetto alla sua risposta nota. Aggiungete `--online` per controllare le firme sull'elenco dei compiti e sulla descrizione delle versioni precedenti del progetto. |
| `skynet-agent verify-install` | Verifica i file della versione installata ed esegue il calcolo di prova. |
| `skynet-agent version` | Mostra la versione dell'agente, il numero di versione, la versione di Go e la piattaforma. |
| `skynet-agent autostart` | `status` mostra se l'avvio all'accesso è attivo. `enable` lo attiva e `disable` lo disattiva. |
| `skynet-agent uninstall --yes` | Rimuove un'installazione Linux. Aggiungete `--purge` per eliminare anche i dati salvati. |

## Impostazioni

| Impostazione | Predefinito | Significato |
|---|---|---|
| `workers` | 1 | Numero di porzioni di lavoro che l'agente desktop può eseguire contemporaneamente, da 1 a 256. Android ne esegue una. |
| `run_on_battery` | false | Consentire il calcolo con l'alimentazione a batteria. |
| `paused` | false | Attendere prima di avviare nuove porzioni di lavoro. I comandi `pause` e `resume` modificano questa impostazione. |
| `poll_minutes` | 30 | Intervallo approssimativo tra i controlli del repository, da 5 a 1440 minuti. I controlli non riusciti hanno un proprio programma di nuovi tentativi. |
| `update` | auto | Su desktop, `auto` installa gli aggiornamenti firmati idonei, `notify` registra quando ne è disponibile uno e `off` salta installazione e avvisi. Tutte e tre le modalità controllano comunque una pausa firmata dai responsabili. |
| `submit` | auto | `auto` invia i risultati man mano che il lavoro procede. `manual` li tiene nella posta in uscita finché non eseguite `skynet-agent outbox send`. |
| `submit_via` | net | Pubblica record firmati tramite relay e nodi. È l'unico canale funzionante nella versione 1.0. |
| `max_task_minutes` | 120 | Limite di tempo per porzione di lavoro, da 1 a 1440 minuti. Un limite più breve nel compito ha la precedenza. |
| `report_platform` | true | Include nei nuovi risultati il sistema operativo, l'architettura del processore e la versione di Go, per esempio `linux-amd64-` seguito dalla versione di Go. |

Per esempio, `skynet-agent config set workers 4` consente fino a quattro worker desktop. Per compatibilità con le installazioni precedenti, `skynet-agent config show` elenca anche i vecchi limiti dei commenti e le impostazioni di IA. Non hanno alcun effetto sui calcoli Go né sulla pubblicazione in rete.

## Facoltativo: rispondere a domande di ricerca con il proprio modello di IA locale

La modalità IA locale non è disponibile nella versione 1.0. Potete comunque scrivere e pubblicare la vostra risposta sulla bacheca dei compiti.

## Sicurezza, onestamente

- **Gli aggiornamenti e gli elenchi dei compiti sono firmati.** L'agente controlla le loro firme Ed25519 rispetto alla chiave di rilascio del progetto incorporata nel programma. Prima di passare a un aggiornamento desktop, controlla il numero di versione, verifica le dimensioni e lo SHA-256 dell'eseguibile ed esegue un calcolo di prova. Rifiuta gli elenchi dei compiti più vecchi e smette di avviare lavoro da un elenco scaduto.
- **I compiti forniscono dati.** Gli unici calcoli che un compito può selezionare sono incorporati nell'eseguibile. Aggiungere un nuovo tipo di calcolo richiede una nuova versione desktop o un aggiornamento dell'app Android. [Codice sorgente Go per i calcoli](../../agent-go/kernels)
- **Ogni porzione di lavoro viene eseguita in un processo separato** nel vostro account. Il worker richiede una priorità di CPU bassa. L'agente ferma il worker se raggiunge il limite di tempo.
- **Un aggiornamento desktop può tornare alla versione precedente.** Il programma di avvio controlla la versione attiva prima di avviarla. Se il controllo fallisce, o se tre tentativi consecutivi di eseguire l'agente si arrestano in modo anomalo entro il loro primo minuto, il programma di avvio può ripristinare una versione precedente verificata, se disponibile. Ricorda il numero della versione non riuscita.
- **La chiave del dispositivo è un file non cifrato.** Chiunque copi `identity.key` può firmare come questo dispositivo. Un backup privato vi permette di mantenere il vostro nome sulla bacheca dopo aver reinstallato.
- **La prima installazione dipende da dove ottenete il programma di installazione o lo script.** Dopo l'installazione, chiunque controlli la chiave di rilascio del progetto può firmare nuovo codice che viene eseguito con i vostri permessi utente. I responsabili detengono quella chiave durante questa fase di ricerca. Per esaminare prima gli aggiornamenti desktop, usate `skynet-agent config set update notify` ed eseguite `skynet-agent update` quando siete pronti. La rete SkyNet proposta è pensata per funzionare senza una chiave di rilascio centrale. [Progettazione dell'agente di ricerca e tabella delle minacce, in russo](../../docs/RESEARCH_AGENT.md)

## Riservatezza

GitHub vede il vostro indirizzo IP quando scaricate compiti o aggiornamenti. Anche i relay e i nodi completi che contattate vedono il vostro indirizzo IP. Il nodo completo incorporato usa HTTP non cifrato. I risultati e i post della bacheca sono pubblici. La loro chiave pubblica permette ai lettori di collegare tra loro i record dello stesso dispositivo.

I risultati automatici contengono i dati del calcolo e i campi descritti sopra. Usate `skynet-agent config set report_platform false` per omettere l'etichetta della piattaforma dai risultati futuri. L'agente non esamina i vostri file personali né include numeri di serie hardware. Quando pubblicate un compito o un rapporto sulla bacheca, il testo che scegliete di inviare diventa pubblico.

## Quanto vi costa

Un worker occupato può usare circa un core della CPU. La priorità bassa aiuta gli altri programmi a ottenere tempo di CPU quando ne hanno bisogno. Il lavoro consuma comunque elettricità e può produrre calore. Su un portatile l'agente controlla l'alimentazione circa una volta al minuto. Per impostazione predefinita attende di avviare nuove porzioni di lavoro quando rileva l'alimentazione a batteria. Una porzione già in esecuzione può terminare, e l'agente desktop può iniziare a lavorare se la fonte di alimentazione è sconosciuta.

Su Android, scollegare l'alimentazione annulla la porzione in corso e la lascia disponibile per un nuovo tentativo. Selezionate **Lavora anche a batteria** nell'app se volete che continui a calcolare senza alimentazione.

## Rimozione

Su Windows, usate il programma di disinstallazione di **SkyNet Agent**. Per impostazione predefinita conserva la chiave del dispositivo, le code e la cronologia delle versioni. Scegliete l'opzione di eliminazione dei dati durante la disinstallazione per rimuoverli anch'essi.

Su Linux, eseguite il comando seguente. Disattiva il servizio utente, ferma l'agente e rimuove i programmi installati. La chiave, le impostazioni, i progressi e le code vengono conservati.

```sh
skynet-agent uninstall --yes
```

Per rimuovere anche i dati salvati dell'agente, usate `skynet-agent uninstall --yes --purge` quando disinstallate. Su Android, disinstallate **SkyNet Agent** tramite le impostazioni di Android per rimuovere l'app e i suoi dati locali. I record pubblicati restano pubblici.

## Se qualcosa non va

- **«no valid signature from a trusted key»** significa che il documento scaricato non ha superato la verifica. L'agente lo rifiuta. Può comunque usare un elenco dei compiti verificato in precedenza finché quell'elenco non scade. Su desktop, `skynet-agent status` mostra l'ultimo errore del repository. Il registro di esecuzione è `logs/agent.log` nella cartella dell'agente.
- **I risultati restano nella posta in uscita.** Usate `skynet-agent status` o `skynet-agent outbox list` per vedere cosa è in attesa. In modalità manuale, eseguite `skynet-agent outbox send`. Se rispondono troppi pochi relay o nodi, il risultato resta in coda per un altro tentativo.
- **Un'installazione precedente mostra «GitHub submission is unsupported».** Eseguite `skynet-agent config set submit_via net` per usare record firmati per i nuovi risultati. Le voci già contrassegnate per GitHub e le vecchie risposte di IA restano nella posta in uscita per essere esaminate.
- **L'agente è in esecuzione ma non inizia nuovo lavoro.** Controllate `skynet-agent tasks` e il registro di esecuzione. Potrebbe essere in pausa, in attesa dell'alimentazione, senza compiti idonei o in attesa di spazio nella posta in uscita. Su Android, collegate il caricatore e toccate **Avvia** se avete fermato l'app in precedenza.

## Cosa è stato provato

I test dell'agente vengono eseguiti automaticamente su Windows e Linux. Coprono gli elenchi dei compiti firmati, i calcoli con risposte note, gli aggiornamenti e il ritorno alla versione precedente, i record firmati, la consegna, la bacheca dei compiti e un'esecuzione che avvia un worker e consegna il suo risultato a un nodo simulato.

Le installazioni reali sono state provate su Windows 11, Linux Mint, Ubuntu Server e un emulatore Android 14. L'app Android non è ancora stata verificata su un dispositivo fisico. Se qualcosa non funziona sul vostro sistema, aprite una issue.

## Licenza

Il codice dell'agente è sotto [licenza MIT](../../agent/LICENSE).
