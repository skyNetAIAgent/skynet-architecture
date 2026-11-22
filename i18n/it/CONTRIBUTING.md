# Come contribuire

[English](../../CONTRIBUTING.md) · [中文](../zh/CONTRIBUTING.md) · [Español](../es/CONTRIBUTING.md) · [Français](../fr/CONTRIBUTING.md) · [Deutsch](../de/CONTRIBUTING.md) · **Italiano** · [Русский](../ru/CONTRIBUTING.md) · [Português](../pt/CONTRIBUTING.md) · [العربية](../ar/CONTRIBUTING.md)

Grazie per voler aiutare. Qui conta la precisione, non la quantità: una falla trovata con uno scenario concreto vale più di dieci pagine di ragionamenti generali.

## Cosa portare

- **Un attacco al progetto attuale.** Uno scenario: chi agisce, cosa fa, cosa ottiene, perché la rete non se ne accorge. Indicate la sezione di [CURRENT_DESIGN](../../docs/CURRENT_DESIGN.md).
- **Una soluzione a una [questione aperta](../../docs/OPEN_QUESTIONS.en.md).**
- **Una fonte**: un articolo, un protocollo o un progetto che risolve parte di un problema, con versione, data e ciò che **non** dimostra per il nostro caso.
- **Un calcolo dei costi** o la correzione di uno esistente.
- **Una correzione di traduzione**: un'imprecisione in una traduzione della base (tramite il file di errata).
- **Un compito per l'agente di ricerca**: un calcolo che risponda a parte di una questione aperta (vedere [tasks/README.md](../../tasks/README.md)).
- **Potenza di calcolo**: se non avete un assistente di IA né tempo per scrivere, fate girare l'[agente di ricerca](AGENT.md) sul vostro computer o telefono.

## Come presentarlo

Aprite una issue e iniziate il titolo con un'etichetta:

| Etichetta | Per |
|---|---|
| `[Attack]` | Un modo per ingannare o disturbare la rete |
| `[Q<N>]` | Una proposta per la questione aperta N |
| `[Source]` | Un articolo o progetto utile |
| `[Cost]` | Una stima dei costi o correzione di numeri |
| `[Translation]` | Un'imprecisione di traduzione |
| `[Task]` | Un calcolo per l'agente di ricerca |

Nel testo indicate:

1. Cosa è garantito e sotto quali ipotesi.
2. Il meccanismo.
3. Gli attacchi noti e cosa resta.
4. Il costo, contrassegnato [calcolo] o [misurato].
5. Quali dei sei [requisiti](REQUIREMENTS.md) sono soddisfatti e quali no.

Le pull request ai documenti di lavoro (`docs/`) sono benvenute. Se cambiate lo stato di un punto, spiegate perché. Issue e pull request possono essere scritte in qualsiasi lingua del repository.

## Regole

- **La base non cambia.** Una pull request che modifica il manifesto, i requisiti, il README o le loro impronte non sarà accettata. Vedere [CORE.md](../../CORE.md).
- Un calcolo non viene spacciato per una misurazione, né una proposta per una decisione.
- Non pubblicate chiavi, password, dati personali o indirizzi di computer.
- Siate cortesi e concreti. Criticate le idee, non le persone.

Se lavorate con un assistente di IA, dategli [AGENTS.md](AGENTS.md). L'autore di una issue è responsabile dell'esattezza del suo testo.
