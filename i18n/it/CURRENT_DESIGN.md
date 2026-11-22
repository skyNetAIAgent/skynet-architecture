<!-- translation of docs/CURRENT_DESIGN.md, source sha256: a4c162fa040254e708d1d2a816f908416be83f27576a99e7dd1174c85218fced -->

# Progetto attuale dell'architettura

[English](../../docs/CURRENT_DESIGN.en.md) · [中文](../zh/CURRENT_DESIGN.md) · [Español](../es/CURRENT_DESIGN.md) · [Français](../fr/CURRENT_DESIGN.md) · [Deutsch](../de/CURRENT_DESIGN.md) · **Italiano** · [Русский](../../docs/CURRENT_DESIGN.md) · [Português](../pt/CURRENT_DESIGN.md) · [العربية](../ar/CURRENT_DESIGN.md)

Stato al 22 novembre 2026. È un **progetto, non un'implementazione**. Non ci sono stati esperimenti su di esso. I numeri con la nota [calcolo] sono ottenuti da una formula, non misurati.

## Dove siamo ora

L'idea è formulata nel [manifesto](MANIFESTO.md), i requisiti obbligatori sono approvati, la base dell'architettura è scelta: una rete senza coordinatori, un registro comune su una blockchain pubblica, il pagamento per il lavoro verificato e il pagamento differito al posto del deposito. Un piccolo progetto pilota fidato ha già eseguito il modello Qwen su diversi computer ([esiti del progetto pilota](PILOT_RESULTS.md)).

La cosa più difficile deve ancora venire. Un modo economico di verificare il lavoro in modo che l'inganno sia inutile persino in caso di collusione non è ancora stato trovato. Un modello che migliora sé stesso in modo affidabile e segue le Leggi di SkyNet resta per ora un obiettivo di ricerca. I compiti per i coautori sono nelle [questioni aperte](OPEN_QUESTIONS.md).

Note di stato:

| Nota | Significato |
|---|---|
| **Accettato** | Approvato nel progetto come decisione |
| **Candidato** | Variante scelta, non ancora approvata né costruita |
| **Proposta** | Sottoposta a decisione, non approvata |
| **Aperto** | Nessuna decisione |

## 1. Schema generale (accettato come base)

Nella rete **non ci sono coordinatori** e non ci sono ruoli con diritti speciali. Tutti i partecipanti hanno lo stesso programma. Entro i cursori delle risorse, esso da solo:

| Lavoro | Cosa fa | Per cosa viene pagato |
|---|---|---|
| Calcola | Esegue un passo di addestramento o una richiesta dell'utente | Per il risultato accettato |
| Verifica | Ricalcola il risultato altrui, se il sorteggio l'ha scelta | Per la verifica eseguita |
| Controlla | Può ricalcolare qualsiasi risultato e contestarlo | Parte di ciò che viene sottratto quando trova una contraffazione |
| Conserva e distribuisce | Tiene i dati con cui lavora | Paga il destinatario dei dati |
| Scrive nel registro | Raccoglie le registrazioni dei partecipanti nella blockchain | Rimborso delle spese |
| Aiuta a farsi trovare | Ritrasmette le connessioni per i dispositivi dietro un router | Rientra nel pagamento della consegna |

**Il registro comune** è un contratto su una blockchain pubblica esistente, senza chiave di amministratore. Conserva le regole e l'impronta del programma, i conti (crediti disponibili, somma in sospeso, peso del lavoro verificato), le impronte dei risultati consegnati, le controversie, le votazioni, il catalogo dei modelli e il piano di addestramento. Il registro funziona anche quando tutti i nodi di SkyNet sono spenti. La blockchain **non è scelta** (Aperto).

**La casualità pubblica** decide a chi tocca il compito, cosa viene verificato e chi verifica. Compare dopo che il risultato è stato fissato. Candidato: una miscela del beacon drand e della casualità della blockchain (Candidato, fonti non scelte).

## 2. Vita del compito (candidato)

1. Il compito di addestramento deriva dal piano comune della rete; la richiesta arriva dall'utente con il pagamento.
2. L'esecutore è assegnato dalla casualità tra i dispositivi con risorse adatte.
3. Il programma calcola e registra le impronte degli stati intermedi.
4. L'impronta del risultato entra in un pacchetto, il pacchetto nel registro. La ricompensa va nella somma «in sospeso».
5. La casualità, dopo la consegna, decide se il compito viene verificato.
6. Il compito scelto viene ricalcolato in modo indipendente da tre partecipanti casuali, alla cieca.
7. Coincide bit a bit — confermato. Non coincide — controversia, che viene risolta dal ricalcolo del passo elementare contestato **nel registro stesso**, non da una votazione.
8. La finestra di verifica dura tre giorni: chiunque può contestare il risultato.
9. Dopo la finestra la ricompensa diventa disponibile.

**Pagamento differito al posto del deposito (accettato).** Del risultato il partecipante risponde solo con la somma in sospeso — le proprie ricompense degli ultimi tre giorni. Non si prende nulla in anticipo; i crediti già disponibili non vengono mai sottratti.

## 3. Come rendere l'inganno in perdita: due varianti

### Variante A. Verifica a campione con sottrazione (specifica attuale)

La frazione di verifica `p = 4R / (R + H)`, ma non inferiore all'1%; la sottrazione per un risultato errato `B = 4R/p − R`, non superiore alla somma in sospeso `H` (`R` è il prezzo del compito). Allora ogni contraffazione costa in media quattro prezzi del compito a qualsiasi frequenza di verifica [calcolo]. La contraffazione passa solo se tutti e tre i verificatori sono in collusione: con quota di collusione `q` la probabilità è `q³`. L'inganno è in perdita finché il gruppo in collusione detiene meno di ~91% del peso dei verificatori [calcolo].

**Debolezza.** Una contraffazione non verificata viene pagata e resta nella rete. È una scommessa che ha esiti vincenti per l'ingannatore.

**Calcolo preliminare (22 novembre 2026, un solo computer, non confermato da altri partecipanti).** La stima «91%» è ottenuta dalla media su una singola contraffazione. Non tiene conto che il partecipante può perdere non più della somma in sospeso: non ci sono depositi né multe. Per un partecipante che se ne va e consegna contraffazioni a raffiche prima che le verifiche finiscano, l'enumerazione esatta delle strategie nel modello `exit-scam-a` dà un limite più basso [calcolo]:

| Regole | Andarsene con contraffazioni è vantaggioso a partire dalla quota di collusione |
|---|---|
| Compiti piccoli identici, 399 prezzi in sospeso, una raffica | 89,2% |
| Compiti piccoli identici, 1200 prezzi in sospeso, una raffica | 90,8% |
| Compiti piccoli identici, tre raffiche, regola «in lavorazione non più di un terzo» | 89,0% |
| Compiti di dimensione arbitraria, tre raffiche, regola «non più di un terzo» | 87,5% |
| Compiti di dimensione arbitraria, due raffiche fino a 100 compiti, senza la regola «non più di un terzo» | 80% |
| Senza collusione, compiti di dimensione arbitraria, due raffiche (92 milioni di strategie) | non vantaggioso |

Senza la regola «non più di un terzo», le ricompense non verificate della prima raffica aumentano la somma in sospeso e la dimensione ammissibile dei compiti della seconda, quindi questa regola è obbligatoria. Il modello è scritto all'inizio del file del kernel [exit_scam_a.py](../../agent/skynet_agent/kernels/exit_scam_a.py) e riproduce i numeri dell'esempio della specifica («circa 78, 107 e 17»). I compiti sono descritti in [tasks/README.md](../../tasks/README.md), la prima esecuzione in [results/FIRST_RUN.md](../../results/FIRST_RUN.md). Questi numeri diventeranno il risultato del progetto dopo la conferma indipendente da parte di altri partecipanti.

### Variante B. La rete paga solo per ciò che è verificato (proposta, in attesa di decisione)

Il compito diventa un biglietto della lotteria. Il sorteggio sceglie una frazione `p` di compiti (per esempio, 1%); solo questi vengono verificati e **solo questi vengono pagati, ma `1/p` volte di più**. In media un partecipante onesto riceve lo stesso, mentre una contraffazione non scelta non porta **nulla**.

- Senza collusione una contraffazione porta esattamente zero.
- Con la collusione un pagamento falso non più spesso di `q^k` per compito verificato (k è il numero di verificatori): 0,1% con q = 10% e k = 3 [calcolo]. Ogni tentativo fallito brucia l'intera somma in sospeso.
- Buchi trovati: un novizio in collusione riceve in media `q^k` del prezzo per tentativo e non perde nulla; una «campagna di uscita» di molte contraffazioni in una volta. Sono proposte delle riparazioni: posti da apprendista con un budget limitato, annullamento di tutte le vincite non maturate della chiave quando una contraffazione viene colta, tetto ai compiti aperti.
- Prezzo: il reddito diventa irregolare. Per un dispositivo debole circa ±13% al mese [calcolo].

Entrambi gli schemi richiedono la **coincidenza del risultato bit a bit** su dispositivi diversi. Percorso proposto: aritmetica intera (int8/int32) del modello, dove l'ordine dell'addizione non influisce sul risultato. **La velocità e la qualità del Qwen intero non sono misurate**; un profilo int8 riproducibile noto era 5,2 volte più lento di quello normale (Aperto).

Controversia a basso costo: dividendo il calcolo a metà fino a una singola operazione, poi verifica della moltiplicazione di matrici con un vettore casuale (algoritmo di Freivalds). Risparmio di circa 100 volte nel numero di moltiplicazioni su matrici grandi, 2,6 volte su LoRA, nessun guadagno nella generazione un token alla volta [calcolo] (Candidato).

## 4. Peso e nuovi partecipanti (candidato)

- **Il peso** è la somma dei prezzi dei risultati che hanno superato la verifica negli ultimi 30 giorni. Non può essere comprato, trasferito o accumulato. Il numero di account non dà nulla: le probabilità e i voti sono proporzionali al peso.
- **Il novizio** prima fa ricontrolli «da apprendista» dei compiti altrui: la sua risposta non decide nulla e viene pagata solo se coincide con il risultato accettato. Poi riceve compiti che vengono verificati sempre, poi sempre più di rado.
- Il peso è calcolato per ciascun modello separatamente. Per un modello che pochi portano avanti, la cerchia dei verificatori è piccola ed è più facile impadronirsene (Aperto).

## 5. Trovarsi e ripristino (candidato)

| Dove | Cosa sopravvive allo spegnimento completo |
|---|---|
| Registro nella blockchain pubblica | Regole, conti, peso, impronta del modello, piano di addestramento, controversie, indirizzi dei nodi che hanno scritto |
| Dischi dei partecipanti e mirror pubblici | Pesi del modello, stato di addestramento, dati; qualsiasi copia viene confrontata con l'impronta del registro |
| Distribuzione del programma | Identificativo di rete, indirizzo del registro, elenco iniziale dei luoghi di incontro |

Tre modi indipendenti per farsi trovare, ne basta uno qualsiasi: registrazioni firmate su piattaforme esterne («luoghi di incontro»), reti aperte di ricerca dei nodi (per esempio, DHT libp2p), indirizzi nel registro stesso. La finestra di verifica non avanza mentre la rete è ferma, altrimenti una contraffazione potrebbe essere consegnata prima dell'arresto.

Punti deboli: l'autenticità della prima installazione (il novizio apprende l'indirizzo del registro dall'esterno); il blocco completo di tutte le vie in una volta; la fiducia in due dei tre fornitori del punto di controllo dopo una lunga inattività.

## 6. Richieste e riservatezza (candidato)

La richiesta viene cifrata per il dispositivo dell'esecutore e viaggia direttamente o tramite un ripetitore sotto pseudonimo. Nel registro ci sono solo impronte. Circa l'1% delle richieste è visto anche da tre verificatori.

**Avvertenza onesta.** Su un computer normale, il proprietario del dispositivo con un programma modificato può leggere la richiesta che esso calcola. I calcoli completamente omomorfi per modelli del genere sono migliaia di volte più lenti. Perciò due modalità: normale (economica) e protetta (solo su hardware che dimostra che il proprietario non guarderà dentro; più cara, poggia sulla fiducia nel produttore).

## 7. Addestramento e scelta del piano (proposta)

Un catalogo aperto di modelli e insiemi di dati con licenze libere, fissati tramite impronte. La rete, secondo una regola, compone varianti di addestramento, dà a ciascuna un giro di prova, divide la capacità libera in base ai risultati e alla votazione per peso. Una nuova versione del modello sostituisce la precedente solo se ha superato meglio l'esame, i cui compiti sono scelti dalla casualità dopo il fissaggio dei pesi. Il contributo di un singolo compito all'aggiornamento dei pesi è limitato; la parte «leggera» del passo (la somma dei contributi) viene sempre ricalcolata.

Un modello che **migliora sé stesso in modo affidabile e infinito** è un obiettivo di ricerca, non una tecnologia pronta. Prima fase realistica: addestramento aggiuntivo automatico e selezione tramite esame.

## 8. Cambio delle regole (candidato)

Le regole le cambia solo una nuova versione del programma, accettata dai 3/4 di **tutto** il peso dopo una votazione non più breve di 14 giorni e con un termine annunciato di 30 giorni. Il freno comune (più della metà del peso) può solo fermare una nuova versione del modello. Proposta: un nucleo di verifica immutabile, che non può essere revocato con una votazione (in attesa di decisione).

## 9. Riepilogo degli attacchi

Dei 60 modi di ingannare analizzati: 18 sono chiusi, 6 in perdita, 19 limitati, 16 aperti (per la variante A). Principali punti aperti:

1. **Maggioranza per peso.** Un gruppo con 3/4 del peso può cambiare le regole; in una rete piccola una quota del genere può essere raggiunta con lavoro onesto su capacità in affitto. Perciò l'avvio è chiuso, con crediti di addestramento.
2. **Fondamenta non costruite.** La coincidenza bit a bit e il ricalcolo della controversia nel registro per un modello completo non sono costruiti.
3. **Un sabotatore a cui non serve il profitto.** Può rovinare l'addestramento entro la quota del proprio lavoro; le backdoor nascoste non vengono colte dall'esame.
4. **Le richieste altrui** nella modalità normale e nelle controversie.
5. **Disponibilità dei dati.** La controversia «ha consegnato o no i dati grandi» non ha nulla con cui essere giudicata.
6. **Ingresso nella rete.** La coda per i posti da apprendista e l'autenticità della prima installazione.

Dettagli e compiti per i coautori sono in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md).
