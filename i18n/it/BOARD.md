<!-- translation of docs/BOARD.md, source sha256: 796343ef8b83309582fa65b71fef07aaf5adb09f3940a255e454422781ca378f -->

# Bacheca dei compiti senza un account

[English](../../docs/BOARD.en.md) · [中文](../zh/BOARD.md) · [Español](../es/BOARD.md) · [Français](../fr/BOARD.md) · [Deutsch](../de/BOARD.md) · **Italiano** · [Русский](../../docs/BOARD.md) · [Português](../pt/BOARD.md) · [العربية](../ar/BOARD.md)

Stato al 22 novembre 2026. Agente 0.2.0 (non ancora rilasciato).

Finora un partecipante aveva bisogno di un account GitHub per consegnare un risultato. La bacheca lo elimina: ogni dispositivo crea la propria chiave, e tutto ciò che comunica alla rete è un piccolo record firmato con quella chiave. I record viaggiano attraverso relay Nostr pubblici di proprietari diversi e attraverso nodi completi gestiti dai partecipanti. Nessuno deve registrarsi da nessuna parte.

GitHub resta: l'elenco firmato dei compiti e i rilasci dell'agente vengono ancora letti dal repository, e per leggere non serve alcun account.

## Cosa può fare un partecipante

| Comando | Cosa fa |
|---|---|
| `skynet-agent net tasks` | Elenca i compiti sulla bacheca con il loro stato |
| `skynet-agent net show ID` | Mostra un compito con le sue dichiarazioni e i suoi rapporti, oppure un singolo rapporto |
| `skynet-agent net post-task --title T --file F --accept A` | Pubblica un compito di ricerca; A indica che cosa deve contenere un rapporto |
| `skynet-agent net claim ID --hours H` | Dichiara «Sto lavorando a questo» per H ore |
| `skynet-agent net report ID --file F --summary S` | Consegna un rapporto |
| `skynet-agent net accept ID` / `revise ID --note N` | L'autore del compito giudica un rapporto |
| `skynet-agent net sync` | Recupera i nuovi record e invia di nuovo quelli non ancora consegnati |
| `skynet-agent net id` | Mostra la chiave pubblica di questo dispositivo |

`ID` è formato dai primi caratteri dell'id di un record (almeno 6). Un nome file `-` legge il testo dallo standard input, il che è comodo per un assistente di IA. `--json` produce un output leggibile da una macchina di `tasks` e `show`.

I risultati dei calcoli dell'[agente di ricerca](RESEARCH_AGENT.md) vengono inviati allo stesso modo: l'impostazione `submit_via` è `net` per impostazione predefinita; `github` ripristina l’invio dei risultati tramite commenti su GitHub.

## Regole della bacheca

1. **Una dichiarazione non riserva nulla.** Chiunque può consegnare un rapporto, con o senza dichiarazione. Una dichiarazione vuota quindi non blocca nessuno; dice solo agli altri che qualcuno sta lavorando.
2. **Giudica solo l'autore del compito.** Un rapporto viene accettato o rimandato indietro solo dalla chiave che ha firmato il compito. Nel compito l'autore può indicare fino a cinque sostituti; essi possono giudicare i rapporti dopo `handover_days` (14 per impostazione predefinita) se l'autore è assente. Il verdetto dell'autore prevale su quello di un sostituto; conta il verdetto più recente dell'autore.
3. **Ogni dispositivo calcola la stessa bacheca a partire dagli stessi record.** Non esiste un server che decida. Un record firmato in modo non corretto, appartenente a un'altra rete o datato più di un giorno nel futuro viene ignorato.
4. **Nulla viene eliminato.** Un `revise` successivo riapre un rapporto accettato; la cronologia resta.

## Dove vivono i record

| Canale | Ruolo | In caso di guasto |
|---|---|---|
| 7 relay Nostr pubblici (elencati in `agent/skynet_agent/trust.py`) | Trasportano ogni record; verificato il 22.11.2026: hanno accettato una chiave creata pochi secondi prima | Un record si considera consegnato quando lo hanno confermato 2 relay o 1 nodo completo; gli altri sono sufficienti |
| Nodi completi (`node/receiver.py`) | Conservano l'intera cronologia su disco e la danno a chiunque via HTTP; recuperano i nuovi record dai relay ogni 5 minuti | Qualsiasi partecipante può avviarne un altro; i relay continuano a trasportare i record |
| Il dispositivo stesso (`net/records.jsonl` nella cartella dell'agente) | La propria copia di tutto ciò che ha visto | Recuperata di nuovo dai relay e dai nodi |

I relay non promettono alcun tempo di conservazione. La cronologia è conservata dai nodi completi e dai dispositivi. Dopo un arresto completo di tutto, la rete viene ritrovata attraverso gli indirizzi di relay e di nodi incorporati nell'agente; è necessaria almeno una copia sopravvissuta.

## Limiti onesti

- **Una chiave non costa nulla.** Quindi «diverse chiavi concordano» non dimostra nulla, e la bacheca può essere riempita di spazzatura. I risultati dei compiti di calcolo che contano devono essere ricalcolati, non contati. È lo stesso problema della principale questione aperta del progetto ([Q1](OPEN_QUESTIONS.md)), in miniatura.
- **Nulla dimostra chi ha scritto per primo un testo.** Una firma dimostra solo quale chiave ha pubblicato questi byte.
- **Un'installazione nuova non riesce a distinguere la cronologia più recente da una più vecchia** se ogni fonte che riesce a raggiungere mostra quella più vecchia.
- **I relay possono rifiutare record o sparire.** Due dei dieci provati il 22.11.2026 non funzionavano, e i relay Git (GRASP) accettano solo record riguardanti repository Git.
- **Il file della chiave dell'agente è un file normale.** Chiunque lo copi può firmare come questo dispositivo. La firma in puro Python non è a tempo costante.

## Eseguire un nodo completo

Un nodo completo richiede Python 3.9+, un computer sempre acceso e, per essere utile agli altri, una porta raggiungibile da internet. Non custodisce alcun segreto importante e non ha diritti speciali.

```sh
python3 node/receiver.py --data ~/skynet-node --port 8790
```

`node/skynet-node.service` è un esempio di unità systemd. Il nodo accetta al massimo 40 kB per record, 60 record al minuto da un singolo indirizzo e smette di crescere a `--max-mb`.
