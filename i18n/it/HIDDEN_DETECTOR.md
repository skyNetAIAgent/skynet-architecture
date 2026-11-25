<!-- translation of docs/HIDDEN_DETECTOR.md, source sha256: a695d12d2972002373f749a618c390c3e937e344afd1e816d8c46319fe1127cb -->

# Il rilevatore nascosto e mutevole: che cosa dà il segreto delle regole

[English](../../docs/HIDDEN_DETECTOR.en.md) · [中文](../zh/HIDDEN_DETECTOR.md) · [Español](../es/HIDDEN_DETECTOR.md) · [Français](../fr/HIDDEN_DETECTOR.md) · [Deutsch](../de/HIDDEN_DETECTOR.md) · **Italiano** · [Русский](../../docs/HIDDEN_DETECTOR.md) · [Português](../pt/HIDDEN_DETECTOR.md) · [العربية](../ar/HIDDEN_DETECTOR.md)

Stato al 25 novembre 2026. Esito del sesto consiglio dei modelli.

## 1. Domanda e sintesi breve

Il proprietario del progetto ha chiesto testualmente:

> «Con regole aperte (D4) l'imbroglione conosce il rilevatore e contraffà proprio dove esso è
> tranquillo. E se si nascondesse il rilevatore? Per esempio, la rete genererebbe a tempi casuali in modo casuale
> nuove regole di verifica dell'onestà e gli agenti verificherebbero secondo esse. Data l'architettura
> distribuita e aperta della rete skynet, nessuno deve conoscere le regole di verifica e queste devono
> essere cifrate, la chiave del cifrario cambiata. Pensate con il consiglio dei modelli in questa direzione. In precedenza io
> ho sollevato la questione dell'uso della blockchain — esiste una variante per fare un rilevatore dinamico sulla
> base della blockchain? Forse oltre alla blockchain esistono altre tecnologie o algoritmi?»

**Stato del documento.** Questo è un ragionamento e un calcolo, non una misurazione. Durante il lavoro del consiglio non c'era
rete, non sono stati condotti esperimenti; i lavori scientifici sono citati a memoria e non sono stati verificati. Le misurazioni sono prese solo
dagli esiti dell'esperienza D5 al 25 novembre ([EXPERIMENT_D5](EXPERIMENT_D5.md), sezione 7) e dalla precedente
sintesi [STRATEGY_SEARCH](STRATEGY_SEARCH.md). Restano decisioni accettate del progetto solo D1–D25
([ROADMAP](ROADMAP.md)); tutto ciò che sotto è chiamato «raccomandazione» il proprietario deve accettarlo o
respingere esplicitamente. Marcature: [misurato] — misurato in D5; [calcolo] — segue da una formula con parametri nominati;
[ipotesi] — grandezza presa per la stima e non misurata.

Notazioni che ricorrono sotto: `R` — pagamento di un compito; `H_lock` — somma non maturata
dell'esecutore che si brucia in caso di contraffazione dimostrata; `c_f` — costi della contraffazione; `p` —
probabilità di verifica completa del compito; `ρ` — tempo di verifica della risposta pronta in un passaggio,
diviso per il tempo di generazione; `γ` — di quante volte il profilo intero esatto è più lento della normale
generazione llama.cpp Q8_0; `q` — quota di collusione; `n_w` — numero di compiti della chiave per finestra di maturazione.

**Sintesi breve.**

1. **Un rilevatore nascosto non dà più di una verifica aperta con casualità segreta dello stesso prezzo.**
   Se l'imbroglione conosce la legge secondo cui si scelgono le regole (e secondo D4 il codice dell'agente è aperto, quindi
   egli la conosce), la probabilità di catturare qualsiasi sua contraffazione con una regola nascosta è uguale
   alla probabilità di cattura con il programma aperto «dopo la fissazione della risposta lanciare una moneta e applicare
   la regola uscita». Questo è stato ottenuto indipendentemente da tutti gli undici lavori, tutti e quattro i critici l'hanno
   confermato. Dunque la segretezza non permette di abbassare la frequenza di verifica sotto la precedente soglia
   `R/(R + H_lock)`.
2. **Una regola che vive più a lungo di un compito è peggiore di una moneta fresca.** L'imbroglione impara dai propri
   esiti («catturato / non catturato»), prova il rilevatore con nuove chiavi gratuite, apprende la regola tramite
   qualsiasi complice a cui è stato dato di applicarla. Anche senza alcuna fuga, una regola comune per l'epoca è
   più pericolosa: nell'esempio di ChatGPT un'ondata di dieci contraffazioni dà `+8,1R` contro `−2,38R` con
   monete indipendenti [calcolo]. «Cambiare le regole a tempi casuali» è perciò peggiore del cambiare
   la scelta a ogni compito.
3. **È utile esattamente una forma di segretezza:** il segreto della scelta casuale *prima* che l'esecutore
   abbia fissato irrevocabilmente la risposta, e il segreto del *ruolo* — se questo pagatore verifica e chi
   è nominato verificatore. Le regole, la famiglia di verifiche e la legge di scelta restano aperte. Questa
   forma è già nella strategia del consiglio precedente («moneta segreta del pagatore»).
4. **Che cosa prendere dalla blockchain e dalla crittografia.** La blockchain è un registro di fissazioni, ordine, rivelazioni e
   bruciatura delle somme; segreti non ce ne sono e non possono esserci. Un faro esterno a soglia di casualità e
   il ritardo VDF dal blocco finale sono fonti di casualità per campioni comuni secondo D20 (audit
   dell'addestramento, esame, nomina dei verificatori), mescolate con hash. VRF e impegno a un sale prima della
   fissazione — dove l'esito della moneta influenza denaro altrui. «Rilevatore dinamico sulla blockchain»
   nella forma corretta è **un generatore aperto di regole nel nucleo più casualità fresca dopo la
   fissazione**, non regole cifrate.
5. **Che cosa respingere come fondamento della garanzia.** Conservazione a soglia di regole segrete da parte dei partecipanti
   (si rivela o si blocca con la collusione, con `q = 1` non c'è protezione — violazione di D7),
   ambienti di esecuzione attendibili TEE (fiducia nel produttore, sulle schede dell'esperienza D5 non ci sono),
   cifratura omomorfica FHE (secondo la stima dei critici da 19 ore a 15 giorni di calcolo per una
   risposta), calcolo multipartito MPC (centinaia di megabyte e più di traffico per token e di nuovo
   dipendenza da `q`), offuscamento indistinguibile iO (impraticabile e comunque lascia all'imbroglione
   una «prova di esecuzione»), cifratura funzionale e PIR (risolvono altri problemi). Trappole, soglie segrete e
   statistica sono ammesse solo come segnale per una verifica *aggiuntiva*.
6. **È stato trovato un errore nelle tabelle precedenti.** In STRATEGY_SEARCH 5.3 e nella maggior parte dei lavori di questo
   consiglio la cella «pagatore pigro, l'esecutore lo distingue» × «novizio» contiene 0. Corretto —
   **fino a `+R`**: la regola «il novizio si verifica sempre» la esegue il programma del pagatore, e il pigro
   pagatore non la esegue. Peggio ancora, le nuove chiavi permettono di scoprire gratuitamente quale
   pagatore è pigro. Protegge da ciò solo la non collegabilità dei pagatori tra le richieste,
   e va ancora costruita.
7. **Il consiglio non propone nuove decisioni sulla garanzia.** Si propongono un chiarimento di D4 («il nucleo accetta
   casualità futura, ma non un segreto di lunga durata») e un chiarimento di D20 («le fonti si mescolano con hash,
   non con la scelta; il faro — per decisioni comuni, non per il denaro del pagatore»). Il prezzo della verifica non
   cambia per la segretezza: la voce principale è ancora il rallentamento del profilo esatto `γ`
   (+50…+82% rispetto a Q8_0 con pacchetto 1 [misurato γ, calcolo]), e non la verifica stessa.

---

## 2. Perché il segreto delle regole non aiuta: affermazioni e controesempi

### 2.1. Una regola nascosta è uguale a una regola aperta con moneta segreta

**Modello.** Il difensore sceglie la regola di verifica `r` dalla distribuzione `D`. La regola `r` cattura
la contraffazione `x` con probabilità `π_r(x)`. L'imbroglione conosce la distribuzione `D` (secondo D4 il generatore di regole è
parte del nucleo aperto), ma non conosce la `r` uscita, e sceglie la contraffazione prima che `r` esca.

**Affermazione 1 (equivalenza).** La probabilità di cattura della contraffazione `x` è uguale a
`π̄(x) = E_{r~D}[π_r(x)]`, il prezzo medio della verifica è uguale al prezzo medio delle regole. Il programma aperto
«dopo la fissazione irrevocabile della risposta prendere casualità fresca, scegliere `r` secondo la legge `D`
e applicarla» dà per **ogni** contraffazione la stessa probabilità di cattura e lo stesso prezzo. Dunque,
la segretezza dell'implementazione aggiunge alla protezione zero.

La dimostrazione è una media su `r`: gli esiti dei due esperimenti coincidono per ogni valore della
casualità. L'hanno condotta indipendentemente gpt1, gpt2, ds1, ds2, claude1, claude2, mm1–mm5; i critici
ChatGPT, DeepSeek, Claude e MiniMax l'hanno confermata. È lo stesso risultato del confine del consiglio
precedente `E_F[π] − E_P[π] ≤ TV(F, P)` ([STRATEGY_SEARCH](STRATEGY_SEARCH.md), sezione 2.1): la grandezza
`π̄` è una normale funzione delle osservazioni con valori da 0 a 1, e il segreto non la cambia.

**Affermazione 2 (le informazioni sul segreto nuocciono solo al difensore).** Se l'imbroglione prima della contraffazione riceve
qualsiasi segnale `Z` sulla regola uscita — da una controversia passata, da una prova, tramite una quota di chiave, da una fuga
dell'enclave — il suo miglior risultato non peggiora: `E_Z[min_x E[π_r(x) | Z]] ≤ min_x π̄(x)`. Egli può sempre
ignorare il segnale (claude1, claude2; confermato dai critici).

Il critico ChatGPT ha precisato il confine di questa affermazione: la disuguaglianza è non stretta. Se tutte le regole hanno
la stessa contraffazione «peggiore per il difensore», rivelare la regola può non cambiare nulla. La frase di
claude1 «qualsiasi fuga peggiora strettamente» è quindi errata; è vero «non migliora mai».

**In che cosa differisce dalla randomizzazione.** Diversi lavori (ds1, ds2, mm2) hanno scritto la conseguenza come
«un rilevatore nascosto è pari a verificare tutta la risposta con probabilità `p`». Questo è impreciso. L'equivalente
di un rilevatore nascosto è *una miscela delle stesse regole*. Una miscela di verifiche parziali a volte è più forte di una verifica
completa allo stesso prezzo, ma il guadagno lo dà la randomizzazione, non il segreto, e si conserva con l'algoritmo
aperto:

- **Controesempio di gpt1.** Il risultato ha tre parti verificabili indipendentemente dello stesso prezzo, e per la struttura
  del compito qualsiasi contraffazione ammissibile ne guasta almeno due. La verifica di una parte casuale per un terzo
  del prezzo completo cattura non meno di 2/3 delle contraffazioni; il ricalcolo completo con probabilità 1/3 — solo 1/3.
- **Variante di gpt2.** Tre test a metà del prezzo del ricalcolo completo, ciascuno cattura due classi di errore
  su tre: la miscela cattura 2/3, il ricalcolo completo di metà dei compiti — 1/2. Se si aggiunge una quarta classe,
  che nessun test cattura, la garanzia della miscela scende a 0.

Per Qwen una tale copertura delle classi di errore non è dimostrata: una sola posizione errata della risposta è già una
contraffazione, e per essa qualsiasi verifica parziale cattura non più della propria quota. Perciò il guadagno pratico
della miscela oggi è nullo (critici Claude e ChatGPT). L'affermazione di mm2 «la miscela è sempre più cara del tipo decisivo» è errata
in generale; nella sua formula c'è inoltre un fattore in più (i numeri 0,2111 / 0,22
/ 0,2333 sono calcolati con la formula corretta, è scritta quella errata — critici Claude e DeepSeek).

**Dove il segreto non si riduce alla moneta.** È un'etichetta privata del difensore, legata alla risposta corretta:
il riferimento della trappola, che conosce solo il pagatore (gpt1, gpt2). Non si può sostituire con un bit casuale.
Ma, come mostrato nella sezione 3, costa non meno di una generazione e perciò non rende la verifica più
economica.

**Contro una regola «fissa» il nascosto è davvero migliore.** claude1 porta un esempio: se la
regola aperta guarda sempre le posizioni 1–8, la contraffazione nella posizione 9 non si cattura mai. Ma lo stesso
guadagno lo dà la regola aperta «scegliere 8 posizioni uniformemente dopo la fissazione» (mm3, teorema 2:
una posizione fresca cattura `e/N` contraffazioni, dove `e` è il numero di posizioni guastate su `N`, indipendentemente dal fatto che
l'imbroglione conosca la regola). Il critico MiniMax ha chiamato questo l'errore principale del round: molti lavori
confrontavano il rilevatore nascosto con una regola aperta fissa e attribuivano al segreto un guadagno
che appartiene alla casualità.

### 2.2. Apprendimento dell'imbroglione dagli esiti e prove con nuove chiavi

Un segreto che si usa più di una volta si impara. Per questo all'avversario non serve
conoscere la regola per intero — basta trovare un posto sicuro.

- **Due posizioni su dieci (claude1).** La regola nascosta verifica 2 posizioni su 10, la cattura di una contraffazione
  a una posizione — 1/5. Dopo che una controversia ha rivelato una posizione verificabile, la cattura scende a 1/9, dopo
  la rivelazione della seconda — a 0. Se la regola si rivela alla prima controversia, il numero atteso di catturate su 100
  contraffazioni è `1 − 0,8¹⁰⁰ = 0,9999999998`, cioè praticamente una, mentre una moneta fresca catturerebbe in media 20 [calcolo, confermato
  dai critici]. Il critico ChatGPT ha notato che questo è vero per un ordine concreto
  di prove e per la rivelazione completa alla prima cattura; in generale una controversia rivela almeno
  la posizione verificata, ma non necessariamente tutto l'insieme.
- **Otto posizioni su mille (ds2).** Con un sottoinsieme nascosto costante di 8 posizioni su 1000,
  la prima contraffazione a una posizione passa con probabilità 0,992, come con un campione pubblico fresco
  della stessa quota. La differenza è che con un sottoinsieme nascosto costante la posizione passata
  resta sicura per sempre. Il numero di ds2 «≈ 2718 tentativi per ricostruire tutto l'insieme»
  è calcolato con un modello errato (con reinserimento); senza reinserimento servono circa 890 tentativi, e soprattutto
  all'avversario basta una posizione sicura (critici Claude, DeepSeek e ChatGPT).
- **Regola dell'epoca e chiave matura (claude2).** Una regola deterministica per un'epoca di 100 compiti,
  `p = 1%`, `H_lock = 99R`: l'imbroglione che con una prova ha trovato una zona sicura ottiene circa
  `0,99·100R − 0,01·99R = 98,01R` per epoca contro `≤ 0` con una moneta fresca [calcolo, confermato].
- **Bit comune dell'epoca (gpt2).** `R = 1`, bloccato `9R`, dieci contraffazioni di un'ondata, la prima contraffazione dimostrata
  annulla l'ondata e `9R`, frequenza di verifica di una singola richiesta 1/10. Se un bit nascosto
  dell'epoca decide «verificare tutto» o «saltare tutto», il guadagno dell'ondata è `0,9·10R − 0,1·9R = +8,1R` —
  violazione di D1 **prima di qualsiasi fuga**. Con dieci monete indipendenti agli stessi costi
  `(0,9¹⁰·10 − (1 − 0,9¹⁰)·9)R = −2,3751096381R` [calcolo, ripetuto da tutti i critici].
  Analogamente nel critico ChatGPT: con `R = 1`, `H = 4`, `p = 0,2` e dieci contraffazioni una moneta comune
  per tutta l'ondata dà `+7,2R` anche con l'annullamento di tutta l'ondata.

**Chiavi Sybil.** Le nuove chiavi sono gratuite. Una chiave con conto vuoto non perde nulla alla cattura, quindi
le prove del rilevatore con essa non costano quasi nulla. La protezione regge solo dove il novizio
viene davvero verificato sempre (`p = 1`). Il critico ChatGPT ha precisato che dalla gratuità delle chiavi non
segue che l'adattamento sia istantaneo: ogni esito informativo richiede un compito pagato e
tempo, e con un riscontro rumoroso — diversi tentativi. La conclusione non cambia: un segreto
che vive a lungo prima o poi si impara, e una moneta fresca non insegna nulla, perché il lancio successivo è indipendente dai
precedenti.

**Conclusione.** La scelta va fatta di nuovo per ogni compito, non secondo un calendario. Proprio per questo
«la rete a tempi casuali genera nuove regole» è peggiore di «una moneta fresca a ogni compito»,
che si rigenera da sola e gratuitamente (ds1).

### 2.3. La regola trapela attraverso coloro che la applicano

«Una regola che nessuno conosce e che tutti eseguono» in una rete aperta è impossibile. Il nodo che
applica la regola la conosce al momento dell'applicazione: codice e chiavi stanno nella memoria della macchina, e il proprietario
della macchina secondo il modello dell'avversario può leggerli ([THREAT_MODEL](THREAT_MODEL.md), sezione 1.3).
claude1 ha formulato l'elenco completo dei portatori del segreto:

1. la regola non c'è ancora — sarà derivata da casualità futura (faro, VDF);
2. la regola viene eseguita in hardware che il proprietario non può aprire (TEE) — allora la fiducia
   si trasferisce al produttore, e R4 chiama questo un'ipotesi;
3. la regola è cifrata in modo che la si possa eseguire senza conoscerla (iO, FHE, MPC) — vedi sezione 3;
4. la regola la conosce un comitato di partecipanti — allora la rivela o la blocca la collusione.

Il critico ChatGPT ha completato l'elenco: MPC sulle quote e il calcolo di uno schema aperto su un
parametro cifrato permettono all'operatore di non vedere affatto il risultato. Questo non cambia la conclusione, perché
tali schemi si reggono di nuovo sulla quota di partecipanti onesti o sul detentore della chiave.

**Una chiave a soglia protegge la conservazione, ma non l'applicazione** (claude2, l'argomento più forte del consiglio contro
una regola segreta presso il comitato). Anche se la chiave è divisa in modo affidabile, la regola dell'epoca decifrata
la esegue un nodo concreto. Con `m` applicazioni indipendenti la probabilità che almeno un
nodo applicante sia della coalizione è `1 − (1 − q)^m`: su 10 applicazioni è 0,65 / 0,97 / 0,999 con
`q` = 0,1 / 0,3 / 0,5. La probabilità che la regola dell'epoca *non* sia appresa dalla coalizione in 100 applicazioni con
`q = 0,1` è `0,9¹⁰⁰ ≈ 2,7·10⁻⁵` [calcolo, confermato dai critici].

**Nascondere al verificatore è privo di senso** (claude2, corollario 4.2). Un verificatore colluso può
non verificare affatto e dire «pulito»; l'onesto non ha nulla da nascondere. L'unico da cui bisogna
nascondere la decisione è l'esecutore prima della fissazione della risposta. claude2 ha aggiunto il teorema 4: se il verificatore non
deve sapere quali posizioni verifica, deve «toccare» tutte le posizioni, e il risparmio del
campionamento scompare. Il critico ChatGPT ha notato che questa conclusione è vera in un modello speciale (un server,
nessuna preelaborazione), e con altri modelli di accesso alla memoria può cambiare;
il critico Claude — che il teorema confuta una variante che nessuno difendeva.

**Un segreto nascosto non dà un verdetto verificabile.** mm2 ha notato che l'affermazione «esiste una regola segreta
che ha accettato il risultato» è sempre vera per la regola «accettare tutto». I critici Claude e
ChatGPT hanno precisato: una prova a conoscenza zero può attestare un'affermazione sostanziale «la regola è derivata da un impegno registrato prima della fissazione, e ha accettato
il risultato». Ma una tale prova richiede una relazione aperta nel nucleo, cioè ci riporta
al generatore aperto, e il suo prezzo per Qwen non è calcolato.

### 2.4. Chiave a soglia con quota di collusione q

Sia la chiave divisa tra `n` detentori, per decifrare servono `t` quote. Allora la coalizione apprende
il segreto in anticipo se ha `t` o più posti, e può fermare il lavoro se ha `n − t + 1`
o più posti. Se i posti sono scelti indipendentemente e ciascuno con probabilità `q` appartiene alla coalizione,
sono code binomiali. Tabella del critico Claude, verificata dai critici ChatGPT e DeepSeek;
in ogni cella «rivelazione / arresto» [calcolo]:

| `n`, `t` | `q = 0,1` | `q = 0,3` | `q = 0,5` | `q = 1` |
|---|---|---|---|---|
| 5, 3 | 0,856% / 0,856% | 16,3% / 16,3% | 50% / 50% | 1 / 1 |
| 7, 5 | 0,0177% / 2,57% | 2,88% / 35,3% | 22,7% / 77,3% | 1 / 1 |
| 16, 11 | 2,7·10⁻⁸ / 0,33% | 0,157% / 34,0% | 10,5% / 89,5% | 1 / 1 |
| 30, 16 | 3,66·10⁻⁹ / 3,56·10⁻⁸ | 0,637% / 1,69% | 42,8% / 57,2% | 1 / 1 |
| 64, 43 | 4,75·10⁻²⁸ / 1,20·10⁻⁷ | 9,43·10⁻¹⁰ / 26,2% | 0,41% / 99,6% | 1 / 1 |
| 100, 51 | 6,3·10⁻²⁵ / 5,8·10⁻²⁴ | 9,0·10⁻⁶ / 2,2·10⁻⁵ | 46,0% / 54,0% | 1 / 1 |
| 100, 67 | 9,6·10⁻⁴³ / 7,0·10⁻¹¹ | 2,7·10⁻¹⁴ / 22,1% | 0,044% / ≈1 | 1 / 1 |

Che cosa ne segue:

1. **Nessuna riga dà protezione con `q = 1`.** D7 richiede una verifica indipendente dalla quota di
   collusione, perciò il segreto presso il comitato non soddisfa D7 con nessuna soglia.
2. **Una soglia alta custodisce bene il segreto, ma si blocca facilmente.** Riga 16/11: con `q = 0,3`
   la rivelazione è 0,157%, ma con probabilità 34% la coalizione ferma l'emissione semplicemente non inviando
   le quote.
3. **Le epoche si sommano.** Con probabilità di rivelazione 0,856% per epoca (3 su 5, `q = 0,1`), su
   30 epoche indipendenti almeno una rivelazione avverrà con probabilità 22,7% (gpt1) [calcolo].
4. **La tabella è ottimistica.** La scelta indipendente dei posti è un'ipotesi. Si rompe se i detentori
   sono scelti per peso, e il peso si può accumulare con richieste verificate autopagate; se per un modello raro la quota di collusione è superiore alla media; con la corruzione dopo la nomina; con proprietari comuni dei posti.
   In [THREAT_MODEL](THREAT_MODEL.md) (sezione 1.7) c'è già un esempio: il 42,1% del peso totale dà
   `q_eff = 88,9%` tra gli ammessi al compito (su questo ha richiamato l'attenzione il critico MiniMax).
5. **Errori nei lavori.** claude1 ha scritto la condizione «`q < min(t/n, 1 − t/n) ≤ 1/2`» come teorema; questo
   non è un teorema: con `t = n` il segreto regge finché nel comitato c'è almeno un onesto, e il blocco
   può avere un esito alternativo sicuro (critico Claude). mm4 ha confuso le soglie di rivelazione e di blocco;
   mm2 riteneva erroneamente che la decifratura a soglia richieda tutti i detentori; ds1 ha scritto in modo contraddittorio
   «si ricostruisce con `t + 1` quote». L'affermazione di mm3 «con `q ≥ t` la coalizione contraffà
   la regola» è vera solo dove il verdetto è una firma a soglia senza contenuto verificabile; se
   si decifra un crittogramma fissato in anticipo, la coalizione apprende la regola, ma non può sostituirla.

**Come leggere i requisiti R2/R3.** ds1, mm1, mm3 e mm4 hanno scritto che il requisito di ripristino dopo
un arresto completo «vieta in linea di principio» i segreti comuni. I critici Claude e ChatGPT considerano questo un eccesso:
le quote dei detentori possono sopravvivere all'arresto sui loro dischi; R2/R3 vietano di dipendere dall'indirizzo di un coordinatore vivo,
non dal ritorno di una parte dei partecipanti. Il confine esatto (claude2):
un segreto senza il quale non si può verificare il fondamento di una decisione **passata** è incompatibile con la verificabilità
dopo il riavvio. Dunque qualsiasi regola segreta deve rivelarsi non più tardi del pagamento, e il suo segreto
vive non più a lungo del segreto della moneta. La conclusione sull'inidoneità delle regole segrete è la stessa, il fondamento di ds1, mm1,
mm3 era esagerato.

### 2.5. Principio di Kerckhoffs, giochi di sicurezza, banche e CAPTCHA

**Kerckhoffs.** Il principio di Kerckhoffs (a memoria) ammette un algoritmo aperto con chiave chiusa.
In questo gioco la «chiave» chiusa deve essere l'implementazione imprevedibile prima della fissazione della chiamata
di verifica, non l'algoritmo. Il cambio di una chiave di lunga durata è utile dopo una compromissione, ma non cancella
ciò che l'imbroglione ha già appreso sulla funzione che quella chiave decifrava (critico ChatGPT).

**Giochi di sicurezza.** Il difensore con un budget limitato randomizza — è la classica teoria dei giochi
di Stackelberg e dei giochi di ispezione (a memoria). Ma lì la distribuzione del difensore è di solito considerata
nota all'attaccante, e tutto il vantaggio viene dalla casualità, non dal segreto della distribuzione. Il critico
DeepSeek ha corretto mm3: l'ignoranza della distribuzione da parte dell'imbroglione non può portare il suo guadagno sopra la migliore
risposta alla distribuzione vera, e secondo D4 egli quella distribuzione è comunque tenuto a conoscerla. Per la miscela
di test diversi gpt1 ha scritto un problema di programmazione lineare: massimizzare la probabilità di cattura minima rispetto alle
contraffazioni `min_f Σ w_j D(j,f)` con il budget `Σ w_j c_j ≤ B`.

**«Bersaglio mobile».** L'idea della moving target defense (a memoria) è preziosa quando all'osservatore
serve tempo per adattarsi a una nuova configurazione. In SkyNet il miglior «bersaglio mobile» è
una nuova configurazione a ogni compito, cioè una moneta fresca (mm4, mm5).

**Perché la segretezza funziona in banca e nei CAPTCHA, ma non in SkyNet.** I lavori e i critici sono concordi
sulle seguenti differenze (claude2, ds2, mm3, mm5, critico ChatGPT):

| | Antifrode bancario, CAPTCHA | SkyNet |
|---|---|---|
| Chi detiene il modello di verifica | Una sola organizzazione sul proprio server | Non c'è un centro; il codice dell'agente è aperto (D4) |
| Riscontro all'attaccante | Spesso non attribuibile, con ritardo | L'esito è visibile subito e legato al compito |
| Prezzo del tentativo | Apertura di un conto, documenti, limite dei tentativi | La chiave è gratuita (Sybil) |
| Sanzioni | Non monetarie: blocco, tribunale, informazioni esterne | Solo la bruciatura della somma non maturata (R5) |
| Scopo della protezione | Ridurre le perdite in media | Il guadagno atteso di qualsiasi coalizione non superiore a zero (D1) |
| Verificabilità della decisione | Non richiesta a terzi | Ogni nodo verifica da sé il fondamento |

La banca ha etichette private degli esiti, un prezzo per l'apertura del conto e un limite dei tentativi; il CAPTCHA —
un verificatore esterno. Sono informazioni aggiuntive e costi dell'attaccante. Con il cambio del file cifrato
delle regole essi non compaiono in SkyNet. ds2 e mm5 hanno chiamato esattamente l'essenza: dove la segretezza
funziona, il segreto è di fatto monouso, cioè è la stessa moneta.

**La premessa principale della domanda in SkyNet è in parte errata** (mm3). La verifica principale del progetto è il confronto
bit per bit con il ricalcolo esatto. Non ha «un posto dove il rilevatore è tranquillo»: la risposta onesta coincide
ovunque, la contraffazione diverge dove è contraffatta. «Zone silenziose» ci sono solo nei rilevatori statistici e nelle verifiche
parziali. I rilevatori statistici contro la contraffazione principale (la normale generazione Q8_0 invece del profilo
esatto) sono quasi inutili, e per le verifiche parziali aiuta la scelta fresca
dopo la fissazione.

---

## 3. Analisi delle tecnologie

I prezzi sotto sono [calcolo] su parametri nominati esplicitamente e [ipotesi] sulla velocità della crittografia a memoria;
nessuna di queste tecnologie è stata misurata nel progetto. Misure di base: `ρ = 0,10–0,40` con pacchetto 1
e `0,26–0,64` con pacchetto 8; `γ = 1,5–1,8` con pacchetto 1 e `2,5–2,8` con pacchetto 8 [misurato, O3 e O4].
Modello D5: 32 blocchi, dimensione nascosta 2560, MLP 9216, 24 blocchi Gated DeltaNet con stato
`32×128×128`, vocabolario 248 320, circa 4,2·10⁹ moltiplicazioni-addizioni per token.

| Tecnologia | Che cosa dà | Che cosa non dà | Prezzo [calcolo / ipotesi] | Verdetto |
|---|---|---|---|---|
| **Registro blockchain** | Ordine, fissazione definitiva della risposta (D24, 2–4 KB di crittogramma), impegni, rivelazioni, calcolo una tantum, bruciatura | Segretezza: tutto nel blocco lo vedono tutti. Casualità non manipolabile: il produttore del blocco può trattenere un blocco scomodo (H13) | Controversia pilota: 93 transazioni, 5,8–6,3 mln gas, con 1 gwei e 3000 $/ETH — 17,4–18,9 $, con 20 gwei — 348–378 $ (critico ChatGPT secondo THREAT_MODEL, H3) | **Prendere come registro** |
| **Smart contract come rilevatore** | Calcolo automatico su un fondamento già verificato | Né conservazione del segreto, né calcolo del modello | Ricalcolo di un token dentro il contratto: `4,2·10⁹ × 3 gas ≈ 1,26·10¹⁰ gas` ≈ 37 800 $ per token con 1 gwei e 3000 $/ETH (ds1, confermato). Critico Claude: sono circa 420 blocchi da 30 mln di gas (limite a memoria). Critico ChatGPT: una semplice operazione MUL a memoria costa 5 gas, quindi questo è uno scenario, non un limite inferiore rigoroso | **Respingere come rilevatore** |
| **Faro esterno a soglia** (classe drand, a memoria) | Casualità pubblica che nessuno conosce in anticipo, se è onesta la soglia del suo comitato | Segretezza: il round viene pubblicato per tutti. Una coalizione dentro il comitato del faro apprende il round prima o può non emetterlo | Centinaia di byte per round per lotto e l'attesa di un round (a memoria, 30 s nella catena principale e circa 3 s in una veloce) | **Prendere come una delle due fonti di D20** per i campioni comuni |
| **VDF dal blocco finale** | Un ritardo entro il quale il produttore del blocco non riesce a scegliere un blocco comodo | Entropia indipendente: un VDF dallo stesso blocco non è una seconda fonte indipendente (critico ChatGPT) | Lavoro sequenziale del calcolatore; verifica rapida | **Prendere come complemento al faro**, scrivere l'ipotesi sul vantaggio dell'hardware veloce |
| **Cifratura timelock tramite faro** | Rivelazione differita di riferimenti comuni, compiti d'esame | Segretezza oltre il round; eredita la soglia del faro | Come al faro | **Solo per la rivelazione differita di dati comuni**; non rivelare così i dati privati |
| **Puzzle con blocco temporale** (Rivest–Shamir–Wagner, a memoria) | Ritardo della rivelazione | Il creatore conosce subito la risposta; la moneta è più semplice | Lavoro sequenziale | **Respingere** |
| **VRF** | Un valore univoco e verificabile per una chiave e un input registrati in anticipo | Segretezza dal proprietario della chiave: egli calcola il valore quando vuole. La verifica della prova VRF rivela il valore (errore di mm4). Non dimostra il fatto del ricalcolo VRF | Una chiamata e centinaia di byte per risposta | **Prendere**: per la nomina dei verificatori (contro la corruzione dopo la nomina) e come moneta del pagatore dove dall'esito dipende un pagamento altrui; la chiave si registra per l'ordine prima della fissazione |
| **Commit–reveal** | Legare un sale a un solo ordine prima della fissazione della risposta | Protezione dal «rivelatore per ultimo», che può tacere | gpt2: 448 byte per schema | **Prendere in modo ristretto**: impegno prima della fissazione, senza diritto di scegliere l'esito |
| **Crittografia a soglia** (Shamir, DKG, decifratura a soglia) | Conservazione della chiave senza un solo detentore | Indipendenza da `q` (sezione 2.4); protezione nell'applicazione della regola (sezione 2.3) | DKG con `n = 7`, `t = 5`: `7·6·32 + 7·5·48 = 3024` byte di payload (gpt2), firma a soglia BLS — 288 byte; senza replica e lamentele | **Respingere per le regole segrete**; faro interno a soglia dei partecipanti — solo come una delle fonti, non l'unica |
| **TEE** (SGX, SEV, TDX, GPU protette) | Esecuzione di codice nascosto al proprietario della macchina, con fiducia nel produttore | Indipendenza dal produttore e dalla sua catena di attestazione; nel parco D5 non ci sono GPU protette (RTX 2060, RTX 4070 Laptop, RX 580) | Scenario del critico ChatGPT: verifica protetta 1,2 volte più lunga di quella aperta, `p = 0,1` — circa 3,20% del tempo di generazione con caricamento dei pesi; modello su CPU — circa 50–100 ms per token contro 15–50 ms su GPU (critico Claude) [ipotesi]. Critico MiniMax: il proprietario può usare l'enclave come oracolo, il segreto regge sul limite del numero di richieste | **Solo come modalità di privacy a scelta dell'utente**, non fondamento della garanzia |
| **FHE** | Calcolo su dati cifrati e, tramite uno schema universale, su un programma cifrato | Verifica della correttezza del calcolo; il risultato lo apre il detentore della chiave (di nuovo `q`). Lo schema approssimato CKKS non riproduce i bit del profilo v2 | 1,4·10⁷–2,6·10⁷ bootstrap per token, con 10⁴–10⁵ bootstrap al secondo [ipotesi] — 140–2600 s per token, da 19 ore a 15 giorni per una risposta di 500 token; fattore rispetto alla verifica aperta `Φ ≈ 3·10³…2·10⁵` (claude2, critici Claude, ChatGPT, MiniMax). Aggiunta `p·ρ·Φ` con `n_w = 300`: da 2,1 a 139 generazioni per risposta | **Respingere per la verifica**; studiare solo per la privacy |
| **MPC** | Calcolo senza raccogliere il segreto in un solo posto | Indipendenza da `q`: la protezione regge sulla maggioranza onesta o su «almeno un onesto» con il diritto di far fallire il lavoro; con `q = 1` non c'è protezione | Per nascondere la *scelta* della verifica bisogna elaborare tutto — `1/p` = 31 / 303 / 4329 volte più caro della moneta con `n_w` = 30 / 300 / 4320 (critico Claude). Nascondere la *richiesta*: critico Claude — dal limite inferiore di 151 MB per token a 0,15–1 GB, 10–67 minuti per risposta a 1 Gbit/s; critico ChatGPT — 448 MB per posizione, 224 GB per 500 posizioni; critico MiniMax — fino a 180 TB per risposta (le stime divergono di ordini di grandezza, vedi sezione 7) | **Respingere per la verifica** |
| **iO** (offuscamento indistinguibile) | In teoria — esecuzione di un programma senza rivelarne la struttura | Non esiste un'implementazione pratica per il modello; anche un iO ideale lascia all'imbroglione una «prova di esecuzione» della propria contraffazione attraverso il rilevatore | Non valutato | **Respingere** |
| **Offuscamento di funzioni puntuali** | Verifica «coincide con il riferimento» senza rivelare il riferimento | Protezione con uno spazio ridotto di risposte: enumerazione; è la stessa trappola | Hash | Solo come parte della trappola |
| **Cifratura funzionale** | Ottenimento del valore di una funzione da parte del proprietario della chiave funzionale | Nascondere la funzione al proprietario della chiave (serve uno schema separato); serve un emittente delle chiavi | Non valutato | **Respingere** per questo compito |
| **PIR, ORAM** | Nascondere l'indice di lettura al server | Nascondere la regola; attestazione della provenienza dei dati | Critico ChatGPT: in PIR a due server su 10 000 record da 32 byte — una consultazione di circa 320 KB per server e la non collusione dei server | **Respingere** per questo compito |
| **Trappole** (richiesta con risposta nota in anticipo) | Nuove informazioni: un riferimento correlato alla verità | Un risparmio. Una trappola della stessa forza della moneta costa il lavoro dell'esecutore (≈ una generazione, pagata e inutile a tutti) e il riferimento (una generazione, se è fresco). La ripetizione di una vecchia richiesta la coalizione la riconosce | Rapporto del prezzo della trappola al prezzo della moneta `≥ 1/((1 − σ)ρ)`, dove `σ` è la probabilità di riconoscere la trappola: con `ρ = 0,21` — 5,3 / 6,8 / 9,5 / ∞ volte con `σ = q` = 0,1 / 0,3 / 0,5 / 1; con `ρ = 0,40` — 2,8 / 3,6 / 5,0 / ∞ (claude2). gpt2: trappole monouso sull'1% dei lavori con due generazioni aggiungono 2,02% | **Solo «segnale verso l'alto»**, senza ridurre la frequenza e senza la marcatura «verificato» |
| **Test statistici e soglie segrete** | Diagnosi di guasti di massa e errori di implementazione | Riduzione della frequenza: il confine `TV`; la soglia si impara con le prove | Poco | **Solo «segnale verso l'alto»** |
| **Verificatore nascosto, pagatori non collegabili** | Contro la corruzione dopo la nomina (nomina VRF) e contro la distinzione dei pagatori pigri (chiavi monouso del pagatore, claude1) | Indipendenza da `q` con la verifica da parte del comitato. Per un pagamento non collegabile serve un emittente o un altro meccanismo senza privilegi speciali — non costruito | Kilobyte e secondi (claude1), non valutato del tutto | **Prendere la nomina VRF; studiare i pagatori non collegabili** |
| **Prova ZK del calcolo** | L'unica via a un verdetto verificabile pubblicamente su un testimone chiuso | Non riguarda la segretezza delle regole; il prezzo per Qwen non è calcolato. Esperienza del pilota: esecuzione di zkVM 17 700 volte più lenta anche senza costruire la prova | Non valutato | **Studiare** separatamente |
| **«Moving target defense»** | Il valore del cambio di configurazione finché l'osservatore non si è adattato | In SkyNet il miglior cambio è a ogni compito, cioè una moneta fresca | Zero oltre la moneta | Ridurre alla moneta fresca |
| **Antifrode bancario, CAPTCHA** | Funzionano grazie a un server chiuso, al prezzo del tentativo, a sanzioni non monetarie e a chiamate monouso | Nulla di tutto ciò in SkyNet compare cambiando il file delle regole (sezione 2.5) | — | Non trasferire |

**Scoperta separata di claude1 (non sulla segretezza): la verifica di Freivalds.** Verificare la moltiplicazione di una matrice
per un vettore con una proiezione casuale può costare meno della moltiplicazione stessa: rapporto circa 1740 per token e
blocco [calcolo, confermato dal critico Claude]. Ma il critico ChatGPT ha notato che questo non è un'accelerazione della
risposta: bisogna trasmettere le attivazioni intermedie, tenere conto delle non linearità, degli arrotondamenti del profilo v2
e della freschezza del vettore per ogni richiesta. La conclusione di claude1 «il traffico delle attivazioni lo rende peggiore del passaggio
completo» è vera. Non si può dichiarare tutto Qwen verificato con una sola moltiplicazione.

---

## 4. Strategia raccomandata

### 4.1. Passi

Questa è la strategia del consiglio precedente («pagatore-ispettore»), precisata dai lavori e dai critici di questo
consiglio. Nessun passo richiede regole segrete. I passi 3, 4 e 9 dipendono da decisioni non ancora accettate
(sezione 5).

1. **Nucleo aperto.** Il generatore dell'istanza di verifica, la famiglia di verifiche ammissibili e la legge di scelta —
   parte aperta del nucleo con impronta fissata (D4). «Nuove regole a tempi casuali» sono
   nuovi valori di casualità, non nuovi algoritmi.
2. **Fissazione.** L'esecutore calcola nel profilo esatto v2 e con una sola scrittura con ricevuta mette nel registro
   il crittogramma della risposta (D24). Fino a quel momento non si fa alcuna scelta di verifica.
3. **Moneta segreta del pagatore.** Dopo la fissazione irrevocabile il programma del pagatore prende casualità fresca
   e decide se verificare la risposta, con probabilità
   `p = max(p_utente, (R − c_f)/(R + H_lock))`; con `c_f ≈ 0` è `R/(R + H_lock)`; con `H_lock = 0`
   (novizio) — sempre. Per il denaro del pagatore stesso il faro non serve.
4. **Moneta verificabile dove da essa dipende denaro altrui.** Se dall'esito della moneta dipende un
   pagamento altrui (lotteria con premio comune, controversie di nodi terzi), la moneta deve essere verificabile:
   VRF di una chiave registrata per l'ordine prima della fissazione, o impegno a un sale pubblicato
   prima della fissazione (gpt2, claude2). Un impegno fatto dopo la fissazione è privo di senso: il pagatore
   sceglie l'esito vedendo già la risposta (errore di mm5 nella proposta D28).
5. **Blocco della somma.** `H_lock` — solo la somma che matura dopo la scadenza della controversia; il termine di verifica `δ`
   è molto minore della finestra di maturazione `W` (in tempo attivo, D12). La prima contraffazione dimostrata
   brucia atomicamente tutta la somma non maturata della chiave, comprese le ricompense della stessa ondata; al danneggiato
   si restituisce non più del suo pagamento (candidato D26). Senza atomicità le formule non reggono un'ondata:
   10 contraffazioni parallele con `R = 1`, `H = 4`, `p = 0,2` danno `+4,4295R` invece di `−2,49676R`
   [calcolo].
6. **Marcature.** «Verificato» — solo una risposta completamente verificata prima di essere mostrata; tutto il resto —
   «non verificato» per impostazione predefinita. Un passo di addestramento non verificato non entra nel modello rilasciato (D6).
7. **Campioni comuni secondo D20.** Audit dell'addestramento, esame, lotteria con premio comune e nomina
   dei verificatori prendono casualità da non meno di due fonti indipendenti (faro esterno a soglia
   e VDF dal blocco finale), mescolate con hash; il round è fissato prima della fissazione e arriva dopo
   di essa. I nodi nominati apprendono la scelta tramite VRF.
8. **Segnali solo verso l'alto.** Trappole, anomalie, test statistici possono assegnare
   una verifica aggiuntiva, ma non riducono la frequenza e non danno la marcatura «verificato».
9. **Non collegabilità del pagatore** (elemento di ricerca). Chiavi monouso del pagatore e
   un ripetitore, perché l'esecutore non possa distinguere un pagatore verificatore da uno pigro (claude1).
   Finché il meccanismo non è costruito, nella tabella del rischio c'è la riga «i pigri sono distinguibili: fino a `+R`, anche
   per il novizio».
10. **Che cosa non c'è nel fondamento.** Regole segrete, chiavi di verifica di rete, comitati a soglia
    di custodi, TEE, FHE, MPC, iO.

### 4.2. Ruolo della blockchain e del faro: il «rilevatore dinamico sulla blockchain» nella forma corretta

La domanda del proprietario su un rilevatore dinamico sulla blockchain riceve questa risposta. La blockchain fa bene
ciò che è richiesto a un rilevatore, *tranne* il segreto:

- **fissa la risposta prima della scelta della verifica** — senza questo nessuna casualità aiuta;
- **conserva gli impegni** verso round e sali futuri, perché nessuno possa scegliere un esito comodo;
- **rende la scelta riproducibile**: qualsiasi nodo dopo il round calcola da sé che cosa è stato scelto,
  e verifica il fondamento della decisione anche dopo un arresto completo della rete;
- **esegue la bruciatura e il calcolo una tantum**.

La «dinamicità» non la dà la cifratura delle regole, ma il fatto che l'istanza di verifica ogni volta è derivata dalla
casualità che non esisteva ancora al momento della fissazione della risposta. Per la risposta privata questa
casualità è la moneta del pagatore; per le decisioni comuni — il faro secondo D20. I lavori l'hanno chiamato così:
«generatore aperto di regole nel nucleo più un'istanza della regola derivata dal faro, il cui round
è fissato prima della fissazione» (claude1); «le regole sono aperte, il segreto è solo nella scelta: chi, quando e quale
regola applicare» (mm4); «imprevedibile, non segreto» (mm3).

Due errori da evitare:

- **Il faro nella decisione monetaria del pagatore** (mm3, mm4). Il sorteggio pubblico dice *che cosa* verificare,
  ma verifica lo stesso pagatore; un pagatore pigro non verificherà nemmeno con un sorteggio pubblico, e sanzioni
  per la mancata verifica senza cauzione non ce ne sono (R5). Il sorteggio pubblico qui aggiunge solo un'ipotesi sull'onestà
  del faro e il ritardo del round (critici Claude, DeepSeek; mm2 e claude2 dicono lo stesso). mm3 e mm4
  non sono d'accordo (sezione 7).
- **Modalità di riserva «secondo l'ultimo valore disponibile»** (mm3). Se il faro non è disponibile e le verifiche
  dell'epoca vanno secondo un valore già noto, l'imbroglione sa in anticipo che non sarà verificato. Questo viola direttamente
  D20. Se il round non è disponibile, l'operazione contestata attende oppure la verifica è obbligatoria.

Un'altra precisazione: «scegliere quello comodo tra due bit indipendenti» riduce la probabilità della verifica obbligatoria
da `p` a `p²` (critico ChatGPT), mentre *mescolare* due fonti con un hash univoco è esattamente ciò che
richiede D20. L'aggiunta proposta da mm5 a D19 «moneta segreta e faro non si mescolano» confonde queste due
azioni e contraddirebbe D20 (critico Claude).

### 4.3. Prezzo

Il segreto delle regole non cambia il prezzo: non tocca né `ρ` né `γ`.

| `n_w` | `p = R/(R + H_lock)` | Verifica `p·ρ` con `ρ` = 0,10 / 0,21 / 0,40 | Totale rispetto a Q8_0, pacchetto 1 | Pacchetto 8 |
|---|---|---|---|---|
| 30 | 3,23% | 0,32% / 0,68% / 1,29% | +50,5…+82,3% | +152…+186% |
| 300 | 0,33% | 0,033% / 0,070% / 0,133% | +50,0…+80,2% | +150…+181% |
| 4320 | 0,023% | 0,0023% / 0,0049% / 0,0093% | +50,0…+80,0% | +150…+180% |

La tabella è [calcolo] sulla formula `γ(1 + pρ) − 1` e su `ρ`, `γ` misurati (critico MiniMax, verificato
dai critici DeepSeek e Claude). Il critico ChatGPT ricorda che i punti estremi dell'intervallo di `γ` e `ρ`
sono presi da schede diverse e non sono stati misurati in coppia; è un inviluppo, non una misurazione.

- **Novizio.** La prima risposta — verifica completa, 10–40% della sua generazione. Con un lavoro onesto strettamente sequenziale
  e una crescita di `H_lock` di `R` per compito, il numero atteso di verifiche complete nei primi
  30 compiti è `1 + 1/2 + … + 1/30 ≈ 3,995`; è 1,33% / 2,80% / 5,33% del lavoro della finestra con
  `ρ` = 0,10 / 0,21 / 0,40 (mm1, critico ChatGPT) [calcolo]. Con un avvio parallelo da conto vuoto
  la verifica completa tocca a ogni richiesta.
- **Riferimento del 5%.** Come sovrapprezzo per la verifica è raggiungibile: `p·ρ ≤ 0,05` richiede `p` non superiore a 50% /
  23,81% / 12,5%, cioè `H_lock/R ≥ ρ/0,05 − 1` = 1 / 3,2 / 7 (gpt1, gpt2) [calcolo]. Come «5% oltre
  la normale generazione» — no: il profilo esatto stesso costa +50…+80% [misurato γ]. L'unica via al 5% —
  nuclei bit per bit uguali più veloci.
- **Aggiunte della strategia.** 32–64 byte di impegno o centinaia di byte di VRF per risposta dove serve
  la verificabilità della moneta; il faro — centinaia di byte per round per lotto e il ritardo di un round solo per
  i campioni comuni (critico Claude) [calcolo].
- **Chi paga** (mm4, critico MiniMax). Il sovrapprezzo del profilo esatto `γ − 1` lo porta l'esecutore su ogni
  risposta pagata; la verifica `p·ρ` — il pagatore dal proprio anticipo. Lo spostamento della verifica sul
  pagatore elimina il ruolo «verificatore a cui si paga la verifica» da
  [CURRENT_DESIGN](CURRENT_DESIGN.md), sezione 1. Allora o il prezzo `R` cresce del 50–80%, oppure il margine
  dell'esecutore tende a zero. È una domanda separata del proprietario (sezione 5).
- **Lotteria B** (si pagano solo le risposte scelte e completamente verificate, variante di gpt1, gpt2
  e del critico ChatGPT). Con una quota di scelta del 5% le verifiche costano in media 0,5 / 1,05 / 2% del tempo della generazione
  esatta, ma il 95% delle risposte resta non verificato e non pagato; la varianza di un singolo pagamento
  `19R²`; la probabilità di non ricevere alcun pagamento su 20 richieste indipendenti `0,95²⁰ ≈ 35,85%`, su 30 —
  21,46% [calcolo].
- **Addestramento.** Il ricalcolo completo di un passo costa circa 100% del passo per ogni nodo verificatore; il riferimento del 20%
  non è mostrato da nessuno schema. Con `N = 1000` nodi riceventi, anche con costi nulli per il resto,
  per una verifica resta non più di 0,0002 del lavoro del passo (critico ChatGPT) [calcolo].

### 4.4. Rischio residuo

Guadagno atteso di una contraffazione rispetto all'inazione; «danno» — la quota di contraffazioni non rilevate
del danneggiatore, tutte con la marcatura «non verificato». La tabella è composta dalle tabelle dei critici Claude, DeepSeek,
ChatGPT e MiniMax e da STRATEGY_SEARCH 5.3; **sono evidenziate le celle corrette da questo consiglio**. Il rilevatore
nascosto non migliora nessuna riga [calcolo].

| Caso | `q = 0,1` | `q = 0,3` | `q = 0,5` | `q = 1` | Novizio, `H = 0` |
|---|---|---|---|---|---|
| Denaro, il pagatore verifica da sé; il registro è vivo, D26 e D23 risolte | ≤ 0 | ≤ 0 | ≤ 0 | ≤ 0 | `−c_f` (verifica sempre) |
| Lo stesso, ma la coalizione `q = 1` include i produttori dei blocchi e censura la controversia | — | — | — | fino a `+R` | fino a `+R` |
| Risposta falsa con la marcatura «verificato» | 0 | 0 | 0 | 0 | 0 |
| Danno con `p = R/(R + H)`: passa tutta la serie di `n_w` contraffazioni | ≈ 50% | ≈ 50% | ≈ 50% | ≈ 50% | 0 con un pagatore onesto |
| Danno con `p = 3R/(R + H)` | ≈ 12,5% | lo stesso | lo stesso | lo stesso | 0 |
| Pagatori pigri della quota `λ`, l'esecutore non li distingue | ≤ 0 con `p(1 − λ) ≥ R/(R + H)` | lo stesso | lo stesso | lo stesso | **`+λR`** |
| Pagatori pigri distinguibili (con prove da nuove chiavi — gratuitamente) | fino a `+R` | fino a `+R` | fino a `+R` | fino a `+R` | **fino a `+R`** |
| Pagatore senza attrezzatura ha affidato la verifica a una terna casuale | +0,001R | +0,027R | +0,125R | +R | lo stesso |
| Campione comune secondo D20, almeno una fonte onesta | ≤ 0 | ≤ 0 | ≤ 0 | ≤ 0 con una fonte esterna onesta; altrimenti fino a `+R` | lo stesso |
| Solo faro interno dei partecipanti 64/43 | ≤ 0 tranne 4,8·10⁻²⁸ | tranne 9,4·10⁻¹⁰ | tranne 0,41% | fino a `+R` | lo stesso |
| Per confronto: regola segreta dell'epoca presso il comitato | trapela in 10 applicazioni con probabilità 0,65; poi circa `(1 − p)·E·R` per epoca | 0,97 | 0,999 | fino a `+R` per contraffazione | le prove sono gratuite: fino a `+R` |
| Addestramento senza un nodo che verifica da sé | fino a `+R` | fino a `+R` | fino a `+R` | fino a `+R` | fino a `+R` |

Come leggere la tabella:

- **La riga «≤ 0 con qualsiasi `q`»** è vera solo con le condizioni nominate: `q` — la quota di collusione tra
  i verificatori estranei; se la stessa coalizione controlla la produzione dei blocchi o il faro, può
  ritardare o censurare la prova (lo hanno detto direttamente gpt1 e gpt2). Servono anche `δ ≪ W`,
  la bruciatura atomica (D26), la soluzione del conflitto con D16 e la regola delle controversie false (D23, calcolo M9).
- **L'esecuzione della verifica è importante non meno della frequenza.** Esempio del critico ChatGPT: `R = 1`, `H = 3`,
  `p = 1/4`, `c_f = 0` danno esattamente un'aspettativa nulla; se il pagatore esegue solo il 90% delle verifiche assegnate,
  la probabilità di cattura è 0,225 e il guadagno `+0,1R` [calcolo]. Se la prima contraffazione si può
  spiegare come guasto secondo l'attuale D16 e conservare `H`, l'aspettativa `(1 − p)R − c_f` è positiva.
- **«≈ 50%»** è la probabilità che passi *tutta la serie* di `n_w = H/R` contraffazioni con la crescita di
  `H` dopo ogni salto (`h/(h + n)` con `n = h`). Una contraffazione mirata di una chiave matura
  passa con probabilità `1 − p`: con `H = 4320R` è circa 99,977% (critico ChatGPT secondo ds2).
- **Le righe «pigri»** sono corrette: il precedente valore 0 per il novizio è errato (sezione 1, punto 6).
  Scenario: una chiave fresca presenta una contraffazione al pagatore `X`; se `X` verifica, si perde solo `c_f`,
  non c'è nulla da bruciare; se `X` è pigro, la chiave ottiene `R` e la conoscenza «`X` è pigro»; poi le chiavi mature
  della coalizione presentano contraffazioni solo ai pigri (critico Claude). Il critico ChatGPT ha aggiunto che anche con
  la piena indistinguibilità la condizione `p(1 − λ) ≥ 1` per il novizio è irrealizzabile con `λ > 0`, e
  le chiavi non collegabili chiudono solo un canale di distinzione: testo, tempo, dimensione della richiesta e pagamento collegato
  restano.

### 4.5. Novizio

Un novizio con conto vuoto (`H_lock = 0`) contro un pagatore onesto viene sempre verificato e perde
`c_f`. La segretezza delle regole qui non aggiunge nulla. Due precisazioni di questo consiglio: contro un pagatore pigro
il novizio ottiene fino a `+R` (sezione 4.4), e le nuove chiavi gratuite possono alzare la quota di richieste
verificate completamente: se la quota di lavoro sui primi ordini di chiavi vuote è `f`, e sul
resto `p = 0,1`, il sovrapprezzo è `ρ[f + 0,1(1 − f)]`, e la condizione del 5% con `ρ = 0,21` dà `f ≤ 0,1534`
(critico ChatGPT) [calcolo]. Nessuno schema del consiglio finora regge il flusso di nuove chiavi e l'autopagamento
contemporaneamente.

### 4.6. Pagatore pigro

La strategia si regge sul fatto che il pagatore lancia davvero la moneta e verifica. Un pagatore pigro,
che l'esecutore può distinguere, dà fino a `+R` a qualsiasi chiave. Mezzi in ordine decrescente di forza: (a) il programma del pagatore
per impostazione predefinita esegue la regola del nucleo, e la disattivazione della verifica toglie
dalla risposta la marcatura «verificato»; (b) chiavi non collegabili del pagatore (claude1) — serve un meccanismo di pagamento
senza un emittente con privilegi speciali: la firma cieca richiede un emittente, Privacy Pass (a memoria) — uno schema
con emittente sul server; un emittente a soglia introduce di nuovo `q` (critico Claude); (c) il sorteggio pubblico
del faro *non* corregge il pagatore pigro (sezione 4.2). Come conciliare la non collegabilità con la regola delle controversie
false senza cauzione (D23), non è risolto.

### 4.7. Utente senza attrezzatura

L'utente che non può ricalcolare da sé la risposta non è protetto da questa strategia. Se affida
la verifica a una terna casuale, la coalizione ottiene `q³R`: +0,001R / +0,027R / +0,125R / +R; con un solo
assistente — `qR`, e con un complice scelto di proposito — fino a `+R` con qualsiasi quota media (critico
ChatGPT) [calcolo]. Una perdita positiva limitata D1 è direttamente vietata, quindi questa è una falla aperta
D21. Il rilevatore nascosto non la chiude: claude1 ha mostrato un controesempio con «canarini segreti» —
un verificatore colluso supera onestamente tutti i compiti di controllo altrui e mente solo sulle proprie
contraffazioni, che riconosce dalla chiave dell'esecutore o dalla libertà di scelta (la contraffazione non deve essere
deterministica, la risposta esatta è deterministica). La variante onesta è vendere due livelli di servizio
con una differenza chiaramente scritta: «verificato da me» e «verificato dai nominati, perdita `R·q^k`» (mm1).

### 4.8. Danno

Al danneggiatore il guadagno non serve. Con qualsiasi frequenza `p < 1` una parte delle sue contraffazioni passa. L'unica
protezione è la marcatura «non verificato» per impostazione predefinita e «verificato» solo dopo la verifica completa prima della presentazione.
Il rilevatore nascosto non cambia la riga del danno (tutti i lavori). mm1 ha trovato l'unico punto in cui *la scelta fresca* cambia sostanzialmente
il quadro del danno: con la verifica parziale (soprattutto del passo di addestramento) contro un campione fisso aperto
l'imbroglione con una sola esecuzione esatta trova le celle non verificate e contraffà solo quelle, cattura 0; la scelta fresca del campione dopo la fissazione dà la cattura `s` (la quota
della parte verificata) per una deviazione e `1 − (1 − s)^m` per `m` deviazioni. I critici DeepSeek e
Claude hanno precisato: è casualità fresca, non segreto delle regole; il motivo di tale contraffazione è il danno, non il
denaro (contro il lavoro onesto la contraffazione esatta guadagna circa zero); e la conclusione si regge su
un'ipotesi non stabilita, che le celle del passo di addestramento si possano contraffare indipendentemente.

---

## 5. Decisioni

Le formulazioni sotto sono **raccomandazioni**, non decisioni accettate. I requisiti immutabili R1–R6 non cambiano modificando
le righe della roadmap. Secondo D4, dopo l'avvio con un'impronta fissata il cambiamento dell'insieme delle transizioni ammissibili richiede il passaggio a una nuova rete; il cambio di chiave non dà tale diritto
(critico ChatGPT).

### 5.1. D4 — completare, non cambiarne il senso

Il testo attuale di D4: la verifica è automatica, senza votazioni; ogni nodo esegue da sé la verifica secondo
l'impronta fissata delle regole. Il consiglio è unanime contro l'indebolimento di D4 per regole segrete:
una regola segreta richiede di accettare il verdetto dei detentori della chiave, dell'enclave o del gruppo, che il nodo
non può verificare da sé. Il critico ChatGPT ha mostrato come sarebbe un tale indebolimento: «il nodo accetta il verdetto del programma corrente scelto dai detentori della chiave dell'epoca», «il nodo accetta il rapporto del programma misurato secondo la catena attendibile del produttore» o «il nodo accetta il bit emesso dal gruppo».

**Aggiunta proposta** (unione delle varianti dei critici Claude e ChatGPT, claude1, claude2, gpt1,
della proposta D27 di mm5):

> «Il nucleo può accettare in ingresso casualità sconosciuta all'esecutore fino alla fissazione definitiva
> del risultato: (a) la moneta segreta della parte la cui propria decisione è protetta, lanciata dopo la
> fissazione; (b) i valori delle fonti D20 nei round fissati prima della fissazione e che arrivano dopo di essa.
> Il generatore dell'istanza di verifica, la famiglia di verifiche ammissibili e la legge di scelta sono la parte aperta del nucleo
> con impronta fissata; nuove regole a tempi casuali sono nuovi valori di casualità, non
> nuovi algoritmi. L'istanza realizzata che influenza diritti altrui viene pubblicata non più tardi del pagamento
> e ricalcolata da ogni nodo. La marcatura locale del pagatore di per sé non crea una testimonianza di rete
> sul lavoro. Regole e chiavi di verifica segrete di lunga durata, comitati a soglia,
> attestazioni TEE e verdetti chiusi non sono contenuti nel fondamento della decisione comune; sono ammessi solo
> come verifiche aggiuntive che aumentano la frequenza».

**Che cosa non cambia:** l'immutabilità del nucleo, l'assenza di votazioni, la verifica autonoma da parte di ogni
nodo. **Che cosa rompe:** nulla; l'aggiunta chiude la direzione dei «rilevatori segreti» come fondamento della
garanzia. La possibilità di una prova verificabile pubblicamente di una relazione fissata (ZK) resta
aperta e non richiede modifiche di D4 (critico ChatGPT).

### 5.2. D20 — precisare

Il testo attuale di D20: non meno di due fonti pubbliche indipendenti, valore in un momento fissato in anticipo dopo la fissazione definitiva,
senza diritto di saltare.

**Chiarimento proposto** (critico Claude con aggiunte del critico ChatGPT):

> «Non meno di due fonti pubbliche indipendenti; i loro valori si combinano con una funzione
> hash univoca con etichetta di dominio e identificatore del lotto, e non scegliendo uno dei valori. Il round
> di ciascuna fonte è fissato prima della fissazione definitiva e arriva dopo l'accettazione definitiva
> del blocco con la fissazione. L'omissione, il nuovo sorteggio, la sostituzione della fonte o il passaggio a un valore noto in precedenza sono vietati;
> se il round non è disponibile, l'operazione contestata attende, la nuova richiesta non riceve il biglietto per quel round.
> Il faro si usa per campioni che influenzano diritti altrui (addestramento, esame, lotteria con premio comune, nomina dei verificatori);
> per la verifica privata da parte del pagatore del proprio denaro non è richiesto. Un faro interno a soglia dei partecipanti può essere una delle fonti solo
> con un'ipotesi scritta sulla quota di collusione dei suoi detentori e non può essere l'unica. Un VDF dallo
> stesso blocco non è considerato una fonte indipendente. La fiducia nelle fonti è un'ipotesi secondo R4».

**Che cosa esclude:** la modalità di riserva «ultimo valore disponibile» (mm3), la modifica di mm5 a D19
(«non mescolare le fonti»), il faro nella decisione monetaria del pagatore (mm3, mm4). **Rischio aperto:**
se «aspettare il round» significa un ritardo infinito, è un rischio non chiuso R1/R6 (critico ChatGPT);
il critico MiniMax propone invece dell'attesa di considerare la verifica obbligatoria.

### 5.3. Che cosa non cambia

- **D1** — non cambiare e non indebolire fino a «finché `q` è piccolo»; una perdita positiva limitata
  resta una violazione (tutti i lavori e i critici).
- **D7** — una regola segreta non lo soddisfa con nessuna soglia (sezione 2.4).
- **D19** — non cambiare: l'aggiunta di mm5 è errata (sezione 4.2).
- **D6** — la segretezza non cambia la riga del danno; le marcature si precisano secondo la domanda 3 della sintesi precedente.

### 5.4. Legame con le otto domande della sintesi precedente

Le otto domande di [STRATEGY_SEARCH](STRATEGY_SEARCH.md), sezione 6, restano aperte. Questo consiglio
ha aggiunto ad esse:

| Domanda della sintesi precedente | Che cosa ha aggiunto il sesto consiglio |
|---|---|
| 1. D21, D11, D2: se pagare una risposta saltata dalla moneta | Nuovi argomenti non ce ne sono. Corretta la cella «pagatore pigro × novizio» (fino a `+R`): se il pagamento del saltato è permesso, serve una protezione dalla distinzione dei pigri. Il critico ChatGPT resta per la verifica completa come contratto principale e per la lotteria B come separata |
| 2. D7: quale verifica è ammissibile per il pagamento | Confermato che né la segretezza, né l'attestazione, né il comitato possono abbassare la frequenza inferiore; alzare si può. Aggiunto: conta la quota di verifiche *eseguite*, non solo la frequenza (esempio `+0,1R`) |
| 3. D6: marcature | La trappola, la statistica e il rilevatore nascosto non danno la marcatura «verificato» |
| 4. D16: guasto onesto | Se la prima contraffazione si può dichiarare un guasto e conservare `H`, la moneta non frena: `(1 − p)R − c_f > 0`. La decisione su D16 serve prima di qualsiasi attivazione del pagamento del saltato |
| 5. D8: termine e diritti della controversia | La condizione `δ ≪ W` e la vivezza del registro entrano nella riga «≤ 0» (sezione 4.4) |
| 6. D23: blocco fino a M9 | Nessuno degli undici lavori ha calcolato M9; il blocco resta. La non collegabilità dei pagatori aggiunge a M9 una nuova domanda |
| 7. Nuova D26: blocco della somma | Confermata la necessità della bruciatura atomica dell'ondata; il bit comune dell'epoca — nuovo controesempio (`+8,1R`) |
| 8. D1: se cambiarla | Non cambiare |

### 5.5. Nuove domande-decisioni di questo consiglio

**Domanda A (D4).** Accettare l'aggiunta a D4 della sezione 5.1? *Raccomandazione dei critici Claude, ChatGPT
e DeepSeek:* sì; il senso di D4 non cambia. *Su che cosa sono divergenti:* il critico ChatGPT propone una redazione più dettagliata, che parla esplicitamente di verifica «secondo una prova verificabile pubblicamente dell'affermazione fissata»; il critico DeepSeek ritiene sufficiente una breve nota sulla casualità dopo la fissazione;
il critico MiniMax (come mm2 e mm5) ritiene che D4 non vada cambiata affatto, perché la regola di verifica
è comunque aperta.

**Domanda B (D20).** Accettare il chiarimento di D20 della sezione 5.2? *Raccomandazione:* sì. *Su che cosa sono divergenti:*
che cosa fare se il round non è disponibile — aspettare (critici Claude e ChatGPT) o considerare la verifica
obbligatoria (critici DeepSeek e MiniMax). L'attesa può diventare un ritardo infinito; la verifica obbligatoria
cambia il prezzo e, nella lotteria, la composizione dei vincitori.

**Domanda C (faro o moneta nella decisione monetaria).** Scrivere che per la verifica privata
da parte del pagatore del proprio denaro il faro non si usa? *Raccomandazione* dei critici Claude e DeepSeek, nonché
di claude1, gpt1, gpt2, ds1, ds2, mm1, mm2: sì. *Contro:* mm3, mm4, mm5 (sorteggio pubblico invece della moneta),
claude2 (VRF del pagatore più faro per gli affari comuni). Il critico DeepSeek propone di confrontare prima
entrambi gli schemi con un mini-agente sugli stessi attacchi (sezione 6).

**Domanda D (pagatori non collegabili).** Includere nel programma di ricerca un meccanismo per cui
l'esecutore non possa collegare le richieste di un solo pagatore? *Raccomandazione* del critico Claude: sì, come
ricerca; fino alla sua costruzione la tabella del rischio contiene la riga «i pigri sono distinguibili: fino a `+R`».
*Aperto:* pagamento senza un emittente con privilegi speciali, compatibilità con D23, distinzione per testo e
tempo.

**Domanda E (peso).** Scrivere nella specifica del peso ([CURRENT_DESIGN](CURRENT_DESIGN.md), sezione 4),
che il peso con cui si scelgono i detentori o i verificatori non cresca con richieste autopagate?
*Raccomandazione* del critico Claude: sì. claude2 proponeva la selezione «per peso del lavoro verificato» senza tale
precisazione.

**Domanda F (chi paga il profilo esatto).** Come distribuire il sovrapprezzo `γ − 1`, se il ruolo del
verificatore pagato scompare? *L'hanno posta* mm4 e il critico MiniMax; non è stata proposta una soluzione.

**Domanda G (nuove decisioni di mm5).** Accettare D27 («segreto della scelta, non segreto della verifica») e D28
(«moneta con rivelazione differita»)? *Raccomandazione dei critici:* D27 per senso entra nell'aggiunta a D4
(sezione 5.1); D28 duplica l'impegno alla moneta di gpt2 e claude1 e ha senso solo se
l'impegno è pubblicato *prima* della fissazione della risposta.

---

## 6. Che cosa calcolare con i mini-agenti e che cosa verificare con l'esperienza

### 6.1. Mini-agenti (frazioni esatte, hash di controllo, ripetizione su un secondo dispositivo)

Elenco comune dei quattro critici. Per ogni calcolo conservare la descrizione delle regole, gli input, le frazioni esatte,
la storia peggiore, la versione e l'hash di controllo (critico ChatGPT).

1. **Regola dell'epoca contro moneta fresca.** Ondata, `H_lock`, bruciatura di tutta la somma, sequenza adattiva.
   Riferimenti: `+8,1R` / `−2,3751096381R` (gpt2), `98,01R` (claude2),
   1/5 → 1/9 → 0 (claude1), `+4,4295R` / `−2,49676R` / `+7,2R` (consiglio precedente e critico ChatGPT).
2. **Prove dei pagatori pigri con nuove chiavi.** Aspettativa della prova, tempo fino al riconoscimento
   del pagatore, guadagno delle chiavi mature; con pagatori collegabili e non collegabili. Aspettativa
   del critico Claude: con la collegabilità il freno contro i pigri è zero.
3. **Moneta segreta contro sorteggio pubblico del faro** sugli stessi attacchi (critico DeepSeek). Aspettativa:
   esiti monetari uguali e prezzo maggiore per il sorteggio pubblico.
4. **Programma lineare della miscela di test** (gpt1, gpt2): riferimento «tre classi → 2/3 contro 1/2»,
   aggiunta di una classe non coperta → 0; minimax sulla matrice «test × contraffazione».
5. **Code della soglia:** binomiali, senza reinserimento, per peso con autopagamento, con corruzione dopo
   la nomina. Riferimento «3 su 5»: `107/12500`, `4077/25000`, `1/2`, `1`; SHA-256 di controllo
   delle quattro righe di gpt1, ripetuto dal critico ChatGPT:
   `fd83fbdd42baa56d982eba3be90888cf3ec5a6261b5daa53d42fdc42b99c8323`.
6. **Trappole:** `1/((1 − σ)ρ)` sulla griglia di `ρ` e `σ`; riconoscimento della ripetizione; ammortamento della banca dei riferimenti
   contro il ricalcolo; verifica dell'affermazione di mm2 sul prezzo quasi nullo della ripetizione di una richiesta verificata.
7. **Deviazioni nella VRF e nell'impegno del pagatore:** rifiuto di rivelare, più chiavi, interruzione dopo
   la rivelazione, lotteria con premio comune.
8. **Miscela delle fonti D20:** distorsione con una sola fonte onesta, con la trattenuta del blocco, con
   l'indisponibilità del round; divieto dell'«ultimo valore».
9. **La contraffazione «chirurgica» di mm1** contro il campione fisso aperto e quello fresco: cattura 0 contro `s`;
   soglia `p·s ≥ (R − c)/(R + H_lock)`.
10. **Conteggio delle operazioni non lineari per token** secondo la configurazione fissata D5 per le stime FHE e MPC
    (ora 1,4·10⁷–2,6·10⁷ in modo approssimato); stime di DKG, commit–reveal, VRF in byte e messaggi.
11. **Pacchetto 8 presso il pagatore** (mm3): `ρ` è misurata rispetto alla generazione a pacchetti, e il ricalcolo di una
    risposta da parte del pagatore non diventa così più economico.
12. **Correzione delle tabelle:** mm1 (`k = 10`, `H_lock = 10R`), mm5 (`p·ρ`), cella «pigro × novizio»
    in STRATEGY_SEARCH 5.3.
13. **M9** — prezzo della controversia per la regola D7 e condizione di rimozione del blocco D23; autocontroversia, limite del rimborso,
    flusso di nuove chiavi.

### 6.2. Esperienze

**Per la conclusione sul rilevatore nascosto l'esperienza non serve:** sono teoremi, la misurazione non li confuta (claude1,
claude2, ds2, critici Claude e DeepSeek). Anche esperienze con FHE, MPC e TEE non servono: il loro miglior esito
non cambia i teoremi.

**Nell'ambito di D5 (permesso):** O5 — qualità su 320 compiti; O3 e O4 con nuclei bit per bit uguali più veloci —
l'unica via al riferimento del 5%.

**Fuori D5 — solo con un permesso separato del proprietario:**

- tempo di un passaggio di verifica su CPU di portatile e su telefono, avvio a freddo e a caldo, energia;
- quanto i metadati della richiesta (tempo, dimensione, testo) permettono all'esecutore di distinguere un pagatore
  verificatore — da questo dipende il prezzo delle chiavi non collegabili;
- frequenza delle divergenze hardware silenziose `P_f` — prima di qualsiasi modifica di D16;
- quota di coincidenza dei token di Q8_0 e del profilo esatto (per la stima della contraffazione economica e per l'esatto
  decoding speculativo);
- ritardo e costo del round di un faro reale, comportamento con una fonte silenziosa;
- per le trappole — se la verifica viene riconosciuta e quanto costano i riferimenti;
- il ricalcolo esatto del passo di addestramento come premessa di qualsiasi sua verifica.

---

## 7. Divergenze non risolte dal consiglio e riferimenti dubbi

### 7.1. Divergenze

1. **Pagamento della risposta saltata dalla moneta contro verifica completa di ogni risposta pagata.** claude1,
   claude2, ds1, ds2 e mm1–mm5 si basano sul pagamento del saltato sotto il rischio di bruciatura della somma non maturata;
   gpt1, gpt2 e il critico ChatGPT — sulla verifica completa come contratto principale e sulla lotteria B come
   separata. Ereditato dal consiglio precedente; decisione del proprietario su D21, D11, D7.
2. **Faro o moneta nella decisione monetaria del pagatore** — sezione 5.5, domanda C. mm3 e mm4 ritengono che
   il sorteggio pubblico rimuova l'ipotesi del pagatore onesto; i critici Claude e DeepSeek ritengono questo
   un errore (un pagatore pigro non verificherà nemmeno con un sorteggio pubblico). Non calcolato.
3. **`R/(R + H_lock)` o `R/H`.** Il primo è esatto per il denaro; il secondo dà un margine e un numero atteso finito
   di contraffazioni fino alla cattura con `H` fisso, ma costa circa due volte di più con `H` piccolo.
   Il critico ChatGPT ha mostrato che, con la crescita di `H` dopo ogni salto, per entrambe le regole il numero medio di
   salti fino alla prima cattura è infinito. Il consiglio non ha dato nuovi argomenti.
4. **La trappola come guadagno autonomo.** mm2 (il riferimento segreto — l'unico guadagno reale)
   e ds1 (risparmio del riferimento in cache) contro claude2, mm4, mm5, gpt1 e i critici Claude e DeepSeek.
   Il critico ChatGPT ha preso una posizione intermedia: un riferimento già noto al pagatore onesto può
   ridurre il prezzo marginale, e per trappole fresche indistinguibili `σ` può essere 0 anche con `q = 1`
   tra esecutori estranei. Il calcolo non è stato eseguito.
5. **Miscela di tipi di verifica come mezzo di risparmio.** gpt1, gpt2, claude2 — possibile con una copertura dimostrata
   delle classi di errore; mm2 — mai. Per Qwen la copertura non è dimostrata.
6. **Faro interno a soglia dei partecipanti.** mm3 — la migliore primitiva; mm5 — solo esterno; claude1,
   claude2 e il critico Claude — ammissibile solo come una delle fonti.
7. **Quanto R2/R3 vietano i segreti comuni.** ds1, mm1, mm3 — in linea di principio; claude2, critici Claude
   e ChatGPT — solo i segreti necessari per verificare le decisioni passate.
8. **Prezzo di MPC.** Le stime divergono di ordini di grandezza: ds1 — 2,4–14 MB per token (i critici ritengono che sia il
   prezzo della traccia di verifica, non di MPC); critico Claude — 0,15–1 GB per token; critico ChatGPT — 448 MB per
   posizione; critico MiniMax — fino a 180 TB per risposta (egli considera tutte le moltiplicazioni in rete, e il critico ChatGPT
   osserva che la moltiplicazione di un peso aperto per un'attivazione condivisa in molti protocolli si esegue
   localmente). La conclusione «MPC fuori budget e dipendente da `q`» non cambia.
9. **Fattori FHE:** ds1 `10³–10⁶`, claude2 `3·10³–2·10⁵`; il critico ChatGPT ritiene che moltiplicare la
   stima per bootstrap per `ρ` di un passaggio pronto sia scorretto, e serve una stima dello stesso passaggio con
   uno schema concreto. Le conclusioni non ne dipendono.
10. **Campione nascosto con verifica parziale** (mm1): «rilevatore segreto» o moneta fresca —
    divergenza di parole; l'applicabilità al passo di addestramento dipende dall'indipendenza non misurata delle celle.
11. **D16.** Bruciare `H_lock` per qualsiasi divergenza dimostrata con indennizzo agli onesti da un contributo di rete
    (linea di claude1 e dei critici Claude e DeepSeek) contro la conservazione delle ricompense precedenti in caso di guasto onesto
    (gpt1, gpt2, critico ChatGPT). Serve una misurazione di `P_f`.
12. **Addestramento.** Nessuno schema soddisfa D7 con `q = 1` entro il 20%.
13. **La classe principale delle contraffazioni:** quella costosa «chirurgica» (mm1) o quella economica Q8_0 (mm3, mm4). Non misurato.

### 7.2. Errori trovati nei numeri dei lavori

Perché i numeri errati non finiscano in altri documenti:

| Lavoro | Affermazione | Corretto [calcolo dei critici] |
|---|---|---|
| mm1 | Con `H_lock = 10R` frequenza 0,0909 e prezzo della verifica 0,005–0,009% | `0,0909·ρ` = 0,91–3,64% |
| mm1 | Fuga dei «dieci» con `q = 0,1`: `1·10⁻⁵R` | `10⁻¹⁰R` |
| mm1 | Soglia 25% con `H_lock = R` | 29,29% con i parametri propri di mm1 |
| mm5 | `p·ρ` = 0,021–0,042% con `p = 0,1` | 2,1–4,0% (la tabella propria di mm5 è corretta) |
| mm5 | «FHE è deterministico, l'osservatore costruisce un dizionario» | Gli schemi FHE robusti sono probabilistici |
| mm5 | «VRF imprevedibile per il proprietario» | Il proprietario calcola la VRF quando vuole |
| mm5 | Ricalcolo completo del passo di addestramento ≈ 36,8% | 36,8% è un esempio di carico misto; il ricalcolo del passo ≈ 100% |
| mm2 | «Il 5% è raggiungibile con `p ≤ 0,33%`» | Con `ρ = 0,21` è ammissibile `p ≤ 23,8%` |
| mm4 | «VRF non rivela la scelta» | La verifica della prova VRF rivela il valore |
| ds2 | `N·H_s ≈ 2718` tentativi | Circa 890 senza reinserimento; serve una posizione sicura |
| ds1 | La trappola costa `φ·ρ`, il riferimento in cache risparmia | La trappola costa non meno della generazione dell'esecutore; prima bisogna ottenere la cache |
| ds1, ds2 | Le trappole aggiungono la cattura `φ` con qualsiasi `q` | Non più di `φ(1 − q)` con la ripetizione; con `q = 1` — 0 |
| claude1, claude2, mm3, mm4, STRATEGY_SEARCH | Pagatore pigro × novizio = 0 | Fino a `+R` |
| claude2 | Formula dell'esempio dell'epoca `(1 − p)(E − 1)R` | `(1 − p)·E·R − p·H_lock = 98,01R`; la coincidenza è casuale |

### 7.3. Riferimenti dubbi (valutazioni dei critici a memoria, senza verifica)

| Lavoro | Affermazione | Valutazione |
|---|---|---|
| mm5 | «RandAILight» come faro | Dubbio; il nome è sconosciuto ai critici |
| mm5 | «iO teoricamente possibile, Barak e coautori ~2001» | Confuso: Barak e coautori 2001 — impossibilità dell'offuscamento «scatola nera»; candidati iO — Garg e coautori 2013 |
| mm1 | «Roadmap di iO di Barak e coautori, 2019» | Dubbio |
| mm2 | Appendice F: «Ben-Or e coautori», «Allingham, Melvin, Temple 1992», «Dwork ~1999», «Hashcash — Homestein», «Awasthi», «Randcast Bader ~2020» | Dubbio quasi su tutti i punti; non trasferire nella sintesi |
| mm3 | «Cui, Wang e altri, Skoglid e altri» sulla moving target defense | Dubbio |
| ds1 | «Canetti 1997 — funzioni puntuali nel modello dell'oracolo casuale» | Dubbio (a memoria — un'ipotesi del tipo DDH) |
| ds1 | «Bishop–Jain–Kowalczyk 2018» | Dubbio sull'anno (a memoria 2015) |
| ds1, ds2 | «drand ~30 s» | In parte: a memoria, in catene diverse 30 s e 3 s |
| ds2 | «MPC 5,98·10¹² MAC (claude2)» | Il riferimento è impreciso |
| claude1 | «SGX.Fail, chiave master di Secret Network, 2022» | Dubbio nei dettagli (l'autore stesso l'ha segnalato) |
| claude1 | Privacy Pass come modello di emissione senza una parte speciale | A memoria — schema con emittente sul server |
| claude2 | Limite inferiore PIR — Beimel, Ishai, Malkin | Dubbio: i loro lavori riguardano PIR con preelaborazione; il limite classico, a memoria, è di Chor e coautori |
| claude2 | Lowd–Meek, Tramèr: `d` richieste binarie bastano per qualsiasi classificatore | Dubbio in generale |

Gli altri riferimenti dei lavori (Shamir, Feldman, Pedersen, Gennaro–Jarecki–Krawczyk–Rabin, Micali–Rabin–Vadhan,
Boneh e coautori sul VDF, Rivest–Shamir–Wagner, Aumann–Lindell, Asharov–Orlandi, giochi di ispezione,
Barak e coautori sull'impossibilità della «scatola nera») ai critici sembrano attribuiti correttamente per direzione;
le fonti primarie non sono state verificate.

---

## 8. Chi ha fatto che cosa

Il consiglio ha lavorato sui materiali del progetto, senza accesso alla rete e senza esperimenti.

- **Undici lavori indipendenti:** ChatGPT — due (gpt1, gpt2), DeepSeek — due (ds1, ds2),
  Claude — due (claude1, claude2), MiniMax — cinque (mm1 con enfasi sull'economia, mm2 — sulla protezione dall'inganno,
  mm3 — sulla distribuzione e il ripristino, mm4 — sui controesempi, mm5 — sulle soluzioni non standard). Ogni lavoro ha analizzato sei direzioni del mandato: chi detiene la chiave, come verificare
  secondo una regola sconosciuta, che cosa può essere un rilevatore segreto, la teoria, il prezzo e la compatibilità
  con le decisioni.
- **Quattro critiche:** una da ChatGPT, DeepSeek, Claude e MiniMax (la critica di MiniMax è formulata
  come proposta con critica). Ogni critico ha letto tutti gli undici lavori, cercato errori e
  controesempi e ricalcolato i numeri chiave. Il critico DeepSeek ha verificato l'aritmetica con programmi locali su frazioni
  esatte, il critico Claude — con brevi calcoli in Python, il critico ChatGPT
  ha riprodotto l'hash di controllo della tabella di gpt1.
- **Sintesi:** questo documento è stato compilato da Claude sui lavori e sulle critiche. Nuove valutazioni e numeri oltre ai lavori,
  alle critiche, agli esiti D5 e a STRATEGY_SEARCH non sono stati aggiunti; dove i critici sono divergenti, è indicato.
