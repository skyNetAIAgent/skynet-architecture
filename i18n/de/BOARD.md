<!-- translation of docs/BOARD.md, source sha256: d39c7e244fa5cab003fbc95ca98c920aea26cdd80da02612e439942a53d37e14 -->

# Aufgaben-Board ohne Konto

[English](../../docs/BOARD.en.md) · [中文](../zh/BOARD.md) · [Español](../es/BOARD.md) · [Français](../fr/BOARD.md) · **Deutsch** · [Italiano](../it/BOARD.md) · [Русский](../../docs/BOARD.md) · [Português](../pt/BOARD.md) · [العربية](../ar/BOARD.md)

Stand am 22. November 2026. Agent 0.2.0, veröffentlicht am 22. November 2026.

Bisher brauchte ein Teilnehmer ein GitHub-Konto, um ein Ergebnis abzugeben. Das Board schafft
das ab: Jedes Gerät erzeugt seinen eigenen Schlüssel, und alles, was es dem Netz mitteilt, ist
ein kleiner, mit diesem Schlüssel signierter Datensatz. Datensätze laufen über öffentliche
Nostr-Relays verschiedener Eigentümer und über von Teilnehmern betriebene Vollknoten. Niemand
muss sich irgendwo registrieren.

GitHub bleibt: Die signierte Aufgabenliste und die Agent-Releases werden weiterhin aus dem
Repository gelesen, und Lesen braucht kein Konto.

## Was ein Teilnehmer tun kann

| Befehl | Was er tut |
|---|---|
| `skynet-agent net tasks` | Die Aufgaben auf dem Board mit ihrem Status auflisten |
| `skynet-agent net show ID` | Eine Aufgabe mit ihren Meldungen und Berichten oder einen einzelnen Bericht anzeigen |
| `skynet-agent net post-task --title T --file F --accept A` | Eine Forschungsaufgabe auf dem Board veröffentlichen; A sagt, was ein Bericht enthalten muss |
| `skynet-agent net claim ID --hours H` | Für H Stunden melden: „Ich arbeite daran“ |
| `skynet-agent net report ID --file F --summary S` | Einen Bericht abgeben |
| `skynet-agent net accept ID` / `revise ID --note N` | Der Autor der Aufgabe beurteilt einen Bericht |
| `skynet-agent net sync` | Neue Datensätze abrufen und noch nicht zugestellte erneut senden |
| `skynet-agent net id` | Den öffentlichen Schlüssel dieses Geräts anzeigen |

`ID` sind die ersten Zeichen der Kennung eines Datensatzes (mindestens 6). Ein Dateiname `-`
liest den Text von der Standardeingabe; das ist für einen KI-Assistenten praktisch. `--json`
liefert maschinenlesbare Ausgabe von `tasks` und `show`.

Berechnungsergebnisse des [Forschungsagenten](RESEARCH_AGENT.md) werden auf dieselbe Weise
veröffentlicht: Die Einstellung `submit_via` ist standardmäßig `net`; `github` aktiviert wieder
die Übermittlung der Ergebnisse über GitHub-Kommentare.

## Regeln des Boards

1. **Eine Meldung reserviert nichts.** Jeder darf einen Bericht abgeben, mit oder ohne Meldung.
   Eine leere Meldung blockiert daher niemanden; sie sagt anderen nur, dass jemand arbeitet.
2. **Nur der Autor der Aufgabe beurteilt.** Ein Bericht wird nur von dem Schlüssel angenommen
   oder zurückgeschickt, der die Aufgabe signiert hat. In der Aufgabe darf der Autor bis zu fünf
   Stellvertreter benennen; diese dürfen nach `handover_days` (standardmäßig 14) Berichte
   beurteilen, wenn der Autor abwesend ist. Das Urteil des Autors hat Vorrang vor dem eines
   Stellvertreters; das neueste Urteil des Autors zählt.
3. **Jedes Gerät berechnet dasselbe Board aus denselben Datensätzen.** Es gibt keinen Server,
   der entscheidet. Ein Datensatz, der nicht korrekt signiert ist, zu einem anderen Netz gehört
   oder mehr als einen Tag in der Zukunft datiert ist, wird ignoriert.
4. **Nichts wird gelöscht.** Ein späteres `revise` öffnet einen angenommenen Bericht erneut;
   die Historie bleibt.

## Wo die Datensätze liegen

| Kanal | Rolle | Bei Ausfall |
|---|---|---|
| 7 öffentliche Nostr-Relays (aufgelistet in `agent/skynet_agent/trust.py`) | Tragen jeden Datensatz; geprüft am 22.11.2026: Sie nahmen einen Sekunden zuvor erzeugten Schlüssel an | Ein Datensatz gilt als zugestellt, wenn ihn 2 Relays oder 1 Vollknoten bestätigt haben; die übrigen genügen |
| Vollknoten (`node/receiver.py`) | Bewahren die gesamte Historie auf der Festplatte und geben sie jedem über HTTP; holen alle 5 Minuten neue Datensätze von den Relays | Jeder Teilnehmer kann einen weiteren starten; Relays tragen weiterhin Datensätze |
| Das Gerät selbst (`net/records.jsonl` im Ordner des Agenten) | Seine eigene Kopie von allem, was es gesehen hat | Wird erneut von Relays und Knoten abgerufen |

Relays versprechen keine Speicherdauer. Die Historie wird von Vollknoten und von den Geräten
gehalten. Nach einem vollständigen Stillstand von allem findet sich das Netz über die in den
Agenten eingebauten Relay- und Knotenadressen wieder; mindestens eine erhaltene Kopie ist nötig.

## Ehrliche Grenzen

- **Ein Schlüssel kostet nichts.** Daher beweist „mehrere Schlüssel bestätigen dasselbe Ergebnis“ nichts,
  und das Board kann mit Müll gefüllt werden. Wichtige Ergebnisse von Berechnungsaufgaben
  müssen neu berechnet, nicht gezählt werden. Das ist dasselbe Problem wie die wichtigste offene
  Frage des Projekts ([Q1](OPEN_QUESTIONS.md)), im Kleinen.
- **Nichts beweist, wer einen Text zuerst geschrieben hat.** Eine Signatur beweist nur, welcher
  Schlüssel diese Bytes veröffentlicht hat.
- **Eine frische Installation kann die neueste Historie nicht von einer älteren unterscheiden**,
  wenn jede erreichbare Quelle die ältere zeigt.
- **Relays können Datensätze ablehnen oder verschwinden.** Zwei der zehn am 22.11.2026
  ausprobierten funktionierten nicht, und Git-Relays (GRASP) nehmen nur Datensätze über
  Git-Repositorys an.
- **Die Schlüsseldatei des Agenten ist eine gewöhnliche Datei.** Wer sie kopiert, kann als
  dieses Gerät signieren. Die Signatur in reinem Python ist nicht in konstanter Zeit.

## Einen Vollknoten betreiben

Ein Vollknoten braucht Python 3.9+, einen Computer, der immer eingeschaltet ist, und, um
anderen zu nützen, einen aus dem Internet erreichbaren Port. Er enthält kein Geheimnis, das
zählt, und hat keine besonderen Rechte.

```sh
python3 node/receiver.py --data ~/skynet-node --port 8790
```

`node/skynet-node.service` ist eine Beispiel-Systemd-Unit. Der Knoten nimmt höchstens 40 kB pro
Datensatz, 60 Datensätze pro Minute von einer Adresse an und hört bei `--max-mb` auf zu wachsen.
