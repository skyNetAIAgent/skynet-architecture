<!-- translation of docs/CONNECT.md, source sha256: 125af61335dde49176b5b023903489a40b1792ebe8e8eb04a960681206774db9 -->

# Come partecipare

[English](../../docs/CONNECT.md) · [中文](../zh/CONNECT.md) · [Español](../es/CONNECT.md) · [Français](../fr/CONNECT.md) · [Deutsch](../de/CONNECT.md) · **Italiano** · [Русский](../ru/CONNECT.md) · [Português](../pt/CONNECT.md) · [العربية](../ar/CONNECT.md)

Potete aiutare a progettare SkyNet con il vostro computer o telefono. L'agente di ricerca è un
piccolo programma open source: riceve calcoli di ricerca firmati, li esegue nel tempo libero del
vostro dispositivo e pubblica i risultati. Non serve alcun account, da nessuna parte. **In questa
fase non sono previste ricompense**: è un aiuto volontario per la ricerca, non la rete SkyNet stessa.

## Installazione

| Il vostro dispositivo | Cosa fare |
|---|---|
| **Windows 10/11** (64 bit) | Scaricate `SkyNetAgentSetup-<version>-amd64.exe` dalla [versione più recente](https://github.com/skyNetAIAgent/skynet-architecture/releases/latest) ed eseguitelo. Windows mostra «Windows ha protetto il PC» perché il file non ha una firma del codice: scegliete **Ulteriori informazioni**, poi **Esegui comunque**. |
| **Linux** (x86_64 o ARM64) | Scaricate `skynet-agent-linux-install-<version>.sh` dalla [versione più recente](https://github.com/skyNetAIAgent/skynet-architecture/releases/latest) ed eseguite `sh skynet-agent-linux-install-<version>.sh`. |
| **Android 7.0+** (64 bit) | Scaricate `skynet-agent.apk` dalla pagina delle versioni, apritelo e consentite l'installazione da questa fonte. L'app funziona solo mentre il telefono è in carica. |

macOS e iPhone non sono supportati.

Il programma di installazione avvia l'agente subito e lo imposta per avviarlo di nuovo dopo un
riavvio (su Windows potete deselezionare questa opzione; su Android premete **Avvia** una volta).
Dopodiché non c'è altro da fare: l'agente si aggiorna da solo (solo a versioni firmate dal progetto),
prende i compiti e pubblica i risultati autonomamente. Trova da solo un nodo completo sulla vostra
rete locale, se ce n'è uno.

Gli agenti attualmente online sono elencati su http://62.213.14.254:8790/agents: sistema, processore,
memoria, scheda grafica, versione e unità calcolate. Non viene mostrato alcun indirizzo IP né nome del
computer.

## Cosa usa e cosa non fa mai

- Un core del processore alla priorità più bassa per impostazione predefinita, così i vostri
  programmi non vengono rallentati. Su un portatile non lavora a batteria, a meno che non glielo
  consentiate.
- Non esegue mai codice che proviene da un compito, non invia mai i vostri file e non richiede
  diritti di amministratore. Ogni risultato è un piccolo record pubblico firmato con la chiave del
  vostro dispositivo.
- Per mettere in pausa o fermare: la cartella **SkyNet Agent** nel menu Start su Windows,
  `skynet-agent pause` / `stop` su Linux, il pulsante **Ferma** nell'app.
- Per rimuoverlo: **SkyNet Agent → Disinstalla** su Windows, `skynet-agent uninstall --yes` su Linux,
  disinstallate l'app su Android.

Dettagli: [la guida dell'agente](AGENT.md).

## Aiutate con le idee, non solo con il calcolo

Il principale problema aperto del progetto è come verificare i calcoli in modo che imbrogliare non
convenga mai, a basso costo, senza depositi né multe. Se voi, o il vostro assistente di IA, avete
un'idea o avete trovato una falla, consultate la [bacheca dei compiti](BOARD.md), la
[roadmap](ROADMAP.md) e le [domande aperte](OPEN_QUESTIONS.md).
