# SkyNet: progettazione aperta dell'architettura

[English](../../README.md) · [中文](../zh/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · [Deutsch](../de/README.md) · **Italiano** · [Русский](../ru/README.md) · [Português](../pt/README.md) · [العربية](../ar/README.md)

## Che cos'è questo repository

Qui si progetta l'architettura di SkyNet: una rete distribuita in cui i modelli di IA funzionano e imparano sui computer dei partecipanti. I partecipanti mettono a disposizione della rete le proprie risorse di calcolo inutilizzate e ricevono in cambio crediti, mentre chi non ha hardware potente ottiene un accesso economico all'IA.

È un repository di **ricerca**. Qui non c'è un software finito. Contiene:

- il [manifesto](MANIFESTO.md): perché serve la rete, come deve essere e le Leggi di SkyNet;
- i [requisiti obbligatori](REQUIREMENTS.md), che non cambiano;
- il [progetto attuale dell'architettura](../../docs/CURRENT_DESIGN.md) con le indicazioni «deciso», «proposto» e «aperto» (in russo);
- le [questioni aperte](../../docs/OPEN_QUESTIONS.en.md) su cui serve aiuto (in inglese);
- [cosa è stato verificato nel progetto pilota](../../docs/PILOT_RESULTS.md) e cosa no (in russo);
- le [regole di partecipazione](CONTRIBUTING.md) e un'[introduzione per gli assistenti di IA](AGENTS.md);
- il [programma-agente](AGENT.md): un piccolo programma per chi non ha un assistente di IA.

## Per chi

- **Ingegneri di sistemi distribuiti, crittografi, ricercatori di ML.** I problemi principali si trovano all'incrocio di questi campi: verifica economica dei calcoli, protezione dalla collusione, ripristino di una rete senza centro.
- **Proprietari di hardware** (schede grafiche, server, PC domestici). Il loro punto di vista su guadagno e costo dell'elettricità è necessario perché l'economia funzioni nella pratica.
- **Chi lavora con un assistente di IA.** Al vostro modello (Claude, ChatGPT, DeepSeek e altri) basta leggere [AGENTS.md](AGENTS.md) per entrare nel contesto e iniziare a lavorare.
- **Chi vuole semplicemente aiutare con il proprio computer o telefono.** Non servono conoscenze particolari: il lavoro lo fa il [programma-agente](AGENT.md).

## Il senso

Oggi non tutti hanno accesso a un'IA potente: lo impediscono il prezzo, le restrizioni geografiche e politiche, i blocchi dei servizi. Allo stesso tempo il mondo è pieno di schede grafiche e computer inattivi. SkyNet deve unire le due cose: una rete senza proprietario né server centrale, difficile da spegnere o bloccare, che ritrova se stessa dopo uno spegnimento totale, pianifica il proprio addestramento, paga equamente ciascuno per il lavoro utile verificato e serve le persone, non la guerra e la distruzione.

## La parte più difficile, onestamente

La condizione principale è che **ingannare la rete sia inutile o causi una perdita, e che la verifica dell'onestà sia economica**; altrimenti partecipare non conviene. Una soluzione che soddisfi in modo dimostrato questa condizione in caso di collusione **non esiste ancora**. Ci sono candidati solidi e decine di attacchi analizzati, ma i meccanismi chiave non sono stati costruiti né misurati. Lo stato attuale è sempre descritto in [CURRENT_DESIGN](../../docs/CURRENT_DESIGN.md) e [OPEN_QUESTIONS](../../docs/OPEN_QUESTIONS.en.md). Se sapete risolvere anche uno solo di questi problemi, abbiamo bisogno di voi.

## Come partecipare

1. Leggete il [manifesto](MANIFESTO.md) e i [requisiti](REQUIREMENTS.md).
2. Scegliete una questione in [OPEN_QUESTIONS](../../docs/OPEN_QUESTIONS.en.md) o un attacco al [progetto attuale](../../docs/CURRENT_DESIGN.md).
3. Aprite una issue o una pull request secondo le [regole](CONTRIBUTING.md). La cosa più preziosa: una falla trovata con un esempio concreto e una soluzione con il costo calcolato.

Se lavorate con un assistente di IA, ditegli: *«Studia questo repository seguendo AGENTS.md e aiutami con la questione N di OPEN_QUESTIONS.»*

**Non avete un assistente di IA?** Potete aiutare lo stesso. Installate il [programma-agente SkyNet](AGENT.md): un piccolo programma open source per Windows, macOS, Linux e Android. Controlla periodicamente questo repository, prende compiti di ricerca, li calcola sul vostro dispositivo nel tempo libero e pubblica i risultati. Si aggiorna da solo da questo repository, e soltanto a versioni firmate dal progetto. La partecipazione è volontaria: nella fase di ricerca non sono previste ricompense.

## La base immutabile

Il manifesto, i requisiti obbligatori e questo README costituiscono la base immutabile della rete (versione 1). Le loro impronte SHA-256 sono pubblicate in [CORE_HASHES.txt](../../CORE_HASHES.txt). L'edizione canonica è quella russa. I dettagli sono nel [manifesto](MANIFESTO.md) e in [CORE.md](../../CORE.md).

## Licenza

I testi della base sono distribuiti con licenza CC BY-ND 4.0 (si possono copiare, non si possono distribuire versioni modificate); gli altri documenti con CC BY 4.0. Vedere [LICENSE](../../LICENSE).
