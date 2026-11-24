<!-- translation of docs/THREAT_MODEL.md, source sha256: ad971a2fe29f57d18ba6e2f6d8b4b6eedb8fb813c17a1cd1343ca6b141c990a8 -->

# Modello dell'avversario e tabella degli attacchi

[English](../../docs/THREAT_MODEL.en.md) · [中文](../zh/THREAT_MODEL.md) · [Español](../es/THREAT_MODEL.md) · [Français](../fr/THREAT_MODEL.md) · [Deutsch](../de/THREAT_MODEL.md) · **Italiano** · [Русский](../../docs/THREAT_MODEL.md) · [Português](../pt/THREAT_MODEL.md) · [العربية](../ar/THREAT_MODEL.md)

Stato al 24 novembre 2026.

Questo documento è il risultato del consiglio dei modelli per la fase 1 della tabella di marcia («Formulazione precisa»,
[ROADMAP](ROADMAP.md), sezione 4). Vi sono raccolti il modello dell'avversario, il confronto del numero di attacchi,
lo stato di ciascuno dei 60 attacchi della specifica per le varianti A e B, i nuovi attacchi trovati dal consiglio
e le questioni che può risolvere solo il proprietario del progetto.

**Stato del documento.** È il risultato di un ragionamento e di un calcolo con formule, non una misurazione.
Non ci sono stati esperimenti, avvii della rete né ricalcoli software per esso. I numeri con la nota
[calcolo] sono ottenuti con le formule nei lavori del consiglio e verificati a mano dai critici; non sono
stati ripetuti da un secondo dispositivo. Diventa decisione accettata solo ciò che approverà il proprietario
del progetto. Tutto il resto qui è una valutazione del consiglio e, in caso di disaccordo, è indicato come «controverso».

**Come leggere.** La sezione 1 stabilisce chi attacca e che cosa conta come guadagno. La sezione 2 spiega
la discrepanza tra 59 e 60. La sezione 3 è la tabella principale: su di essa qualsiasi partecipante può indicare
un attacco non chiuso e verificarlo nei documenti di partenza. La sezione 4 è un breve riepilogo, la sezione 5
contiene le domande al proprietario, la sezione 6 indica chi ha partecipato.

Documenti di partenza: le decisioni D1–D5 in [ROADMAP](ROADMAP.md), sezione 3; le varianti A e B in
[CURRENT_DESIGN](CURRENT_DESIGN.md), sezione 3; [OPEN_QUESTIONS](OPEN_QUESTIONS.md);
[PILOT_RESULTS](PILOT_RESULTS.md); la prima esecuzione [FIRST_RUN](FIRST_RUN.md);
i requisiti obbligatori [REQUIREMENTS](REQUIREMENTS.md). La tabella dei 60 attacchi è presa
dalla specifica della rete senza coordinatori del 20 novembre 2026 (di seguito SPEC); i numeri di riga
1.1–7.4 sono i suoi numeri.

---

## 1. Modello dell'avversario

### 1.1. Notazioni e varianti

| Simbolo | Significato |
|---|---|
| `R`, `c` | Prezzo del compito e costo di esecuzione onesta, `c ≤ R` |
| `H` | Somma in sospeso: le ricompense non maturate della chiave negli ultimi tre giorni. Si può addebitare solo quella (non ci sono depositi né multe, requisito R5) |
| `p` | Quota di verifica: in A `p = 4R/(R+H)`, ma non meno dell'1%; in B è costante, per esempio 1% |
| `B` | Addebito in A: `B = 4R/p − R`, non superiore a `H`; con `p > 1%` è `B = H`, altrimenti `B = 399R` |
| `k` | Numero di verificatori del compito, 3 (con i giri di sorteggio in media 3,5–4,5) |
| `q`, `q_eff` | Quota della coalizione in tutto il peso dei verificatori del modello e tra quelli che verificano effettivamente il compito (sezione 1.7) |
| `G` | Prezzo completo della controversia nel registro |

**Variante A** (specifica attuale): verifica a campione con addebito da `H`; una consegna non verificata
e non contestata viene pagata. **Variante B** (proposta): vengono pagati solo i compiti scelti dal sorteggio
e confermati, al prezzo `R/p`; ciò che non è scelto non viene pagato a nessuno; una contraffazione colta
brucia tutta la `H` della chiave. B è descritta per sommi capi e il consiglio ha esaminato «B come descritta»:
nella descrizione non ci sono il percorso del novizio, l'ammissione dei verificatori in base a `H`, la tariffa
dei verificatori e la fonte di `R/p` per le richieste.

### 1.2. Chi attacca

I profili sono unificati in tutti e sei i lavori. Le combinazioni sono obbligatorie: coalizione con chiavi
gratuite, affittuario diventato coalizione, partecipante a lungo onesto in collusione, utente in collusione
con i verificatori, sabotatore con chiavi gratuite.

| Profilo | Di che cosa dispone | Che cosa vuole |
|---|---|---|
| Singolo | Le proprie chiavi, il proprio dispositivo, un programma modificato | Crediti senza lavoro o oltre il lavoro |
| Coalizione con quota `q` | Chiavi sotto gestione comune; trasferimento istantaneo di risultati, passi di calcolo, stati e richieste; cassa comune | Far passare una contraffazione, ricevere il pagamento delle verifiche senza ricalcolo, vincere le votazioni |
| Proprietario di molte chiavi | Quante chiavi si vuole quasi gratis; il peso e la `H` delle nuove chiavi sono nulli | Code, posti da apprendista, distribuzione dei dati, assegnazioni, biglietti B |
| Affittuario di potenza | Ore GPU al prezzo di mercato, lavoro onesto e pagato dalla rete | Una quota di peso, poi collusione, modello raro o regole |
| Sabotatore senza profitto | Pronto a perdere tutte le ricompense non maturate | Il danno in sé: modello, risposte, backdoor, arresto |
| Partecipante con il conto vuoto | `H = 0`, nessun peso | Qualsiasi pagamento senza lavoro |
| A lungo onesto, poi uscita | Grande `H` e peso; sceglie il momento, la dimensione e il numero di ondate | Più di `H` più il pagamento onesto degli ultimi compiti |
| Utente | La propria richiesta, crediti, diritto di controversia, collusione con l'esecutore o con i verificatori | Risposta gratuita, rimborso per una risposta corretta, dati altrui |
| Operatori di relay, punti d'incontro, nodi di registrazione, punti di accesso alla blockchain, custodi dei dati | Vedono indirizzi e orari, ritardano, non trasmettono, mostrano un ambiente falso | Censura, isolamento di un nodo, rivelazione dell'identità, pagamento per le registrazioni |
| Parti esterne | Faro della casualità, produttore del blocco, fornitori di checkpoint, produttore della modalità protetta, distributore del programma | Spostare il campione, inserire una storia o un programma falso |
| Proprietario di dispositivi altrui | Chiavi di lavoro rubate o infettate | Confermare contraffazioni, rischiando la `H` altrui |

### 1.3. Che cosa l'avversario può e che cosa non può

**Può:** creare quante chiavi vuole; eseguire un programma modificato e leggere tutto sul proprio
dispositivo, comprese le richieste private in modalità normale; trasmettere qualsiasi dato all'interno della
coalizione; spegnersi, scegliere il momento della consegna, tacere, dare i dati ad alcuni nodi e non ad altri,
tenere l'unica copia; affittare potenza; votare e comprare voti; offrire apertamente una tangente tramite
smart contract (le conferme stanno nel registro, il pagamento si può eseguire senza fiducia);
come produttore del blocco — non pubblicare il blocco e scegliere uno dei due valori della casualità;
controllare parte dei ripetitori e circondare un nodo; avere un vantaggio esterno o dare valore al danno in sé.

**Non può** (sono ipotesi, vanno dichiarate apertamente): falsificare la firma di una chiave altrui non
rubata, trovare una collisione dell'hash, aprire un commitment in due modi, falsificare il sorteggio
segreto (VRF); riscrivere i blocchi finali di una blockchain pubblica — il registro non ha una chiave
di amministratore ed è corretto (premessa 1 della SPEC; il programma non è scritto); prevedere o spostare
la casualità dopo il fissaggio del pacchetto (premessa 2; le fonti non sono scelte; la miscelazione
protegge dalla previsione, ma non dalla scelta tramite l'ultima fonte, N13); ottenere una coincidenza
bit a bit senza calcolare (premessa 3; non verificato); cambiare l'esito del ricalcolo di un passo nel
registro (premessa 4; per il modello completo non è costruito); cambiare il programma di un nodo altrui
(D4); addebitare crediti disponibili altrui, ottenere un secondo pagamento per lo stesso numero, revocare
un pacchetto consegnato.

**Che cosa la rete non vede per principio:** a chi appartengono le chiavi e se i partecipanti sono
indipendenti; se un nodo ha dato i dati a un altro; che cosa funziona sul computer altrui; in che cosa
il ricalcolo differisce dalla copia dello stato altrui. Se il caso onesto e quello falso danno al nodo
gli stessi dati, nessuna regola li distingue ([OPEN_QUESTIONS](OPEN_QUESTIONS.md)).

### 1.4. Guadagno dell'avversario e danno alla rete

Il guadagno si calcola per tutta la coalizione da uno stesso stato iniziale, con gli stessi diritti,
compiti e orizzonte fino al regolamento finale, inclusa l'uscita. Si sommano i crediti maturati, i rimborsi,
il valore del servizio ricevuto e dei nuovi diritti; si sottraggono i costi reali (lavoro, energia, affitto,
gas, pagamenti esterni). I trasferimenti interni alla coalizione si elidono, un credito non si conta due
volte, la perdita della vittima non è di per sé un reddito della coalizione. Tipi di guadagno: crediti per
una dichiarazione falsa (contraffazione, copia, conferma senza ricalcolo, riga altrui); costi risparmiati
a parità di pagamento; peso e posti nel sorteggio; rimborso per una risposta corretta o parte non pagata
dei dati; guadagno per effetto — influenza sulla risposta o sul modello, lettura della richiesta altrui,
controllo delle regole, dell'emissione, del catalogo, del piano, il danno in sé.

Il danno alla rete si calcola separatamente, nelle proprie unità: è accettato un risultato errato;
il risultato è usato prima della verifica; sono emessi crediti senza lavoro; un onesto ha perso `H`;
sono congelati i pagamenti o l'ingresso dei novizi; sono rivelati dati privati; sono sostituiti la storia,
le regole, il programma o la versione del modello; la rete ha speso lavoro in verifiche e controversie
imposte. Il danno senza guadagno non viola D1, ma può violare altri requisiti; nella tabella è «n/a»
con il nome del requisito.

### 1.5. Formulazione formale di D1

D1 (accettata il 23 novembre 2026): «il truffatore non ottiene ciò che vuole»; il guadagno atteso da una
contraffazione non è maggiore di zero rispetto al lavoro onesto e all'inazione, per qualsiasi coalizione,
incluso un novizio con il conto vuoto e un numero qualsiasi di chiavi; una perdita limitata ma positiva
non soddisfa il criterio.

Sia `U(σ)` l'utilità attesa della coalizione con la strategia `σ`. Per ogni strategia con una dichiarazione
falsa servono **entrambe** le diseguaglianze:

- `Δ₀ = E[U(σ) − U(inazione)] ≤ 0` — ogni dichiarazione falsa è sostituita dal rifiuto del compito
  (la `H₀` già guadagnata in questo caso matura);
- `Δч = E[U(σ) − U(lavoro onesto)] ≤ 0` — ogni dichiarazione falsa è sostituita da un'esecuzione onesta.

Il requisito vale per qualsiasi `q` da 0 a 1, con `H = 0` e qualsiasi numero di chiavi. Per confutarlo
basta uno stato ammissibile e una differenza positiva. Non si può confrontare con la maggiore delle due
basi: con inazione 0, guadagno onesto 0,60 e dichiarazione falsa 0,20, tale confronto dà «nessuna
violazione», sebbene `Δ₀ = +0,20` [calcolo].

Un lavoro ha proposto di dividere D1 in livello economico (solo crediti) e livello per effetto (influenza
sulla risposta e sul modello, lettura della richiesta, danno). Il consiglio non lo decide da sé: la questione
è portata al proprietario (sezione 5, questione 1). Nella tabella il guadagno solo per effetto è
contrassegnato «no (eff.)».

### 1.6. Principio generale della colonna «dati per il rifiuto»

In caso di collusione dell'esecutore con tutti i verificatori assegnati, il nodo vede solo dati concordati:
impronte del risultato e del passo, stati rivelati con prove di inclusione. Tutti sono compatibili
con una contraffazione. Restano verificabili in modo indipendente solo l'ingresso e il modello fissato,
sui quali il nodo può ricalcolare da sé il compito — circa +100% di lavoro [calcolo]; né A né B lo
richiedono, e per una richiesta privata un nodo estraneo non ha nemmeno l'ingresso. Perciò nella tabella
spesso c'è «no, salvo ricalcolo completo».

### 1.7. Quota di collusione `q_eff`

Tutte le soglie del tipo «fino al 91%» si riferiscono alla quota della coalizione tra coloro che verificano
effettivamente il compito. `q_eff` è la quota della coalizione tra i verificatori che (1) sono ammessi
al compito (secondo la regola 2.6 della SPEC, per un compito di un esecutore di lunga data serve
`H_v ≥ B`, fino a `399R`), (2) hanno risposto entro il termine del giro e (3) hanno ricevuto i dati
per la verifica. Esempio [calcolo]: 3000 dispositivi domestici onesti da 8 ore e 100 onesti a ciclo
continuo contro 800 affittati a ciclo continuo. La quota dell'avversario su tutto il peso è 42,1%
(19 200 su 45 600 ore-dispositivo al giorno); un dispositivo domestico accumula circa `144R < 399R`
e non è ammesso ai compiti di esecutori di lunga data; tra gli ammessi `q_eff = 800/900 = 88,9%`,
`q_eff³ ≈ 0,70`. Riserva dei critici: questo riguarda i compiti con `B = 399R`. La condizione (3) può
portare `q_eff` a uno con qualsiasi quota complessiva (N2). La formula `q^k` è valida solo per scelte
indipendenti; nella SPEC i giri proseguono fino a tre risposte e per una collusione parziale serve
la distribuzione di chi ha risposto.

### 1.8. Formule di base [calcolo]

- **A, una contraffazione:** guadagno `R − 4R(1 − q³)`; in perdita con `q < 0,9086`. **Novizio A:**
  `p = 1`, `B = H = 3R`, guadagno `R(4q³ − 3)`.
- **A, uscita con contraffazioni** (enumerazione FIRST_RUN su un solo dispositivo, non confermata):
  conveniente da `q = 0,875` (qualsiasi dimensione, tre ondate, regola «in lavorazione non più di un terzo
  di `H`»; 1,00004·H₀ a 0,875, 1,034·H₀ a 0,880), da 0,890 (compiti uguali), da 0,800 senza la regola
  del terzo; senza collusione, su 92 milioni di strategie non c'è un'uscita conveniente (il migliore
  0,980·H₀). È un'enumerazione di famiglie, non una dimostrazione.
- **B, una contraffazione** è conveniente con `q^k > pH/(R + pH)`; con `p = 1%`, `k = 3`: `q ≈ 0,928`
  per `H = 400R`, `0,659` per `40R`, qualsiasi `q > 0` per `H = 0`. Il pagamento lordo medio per
  contraffazione è `R·q^k` e non dipende da `p`.
- **B, ondata di `N` contraffazioni:** `E = a^N·H₀ + N·a^(N−1)·q^k·R`, `a = 1 − p(1 − q^k)`. La prima
  contraffazione è conveniente con `H₀` inferiore a 2,8R / 14,3R / 52R / 105R / 269R per `q` = 0,3 / 0,5 / 0,7 /
  0,8 / 0,9. Con `H₀ = 0` il guadagno massimo per chiave è circa `q^k·R/(e·p·(1 − q^k))`: 0,037R / 1,0R /
  5,3R / 19R per `q` = 0,1 / 0,3 / 0,5 / 0,7. Una sola ondata senza enumerazione è una stima inferiore.
- **Probabilità di un pagamento indebito** per compito senza controversia esterna: in A `1 − p + p·s`,
  in B `p·s` (`s` è la probabilità di collusione completa al momento della scelta); con `p = 0,01`,
  `s = 0,125` — 0,99125 e 0,00125, mentre il pagamento indebito lordo con `R = 1` è 0,99125 e 0,125.
  Non si possono confrontare le varianti solo in base alla frequenza del pagamento indebito.

---

## 2. Confronto «60 e 59»

Nella SPEC ci sono esattamente 60 righe (12 + 12 + 10 + 5 + 11 + 6 + 4): 18 chiuse, 6 in perdita,
19 limitate, 16 aperte e **una «non attacco» — la riga 1.9** (consegnare un risultato corretto calcolato
su attrezzatura altrui è permesso dalla decisione D2); il riepilogo di CURRENT_DESIGN, sezione 9, e il
paragrafo «In breve» della SPEC hanno sommato solo quattro categorie e perso la quinta, da qui 59. Tutti
e sei i lavori e tutti e tre i critici sono giunti a questo indipendentemente. La scrittura corretta è:
60 = 18 + 6 + 19 + 16 + 1.

---

## 3. Tabella degli attacchi

### 3.1. Notazioni

**Stato:** chiuso — il nodo respinge l'attacco in base ai dati del registro con le premesse indicate;
in perdita — l'attacco è possibile, in media è in perdita fino al limite indicato; limitato — è possibile,
il danno o il guadagno sono limitati da una regola; aperto — non c'è soluzione; non attacco.

**D1:** sì — il guadagno non è maggiore di zero per qualsiasi coalizione; **no** — esiste una strategia
con guadagno positivo almeno rispetto a una base; cond. — soddisfatta solo con le premesse indicate,
che non dipendono dalla quota di collusione (premesse 1–4 della SPEC, non ancora costruite);
no (eff.) — non c'è guadagno monetario o non è stabilito, ma si ottiene un guadagno per effetto
(sezione 1.5); n/a — nell'attacco non c'è una dichiarazione falsa a scopo di guadagno, è interessato
il requisito indicato; ? — la regola non è definita, il segno del guadagno non è stabilito.

**Dati** — in base a quali dati verificabili in modo indipendente il nodo respingerà una dichiarazione
falsa in caso di collusione dell'esecutore con tutti i verificatori. «controverso» — i lavori o i critici
sono in disaccordo e la disputa non è risolta. I riferimenti «N…» portano ai nuovi attacchi nella sezione 3.9.

### 3.2. Esecutore

| № | In breve | A | D1 in A | B | D1 in B | Dati per il rifiuto in caso di collusione | Che cosa serve per chiudere |
|---|---|---|---|---|---|---|---|
| 1.1 | Un novizio con il conto vuoto consegna una contraffazione | in perdita fino a `q ≈ 0,909`: i primi compiti sono verificati sempre, guadagno `R(4q³−3)`. Controverso: il critico ChatGPT considera la riga aperta, perché i `3R` iniziali si possono ottenere copiando (2.2, N1) | **no** con `q ≥ 0,909`, e con qualsiasi `q > 0` — tramite il pagamento delle riverifiche da apprendista | aperto: `R·q^k` per tentativo senza perdite, chiavi quante se ne vuole | **no** con qualsiasi `q > 0` | No, salvo ricalcolo completo sull'ingresso aperto; per una richiesta — solo presso l'utente | Verificare i primi risultati pagabili in un modo che ogni nodo esegue da sé; prima di ciò — solo lavoro non pagato. In B — ammissione in base a `H` (N16) |
| 1.2 | Un partecipante di lunga data contraffà parte dei compiti | in perdita fino a `q ≈ 0,909`; il 99% delle contraffazioni non viene verificato e resta nella rete | **no** con `q` alto | in perdita con `q^k R < p(1−q^k)H`: 0,928 con `H = 400R`, 0,659 con `40R`, qualsiasi `q` con `H = 0` o da una chiave vuota (N16) | **no** | No, salvo ricalcolo completo | Verifica del risultato pagabile indipendente dalla quota di collusione (fase 4). In B — `p` e ammissione in funzione di `H` |
| 1.3 | A lungo onesto, poi un grande inganno e l'uscita | in perdita solo nelle famiglie enumerate sotto 0,875 / 0,890 / 0,800 (sezione 1.8) | **no** con `q ≥ 0,875`; sotto non è dimostrato | aperto: la campagna di uscita non è calcolata; con `H` piccola è conveniente con qualsiasi `q > 0` | **no** | No, salvo ricalcolo | Dimostrazione per tutte le strategie in A; calcolo della campagna di uscita di B, incluso `H₀ = 0` (fase 2) |
| 1.4 | Consegna una contraffazione e sparisce vedendo il campione | chiuso: il pacchetto non si revoca, la sparizione dopo il campione è un risultato errato | cond. | idem | cond. | La riga del pacchetto e l'assenza di rivelazione entro il termine | Un guasto di comunicazione onesto è indistinguibile (costo per gli onesti); per una richiesta privata — disponibilità dell'ingresso |
| 1.5 | Scopre in anticipo o manipola il campione | aperto oggi: chiuso solo con la premessa 2, e le fonti non sono scelte (così hanno valutato i lavori ChatGPT; i critici Claude e ChatGPT sono d'accordo) | cond.; **no** con la scelta tramite l'ultima fonte (N13) | idem | idem | I valori pubblici del faro e del blocco; la collusione sulla soglia del faro o la trattenuta del blocco non sono visibili da essi | Scegliere le fonti; il round del faro rigorosamente dopo l'accettazione finale del blocco; scrivere la fiducia nelle parti esterne come ipotesi |
| 1.6 | Doppio pagamento o compito altrui | limitato: il numero è unico, ma il registro respinge una riga con un compito altrui solo su obiezione; se l'esecutore è spento per tutta la finestra, la riga matura. Confermato da tutti e tre i critici | **no**: pagamento di `R` a una chiave altrui | idem | **no** | L'assegnazione è calcolabile se l'elenco degli ammessi al sorteggio sta nel registro | Il registro verifica da sé l'assegnazione all'accettazione della riga (a basso costo) |
| 1.7 | Si assegna compiti da solo, inventa lavoro | aperto: l'esecutore è scelto dal sorteggio (questa parte è chiusa), ma la regola di approvazione del piano di addestramento non è accettata (ROADMAP, «Che cosa non è risolto», punto 5); la ripetizione del contenuto dà più pagamenti (N22). Critico DeepSeek: «chiuso per un piano fisso, aperto per il piano» | **no** | idem | **no** | Il nodo verifica che il compito sia nel piano; il diritto all'emissione e la non ripetibilità — no | Regola del piano nel nucleo immutabile; emissione solo per un posto consentito del piano; accredito una volta sola in base al contenuto |
| 1.8 | Prende i compiti convenienti, abbandona gli altri | limitato: ciò che è abbandonato va a un altro | sì a costi uguali; controverso se D1 sia violata dal piccolo guadagno della selezione a costi disuguali | limitato; la selezione dopo il sorteggio è impossibile | idem | Assegnazione e termine nel registro | Costo uguale dei compiti; la quota diminuisce dopo quelli abbandonati |
| 1.9 | Il risultato è calcolato su attrezzatura altrui | non attacco (D2) | n/a | non attacco | n/a | — | Distinguere dalla consegna ripetuta dello stesso risultato (N1, N22) |
| 1.10 | Tira per le lunghe la controversia o tace | limitato: il silenzio è una sconfitta; con `H` piccola la differenza di spese della controversia la paga la rete | n/a; controverso con una controversia costosa (N3) | limitato; `H` è spesso vicina a zero | idem | Timer dei passi nel registro | Termini dei passi; preventivo del prezzo della controversia |
| 1.11 | Contraffazioni prima dell'arresto della rete | chiuso: la finestra non scorre mentre la rete è ferma; la soglia non è scelta | cond. | idem | cond. | Tempo della finestra in base ai pacchetti con una quota di peso non inferiore alla soglia | Scegliere la soglia (3.10); conservare le righe durante l'inattività (N7) |
| 1.12 | Nasconde una contraffazione non fornendo i dati | aperto per i dati grandi: il registro non vede «dato o non dato»; per l'addestramento serve lo stato del passo precedente | **no** | aperto; non pagato, ma già usato | **no** | Per i dati piccoli — pubblicazione nella blockchain; per quelli grandi — no | Disponibilità dei dati prima del sorteggio; «niente dati entro il termine — errato» anche per lo stato di addestramento (N2, M3) |

### 3.3. Verificatore

| № | In breve | A | D1 in A | B | D1 in B | Dati per il rifiuto in caso di collusione | Che cosa serve per chiudere |
|---|---|---|---|---|---|---|---|
| 2.1 | Conferma senza ricalcolare | Controverso. chiuso per un verificatore fuori dalla coalizione (quattro lavori, i critici Claude e DeepSeek); aperto secondo la valutazione dei lavori ChatGPT e del critico ChatGPT: dentro la coalizione gli stessi dati sono compatibili con l'assenza di ricalcolo | sì per uno non collegato; dentro la coalizione — 2.2 | idem | idem | Il proprio stato in un punto casuale e la prova di inclusione; l'origine del calcolo non è verificabile | Non pubblicare gli stati intermedi per la disponibilità (N11) |
| 2.2 | Pagamento della verifica del proprio gruppo senza ricalcolo | limitato: circa 0,3% del reddito con il 10% del peso [calcolo: 0,01·3·0,1] | **no** con qualsiasi `q > 0`: risparmio del ricalcolo (cinque lavori, tutti e tre i critici) | limitato, se la verifica in B è pagata come in A (la tariffa non è definita) | **no** a parità di pagamento | No: ricalcolo e copia danno gli stessi dati | Non pagare la ripetizione; la riparazione «pagare dalla ricompensa del compito verificato» non azzera il guadagno (sezione 4.5) |
| 2.3 | Collusione dell'esecutore con tutti i verificatori | in perdita fino a `q_eff ≈ 0,909` (uscita — 0,875) | **no** | in perdita secondo la formula della sezione 1.8 | **no** | No, salvo ricalcolo completo; richiesta privata — solo presso l'utente | Verifica indipendente dalla quota di collusione (fase 4), oppure un indebolimento esplicito di D1 (questione 2) |
| 2.4 | Corruzione o pressione dopo il campione | aperto: il verificatore di una richiesta si rivela all'esecutore; tangente tramite contratto (N4); con M1 il corrotto non rischia. L'abbassamento è confermato da tutti e tre i critici | **no** | idem; con `H = 0` la corruzione costa meno | **no** | No | Richiesta ai verificatori senza contatto con l'esecutore; conseguenze della mancata rivelazione (M1) |
| 2.5 | Un gruppo risponde per primo e occupa i posti | chiuso: si contano tutte le risposte entro il termine; il termine non è scelto | cond. | idem | cond. | L'orario delle risposte nel registro | Il termine del giro non è più breve del ciclo giornaliero; tenere conto della crescita di `q_eff` |
| 2.6 | Un account con peso senza `H` conferma le contraffazioni | chiuso: ammissione solo con `H_v ≥ B`; effetto collaterale — la crescita di `q_eff` (N5) | sì | aperto: in B non c'è una regola di ammissione | **no**: la coalizione riceve `R/p` senza rischio | La `H` del verificatore nel registro (in A) | Una propria misura di responsabilità del verificatore in B |
| 2.7 | Accusa falsamente un esecutore onesto | chiuso con la premessa 4 (non costruita) | cond. | idem | cond. | Ricalcolo del passo nel registro | Macchina di riferimento del modello completo; rimborso per timeout — 2.8, 4.2 |
| 2.8 | Accusa un esecutore spento | limitato: per una richiesta privata non c'è un difensore, si brucia la `H` dell'onesto | **no** per l'insieme «utente + verificatori» (rimborso per una risposta corretta ricevuta); n/a per il puro danneggiamento | idem | idem | Per l'addestramento può difendere chiunque tramite l'ingresso aperto; per una richiesta privata non ci sono dati | Copia della richiesta accessibile al difensore senza rivelarla |
| 2.9 | Flusso di controversie false | limitato dal costo della `H` dell'attaccante | n/a (verifica economica) | limitato; in B `H` è spesso 0 | n/a | Esito della controversia nel registro | Risolvere la contraddizione N23 |
| 2.10 | Intercettazione della scoperta altrui | aperto: l'ordine non è elaborato | **no**: una quota dell'addebito va all'intercettatore | aperto; il premio in B non è definito | ? | Obiezione nascosta `hash(scoperta ‖ chiave)` con marca del blocco | Consegna nascosta con rivelazione e legame alla chiave (a basso costo); certifica la priorità della fissazione, non il momento dell'apertura |
| 2.11 | Denuncia la propria contraffazione per una quota dell'addebito | chiuso per il compito scelto; un'autodenuncia separata è in perdita | sì | il premio in B non è definito | ? | Il registro non paga chi trova prima della fine della verifica assegnata | Regola del premio per B |
| 2.12 | Rifiuta le verifiche | limitato: il sorteggio passa al giro successivo | n/a; controverso: con `G > B` a chi non è d'accordo conviene tacere (N3), dipende dal preventivo di `G` | idem | idem | — | Preventivo di `G`; conseguenze della mancata presentazione senza depositi |

### 3.4. Insieme degli account, peso e votazioni

| № | In breve | A | D1 in A | B | D1 in B | Dati per il rifiuto in caso di collusione | Che cosa serve per chiudere |
|---|---|---|---|---|---|---|---|
| 3.1 | Migliaia di account | chiuso per il peso e i voti; limitato nel complesso: i pagamenti da apprendista, la distribuzione e le assegnazioni crescono con il numero di chiavi (i critici Claude e DeepSeek). Critico ChatGPT: il numero di tentativi pagabili dipende dai posti assegnati, non dalle registrazioni | **no** | aperto: ogni chiave con un'assegnazione è un biglietto con speranza `R·q^k` | **no** | Non ci sono dati che colleghino le chiavi | Ingresso senza pagamenti fino alla verifica indipendente; in B — ammissione in base a `H` (N16) |
| 3.2 | Gonfiamento del peso con contraffazioni o richieste a se stessi | in perdita fino alla soglia; le contraffazioni non verificate che hanno superato la finestra ricevono peso | **no** al limite | aperto: con `H = 0` una contraffazione scelta dà peso quasi gratis | **no** | No, salvo ricalcolo | Peso solo per ciò che è verificato in modo indipendente; conciliare «ha superato la finestra» (SPEC) e «ha superato la verifica» (CURRENT_DESIGN) |
| 3.3 | Affitta potenza e accumula peso onestamente | aperto in una rete piccola: per ¾ del peso — un mese e mezzo con il triplo del lavoro degli altri, per il 91% — dieci volte tanto [calcolo SPEC] | n/a (l'affitto è permesso da D2); porta a 2.3 e 3.7 | idem | n/a | No: il lavoro è onesto | Verifica indipendente dalla quota di peso; nucleo immutabile (D4) |
| 3.4 | Compiti grandi che solo lui stesso verificherà | chiuso dalla regola della dimensione piccola uguale; la cattura dei compiti piccoli di un modello raro — riga 3.5 | sì | idem | sì | La dimensione del compito è una regola del nucleo | — |
| 3.5 | Cattura delle verifiche di un modello raro | aperto: `q_eff ≈ 1` è raggiungibile | **no** | idem | **no** | No | Non pagare un modello senza una soglia di verificatori indipendenti su attrezzatura diversa |
| 3.6 | Account vuoti nei posti da apprendista | aperto: coda di novizi onesti; pagamento dell'apprendista per una copia (2.2) | **no** tramite la copia; n/a per la coda | aperto; il budget dei posti lo prende chi ha più chiavi | **no** | No | Non pagare la riverifica da apprendista; termine di liberazione del posto (N28) |
| 3.7 | ¾ del peso cambiano le regole a proprio favore | Controverso. Critici Claude e DeepSeek: aperto — D4 protegge il nucleo della verifica, ma non l'emissione, il tasso, la commissione, il freno e il catalogo. Critico ChatGPT: limitato — D4 ha priorità sulla vecchia SPEC, il profitto richiede un cambiamento concreto | **no** (cattura dell'emissione), controverso | idem | idem | Impronta del nucleo: il nodo rifiuta una versione che cambia il nucleo | Elencare la composizione del nucleo (questione 5) |
| 3.8 | Blocca le decisioni (½ — modello, ¼ — regole) | limitato: reversibile, ma l'errore non si corregge | n/a (resilienza) | idem | n/a | — | — |
| 3.9 | Compra i voti | limitato: serve ¾ di tutto il peso; la tangente la esegue il contratto | come 3.7: **no**, se la maggioranza cambia l'emissione; controverso | idem | idem | No | Come 3.7 |
| 3.10 | Smette di consegnare pacchetti per congelare la finestra | aperto: soglia alta — congelamento dei pagamenti; bassa — la coalizione tiene la finestra con i propri pacchetti, le contraffazioni maturano (N14) | **no** (ramo della soglia bassa) | idem; la contraffazione scelta riceve `R/p` | **no** | Tempo e quote di peso dei pacchetti | Soglia con dimostrazione di entrambi i limiti; distinguere il peso attivo della rete e la composizione dei verificatori |

### 3.5. Utente

| № | In breve | A | D1 in A | B | D1 in B | Dati per il rifiuto in caso di collusione | Che cosa serve per chiudere |
|---|---|---|---|---|---|---|---|
| 4.1 | Non paga la risposta, spende i crediti due volte | limitato da una parte della risposta; la doppia spesa è chiusa | **no**: la parte non pagata è una perdita positiva (questione 3) | idem | **no** | Fissaggio dei crediti; il registro non vede il trasferimento di una parte | Uno scambio onesto senza una parte fidata nel caso generale è impossibile: ridurre la parte oppure riconoscere l'ipotesi |
| 4.2 | Contesta una risposta corretta per ottenere un rimborso | aperto per due vie: la controversia si chiude con la coincidenza dei verificatori estratti (N17); rimborso per timeout con l'esecutore spento. La valutazione «chiuso» in tre lavori è stata giudicata eccessiva da tutti e tre i critici | **no** | idem | **no** | Ricalcolo nel registro — solo se la controversia è arrivata fin lì | Diritto di portare la controversia fino al ricalcolo; regola del timeout; difensore con i dati |
| 4.3 | Utente ed esecutore emettono crediti con le richieste | chiuso: le richieste non emettono crediti | sì | chiuso, se `R/p` è pagato solo con i pagamenti degli utenti; la fonte non è scritta | cond. | Regola dell'emissione | Scrivere la fonte di `R/p` in B (questione 12) |
| 4.4 | Inonda la rete di richieste | limitato dal portafoglio | n/a | idem | n/a | — | — |
| 4.5 | Copia il modello e serve fuori dalla rete | aperto nel conteggio della SPEC (è tra i 16) | n/a: rischio per la domanda | idem | n/a | — | — |

### 3.6. Registro, programma e comunicazione

| № | In breve | A | D1 in A | B | D1 in B | Dati per il rifiuto in caso di collusione | Che cosa serve per chiudere |
|---|---|---|---|---|---|---|---|
| 5.1 | Riscrive la storia o i conti | chiuso con la premessa 1 | cond. | idem | cond. | Blocchi finali tramite punti indipendenti | Verifica formale del programma del registro |
| 5.2 | Il nodo di registrazione non fa passare o altera le registrazioni | limitato per la censura (una propria registrazione costa monete della blockchain, non è accessibile a un conto vuoto); aperto per una riga con prezzo o destinatario errato senza obiezione (i critici DeepSeek e ChatGPT) | **no** | idem | **no** | Prezzo e destinatario sono verificabili, ma ora solo su obiezione | Verifica della riga all'accettazione; rimborso delle registrazioni senza emissione (N12) |
| 5.3 | Programma falso a un novizio | aperto: indirizzo e riferimento da un'unica fonte | n/a (autenticità) | idem | n/a | No prima della prima installazione | Fonti indipendenti dell'indirizzo e dell'impronta; build riproducibile |
| 5.4 | Aggiornamento dannoso | limitato: D4 permette di rifiutare un'impronta altrui del nucleo; non c'è una build riproducibile del programma del nodo, quindi il «chiuso» della SPEC non regge; per il resto del programma — aperto | n/a | idem | n/a | Impronta nel registro senza un legame verificabile con il sorgente | Build riproducibile; la coincidenza con il testo approvato non ne dimostra la sicurezza |
| 5.5 | Pagamento di un archivio inesistente o erogazione a se stessi | chiuso: per l'archiviazione non si emette nulla | sì | idem | sì | Regola dell'emissione | — |
| 5.6 | Prende il pagamento, non consegna i dati | limitato a una parte | **no**: perdita di una parte dal lato del destinatario senza ricevuta (questione 3) | idem | **no** | Impronta della parte; la ricevuta conferma il pagamento, non la consegna | Come 4.1 |
| 5.7 | Blocca tutti i percorsi d'incontro | aperto con il blocco di tutti i percorsi | n/a (distribuzione) | idem | n/a | — | — |
| 5.8 | Circonda un nodo con uno stato falso | limitato dalla fiducia in due fornitori su tre; con la loro collusione — aperto (N29) | cond. | idem | cond. | Blocco finale tramite punti indipendenti | Client leggero con verifica del consenso |
| 5.9 | Divide la rete per due pagamenti | chiuso: un solo registro | sì | idem | sì | Il numero del compito in un solo registro | Scissione delle regole — N15 |
| 5.10 | Ruba una chiave di lavoro | limitato: la chiave non spende i crediti del portafoglio | Controverso: n/a (danno alla vittima) oppure **no** — le chiavi rubate confermano contraffazioni a spese della `H` altrui (N9, sostenuto dal critico Claude) | idem | idem | La firma non mostra l'operatore | Revoca della chiave; conservazione hardware |
| 5.11 | Esaurisce la distribuzione gratuita | aperto: non è verificato se basterà ai novizi | n/a (rifiuto del servizio); controverso se il beneficio è definito «a chi arriva per primo» | idem | idem | Un nuovo proprietario è indistinguibile da una nuova chiave del precedente | Distribuzione solo per compiti già assegnati |

### 3.7. Modello e addestramento

| № | In breve | A | D1 in A | B | D1 in B | Dati per il rifiuto in caso di collusione | Che cosa serve per chiudere |
|---|---|---|---|---|---|---|---|
| 6.1 | Il sabotatore consegna contributi errati | limitato: circa `x/3` contributi con una quota di lavoro `x` [calcolo SPEC]; con collusione completa non è dimostrato; il contributo agisce subito (N21) | n/a per i crediti; no (eff.) | aperto: una contraffazione non scelta è gratuita, il limite `x/3` non vale (i critici Claude e ChatGPT) | **no** | No, salvo ricalcolo | Promuovere solo contributi verificati (costo — ritardo e memoria) |
| 6.2 | Comportamento nascosto | aperto: l'esame coglie il peggioramento, non la backdoor | no (eff.) | idem | no (eff.) | No; la backdoor è possibile anche con un passo corretto | Compito di ricerca |
| 6.3 | Dataset dannoso o licenza altrui | aperto: un calcolo corretto su dati dannosi non si corregge | n/a; no (eff.) | idem | idem | No: l'hash e l'etichetta sono uguali presso il titolare dei diritti e presso un estraneo | Limitare il catalogo a fonti verificabili |
| 6.4 | Adattamento all'esame | limitato: i compiti si scelgono dopo la fissazione | no (eff.) entro limiti non misurabili | idem | idem | Il momento della scelta dei compiti | — |
| 6.5 | Contraffazione dei risultati dell'esame | in perdita fino alla soglia 2.3; l'esame è verificato sempre, senza lotteria | **no** con `q` alto | come in A; la formula `R·q^k` non è applicabile all'esame (sezione 4.5) | **no** | L'esame è piccolo e aperto: ogni nodo può ricalcolarlo da sé | Ricalcolo dell'esame da parte di ogni nodo (raccomandato dal critico DeepSeek; critico ChatGPT: costo e obbligatorietà non stabiliti) |
| 6.6 | Cattura della votazione sul piano | limitato: proprietà dello schema | n/a; **no** in combinazione con 1.7 | idem | idem | No | Vedi 1.7 |

### 3.8. Riservatezza

| № | In breve | A | D1 in A | B | D1 in B | Dati per il rifiuto in caso di collusione | Che cosa serve per chiudere |
|---|---|---|---|---|---|---|---|
| 7.1 | Il proprietario del dispositivo legge le richieste | aperto in modalità normale | n/a; no (eff.) — la privacy è violata | idem | idem | No | Modalità protetta al costo della fiducia nel produttore (N25) |
| 7.2 | Raccolta massiva di richieste altrui | limitato dalla quota di assegnazioni e posti di verifica | n/a; no (eff.) | idem | idem | — | — |
| 7.3 | Collegamento delle richieste dell'utente | aperto: pseudonimo e indirizzi presso il ripetitore | n/a | idem | n/a | — | Pagamento non collegabile |
| 7.4 | Lettura della richiesta tramite verifica o controversia | aperto: circa l'1% delle richieste è visto da altri tre dispositivi; una controversia falsa pubblica un frammento | n/a; no (eff.) | idem; la quota `p` non limita la rivelazione — la controversia la apre l'utente | idem | — | Controversia senza rivelazione (prova a divulgazione zero del passo) |

### 3.9. Nuovi attacchi trovati dal consiglio

I duplicati dei diversi lavori sono unificati. «Lavori» — quanti dei sei lavori del round 1 hanno individuato
l'attacco; «Critici» — la conclusione del round 2. I numeri N1… sono propri di questo documento e non
coincidono con i numeri locali dei lavori. Non ci sono nuovi attacchi confutati; dove la motivazione
è confutata, è detto.

| № | Attacco | Lavori | Critici | A · D1 | B · D1 | Che cosa serve per chiudere |
|---|---|---|---|---|---|---|
| N1 | **Un solo calcolo — molti pagamenti.** Una chiave della coalizione ricalcola una volta un compito altrui (anche onesto) e distribuisce il passo a tutte le proprie chiavi estratte come verificatori o apprendisti per quel compito. Generalizza 2.2: non serve la collusione con l'esecutore | 1 | Confermato da tutti e tre; il vantaggio cresce con il numero di posti pagabili assegnati, non di chiavi | aperto · **no** | aperto · **no** | Non ci sono dati. Nessun pagamento deve dipendere dalla ripetizione di un lavoro già fatto |
| N2 | **Affamamento dei verificatori onesti sui dati.** Il verificatore prende la richiesta dall'esecutore e si rivela; l'esecutore della coalizione dà la richiesta solo ai propri; l'onesto che «non l'ha ricevuta» non risponde e non perde nulla; i giri proseguono finché non si raccolgono tre risposte della coalizione | 1 (in parte altri 3) | Vero con una riserva: servono circa `3/(λ·q)` giri giornalieri — circa 15 giorni con `q = 5%`, `λ ≈ 4`, circa 75 giorni con `q = 1%` [calcolo], l'attacco è visibile dal registro. Il meccanismo «pubblicazione di una copia cifrata» è nominato nella SPEC, ma non è definito. Per l'addestramento — solo con un'unica copia dell'ingresso | aperto · **no** per le richieste | aperto · **no** | Il registro non vede il trasferimento. Disponibilità degli ingressi prima del sorteggio; per una richiesta privata non c'è soluzione; vedi M3 |
| N3 | **La controversia costa più della posta.** Il gioco della controversia nel pilota — 93 transazioni, 5,8–6,3 milioni di gas: circa 18 $ con 1 gwei e 3000 $ per ETH, circa 360 $ con 20 gwei [calcolo; i prezzi sono ipotesi]. La ripetizione della riga — 14,1 milioni di gas, un altro prototipo, non si possono sommare | 1 (in parte altri 3) | Vero come dilemma, i numeri sono condizionali: o la parte lesa sostiene `G − B`, e l'onesto non d'accordo tace; oppure la rete rimborsa `G` (così si legge 1.10 della SPEC), e il sabotatore costringe la rete a pagare `G` per ogni contraffazione colta | aperto · **no** | aperto · **no** | Il preventivo di `G` per la catena scelta; i compiti in cui un errore richiede una controversia — solo con `H ≥ G` |
| N4 | **Tangente «P+ε»:** il contratto paga al verificatore ε per la conferma e promette di rimborsare `H_v` in caso di cattura. Sottotipo di 2.4 | 1 | Critico DeepSeek: sostanziale; critico ChatGPT: eseguibilità ed equilibrio non dimostrati | aperto · **no** | aperto · **no** | Verifica in cui l'accordo non decide nulla; vedi M1 |
| N5 | **Crescita di `q_eff` tramite l'ammissione `H_v ≥ B`:** 42,1% del peso complessivo danno l'88,9% tra gli ammessi (sezione 1.7) | 2 | Confermato; solo per compiti con `B = 399R` | limitato · **no** in caso di cattura | aperto (2.6) | Calcolare i limiti su `q_eff`; calcolare il compromesso tra dimensione dell'addebito e ampiezza del giro |
| N6 | **Il peso scompare dopo 30 giorni di calendario di arresto:** la finestra è ferma, il peso si conta «su 30 giorni»; il primo gruppo che ritorna riceve tutto il peso | 1 | Vero alla lettera della SPEC, ma condizionale: non è detto se tempo di calendario o attivo; con peso nullo di tutti il sorteggio non è definito | aperto · **no** | aperto · **no** | Calcolare il peso sul tempo attivo della rete (a basso costo) e definire l'accredito iniziale |
| N7 | **Le righe dei pacchetti vivono circa 18 giorni, la finestra può restare ferma più a lungo:** dopo l'inattività resta una radice senza righe, non c'è nulla con cui contestare | 3 | Confermato da tutti | aperto · ? | aperto · ? | Conservare le righe e le motivazioni delle transizioni per tutto il periodo di verifica e controversia; senza dati la scrittura contestata attende |
| N8 | **Un proprio modello nel catalogo dà `q = 1`:** un modello che solo l'attrezzatura della coalizione esegue | 1 | Critico ChatGPT: è la combinazione di 1.7, 3.5 e 6.6; non è dimostrato che una piccola quota di peso porti un modello nel catalogo | aperto · **no** | aperto · **no** | Non pagare un modello senza un giro minimo di verificatori su attrezzatura diversa |
| N9 | **Dispositivi altrui come peso gratuito dei verificatori:** le chiavi di lavoro rubate confermano contraffazioni, si brucia la `H` delle vittime. Estensione di 5.10 | 1 | Confermato; la crescita di `q` dipende dal peso delle chiavi catturate, non dal numero di dispositivi | aperto · **no** | aperto · **no** | Conservazione hardware della chiave; conteggio delle compromissioni nel `q` ammissibile |
| N10 | **La consegna istantanea di contraffazioni aumenta il flusso di assegnazioni** (B) | 1 | Condizionale: la crescita di 10–100 volte non segue dalle regole della SPEC | limitato · sì | aperto · **no** | Ritmo delle assegnazioni solo in base al lavoro verificato |
| N11 | **Disponibilità contro 2.1:** pubblicare gli stati intermedi per N2 permette di confermare senza ricalcolo | 1 | È un limite del cambiamento proposto, non un attacco autonomo | — | — | Pubblicare solo gli ingressi, quelli intermedi — nella controversia |
| N12 | **Pagamento per la registrazione nel registro oltre i costi:** rimborso di registrazioni spazzatura o cartello dei nodi di registrazione | 2 | La regola di rimborso nella SPEC non è definita; il normale reddito dell'intermediario non viola D1 | aperto · cond. | aperto · cond. | Rimborsare solo registrazioni con risultati accettati e non oltre la commissione effettiva |
| N13 | **Scelta tramite l'ultima fonte di casualità:** se il round del faro è noto prima del blocco decisivo, il suo produttore sceglie tra due valori; in A `p → p²`, guadagno circa +0,96R per contraffazione [calcolo]. Critico Claude: con un calendario dei produttori noto in anticipo, la coalizione consegna pacchetti in funzione dei propri blocchi | 4 | Confermato da tutti; i numeri valgono solo con un ordine errato delle fonti | aperto · **no** con ordine errato | idem | Round del faro rigorosamente dopo l'accettazione finale del blocco |
| N14 | **La finestra scorre senza maggioranza:** una coalizione del 40%, spegnendo metà degli onesti, ottiene 40/70 = 57% tra gli attivi [calcolo]. Sottotipo di 3.10 | 2 | Confermato come sottotipo di 3.10 | in perdita · **no** per le perdite di tipo B | aperto · **no** | Vedi 3.10 |
| N15 | **Scissione delle regole:** le somme non maturate maturano in due rami | 1 | Condizionale: il raddoppio di un solo obbligo non è dimostrato | aperto · ? | aperto · ? | Contratto separato con separazione dei saldi |
| N16 | **In B il deterrente è legato alla chiave, ma l'accesso ai compiti no:** le contraffazioni da una chiave vuota separata danno `R·q^k` senza perdite. Radice comune di 1.1-B, 1.2-B, 1.3-B, 3.1-B | 2 + critico Claude | Due lavori hanno motivato il buco col fatto che un normale partecipante di B ha `H = 0` nel 23,5–54,7% delle finestre; questo argomento è confutato (sezione 4.5). La forma corretta l'ha data il critico Claude | — | aperto · **no** | Ammissione ai biglietti con `H` non inferiore al pagamento atteso per la contraffazione; allora B perde la quota di verifica bassa costante (questione 8) |
| N17 | **La controversia dell'utente la decide il campione, non l'aritmetica:** la controversia è chiusa se i verificatori estratti coincidono con l'esecutore | 1 | Confermato dai critici Claude e DeepSeek; critico ChatGPT: vero, ma 4.2 riguarda la pretesa opposta | aperto · **no** | aperto · **no** | Diritto di portare la controversia fino al ricalcolo nel registro |
| N18 | **Contraffazioni → peso → `q`.** Estensione di 3.2 | 1 | Confermato; la conclusione monetaria richiede di considerare i pagamenti futuri | limitato · **no** al limite | aperto · **no** | Peso solo per ciò che è verificato in modo indipendente |
| N19 | **Spazzatura da chiavi gratuite prima dell'assegnazione** sovraccarica nodi e code | 4 | Confermato; un posto a un novizio onesto non è garantito in nessuna variante. La valutazione «la spazzatura costa alla rete 3–4,5 di lavoro con costi quasi nulli in A» è stata confutata dal critico Claude | aperto · n/a | aperto · **no** in combinazione con biglietti gratuiti | Rifiutare i messaggi senza assegnazione prima dell'elaborazione costosa; il percorso da un conto a zero è obbligatorio |
| N20 | **Divergenza imposta delle aritmetiche** dell'esecutore e dell'arbitro | 2 | Confermato; la divergenza in sé non dimostra un guadagno | aperto · ? | aperto · ? | Semantica unica ed eseguibile delle operazioni e verifica delle implementazioni rispetto al riferimento |
| N21 | **Uso del risultato prima della verifica:** la risposta è stata letta, il passo è preso come passo successivo e resta nella genealogia del modello | 5 (+1 in 6.1) | Confermato da tutti; il danno è possibile anche con `q = 0`; `1 − p` è la quota dei non scelti, non dei non applicati | aperto · no (eff.) | aperto · no (eff.) | Verificare il blocco prima della consegna; promuovere solo il discendente verificato (costo — ritardo e memoria) |
| N22 | **Un solo diritto di emissione con numeri diversi** (esecuzioni di prova identiche, ripetizione di un passo dopo il riavvio) | 3 | Confermato; due ordini legittimi possono avere lo stesso output | aperto · **no** | aperto · **no** | Accredito una volta sola in base al diritto canonico sul posto del piano |
| N23 | **Contraddizione delle regole di controversia da un conto a zero** (ROADMAP lo richiede, SPEC no) | 1 | Confermato dai critici DeepSeek e ChatGPT | aperto · n/a | aperto · n/a | Decisione del proprietario (questione 4) |
| N24 | **Appropriazione del compito di un esecutore spento** — sviluppo di 1.6 | 2 | Confermato | vedi 1.6 | vedi 1.6 | Verifica dell'assegnazione all'accettazione della riga |
| N25 | **Collusione con il produttore della modalità protetta** | 1 | Vero nei limiti di 7.1 | aperto · n/a | aperto · n/a | Scrivere l'ipotesi di fiducia nel produttore |
| N26 | **Ricevute false sulla trasmissione dei dati** | 1 | Non c'è reddito esterno: la coalizione paga se stessa | aperto · n/a | aperto · n/a | Non c'è un segno della consegna di dati grandi |
| N27 | **Mancata consegna selettiva da parte del ripetitore** | 1 | Confermato per la disponibilità | limitato · n/a | limitato · n/a | Più ripetitori, percorsi alternativi |
| N28 | **«Apprendista eterno»** occupa un posto e non completa la riverifica (in relazione a 3.6) | 1 | Confermato | aperto · n/a | aperto · n/a | Termine e liberazione automatica del posto |
| N29 | **Collusione di due fornitori di checkpoint su tre** (in relazione a 5.8) | 1 | Confermato; «più fornitori» non risolve la collusione della maggioranza richiesta | limitato · cond. | limitato · cond. | Client leggero con verifica del consenso |
| N30 | **All'utente è consegnato un blocco diverso da quello fissato** | 1 | Confermato | aperto · ? | aperto · ? | Legare il blocco consegnato a un commitment e verificarlo prima dell'uso |
| N31 | **Un errore comune nel nucleo stesso** accetta una transizione errata in tutti i nodi | 1 | Confermato; diverso da N20 | aperto · ? | aperto · ? | Specifica indipendente della transizione; secondo D4 la correzione è solo il passaggio a una nuova rete |
| N32 | **Riconoscimento di una breve richiesta privata tramite l'impronta pubblica** | 2 | Confermato condizionatamente: hash deterministico e piccolo insieme di testi | aperto · no (eff.) | idem | Commitment occultanti con casualità fresca |

**Trovati solo dai critici** (non verificati da altri partecipanti):

| № | Attacco | Chi | A · D1 | B · D1 | Che cosa serve per chiudere |
|---|---|---|---|---|---|
| M1 | **Rifiuto gratuito della rivelazione.** I verificatori della coalizione consegnano un «confermo» nascosto e lo rivelano solo se tutte le risposte consegnate sono sue; altrimenti tacciono e non perdono nulla. La corruzione di un verificatore estraneo diventa senza rischio: invece del rischio di `399R` — zero [calcolo]. Condizione: se le risposte nascoste siano visibili prima della rivelazione — non è definito nella SPEC | critico Claude | aperto · **no** | aperto · **no** | Conseguenze della mancata rivelazione senza depositi (perdita del pagamento e del peso per il giro) oppure occultamento del numero e dell'autore delle risposte; il costo per gli onesti spenti non è calcolato |
| M3 | **Carico tramite il meccanismo di disponibilità.** Se a «non l'ha ricevuta» si risponde con la pubblicazione obbligatoria di una copia, il verificatore della coalizione dichiara sempre «non l'ha ricevuta»; con `q = 10%`, `λ ≈ 4` questo è circa il 34% dei compiti scelti [calcolo] | critico Claude | aperto · n/a | idem | La dichiarazione di mancata consegna deve costare al dichiarante non meno della pubblicazione provocata (dalla sua `H`) |
| M4 | **Guasto e inganno sotto una stessa regola di addebito:** la causa non si verifica con un output errato identico | critico ChatGPT | ? | ? | Non è presentata una regola equa verso entrambe le parti (questione 11) |

(M2 del critico Claude è N16.)

---

## 4. Conclusione

### 4.1. Quanti attacchi violano D1

Conteggio sulla tabella delle sezioni 3.2–3.8 [calcolo sulla tabella]. Le righe contrassegnate «controverso»
sono incluse e nominate separatamente.

| | Variante A | Variante B |
|---|---|---|
| Guadagno monetario («**no**»), su 60 righe | 24 (e altri 2 condizionati: 1.5 con un ordine errato delle fonti, 6.6 in combinazione con 1.7): 1.1, 1.2, 1.3, 1.6, 1.7, 1.12, 2.2, 2.3, 2.4, 2.8, 2.10, 3.1, 3.2, 3.5, 3.6, 3.7*, 3.9*, 3.10, 4.1, 4.2, 5.2, 5.6, 5.10*, 6.5 | 25: gli stessi senza 2.10 (in B «?»), più 2.6 e 6.1 (e gli stessi 2 condizionati) |
| Solo guadagno per effetto («no (eff.)») | 7: 6.1, 6.2, 6.3, 6.4, 7.1, 7.2, 7.4 | 6: gli stessi senza 6.1 |
| Nuovi attacchi con «**no**» monetario (N1–N32, M1) | 14 | 16 |

Le righe controverse sono contrassegnate con un asterisco (3.7, 3.9, 5.10). Senza di esse in A restano 21,
in B — 22. Il numero di righe non si può sommare come numero di modi indipendenti di ingannare: uno schema
è spesso descritto da più righe. La conclusione principale non dipende dal conteggio: **D1 nella forma
letterale non è soddisfatta né dalla variante A né dalla variante B**, e su questo concordano tutti e sei
i lavori e tutti e tre i critici.

**Confronto tra A e B.** B nella forma descritta è peggiore di A con `H` vuote e basse per
`0 < q < 0,909`: una chiave vuota riceve `R·q^k` per un tentativo senza perdite (N16). Con `q = 0`
B è migliore: una contraffazione non scelta non porta nulla, nemmeno con l'uscita. Con `q ≥ 0,909`
perdono entrambe. Se si trasferisce in B il percorso del novizio di A (verifica completa dei primi
compiti), la differenza sulle chiavi vuote scompare (`q^k R − (1 − q^k)·3R`, come in A [calcolo]),
ma B perde la quota di verifica bassa costante. Questo è un input per la decisione D3 nella fase 2,
non la decisione stessa.

### 4.2. Critici per l'avvio della rete con crediti reali

Riepilogo delle valutazioni dei lavori e dei critici. Un avvio chiuso con crediti di addestramento
non blocca questi punti, tranne la privacy, il ripristino (N6, N7) e i punti senza i quali il pilota
non verifica ciò che deve verificare (N2, N3).

1. **Collusione su `q_eff`:** 1.1, 1.2, 1.3, 2.3, 3.2, 3.5, 6.5 e N5. In entrambe le varianti
   l'accettazione si basa sull'accordo del campione di partecipanti.
2. **Pagamento della ripetizione:** 2.2, 3.6, N1. Viola D1 con qualsiasi `q > 0`; non si è trovata
   una riparazione economica.
3. **Chiavi vuote in B:** N16, 1.1-B, 3.1-B.
4. **Diritto all'emissione e destinatario:** 1.7, 1.6, 5.2, N22, e anche 3.7 per l'emissione fuori dal nucleo.
5. **Disponibilità dei dati:** 1.12, N2, N7.
6. **Controversie:** 4.2 e N17; il prezzo della controversia N3, la connessa 2.12; la contraddizione N23; M1.
7. **Uso prima della verifica:** N21, 6.1, N30 (se il proprietario includerà l'effetto in D1).
8. **Ripristino:** N6 (peso dopo l'arresto) e N7 (righe dei pacchetti).
9. **Ingresso e programma:** 5.3, 5.4, N19.
10. **Privacy:** 7.1, 7.4, N32 — violano una condizione obbligatoria indipendentemente dal denaro.

### 4.3. Radice comune

In entrambe le varianti la normale accettazione del risultato si basa sull'accordo di un campione
casuale di partecipanti, cioè su firme che in caso di collusione non dimostrano nulla. Perciò il limite
della difesa si esprime sempre tramite la quota di collusione `q_eff`, e `q_eff` si può alzare con
l'affitto di potenza, la cattura di un modello raro, la regola di ammissione in base a `H` (N5),
l'affamamento sui dati (N2), chiavi rubate (N9) o un lungo arresto (N6). I dati verificabili in modo
indipendente in caso di collusione completa sono solo l'ingresso e il modello, sui quali il nodo può
ricalcolare da sé il compito; né A né B lo richiedono, e per una richiesta privata il nodo non ha
nemmeno l'ingresso. D1 è raggiungibile solo con una verifica che non dipende dalla quota di collusione
(fase 4 [ROADMAP](ROADMAP.md)), oppure con un indebolimento esplicito di D1 a «con `q < q*`» per
decisione del proprietario.

### 4.4. Riparazioni economiche confermate dai critici

| Riparazione | Chiude | Riserva |
|---|---|---|
| Il registro verifica da sé assegnazione, prezzo e destinatario della riga all'accettazione, non su obiezione | 1.6, 5.2, N24 | L'elenco degli ammessi al sorteggio deve stare nel registro |
| Accredito una volta sola in base al diritto canonico sul posto del piano e all'impronta del contenuto | N22, parte di 1.7 | Due ordini legittimi possono dare lo stesso output; il buco principale di 1.7 — la regola del piano — resta |
| Consegna nascosta di un'obiezione con rivelazione e legame alla chiave | 2.10 | Certifica la priorità della fissazione, non il momento dell'apertura |
| Calcolare peso e finestra sul tempo attivo della rete, non sul calendario | N6 | Serve una regola di accredito iniziale dopo l'arresto |
| Round del faro rigorosamente dopo l'accettazione finale del blocco | 1.5 (parte), N13 | Le fonti non sono ancora scelte |
| Ogni nodo ricalcola da sé l'esame prima di accettare la versione | 6.5 | Raccomandato da un critico; costo e obbligatorietà non sono ancora stabiliti |
| Correggere il riepilogo di CURRENT_DESIGN: 60 = 18 + 6 + 19 + 16 + 1 | Confronto 59/60 | — |

### 4.5. Conclusioni confutate

Queste affermazioni dei lavori del round 1 sono state giudicate errate dai critici; non sono state
riportate nella tabella.

| Affermazione | Dove | Perché è errata |
|---|---|---|
| Soglia di convenienza della contraffazione in B `q^k > H/(H+R)` | un lavoro DeepSeek | Manca il fattore `p`. È corretto `q^k > pH/(R+pH)`. Con `p = 1%`, `H = 400R`, `q = 0,95`: guadagno `0,857R`, perdita attesa `0,01·0,143·400R = 0,572R`, risultato +0,285R per contraffazione, mentre secondo la formula errata — una perdita [calcolo]. L'errore gonfia la difesa quasi fino al massimo (0,999 invece di 0,93) |
| La soglia del 90,9% del novizio A «è valida nell'ipotesi che i 3R siano accumulati con la collusione» | lo stesso lavoro | La soglia non dipende da come sono stati ottenuti i `3R` |
| La contraffazione dell'esame in B dà `R·q^k` | entrambi i lavori DeepSeek | L'esame è verificato sempre, senza lotteria; la formula della lotteria non è applicabile |
| La riparazione 2.2 «pagare i verificatori dalla ricompensa del compito verificato» azzera il guadagno | un lavoro Claude | Chi copia risparmia comunque il ricalcolo; anche rispetto all'inazione il guadagno è positivo; la riparazione non tocca la copia su un compito onesto altrui (N1). Rimuove solo l'emissione di crediti per una verifica vuota |
| «Un normale partecipante di B ha `H = 0` nel 23,5–54,7% delle finestre, e in quel momento la contraffazione non comporta alcun rischio» | entrambi i lavori Claude | I numeri `0,99^60 ≈ 54,7%`, `0,99^144 ≈ 23,5%`, `0,99^432 ≈ 1,3%` sono corretti, ma è la quota di finestre a posteriori. La `H` brucia al momento della cattura, comprese le vincite arrivate dopo la presentazione. La conclusione sul buco è vera per un'altra ragione — tramite la chiave vuota (N16) |
| D1 si verifica confrontando con la maggiore delle due basi | un lavoro Claude | Trascura il caso con guadagno positivo rispetto all'inazione (esempio nella sezione 1.5) |
| «La spazzatura costa alla rete 3–4,5 di lavoro con costi quasi nulli dell'attaccante» (variante A) | un lavoro Claude | In A una chiave riceve compiti solo con `H ≥ 3R`, e ogni risultato spazzatura brucia questi `3R`; non c'è amplificazione multipla. L'amplificazione c'è solo in B senza ammissione in base a `H` |
| Stati corretti nella tabella: 2.6-B «chiuso» (lavori DeepSeek e Claude); 1.7 «chiuso / sì», 1.6 e 4.2 «chiusi / sì», 4.1 e 5.6 «D1 sì», 2.2 «non viola D1» (lavori DeepSeek, in parte Claude); 3.4 «no», 2.7 «aperto / no», 5.11 «no» (lavori ChatGPT) | diversi | Le motivazioni sono nelle righe corrispondenti della tabella: in B non c'è una regola di ammissione; la regola del piano è aperta; la verifica dell'assegnazione e la controversia dell'utente danno un guadagno; D1 vieta una perdita limitata; il guadagno in 3.4 e 2.7 è preso dalle righe vicine; nella SPEC non c'è un beneficio personale |
| 1.3: guadagno 1,034·H₀ nel punto 0,875 | un lavoro Claude | 1,034·H₀ si riferisce al punto 0,880; a 0,875 — 1,00004·H₀ |

Restano controverse (non confutate) le valutazioni 2.1 «aperto» in entrambi i lavori ChatGPT e 3.7
«limitato»: i critici sono in disaccordo (righe 2.1 e 3.7 della tabella).

---

## 5. Domande al proprietario

Decisioni senza le quali la fase 1 non si può chiudere. Il consiglio non le prende. Tutte e dodici le domande sono state decise il 24 novembre 2026 su incarico del proprietario (decisioni D6–D17 in [ROADMAP](ROADMAP.md), sezione 3).

1. **L'effetto rientra in D1?** *(Deciso — D6: sì.)* Un lavoro ha proposto di distinguere D1 economico (solo crediti)
   e D1 per effetto (influenza sulla risposta e sul modello, lettura della richiesta, il danno in sé).
   Le parole «il truffatore non ottiene ciò che vuole» nel senso letterale includono l'effetto; allora
   l'uso del risultato prima della verifica (N21) viola D1 in entrambe le varianti con qualsiasi `q`,
   e lo si può chiudere solo con una verifica prima della consegna e della promozione (costo — ritardo
   e memoria).
2. **Richiedere una verifica indipendente dalla quota di collusione, oppure indebolire D1 a «con `q < q*`»?** *(Deciso — D7: è richiesta una verifica indipendente dalla quota di collusione.)*
   Senza una delle due, D1 è irraggiungibile né in A né in B.
3. **Perdita di una parte nello scambio** *(Deciso — D10: violazione di D1; scambio solo di una riga del registro.)* (4.1, 5.6): uno scambio onesto senza una parte fidata nel caso
   generale è impossibile. Riconoscerla come ipotesi esplicita o considerarla una violazione di D1?
4. **Controversia da un conto a zero** *(Deciso — D8: solo i verificatori assegnati e l'utente su propria richiesta.)* (N23): la ROADMAP la richiede, la SPEC no. Con che cosa allora
   limitare il flusso di controversie false senza depositi?
5. **Composizione del nucleo immutabile** *(Deciso — D11: la verifica, il pagamento di ciò che è verificato, l'emissione, la controversia e le regole del registro; il resto nei limiti.)* (3.7): vi rientrano la regola di emissione, il tasso, la commissione
   di rete, il freno e il catalogo, o solo la verifica?
6. **Regola di approvazione del piano di addestramento** *(Deciso — D9: il piano si ricava con una regola dal catalogo e dall'esame.)* (1.7, ROADMAP «Che cosa non è risolto», punto 5):
   chi e come autorizza un compito a emettere crediti.
7. **Tempo per il peso e la finestra** *(Deciso — D12: tempo attivo della rete.)* (N6): tempo di calendario o tempo attivo della rete.
8. **Ammissione ai compiti in B** *(Deciso — D13: sì, il percorso del novizio della variante A.)* (N16): introdurre in B la dipendenza dell'accesso da `H`, sapendo che
   allora B perde la quota di verifica bassa costante. È un input per D3.
9. **Prezzo della controversia** *(Deciso — D14: la rete di secondo livello più economica; la differenza la paga la commissione di rete.)* (N3): quale catena considerare per il preventivo di `G` e chi sostiene
   la differenza `G − B` — la parte lesa o la rete.
10. **Pagare o no la verifica ripetuta e le riverifiche da apprendista** *(Deciso — D15: un semplice ricalcolo che si può copiare non viene pagato.)* (2.2, N1), se una copia non
    si può distinguere dal ricalcolo?
11. **Guasto hardware onesto:** *(Deciso — D16: no; il compito non viene pagato, la somma in sospeso non viene bruciata.)* addebitarlo allo stesso modo dell'inganno?
12. **Fonte del pagamento `R/p` in B per le richieste** *(Deciso — D17: solo dai pagamenti degli utenti.)* (4.3): solo dai pagamenti degli utenti o con emissione.

---

## 6. Chi ha fatto che cosa

Il consiglio dei modelli ha lavorato sui materiali del progetto, senza accesso alla rete e senza esperimenti.

- **Round 1, sei lavori indipendenti:** due lavori ChatGPT, due lavori DeepSeek, due lavori Claude.
  Ognuno ha composto il modello dell'avversario, il confronto delle 60 righe, gli stati per le varianti
  A e B, i dati per il rifiuto e i nuovi attacchi.
- **Round 2, tre critiche:** una da ChatGPT, DeepSeek e Claude. Ogni critico ha letto tutti e sei
  i lavori, confrontato le affermazioni con i documenti di partenza, ricalcolato le formule a mano
  e indicato divergenze ed errori.
- **Sintesi:** questo documento è stato composto da Claude sulla base dei lavori e delle critiche.
  Dove i critici erano in disaccordo, nella tabella c'è «controverso»; nella sintesi non sono state
  aggiunte valutazioni nuove proprie.
