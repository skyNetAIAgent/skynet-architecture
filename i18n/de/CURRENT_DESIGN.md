<!-- translation of docs/CURRENT_DESIGN.md, source sha256: a4c162fa040254e708d1d2a816f908416be83f27576a99e7dd1174c85218fced -->

# Aktueller Architekturentwurf

[English](../../docs/CURRENT_DESIGN.en.md) · [中文](../zh/CURRENT_DESIGN.md) · [Español](../es/CURRENT_DESIGN.md) · [Français](../fr/CURRENT_DESIGN.md) · **Deutsch** · [Italiano](../it/CURRENT_DESIGN.md) · [Русский](../../docs/CURRENT_DESIGN.md) · [Português](../pt/CURRENT_DESIGN.md) · [العربية](../ar/CURRENT_DESIGN.md)

Stand vom 22. November 2026. Dies ist ein **Entwurf, keine Implementierung**. Experimente dazu
gab es nicht. Zahlen mit der Markierung [Berechnung] wurden anhand einer Formel ermittelt, nicht
gemessen.

## Wo wir jetzt stehen

Die Idee ist im [Manifest](MANIFESTO.md) formuliert, die verbindlichen Anforderungen sind
genehmigt, die Grundlage der Architektur ist gewählt: ein Netz ohne Koordinatoren, ein gemeinsames
Journal auf einer öffentlichen Blockchain, Bezahlung für geprüfte Arbeit und aufgeschobene
Auszahlung statt Pfand. Ein kleiner vertrauenswürdiger Pilot hat das Qwen-Modell bereits auf
mehreren Computern laufen lassen ([Pilotergebnisse](../../docs/PILOT_RESULTS.md)).

Das Schwierigste liegt noch vor uns. Eine billige Methode, Arbeit so zu prüfen, dass Betrug selbst
bei Absprache nutzlos ist, wurde noch nicht gefunden. Ein Modell, das sich selbst zuverlässig
verbessert und den Gesetzen von SkyNet folgt, bleibt vorerst ein Forschungsziel. Aufgaben für
Mitautoren stehen in den [offenen Fragen](OPEN_QUESTIONS.md).

Statusmarkierungen:

| Markierung | Bedeutung |
|---|---|
| **Angenommen** | Im Projekt als Entscheidung genehmigt |
| **Kandidat** | Gewählte Variante, noch nicht genehmigt oder nicht gebaut |
| **Vorschlag** | Zur Entscheidung vorgelegt, nicht genehmigt |
| **Offen** | Keine Entscheidung |

## 1. Allgemeines Schema (als Grundlage angenommen)

Im Netz gibt es **keine Koordinatoren** und keine Rollen mit Sonderrechten. Alle Teilnehmer haben
dasselbe Programm. Innerhalb der Ressourcenregler macht es selbst:

| Arbeit | Was es tut | Wofür bezahlt wird |
|---|---|---|
| Rechnet | Führt einen Lernschritt oder eine Nutzeranfrage aus | Für das angenommene Ergebnis |
| Prüft | Rechnet ein fremdes Ergebnis nach, wenn das Los es gewählt hat | Für die ausgeführte Prüfung |
| Überwacht | Kann jedes Ergebnis nachrechnen und es anfechten | Ein Teil des abgezogenen Betrags bei einer gefundenen Fälschung |
| Speichert und verteilt | Hält die Daten, mit denen es arbeitet | Der Datenempfänger bezahlt |
| Schreibt ins Journal | Sammelt die Einträge der Teilnehmer in die Blockchain | Aufwandsentschädigung |
| Hilft beim Auffinden | Leitet Verbindungen für Geräte hinter einem Router weiter | Ist in der Zustellvergütung enthalten |

**Das gemeinsame Journal** ist ein Vertrag auf einer bestehenden öffentlichen Blockchain ohne
Administratorschlüssel. Es speichert die Regeln und den Hash des Programms, die Konten (verfügbare
Credits, der ausstehende Betrag, das Gewicht geprüfter Arbeit), die Hashes der eingereichten
Ergebnisse, Streitfälle, Abstimmungen, den Modellkatalog und den Lernplan. Das Journal arbeitet
sogar, wenn alle SkyNet-Knoten ausgeschaltet sind. Die Blockchain ist **nicht gewählt** (Offen).

**Der öffentliche Zufall** entscheidet, wer eine Aufgabe bekommt, was geprüft wird und wer prüft.
Er entsteht, nachdem das Ergebnis festgeschrieben ist. Kandidat: eine Mischung aus dem drand-Beacon
und dem Zufall der Blockchain (Kandidat, Quellen nicht gewählt).

## 2. Das Leben einer Aufgabe (Kandidat)

1. Eine Lernaufgabe wird aus dem gemeinsamen Plan des Netzes abgeleitet; eine Anfrage kommt vom Nutzer mit Bezahlung.
2. Den Ausführenden bestimmt der Zufall unter den Geräten mit passenden Ressourcen.
3. Das Programm rechnet und schreibt die Hashes der Zwischenzustände auf.
4. Der Hash des Ergebnisses kommt in ein Paket, das Paket ins Journal. Die Belohnung geht in den ausstehenden Betrag.
5. Der Zufall entscheidet nach der Abgabe, ob die Aufgabe geprüft wird.
6. Die gewählte Aufgabe rechnen drei zufällige Teilnehmer unabhängig nach, blind.
7. Stimmt bis aufs Bit überein — bestätigt. Stimmt nicht überein — ein Streitfall, den die Neuberechnung des strittigen elementaren Schritts **im Journal selbst** entscheidet, nicht eine Abstimmung.
8. Das Prüffenster beträgt drei Tage: Jeder kann das Ergebnis anfechten.
9. Nach dem Fenster wird die Belohnung verfügbar.

**Aufgeschobene Auszahlung statt Pfand (angenommen).** Für ein Ergebnis haftet ein Teilnehmer nur
mit dem ausstehenden Betrag — seinen Belohnungen der letzten drei Tage. Im Voraus wird nichts
genommen, bereits verfügbare Credits werden niemals abgezogen.

## 3. Wie man Betrug unrentabel macht: zwei Varianten

### Variante A. Stichprobenprüfung mit Abzug (aktuelle Spezifikation)

Der Prüfanteil `p = 4R / (R + H)`, aber nicht weniger als 1%; der Abzug für ein falsches Ergebnis
`B = 4R/p − R`, nicht mehr als der ausstehende Betrag `H` (`R` — der Preis der Aufgabe). Dann kostet
jede Fälschung im Durchschnitt vier Preise der Aufgabe bei jeder Prüfhäufigkeit [Berechnung]. Eine
Fälschung geht nur durch, wenn alle drei Prüfer abgesprochen sind: bei einem Abspracheanteil `q` ist
die Wahrscheinlichkeit `q³`. Betrug ist unrentabel, solange die abgesprochene Gruppe weniger als
~91% des Gewichts der Prüfer hält [Berechnung].

**Schwäche.** Eine ungeprüfte Fälschung wird bezahlt und bleibt im Netz. Das ist eine Wette mit
Ausgängen, bei denen der Betrüger gewinnt.

**Vorläufige Berechnung (22. November 2026, ein Computer, von anderen Teilnehmern nicht
bestätigt).** Die Schätzung „91%“ stammt aus dem Durchschnitt einer einzelnen Fälschung. Sie
berücksichtigt nicht, dass ein Teilnehmer höchstens den ausstehenden Betrag verlieren kann: Pfänder
und Strafen gibt es nicht. Für einen Teilnehmer, der das Netz verlässt und Fälschungen stapelweise
vor Abschluss der Prüfungen einreicht, ergibt die exakte Aufzählung der Strategien im Modell
`exit-scam-a` eine niedrigere Grenze [Berechnung]:

| Regeln | Der Abgang mit Fälschungen lohnt sich ab einem Abspracheanteil |
|---|---|
| Gleiche kleine Aufgaben, 399 Preise ausstehend, ein Stapel | 89,2% |
| Gleiche kleine Aufgaben, 1200 Preise ausstehend, ein Stapel | 90,8% |
| Gleiche kleine Aufgaben, drei Stapel, Regel „nicht mehr als ein Drittel in Arbeit“ | 89,0% |
| Aufgaben beliebiger Größe, drei Stapel, Regel „nicht mehr als ein Drittel“ | 87,5% |
| Aufgaben beliebiger Größe, zwei Stapel bis 100 Aufgaben, ohne die Regel „nicht mehr als ein Drittel“ | 80% |
| Ohne Absprache, Aufgaben beliebiger Größe, zwei Stapel (92 Mio. Strategien) | lohnt sich nicht |

Ohne die Regel „nicht mehr als ein Drittel“ erhöhen die ungeprüften Belohnungen des ersten Stapels
den ausstehenden Betrag und die zulässige Größe der Aufgaben des zweiten, deshalb ist diese Regel
verpflichtend. Das Modell steht am Anfang der Kernel-Datei
[exit_scam_a.py](../../agent/skynet_agent/kernels/exit_scam_a.py) und reproduziert die Zahlen aus dem
Beispiel der Spezifikation („etwa 78, 107 und 17“). Die Aufgaben sind in
[tasks/README.md](../../tasks/README.md) beschrieben, der erste Durchlauf in
[results/FIRST_RUN.md](../../results/FIRST_RUN.md). Diese Zahlen werden nach unabhängiger Bestätigung
durch andere Teilnehmer zum Ergebnis des Entwurfs.

### Variante B. Das Netz bezahlt nur für Geprüftes (Vorschlag, wartet auf Entscheidung)

Eine Aufgabe wird zum Lottoschein. Das Los wählt den Anteil `p` der Aufgaben (zum Beispiel 1%), nur
sie werden geprüft und **nur sie werden bezahlt, aber um das `1/p`-fache teurer**. Im Durchschnitt
erhält ein ehrlicher Teilnehmer genauso viel, und eine nicht gewählte Fälschung bringt **nichts**.

- Ohne Absprache bringt eine Fälschung genau null.
- Mit Absprache ist eine falsche Auszahlung höchstens `q^k` pro geprüfte Aufgabe (k — die Zahl der
  Prüfer): 0,1% bei q = 10% und k = 3 [Berechnung]. Jeder fehlgeschlagene Versuch verbrennt den
  gesamten ausstehenden Betrag.
- Gefundene Löcher: Ein Neuling in einer Absprache erhält im Durchschnitt `q^k` Preise pro Versuch
  und verliert nichts; eine „Ausstiegskampagne“ aus vielen Fälschungen auf einmal. Reparaturen sind
  vorgeschlagen: Lehrlingsplätze aus einem begrenzten Budget, die Annullierung aller unreifen
  Gewinne eines Schlüssels bei einer erwischten Fälschung, eine Obergrenze offener Aufgaben.
- Preis: Das Einkommen wird ungleichmäßig. Für ein schwaches Gerät etwa ±13% im Monat [Berechnung].

Beide Schemata verlangen die **Übereinstimmung des Ergebnisses bis aufs Bit** auf verschiedenen
Geräten. Der vorgeschlagene Weg: ganzzahlige (int8/int32) Modellarithmetik, bei der die Reihenfolge
der Addition das Ergebnis nicht beeinflusst. **Geschwindigkeit und Qualität des ganzzahligen Qwen
sind nicht gemessen**; ein bekanntes reproduzierbares int8-Profil war 5,2-mal langsamer als das
gewöhnliche (Offen).

Ein billiger Streitfall: durch Halbieren der Berechnung bis zu einer einzigen Operation, dann die
Prüfung der Matrixmultiplikation mit einem Zufallsvektor (Algorithmus von Freivalds). Eine Ersparnis
von etwa dem 100-Fachen bei der Zahl der Multiplikationen auf großen Matrizen, das 2,6-Fache bei
LoRA, kein Gewinn bei der Erzeugung Token für Token [Berechnung] (Kandidat).

## 4. Gewicht und neue Teilnehmer (Kandidat)

- **Gewicht** ist die Summe der Preise der Ergebnisse, die in 30 Tagen die Prüfung bestanden haben.
  Man kann es nicht kaufen, übertragen oder anhäufen. Die Zahl der Konten bringt nichts: Chancen und
  Stimmen sind dem Gewicht proportional.
- Ein **Neuling** macht zuerst „Lehrlings“-Nachprüfungen fremder Aufgaben: Seine Antwort entscheidet
  nichts und wird nur bezahlt, wenn sie mit dem angenommenen Ergebnis übereinstimmt. Danach bekommt
  er Aufgaben, die immer geprüft werden, dann immer seltener.
- Das Gewicht wird für jedes Modell einzeln gezählt. Bei einem Modell, das nur wenige betreiben, ist
  der Kreis der Prüfer klein und leichter zu übernehmen (Offen).

## 5. Auffinden und Wiederherstellung (Kandidat)

| Wo | Was eine vollständige Abschaltung übersteht |
|---|---|
| Das Journal in der öffentlichen Blockchain | Regeln, Konten, Gewicht, Hash des Modells, Lernplan, Streitfälle, Adressen der Knoten, die geschrieben haben |
| Die Datenträger der Teilnehmer und öffentliche Spiegel | Modellgewichte, Lernzustand, Daten; jede Kopie wird gegen den Hash aus dem Journal geprüft |
| Die Distribution des Programms | Netzkennung, Adresse des Journals, anfängliche Liste der Treffpunkte |

Drei unabhängige Wege, sich zu finden, einer genügt: signierte Einträge auf externen Plattformen
(„Treffpunkte“), offene Netze zum Auffinden von Knoten (zum Beispiel DHT von libp2p), Adressen im
Journal selbst. Das Prüffenster läuft nicht, solange das Netz stillsteht, andernfalls ließe sich
eine Fälschung vor dem Anhalten einreichen.

Schwache Stellen: die Echtheit der ersten Installation (die Adresse des Journals erfährt der Neuling
von außen); die vollständige Sperrung aller Wege auf einmal; das Vertrauen in zwei von drei
Checkpoint-Anbietern nach langem Stillstand.

## 6. Anfragen und Privatsphäre (Kandidat)

Die Anfrage wird für das Gerät des Ausführenden verschlüsselt und geht direkt oder über einen
Weiterleiter unter einem Pseudonym. Im Journal stehen nur Hashes. Etwa 1% der Anfragen sehen außerdem
drei Prüfer.

**Ehrlicher Vorbehalt.** Auf einem gewöhnlichen Computer kann der Besitzer des Geräts mit einem
veränderten Programm die Anfrage lesen, die es berechnet. Vollständig homomorphe Berechnungen sind
für solche Modelle tausende Male langsamer. Deshalb zwei Modi: der gewöhnliche (billige) und der
geschützte (nur auf Hardware, die beweist, dass der Besitzer nicht hineinschauen wird; teurer,
beruht auf dem Vertrauen zum Hersteller).

## 7. Lernen und Planauswahl (Vorschlag)

Ein offener Katalog von Modellen und Datensätzen mit freien Lizenzen, durch Hashes festgeschrieben.
Das Netz stellt nach einer Regel Lernvarianten zusammen, gibt jeder einen Probelauf, verteilt die
freie Kapazität nach den Ergebnissen und der Abstimmung nach Gewicht. Eine neue Modellversion ersetzt
die vorherige nur, wenn sie das Examen besser bestanden hat, dessen Aufgaben nach der Fixierung der
Gewichte durch den Zufall gewählt wurden. Der Beitrag einer einzelnen Aufgabe zur Aktualisierung der
Gewichte ist begrenzt; der „leichte“ Teil des Schritts (das Addieren der Beiträge) wird immer
nachgerechnet.

Ein Modell, das sich **zuverlässig und endlos selbst verbessert**, ist ein Forschungsziel, keine
fertige Technologie. Eine realistische erste Etappe: automatische Feinabstimmung und Auswahl durch
das Examen.

## 8. Regeländerung (Kandidat)

Die Regeln ändert nur eine neue Programmversion, die 3/4 des **gesamten** Gewichts angenommen hat,
nach einer Abstimmung von nicht kürzer als 14 Tagen und einer angekündigten Frist von 30 Tagen. Die
allgemeine Bremse (mehr als die Hälfte des Gewichts) kann eine neue Modellversion nur stoppen.
Vorschlag: ein unveränderlicher Prüfkern, der per Abstimmung nicht abgeschafft werden kann (wartet
auf Entscheidung).

## 9. Zusammenfassung der Angriffe

Von 60 untersuchten Betrugsweisen: 18 sind geschlossen, 6 unrentabel, 19 begrenzt, 16 offen (für
Variante A). Die wichtigsten offenen Stellen:

1. **Mehrheit nach Gewicht.** Eine Gruppe mit 3/4 des Gewichts kann die Regeln ändern; in einem
   kleinen Netz lässt sich ein solcher Anteil durch ehrliche Arbeit auf gemieteter Rechenleistung
   ansammeln. Deshalb ist der Start geschlossen, auf Übungskrediten.
2. **Ungebaute Grundlagen.** Die Übereinstimmung bis aufs Bit und die Neuberechnung des Streitfalls
   im Journal für ein vollständiges Modell sind nicht gebaut.
3. **Ein Saboteur, der keinen Nutzen braucht.** Er kann das Lernen im Rahmen des Anteils seiner
   Arbeit verderben; versteckte Hintertüren fängt das Examen nicht.
4. **Fremde Anfragen** im gewöhnlichen Modus und bei Streitfällen.
5. **Verfügbarkeit der Daten.** Den Streitfall „hat große Daten geliefert oder nicht“ lässt sich
   mit nichts entscheiden.
6. **Netzbeitritt.** Die Warteschlange auf Lehrlingsplätze und die Echtheit der ersten Installation.

Einzelheiten und Aufgaben für Mitautoren stehen in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md).
