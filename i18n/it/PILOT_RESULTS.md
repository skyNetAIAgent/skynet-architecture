<!-- translation of docs/PILOT_RESULTS.md, source sha256: 73d115fb10056d64e4cee61811cfd158629d32514eaa0ca4ca9c7939d3700489 -->

# Cosa è stato verificato nel pilota

[English](../../docs/PILOT_RESULTS.en.md) · [中文](../zh/PILOT_RESULTS.md) · [Español](../es/PILOT_RESULTS.md) · [Français](../fr/PILOT_RESULTS.md) · [Deutsch](../de/PILOT_RESULTS.md) · **Italiano** · [Русский](../../docs/PILOT_RESULTS.md) · [Português](../pt/PILOT_RESULTS.md) · [العربية](../ar/PILOT_RESULTS.md)

Prima di scegliere l'architettura senza coordinatori, il progetto ha realizzato un **pilota fidato** con un server centrale
e diversi prototipi di ricerca per la verifica. Di seguito ciò che è stato realmente eseguito e misurato,
e dove passano i limiti di questi risultati. Il codice sorgente del pilota non è incluso in questo repository.

Il pilota è un sistema chiuso con un operatore fidato. Non è protetto dall'inganno in una rete aperta
e non implementa l'architettura obiettivo. Tutti i pagamenti al suo interno sono di prova (TEST_CREDIT, senza prelievo).

## Inferenza e contabilizzazione

| Cosa | Risultato |
|---|---|
| Circuito server | API, coda, PostgreSQL, agente, verifica separata del risultato e accredito di prova in un'unica transazione. L'invio ripetuto non produce un secondo accredito, il lease scaduto del compito viene rifiutato |
| GPU debole | Qwen2.5-0.5B-Instruct Q4_K_M tramite llama.cpp (Vulkan) sulla Intel Arrow Lake-P integrata: compito accettato, sostituzione della risposta rifiutata |
| Seconda GPU | Qwen3-4B-Instruct-2507 Q4_K_M su RTX 2060 6 GB: tutti i livelli sulla GPU, circa 2,4 GiB di VRAM, mediana 73,8 token/s su un profilo breve |
| Modello su più computer | I livelli di Qwen3-4B venivano distribuiti sulla rete locale tra la RTX 2060 e la GPU del partecipante (RTX 4070 Laptop, poi Intel Arrow Lake-P). Il partecipante riceveva in memoria solo la parte assegnata dei pesi. La coppia RTX 2060 + RTX 4070 Laptop ha dato circa 38–40 token/s contro 69,5 su una singola RTX 2060: memoria aggiuntiva non garantisce un'accelerazione |
| Ripristino | Pausa, ripresa e ripristino automatico del gruppo dopo l'interruzione del tunnel |

La verifica nel pilota è la ripetizione della generazione sulla **stessa GPU fidata**. Non è una prova dell'onestà
di un nodo sconosciuto.

## Prototipi di verifica dei calcoli

| Cosa | Risultato | Limite |
|---|---|---|
| Groth16 per due matmul intere + verificatore Solidity | Prove reali e un pagamento unico in una EVM locale | Compito piccolo su CPU |
| RISC Zero per una riga della proiezione Q4_K di Qwen su dati reali | Prova 22 min 10 s, verifica 117 ms, ingressi 11,7 KB | Una riga, non l'intero grafo; ben oltre il budget |
| Batch di otto righe nella zkVM | 350 ms di esecuzione contro 19,8 µs in modo nativo (~17 700×) | Senza costruzione della prova |
| Cartesi: disputa sul risultato di Qwen | Sostituzione di un bit rilevata; disputa di 93 transazioni, 5,8–6,3 milioni di gas | Richiede un contestatore onesto e tempestivo |
| Ripetizione completa dell'aritmetica della riga nella EVM | 14,1 milioni di gas per invio | Una riga |
| Auditor automatici | Un auditor di terze parti ha confutato un vettore falso nonostante due concordi | Senza un osservatore l'errore è passato secondo la regola ottimistica |
| Collusione tra esecutore e verificatore | Hanno ricevuto un pagamento per un risultato errato | Mostra perché il voto dei verificatori non è una garanzia |

## Cosa non è stato fatto

- Addestramento distribuito.
- Quote hardware rigide di CPU/GPU/RAM/VRAM.
- Pagamenti in denaro reale.
- Verifica su hardware indipendente in una rete aperta.
- Misurazione dell'energia.
- Esperimenti sulla nuova architettura senza coordinatori: per ora è solo progettata.
