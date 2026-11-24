<!-- translation of docs/VERIFICATION_SEARCH.md, source sha256: cdf54a57e7747ae1f862b5b29fa7a53eee7fca80d8bae17a0cbc60f022cec00b -->

# Ricerca di una verifica indipendente dalla quota di collusione

[English](../../docs/VERIFICATION_SEARCH.en.md) · [中文](../zh/VERIFICATION_SEARCH.md) · [Español](../es/VERIFICATION_SEARCH.md) · [Français](../fr/VERIFICATION_SEARCH.md) · [Deutsch](../de/VERIFICATION_SEARCH.md) · **Italiano** · [Русский](../../docs/VERIFICATION_SEARCH.md) · [Português](../pt/VERIFICATION_SEARCH.md) · [العربية](../ar/VERIFICATION_SEARCH.md)

Stato al 24 novembre 2026.

Questo documento è il risultato del consiglio dei modelli per la fase 4 della tabella di marcia («Ricerca di una garanzia indipendente
dalla quota di collusione», [ROADMAP](ROADMAP.md), sezione 4). Il consiglio cercava una verifica che ogni nodo
esegue da sé, così che l'accordo o la collusione degli altri verificatori non decida nulla. La ricerca riguardava due
tipi di lavoro: la risposta del modello Qwen a una richiesta dell'utente e il passo di addestramento.

**Stato del documento.** È il risultato di un ragionamento e di un calcolo con formule, non una misurazione.
Non ci sono stati esperimenti con il modello, avvii della rete, sistemi di prova e model checking. I partecipanti e i critici hanno eseguito solo brevi programmi aritmetici e piccole enumerazioni
sul processore; due di queste enumerazioni dei lavori ChatGPT sono state ripetute da due critici, e gli hash di controllo
sono coincisi. I numeri con la nota [calcolo] sono ottenuti con le formule da parametri nominati esplicitamente. I parametri
dei modelli e delle schede video sono stati inseriti dai partecipanti stessi; nessun lavoro li ha confrontati con la configurazione pubblicata
di Qwen3.5-4B o del modello da circa 27 miliardi di parametri. **Le uniche decisioni accettate sono
le decisioni D1–D25** in [ROADMAP](ROADMAP.md), sezione 3. Tutto il resto qui è una
valutazione del consiglio. Dove i critici divergono, è indicato «controverso».

**Come leggere.** La sezione 1 — che cosa si cerca e in quali condizioni. La sezione 2 — che cosa è stato dimostrato impossibile
e quali affermazioni di impossibilità sono state confutate. Le sezioni 3 e 4 — l'analisi dei meccanismi per la risposta
del modello e per il passo di addestramento, con il miglior candidato e i suoi limiti. La sezione 5 — che cosa è rimasto
non dimostrato e quali esperimenti e calcoli lo risolveranno. La sezione 6 — le domande al proprietario. La sezione 7 — chi
ha partecipato.

**Sintesi breve.**

1. **Risposta del modello.** Una verifica indipendente dalla quota di collusione esiste solo dove l'intera
   risposta è verificata dal pagatore stesso, il cui denaro è in gioco. Il miglior candidato è «PPS»: il pagatore in un solo
   passaggio ricalcola la richiesta e la risposta pronta in un profilo intero esatto, il pagamento avviene
   solo dal suo pagamento anticipato, la controversia sulla prova di errore è verificata da ogni nodo. Il costo calcolato è
   1,2–3,8% del tempo di generazione, ma solo con la generazione di una risposta alla volta [calcolo]. Il candidato
   non copre il consumatore senza attrezzatura e dipende da una coincidenza di bit non misurata.
2. **Passo di addestramento.** Non è stata trovata una verifica del passo stesso entro circa il 20%, indipendente dalla quota di collusione.
   Su questo concordano tutti e sei i lavori e tutte e tre le critiche.
3. **L'unico percorso sopravvissuto per l'addestramento** cambia ciò per cui si paga: la rete paga
   per un miglioramento dimostrato del modello in un esame scelto dopo la fissazione dell'aggiornamento. Secondo la decisione D18 questo percorso
   è studiato come candidato di una nuova unità di pagamento, ma per ora non è accettato; servono calcoli, esperimenti e le correzioni
   trovate dai critici.
4. **Decidono l'esperimento D5** (coincidenza dei bit del Qwen3.5-4B intero su due schede video e tra
   due modalità di calcolo, tempo, qualità) **e i calcoli dei mini-agenti** della sezione 5.3; su di essi si prende
   la decisione finale sul pagamento dell'addestramento (D18).

Documenti di partenza: le decisioni D1–D17 e la fase 4 in [ROADMAP](ROADMAP.md); il modello dell'avversario
e la formulazione formale di D1 in [THREAT_MODEL](THREAT_MODEL.md), sezione 1.5; le varianti A e B
in [CURRENT_DESIGN](CURRENT_DESIGN.md); [OPEN_QUESTIONS](OPEN_QUESTIONS.md);
[PILOT_RESULTS](PILOT_RESULTS.md); [requisiti obbligatori](../ru/REQUIREMENTS.md). I partecipanti
hanno anche letto le precedenti ricerche del progetto sull'aritmetica esatta, sumcheck/GKR, Brakedown e il costo
del testimone per LoRA (documenti `LORA_*` e `HONESTY_RESEARCH_GATE` dell'archivio di ricerca; in questo
repository non sono inclusi). I partecipanti non avevano ancora le decisioni D6–D17: sono state accettate lo stesso giorno.
In fase di sintesi queste decisioni sono state applicate alle conclusioni dei lavori; dove una decisione cambia il verdetto, è detto esplicitamente.

---

## 1. Impostazione

### 1.1. Che cosa si cerca

Si cerca una procedura che il nodo esegue da sé sui dati che la coalizione non può falsificare:
l'input del compito, il modello fissato, le regole fissate e, possibilmente, una prova
matematica. La decisione del nodo non deve basarsi sulle firme e sui verdetti di altri nodi. Allora
la quota dei verificatori collusi `q`, compreso `q = 1`, non influisce sulla decisione.

Due tipi di lavoro:

- **(a) risposta del modello** Qwen dell'ordine di 4–27 miliardi di parametri a una richiesta dell'utente;
- **(b) passo di addestramento** (LoRA o completo) su una porzione di dati assegnata.

### 1.2. Condizioni obbligatorie

| Condizione | Che cosa ne segue per la verifica |
|---|---|
| **D1** | Il guadagno atteso da qualsiasi dichiarazione falsa non è maggiore di zero né rispetto all'inazione (`Δ₀ ≤ 0`) né rispetto al lavoro onesto (`Δч ≤ 0`), per qualsiasi coalizione, compreso un novizio con il conto vuoto e un numero qualsiasi di chiavi. Servono **entrambe** le disuguaglianze ([THREAT_MODEL](THREAT_MODEL.md), sezione 1.5). Una perdita positiva limitata come `R·q^k` nella variante B non va bene |
| **D2** | Si paga solo il risultato verificabile. Il tempo di lavoro, la potenza dichiarata e l'attrezzatura accesa non costituiscono un motivo sufficiente. Il modo in cui l'esecutore ha ottenuto il risultato corretto (cache, un'altra macchina) non è importante |
| **D4** | La verifica è automatica, senza votazioni; ogni nodo la esegue da sé secondo un'impronta fissata delle regole |
| **D6** | Il danno rientra in D1: una risposta falsa non deve essere consegnata all'utente come verificata, un passo falso non deve entrare nel modello. Il risultato si usa solo dopo una verifica indipendente dalla quota di collusione, oppure è marcato esplicitamente come non verificato |
| **D7** | È richiesta una verifica indipendente dalla quota di collusione. Non è ammesso indebolire D1 a «finché i collusi sono meno di `q*`» |
| **D8** | Possono contestare solo i verificatori del compito assegnati per sorteggio e l'utente sulla propria richiesta. Senza deposito. Gli altri segnalano un sospetto sulla bacheca senza diritto di fermare il pagamento |
| **D15** | Un semplice ricalcolo che si può copiare non viene pagato |
| **R5** | Nessun deposito, contributo o multa. Si possono perdere solo le ricompense non maturate («somma in sospeso» `H`) |
| **Riferimenti di costo** | Un supplemento per la verifica di circa il 5% del lavoro per le richieste e di circa il 20% per l'addestramento. Sono riferimenti, non confermati dai requisiti |

Decisioni correlate: D9 (il piano di addestramento si ricava con una regola dal catalogo e dai risultati dell'esame,
i crediti sono emessi una volta sola per il contenuto del compito), D10 (lo scambio avviene con una sola voce di registro),
D12 (le finestre si contano nel tempo attivo della rete), D14 (il prezzo della controversia — secondo la rete di secondo
livello più economica), D16 (un guasto hardware onesto non è punito), D17 (i pagamenti per le richieste nella variante B —
solo dai pagamenti degli utenti).

Il campionamento statistico, la fiducia nell'enclave hardware e il piccolo errore crittografico
previsti dai requisiti sono ipotesi: si possono proporre, ma vanno nominate apertamente.

### 1.3. Modelli e parametri usati dai lavori

Nei materiali non c'era un manifesto fissato di Qwen3.5-4B. Ogni lavoro ha preso una propria configurazione densa
convenzionale, quindi «4B» in lavori diversi significa numeri diversi. Se in Qwen3.5 ci sono strati ibridi di attenzione lineare, tutte le quote di attenzione e le conclusioni sulla coincidenza delle modalità di calcolo
cambiano (sezione 5).

| Lavoro | Risposta del modello (a) | Passo di addestramento (b) |
|---|---|---|
| claude1 | «4B»: 36 strati, larghezza 2560, query di attenzione 4096, chiavi/valori 1024, MLP 9728, vocabolario 151 936, input e testa condivisi (4,022 miliardi di parametri). «27B»: 64 strati, 5120, 6144, 1024, 20 480, 151 936, separati (26,386 miliardi). Richieste 500/500 e 2000/1000 token | LoRA di rango 16 sulle matrici degli strati superiori, esame `n = 10⁴–10⁶` posizioni |
| claude2 | La stessa «4B». Richiesta 1000 token, risposta 500; lavoro della richiesta 5,98·10¹² MAC [calcolo] | LoRA di rango 16/64 su tutte e sette le matrici, contesto 4096, porzione di 64 o 7680 sequenze |
| gpt1 | «S»: 36 blocchi, 2560, KV 640, MLP 11 008, 151 936. «Lg»: 48, 5120, 1024, 31 232. Input 128, output 32 token | 8 micropacchetti da 512 token, LoRA di rango 8 su Q, V |
| gpt2 | «Piccolo»: 36, 3072, KV 768, MLP 8192, vocabolario 150 000. «Grande»: 60, 6144, 1024, 18 432. Input 128, output 128 | Lo stesso di gpt1 |
| ds1 | Classe Qwen3-4B: 4·10⁹ parametri, 36 strati, 2560, MLP 9728 | Profilo Qwen2.5-1.5B dalle ricerche precedenti: 28 blocchi, 1536, MLP 8960, LoRA di rango 8 su q/v, 512 token × 8 micropacchetti |
| ds2 | 36 strati, 2560, MLP 8960, 32/8 teste; contesto 2048, risposta 200 | Lo stesso profilo 1.5B |

Attrezzatura (scheda tecnica a memoria, non verificata): classe RTX 2060 — 336 GB/s di memoria, circa 103 TOPS
INT8, 6 GB; classe RTX 4090 — 1008 GB/s, circa 660 TOPS, 24 GB. Le quote di picco 0,8 per la memoria e 0,4
per il calcolo sono scenariali. L'unica misura di velocità è 73,8 token/s di Qwen3-4B Q4_K_M
su RTX 2060 nel pilota ([PILOT_RESULTS](PILOT_RESULTS.md)). È un altro formato di pesi, e non
conferma né confuta i modelli sopra.

La formulazione comune di D1 per una dichiarazione falsa, su cui i lavori si sono trovati d'accordo: con prezzo del compito `R`,
costo di esecuzione del lavoro onesto `c`, costo della contraffazione `c_f` e probabilità della sua accettazione `ε`,
servono `Δ₀ = εR − c_f ≤ 0` e `Δч = εR − c_f − (R − c) ≤ 0` [calcolo].

---

## 2. Limiti inferiori: che cosa è stato dimostrato impossibile

### 2.1. Limiti confermati dai critici

Sono affermazioni su **classi** di verifiche. Nessuna di esse esclude tutte le verifiche concepibili;
nessuno ha dimostrato un limite inferiore comune del costo per tutti gli algoritmi.

1. **Indistinguibilità.** Se il nodo accetta un risultato solo dai messaggi di altri nodi, allora con
   la collusione di tutti i loro autori esiste un risultato falso che accetterà: la coalizione invierà le stesse
   firme e le stesse impronte che nel caso di un risultato onesto. Con `q = 1` il nodo è protetto solo da ciò che
   ha verificato da sé. (claude1, lemma 1; claude2, 3.1; gpt2, 9.4; ds2, 6.1. Tutti i critici concordano.)
2. **Scala «ogni nodo da sé».** Se un cambiamento dello stato comune (emissione di crediti, peso) deve
   essere protetto per ciascuno degli `N` nodi completi, ognuno di essi verifica ciascun risultato di questo tipo,
   e il costo totale non è inferiore a `N·v`, dove `v` è il costo di una verifica. Per rientrare nel 5% o nel 20%, con
   `N = 1000` serve `v/W ≤ 5·10⁻⁵` o `2·10⁻⁴` di lavoro [calcolo]. Da qui tre modi per ottenere
   l'indipendenza dalla collusione: decide l'unico partecipante il cui denaro è in gioco; la verifica è compressa
   (prova breve o piccolo esame); il risultato non cambia affatto lo stato comune.
   (claude1, lemma 2; claude2, 3.4; gpt1, §2; ds2, 6.1. Tutti i critici concordano; il critico ChatGPT
   ha corretto la formula di ds2 in `1 + n·a` invece di `(1 + a)·n`.)
3. **Campionamento di celle senza codifica.** Se il nodo legge in media `s` di `N` celle sostituibili
   in modo indipendente (strati, posizioni, sequenze), esiste una cella che verifica
   con probabilità non superiore a `s/N`; la sua sostituzione passa con probabilità non inferiore a `1 − s/N`.
   (claude2, 3.2; gpt2, 9.2; gpt1, 5.4; claude1, I2. Il critico Claude ha notato una lacuna nel rigore per
   un verificatore le cui monete dipendono dalla radice della traccia; la conclusione non cambia.)
4. **Verifica a campione e margine dell'esecutore.** Per una dichiarazione falsa `σ` con costi `c_σ` e somma
   in sospeso `H`, D1 rispetto all'inazione richiede `π(σ) ≥ (R − c_σ)/(R + H)`, dove `π` è la probabilità
   di scoperta. Per una contraffazione economica e un conto vuoto serve `π ≈ 1`, cioè la verifica completa. Per
   una contraffazione quasi onesta serve una quota di verifica non inferiore a `m/(1 + m)` con margine `m`. Per una chiave
   con `H > 0` e la verifica di un blocco su `L + 1` serve `H ≥ R·((L+1)/m_s − 1)`: 36R per 36 strati
   e 64R per 64 strati con un solo blocco verificabile [calcolo]. La casualità fresca del nodo rende `π`
   indipendente dalla collusione, ma non la rende uguale a uno. (claude1, lemma 3; claude2, 3.11, ottenuto
   in modo indipendente. Tutti i critici concordano. Il critico ChatGPT ha precisato: con la verifica obbligatoria del blocco
   di uscita, la soglia per un tentativo quasi gratuito è 35R.)
5. **Verifiche lineari fisse su un campo.** Per `t < n` verifiche lineari fissate in anticipo
   esiste un nucleo comune non nullo: un errore che vi appartiene non viene visto. Un vettore uniforme fresco,
   scelto dopo la fissazione, lascia passare un errore fisso non nullo con probabilità non superiore a `1/p`. Sugli interi limitati
   il limite non si applica (vedi 2.2, punto 3). (gpt1, 5.2;
   gpt2, 9.1; claude2, 3.5; ds2, 5.2; claude1, B4.)
6. **Errore nullo equivale al determinismo.** Una verifica con zero accettazioni false per qualsiasi moneta
   diventa deterministica fissando le monete. (claude2, 3.6.)
7. **Casualità comune con collusione totale.** Con `q = 1` una casualità comune a tutti i nodi è possibile
   solo dall'esterno della rete (faro esterno o Fiat–Shamir); lo scambio di impegni tra i nodi SkyNet
   non aiuta. Le monete personali di nodi diversi danno decisioni diverse, e non si ottiene un calcolo unico.
   (claude2, 3.8; gpt2, 6.1. Il critico ChatGPT ha aggiunto: il faro deve essere non spostabile, disponibile
   e rivelarsi rigorosamente dopo l'accettazione finale del blocco; questo è già l'attacco 1.5 e N13
   in [THREAT_MODEL](THREAT_MODEL.md).)
8. **Ripetizioni gratuite.** Se un tentativo si può ripetere quasi gratis (per esempio, la casualità
   si ricava dall'hash della dichiarazione stessa), la probabilità di successo cresce con il numero di tentativi. Per la scelta delle celle
   non si può usare Fiat–Shamir. (claude2, 3.3; ds2, 5.1.)
9. **Verificatore che costruisce da sé il risultato.** Se il nodo calcola da sé tutto lo stato
   e legge la dichiarazione solo per confrontarla, allora, togliendo il confronto, si ottiene un esecutore onesto
   con lo stesso lavoro. Quindi una tale verifica costa non meno del 100% del lavoro ottimale. Solo una verifica con un suggerimento può essere economica: una risposta pronta, una traccia o una prova.
   (gpt2, 9.5. I critici Claude e DeepSeek l'hanno definita la migliore formulazione del limite generale.)
10. **Certificato del token vincente.** Per uno stato nascosto di posizione generale non si può certificare
    il vincitore senza ottenere informazioni su ogni riga del vocabolario che può vincere. Nel caso peggiore
    si verifica tutto il vocabolario. (claude1, B6; gpt2, 9.3.)
11. **Input privato.** Un nodo estraneo senza la richiesta non può verificare la risposta, se non c'è
    una prova a conoscenza zero. Il critico ChatGPT ha precisato il limite: un impegno occultante
    insieme a una tale prova potrebbe trasmettere la proprietà necessaria, e il lemma
    non lo esclude. (claude2, 3.7; ds2, 6.2; gpt1, §1.)

### 2.2. Affermazioni di impossibilità che i critici hanno confutato

1. **«La D1 letterale richiede un errore esattamente nullo»** (ds1, F1). È vero solo se il tentativo non
   costa nulla. Se la casualità è esterna e imprevedibile, e ogni tentativo richiede una nuova fissazione
   e costa `c_min > 0`, allora `Δ₀ ≤ εR − c_min ≤ 0` con `ε ≤ c_min/R` (claude1, lemma 4; ds2, 5.1).
   Anche il candidato di ds1 si basa su un hash con errore maggiore di zero. Hanno confutato tutti e tre
   i critici. Riserva del critico ChatGPT: il progetto non ha ancora stabilito il limite inferiore del costo del tentativo più economico per qualsiasi
   coalizione, quindi un piccolo errore è compatibile con D1 solo condizionatamente
   (questione 2 nella sezione 6).
2. **«La verifica di una risposta pronta costa +100% del tempo per definizione»** (ds1, F2). È falso per
   una risposta pronta: verificando tutte le posizioni in un solo passaggio, i pesi si leggono una volta, non per ogni
   token. Per numero di operazioni la verifica è davvero uguale alla generazione, ma per tempo, con la generazione
   di una risposta alla volta, può essere decine di volte più rapida. Inoltre ds1 confrontava
   profili di pesi non comparabili. Hanno confutato tutti e tre i critici.
3. **«La verifica lineare esatta richiede non meno di `N` forme e `N²` operazioni»** (ds1, F3). È falso
   due volte: coefficienti freschi dopo la fissazione danno una probabilità di passaggio di circa `Q^(−s)`, e sugli
   interi limitati basta una forma con impacchettamento a bit `Σ y_i·B^i` con `B > 2U`
   (gpt1, 5.3; gpt2, 6.2); la matrice identità legge le coordinate in `O(N)`. Hanno confutato tutti e tre
   i critici.
4. **«Il traffico minimo della verifica di una risposta è uguale alla dimensione della traccia di calcolo»** (conclusione dal lemma 5.3
   di ds2). La verifica di una risposta pronta ha bisogno solo dei token della risposta, e il verificatore di una prova breve
   legge la prova e le radici, non i dati stessi. Hanno confutato tutti e tre i critici.
5. **«Qualsiasi generazione onesta deve eseguire tante operazioni quante la verifica in un solo
   passaggio»** (claude1, §4.1 e B5). È un limite superiore del costo della verifica, non inferiore (critico
   Claude), e non vale se l'esecutore dispone di una cache legittima del risultato pronto
   (critico ChatGPT).
6. **«Una verifica esatta economica è impossibile senza casualità segreta o crittografia»** (claude2, 3.5).
   Controesempio: l'equazione normale esatta della regressione ridge sui numeri razionali
   si verifica in modo deterministico (critico ChatGPT).

### 2.3. Limiti controversi o condizionali

- **Dimensione dell'esame `n ≳ 2σ²·ln(1/ε)/δ²`** (claude2, 3.10). I critici Claude e DeepSeek la applicano
  come stima di lavoro. Il critico ChatGPT ha mostrato che da una sola varianza non si può ricavare il necessario
  `n` per qualsiasi distribuzione: servono alternative date e un'unità di campionamento indipendente.
  **Controverso**: va bene come stima nel modello indicato, non come teorema.
- **Barriera quantitativa della prova completa** (claude2, 3.9): il budget del 5% lascia circa 1–5,
  il budget del 20% — circa 6–18 operazioni sul campo per una cella non lineare, mentre le costruzioni note
  di arrotondamento costano decine, softmax — centinaia [calcolo con costi ipotizzati]. Tutti
  i critici concordano che questo è il limite delle costruzioni note, non un teorema.

---

## 3. Risposta del modello (a)

### 3.1. Tutti i meccanismi esaminati

Il «costo» è indicato come supplemento rispetto al lavoro dell'esecuzione onesta; tutti i numeri sono [calcolo] sui parametri
dei lavori. Il «verdetto» è il risultato dopo tre critiche e tenendo conto di D6–D17.

| Meccanismo (lavori) | Idea | Garanzia e ipotesi | Dati del nodo | Collusione e controesempio | Costo [calcolo] | Verdetto |
|---|---|---|---|---|---|---|
| **Ripetizione completa da parte di ogni nodo**, passaggio causale sulla risposta pronta (tutti e sei) | Il nodo con l'input calcola da sé tutte le posizioni e verifica ogni token e la prima causa di arresto | Errore nullo con profilo esatto, input autentico e nucleo funzionante | Richiesta, risposta, modello, profilo, seme | La collusione non aiuta: decide il proprio ricalcolo | Circa 100% delle operazioni per ciascuno degli `N` nodi; un nodo estraneo non vede la richiesta privata | **Regge** come riferimento; non rientra nel 5% con la verifica da parte di tutti i nodi |
| **I1 / PPS** (claude1): verifica il pagatore | Il pagatore in un solo passaggio ricalcola la richiesta e la risposta nel profilo intero «INT-canone»; pagamento solo dal suo pagamento anticipato; nessuna emissione e nessun peso per la richiesta pagata | Errore nullo con A1 (stessi bit su hardware diverso **e** con decodifica punto per punto e passaggio dell'intera sequenza sulla stessa scheda), A2 (il registro conserva), A3 (hash, cifratura), A4 (il pagatore pubblica in tempo la prova di errore), A5 (i dati della controversia sono disponibili) | Richiesta, risposta (`T·4` byte), impronte del modello e del profilo, seme; pesi in memoria 4,02 GB per 4B W8, 12,8–25,6 GB per 27B | Decide l'unico partecipante il cui denaro è in gioco; la collusione «pagatore + esecutore» sposta solo i loro stessi crediti | 4B, 500/500, RTX 2060: 3,98·10¹² MAC, 0,19 s contro 7,5 s di generazione — circa 2,5–2,6%; tutti gli scenari 1,2–3,8% con generazione di una risposta alla volta; 8–22% con batch 8; 21–48% con batch 32. Senza GPU circa 8 s per 1000 token sul processore — 100–300% | **Regge con correzioni** (tutti e tre i critici); correzioni in 3.2 |
| **I8 — controversia sulle radici degli strati** (claude1) | L'esecutore fissa le impronte del flusso residuo per strato. Il pagatore trova il primo blocco in cui il ricalcolo diverge e ne pubblica l'input; ogni nodo ricalcola un blocco. Senza prova nella finestra il pagamento va all'esecutore | Nessuna prova falsa di errore con A1; un rifiuto falso del pagatore è impossibile | Input del blocco (10–20 MB con 1000 posizioni), pesi di uno strato (101–388 MB) | La verifica è decisa da ogni nodo stesso. Controesempi: l'esecutore mette nel registro solo l'impronta del testo cifrato e non consegna la risposta stessa; il registro è identico con risposta consegnata e trattenuta; la censura del blocco nella finestra dipende da validatori esterni | Circa 1,0·10¹¹ MAC per nodo per 4B, 3,9·10¹¹ per 27B; con 1000 nodi una falsa controversia — dell'ordine di 10–20 GB di traffico di rete (stima del critico Claude) | **Regge con correzioni**: testo cifrato nel registro, limite delle false controversie, tempestività e censura come ipotesi nominate |
| **M1 — Freivalds del pagatore con vettore segreto** (ds2) | Il pagatore ricalcola le operazioni elemento per elemento e verifica le moltiplicazioni di matrici con prodotti scalari sul proprio vettore segreto fresco | Errore non superiore a `N/p` su tutte le uguaglianze, trascurabile con `p ≈ 2⁶¹`; servono la verifica dell'intervallo e le somme grezze prima dell'arrotondamento | Traccia di calcolo dell'esecutore | Verifica il pagatore stesso. Controesempio alla messa in cache del vettore: conoscendo il vettore di uno strato, l'esecutore controlla l'uscita di quello strato in tutte le richieste future (critico DeepSeek) — il vettore deve essere fresco per ogni richiesta | Dichiarato 2,7%; non riproducibile: softmax 0,79%, non 2,45%, e con un costo della moltiplicazione sul campo di 10–100 MAC le proiezioni danno +1,6–15,8% (critico DeepSeek). Traffico — **controverso**: circa 14 MB per token con int32 grezzi e circa 15 GB di traccia per una richiesta di 1850 token (critico Claude); 7,419 MB per token anche in INT16 e 7,477 GB di prefill (critico ChatGPT); circa 2,4 MB per token se il pagatore ricalcola da sé i punteggi di attenzione (critico DeepSeek) | **Regge come verifica** per un pagatore senza GPU, ma con un canale rapido; il costo dichiarato è confutato |
| **I2 — strati campionati** con casualità fresca del nodo (claude1; ds1, 3.1; gpt2, §8) | Il nodo verifica `m_s` strati casuali su `L` tramite le impronte | Un errore singolo passa con probabilità `1 − m_s/(L+1)` | Input dello strato, pesi dello strato | Contraffazione: risposta con un modello piccolo più una traccia onesta del modello grande; un passaggio è distorto, poi segue una continuazione coerente | Hashing della traccia 0,38–4 GB; 1–8% per l'esecutore a seconda della velocità dell'hash | **Confutato** per il conto vuoto (limite 2.1, punto 4); va bene solo per chiavi con `H ≥ 35–64R` |
| **PVYa** (claude2): l'utente verifica un campione di celle «blocco × token» con la propria casualità segreta | Scelta della cella proporzionale alla sua quota di operazioni | Solo guadagno monetario, non danno | Celle della traccia, percorso nell'albero delle impronte | Controesempio del critico Claude: risposta con un modello piccolo e traccia prefill onesta; la contraffazione economica in tempo viene colta con probabilità di circa 0,3–1%, `Δч ≈ +0,94c`. Critico ChatGPT: nel modello dei costi uguali `Δ₀/c = +0,019`; serve anche il legame delle chiavi e dei valori di attenzione al prefisso | All'utente da <0,001% a 2,7%, variante rigorosa circa 5,6%; all'esecutore l'hashing di circa 4 GB di traccia — 2–4 s di processore, 30–50% del tempo della richiesta su RTX 2060 | **Confutato** (critici Claude e ChatGPT). Il critico DeepSeek lo accettava separando la variante rigorosa da quella relativa, ma la variante relativa non soddisfa la scrittura bidirezionale di D1, e per D6 serve una garanzia anche sul danno, che PVYa non offre |
| **I3 — Freivalds sulla traccia** da parte di un nodo della rete (claude1; ds1, 2.2; gpt1; gpt2, 6.1) | Verifica di ogni moltiplicazione su un vettore casuale tramite la traccia inviata | `≤ 1/p` per errore; servono le uscite grezze prima dell'arrotondamento | Tutta la traccia | La collusione non aiuta, se il vettore è fresco | Traccia 4,4 GB per risposta (4B), 15,2 GB (27B); per il prefill di 4096 posizioni solo gate/up — 5,74 GB in INT16 contro 0,755 GB nella stima di ds1 (critico ChatGPT) | **Confutato come verifica economica**: urta contro il traffico, non contro l'aritmetica |
| **I4 — tabelle di somme parziali** (tutti e sei) | Il nodo costruisce in anticipo tabelle delle uscite dello strato per gruppi di input | Esatto con pesi canonici | Tabelle | — | Gruppo 2: 859 GB per una matrice 4B, circa 476 TB per tutto il corpo; piani di bit — non meno di 128 dimensioni del modello | **Confutato dal calcolo** (tutti i critici) |
| **I5 — certificato del token vincente** (claude1; ds1, 2.5; gpt1, 4.3; gpt2, 5.3) | Albero di cluster di righe della testa con limiti superiori dimostrati | Esatto per la scelta greedy con copertura completa del vocabolario e stato nascosto verificato | Stato nascosto dell'ultimo strato | Uno stato nascosto sostituito certifica un altro token | Risparmia non più della quota della testa: 2,10% / 0,60% (gpt1), 6,04% / 1,76% (gpt2), fino a 9,67% (claude1); nel caso peggiore tutto il vocabolario | **Regge come parte** della verifica (scelta greedy) |
| **Gumbel-max come campionatore canonico** (claude1; claude2, 5.5) | La scelta con temperatura si riduce a `argmax(z/τ + g)` con rumore da PRF sul seme | L'identità è corretta | Seme | La distribuzione differisce dalla solita top-p/top-k — è un cambio di prodotto | Rumore fresco per ogni token: circa `V` valori PRF e massimi di gruppo, 75,97 milioni di valori PRF per 500 token | **Regge** come modo di fissare la scelta; il risparmio del certificato per il campionamento **non è giustificato** (critici DeepSeek e ChatGPT) |
| **Certificato di Gumbel «con margine»** (claude2, 5.5) | Si accetta il token quasi vincente entro una tolleranza | — | — | Controesempio: con logit uguali e differenza di rumore inferiore a `2η` passa un token errato (critico ChatGPT); qualsiasi tolleranza apre la sostituzione (ds2, 6.4) | — | **Confutato** |
| **Certificato intervallare con ricalcolo esatto in caso di ambiguità** (gpt1, 4.4; gpt2, 5.4) | Approssimazione di rango basso della matrice congelata e limite dimostrato del resto; dove l'intervallo ammette arrotondamenti diversi, il nodo ricalcola esattamente | Errore nullo con norme del resto calcolate in modo indipendente e ricalcolo obbligatorio | Propri fattori e norme dei resti | Non si possono prendere chiavi e valori dal messaggio dell'esecutore | Passaggio rapido 0,521% delle operazioni dello strato; per il 5% la quota di uscite ambigue non supera 4,479% nello strato riscaldato e 1,342% con preparazione a freddo (critico ChatGPT). Critico Claude: su pesi vicini al rango pieno gli intervalli quasi certamente coprono molte celle, e il costo è vicino al 100% | **Regge** matematicamente; **costo controverso**, non dimostrato |
| **Impacchettamento esatto a bit** (gpt1, 5.3; gpt2, 6.2) | Una forma lineare `Σ y_i·B^i` sugli interi | Esatto con `B > 2U` e intervalli dimostrati | Somme grezze | Piccola enumerazione: con `B = 8` 9 accettazioni corrette e 0 false, con `B = 4` 20 false su 29 (ripetuta da due critici, hash coincisi) | Quasi senza guadagno: per W8A16 con larghezza 3072 una parola a 64 bit per uscita | **Regge** come primitiva esatta, non dà risparmio |
| **Cache dei prefissi verificati** (gpt2, 5.1) | Il nodo riutilizza lo stato che ha calcolato da sé | Esatto per la stessa posizione e versione | La propria cache | Una radice altrui può collegare uno stato errato | Guadagno solo sulle ripetizioni; la stessa cache è disponibile all'esecutore | **Regge**, in generale non riduce il costo |
| **Prove brevi sumcheck/GKR** per la risposta (claude1, I6; claude2, 4.9 e 5.7) | L'esecutore dimostra l'intero passaggio; ogni nodo verifica la prova | Garanzia computazionale; il limite di errore end-to-end per il grafo Qwen non è ricavato | Prova, pesi per la valutazione in un punto casuale | La collusione non aiuta con lo schema completo e gli input verificati | Riferimento FlashProve 70–95× del proprio profilo (denominatore poco chiaro); stima di claude2 — 6–20 volte più costoso del lavoro con contesto 2048; nella lettura migliore circa 16,8× (critico ChatGPT) | **Regge** come garanzia condizionale; **non rientra** nel 5% |
| **Cambiare il compito: pagare un esito verificabile** (claude1, I7; claude2, 5.4; gpt1, 3.1; gpt2, 4) | Per esempio un vettore che soddisfa una formula SAT, codice che supera i test, una soluzione con risposta verificabile | Esatto per il proprio predicato | Compito e risultato | L'esecutore può inviare un risultato corretto che il modello non ha prodotto; secondo D2 è ammesso | Verifica SAT — non più di `3m` letture | **Regge per una classe ristretta**; la quota di tali richieste è ignota; il dialogo libero non è coperto |
| **P0 / M4 — la richiesta pagata non dà emissione né peso** (claude1, claude2, ds2) | Il denaro passa solo dal pagatore all'esecutore | Il trasferimento dei propri crediti è neutrale all'interno della coalizione | — | Senza questa regola la verifica da parte del pagatore non protegge la rete (limite 2.1, punto 2) | 0 | **Regge**; è coerente con D17 |
| **Verificatore batch di un nodo dedicato, pagamento solo del prefill** (ds1, 3.3–3.4) | Un nodo verifica il pacchetto; si paga il prefill esatto | — | — | La firma del nodo dedicato è identica con verifica reale e simulata; un prefill esatto con una risposta inventata passa | — | **Confutato** (critico ChatGPT) |
| **Prodotto delle probabilità di errore di nodi diversi** (ds1, 3.2) | Ogni nodo verifica con la propria casualità | — | — | Funziona solo con l'accettazione obbligatoria da parte di tutti i nodi onesti; con `q = 1` non ce ne sono | — | **Confutato** |
| **Controversia aperta nella finestra** (tutti e sei) | Chiunque può obiettare prima della scadenza della finestra | Serve un osservatore onesto con dati e tempo | — | Se tutti coloro che hanno visto i dati tacciono, il risultato falso passa con probabilità 1; il pilota lo ha mostrato | Pilota: 93 transazioni e 5,8–6,3 milioni di gas nella controversia Cartesi | **Confutato** come verifica indipendente dalla collusione; D8 inoltre limita la cerchia di chi contesta |
| **Delega da parte di un pagatore debole** (claude1, 4.10) | Il pagatore affida la verifica al proprio dispositivo o a un nodo scelto | La fiducia in quello scelto è un'ipotesi del pagatore | — | Con la scelta casuale ritorna la dipendenza da `q` | — | **Ipotesi**, non soluzione |

### 3.2. Il miglior candidato per la risposta del modello e le correzioni dei critici

**Candidato.** L'intera risposta è verificata dal pagatore stesso. Se dispone di una scheda video su cui
sta il modello, è PPS (claude1). Se non ha scheda video ma ha un canale rapido, è M1 (ds2)
con un vettore segreto fresco per ogni richiesta. In entrambi i casi la richiesta pagata non dà emissione
di crediti né peso (P0; è coerente con D17), e la controversia è decisa da ogni nodo in base alla prova di errore
(I8). Perché la collusione non aiuta: la decisione è presa dall'unico partecipante il cui denaro è in gioco;
egli ha i dati completi — richiesta, risposta e modello; la verifica è completa, non a campione.

**Correzioni senza le quali il candidato non regge.**

1. **Trattenimento della risposta.** Nel registro va messo il testo cifrato della risposta stesso, non solo la sua impronta:
   circa 2–4 KB per risposta (critico Claude). Questo coincide con D10: scambio con una sola voce di registro.
2. **False controversie.** La coalizione «pagatore = esecutore» può creare quante richieste minuscole vuole e per ognuna
   presentare una controversia, che tutti i nodi scaricano e ricalcolano. D8 limita il flusso delle controversie al numero di richieste,
   ma le richieste pagate a se stessi non sono limitate da questo tetto. Nessun lavoro ha dato una soluzione
   (sezione 5, compito M9).
3. **Tempestività e censura.** Il pagatore deve essere in rete e riuscire a pubblicare
   la prova nella finestra, e il registro deve accettarla. La censura del blocco nella finestra dipende dall'onestà
   dei validatori esterni del registro. È un'ipotesi di collusione in un altro insieme, va nominata
   apertamente. Per il telefono del pagatore viene violata più spesso di tutto. La finestra secondo D12 si conta nel tempo attivo
   della rete.
4. **Legame degli estremi.** La controversia sul primo strato richiede il legame alla richiesta privata originale, quella
   sull'ultimo — al testo cifrato pagato (critico ChatGPT).
5. **Arresto.** Va verificata la prima causa di arresto. La condizione «ultimo token EOS o
   limite raggiunto» lascia passare una risposta aggiunta dopo un EOS precoce (critico ChatGPT).
6. **Aritmetica di INT-canone.** Il prodotto delle probabilità di attenzione per i valori nella specifica
   si accumula in int64. Se non lo si esegue sulle unità tensoriali, il costo dello scenario lungo
   2000/1000 cresce dal 3,8% a circa l'8% (stima del critico Claude); via d'uscita — scomporre la probabilità
   a 16 bit in due metà a 8 bit. Il critico ChatGPT ha trovato altre tre lacune: con una sola
   chiave ammessa softmax dà il valore 65 536, che non sta in 16 bit; la somma dei quadrati
   in RMSNorm può superare int64 (tre componenti da `2³¹−1` danno già più di `INT64_MAX`); servono
   larghezze esplicite, posizioni RoPE e ordine di arrotondamento. Il principio stesso regge queste correzioni.
7. **Emissione in streaming.** Secondo D6 l'utente non deve vedere testo non verificato come verificato.
   Con l'emissione in streaming ogni prefisso mostrato deve essere verificato, e la frequenza di tali verifiche
   entra nel costo (gpt2, §1).

**Limiti del candidato.**

- Il costo 1,2–3,8% è valido solo con la generazione di una risposta alla volta. All'esecutore conviene
  unire le richieste in pacchetti, e con un pacchetto di 8–32 il confronto onesto dà 8–48% [calcolo].
- Il consumatore senza attrezzatura non è coperto dal candidato. Per 27B il pagatore ha bisogno di non meno di
  13 GB di memoria video. Il consumatore principale secondo i requisiti è il partecipante senza attrezzatura. Secondo D6 la sua
  risposta può essere consegnata solo con la nota «non verificato»; come pagare in tal caso l'esecutore
  senza violare D1, nessun lavoro lo ha risolto.
- Tutto dipende dall'ipotesi non misurata A1: coincidenza dei bit su schede video diverse **e** tra
  decodifica punto per punto e passaggio dell'intera sequenza su una scheda. Se in Qwen3.5
  ci sono strati ricorrenti di attenzione lineare, la loro forma parallela arrotonda diversamente, e il costo
  della verifica può crescere di circa il doppio (claude1, 3.4, stima con 10 µs per passo ipotizzati).
- La controversia rivela la richiesta: l'input del blocco ricostruisce quasi reversibilmente il testo. Non c'è controversia senza rivelazione.
- L'energia non è misurata: quando il limite è il calcolo la scheda video consuma più che quando il limite è la memoria,
  quindi la quota per energia può essere maggiore della quota per tempo.
- Gli acceleratori (certificato intervallare, certificato del vincitore per la scelta greedy, cache dei propri
  prefissi) sono ammessi solo sopra la verifica completa, non al suo posto.

---

## 4. Passo di addestramento (b)

### 4.1. Tutti i meccanismi esaminati

La differenza principale rispetto alla risposta del modello: il passo di addestramento non ha un pagatore il cui denaro è in gioco. Il pagamento
avviene con emissione di crediti, quindi per il limite 2.1, punto 2, il fondamento deve essere verificato da ogni nodo
completo. Secondo D15, inoltre, un tale semplice ricalcolo non viene pagato.

| Meccanismo (lavori) | Idea | Garanzia e ipotesi | Dati del nodo | Collusione e controesempio | Costo [calcolo] | Verdetto |
|---|---|---|---|---|---|---|
| **T1 — ripetizione completa della transizione** da parte di ogni nodo (tutti e sei) | Il nodo ripete il passo dal genitore accettato e confronta tutto lo stato successivo, compresi i pesi master, i momenti m, v dell'ottimizzatore e il numero del passo | Errore nullo con profilo esatto e dati autentici | Genitore, porzione di dati, regole | Verificare solo i pesi non basta: gli stessi pesi con v azzerato cambiano il passo successivo (critico ChatGPT) | +100% per ogni nodo, in totale `N × 100%`; per esempio, circa 2,62·10¹⁵ MAC per il ricalcolo di una porzione di 64 × 4096 per 4B | **Regge** come riferimento; non rientra nel 20% |
| **T2 — strati, micropacchetti e passi campionati** (claude1; ds1, 3.1) | Il nodo verifica una parte casuale del passo | `1 − m_s/L` di passaggio | Parte della traccia | Contraffazione: consegnare un aggiornamento casuale o copiato; sostituire un gradiente al confine | Con `N = 1000`, 36 strati e un solo strato verificato — circa 28 lavori per passo | **Confutato** (limite 2.1, punto 4) |
| **VYa-S** (claude2): il faro sceglie le celle «blocco × sequenza», ogni nodo verifica la loro prova compressa | Probabilità di passare `(1 − f)^s` con quota di contraffazione `f` | Faro esterno, hash, prova della cella; solo guadagno monetario, non danno | Prove delle celle scelte | Critico Claude: copiare la traccia di una sequenza su tutta la porzione — sono incoerenti solo le celle di legame (circa 10,5% del peso); con `s = 30` `Δ₀ ≈ +0,036R`, con `s = 10` `Δ₀ ≈ +0,33R` e `Δч ≈ +0,26c`. Critico ChatGPT: un gradiente nullo al confine del blocco rende internamente corrette tutte le celle inferiori; nella formula è stata inserita la quota di lavoro risparmiato invece della quota di uguaglianze errate; anche con la loro uguaglianza `Δ₀/c ≈ +0,096`. Critico DeepSeek: è soddisfatta solo `Δч ≤ 0`, mentre D1 richiede anche `Δ₀ ≤ 0` | Prove 0,66%, riconteggio degli input 0,39%, hashing 3,7–10% con `s = 30`; limiti degli strati — 96,64 GB per un compito di 64 sequenze e 11,60 TB per un compito di 7680 | **Confutato nella forma attuale** (tutti e tre i critici). La riparazione proposta — una verifica separata del legame su sequenze casuali; non calcolata |
| **T3 — prova breve del passo** sumcheck/GKR con impegni (claude1, T3; claude2, 4.9; ds1, 2.9; gpt1, 6.3; gpt2, 7.2) | L'esecutore dimostra l'intera transizione, ogni nodo verifica una sola prova | Garanzia computazionale con schema completo con legame dell'input, arrotondamenti, intervalli e ottimizzatore; il limite di errore end-to-end non è ricavato | Prova, radici, un passaggio sui pesi per pacchetto | La collusione non aiuta con un trascritto comune | Riferimento VeriLoRA circa 137× (121,93 s di prova per 0,89 s di addestramento, altro modello 3B); il budget lascia 11,43% — divario di circa 1200×. Per il profilo 1.5B una sola divisione esatta di softmax — 11 973 394 432 celle del campo e 10 998 054 912 verifiche di intervallo, 356,835 GiB prima dell'allineamento; scrittura di 3,067 TB a 100 GB/s — 30,67 s contro 6,6 s di budget con passo di 60 s | **Regge come direzione**; le disposizioni concrete sono confutate, il 20% non è dimostrato. Il critico ChatGPT la considera il ramo di ricerca più forte per il passo invariato |
| **M1 per l'addestramento** (ds2) | Vettore segreto più ricalcolo delle operazioni elemento per elemento | Come in 3.1 | Traccia | Manca il legame della traccia alla porzione assegnata: un calcolo corretto su dati sostituiti passa (critico DeepSeek) | Dichiarato 1,5%; non sono contate le operazioni inverse elemento per elemento (circa ×2–2,5) né il costo della moltiplicazione sul campo. Traffico 16,08 GB per passo in INT16, 64,318 GB in INT64 — non meno di 514,5 s a 1 Gbit/s | **Confutato** per l'addestramento quanto a traffico e legame |
| **Freivalds sulla traccia del passo** (ds1, 2.2; gpt2, 6.1) | Verifica di ogni moltiplicazione del passo | `≤ p^(−t)` | Tutta la traccia | — | 64,3 GB per passo (1.5B); 123,92–410,44 GB per LoRA e 369,72–2073,34 GB per l'addestramento completo per passo (gpt2); non meno di 991 s a 1 Gbit/s | **Confutato** come verifica economica |
| **T5 — il passo come formula di aggiornamento** (tutti e sei) | I nodi verificano i fattori di aggiornamento, non la nuova matrice | Verifica solo l'ultima addizione | Fattori | Controesempio: il gradiente inviato `G = 0` con quello vero non nullo supera la verifica della formula | Circa 10⁻⁶ del lavoro | **Confutato** come verifica del passo; il ricalcolo dell'ottimizzatore e dell'addizione rientra nel nucleo |
| **Solo il delta LoRA** (ds1, 3.5) | Verificare solo l'adattatore | — | — | L'uscita della parte congelata dipende dal nuovo input | — | **Confutato** |
| **T4 — pagamento per il miglioramento** misurato da ogni nodo su un campione fresco (claude1) | L'aggiornamento è fissato prima del round; un faro esterno sceglie `n` posizioni dell'esame; ogni nodo calcola da sé la differenza troncata delle perdite; si paga l'eccedenza rispetto alla soglia di confidenza | Pagamento di un aggiornamento senza miglioramento con probabilità `≤ ε = 2⁻⁴⁰` con faro esterno, campionamento con reimmissione, profilo esatto e fissazione prima del faro; il costo del tentativo deve essere non inferiore a `ε·κ·B/2` | Pool dell'esame, tutti i `K` aggiornamenti del round | Non ci sono verificatori, calcola ogni nodo. Controesempi: (1) il troncamento delle differenze paga un aggiornamento dannoso: +0,01 nat sul 99,5% delle posizioni e −20 sullo 0,5% danno dopo il troncamento +0,005 con un vero −0,09 (critico Claude); +0,1 sul 99% e −100 sull'1% danno +0,089 con un vero −0,901 (critico ChatGPT); (2) il pool pubblico permette di apprendere direttamente su di esso; (3) un duplicato con rumore, con fusione per somma, dà un contributo positivo | Soglia con `B = 2`: 0,0745 nat con `n = 10⁴`, 0,0236 con `n = 10⁵` (Hoeffding). Per rientrare nel 20% servono `D ≥ n(1 + K·a)/0,6` token di addestramento per nodo per round; con `K = N = 10⁴` sono 1,85·10⁸ token, circa 26 h. Cache degli stati — 0,51 GB secondo la stima di claude1 o 524,3 GB in int16, se le posizioni sono prese da prefissi diversi da 1024 token (critico ChatGPT) | **Regge con correzioni** come nuova unità di pagamento; non verifica il passo. È controverso se la rivelazione selettiva dei candidati dopo il faro sia pericolosa: critico Claude — no con `ε = 2⁻⁴⁰`, critico ChatGPT — non considerato |
| **ODU** (claude2): pagamento per il miglioramento dimostrato in un esame scelto dal faro dopo la fissazione | Il candidato dimostra l'esame; ogni nodo verifica la prova invece di ricalcolare | Come T4, ma elimina la crescita del costo con il numero di nodi; l'addestramento può essere condotto in qualsiasi aritmetica | Prova dell'esame | Critico Claude: il candidato calcola gratis l'esame presso di sé e dimostra solo i candidati vincenti, quindi serve `ε ≲ 0,23%`, non 10%. Critico ChatGPT: lo stesso argomento, più la selezione adattiva sull'esame comune e il fatto che il pagamento secondo il limite di confidenza non si somma telescopicamente (0,16 invece di 0,20 nell'esempio). Critico DeepSeek: `ε = 10%` passa formalmente, ma solo al prezzo dell'intero budget del 20% | Prova dell'esame circa 2,4 h per candidato, in sequenza: con 100 candidati un'epoca non è più breve di 10 giorni (critico Claude). Quota dell'esame 0,655% dei token di addestramento, 0,327% se si dimostra anche il genitore — circa 858 token, meno di una sequenza di 4096 (critico ChatGPT) | **Regge con correzioni** come struttura; `ε` — **controverso** (2 critici su 3: serve molto meno del 10%); l'attribuzione non è risolta |
| **Esame ds1** (ds1, 2.8): 20–82 token, «errore nullo» | Si paga il miglioramento in un esame piccolo | «Errore nullo» solo per definizione | — | Rumore della media circa 0,28 nat su 82 token con miglioramento del passo 10⁻⁴–10⁻³ (critico DeepSeek) — si paga il rumore; la fonte della casualità non è nominata; l'esame non vede i momenti dell'ottimizzatore sostituiti | Dichiarato +1–3%; con il contesto completo di ciascuno dei 20 token valutati — 103,4% della stima matriciale del passo (critico ChatGPT) | **Confutato** |
| **Passo di Gauss–Newton smorzato con certificato duale** (gpt1, 6.4) | Nuovo ottimizzatore; l'esecutore fornisce un vettore breve, il nodo dimostra ogni bit del passo arrotondato con `4λδ² > η²‖r‖²` | Errore nullo per il nuovo passo con un modello lineare dato | Forward esatto e due passaggi delle derivate | Un pareggio con il limite di arrotondamento esatto richiede la soluzione esatta (critico ChatGPT) | `3N/(2k+2)`: 8,82% con `k = 16` e `N = 1`, 75% con `k = 1`; con `N = 100` — centinaia di punti percentuali | **Regge** come contratto modificato; il costo cresce con `N`, la qualità è ignota |
| **Segno esatto: regressione ridge, testa lineare** (claude1, T6; claude2, 4.1; gpt1, 3.2; gpt2, 4; ds1, 2.1; ds2, M2) | Il nodo verifica la condizione di ottimo `Xᵀ(Xw − y) + λw = 0` | Esatto con caratteristiche autentiche | Caratteristiche, etichette | Le caratteristiche vanno verificate separatamente; in M2 di ds2 manca il termine `λw`, e un ottimo errato passa (critico ChatGPT) | 44,4% con rango 8 e 12,1% con 32 rispetto alla costruzione della matrice (gpt1); 0,390% in un'altra disposizione (gpt2) | **Regge per un compito ristretto**; non è l'addestramento di Qwen, la quota di tale lavoro è ignota |
| **Più primi passi LoRA diversi** (gpt2, 7.3) | Con l'adattatore nullo le parti comuni si calcolano una volta | Esatto | Cache comune | Non si trasferisce ai passi successivi | 16,70% per sei inizi ammessi contro sei avvii a freddo | **Regge**, applicabilità ristretta |
| **Addestramento di ordine zero** (claude2, 5.8); **campo piccolo sulle unità tensoriali** (claude2, 5.11); **cache del prefisso congelato e LoRA sui blocchi superiori** (claude1; claude2, 5.9) | Riduzioni di costo | — | — | L'ordine zero cambia l'ottimizzatore; il campo piccolo non dà l'errore dichiarato senza limiti di intervallo | Cache del prefisso — circa 20,97 TB per un milione di sequenze lunghe 4096 | Idee; **non dimostrate** |
| **T7 — controversia aperta** (tutti e sei) | — | Serve un osservatore | — | Per l'addestramento non c'è un osservatore interessato | — | **Confutato** |

### 4.2. Il miglior candidato per il passo di addestramento e i suoi limiti

**Non esiste una verifica del passo stesso entro il 20%, indipendente dalla quota di collusione.** È un risultato
negativo generale, confermato da più lati: la scala `N·v`, la traccia da 64 GB a 2 TB per passo,
le prove decine o centinaia di volte più costose del lavoro, il budget delle operazioni elemento per elemento.

Con il **fondamento del pagamento invariato** restano due vie: la ripetizione completa della transizione (riferimento, +100%
per nodo) e, a lungo termine, la prova obbligatoria dell'intero passo (T3). Per T3 servono un grafo concreto, una robustezza della composizione dimostrata e un preventivo completo; ora non c'è.

Con il **cambio del fondamento del pagamento** (decisione del proprietario, sezione 6, questione 1) il miglior candidato è
la combinazione di T4 e ODU con le correzioni dei critici:

1. L'esame è scelto da un faro esterno rigorosamente dopo la fissazione di tutti gli aggiornamenti e l'accettazione finale
   del blocco.
2. La soglia è presa dal limite statistico con `ε` crittograficamente piccolo (come in T4), non dal 10%.
3. L'esame è verificato con una prova (struttura ODU), affinché il costo non cresca con il numero di nodi.
4. Le perdite sono limitate dall'aritmetica stessa (probabilità minima nel profilo) e non vengono troncate,
   altrimenti si pagano aggiornamenti dannosi.
5. L'attribuzione dei duplicati va risolta senza una catena sequenziale di prove. Nessun lavoro lo ha
   risolto.

**Limiti.**

- Non è una verifica del passo. L'esame non vede i momenti dell'ottimizzatore, non certifica l'origine
  dell'aggiornamento e non esclude l'addestramento sull'esame stesso.
- Secondo D6 un passo falso non deve entrare nel modello. Il miglioramento nell'esame non dimostra l'assenza di danno
  sulle richieste rare e di backdoor (Q4 in [OPEN_QUESTIONS](OPEN_QUESTIONS.md)). Il candidato limita
  il vantaggio monetario, ma non il danno.
- È ignoto se il miglioramento onesto di un singolo aggiornamento superi la soglia: il rumore della differenza delle perdite `σ`
  non è misurato. Se non la supera, i partecipanti onesti non ricevono il pagamento e R6 è violato.
- I dispositivi deboli con un miglioramento piccolo non superano la soglia; «tutta la potenza libera impara»
  vale solo come «impara», non come «riceve il pagamento».
- Legame con D9: il piano di addestramento si ricava già dai risultati dell'esame. Questo rende l'esame parte
  del nucleo, ma non risolve la questione se si possa pagare il miglioramento invece del passo.

---

## 5. Che cosa non è dimostrato e con che cosa verificarlo

### 5.1. Che cosa non è dimostrato

1. La coincidenza dei bit del profilo intero su schede video diverse e tra la decodifica punto per punto
   e il passaggio dell'intera sequenza su una scheda (A1, questione Q2). Da questo dipendono PPS, M1,
   il certificato intervallare e qualsiasi ripetizione esatta.
2. Il tempo di verifica di una risposta pronta rispetto alla generazione su schede reali con pacchetti 1, 8, 32;
   l'energia; il comportamento degli strati ibridi di attenzione lineare.
3. La qualità e la velocità del profilo intero di Qwen3.5-4B rispetto a quello normale.
4. Il costo del certificato intervallare e del certificato del vincitore su pesi reali.
5. La disponibilità dei dati della controversia, il limite delle false controversie senza depositi, la tempestività e la censura del registro.
6. Per il pagamento per il miglioramento: l'entità del miglioramento onesto rispetto alla soglia, la regola di attribuzione senza
   vantaggio dei duplicati, il limite delle perdite senza troncamento, il costo della prova dell'esame.
7. Per la prova breve del passo: il preventivo completo di un passo e il limite di errore end-to-end.
8. La configurazione esatta di Qwen3.5-4B e del modello da circa 27B: tutti i numeri dei lavori sono stati inseriti a mano.

### 5.2. Esperimenti minimi

La decisione D5 autorizza il primo esperimento: il Qwen3.5-4B intero su RTX 2060 del Linux domestico
dell'accompagnatore, sul suo computer e, con il consenso, sui dispositivi di altri partecipanti tramite
mini-agenti, dopo la fase 0. Profili, metriche e soglie sono fissati prima della misurazione. La coincidenza dei bit
riguarda solo le configurazioni provate.

| № | Esperimento | Che cosa si misura | Confuta il candidato se |
|---|---|---|---|
| O1 (D5) | Qwen3.5-4B intero su due schede video diverse | Hash dei logit e dei token su un insieme di richieste; il primo token non coincidente, EOS, pareggi, contesto lungo, richieste con logit vicini | Almeno un bit differisce con la stessa specifica |
| O2 (D5) | Passaggio dell'intera sequenza contro decodifica punto per punto su una scheda | Lo stesso confronto dei bit; separatamente per gli strati ibridi, se ci sono | Almeno un bit differisce |
| O3 (D5) | Velocità: verifica di una risposta pronta contro generazione | Tempo con pacchetti 1, 8, 32 e combinazioni input/output 128/32, 128/128, 500/500, 2000/1000; implementazione del prodotto di attenzione a 16 e 8 bit; memoria, traffico | La quota di verifica con pacchetto 1 è maggiore del 5% |
| O4 (D5) | Velocità del profilo intero contro quello normale sulle stesse schede | Token al secondo, memoria | Il rallentamento rende il servizio non conveniente (soglia da fissare prima dell'esperimento) |
| O5 (D5) | Qualità del profilo intero contro quello normale | Lo stesso insieme di compiti | La perdita di qualità è superiore a una soglia fissata in anticipo |
| O6 (fuori da D5, serve un'autorizzazione separata) | Rumore del miglioramento di un singolo adattatore LoRA | Distribuzione della differenza delle perdite base/adattatore di rango 16 dopo un giorno di addestramento, `σ` e `δ/σ` | Il miglioramento onesto è tipicamente inferiore alla soglia con una dimensione ammissibile dell'esame |
| O7 (fuori da D5; l'avvio di sistemi di prova è attualmente vietato da un limite di ricerca) | Costo della prova di un blocco forward su 4096 token | Coefficiente `P` | `P` è maggiore di circa 300 — allora ODU e VYa-S non rientrano (stima di claude2) |
| O8 (fuori da D5) | Rapporto tra il costo della moltiplicazione sul campo e il MAC tensoriale su RTX 2060 e RTX 4090 | Coefficiente `R_f` | Decide tutti i preventivi di Freivalds e GKR |
| O9 (fuori da D5) | Energia della verifica | Joule per verifica e per generazione | La quota per energia è maggiore del riferimento |

### 5.3. Calcoli esatti che si possono affidare ai mini-agenti

Sono calcoli deterministici senza misurazioni. Per ogni compito si fissano la versione della procedura,
i byte di input o il generatore con i limiti dell'enumerazione, gli interi o le frazioni esatti, la serializzazione della risposta
e SHA-256; il risultato è ripetuto su un secondo dispositivo. La coincidenza conferma il conto, ma non
la semantica né la disuguaglianza economica.

| № | Compito | Parametri | Che cosa risolve |
|---|---|---|---|
| M1 | Distinta del grafo secondo il manifesto fissato di Qwen3.5-4B e del modello da circa 27B (`config.json` pubblicato con hash) | Forme e tipi di tutte le operazioni di riempimento del contesto, generazione, verifica della risposta e passo di addestramento; MAC, byte delle somme grezze, durata dei buffer; strati ibridi; LoRA e addestramento completo | Precisa numeratori e denominatori di tutti i preventivi |
| M2 | Tabella della quota di verifica `ρ(B)` secondo il modello «a tetto» | `L, d`, larghezze di attenzione e MLP, vocabolario, `P, T`, pacchetto `B ∈ {1, 8, 32}`, banda di memoria, TOPS, quote di picco | Previsione per l'esperimento O3 |
| M3 | Limiti di overflow di INT-canone | Tutti gli accumulatori secondo la specifica, compreso il prodotto di attenzione fino a `T ≤ 32 768`, la somma dei quadrati di RMSNorm, la dimensione della probabilità in softmax; variante con due metà a 8 bit | Trova un input con overflow o ne dimostra l'assenza |
| M4 | Traffico esatto di M1 | int32 grezzi e traccia della richiesta su una griglia (input, output, modello); con e senza ricalcolo dei punteggi di attenzione da parte del pagatore | Elimina la divergenza dei critici sul traffico di M1 |
| M5 | Ondata di contraffazioni per schemi campionati con `H > 0` | `π = m_s/(L+1)`, `H₀` iniziale, `R`, tetto dei compiti aperti; enumerazione della dimensione e del numero di ondate | `H*` minimo con cui la contraffazione prima dell'uscita non conviene |
| M6 | VYa-S: enumerazione delle strategie di copia e degli input degeneri | Quota `f`, numero di celle `s`, pesi delle celle, numero di verifiche di legame `s'`; prima e dopo la riparazione | La `Δ₀` massima; se la riparazione regge |
| M7 | Economia della prova selettiva e della rivelazione in ODU e T4 | `e/R`, `P`, margine `m`, numero di chiavi e candidati | La `ε` massima ammissibile |
| M8 | Scala di T4 | `D(N)` con `K = N`, `n`, `a`, `ε` | Il limite del numero di candidati per il 20% |
| M9 | Costo della falsa controversia I8 | Traffico e calcoli della rete in funzione di `N`, `P + T`, passo delle impronte `k` | Se serve un limite delle false controversie e quale |
| M10 | Tabelle della soglia `t(n, ε, V̂)` | Hoeffding e Bernstein empirico con termine `B`; griglia `n, ε, B` | L'esame minimo |
| M11 | Troncamento delle perdite | Quota massima pagata di aggiornamenti dannosi con `B, n, ε`; limite delle perdite di INT-canone in funzione della probabilità minima | La scelta di `B` senza pagare il danno |
| M12 | Attribuzione su un modello giocattolo di fusione | Perdite lineari-quadratiche, gradienti noti; regole «separatamente», «lasciarne uno», Shapley; duplicati e duplicati con rumore; frazioni esatte | Se esiste una regola senza vantaggio dei duplicati |
| M13 | Suggerimenti e gadget della prova breve | Numero di valori con arrotondamento, divisione e tabelle per token e strato; celle, accessi alle tabelle e impegni per una operazione di arrotondamento e softmax | La barriera 2.3 e il preventivo di T3 |
| M14 | Piccole enumerazioni per verificare le formule | Impacchettamento a bit con `B = 8` e `B = 4` (ripetizione degli hash); catena di 8 transizioni con scelta 2: 224 coppie, 56 catturate, 168 mancate; campo F₅ ed errore (1, −1): 5 mancati su 25 | Verifica dell'implementazione dei modelli probabilistici |
| M15 | Certificato del vincitore su matrici strutturate sintetiche | Righe raggruppate, distacco dei logit dato, pareggi, scala comune | Risparmio con distribuzioni diverse; su pesi reali — dopo O1 |
| M16 | Certificato intervallare su prefissi fissati | Quota di uscite ambigue `u`, numero di ricalcoli completi, costo della preparazione per numero di richieste | Se l'accelerazione rientra nel 5% (dopo che i pesi sono disponibili) |
| M17 | Passo di Gauss–Newton su un blocco piccolo | Matrice razionale esplicita `J`, identità `⟨Jx, z⟩ = ⟨x, Jᵀz⟩`, lunghezze degli interi, numero di raffinamenti, pareggi | Il costo del nuovo contratto |
| M18 | Calcolo dei pagamenti e ripristino | Enumerazione finita: un solo numero di compito, due genitori, biforcazione, scomparsa dell'input, collusione di tutti gli assegnati, conto vuoto | Non più di un pagamento per risultato; nulla si applica prima dell'accettazione |

---

## 6. Decisioni richieste da questa fase

Il consiglio non prende decisioni. Qui sotto — le domande con la raccomandazione del consiglio. Il proprietario ha incaricato di deciderle
l'accompagnatore; le decisioni D18–D25 sono state accettate il 24 novembre 2026 e registrate in [ROADMAP](ROADMAP.md),
sezione 3. Ogni decisione è indicata dopo la domanda.

1. **Cambiare il fondamento del pagamento dell'addestramento in «pagamento per il miglioramento dimostrato»?** Secondo D2
   si paga un risultato verificabile; il miglioramento in un esame formalmente lo è, ma è un altro
   oggetto rispetto al passo eseguito. Tre lavori (claude1, claude2, ds1) lo considerano il candidato principale,
   tre (gpt1, gpt2, ds2) — un altro contratto, non una verifica del passo. *Raccomandazione del consiglio:* permettere
   di studiare questa via come candidato di una nuova unità di pagamento dell'addestramento, senza chiamarla verifica del passo.
   Decidere definitivamente dopo i calcoli M7, M8, M10–M12 e l'esperimento O6. Condizioni: faro esterno dopo
   la fissazione, `ε` crittograficamente piccolo, perdite senza troncamento, prova dell'esame, regola di
   attribuzione senza vantaggio dei duplicati. Secondo D6 annotare che il miglioramento non dimostra l'assenza di danno.
   **Deciso — D18:** la via è studiata come candidato di una nuova unità di pagamento dell'addestramento, ma non è accettata e non
   è chiamata verifica del passo. La decisione di accettazione — dopo M7, M8, M10–M12 e l'esperimento O6 (è fuori da D5
   e richiede l'autorizzazione del proprietario). Il modello
   è emesso solo secondo la regola D9. La ricerca della verifica del passo stesso (T3) continua.
2. **È ammissibile un piccolo errore crittografico?** I requisiti lo chiamano ipotesi. I lavori
   claude1, claude2, ds2 e i critici Claude e DeepSeek ritengono che un errore `2⁻⁴⁰…2⁻¹²⁸` sia compatibile
   con D1 come aspettativa, se la casualità è esterna e imprevedibile e ogni tentativo costa
   più di `ε·R`. I lavori gpt1, gpt2 e il critico ChatGPT: un solo piccolo errore non basta per D1, serve
   un limite inferiore dimostrato del costo del tentativo più economico. ds1 ritiene che serva esattamente zero.
   *Raccomandazione del consiglio:* accettare il piccolo errore come ipotesi nominata esplicitamente con tre condizioni —
   faro esterno rigorosamente dopo l'accettazione finale del blocco, divieto di Fiat–Shamir per il campionamento,
   limite inferiore registrato del costo del tentativo. Senza questa decisione sono impossibili sia il pagamento per il miglioramento
   sia le prove brevi.
   **Deciso — D19:** il piccolo errore è ammesso come ipotesi esplicita con queste tre condizioni,
   non superiore a `2⁻⁸⁰` per tentativo e con `ε·R` minore del limite inferiore registrato del costo del tentativo. La normale
   verifica a campione con errore `q^k` non è autorizzata da questo.
3. **Quale faro esterno e la fiducia di chi è ammissibile?** Senza una fonte esterna di casualità comune con
   `q = 1` non funziona nessuno schema con campionamento dopo la fissazione (limite 2.1, punto 7). Le fonti non sono ancora
   scelte (attacco 1.5 e N13). *Raccomandazione del consiglio:* scegliere più fonti indipendenti
   e registrare la fiducia in esse come ipotesi.
   **Deciso — D20:** non meno di due fonti pubbliche indipendenti, il valore è preso in un momento fissato in anticipo
   dopo la fissazione finale, senza diritto di omissione. Le fonti concrete
   e il costo di influenzarle — nella fase 2. Prima della scelta non si includono schemi con campionamento.
4. **Accettare che per la risposta del modello una verifica indipendente dalla collusione esista solo presso il pagatore
   che verifica da sé?** *Raccomandazione del consiglio:* sì. Per il consumatore senza attrezzatura la risposta
   è consegnata con la nota «non verificato» (lo consente D6), e la delega della verifica è una sua propria
   ipotesi. Decidere separatamente come pagare l'esecutore per tale risposta senza violare D1: non c'è soluzione.
   **Deciso — D21:** sì. La rete non paga una risposta senza verifica. L'utente senza attrezzatura può
   nominare da sé un verificatore; è una sua propria ipotesi, e la rete non gli promette D1.
   La garanzia D1 per tale utente resta una questione aperta.
5. **Permettere cambiamenti del prodotto in cambio di una verifica esatta economica?** Qui rientrano la scelta canonica
   del token tramite Gumbel-max (cambia la distribuzione rispetto al normale campionamento top-p/top-k),
   il profilo intero esatto (può peggiorare la qualità), i compiti con esito verificabile (formule,
   test) e i nuovi ottimizzatori con certificato esatto (Gauss–Newton, regressione ridge).
   *Raccomandazione del consiglio:* permetterli come tipi separati di compiti del piano con un contratto esplicito, dopo
   gli esperimenti O5 e il calcolo M17.
   **Deciso — D22:** permetterli come tipi separati di compiti del piano con un contratto esplicito, dopo O5 e M17.
   Il campionamento normale resta disponibile con la nota «non verificato».
6. **Come limitare le false controversie del pagatore senza depositi?** D8 limita le controversie al numero di
   richieste, ma la coalizione che paga a se stessa le richieste aggira questo limite. *Raccomandazione
   del consiglio:* calcolare il costo della falsa controversia (M9) prima di decidere; il consiglio non ha trovato una regola che non
   richieda un deposito.
   **Deciso — D23:** prima il calcolo M9. PPS non è incluso finché non si sceglie una regola
   per limitare le false controversie senza deposito.
7. **Conservare nel registro il testo cifrato della risposta?** Senza questo l'esecutore può trattenere la risposta.
   *Raccomandazione del consiglio:* sì, circa 2–4 KB per risposta; è coerente con D10.
   **Deciso — D24:** sì, il testo cifrato è registrato nel registro con una sola voce insieme all'accettazione.
8. **Serve la scrittura bidirezionale di D1 anche per una contraffazione parziale?** Il lavoro claude2 chiedeva
   se sia ammissibile una contraffazione che è peggiore del lavoro onesto ma migliore dell'inazione. La formulazione formale
   di D1 in [THREAT_MODEL](THREAT_MODEL.md), sezione 1.5, richiede già entrambe le disuguaglianze. *Raccomandazione
   del consiglio:* non cambiare; per questo VYa-S e PVYa nella variante relativa sono stati respinti.
   **Deciso — D25:** non cambiare.

---

## 7. Chi ha fatto che cosa

Il consiglio dei modelli ha lavorato sui materiali del progetto, senza accesso alla rete e senza esperimenti.

- **Round 1, sei lavori indipendenti:** due lavori ChatGPT (gpt1, gpt2), due lavori DeepSeek
  (ds1, ds2), due lavori Claude (claude1, claude2). Ognuno ha analizzato le direzioni della fase 4
  della tabella di marcia, proposto meccanismi propri e calcolato il loro costo. Brevi programmi aritmetici
  sono stati eseguiti da claude1, claude2, gpt1 e gpt2; gpt1 e gpt2 hanno allegato piccole enumerazioni
  con hash di controllo.
- **Round 2, tre critiche:** una da ChatGPT, DeepSeek e Claude. Ogni critico ha letto tutti e sei
  i lavori, cercato controesempi e ricalcolato i numeri chiave. I critici ChatGPT e DeepSeek hanno ripetuto le piccole
  enumerazioni di gpt1 e gpt2 sul processore; gli hash sono coincisi.
- **Sintesi:** questo documento è stato compilato da Claude sulla base dei lavori e delle critiche. Dove i critici divergevano, è indicato
  «controverso». In fase di sintesi alle conclusioni sono state applicate le decisioni D6–D17, che i partecipanti non avevano; non sono state aggiunte nuove
  valutazioni e nuovi numeri oltre ai lavori e alle critiche.
