<!-- translation of docs/ANTIFRAUD_OPTIONS.md, source sha256: 63c43d6864c5cccb6fa61953c9ba9594e26e3dba1a4c8241129e6f346bc08f20 -->

# Opzioni contro l'inganno: esito degli audit e del consiglio dei modelli

[English](../../docs/ANTIFRAUD_OPTIONS.en.md) · [中文](../zh/ANTIFRAUD_OPTIONS.md) · [Español](../es/ANTIFRAUD_OPTIONS.md) · [Français](../fr/ANTIFRAUD_OPTIONS.md) · [Deutsch](../de/ANTIFRAUD_OPTIONS.md) · **Italiano** · [Русский](../../docs/ANTIFRAUD_OPTIONS.md) · [Português](../pt/ANTIFRAUD_OPTIONS.md) · [العربية](../ar/ANTIFRAUD_OPTIONS.md)

Stato al 27 novembre 2026.

**Che cosa è stato fatto.** Il proprietario del progetto ha raccolto sei audit indipendenti di completezza e due mappe dei meccanismi di protezione dall'inganno e ha proposto tre idee proprie: incorporare la verificabilità nel modello stesso, prendere tecniche dai giochi e «incrociare» le vie alternative di verifica con il lavoro utile. Il consiglio dei modelli ha scritto undici lavori indipendenti e quattro critiche incrociate e ha riunito tutto questo nelle opzioni descritte qui sotto.

**Stato.** Questo documento è un ragionamento e un calcolo. Le grandezze misurate sono prese solo dall'esperienza D5 ([EXPERIMENT_D5](EXPERIMENT_D5.md)) e sono contrassegnate con [misurato]. Tutto il resto è contrassegnato con [calcolo] o è chiamato ipotesi. Le uniche decisioni accettate restano D1–D25 ([ROADMAP](ROADMAP.md), sezione 3); tutto ciò che qui si propone di cambiare sono proposte del consiglio, non decisioni. Il consiglio non ha eseguito nuovi esperimenti, prototipi e installazioni. La letteratura è citata a memoria dei modelli o secondo i dati degli audit e non è stata verificata con le fonti primarie. Sintesi precedenti: [STRATEGY_SEARCH](STRATEGY_SEARCH.md) e [HIDDEN_DETECTOR](HIDDEN_DETECTOR.md).

**Notazioni.** `R` — il prezzo del compito; `c` — il costo del lavoro onesto nel profilo esatto (intero); `c_f` — i costi dell'imbroglione per la contraffazione; `H_lock` — la somma non maturata bloccata della chiave; `p` — la probabilità di verifica della risposta; `q` — la quota di peso della coalizione tra i verificatori assegnati; `ρ` — il tempo di verifica della risposta pronta in un solo passaggio in frazioni del tempo della sua generazione esatta: 0,10–0,40 con pacchetto 1 e 0,26–0,64 con pacchetto 8 [misurato]; `γ` — il rallentamento del profilo esatto rispetto al normale Q8_0: 1,52–1,78 con pacchetto 1 e 2,47–2,79 con pacchetto 8 [misurato, solo RTX 2060].

## Sintesi breve

1. **Costoso non è verificare, ma calcolare in modo esatto.** La verifica di una risposta costa il 10–40% della sua generazione [misurato], ma la maggiorazione principale è il rallentamento del profilo esatto di 1,52–1,78 volte [misurato]. Il riferimento «circa 5%» con i nuclei attuali è irraggiungibile in qualsiasi opzione, per quanto rara sia la verifica [calcolo].
2. **L'idea «impronte e ricalcolo di un frammento casuale» funziona, ma non come riduzione del costo della garanzia.** Se si aprono `s` frammenti su `N`, una cella sostituita in modo mirato passa con probabilità non inferiore a `1 − s/N`. La valutazione «30 volte più economico, e l'inganno viene comunque catturato» significa in realtà «30 volte meno catture». Le impronte sono utili in un altro ruolo: una radice corta della traccia permette di risolvere una controversia con divisione a metà fino a un solo passo e dà a un dispositivo debole una verifica parziale con una nota onesta.
3. **L'idea «verificabilità dentro il modello» funziona in una sola forma:** fare fine-tuning o riscrivere i nuclei in modo che il profilo esatto diventi veloce. Questo riduce `γ` e non indebolisce la garanzia. Le impronte le scrive un programma, non il modello, e per esse il fine-tuning non serve. Le somme di controllo negli strati proteggono l'esecutore onesto dai guasti dell'attrezzatura, ma non dal dolo.
4. **Dai giochi si trasferisce solo l'ordine delle mosse:** «sigillato → fissazione definitiva → scelta segreta → apertura → ricalcolo». Al calcolo sono agganciate solo due mosse: il ricalcolo del frammento aperto e la verifica del testimone del compito. Un gioco separato accanto al lavoro utile non dimostra nulla.
5. **Le opzioni sono quattro e una sovrastruttura:** la verifica completa di ogni risposta da parte del pagatore; la lotteria su ordini interi; la moneta segreta del pagatore con la somma bloccata; i compiti con esito verificabile; e la decodifica speculativa esatta come possibile modo per ridurre il costo della prima e della terza opzione.
6. **Raccomandazione.** Il contratto principale è la verifica completa di ogni risposta da parte del pagatore nel profilo esatto. Esso è l'unico che soddisfa le decisioni accettate senza modificarle. I compiti con esito verificabile sono un tipo separato di compiti e per ora l'unica garanzia rigorosa per l'addestramento. La lotteria è una tariffa per le partite. La moneta con la somma bloccata resta una candidata fino al calcolo M9 e alle decisioni del proprietario.
7. **Primo passo.** Un calcolo: M9 — controversie false senza deposito, tutti i rami del silenzio e del rifiuto. Un esperimento (con il permesso del proprietario): sui profili già assemblati v2 e llama.cpp Q8_0 misurare la coincidenza dei token con un prefisso comune. Esso risolve subito tre questioni (sezione 5).
8. **Letteralmente irrealizzabile:** proteggere il consumatore senza attrezzatura in caso di collusione totale dei verificatori; verificare il passo di addestramento in caso di collusione totale entro un sovrapprezzo del 20%; contenere una risposta verificata nel 5% con il `γ` misurato. Le attenuazioni minime sono formulate come domande al proprietario nella sezione 7.

## 1. Che cosa hanno trovato gli audit

Etichette degli audit: RU — `SkyNet_audit_completeness_RU`; SC — `skynet_completeness_audit`; GPT — `gpt-SkyNet-audit`; DS — `deepseek-AUDIT_REPORT`; GEM — `gemini_report`; CR — `chat_responses`; le mappe — `mehanizmy-anti-obman` (MEH) e `mechanisms_map_report` (MAP). Dove i lavori del consiglio hanno letto diversamente chi ha chiamato che cosa, questo è contrassegnato con la parola «contestato».

### 1.1. Approcci trascurati

| Approccio | Chi degli audit lo ha nominato | Valutazione del consiglio |
|---|---|---|
| Impronte delle attivazioni, TOPLOC | SC, GPT, GEM, CR, DS (in una riga), MAP; MEH — contestato | Non è una base di pagamento; solo un segnale per una verifica esatta aggiuntiva (sezione 2.4) |
| Schemi ottimistici, controversia con arbitro, divisione a metà | Tutti e sei e entrambe le mappe | Uno strato necessario per la controversia; con la collusione totale non c'è nessuno con cui discutere, quindi non sostituisce la verifica del pagatore |
| Test statistici di sostituzione del modello | GPT, DS, GEM, CR, MAP; SC e RU — contestato | Solo un segnale per aumentare la frequenza di verifica; non entra nel nucleo |
| Aritmetica in virgola mobile riproducibile, nuclei interi tipo Ozaki | SC, GEM, DS, GPT, RU; CR nomina RepOps | L'aritmetica in virgola mobile non sostituisce il profilo intero; l'accelerazione dei nuclei è un'ipotesi da esperimento |
| Somme di controllo ABFT | SC, GEM, DS, GPT, RU | Autocontrollo del nodo onesto contro i guasti; copre solo le moltiplicazioni lineari |
| Verifica di Freivalds | SC, CR, GPT, GEM, le mappe | Funziona per la parte lineare dell'aritmetica esatta con un vettore segreto fresco dopo la fissazione |
| Disponibilità dei dati | SC, DS, GPT; GEM — contrario; RU e le mappe — contestato | Ingegneria della controversia e dell'addestramento, non garanzia R4 |
| Progettazione di meccanismi con verifica costosa | GEM, DS, GPT, SC | Conferma la soglia `R/(R + H_lock)`; non dà una leva nuova |
| Attestazione hardware GPU, TEE | Quasi tutti | Segnale aggiuntivo e modalità di privacy; non si può ridurre la frequenza di verifica in base a essa |
| Fideiussione e assicurazione senza deposito del partecipante | SC, GEM, DS, GPT, RU | Il blocco altrui è in sostanza un deposito di un terzo, una questione per R5; il fondo assicurativo apre l'autocontroversia |
| Esperienza di Bittensor, Gensyn, Prime Intellect, Hyperbolic, Ritual, Atoma, Golem | Tutti e sei e le mappe | Tutti si reggono su un deposito, validatori fidati, TEE o «un onesto»; sono trasferibili singole tecniche |

Da un solo audit sono nominati: le prove campionarie per strati come base (RU), il collegamento del testo cifrato della risposta all'impegno tramite DLEQ (SC), il pool di coupon (SC; secondo uno dei lavori — anche GEM e GPT).

### 1.2. Punti deboli delle conclusioni precedenti

- La soglia `p ≥ R/(R + H_lock)` è valida a tre condizioni che prima non erano state nominate: il prezzo non è inferiore al costo, la moneta viene davvero lanciata, la somma è disponibile per la bruciatura (GPT, SC, GEM, RU).
- La conclusione «il riferimento del 5% è confutato» riguarda una sola implementazione dei nuclei (GEM, SC, DS).
- La barriera delle prove brevi è calcolata per una sola configurazione (SC, GEM, DS, GPT).
- La coincidenza dei bit è mostrata su sei configurazioni, non «su qualsiasi hardware» (DS, GEM, SC, GPT). I critici hanno precisato: per un lungo passaggio su una risposta pronta — su tre.
- L'affermazione «un pagatore pigro e un novizio insieme danno zero» era un errore: il guadagno arriva a `+R`.
- L'enumerazione di «92 milioni di strategie» non dimostra la completezza (RU).
- La letteratura dei consigli precedenti è citata a memoria (RU, GEM, DS, GPT).

### 1.3. Contraddizioni tra requisiti e decisioni

- **D16 contro la verifica a campione.** Se un guasto onesto non è punito, l'imbroglione dichiara la contraffazione un guasto e riceve `(1 − p)·R − c_f` (DS, GEM, RU, SC).
- **D19.** La terza condizione — «l'errore moltiplicato per `R` è minore del costo del tentativo» — non è applicabile quando il tentativo è gratuito (DS, RU; nel consiglio — ChatGPT).
- **L'emissione di crediti per l'addestramento a domanda nulla**, la collusione totale, il sovrapprezzo del 20% e la verifica da parte di ogni nodo insieme non si realizzano (DS, SC, GEM, GPT, CR, MEH).
- **Il consumatore senza attrezzatura e R4** (SC, GEM, RU, CR).
- **D1 letterale esclude qualsiasi campionamento** (RU, DS).
- **La controversia senza deposito e il fondo per le controversie finito** (SC, GEM, GPT, RU).
- **«Prima la piena certezza, poi gli esperimenti»** è stato chiamato circolo vizioso: `γ`, `ρ`, la qualità e la frequenza dei guasti si stabiliscono solo con la misurazione (DS, GPT). Questa è l'opinione degli audit e di un critico; il consiglio non ha violato e non revoca il limite in vigore sugli esperimenti.

### 1.4. Nuovi attacchi

- **Il pagatore pigro.** Se una quota `λ` dei pagatori non verifica, la soglia diventa `R/((1 − λ)(R + H_lock))`; con il conto vuoto è maggiore di uno, e l'imbroglione che ha riconosciuto il pagatore pigro riceve fino a `+R` (SC) [calcolo].
- **La moneta non è imposta:** il programma del pagatore si può ricompilare con `p = 0` (GEM, SC).
- **Rivendita della risposta tra sessioni** («attacco della mafia»): l'intermediario prende l'ordine, compra la risposta da un esecutore onesto e non paga. Funziona senza la collusione dei verificatori; si cura con l'ordine «pagamento anticipato bloccato → risposta → verifica entro il termine → pagamento» (GEM; sviluppato nel consiglio).
- **Vendita della somma non maturata** prima dell'uscita (RU). Si cura con il divieto di trasferimento.
- **L'autopagamento** accresce la somma bloccata e abbassa la frequenza di verifica. La critica ha mostrato che questo non apre l'accesso al denaro (il denaro proprio dell'imbroglione brucia alla cattura), ma rende più economico il danno mirato.
- **Inondazione di chiavi gratuite:** ogni nuova chiave richiede una verifica completa e carica il pagatore; è una negazione del servizio, non un furto.
- **Sostituzione di uno o due token dentro la finestra dell'impronta TOPLOC** (SC).

### 1.5. Che cosa è dubbio nei riferimenti e nei numeri degli audit

- **Accelerazione dei nuclei secondo Ozaki fino a `γ` = 1,05–1,20.** Dubbio: i nuclei veloci di D5 usano già le stesse istruzioni a 8 bit, e con essi è stato misurato 1,52–1,78; 24 blocchi su 32 sono ricorsione, che la decomposizione non accelera. Non si può mettere questo numero nei preventivi accanto a quelli misurati.
- **TOPLOC:** «258 byte per 32 token», «10–100 volte più veloce», «costi aggiuntivi 1–3%». Due lavori lo confermano a memoria, tre — «non posso verificare»; per SkyNet nulla di tutto ciò è stato misurato.
- **Non è stato possibile verificare:** i numeri di DeepProve e FlashProve, Verde (negli audit tre diversi insiemi di sovrapprezzi), le perdite di TEE su H100, il costo di DLEQ in gas, gli stati e gli incidenti di Bittensor e di altre reti, alcuni numeri arXiv.
- **Attribuzioni errate:** l'algoritmo Krum è attribuito ad autori sbagliati (MEH); in un audit c'è un errore aritmetico nella soglia (`c_f ≈ 0,3c`, `p ≥ 0,73`).
- Lo stesso numero in due audit non sono due misurazioni indipendenti: entrambi possono riportare la stessa fonte.

## 2. Le idee del proprietario sviluppate fino a costruzioni

### 2.1. Verificabilità dentro il modello e fine-tuning

- **«Il modello protegge se stesso» non funziona.** I pesi e il codice sono aperti; l'imbroglione non è obbligato a eseguire il modello. Tutti e undici i lavori lo hanno confermato.
- **«Il modello scrive le impronte»** — è un programma di hashing attorno a pesi immutati. Il fine-tuning non serve e non aggiunge nulla.
- **Le somme di controllo negli strati (ABFT)** catturano un guasto casuale. Un avversario consapevole sceglie un errore che conserva la somma. La ricorsione, le tabelle e la divisione nell'attenzione non sono coperti dalle somme. La tesi di alcuni lavori «ABFT elimina il conflitto D16» è stata giudicata esagerata dai critici.
- **Il fine-tuning ha senso solo per ridurre `γ`:** fare in modo che il profilo esatto coincida con i nuclei veloci a 8 bit («canone grezzo», proposta di DeepSeek). I bit restano bit, la garanzia non cambia. Rischio: il primo profilo a 8 bit in D5 è già stato scartato per la qualità [misurato]; il costo dell'addestramento e la perdita di qualità non sono misurati, le GPU-ore nominate nei lavori sono ipotesi.
- **Il fine-tuning «per la resistenza all'arrotondamento»**, affinché il profilo veloce si verifichi con una tolleranza, riporta al contratto con tolleranza (sezione 2.4) e non dà un confine dimostrabile.
- **Un modello con meno stato** riduce il traffico della verifica del frammento, ma non aumenta la quota di sostituzioni catturabili.

**Verdetto:** funziona una sola forma — l'accelerazione del profilo esatto. Si risolve con un esperimento.

### 2.2. Impronte e ricalcolo di un frammento casuale

**Costruzione.** Prima della scelta del verificatore, l'esecutore sigilla con un'unica radice i token e gli stati intermedi. Il verificatore sceglie segretamente un frammento, riceve l'ingresso sigillato del frammento e lo ricalcola nel profilo esatto. Il frammento si può verificare senza ricalcolare tutto l'inizio della risposta: lo conferma anche D5, dove il passaggio a frammenti dà gli stessi hash degli stati [misurato]. L'affermazione di alcuni lavori «non si può ricalcolare un frammento senza il prefisso» è stata respinta dalla critica.

**Perché il confine `1 − s/N` non è aggirato.** L'imbroglione calcola onestamente tutto tranne una cella, e continua onestamente dal valore sostituito. La traccia è coerente ovunque, tranne in una transizione. Se si aprono `s` transizioni su `N`, esisterà una transizione verificata con probabilità non maggiore di `s/N`. Le impronte rendono la menzogna individuabile, ma non la moltiplicano. Il confine può aggirarlo solo una verifica in cui qualsiasi menzogna viola una grande quota di uguaglianze (prove brevi), e il suo costo è quello di prima.

**Due tipi di porzioni** [calcolo sulla configurazione D5]:

| Porzione | Che cosa certifica | Che cosa bisogna trasmettere | Che cosa non cattura |
|---|---|---|---|
| Per strati: un blocco su tutta la sequenza | Una transizione del blocco dall'ingresso presentato; il blocco è circa il 2,65% del passaggio, la testa di uscita circa il 15,1% | 0,78 / 4,9 / 14,6 MiB con 160 / 1000 / 3000 posizioni | Una sostituzione costruita in un altro strato: probabilità 1 su 32–33 |
| Per posizioni: tutti gli strati su un segmento di 64 posizioni | I token del segmento sono uguali alla scelta esatta con lo stato sigillato del confine sinistro | 48 MiB di stato e 64 KiB per ogni posizione precedente: 58 / 110 / 236 MiB | Una posizione sostituita fuori dal segmento: passa con probabilità `1 − L/T`, per esempio 93,6% con 500 + 500 token |

All'esecutore, inoltre, servono 0,13–2,38 GiB di punti di controllo per risposta durante la finestra della controversia [calcolo]. Nel registro può andare solo la radice di 32 byte: lo stato stesso è di 3–5 ordini di grandezza più grande della voce D24.

**La contraffazione «bozza con il profilo veloce + passaggio esatto».** L'ha trovata la critica Claude. L'imbroglione genera la risposta in Q8_0, poi fa un solo passaggio esatto sui token pronti e stampa la traccia. In una tale traccia sono coerenti tutte le transizioni di tutti i blocchi; non coincidono solo le posizioni in cui il token della bozza differisce dalla scelta esatta.

- Il costo della contraffazione è `c·(1/γ + ρ)`, il risparmio rispetto al lavoro onesto è `1 − 1/γ − ρ`: 18,4% con `γ = 1,65`, `ρ = 0,21`; la contraffazione conviene quando `ρ < 1 − 1/γ` (0,34 / 0,39 / 0,44 con `γ` = 1,52 / 1,65 / 1,78) [calcolo].
- La porzione per strati non la cattura (tranne la probabilità 1 su 32–33 sulla testa di uscita).
- La porzione per posizioni di lunghezza 64 la cattura con probabilità del 97%, se i token di Q8_0 e del profilo esatto coincidono nel 95% delle posizioni; 49% con coincidenza del 99%; 29% con 99,5%; 6,5% con 99,9% [calcolo]. La quota di coincidenza non è misurata.
- La verifica completa la cattura sempre. Il buco riguarda solo gli schemi in cui la porzione **sostituisce** il passaggio completo.

Conseguenza: la porzione certifica «l'esecutore ha pagato almeno il passaggio esatto», non «la risposta è stata generata dal profilo esatto». Qui i critici sono divergenti: DeepSeek ritiene che la porzione per posizioni catturi la sostituzione dell'intera risposta con Q8_0 con probabilità 1; MiniMax — che questa probabilità non è misurata; Claude ha portato il calcolo sopra. Decide la misurazione della coincidenza dei token.

La critica MiniMax ha aggiunto: la contraffazione gratuita «interrompere la risposta prima» non crea affatto celle false. La lunghezza della risposta e la causa dell'arresto devono entrare nell'oggetto della verifica.

**Che cosa dà comunque la radice della traccia:**

- **Controversia con divisione a metà.** Due parti con tracce diverse, in un numero logaritmico di mosse, convergono a un solo passo, che ogni nodo ricalcola da sé. La critica ha precisato: le 15–23 mosse dichiarate bastano solo fino alla cella, dentro il blocco servono altre circa 27 divisioni; la regola «il silenzio è una sconfitta» richiede il calcolo M9.
- **Il dispositivo debole.** Un pagatore senza scheda video può verificare un segmento per ogni risposta. Questo dà la nota «verificato parzialmente», non «verificato». Il costo per lui è un traffico di 52–300 MiB per risposta e il tempo del processore; su un telefono non è misurato.
- **L'immutabilità della storia dell'esecutore** e la controversia su una richiesta privata con l'apertura di una cella.

**Verdetto:** la costruzione è possibile e utile per la controversia e per il dispositivo debole, ma non riduce il costo della garanzia D1 e D25. Perché la sostituzione mirata diventi meno vantaggiosa dell'inazione, con 32 blocchi bisogna aprire 2 / 4 / 7 / 10 blocchi con un margine del 5 / 10 / 20 / 30% [calcolo], e anche questo non aiuta contro il danno (D6).

### 2.3. Tecniche dai giochi

| Tecnica | Dove la mossa è agganciata al calcolo | Dove non è agganciata |
|---|---|---|
| «Sigillato — aperto» | Il frammento aperto deve coincidere con il ricalcolo dall'ingresso sigillato | Il sigillo stesso non dimostra nulla: si può sigillare anche una menzogna coerente |
| «Uno taglia — l'altro sceglie» | La scelta avviene dopo la fissazione con la moneta segreta del verificatore | Chi taglia guasta una parte su `N`; non c'è risparmio rispetto alla verifica completa |
| Moneta comune di due parti | Non serve quando in gioco ci sono i soldi di un solo pagatore: basta la sua moneta segreta | Chi si rivela per ultimo fa fallire l'esito svantaggioso; con la collusione totale tutti i contributi sono noti alla coalizione |
| Carte senza croupier (mental poker) | — | Per scegliere il numero del frammento è ridondante: lo fa la stessa cosa una funzione casuale verificabile |
| «Ognuno controlla l'avversario» | Il pagatore verifica la propria risposta — su questo sono costruite tutte le opzioni della sezione 3 | L'esecutore non può punire un pagatore disonesto senza deposito (calcolo M9) |
| Carte marcate, acquirente segreto | — | In una rete aperta il segreto della trappola lo custodisce solo il pagatore, quindi la trappola coincide con la sua verifica ed è più costosa di essa |

Una fonte pubblica comune di casualità serve solo dove si verificano i soldi altrui; allora vale D20 (non meno di due fonti indipendenti).

**Verdetto:** dai giochi sono presi l'ordine delle mosse e il principio principale «verifica chi ha i soldi in gioco». Il gioco non trasforma il campionamento in una verifica completa.

### 2.4. Esecutore veloce e giudice esatto

**Il contratto con tolleranza.** L'esecutore calcola nel veloce Q8_0, il pagatore fa il passaggio esatto e accetta la risposta se in ogni posizione il punteggio del token scelto è inferiore al massimo di non più di `m`. Il vantaggio rispetto al «certificato con margine» respinto in precedenza: il verdetto si calcola con numeri interi ed è identico su qualsiasi dispositivo. Ma la critica ha trovato quattro difetti.

- **La tolleranza legittima risposte altrui.** Qualsiasi bozza più un passaggio esatto mostra all'esecutore tutti i punteggi; egli corregge le posizioni fuori tolleranza e ottiene una risposta ammissibile. Il produttore più economico di una tale risposta è il modello-bozza più economico, non il Q8_0 dello stesso modello.
- **La libertà di scelta è un canale di danno.** Nelle posizioni con uno scarto inferiore a `m` il token lo sceglie l'esecutore, compreso l'arresto anticipato. Esempio: i punteggi «continuare» e «fermarsi» sono 100 e 99; con `m = 1` una risposta interrotta passa la verifica completa. Un tale testo riceverebbe la nota «verificato con tolleranza» — in sostanza è una violazione di D6. Una nota simile il consiglio precedente l'ha già respinta.
- **L'esecutore onesto è costretto a verificare se stesso**, altrimenti perde la somma su un solo valore anomalo, anche su un ingresso scelto dal pagatore. Allora il costo è `1 + ρ·γ`: +15…+71% con pacchetto 1, e con pacchetto 8 non c'è guadagno rispetto alla generazione esatta [calcolo].
- **Il costo dichiarato «+0,01…+2,3%» non ha resistito:** per aprire i frammenti l'esecutore ha bisogno degli hash degli stati del profilo esatto, cioè di un passaggio esatto per ogni generazione [calcolo].

Anche con un esecutore veloce, il passaggio esatto completo del giudice costa su RTX 2060 non meno del 31,9% del tempo della generazione normale [calcolo], quindi questo contratto non contiene ogni risposta nel 5%.

**La decodifica speculativa esatta** è lo stesso contratto con `m = 0`. La bozza si ottiene in qualsiasi modo, si paga solo la risposta bit per bit uguale a quella esatta. Il contratto e la garanzia non cambiano, D6 non è toccato. Il costo dipende dalla quota di coincidenza dei token e dalla lunghezza delle serie coincidenti; stima inferiore `1 + ρ·γ`. Non misurato; con una coincidenza inferiore a circa il 95% risulta peggiore della generazione esatta diretta.

**TOPLOC e impronte con tolleranza in virgola mobile.** L'impronta certifica che le attivazioni sono coerenti con il testo, non da dove viene il testo. Contraffazione: il testo con qualsiasi modello, poi un passaggio del modello dichiarato su questo testo — le impronte sono autentiche. Il verdetto con tolleranza dipende dall'attrezzatura: due nodi onesti possono divergere, quindi non si può bruciare la somma in base a esso, e D4 è violato letteralmente. Perché la tariffa con tolleranza sia economica, il verificatore ha bisogno di un riferimento che non ha, finché non ha calcolato da sé il passaggio esatto.

**Verdetto:** il contratto con tolleranza e le impronte con tolleranza non entrano nell'elenco delle opzioni: cambiano il prodotto e mettono una nota su un testo scelto dall'esecutore. Sono ammissibili solo come segnale per una verifica esatta aggiuntiva. La decodifica speculativa esatta è una candidata alla riduzione del costo, si decide con una sola misurazione.

## 3. Opzioni complete

Il costo è la maggiorazione computazionale completa rispetto alla generazione normale Q8_0 senza verifica [calcolo sulle misurazioni D5]. Non include registro, controversie, archiviazione, traffico ed energia: non sono misurati. Il guadagno è quello atteso, per una sola contraffazione presentata. Il limite inferiore «+67%» combina il `ρ` della scheda RTX 4070 Laptop con il `γ` della scheda RTX 2060; su una sola RTX 2060 l'intervallo parte da +84%.

| № | Opzione | Costo con pacchetto 1 | Denaro dell'imbroglione con `q` = 0,1 / 0,3 / 0,5 / 1 | Novizio con conto vuoto | Danneggiatore senza guadagno | Rischio residuo principale |
|---|---|---|---|---|---|---|
| V1 | Verifica completa di ogni risposta da parte del pagatore | +67…+149% (su una sola RTX 2060 +84…+149%) | `−c_f` con tutti i `q` | `−c_f` | Non c'è una falsa nota «verificato»; può far fallire la consegna | Pagatore pigro; rifiuti falsi del pagatore (M9) |
| V2 | Lotteria su ordini interi | +53…+82% e riserva dell'acquirente `R/p` | `−c_f` con tutti i `q` | 0 | La quota `1 − p` delle risposte non è verificata e non è trattenuta da nulla | Reddito irregolare; la riserva è una questione per R5 |
| V3 | Moneta segreta del pagatore e somma bloccata | +50…+82%; la verifica stessa 0,005–3,6% | Non più di zero con tutti i `q`, se il pagatore lancia la moneta in tempo | `−c_f` (verifica sempre) | Passa la quota `1 − p`: fino al 99,98% | Pagatore pigro riconosciuto — fino a `+R`; un guasto onesto brucia la somma |
| V4 | Compiti con esito verificabile | `(N − 1)·v/w`, non misurato | `−c_f` con tutti i `q` | 0 | Un testimone errato non passa | Non è una risposta del modello né un passo di addestramento |
| V5 | Sovrastruttura: decodifica speculativa esatta sopra V1 o V3 | Non misurato; stima inferiore +15…+71% | Come nell'opzione portante | Lo stesso | Lo stesso | La coincidenza dei token non è misurata |

**Il pagatore senza attrezzatura** in tutte le opzioni non ha garanzia. Se affida la verifica a una terna di nodi assegnati, il pagamento falso atteso è `R·q³`: 0,001`R` / 0,027`R` / 0,125`R` / `R` con `q` = 0,1 / 0,3 / 0,5 / 1 [calcolo]. Questo è già scritto in D21.

### V1. Verifica completa di ogni risposta da parte del pagatore

**Passi.** L'ordine fissa il modello, il profilo, il seme, i limiti di lunghezza e la condizione di accettazione. L'esecutore calcola la risposta nel profilo esatto e con una sola voce fissa il testo cifrato e la radice della traccia. Prima della presentazione il pagatore ricalcola tutta la risposta in un solo passaggio, comprese la lunghezza e la causa dell'arresto. Una divergenza significa mancato pagamento; la somma in attesa non brucia. La nota «verificato» si mette solo dopo il passaggio.

**Garanzia e ipotesi.** Una risposta falsa non viene pagata e non riceve la nota con qualsiasi quota di collusione, per il novizio e per qualsiasi numero di chiavi. Ipotesi: i bit coincidono sul dispositivo del pagatore (mostrato su sei esecutori [misurato], sui telefoni — no); il nucleo di verifica è corretto; il pagatore verifica davvero.

**Costo.** `γ·(1 + ρ) − 1`: +67…+149% con pacchetto 1; +211…+358% con pacchetto 8 (su una sola RTX 2060 +251…+358%). Esempio `γ = 1,65`, `ρ = 0,21`: +99,65%. Al pagatore la verifica costa il 15–71% del tempo della sua propria generazione normale [calcolo].

**Che cosa cambiare nelle decisioni.** Nulla; servono precisazioni di D6 (due note, intermedie non ce ne sono), D16 (con la verifica completa la divergenza comporta solo il mancato pagamento) e D22 (sezione 4).

**Non misurato.** La qualità del profilo esatto (esperimento O5); `γ` su altre schede; tempo e memoria su un portatile e un telefono; il costo della controversia; il comportamento con i rifiuti falsi del pagatore.

### V2. Lotteria su ordini interi

**Passi.** L'acquirente riserva in anticipo il premio. Tutti i risultati della partita sono fissati prima del sorteggio. Il sorteggio sceglie una quota `p` degli ordini; quelli scelti il pagatore li verifica completamente e paga `R/p`; gli altri non sono pagati e sono contrassegnati «non verificato».

**Garanzia e ipotesi.** Un pagamento falso è impossibile anche con il conto vuoto e senza bruciatura delle somme; D16 non va cambiato. Ipotesi: sorteggio secondo D20; la riserva dell'acquirente non è considerata un deposito.

**Costo.** `γ·(1 + p·ρ) − 1`: +53…+82% con pacchetto 1; esempio `p = 0,05`, `γ = 1,65`, `ρ = 0,21`: +66,73%. Ma su un risultato **verificato** ricade `1/p` volte più lavoro.

**Punti deboli.** Il reddito è irregolare: con `p = 0,1` un novizio onesto con probabilità 34,87% non riceverà nulla per i primi dieci ordini; con 6000 compiti al mese, `p = 0,01` e un costo pari al 95% del prezzo, la probabilità di un mese in perdita è 33,10% [calcolo]. Le risposte non verificate non sono trattenute da nulla: il danneggiatore con chiavi gratuite fornisce spazzatura gratis.

**Che cosa cambiare.** Rispondere se la riserva `R/p` è «mezzi in anticipo» secondo R5; scegliere le fonti di casualità secondo D20.

**Non misurato.** La probabilità esatta di rovina lungo il percorso, la dimensione della riserva, la domanda per una tale tariffa.

### V3. La moneta segreta del pagatore e la somma bloccata

Questa è la strategia del consiglio 5 ([STRATEGY_SEARCH](STRATEGY_SEARCH.md)) con correzioni.

**Passi.** La risposta è fissata nel profilo esatto. Dopo la fissazione il programma del pagatore lancia la propria moneta segreta e verifica la risposta completamente con probabilità non inferiore a `R/(R + H_lock)`; per il novizio — sempre. Una divergenza dimostrata con una sola azione brucia tutta la somma non maturata della chiave, comprese le ricompense della stessa ondata; al danneggiato si restituisce non più di `R`. La somma non maturata non si può trasferire, vendere o impegnare. La risposta saltata dalla moneta viene pagata e contrassegnata «non verificato».

**Garanzia e ipotesi.** L'esito atteso di qualsiasi serie di contraffazioni non supera la somma bloccata con qualsiasi quota di collusione: esempio di controllo — un'ondata di dieci contraffazioni dà +4,4295`R` senza bruciatura e −2,49676`R` con essa [calcolo, riprodotto dai critici]. Ipotesi: il pagatore lancia davvero la moneta e verifica in tempo; il registro è disponibile; la somma si perde davvero.

**Costo.** +50…+82% con pacchetto 1; la verifica stessa per le chiavi mature è 0,005–3,6% del lavoro. La prima finestra del novizio costa 1,3–5,3% del lavoro della finestra in unità di generazione esatta [calcolo].

**Punti deboli.** Il buco del pagatore pigro non è chiuso da nessuna correzione: con il conto vuoto e `λ > 0` la soglia è irrealizzabile. Con D16 in vigore l'imbroglione dichiara la contraffazione un guasto e riceve `(1 − p)·R − c_f`. Il danneggiatore passa con probabilità `1 − p`. Un'aggiunta economica è il limite inferiore della frequenza (per esempio, `p ≥ 1/11` costa 0,9–3,6% del lavoro), ma anche allora il 90,9% delle contraffazioni del danneggiatore passa [calcolo].

**Che cosa cambiare.** D2, D11 e D21 (pagamento della risposta saltata dalla moneta); D7; revoca di D16 per una divergenza pubblicata; una nuova decisione sulla somma bloccata; la risposta se la bruciatura è una sanzione secondo R5; il calcolo M9.

**Non misurato.** La frequenza dei guasti silenziosi dell'attrezzatura — da essa dipende quanti partecipanti onesti perderanno la somma; la quota di pagatori che eseguono davvero la verifica.

### V4. Compiti con esito verificabile

**Passi.** Il piano (D9) autorizza in anticipo un compito il cui risultato è accompagnato da un testimone verificabile da una macchina: test, dimostrazione formale, soluzione di un problema con certificato di ottimalità. La domanda è sigillata prima della rivelazione del testimone, perché non si possa intercettare. Ogni nodo verifica da sé il testimone; il pagamento è una volta per il contenuto del compito.

**Garanzia.** Un testimone errato non passa con la collusione totale, il conto vuoto e qualsiasi numero di chiavi.

**Costo.** Se `N − 1` nodi verificano per `v` con un costo di generazione `w`, la maggiorazione è `(N − 1)·v/w`. Con `N = 1000` essa sta nel 20% solo con `v/w ≤ 2·10⁻⁴`; con `v/w = 10⁻³` è già 99,9% [calcolo]. Il rapporto `v/w` è preso dagli audit e non è misurato.

**Punti deboli.** È un altro prodotto: non una risposta libera del modello e non un passo del gradiente. Il compito si può risolvere senza modello e senza scheda video. Una regola che generi compiti difficili utili non è presentata. La verifica del testimone è copiabile, quindi secondo D15 non è pagata: l'idea «il telefono guadagna verificando i certificati» la contraddice.

**Che cosa cambiare.** Integrare D9 e D15; D18 resta una ricerca.

**Non misurato.** Quale quota del lavoro della rete rientra in questa classe.

### V5. Sovrastruttura: decodifica speculativa esatta

La bozza si ottiene in qualsiasi modo veloce; l'esecutore stesso la confronta con un passaggio esatto e corregge le divergenze; si paga solo la risposta bit per bit esatta. La garanzia è la stessa dell'opzione portante V1 o V3; le decisioni, oltre alla precisazione di D22, non cambiano. Il guadagno è possibile solo se i token del profilo veloce e di quello esatto coincidono spesso e in serie lunghe. Nulla di tutto questo è misurato.

## 4. Raccomandazione del consiglio e primo passo

**Raccomandazione (sintesi).** Il contratto principale è **V1**. Esso è l'unico che soddisfa D1, D6, D7 e D25 per la risposta senza nuove ipotesi sulla frequenza, sulla somma bloccata e sulla bruciatura e non richiede modifiche delle decisioni accettate. Tutti e undici i lavori danno per esso la stessa formula del costo. **V4** è un tipo separato di compiti del piano. **V2** è una tariffa per le partite concordate. **V3** è una candidata: includerla solo dopo il calcolo M9 e decisioni esplicite del proprietario. **V5** e l'accelerazione dei nuclei esatti sono vie per ridurre il costo, non contratti separati.

**Precisazioni delle decisioni per V1** (proposte, non decisioni):

- D6: le note sono due — «verificato» dopo una verifica completa bit per bit prima della presentazione e «non verificato».
- D16: con la verifica di ogni risposta da parte del pagatore la divergenza comporta solo il mancato pagamento.
- D19: se il tentativo è gratuito, l'ipotesi di D19 non si applica.
- D22: la bozza si può ottenere in qualsiasi modo; si paga solo la risposta bit per bit uguale a quella esatta. La lunghezza della risposta e la causa dell'arresto entrano nell'oggetto della verifica.
- D12 non cambiare: la sostituzione del tempo attivo con l'altezza dei blocchi della catena esterna permette alle somme non maturate di maturare mentre la rete è indisponibile.
- Una nuova decisione sul prezzo: in quale profilo si conta il volume di calcolo. Con un prezzo di 1,10 rispetto al costo del profilo normale, il lavoro onesto nel profilo esatto è in perdita del 42–68% del costo [calcolo]; questa stessa premessa nel progetto non è approvata.

**Un calcolo.** M9: controversie false senza deposito per un ordine una tantum — il silenzio di ciascuna parte, l'autocontroversia, l'autoordine con una falsa controversia, i limiti di byte e di calcolo per causa, la fonte dei mezzi. Senza di esso non si attiva nessuna opzione (D23).

**Un esperimento** (serve il permesso del proprietario; estensione di O3 e O4 già eseguiti). Sui profili già assemblati v2 e llama.cpp Q8_0, con un prefisso comune, misurare la quota di coincidenza dei token, la distribuzione dello scarto del punteggio del token scelto e le lunghezze delle serie di coincidenza. Esso risolve tre questioni: se V5 si ripaga; se il contratto con tolleranza è vitale; se la porzione per posizioni cattura la contraffazione «bozza + passaggio esatto», cioè se il pagatore senza scheda video ha una qualche protezione. Prima conviene controllare se nelle registrazioni di D5 si sono conservati i punteggi completi di entrambi i profili.

**Dove i critici e i lavori sono divergenti.**

1. **Quale contratto è quello principale.** I critici Claude e ChatGPT — V1. Il critico DeepSeek — V3 con correzioni, e V1 come tariffa costosa e modalità per il novizio. Il critico MiniMax — V1 come tariffa di base e moneta per le chiavi mature, ma la rete paga solo per il verificato.
2. **Se pagare la risposta saltata dalla moneta.** A favore — la maggioranza dei lavori; contro — entrambi i lavori ChatGPT e un lavoro MiniMax. Se non si paga, l'esecutore onesto riceve `p·R` per il compito, e questa è una lotteria senza il moltiplicatore `1/p`. Una terza via non c'è; è una scelta del proprietario.
3. **Quale esperimento è il primo.** I critici Claude e ChatGPT — la coincidenza dei token dei due profili. I critici DeepSeek e MiniMax — un microbenchmark dei nuclei a 8 bit tipo Ozaki con confronto bit per bit: mostra se il riferimento del 5% è raggiungibile in generale. La sintesi lo mette al secondo posto.
4. **Il `γ` raggiungibile.** 1,05–1,20, 1,1–1,3 o «non scenderà». Non misurato.
5. **Se sono un deposito secondo R5** la bruciatura della somma non maturata, la riserva della controversia, la riserva della lotteria, il lungo termine di maturazione e la fideiussione.
6. **Se limitare dall'alto la somma bloccata.** Un tetto di 10`R` limita il numero atteso di contraffazioni, ma rende la verifica delle chiavi mature circa 400 volte più costosa [calcolo di un critico, non ricontrollato].
7. **Una terza nota.** Il critico MiniMax propone «verificato parzialmente»; il critico Claude — solo due note.

## 5. Addestramento: che cosa c'è e che cosa non c'è

**Che cosa non c'è.** Nessun lavoro dà una garanzia per il passo di addestramento. L'addestramento non ha un pagatore: la base dell'emissione di crediti deve verificarla ogni nodo completo. L'addestramento a numeri interi non è costruito né misurato; le misurazioni D5 riguardano solo il passaggio diretto e non si trasferiscono al passaggio inverso e all'ottimizzatore.

**Che cosa c'è.**

- **La ripetizione completa del passo da parte di ogni nodo** — rigorosa, ma costa `N` passi aggiuntivi: con dieci nodi circa il 1000% [calcolo].
- **Porzioni del passo:** un nodo verifica una cella su circa quattromila. Costo 0,24% / 2,4% / 24% con 10 / 100 / 1000 nodi [calcolo], ma con la collusione totale la cattura è zero.
- **Il pagamento dell'esito verificabile** (V4): garanzia rigorosa per un'affermazione ristretta. Si verifica il testimone del compito, non il passo del gradiente; le formulazioni dei lavori «l'addestramento è risolto» e «il danno è escluso» la critica le ha giudicate esagerate.
- **Il pagamento per un miglioramento dimostrato all'esame** (D18) resta una ricerca: l'esame certifica il punteggio su un insieme dato, ma non l'assenza di una backdoor nei pesi.

**Il limite.** Con 1000 nodi e un sovrapprezzo del 20%, tutta la verifica indipendente di un nodo deve costare non più di 0,0002 del lavoro del passo [calcolo]. Una prova breve del passo, secondo tutti i preventivi del progetto, è di ordini di grandezza più costosa.

**Raccomandazione del consiglio.** Emettere crediti solo per i risultati che ogni nodo verifica da sé; un passo non verificato non includerlo nella versione del modello (questo è già D6).

## 6. Che cosa è letteralmente irrealizzabile: domande al proprietario

Il consiglio non propone di cambiare i testi R1–R6. Le proposte di due lavori di modificare R4 e R6 la critica le ha respinte: è una base immutabile. L'impossibilità generale di conciliare R4 e R6 per tutti gli algoritmi concepibili non è dimostrata; qui sotto — ciò che è irrealizzabile con le costruzioni trovate.

| № | Che cosa è irrealizzabile | Attenuazione minima | Raccomandazione del consiglio |
|---|---|---|---|
| 1 | Proteggere il consumatore senza attrezzatura con la collusione totale dei verificatori: i casi onesto e falso gli danno messaggi identici | La garanzia è promessa solo alla parte che verifica da sé; agli altri la risposta è mostrata con la nota «non verificato», e la grandezza del rischio `R·q³` è nominata direttamente | Accettare: è già scritto in D21, basta trasferirlo nella descrizione per l'utente |
| 2 | Verificare il passo di addestramento con la collusione totale entro il 20% | (a) pagare per l'esito verificabile, non per il passo; (b) ammettere «almeno un nodo completo onesto»; (c) togliere il riferimento del 20% per una piccola rete | (a): l'unica via con garanzia rigorosa; al tempo stesso una parte della capacità libera resta senza addestramento pagato |
| 3 | Contenere la risposta verificata nel 5% con il `γ` misurato = 1,52–1,78 | Considerare il riferimento del 5% un obiettivo ingegneristico, pubblicare il costo effettivo e condurre la riduzione di `γ` come compito separato | Accettare; il 5% è un riferimento della tabella di marcia, non il testo di R6 |
| 4 | Contenere con l'economia un danneggiatore a cui non serve il guadagno, con `p < 1` | Solo le note e il divieto di usare il non verificato (D6) | Già accettato; non ci sono misure nuove |
| 5 | Controversia senza deposito con un fondo per le controversie finito | Decidere se il pagamento anticipato bloccato dell'acquirente è considerato un deposito secondo R5 | Decidere dopo il calcolo M9 |
| 6 | Essere completamente sicuri della decisione prima di qualsiasi misurazione | Consentire un elenco limitato di misurazioni da cui dipende la scelta | Decisione del proprietario; il consiglio nomina due misurazioni della sezione 4 e l'esperimento O5 |

Domande aggiuntive: se pagare la risposta saltata dalla moneta (sezione 4, punto 2); in quale profilo si calcola il prezzo del compito; se ammettere la fideiussione di un terzo.

## 7. Che cosa calcolare con i mini-agenti e che cosa verificare con esperimenti

**Calcoli** (frazioni esatte, hash di controllo, ripetizione su un secondo dispositivo; non sono esperimenti sul protocollo):

1. M9 per tutti i rami dell'ordine una tantum.
2. Il guadagno della contraffazione «bozza + passaggio esatto» sotto le porzioni su una griglia di `γ`, `ρ`, quota di coincidenza, lunghezza del segmento e della risposta, margine.
3. La moneta con il limite inferiore della frequenza e la quota di pagatori pigri, compreso il conto vuoto.
4. La contraffazione mista «tutto onesto tranne una colonna» e la contraffazione con l'interruzione della risposta.
5. La lotteria: la probabilità esatta di rovina lungo il percorso e la dimensione della riserva dell'acquirente.
6. Le dimensioni esatte dell'ingresso della cella e del passo della controversia secondo il prospetto del profilo v2 (verificare 48 MiB e 64 KiB).
7. L'inondazione con nuove chiavi: il carico sul pagatore e la derivazione della quota di nuove chiavi.
8. L'enumerazione dei più piccoli insiemi falsi di celle su un modello piccolo.
9. La combinazione di `ρ` e `γ` su una sola scheda e con lunghezze uguali; il costo per un risultato verificato.

**Esperimenti.** O5 è autorizzato dalla decisione D5. Gli altri sono fuori da D5 e richiedono il permesso del proprietario:

1. La coincidenza dei token e lo scarto dei punteggi di Q8_0 rispetto a v2 — il primo esperimento.
2. O5 — la qualità del profilo v2 su 320 compiti.
3. Il microbenchmark dei nuclei a 8 bit con confronto bit per bit — la verifica della valutazione di Ozaki.
4. `γ` e `ρ` in coppia su una sola scheda, compresa RTX 4070 Laptop.
5. Tempo e memoria del passaggio e del segmento sul processore di un portatile e su un telefono.
6. Il costo della stampa della traccia, la copertura di ABFT e la frequenza dei guasti silenziosi.
7. Gli esperimenti sull'addestramento O6 e O7 — separatamente, dopo la decisione su D18.

## 8. Chi ha fatto che cosa

- **ChatGPT:** due lavori indipendenti e la critica di tutti i lavori.
- **DeepSeek:** due lavori indipendenti e una critica con il ricalcolo dei numeri in aritmetica esatta.
- **Claude:** due lavori indipendenti, la critica e questa sintesi.
- **MiniMax:** cinque lavori indipendenti e la critica.
- **Gemini** non ha partecipato al consiglio: nell'hub dei modelli non c'era la chiave; il suo audit era tra i dati di input.
- **Gli audit esterni e le mappe dei meccanismi** — dati di input raccolti dal proprietario; il consiglio non li ha ricontrollati sulle fonti primarie.

Limiti della sintesi: il critico ChatGPT ha analizzato dieci lavori su undici; il critico Claude ha letto uno dei lavori non per intero; i calcoli dei critici sono stati eseguiti ciascuno su un solo computer e attendono la ripetizione da parte dei mini-agenti.
