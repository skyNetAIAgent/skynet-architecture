<!-- translation of docs/ROADMAP.md, source sha256: d87250a9f8cbdcefb8b84eeb7782bb83df46b90660c868ad259f1cfea11cf858 -->

# Roadmap: Schutz vor Betrug

[English](../../docs/ROADMAP.en.md) · [中文](../zh/ROADMAP.md) · [Español](../es/ROADMAP.md) · [Français](../fr/ROADMAP.md) · **Deutsch** · [Italiano](../it/ROADMAP.md) · [Русский](../../docs/ROADMAP.md) · [Português](../pt/ROADMAP.md) · [العربية](../ar/ROADMAP.md)

Stand vom 23. November 2026 (aktualisiert nach dem Release v0.2.2). Dies ist ein
**Arbeitsplan, kein Versprechen eines Ergebnisses**. Die Markierung `[x]` bedeutet „erledigt, und
dies lässt sich anhand des Repositoriums oder der Aufzeichnungen des Netzes prüfen“; `[ ]`
bedeutet „nicht erledigt“. Zahlen mit der Markierung [Berechnung] wurden anhand einer Formel
ermittelt, nicht gemessen. Die Roadmap wird bei jeder Statusänderung aktualisiert.

## 1. Ziel und Fertigstellungskriterien

**Ziel der aktuellen Projektphase:** eine Methode zur Ehrlichkeitsprüfung zu finden, bei der
zugleich die verbindlichen Anforderungen erfüllt sind ([REQUIREMENTS](REQUIREMENTS.md)):

- das Netz lässt sich nicht betrügen: Betrug ist nutzlos oder unrentabel, auch für einen Neuling
  mit leerem Konto, bei Absprache und bei vielen Schlüsseln;
- keine Mittel im Voraus: weder Pfänder noch Beiträge noch Strafen;
- die Teilnahme ist vorteilhaft, die Ehrlichkeitsprüfung billig. Richtwerte für den Prüfzuschlag:
  etwa 5% Arbeit für Modellanfragen und etwa 20% für das Training (nicht bestätigt).

**Die Arbeit gilt als erledigt, wenn alles Folgende vorliegt:**

1. **Aufgeschrieben ist, was genau garantiert wird** (Entscheidung D1): für das Ergebnis einer Anfrage, für einen Trainingsschritt, für die Auszahlung und für den Verlauf; für ein leeres Konto, eine
   beliebige Zahl von Schlüsseln, den Weggang und die vollständige Absprache der Aufgabenprüfer.
   Die Anforderung lässt „Betrug ist nutzlos“ zu; ein Nettoverlust bei jedem einzelnen Versuch muss
   nicht nachgewiesen werden.
2. **Für jeden Angriff aus der Angriffstabelle ist eine Regel aufgeschrieben, nach der ein Knoten
   eine falsche Meldung verwirft, und aus welchen Daten er das tut.** Getrennt angegeben sind die
   Wahrscheinlichkeit einer falschen Annahme, der Schaden für das Netz und der Reingewinn der
   Koalition gegenüber Untätigkeit und gegenüber ehrlicher Arbeit. Gegenbeispiel zur Regel: ein
   ehrlicher und ein falscher Fall, in denen der Knoten dieselben Daten sieht. Stichprobe, kleine
   Fehlerwahrscheinlichkeit und „es findet sich ein ehrlicher Beobachter“ werden als Annahmen
   festgehalten.
3. **Der vollständige Preis der Prüfung ist berechnet** gegenüber derselben Aufgabe ohne Prüfung:
   Arbeit des Ausführenden und der Prüfer, Speicher, Datenverkehr, Ablage, Eintrag ins Journal,
   Streitfälle, Wiederholungen nach Ausfällen. Abgeleitet sind der Nettoertrag eines Teilnehmers
   mit großen Ressourcen bei teurem Strom, die Zuzahlung eines Teilnehmers mit schwacher
   Ausrüstung und der Preis für einen Verbraucher ohne Ausrüstung. Eintrag und Streitfall sind ab
   einem leeren Konto möglich; verlieren kann man nur noch nicht ausgereifte Belohnungen.
4. **Die Berechnungen sind reproduzierbar:** beigefügt sind die Version der Regeln und des
   Kernels, die Eingaben, die Grenzen der Aufzählung, die Ausgabe und der Hash; die Berechnung
   wurde auf einem zweiten Gerät wiederholt. Die Wiederholung bestätigt die Rechnung, nicht aber
   die Richtigkeit des Modells selbst: diese wird gesondert begründet.
5. **Gemessen ist, was sich durch Überlegung nicht feststellen lässt:** die Übereinstimmung des
   Ergebnisses bis aufs Bit auf verschiedenen Grafikkarten, Geschwindigkeit und Qualität des
   ganzzahligen Modells, der Preis des Streitfalls. Profile, Metriken und Schwellen sind vor der
   Messung festgelegt.
6. **Die übrigen Anforderungen sind nicht verletzt:** das Netz arbeitet ohne jeden einzelnen
   Knoten oder Standort, findet sich nach vollständigem Stillstand wieder, die Grundlagen der
   Gutschriften lassen sich wiederherstellen; bei einer Netztrennung wartet eine strittige
   Auszahlung auf den gemeinsamen Verlauf, eine Wiederholung wird nicht doppelt bezahlt.

Auch ein ehrliches Ergebnis ist ein Ergebnis: Wenn für eine Klasse von Aufgaben eine billige
Prüfung unmöglich ist, wird dies durch einen Beweis mit der benannten Aufgabenklasse und den
benannten Daten des Prüfers gezeigt, nicht durch das Fehlen von Ideen.

## 2. Wo wir jetzt stehen

| Was | Status | Wo es festgehalten ist |
|---|---|---|
| Anhand von Signaturen und kurzen Antworten lässt sich nicht feststellen, welches Gerät wie lange gearbeitet hat: ein Vermittler, ein Cache und eine untätige Karte liefern dieselben Daten | Durch Überlegung festgestellt | [OPEN_QUESTIONS](OPEN_QUESTIONS.md), „Was bereits verworfen wurde“ |
| Das Netz bezahlt für das überprüfbare Ergebnis, nicht für die Ressource | Angenommen (D2); die Ergebniseinheit und die Annahmebedingung sind noch nicht bestimmt | [CURRENT_DESIGN](CURRENT_DESIGN.md), Abschnitt 1 |
| Aufgeschobene Auszahlung statt Pfand: Der Teilnehmer haftet nur mit dem ausstehenden Betrag | Angenommen | CURRENT_DESIGN, Abschnitt 2 |
| Variante A: Stichprobenprüfung mit Abzug | Aktuelle Spezifikation | CURRENT_DESIGN, Abschnitt 3 |
| Variante B: Das Netz bezahlt nur für geprüfte Aufgaben, und zwar zum `1/p`-Fachen des regulären Preises | Hauptkandidat; Wahl nach dem Vergleich (D3) | CURRENT_DESIGN, Abschnitt 3 |
| Übereinstimmung des Ergebnisses bis aufs Bit durch ganzzahlige Arithmetik | Auf kurzen Eingaben gemessen: Prozessor, RTX 2060 und RTX 4070 Laptop liefern dieselben Bits für das ganzzahlige Qwen3.5-4B (24. November 2026); langer Kontext, Geschwindigkeit und Qualität sind noch nicht gemessen | [EXPERIMENT_D5](EXPERIMENT_D5.md), Abschnitt 7 |
| Streitfall durch Halbieren mit Neuberechnung eines Schritts im Journal | Gemessen für eine Zeile des Modells; für das vollständige Modell nicht gebaut | [PILOT_RESULTS](PILOT_RESULTS.md) |
| Prüfung der Matrixmultiplikation mit einem Zufallsvektor innerhalb des Streitfalls | Kandidat, es gibt nur eine rechnerische Schätzung | CURRENT_DESIGN, Abschnitt 3 |
| Ein unveränderlicher Prüfkern, der nicht per Abstimmung abgeschafft werden kann | Angenommen (D4) | CURRENT_DESIGN, Abschnitt 8 |

**Was über die Stärke des Schutzes bekannt ist.**

- Variante A, ohne Absprache: In der aufgezählten Familie (zwei Wellen von Fälschungen, 92 Mio.
  Strategien) bringt der Abgang mit Fälschungen nicht mehr als der gewöhnliche Abgang
  [Berechnung].
- Variante A, Absprache: Die ersten Gitterpunkte, an denen der Abgang mit Fälschungen lohnt, sind
  ein Abspracheanteil von 87,5% (Aufgaben beliebiger Größe) und 89,0% (gleiche Aufgaben) bei der
  Regel „nicht mehr als ein Drittel in Arbeit“, 80% ohne diese Regel. Gitterschritt 0,002–0,02;
  andere Strategiefamilien sind nicht aufgezählt [Berechnung, [FIRST_RUN](FIRST_RUN.md)].
- Variante B, ohne Absprache: Bei genauem Vergleich wird eine Fälschung nicht bezahlt.
- Variante B, Absprache: `q` ist der Gewichtsanteil der Koalition unter den Prüfern dieses
  Modells. Eine Fälschung wird nur bezahlt, wenn die Aufgabe gewählt ist und alle `k` Prüfer an der Absprache beteiligt sind. Die mittlere Auszahlung für eine eingereichte Fälschung beträgt `R·q^k`
  (`R` ist der Preis der Aufgabe) und hängt nicht von `p` ab [Berechnung]. Bei `q = 1` ist das
  der volle Preis. Bei einem Neuling mit leerem Konto gibt es nichts abzuziehen.
- Für keine der beiden Varianten ist eine Garantie gegen unberechtigte Auszahlungen bei vollständiger Absprache der Prüfer nachgewiesen. Sie ergibt sich aus der Prüfung jedes bezahlten Ergebnisses
  anhand von Daten, die jeder Knoten selbst prüft. Die vollständige Neuberechnung fügt etwa 100%
  Arbeit hinzu. Messungen des Piloten: Der Beweis von RISC Zero für eine Zeile des Modells wurde in
  22 min 10 s erstellt; die Ausführung von acht Zeilen in der zkVM dauerte etwa 17 700-mal länger
  als gewöhnlich, ohne Beweiserstellung. Eine allgemeine Untergrenze für den Preis ergeben diese
  Messungen nicht.
- Ungleichmäßigkeit des Einkommens in Variante B: Bei 6000 Aufgaben im Monat, einer Prüfung von 1
  aus 100 und Selbstkosten von 95% des Preises beträgt die Wahrscheinlichkeit eines verlustreichen
  Monats 33,10% [Berechnung, FIRST_RUN].
- Der erste Durchlauf der Berechnungen (702 Portionen) wurde auf einem Computer gemacht. Ein
  zweites Gerät hat bis zum 23. November alle 702 Portionen nachgerechnet; alle stimmten überein.
  Seine Einträge sind mit dem Schlüssel `46000d30…` signiert und auf einem vollständigen Knoten
  verfügbar. Beide Geräte gehören den Betreuern, deshalb ist dies noch keine Bestätigung durch
  einen unabhängigen Teilnehmer.

**Was nicht gelöst ist.**

1. Neuling mit leerem Konto in einer Absprache (Variante B): mittlerer Gewinn `R·q^k` pro
   Versuch, es gibt keine Verluste.
2. „Lange ehrlich, dann groß betrogen und gegangen“: Der Verlust ist auf den ausstehenden Betrag
   begrenzt, der Gewinn wächst mit der Zahl der Fälschungen. Reparaturen für Variante B sind
   vorgeschlagen, nicht berechnet.
3. Müllstrom von kostenlosen Schlüsseln. Ein Schlüssel kostet nichts; die Bezahlung durch
   Prozessorarbeit bringt schwache Geräte in eine schlechtere Lage.
4. Ein Ergebnis, das vor der Prüfung genutzt wurde. Die Antwort ist vom Nutzer bereits gelesen,
   der Schritt bereits ins Training eingegangen; die Begrenzung der Auszahlungen behebt das
   nicht. In Variante B gilt das auch für nicht gewählte Aufgaben.
5. Lernaufgaben, die durch die Ausgabe von Credits bezahlt werden: Wer und nach welcher Regel
   genehmigt sie. Eine korrekt ausgeführte, aber selbst zugewiesene Aufgabe darf keine Credits
   geben.
6. Seltenes Modell: Der Kreis der Prüfer ist klein, und `q` kann dafür nahe bei eins liegen.
7. Verfügbarkeit der Daten und Streitfall über eine private Anfrage ohne Offenlegung der Anfrage.
8. Die Übereinstimmung bis aufs Bit des ganzzahligen Modells ist nur auf kurzen Eingaben von drei
   Geräten bestätigt; langer Kontext, Geschwindigkeit und Qualität sind nicht gemessen.
9. Ein Saboteur, der keinen Nutzen braucht, und die Vergiftung von Trainingsdaten. Der
   wirtschaftliche Schutz wirkt bei ihnen nicht.

## 3. Entscheidungen

Die Entscheidungen D1–D5 wurden am 23. November 2026 getroffen, D6–D25 am 24. November 2026 (im Auftrag des Eigentümers; D18–D25 zu den Fragen der Phase 4, Begründungen in [VERIFICATION_SEARCH](VERIFICATION_SEARCH.md), Abschnitt 6).

| Nr. | Frage | Entscheidung |
|---|---|---|
| D1 | Was als Garantie angenommen wird | **Der Betrüger bekommt nicht, was er will.** Betrugsversuche lassen sich nicht ausschließen, aber jeder Versuch muss für denjenigen, der ihn unternimmt, nutzlos sein: Der erwartete Gewinn aus einer Fälschung ist nicht größer als null im Vergleich zur ehrlichen Arbeit und zur Untätigkeit, für jede Koalition, einschließlich eines Neulings mit leerem Konto und beliebig vieler Schlüssel. Das Ziel ist, dass ein falsches Ergebnis überhaupt nicht bezahlt wird. Ein Nettoverlust bei jedem Versuch ist nicht erforderlich. Eine begrenzte, aber positive Leckage (zum Beispiel `R·q^k` bei einem Neuling in Variante B) **erfüllt das Kriterium nicht** und bleibt ein offenes Loch |
| D2 | Grundlage der Bezahlung | **Angenommen: Bezahlt wird nur das überprüfbare Ergebnis.** Eingeschaltete Ausrüstung, Arbeitszeit und behauptete Leistung sind keine Grundlage der Bezahlung: Eine Grafikkarte lässt sich auch mit etwas Fremdem belasten |
| D3 | Variante A oder B | **Die Entscheidung wird nach dem Vergleich bei gleichen Angriffen und gleichem Preis (Phase 2) getroffen.** Hauptkandidat ist Variante B |
| D4 | Unveränderlicher Prüfkern | **Angenommen in verstärkter Form.** Die Prüfung läuft automatisch, ohne Beteiligung eines Menschen und ohne Abstimmungen. Die Regeln der Prüfung werden nicht per Abstimmung geändert. Jeder Knoten führt die Prüfung selbst nach dem festgeschriebenen Fingerabdruck der Regeln aus, deshalb ändert ein Austausch des Algorithmus auf einem Knoten oder bei einem Anbieter des Programms nichts an den Entscheidungen der anderen. Offen: wie ein Fehler im Kern selbst behoben wird (nur durch den Übergang zu einem neuen Netz) und wie ein Teilnehmer sich vergewissert, dass sein Programm dem veröffentlichten Fingerabdruck entspricht (reproduzierbarer Build). Der Release-Schlüssel, mit dem derzeit die Mini-Agenten signiert werden, ist ein Werkzeug der Forschung; im Zielnetz darf es ihn nicht geben |
| D5 | Erster Versuch mit dem ganzzahligen Qwen3.5-4B | **Erlaubt:** eine Grafikkarte RTX 2060 auf dem heimischen Linux des Betreuers, dessen Computer und, mit Einverständnis, Geräte anderer Teilnehmer über Mini-Agenten. Wird nach Phase 0 ausgeführt |
| D6 | Gehört Schaden zu D1 | **Ja** (entschieden am 24. November 2026 im Auftrag des Eigentümers). „Der Betrüger bekommt nicht, was er will“ bezieht sich nicht nur auf Credits, sondern auch auf das Ergebnis: Eine falsche Antwort darf dem Nutzer nicht als geprüft ausgegeben werden, ein falscher Schritt nicht ins Modell eingehen. Deshalb wird ein Ergebnis nur nach einer Prüfung genutzt, die nicht vom Abspracheanteil abhängt, oder ausdrücklich als ungeprüft gekennzeichnet |
| D7 | Prüfung unabhängig vom Abspracheanteil oder Abschwächung von D1 | **Eine Prüfung, die nicht vom Abspracheanteil abhängt, ist erforderlich** (24. November 2026). D1 wird nicht auf „solange die Verschworenen weniger als q\* sind“ abgeschwächt. Phase 4 wird zur Hauptphase |
| D8 | Streitfall ab leerem Konto | **Streiten können nur die durch Los bestimmten Prüfer dieser Aufgabe und der Nutzer für seine eigene Anfrage** (24. November 2026). Ohne Pfand; der Strom der Streitfälle ist durch die Zahl der Prüfungen und Anfragen begrenzt. Alle übrigen melden einen Verdacht auf dem Brett, ohne das Recht, eine Auszahlung zu stoppen |
| D9 | Wer den Trainingsplan genehmigt | **Niemand persönlich: Der Plan wird durch eine festgeschriebene Regel aus dem offenen Katalog und den Ergebnissen des Examens abgeleitet** (24. November 2026). Ohne Abstimmungen. Credits werden nur für Aufgaben des Plans ausgegeben, einmal je Aufgabeninhalt |
| D10 | Leckage eines Teils beim Tausch | **Gilt als Verletzung von D1.** Der Tausch von Credits und anderen Werten läuft nur über das Journal, mit einem einzigen Eintrag für beide Teile, ohne eine vertrauenswürdige Partei außerhalb des Journals |
| D11 | Zusammensetzung des unveränderlichen Kerns | **Die Prüfung, die Regel „Bezahlt wird nur das Geprüfte“, die Regel der Credit-Ausgabe, der Streitfall und die Journalregeln.** Tarife, Netzgebühr und Modellkatalog ändern sich nur innerhalb der im Kern festgeschriebenen Grenzen |
| D12 | Zeit für Gewicht und Prüffenster | **Die aktive Zeit des Netzes**, nicht der Kalender: Solange das Netz stillsteht, altert das Gewicht nicht und das Prüffenster läuft nicht |
| D13 | Zugang zu Aufgaben in Variante B | **Der Neulingsweg aus Variante A wird eingeführt:** Der Zugang zu Aufgaben hängt vom ausstehenden Betrag des Schlüssels ab. Die endgültige Wahl zwischen A und B (D3) erfolgt nach dem Vergleich |
| D14 | Preis des Streitfalls | **Für den Kostenvoranschlag wird ein Layer-2-Netz mit dem billigsten Eintrag genommen.** Die Differenz zwischen dem Preis des Streitfalls und dem Betrag, der vom Verlierer abgezogen werden kann, bezahlt die Netzgebühr der Verbraucher, nicht die Ausgabe von Credits |
| D15 | Wiederholte Prüfungen und Lehrlingsprüfungen | **Eine einfache Neuberechnung, die sich kopieren lässt, wird nicht bezahlt.** Eine Prüfung wird nur dort bezahlt, wo ihr Ergebnis nicht durch Kopieren der Antwort eines anderen erhalten werden kann |
| D16 | Ehrlicher Geräteausfall | **Wird nicht als Betrug bestraft:** Die Aufgabe wird nicht bezahlt, der ausstehende Betrag verfällt nicht; die Zahl solcher Ausfälle pro Schlüssel ist begrenzt |
| D17 | Quelle der Auszahlung für Anfragen in Variante B | **Nur aus den Zahlungen der Nutzer**, ohne Ausgabe von Credits |
| D18 | Bezahlung des Trainings für eine nachgewiesene Verbesserung | **Wird als Kandidat für eine neue Einheit der Trainingsbezahlung untersucht, aber nicht angenommen.** Das ist weder eine Prüfung des Schritts noch ein Beweis dafür, dass kein Schaden entsteht: Das Modell wird nur nach der Regel D9 freigegeben. Die Entscheidung über die Annahme erfolgt nach den Berechnungen M7, M8, M10–M12 und dem Versuch O6 (außerhalb von D5, die Erlaubnis des Eigentümers ist erforderlich). Die Suche nach einer Prüfung des Schritts selbst geht weiter |
| D19 | Kleine kryptografische Fehlerwahrscheinlichkeit | **Wird als ausdrückliche Annahme zugelassen** unter drei Bedingungen: Zufälligkeit von einem externen Beacon nach der endgültigen Fixierung, die Stichprobe wird nicht aus den Daten des Ausführenden abgeleitet (ohne Fiat–Shamir), die Untergrenze des Preises eines Versuchs ist aufgeschrieben und `ε·R` ist kleiner als sie. Der Fehler beträgt höchstens `2⁻⁸⁰` pro Versuch. Eine gewöhnliche Stichprobenprüfung mit Leckage `q^k` wird dadurch nicht zulässig |
| D20 | Externer Beacon | **Mindestens zwei unabhängige öffentliche Quellen**, der Wert wird zu einem im Voraus bestimmten Zeitpunkt nach der endgültigen Fixierung entnommen, ohne das Recht, ihn zu überspringen. Die Quellen und der Preis des Einflusses auf sie werden in Phase 2 gewählt; das Vertrauen in sie wird als Annahme aufgeschrieben. Bis zur Wahl des Schemas mit Stichprobe werden sie nicht einbezogen |
| D21 | Wer die Antwort des Modells prüft | **Eine vom Abspracheanteil unabhängige Prüfung der Antwort gibt es nur beim Zahler, der selbst prüft.** Eine Antwort ohne Prüfung bezahlt das Netz nicht. Ein Nutzer ohne Ausrüstung kann selbst einen Prüfer bestimmen; das ist seine Annahme, D1 sagt das Netz für ihn nicht zu. Die Garantie für einen solchen Nutzer bleibt eine offene Frage |
| D22 | Produktänderungen für eine billige Prüfung | **Sind als eigene Aufgabentypen des Plans mit ausdrücklichem Vertrag erlaubt** (kanonische Token-Wahl, ganzzahliges Profil, Aufgaben mit prüfbarem Ausgang, exakte Optimierer), nach dem Versuch O5 und der Berechnung M17. Die gewöhnliche Stichprobe bleibt mit der Kennzeichnung „ungeprüft“ |
| D23 | Falsche Streitfälle des Zahlers | **Zuerst die Berechnung M9.** Die Prüfung durch den Zahler wird nicht einbezogen, solange keine Regel zur Begrenzung falscher Streitfälle ohne Pfand gewählt ist |
| D24 | Chiffretext der Antwort im Journal | **Ja:** wird mit einem einzigen Eintrag zusammen mit der Annahme aufgezeichnet, etwa 2–4 KB pro Antwort |
| D25 | Zweiseitige Formulierung von D1 | **Wird nicht geändert:** Eine Fälschung, die schlechter als ehrliche Arbeit, aber vorteilhafter als Untätigkeit ist, verletzt ebenfalls D1 |

**Reihenfolge der Arbeit.** Zuerst wird Phase 0 abgeschlossen — die Mini-Agenten und die
Anwendungen für Smartphones, damit sich andere Menschen an der Arbeit beteiligen können. Danach
die Phasen 1–5 nach dieser Roadmap.

## 4. Phasen und Checkliste

Zuerst wird Phase 0 abgeschlossen. Danach laufen die Phasen 1–4 gleichzeitig: Es sind
Berechnungen und Überlegungen. Phase 5 (der Versuch ist durch die Entscheidung D5 erlaubt) läuft
nach Phase 0. Phase 6 führt die Ergebnisse zusammen.

### Phase 0. Mini-Agenten und Anwendungen für Smartphones (wird zuerst ausgeführt)

**Ziel der Phase.** Auf jeder unterstützten Plattform durchläuft ein Mensch den Weg „heruntergeladen → installiert → gestartet“, und danach aktualisiert sich der Mini-Agent ohne Beteiligung des Menschen, nimmt Aufgaben und liefert das Ergebnis ab. Ohne Benutzerkonto, ohne Administratorrechte, ohne vorab installiertes Python. Jeder Schritt ist auf einem lebenden Gerät geprüft, nicht nur durch automatische Tests.

**Fertig, wenn** für jede Plattform aus der Liste unten: ein Mensch ohne Erfahrung den Weg anhand
einer einzigen Seite der Anleitung gegangen ist; der Agent auf diesem Gerät selbst einen neuen
Release erhalten hat, selbst eine Aufgabe der neuen Liste genommen hat, sein Ergebnis auf dem
vollständigen Knoten erschienen ist und mit dem Ergebnis eines anderen Geräts übereingestimmt hat.
Aufgeschrieben sind System, Architektur, die Versionen davor und danach und die Kennung des
Eintrags auf dem Knoten.

Plattformen: Windows, Linux, Android (Entscheidung vom 23. November 2026). Für macOS und iOS
werden Mini-Agenten nicht gemacht und nicht geprüft. Der Installationsbefehl für Linux
funktioniert möglicherweise auch unter macOS, aber das wird nicht unterstützt. Die
Windows-Version wird ohne Codesignatur veröffentlicht: Bei der Installation zeigt Windows eine
SmartScreen-Warnung, sie muss manuell bestätigt werden; die Echtheit der Datei wird anhand des
veröffentlichten Hashes und der Signatur des Projekts geprüft.

Bereits erledigt:

- [x] Öffentliches Repositorium, unveränderliche Grundlage in neun Sprachen (Tag `core-v1`).
- [x] Agentenprogramm für Windows und Linux: signierte Aufgaben und Aktualisierungen,
      automatische Prüfungen in CI (Release 0.2.0). Installation mit einem Befehl im Terminal;
      Python 3.9+ ist nötig.
- [x] Ergebnisse und [Aufgabenbrett](BOARD.md) ohne Benutzerkonto.
- [x] Erster vollständiger Knoten, der den Verlauf der Einträge speichert.
- [x] Erste Forschungsaufgabe „Schutz vor Betrügern“ auf dem Brett, in neun Sprachen.
- [x] Testanwendung für Android 0.1.0 (nur auf dem Emulator geprüft).

**Schritt 1. Zuverlässigkeit der Aktualisierung (Release 0.2.1, ohne neue Aufgaben)**

- [x] Die erste Installation prüft die Signatur des Release mit einem in den Installer selbst
      eingebetteten Schlüssel, **bevor** der heruntergeladene Code gestartet wird (früher prüfte
      der heruntergeladene Agent sich selbst).
- [x] Der Wechsel auf eine neue Version mit einer einzigen atomaren Operation: Zuerst wird das
      neue Verzeichnis vorbereitet und geprüft, dann wird ein einziger Zeiger geändert; der
      vorherige funktionsfähige Satz bleibt erhalten.
- [x] Die größte angenommene Release-Nummer wird außerhalb der Versionsverzeichnisse gespeichert
      und auch bei einer Neuinstallation geprüft (Schutz vor dem Rückstieg auf einen alten
      Release).
- [x] Geräteschlüssel, Einstellungen, Fortschritt und nicht gesendete Ergebnisse werden außerhalb
      der Versionsverzeichnisse gespeichert und überstehen Aktualisierung und Neuinstallation.
- [x] Ohne Netz arbeitet der Agent auf der letzten funktionsfähigen Version weiter und wiederholt
      die Verbindung mit wachsendem Abstand.
- [x] Automatische Prüfung in CI: eine ausgetauschte Datei, ein fremder Schlüssel, eine alte
      Nummer, eine überzählige Datei, ein abgebrochener Download und ein inkompatibles Python
      werden verworfen, die funktionsfähige Version bleibt erhalten.
- [x] **Live-Prüfung auf einem Server:** Die Installation von 0.2.0 ist am 23. November 2026 selbst auf
      0.2.2 übergegangen, Geräteschlüssel und Fortschritt sind erhalten. Auf dem heimischen Linux
      wurde der Agent mit dem neuen Installer (0.2.2) neu installiert; seine Selbstaktualisierung
      wird der nächste Release prüfen.
- [x] Live-Prüfung der Selbstaktualisierung unter Windows: Die Installation des Eigentümers ging
      selbst von 0.2.2 → 0.3.0 → Go 1.0.1 über (23. November 2026).

**Schritt 2. Android: Anwendung ohne Token**

- [x] Neue APK 0.2.0 mit eingebettetem Agenten 0.2.2: Veröffentlichung durch signierte Einträge,
      der Token-Bildschirm und die Hinweise zum Token sind entfernt.
- [x] Den fälschlichen Rückstieg ohne Netz beheben: Früher markierten drei Starts ohne Verbindung
      die funktionsfähige neue Version als fehlerhaft. Jetzt wird die Version durch eine lokale
      Selbstprüfung bestätigt.
- [x] Die Anwendung prüft einmal täglich neue APK-Versionen, gleicht Hash und Signatur des
      Projekts ab und bietet die Installation an; die Installation bestätigt der Mensch (so ist
      Android außerhalb des Stores aufgebaut).
- [x] Start nach dem Neustart über einen Schalter des Nutzers (auf dem Emulator geprüft).
- [x] Prüfung der Aktualisierung über APK 0.1.0 im Emulator Android 14: die Daten bleiben erhalten.
- [x] APK 0.4.1 (24. November 2026): Der Versand der Ergebnisse wurde behoben — Android verbot die
      Art der Speicherung des Geräteschlüssels; auf dem Emulator wurden 4 von 4 ohne Token gerechnet
      und gesendet.
- [x] APK 0.4.2: Der Start nach dem Neustart ist standardmäßig aktiviert (durch einen Neustart des
      Emulators geprüft). Der alte Testrelease 0.1.0, der einen Token verlangte, ist als veraltet
      gekennzeichnet.
- [ ] Prüfung des Angebots einer neuen APK durch die Anwendung selbst (greift mit der nächsten
      APK-Version).
- [ ] **Prüfung auf einem echten Telefon** (ein Teilnehmer mit einem Telefon ist nötig):
      Installation, Arbeit beim Laden, Neustart, Energiesparen des Herstellers.

**Schritt 3. Windows: Installer als eine Datei**

- [x] `SkyNetAgentSetup.exe` wird in GitHub Actions gebaut, ohne Codesignatur; darin ein
      eingebettetes Python von python.org, der Agent und ein signierter Release. Daneben werden
      sein Hash und die Signatur des Projekts veröffentlicht. Installation ins Profil des
      Nutzers, ohne Administratorrechte, funktioniert ohne Netz.
- [x] Verknüpfungen im Startmenü: Status des Agenten, Pause, Fortsetzen, Beenden, Deinstallation.
- [x] Die Häkchen „jetzt starten“ und „beim Anmelden starten“ im Installer sind standardmäßig
      aktiviert (ab 1.3.3); die Wahl bleibt bei der Aktualisierung erhalten.
- [x] Deinstallation über „Apps“; bei der Deinstallation kann der Geräteschlüssel behalten
      werden.
- [x] Automatische Prüfung in CI auf einem sauberen Windows ohne Python: Installation,
      Selbstprüfung, Deinstallation.
- [x] Live-Prüfung auf dem Computer einer Person: Der Eigentümer hat den Agenten aus den Releases
      installiert (Release v0.2.2).

**Schritt 4. Linux**

- [x] Der Installer nutzt das systemweite Python 3.9+, und wenn es fehlt, installiert er ein portables
      Python und prüft dessen Hash. Es gibt auch einen Installer als eine Datei, der ohne Netz
      funktioniert (Release v0.2.2).
- [x] Ab 1.3.3 startet der Installer den Agenten sofort, registriert einen systemd-Benutzerdienst
      (Start nach dem Neustart) und versucht, den Betrieb ohne Anmeldung zu aktivieren (linger);
      `--no-autostart` — nur Installation.
- [x] Ab 1.3.4 findet der Agent selbst einen vollständigen Knoten in seinem lokalen Netz (Anfrage
      per UDP, Antwort nur an private Adressen). Nötig dort, wo der Router von innerhalb des Netzes
      nicht zur externen Adresse des Knotens durchlässt; früher wurde dies durch manuelle
      Einstellung der Adresse umgangen.
- [x] Live-Prüfung der Suche nach einem Knoten im lokalen Netz: Agent 1.3.4 fand den Knoten
      ohne manuelle Einstellung und erschien auf der Agentenseite (25. November 2026).
- [x] Prüfung in CI: Debian 12 ohne Python und Ubuntu 24.04 mit Python; Live-Installation auf Linux Mint.
- [ ] Live-Prüfung bei einem Teilnehmer, der nicht mit den Betreuern verbunden ist.

**Schritt 5. Agent in Go statt Python (Entscheidung des Eigentümers vom 23. November 2026)**

Der Agent ist in Go neu geschrieben: ein kleines Programm, Python ist nicht nötig. Das eingebettete
Python und seine Aktualisierung werden nicht mehr benötigt, deshalb ist der frühere Schritt
„Aktualisierung des eingebetteten Python“ entfallen.

- [x] Signaturen, Aufgaben, sieben Rechenkerne, Einträge, Nostr, Brett, Arbeitszyklus, Aktualisierung
      über den zweiten Kanal (`agent/v2/release.json`), Starter, Autostart — in Go, nur die
      Standardbibliothek (Code schrieb ChatGPT, geprüft hat DeepSeek).
- [x] Die Ergebnisse von Go stimmen mit Python Bit für Bit überein bei allen schnellen Portionen der
      Referenz und bei allen geprüften schweren; der Abgleich aller 1 199 Portionen läuft weiter.
- [x] Reproduzierbarer Build: gleiche Hashes der Programme beim Bauen unter Windows und Linux.
- [x] Die Brücke auf Python 0.4.0 stellt installierte Agenten selbst auf Go um und behält dabei
      Geräteschlüssel, Fortschritt und Warteschlange. Live-Übergang: Server, heimisches Linux und
      Windows des Eigentümers sind selbst auf Go 1.0.1 übergegangen.
- [x] Installer in Go: Windows 4,7 MB, Linux als eine Datei; Android-Anwendung 0.3.0 mit Go-Engine,
      etwa 8 MB statt 40 (geprüft auf dem Emulator Android 14).
- [x] Releases in Go 1.1.0–1.3.4 (24. November 2026): Antworten des lokalen KI-Modells,
      Berechnungen der Phase 4, Agentenseite, Autostart, Suche nach einem Knoten im lokalen Netz;
      installierte Agenten aktualisierten sich selbst.
- [ ] Die Brücke und die Python-Kopien nach zwei geprüften Releases in Go entfernen.

**Schritt 6. Aufgabenstrom**

- [x] Vier neue Rechenaufgaben der Phase 2 (Ausstiegskampagne in Variante B, Lehrlingsplätze,
      Lotterie mit gewähltem Prüfanteil, Zertifikat des gewinnenden Tokens) — neue eingebaute
      Kerne des Agenten 0.3.0, 515 Portionen in der Aufgabenliste Nr. 2. Die Mathematik wurde
      unabhängig mit einer anderen Methode an 111 Punkten nachgeprüft. Das Zertifikat bringt bei
      zufälligen Matrizen keine Ersparnis (etwa 0,8% zusätzliche Arbeit), deshalb sind 20 Portionen
      als Grundlage für den Vergleich mit den Gewichten des echten Modells belassen.
- [x] Neue Aufgaben erfordern den Agenten 0.3.0 und höher; ein alter Agent überspringt eine
      inkompatible Aufgabe und arbeitet weiter (durch einen Test geprüft).
- [ ] Wenn alle Aufgaben gerechnet sind, wartet der Agent und nimmt selbst die nächste Liste auf.
- [ ] Der Ergebnissammler arbeitet nach Zeitplan auf dem vollständigen Knoten und veröffentlicht
      eine Übersicht.
- [ ] Unabhängige Bestätigung aller 702 Portionen der ersten Liste. Ein zweites Gerät (der Server
      der Betreuer) hat alle 702 nachgerechnet, alle stimmten überein; einen Teilnehmer, der nicht
      mit den Betreuern verbunden ist, gibt es noch nicht.

**Schritt 7. Pilot mit anderen Menschen**

- [x] Seite [„Wie man sich anschließt“](CONNECT.md) in neun Sprachen: ein Link für jedes System.
- [x] Agentenseite online auf dem vollständigen Knoten: `http://62.213.14.254:8790/agents` —
      Betriebssystem, Prozessor, RAM, Grafikkarten, Version, Portionen; ohne IP-Adressen und
      Computernamen. Der Agent meldet sich alle 2 Minuten, 5 Minuten Stille entfernen ihn aus der
      Liste (Agent 1.3.0+).
- [ ] Je ein Teilnehmer, der nicht mit den Betreuern verbunden ist, auf jeder Plattform; die
      Fertigstellungskriterien der Phase sind erfüllt.
- [ ] Zweiter und dritter vollständiger Knoten bei verschiedenen Besitzern.

**Schritt 8. KI-Agenten**

- [x] Der Agent holt selbst neue Aufgaben des Bretts und übergibt sie dem lokalen Modell des
      Teilnehmers; die Antwort wird erst nach Freigabe durch den Menschen gesendet. Der Text der
      Aufgabe gilt als nicht vertrauenswürdig (Agent 1.1.0, standardmäßig ausgeschaltet).
- [ ] Anleitung für den KI-Assistenten: wie man eine Aufgabe vom Brett nimmt, einen Bericht
      einreicht und einen fremden prüft.
- [ ] Bericht zu einer Brettaufgabe von einem Teilnehmer, der nicht mit den Betreuern verbunden
      ist.

**Entscheidungen des Eigentümers zu Phase 0** (23. November 2026): macOS und iOS werden nicht
gemacht; die Windows-Version wird ohne Codesignatur veröffentlicht.

### Phase 1. Genaue Formulierung

- [x] Die Entscheidungen D1 und D2 sind getroffen und aufgeschrieben (Abschnitt 3).
- [ ] Für eine offene Anfrage und einen Lernschritt sind aufgeschrieben: Annahmeregel, Arithmetik,
      Grundlage der Ausgabe von Credits, der Zeitpunkt, zu dem das Ergebnis im Verhältnis zur Auslosung festgelegt wird und der Zeitpunkt, ab dem das Ergebnis genutzt werden darf.
- [x] Gegnermodell in einem Dokument: [THREAT_MODEL](THREAT_MODEL.md), Abschnitt 1 (Modellrat aus
      sechs Modellen und drei Kritikern, 24. November 2026).
- [x] Die Tabelle der analysierten Angriffe ist in neun Sprachen veröffentlicht, mit dem Status
      jedes Angriffs für die Varianten A und B: 60 Angriffe der Spezifikation und 32 neue. Die
      Abweichung zwischen 59 und 60 ist erklärt: In der Zusammenfassung fehlte die Zeile 1.9
      („kein Angriff“).
- [x] Für jeden Angriff ist aufgeschrieben, anhand welcher unabhängig prüfbaren Daten ein Knoten
      eine falsche Meldung bei Absprache von Ausführendem und Prüfern verwirft. Ergebnis: Weder
      Variante A noch Variante B erfüllt D1 wörtlich; ein Geldgewinn ist in 24 Zeilen von A und 25
      Zeilen von B möglich [Berechnung].
- [x] Entscheidungen zu allen zwölf Fragen aus Abschnitt 5 von [THREAT_MODEL](THREAT_MODEL.md): D6–D17.

Fertig, wenn: jeder Teilnehmer anhand der Tabelle einen nicht geschlossenen Angriff nennen und
dies prüfen kann.

### Phase 2. Ökonomie: Berechnungen, die Mini-Agenten ausführen

Jede Aufgabe ist ein genaues Modell mit endlichem Eingangsraster; Wahrscheinlichkeiten und Summen
werden als exakte Brüche berechnet, der Hash jeder Portion wird zwischen den Geräten abgeglichen.

- [x] Variante A, Abgang mit Fälschungen: erster Durchlauf.
- [x] Variante B, Ungleichmäßigkeit des Einkommens bei konstantem Prüfanteil: erster Durchlauf.
- [ ] Unabhängige Bestätigung beider Berechnungen (siehe Phase 0).
- [ ] **Ausstiegskampagne in Variante B.** Eingaben: ausstehender Betrag `H₀`, Preis `R`,
      Prüfanteil `p`, Absprache `q` und `k`, Obergrenze gleichzeitiger Aufgaben `C`, Zahl der
      Wellen `T`. Eine erwischte Fälschung setzt den gesamten ausstehenden Betrag auf null,
      einschließlich der Gewinne der Welle. Den größten erwarteten Auszahlungsüberschuss über `H₀`
      finden, auch bei `H₀ = 0`, `q = 0` und `q = 1`.
- [ ] **Lehrlingsplätze.** Pro Epoche werden `S` Plätze zwischen `n` ehrlichen und `m` Schlüsseln
      der Koalition verteilt. Die erwartete Leckage über `E` Epochen finden und den Anteil der
      Plätze, der an ehrliche Neulinge geht, bei wachsendem `m`.
- [ ] **Lotterie mit gewähltem Prüfanteil.** Für `N` Aufgaben im Monat das kleinste `p` nehmen,
      bei dem im Durchschnitt mindestens 60 Aufgaben bezahlt werden. Die Wahrscheinlichkeit eines
      verlustreichen Monats und Quartals finden, die Wahrscheinlichkeit eines Monats ohne eine
      einzige Auszahlung und die Zahl der Neuberechnungen für das Netz.
- [ ] **Zertifikat des gewinnenden Tokens** (siehe Phase 4): Zahl der Prüfoperationen gegenüber
      der vollständigen Neuberechnung der Ausgabeschicht auf einer gegebenen Eingabemenge.
- [ ] Formel für den vollständigen Preis der Prüfung für drei Arten von Teilnehmern; nach Phase 5
      werden die Messungen eingesetzt.
- [ ] Vergleich der Varianten A und B bei gleichen Angriffen und gleichem Preis, danach die
      Entscheidung D3. Möglicher Ausgang: Beide Varianten bleiben Forschungsvarianten.

Fertig, wenn: Für jede Variante eine Tabelle „Abspracheanteil → größter erwarteter Gewinn des
Betrügers“ vorliegt, nachgerechnet auf mindestens zwei unabhängigen Geräten.

### Phase 3. Bekannte Löcher schließen

- [ ] **Neuling mit leerem Konto.** Kandidat: Die ersten Aufgaben eines Neulings sind so
      beschaffen, dass jeder Knoten sie selbst genau prüft, und erst danach werden Belohnung und
      Gewicht gutgeschrieben. Reservevariante: ein gemeinsames Budget für Lehrlingszahlungen pro
      Epoche; es begrenzt die Leckage, macht sie aber nicht null, und eine Absprache kann alle
      Plätze besetzen.
- [ ] **„Lange ehrlich, dann groß betrogen“.** Kandidat: eine Obergrenze für die Summe aller
      offenen Verbindlichkeiten eines Schlüssels, die größten möglichen Gewinne eingerechnet. Das
      ist die Grenze einer Welle, keine Leckage von null.
- [ ] **Müll von kostenlosen Schlüsseln.** Kandidat: Ein Knoten nimmt Daten nur zu erlaubten
      Aufgabennummern an, begrenzt Größe, Warteschlange und Arbeit pro Epoche. Den Kanal kann man
      trotzdem füllen; ein garantierter Platz für einen ehrlichen Neuling bei beliebiger
      Schlüsselzahl ist nicht erreicht.
- [ ] **Ergebnis, das vor der Prüfung genutzt wurde.** Kandidat: Den Antwortblock vor der Ausgabe
      prüfen; den Lernschritt in einem eigenen Zweig halten und nur den geprüften Nachkommen
      übernehmen. Preis: Verzögerung und Speicher.
- [ ] Lernaufgaben: Genehmigungsregel ohne einen Teilnehmer mit Sonderrechten.
- [ ] Seltenes Modell: eine aus der Gewichtsverteilung abgeleitete Schwelle, unterhalb derer das
      Netz für das Modell nicht bezahlt.
- [ ] Fauler Prüfer und erneutes Einreichen eines bekannten Ergebnisses: kryptografische Commitments, die den Wert bis zur Offenlegung verbergen, einmalige Gutschrift nach dem Inhalt.
- [ ] Geräteausfall bei einem ehrlichen Teilnehmer: eine Regel, die dem Betrüger keinen Gewinn
      verschafft.
- [ ] Verfügbarkeit der Daten und Streitfall über eine private Anfrage ohne Offenlegung.
- [ ] Streitfenster bei Netzstillstand, Schutz vor veraltetem Verlauf, Netztrennung.

Fertig, wenn: Zu jedem Punkt eine Konstruktion mit Annahmen, ein Angriff auf sie und der Preis
veröffentlicht sind, oder ein Gegenbeispiel, oder der Status „offen“ mit Begründung.

### Phase 4. Suche nach einer Garantie, die nicht vom Abspracheanteil abhängt

Gesucht wird eine Prüfung, die jeder Knoten selbst ausführt, sodass die Zustimmung der Prüfer
nichts entscheidet. Die Richtungen sind nicht genehmigt. Für jede sind die zu prüfenden
Operationen, die Daten, die Fehlerwahrscheinlichkeit und der Preis einer ganzen Anfrage oder eines
Schritts anzugeben; danach zu einer Konstruktion auszubauen oder durch ein Gegenbeispiel zu
schließen.

- [x] Der Modellrat (sechs Arbeiten und drei Kritiken) hat alle Richtungen durchgearbeitet; Ergebnis
      und Aufgaben für die Mini-Agenten — [VERIFICATION_SEARCH](VERIFICATION_SEARCH.md), 24. November 2026.
- [x] Erste exakte Berechnungen für die Mini-Agenten: M8, M10, M12 und M14 aus Abschnitt 5.3 der
      Zusammenfassung ([STAGE4_KERNELS](STAGE4_KERNELS.md)), Agent 1.2.0, Aufgabenliste Nr. 3. Die
      Berechnungen M5, M7 und M18 wurden zurückgestellt: In den Arbeiten fehlen die Regeln, um sie
      eindeutig zu bestimmen.
- [ ] **Aufgaben mit billigem exaktem Richtigkeitsmerkmal.** Beispiel: Bei der Ridge-Regression
      prüft ein Knoten die Optimalitätsbedingung in einem Durchlauf über die Daten. Frage: Welcher
      Anteil der Netzarbeit passt in solche Aufgaben. Mit dieser Richtung beginnen: Sie führt zu null unberechtigten Auszahlungen. *Ergebnis:* Hält für eine enge Klasse von Aufgaben; der Anteil solcher Arbeit ist unbekannt.
- [x] **Prüfung jeder Matrixmultiplikation mit einem Zufallsvektor** statt Neuberechnung. Der
      Vektor wird nach der Fixierung des Ergebnisses gewählt; die Wahrscheinlichkeit, einen Fehler
      zu übersehen, hängt nicht von der Absprache ab. Vorteilhaft für große Batches; bei der
      Erzeugung Token für Token gibt es keinen Gewinn. Die übrigen Operationen (Rundung,
      Aktivierungen, Cache, Optimierer) müssen gesondert geprüft werden. *Ergebnis:* Als billige Prüfung
      durch einen Netzknoten widerlegt (stößt an den Datenverkehr); hält als Prüfung des Zahlers mit schnellem Kanal.
- [ ] **Prüfung einer fertigen Antwort in einem Modelllauf** mit exaktem Profil und in der
      Aufgabe festgelegter Zufälligkeit. Die Zahl der Operationen ist von derselben Größenordnung
      wie bei der Erzeugung; ob dies in 5% passt, ist nicht festgestellt. *Ergebnis:* Bester Kandidat für die Antwort des Modells ist die Prüfung
      durch den Zahler, 1,2–3,8% bei der Erzeugung einer einzelnen Antwort [Berechnung]; wartet auf den Versuch D5 und die Entscheidung D23.
- [x] **Tabellen exakter Teilsummen für unveränderliche Schichten:** Ein Knoten leitet einmal
      Tabellen aus den Gewichten ab und erhält danach die Ausgabe einer Schicht durch Lesen und
      Addieren. Auch auf einen einzelnen Token anwendbar; stößt an die Speichermenge. *Ergebnis:* durch Berechnung widerlegt.
- [x] **Zertifikat des gewinnenden Tokens** für ein großes Vokabular: Der Ausführende übermittelt
      die Abdeckung des Vokabulars in Gruppen, der Knoten prüft die oberen Grenzen und steigt nur
      dort zu einzelnen Tokens hinab, wo die Grenze den Gewinner nicht trennt. Im schlimmsten Fall
      wird das gesamte Vokabular geprüft. *Ergebnis:* hält als Teil der Prüfung der gierigen Auswahl.
- [x] **Lernschritt als exakte Aktualisierungsformel:** Die Knoten speichern und prüfen nicht die
      neue Gewichtsmatrix, sondern die Aktualisierungsfaktoren. Hergeleitet nur für eine lineare
      Schicht mit einfachem SGD. *Ergebnis:* als Prüfung des Schritts widerlegt.
- [x] **Ein Streitfall, offen für jeden Teilnehmer innerhalb des Fensters.** Die Garantie ist
      bedingt: Es braucht mindestens einen Beobachter, der die Daten erhalten und rechtzeitig Einspruch erhoben hat. Wer die Beobachtung bei leerem Konto bezahlt, ist nicht entschieden.
      Als Reserve behalten. *Ergebnis:* als vom Abspracheanteil unabhängige Prüfung widerlegt.
- [ ] **Bezahlung für die gemessene Modellverbesserung** auf Aufgaben, die nach der Fixierung der
      Gewichte gewählt wurden. Ändert die Grundlage der Bezahlung und erfordert eine gesonderte
      Entscheidung. Geeignet für die Auswahl von Modellversionen. *Ergebnis:* der einzige
      verbliebene Weg für das Training, mit Korrekturen; wird nach D18 untersucht.
- [ ] **Rechenbeweise für das Training (sumcheck, GKR)** für einen bestimmten Schritt:
      vollständiger Kostenvoranschlag mit Bereichen, Rundung und Bindung des Eingangs an die
      Aufgabe. *Ergebnis:* hält als Richtung; konkrete Aufteilungen sind widerlegt, 20% sind nicht gezeigt.
- [x] **Untere Grenze:** zeigen, welche Klassen von Prüfungen nicht fehlerfrei sein können.
      Anfang: Ein fester Satz linearer Prüfungen, dessen Anzahl kleiner als die Größe des
      Ergebnisses ist, lässt immer irgendeinen Fehler durch; offen bleiben frische Zufälligkeit
      und Eingaben mit bekannter Struktur. *Ergebnis:* die haltbaren Grenzen sind in
      [VERIFICATION_SEARCH](VERIFICATION_SEARCH.md), Abschnitt 2, veröffentlicht.
- [ ] Ideen von Teilnehmern und KI-Assistenten vom Brett: Jede durchläuft dieselbe Analyse,
      einschließlich des Falls `q = 1`.

Fertig, wenn: Für jede Richtung eine Konstruktion mit Kostenvoranschlag, ein Gegenbeispiel oder
eine bewiesene Grenze veröffentlicht ist. Als gefunden gilt eine Konstruktion, die alle Kriterien
aus Abschnitt 1 erfüllt.

### Phase 5. Grundlagen, die sich nur durch Erfahrung feststellen lassen (durch D5 erlaubt)

- [x] Versuchsplan: ganzzahliges Profil Qwen3.5-4B, Protokolle O1–O5 und Widerlegungskriterien
      vor dem Start — [EXPERIMENT_D5](EXPERIMENT_D5.md), 24. November 2026. Die zweite Grafikkarte —
      RTX 4070 Laptop auf dem Computer des Eigentümers.
- [x] Vorbereitung (P0) und Profil v2: Das Modell wurde mit dem offiziellen Quelltext abgeglichen;
      auf dem Prozessor wählt das ganzzahlige Profil denselben Token wie das offizielle Modell, in
      90 von 90 Positionen (Korrelation der Logits 0,9996). Das erste Profil v1 verlor an Genauigkeit
      und wurde ersetzt.
- [x] Kurze Eingaben: Prozessor, RTX 2060 (Linux) und RTX 4070 Laptop (Windows) liefern dieselben
      Bits — je 242 Mio. Logits, 976 Tokens und 37 Tsd. Zustands-Hashes pro Gerät; die Erzeugung
      Token für Token und der Durchlauf über eine fertige Antwort stimmen überein (O1 und O2,
      24. November 2026).
- [x] Andere Architektur: AMD Radeon RX 580 (OpenCL, Mesa) und NVIDIA über OpenCL liefern
      dieselben Bits wie die CUDA-Version und der Prozessor, auf denselben kurzen Eingaben
      (25. November 2026).
- [x] Langer Kontext (512 + 64, 2048 + 256, 4096 + 64 Tokens): RTX 2060 (CUDA und OpenCL) und
      RTX 4070 Laptop liefern dieselben Bits; die Erzeugung stimmt mit dem Durchlauf über eine
      fertige Antwort überein (25. November 2026). RX 580: Die Erzeugung stimmt überein, aber der
      Durchlauf über eine lange Antwort wird vom Treiber abgebrochen — der Attention-Kernel muss
      aufgeteilt werden.
- [x] Anteil der Zeit für die Prüfung einer Antwort an der Erzeugung (O3): 0,10–0,40 bei Batch 1
      auf RTX 2060 und RTX 4070 Laptop — die Schwelle von 5% ist für die derzeitige Implementierung
      widerlegt (25. November 2026).
- [x] Seine Geschwindigkeit gegenüber dem gewöhnlichen Profil (O4): auf der RTX 2060 1,5–1,8-mal
      langsamer als llama.cpp Q8_0 bei Batch 1, 2,5–2,8-mal bei Batch 8 (25. November 2026).
- [x] Der Modellrat zur Prüfung „nicht direkt“ (Vorhersage von Betrug, Anomalien,
      Stichprobenprüfung, Inspektionsspiele): [STRATEGY_SEARCH](STRATEGY_SEARCH.md),
      25. November 2026.
- [x] Der Modellrat zu einem verborgenen und sich ändernden Detektor (geheime Regeln,
      Verschlüsselung, Blockchain, Schwellenkryptografie, FHE, MPC, TEE): Die Geheimhaltung der
      Regeln bringt nicht mehr als eine geheime Zufallsprüfung zum selben Preis; nützlich sind
      nur die Geheimhaltung der Auswahl vor der Fixierung der Antwort und die Geheimhaltung der
      Rolle — [HIDDEN_DETECTOR](HIDDEN_DETECTOR.md), 25. November 2026.
- [x] Audit der Vollständigkeit der Forschung (sechs unabhängige Audits und zwei vom
      Eigentümer zusammengestellte Mechanismuskarten) und der Modellrat zu den Varianten der
      Betrugsbekämpfung, einschließlich der Ideen „Überprüfbarkeit innerhalb des Modells“ und
      „Tricks aus Spielen“: [ANTIFRAUD_OPTIONS](ANTIFRAUD_OPTIONS.md), 27. November 2026.
      Die Entscheidungen zu den Varianten stehen noch beim Eigentümer aus.
- [ ] Seine Qualität gegenüber dem gewöhnlichen Profil auf derselben Aufgabensammlung.
- [ ] Gesonderte Messpläne (außerhalb von D5): Energie der Prüfung, ganzzahliges Training.
- [ ] Preis des Streitfalls im Journal für das vollständige Modell. Davor sind nötig: die Wahl der
      Blockchain, die Referenzmaschine des vollständigen Modells, die Bindung der Eingabe, der Länge des Rechenablaufs und des Rechenpfads.

Fertig, wenn: Jede Zahl gemessen ist, die Messbedingungen aufgeschrieben sind und ein zweiter
Teilnehmer die Messung wiederholt hat. Die Übereinstimmung der Bits bezieht sich nur auf die
geprüften Konfigurationen.

### Phase 6. Zusammenführung und Abnahme

- [x] Die Entscheidung D4 über den unveränderlichen Kern (Abschnitt 3).
- [ ] Zusammensetzung des Kerns und die Art, wie ein Teilnehmer sich vergewissert, dass
      sein Programm dem veröffentlichten Fingerabdruck entspricht.
- [ ] CURRENT_DESIGN und die Angriffstabelle nach dem Ergebnis der Phasen 1–5 aktualisieren.
- [ ] Eine Meldung ist auf dem Papier von der Freigabe der Aufgabe bis zur Nutzung des Ergebnisses
      verfolgt, einschließlich Ablehnung, Wiederholung und Netztrennung.
- [ ] Offene Begutachtung der endgültigen Konstruktion: Modellrat und Aufgabe auf dem Brett.
- [ ] Für jede Anforderung ist ein Beweis, eine Messung, ein Gegenbeispiel oder der Status
      „offen“ veröffentlicht. Prüfung anhand der sechs Kriterien aus Abschnitt 1.

## 5. Wie die Arbeit abläuft

1. Ein Punkt der Checkliste wird zu einer Aufgabe: einer Rechenaufgabe (sie wird von
   Mini-Agenten gerechnet, das Ergebnis wird durch Übereinstimmung abgeglichen) oder einer
   Forschungsaufgabe (sie wird auf dem Brett veröffentlicht).
2. Teilnehmer und ihre KI-Assistenten reichen Berichte ein. Ein Bericht wird nur angenommen, wenn
   er sich prüfen lässt: durch Nachrechnen, ein Gegenbeispiel oder einen Verweis auf die Quelle.
   Die Zahl zustimmender Schlüssel beweist nichts; die Entscheidung des Autors der Aufgabe auf dem
   Brett bestätigt keine Berechnung.
3. Nach dem Ergebnis der Prüfung wird die Aufgabe geschlossen, präzisiert oder bringt neue
   Aufgaben hervor.
4. Eine Statusänderung wird mit einer einzigen Änderung und mit Datum in diese Roadmap und in
   CURRENT_DESIGN eingetragen.

## 6. Was diese Roadmap nicht verspricht

- Dass eine Lösung unter den gegebenen Bedingungen existiert. Das ist Gegenstand der Suche.
- Fristen. Das Projekt hat keine bezahlten Ausführenden; die Geschwindigkeit hängt von den
  Teilnehmern ab.
- Belohnungen für die Teilnahme an der Ausarbeitung.
