<!-- translation of docs/STRATEGY_SEARCH.md, source sha256: 9c3fdac8710ac98433828b793ab6aad7fd31da5661c1fecb590bb7c63a2cdd26 -->

# Verifica «non a forza bruta»: che cosa dà la matematica invece del ricalcolo completo

[English](../../docs/STRATEGY_SEARCH.en.md) · [中文](../zh/STRATEGY_SEARCH.md) · [Español](../es/STRATEGY_SEARCH.md) · [Français](../fr/STRATEGY_SEARCH.md) · [Deutsch](../de/STRATEGY_SEARCH.md) · **Italiano** · [Русский](../../docs/STRATEGY_SEARCH.md) · [Português](../pt/STRATEGY_SEARCH.md) · [العربية](../ar/STRATEGY_SEARCH.md)

Stato al 25 novembre 2026.

Questo documento è il risultato del quinto consiglio dei modelli. Il proprietario del progetto ha chiesto testualmente:

> «Forse avrebbe senso scegliere un'altra strategia? Per esempio, collegare un po' di
> matematica? Per non verificare tutto di seguito, ma prevedere il tentativo di inganno e verificare solo
> in quel caso? Oppure fare un'analisi intelligente del funzionamento della rete skynet e trovare un comportamento sospetto?
> Pensate in questa direzione, che cosa c'è ancora nella scienza che possa aiutare a non risolvere a forza bruta».

Il consiglio ha esaminato la teoria dei giochi di ispezione, la verifica basata sul rischio, la ricerca di anomalie, le trappole, la verifica a campione, i meccanismi senza verifica, la crittografia e l'economia senza depositi, e poi ha proposto una strategia e revisioni delle decisioni.

**Stato del documento.** È il risultato di un ragionamento e di un calcolo con formule, non una misurazione. Non ci sono stati esperimenti, avvii della rete e installazioni. I partecipanti e i critici hanno eseguito solo brevi programmi aritmetici e piccole enumerazioni sul processore. I numeri misurati sono presi solo dai [risultati dell'esperienza D5](EXPERIMENT_D5.md) (sintesi D5_RESULTS al 25 novembre 2026) e sono contrassegnati con [misurato]; i numeri ottenuti con le formule da parametri nominati esplicitamente sono contrassegnati con [calcolo]. I lavori degli scienziati sono citati **a memoria**: non c'era rete, i testi delle fonti primarie non sono stati verificati. **Le uniche decisioni accettate sono le decisioni D1–D25** in [ROADMAP](ROADMAP.md), sezione 3. Tutto il resto qui è una valutazione e una raccomandazione del consiglio. Dove i critici divergono, è detto esplicitamente.

## 1. Sintesi breve

1. **«Prevedere l'inganno e verificare solo i sospetti» con regole aperte non fa risparmiare verifiche.** Le regole di verifica sono uguali per tutti i nodi e note all'imbroglione (D4). Egli presenta la contraffazione solo dove il rilevatore dice «sicuro», e fino al momento dell'inganno si comporta come onesto. È dimostrato rigorosamente: il rilevatore alza la probabilità di verifica della contraffazione rispetto alla verifica media del lavoro onesto non più della distanza tra le loro distribuzioni osservabili (sezione 2). Perciò la previsione, le anomalie, la fiducia basata sulla storia e i grafi possono solo **aggiungere** verifiche oltre il limite inferiore, ma non abbassare la frequenza sotto di esso. Su questo concordano tutti e sei i lavori e tutti e tre i critici.
2. **Gli indizi non falsificabili sono esattamente due:** il risultato del ricalcolo esatto dopo che la risposta è stata fissata in modo irreversibile, e la somma bruciabile in sospeso — le ricompense non ancora pagate della chiave, che andranno perse alla cattura. Tutto il risparmio reale deriva dal secondo indizio, non dall'«intelligenza».
3. **La migliore strategia trovata per le risposte del modello:** il pagatore verifica da sé la propria risposta in un solo passaggio, e prende la decisione «verificare o no» con **la propria moneta segreta** dopo la fissazione della risposta, con probabilità non inferiore a `R/(R + H_lock)`. Qui `R` è il prezzo del compito, `H_lock` è la parte delle ricompense non maturate dell'esecutore che non farà in tempo a maturare entro la fine della verifica. La risposta di un novizio con il conto vuoto è verificata sempre. Allora, alle condizioni della sezione 4, la contraffazione non conviene con nessuna quota di collusione degli altri, compresa la collusione totale. Questa strategia è sostenuta da due critici su tre; il critico ChatGPT preferisce la verifica completa di ogni risposta (sezione 6).
4. **Il costo della verifica stessa è in questo caso frazioni di percento:** circa 0,005–2% del lavoro a seconda del calendario e del carico della chiave, per le chiavi poco attive con limitazione del danno — fino al 6,7% [calcolo]. Il costo principale si sposta nel profilo esatto: è 1,5–1,8 volte più lento della normale generazione a 8 bit con pacchetto 1 e 2,5–2,8 volte con pacchetto 8 [misurato]. Insieme questo è +50…+82% rispetto alla generazione normale con pacchetto 1 [calcolo]. Il riferimento del 5% urta contro la velocità del profilo esatto, non contro la verifica.
5. **Il danno non si chiude con l'economia.** Al danneggiatore il guadagno non serve: con la verifica a campione una parte delle sue contraffazioni passa (circa la metà con il calendario più economico, sezione 4). Perciò la risposta non verificata deve avere la nota «non verificato», e «verificato» si mette solo dopo la verifica completa prima della presentazione. Per il passo di addestramento di una nuova garanzia il consiglio non ha trovato nulla.
6. **L'utente senza attrezzatura** non è protetto da questa strategia: se per lui verificano nodi altrui casuali, la perdita è `R·q^k` e con la collusione totale — l'intero prezzo (sezione 5). Questo resta una questione aperta D21.
7. **Che cosa deve decidere il proprietario:** se consentire il pagamento di un non verificato secondo la regola della moneta (D21, D11, D7); che cosa fare con i guasti onesti gratuiti (D16), che sono incompatibili con la verifica a campione; se accettare la nuova decisione D26 sul «blocco» della somma in sospeso e sul limite del rimborso al danneggiato; la regola delle controversie false (D23, calcolo M9) resta una condizione di inclusione. Le domande sono formulate nella sezione 6.

**Notazioni.** `R` — il prezzo del compito; `c` — il costo del lavoro onesto; `c_f` — i costi della contraffazione (caso peggiore — quasi zero); `H` — la somma in sospeso della chiave dell'esecutore; `H_lock` — la sua parte che non maturerà prima dell'esito finale della verifica di questo compito; `p` — la probabilità di verifica del compito; `q` — la quota di collusione tra i verificatori; `k` — il numero di verificatori assegnati; `n_w` — il numero di compiti della chiave per finestra di maturazione; `ρ` — il tempo di verifica della risposta in un solo passaggio diviso per il tempo della sua generazione (0,10–0,40 con pacchetto 1, 0,26–0,64 con pacchetto 8 [misurato]); `γ` — il rallentamento del profilo esatto rispetto a llama.cpp Q8_0 (1,5–1,8 con pacchetto 1, 2,5–2,8 con pacchetto 8 [misurato]); PPS — verifica da parte del pagatore stesso. `Δ₀` e `Δч` — la differenza attesa del guadagno della contraffazione rispetto all'inazione e rispetto al lavoro onesto; D1 e D25 richiedono che entrambe non siano maggiori di zero.

**Come leggere.** La sezione 2 — perché la previsione dell'inganno non funziona. La sezione 3 — la tabella di tutti gli approcci. La sezione 4 — le formule che hanno superato la critica e gli errori trovati. La sezione 5 — la strategia raccomandata, il suo costo e il rischio residuo. La sezione 6 — le questioni-decisioni. La sezione 7 — i calcoli e gli esperimenti. La sezione 8 — i disaccordi irrisolti e i riferimenti dubbi. La sezione 9 — chi ha fatto che cosa.

## 2. Perché «prevedere l'inganno» non funziona con regole aperte

### 2.1. Il confine attraverso la variazione totale

Sia la decisione di verificare presa da una qualsiasi regola `π(x)` con valore da 0 a 1, dove `x` è tutto ciò che la rete o il pagatore vedono prima della decisione: tempo di risposta, testo, statistica, storia della chiave, grafo dei legami. Il lavoro onesto dà osservazioni con distribuzione `P`, la contraffazione — con distribuzione `F`. Allora

`E_F[π] − E_P[π] = Σ_x π(x)·(F(x) − P(x)) ≤ Σ_{x: F(x) > P(x)} (F(x) − P(x)) = TV(F, P)`.

La disuguaglianza è vera perché `π ≤ 1` dove `F > P` e `π ≥ 0` dove `F < P`. La grandezza `TV` è la distanza di variazione totale: quanto in generale sono distinguibili due distribuzioni. Da qui (teorema T4 del lavoro claude2; la stessa disuguaglianza in gpt1 e gpt2):

1. **La contraffazione è verificata non più spesso del lavoro onesto in media, più `TV`.** Se la contraffazione è difficile da distinguere dalle osservazioni (`TV ≈ 0`), il rilevatore la verifica con la stessa rarità del lavoro onesto.
2. **Contro un avversario consapevole è ancora peggio.** Le regole sono aperte (D4), quindi l'avversario stesso calcola `π` e sceglie quell'osservazione con cui la verifica è meno probabile. La probabilità di cattura della sua migliore contraffazione è uguale al più piccolo `π(x)` tra le osservazioni che egli può creare a buon mercato.
3. **Conseguenza per il risparmio.** Perché la contraffazione sia in perdita, la si deve verificare con probabilità non inferiore a `R/(R + H_lock)` (sezione 4). Con `TV ≈ 0` la stessa frequenza si dovrà mantenere anche per il lavoro onesto, cioè non c'è risparmio. Secondo la stima di claude2, il guadagno dell'«intelligenza» non è più di un fattore `R/(R − c*)`, dove `c*` è il prezzo della contraffazione indistinguibile più economica; con un plausibile `c* ≈ 0,5R` questo non è più di due volte, ma `c*` lo sceglie l'avversario, e non è misurato.
4. **La storia della chiave non dice nulla sul momento dell'inganno.** La chiave che deciderà di ingannare al compito successivo, fino a quel compito ha la stessa storia di una onesta (rapporto di verosimiglianza esattamente 1; teorema T5 di claude2, controesempio di gpt1). Perciò i test sequenziali (SPRT di Wald, CUSUM di Page), gli algoritmi bandit e la «fiducia» bayesiana lo scoprono solo dopo l'inganno. Una piccola enumerazione di claude1 ha mostrato: se la frequenza di verifica basata sulla fiducia si abbassa del 10% sotto la soglia, compare una strategia vantaggiosa «accumulare fiducia e ingannare» (+1,7R…+2,5R per 60 compiti), con un abbassamento della metà — +14,4R…+19,4R [calcolo]. Il critico Claude ha riprodotto questi numeri, il critico DeepSeek nel modello più vicino ha ottenuto un'altra grandezza (+0,085R), ma lo stesso segno (sezione 8).

### 2.2. Esempio sulle misurazioni D5

La contraffazione economica più naturale è **lo stesso Qwen avviato in llama.cpp Q8_0**. Il profilo esatto è più lento di 1,5–1,8 volte con pacchetto 1 e di 2,5–2,8 volte con pacchetto 8 [misurato], quindi la contraffazione è sensibilmente più economica del lavoro onesto. Al tempo stesso è la risposta dello stesso modello: tempo, stile, perplessità sotto il modello piccolo sono uguali a quelli della risposta onesta, e il ritardo l'esecutore può aggiungerlo da sé. Se la risposta Q8_0 coincide con quella esatta token per token, non è una contraffazione: secondo D2 conta il risultato. Se è divergente almeno in un token, lo scoprirà solo il ricalcolo esatto, perché i bit del profilo esatto coincidono su qualsiasi dispositivo provato [misurato].

Riserva del critico ChatGPT: in D5 è stata misurata la vicinanza del profilo esatto al modello ufficiale (lo stesso token in 90 posizioni su 90, correlazione dei logit 0,9996 [misurato]), mentre la vicinanza della contraffazione Q8_0 al profilo esatto per indizi economici non è stata misurata. Per la garanzia questo non è importante: basta che nessuno abbia mostrato un indizio che distingua ogni contraffazione disponibile dalla risposta onesta.

### 2.3. Dove i rilevatori sono comunque utili

I rilevatori, le trappole e l'analisi della rete sono ammissibili se **solo aumentano** la frequenza di verifica:

- come coda di verifiche volontarie aggiuntive del pagatore, che non contano per la garanzia, ma aumentano la cattura reale;
- contro i danneggiatori imprudenti, che non ottimizzano il comportamento;
- per la diagnosi di guasti dell'attrezzatura e dei driver; un partecipante può tenere un CUSUM sulle proprie autoverifiche e fermarsi prima di perdere la somma in sospeso;
- su un flusso di errori non adattivo trovano più errori per ora di verifica. Esempio di gpt1 [calcolo]: con una quota di contraffazioni del 2%, sensibilità del 90% e 5% di falsi allarmi, si verifica l'8,57% dei compiti, si cattura il 90,2% di questa famiglia di contraffazioni, il costo è 1,80% contro 18,94% della verifica uniforme. Ma la famiglia di contraffazioni che il rilevatore non segnala viene lasciata passare nel 98% dei casi.

C'è anche l'attacco inverso (claude2): le richieste alle quali la risposta onesta sembra «anomala» fanno spendere verifiche su onesti. Se la verifica la paga chi l'ha provocata, questo è limitato da sé; se la paga la rete, è un trasferimento di carico.

## 3. Analisi degli approcci

Nella tabella «garantisce» — che cosa segue rigorosamente con le ipotesi nominate; «con `q`» — il comportamento con una quota di collusione dei verificatori; «conto vuoto» — un novizio con `H = 0` e una moltitudine di chiavi gratuite; «verdetto» — l'esito dopo tre critiche.

| Approccio | Essenza | Che cosa garantisce | Con `q` e con `q = 1` | Conto vuoto, molte chiavi | Costo | Verdetto dopo la critica |
|---|---|---|---|---|---|---|
| Giochi di ispezione (Dresher, Maschler, rassegna di Avenhaus–von Stengel–Zamir; giochi di sicurezza di Tambe e coautori — a memoria) | Verifica casuale annunciata in anticipo con una frequenza alla quale l'inganno non è redditizio | `Δ₀ ≤ 0` con `p ≥ (R − c_f)/(R + H_lock)`, compreso il caso di una serie di contraffazioni prima dell'uscita (alle condizioni della sezione 4) | Se verifica il pagatore, non dipende da `q`, compreso `q = 1`. Se verificano i verificatori assegnati — cattura `p·(1 − q^k)`, con `q = 1` zero | `H = 0` ⇒ `p = 1`; ogni chiave risponde con la propria somma, Sybil non aiuta | `p·ρ`: centesimi–decimi di percento per le chiavi attive; verifica completa per il novizio [calcolo] | **Base della strategia**, se la frequenza la esegue chi ha i soldi in gioco |
| Verifica basata sul rischio: SPRT, CUSUM, bandit, fiducia bayesiana | Verificare più spesso i novizi e i sospetti, più raramente quelli di lunga data | Cattura rapidamente l'imbroglione rumoroso costante; contro lo stratega nulla | Il verdetto basato sulle opinioni dei verificatori si rompe con la collusione; con `q = 1` zero | Le nuove chiavi sono gratuite; la chiave «di lunga data» accumula fiducia e inganna alla fine | Il risparmio del 40–70% (ds1) riguarda l'avversario rumoroso, non SkyNet | Abbassare la frequenza sotto la soglia **non si può** (controesempio della sezione 2.1); si possono distribuire verifiche aggiuntive |
| Anomalie, grafi, Sybil (tempo, logit, entropia, perplessità del modello piccolo, filigrane, coerenza delle ripetizioni, grafi di collusione, SybilGuard/SybilLimit/SybilRank) | Cercare comportamenti e legami sospetti | Contro chi conosce il rilevatore — nulla (confine della sezione 2.1) | La contraffazione coordinata sembra un accordo onesto; con `q = 1` non c'è protezione | SybilRank richiede nodi iniziali fidati e un numero piccolo di legami «attaccanti»; i legami la coalizione li compra con lavoro onesto | La perplessità del modello piccolo — circa 1,3–5% di **ogni** risposta secondo la stima di claude1 (critico ChatGPT: ai margini di ds2 1,875–9%) [calcolo], più costosa della verifica secondo la regola; la filigrana certifica solo il campionatore | Solo **segnale per verifiche aggiuntive** e diagnosi dei guasti |
| Trappole, gold questions, modello di Dawid–Skene | Compiti con risposta nota, indistinguibili da quelli veri | Solo se la trappola è indistinguibile e la risposta è segreta. In una rete pubblica il segreto può custodirlo solo il pagatore, e la trappola coincide con la sua verifica (T9 di claude2) | La collusione si divide istantaneamente le trappole; Dawid–Skene presuppone errori indipendenti | Le chiavi usa e getta studiano le trappole con tentativi; il tipo di compito (D22) è visibile all'esecutore | Un riferimento fresco di testo libero costa una generazione completa, più della verifica (`ρ < 1`); per il livello `2⁻⁸⁰` con una quota di trappole del 10% servono 526–527 assegnazioni [calcolo] | Non più economico della verifica da parte del pagatore; la forma ammissibile è la ripetizione di una richiesta già verificata del pagatore |
| Verifica a campione e lotteria (parte dei token o degli strati dopo la fissazione; BOINC, TrueBit, opML, proof of sampling — a memoria) | Verificare una piccola parte del calcolo; oppure pagare solo quanto scelto dal sorteggio (lotteria B) | Token: un singolo difetto passa con probabilità `1 − s/N` (99,2% con 8 posizioni su 1000 [calcolo]). Lotteria B con verifica dello scelto da parte del pagatore: `Δ₀ = −c_f` con qualsiasi `p` | La lotteria con comitato dà al novizio `R·q^k`: 0,001R / 0,027R / 0,125R / R con `q` = 0,1 / 0,3 / 0,5 / 1, `k = 3` [calcolo] | La lotteria B con il pagatore va bene per il novizio; il campionamento di token — no | Stato di Qwen3.5-4B: 48 MiB + 64 KiB per posizione, un campione alla posizione 500/1500/4000 — 79/142/298 MiB [calcolo]; la lotteria dà un reddito irregolare e richiede un pagamento anticipato `R/p` | I token e gli strati sono **peggiori** del passaggio completo sia per traffico sia per garanzia; la lotteria B con il pagatore è una variante ammissibile. I sistemi esterni si reggono su un deposito o su «un onesto su N» |
| Peer prediction (Bayesian Truth Serum di Prelec, peer truth serum, DMI — a memoria) | Pagare per la coerenza dei rapporti senza verifica | La veridicità è un equilibrio solo senza collusione; ci sono equilibri non informativi | Con `q > 0` il gruppo si mette d'accordo; con `q = 1` il meccanismo paga per qualsiasi cosa | Biglietti gratuiti da ogni chiave | Verifica non c'è, ma si paga per non si sa cosa | **Inapplicabili** al calcolo deterministico; il pagamento per la coincidenza è il pagamento per la copia, vietato da D15 |
| Crittografia senza prova completa, TEE, seme | Impegni e rivelazioni a campione, controversia con divisione a metà, sumcheck/GKR, attestazione TEE, generazione deterministica | Il campionamento senza codifica — lo stesso confine `1 − s/N`; la prova completa — sì con D19, ma secondo il preventivo della fase 4 è 16,8 volte e più costosa per la risposta; TEE — fiducia nel produttore | La controversia e il determinismo non dipendono da `q`; con TEE una sola chiave estratta colpisce tutto il parco | Ridurre la frequenza in base all'attestazione darebbe la frequenza ridotta a tutte le chiavi dell'avversario | Impegno sulla risposta — 2–4 KB nel registro (D24) | Servono un impegno sulla risposta, una moneta segreta e una controversia a metà; TEE — solo per aumentare la verifica o per la privacy. La proposta di ds1 di ridurre la frequenza in base al TEE è stata respinta da tutti i critici |
| Economia senza depositi (pagamenti differiti, reputazione come capitale, assicurazione, prezzo della chiave con il lavoro) | Punire con la perdita delle ricompense non maturate e del reddito futuro | La somma in sospeso è l'unica leva compatibile con R5. Il reddito futuro all'uscita è zero. L'assicurazione risarcisce la vittima, ma non riduce il guadagno dell'imbroglione | Funziona se la frequenza la esegue il pagatore | `H = 0` ⇒ verifica completa. L'ingresso con il lavoro è un deposito nascosto, inutile all'uscita; con la perdita da comitato `R·q³` e `q = 0,3` il prezzo d'ingresso `10R` viene ripagato da circa 370 tentativi (ds1) [calcolo] | Ritardo del pagamento per la finestra di maturazione | `H_lock` è una parte obbligatoria della strategia; il resto non serve come fondamento della garanzia |

## 4. Limiti inferiori e formule che hanno superato la critica

### 4.1. Contraffazione singola: soglia `R/(R + H_lock)`, non `R/H`

La contraffazione intercettata non viene pagata e brucia la somma in sospeso (non si può addebitare altro secondo R5). Allora

`Δ₀ = (1 − p)·R − p·H_lock − c_f ≤ 0  ⇔  p ≥ (R − c_f)/(R + H_lock)`,

e con una contraffazione quasi gratuita — `p ≥ R/(R + H_lock)`. Contro il lavoro onesto `Δч = Δ₀ − (R − c) ≤ Δ₀`, quindi la seconda condizione di D25 si soddisfa da sé. Per il novizio `H_lock = 0`, e `p = 1`. Frequenza minima [calcolo, claude2]: 0,5 con `H_lock = R`; 0,25 con `3R`; 0,0909 con `10R`; 0,01 con `99R`; 0,000231 con `4320R`.

Il lavoro claude1 ha proposto la regola `p = min(1, R/H)` e l'ha chiamata esatta. Il critico Claude ha mostrato con un'enumerazione che la soglia esatta è `R/(R + H)`: con essa il massimo guadagno della contraffazione è esattamente 0, mentre già con `0,99·R/(R + H)` — da +0,225R a +0,299R [calcolo]. La regola `R/H` contiene un margine. Il critico DeepSeek ha osservato che questo margine è utile per il danno: con `R/H` il numero atteso di contraffazioni fino alla cattura è finito (circa `H/R + 1`), con `R/(R + H)` — infinito (sezione 4.4). Quale formula prendere nel nucleo non è deciso (sezione 8).

### 4.2. Condizione: la somma non matura prima dell'esito della verifica

Si può bruciare solo ciò che non è ancora stato pagato al momento della controversia dimostrata. Se una parte di `H` riesce a maturare prima, la regola si rompe. Controesempi [calcolo]:

- claude2: una chiave con `H = 99R`, che maturano prima dell'esito, presenta `n` contraffazioni con `p = 1%`; guadagno 0,99R con `n = 1`, 9,04R con 10, 36,6R con 100;
- critico Claude: una chiave con `H₀ = 100R` smette il lavoro onesto e presenta contraffazioni, mentre i pagatori verificano in ritardo; guadagno +0,99R, +9,1R, +49,7R, +74,4R con `n` = 1, 10, 100, 300. Con il «blocco» (brucia tutto) le stesse strategie danno da −0,01R a −0,75R.

Perciò al denominatore della frequenza per il compito `i` entra solo quella parte della somma che maturerà **dopo** il termine ultimo della controversia su `i`, e il termine di verifica da parte del pagatore `δ` deve essere molto minore della finestra di maturazione `W`; entrambi i termini si contano nel tempo attivo (D12). È l'ipotesi della «verifica tempestiva»; per un telefono che si collega raramente alla rete, essa si viola per prima.

### 4.3. Ondate di contraffazioni prima dell'uscita

La serie di contraffazioni prima dell'uscita è coperta dalla formula della contraffazione singola solo con la regola **«la prima cattura dimostrata brucia tutta la somma non maturata della chiave, comprese le ricompense della stessa ondata»**.

- Senza questa regola (gpt1): 10 contraffazioni parallele con `R = 1`, `B = 4R`, `d = 0,2`, quando ogni contraffazione non intercettata viene pagata e la vecchia somma si perde una sola volta, danno `10·0,8 − 4·(1 − 0,8¹⁰) = +4,4295R`, sebbene una sola contraffazione dia zero. Se la cattura annulla tutta l'ondata, la stessa strategia dà −2,49676R [calcolo; ripetuto dai critici].
- Il critico ChatGPT ha aggiunto un secondo esempio: con `H = R`, `p = 1/2`, due contraffazioni con monete indipendenti e un addebito una tantum della vecchia somma, il guadagno è `R/4` [calcolo]. Dunque il protocollo è obbligato a collegare atomicamente tutti gli impegni aperti della chiave con tutto il suo ricavo non maturato.

Con questa regola la dimostrazione di claude2 (T2) è corretta: ogni nuova contraffazione moltiplica l'esito atteso per `(1 − p_j)·(1 + α_j/(H_lock + A)) ≤ 1`, dove `α_j` è il pagamento per il non verificato e `A` è il già accumulato bruciabile. L'induzione sul numero di contraffazioni dà `E[esito] ≤ H_lock` per qualsiasi serie e qualsiasi sequenza adattiva. Per una serie omogenea lo stesso segue da `(1 + R/H)ⁿ ≥ 1 + nR/H`. La verifica su una griglia di frazioni esatte ha dato il massimo superamento esattamente 0 [calcolo].

### 4.4. Verifica da parte del comitato: fattore `1 − q^k`

Se la cattura deve essere registrata da almeno uno dei `k` verificatori assegnati, e ciascuno con probabilità `q` appartiene alla coalizione, la probabilità di cattura scende a `p·(1 − q^k)`, e la soglia diventa `p ≥ R/((R + H_lock)·(1 − q^k))`. È irrealizzabile con `1 − q^k < R/(R + H_lock)` e sempre irrealizzabile con `q = 1`. Nella lotteria B con comitato il novizio riceve `R·q^k` per tentativo: 0,001R / 0,027R / 0,125R / R con `q` = 0,1 / 0,3 / 0,5 / 1 e `k = 3` [calcolo]. Questo coincide con il modello dell'avversario. L'indipendenza delle scelte è anch'essa un'ipotesi: scegliendo `k` diversi tra `N` partecipanti, dei quali `C` in collusione, la probabilità di collusione completa è `C(C,k)/C(N,k)`; con l'indisponibilità generale dei dati o un rilascio selettivo può arrivare a `q` o a 1 (critico ChatGPT secondo il modello dell'avversario). Conclusione di tutti i lavori: **la frequenza deve eseguirla chi difende la propria decisione** — il pagatore per i propri soldi, ogni nodo per la propria contabilità.

### 4.5. Danno: la quota di non intercettato

Al danneggiatore il guadagno non serve, quindi il danno si valuta con la quota delle sue contraffazioni passate senza cattura.

- **Il calendario più economico rende il danno illimitato.** Con `p = R/(R + H)` le contraffazioni non verificate aumentano esse stesse `H`, e la frequenza scende. La probabilità di sopravvivere a `n` contraffazioni partendo da `h = H/R` è `h/(h + n)`; il numero atteso di contraffazioni fino alla cattura è infinito (T8 di claude2). La stima di claude1 «`e^{−m}`» sottovaluta il passaggio: con `H₀ = 4320R` e 4320 contraffazioni il passaggio esatto è 0,50 invece di 0,37 con frequenza `m·R/H` e `m = 1`; 0,125 invece di 0,050 con `m = 3`; 0,0078 invece di 0,0009 con `m = 7` [calcolo, critico Claude].
- **Una contraffazione mirata** passa con probabilità `1 − p`: per una chiave matura con `n_w = 4320` circa 99,977% (critico ChatGPT) [calcolo].
- **La correzione basata sulla parte verificata della somma non ha retto.** claude2 ha proposto di calcolare la frequenza su `H_ver` — ricompense solo per i compiti verificati; allora per una chiave onesta `p ≈ 1/√n_w` (punto fisso `p²·n_w + p − 1 = 0`) e la quota di contraffazioni del danneggiatore è circa `p`: 5,6% con `n_w = 300`, 1,8% con 3000, 0,58% con 30 000 [calcolo]. Il critico Claude ha mostrato che `H_ver` viene gonfiato dalle richieste autopagate della coalizione; il critico ChatGPT — che il danneggiatore con una chiave nuova, dopo una risposta verificata con `p = 1/2`, ottiene che sia falsa circa la metà delle sue risposte consegnate. Un confine economico del danno che regga l'autopagamento e le nuove chiavi non l'ha trovato nessun lavoro.

Conclusione: con qualsiasi `p < 1` una parte delle risposte del danneggiatore è falsa. Per le richieste questo è ammissibile solo con la nota «non verificato» (testo D6), per il passo di addestramento — no.

### 4.6. Altre formule che hanno superato la critica

- **I guasti gratuiti sono incompatibili con la verifica a campione** (claude1). Se un guasto onesto non brucia la somma (D16), l'imbroglione catturato chiama la contraffazione un guasto, e `Δ₀ = (1 − p)·R − c_f > 0`. Con `b` guasti gratuiti per finestra la perdita è dell'ordine di `b·H` per finestra [calcolo].
- **Pagatori pigri** (claude2). Se una quota `λ` di pagatori non verifica e l'esecutore non li distingue, serve `p·(1 − λ) ≥ R/(R + H_lock)`. Se li distingue — la contraffazione contro di loro frutta fino a `R` senza rischio. Il contenimento è un bene comune: il pagatore che disattiva la verifica risparmia frazioni di percento e non perde nulla. È l'ipotesi «i pagatori in media eseguono la moneta del nucleo».
- **Prezzo e irregolarità della lotteria B** (claude2, T7, con la correzione del critico ChatGPT). Il pagamento `R/p` con probabilità `p` dà un coefficiente di variazione del reddito `√((1 − p)/(pT))` per `T` compiti. Per una dispersione data `v` serve `p ≥ 1/(1 + T·v²)`; con `T = 6000`, `v = 10%`, `ρ = 0,21` il prezzo minimo della verifica è 0,3443% [calcolo]. Con la verifica «da ciascuno dei 1000 nodi» lo stesso prezzo si moltiplica per il numero di nodi, quindi la lotteria con verifica da parte di tutti i nodi per l'emissione di crediti è inutilizzabile.
- **La collusione tra pagatore ed esecutore** si riduce a un trasferimento dei propri soldi all'interno della coalizione, finché la richiesta pagata non crea emissione di crediti, peso e diritto al risarcimento dalla cassa comune.

### 4.7. Errori nelle formule dei lavori (in breve)

| Lavoro | Errore | Correzione |
|---|---|---|
| ds2 | La seconda soglia è scritta come `(c − c_f)/R` | Deve essere `(c − c_f)/(R + H)`; questa soglia non è mai vincolante. Trasmettere ai mini-agenti solo quella corretta |
| ds1 | Nel gioco la perdita è presa `L = H + V` senza tener conto della `c_f` già spesa | Soglia `(R − c_f)/(R + H + V)`; con `H = 0`, `c_f = 0,1R` — 90%, non 100% |
| claude1 | Equilibrio del gioco di ispezione con `L = H + R` (doppio conteggio di `R`) | Punto di indifferenza `(R − c_f)/(R + H)`: con `H = R`, `c_f = 0` — 1/2, non 1/3 |
| claude1 | «La regola `R/H` è esatta»; danno `e^{−m}` | Soglia esatta `R/(R + H)`; il passaggio è più alto (sezione 4.5) |
| claude1 | Generazione speculativa «circa `1 + ρ·s`» | Non derivato; secondo il critico DeepSeek — doppio conteggio; con pacchetto 8 risulta 1,65–2,79 |
| claude2 | T7: «`κ·CV²` non dipende da `p`» | C'è un fattore `1 − p`; soglia esatta `p ≥ 1/(1 + T·v²)` |
| claude2 | Il prezzo complessivo 0,2–1,2% è preso con `n_w = 3000` | Con `n_w = 300` — 0,56–2,24% (fino a 3,6% con pacchetto 8), con `n_w = 30` — 1,7–6,7% [calcolo] |
| claude2 | Snapshot dello stato 0,33 e 2,9 GiB per risposta | Con la cache di attenzione 0,651 GiB (500/500, passo 64) e 12,38 GiB (2000/1000, passo 16) [calcolo, critico ChatGPT] |
| claude2 | In S1 il pagamento del non verificato `α` con la regola su `H_ver` è sempre uguale a `R` | Non c'è un passaggio graduale A/B in S1; il faro comune per la decisione di verifica non serve |
| ds1, gpt1, gpt2 | Preventivi delle strategie senza il rallentamento del profilo esatto | Il prezzo completo è 1,5–1,8 volte più alto già con pacchetto 1 (sezione 5.2) |
| ds1 | «La verifica di `k` token non è più economica di un passaggio completo» | Per calcoli è più economica; perde per il traffico dello stato e per la garanzia |
| gpt2 | Certificato secondo i limiti dei logit: 6,25% | I limiti richiedono lo stato vero dell'ultimo strato; la testa è circa il 15% delle moltiplicazioni, il risparmio non è più della sua quota |
| ds2 | Quota stabile di inganno contro CUSUM `θ = d_h/(d_h + d_f)` | È un'approssimazione secondo la deriva media, non un teorema |
| ds1 | SPRT: 65 e 133 osservazioni | Ricalcolo esatto del critico ChatGPT: 132,73 e 76,70, test fisso — 229 [calcolo]; non riguarda l'avversario strategico |

## 5. Strategia raccomandata

### 5.1. Risposte del modello: «il pagatore-ispettore con la posta»

Il nucleo è preso dai lavori claude1 e claude2, le correzioni — da gpt1 e dalle tre critiche.

1. **Profilo esatto.** Ogni risposta pagabile è generata nel profilo esatto v2 (scelta greedy o Gumbel-max canonico), il testo cifrato della risposta è registrato nel registro con una sola voce insieme all'accettazione (D24).
2. **Moneta segreta del pagatore.** Dopo che la risposta è stata fissata in modo irreversibile, il programma del pagatore con la propria casualità segreta decide se verificarla in un solo passaggio, con probabilità `p_i = max(p_utente, R_i/(R_i + H_lock))`. `p_utente` lo sceglie l'utente stesso; con `p_utente = 1` egli vede solo risposte verificate. Con `H_lock = 0` (novizio) la verifica è sempre. Un faro comune per questo non serve, finché il pagamento non dipende dall'esito della moneta; la decisione non attende un blocco pubblico.
3. **Blocco della somma.** `H_lock` per il compito `i` — le ricompense non maturate della chiave che matureranno dopo il termine ultimo della controversia su `i`; il termine di verifica `δ` è molto minore della finestra di maturazione (sezione 4.2).
4. **Bruciatura.** Qualsiasi divergenza dimostrata brucia **tutta** la somma non maturata della chiave, comprese le ricompense della stessa ondata. Al danneggiato si restituisce non più del suo pagamento `R`, il resto viene distrutto. Altrimenti è possibile l'attacco di «autocontroversia»: la coalizione con la propria chiave-pagatore intercetta una richiesta autopagata deliberatamente contraffatta e prende le somme altrui aggirando la finestra di maturazione (critico Claude).
5. **Note.** «Verificato» — solo una risposta verificata completamente prima della presentazione. Tutto il resto per impostazione predefinita è «non verificato». La nota «verificato a campione» (claude1) è stata respinta da tutti i critici come fuorviante.
6. **Segnali solo verso l'alto.** Anomalie, perplessità, grafi, ripetizioni di richieste verificate (trappole) avviano solo verifiche volontarie aggiuntive. Abbassare la frequenza in base alla storia, alla reputazione, alle anomalie, all'attestazione o al numero di chiavi è vietato.
7. **Controversie** — solo con la prova della divergenza, che ogni nodo verifica da sé (I8). La strategia non si attiva senza una regola delle controversie false (D23, calcolo M9).
8. **Variante per le chiavi con una piccola somma.** Dove la verifica frequente è costosa per il pagatore, è ammessa la lotteria B: si paga solo la risposta scelta dal sorteggio, il suo pagatore la verifica per intero (gpt1, claude2). In essa il guasto onesto gratuito (D16) si conserva senza modifiche, ma il reddito dell'esecutore è irregolare, e il pagatore tiene un pagamento anticipato `R/p`.

La strategia richiede di modificare D16 e D21 (sezione 6). Tutti gli zeri della garanzia sono condizionali: la coincidenza dei bit sui dispositivi provati, non su qualsiasi dispositivo; la verifica tempestiva; la vitalità del registro e l'assenza di censura della prova; la correttezza del nucleo; l'esecuzione onesta della moneta da parte del programma del pagatore; la regola delle controversie false.

### 5.2. Prezzo

Parametri: `p = R/(R + H)` con `H ≈ n_w·R` a regime; `ρ` = 0,10 / 0,21 / 0,40 (pacchetto 1); `γ` = 1,5–1,8 (pacchetto 1) e 2,5–2,8 (pacchetto 8). Il prezzo completo rispetto a Q8_0 — `γ·(1 + p·ρ) − 1`. Tabella del critico Claude [calcolo]:

| `n_w` (compiti della chiave per finestra) | `p` a regime | Verifica con `ρ` = 0,10 / 0,21 / 0,40 | Totale rispetto a Q8_0, pacchetto 1 | Totale, pacchetto 8 | Verifiche nella prima finestra di una nuova chiave |
|---|---|---|---|---|---|
| 30 | 3,23% | 0,32% / 0,68% / 1,29% | +50,5% … +82,3% | +152% … +186% | circa 4,0 |
| 300 | 0,33% | 0,033% / 0,070% / 0,133% | +50,0% … +80,2% | +150% … +181% | circa 6,3 |
| 4320 | 0,023% | 0,002% / 0,005% / 0,009% | +50,0% … +80,0% | +150% … +180% | circa 9,0 |

Altri calendari [calcolo]: con la frequenza minima in termini di denaro `p ≈ t_task/t_lock ≈ 2,3·10⁻⁴` la verifica costa circa 0,005% del lavoro (critico DeepSeek); con la frequenza con limitazione del danno `p ≈ 1/√n_w` — 0,18–0,72% con `n_w = 3000` e 0,56–2,2% con `n_w = 300`; con la lotteria B con `p = 5%` — 0,5–2,0% con pacchetto 1. Se alla regola monetaria si aggiunge un pavimento contro il danno su `H_ver`, la verifica cresce fino a 0,15–2,2% con `n_w` = 300–4320 e fino a 6,7% con `n_w = 30` (critico Claude). Il primo compito del novizio costa una verifica completa, 10–40% della sua generazione.
Per confronto: la verifica completa di ogni risposta (contratto principale di gpt1, gpt2, ds2) costa `γ·(1 + ρ) − 1` = +65…+152% rispetto a Q8_0, con `γ = 1,65`, `ρ = 0,21` — +99,65% [calcolo].

Non sono calcolati: la registrazione di 2–4 KB per ogni risposta nel registro, le controversie false (M9), l'energia, la verifica sui dispositivi dei pagatori. **Il collo di bottiglia del riferimento del 5% è il rallentamento del profilo esatto, non la verifica.** Possono ridurlo nuclei veloci bit per bit uguali e la decodifica speculativa esatta: la bozza è generata dal veloce Q8_0, e il profilo esatto accetta il prefisso fino alla prima divergenza. Stima di claude2 con coincidenza del 99% dei token e blocco 32 — circa 0,78 del tempo di un token esatto, cioè +28% rispetto a Q8_0 invece di +65%; con coincidenza del 95% — 1,33 del tempo di un token esatto, peggio della generazione diretta (critico Claude) [calcolo; la coincidenza non è misurata].

### 5.3. Rischio residuo

Guadagno atteso per una contraffazione; «danno» — la quota di contraffazioni non rilevate del danneggiatore, tutte con la nota «non verificato». Sintesi del critico Claude e del critico DeepSeek [calcolo].

| Caso | `q = 0,1` | `q = 0,3` | `q = 0,5` | `q = 1` | Novizio, `H = 0` |
|---|---|---|---|---|---|
| Denaro, il pagatore verifica da sé | ≤ 0 | ≤ 0 | ≤ 0 | ≤ 0 | `−c_f` (verifica sempre) |
| Risposta falsa mostrata come «verificato» | 0 | 0 | 0 | 0 | 0 |
| Danno con `p = R/(R + H)`: non intercettato dopo `n_w` contraffazioni | circa 50% | circa 50% | circa 50% | circa 50% | 0 (i primi vengono verificati) |
| Lo stesso con `p = 3R/(R + H)` | circa 12,5% | idem | idem | idem | 0 |
| Il pagatore senza attrezzatura affida la verifica a una terna casuale | +0,001R | +0,027R | +0,125R | +R | idem |
| Il pagatore non verifica, l'esecutore lo distingue | fino a +R | fino a +R | fino a +R | fino a +R | 0 |
| Addestramento, c'è un auditor onesto a frequenza piena | ≤ 0 | ≤ 0 | ≤ 0 | — | `−c_f` |
| Addestramento, non c'è un auditor onesto | fino a +R | fino a +R | fino a +R | fino a +R | fino a +R |

Le righe «il pagatore verifica da sé» non dipendono da `q`. Questo è il risultato principale del consiglio: la verifica indipendente dalla quota di collusione è economica per il pagatore se egli verifica a campione, e la somma bruciabile dell'esecutore è bloccata fino alla fine della verifica.

### 5.4. Il novizio

Una chiave con il conto vuoto è verificata sempre, quindi la contraffazione da parte sua dà `−c_f`. Man mano che si accumula la somma bloccata la frequenza scende: con la regola `R/(R + H)` nella prima finestra circa 4,0 / 6,3 / 9,0 verifiche complete con `n_w` = 30 / 300 / 4320 (critico Claude), con la regola `R/H` — 5,0 / 7,3 / 10,0 (claude1) [calcolo]. Il prezzo della prima finestra con `n_w = 30` — 1,7 / 3,5 / 6,6% con `ρ` = 0,10 / 0,21 / 0,40 (claude1) [calcolo]. Il «prezzo d'ingresso» è il lavoro utile verificato completamente, non una quota d'iscrizione. Il rovescio della medaglia è il carico: la coalizione di nuove chiavi costringe i pagatori a verificare ogni loro risposta. Questo colpisce il prezzo (R6), ma non D1; la grandezza va calcolata (sezione 7).

### 5.5. L'utente senza attrezzatura

La strategia non lo protegge. Se egli affida la verifica a una terna casuale di nodi altrui, la perdita attesa è `R·q³`: 0,001R / 0,027R / 0,125R / R con `q` = 0,1 / 0,3 / 0,5 / 1 [calcolo]. Se la affida al proprio dispositivo o a un nodo conoscente, è una sua ipotesi secondo D21; con la collusione dell'aiutante con l'esecutore la falsa certificazione è possibile con probabilità 1. Il critico Claude propone di verificare con un esperimento quanto costa la verifica in un solo passaggio sul processore di un portatile e di un telefono: con una frequenza di circa una verifica per finestra della chiave, una verifica lenta e rara può risultare accettabile. La garanzia per un tale utente resta una questione aperta D21.

### 5.6. Addestramento

Per il passo di addestramento il consiglio non ha trovato una nuova garanzia. Il passo non ha un pagatore con i soldi in gioco, quindi la verifica a campione deve eseguirla ogni nodo che necessita della garanzia, e il prezzo si moltiplica per il numero di tali nodi. Varianti:

- **Ripetizione completa del passo** dal genitore accettato — circa 100% del lavoro del passo per ogni nodo verificatore. Esempio del critico ChatGPT: se l'inferenza è l'80% del lavoro di base, `ρ = 0,21` e ogni passo si ripete una volta, risulta 0,8·0,21 + 0,2·1 = 36,8% oltre il lavoro di base [calcolo]; con `N` nodi che verificano da sé, il secondo termine si moltiplica per `N`.
- **Verifica a campione del passo da parte di tutti i nodi completi** (claude2, S2): solo per il denaro con una finestra di 3 giorni — 0,23% / 2,3% / 23% del lavoro della rete con 10 / 100 / 1000 nodi verificatori; con una limitazione del danno del 10% — 10 volte più costosa [calcolo; la colonna del danno non è derivata rigorosamente]. Richiede un addestramento intero esatto, che non è costruito né misurato.
- **Audit «un onesto su N»** (claude1, S2) — è un'ipotesi che la fase 4 ha già respinto per l'addestramento; senza un audit pagato l'equilibrio è «non ci sono auditor».
- **Pagamento per il miglioramento dimostrato (D18)** — non è una verifica del passo; il calcolo M12 ha già mostrato che il duplicato esatto della richiesta aumenta l'accredito del proprietario secondo tutte e tre le regole di attribuzione (calcolo dei mini-agenti, sintesi D5_RESULTS).

L'addizione robusta dei contributi (Krum, mediana, media troncata — a memoria) limita il danno della quota non intercettata, ma non protegge dai danneggiatori coordinati con una quota di peso notevole e non soddisfa D1. Un passo non verificato non deve entrare nella versione rilasciata del modello (D6).

## 6. Decisioni da modificare o accettare

Le formulazioni seguenti sono **raccomandazioni del consiglio**, non decisioni accettate. Ogni questione va accettata o respinta esplicitamente. I requisiti immutabili R1–R6 non cambiano con la modifica di una riga della tabella di marcia (promemoria di gpt1).

**Domanda 1 (D21, nonché D11 e D2). Consentire al pagatore di pagare dal proprio pagamento anticipato una risposta che il suo programma, secondo la regola del nucleo, non ha verificato?** Attualmente D21 dice: «La rete non paga una risposta senza verifica», e D11 — «si paga solo il verificato».
*Raccomandazione (critico Claude, secondo i lavori claude1 e claude2):* sì. La seconda frase proposta di D21: «Il pagatore paga dal proprio pagamento anticipato la risposta che ha verificato o lasciato passare secondo la regola D7 con la propria moneta segreta; la risposta lasciata passare ha la nota «non verificato». Non c'è emissione di crediti né peso per la richiesta pagata». Contemporaneamente va precisato D11 (e, secondo l'osservazione del critico DeepSeek, D2), altrimenti le modifiche si contraddicono a vicenda.
*Dove sono divergenti:* il critico DeepSeek — non cambiare D21 per ora (la strategia è comunque bloccata da D23) e usare la lotteria B (`α = 0`, pagamento `R/p` allo scelto), compatibile con gli attuali D2, D11, D21. Il critico ChatGPT — lasciare come contratto principale la verifica completa di ogni risposta da parte del pagatore, e introdurre il pagamento degli scelti dal gruppo con un contratto separato; senza una verifica autonoma non c'è pagamento di rete.

**Domanda 2 (D7). Come scrivere quale verifica è ammissibile per il pagamento?**
*Raccomandazione (critico Claude):* «La verifica indipendente dalla quota di collusione è obbligatoria per la nota «verificato», per l'emissione di crediti e per il peso. Il pagamento della richiesta con i mezzi del pagatore è ammesso dopo la verifica da parte del pagatore oppure dopo il passaggio della verifica secondo la regola del nucleo: moneta segreta del pagatore, lanciata dopo la fissazione della risposta, con probabilità non inferiore a `R_i/(R_i + H_lock)`. Abbassare questa probabilità in base alla storia, alla reputazione, alle anomalie, all'attestazione o al numero di chiavi è vietato; alzarla è permesso. La verifica da parte dei verificatori assegnati non serve come base del pagamento. D1 non si indebolisce fino a `q < q*`». Separatamente va scelto `R/(R + H_lock)` (soglia esatta) oppure `R/H` (con margine, numero finito di contraffazioni del danneggiatore fino alla cattura).
*Dove sono divergenti:* i critici DeepSeek e ChatGPT propongono di non cambiare il testo di D7, ma di aggiungere l'ambito di applicazione: la garanzia alla parte che esegue essa stessa la verifica non dipende da `q`; la parte che ha delegato la verifica è protetta solo con una quota di collusione degli assegnati inferiore a `q*`, e questo le viene mostrato (critico DeepSeek). Il critico ChatGPT aggiunge: rating, quorum, scadenza e l'ipotesi `q_eff < q*` non danno diritto a uno status indipendente.

**Domanda 3 (D6). Precisare le note del risultato?**
*Raccomandazione (comune ai critici, formulazione secondo ds1):* «Una risposta falsa non viene presentata come «verificata». Le note sono due: «verificato» — verifica completa prima della presentazione con un metodo indipendente dalla quota di collusione (per la richiesta — dal pagatore in persona, oppure con una prova accettata dal nucleo); «non verificato» — per impostazione predefinita, messa automaticamente, può toglierla solo una tale verifica. L'emissione in streaming — a blocchi verificati oppure con questa nota. Un passo di addestramento non verificato non entra nella versione rilasciata del modello». Il critico ChatGPT precisa: il passo non verificato e i suoi discendenti possono stare solo in un ramo di ricerca isolato senza pagamento per la transizione.
*Dove sono divergenti:* in sostanza non divergono; claude1 proponeva una terza nota «verificato a campione» — l'hanno respinta tutti e tre i critici.

**Domanda 4 (D16). Che cosa fare con un guasto hardware onesto?** Attualmente il guasto non è punito, e la somma in sospeso non brucia. Con la verifica a campione con pagamento del non verificato questa è una perdita diretta (sezione 4.6).
*Raccomandazione (critici Claude e DeepSeek, secondo claude1):* «Con la verifica completa o la lotteria B un guasto onesto non è punito (regola precedente). Con la verifica a campione con pagamento del non verificato qualsiasi divergenza dimostrata brucia l'`H_lock` della chiave indipendentemente dalla causa, poiché la causa da un'uscita errata identica non si può stabilire. La perdita attesa dell'onesto (circa `P_f·R` per compito, dove `P_f` è la probabilità di guasto silenzioso) è risarcita da un supplemento incondizionato dal prelievo di rete. La regola si attiva solo dopo la misurazione di `P_f`».
*Dove sono divergenti:* il critico ChatGPT — conservare la protezione dal guasto onesto: il guasto lascia il risultato senza pagamento, le ricompense precedenti si conservano, il numero di guasti per chiave è limitato, e l'affidabilità del calcolo non deve dipendere dall'addebito delle ricompense precedenti. Egli osserva anche che il supplemento dal prelievo altrui per ogni compito aumenta il pagamento anche alla contraffazione e cambia la soglia. Il critico Claude aggiunge: bruciare la finestra di reddito per un'instabilità non misurata colpisce i nodi deboli (R6), il supplemento risarcisce la media, non il rischio di rovina. La disputa si risolve con la scelta della struttura di pagamento (la lotteria B conserva D16, il pagamento del non verificato — no) e con la misurazione di `P_f`.

**Domanda 5 (D8). Come organizzare il termine e i diritti della controversia?**
*Raccomandazione (critico Claude):* «Il pagatore presenta la prova della divergenza non oltre il termine `δ` di tempo attivo dopo aver ricevuto la risposta; la controversia si risolve solo con una prova che ogni nodo verifica da sé». *Aggiunta (critico ChatGPT):* l'esecutore ha diritto di chiedere il calcolo secondo il proprio ordine fissato in caso di rifiuto ingiustificato o di silenzio dell'acquirente; entrambe le parti disputano da un conto zero senza deposito; il duplicato non avvia una nuova verifica costosa; fino alla decisione la somma contestata resta in sospeso. Qui c'è un bivio aperto: se si paga alla scadenza del termine senza obiezione, l'assenza del pagatore paga la contraffazione; se si rifiuta per il silenzio, il pagatore disonesto ottiene gratis una risposta corretta.
*Dove sono divergenti:* claude2 e il critico DeepSeek propongono, dopo M9, di consentire la controversia a qualsiasi nodo sul compito scelto dal faro con una quota di controversie false; il critico Claude lo ritiene vuoto per una richiesta privata (un nodo estraneo non ha la richiesta) e utile solo per l'addestramento.

**Domanda 6 (D23). Lasciare il blocco fino al calcolo M9?**
*Raccomandazione (tutti e tre i critici):* lasciarlo. Integrare (critico Claude): «M9 si calcola per la regola D7: le controversie sono rare in equilibrio, ma la coalizione «pagatore = esecutore» può presentarle a volontà su richieste autopagate; la somma bruciata viene distrutta, al danneggiato si restituisce non più del suo pagamento». Il critico ChatGPT propone di scrivere il criterio di revoca del blocco: limiti superiori di byte, calcoli, messaggi e termini per una singola causa, limite delle cause contemporaneamente aperte, fonte di copertura del carico, verifica del formato e dell'unicità prima del ricalcolo costoso, resistenza alle richieste autopagate, alla collusione di entrambe le parti, al rifiuto falso dell'acquirente, alla partizione della rete e all'indisponibilità dei dati.

**Domanda 7 (nuova D26). Accettare la decisione sul blocco della somma in sospeso e sul limite del rimborso?**
*Raccomandazione (critico Claude, con le correzioni della sezione 4):* «`H_lock` del compito `i` — le ricompense non maturate della chiave che matureranno dopo il termine ultimo della controversia su `i`; il termine di verifica da parte del pagatore è molto minore della finestra di maturazione. Una divergenza dimostrata brucia tutta la somma non maturata della chiave, comprese le ricompense dei compiti consegnati dopo quello contestato e nella stessa ondata. Al pagatore danneggiato si restituisce non più del suo pagamento per la risposta contestata; il resto viene distrutto; la prima controversia non prende somme dovute ad altri pagatori». Senza questa regola la strategia delle sezioni 5.1–5.3 non regge (controesempi +4,4295R e fino a +74,4R nelle sezioni 4.2–4.3).
*Dove sono divergenti:* il critico ChatGPT non discute il blocco in questa forma, poiché non sostiene il pagamento del non verificato; ma egli stesso esige di collegare atomicamente gli impegni aperti con tutto il ricavo non maturato.

**Domanda 8 (D1). Bisogna cambiare D1?**
*Raccomandazione (tutti e tre i critici):* non indebolire il testo. Le varianti «D1 con una quota di collusione inferiore a `q*`» e «perdita non superiore a `ε` del fatturato» (claude1, ds1, ds2, gpt1) sono respinte: con `q = 1` esse consegnano alla coalizione tutta l'emissione non verificata, contraddicono D19 e l'immutabile R4, e il «fatturato» viene gonfiato da autotrasferimenti. Il critico Claude propone una nota: per la risposta del modello D1 è garantito nei confronti del pagatore che esegue la verifica del nucleo; la verifica a campione con la sua moneta segreta soddisfa D1 come aspettativa ed è registrata come ipotesi sull'avversario razionale (secondo R4 il campionamento statistico è un'ipotesi); per il consumatore che non verifica D1 la rete non lo promette. Il critico DeepSeek — una nota che la garanzia D1 riguarda ogni risultato con la nota «verificato» e ogni emissione di crediti.

## 7. Che cosa calcolare con i mini-agenti e che cosa verificare con esperimenti

### 7.1. Calcoli esatti (frazioni, hash di controllo, ripetizione su un secondo dispositivo)

1. Enumerazione completa della regola D7 con maturazione della somma, ondate, più chiavi, prezzi diversi nell'ondata e verifiche a posteriori. Valori di riferimento: `κ = 1` → 0; `κ = 0,9` con `H₀ = 0` → +1,734R (riprodotto dal critico Claude, non riprodotto dal critico DeepSeek — deve decidere l'enumerazione); `0,99·R/(R + H)` → +0,225R; controesempio di maturazione +0,99R / +9,08R / +49,7R / +74,4R.
2. Formula dell'ondata di gpt1: +4,4295R con addebito separato e −2,49676R con la bruciatura di tutta l'ondata.
3. Attacco di «autocontroversia»: con quale quota di rimborso al danneggiato il guadagno diventa positivo.
4. Perdita dei guasti gratuiti (`b` per finestra) e supplemento `P_f·R` con la dispersione delle perdite dell'onesto.
5. Danno con i calendari `H_lock`, `H_old`, `H_ver`, `m·R/(R + H)` con autopagamento e nuove chiavi; valori di riferimento 0,50 / 0,125 / 0,0078 con `n_w = 4320`.
6. Pagatori pigri: la quota `λ` e la distinguibilità con cui il contenimento scompare.
7. Carico della coalizione di nuove chiavi sui pagatori con `p = 1` per i novizi.
8. M9 (controversie false) per la regola D7 — condizione D23.
9. Prezzo complessivo `γ·(1 + p·ρ)` su una griglia di `γ`, `ρ` misurati e della distribuzione di `n_w`.
10. Probabilità di collusione completa con scelta senza reimmissione (`C(C,k)/C(N,k)`) e con i giri di sorteggio.
11. Dimensioni degli snapshot dello stato secondo la configurazione fissata del modello (M1) — disputa sul prezzo dei token campionati e degli snapshot.
12. La soglia corretta di ds2 e lo script di controllo di gpt2 (SHA-256 inizia con `58aec3b0` e termina con `cd07ba`; è coinciso presso i critici Claude e DeepSeek).
13. Catene esatte di SPRT e CUSUM su griglie finite, compreso il cambiamento di comportamento dopo una buona storia.
14. Tabelle delle trappole `(1 − g·θ·d)^m` per i livelli `10⁻³`, `10⁻⁹`, `2⁻⁸⁰`.

### 7.2. Solo con esperimenti

L'esperimento D5 autorizza il lavoro con il Qwen3.5-4B intero nella misura di O1–O5 del suo protocollo. **Tutto il resto — solo con un'autorizzazione separata del proprietario.**

1. Nell'ambito di D5: nuclei veloci bit per bit uguali (O3, O4) — l'unica via per avvicinarsi al 5%; la quota di verifica sui dispositivi dei pagatori e con pacchetti 1, 8, 32; O5 — la qualità su 320 compiti.
2. Fuori da D5: decodifica speculativa esatta — la distribuzione della lunghezza del prefisso coincidente di Q8_0 e del profilo esatto sulle risposte lunghe.
3. Fuori da D5: la frequenza delle divergenze silenziose `P_f` con un lungo funzionamento su dispositivi volontari — prima di qualsiasi modifica di D16.
4. Fuori da D5: tempo e memoria della verifica in un solo passaggio sul processore di un portatile e di un telefono.
5. Coincidenza dei bit su input limite (traboccamento, pareggi, fine anticipata della risposta) e su nuovi driver; su RX 580 un lungo passaggio su una risposta pronta veniva interrotto dal driver [misurato].
6. Fuori da D5: O9 (energia), O6 (rumore del miglioramento LoRA), O7 (prezzo della prova di un blocco), l'addestramento intero — presupposto di qualsiasi schema di verifica del passo.
7. Fuori da D5, facoltativamente: quanto le contraffazioni economiche sono distinguibili per indizi. Questo non dà una garanzia con nessun esito, ma precisa solo il tetto della sezione 2.1.

## 8. Disaccordi irrisolti e riferimenti dubbi

### 8.1. Disaccordi

1. **La verifica a campione da parte del pagatore soddisfa il D1 letterale.** claude1, claude2, i critici Claude e DeepSeek — sì per il denaro, no per il danno. ds1 e ds2 — serve la verifica completa (i critici ritengono che non abbiano notato la verifica da parte del pagatore con frequenza basata sulla somma bloccata). gpt1, gpt2 e il critico ChatGPT — verifica completa di ogni risposta, e il pagamento degli scelti — solo con un contratto separato per i gruppi. La decisione se basti il guadagno atteso nella prima frase di R4 è del proprietario.
2. **`R/(R + H_lock)` o `R/H`.** Il primo è esatto per il denaro, il secondo dà margine e un numero atteso finito di contraffazioni fino alla cattura; la differenza di prezzo è di circa due volte con una somma piccola.
3. **Se pagare il non verificato** (`α = R` o un G(α) graduale in claude2) **o solo lo scelto** (`α = 0`, lotteria B). Dipende dalla modifica di D2, D11, D21 e dall'irregolarità non misurata del reddito.
4. **Faro o moneta segreta.** claude2 — faro comune (D20); claude1 e i critici Claude e DeepSeek — moneta segreta del pagatore, il faro serve solo con `α < R` e per le controversie di nodi terzi. Critico ChatGPT: la moneta segreta va bene per la verifica personale, ma non può disporre del premio comune; scegliendo il comodo tra due esiti indipendenti del faro, la cattura scende da `p` a `p²`.
5. **D16** — sezione 6, domanda 4.
6. **Il confine del danno** — nessuno schema ha retto l'autopagamento e le nuove chiavi.
7. **Addestramento** — audit «uno su N» (claude1), verifica da parte di ogni nodo completo con rollback del ramo (claude2), D18 o ripetizione completa (ds1, ds2, gpt1, gpt2); nessuno schema soddisfa D7 con `q = 1`.
8. **Le grandezze dell'enumerazione di claude1** (+1,73R con `κ = 0,9`): riprodotte dal critico Claude, non riprodotte dal critico DeepSeek (+0,085R nel modello più vicino); il segno è uguale in entrambi.
9. **Decodifica speculativa:** 1,15–1,38 (claude1) contro circa 0,78 del tempo di un token esatto (claude2); entrambi non misurati.
10. **Trappole:** ds2 calcola il numero necessario di trappole, claude1 e claude2 dimostrano che in una rete pubblica la trappola coincide con la verifica da parte del pagatore. Le conclusioni sono compatibili.

### 8.2. Riferimenti bibliografici segnalati dai critici come dubbi

Tutti i riferimenti sono dati a memoria, senza verifica dei testi.

- SybilGuard e SybilRank sotto un comune «Yu e coautori» (ds1): secondo la memoria dei critici, SybilGuard e SybilLimit — Yu e coautori (2006, 2008), SybilRank — Cao e coautori (2012); l'anno di SybilRank è di per sé segnalato dal critico Claude come incerto.
- «Proof of Sampling (2024)» e «Verde (Gensyn, 2025)» (claude1, claude2) — i lavori stessi scrivono «non sono sicuro»; il funzionamento del meccanismo non è confermato.
- Peer Truth Serum come lavoro di Witkowski e Parkes (2012) (ds2): il critico Claude lo ritiene dubbio (secondo la sua memoria loro hanno la «BTS robusta», e il nome appartiene a Radanovic e Faltings), il critico DeepSeek — corretto. Disaccordo.
- DMI come lavoro di Kong e Schoenebeck (2019) (ds1, ds2): dubbio secondo la memoria dei critici Claude e ChatGPT (DMI è un lavoro di Kong intorno al 2020); il critico DeepSeek ritiene l'attribuzione corretta.
- «Attacchi di autopredizione alla BTS di Radanovic e Faltings» (ds1) — dubbio.
- «Gao, Wright e Layton-Brown (2016)» sulla superiorità della verifica a campione rispetto al peer prediction (claude2) — l'anno non è confermato (critico DeepSeek), l'incondizionatezza della conclusione è dubbia (critico ChatGPT).
- Kreps e Wilson (1982) come fondamento di «la reputazione funziona solo con un orizzonte lungo» (claude1) — dubbio (critico ChatGPT).
- DetectGPT come giustificazione della soglia di perplessità del modello piccolo (ds1) — scorretto: studia un'altra proprietà (critico ChatGPT).
- La formula generale del passaggio `(1 − f)^s` come proprietà di BOINC, TrueBit, opML (ds1, ds2) — non segue dai loro protocolli.
- I riferimenti di ds1 e ds2 a «0,3–0,7% / 0,33–0,66% dei token dell'esame» e «circa 2,4 ore per candidato» non sono stati trovati nei documenti di input.

## 9. Chi ha fatto che cosa

Il consiglio dei modelli ha lavorato sui materiali del progetto, senza accesso alla rete e senza esperimenti.

- **Sei lavori indipendenti:** due lavori ChatGPT (gpt1, gpt2), due lavori DeepSeek (ds1, ds2), due lavori Claude (claude1, claude2). Ognuno ha analizzato le sette direzioni dell'incarico, ne ha aggiunte di proprie, le ha confrontate con le decisioni D1, D6, D7 e ha proposto strategie con prezzo e rischio residuo. Brevi programmi aritmetici e piccole enumerazioni sono stati eseguiti da claude1 (enumerazione di strategie contro la regola di frequenza), claude2 (griglia di frazioni esatte), gpt1 e gpt2 (gpt2 ha allegato uno script di controllo con hash).
- **Tre critiche:** una da ChatGPT, DeepSeek e Claude. Ogni critico ha letto tutti e sei i lavori, ha cercato errori e controesempi, ha ricalcolato i numeri chiave. I critici Claude e DeepSeek hanno ripetuto lo script di controllo di gpt2, l'hash è coinciso; il critico Claude ha ripetuto l'enumerazione di claude1, il critico DeepSeek non ne ha riprodotto le grandezze.
- **Sintesi:** questo documento è stato compilato da Claude sulla base dei lavori e delle critiche. Non sono state aggiunte nuove valutazioni e nuovi numeri oltre ai lavori, alle critiche e alle misurazioni D5; dove i critici sono divergenti, è indicato.
