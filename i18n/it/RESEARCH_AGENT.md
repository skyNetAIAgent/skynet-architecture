<!-- translation of docs/RESEARCH_AGENT.md, source sha256: be3193497fd35b1568b634f7647119965e68e6e665fea52b5a8ecb8aa477aa9e -->

# Programma agente: come aiutare il progetto senza un assistente IA

[English](../../docs/RESEARCH_AGENT.en.md) · [中文](../zh/RESEARCH_AGENT.md) · [Español](../es/RESEARCH_AGENT.md) · [Français](../fr/RESEARCH_AGENT.md) · [Deutsch](../de/RESEARCH_AGENT.md) · **Italiano** · [Русский](../../docs/RESEARCH_AGENT.md) · [Português](../pt/RESEARCH_AGENT.md) · [العربية](../ar/RESEARCH_AGENT.md)

Stato al 22 novembre 2026. Versione dell'agente 0.1.0. Istruzioni per il partecipante:
[agent/README.md](../../agent/README.md) ([in russo](../ru/AGENT.md)).

## Perché

Il repository è pensato per persone che hanno un assistente IA: legge i documenti e aiuta
a progettare. La maggior parte delle persone non ha un tale assistente, ma ha un computer o un
telefono. Il programma agente offre loro un modo di partecipare: controlla periodicamente questo
repository, prende i compiti, li esegue sul dispositivo del partecipante e pubblica i risultati.

In questa fase **non ci sono ricompense**: né crediti, né denaro, né promesse di accrediti futuri.
L'obiettivo è attrarre il maggior numero possibile di risorse di calcolo e di verificatori
indipendenti alla progettazione dell'architettura.

L'agente è **uno strumento di ricerca, non la rete SkyNet**. È costruito in modo più semplice e più
centralizzato di quanto debba essere la rete, e non soddisfa da solo i suoi requisiti obbligatori.
Più sotto questo è detto apertamente in ogni punto.

## Come è fatto

| Parte | Dove si trova | Che cosa fa |
|---|---|---|
| Elenco dei compiti | `tasks/index.json` e la firma `tasks/index.json.sig` | Indica il calcolo incorporato, i suoi parametri e il numero di porzioni indipendenti |
| Agente | `agent/skynet_agent/`, solo libreria standard di Python 3.9+ | Verifica le firme, sceglie una porzione, calcola, pubblica, si aggiorna |
| Descrizione della versione | `agent/release.json` e la firma | Elenca i file dell'agente con dimensione e SHA-256 |
| Programma di avvio | `agent/launcher.py` | Avvia la versione corrente, passa a quella nuova, torna indietro da quella rotta |
| Risultati | Commenti nella issue GitHub a nome del partecipante | Registrazione leggibile da una macchina con l'impronta del risultato |
| Riepilogo | `results/`, generato da `tools/collect_results.py` | Confronta i risultati di persone diverse, riverifica i ritrovamenti |

Un ciclo di lavoro dell'agente:

1. Una volta ogni 30 minuti (con uno scarto casuale) scarica la descrizione della versione e l'elenco dei compiti.
2. Verifica la firma di ciascuno di essi con la chiave di rilascio incorporata nella copia installata.
3. Se c'è una versione con numero maggiore, scarica i suoi file, confronta ciascuno con l'impronta,
   la mette accanto a quella corrente e si riavvia.
4. Sceglie una porzione casuale di un compito che non ha ancora calcolato.
5. La calcola in un processo separato con priorità più bassa e limite di tempo.
6. Mette il risultato nella «posta in uscita» e lo pubblica come commento nella issue GitHub. I risultati
   di un compito sono pubblicati in blocco, non più di un commento all'ora, per non sommergere la issue
   e gli iscritti di notifiche. Dopo un tentativo fallito, il successivo è rinviato: di un minuto,
   poi il doppio più a lungo, ma non più di un'ora. Se non è possibile pubblicare (nessun accesso a
   GitHub), dopo trecento risultati non pubblicati l'agente smette di prendere lavoro e lo segnala.

Non c'è uno scheduler: ogni agente sceglie da sé la porzione. La coincidenza delle porzioni tra
partecipanti diversi è voluta: tutti i compiti di calcolo sono interi, quindi su qualsiasi dispositivo
si ottengono le stesse cifre, e una porzione è considerata confermata quando la stessa impronta
è stata pubblicata da tanti account diversi quanti ne richiede il compito.

## Il compito è dati, non un programma

L'agente non scarica né esegue mai codice da un compito. Il compito indica uno dei calcoli
incorporati nell'agente («kernel») e gli passa dei numeri. Ogni kernel verifica i parametri e
limita il volume di lavoro. Un nuovo tipo di calcolo appare solo con una nuova versione firmata
dell'agente, il cui codice sorgente si trova nel repository e si legge con gli occhi.

I kernel della versione 0.1:

| Kernel | Che cosa calcola |
|---|---|
| `selftest` | Calcolo intero di controllo: l'impronta deve coincidere su tutti i dispositivi |
| `exit-scam-a` | Attesa esatta del pagamento di un partecipante che, prima di andarsene, consegna risultati falsi (variante A da [CURRENT_DESIGN](CURRENT_DESIGN.md)); enumera una famiglia di strategie e segnala quelle più vantaggiose dell'uscita onesta |
| `lottery-b` | Probabilità esatta di un mese o trimestre in perdita, se si paga solo per i compiti verificati (variante B) |
| `ai-answer` | A richiesta del partecipante: una domanda per un modello IA locale che egli esegue da sé |

Il modello esatto di ogni calcolo è scritto all'inizio del file sorgente del kernel, affinché
chiunque possa ricalcolare il risultato in modo indipendente. I compiti e il loro significato:
[tasks/README.md](../../tasks/README.md).

**Confine con la regola del progetto sugli esperimenti.** I primi compiti sono calcoli secondo
formule dai documenti (analisi dei costi e ricerca di controesempi) e domande ai modelli linguistici.
Non sono misurazioni sull'hardware né esperimenti con la rete. I compiti di misurazione (per esempio,
se i bit dell'output intero coincidono su diverse schede video) sono pubblicati solo dopo la
decisione del proprietario del progetto di aprire gli esperimenti.

## Modalità IA (facoltativa, sperimentale)

Un partecipante che esegue in locale un modello aperto (Ollama, il server llama.cpp, LM Studio
e simili con un'interfaccia compatibile con OpenAI) può attivare `ai.enabled`. Allora l'agente
passa al modello le domande dell'elenco firmato e pubblica le risposte. Così le persone senza
abbonamento all'IA, ma con una scheda video, diventano partecipanti al «consiglio dei modelli».

- L'agente non scarica e non avvia alcun modello e per impostazione predefinita si rivolge solo a un
  server sullo stesso computer.
- La domanda e i documenti che cita sono definiti dall'elenco firmato. Ogni documento è confrontato
  con l'impronta, quindi non è possibile far vedere al modello un testo diverso.
- Per impostazione predefinita la risposta attende nella «posta in uscita» finché il partecipante non
  la approva: il testo è pubblicato a suo nome.
- La risposta è contrassegnata come generata da una macchina e non verificata da nessuno. Il numero
  di risposte per domanda è limitato.

Verificata solo con un server fittizio nei test automatici. Con ambienti reali di esecuzione dei
modelli la modalità non è ancora stata verificata.

## Applicazione per Android (sperimentale)

Per chi non vuole configurare Termux c'è un'applicazione: un solo file APK, un pulsante «Start».
Codice sorgente e istruzioni: [android/README.md](ANDROID.md). Nell'applicazione sono
incorporati lo stesso pacchetto `skynet_agent` e Python (tramite Chaquopy). Differenze rispetto
all'agente su computer:

- Android non permette di eseguire processi Python separati, quindi la porzione è calcolata nel
  processo in background dell'applicazione stessa, una alla volta. Se una porzione dura oltre il
  limite, il watchdog termina quel processo, Android riavvia il servizio e il compito resta ai
  dispositivi più veloci.
- La nuova versione dell'agente è prelevata dal repository con la stessa firma della chiave di
  rilascio. La verifica la copia incorporata; se la nuova versione qui non si avvia o i suoi file
  sono modificati, l'applicazione torna a quella incorporata.
- L'applicazione stessa (schermata, servizio, watchdog) cambia solo con un nuovo APK. L'APK è firmato
  con una chiave separata dei responsabili del progetto: è un secondo punto di fiducia unico, che nella
  rete non deve esistere.
- I risultati sono pubblicati con un token GitHub che il partecipante inserisce nell'applicazione.
- Lavora solo in carica, a meno che il partecipante non abbia permesso altrimenti. Non c'è la
  modalità IA.

Stato al 22 novembre 2026: l'applicazione si compila, la sua parte in Python supera i test su
computer (`agent/tests/test_android_glue.py`). La build di verifica con una chiave di test è riuscita
sull'emulatore Android 14 (x86_64) con un repository di test locale: installazione, verifica delle
firme, calcolo di tutte le 7 porzioni di test senza errori, attesa senza carica, lavoro in background,
salvataggio del token e suo utilizzo verso la vera API di GitHub, arresto e riavvio con lo stato
conservato. Su un telefono reale l'applicazione non è ancora stata eseguita, la build per ARM
(`arm64-v8a`) non è stata verificata. Non è distribuita tramite Google Play: le sue regole vietano
le applicazioni che scaricano codice eseguibile.

## Di cosa si fida l'agente

| Che cosa | Fiducia |
|---|---|
| Firma Ed25519 con la chiave di rilascio | Sì. Senza di essa non sono accettati né la versione né l'elenco dei compiti |
| Canale (HTTPS, mirror, GitHub stesso) | No per l'integrità: la sostituzione di un file rompe la firma o l'impronta |
| Contenuto del compito | No: i parametri sono verificati, il volume di lavoro è limitato, nel compito non c'è codice |
| Risposta del modello locale | No: è testo, è pubblicata come non verificata |
| Prima installazione | Sì, al canale HTTPS fino a GitHub. Si può verificare l'installazione con il comando `selftest --online` |

**Confine onesto.** Il detentore della chiave di rilascio può distribuire il programma a tutti gli
agenti installati. Attualmente la chiave è dei responsabili del progetto. È un punto di fiducia unico,
che nella rete SkyNet non deve esistere: nel progetto di destinazione il programma si aggiorna solo
a una versione la cui impronta è stata accettata dal voto dei partecipanti nel registro comune, e la
firma con la chiave di qualcuno non è sufficiente
([CURRENT_DESIGN, sezione 8](CURRENT_DESIGN.md)). Il partecipante che non vuole fidarsi della chiave
imposta `update` su `notify` e si aggiorna a mano, dopo aver letto le modifiche.

## Tabella delle minacce

| Minaccia | Come è coperta | Che cosa resta |
|---|---|---|
| Compromissione del repository o di un account con diritto di scrittura: sostituzione dell'agente | La versione è accettata solo con la firma di una chiave che non è nel repository | Coperto, finché la chiave non viene rubata |
| Sostituzione di un file durante il trasferimento o su un mirror | Firma della descrizione della versione e SHA-256 di ogni file | Coperto |
| Ritorno a una vecchia versione vulnerabile | Il numero di versione deve essere maggiore di quello corrente | Coperto per gli agenti installati. Una nuova installazione prende ciò che si trova nel repository |
| Compito dannoso | Il compito non contiene codice; il kernel verifica i parametri e limita il volume di lavoro e di memoria; c'è un limite di tempo | Limitato: un compito firmato può occupare la CPU fino al limite di tempo |
| Ripetizione di un vecchio elenco firmato di compiti | Il numero dell'elenco deve essere non inferiore a quello già visto; l'elenco può avere una scadenza | Limitato: un'installazione fresca può ricevere un vecchio elenco e calcolare invano compiti chiusi |
| Versione rotta | Il programma di avvio torna alla versione precedente dopo tre crash rapidi o se i file della nuova versione sono spariti, e ricorda il numero non valido. Le richieste ripetute di riavvio sono eseguite con una pausa crescente | Coperto per i crash all'avvio. Un errore silenzioso nel calcolo è colto dal confronto dei risultati |
| Furto della chiave di rilascio | La chiave si trova fuori dal repository, su Windows è cifrata per l'account del proprietario | **Aperto.** Il ladro può pubblicare una versione dannosa. Il cambio di chiave avviene con una nuova versione firmata con la vecchia chiave, disponibile anche al ladro |
| Perdita della chiave di rilascio | Copia di riserva presso il proprietario | Senza la chiave gli agenti installati non possono essere aggiornati: i partecipanti dovranno reinstallare l'agente |
| Falsificazione del risultato | Il calcolo intero è confrontato tra account diversi; i ritrovamenti sono ricalcolati durante la raccolta | Limitato: una persona con due account «confermerà» sé stessa. Non ci sono ricompense, quindi non c'è vantaggio in questo, ma un sabotatore è possibile. I responsabili ricalcolano a campione |
| Flusso di commenti spazzatura da account altrui | Il raccoglitore accetta solo registrazioni con impronta corretta e compito noto | Limitato dagli strumenti di GitHub |
| Fuga del token GitHub | L'agente non conserva il token, lo prende da `gh` o da una variabile e non lo invia da nessuna parte, tranne a GitHub via HTTPS, senza reindirizzamenti | Il token con diritto di scrittura nei repository pubblici resta responsabilità del partecipante |
| Codice altrui accanto all'agente (un modulo inserito nella cartella corrente) | Modalità isolata di Python (`-I`) | Coperto. Da un programma con i diritti dello stesso utente sullo stesso computer non c'è protezione |
| Consumo di risorse del partecipante | Un processo per impostazione predefinita, priorità più bassa, pausa a batteria, limite di tempo, comandi `pause` e `stop` | L'elettricità il partecipante la spende da sé e gratuitamente |
| Arresto di tutti gli agenti da parte dei responsabili | Il contrassegno firmato `halt` nella descrizione della versione; vale anche con gli aggiornamenti disattivati | È una leva intenzionale: solo arresto, senza avviare nulla |

## Che cosa riferisce di sé

Solo il contenuto della registrazione pubblicata: nome del compito, numero della porzione, cifre del
risultato, tempo di calcolo e, se non disattivata, un'etichetta approssimativa della piattaforma del
tipo `linux-amd64-py3.12`. Le richieste vanno solo a GitHub. Non sono raccolte informazioni sui file,
sulla rete e sull'hardware del partecipante.

## Procedura per i responsabili

La chiave di rilascio è creata una sola volta e conservata fuori dal repository:

```
python tools/keytool.py generate
```

La copia di riserva del segreto la fa il proprietario stesso, a mano, con il comando
`python tools/keytool.py backup`, e la conserva fuori dal computer. Il segreto non va mostrato agli
assistenti, né inserito in chat e file.

Nuova versione dell'agente:

```
python tools/make_release.py --seq <numero successivo> --version <x.y.z>
```

poi caricamento dei file modificati di `agent/` nel repository. Nuovo elenco dei compiti:

```
python tools/sign_tasks.py
```

poi caricamento di `tasks/index.json` e `tasks/index.json.sig`. Raccolta dei risultati:

```
python tools/collect_results.py
```

Per fermare il lavoro di tutti gli agenti finché l'errore non è corretto: pubblicare una descrizione
della versione con `--halt-through <numero>` e il motivo.

## Che cosa qui non c'è e perché è onesto dirlo

- **Non è una rete distribuita.** I compiti e le versioni sono distribuiti da un solo repository,
  firmati da una sola chiave, i risultati sono ricevuti da un'unica piattaforma. I requisiti R1–R4
  dei [requisiti obbligatori](../ru/REQUIREMENTS.md) non si applicano all'agente e non sono
  soddisfatti da esso.
- **Serve un account GitHub.** Senza di esso i risultati sono pubblicati solo a mano tramite un link.
- **Non c'è protezione contro account multipli.** Per la fase gratuita questo è accettabile.
- **Android non è verificato su un dispositivo reale**; l'avvio automatico su macOS, Linux e Android
  è verificato solo a livello dei file creati. Due casi sono considerati secondo la documentazione e
  anch'essi non verificati su dispositivi reali: Python del Microsoft Store su Windows (vede una copia
  privata di `AppData` e del registro, quindi la cartella dell'agente si trova nel profilo e l'avvio
  automatico va aggiunto a mano) e Python dal sito python.org su macOS senza certificati installati
  (l'agente ripete la richiesta con il file dei certificati di sistema).
- **I primi compiti sono leggeri.** L'intero primo lotto (702 porzioni) ha richiesto su un solo
  computer desktop 15,5 ore di tempo CPU con 16 processi simultanei a priorità più bassa, cioè circa
  un'ora di tempo reale [misurato su un solo PC, 22 novembre 2026]. Il meccanismo è pronto ad
  accettare compiti pesanti. Che cosa ne è uscito: [results/FIRST_RUN.md](../../results/FIRST_RUN.md).

## Prossimi passi

1. Compiti di misurazione su dispositivi diversi: la principale incognita del progetto è la
   coincidenza del risultato fino al bit su diverse schede video. Sono esperimenti, attendono la
   decisione del proprietario.
2. Abbandono dell'account GitHub: ricezione dei risultati tramite diverse piattaforme pubbliche
   indipendenti, come nel progetto di destinazione della rete.
3. Abbandono della chiave unica: diverse firme indipendenti, poi accettazione delle versioni secondo
   le regole della rete stessa.
4. Gestione del modello locale: scaricamento di un modello aperto con verifica dell'impronta,
   affinché la modalità IA si attivi con un solo comando.
