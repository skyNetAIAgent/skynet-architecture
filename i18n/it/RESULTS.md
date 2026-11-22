<!-- translation of results/README.md, source sha256: 45df5513ecce206740e2354af46f84e5f3ecf7faccd93a990f4a851df0f249c9 -->

# Risultati degli agenti di ricerca

[English](../../results/README.md) · [中文](../zh/RESULTS.md) · [Español](../es/RESULTS.md) · [Français](../fr/RESULTS.md) · [Deutsch](../de/RESULTS.md) · **Italiano** · [Русский](../ru/RESULTS.md) · [Português](../pt/RESULTS.md) · [العربية](../ar/RESULTS.md)

Questa cartella viene scritta da `tools/collect_results.py` a partire dai commenti pubblici dei risultati di
[agenti di ricerca](../../agent/README.md):

- `REPORT.md`: un riepilogo leggibile, con i riscontri verificati e i conflitti;
- `summary.json`: lo stesso, per ogni compito, per i programmi;
- `coverage.json`: quanti risultati concordanti ha ciascuna unità di ciascun compito. Gli agenti lo leggono per
  preferire le unità che non hanno ancora risultati; è solo un suggerimento e non richiede firma;
- `ai/`: le risposte dei modelli di IA locali dei partecipanti, generate da macchine e non verificate.

Un'unità è confermata quando il numero di account GitHub diversi richiesti dal compito
ha pubblicato lo stesso hash del risultato. Ogni "hit" segnalato della ricerca exit-scam viene ricalcolato
esattamente dal raccoglitore prima di essere elencato. Cosa significano i compiti:
[tasks/README.md](TASKS.md).

Non è stato ancora raccolto nulla dai partecipanti. Una prima esecuzione dell'intero elenco di compiti su un
computer, non ancora confermata da nessun altro, è descritta in [FIRST_RUN.md](FIRST_RUN.md).
