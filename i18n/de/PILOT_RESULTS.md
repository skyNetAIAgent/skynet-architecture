<!-- translation of docs/PILOT_RESULTS.md, source sha256: 73d115fb10056d64e4cee61811cfd158629d32514eaa0ca4ca9c7939d3700489 -->

# Was im Pilotprojekt geprüft wurde

[English](../../docs/PILOT_RESULTS.en.md) · [中文](../zh/PILOT_RESULTS.md) · [Español](../es/PILOT_RESULTS.md) · [Français](../fr/PILOT_RESULTS.md) · **Deutsch** · [Italiano](../it/PILOT_RESULTS.md) · [Русский](../../docs/PILOT_RESULTS.md) · [Português](../pt/PILOT_RESULTS.md) · [العربية](../ar/PILOT_RESULTS.md)

Vor der Wahl einer Architektur ohne Koordinatoren stellte das Projekt ein **vertrauenswürdiges Pilotprojekt** mit zentralem Server
und mehrere Forschungsprototypen zur Überprüfung zusammen. Im Folgenden steht, was tatsächlich ausgeführt und gemessen wurde
und wo die Grenzen dieser Ergebnisse verlaufen. Der Quelltext des Pilotprojekts ist in diesem Repository nicht enthalten.

Das Pilotprojekt ist ein geschlossenes System mit einem vertrauenswürdigen Betreiber. Es ist nicht gegen Betrug in einem offenen Netz
geschützt und setzt die Zielarchitektur nicht um. Alle Auszahlungen darin sind Übungsauszahlungen (TEST_CREDIT, ohne Abhebung).

## Inferenz und Abrechnung

| Was | Ergebnis |
|---|---|
| Server-Kreislauf | API, Warteschlange, PostgreSQL, Agent, getrennte Überprüfung des Ergebnisses und Übungsgutschrift in einer Transaktion. Erneutes Senden ergibt keine zweite Gutschrift; eine veraltete Aufgaben-Lease wird abgelehnt |
| Schwache GPU | Qwen2.5-0.5B-Instruct Q4_K_M über llama.cpp (Vulkan) auf der integrierten Intel Arrow Lake-P: angenommene Aufgabe, abgelehnte Antwortunterschiebung |
| Zweite GPU | Qwen3-4B-Instruct-2507 Q4_K_M auf RTX 2060 6 GB: alle Schichten auf der GPU, etwa 2,4 GiB VRAM, Median 73,8 Token/s auf einem kurzen Profil |
| Modell auf mehreren Computern | Die Schichten von Qwen3-4B wurden über das lokale Netz zwischen der RTX 2060 und der GPU eines Teilnehmers verteilt (RTX 4070 Laptop, dann Intel Arrow Lake-P). Der Teilnehmer erhielt nur den zugewiesenen Teil der Gewichte in den Speicher. Das Paar RTX 2060 + RTX 4070 Laptop ergab etwa 38–40 Token/s gegenüber 69,5 auf einer einzelnen RTX 2060: zusätzlicher Speicher garantiert keine Beschleunigung |
| Wiederherstellung | Pause, Wiederaufnahme und automatische Wiederherstellung der Gruppe nach einem Tunnelabriss |

Die Überprüfung im Pilotprojekt ist die Wiederholung der Generierung auf **derselben vertrauenswürdigen** GPU. Das ist kein Beweis für die Ehrlichkeit
eines unbekannten Knotens.

## Prototypen zur Überprüfung von Berechnungen

| Was | Ergebnis | Grenze |
|---|---|---|
| Groth16 für zwei ganzzahlige matmul + Solidity-Verifier | Echte Beweise und eine einmalige Auszahlung in einer lokalen EVM | Kleine Aufgabe auf der CPU |
| RISC Zero für eine Q4_K-Zeile der Qwen-Projektion auf realen Daten | Beweis 22 min 10 s, Überprüfung 117 ms, Eingaben 11,7 KB | Eine Zeile, nicht der ganze Graph; weit über dem Budget |
| Paket aus acht Zeilen in der zkVM | 350 ms Ausführung gegenüber 19,8 µs nativ (~17 700×) | Ohne Erstellung des Beweises |
| Cartesi: Streit um ein Qwen-Ergebnis | Die Unterschiebung eines Bits wurde gefunden; der Streit umfasste 93 Transaktionen, 5,8–6,3 Millionen Gas | Erfordert einen rechtzeitigen ehrlichen Anfechter |
| Vollständige Wiederholung der Zeilenarithmetik in der EVM | 14,1 Millionen Gas pro Einreichung | Eine Zeile |
| Automatische Auditoren | Ein externer Auditor widerlegte einen falschen Vektor trotz zweier zustimmender Auditoren | Ohne Beobachter ging der Fehler nach der optimistischen Regel durch |
| Absprache zwischen Ausführendem und Prüfer | Erhielten eine Auszahlung für ein falsches Ergebnis | Zeigt, warum die Abstimmung der Prüfer keine Garantie ist |

## Was es nicht gab

- Verteiltes Training.
- Harte Hardware-Quoten für CPU/GPU/RAM/VRAM.
- Echte Geldauszahlungen.
- Überprüfung auf unabhängiger Hardware in einem offenen Netz.
- Energiemessungen.
- Experimente zur neuen Architektur ohne Koordinatoren: sie ist bislang nur entworfen.
