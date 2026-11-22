<!-- translation of docs/OPEN_QUESTIONS.md, source sha256: 399c8aa1465bb599179acb60130b35242d9b6d03a63de6f016bc462e968b83eb -->

# Offene Fragen

[English](../../docs/OPEN_QUESTIONS.en.md) · [中文](../zh/OPEN_QUESTIONS.md) · [Español](../es/OPEN_QUESTIONS.md) · [Français](../fr/OPEN_QUESTIONS.md) · **Deutsch** · [Italiano](../it/OPEN_QUESTIONS.md) · [Русский](../../docs/OPEN_QUESTIONS.md) · [Português](../pt/OPEN_QUESTIONS.md) · [العربية](../ar/OPEN_QUESTIONS.md)

Hier sind die Aufgaben gesammelt, ohne deren Lösung SkyNet nicht funktionieren wird. Sie sind nach Wichtigkeit geordnet.
Zu jeder ist angegeben, was bereits bekannt ist und was **bereits verworfen wurde**, damit man sich nicht im Kreis dreht.

Ein guter Beitrag: eine konkrete Konstruktion, die Annahmen werden direkt benannt, ein Angriff auf sie wird durchgespielt,
der Preis ist berechnet (nach Berechnungen, Speicher, Datenverkehr, Blockchain-Eintrag). Noch wertvoller ist ein gefundenes Loch
im aktuellen Projekt mit einem konkreten Szenario.

Ein Teil der Fragen lässt sich durch Berechnung voranbringen. Solche Berechnungen führt der [Forschungsagent](RESEARCH_AGENT.md)
auf den Computern von Freiwilligen aus; die Aufgabenliste und ihre Bedeutung sind in [tasks/README.md](../../tasks/README.md) beschrieben,
die Zusammenfassung der Ergebnisse erscheint im Ordner `results/`. Zurzeit beziehen sich die Aufgaben auf die Fragen Q1, Q5 und Q9.

---

## Q1. Billige Prüfung, bei der Betrug selbst bei Absprache nutzlos ist

**Die Hauptfrage des Projekts.** Es ist nötig, dass ein falsches Ergebnis keinen Nutzen bringt und die Prüfung wenige
Prozent der nützlichen Arbeit kostet. Zielwerte: etwa 5 % für die Inferenz, etwa 20 % für das Training (nicht bestätigt).

Was bekannt ist:

- Die stichprobenartige Prüfung mit Abschreibung oder „Bezahlung nur des Geprüften“ geben eine wirtschaftliche Garantie
  bis zur Abspracheschwelle (siehe [CURRENT_DESIGN, Abschnitt 3](CURRENT_DESIGN.md)). Eine Null geben sie nicht, wenn
  sich alle Prüfer absprechen, die die Aufgaben prüfen.
- Eine Null bei Absprache gibt die Prüfung **jedes** bezahlten Ergebnisses. Die Neuberechnung kostet +100 % Arbeit.
  Kryptografische Beweise sind bislang Hunderte bis Tausende Male teurer als die Arbeit selbst.

Messungen aus dem Projektpiloten (auf konkreten CPUs, siehe [PILOT_RESULTS](PILOT_RESULTS.md)):
Der RISC-Zero-Beweis für eine Zeile der Qwen-Projektion brauchte 22 Minuten; die Ausführung eines Pakets
aus acht Zeilen in der zkVM dauerte ~17 700-mal länger als nativ; die vollständige Wiederholung der Arithmetik
einer Zeile in der EVM kostete 14,1 Mio. gas. Die veröffentlichte Arbeit FlashProve (2026) meldet 70–95× GPU-Zeit
für ihr ganzzahliges Inferenzprofil.

Was wir suchen: ein Prüfschema für die LLM-Inferenz und einen Trainingsschritt (LoRA oder vollständig), dessen
Gesamtkosten (prover + verifier + Daten + Blockchain) ins Budget passen, oder einen Beweis, dass dies für diese
Aufgabenklasse unmöglich ist.

## Q2. Bitgenaue Übereinstimmung des Ergebnisses auf verschiedenen Grafikkarten

Das gesamte Prüfschema beruht auf dem exakten Vergleich. Mit Gleitkomma addieren verschiedene GPUs in
unterschiedlicher Reihenfolge und liefern unterschiedliche Bits; eine Toleranz öffnet den „stillen“ Betrug
mit einem billigen Modell.

Kandidat: ein vollständig ganzzahliges Modell (int8-Gewichte und -Aktivierungen, Akkumulation in int32,
Skalierung mit ganzzahligem Multiplikator und Verschiebung, ganzzahlige Nichtlinearitäten oder Tabellen).
Für das Training: Zerlegung in Acht-Bit-Teile (Ozaki-Schema).

Offen: die Qualität des ganzzahligen Qwen, seine Geschwindigkeit auf Consumer-GPUs (AMD, NVIDIA, Intel),
das ganzzahlige Training. Benötigt werden konkrete Kernel, eine Abschätzung der Qualitätsverluste,
bekannte Arbeiten.

## Q3. Streit mit Neuberechnung in der Blockchain für das vollständige Modell

Der Streit wird durch Halbieren auf eine Operation eingeengt, die der Vertrag selbst neu berechnet. Gebaut ist das
nur für eine Zeile des Modells (erfolgreicher Einspruch ~14 Mio. gas, das Spiel aus 93 Transaktionen ~6 Mio. gas).
Benötigt: eine Referenz-Ganzzahlmaschine für das vollständige Modell, ein Beweis, dass sich das Spiel nicht ablenken
lässt (Eingabe, Länge oder Pfad unterschieben), Fristen für die Züge, der Preis unter Last, die Wahl der Blockchain
oder von L2.

## Q4. Was gelernt werden soll und wie man verhindert, dass das Modell verdorben wird

- Wie das Netz selbst und ohne Menschen mit Sonderrechten den Trainingsplan wählt.
- Wie man sich vor einem Schädling schützt, der bereit ist, Credits zu verlieren: unbemerkte Fälschungen
  wirken sofort auf das Training ein.
- Wie man versteckte Verhaltens-Backdoors fängt, die die Qualitätsprüfung nicht sieht.
- Wie man Datensätze im Katalog prüft: eine korrekte Berechnung auf schädlichen Daten wird von der Prüfung
  nicht korrigiert.

Bekannte enge Garantie: Ist das Basismodell eingefroren und ändert der trainierbare Teil die Logits um
höchstens `b`, dann ändert dort, wo der Abstand zwischen den zwei besten Tokens größer als `2b` ist, eine
Vergiftung die Antwort nicht.

## Q5. Übernahme der Mehrheit

Das Gewicht misst Arbeit, nicht Unabhängigkeit. Der Besitzer von tausend gemieteten GPUs sieht aus wie tausend
Teilnehmer. Eine Gruppe mit 3/4 des Gewichts kann die Regeln ändern. Benötigt werden Mechanismen, die den Schaden
einer ehrlich erlangten Mehrheit begrenzen: ein unveränderlicher Kern, eine Schwelle für Modelle, Regeln für den
geschlossenen Start und Bedingungen für die Öffnung des Netzes.

## Q6. Privatsphäre von Anfragen auf gewöhnlichen Geräten

Der Besitzer des Geräts kann die Anfrage lesen, die es berechnet. Das Aufteilen der Schichten hilft nicht:
verborgene Vektoren werden wiederhergestellt. Benötigt: billige Teilmaßnahmen, Zugangsregeln zu fremden
Anfragen, ein Streit um eine private Anfrage ohne Veröffentlichung von Zwischendaten, eine Bezahlung, die sich
nicht mit dem Zahler verknüpfen lässt.

## Q7. Verfügbarkeit der Daten

Der Prüfer sagt „man hat mir die Daten nicht gegeben“, der Speichernde sagt „ich habe sie gegeben“, das Journal
hat die Übertragung nicht gesehen. Für kleine Daten hilft die Veröffentlichung in der Blockchain; für große
(den Modellzustand) gibt es keine Lösung. Außerdem: wie viele unabhängige Kopien nötig sind und wie man sich
vergewissert, dass sie bei verschiedenen Besitzern liegen.

## Q8. Widerstandsfähigkeit gegen Blockaden und die Erstinstallation

- Wie ein Neuling das echte Programm und die Adresse des Journals erhält, wenn die wichtigsten Plattformen
  blockiert sind.
- Welche unabhängigen öffentlichen „Treffpunkte“ man nutzt, damit sie sich nicht mit einer einzigen Entscheidung
  blockieren lassen.
- Wie man über NAT und Relais ohne zentrale Server arbeitet.

## Q9. Ökonomie

- Die Arbeitseinheit und der Satz für das Training, bei denen die Ausgabe von Credits diese nicht auf null entwertet.
- Ob die Teilnahme für Besitzer großer Rechenkapazitäten bei realen Strompreisen lohnt.
- Die Ungleichmäßigkeit des Einkommens, wenn nur geprüfte Aufgaben bezahlt werden.
- Kauf und Verkauf von Credits gegen Geld und Kryptowährung.

## Q10. Wie ein Modell, das selbst lernt, den Gesetzen von SkyNet folgen wird

Das Manifest verlangt, dass das Modell der Menschheit und dem Menschen keinen Schaden zufügt, die Anfragen der
Menschen im Rahmen der höheren Gesetze ausführt und sich selbst schont. Solche Regeln zuverlässig im Modell zu
verankern, ist eine ungelöste wissenschaftliche Aufgabe, und in einem Netz ohne Moderatoren und mit Selbstlernen
ist sie noch schwerer. Benötigt: wie die Gesetze in die Prüfung vor dem Austausch der Modellversion eingehen, wie
das Training sie nicht aufweicht, wer und wie Streitfälle ohne Menschen mit Sonderrechten entscheidet, wie man die
Gesetze nicht zur Zensur nützlichen Wissens macht.

---

## Was bereits verworfen wurde und warum

| Idee | Warum sie nicht passt |
|---|---|
| Für Arbeitszeit oder gemeldete Leistung nach Berichten und Unterschriften zahlen | Ein abgesprochener Agent und Prüfer unterschreiben alles; eine stillstehende Karte liefert dieselben Meldungen |
| Kurze Aufgaben mit Antwortprüfung als Nachweis der Arbeit einer bestimmten Grafikkarte | Die Antwort lässt sich auf einem fremden Computer berechnen oder aus dem Cache nehmen: Der Prüfer sieht gleiche Daten |
| Eine Kaution oder ein Aufnahmebeitrag | Durch die Anforderung R5 verboten |
| Strafen von einem zugänglichen Konto | Durch die Anforderung R5 verboten |
| Vertrauen in einen einzigen ehrlichen Prüfer als Garantie bei vollständiger Absprache | Ersetzt die Anforderung R4 durch eine Annahme |
| Mehrheitsabstimmung über die Richtigkeit des Ergebnisses | Die Mehrheit lässt sich erobern; die Richtigkeit muss die Arithmetik entscheiden |

Allgemeines Prinzip: **Wenn der ehrliche und der fiktive Fall dem Prüfer dieselben Daten liefern, kann kein
Algorithmus über diesen Daten sie unterscheiden.** Eine neue Signatur oder ein Eintrag in der Blockchain fügen
solche Daten nicht hinzu. Deshalb zahlt das Netz für das geprüfte Ergebnis und nicht für die Ressource.
