<!-- translation of tasks/README.md, source sha256: 761301bce18193a8aa61cf3fb87ae267379898b5e4164ffab7e23094d1ec08b5 -->

# Compiti per gli agenti di ricerca

[English](../../tasks/README.md) · [中文](../zh/TASKS.md) · [Español](../es/TASKS.md) · [Français](../fr/TASKS.md) · [Deutsch](../de/TASKS.md) · **Italiano** · [Русский](../ru/TASKS.md) · [Português](../pt/TASKS.md) · [العربية](../ar/TASKS.md)

Questa cartella contiene il lavoro svolto dagli [agenti di ricerca](../../agent/README.md):

- [`index.json`](../../tasks/index.json): l'elenco corrente dei compiti;
- `index.json.sig`: la sua firma (gli agenti ignorano un elenco senza una firma valida);
- [`context/`](../../tasks/context): testi congelati che le domande dell'IA citano.

I risultati compaiono come commenti nella issue di tracciamento di ciascun compito e sono riassunti in
[`results/`](../../results) da `tools/collect_results.py`.

## Che cos'è un compito

Un compito è un dato: il nome di un calcolo incorporato nell'agente (un «kernel»), i suoi
parametri e il numero di parti indipendenti («porzioni») in cui il lavoro è suddiviso. Un compito
non può contenere codice. Un nuovo tipo di calcolo richiede una nuova versione firmata dell'agente.

```json
{"id": "exit-a-honest-check", "kernel": "exit-scam-a", "kernel_version": 1,
 "units": 256, "redundancy": 2, "issue": 12,
 "params": {"H0": 1200, "q": [0, 1], "cap_third": false, "batches": 2, "n_max": 200,
            "sizes": {"mode": "grid", "points": 48}}}
```

Non c'è alcun pianificatore. Ogni agente sceglie una porzione casuale che non ha ancora fatto. Che più agenti
finiscano sulla stessa porzione è voluto: tutti i calcoli incorporati sono aritmetica intera esatta, quindi
un lavoro identico produce cifre identiche su ogni dispositivo, e una porzione conta come confermata quando
`redundancy` account GitHub diversi pubblicano la stessa impronta. Impronte diverse per una porzione
sono un conflitto che un responsabile risolve ricalcolandola.

## Kernel dell'agente 0.1

| Kernel | Cosa calcola | Sorgente |
|---|---|---|
| `selftest@1` | Un carico di lavoro fisso con calcoli su numeri interi; ogni dispositivo deve restituire lo stesso digest | [selftest.py](../../agent/skynet_agent/kernels/selftest.py) |
| `exit-scam-a@1` | Pagamento atteso esatto di un partecipante che presenta risultati falsi e se ne va, su una famiglia di strategie; segnala le strategie che battono l'uscita onesta | [exit_scam_a.py](../../agent/skynet_agent/kernels/exit_scam_a.py) |
| `lottery-b@1` | Probabilità esatta di un mese o trimestre in perdita quando vengono pagati solo i compiti controllati | [lottery_b.py](../../agent/skynet_agent/kernels/lottery_b.py) |
| `ai-answer@1` | Facoltativo: una domanda per un modello di IA locale eseguito dal partecipante | [ai_answer.py](../../agent/skynet_agent/kernels/ai_answer.py) |

Ogni file sorgente inizia con il modello esatto che implementa, così chiunque può ricalcolare un
risultato in modo indipendente.

## I compiti pubblicati ora, e perché

Riguardano tutti la principale questione aperta del progetto: si può rendere l'imbroglio inutile
a basso costo ([OPEN_QUESTIONS, Q1](../../docs/OPEN_QUESTIONS.en.md)).

| Compito | Domanda |
|---|---|
| `selftest-1` | La pipeline funziona sul vostro dispositivo? |
| `exit-a-honest-check` | Senza collusione, c'è un modo di guadagnare con i falsi prima di andarsene? Il progetto dice di no |
| `exit-a-uniform-h399`, `exit-a-uniform-h1200` | Con compiti piccoli uguali: a partire da quale quota di verificatori in collusione conviene andarsene con i falsi? La stima del progetto è circa il 91% |
| `exit-a-uniform-cap-h399` | Lo stesso con il limite proposto «al massimo un terzo dell'importo in sospeso impegnato in compiti in corso», in tre ondate |
| `exit-a-sizes-cap`, `exit-a-sizes-nocap` | Lo stesso quando i compiti possono avere qualsiasi dimensione, con e senza quel limite |
| `lottery-b-table` | Se vengono pagati solo i compiti controllati, quanto spesso un piccolo partecipante ha un mese in perdita? |
| `ask-variant-b-attack` | Per i modelli di IA locali: trovare un nuovo attacco a «la rete paga solo per il lavoro controllato» |

Sono calcoli sulle regole così come scritte nei documenti di progettazione. Non sono
misurazioni dell'hardware né esperimenti con la rete. I compiti di misurazione (per
esempio, se l'inferenza con aritmetica intera dà gli stessi bit su schede grafiche diverse) saranno
pubblicati solo dopo che i responsabili del progetto apriranno gli esperimenti.

## Quattro compiti nell'elenco 2

Questi compiti richiedono la sequenza di rilascio 5 o successiva dell'agente. I nove compiti
originali mantengono i loro ID così che il lavoro già in corso possa essere completato. Ogni nuova porzione restituisce
frazioni esatte come stringhe decimali, ad esempio `3/10`.

| Compito | Come leggere una porzione |
|---|---|
| `exit-campaign-b-grid` | Un partecipante dovrebbe incassare o rischiare il proprio saldo in sospeso sul lavoro falso? Ogni punto riporta il miglior guadagno atteso rispetto all'incasso, quanti falsi presentare prima (zero significa fermarsi) e se il guadagno è positivo. Confrontare le quote di collusione a parità di saldo, frequenza dei controlli, numero di verificatori, limite di ondate e orizzonte. |
| `apprentice-seats-grid` | Quanto possono raccogliere le chiavi della coalizione da un insieme fisso di posti da apprendista? Ogni riga riporta il numero di chiavi della coalizione, le ricompense attese per un'epoca e per tutte le epoche, la quota onesta dei posti occupati e la probabilità che nessuna chiave onesta ottenga un posto. |
| `lottery-adaptive-grid` | Quanto spesso un partecipante onesto perde denaro quando i controlli sono rari quanto la griglia consente? Una porzione realizzabile riporta la frequenza dei controlli, le probabilità di una perdita e di nessun pagamento per un mese e un trimestre, e il carico di lavoro mensile atteso dei verificatori. Un punto irraggiungibile significa che anche la frequenza più alta disponibile dà meno di 60 controlli attesi. |
| `token-certificate-grid` | I limiti di gruppo possono certificare il token con il punteggio più alto con meno moltiplicazioni? Ogni porzione verifica i vincitori di una matrice di interi con seme rispetto a una scansione completa e riporta le moltiplicazioni e le righe di pesi lette, sommate sui vettori di query. Il rapporto verifica/scansione completa è inferiore a uno in caso di risparmio e superiore a uno in caso di lavoro extra. Esclude la costruzione dell'indice e la ricerca del vincitore dichiarato. Le matrici sono casuali, quindi non si prevede alcun risparmio (una prima esecuzione ha trovato circa lo 0.8% di lavoro in più rispetto a una scansione completa); queste 20 porzioni sono una linea di base per esecuzioni successive sui pesi di un modello reale. |

## Proporre un compito

Aprite una issue intitolata `[Task] …` e dite:

1. la domanda a cui risponde il calcolo e a quale questione aperta appartiene;
2. il modello esatto, così che possa essere ricalcolato in modo indipendente;
3. quale kernel e quali parametri lo realizzerebbero, oppure cosa deve calcolare un nuovo kernel;
4. come verrebbe notato un risultato sbagliato o falsificato.

I responsabili controllano il compito con `tools/sign_tasks.py --check`, lo aggiungono a `index.json` e firmano
l'elenco. Solo chi possiede la chiave di rilascio può firmare; vedere
[docs/RESEARCH_AGENT.md](RESEARCH_AGENT.md).
