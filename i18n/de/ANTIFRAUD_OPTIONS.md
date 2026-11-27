<!-- translation of docs/ANTIFRAUD_OPTIONS.md, source sha256: 63c43d6864c5cccb6fa61953c9ba9594e26e3dba1a4c8241129e6f346bc08f20 -->

# Varianten der Betrugsbekämpfung: Ergebnis der Audits und des Modellrats

[English](../../docs/ANTIFRAUD_OPTIONS.en.md) · [中文](../zh/ANTIFRAUD_OPTIONS.md) · [Español](../es/ANTIFRAUD_OPTIONS.md) · [Français](../fr/ANTIFRAUD_OPTIONS.md) · **Deutsch** · [Italiano](../it/ANTIFRAUD_OPTIONS.md) · [Русский](../../docs/ANTIFRAUD_OPTIONS.md) · [Português](../pt/ANTIFRAUD_OPTIONS.md) · [العربية](../ar/ANTIFRAUD_OPTIONS.md)

Stand vom 27. November 2026.

**Was getan wurde.** Der Eigentümer des Projekts hat sechs unabhängige Audits der Vollständigkeit und zwei Karten
der Mechanismen zum Schutz vor Betrug zusammengestellt und drei eigene Ideen vorgeschlagen: die Verifizierbarkeit in das
Modell selbst einzubauen, Techniken aus Spielen zu übernehmen und die Umgehungswege der Prüfung mit nützlicher Arbeit zu „kreuzen“. Der Modellrat
hat elf unabhängige Arbeiten und vier wechselseitige Kritiken geschrieben und alles zu den unten beschriebenen Varianten zusammengeführt.

**Status.** Dieses Dokument ist Überlegung und Berechnung. Gemessene Größen sind nur dem Experiment D5
([EXPERIMENT_D5](EXPERIMENT_D5.md)) entnommen und mit [gemessen] gekennzeichnet. Alles Übrige ist mit [Berechnung] gekennzeichnet oder
als Annahme bezeichnet. Angenommene Entscheidungen bleiben nur D1–D25 ([ROADMAP](ROADMAP.md),
Abschnitt 3); alles, was hier geändert werden soll, sind Vorschläge des Rats, keine Entscheidungen. Neue
Experimente, Prototypen und Installationen hat der Rat nicht durchgeführt. Die Literatur wird aus dem Gedächtnis der Modelle oder
nach den Daten der Audits angeführt und wurde nicht mit den Primärquellen abgeglichen. Frühere Zusammenstellungen:
[STRATEGY_SEARCH](STRATEGY_SEARCH.md) und [HIDDEN_DETECTOR](HIDDEN_DETECTOR.md).

**Bezeichnungen.** `R` — Preis der Aufgabe; `c` — Selbstkosten ehrlicher Arbeit im exakten
(ganzzahligen) Profil; `c_f` — Kosten des Betrügers für die Fälschung; `H_lock` — der gesperrte,
noch nicht ausgereifte Betrag des Schlüssels; `p` — Wahrscheinlichkeit der Prüfung einer Antwort; `q` — Anteil des Gewichts der Koalition unter den
zugewiesenen Prüfern; `ρ` — Zeit der Prüfung einer fertigen Antwort in einem Durchlauf in Anteilen der Zeit
ihrer exakten Generierung: 0,10–0,40 bei Batch 1 und 0,26–0,64 bei Batch 8 [gemessen]; `γ` — Verlangsamung
des exakten Profils gegenüber dem gewöhnlichen Q8_0: 1,52–1,78 bei Batch 1 und 2,47–2,79 bei Batch 8
[gemessen, nur RTX 2060].

## Kurzes Fazit

1. **Teuer ist nicht das Prüfen, sondern das exakte Rechnen.** Die Prüfung einer Antwort kostet 10–40% ihrer
   Generierung [gemessen], aber der Hauptaufschlag ist die Verlangsamung des exakten Profils um das 1,52–1,78-Fache
   [gemessen]. Der Richtwert „etwa 5%“ ist mit den heutigen Kernen in keiner Variante erreichbar, so
   selten die Prüfung auch sei [Berechnung].
2. **Die Idee „Fingerabdrücke und Neuberechnung eines zufälligen Stücks“ funktioniert, aber nicht als Verbilligung der Garantie.**
   Wenn `s` Stücke von `N` offengelegt werden, kommt eine gezielt ausgetauschte Zelle
   mit einer Wahrscheinlichkeit von nicht weniger als `1 − s/N` durch. Die Einschätzung „30-mal billiger, und der Betrug wird trotzdem gefangen“
   bedeutet in Wirklichkeit „30-mal weniger Entdeckungen“. Die Fingerabdrücke sind in einer anderen Rolle nützlich: Eine kurze Wurzel
   der Spur erlaubt es, einen Streit durch Halbierung bis zu einem Schritt zu zerlegen, und gibt einem schwachen Gerät
   eine Teilprüfung mit ehrlicher Markierung.
3. **Die Idee „Verifizierbarkeit im Modell“ funktioniert in einer Form:** die Kerne so fein abzustimmen oder neu zu schreiben,
   dass das exakte Profil schnell wird. Das senkt `γ` und schwächt die Garantie nicht.
   Die Fingerabdrücke schreibt das Programm, nicht das Modell, und Feintuning ist dafür nicht nötig. Prüfsummen
   in den Schichten schützen den ehrlichen Ausführenden vor Hardwareausfällen, aber nicht vor Absicht.
4. **Aus den Spielen überträgt sich nur die Reihenfolge der Züge:** „versiegelt → endgültige Fixierung → geheime
   Wahl → Offenlegung → Neuberechnung“. Mit der Berechnung sind nur zwei Züge verknüpft: die Neuberechnung des offengelegten Stücks
   und die Prüfung des Zeugen der Aufgabe. Ein separates Spiel neben der nützlichen Arbeit beweist nichts.
5. **Es gibt vier Varianten und ein Zusatzmodul:** vollständige Prüfung jeder Antwort durch den Zahler;
   Lotterie nach ganzen Aufträgen; geheime Münze des Zahlers mit gesperrtem Betrag; Aufgaben
   mit verifizierbarem Ergebnis; und exakte spekulative Dekodierung als möglicher Weg, die
   erste und die dritte Variante zu verbilligen.
6. **Empfehlung.** Der Hauptvertrag ist die vollständige Prüfung jeder Antwort durch den Zahler im exakten
   Profil. Er allein erfüllt die angenommenen Entscheidungen ohne deren Änderung. Aufgaben mit verifizierbarem Ergebnis sind
   ein eigener Aufgabentyp und vorerst die einzige strenge Garantie für das Training. Die Lotterie ist ein Tarif
   für Chargen. Die Münze mit gesperrtem Betrag bleibt Kandidat bis zur Berechnung M9 und zu Entscheidungen des Eigentümers.
7. **Der erste Schritt.** Eine Berechnung: M9 — falsche Streitfälle ohne Pfand, alle Zweige des Schweigens und der Ablehnung.
   Ein Experiment (mit Genehmigung des Eigentümers): am bereits zusammengestellten Profil v2 und llama.cpp Q8_0 die
   Übereinstimmung der Token bei gemeinsamem Präfix messen. Es entscheidet drei Fragen auf einmal (Abschnitt 5).
8. **Wörtlich unmöglich:** den Verbraucher ohne Ausrüstung bei vollständiger Absprache
   der Prüfer zu schützen; den Trainingsschritt bei vollständiger Absprache innerhalb eines Aufschlags von 20% zu prüfen; eine
   geprüfte Antwort bei gemessenem `γ` in 5% unterzubringen. Die minimalen Abschwächungen sind
   als Fragen an den Eigentümer in Abschnitt 7 formuliert.

## 1. Was die Audits gefunden haben

Kennzeichen der Audits: RU — `SkyNet_audit_completeness_RU`; SC — `skynet_completeness_audit`; GPT —
`gpt-SkyNet-audit`; DS — `deepseek-AUDIT_REPORT`; GEM — `gemini_report`; CR — `chat_responses`;
Karten — `mehanizmy-anti-obman` (MEH) und `mechanisms_map_report` (MAP). Wo die Arbeiten des Rats
unterschiedlich gelesen haben, wer was genannt hat, ist das mit dem Wort „strittig“ vermerkt.

### 1.1. Übersehene Ansätze

| Ansatz | Wer von den Audits ihn genannt hat | Einschätzung des Rats |
|---|---|---|
| Fingerabdrücke der Aktivierungen, TOPLOC | SC, GPT, GEM, CR, DS (in einer Zeile), MAP; MEH — strittig | Keine Zahlungsgrundlage; nur Signal für eine zusätzliche exakte Prüfung (Abschnitt 2.4) |
| Optimistische Schemata, Streit mit dem Schiedsrichter, Halbierung | Alle sechs und beide Karten | Nötige Schicht des Streits; bei vollständiger Absprache gibt es niemanden zum Streiten, daher kein Ersatz für die Prüfung durch den Zahler |
| Statistische Tests der Modellsubstitution | GPT, DS, GEM, CR, MAP; SC und RU — strittig | Nur Signal für die Erhöhung der Prüfhäufigkeit; gehört nicht zum Kern |
| Reproduzierbare Gleitkommaarithmetik, ganzzahlige Kerne vom Typ Ozaki | SC, GEM, DS, GPT, RU; CR nennt RepOps | Gleitkommaarithmetik ersetzt das ganzzahlige Profil nicht; die Beschleunigung der Kerne ist eine Hypothese für ein Experiment |
| Prüfsummen ABFT | SC, GEM, DS, GPT, RU | Selbstkontrolle des ehrlichen Knotens gegen Ausfälle; deckt nur lineare Multiplikationen ab |
| Freivalds-Prüfung | SC, CR, GPT, GEM, Karten | Funktioniert für den linearen Teil der exakten Arithmetik bei frischem geheimen Vektor nach der Fixierung |
| Verfügbarkeit der Daten | SC, DS, GPT; GEM — dagegen; RU und Karten — strittig | Technik des Streits und des Trainings, keine Garantie für R4 |
| Mechanism Design mit teurer Prüfung | GEM, DS, GPT, SC | Bestätigt die Schwelle `R/(R + H_lock)`; gibt keinen neuen Hebel |
| Hardware-Attestierung der GPU, TEE | Fast alle | Zusätzliches Signal und Privatsphärenmodus; die Prüfhäufigkeit danach zu senken ist unzulässig |
| Bürgschaft und Versicherung ohne Pfand des Teilnehmers | SC, GEM, DS, GPT, RU | Ein fremdes Schloss ist im Wesentlichen das Pfand eines Dritten, eine Frage zu R5; der Versicherungsfonds eröffnet den Selbststreit |
| Erfahrung von Bittensor, Gensyn, Prime Intellect, Hyperbolic, Ritual, Atoma, Golem | Alle sechs und die Karten | Alle stützen sich auf ein Pfand, vertrauenswürdige Validatoren, TEE oder „einen Ehrlichen“; übertragbar sind einzelne Techniken |

Von nur einem Audit genannt: schichtweise Stichprobenbeweise als Grundlage (RU), Bindung des
Chiffretexts der Antwort an das Commitment über DLEQ (SC), Coupon-Pool (SC; nach einer der Arbeiten —
auch GEM und GPT).

### 1.2. Schwache Stellen früherer Schlussfolgerungen

- Die Schwelle `p ≥ R/(R + H_lock)` ist unter drei Bedingungen richtig, die früher nicht genannt wurden: Der Preis
  liegt nicht unter den Selbstkosten, die Münze wird tatsächlich geworfen, der Betrag ist zum Verbrennen verfügbar
  (GPT, SC, GEM, RU).
- Die Schlussfolgerung „der Richtwert 5% ist widerlegt“ bezieht sich auf eine Implementierung der Kerne (GEM, SC, DS).
- Die Barriere der kurzen Beweise ist für eine Anordnung berechnet (SC, GEM, DS, GPT).
- Die Übereinstimmung der Bits ist an sechs Konfigurationen gezeigt, nicht „auf beliebiger Hardware“ (DS, GEM, SC, GPT).
  Die Kritiken präzisierten: für einen langen Durchlauf über eine fertige Antwort — an drei.
- Die Behauptung „ein fauler Zahler und ein Neuling zusammen ergeben null“ war ein Fehler: Der Gewinn beträgt bis zu `+R`.
- Die Aufzählung „92 Mio. Strategien“ beweist keine Vollständigkeit (RU).
- Die Literatur früherer Räte ist aus dem Gedächtnis angeführt (RU, GEM, DS, GPT).

### 1.3. Widersprüche der Anforderungen und Entscheidungen

- **D16 gegen die Stichprobenprüfung.** Wenn ein ehrlicher Ausfall nicht bestraft wird, erklärt der Betrüger
  die Fälschung zum Ausfall und erhält `(1 − p)·R − c_f` (DS, GEM, RU, SC).
- **D19.** Die dritte Bedingung — „der mit `R` multiplizierte Fehler ist kleiner als der Preis des Versuchs“ — ist nicht anwendbar,
  wenn der Versuch kostenlos ist (DS, RU; im Rat — ChatGPT).
- **Die Ausgabe von Credits für das Training bei null Nachfrage**, vollständige Absprache, ein Aufschlag von 20% und die Prüfung
  durch jeden Knoten sind zusammen nicht erfüllbar (DS, SC, GEM, GPT, CR, MEH).
- **Der Verbraucher ohne Ausrüstung und R4** (SC, GEM, RU, CR).
- **Das wörtliche D1 schließt jede Stichprobe aus** (RU, DS).
- **Streit ohne Pfand und ein endlicher Streitfonds** (SC, GEM, GPT, RU).
- **„Zuerst vollständige Sicherheit, dann Experimente“** wurde als Teufelskreis bezeichnet: `γ`, `ρ`, Qualität
  und Ausfallhäufigkeit werden nur durch Messung festgestellt (DS, GPT). Das ist die Meinung der Audits und eines
  Kritikers; die geltende Beschränkung für Experimente hat der Rat nicht verletzt und hebt sie nicht auf.

### 1.4. Neue Angriffe

- **Der faule Zahler.** Wenn der Anteil `λ` der Zahler nicht prüft, wird die Schwelle zu
  `R/((1 − λ)(R + H_lock))`; bei leerem Konto ist sie größer als eins, und der Betrüger, der den
  faulen Zahler erkennt, erhält bis zu `+R` (SC) [Berechnung].
- **Die Münze wird nicht erzwungen:** Das Programm des Zahlers kann mit `p = 0` neu gebaut werden (GEM, SC).
- **Weiterverkauf der Antwort zwischen Sitzungen** („Mafia-Angriff“): Ein Vermittler nimmt den Auftrag an, kauft die Antwort
  bei einem ehrlichen Ausführenden und zahlt nicht. Es funktioniert ohne Absprache der Prüfer; geheilt wird es durch die Reihenfolge
  „Vorauszahlung gesperrt → Antwort → Prüfung in der Frist → Zahlung“ (GEM; im Rat weiterentwickelt).
- **Verkauf des noch nicht ausgereiften Betrags** vor dem Weggang (RU). Geheilt durch das Verbot der Übertragung.
- **Selbstzahlung** erhöht den gesperrten Betrag und senkt die Prüfhäufigkeit. Die Kritik zeigte,
  dass das Geld dadurch nicht geöffnet wird (das eigene Geld des Betrügers verbrennt bei der Entdeckung),
  aber der gezielte Schaden wird billiger.
- **Flut kostenloser Schlüssel:** Jeder neue Schlüssel verlangt eine vollständige Prüfung
  und belastet den Zahler; das ist eine Dienstverweigerung, kein Diebstahl.
- **Substitution eines oder zweier Token innerhalb des Fensters des TOPLOC-Fingerabdrucks** (SC).

### 1.5. Was an den Verweisen und Zahlen der Audits zweifelhaft ist

- **Beschleunigung der Kerne nach Ozaki bis `γ` = 1,05–1,20.** Zweifelhaft: Die schnellen Kerne von D5 verwenden bereits
  dieselben 8-Bit-Instruktionen, und mit ihnen wurden 1,52–1,78 gemessen; 24 Blöcke von 32 sind Rekursion, die
  die Zerlegung nicht beschleunigt. Man darf diese Zahl nicht neben den gemessenen Werten in die Kostenvoranschläge setzen.
- **TOPLOC:** „258 Bytes auf 32 Token“, „10–100-mal schneller“, „Overhead 1–3%“. Zwei Arbeiten
  bestätigen es aus dem Gedächtnis, drei — „kann ich nicht prüfen“; für SkyNet ist davon nichts gemessen.
- **Nicht prüfen ließen sich:** die Zahlen von DeepProve und FlashProve, Verde (in den Audits drei verschiedene Sätze
  von Aufschlägen), die Verluste von TEE auf H100, der Preis von DLEQ in Gas, Status und Vorfälle von Bittensor und anderen
  Netzen, eine Reihe von arXiv-Nummern.
- **Falsche Zuordnungen:** Der Algorithmus Krum ist den falschen Autoren zugeschrieben (MEH); bei einem Audit
  gibt es einen arithmetischen Fehler in der Schwelle (`c_f ≈ 0,3c`, `p ≥ 0,73`).
- Zwei Audits mit derselben Zahl sind nicht zwei unabhängige Messungen: Beide können eine Quelle nacherzählen.

## 2. Ideen des Eigentümers, zu Konstruktionen ausgearbeitet

### 2.1. Verifizierbarkeit im Modell und Feintuning

- **„Das Modell schützt sich selbst“ funktioniert nicht.** Gewichte und Code sind offen; der Betrüger ist nicht verpflichtet, das
  Modell zu starten. Das haben alle elf Arbeiten bestätigt.
- **„Das Modell schreibt Fingerabdrücke“** — das ist ein Hashing-Programm um unveränderte Gewichte.
  Feintuning ist nicht nötig und fügt nichts hinzu.
- **Prüfsummen in den Schichten (ABFT)** fangen einen zufälligen Ausfall. Ein wissender Gegner wählt
  einen Fehler, der die Summe erhält. Rekursion, Tabellen und Division in der Attention sind durch Summen nicht abgedeckt.
  Die These mehrerer Arbeiten „ABFT beseitigt den Konflikt D16“ haben die Kritiken als übertrieben beurteilt.
- **Feintuning ist nur zur Senkung von `γ` sinnvoll:** dafür zu sorgen, dass das exakte Profil mit den schnellen 8-Bit-Kernen übereinstimmt
  („vergröberter Kanon“, ein Vorschlag von DeepSeek). Die Bits bleiben Bits, die Garantie ändert sich nicht. Risiko: Das erste 8-Bit-Profil in D5 wurde bereits wegen der Qualität abgelehnt
  [gemessen]; der Preis des Trainings und der Qualitätsverlust sind nicht gemessen, die in den Arbeiten genannten GPU-Stunden —
  Annahmen.
- **Feintuning „auf Rundungsrobustheit“**, damit das schnelle Profil mit Toleranz geprüft wird,
  führt zurück zum Vertrag mit Toleranz (Abschnitt 2.4) und gibt keine beweisbare Grenze.
- **Ein Modell mit kleinerem Zustand** verringert den Traffic der Prüfung eines Stücks, erhöht aber nicht den Anteil
  der entdeckbaren Substitutionen.

**Urteil:** Es funktioniert eine Form — die Beschleunigung des exakten Profils. Sie wird durch ein Experiment entschieden.

### 2.2. Fingerabdrücke und Neuberechnung eines zufälligen Stücks

**Konstruktion.** Der Ausführende versiegelt vor der Wahl des Prüfers mit einer Wurzel die Token
und die Zwischenzustände. Der Prüfer wählt geheim ein Stück, erhält den versiegelten Eingang
des Stücks und rechnet es im exakten Profil neu. Das Stück lässt sich ohne Neuberechnung des ganzen
Anfangs der Antwort prüfen: Das bestätigt auch D5, wo der Durchlauf in Stücken dieselben Hashes der Zustände ergibt [gemessen].
Die Behauptung mehrerer Arbeiten „man kann ein Stück nicht ohne Präfix neu berechnen“ hat die Kritik verworfen.

**Warum die Grenze `1 − s/N` nicht umgangen wird.** Der Betrüger rechnet alles ehrlich, außer einer Zelle,
und setzt ehrlich vom substituierten Wert fort. Die Spur ist überall stimmig, außer bei einem Übergang.
Wenn `s` von `N` Übergängen offengelegt werden, findet sich ein Übergang, der mit einer Wahrscheinlichkeit
von nicht mehr als `s/N` geprüft wird. Die Fingerabdrücke machen die Lüge auffindbar, vervielfachen sie aber nicht. Die Grenze kann
nur eine Prüfung umgehen, bei der jede Lüge einen großen Anteil der Gleichungen verletzt (kurze Beweise),
und ihr Preis ist der bisherige.

**Zwei Arten von Schnitten** [Berechnung nach der Konfiguration D5]:

| Schnitt | Was er bezeugt | Was zu übertragen ist | Was er nicht fängt |
|---|---|---|---|
| Nach Schichten: ein Block auf der ganzen Sequenz | Einen Übergang des Blocks vom vorgelegten Eingang; der Block — etwa 2,65% des Durchlaufs, der Ausgabekopf — etwa 15,1% | 0,78 / 4,9 / 14,6 MiB bei 160 / 1000 / 3000 Positionen | Eine in einer anderen Schicht zusammengesetzte Substitution: Chance 1 aus 32–33 |
| Nach Positionen: alle Schichten auf einem Segment von 64 Positionen | Die Token des Segments sind gleich der exakten Wahl beim versiegelten Zustand der linken Grenze | 48 MiB Zustand und 64 KiB je vorheriger Position: 58 / 110 / 236 MiB | Eine substituierte Position außerhalb des Segments: kommt mit der Wahrscheinlichkeit `1 − L/T` durch, zum Beispiel 93,6% bei 500 + 500 Token |

Der Ausführende muss dabei 0,13–2,38 GiB Kontrollpunkte pro Antwort für die Dauer des Streitfensters
speichern [Berechnung]. Ins Journal kann nur die Wurzel von 32 Bytes gehen: Der Zustand selbst ist um 3–5 Größenordnungen
größer als der Eintrag D24.

**Die Fälschung „Entwurf mit dem schnellen Profil + exakter Durchlauf“.** Sie hat die Kritik von Claude gefunden. Der Betrüger
generiert die Antwort in Q8_0, macht dann einen exakten Durchlauf über die fertigen Token und druckt die Spur.
In einer solchen Spur sind alle Übergänge aller Blöcke stimmig; es stimmen nur die Positionen nicht, wo das Token
des Entwurfs von der exakten Wahl abweicht.

- Der Preis der Fälschung ist `c·(1/γ + ρ)`, die Ersparnis gegenüber ehrlicher Arbeit `1 − 1/γ − ρ`: 18,4% bei
  `γ = 1,65`, `ρ = 0,21`; die Fälschung ist vorteilhaft, wenn `ρ < 1 − 1/γ` (0,34 / 0,39 / 0,44 bei `γ` =
  1,52 / 1,65 / 1,78) [Berechnung].
- Der Schnitt nach Schichten fängt sie nicht (außer der Chance 1 aus 32–33 am Ausgabekopf).
- Der Schnitt nach Positionen mit der Länge 64 fängt sie mit einer Wahrscheinlichkeit von 97%, wenn die Token von Q8_0 und des exakten Profils
  an 95% der Positionen übereinstimmen; 49% bei Übereinstimmung 99%; 29% bei 99,5%; 6,5% bei 99,9% [Berechnung].
  Der Übereinstimmungsanteil ist nicht gemessen.
- Die vollständige Prüfung fängt sie immer. Die Lücke betrifft nur Schemata, wo der Schnitt den
  vollständigen Durchlauf **ersetzt**.

Folge: Der Schnitt bezeugt „der Ausführende hat mindestens einen exakten Durchlauf bezahlt“, nicht „die Antwort
wurde mit dem exakten Profil generiert“. Hier sind die Kritiken auseinandergegangen: DeepSeek meint, der Schnitt
nach Positionen fange die Substitution der ganzen Antwort durch Q8_0 mit Wahrscheinlichkeit 1; MiniMax — diese Wahrscheinlichkeit
sei nicht gemessen; Claude führte die obige Berechnung an. Es entscheidet die Messung der Übereinstimmung der Token.

Die Kritik von MiniMax fügte hinzu: Die kostenlose Fälschung „die Antwort früher abbrechen“ erzeugt überhaupt keine falschen Zellen.
Die Länge der Antwort und der Grund des Anhaltens müssen in den Gegenstand der Prüfung eingehen.

**Was die Wurzel der Spur dennoch gibt:**

- **Streit durch Halbierung.** Zwei Seiten mit verschiedenen Spuren kommen in einer logarithmischen Zahl von Zügen
  zu einem Schritt, den jeder Knoten selbst neu berechnet. Die Kritik präzisierte: Die angegebenen
  15–23 Züge reichen nur bis zur Zelle, innerhalb des Blocks braucht es noch etwa 27 Halbierungen; die Regel
  „Schweigen — Verlust“ verlangt die Berechnung M9.
- **Schwaches Gerät.** Ein Zahler ohne Grafikkarte kann ein Segment pro Antwort prüfen. Das ergibt die Markierung
  „teilweise geprüft“, nicht „geprüft“. Der Preis für ihn ist Traffic von 52–300 MiB pro Antwort und Prozessorzeit; auf dem Telefon nicht gemessen.
- **Unveränderlichkeit der Historie des Ausführenden** und Streit über eine private Anfrage mit Offenlegung einer Zelle.

**Urteil:** Die Konstruktion ist möglich und nützlich für den Streit und das schwache Gerät, verbilligt aber die Garantie D1
und D25 nicht. Damit eine gezielte Substitution unvorteilhafter als Untätigkeit wird, müssen bei 32 Blöcken
2 / 4 / 7 / 10 Blöcke offengelegt werden bei einer Marge von 5 / 10 / 20 / 30% [Berechnung], und gegen den Schaden (D6)
hilft auch das nicht.

### 2.3. Techniken aus Spielen

| Technik | Wo der Zug mit der Berechnung verknüpft ist | Wo er nicht verknüpft ist |
|---|---|---|
| „Versiegelt — geöffnet“ | Das offengelegte Stück muss mit der Neuberechnung vom versiegelten Eingang übereinstimmen | Das Versiegeln selbst beweist nichts: Man kann auch eine stimmige Lüge versiegeln |
| „Einer schneidet — der andere wählt“ | Die Wahl erfolgt nach der Fixierung mit der geheimen Münze des Prüfers | Der Schneidende verdirbt einen Teil von `N`; es gibt keine Ersparnis gegenüber der vollständigen Prüfung |
| Gemeinsame Münze zweier Seiten | Nicht nötig, wenn das Geld eines Zahlers auf dem Spiel steht: seine geheime Münze genügt | Wer sich zuletzt offenbart, vereitelt den ungünstigen Ausgang; bei vollständiger Absprache sind alle Beiträge der Koalition bekannt |
| Karten ohne Croupier (mental poker) | — | Für die Wahl der Nummer des Stücks überflüssig: Das leistet dieselbe überprüfbare Zufallsfunktion |
| „Jeder beobachtet den Gegner“ | Der Zahler prüft seine Antwort — darauf sind alle Varianten des Abschnitts 3 gebaut | Der Ausführende kann einen unehrlichen Zahler ohne Pfand nicht bestrafen (Berechnung M9) |
| Markierte Karten, geheimer Käufer | — | Das Geheimnis der Falle hält in einem offenen Netz nur der Zahler, daher fällt die Falle mit seiner Prüfung zusammen und ist teurer als sie |

Eine gemeinsame öffentliche Quelle der Zufälligkeit ist nur dort nötig, wo fremdes Geld geprüft wird; dann
gilt D20 (nicht weniger als zwei unabhängige Quellen).

**Urteil:** Aus den Spielen sind die Reihenfolge der Züge und das Hauptprinzip übernommen „es prüft der, dessen Geld auf dem Spiel steht“.
Das Spiel verwandelt eine Stichprobe nicht in eine vollständige Prüfung.

### 2.4. Schneller Ausführender und exakter Richter

**Vertrag mit Toleranz.** Der Ausführende rechnet im schnellen Q8_0, der Zahler macht einen exakten Durchlauf
und nimmt die Antwort an, wenn an jeder Position die Bewertung des gewählten Tokens hinter der größten
um nicht mehr als `m` zurückbleibt. Der Vorteil gegenüber dem früher verworfenen „Zertifikat mit Reserve“: Das Urteil
wird in ganzen Zahlen berechnet und ist auf jedem Gerät gleich. Aber die Kritik hat vier Mängel gefunden.

- **Die Toleranz legitimiert fremde Antworten.** Jeder Entwurf plus ein exakter Durchlauf zeigt
  dem Ausführenden alle Bewertungen; er korrigiert die Positionen außerhalb der Toleranz und erhält eine zulässige Antwort. Der
  billigste Produzent einer solchen Antwort ist das billigste Entwurfsmodell, nicht Q8_0 desselben Modells.
- **Die Wahlfreiheit ist ein Kanal des Schadens.** An Positionen mit einem Abstand kleiner als `m` wählt der Ausführende das Token, einschließlich des frühen Abbruchs. Beispiel: Die Bewertungen „fortsetzen“ und „anhalten“ sind
  100 und 99; bei `m = 1` besteht die abgebrochene Antwort die vollständige Prüfung. Ein solcher Text würde die
  Markierung „mit Toleranz geprüft“ erhalten — im Wesentlichen ist das eine Verletzung von D6. Eine ähnliche Markierung hat der frühere
  Rat bereits verworfen.
- **Der ehrliche Ausführende ist gezwungen, sich selbst zu prüfen**, sonst verliert er den Betrag bei einem Ausreißer,
  auch bei einer vom Zahler gewählten Eingabe. Dann ist der Preis `1 + ρ·γ`: +15…+71% bei Batch 1,
  und bei Batch 8 gibt es keinen Gewinn gegenüber der exakten Generierung [Berechnung].
- **Der angegebene Preis „+0,01…+2,3%“ hat nicht gehalten:** Für die Offenlegung von Stücken braucht der Ausführende
  die Hashes der Zustände des exakten Profils, also einen exakten Durchlauf für jede Generierung [Berechnung].

Selbst bei einem schnellen Ausführenden kostet der vollständige exakte Durchlauf des Richters auf einer RTX 2060 nicht weniger als 31,9%
der Zeit der gewöhnlichen Generierung [Berechnung], sodass dieser Vertrag jede Antwort nicht in 5% unterbringt.

**Exakte spekulative Dekodierung** — derselbe Vertrag bei `m = 0`. Der Entwurf entsteht auf beliebige Weise,
bezahlt wird nur die Antwort, die bitgleich zur exakten ist. Vertrag und Garantie ändern sich nicht,
D6 ist nicht berührt. Der Preis hängt vom Anteil der übereinstimmenden Token und der Länge der übereinstimmenden Serien ab; die untere Schätzung
`1 + ρ·γ`. Nicht gemessen; bei einer Übereinstimmung unter etwa 95% kommt es schlechter heraus als die direkte exakte Generierung.

**TOPLOC und Fingerabdrücke mit Toleranz in Gleitkommaarithmetik.** Der Fingerabdruck bezeugt, dass
die Aktivierungen mit dem Text stimmig sind, nicht woher der Text kam. Fälschung: Text von einem beliebigen Modell,
dann ein Durchlauf des angegebenen Modells über diesen Text — die Fingerabdrücke sind echt. Das Urteil mit Toleranz
hängt von der Hardware ab: Zwei ehrliche Knoten können auseinandergehen, daher darf man danach keinen Betrag
verbrennen, und D4 wird wörtlich verletzt. Damit der Tarif mit Toleranz billig ist, braucht der Prüfer eine
Referenz, die er nicht hat, solange er nicht selbst einen exakten Durchlauf gerechnet hat.

**Urteil:** Der Vertrag mit Toleranz und die Fingerabdrücke mit Toleranz gehören nicht in die Liste der Varianten: Sie
ändern das Produkt und setzen eine Markierung auf einen vom Ausführenden gewählten Text. Zulässig sind sie nur als Signal
für eine zusätzliche exakte Prüfung. Die exakte spekulative Dekodierung ist ein Kandidat für die
Verbilligung, entschieden durch eine Messung.

## 3. Ganzheitliche Varianten

Preis — der vollständige Rechenaufschlag gegenüber der gewöhnlichen Generierung Q8_0 ohne Prüfung
[Berechnung nach den Messungen D5]. Darin sind Journal, Streitfälle, Speicherung, Traffic und Energie nicht enthalten: Sie
sind nicht gemessen. Der Gewinn ist erwartet, für eine eingereichte Fälschung. Der untere Rand „+67%“ verbindet `ρ`
der Karte RTX 4070 Laptop mit `γ` der Karte RTX 2060; auf einer RTX 2060 beginnt der Bereich bei +84%.

| № | Variante | Preis bei Batch 1 | Geld des Betrügers bei `q` = 0,1 / 0,3 / 0,5 / 1 | Neuling mit leerem Konto | Saboteur ohne Gewinn | Hauptrestrisiko |
|---|---|---|---|---|---|---|
| V1 | Vollständige Prüfung jeder Antwort durch den Zahler | +67…+149% (auf einer RTX 2060 +84…+149%) | `−c_f` bei allen `q` | `−c_f` | Keine falsche Markierung „geprüft“; kann die Lieferung vereiteln | Fauler Zahler; falsche Ablehnungen des Zahlers (M9) |
| V2 | Lotterie nach ganzen Aufträgen | +53…+82% und Reserve des Käufers `R/p` | `−c_f` bei allen `q` | 0 | Der Anteil `1 − p` der Antworten ist ungeprüft und durch nichts zurückgehalten | Ungleichmäßiges Einkommen; die Reserve — eine Frage zu R5 |
| V3 | Geheime Münze des Zahlers und gesperrter Betrag | +50…+82%; die Prüfung selbst 0,005–3,6% | Nicht mehr als null bei allen `q`, wenn der Zahler die Münze rechtzeitig wirft | `−c_f` (Prüfung immer) | Es kommt der Anteil `1 − p` durch: bis 99,98% | Erkannter fauler Zahler — bis `+R`; ein ehrlicher Ausfall verbrennt den Betrag |
| V4 | Aufgaben mit verifizierbarem Ergebnis | `(N − 1)·v/w`, nicht gemessen | `−c_f` bei allen `q` | 0 | Ein falscher Zeuge besteht nicht | Das ist keine Modellantwort und kein Trainingsschritt |
| V5 | Zusatzmodul: exakte spekulative Dekodierung über V1 oder V3 | Nicht gemessen; untere Schätzung +15…+71% | Wie bei der Trägervariante | Ebenso | Ebenso | Die Übereinstimmung der Token ist nicht gemessen |

**Der Zahler ohne Ausrüstung** hat in allen Varianten keine Garantie. Wenn er die Prüfung einem
Trio zugewiesener Knoten überträgt, ist die erwartete falsche Auszahlung `R·q³`: 0,001`R` / 0,027`R` / 0,125`R`
/ `R` bei `q` = 0,1 / 0,3 / 0,5 / 1 [Berechnung]. Das ist bereits in D21 festgehalten.

### V1. Vollständige Prüfung jeder Antwort durch den Zahler

**Schritte.** Der Auftrag legt Modell, Profil, Seed, Längengrenzen und die Abnahmebedingung fest.
Der Ausführende rechnet die Antwort im exakten Profil und fixiert mit einem Eintrag den Chiffretext und die Wurzel
der Spur. Der Zahler rechnet vor der Anzeige die ganze Antwort in einem Durchlauf neu, einschließlich Länge und Grund
des Anhaltens. Eine Abweichung bedeutet Nichtzahlung; der wartende Betrag verbrennt nicht. Die Markierung „geprüft“
wird erst nach dem Durchlauf gesetzt.

**Garantie und Annahmen.** Eine falsche Antwort wird bei jedem Abspracheanteil
nicht bezahlt und erhält keine Markierung, für den Neuling und für jede Zahl von Schlüsseln. Annahmen: Die Bits stimmen auf dem Gerät
des Zahlers überein (an sechs Ausführenden gezeigt [gemessen], auf Telefonen — nicht); der Prüfkern
ist korrekt; der Zahler prüft tatsächlich.

**Preis.** `γ·(1 + ρ) − 1`: +67…+149% bei Batch 1; +211…+358% bei Batch 8 (auf einer RTX 2060
+251…+358%). Beispiel `γ = 1,65`, `ρ = 0,21`: +99,65%. Dem Zahler kostet die Prüfung 15–71%
der Zeit seiner eigenen gewöhnlichen Generierung [Berechnung].

**Was in den Entscheidungen zu ändern ist.** Nichts; nötig sind Präzisierungen von D6 (zwei Markierungen, keine Zwischenstufen),
D16 (bei vollständiger Prüfung zieht eine Abweichung nur die Nichtzahlung nach sich) und D22 (Abschnitt 4).

**Nicht gemessen.** Die Qualität des exakten Profils (Experiment O5); `γ` auf anderen Karten; Zeit und Speicher
auf Laptop und Telefon; der Preis des Streits; das Verhalten bei falschen Ablehnungen des Zahlers.

### V2. Lotterie nach ganzen Aufträgen

**Schritte.** Der Käufer reserviert vorab die Prämie. Alle Ergebnisse der Charge werden vor der Auslosung fixiert.
Das Los wählt den Anteil `p` der Aufträge; die gewählten prüft der Zahler vollständig und zahlt `R/p`;
die übrigen werden nicht bezahlt und mit „nicht geprüft“ markiert.

**Garantie und Annahmen.** Eine falsche Auszahlung ist auch bei leerem Konto und ohne Verbrennung
von Beträgen unmöglich; D16 muss nicht geändert werden. Annahmen: das Los nach D20; die Reserve des Käufers gilt nicht als Pfand.

**Preis.** `γ·(1 + p·ρ) − 1`: +53…+82% bei Batch 1; Beispiel `p = 0,05`, `γ = 1,65`, `ρ = 0,21`:
+66,73%. Aber auf ein **geprüftes** Ergebnis kommt `1/p`-mal mehr Arbeit.

**Schwache Stellen.** Das Einkommen ist ungleichmäßig: Bei `p = 0,1` erhält ein ehrlicher Neuling mit einer Wahrscheinlichkeit von 34,87% nichts
für die ersten zehn Aufträge; bei 6000 Aufgaben im Monat, `p = 0,01` und Selbstkosten von 95% des Preises
ist die Wahrscheinlichkeit eines verlustbringenden Monats 33,10% [Berechnung]. Ungeprüfte Antworten werden durch nichts zurückgehalten: Ein Saboteur
mit kostenlosen Schlüsseln liefert Müll kostenlos.

**Was zu ändern ist.** Antworten, ob die Reserve `R/p` „Mittel im Voraus“ nach R5 ist; die Quellen
der Zufälligkeit nach D20 wählen.

**Nicht gemessen.** Die genaue Ruinwahrscheinlichkeit auf dem Weg, die Größe der Reserve, die Nachfrage nach einem solchen Tarif.

### V3. Geheime Münze des Zahlers und gesperrter Betrag

Das ist die Strategie des fünften Modellrats ([STRATEGY_SEARCH](STRATEGY_SEARCH.md)) mit Korrekturen.

**Schritte.** Die Antwort wird im exakten Profil fixiert. Nach der Fixierung wirft das Programm des Zahlers
seine geheime Münze und prüft die Antwort vollständig mit einer Wahrscheinlichkeit nicht unter `R/(R + H_lock)`;
beim Neuling — immer. Eine bewiesene Abweichung verbrennt mit einer einzigen Handlung den gesamten noch nicht ausgereiften Betrag
des Schlüssels, einschließlich der Belohnungen derselben Welle; dem Geschädigten werden nicht mehr als `R` erstattet. Der noch nicht ausgereifte
Betrag kann nicht übertragen, verkauft oder verpfändet werden. Eine von der Münze übersprungene Antwort wird bezahlt
und mit „nicht geprüft“ markiert.

**Garantie und Annahmen.** Das erwartete Ergebnis jeder Serie von Fälschungen übersteigt den gesperrten Betrag
bei keinem Abspracheanteil: Das Kontrollbeispiel — eine Welle von zehn Fälschungen ergibt +4,4295`R` ohne
Verbrennung und −2,49676`R` mit ihr [Berechnung, von den Kritikern reproduziert]. Annahmen: Der Zahler
wirft die Münze tatsächlich und prüft rechtzeitig; das Journal ist verfügbar; der Betrag geht tatsächlich
verloren.

**Preis.** +50…+82% bei Batch 1; die Prüfung selbst bei ausgereiften Schlüsseln — 0,005–3,6% der Arbeit. Das erste
Fenster eines Neulings kostet 1,3–5,3% der Arbeit des Fensters in Einheiten der exakten Generierung [Berechnung].

**Schwache Stellen.** Die Lücke des faulen Zahlers ist durch keine Reparatur geschlossen: Bei leerem Konto
und `λ > 0` ist die Schwelle unerfüllbar. Bei geltendem D16 erklärt der Betrüger die Fälschung zum Ausfall und erhält
`(1 − p)·R − c_f`. Ein Saboteur kommt mit einer Wahrscheinlichkeit von `1 − p` durch. Eine billige Ergänzung ist die Untergrenze
der Häufigkeit (zum Beispiel kostet `p ≥ 1/11` 0,9–3,6% der Arbeit), aber auch dann kommen 90,9% der Fälschungen des Saboteurs
durch [Berechnung].

**Was zu ändern ist.** D2, D11 und D21 (Zahlung für eine von der Münze übersprungene Antwort); D7; Aufhebung von D16 für
eine veröffentlichte Abweichung; eine neue Entscheidung über den gesperrten Betrag; die Antwort, ob die Verbrennung
eine Strafe nach R5 ist; die Berechnung M9.

**Nicht gemessen.** Die Häufigkeit stiller Hardwareausfälle — von ihr hängt ab, wie viele ehrliche Teilnehmer
den Betrag verlieren; der Anteil der Zahler, die die Prüfung tatsächlich ausführen.

### V4. Aufgaben mit verifizierbarem Ergebnis

**Schritte.** Der Plan (D9) lässt vorab eine Aufgabe zu, deren Ergebnis von einem Zeugen begleitet wird,
der maschinell geprüft werden kann: Tests, ein formaler Beweis, die Lösung einer Aufgabe mit einem
Optimalitätszertifikat. Das Angebot wird vor der Offenlegung des Zeugen versiegelt, damit man ihn nicht
abfangen kann. Jeder Knoten prüft den Zeugen selbst; die Zahlung — einmal für den Inhalt der Aufgabe.

**Garantie.** Ein falscher Zeuge besteht nicht bei vollständiger Absprache, leerem Konto und jeder Zahl
von Schlüsseln.

**Preis.** Wenn `N − 1` Knoten mit `v` bei Kosten der Generierung `w` prüfen, ist der Aufschlag
`(N − 1)·v/w`. Bei `N = 1000` passt er nur bei `v/w ≤ 2·10⁻⁴` in 20%; bei `v/w = 10⁻³`
sind das bereits 99,9% [Berechnung]. Das Verhältnis `v/w` ist aus den Audits übernommen und nicht gemessen.

**Schwache Stellen.** Das ist ein anderes Produkt: keine freie Antwort des Modells und kein Gradientenschritt. Die Aufgabe
lässt sich ohne Modell und ohne Grafikkarte lösen. Eine Regel, die nützliche schwierige Aufgaben erzeugt,
ist nicht vorgelegt. Die Prüfung des Zeugen ist kopierbar, daher wird sie nach D15 nicht bezahlt: Die Idee „das Telefon
verdient mit der Prüfung von Zertifikaten“ widerspricht dem.

**Was zu ändern ist.** D9 und D15 ergänzen; D18 bleibt Forschung.

**Nicht gemessen.** Welcher Anteil der Arbeit des Netzes in diese Klasse fällt.

### V5. Zusatzmodul: exakte spekulative Dekodierung

Der Entwurf entsteht auf beliebige schnelle Weise; der Ausführende gleicht ihn selbst mit einem exakten Durchlauf ab
und korrigiert Abweichungen; bezahlt wird nur die bitgleich exakte Antwort. Die Garantie ist dieselbe wie
bei der Trägervariante V1 oder V3; die Entscheidungen ändern sich außer der Präzisierung von D22 nicht. Ein Gewinn ist nur möglich,
wenn die Token des schnellen und des exakten Profils häufig und in langen Serien übereinstimmen. Nichts
davon ist gemessen.

## 4. Empfehlung des Rats und erster Schritt

**Empfehlung (Zusammenfassung).** Der Hauptvertrag ist **V1**. Er allein erfüllt D1, D6, D7 und D25 für
die Antwort ohne neue Annahmen über Häufigkeit, gesperrten Betrag und Verbrennung und verlangt keine Änderung der angenommenen
Entscheidungen. Alle elf Arbeiten geben für ihn dieselbe Preisformel. **V4** — ein eigener Typ
von Aufgaben des Plans. **V2** — ein Tarif für abgestimmte Chargen. **V3** — ein Kandidat: erst nach der Berechnung M9 und ausdrücklichen Entscheidungen des Eigentümers einschalten. **V5** und die Beschleunigung der exakten Kerne — Wege
zur Senkung des Preises, keine eigenen Verträge.

**Präzisierungen der Entscheidungen für V1** (Vorschläge, keine Entscheidungen):

- D6: Es gibt zwei Markierungen — „geprüft“ nach vollständiger bitweiser Prüfung vor der Anzeige und „nicht geprüft“.
- D16: Bei der Prüfung jeder Antwort durch den Zahler zieht eine Abweichung nur die Nichtzahlung nach sich.
- D19: Wenn der Versuch kostenlos ist, wird die Annahme D19 nicht angewandt.
- D22: Der Entwurf kann auf beliebige Weise gewonnen werden; bezahlt wird nur die Antwort, die bitgleich
  zur exakten ist. Die Länge der Antwort und der Grund des Anhaltens gehen in den Gegenstand der Prüfung ein.
- D12 nicht ändern: Der Ersatz der aktiven Zeit durch die Höhe der Blöcke der externen Kette erlaubt es, noch nicht ausgereifte
  Beträge ausreifen zu lassen, während das Netz nicht verfügbar ist.
- Neue Entscheidung über den Preis: In welchem Profil wird der Umfang der Berechnungen gezählt. Bei einem Preis vom 1,10-Fachen der
  Selbstkosten des gewöhnlichen Profils verliert ehrliche Arbeit im exakten Profil 42–68% der Selbstkosten
  [Berechnung]; diese Prämisse selbst ist im Projekt nicht angenommen.

**Eine Berechnung.** M9: falsche Streitfälle ohne Pfand für einen einmaligen Auftrag — Schweigen jeder
Seite, Selbststreit, Selbstauftrag mit falschem Streit, Grenzen der Bytes und Berechnungen pro Fall, Quelle
der Mittel. Ohne sie wird keine Variante eingeschaltet (D23).

**Ein Experiment** (Genehmigung des Eigentümers nötig; Erweiterung der bereits durchgeführten O3 und O4). Am zusammengestellten
Profil v2 und llama.cpp Q8_0 bei gemeinsamem Präfix den Anteil der übereinstimmenden Token, die Verteilung
des Rückstands der Bewertung des gewählten Tokens und die Längen der Übereinstimmungsserien messen. Es entscheidet drei Fragen:
ob sich V5 lohnt; ob der Vertrag mit Toleranz lebensfähig ist; ob der Schnitt nach Positionen die Fälschung
„Entwurf + exakter Durchlauf“ fängt, das heißt, ob der Zahler ohne Grafikkarte überhaupt einen Schutz hat.
Zuerst lohnt es sich zu prüfen, ob in den Aufzeichnungen von D5 die vollständigen Bewertungen beider Profile erhalten geblieben sind.

**Wo die Kritiken und Arbeiten auseinandergegangen sind.**

1. **Welcher Vertrag der Hauptvertrag ist.** Die Kritiker Claude und ChatGPT — V1. Der Kritiker DeepSeek — V3 mit Reparaturen,
   und V1 als teurer Tarif und Modus des Neulings. Der Kritiker MiniMax — V1 als Basistarif und die Münze
   für ausgereifte Schlüssel, aber das Netz zahlt nur für Geprüftes.
2. **Ob für eine von der Münze übersprungene Antwort zu zahlen ist.** Dafür — die Mehrheit der Arbeiten; dagegen — beide Arbeiten
   von ChatGPT und eine Arbeit von MiniMax. Wenn nicht gezahlt wird, erhält der ehrliche Ausführende `p·R`
   für die Aufgabe, und das ist eine Lotterie ohne den Faktor `1/p`. Ein Drittes gibt es nicht; das ist die Wahl des Eigentümers.
3. **Welches Experiment das erste ist.** Die Kritiker Claude und ChatGPT — die Übereinstimmung der Token zweier Profile.
   Die Kritiker DeepSeek und MiniMax — ein Mikrobenchmark der 8-Bit-Kerne vom Typ Ozaki mit bitweiser Abgleichung:
   Er zeigt, ob der Richtwert von 5% überhaupt erreichbar ist. Die Zusammenfassung setzt ihn an die zweite Stelle.
4. **Das erreichbare `γ`.** 1,05–1,20, 1,1–1,3 oder „wird nicht sinken“. Nicht gemessen.
5. **Ob als Pfand nach R5 gelten:** die Verbrennung des noch nicht ausgereiften Betrags, die Streitreserve, die Lotteriereserve,
  die lange Reifezeit und die Bürgschaft.
6. **Ob der gesperrte Betrag nach oben begrenzt werden soll.** Eine Obergrenze von 10`R` begrenzt die erwartete Zahl
   der Fälschungen, macht aber die Prüfung ausgereifter Schlüssel etwa 400-mal teurer [Berechnung eines
   Kritikers, nicht nachgeprüft].
7. **Die dritte Markierung.** Der Kritiker MiniMax schlägt „teilweise geprüft“ vor; der Kritiker Claude — nur
   zwei Markierungen.

## 5. Training: Was es gibt und was nicht

**Was es nicht gibt.** Keine Arbeit gibt eine Garantie für den Trainingsschritt. Das Training hat keinen Zahler:
Die Grundlage der Ausgabe von Credits muss jeder volle Knoten prüfen. Ganzzahliges Training
ist nicht gebaut und nicht gemessen; die Messungen D5 betreffen nur den Vorwärtsdurchlauf und übertragen sich nicht auf den Rückwärtsdurchlauf
und den Optimierer.

**Was es gibt.**

- **Vollständige Wiederholung des Schritts durch jeden Knoten** — streng, kostet aber `N` zusätzliche Schritte: bei zehn
  Knoten etwa 1000% [Berechnung].
- **Schnitte des Schritts:** Der Knoten prüft etwa eine Zelle von viertausend. Der Preis 0,24% / 2,4% /
  24% bei 10 / 100 / 1000 Knoten [Berechnung], aber bei vollständiger Absprache ist die Entdeckung null.
- **Zahlung für ein verifizierbares Ergebnis** (V4): eine strenge Garantie für eine enge Aussage. Geprüft wird
  der Zeuge der Aufgabe, nicht der Gradientenschritt; die Formulierungen der Arbeiten „das Training ist gelöst“ und „der Schaden ist ausgeschlossen“
  hat die Kritik als übertrieben beurteilt.
- **Zahlung für eine bewiesene Verbesserung im Examen** (D18) bleibt Forschung: Das Examen
  bezeugt die Punktzahl auf einem gegebenen Satz, aber nicht das Fehlen einer Hintertür in den Gewichten.

**Die Grenze.** Bei 1000 Knoten und einem Aufschlag von 20% darf die gesamte unabhängige Prüfung eines Knotens nicht mehr als
0,0002 der Arbeit des Schritts kosten [Berechnung]. Ein kurzer Beweis des Schritts ist nach allen Kostenvoranschlägen des Projekts
um Größenordnungen teurer.

**Empfehlung des Rats.** Credits nur für Ergebnisse ausgeben, die jeder Knoten selbst prüft;
einen ungeprüften Schritt nicht in die Version des Modells aufnehmen (das ist bereits D6).

## 6. Was wörtlich unmöglich ist: Fragen an den Eigentümer

Die Texte R1–R6 schlägt der Rat nicht zu ändern vor. Die Vorschläge zweier Arbeiten, R4 und R6 zu ändern, hat die Kritik
abgelehnt: Das ist die unveränderliche Grundlage. Die allgemeine Unmöglichkeit, R4 und R6 für alle denkbaren
Algorithmen zu vereinbaren, ist nicht bewiesen; unten steht, was mit den gefundenen Konstruktionen unmöglich ist.

| № | Was unmöglich ist | Minimale Abschwächung | Empfehlung des Rats |
|---|---|---|---|
| 1 | Den Verbraucher ohne Ausrüstung bei vollständiger Absprache der Prüfer zu schützen: Der ehrliche und der falsche Fall geben ihm gleiche Nachrichten | Die Garantie wird nur der Seite versprochen, die selbst prüft; den Übrigen wird die Antwort mit der Markierung „nicht geprüft“ gezeigt, und die Größe des Risikos `R·q³` wird direkt genannt | Annehmen: Das ist bereits in D21 festgehalten, nur in die Beschreibung für den Nutzer zu übertragen |
| 2 | Den Trainingsschritt bei vollständiger Absprache innerhalb von 20% zu prüfen | (a) für ein verifizierbares Ergebnis zahlen, nicht für den Schritt; (b) „mindestens einen ehrlichen vollen Knoten“ zulassen; (c) den Richtwert 20% für ein kleines Netz aufheben | (a): der einzige Weg mit strenger Garantie; dabei bleibt ein Teil der freien Leistung ohne bezahltes Training |
| 3 | Eine geprüfte Antwort bei gemessenem `γ` = 1,52–1,78 in 5% unterzubringen | Den Richtwert 5% als Ingenieurziel betrachten, den tatsächlichen Preis veröffentlichen und die Senkung von `γ` als eigene Aufgabe führen | Annehmen; 5% — ein Richtwert der Roadmap, nicht der Text von R6 |
| 4 | Den Saboteur, der keinen Gewinn braucht, bei `p < 1` ökonomisch zurückzuhalten | Nur Markierungen und das Verbot, Ungeprüftes zu verwenden (D6) | Bereits angenommen; keine neuen Maßnahmen |
| 5 | Streit ohne Pfand bei einem endlichen Streitfonds | Entscheiden, ob die gesperrte Vorauszahlung des Käufers als Pfand nach R5 gilt | Nach der Berechnung M9 entscheiden |
| 6 | Vor allen Messungen vollständig sicher in der Entscheidung zu sein | Eine begrenzte Liste von Messungen erlauben, von denen die Wahl abhängt | Entscheidung des Eigentümers; der Rat nennt zwei Messungen aus Abschnitt 4 und das Experiment O5 |

Zusätzliche Fragen: ob für eine von der Münze übersprungene Antwort zu zahlen ist (Abschnitt 4, Punkt 2);
in welchem Profil der Preis der Aufgabe gezählt wird; ob eine Bürgschaft eines Dritten zuzulassen ist.

## 7. Was die Mini-Agenten berechnen und was durch Experimente zu prüfen ist

**Berechnungen** (exakte Brüche, Kontrollhash, Wiederholung auf einem zweiten Gerät; sie sind keine Experimente über das Protokoll):

1. M9 für alle Zweige des einmaligen Auftrags.
2. Der Gewinn der Fälschung „Entwurf + exakter Durchlauf“ unter Schnitten auf einem Gitter von `γ`, `ρ`, Übereinstimmungsanteil,
   Länge des Segments und der Antwort, Marge.
3. Die Münze mit Untergrenze der Häufigkeit und dem Anteil fauler Zahler, einschließlich des leeren Kontos.
4. Die gemischte Fälschung „alles ehrlich außer einer Spalte“ und die Fälschung durch Abbruch der Antwort.
5. Lotterie: die genaue Ruinwahrscheinlichkeit auf dem Weg und die Größe der Reserve des Käufers.
6. Die genauen Größen des Eingangs einer Zelle und des Schritts des Streits nach der Aufstellung des Profils v2 (48 MiB und 64 KiB abgleichen).
7. Die Flut neuer Schlüssel: die Last für den Zahler und die Ableitung der Quote neuer Schlüssel.
8. Die Aufzählung der kleinsten falschen Mengen von Zellen auf einem kleinen Modell.
9. Die Zusammenführung von `ρ` und `γ` auf einer Karte und gleichen Längen; der Preis für ein geprüftes Ergebnis.

**Experimente.** O5 ist durch die Entscheidung D5 erlaubt. Die übrigen liegen außerhalb von D5 und verlangen die Genehmigung des Eigentümers:

1. Übereinstimmung der Token und Rückstand der Bewertungen Q8_0 gegen v2 — das erste Experiment.
2. O5 — die Qualität des Profils v2 an 320 Aufgaben.
3. Mikrobenchmark der 8-Bit-Kerne mit bitweiser Abgleichung — Prüfung der Einschätzung von Ozaki.
4. `γ` und `ρ` paarweise auf einer Karte, einschließlich RTX 4070 Laptop.
5. Zeit und Speicher des Durchlaufs und des Segments auf dem Prozessor eines Laptops und auf dem Telefon.
6. Der Preis des Druckens der Spur, die Abdeckung von ABFT und die Häufigkeit stiller Ausfälle.
7. Experimente zum Training O6 und O7 — gesondert, nach der Entscheidung zu D18.

## 8. Wer was getan hat

- **ChatGPT:** zwei unabhängige Arbeiten und eine Kritik aller Arbeiten.
- **DeepSeek:** zwei unabhängige Arbeiten und eine Kritik mit Neuberechnung der Zahlen in exakter Arithmetik.
- **Claude:** zwei unabhängige Arbeiten, eine Kritik und diese Zusammenfassung.
- **MiniMax:** fünf unabhängige Arbeiten und eine Kritik.
- **Gemini** hat am Rat nicht teilgenommen: Im Hub der Modelle gab es keinen Schlüssel; sein Audit war unter den
  Eingabedaten.
- **Externe Audits und Karten der Mechanismen** — vom Eigentümer zusammengestellte Eingabedaten; der Rat
  hat sie nicht anhand der Primärquellen nachgeprüft.

Beschränkungen der Zusammenfassung: Der Kritiker ChatGPT hat zehn Arbeiten von elf durchgesehen; der Kritiker Claude hat
eine der Arbeiten nicht vollständig gelesen; die Berechnungen der Kritiker wurden jeweils auf einem Computer ausgeführt und warten auf
die Wiederholung durch die Mini-Agenten.
