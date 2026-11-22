# Introduzione per gli assistenti di IA

[English](../../AGENTS.md) · [中文](../zh/AGENTS.md) · [Español](../es/AGENTS.md) · [Français](../fr/AGENTS.md) · [Deutsch](../de/AGENTS.md) · **Italiano** · [Русский](../ru/AGENTS.md) · [Português](../pt/AGENTS.md) · [العربية](../ar/AGENTS.md)

Questo file è per qualsiasi modello (Claude, ChatGPT/Codex, DeepSeek, Gemini e altri) a cui una persona abbia chiesto aiuto con il progetto SkyNet. Leggilo per intero prima di rispondere. Rispondi all'utente nella sua lingua.

## Che cos'è il progetto

SkyNet è la ricerca e la progettazione dell'architettura di una rete distribuita in cui i modelli di IA funzionano e imparano sui computer dei partecipanti. I partecipanti guadagnano crediti per il lavoro utile verificato; chi non ha hardware ottiene un accesso economico all'IA. La rete serve le persone e segue le Leggi di SkyNet. Non c'è software finito: il repository è un luogo di lavoro comune sull'architettura.

## Ordine di lettura

1. [MANIFESTO.md](MANIFESTO.md): perché e come deve essere la rete, le Leggi di SkyNet.
2. [REQUIREMENTS.md](REQUIREMENTS.md): requisiti obbligatori. **La cosa più importante.**
3. [CURRENT_DESIGN.md](../../docs/CURRENT_DESIGN.md): progetto attuale e i suoi stati (in russo; leggilo o traducilo direttamente).
4. [OPEN_QUESTIONS.en.md](../../docs/OPEN_QUESTIONS.en.md): problemi aperti e idee già scartate.
5. [PILOT_RESULTS.md](../../docs/PILOT_RESULTS.md): cosa è stato realmente misurato (in russo).
6. [CONTRIBUTING.md](CONTRIBUTING.md): come presentare un contributo.
7. [ROADMAP.md](ROADMAP.md): la tabella di marcia del lavoro sulla protezione dall'inganno, con l'elenco di ciò che è fatto e di ciò che manca.

## La base immutabile

Il manifesto, i requisiti obbligatori e il README sono la base immutabile di SkyNet (vedi [CORE.md](../../CORE.md)). **Non proporre modifiche a questi file**, salvo registrare refusi nel file di errata. Se una soluzione è incompatibile con la base, di' chiaramente quale requisito viola; non riscrivere il requisito per adattarlo alla soluzione.

## Condizioni che non cambiano

Verifica ogni soluzione rispetto ai sei requisiti:

1. La rete è distribuita, senza centro e senza ruoli con diritti speciali.
2. La rete conserva informazioni su se stessa su risorse pubbliche.
3. Dopo lo spegnimento di tutti i nodi, la rete si ritrova tramite risorse pubbliche e si ripristina.
4. I partecipanti non possono ingannare la rete: l'inganno è inutile o causa una perdita, anche per un nuovo arrivato con il conto vuoto, in caso di collusione e con molti account.
5. Niente denaro in anticipo: niente depositi, quote o multe.
6. **Partecipare conviene** e la verifica dell'onestà è economica. Se la verifica divora il guadagno, la soluzione non va bene, per quanto sicura sia.

Tipi di partecipanti: con grandi risorse (vendono i crediti in eccesso), con hardware modesto (pagano la differenza), senza hardware (pagano soltanto). Il modello di base è Qwen. Le persone non vedono le richieste altrui. Il partecipante non configura nulla a mano tranne i cursori delle risorse. Le Leggi di SkyNet (dalla Zero alla Terza) sono vincolanti.

## Regole di lavoro

- **Separa il deciso, il proposto, il verificato e l'aperto.** Usa le indicazioni di CURRENT_DESIGN. Non trasformare una proposta in una decisione né un calcolo in una misurazione.
- **Non indebolire i requisiti in silenzio.** La fiducia nell'hardware (TEE), una maggioranza onesta, il campionamento statistico, una piccola probabilità di errore sono ipotesi; nominale chiaramente.
- **Per ogni schema di protezione, rispondi:** con quali dati verificabili in modo indipendente la rete respingerà un'affermazione falsa se l'esecutore e i verificatori sono in collusione? Se il caso onesto e quello falso danno gli stessi dati, lo schema non funziona.
- **Calcola il costo completo**: calcolo del prover e del verificatore, memoria, traffico, scritture sulla blockchain, tentativi ripetuti dopo i guasti. CPU, GPU, RAM e VRAM separatamente, mai in un'unica percentuale.
- **Non ripetere idee scartate** (elenco alla fine di OPEN_QUESTIONS) senza un argomento nuovo.
- **Attacca le tue stesse proposte.** Un controesempio onesto vale più di un tono sicuro.
- **Non inventare fonti, versioni o numeri.** Indica la fonte e i limiti della sua applicabilità.
- Non trovare una soluzione è un risultato onesto. Non dimostra l'impossibilità.

**Nove lingue.** Tutto ciò che è scritto per le persone (documenti, guide, schermate dei programmi) viene pubblicato in tutte le nove lingue del progetto: inglese, cinese, spagnolo, francese, tedesco, italiano, russo, portoghese e arabo. Una traduzione inizia con una riga che indica la sua fonte e l'hash della fonte; `python tools/check_translations.py` elenca le traduzioni mancanti o non aggiornate. Se traduzione e fonte differiscono, vale la fonte.

## Formato del contributo

1. Affermazione: cosa è garantito e sotto quali ipotesi.
2. Meccanismo: passi, dati, chi verifica cosa.
3. Attacchi: come aggirarlo e cosa resta (chiuso / in perdita / limitato / aperto).
4. Costo: stima contrassegnata [calcolo] o [misurato], con la fonte.
5. Quali requisiti sono soddisfatti e quali no.

Presentalo come issue o pull request secondo [CONTRIBUTING.md](CONTRIBUTING.md).

## L'agente di ricerca e i suoi risultati

Chi non ha un assistente di IA aiuta tramite l'[agente di ricerca](AGENT.md): un programma che prende compiti di calcolo da [tasks/](../../tasks/README.md) e pubblica risultati, riassunti in `results/`. Puoi aiutare proponendo un compito ben definito (un modello esatto che altri possano ricalcolare), verificando in modo indipendente un risultato pubblicato o spiegando che cosa significa un risultato per il progetto. Le risposte contrassegnate come generate da modelli locali sono testo non verificato: trattale come idee da controllare, non come fatti.

## Sicurezza

Non aggiungere al repository chiavi, password, dati personali o indirizzi di computer altrui. Non proporre attacchi a sistemi reali di terzi: l'analisi degli attacchi qui riguarda solo l'architettura di SkyNet. Non progettare usi della rete per la guerra, le armi o il danno alle persone: ciò contraddice le Leggi di SkyNet.
