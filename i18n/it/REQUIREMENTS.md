# Requisiti obbligatori di SkyNet

[English](../../REQUIREMENTS.md) · [中文](../zh/REQUIREMENTS.md) · [Español](../es/REQUIREMENTS.md) · [Français](../fr/REQUIREMENTS.md) · [Deutsch](../de/REQUIREMENTS.md) · **Italiano** · [Русский](../ru/REQUIREMENTS.md) · [Português](../pt/REQUIREMENTS.md) · [العربية](../ar/REQUIREMENTS.md)

*Versione 1, 22 novembre 2026. Edizione canonica, parte della base immutabile di SkyNet. Traduzione italiana; il [testo russo](../ru/REQUIREMENTS.md) è quello canonico.*

Questi requisiti, insieme al [manifesto](MANIFESTO.md) e alle Leggi di SkyNet, costituiscono la **base immutabile della rete**: non possono essere modificati con una votazione né per decisione dei creatori, degli sviluppatori o della maggioranza dei partecipanti. Una soluzione che violi anche un solo requisito non è adatta a SkyNet. Può essere discussa come ricerca, ma indicando chiaramente quale requisito viola.

## Le sei condizioni principali

| N. | Requisito | Come verificare una soluzione |
|---|---|---|
| R1 | **La rete è distribuita.** | I dispositivi di diversi partecipanti ne garantiscono insieme il funzionamento. La perdita di un qualsiasi nodo, di un qualsiasi server, anche di uno appartenente ai creatori del progetto, o di un sito di pubblicazione non impedisce agli altri di continuare. |
| R2 | **La rete conserva informazioni su se stessa su risorse pubbliche.** | Il software installato ottiene dall'esterno informazioni sufficienti a riconoscere la rete e trovare i nodi che ritornano. Queste informazioni sopravvivono allo spegnimento simultaneo di tutti i nodi. Le fonti sono più d'una. |
| R3 | **La rete ritrova se stessa e si ripristina dopo uno spegnimento totale.** | I programmi che ritornano si ritrovano da soli tramite risorse pubbliche, senza l'indirizzo di un coordinatore attivo e senza un elenco manuale di nodi. |
| R4 | **I partecipanti non possono ingannare la rete.** | Un'affermazione falsa non porta a un risultato accettato, a poteri altrui, a una ricompensa immeritata né a una storia riscritta. Si tiene conto della collusione e degli account multipli (Sybil). Per ogni soluzione si mostra con quali dati verificabili in modo indipendente la rete respingerà un'affermazione falsa. **Significato pratico:** l'inganno è inutile o causa una perdita, anche per un nuovo arrivato con il conto vuoto. |
| R5 | **Niente denaro in anticipo.** | Niente quote, niente depositi, niente multe addebitate sul conto. Depositi e multe allontanano i partecipanti. |
| R6 | **Partecipare conviene.** | Fornire risorse (GPU, VRAM, CPU, RAM, SSD, HDD) è redditizio. La verifica dell'onestà è economica: il suo costo va bene a tutti, in particolare ai proprietari di grandi impianti e di elettricità costosa. |

**R6 è il più importante.** Se la verifica dell'onestà richiede molto calcolo, partecipare smette di convenire e la rete perde il suo senso.

## Tipi di partecipanti

| Partecipante | Cosa fa |
|---|---|
| Con grandi risorse | Guadagna crediti sufficienti per le proprie esigenze e vende l'eccedenza ad altri partecipanti |
| Con hardware modesto | Guadagna meno di quanto spende per i modelli della rete e paga la differenza in criptovaluta o denaro |
| Senza hardware | Solo consumatore: paga per usare i modelli |

La stessa persona può essere sia fornitore di risorse sia utente.

## Altre condizioni adottate

- **Lo stato viene conservato.** I diritti confermati, gli obblighi, la storia dei compiti accettati, l'ultima versione accettata del modello e i dati per riprendere l'addestramento sopravvivono a un arresto totale. Ripetere un passo incompiuto non dà una seconda ricompensa.
- **Divisione della rete.** Quando le storie si contraddicono, i crediti contestati attendono la storia canonica. Uno stesso contributo non viene mai pagato due volte.
- **Siti e chiavi sostituibili.** La perdita di un account, di un mirror o di una chiave non impedisce per sempre il ripristino.
- **Decisioni verificabili dopo il riavvio.** Per i crediti, le modifiche delle regole e l'accettazione di una versione del modello si conservano dati con cui qualsiasi nodo può verificare il fondamento della decisione.
- **Minimo pubblico.** Il catalogo aperto contiene solo ciò che serve per la scoperta e la verifica dell'autenticità. Chiavi private, richieste private e dati personali non vengono pubblicati.
- **Riservatezza.** Le persone non vedono le richieste né i dati personali altrui.
- **Indipendenza dalle singole persone.** Nessuno ha diritti speciali, nemmeno lo sviluppatore. La rete stabilisce e modifica da sola il proprio piano di addestramento; è ammessa una votazione su un elenco di opzioni.
- **Semplicità per il partecipante.** Il partecipante non sceglie nulla a mano: installa il programma, accetta le condizioni, regola i cursori delle risorse e preme «Avvia».
- **Limiti di risorse separati.** CPU, GPU, RAM, VRAM e disco sono limitati separatamente; non si possono sommare in un'unica percentuale.
- **Tutta la potenza libera addestra.** La potenza non impegnata dalle richieste serve all'addestramento.
- **Modello di base.** All'inizio, Qwen con pesi aperti e licenza libera. Si può passare solo a un altro modello con pesi aperti e licenza libera.
- **Leggi di SkyNet.** Le quattro leggi del [manifesto](MANIFESTO.md) vincolano sia il comportamento del modello sia le regole della rete. La rete serve le persone e non viene costruita come strumento di guerra.

## Cosa non può sostituire i requisiti

- Il tempo di funzionamento, il numero di rapporti e il periodo dei checkpoint **non** sono fondamento di pagamento.
- La firma di un partecipante, anche insieme a quella di un altro nodo, **non** dimostra che una risorsa sia stata fornita: chi è in collusione firmerà qualsiasi cosa.
- Il campionamento statistico, la fiducia in un'enclave hardware (TEE) o un piccolo errore crittografico sono ipotesi. Si possono proporre, ma vanno nominate chiaramente, non spacciate per il rispetto di R4.
- Un test riuscito non dimostra la protezione dall'inganno.
