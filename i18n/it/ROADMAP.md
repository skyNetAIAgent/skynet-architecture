<!-- translation of docs/ROADMAP.md, source sha256: 4cd77f720933922c55c4d78c3e761ca614215cc0ed8610b0fb2ae2e3fbee22e2 -->

# Tabella di marcia: difesa dall'inganno

[English](../../docs/ROADMAP.en.md) · [中文](../zh/ROADMAP.md) · [Español](../es/ROADMAP.md) · [Français](../fr/ROADMAP.md) · [Deutsch](../de/ROADMAP.md) · **Italiano** · [Русский](../../docs/ROADMAP.md) · [Português](../pt/ROADMAP.md) · [العربية](../ar/ROADMAP.md)

Stato al 23 novembre 2026. È un **piano di lavoro, non una promessa di risultato**. Il segno `[x]`
significa «fatto, e lo si può verificare nel repository o nelle registrazioni della rete»; `[ ]` significa
«non fatto». I numeri con la nota [calcolo] sono ottenuti da una formula, non misurati. La tabella di
marcia viene aggiornata a ogni cambiamento di stato.

## 1. Obiettivo e segni di completamento

**Obiettivo della fase attuale del progetto:** trovare un modo di verificare l'onestà per il quale siano
soddisfatti insieme i requisiti obbligatori ([REQUIREMENTS](REQUIREMENTS.md)):

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
| La rete paga per il risultato verificabile, non per la risorsa | Base del progetto; l'unità di risultato e la condizione di accettazione attendono di essere fissate (D2) | [CURRENT_DESIGN](CURRENT_DESIGN.md), sezione 1 |
| Pagamento differito al posto del deposito: il partecipante risponde solo con la somma in sospeso | Accettato | CURRENT_DESIGN, sezione 2 |
| Variante A: verifica a campione con annullamento delle ricompense non ancora maturate | Specifica attuale | CURRENT_DESIGN, sezione 3 |
| Variante B: la rete paga solo per i compiti verificati, `1/p` volte di più | Proposta (D3) | CURRENT_DESIGN, sezione 3 |
| Coincidenza del risultato bit a bit tramite aritmetica intera | Candidato, non misurato | OPEN_QUESTIONS, Q2 |
| Controversia per dimezzamento con ricalcolo di un passo nel registro | Misurato per una riga del modello; per il modello completo non costruito | [PILOT_RESULTS](PILOT_RESULTS.md) |
| Verifica della moltiplicazione di matrici con un vettore casuale dentro la controversia | Candidato, c'è solo una stima calcolata | CURRENT_DESIGN, sezione 3 |
| Nucleo di verifica immutabile, che non si può revocare con una votazione | Proposta (D4) | CURRENT_DESIGN, sezione 8 |

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
- La prima esecuzione dei calcoli (702 porzioni) è stata fatta su un computer. Un secondo dispositivo entro
  il 22 novembre ha ricalcolato 40 porzioni; tutte sono coincise. Le sue registrazioni sono firmate con la
  chiave `46000d30…` e sono disponibili sul nodo completo. Le restanti 662 porzioni non sono confermate in
  modo indipendente.

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

## 3. Decisioni in attesa di approvazione

Finché una decisione non è presa, i punti del piano che ne dipendono restano proposte.

| N. | Domanda | Che cosa dipende da essa |
|---|---|---|
| D1 | Che cosa si accetta come garanzia. Basta «l'inganno non rende nulla, ciò che si è speso va perso, il lavoro onesto conviene di più»? È ammessa una perdita limitata in caso di collusione, o un pagamento indebito va escluso anche con collusione completa dei verificatori | Segni di completamento, fasi 3 e 4 |
| D2 | Fissare il pagamento per il risultato verificabile al posto della potenza e del tempo; definire l'unità di risultato e la condizione di accettazione | Fasi 2–6 |
| D3 | Variante A, variante B o nessuna. Si decide dopo il confronto sugli stessi attacchi e allo stesso costo (fase 2) | Fasi 3 e 6 |
| D4 | Il nucleo di verifica immutabile e che cosa vi rientra | Fase 6 |
| D5 | Prima esperienza: Qwen3.5-4B ad aritmetica intera su due schede video diverse (se i bit coincidono, velocità, qualità) | Fase 5 |

## 4. Fasi e lista di controllo

Le fasi 1–4 procedono in parallelo: sono calcoli e ragionamenti. La ricerca di nuovi algoritmi (fase 4)
non aspetta le altre. La fase 5 richiede la decisione D5. La fase 6 riunisce i risultati.

### Fase 0. Strumenti di collaborazione

- [x] Repository pubblico, base immutabile in nove lingue (etichetta `core-v1`).
- [x] Programma-agente per Windows, Linux e macOS: compiti e aggiornamenti firmati,
      verifiche automatiche su tre sistemi (versione 0.2.0).
- [x] Risultati e [bacheca dei compiti](BOARD.md) senza account.
- [x] Primo nodo completo, che conserva la cronologia delle registrazioni.
- [x] Primo compito di ricerca «Difesa dai truffatori» sulla bacheca, in nove lingue.
- [ ] Relazione su un compito della bacheca da parte di un partecipante non legato ai manutentori, con
      l'indicazione di chi e come l'ha ottenuta. Ora tutte le registrazioni nella rete sono fatte dai
      dispositivi dei manutentori. Chiavi diverse non dimostrano proprietari diversi.
- [ ] Conferma indipendente di tutte le 702 porzioni del primo elenco di compiti (ora 40).
- [ ] Aggiornamento dell'agente da una versione rilasciata alla successiva, osservato su un'installazione
      reale (ora verificato solo con i test).
- [ ] Applicazione Android: verifica su un telefono reale, pubblicazione dei risultati senza token.
- [ ] Installazione senza Python già installato: un solo file per Windows, macOS e Linux.
- [ ] Istruzioni per l'assistente IA: come prendere un compito dalla bacheca, consegnare una relazione e
      verificare quella altrui.
- [ ] Ciclo automatico per gli assistenti IA: l'agente prende da solo i nuovi compiti della bacheca e li
      passa al modello locale del partecipante. Ora si fa con comandi a mano.
- [ ] Secondo e terzo nodo completo presso proprietari diversi.
- [ ] Correggere la riga obsoleta in BOARD («l'agente 0.2.0 non è ancora uscito»).

### Fase 1. Formulazione precisa

- [ ] Le decisioni D1 e D2 sono prese e scritte.
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

### Fase 5. Fondamenti che si stabiliscono solo con l'esperienza (richiede D5)

- [ ] Qwen3.5-4B ad aritmetica intera su due schede video diverse: se i bit coincidono.
- [ ] La sua velocità rispetto al profilo normale sulle stesse schede.
- [ ] La sua qualità rispetto al profilo normale sullo stesso insieme di compiti.
- [ ] Piani di misurazione separati (fuori da D5): energia della verifica, addestramento con aritmetica intera.
- [ ] Costo della controversia nel registro per il modello completo. Prima servono la scelta della
      blockchain, una macchina di riferimento del modello completo, il vincolo sui dati di ingresso, sulla lunghezza e sul percorso del calcolo.

Completato quando: ogni numero è misurato, le condizioni di misurazione sono scritte, la misurazione è
stata ripetuta da un secondo partecipante. La coincidenza dei bit riguarda solo le configurazioni provate.

### Fase 6. Sintesi e accettazione

- [ ] Decisione D4 sul nucleo immutabile — prima della verifica finale sulla cattura della maggioranza.
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
