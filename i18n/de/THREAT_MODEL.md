<!-- translation of docs/THREAT_MODEL.md, source sha256: 96c64b91168c36392f3f705d1ce619df7c73340c08bffee57773d75508990fff -->

# Gegnermodell und Angriffstabelle

[English](../../docs/THREAT_MODEL.en.md) · [中文](../zh/THREAT_MODEL.md) · [Español](../es/THREAT_MODEL.md) · [Français](../fr/THREAT_MODEL.md) · **Deutsch** · [Italiano](../it/THREAT_MODEL.md) · [Русский](../../docs/THREAT_MODEL.md) · [Português](../pt/THREAT_MODEL.md) · [العربية](../ar/THREAT_MODEL.md)

Stand vom 24. November 2026.

Dieses Dokument ist das Ergebnis des Modellrats zu Phase 1 der Roadmap („Genaue Formulierung“,
[ROADMAP](ROADMAP.md), Abschnitt 4). Es versammelt das Gegnermodell, den Abgleich der Zahl der
Angriffe, den Status jedes der 60 Angriffe der Spezifikation für die Varianten A und B, die vom Rat
gefundenen neuen Angriffe und die Fragen, die nur der Eigentümer des Projekts entscheiden kann.

**Status des Dokuments.** Dies ist das Ergebnis von Überlegung und Berechnung nach Formeln, keine
Messung. Experimente, Netzstarts und programmgestützte Nachrechnungen gab es dafür nicht. Zahlen mit
der Markierung [Berechnung] wurden nach den Formeln in den Arbeiten des Rats ermittelt und von den
Kritikern manuell geprüft; auf einem zweiten Gerät wurden sie nicht wiederholt. Zu angenommenen
Entscheidungen wird nur, was der Eigentümer des Projekts bestätigt. Alles Übrige hier ist eine
Einschätzung des Rats, und bei Widerspruch ist in ihr „strittig“ angegeben.

**Wie man liest.** Abschnitt 1 legt fest, wer angreift und was als Gewinn gilt. Abschnitt 2 erklärt
die Diskrepanz 59 und 60. Abschnitt 3 ist die Haupttabelle: Anhand ihrer kann jeder Teilnehmer einen
nicht geschlossenen Angriff nennen und dies anhand der Ausgangsdokumente prüfen. Abschnitt 4 ist eine
kurze Zusammenfassung, Abschnitt 5 sind die Fragen an den Eigentümer, Abschnitt 6 — wer beteiligt war.

Ausgangsdokumente: die Entscheidungen D1–D5 in [ROADMAP](ROADMAP.md), Abschnitt 3; die Varianten A und B in
[CURRENT_DESIGN](CURRENT_DESIGN.md), Abschnitt 3; [OPEN_QUESTIONS](OPEN_QUESTIONS.md);
[PILOT_RESULTS](PILOT_RESULTS.md); der erste Durchlauf [FIRST_RUN](FIRST_RUN.md);
die verbindlichen Anforderungen [REQUIREMENTS](REQUIREMENTS.md). Die Tabelle der 60 Angriffe ist
der Spezifikation des Netzes ohne Koordinatoren vom 20. November 2026 entnommen (im Folgenden SPEC); die Zeilennummern
1.1–7.4 sind ihre Nummern.

---

## 1. Gegnermodell

### 1.1. Bezeichnungen und Varianten

| Symbol | Bedeutung |
|---|---|
| `R`, `c` | Preis der Aufgabe und Selbstkosten der ehrlichen Ausführung, `c ≤ R` |
| `H` | Ausstehender Betrag: noch nicht ausgereifte Belohnungen des Schlüssels für die letzten drei Tage. Nur er kann abgezogen werden (keine Pfänder und Strafen, Anforderung R5) |
| `p` | Prüfanteil: in A `p = 4R/(R+H)`, aber nicht weniger als 1%; in B konstant, zum Beispiel 1% |
| `B` | Abzug in A: `B = 4R/p − R`, nicht mehr als `H`; bei `p > 1%` ist das `B = H`, sonst `B = 399R` |
| `k` | Zahl der Prüfer der Aufgabe, 3 (bei Auslosungsrunden im Mittel 3,5–4,5) |
| `q`, `q_eff` | Anteil der Koalition am gesamten Gewicht der Prüfer des Modells und unter denen, die die Aufgabe tatsächlich prüfen (Abschnitt 1.7) |
| `G` | Vollständiger Preis des Streitfalls im Journal |

**Variante A** (aktuelle Spezifikation): Stichprobenprüfung mit Abzug aus `H`; eine nicht bestrittene
ungeprüfte Abgabe wird bezahlt. **Variante B** (Vorschlag): bezahlt werden nur die ausgelosten und
bestätigten Aufgaben, zum Preis `R/p`; nicht Ausgelostes wird niemandem bezahlt; eine erwischte
Fälschung verbrennt den gesamten `H` des Schlüssels. B ist als Skizze beschrieben, und der Rat
untersuchte „B wie beschrieben“: der Weg des Neulings, die Zulassung der Prüfer nach `H`, der Tarif
der Prüfer und die Quelle von `R/p` für Anfragen fehlen in der Beschreibung.

### 1.2. Wer angreift

Die Profile sind über alle sechs Arbeiten zusammengeführt. Kombinationen sind verbindlich: eine Koalition mit kostenlosen Schlüsseln,
ein Mieter, der zur Koalition wurde, ein lange ehrlicher Teilnehmer bei Absprache, ein Nutzer in Absprache
mit den Prüfern, ein Saboteur mit kostenlosen Schlüsseln.

| Profil | Worüber er verfügt | Was er will |
|---|---|---|
| Einzelgänger | Eigene Schlüssel, eigenes Gerät, verändertes Programm | Credits ohne Arbeit oder über die Arbeit hinaus |
| Koalition mit Anteil `q` | Schlüssel unter gemeinsamer Verwaltung; sofortige Weitergabe von Ergebnissen, Rechenschritten, Zuständen und Anfragen; gemeinsame Kasse | Eine Fälschung durchlassen, Bezahlung der Prüfungen ohne Neuberechnung erhalten, Abstimmungen gewinnen |
| Besitzer vieler Schlüssel | Beliebig viele Schlüssel fast umsonst; Gewicht und `H` neuer Schlüssel sind null | Warteschlangen, Lehrlingsplätze, Datenverteilung, Zuweisungen, Lose in B |
| Mieter von Rechenleistung | GPU-Stunden zum Marktpreis, die Arbeit ist ehrlich und wird vom Netz bezahlt | Einen Gewichtsanteil, dann Absprache, ein seltenes Modell oder die Regeln |
| Saboteur ohne Nutzen | Bereit, alle noch nicht ausgereiften Belohnungen zu verlieren | Der Schaden selbst: Modell, Antworten, Hintertür, Stillstand |
| Teilnehmer mit leerem Konto | `H = 0`, kein Gewicht | Jede Auszahlung ohne Arbeit |
| Lange ehrlich, dann Weggang | Großes `H` und Gewicht; wählt Zeitpunkt, Größe und Zahl der Wellen | Mehr als `H` plus ehrliche Bezahlung der letzten Aufgaben |
| Nutzer | Eigene Anfrage, Credits, Recht auf Streitfall, Absprache mit dem Ausführenden oder den Prüfern | Kostenlose Antwort, Rückerstattung für eine richtige Antwort, fremde Daten |
| Betreiber von Relais, Treffpunkten, Schreibknoten, Blockchain-Zugangspunkten, Datenverwahrern | Sehen Adressen und Zeit, verzögern, geben nicht weiter, zeigen eine falsche Umgebung | Zensur, Abtrennung eines Knotens, Offenlegung der Identität, Bezahlung für Einträge |
| Externe Parteien | Zufallsbeacon, Blockproduzent, Anbieter von Kontrollpunkten, Hersteller des geschützten Modus, Verteiler des Programms | Die Stichprobe verschieben, eine falsche Historie oder ein falsches Programm unterschieben |
| Besitzer fremder Geräte | Gestohlene oder infizierte Arbeitsschlüssel | Fälschungen bestätigen und dabei fremdes `H` riskieren |

### 1.3. Was der Gegner kann und was nicht

**Kann:** beliebig viele Schlüssel erzeugen; ein verändertes Programm starten und alles auf seinem
Gerät lesen, einschließlich privater Anfragen im gewöhnlichen Modus; innerhalb der Koalition beliebige Daten
weitergeben; sich abschalten, den Zeitpunkt der Abgabe wählen, schweigen, Daten einem Knoten geben und einem anderen nicht,
die einzige Kopie halten; Rechenleistung mieten; abstimmen und Stimmen kaufen; offen
Bestechungsgeld über einen Smart Contract anbieten (die Bestätigungen liegen im Journal, die Zahlung lässt sich ohne Vertrauen ausführen);
als Blockproduzent — einen Block nicht veröffentlichen und einen von zwei Zufallswerten wählen;
einen Teil der Relais halten und einen Knoten umgeben; einen externen Nutzen haben oder den Schaden selbst wertschätzen.

**Kann nicht** (das sind Annahmen, sie müssen direkt benannt werden): die Signatur eines fremden, nicht gestohlenen
Schlüssels fälschen, eine Hash-Kollision finden, ein Commitment auf zwei Arten öffnen, die geheime Auslosung (VRF)
fälschen; die endgültigen Blöcke einer öffentlichen Blockchain umschreiben — das Journal hat keinen Administratorschlüssel und ist
korrekt (Voraussetzung 1 der SPEC; das Programm ist nicht geschrieben); die Zufälligkeit nach
der Fixierung des Pakets vorhersagen oder verschieben (Voraussetzung 2; die Quellen sind nicht gewählt; die Mischung schützt vor Vorhersage,
aber nicht vor der Wahl durch die letzte Quelle, N13); eine Übereinstimmung bis aufs Bit ohne Berechnung
erhalten (Voraussetzung 3; nicht geprüft); das Ergebnis der Neuberechnung eines Schritts im Journal ändern (Voraussetzung 4; für das vollständige
Modell nicht gebaut); das Programm eines fremden Knotens ändern (D4); fremde verfügbare Credits abbuchen,
eine zweite Auszahlung für dieselbe Nummer erhalten, ein abgegebenes Paket widerrufen.

**Was das Netz grundsätzlich nicht sieht:** wem die Schlüssel gehören und ob die Teilnehmer unabhängig sind; ob
ein Knoten Daten an einen anderen gegeben hat; was auf einem fremden Computer läuft; wodurch sich die Neuberechnung von der Kopie eines fremden
Zustands unterscheidet. Wenn der ehrliche und der falsche Fall dem Knoten dieselben Daten geben, unterscheidet keine Regel sie
([OPEN_QUESTIONS](OPEN_QUESTIONS.md)).

### 1.4. Gewinn des Gegners und Schaden des Netzes

Der Gewinn wird für die gesamte Koalition aus einem Anfangszustand berechnet, mit denselben Rechten, Aufgaben
und demselben Horizont bis zur endgültigen Abrechnung, einschließlich des Weggangs. Addiert werden ausgereifte Credits, Erstattungen,
der Wert der erhaltenen Dienstleistung und neuer Rechte; abgezogen werden reale Kosten (Arbeit, Energie, Miete, Gas,
externe Zahlungen). Übertragungen innerhalb der Koalition werden verrechnet, ein Credit wird nicht doppelt gezählt, der Verlust
des Opfers ist für sich genommen kein Einkommen der Koalition. Arten des Gewinns: Credits für eine falsche Meldung (Fälschung, Kopie,
Bestätigung ohne Neuberechnung, fremde Zeile); eingesparte Kosten bei gleicher Bezahlung; Gewicht und Plätze
in der Auslosung; Rückerstattung für eine richtige Antwort oder der unbezahlte Teil der Daten; Gewinn durch den Effekt — Einfluss auf
die Antwort oder das Modell, Lesen einer fremden Anfrage, Kontrolle über Regeln, Ausgabe, Katalog, Plan, der Schaden selbst.

Der Schaden für das Netz wird getrennt in eigenen Einheiten berechnet: ein falsches Ergebnis wurde angenommen; das Ergebnis wurde
vor der Prüfung genutzt; Credits ohne Arbeit wurden ausgegeben; ein Ehrlicher hat `H` verloren; Auszahlungen oder der Zugang
für Neulinge wurden eingefroren; private Daten wurden offengelegt; Historie, Regeln, Programm oder Modellversion wurden
ersetzt; das Netz hat Arbeit für aufgezwungene Prüfungen und Streitfälle aufgewendet. Schaden ohne Gewinn verletzt D1 nicht, kann aber
andere Anforderungen verletzen; in der Tabelle ist das „n. z.“ mit dem Namen der Anforderung.

### 1.5. Formale Schreibweise von D1

D1 (angenommen am 23. November 2026): „der Betrüger bekommt nicht, was er will“; der erwartete Gewinn aus einer Fälschung
ist nicht größer als null im Vergleich zur ehrlichen Arbeit und zur Untätigkeit, für jede Koalition, einschließlich eines Neulings
mit leerem Konto und beliebig vieler Schlüssel; eine begrenzte positive Leckage erfüllt das Kriterium nicht.

Sei `U(σ)` der erwartete Nutzen der Koalition bei der Strategie `σ`. Für jede Strategie mit einer falschen
Meldung werden **beide** Ungleichungen benötigt:

- `Δ₀ = E[U(σ) − U(Untätigkeit)] ≤ 0` — jede falsche Meldung ist durch die Ablehnung der Aufgabe ersetzt
  (das bereits verdiente `H₀` reift dabei aus);
- `Δч = E[U(σ) − U(ehrliche Arbeit)] ≤ 0` — jede falsche Meldung ist durch ehrliche Ausführung ersetzt.

Die Anforderung gilt bei jedem `q` von 0 bis 1, bei `H = 0` und beliebiger Zahl von Schlüsseln. Zur Widerlegung
genügt ein zulässiger Zustand und eine positive Differenz. Mit dem Größeren der beiden Bezugspunkte zu vergleichen ist nicht zulässig: bei Untätigkeit 0, ehrlichem Gewinn 0,60 und falscher Meldung 0,20 ergibt ein solcher Vergleich
„keine Verletzung“, obwohl `Δ₀ = +0,20` [Berechnung].

Eine Arbeit schlug vor, D1 in eine wirtschaftliche Ebene (nur Credits) und eine Ebene nach dem Effekt
(Einfluss auf Antwort und Modell, Lesen der Anfrage, Schaden) zu teilen. Der Rat übernimmt das nicht selbst: die Frage ist
an den Eigentümer verwiesen (Abschnitt 5, Frage 1). In der Tabelle ist ein Gewinn nur nach dem Effekt mit „nein (Eff.)“ markiert.

### 1.6. Allgemeines Prinzip der Spalte „Daten für die Ablehnung“

Bei Absprache des Ausführenden mit allen zugewiesenen Prüfern sieht der Knoten nur abgestimmte Daten:
Fingerabdrücke des Ergebnisses und des Rechenschritts, offengelegte Zustände mit Inklusionsbeweisen. Alle sind vereinbar
mit einer Fälschung. Unabhängig prüfbar bleiben nur die Eingabe und das festgeschriebene Modell, anhand deren der Knoten
die Aufgabe selbst neu berechnen kann — etwa +100% Arbeit [Berechnung]; weder A noch B verlangt das, und für eine
private Anfrage hat ein fremder Knoten nicht einmal die Eingabe. Deshalb steht in der Tabelle oft „nein, außer vollständiger
Neuberechnung“.

### 1.7. Abspracheanteil `q_eff`

Alle Schwellen der Form „bis 91%“ beziehen sich auf den Anteil der Koalition unter denen, die die Aufgabe tatsächlich prüfen.
`q_eff` ist der Anteil der Koalition unter den Prüfern, die (1) zur Aufgabe zugelassen sind (nach Regel 2.6 der SPEC
braucht man bei einer Aufgabe eines langjährigen Ausführenden `H_v ≥ B`, bis `399R`), (2) innerhalb der Frist der Runde geantwortet haben und (3) Daten
zur Prüfung erhalten haben. Beispiel [Berechnung]: 3000 ehrliche Heimgeräte je 8 Stunden und 100 ehrliche
rund um die Uhr gegen 800 gemietete rund um die Uhr. Der Anteil des Gegners am gesamten Gewicht ist 42,1%
(19 200 von 45 600 Gerätestunden pro Tag); ein Heimgerät sammelt etwa `144R < 399R`
und wird zu Aufgaben langjähriger Ausführender nicht zugelassen; unter den Zugelassenen `q_eff = 800/900 = 88,9%`,
`q_eff³ ≈ 0,70`. Einwand der Kritiker: das betrifft Aufgaben mit `B = 399R`. Bedingung (3) kann
`q_eff` bei jedem Gesamtanteil bis auf eins heben (N2). Die Formel `q^k` gilt nur für unabhängige Auswahlen;
in der SPEC gehen die Runden bis zu drei Antworten, und für eine teilweise Absprache braucht man die Verteilung der Antwortenden.

### 1.8. Grundformeln [Berechnung]

- **A, eine Fälschung:** Gewinn `R − 4R(1 − q³)`; unrentabel bei `q < 0,9086`. **Neuling A:**
  `p = 1`, `B = H = 3R`, Gewinn `R(4q³ − 3)`.
- **A, Weggang mit Fälschungen** (Aufzählung FIRST_RUN auf einem Gerät, nicht bestätigt): lohnt ab
  `q = 0,875` (beliebige Größen, drei Wellen, Regel „nicht mehr als ein Drittel `H` in Arbeit“; 1,00004·H₀ bei
  0,875, 1,034·H₀ bei 0,880), ab 0,890 (gleiche Aufgaben), ab 0,800 ohne die Drittel-Regel; ohne Absprache
  gibt es in 92 Mio. Strategien keinen lohnenden Weggang (bestes 0,980·H₀). Das ist eine Aufzählung von Familien, kein Beweis.
- **B, eine Fälschung** lohnt bei `q^k > pH/(R + pH)`; bei `p = 1%`, `k = 3`: `q ≈ 0,928` für
  `H = 400R`, `0,659` für `40R`, jedes `q > 0` für `H = 0`. Die mittlere Bruttoauszahlung für eine Fälschung ist
  `R·q^k` und hängt nicht von `p` ab.
- **B, Welle aus `N` Fälschungen:** `E = a^N·H₀ + N·a^(N−1)·q^k·R`, `a = 1 − p(1 − q^k)`. Die erste
  Fälschung lohnt bei `H₀` unter 2,8R / 14,3R / 52R / 105R / 269R für `q` = 0,3 / 0,5 / 0,7 /
  0,8 / 0,9. Bei `H₀ = 0` ist der größte Gewinn je Schlüssel etwa `q^k·R/(e·p·(1 − q^k))`: 0,037R / 1,0R /
  5,3R / 19R für `q` = 0,1 / 0,3 / 0,5 / 0,7. Eine Welle ohne Aufzählung ist eine untere Schätzung.
- **Wahrscheinlichkeit einer falschen Auszahlung** je Aufgabe ohne externen Streitfall: in A `1 − p + p·s`, in B `p·s`
  (`s` — Wahrscheinlichkeit vollständiger Absprache bei der Auswahl); bei `p = 0,01`, `s = 0,125` — 0,99125 und 0,00125,
  und die Bruttoauszahlung für eine Fälschung bei `R = 1` — 0,99125 und 0,125. Die Varianten allein nach der Häufigkeit
  falscher Auszahlungen zu vergleichen ist nicht zulässig.

---

## 2. Abgleich „60 und 59“

In der SPEC gibt es genau 60 Zeilen (12 + 12 + 10 + 5 + 11 + 6 + 4): 18 geschlossen, 6 unrentabel, 19 begrenzt,
16 offen und **eine „kein Angriff“ — Zeile 1.9** (ein richtiges Ergebnis abzugeben, das auf fremder
Ausrüstung berechnet wurde, ist durch Entscheidung D2 erlaubt); die Zusammenfassung von CURRENT_DESIGN, Abschnitt 9, und der Absatz „Kurz“ in der SPEC
haben nur vier Kategorien summiert und die fünfte verloren, daher 59. Alle sechs Arbeiten und alle drei Kritiker
kamen unabhängig dazu. Die richtige Schreibweise: 60 = 18 + 6 + 19 + 16 + 1.

---

## 3. Angriffstabelle

### 3.1. Bezeichnungen

**Status:** geschl. — der Knoten verwirft den Angriff anhand der Daten des Journals unter den genannten Voraussetzungen;
unrent. — der Angriff ist möglich, im Mittel unrentabel bis zur genannten Grenze; begr. — möglich, Schaden oder
Gewinn sind durch eine Regel begrenzt; offen — es gibt keine Lösung; kein Angriff.

**D1:** ja — Gewinn nicht größer als null für jede Koalition; **nein** — es gibt eine Strategie mit
positivem Gewinn mindestens gegenüber einem Bezugspunkt; bed. — nur unter den genannten,
vom Abspracheanteil unabhängigen Voraussetzungen erfüllt (Voraussetzungen 1–4 der SPEC, noch nicht gebaut);
nein (Eff.) — es gibt keinen Geldgewinn oder er ist nicht festgestellt, aber es wird ein Gewinn durch den Effekt erreicht
(Abschnitt 1.5); n. z. — der Angriff enthält keine falsche Meldung um eines Gewinns willen, die genannte Anforderung ist betroffen;
? — die Regel ist nicht festgelegt, das Vorzeichen des Gewinns ist nicht festgestellt.

**Daten** — anhand welcher unabhängig prüfbaren Daten der Knoten eine falsche Meldung bei Absprache
des Ausführenden mit allen Prüfern verwirft. „strittig“ — Arbeiten oder Kritiker widersprechen sich, und der Streit ist nicht entschieden.
Verweise „N…“ führen zu neuen Angriffen in Abschnitt 3.9.

### 3.2. Ausführender

| Nr. | Kurz | A | D1 in A | B | D1 in B | Daten für die Ablehnung bei Absprache | Was zur Schließung nötig ist |
|---|---|---|---|---|---|---|---|
| 1.1 | Neuling mit leerem Konto gibt eine Fälschung ab | unrent. bis `q ≈ 0,909`: die ersten Aufgaben werden immer geprüft, Gewinn `R(4q³−3)`. Strittig: Kritiker ChatGPT hält die Zeile für offen, da die Start-`3R` durch Kopieren erlangt werden können (2.2, N1) | **nein** bei `q ≥ 0,909`, und bei jedem `q > 0` — über die Bezahlung von Lehrlings-Nachprüfungen | offen: `R·q^k` für einen Versuch ohne Verluste, Schlüssel beliebig viele | **nein** bei jedem `q > 0` | Nein, außer vollständiger Neuberechnung anhand der offenen Eingabe; für eine Anfrage — nur beim Nutzer | Die ersten bezahlten Ergebnisse mit einem Verfahren prüfen, das jeder Knoten selbst ausführt; bis dahin — nur unbezahlte Arbeit. In B — Zulassung nach `H` (N16) |
| 1.2 | Langjähriger Teilnehmer fälscht einen Teil der Aufgaben | unrent. bis `q ≈ 0,909`; 99% der Fälschungen werden nicht geprüft und bleiben im Netz | **nein** bei hohem `q` | unrent. bei `q^k R < p(1−q^k)H`: 0,928 bei `H = 400R`, 0,659 bei `40R`, jedes `q` bei `H = 0` oder von einem leeren Schlüssel (N16) | **nein** | Nein, außer vollständiger Neuberechnung | Prüfung des bezahlten Ergebnisses, unabhängig vom Abspracheanteil (Phase 4). In B — `p` und Zulassung in Abhängigkeit von `H` |
| 1.3 | Lange ehrlich, dann großer Betrug und Weggang | unrent. nur in den aufgezählten Familien unter 0,875 / 0,890 / 0,800 (Abschnitt 1.8) | **nein** bei `q ≥ 0,875`; darunter nicht bewiesen | offen: die Ausstiegskampagne ist nicht berechnet; bei kleinem `H` lohnt sie ab jedem `q > 0` | **nein** | Nein, außer Neuberechnung | Beweis für alle Strategien in A; Berechnung der Ausstiegskampagne in B, einschließlich `H₀ = 0` (Phase 2) |
| 1.4 | Gibt eine Fälschung ab und verschwindet, nachdem er die Stichprobe gesehen hat | geschl.: das Paket wird nicht widerrufen, das Verschwinden nach der Stichprobe ist ein falsches Ergebnis | bed. | ebenso | bed. | Zeile des Pakets und fehlende Offenlegung bis zur Frist | Ein ehrlicher Verbindungsausfall ist nicht unterscheidbar (Preis für die Ehrlichen); für eine private Anfrage — Verfügbarkeit der Eingabe |
| 1.5 | Erfährt die Stichprobe im Voraus oder wählt sie aus | offen heute: geschlossen nur unter Voraussetzung 2, und die Quellen sind nicht gewählt (so schätzten die Arbeiten ChatGPT; die Kritiker Claude und ChatGPT stimmen zu) | bed.; **nein** bei der Wahl durch die letzte Quelle (N13) | ebenso | ebenso | Öffentliche Werte des Beacons und des Blocks; Absprache über die Schwelle des Beacons oder Zurückhalten des Blocks sind daran nicht sichtbar | Quellen wählen; Runde des Beacons streng nach der endgültigen Annahme des Blocks; Vertrauen in externe Parteien als Annahme festhalten |
| 1.6 | Doppelte Bezahlung oder fremde Aufgabe | begr.: die Nummer ist eindeutig, aber eine Zeile mit fremder Aufgabe verwirft das Journal nur auf Einspruch; wenn der Ausführende für das gesamte Fenster ausgeschaltet ist, reift die Zeile aus. Alle drei Kritiker bestätigten | **nein**: Auszahlung `R` an einen fremden Schlüssel | ebenso | **nein** | Die Zuweisung ist berechenbar, wenn die Liste der zur Auslosung Zugelassenen im Journal liegt | Das Journal prüft die Zuweisung selbst bei der Annahme der Zeile (billig) |
| 1.7 | Weist sich selbst Aufgaben zu, erfindet Arbeit | offen: den Ausführenden wählt die Auslosung (dieser Teil ist geschlossen), aber die Regel zur Genehmigung des Trainingsplans ist nicht angenommen (ROADMAP, „Was nicht gelöst ist“, Nr. 5); die Wiederholung des Inhalts ergibt mehrere Zahlungen (N22). Kritiker DeepSeek: „geschlossen für einen festen Plan, offen für den Plan“ | **nein** | ebenso | **nein** | Der Knoten prüft, dass die Aufgabe im Plan steht; das Recht auf Ausgabe und die Nichtwiederholung — nicht | Regel des Plans im unveränderlichen Kern; Ausgabe nur nach einer erlaubten Planstelle; Gutschrift einmal nach dem Inhalt |
| 1.8 | Nimmt lohnende Aufgaben, wirft die übrigen weg | begr.: Weggeworfenes geht an einen anderen | ja bei gleichen Kosten; strittig, ob ein kleiner Gewinn aus der Auswahl bei ungleichen Kosten D1 verletzt | begr.; Auswahl nach der Auslosung ist unmöglich | ebenso | Zuweisung und Frist im Journal | Gleiche Selbstkosten der Aufgaben; die Quote sinkt nach weggeworfenen |
| 1.9 | Das Ergebnis wurde auf fremder Ausrüstung berechnet | kein Angriff (D2) | n. z. | kein Angriff | n. z. | — | Vom mehrfachen Abgeben desselben Ergebnisses unterscheiden (N1, N22) |
| 1.10 | Zieht den Streitfall in die Länge oder schweigt | begr.: Schweigen ist ein Verlust; bei kleinem `H` zahlt das Netz die Differenz der Kosten des Streitfalls | n. z.; strittig bei teurem Streitfall (N3) | begr.; `H` ist oft nahe null | ebenso | Timer der Züge im Journal | Fristen der Züge; Kostenvoranschlag des Preises des Streitfalls |
| 1.11 | Fälschungen vor dem Stillstand des Netzes | geschl.: das Fenster läuft nicht, solange das Netz steht; die Schwelle ist nicht gewählt | bed. | ebenso | bed. | Zeit des Fensters nach Paketen mit einem Gewichtsanteil nicht unter der Schwelle | Schwelle wählen (3.10); Zeilen für die Dauer des Stillstands speichern (N7) |
| 1.12 | Verbirgt eine Fälschung, indem er die Daten nicht herausgibt | offen für große Daten: „gegeben oder nicht gegeben“ sieht das Journal nicht; für das Training wird der Zustand des vorherigen Schritts benötigt | **nein** | offen; nicht bezahlt, aber bereits genutzt | **nein** | Für kleine Daten — Veröffentlichung in der Blockchain; für große — nein | Verfügbarkeit der Daten vor der Auslosung; „keine Daten bis zur Frist — falsch“ auch für den Trainingszustand (N2, M3) |

### 3.3. Prüfer

| Nr. | Kurz | A | D1 in A | B | D1 in B | Daten für die Ablehnung bei Absprache | Was zur Schließung nötig ist |
|---|---|---|---|---|---|---|---|
| 2.1 | Bestätigt, ohne neu zu berechnen | Strittig. geschl. für einen Prüfer außerhalb der Koalition (vier Arbeiten, die Kritiker Claude und DeepSeek); offen nach Einschätzung der Arbeiten ChatGPT und des Kritikers ChatGPT: innerhalb der Koalition sind dieselben Daten mit dem Fehlen einer Neuberechnung vereinbar | ja für einen nicht verbundenen; innerhalb der Koalition — 2.2 | ebenso | ebenso | Der eigene Zustand an einem zufälligen Punkt und ein Inklusionsbeweis; die Herkunft der Berechnung ist nicht prüfbar | Zwischenzustände nicht um der Verfügbarkeit willen veröffentlichen (N11) |
| 2.2 | Bezahlung der Prüfung der eigenen Gruppe ohne Neuberechnung | begr.: etwa 0,3% des Einkommens bei 10% Gewicht [Berechnung: 0,01·3·0,1] | **nein** bei jedem `q > 0`: Einsparung der Neuberechnung (fünf Arbeiten, alle drei Kritiker) | begr., wenn die Prüfung in B wie in A bezahlt wird (Tarif nicht festgelegt) | **nein** bei derselben Bezahlung | Nein: Neuberechnung und Kopie ergeben dieselben Daten | Nicht für die Wiederholung zahlen; die Reparatur „aus der Belohnung der geprüften Aufgabe zahlen“ setzt den Gewinn nicht auf null (Abschnitt 4.5) |
| 2.3 | Absprache des Ausführenden mit allen Prüfern | unrent. bis `q_eff ≈ 0,909` (Weggang — 0,875) | **nein** | unrent. nach der Formel in Abschnitt 1.8 | **nein** | Nein, außer vollständiger Neuberechnung; private Anfrage — nur beim Nutzer | Prüfung, die nicht vom Abspracheanteil abhängt (Phase 4), oder eine ausdrückliche Abschwächung von D1 (Frage 2) |
| 2.4 | Bestechung oder Druck nach der Stichprobe | offen: der Prüfer einer Anfrage offenbart sich dem Ausführenden; Bestechung über einen Vertrag (N4); mit M1 riskiert der Bestochene nichts. Die Herabstufung bestätigten alle drei Kritiker | **nein** | ebenso; bei `H = 0` ist die Bestechung billiger | **nein** | Nein | Anfrage an die Prüfer ohne Kontakt zum Ausführenden; Folgen der Nichtoffenlegung (M1) |
| 2.5 | Eine Gruppe antwortet zuerst und besetzt die Plätze | geschl.: alle Antworten innerhalb der Frist werden gezählt; die Frist ist nicht gewählt | bed. | ebenso | bed. | Zeit der Antworten im Journal | Frist der Runde nicht kürzer als der Tageszyklus; den Anstieg von `q_eff` berücksichtigen |
| 2.6 | Ein Eintrag mit Gewicht ohne `H` bestätigt Fälschungen | geschl.: Zulassung nur bei `H_v ≥ B`; Nebenwirkung — Anstieg von `q_eff` (N5) | ja | offen: eine Zulassungsregel in B gibt es nicht | **nein**: die Koalition erhält `R/p` ohne Risiko | `H` des Prüfers im Journal (in A) | Eigenes Maß der Verantwortung des Prüfers in B |
| 2.7 | Beschuldigt einen ehrlichen Ausführenden falsch | geschl. unter Voraussetzung 4 (nicht gebaut) | bed. | ebenso | bed. | Neuberechnung des Schritts im Journal | Referenzmaschine des vollständigen Modells; Rückerstattung nach Timeout — 2.8, 4.2 |
| 2.8 | Beschuldigt einen ausgeschalteten Ausführenden | begr.: bei einer privaten Anfrage gibt es keinen Verteidiger, `H` des Ehrlichen wird verbrannt | **nein** für die Verbindung „Nutzer + Prüfer“ (Rückerstattung für eine erhaltene richtige Antwort); n. z. für reine Sabotage | ebenso | ebenso | Für das Training schützt jeder anhand der offenen Eingabe; für eine private Anfrage gibt es keine Daten | Kopie der Anfrage, die dem Verteidiger ohne Offenlegung zugänglich ist |
| 2.9 | Strom falscher Streitfälle | begr. durch den Preis `H` des Angreifers | n. z. (billige Prüfung) | begr.; in B ist `H` oft 0 | n. z. | Ausgang des Streitfalls im Journal | Den Widerspruch N23 entscheiden |
| 2.10 | Abfangen eines fremden Funds | offen: die Reihenfolge ist nicht ausgearbeitet | **nein**: Anteil des Abgezogenen für den Abfänger | offen; die Prämie in B ist nicht festgelegt | ? | Verdeckter Einspruch `hash(Fund ‖ Schlüssel)` mit Blockmarkierung | Verdeckte Abgabe mit Offenlegung und Bindung an den Schlüssel (billig); belegt den Vorrang der Fixierung, nicht den Zeitpunkt der Öffnung |
| 2.11 | Denunziert seine eigene Fälschung für einen Anteil am Abzug | geschl. für die gewählte Aufgabe; eine gesonderte Selbstdenunziation ist unrentabel | ja | die Prämie in B ist nicht festgelegt | ? | Das Journal zahlt dem Finder nichts vor dem Ende der zugewiesenen Prüfung | Prämienregel für B |
| 2.12 | Weigert sich zu prüfen | begr.: die Auslosung geht in die nächste Runde | n. z.; strittig: bei `G > B` ist dem Nichtzustimmenden Schweigen vorteilhafter (N3), hängt vom Kostenvoranschlag `G` ab | ebenso | ebenso | — | Kostenvoranschlag `G`; Folgen des Nichterscheinens ohne Pfänder |

### 3.4. Menge der Einträge, Gewicht und Abstimmungen

| Nr. | Kurz | A | D1 in A | B | D1 in B | Daten für die Ablehnung bei Absprache | Was zur Schließung nötig ist |
|---|---|---|---|---|---|---|---|
| 3.1 | Tausende Konten | geschl. für Gewicht und Stimmen; im Ganzen begr.: Lehrlingszahlungen, Verteilung und Zuweisungen wachsen mit der Zahl der Schlüssel (Kritiker Claude und DeepSeek). Kritiker ChatGPT: die Zahl der bezahlten Versuche hängt von den zugewiesenen Plätzen ab, nicht von Registrierungen | **nein** | offen: jeder Schlüssel mit Zuweisung ist ein Los mit Erwartung `R·q^k` | **nein** | Keine Daten, die Schlüssel verbinden | Zugang ohne Auszahlungen bis zur unabhängigen Prüfung; in B — Zulassung nach `H` (N16) |
| 3.2 | Gewicht durch Fälschungen oder Anfragen an sich selbst aufblähen | unrent. bis zur Schwelle; ungeprüfte Fälschungen, die das Fenster passiert haben, erhalten Gewicht | **nein** an der Grenze | offen: bei `H = 0` gibt eine gewählte Fälschung fast umsonst Gewicht | **nein** | Nein, außer Neuberechnung | Gewicht nur für unabhängig Geprüftes; „Fenster passiert“ (SPEC) und „Prüfung bestanden“ (CURRENT_DESIGN) abstimmen |
| 3.3 | Mietet Rechenleistung und sammelt ehrlich Gewicht | offen in einem kleinen Netz: für ¾ des Gewichts — anderthalb Monate mit dreifach mehr Arbeit als die übrigen, für 91% — zehnfach [Berechnung SPEC] | n. z. (Miete durch D2 erlaubt); führt zu 2.3 und 3.7 | ebenso | n. z. | Nein: die Arbeit ist ehrlich | Prüfung, die nicht vom Gewichtsanteil abhängt; unveränderlicher Kern (D4) |
| 3.4 | Große Aufgaben, die nur er selbst prüft | geschl. durch die Regel gleicher kleiner Größe; die Übernahme kleiner Aufgaben eines seltenen Modells — Zeile 3.5 | ja | ebenso | ja | Größe der Aufgabe — Regel des Kerns | — |
| 3.5 | Übernahme der Prüfungen eines seltenen Modells | offen: `q_eff ≈ 1` ist erreichbar | **nein** | ebenso | **nein** | Nein | Ein Modell nicht ohne Schwelle unabhängiger Prüfer auf anderer Ausrüstung bezahlen |
| 3.6 | Leere Einträge auf Lehrlingsplätzen | offen: Warteschlange ehrlicher Neulinge; Bezahlung des Lehrlings für eine Kopie (2.2) | **nein** über die Kopie; n. z. für die Warteschlange | offen; das Budget der Plätze nimmt, wer mehr Schlüssel hat | **nein** | Nein | Nicht für die Lehrlings-Nachprüfung zahlen; Frist der Freigabe des Platzes (N28) |
| 3.7 | ¾ des Gewichts ändern die Regeln zu ihren Gunsten | Strittig. Kritiker Claude und DeepSeek: offen — D4 schützt den Prüfkern, aber nicht Ausgabe, Bezahlungssatz, Entgelt, Bremse und Katalog. Kritiker ChatGPT: begr. — D4 hat Vorrang vor der alten SPEC, der Profit verlangt eine konkrete Änderung | **nein** (Übernahme der Ausgabe), strittig | ebenso | ebenso | Fingerabdruck des Kerns: der Knoten lehnt eine Version ab, die den Kern ändert | Zusammensetzung des Kerns auflisten (Frage 5) |
| 3.8 | Blockiert Entscheidungen (½ — Modell, ¼ — Regeln) | begr.: umkehrbar, aber der Fehler lässt sich nicht beheben | n. z. (Lebensfähigkeit) | ebenso | n. z. | — | — |
| 3.9 | Kauft Stimmen | begr.: ¾ des gesamten Gewichts sind nötig; die Bestechung führt ein Vertrag aus | wie 3.7: **nein**, wenn die Mehrheit die Ausgabe ändert; strittig | ebenso | ebenso | Nein | Wie 3.7 |
| 3.10 | Hört auf, Pakete abzugeben, um das Fenster einzufrieren | offen: hohe Schwelle — Einfrieren der Auszahlungen; niedrige — die Koalition hält das Fenster mit ihren Paketen, Fälschungen reifen aus (N14) | **nein** (Zweig niedriger Schwelle) | ebenso; eine gewählte Fälschung erhält `R/p` | **nein** | Zeit und Gewichtsanteile der Pakete | Schwelle mit Beweis beider Grenzen; aktives Gewicht des Netzes und Zusammensetzung der Prüfer unterscheiden |

### 3.5. Nutzer

| Nr. | Kurz | A | D1 in A | B | D1 in B | Daten für die Ablehnung bei Absprache | Was zur Schließung nötig ist |
|---|---|---|---|---|---|---|---|
| 4.1 | Zahlt nicht für die Antwort, gibt Credits zweimal aus | begr. durch einen Teil der Antwort; die doppelte Ausgabe ist geschlossen | **nein**: der unbezahlte Teil ist eine positive Leckage (Frage 3) | ebenso | **nein** | Fixierung der Credits; die Übergabe eines Teils sieht das Journal nicht | Ein ehrlicher Austausch ohne vertrauenswürdige Partei ist im Allgemeinen unmöglich: den Teil verkleinern oder die Annahme anerkennen |
| 4.2 | Bestreitet eine richtige Antwort, um eine Rückerstattung zu erhalten | offen auf zwei Wegen: der Streitfall wird durch die Übereinstimmung der Prüfer nach der Auslosung geschlossen (N17); Rückerstattung nach Timeout bei ausgeschaltetem Ausführenden. Die Einschätzung „geschlossen“ in drei Arbeiten hielten alle drei Kritiker für zu hoch | **nein** | ebenso | **nein** | Neuberechnung im Journal — nur wenn der Streitfall dorthin gelangt ist | Recht, den Streitfall bis zur Neuberechnung zu führen; Timeout-Regel; Verteidiger mit Daten |
| 4.3 | Nutzer und Ausführender geben Credits durch Anfragen aus | geschl.: Anfragen geben keine Credits aus | ja | geschl., wenn `R/p` nur aus den Zahlungen der Nutzer bezahlt wird; die Quelle ist nicht festgeschrieben | bed. | Regel der Ausgabe | Die Quelle von `R/p` in B festschreiben (Frage 12) |
| 4.4 | Überflutet das Netz mit Anfragen | begr. durch die Wallet | n. z. | ebenso | n. z. | — | — |
| 4.5 | Kopiert das Modell und bedient außerhalb des Netzes | offen in der Rechnung der SPEC (gehört zu den 16) | n. z.: Risiko für die Nachfrage | ebenso | n. z. | — | — |

### 3.6. Journal, Programm und Verbindung

| Nr. | Kurz | A | D1 in A | B | D1 in B | Daten für die Ablehnung bei Absprache | Was zur Schließung nötig ist |
|---|---|---|---|---|---|---|---|
| 5.1 | Schreibt die Historie oder Konten um | geschl. unter Voraussetzung 1 | bed. | ebenso | bed. | Endgültige Blöcke über unabhängige Punkte | Formale Prüfung des Journalprogramms |
| 5.2 | Der Schreibknoten lässt Einträge nicht durch oder verfälscht sie | begr. für Zensur (ein eigener Eintrag kostet Blockchain-Münzen, für ein leeres Konto unzugänglich); offen für eine Zeile mit falschem Preis oder Empfänger ohne Einspruch (Kritiker DeepSeek und ChatGPT) | **nein** | ebenso | **nein** | Preis und Empfänger sind prüfbar, aber derzeit nur auf Einspruch | Prüfung der Zeile bei der Annahme; Erstattung von Einträgen ohne Ausgabe (N12) |
| 5.3 | Ein falsches Programm für den Neuling | offen: Adresse und Referenz aus einer Quelle | n. z. (Echtheit) | ebenso | n. z. | Nein bis zur ersten Installation | Unabhängige Quellen für Adresse und Fingerabdruck; reproduzierbarer Build |
| 5.4 | Schädliches Update | begr.: D4 erlaubt, einen fremden Fingerabdruck des Kerns abzulehnen; einen reproduzierbaren Build des Programms des Knotens gibt es nicht, deshalb hält „geschlossen“ in der SPEC nicht; für das übrige Programm — offen. | n. z. | ebenso | n. z. | Fingerabdruck im Journal ohne prüfbare Verbindung zum Quelltext | Reproduzierbarer Build; die Übereinstimmung mit dem genehmigten Text beweist nicht dessen Sicherheit |
| 5.5 | Bezahlung für nicht existierende Speicherung oder Ausgabe an sich selbst | geschl.: für Speicherung wird nichts ausgegeben | ja | ebenso | ja | Regel der Ausgabe | — |
| 5.6 | Nimmt die Bezahlung, gibt die Daten nicht heraus | begr. durch einen Teil | **nein**: Leckage eines Teils auf der Seite des Empfängers ohne Quittung (Frage 3) | ebenso | **nein** | Fingerabdruck des Teils; die Quittung bestätigt die Bezahlung, nicht die Lieferung | Wie 4.1 |
| 5.7 | Blockiert alle Wege des Treffpunkts | offen bei Blockierung aller Wege | n. z. (Verteiltheit) | ebenso | n. z. | — | — |
| 5.8 | Umringt den Knoten mit einem falschen Zustand | begr. durch das Vertrauen in zwei von drei Anbietern; bei deren Absprache — offen (N29) | bed. | ebenso | bed. | Endgültiger Block über unabhängige Punkte | Leichtclient mit Konsensprüfung |
| 5.9 | Teilt das Netz für zwei Auszahlungen | geschl.: ein Journal | ja | ebenso | ja | Nummer der Aufgabe in einem Journal | Regelspaltung — N15 |
| 5.10 | Stiehlt einen Arbeitsschlüssel | begr.: der Schlüssel gibt keine Credits der Wallet aus | Strittig: n. z. (Schaden für das Opfer) oder **nein** — gestohlene Schlüssel bestätigen Fälschungen auf fremdes `H` (N9, vom Kritiker Claude unterstützt) | ebenso | ebenso | Die Signatur zeigt nicht den Betreiber | Widerruf des Schlüssels; Hardware-Speicherung |
| 5.11 | Erschöpft die kostenlose Verteilung | offen: ob es für Neulinge reicht, ist nicht geprüft | n. z. (Dienstverweigerung); strittig, wenn die Vergünstigung „dem zuerst Gekommenen“ gilt | ebenso | ebenso | Ein neuer Besitzer ist von einem neuen Schlüssel des bisherigen nicht unterscheidbar | Verteilung nur nach bereits zugewiesenen Aufgaben |

### 3.7. Modell und Training

| Nr. | Kurz | A | D1 in A | B | D1 in B | Daten für die Ablehnung bei Absprache | Was zur Schließung nötig ist |
|---|---|---|---|---|---|---|---|
| 6.1 | Der Saboteur gibt falsche Beiträge ab | begr.: etwa `x/3` der Beiträge bei einem Arbeitsanteil `x` [Berechnung SPEC]; bei vollständiger Absprache nicht bewiesen; der Beitrag wirkt sofort (N21) | n. z. nach Credits; nein (Eff.) | offen: eine nicht gewählte Fälschung ist kostenlos, die Grenze `x/3` gilt nicht (Kritiker Claude und ChatGPT) | **nein** | Nein, außer Neuberechnung | Nur geprüfte Beiträge übernehmen (Preis — Verzögerung und Speicher) |
| 6.2 | Verborgenes Verhalten | offen: das Examen fängt eine Verschlechterung, nicht eine Hintertür | nein (Eff.) | ebenso | nein (Eff.) | Nein; eine Hintertür ist auch bei einem richtigen Schritt möglich | Forschungsaufgabe |
| 6.3 | Schädlicher Datensatz oder fremde Lizenz | offen: eine richtige Berechnung auf schädlichen Daten lässt sich nicht beheben | n. z.; nein (Eff.) | ebenso | ebenso | Nein: Hash und Aufschrift sind beim Rechteinhaber und beim Fremden gleich | Den Katalog auf prüfbare Quellen beschränken |
| 6.4 | Anpassung an das Examen | begr.: die Aufgaben werden nach der Fixierung gewählt | nein (Eff.) im Bereich des Nichtmessbaren | ebenso | ebenso | Zeit der Wahl der Aufgaben | — |
| 6.5 | Fälschung der Ergebnisse des Examens | unrent. bis zur Schwelle 2.3; das Examen wird immer geprüft, ohne Lotterie | **nein** bei hohem `q` | wie in A; die Formel `R·q^k` ist auf das Examen nicht anwendbar (Abschnitt 4.5) | **nein** | Das Examen ist klein und offen: jeder Knoten kann es selbst neu berechnen | Neuberechnung des Examens durch jeden Knoten (empfahl Kritiker DeepSeek; Kritiker ChatGPT: Preis und Verbindlichkeit sind nicht festgestellt) |
| 6.6 | Übernahme der Abstimmung über den Plan | begr.: Eigenschaft des Schemas | n. z.; **nein** in Verbindung mit 1.7 | ebenso | ebenso | Nein | Siehe 1.7 |

### 3.8. Vertraulichkeit

| Nr. | Kurz | A | D1 in A | B | D1 in B | Daten für die Ablehnung bei Absprache | Was zur Schließung nötig ist |
|---|---|---|---|---|---|---|---|
| 7.1 | Der Besitzer des Geräts liest die Anfragen | offen im gewöhnlichen Modus | n. z.; nein (Eff.) — die Privatsphäre ist verletzt | ebenso | ebenso | Nein | Geschützter Modus zum Preis des Vertrauens in den Hersteller (N25) |
| 7.2 | Massensammlung fremder Anfragen | begr. durch den Anteil der Zuweisungen und Prüfplätze | n. z.; nein (Eff.) | ebenso | ebenso | — | — |
| 7.3 | Verknüpfung der Anfragen eines Nutzers | offen: Pseudonym und Adressen beim Relais | n. z. | ebenso | n. z. | — | Nicht verknüpfbare Bezahlung |
| 7.4 | Lesen einer Anfrage durch Prüfung oder Streitfall | offen: etwa 1% der Anfragen sehen drei weitere Geräte; ein falscher Streitfall veröffentlicht ein Fragment | n. z.; nein (Eff.) | ebenso; der Anteil `p` begrenzt die Offenlegung nicht — den Streitfall eröffnet der Nutzer | ebenso | — | Streitfall ohne Offenlegung (Zero-Knowledge-Beweis des Schritts) |

### 3.9. Neue Angriffe, vom Rat gefunden

Doppelte aus verschiedenen Arbeiten sind zusammengeführt. „Arbeiten“ — wie viele der sechs Arbeiten der Runde 1 den Angriff herausgestellt haben;
„Kritiken“ — das Ergebnis der Runde 2. Die Nummern N1… sind eigene für dieses Dokument und stimmen nicht mit lokalen
Nummern in den Arbeiten überein. Widerlegte neue Angriffe gibt es nicht; wo die Begründung widerlegt ist, ist das gesagt.

| Nr. | Angriff | Arbeiten | Kritiken | A · D1 | B · D1 | Was zur Schließung nötig ist |
|---|---|---|---|---|---|---|
| N1 | **Eine Berechnung — viele Zahlungen.** Ein Schlüssel der Koalition berechnet einmal eine fremde (sogar ehrliche) Aufgabe neu und verteilt den Rechenschritt an alle seine Schlüssel, die als Prüfer oder Lehrlinge auf diese Aufgabe gefallen sind. Verallgemeinert 2.2: eine Absprache mit dem Ausführenden ist nicht nötig | 1 | Alle drei bestätigten; der Vorteil wächst mit der Zahl der zugewiesenen bezahlten Plätze, nicht der Schlüssel | offen · **nein** | offen · **nein** | Es gibt keine Daten. Keine Auszahlung darf von der Wiederholung bereits geleisteter Arbeit abhängen |
| N2 | **Aushungern ehrlicher Prüfer mit Daten.** Ein Prüfer holt die Anfrage beim Ausführenden und offenbart sich; der Ausführende der Koalition gibt die Anfrage nur den eigenen; ein Ehrlicher antwortet nicht auf „nicht erhalten“ und verliert nichts; die Runden laufen, bis drei Antworten der Koalition beisammen sind | 1 (teilweise noch 3) | Richtig mit dem Vorbehalt: nötig sind etwa `3/(λ·q)` Tagesrunden — etwa 15 Tage bei `q = 5%`, `λ ≈ 4`, etwa 75 Tage bei `q = 1%` [Berechnung], und der Angriff ist im Journal bemerkbar. Der Mechanismus „Veröffentlichung einer verschlüsselten Kopie“ ist in der SPEC genannt, aber nicht definiert. Für das Training — nur bei einer einzigen Kopie der Eingabe | offen · **nein** für Anfragen | offen · **nein** | Das Journal sieht die Übergabe nicht. Verfügbarkeit der Eingaben vor der Auslosung; für eine private Anfrage gibt es keine Lösung; siehe M3 |
| N3 | **Der Streitfall ist teurer als der Einsatz.** Das Spiel des Streitfalls im Piloten — 93 Transaktionen, 5,8–6,3 Mio. gas: etwa 18 $ bei 1 Gwei und 3000 $ für ETH, etwa 360 $ bei 20 Gwei [Berechnung; die Preise sind Annahmen]. Die Wiederholung einer Zeile — 14,1 Mio. gas, ein anderer Prototyp, nicht addierbar | 1 (angrenzend noch 3) | Richtig als Dilemma, die Zahlen sind bedingt: entweder trägt die rechte Seite `G − B`, und der ehrliche Nichtzustimmende schweigt; oder das Netz erstattet `G` (so liest sich 1.10 der SPEC), und der Saboteur zwingt das Netz, `G` für jede erwischte Fälschung zu zahlen | offen · **nein** | offen · **nein** | Kostenvoranschlag `G` für die gewählte Chain; Aufgaben, deren Fehler einen Streitfall erfordert — nur bei `H ≥ G` |
| N4 | **Bestechung „P+ε“:** der Vertrag zahlt dem Prüfer ε für die Bestätigung und verspricht, `H_v` bei einer Erwischung zu erstatten. Unterart von 2.4 | 1 | Kritiker DeepSeek: wesentlich; Kritiker ChatGPT: Ausführbarkeit und Gleichgewicht sind nicht bewiesen | offen · **nein** | offen · **nein** | Eine Prüfung, bei der die Zustimmung nichts entscheidet; siehe M1 |
| N5 | **Anstieg von `q_eff` durch die Zulassung `H_v ≥ B`:** 42,1% des Gesamtgewichts ergeben 88,9% unter den Zugelassenen (Abschnitt 1.7) | 2 | Bestätigt; nur für Aufgaben mit `B = 399R` | begr. · **nein** bei Übernahme | offen (2.6) | Grenzen nach `q_eff` berechnen; den Kompromiss zwischen der Größe des Abzugs und der Breite der Runde berechnen |
| N6 | **Gewicht verschwindet nach 30 Kalendertagen Stillstand:** das Fenster steht, das Gewicht wird „für 30 Tage“ gezählt; die erste zurückgekehrte Gruppe erhält das gesamte Gewicht | 1 | Richtig nach dem Wortlaut der SPEC, aber bedingt: Kalender- oder aktive Zeit ist nicht gesagt; bei null Gewicht aller ist die Auslosung nicht bestimmt | offen · **nein** | offen · **nein** | Gewicht nach der aktiven Zeit des Netzes zählen (billig) und die erstmalige Gutschrift festlegen |
| N7 | **Zeilen der Pakete leben etwa 18 Tage, das Fenster kann länger stehen:** nach dem Stillstand bleibt eine Wurzel ohne Zeilen, es gibt nichts zu bestreiten | 3 | Alle bestätigten | offen · ? | offen · ? | Zeilen und Gründe der Übergänge für die gesamte Dauer von Prüfung und Streitfall speichern; ohne Daten wartet eine strittige Buchung |
| N8 | **Ein eigenes Modell im Katalog ergibt `q = 1`:** ein Modell, das nur die Ausrüstung der Koalition zieht | 1 | Kritiker ChatGPT: das ist eine Verbindung von 1.7, 3.5 und 6.6; dass ein kleiner Gewichtsanteil ein Modell in den Katalog bringt, ist nicht bewiesen | offen · **nein** | offen · **nein** | Ein Modell nicht ohne einen Mindestkreis von Prüfern auf anderer Ausrüstung bezahlen |
| N9 | **Fremde Geräte als kostenloses Gewicht der Prüfer:** gestohlene Arbeitsschlüssel bestätigen Fälschungen, `H` der Opfer verbrennt. Erweiterung von 5.10 | 1 | Bestätigt; der Zuwachs von `q` — nach dem Gewicht der übernommenen Schlüssel, nicht nach der Zahl der Geräte | offen · **nein** | offen · **nein** | Hardware-Speicherung des Schlüssels; die Kompromittierung im zulässigen `q` berücksichtigen |
| N10 | **Sofortige Abgabe von Fälschungen erhöht den Strom der Zuweisungen** (B) | 1 | Bedingt: ein Anstieg um das 10–100-Fache folgt nicht aus den Regeln der SPEC | begr. · ja | offen · **nein** | Tempo der Zuweisungen nur nach geprüfter Arbeit |
| N11 | **Verfügbarkeit gegen 2.1:** die Veröffentlichung von Zwischenzuständen um N2 willen erlaubt Bestätigungen ohne Neuberechnung | 1 | Eine Einschränkung der vorgeschlagenen Änderung, kein eigenständiger Angriff | — | — | Nur Eingaben veröffentlichen, Zwischenzustände — im Streitfall |
| N12 | **Gebühr für den Eintrag ins Journal über die Kosten hinaus:** Erstattung von Müll-Einträgen oder ein Kartell der Schreibknoten | 2 | Die Erstattungsregel ist in der SPEC nicht definiert; das gewöhnliche Einkommen eines Vermittlers verletzt D1 nicht | offen · bed. | offen · bed. | Nur Einträge mit angenommenen Ergebnissen erstatten und nicht mehr als die tatsächliche Kommission |
| N13 | **Wahl durch die letzte Zufallsquelle:** wenn die Runde des Beacons vor dem entscheidenden Block bekannt ist, wählt dessen Produzent aus zwei Werten; in A `p → p²`, Gewinn etwa +0,96R pro Fälschung [Berechnung]. Kritiker Claude: bei im Voraus bekanntem Zeitplan der Produzenten gibt die Koalition Pakete passend zu ihren Blöcken ab | 4 | Alle bestätigten; die Zahlen — nur bei falscher Reihenfolge der Quellen | offen · **nein** bei falscher Reihenfolge | ebenso | Runde des Beacons streng nach der endgültigen Annahme des Blocks |
| N14 | **Das Fenster läuft ohne Mehrheit:** eine Koalition von 40%, das Abschalten der Hälfte der Ehrlichen gibt ihr 40/70 = 57% unter den Aktiven [Berechnung]. Unterart von 3.10 | 2 | Bestätigt als Unterart von 3.10 | unrent. · **nein** für Leckagen vom Typ B | offen · **nein** | Siehe 3.10 |
| N15 | **Spaltung der Regeln:** noch nicht ausgereifte Beträge reifen in zwei Zweigen aus | 1 | Bedingt: die Verdopplung einer Verbindlichkeit ist nicht bewiesen | offen · ? | offen · ? | Ein gesonderter Vertrag mit getrennten Salden |
| N16 | **In B ist die Abschreckung an den Schlüssel gebunden, der Zugang zu Aufgaben nicht:** Fälschungen von einem gesonderten leeren Schlüssel ergeben `R·q^k` ohne Verluste. Gemeinsame Wurzel von 1.1-B, 1.2-B, 1.3-B, 3.1-B | 2 + Kritiker Claude | Zwei Arbeiten begründeten das Loch damit, dass bei einem gewöhnlichen Teilnehmer in B `H = 0` in 23,5–54,7% der Fenster ist; dieses Argument ist widerlegt (Abschnitt 4.5). Die richtige Form gab Kritiker Claude | — | offen · **nein** | Zulassung zu Losen bei `H` nicht unter der erwarteten Auszahlung für eine Fälschung; dann verliert B den konstanten niedrigen Prüfanteil (Frage 8) |
| N17 | **Den Streitfall des Nutzers entscheidet die Stichprobe, nicht die Arithmetik:** der Streitfall ist geschlossen, wenn die Prüfer nach der Auslosung mit dem Ausführenden übereinstimmten | 1 | Bestätigten die Kritiker Claude und DeepSeek; Kritiker ChatGPT: richtig, aber 4.2 betrifft die entgegengesetzte Behauptung | offen · **nein** | offen · **nein** | Recht, den Streitfall bis zur Neuberechnung im Journal zu führen |
| N18 | **Fälschungen → Gewicht → `q`.** Erweiterung von 3.2 | 1 | Bestätigt; die finanzielle Schlussfolgerung erfordert die Berücksichtigung künftiger Auszahlungen | begr. · **nein** an der Grenze | offen · **nein** | Gewicht nur für unabhängig Geprüftes |
| N19 | **Müll von kostenlosen Schlüsseln vor der Zuweisung** überlastet Knoten und Warteschlangen | 4 | Bestätigt; ein Platz für einen ehrlichen Neuling ist in keiner Variante garantiert. Die Einschätzung „Müll kostet dem Netz 3–4,5 Arbeit bei fast null Kosten in A“ widerlegte Kritiker Claude | offen · n. z. | offen · **nein** in Verbindung mit kostenlosen Losen | Nachrichten ohne Zuweisung vor der teuren Verarbeitung ablehnen; der Weg von einem leeren Konto ist verbindlich |
| N20 | **Aufgezwungene Abweichung der Arithmetiken** des Ausführenden und des Schiedsrichters | 2 | Bestätigt; die Abweichung selbst beweist keinen Gewinn | offen · ? | offen · ? | Eine einheitliche ausführbare Semantik der Operationen und Prüfung der Implementierungen am Referenzmodell |
| N21 | **Nutzung des Ergebnisses vor der Prüfung:** die Antwort ist gelesen, der Schritt ist als nächster Schritt übernommen und bleibt in der Abstammungslinie des Modells | 5 (+1 in 6.1) | Alle bestätigten; Schaden ist auch bei `q = 0` möglich; `1 − p` ist der Anteil der nicht gewählten, nicht der nicht angewandten | offen · nein (Eff.) | offen · nein (Eff.) | Den Block vor der Ausgabe prüfen; nur einen geprüften Nachkommen übernehmen (Preis — Verzögerung und Speicher) |
| N22 | **Ein Ausgaberecht unter verschiedenen Nummern** (gleiche Probeläufe, Wiederholung eines Schritts nach einem Neustart) | 3 | Bestätigt; zwei rechtmäßige Aufträge können dieselbe Ausgabe haben | offen · **nein** | offen · **nein** | Gutschrift einmal nach dem kanonischen Recht auf die Planstelle |
| N23 | **Widerspruch der Regeln des Streitfalls von einem leeren Konto** (ROADMAP verlangt ihn, SPEC — nicht) | 1 | Bestätigten die Kritiker DeepSeek und ChatGPT | offen · n. z. | offen · n. z. | Entscheidung des Eigentümers (Frage 4) |
| N24 | **Aneignung der Aufgabe eines ausgeschalteten Ausführenden** — Erweiterung von 1.6 | 2 | Bestätigt | siehe 1.6 | siehe 1.6 | Prüfung der Zuweisung bei der Annahme der Zeile |
| N25 | **Absprache mit dem Hersteller des geschützten Modus** | 1 | Richtig im Rahmen von 7.1 | offen · n. z. | offen · n. z. | Die Annahme des Vertrauens in den Hersteller festhalten |
| N26 | **Falsche Quittungen über die Übergabe von Daten** | 1 | Kein externes Einkommen: die Koalition zahlt sich selbst | offen · n. z. | offen · n. z. | Es gibt kein Merkmal der Übergabe großer Daten |
| N27 | **Selektive Nichtlieferung durch ein Relais** | 1 | Bestätigt für die Verfügbarkeit | begr. · n. z. | begr. · n. z. | Mehrere Relais, Ersatzwege |
| N28 | **„Ewiger Lehrling“** besetzt einen Platz und schließt die Nachprüfung nicht ab (zu 3.6) | 1 | Bestätigt | offen · n. z. | offen · n. z. | Frist und automatische Freigabe des Platzes |
| N29 | **Absprache zweier von drei Anbietern eines Kontrollpunkts** (zu 5.8) | 1 | Bestätigt; „mehr Anbieter“ löst eine Absprache der erforderlichen Mehrheit nicht | begr. · bed. | begr. · bed. | Leichtclient mit Konsensprüfung |
| N30 | **Dem Nutzer wird ein Block ausgegeben, der vom festgeschriebenen abweicht** | 1 | Bestätigt | offen · ? | offen · ? | Den ausgegebenen Block an das Commitment binden und vor der Nutzung prüfen |
| N31 | **Ein gemeinsamer Fehler im Kern selbst** nimmt einen falschen Übergang bei allen Knoten an | 1 | Bestätigt; verschieden von N20 | offen · ? | offen · ? | Unabhängige Spezifikation des Übergangs; nach D4 ist die Behebung — nur der Übergang in ein neues Netz |
| N32 | **Erkennung einer kurzen privaten Anfrage am öffentlichen Fingerabdruck** | 2 | Bedingt bestätigt: deterministischer Hash und eine kleine Menge von Texten | offen · nein (Eff.) | ebenso | Verbergende Commitments mit frischer Zufälligkeit |

**Nur von Kritikern gefunden** (von anderen Teilnehmern nicht geprüft):

| Nr. | Angriff | Wer | A · D1 | B · D1 | Was zur Schließung nötig ist |
|---|---|---|---|---|---|
| M1 | **Kostenlose Weigerung, offenzulegen.** Die Prüfer der Koalition geben ein verdecktes „bestätige“ ab und legen es nur offen, wenn alle abgegebenen Antworten ihre sind; sonst schweigen sie und verlieren nichts. Die Bestechung eines fremden Prüfers wird risikolos: statt des Risikos `399R` — null [Berechnung]. Bedingung: ob verdeckte Antworten vor der Offenlegung sichtbar sind — in der SPEC nicht definiert | Kritiker Claude | offen · **nein** | offen · **nein** | Folgen der Nichtoffenlegung ohne Pfänder (Verlust von Bezahlung und Gewicht für die Runde) oder Verbergen von Zahl und Urheberschaft der Antworten; der Preis für ausgeschaltete Ehrliche ist nicht berechnet |
| M3 | **Last durch den Verfügbarkeitsmechanismus.** Wenn auf „nicht erhalten“ mit der verbindlichen Veröffentlichung einer Kopie geantwortet wird, erklärt ein Prüfer der Koalition immer „nicht erhalten“; bei `q = 10%`, `λ ≈ 4` sind das etwa 34% der gewählten Aufgaben [Berechnung] | Kritiker Claude | offen · n. z. | ebenso | Die Erklärung der Nichtlieferung muss dem Erklärenden nicht weniger kosten als die verursachte Veröffentlichung (aus seinem `H`) |
| M4 | **Ausfall und Betrug unter einer Abzugsregel:** die Ursache anhand einer gleichen falschen Ausgabe lässt sich nicht prüfen | Kritiker ChatGPT | ? | ? | Eine beiden Seiten gerechte Regel ist nicht vorgelegt (Frage 11) |

(M2 von Kritiker Claude — das ist N16.)

---

## 4. Ergebnis

### 4.1. Wie viele Angriffe D1 verletzen

Zählung nach der Tabelle der Abschnitte 3.2–3.8 [Berechnung nach der Tabelle]. Mit „strittig“ markierte Zeilen sind einbezogen
und gesondert genannt.

| | Variante A | Variante B |
|---|---|---|
| Geldgewinn („**nein**“), von den 60 Zeilen | 24 (und noch 2 bedingt: 1.5 bei falscher Reihenfolge der Quellen, 6.6 in Verbindung mit 1.7): 1.1, 1.2, 1.3, 1.6, 1.7, 1.12, 2.2, 2.3, 2.4, 2.8, 2.10, 3.1, 3.2, 3.5, 3.6, 3.7*, 3.9*, 3.10, 4.1, 4.2, 5.2, 5.6, 5.10*, 6.5 | 25: dieselben ohne 2.10 (in B „?“), plus 2.6 und 6.1 (und dieselben 2 bedingt) |
| Nur Gewinn durch den Effekt („nein (Eff.)“) | 7: 6.1, 6.2, 6.3, 6.4, 7.1, 7.2, 7.4 | 6: dieselben ohne 6.1 |
| Neue Angriffe mit finanziellem „**nein**“ (N1–N32, M1) | 14 | 16 |

Mit einem Stern sind die strittigen Zeilen markiert (3.7, 3.9, 5.10). Ohne sie bleiben in A 21, in B — 22.
Die Zahl der Zeilen lässt sich nicht als Zahl unabhängiger Betrugsarten addieren: ein Schema ist oft durch
mehrere Zeilen beschrieben. Die Hauptschlussfolgerung hängt nicht von der Zählung ab: **D1 in wörtlicher Form erfüllt
weder Variante A noch Variante B**, und darin stimmen alle sechs Arbeiten und alle drei Kritiker überein.

**Vergleich von A und B.** B ist in der beschriebenen Form schlechter als A bei leeren und niedrigen `H` bei `0 < q < 0,909`:
ein leerer Schlüssel erhält `R·q^k` für einen Versuch ohne Verluste (N16). Bei `q = 0` ist B besser: eine nicht gewählte
Fälschung bringt nichts, sogar beim Weggang. Bei `q ≥ 0,909` verlieren beide. Wenn man in B
den Weg des Neulings aus A überträgt (vollständige Prüfung der ersten Aufgaben), verschwindet der Unterschied bei leeren Schlüsseln
(`q^k R − (1 − q^k)·3R`, wie in A [Berechnung]), aber B verliert den konstanten niedrigen Prüfanteil.
Das ist ein Eingang für die Entscheidung D3 in Phase 2, nicht die Entscheidung selbst.

### 4.2. Kritisch für den Start eines Netzes mit echten Credits

Zusammenfassung der Einschätzungen der Arbeiten und Kritiker. Ein geschlossener Start mit Übungs-Credits blockiert diese Punkte nicht,
außer der Privatsphäre, der Wiederherstellung (N6, N7) und den Punkten, ohne die der Pilot nicht prüft, was er
prüfen soll (N2, N3).

1. **Absprache nach `q_eff`:** 1.1, 1.2, 1.3, 2.3, 3.2, 3.5, 6.5 und N5. In beiden Varianten stützt sich die Abnahme
   auf die Zustimmung einer Stichprobe von Teilnehmern.
2. **Bezahlung der Wiederholung:** 2.2, 3.6, N1. Verletzt D1 bei jedem `q > 0`; eine billige Reparatur wurde nicht gefunden.
3. **Leere Schlüssel in B:** N16, 1.1-B, 3.1-B.
4. **Recht auf Ausgabe und Empfänger:** 1.7, 1.6, 5.2, N22, sowie 3.7 für die Ausgabe außerhalb des Kerns.
5. **Verfügbarkeit der Daten:** 1.12, N2, N7.
6. **Streitfälle:** 4.2 und N17; der Preis des Streitfalls N3, die damit verbundene 2.12; der Widerspruch N23; M1.
7. **Nutzung vor der Prüfung:** N21, 6.1, N30 (wenn der Eigentümer den Effekt in D1 einschließt).
8. **Wiederherstellung:** N6 (Gewicht nach dem Stillstand) und N7 (Zeilen der Pakete).
9. **Eingang und Programm:** 5.3, 5.4, N19.
10. **Privatsphäre:** 7.1, 7.4, N32 — verletzen eine verbindliche Bedingung unabhängig vom Geld.

### 4.3. Gemeinsame Wurzel

In beiden Varianten stützt sich die gewöhnliche Abnahme eines Ergebnisses auf die Zustimmung einer zufälligen Stichprobe von Teilnehmern,
also auf Signaturen, die bei Absprache nichts beweisen. Deshalb wird die Grenze des Schutzes immer
durch den Abspracheanteil `q_eff` ausgedrückt, und `q_eff` lässt sich durch Miete von Rechenleistung, Übernahme eines seltenen
Modells, die Zulassungsregel nach `H` (N5), Aushungern mit Daten (N2), gestohlene Schlüssel (N9) oder
langen Stillstand (N6) erhöhen. Unabhängig prüfbare Daten bei vollständiger Absprache — nur die Eingabe und das Modell,
anhand deren der Knoten die Aufgabe selbst neu berechnen kann; weder A noch B verlangt das, und für eine private
Anfrage hat der Knoten nicht einmal die Eingabe. D1 ist nur durch eine Prüfung erreichbar, die nicht vom Abspracheanteil abhängt
(Phase 4 [ROADMAP](ROADMAP.md)), oder durch eine ausdrückliche Abschwächung von D1 auf „bei `q < q*`“ durch Entscheidung des Eigentümers.

### 4.4. Billige Reparaturen, von den Kritikern bestätigt

| Reparatur | Schließt | Vorbehalt |
|---|---|---|
| Das Journal prüft Zuweisung, Preis und Empfänger der Zeile selbst bei der Annahme, nicht auf Einspruch | 1.6, 5.2, N24 | Die Liste der zur Auslosung Zugelassenen muss im Journal liegen |
| Gutschrift einmal nach dem kanonischen Recht auf die Planstelle und dem Fingerabdruck des Inhalts | N22, Teil von 1.7 | Zwei rechtmäßige Aufträge können dieselbe Ausgabe ergeben; das Hauptloch von 1.7 — die Regel des Plans — bleibt |
| Verdeckte Abgabe eines Einspruchs mit Offenlegung und Bindung an den Schlüssel | 2.10 | Belegt den Vorrang der Fixierung, nicht den Zeitpunkt der Öffnung |
| Gewicht und Fenster nach der aktiven Zeit des Netzes zählen, nicht nach dem Kalender | N6 | Nötig ist eine Regel der erstmaligen Gutschrift nach dem Stillstand |
| Runde des Beacons streng nach der endgültigen Annahme des Blocks | 1.5 (Teil), N13 | Die Quellen sind noch nicht gewählt |
| Jeder Knoten berechnet das Examen vor der Annahme der Version selbst neu | 6.5 | Von einem Kritiker empfohlen; Preis und Verbindlichkeit sind noch nicht festgestellt |
| Die Zusammenfassung von CURRENT_DESIGN korrigieren: 60 = 18 + 6 + 19 + 16 + 1 | Abgleich 59/60 | — |

### 4.5. Widerlegte Schlussfolgerungen

Diese Behauptungen aus den Arbeiten der Runde 1 hielten die Kritiker für falsch; in die Tabelle sind sie nicht übernommen.

| Behauptung | Wo | Warum falsch |
|---|---|---|
| Die Schwelle der Rentabilität einer Fälschung in B `q^k > H/(H+R)` | eine Arbeit DeepSeek | Der Faktor `p` fehlt. Richtig ist `q^k > pH/(R+pH)`. Bei `p = 1%`, `H = 400R`, `q = 0,95`: Gewinn `0,857R`, erwarteter Verlust `0,01·0,143·400R = 0,572R`, Ergebnis +0,285R pro Fälschung, nach der falschen Formel — ein Verlust [Berechnung]. Der Fehler überschätzt den Schutz fast bis zum Vollschutz (0,999 statt 0,93) |
| Die Schwelle 90,9% des Neulings in A sei „richtig unter der Annahme, dass 3R durch Absprache angesammelt wurden“ | dieselbe Arbeit | Die Schwelle hängt nicht davon ab, wie die `3R` erlangt wurden |
| Die Fälschung des Examens in B ergibt `R·q^k` | beide Arbeiten DeepSeek | Das Examen wird immer geprüft, ohne Lotterie; die Lotterieformel ist auf es nicht anwendbar |
| Die Reparatur 2.2 „den Prüfern aus der Belohnung der geprüften Aufgabe zahlen“ setzt den Gewinn auf null | eine Arbeit Claude | Der Kopierende spart weiterhin die Neuberechnung; gegenüber der Untätigkeit ist der Gewinn ebenfalls positiv; das Kopieren einer fremden ehrlichen Aufgabe (N1) betrifft die Reparatur nicht. Sie beseitigt nur die Ausgabe von Credits für eine leere Prüfung |
| „Bei einem gewöhnlichen Teilnehmer in B ist `H = 0` in 23,5–54,7% der Fenster, und in dieser Zeit droht einer Fälschung nichts“ | beide Arbeiten Claude | Die Zahlen `0,99^60 ≈ 54,7%`, `0,99^144 ≈ 23,5%`, `0,99^432 ≈ 1,3%` sind richtig, aber das ist der Anteil der Fenster nach der Tatsache. `H` verbrennt im Moment der Erwischung, einschließlich der Gewinne, die nach der Abgabe kamen. Die Schlussfolgerung über das Loch ist aus einem anderen Grund richtig — über den leeren Schlüssel (N16) |
| D1 wird durch den Vergleich mit dem Größeren der beiden Bezugspunkte geprüft | eine Arbeit Claude | Übersieht den Fall eines positiven Gewinns gegenüber der Untätigkeit (Beispiel in Abschnitt 1.5) |
| „Müll kostet dem Netz 3–4,5 Arbeit bei fast null Kosten des Angreifers“ (Variante A) | eine Arbeit Claude | In A erhält ein Schlüssel Aufgaben nur bei `H ≥ 3R`, und jedes Müll-Ergebnis verbrennt diese `3R`; eine mehrfache Verstärkung gibt es nicht. Eine Verstärkung gibt es nur in B ohne Zulassung nach `H` |
| Status, in der Tabelle korrigiert: 2.6-B „geschlossen“ (Arbeiten DeepSeek und Claude); 1.7 „geschlossen / ja“, 1.6 und 4.2 „geschlossen / ja“, 4.1 und 5.6 „D1 ja“, 2.2 „verletzt D1 nicht“ (Arbeiten DeepSeek, teilweise Claude); 3.4 „nein“, 2.7 „offen / nein“, 5.11 „nein“ (Arbeiten ChatGPT) | verschiedene | Die Begründungen — in den entsprechenden Zeilen der Tabelle: eine Zulassungsregel in B gibt es nicht; die Regel des Plans ist offen; die Prüfung der Zuweisung und der Streitfall des Nutzers ergeben einen Gewinn; D1 verbietet eine begrenzte Leckage; der Gewinn in 3.4 und 2.7 ist aus benachbarten Zeilen übernommen; eine persönliche Vergünstigung gibt es in der SPEC nicht |
| 1.3: Gewinn 1,034·H₀ am Punkt 0,875 | eine Arbeit Claude | 1,034·H₀ gehört zum Punkt 0,880; bei 0,875 — 1,00004·H₀ |

Strittig (nicht widerlegt) bleiben die Einschätzungen 2.1 „offen“ in beiden Arbeiten ChatGPT und 3.7
„begrenzt“: die Kritiker widersprechen sich (Zeilen 2.1 und 3.7 der Tabelle).

---

## 5. Fragen an den Eigentümer

Entscheidungen, ohne die Phase 1 nicht geschlossen werden kann. Der Rat trifft sie nicht.

1. **Gehört der Effekt in D1?** Eine Arbeit schlug vor, D1 wirtschaftlich (nur Credits)
   und D1 nach dem Effekt (Einfluss auf Antwort und Modell, Lesen der Anfrage, der Schaden selbst) zu unterscheiden. Die Worte „der Betrüger
   bekommt nicht, was er will“ schließen nach dem wörtlichen Sinn den Effekt ein; dann verletzt die Nutzung des Ergebnisses
   vor der Prüfung (N21) D1 in beiden Varianten bei jedem `q`, und schließen lässt er sich nur durch
   eine Prüfung vor Ausgabe und Übernahme (Preis — Verzögerung und Speicher).
2. **Eine Prüfung verlangen, die nicht vom Abspracheanteil abhängt, oder D1 auf „bei `q < q*`“ abschwächen?**
   Ohne eines von beidem ist D1 weder in A noch in B erreichbar.
3. **Leckage eines Teils beim Austausch** (4.1, 5.6): ein ehrlicher Austausch ohne vertrauenswürdige Partei ist im Allgemeinen
   unmöglich. Sie als ausdrückliche Annahme anerkennen oder als Verletzung von D1 werten?
4. **Streitfall von einem leeren Konto** (N23): die ROADMAP verlangt ihn, die SPEC — nicht. Womit dann den Strom
   falscher Streitfälle ohne Pfänder begrenzen?
5. **Zusammensetzung des unveränderlichen Kerns** (3.7): gehören dazu die Regel der Ausgabe, der Bezahlungssatz, das Netzentgelt,
   die Bremse und der Katalog, oder nur die Prüfung?
6. **Regel der Genehmigung des Trainingsplans** (1.7, ROADMAP „Was nicht gelöst ist“, Nr. 5): wer und wie
   erlaubt, dass eine Aufgabe Credits ausgibt.
7. **Zeit für Gewicht und Fenster** (N6): Kalender- oder aktive Zeit des Netzes.
8. **Zulassung zu Aufgaben in B** (N16): ob in B die Abhängigkeit des Zugangs von `H` eingeführt wird, im Wissen, dass dann
   B den konstanten niedrigen Prüfanteil verliert. Das ist ein Eingang für D3.
9. **Preis des Streitfalls** (N3): welche Chain für den Kostenvoranschlag `G` zu betrachten ist und wer die Differenz `G − B` trägt —
   die rechte Seite oder das Netz.
10. **Ob für die wiederholte Prüfung und die Lehrlings-Nachprüfungen gezahlt wird** (2.2, N1), wenn die Kopie nicht
    von der Neuberechnung zu unterscheiden ist?
11. **Ehrlicher Hardware-Ausfall:** ob dafür dasselbe abgezogen wird wie für Betrug.
12. **Quelle der Auszahlung `R/p` in B für Anfragen** (4.3): nur aus den Zahlungen der Nutzer oder mit Ausgabe.

---

## 6. Wer was getan hat

Der Modellrat arbeitete nach den Materialien des Projekts, ohne Zugang zum Netz und ohne Experimente.

- **Runde 1, sechs unabhängige Arbeiten:** zwei Arbeiten ChatGPT, zwei Arbeiten DeepSeek, zwei Arbeiten
  Claude. Jede erstellte ein Gegnermodell, den Abgleich der 60 Zeilen, Status für die Varianten A und B,
  Daten für die Ablehnung und neue Angriffe.
- **Runde 2, drei Kritiken:** je eine von ChatGPT, DeepSeek und Claude. Jeder Kritiker las alle sechs
  Arbeiten, glich die Behauptungen mit den Ausgangsdokumenten ab, rechnete die Formeln manuell nach und nannte
  Abweichungen und Fehler.
- **Zusammenführung:** dieses Dokument stellte Claude nach den Arbeiten und Kritiken zusammen. Wo die Kritiker sich widersprachen,
  steht in der Tabelle „strittig“; eigene neue Einschätzungen wurden bei der Zusammenführung nicht hinzugefügt.
