<!-- translation of docs/ROADMAP.md, source sha256: 179a6350fb2d665a7c94f5f2cfa6b2e520f28c4174e3b619f3a31299f63f53ff -->

# Tabella di marcia: difesa dall'inganno

[English](../../docs/ROADMAP.en.md) · [中文](../zh/ROADMAP.md) · [Español](../es/ROADMAP.md) · [Français](../fr/ROADMAP.md) · [Deutsch](../de/ROADMAP.md) · **Italiano** · [Русский](../../docs/ROADMAP.md) · [Português](../pt/ROADMAP.md) · [العربية](../ar/ROADMAP.md)

Stato al 23 novembre 2026 (aggiornato dopo il rilascio della v0.2.2). È un **piano di lavoro, non
una promessa di risultato**. Il segno `[x]`
significa «fatto, e lo si può verificare nel repository o nelle registrazioni della rete»; `[ ]` significa
«non fatto». I numeri con la nota [calcolo] sono ottenuti da una formula, non misurati. La tabella di
marcia viene aggiornata a ogni cambiamento di stato.

## 1. Obiettivo e segni di completamento

**Obiettivo della fase attuale del progetto:** trovare un modo di verificare l'onestà per il quale siano
soddisfatti insieme i requisiti obbligatori ([REQUIREMENTS](../ru/REQUIREMENTS.md)):

- ingannare la rete è impossibile: l'inganno è inutile o in perdita, anche per un novizio con il conto
  vuoto, in caso di collusione e con molte chiavi;
- nessun anticipo di fondi: né depositi, né contributi, né multe;
- partecipare conviene, la verifica dell'onestà è economica. Stime del lavoro aggiuntivo richiesto dalla verifica: circa il 5% del lavoro per le richieste al modello e circa il 20% per l'addestramento
  (non confermati).

**Il lavoro è considerato completo quando c'è tutto ciò che segue:**

1. **È scritto che cosa viene garantito esattamente** (decisione D1): per il risultato di una richiesta, un
   passo di addestramento, il pagamento e la cronologia; per il conto vuoto, un numero arbitrario di
   chiavi, l'uscita e la collusione completa dei verificatori del compito. Il requisito ammette «l'inganno
   è inutile»; non è obbligatorio dimostrare che ogni tentativo comporti una perdita netta.
2. **Per ogni attacco della tabella degli attacchi è scritta la regola con cui un nodo rifiuta una
   dichiarazione falsa, e da quali dati lo fa.** Sono indicati separatamente la probabilità di falsa
   accettazione, il danno alla rete e il guadagno netto della coalizione rispetto all'inazione e rispetto
   al lavoro onesto. Controesempio alla regola: casi onesti e falsi in cui il nodo vede gli stessi dati.
   Il campionamento, la piccola probabilità di errore e «si trova un osservatore onesto» sono scritti come
   ipotesi.
3. **È calcolato il costo completo della verifica** rispetto allo stesso compito senza verifica: lavoro
   dell'esecutore e dei verificatori, memoria, traffico, conservazione, scrittura nel registro, controversie,
   ripetizioni dopo i guasti. Sono ricavati il reddito netto di un partecipante con grandi risorse con
   elettricità cara, il supplemento per un partecipante con attrezzatura debole e il prezzo per il
   consumatore senza attrezzatura. La registrazione e la controversia sono accessibili da un conto a zero;
   si possono perdere solo le ricompense non maturate.
4. **I calcoli sono riproducibili:** sono allegati la versione delle regole e del kernel, gli ingressi,
   i limiti dell'enumerazione, l'uscita e l'hash; il calcolo è stato ripetuto su un secondo dispositivo.
   La ripetizione conferma il calcolo, ma non la correttezza del modello stesso: quella si giustifica
   separatamente.
5. **È misurato ciò che non si può stabilire con il ragionamento:** la coincidenza del risultato bit a bit
   su diverse schede video, la velocità e la qualità del modello ad aritmetica intera, il costo della controversia.
   Profili, metriche e soglie sono fissati prima della misurazione.
6. **Non sono violati gli altri requisiti:** la rete funziona senza un qualsiasi singolo nodo o
   piattaforma, si ritrova dopo uno spegnimento completo, i fondamenti degli accrediti si ricostruiscono;
   in caso di divisione della rete un pagamento contestato attende la cronologia comune, una ripetizione
   non viene pagata due volte.

Anche un esito onesto è un risultato: se per una certa classe di compiti la verifica economica è
impossibile, lo si mostra con una dimostrazione che nomina la classe di compiti e i dati del verificatore,
non con l'assenza di idee.

## 2. Dove siamo ora

| Che cosa | Stato | Dove è registrato |
|---|---|---|
| Da firme e risposte brevi non si può stabilire quale dispositivo ha lavorato e per quanto tempo: un intermediario, una cache e una scheda inattiva danno gli stessi dati | Stabilito con il ragionamento | [OPEN_QUESTIONS](OPEN_QUESTIONS.md), «Che cosa è già stato scartato» |
| La rete paga per il risultato verificabile, non per la risorsa | Accettato (D2); l'unità di risultato e la condizione di accettazione non sono ancora definite | [CURRENT_DESIGN](CURRENT_DESIGN.md), sezione 1 |
| Pagamento differito al posto del deposito: il partecipante risponde solo con la somma in sospeso | Accettato | CURRENT_DESIGN, sezione 2 |
| Variante A: verifica a campione con annullamento | Specifica attuale | CURRENT_DESIGN, sezione 3 |
| Variante B: la rete paga solo per i compiti verificati, `1/p` volte di più | Candidato principale; scelta dopo il confronto (D3) | CURRENT_DESIGN, sezione 3 |
| Coincidenza del risultato bit a bit tramite aritmetica intera | Candidato, non misurato | OPEN_QUESTIONS, Q2 |
| Controversia per dimezzamento con ricalcolo di un passo nel registro | Misurato per una riga del modello; per il modello completo non costruito | [PILOT_RESULTS](PILOT_RESULTS.md) |
| Verifica della moltiplicazione di matrici con un vettore casuale dentro la controversia | Candidato, c'è solo una stima calcolata | CURRENT_DESIGN, sezione 3 |
| Nucleo di verifica immutabile, che non si può revocare con una votazione | Accettato (D4) | CURRENT_DESIGN, sezione 8 |

**Che cosa si sa sulla forza della difesa.**

- Variante A, senza collusione: nella famiglia esaminata (due ondate di contraffazioni, 92 milioni di
  strategie) andarsene con contraffazioni non rende più di un'uscita normale [calcolo].
- Variante A, collusione: i primi punti della griglia in cui andarsene con contraffazioni conviene sono la
  quota di collusione dell'87,5% (compiti di dimensione arbitraria) e dell'89,0% (compiti uguali) con la
  regola «non più di un terzo in lavorazione», 80% senza questa regola. Il passo della griglia è 0,002–0,02;
  altre famiglie di strategie non sono state esaminate [calcolo, [FIRST_RUN](FIRST_RUN.md)].
- Variante B, senza collusione: con il confronto esatto una contraffazione non viene pagata.
- Variante B, collusione: `q` è la quota di peso della coalizione tra i verificatori di quel modello. Una
  contraffazione viene pagata solo se il compito è stato scelto e tutti i `k` verificatori sono in
  collusione. Il pagamento medio per una contraffazione presentata è pari a `R·q^k` (`R` è il prezzo del
  compito) e non dipende da `p` [calcolo]. Con `q = 1` è il prezzo intero. Da un novizio con il conto vuoto
  non c'è nulla da sottrarre.
- Per nessuna delle due varianti è dimostrato che si possano escludere pagamenti indebiti quando tutti i verificatori sono collusi. Questa garanzia si ottiene verificando ogni risultato pagato sulla base di dati che ciascun nodo controlla in autonomia. Il ricalcolo completo aggiunge circa il 100% di lavoro. Misurazioni del progetto pilota: la prova
  RISC Zero per una riga del modello si costruiva in 22 min 10 s; l'esecuzione di otto righe nella zkVM
  andava circa 17.700 volte più lentamente del normale, senza costruire la prova. Queste misurazioni non
  danno un limite inferiore generale del costo.
- Irregolarità del reddito nella variante B: con 6.000 compiti al mese, verifica di 1 su 100 e costo pari
  al 95% del prezzo, la probabilità di un mese in perdita è 33,10% [calcolo, FIRST_RUN].
- La prima esecuzione dei calcoli (702 porzioni) è stata fatta su un solo computer. Un secondo
  dispositivo, entro il 23 novembre, ha ricalcolato tutte le 702 porzioni; tutte sono coincise. Le
  sue registrazioni sono firmate con la chiave `46000d30…` e sono disponibili sul nodo completo.
  Entrambi i dispositivi appartengono ai manutentori, quindi questa non è ancora una conferma da
  parte di un partecipante indipendente.

**Che cosa non è risolto.**

1. Un novizio con il conto vuoto in collusione (variante B): guadagno medio `R·q^k` per tentativo, nessuna
   perdita.
2. «Onesto a lungo, poi inganna in grande e se ne va»: la perdita è limitata alla somma in sospeso, il
   guadagno cresce con il numero di contraffazioni. Le riparazioni per la variante B sono proposte, non
   calcolate.
3. Flusso di spazzatura da chiavi gratuite. La chiave non costa nulla; pagare con il lavoro del processore
   mette i dispositivi deboli in una posizione peggiore.
4. Risultato usato prima della verifica. La risposta è già stata letta dall'utente, il passo è già entrato
   nell'addestramento; limitare i pagamenti non lo corregge. Nella variante B questo vale anche per i
   compiti non scelti.
5. Compiti di addestramento pagati con l'emissione di crediti: chi e con quale regola li approva. Un
   compito eseguito correttamente ma autoassegnato non deve dare crediti.
6. Modello raro: la cerchia dei verificatori è piccola e per esso `q` può essere vicino a uno.
7. Disponibilità dei dati e controversia su una richiesta privata senza rivelare la richiesta.
8. La coincidenza bit a bit e la velocità del modello ad aritmetica intera non sono misurate.
9. Un sabotatore a cui non serve il profitto e l'avvelenamento dei dati di addestramento. Su di essi la
   difesa economica non agisce.

## 3. Decisioni

Le decisioni D1–D5 sono prese il 23 novembre 2026.

| N. | Domanda | Decisione |
|---|---|---|
| D1 | Che cosa si accetta come garanzia | **Il truffatore non ottiene ciò che vuole.** Non si possono escludere i tentativi di inganno, ma ogni tentativo deve essere inutile per chi lo fa: il guadagno atteso di una contraffazione non è maggiore di zero rispetto al lavoro onesto e rispetto all'inazione, per qualsiasi coalizione, incluso un novizio con il conto vuoto e un numero qualsiasi di chiavi. L'obiettivo è che il risultato falso non venga pagato affatto. Non è richiesta una perdita netta su ogni tentativo. Una perdita limitata ma positiva (per esempio `R·q^k` per un novizio nella variante B) **non soddisfa** il criterio e resta un buco aperto |
| D2 | Il fondamento del pagamento | **Accettato: viene pagato solo il risultato verificabile.** L'attrezzatura accesa, il tempo di lavoro e la potenza dichiarata non sono il fondamento del pagamento: una scheda video si può caricare anche con qualcosa di estraneo |
| D3 | Variante A o B | **La decisione viene presa dopo il confronto sugli stessi attacchi e allo stesso costo (fase 2).** Il candidato principale è la variante B |
| D4 | Il nucleo di verifica immutabile | **Accettato in forma rafforzata.** La verifica procede automaticamente, senza intervento umano e senza votazioni. Le regole di verifica non si cambiano con una votazione. Ogni nodo esegue da sé la verifica secondo l'impronta fissata delle regole, perciò la sostituzione dell'algoritmo su un nodo o presso un fornitore del programma non cambia le decisioni degli altri. Aperto: come correggere un errore nel nucleo stesso (solo passando a una nuova rete) e come un partecipante si convince che il suo programma corrisponde all'impronta pubblicata (build riproducibile). La chiave di rilascio con cui ora si firmano i mini-agenti è uno strumento di ricerca; nella rete di destinazione non deve esserci |
| D5 | Prima esperienza con Qwen3.5-4B ad aritmetica intera | **Consentito:** la scheda video RTX 2060 sul Linux domestico del manutentore, il suo computer e, con il consenso, i dispositivi di altri partecipanti tramite i mini-agenti. Si esegue dopo la fase 0 |

**Ordine di lavoro.** Prima si completa la fase 0 — i mini-agenti e le applicazioni per smartphone,
perché altre persone possano collegarsi al lavoro. Poi le fasi 1–5 secondo questa tabella di marcia.

## 4. Fasi e lista di controllo

Prima si completa la fase 0. Poi le fasi 1–4 procedono in parallelo: sono calcoli e ragionamenti.
La fase 5 (l'esperimento è consentito dalla decisione D5) procede dopo la fase 0. La fase 6 riunisce
i risultati.

### Fase 0. Mini-agenti e applicazioni per smartphone (si esegue per prima)

**Obiettivo della fase.** Su ogni piattaforma supportata una persona percorre il percorso «scaricato →
installato → avviato», e poi il mini-agente senza intervento umano si aggiorna, prende i compiti e
restituisce il risultato. Senza account, senza diritti di amministratore, senza Python preinstallato.
Ogni passo è verificato su un dispositivo reale, non solo con test automatici.

**Completato quando** per ogni piattaforma dell'elenco qui sotto: una persona senza esperienza ha
percorso il percorso con una sola pagina di istruzioni; l'agente su quel dispositivo ha ricevuto da
solo un nuovo rilascio, ha preso da solo un compito del nuovo elenco, il suo risultato è apparso sul
nodo completo ed è coinciso con il risultato di un altro dispositivo. Sono registrati il sistema,
l'architettura, le versioni prima e dopo e l'identificatore della registrazione sul nodo.

Piattaforme: Windows, Linux, Android (decisione del 23 novembre 2026). Per macOS e iOS i mini-agenti
non vengono realizzati e non vengono verificati. Il comando di installazione per Linux forse funziona
anche su macOS, ma questo non è supportato. La versione Windows viene rilasciata senza firma del
codice: all'installazione Windows mostra un avviso SmartScreen, che va confermato manualmente;
l'autenticità del file si verifica tramite l'hash pubblicato e la firma del progetto.

Già fatto:

- [x] Repository pubblico, base immutabile in nove lingue (etichetta `core-v1`).
- [x] Programma-agente per Windows e Linux: compiti e aggiornamenti firmati,
      verifiche automatiche in CI (versione 0.2.0). Installazione con un solo comando
      nel terminale; serve Python 3.9+.
- [x] Risultati e [bacheca dei compiti](BOARD.md) senza account.
- [x] Primo nodo completo, che conserva la cronologia delle registrazioni.
- [x] Primo compito di ricerca «Difesa dai truffatori» sulla bacheca, in nove lingue.
- [x] App Android di prova 0.1.0 (verificata solo sull'emulatore).

**Passo 1. Affidabilità dell'aggiornamento (versione 0.2.1, senza nuovi compiti)**

- [x] La prima installazione verifica la firma della versione con la chiave incorporata nello stesso
      installatore, **prima** di eseguire il codice scaricato (in precedenza l'agente scaricato
      verificava se stesso).
- [x] Passaggio alla nuova versione con una sola operazione atomica: prima si prepara e si verifica
      il nuovo catalogo, poi si cambia un solo puntatore; il precedente insieme funzionante viene
      conservato.
- [x] Il numero di versione più alto accettato è conservato fuori dai cataloghi delle versioni e
      viene verificato anche alla reinstallazione (difesa dal ritorno a una versione vecchia).
- [x] La chiave del dispositivo, le impostazioni, il progresso e i risultati non inviati sono
      conservati fuori dai cataloghi delle versioni e sopravvivono all'aggiornamento e alla
      reinstallazione.
- [x] Senza rete l'agente continua a lavorare sull'ultima versione funzionante e ripete il
      collegamento con un intervallo crescente.
- [x] Verifica automatica in CI: un file sostituito, una chiave altrui, un numero vecchio, un file
      in più, un download interrotto e un Python incompatibile vengono rifiutati, la versione
      funzionante resta.
- [x] **Verifica dal vivo sul server:** l'installazione 0.2.0 è passata da sola alla 0.2.2 il 23
      novembre 2026, la chiave del dispositivo e il progresso sono conservati. Sul Linux domestico
      l'agente è stato installato di nuovo con il nuovo installatore (0.2.2); il suo
      autoaggiornamento sarà verificato dal rilascio successivo.
- [x] Verifica dal vivo dell'autoaggiornamento su Windows: l'installazione del proprietario è passata
      da sola attraverso 0.2.2 → 0.3.0 → Go 1.0.1 (23 novembre 2026).

**Passo 2. Android: app senza token**

- [x] Nuovo APK 0.2.0 con l'agente 0.2.2 incorporato: pubblicazione con registrazioni firmate, la
      schermata del token e i suggerimenti sul token sono rimossi.
- [x] Correggere il falso ritorno alla versione precedente senza rete: prima tre avvii senza
      collegamento segnavano una versione nuova funzionante come difettosa. Ora la versione è
      confermata da un'autoverifica locale.
- [x] L'app verifica una volta al giorno le nuove versioni dell'APK, confronta l'hash e la firma del
      progetto e propone di installare; l'installazione è confermata da una persona (così funziona
      Android fuori dallo store).
- [x] Avvio dopo il riavvio tramite l'interruttore dell'utente (verificato sull'emulatore).
- [x] Verifica dell'aggiornamento sopra l'APK 0.1.0 sull'emulatore Android 14: i dati si conservano.
- [ ] Verifica della proposta di un nuovo APK da parte dell'app stessa (funzionerà con la versione
      successiva dell'APK).
- [ ] **Verifica dal vivo su un telefono reale** (serve un partecipante con un telefono):
      installazione, lavoro durante la ricarica, riavvio, risparmio energetico del produttore.

**Passo 3. Windows: installatore in un solo file**

- [x] `SkyNetAgentSetup.exe` viene compilato in GitHub Actions, senza firma del codice; dentro,
      Python incorporato da python.org, l'agente e la versione firmata. Accanto vengono pubblicati
      il suo hash e la firma del progetto. Installazione nel profilo utente, senza diritti di
      amministratore, funziona senza rete.
- [x] Collegamenti nel menu «Start»: stato dell'agente, pausa, ripresa, arresto, rimozione.
- [x] Casella «avvia all'accesso» nell'installatore; la scelta si conserva all'aggiornamento.
- [x] Rimozione tramite «App»; alla rimozione si può conservare la chiave del dispositivo.
- [x] Verifica automatica in CI su un Windows pulito senza Python: installazione, autoverifica,
      rimozione.
- [x] Verifica dal vivo sul computer di una persona: il proprietario ha installato l'agente dalle
      Releases (versione v0.2.2).

**Passo 4. Linux**

- [x] L'installatore usa il Python di sistema 3.9+ e, se non c'è, installa un Python portatile e ne
      verifica l'hash. C'è anche un installatore in un solo file senza rete (versione v0.2.2).
- [x] Servizio utente systemd con il consenso dell'utente; il lavoro senza accesso al sistema è una
      casella separata.
- [x] Verifica in CI: Debian 12 senza Python e Ubuntu 24.04 con Python; installazione dal vivo su Linux Mint.
- [ ] Verifica dal vivo presso un partecipante non legato ai manutentori.

**Passo 5. Agente in Go al posto di Python (decisione del proprietario del 23 novembre 2026)**

L'agente è stato riscritto in Go: un solo piccolo programma, Python non serve. Il Python incorporato e il
suo aggiornamento non servono più, perciò il precedente passo «aggiornamento del Python incorporato» è stato
rimosso.

- [x] Firme, compiti, sette nuclei di calcolo, registrazioni, Nostr, bacheca, ciclo di lavoro,
      aggiornamento sul secondo canale (`agent/v2/release.json`), avviatore, avvio automatico — in Go,
      solo libreria standard (il codice è stato scritto da ChatGPT, verificato da DeepSeek).
- [x] I risultati Go coincidono con Python bit a bit su tutte le porzioni veloci del riferimento e su
      tutte quelle pesanti verificate; il confronto di tutte le 1 199 porzioni continua.
- [x] Build riproducibile: hash dei programmi identici compilando su Windows e Linux.
- [x] Il ponte in Python 0.4.0 trasferisce da solo gli agenti installati a Go conservando la chiave
      del dispositivo, il progresso e la coda. Transizione dal vivo: il server, il Linux domestico e il
      Windows del proprietario sono passati da soli a Go 1.0.1.
- [x] Installatori in Go: Windows 4,7 MB, Linux in un solo file; app Android 0.3.0 con motore Go,
      circa 8 MB invece di 40 (verificato sull'emulatore Android 14).
- [ ] Rimuovere il ponte e le copie Python dopo due rilasci verificati in Go.

**Passo 6. Flusso dei compiti**

- [x] Quattro nuovi compiti di calcolo della fase 2 (campagna di uscita della variante B, posti da
      apprendista, lotteria con quota di verifica scelta, certificato del token vincente) — nuovi
      nuclei incorporati dell'agente 0.3.0, 515 porzioni nell'elenco dei compiti n. 2. La matematica è
      stata verificata in modo indipendente con un altro metodo in 111 punti. Il certificato su matrici
      casuali non dà risparmio (circa lo 0,8% di lavoro in più), perciò sono state lasciate 20 porzioni
      come base per il confronto con i pesi del modello reale.
- [x] I nuovi compiti richiedono l'agente 0.3.0 o superiore; il vecchio agente salta il compito
      incompatibile e continua a lavorare (verificato con un test).
- [ ] Quando tutti i compiti sono calcolati, l'agente aspetta e prende da solo l'elenco successivo.
- [ ] Il raccoglitore dei risultati lavora secondo un programma sul nodo completo e pubblica un
      riepilogo.
- [ ] Conferma indipendente di tutte le 702 porzioni del primo elenco. Un secondo dispositivo (il
      server dei manutentori) ha ricalcolato tutte le 702, tutte sono coincise; un partecipante non
      legato ai manutentori per ora non c'è.

**Passo 7. Pilota con altre persone**

- [ ] Pagina «Come collegarsi» in nove lingue: un collegamento per ogni sistema.
- [ ] Un partecipante per piattaforma, non legato ai manutentori; i segni di completamento della fase
      sono soddisfatti.
- [ ] Secondo e terzo nodo completo presso proprietari diversi.

**Passo 8. Agenti IA**

- [ ] L'agente prende da solo i nuovi compiti della bacheca e li passa al modello locale del
      partecipante; la risposta viene inviata solo dopo l'approvazione di una persona. Il testo del
      compito è considerato non attendibile.
- [ ] Istruzioni per l'assistente IA: come prendere un compito dalla bacheca, consegnare una
      relazione e verificare quella altrui.
- [ ] Relazione su un compito della bacheca da parte di un partecipante non legato ai manutentori.

**Decisioni del proprietario sulla fase 0** (23 novembre 2026): macOS e iOS non vengono realizzati;
la versione Windows viene rilasciata senza firma del codice.

### Fase 1. Formulazione precisa

- [x] Le decisioni D1 e D2 sono prese e scritte (sezione 3).
- [ ] Per una richiesta aperta e un passo di addestramento sono scritti: la regola di accettazione,
      l'aritmetica, il fondamento dell'emissione di crediti, il momento di fissazione del risultato
      rispetto al sorteggio e il momento in cui il risultato si può usare.
- [ ] Modello dell'avversario in un unico documento: collusione, molte chiavi, uscita, noleggio di potenza;
      che cosa conta come guadagno dell'ingannatore e che cosa conta come danno alla rete.
- [ ] La tabella degli attacchi analizzati è pubblicata nel repository in nove lingue con lo stato di ogni
      attacco per le varianti A e B. Prima della pubblicazione verificare le righe: nel riepilogo di
      CURRENT_DESIGN la somma delle categorie è 18 + 6 + 19 + 16 = 59 contro 60 dichiarati.
- [ ] Per ogni attacco è scritto in base a quali dati verificabili in modo indipendente il nodo rifiuterà
      una dichiarazione falsa in caso di collusione dell'esecutore e dei verificatori.

Completato quando: qualsiasi partecipante può indicare in base alla tabella un attacco non chiuso e
verificarlo.

### Fase 2. Economia: calcoli eseguiti dai mini-agenti

Ogni compito è un modello esatto con una griglia finita di ingressi; probabilità e somme si calcolano come
frazioni esatte, l'hash di ogni porzione viene confrontato tra i dispositivi.

- [x] Variante A, uscita con contraffazioni: prima esecuzione.
- [x] Variante B, irregolarità del reddito con quota di verifica costante: prima esecuzione.
- [ ] Conferma indipendente di entrambi i calcoli (vedi fase 0).
- [ ] **Campagna di uscita nella variante B.** Ingressi: somma in sospeso `H₀`, prezzo `R`, quota di
      verifica `p`, collusione `q` e `k`, tetto dei compiti simultanei `C`, numero di ondate `T`. Una sola
      contraffazione colta azzera tutta la somma in sospeso, comprese le vincite dell'ondata. Trovare il
      pagamento atteso più alto oltre `H₀`, anche con `H₀ = 0`, `q = 0` e `q = 1`.
- [ ] **Posti da apprendista.** Per epoca, `S` posti vengono distribuiti tra `n` chiavi oneste e `m` chiavi
      della coalizione. Trovare la perdita attesa su `E` epoche e la quota di posti che tocca ai novizi
      onesti, al crescere di `m`.
- [ ] **Lotteria con quota di verifica scelta.** Per `N` compiti al mese prendere il più piccolo `p` per cui
      in media vengono pagati almeno 60 compiti. Trovare la probabilità di un mese e di un trimestre in
      perdita, la probabilità di un mese senza un solo pagamento e il numero di ricalcoli per la rete.
- [ ] **Certificato del token vincente** (vedi fase 4): numero di operazioni di verifica rispetto al
      ricalcolo completo dello strato di uscita su un insieme dato di ingressi.
- [ ] Formula del costo completo della verifica per tre tipi di partecipanti; dopo la fase 5 vi si
      inseriscono le misurazioni.
- [ ] Confronto delle varianti A e B sugli stessi attacchi e allo stesso costo, poi la decisione D3.
      Esito possibile: entrambe le varianti restano di ricerca.

Completato quando: per ogni variante c'è una tabella «quota di collusione → massimo guadagno atteso
dell'ingannatore», ricalcolata su almeno due dispositivi indipendenti.

### Fase 3. Chiudere i buchi noti

- [ ] **Novizio con il conto vuoto.** Candidato: i primi compiti del novizio sono tali che ogni nodo li
      verifica esattamente da sé, e solo dopo si accreditano la ricompensa e il peso. Variante di riserva:
      un budget comune di pagamenti da apprendista per epoca; limita la perdita ma non la rende nulla, e la
      collusione può occupare tutti i posti.
- [ ] **«Onesto a lungo, poi inganna in grande».** Candidato: un tetto sulla somma di tutti gli obblighi
      aperti della chiave, contando i guadagni più grandi possibili. È il limite di una sola ondata, non
      una perdita nulla.
- [ ] **Spazzatura da chiavi gratuite.** Candidato: il nodo accetta dati solo per i numeri di compito
      consentiti, limita dimensione, coda e lavoro per epoca. Il canale si può comunque riempire; non si è riusciti a garantire un posto al novizio onesto quando il numero di chiavi nella rete è arbitrario.
- [ ] **Risultato usato prima della verifica.** Candidato: verificare il blocco di risposta prima della
      consegna; tenere il passo di addestramento in un ramo separato e promuovere solo il discendente
      verificato. Costo: ritardo e memoria.
- [ ] Compiti di addestramento: regola di approvazione senza un partecipante con diritti speciali.
- [ ] Modello raro: una soglia ricavata dalla distribuzione del peso, al di sotto della quale la rete non
      paga per il modello.
- [ ] Verificatore pigro e ripresentazione di un risultato noto: commitment crittografici che nascondono il valore fino alla successiva rivelazione,
      accredito unico in base al contenuto.
- [ ] Guasto dell'attrezzatura di un partecipante onesto: una regola che non dà guadagno all'ingannatore.
- [ ] Disponibilità dei dati e controversia su una richiesta privata senza rivelazione.
- [ ] Finestra di controversia all'arresto della rete, difesa dalla cronologia obsoleta, divisione della
      rete.

Completato quando: per ogni punto sono pubblicati la costruzione con le ipotesi, un attacco a essa e il
costo, oppure un controesempio, oppure lo stato «aperto» con la ragione.

### Fase 4. Ricerca di una garanzia indipendente dalla quota di collusione

Si cerca una verifica che ogni nodo esegue da sé, così che l'accordo dei verificatori non decide nulla.
Le direzioni non sono approvate. Per ciascuna bisogna indicare le operazioni verificate, i dati, la
probabilità di errore e il costo di un'intera richiesta o di un passo; poi portarla a costruzione oppure
chiuderla con un controesempio.

- [ ] **Compiti con un segno di correttezza esatto ed economico.** Esempio: per la regressione ridge il
      nodo verifica la condizione di ottimo in un solo passaggio sui dati. Domanda: quale quota del lavoro
      della rete rientra in tali compiti. Cominciare da questa direzione: dà un pagamento indebito nullo.
- [ ] **Verifica di ogni moltiplicazione di matrici con un vettore casuale** al posto del ricalcolo. Il
      vettore si sceglie dopo la fissazione del risultato; la probabilità di lasciar passare un errore non
      dipende dalla collusione. Conviene per grandi batch; generando un token alla volta non c'è guadagno.
      Le altre operazioni (arrotondamento, attivazioni, cache, ottimizzatore) vanno verificate separatamente.
- [ ] **Verifica di una risposta pronta con un solo passaggio del modello** con profilo esatto e casualità
      fissata nel compito. Il numero di operazioni è dello stesso ordine della generazione; se rientri nel
      5% non è stabilito.
- [ ] **Tabelle di somme parziali esatte per strati invariati:** il nodo ricava una volta le tabelle dai
      pesi e poi ottiene l'uscita dello strato con letture e addizioni. Applicabile anche a un solo token;
      si scontra con la quantità di memoria.
- [ ] **Certificato del token vincente** per un ampio vocabolario: l'esecutore trasmette la copertura del
      vocabolario a gruppi, il nodo verifica i limiti superiori e scende ai singoli token solo dove il
      limite non separa il vincitore. Nel caso peggiore si verifica l'intero vocabolario.
- [ ] **Passo di addestramento come formula esatta di aggiornamento:** i nodi conservano e verificano non
      la nuova matrice dei pesi, ma i moltiplicatori di aggiornamento. Ricavato solo per lo strato lineare
      con un semplice SGD.
- [ ] **Controversia aperta a qualsiasi partecipante durante la finestra.** Garanzia condizionale: serve
      almeno un osservatore che abbia ricevuto i dati e abbia fatto in tempo a obiettare. Chi paga
      l'osservazione con il conto vuoto non è deciso. Lasciare come riserva.
- [ ] **Pagamento per il miglioramento misurato del modello** su compiti scelti dopo la fissazione dei pesi.
      Cambia il fondamento del pagamento e richiede una decisione separata. Adatto alla selezione delle
      versioni del modello.
- [ ] **Prove di calcolo per l'addestramento (sumcheck, GKR)** per un singolo passo determinato: preventivo
      completo con intervalli, arrotondamento e collegamento dell'ingresso al compito.
- [ ] **Limite inferiore:** mostrare quali classi di verifiche non possono essere prive di errori. Inizio:
      un insieme fisso di verifiche lineari in numero minore della dimensione del risultato lascia sempre
      passare qualche errore; restano aperte la casualità fresca e gli ingressi con struttura nota.
- [ ] Idee dei partecipanti e degli assistenti IA dalla bacheca: ciascuna passa per la stessa analisi,
      incluso il caso `q = 1`.

Completato quando: per ogni direzione sono pubblicati una costruzione con preventivo, un controesempio o
un limite dimostrato. È considerata trovata la costruzione che soddisfa tutti i segni della sezione 1.

### Fase 5. Fondamenti che si stabiliscono solo con l'esperienza (consentito da D5)

- [ ] Qwen3.5-4B ad aritmetica intera su due schede video diverse: se i bit coincidono.
- [ ] La sua velocità rispetto al profilo normale sulle stesse schede.
- [ ] La sua qualità rispetto al profilo normale sullo stesso insieme di compiti.
- [ ] Piani di misurazione separati (fuori da D5): energia della verifica, addestramento con aritmetica intera.
- [ ] Costo della controversia nel registro per il modello completo. Prima servono la scelta della
      blockchain, una macchina di riferimento del modello completo, il vincolo sui dati di ingresso, sulla lunghezza e sul percorso del calcolo.

Completato quando: ogni numero è misurato, le condizioni di misurazione sono scritte, la misurazione è
stata ripetuta da un secondo partecipante. La coincidenza dei bit riguarda solo le configurazioni provate.

### Fase 6. Sintesi e accettazione

- [x] Decisione D4 sul nucleo immutabile (sezione 3).
- [ ] La composizione del nucleo e il modo in cui un partecipante si convince che il suo programma
      corrisponde all'impronta pubblicata.
- [ ] Aggiornare CURRENT_DESIGN e la tabella degli attacchi in base agli esiti delle fasi 1–5.
- [ ] Una dichiarazione è tracciata su carta dall'autorizzazione del compito fino all'uso del risultato,
      inclusi rifiuto, ripetizione e divisione della rete.
- [ ] Revisione aperta della costruzione finale: consiglio dei modelli e compito sulla bacheca.
- [ ] Per ogni requisito è pubblicata una dimostrazione, una misurazione, un controesempio o lo stato
      «aperto». Verifica secondo i sei segni della sezione 1.

## 5. Come procede il lavoro

1. Un punto della lista di controllo diventa un compito: di calcolo (lo eseguono i mini-agenti, si verifica che i risultati delle esecuzioni coincidano) o di ricerca (viene pubblicato sulla bacheca).
2. I partecipanti e i loro assistenti IA consegnano relazioni. Una relazione è accettata solo se la si può
   verificare: con un ricalcolo, un controesempio o un riferimento alla fonte. Il numero di chiavi concordi
   non dimostra nulla; la decisione dell'autore del compito sulla bacheca non conferma il calcolo.
3. In base all'esito della verifica il compito si chiude, si precisa o genera nuovi compiti.
4. Il cambiamento di stato viene riportato in questa tabella di marcia e in CURRENT_DESIGN con una sola
   modifica, con la data.

## 6. Che cosa questa tabella di marcia non promette

- Che la soluzione esista nelle condizioni date. È oggetto della ricerca.
- Scadenze. Il progetto non ha esecutori pagati; la velocità dipende dai partecipanti.
- Ricompense per la partecipazione alla progettazione.
