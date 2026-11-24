<!-- translation of docs/STAGE4_KERNELS.md, source sha256: e81d4e27191f3ce009ea9b71602c58405e742a7229fc972d8c69ae520e675812 -->

# Fase 4. Contratto byte per byte dei calcoli integrati

[English](../../docs/STAGE4_KERNELS.en.md) · [中文](../zh/STAGE4_KERNELS.md) · [Español](../es/STAGE4_KERNELS.md) · [Français](../fr/STAGE4_KERNELS.md) · [Deutsch](../de/STAGE4_KERNELS.md) · **Italiano** · [Русский](../../docs/STAGE4_KERNELS.md) · [Português](../pt/STAGE4_KERNELS.md) · [العربية](../ar/STAGE4_KERNELS.md)

Stato al 24 novembre 2026. Il documento definisce le regole esatte di quattro nuovi calcoli integrati del mini-agente (dalla versione 1.2.0 dell'agente) per i calcoli M8, M10, M12 e M14 da [VERIFICATION_SEARCH](VERIFICATION_SEARCH.md), sezione 5.3. La specifica e l'implementazione in Go sono state scritte da ChatGPT; DeepSeek ha verificato in modo indipendente la specifica sulla base dei lavori originali del consiglio e, basandosi solo su di essa, ha scritto una seconda implementazione in Python ([tools/reference_stage4.py](../../tools/reference_stage4.py)); tutti i 73 risultati dei compiti sono coincisi byte per byte; Claude ha verificato il codice e il confronto. I riferimenti del tipo «claude1, §5.4» indicano i lavori del consiglio dei modelli, riuniti in VERIFICATION_SEARCH. Questo è un conto esatto secondo le formule, non una misurazione: la coincidenza conferma l'aritmetica, ma non le ipotesi dei modelli. I calcoli M5, M7 e M18 sono rinviati: nei lavori mancano le regole per determinarli in modo univoco (sezione «Calcoli rinviati»).

| Calcolo dal §5.3 | Kernel versione 1 | Che cosa si può apprendere da una singola unità |
|---|---|---|
| M8 | `t4-scale` | Quanti token di addestramento per nodo sono necessari con un dato numero di candidati e quanti candidati consente il budget |
| M10 | `exam-thresholds` | In quale intervallo razionale si trova ciascuna delle due soglie dell'esame |
| M12 | `merge-attribution` | Come cambia la somma degli accrediti al partecipante quando si aggiungono copie esatte o con rumore |
| M14 | `verification-enumerations` | Quali casi hanno superato o fallito in modo esaustivo la verifica dell'impacchettamento, della catena o dell'uguaglianza sul campo |

La scelta segue dalla tabella del consiglio nel §5.3. Secondo D18 il pagamento per il miglioramento resta un'ipotesi di ricerca. Per riprodurre tutti e quattro i calcoli bastano i parametri di input. [Esito del consiglio](VERIFICATION_SEARCH.md) · [Decisioni D18–D20](ROADMAP.md)

## Regole comuni della versione 1

Nel compito firmato il nome del kernel e l'intero `kernel_version: 1` sono memorizzati separatamente. L'input `params` è un oggetto con tutti i campi elencati per il kernel. Campi in più o mancanti, ripetizione di una chiave JSON, valori fuori intervallo e tipi errati producono un errore. Un intero si scrive come letterale intero JSON, senza punto decimale né esponente. Stringhe e valori booleani al posto dei numeri sono vietati. I limiti sono inclusivi. Gli assi della griglia conservano l'ordine di input. Il numero di unità è esattamente pari alla dimensione della griglia indicata per il kernel, da 1 a 1 000 000. La numerazione delle unità parte da zero. Nel prodotto cartesiano l'ultimo asse cambia più rapidamente di tutti.

Per il confronto si prende l'intero oggetto del risultato. In Python i byte canonici sono `json.dumps(result, sort_keys=True, ensure_ascii=True, separators=(',', ':')).encode('ascii')`, senza ritorno a capo finale. L'hash del risultato è lo SHA-256 di questi byte, 64 cifre esadecimali minuscole. L'ordine degli elementi degli array è significativo. Una frazione in una stringa si scrive in base decimale come `p/q` con denominatore positivo dopo la riduzione, compresi `0/1` e gli interi con `/1`. Non ci sono segni più né zeri iniziali. Per M14 è definito separatamente l'hash dei byte *all'interno* del risultato dell'impacchettamento. [Codificatore canonico dell'agente](../../agent-go/canon/canon.go)

## M8. Scala di T4 con un aggiornamento da ogni partecipante

`t4-scale@1` calcola il numero intero minimo di token di addestramento del modello per round al quale l'esame aggiunge non più del 20% dei calcoli. Per un dato budget di token il kernel trova anche il numero limite di candidati. Nel modello ogni nodo verifica tutti i `K=N` aggiornamenti. La base costa un passaggio in avanti per posizione, ogni aggiornamento degli strati superiori costa una frazione `a=L_a/L` di un passaggio, e l'addestramento di un token costa tre passaggi. Questi rapporti sono dati dalla proposta. claude1, §5.4 «Prezzo» e §7.5, punto 4 · critic_claude, §1.8 e §10.4, punto 3 · [VERIFICATION_SEARCH, §5.3, M8](VERIFICATION_SEARCH.md)

| Campo `params` | Valori ammessi |
|---|---|
| `N` | Asse di interi da 1 a 1 000 000. Numero di candidati nel round |
| `n` | Asse di interi da 1 a 1 000 000. Numero di posizioni dell'esame |
| `a` | Asse di coppie di interi `[p,q]`, dove `1 ≤ p ≤ q ≤ 1 000 000`. Frazione di un passaggio per aggiornamento |
| `D_budget` | Asse di interi da 1 a 1 000 000 000 000. Budget di token di addestramento per nodo per round |
| `epsilon_bits` | Un intero da 1 a 256. Definisce `ε=1/2^epsilon_bits` per un esame fissato. Con un dato `n` il costo è lo stesso per tutti gli `ε` |

Tutti e cinque i campi sono obbligatori. Ogni asse è un array di lunghezza 1…32, i valori sono unici tenendo conto della riduzione delle frazioni, l'ordine dell'array di input viene conservato. Il numero di unità è pari al prodotto delle lunghezze degli assi e non supera 1 000 000. Numerazione da zero sul prodotto cartesiano `N, n, a, D_budget` nell'ordine dei cicli annidati, il budget cambia più rapidamente di tutti. Un'unità produce un oggetto.

Per il punto scelto poniamo `D=D_budget`, e riduciamo `a=p/q`. Misuriamo i calcoli in unità di `1/q` di un passaggio in avanti per posizione. Allora l'esame richiede `E=n(q+Np)`, l'addestramento richiede `W=3Dq`, la quota dei costi aggiuntivi è `E/W`. La divisione per il volume dell'addestramento del modello deriva dalla formulazione «supplemento» nel §5.4. La condizione del 20% equivale a `5E ≤ W`.

| Campo del risultato | Valore |
|---|---|
| `kernel` | Stringa `t4-scale@1` |
| `N`, `n`, `D_budget` | Interi del punto di input |
| `a`, `epsilon` | Stringhe ridotte `p/q`; `epsilon` si scrive come `1/q`, dove `q = 2^epsilon_bits` è un intero decimale (per esempio, `"1/4"` con `epsilon_bits = 2`) |
| `D_min` | Intero `(5E + 3q − 1) // (3q)`, dove `//` è la divisione intera per difetto. È l'arrotondamento per eccesso della soglia a un token intero |
| `fits` | Valore booleano `D_budget ≥ D_min`. L'uguaglianza vale |
| `N_max` | `null` se `W < 5nq` e anche il passaggio di base supera il budget. Altrimenti l'intero `(W − 5nq) // (5np)`. Zero significa che entra solo la base. Il limite può uscire dall'asse di input `N` |
| `overhead` | `E/W` sotto forma di stringa ridotta `numerator/denominator` |

Il limite inverso deriva dalla disuguaglianza lineare `5npN ≤ W − 5nq` con `p` positivo. Con i parametri ammessi `5E+3q−1 ≤ 5 000 005 000 002 999 999`, `W ≤ 3·10^18`. I denominatori sono positivi. Bastano interi con segno a 64 bit e la riduzione della frazione tramite MCD. In Go per `overhead` si usa `big.Rat`, per `2^epsilon_bits` — `big.Int`. Per un'unità si elaborano non più di 128 elementi degli assi e un numero costante di operazioni aritmetiche.

Per `n=3, N=4, a=1/2` l'esame costa 9 passaggi, con 15 token di addestramento occupa esattamente un quinto. Con 14 token il limite scende a tre candidati. Con `epsilon_bits=2` si ottengono i seguenti byte canonici.

```json
{"D_budget":15,"D_min":15,"N":4,"N_max":4,"a":"1/2","epsilon":"1/4","fits":true,"kernel":"t4-scale@1","n":3,"overhead":"1/5"}
```

A titolo di riferimento, nel §5.4 con `n=100000, N=10000, a=4/36` il minimo esatto è pari a 185 351 852 token. Il prezzo reale dipende dal riutilizzo dei prefissi, dal volume della cache, dalla testa di output, dalla normalizzazione, dal traffico e dal prezzo effettivo dell'addestramento degli strati superiori. La formula copre solo il conteggio dei passaggi descritto nel §5.4. Per stimare la soglia statistica al variare di `ε` serve M10. Il compito proposto fissa `ε=2^-80` secondo il riferimento numerico D19. critic_gpt, sezione su claude1, «Il prezzo nascosto di T4» · [ROADMAP, D18–D19](ROADMAP.md)

## M10. Soglia dell'esame T4 — `exam-thresholds@1`

M10 determina quanto grande deve essere il miglioramento medio osservato all'esame perché superi la soglia statistica. Per un singolo candidato fissato in anticipo si prendono `n` posizioni indipendenti con reimmissione. La differenza delle perdite su ogni posizione viene troncata a `[−B/2, B/2]`. L'input `V` è la varianza campionaria delle differenze troncate con divisore `n−1` (quadrato della deviazione standard). I limiti in nat per posizione sono presi dal passo 6 della descrizione di T4. claude1, §5.4 · critico Claude, §1.8

| Metodo | Soglia esatta `t` |
|---|---|
| Hoeffding | `B·√(ln(1/ε)/(2n))` |
| Bernstein empirico | `√(2V·ln(2/ε)/n) + 7B·ln(2/ε)/(3(n−1))` |

**Parametri e unità.** Cinque campi sono obbligatori. I campi `n`, `epsilon_bits`, `B`, `variance` sono assi di lunghezza da 1 a 32, ciascuno nell'ordine dell'array di input. I valori sull'asse sono distinti, le frazioni si confrontano dopo la riduzione.

| Campo | Valori ammessi |
|---|---|
| `n` | Numero di posizioni, intero da 2 a 1 000 000 |
| `epsilon_bits` | Intero `k` da 1 a 128, `ε = 2⁻ᵏ` per confronto |
| `B` | Larghezza dell'intervallo di troncamento, intero da 1 a 64 |
| `variance` | Frazione `[p,q]`, interi `0 ≤ p ≤ 10⁶` e `1 ≤ q ≤ 10⁶`. In tutti i punti della griglia `V=p/q ≤ B²·floor(n/2)·ceil(n/2)/(n(n−1))` |
| `digits` | Un intero `d` da 1 a 9. La larghezza assoluta garantita di ogni intervallo è minore di `10⁻ᵈ` |

Il massimo della varianza si raggiunge agli estremi dell'intervallo, poiché la varianza è convessa rispetto a ogni osservazione. Con j valori a un estremo il suo numeratore è proporzionale a `j(n−j)`, il che dà il limite indicato. Il numero di unità è pari al prodotto delle lunghezze dei quattro assi e non supera 1 000 000. La numerazione coincide con `itertools.product(n, epsilon_bits, B, variance)`, partendo da zero.

**Algoritmo di riproduzione byte per byte.** Per entrambi i metodi scrivere `t = √(A·ln 2) + C·ln 2`. Per Hoeffding `A=B²k/(2n), C=0`. Per Bernstein `A=2V(k+1)/n, C=7B(k+1)/(3(n−1))`. Tutte le divisioni qui sono razionali.

1. Prendere `S=10^(d+1)`, `l=693147180559945309/10¹⁸`, `h=693147180559945310/10¹⁸`.
2. Il limite inferiore è `(floor(√(S²Al)) + floor(SCl))/S`. Quello superiore è `(ceil(√(S²Ah)) + ceil(SCh))/S`. Entrambi gli addendi vengono arrotondati **separatamente**.
3. Per una frazione non negativa `x=p/q` calcolare `r=isqrt(p//q)`. Questo è `floor(√x)`. Per il limite superiore aggiungere a `r` un'unità esattamente quando `r²q < p`. Anche i normali `floor` e `ceil` si eseguono con divisione intera. Tutte le frazioni ottenute vengono ridotte.

**Certificato di precisione.** Dalla serie per `2·atanh(1/3)=ln 2` prendiamo `T=2·Σ 1/(j·3ʲ)` sui `j` dispari `j=1,3,…,39`. La coda è positiva e limitata dal primo termine omesso moltiplicato per `1/(1−1/9)`. Con un confronto intero otteniamo `l < T < ln 2 ≤ T + 9/(4·41·3⁴¹) < h`. La monotonicità di entrambi gli addendi e l'arrotondamento diretto garantiscono l'inclusione della soglia vera. Nell'intervallo dato `A ≤ 264192` e `C ≤ 19264`. Poiché `√h+√l > 1`, la sostituzione di `l` con `h` cambia la soglia non arrotondata meno di `(515+19264)·10⁻¹⁸`. L'arrotondamento amplia l'intervallo meno di `4/S`. La somma è minore di `10⁻ᵈ` anche con `d=9`. Per un'unità bastano quattro radici quadrate intere e un numero costante di operazioni su interi e frazioni di dimensione di alcune centinaia di bit, indipendentemente da `n`.

**Risposta.** I campi `n`, `epsilon_bits`, `B` e `digits` sono le coordinate intere e la precisione. `variance` è una stringa con la frazione ridotta. `hoeffding` e `bernstein` sono array di due stringhe di questo tipo, con il limite inferiore per primo. Per `n=2, k=1, B=2, V=0, d=1` il kernel produce i seguenti byte canonici.

```json
{"B":2,"bernstein":["323/50","647/100"],"digits":1,"epsilon_bits":1,"hoeffding":["83/100","21/25"],"kernel":"exam-thresholds@1","n":2,"variance":"0/1"}
```

Per una data soglia limite `τ`, la dimensione minima dell'esame **sulla griglia** è stabilita quando nel punto scelto il limite superiore è `≤ τ`, mentre per tutti gli `n` minori con gli stessi parametri il limite inferiore è `> τ`. Se l'intervallo interseca l'obiettivo, può servire una precisione maggiore. I numeri caratterizzano un confronto unilaterale della media troncata con fissazione prima del faro esterno. La correzione per la scelta tra più candidati, la qualità fuori dall'esame, la scelta di `τ` e l'entità dell'effetto reale richiedono dati o regole separati. Il pagamento per il miglioramento resta una variante di ricerca secondo D18. [ROADMAP, D18–D20](ROADMAP.md) · critico GPT, valutazione di T4

## M12. Come cambia l'accredito del proprietario dei duplicati con la fusione per somma

Nel lavoro per M12 sono indicate perdite lineari-quadratiche con gradiente e hessiana noti, tre regole di attribuzione, duplicati esatti e duplicati con rumore. Scegliamo la variante `merge = sum` esplicitamente analizzata nel §5.4. Il critico riporta il caso in cui anche l'aggiunta ripetuta di uno stesso passo migliora la funzione di perdita. Il kernel `merge-attribution@1` lo verifica su coefficienti di input espliciti. claude1, §5.4, passi 6–7 e punto 2 «Attribuzione e duplicati», §7.5, punto 7 · critic_gpt, tabella su claude1, riga T4

| Campo `params` | Significato e limiti inclusivi |
|---|---|
| `scale` | Denominatore comune `s`, intero 1…10 000 |
| `g` | Vettore dei numeratori del gradiente nel punto di base. La sua lunghezza definisce la dimensione `d`, 1…8 |
| `hessian` | Matrice simmetrica dei numeratori dell'hessiana, array di `d` righe da `d` componenti |
| `updates` | Array di `b=1…8` vettori iniziali di numeratori di lunghezza `d`, nell'ordine di presentazione. Sono ammessi vettori uguali |
| `owner` | Indice intero della presentazione iniziale del partecipante verificato, da 0 a `b−1`. Le altre presentazioni iniziali appartengono ad altri partecipanti |
| `copies` | Asse di 1…8 interi distinti 1…8. Il `c` scelto definisce il numero di presentazioni aggiunte dello stesso partecipante |
| `noise` | Asse di 1…32 vettori di numeratori di lunghezza `d` distinti a coppie. Il vettore nullo dà un duplicato esatto |
| `threshold` | Numeratore intero 0…10 000 per la detrazione `t=threshold/s` dalla stima di ogni presentazione |

Ogni componente di `g`, `hessian`, `updates` e `noise` è un intero da −10 000 a 10 000. Per ottenere il valore matematico di ogni componente dividerla per `s` **una sola volta**, anche per la matrice. La versione supporta coefficienti razionali con denominatore comune nell'intervallo indicato. La simmetria è obbligatoria, il segno della curvatura è arbitrario. Gli assi di input `copies, noise` formano una griglia. Per l'unità `u` prendere gli indici `divmod(u,len(noise))` rispettivamente. Dopo le `b` presentazioni iniziali aggiungere `c` vettori, ciascuno uguale a `updates[owner] + noise[j]` nei numeratori. I vettori iniziali vengono conservati. Gli insiemi di presentazioni prima e dopo l'aggiunta vengono considerati separatamente.

**Calcolo.** Sia `U` l'insieme degli indici delle presentazioni di una collezione, e `x(S)` la somma dei loro **vettori matematici** di aggiornamento sul sottoinsieme `S`. Il guadagno in termini di perdite è definito come riduzione rispetto alla base comune,

```text
v(S) = −gᵀx(S) − x(S)ᵀ H x(S)/2,     v(∅) = 0.
```

Per ogni indice `i` calcolare tre stime **con segno**. `separate[i]=v({i})`. La regola «lasciarne uno»: `loo[i]=v(U)−v(U без i)`. La stima `shapley[i]` è pari all'incremento medio `v(S∪{i})−v(S)` su tutte le permutazioni degli indici, dove `S` è costituito dai predecessori di `i`. Questa regola si applica alla funzione completa di riduzione delle perdite. Per il calcolo senza enumerazione fattoriale poniamo `q_i=v({i})`, `h_ij=−x_iᵀ H x_j`. La simmetria dà `v(S)=Σ q_i + Σ_{i<j} h_ij` sui partecipanti di `S`. Quando si esclude un partecipante scompaiono tutti i suoi termini a coppie. In una permutazione uniforme ogni altro partecipante lo precede esattamente nella metà dei casi. Pertanto

```text
loo[i]     = q_i + Σ_{j≠i} h_ij
shapley[i] = q_i + (Σ_{j≠i} h_ij)/2
v(U)       = Σ shapley[i].
```

Successivamente, separatamente per ogni regola, la stima `z` viene convertita nell'accredito `max(0,z−t)` in unità di miglioramento (il coefficiente di pagamento κ è preso pari a uno). Prima si accredita per ogni presentazione, poi si sommano gli accrediti del proprietario. `gain` è l'accredito al proprietario per la sua presentazione iniziale e tutte quelle aggiunte dopo l'aggiunta meno l'accredito per la sua unica presentazione prima dell'aggiunta. Il segno positivo significa un guadagno dalle presentazioni aggiuntive in questo esempio.

**Formato della risposta.** Le chiavi `kernel` (stringa `merge-attribution@1`), `owner`, `scale`, `copies` (intero scelto dall'asse), `noise` (vettore scelto di numeratori interi), `baseline`, `with_copies` e `gain`. Ciascuno degli oggetti `baseline` e `with_copies` contiene `value` — la frazione `v(U)` — e i campi `separate`, `loo`, `shapley` — array di frazioni nell'ordine degli indici delle presentazioni. L'oggetto `gain` contiene una frazione sotto ciascuno dei tre nomi delle regole. Tutte le frazioni di output sono stringhe canoniche.

**Aritmetica e limiti.** Il denominatore comune delle stime intermedie è `2s³`. Se `G, A, z_i` sono i numeratori interi di input del gradiente, dell'hessiana e del passo, il numeratore `q_i` è `−2s Gᵀz_i−z_iᵀAz_i`. Alla metà del termine a coppie corrisponde il numeratore intero `−z_iᵀAz_j`. Il numeratore della detrazione è `2s²·threshold`. Dopo aver aggiunto fino a 16 presentazioni si ha anche `|z_ij| ≤ 20 000`. Da qui `|z_iᵀAz_j| ≤ 8²·20 000²·10 000 = 2,56·10¹⁴`, la parte lineare in valore assoluto non supera `3,2·10¹³`. Anche la somma di 16 stime LOO complete e delle detrazioni, in valore assoluto, è minore di `1,3·10¹⁷`. Tutte le moltiplicazioni e le somme parziali entrano in 64 bit con segno. L'implementazione riduce le frazioni tramite `big.Rat`. Tempo `O(k d²+k²d)` con `k ≤ 16`, senza tabella dei sottoinsiemi. La memoria è limitata ai vettori di input, alla matrice, a tre stime per presentazione e al risultato.

**Verifica manuale.** Con `v(x)=3x−x²/2`, una presentazione `x=1` e soglia nulla, la stima iniziale è pari a `5/2` per tutte le regole. Dopo il duplicato esatto `v(2)=4`. Le regole danno per ogni presentazione `5/2` separatamente, `3/2` con l'esclusione e `2/1` secondo Shapley. Il guadagno totale del proprietario è rispettivamente `5/2`, `1/2`, `3/2`. Questo solo esempio basta a confutare l'assenza di guadagno per ciascuna delle tre regole su tutta la famiglia di tali modelli con soglia nulla.

**Ambito della conclusione.** L'insieme dei partecipanti al confronto è fissato. Il rumore è dato da un vettore esplicito, la soglia è data dall'input. L'accettazione, la riselezione della composizione dopo la detrazione della soglia, i costi di presentazione, l'addestramento dei parametri, gli effetti esterni e l'esame empirico sono fuori da questo modello. Il guadagno numerico riguarda la somma degli accrediti secondo la regola scelta. La verifica completa di D1 richiede di confrontare l'utilità della coalizione anche con il lavoro onesto e con l'inazione. [THREAT_MODEL, §§1.4–1.5](THREAT_MODEL.md) · [ROADMAP, D18 e D25](ROADMAP.md)

## M14. Verifica delle formule con enumerazione finita

Il kernel `verification-enumerations@1` ripete tre piccoli esperimenti. Permette di verificare se l'impacchettamento conserva la distinzione tra vettori ammessi e quanti errori lasciano passare i due tipi di verifica campionaria. I dati iniziali, l'ordine dell'enumerazione e gli hash di riferimento sono pubblicati in GPT2, §6.2 e «Codice di controllo per la prima ripetizione». La catena è data nella tabella «Che cosa affidare ai mini-agenti», la condizione di mancato rilevamento nel campo — nel §6.1. Lavoro GPT2 · [Sintesi, §5.3](VERIFICATION_SEARCH.md)

L'unico parametro `cases` è un array di 1–4 stringhe distinte dalla tabella seguente. `units = len(cases)`. Numerazione da zero, l'unità `u` calcola l'intero esperimento `cases[u]`. La chiave `case` del risultato contiene questa stessa stringa, `kernel` è uguale a `"verification-enumerations@1"`. Il formato degli altri campi dipende dall'esperimento.

| `case` | Campi del risultato oltre a `case` e `kernel` | Valori di controllo |
|---|---|---|
| `packing-8` | Interi `total`, `true_accepts`, `false_accepts`, stringa `verdict_sha256` | 441, 9, 0, `a5c8a8d715fb5293a4dd12753d3483e848f63cb24891a3e584bfdc81954f377c` |
| `packing-4` | Gli stessi campi | 441, 9, 20, `fca92fea5a3148177517b737591e499ed021432078bd9803578a2eaad4074fc9` |
| `chain-8-2` | Interi `total`, `caught`, `missed` | 224, 56, 168 |
| `field-5` | Interi `total`, `caught`, `missed` | 25, 20, 5 |

**Impacchettamento a bit.** Prendere la base `B` dall'etichetta dell'esperimento. Enumerare `(x,y,c,d)` in ordine lessicografico crescente, con `x,y ∈ {−1,0,1}`, `c,d ∈ {−3,…,3}`. Il ciclo interno cambia `d`. Il risultato vero è `(s,t)=(2x−y,−x−y)`. Il criterio di accettazione è la divisibilità di `(c−s)+B(d−t)` per `B²` sugli interi. In caso di coincidenza `(c,d)=(s,t)` l'accettazione incrementa `true_accepts`, negli altri casi di accettazione — `false_accepts`. Scrivere nell'ordine dell'enumerazione esattamente 441 byte, ciascuno con valore 1 in caso di accettazione e 0 in caso di rifiuto. `verdict_sha256` è lo SHA-256 di questi byte grezzi sotto forma di 64 cifre esadecimali minuscole. L'hash normale del risultato dell'unità si calcola separatamente dall'intero JSON canonico. Per la verifica manuale con `B=4`, `x=−1`, `y=1` la risposta vera `(−3,0)` e la dichiarazione `(1,−1)` danno differenza 0.

**Catena.** Per ogni singolo difetto `h=0,…,7` enumerare tutte le coppie non ordinate senza reimmissione come `0 ≤ i < j < 8`. Incrementare `total` di 1 per ogni terna, `caught` — se `h=i` o `h=j`. Il numero di mancati rilevamenti è `missed=total−caught`. Per ogni `h` ci sono 28 coppie, delle quali esattamente 7 contengono `h`.

**Campo.** Enumerare i vettori `(x,y)∈{0,…,4}²`, compreso quello nullo. L'errore `(1,−1)` viene mancato esattamente quando `(x−y) mod 5 = 0`. `total` conta tutti i vettori, `missed` conta i mancati rilevamenti, `caught=total−missed`. Cinque coppie diagonali danno cinque mancati rilevamenti.

L'unità più lunga verifica 441 combinazioni, memorizza 441 byte di verdetti per un solo SHA-256. I contatori non superano 441, il modulo dell'espressione di impacchettamento non supera 46, il massimo modulo della divisione è 64. Bastano interi con segno a 32 bit. I risultati riguardano gli intervalli indicati, un singolo errore fissato e l'enumerazione completa di varianti equiprobabili. La generalizzazione a un protocollo reale richiederebbe di giustificare la distribuzione delle chiamate e l'indipendenza delle verifiche.

## Calcoli rinviati


| Calcolo | Che cosa è già definito | Quali dati permetteranno di ottenere un risultato univoco |
|---|---|---|
| M5. Ondate di contraffazioni | Per una singola contraffazione economica a costo nullo `π=m_s/(L+1)` e `H*=R(1/π−1)`. Per esempio, con `L=36, m_s=2` la soglia è pari a 17,5R | Per l'ondata occorre fissare la distribuzione congiunta delle verifiche e la transizione del saldo con più rilevamenti simultanei, compreso il momento dell'addebito e la disponibilità delle ricompense dell'ondata precedente. Con `π=1/2` un campione comune per due errori uguali lascia passare entrambi con probabilità 1/2, campioni indipendenti — con probabilità 1/4. L'analogia proposta con `exit-scam-a` richiede anche di chiarire se si conserva la sua probabilità separata di assegnazione della verifica. (claude1, §1.3, §4.2 e §7.5, punto 3) (THREAT_MODEL, §1.8) |
| M7. Economia della rivelazione | Per un pagamento fisso R e il pagamento della prova solo nel ramo di successo è noto il ricavo di un singolo tentativo `p(R−Pe)−c_view−c_commit` | Per il limite generale ε servono il costo del tentativo scartato, la regola di pagamento in caso di più successi e la legge congiunta degli esiti dei candidati all'esame comune. Il numero di chiavi di per sé non determina queste grandezze. ODU con prova obbligatoria di ogni tentativo dà un altro budget, e in T4 il pagamento dipende anche dall'entità del miglioramento. (claude2, §5.3) (critic_claude, §2.4) (critic_gpt, analisi di ODU) |
| M18. Pagamenti e ripristino | Sono date l'atomicità dell'accettazione, l'unicità dell'estinzione del diritto nella storia canonica e l'elenco degli scenari | Per contare i percorsi servono una tabella delle transizioni al cambio di ramo, un criterio di finalità, regole di ripristino in caso di scomparsa e ritorno dei dati e un limite finito del numero di presentazioni ripetute. Automi diversi possono soddisfare gli stessi invarianti e dare numeri diversi di pagamenti su storie intermedie. (gpt1, §1 e §7) (critic_gpt, «Completezza, ripristino e prezzo») |
