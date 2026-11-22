<!-- translation of results/FIRST_RUN.md, source sha256: 786aa2e462922d0a3a2ec06d0da0e26d246a2563867e215a11cfbf5a799bfe0a -->

# Prima esecuzione del primo elenco di compiti (un computer, non ancora confermata)

[English](../../results/FIRST_RUN.md) · [中文](../zh/FIRST_RUN.md) · [Español](../es/FIRST_RUN.md) · [Français](../fr/FIRST_RUN.md) · [Deutsch](../de/FIRST_RUN.md) · **Italiano** · [Русский](../ru/FIRST_RUN.md) · [Português](../pt/FIRST_RUN.md) · [العربية](../ar/FIRST_RUN.md)

Il 22 novembre 2026 ogni unità dell'elenco di compiti numero 1 è stata calcolata una volta su un singolo computer Windows con lo stesso codice eseguito dagli agenti: 702 unità, 15,5 ore-CPU, nessun errore. Un computer non è una conferma. I numeri che seguono diventano risultati del progetto solo quando altri partecipanti pubblicano gli stessi hash (vedere [README.md](RESULTS.md)).

## Andarsene con risultati falsi (kernel `exit-scam-a@1`, variante A del progetto)

Un partecipante con un importo H0 «in sospeso» invia risultati falsi in poche ondate rapide e se ne va. Se semplicemente se ne andasse, otterrebbe H0. La tabella indica la quota più bassa di verificatori in collusione a partire dalla quale qualche strategia della famiglia esaminata ha un pagamento atteso superiore a H0. Il modello esatto è all'inizio di [exit_scam_a.py](../../agent/skynet_agent/kernels/exit_scam_a.py).

| Compito | Strategie esaminate | Redditizio dalla quota di collusione | Miglior pagamento atteso lì |
|---|---:|---|---|
| `exit-a-honest-check`: nessuna collusione, qualunque dimensione del compito, due ondate | 92,169,600 | mai | 0.980 × H0 |
| `exit-a-uniform-h399`: compiti piccoli e uguali, 399 prezzi in sospeso, un'ondata | 7,600 | 0.892 (non a 0.890) | 1.0066 × H0 |
| `exit-a-uniform-h1200`: compiti piccoli e uguali, 1200 prezzi in sospeso, un'ondata | 22,800 | 0.908 (non a 0.906) | 1.0117 × H0 |
| `exit-a-uniform-cap-h399`: compiti piccoli e uguali, tre ondate, «al massimo un terzo in lavorazione» | 71,772,196 | 0.890 (non a 0.888) | 1.0059 × H0 |
| `exit-a-sizes-cap`: qualunque dimensione del compito, tre ondate, «al massimo un terzo in lavorazione» | 1,190,974,992 | 0.875 (non a 0.870) | 1.00004 × H0; 1.034 × H0 a 0.880 |
| `exit-a-sizes-nocap`: qualunque dimensione del compito, due ondate, senza quel limite | 69,148,800 | 0.800 (non a 0.780) | 1.218 × H0; 4.91 × H0 a 0.850 |

Cosa suggerisce:

- La stima del progetto «imbrogliare è in perdita finché chi è in collusione detiene meno di circa il 91%» deriva dalla media su un singolo risultato falso. Non tiene conto del fatto che un partecipante non può perdere più dell'importo in sospeso (non ci sono depositi né multe). Per chi se ne va, la perdita è limitata e il guadagno no, il che abbassa la soglia a circa l'87,5–89%.
- La regola proposta «al massimo un terzo dell'importo in sospeso in lavorazione contemporaneamente» è necessaria. Senza di essa, le ricompense non verificate della prima ondata aumentano l'importo in sospeso e consentono compiti più grandi nella seconda ondata, e la soglia scende a circa l'80%.
- Senza collusione non è stato trovato alcun modo redditizio di andarsene con risultati falsi.

Limiti: si tratta di un calcolo in un modello formale delle regole, non di una misurazione; la ricerca copre solo le famiglie elencate; la griglia delle quote di collusione ha passi da 0,002 a 0,02.

## Pagare solo per i compiti controllati (kernel `lottery-b@1`, variante B del progetto)

Probabilità che il reddito di un periodo sia inferiore al costo del lavoro svolto in esso, quando un compito viene controllato con probabilità 1/P e un compito controllato viene pagato P prezzi. Somme binomiali esatte.

| Compiti al mese | Controllati | Costo / prezzo | Mesi in perdita | Trimestri in perdita |
|---:|---|---:|---:|---:|
| 600 | 1 su 10 | 95% | 32.20% | 22.91% |
| 6,000 | 1 su 100 | 95% | 33.10% | 24.02% |
| 6,000 | 1 su 100 | 80% | 4.84% | |
| 60,000 | 1 su 100 | 95% | 10.47% | 1.55% |
| 200,000 | 1 su 100 | 95% | 1.15% | |
| 200,000 | 1 su 100 | 98% | 18.15% | |
| 600 | 1 su 100 | 95% | 44.49% | |

Con 600 compiti al mese e 1 su 100 controllati, non viene pagato proprio nulla nello 0,24% dei mesi. La tabella completa ha 360 celle; comparirà in `summary.json` quando gli agenti la pubblicheranno.
