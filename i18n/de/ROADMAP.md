<!-- translation of docs/ROADMAP.md, source sha256: 4cd77f720933922c55c4d78c3e761ca614215cc0ed8610b0fb2ae2e3fbee22e2 -->

# Roadmap: Schutz vor Betrug

[English](../../docs/ROADMAP.en.md) · [中文](../zh/ROADMAP.md) · [Español](../es/ROADMAP.md) · [Français](../fr/ROADMAP.md) · **Deutsch** · [Italiano](../it/ROADMAP.md) · [Русский](../../docs/ROADMAP.md) · [Português](../pt/ROADMAP.md) · [العربية](../ar/ROADMAP.md)

Stand vom 23. November 2026. Dies ist ein **Arbeitsplan, kein Versprechen eines Ergebnisses**. Die
Markierung `[x]` bedeutet „erledigt, und dies lässt sich anhand des Repositoriums oder der
Aufzeichnungen des Netzes prüfen“; `[ ]` bedeutet „nicht erledigt“. Zahlen mit der Markierung
[Berechnung] wurden anhand einer Formel ermittelt, nicht gemessen. Die Roadmap wird bei jeder
Statusänderung aktualisiert.

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
| Das Netz bezahlt für das überprüfbare Ergebnis, nicht für die Ressource | Grundlage des Projekts; die Ergebniseinheit und die Annahmebedingung warten auf Festschreibung (D2) | [CURRENT_DESIGN](CURRENT_DESIGN.md), Abschnitt 1 |
| Aufgeschobene Auszahlung statt Pfand: Der Teilnehmer haftet nur mit dem ausstehenden Betrag | Angenommen | CURRENT_DESIGN, Abschnitt 2 |
| Variante A: Stichprobenprüfung mit Abzug | Aktuelle Spezifikation | CURRENT_DESIGN, Abschnitt 3 |
| Variante B: Das Netz bezahlt nur für geprüfte Aufgaben, und zwar zum `1/p`-Fachen des regulären Preises | Vorschlag (D3) | CURRENT_DESIGN, Abschnitt 3 |
| Übereinstimmung des Ergebnisses bis aufs Bit durch ganzzahlige Arithmetik | Kandidat, nicht gemessen | OPEN_QUESTIONS, Q2 |
| Streitfall durch Halbieren mit Neuberechnung eines Schritts im Journal | Gemessen für eine Zeile des Modells; für das vollständige Modell nicht gebaut | [PILOT_RESULTS](PILOT_RESULTS.md) |
| Prüfung der Matrixmultiplikation mit einem Zufallsvektor innerhalb des Streitfalls | Kandidat, es gibt nur eine rechnerische Schätzung | CURRENT_DESIGN, Abschnitt 3 |
| Ein unveränderlicher Prüfkern, der nicht per Abstimmung abgeschafft werden kann | Vorschlag (D4) | CURRENT_DESIGN, Abschnitt 8 |

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
  zweites Gerät hat bis zum 22. November 40 Portionen nachgerechnet; alle stimmten überein. Seine
  Einträge sind mit dem Schlüssel `46000d30…` signiert und auf einem vollständigen Knoten
  verfügbar. Die übrigen 662 Portionen sind unabhängig nicht bestätigt.

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
8. Die Übereinstimmung bis aufs Bit und die Geschwindigkeit des ganzzahligen Modells sind nicht
   gemessen.
9. Ein Saboteur, der keinen Nutzen braucht, und die Vergiftung von Trainingsdaten. Der
   wirtschaftliche Schutz wirkt bei ihnen nicht.

## 3. Entscheidungen, die auf Genehmigung warten

Solange eine Entscheidung nicht getroffen ist, bleiben die davon abhängigen Punkte des Plans
Vorschläge.

| Nr. | Frage | Was davon abhängt |
|---|---|---|
| D1 | Was als Garantie angenommen wird. Genügt „Betrug bringt nichts, Ausgegebenes geht verloren, ehrliche Arbeit lohnt sich mehr“? Ist eine begrenzte Leckage bei Absprache zulässig, oder muss eine falsche Auszahlung auch bei vollständiger Absprache der Prüfer ausgeschlossen sein | Fertigstellungskriterien, Phasen 3 und 4 |
| D2 | Die Bezahlung für das überprüfbare Ergebnis statt für Leistung und Zeit festschreiben; die Ergebniseinheit und die Annahmebedingung bestimmen | Phasen 2–6 |
| D3 | Variante A, Variante B oder keine. Entscheidet sich nach dem Vergleich bei gleichen Angriffen und gleichem Preis (Phase 2) | Phasen 3 und 6 |
| D4 | Der unveränderliche Prüfkern und was zu ihm gehört | Phase 6 |
| D5 | Erster Versuch: ganzzahliges Qwen3.5-4B auf zwei verschiedenen Grafikkarten (ob die Bits übereinstimmen, Geschwindigkeit, Qualität) | Phase 5 |

## 4. Phasen und Checkliste

Die Phasen 1–4 laufen gleichzeitig: Es sind Berechnungen und Überlegungen. Die Suche nach neuen
Algorithmen (Phase 4) wartet nicht auf die übrigen. Phase 5 erfordert die Entscheidung D5. Phase 6
führt die Ergebnisse zusammen.

### Phase 0. Werkzeuge für die Zusammenarbeit

- [x] Öffentliches Repositorium, unveränderliche Grundlage in neun Sprachen (Tag `core-v1`).
- [x] Agentenprogramm für Windows, Linux und macOS: signierte Aufgaben und Aktualisierungen,
      automatische Prüfungen auf drei Systemen (Release 0.2.0).
- [x] Ergebnisse und [Aufgabenbrett](BOARD.md) ohne Benutzerkonto.
- [x] Erster vollständiger Knoten, der den Verlauf der Einträge speichert.
- [x] Erste Forschungsaufgabe „Schutz vor Betrügern“ auf dem Brett, in neun Sprachen.
- [ ] Bericht zu einer Brettaufgabe von einem Teilnehmer, der nicht mit den Betreuern verbunden
      ist, mit Angabe, von wem und wie er erzielt wurde. Derzeit sind alle Einträge im Netz von
      Geräten der Betreuer gemacht. Verschiedene Schlüssel beweisen nicht verschiedene Besitzer.
- [ ] Unabhängige Bestätigung aller 702 Portionen der ersten Aufgabenliste (derzeit 40).
- [ ] Aktualisierung des Agenten von einer veröffentlichten Version auf die nächste, beobachtet
      auf einer laufenden Installation (derzeit nur durch Tests geprüft).
- [ ] Android-Anwendung: Prüfung auf einem echten Telefon, Veröffentlichung der Ergebnisse ohne
      Token.
- [ ] Installation ohne vorab installiertes Python: eine Datei für Windows, macOS und Linux.
- [ ] Anleitung für den KI-Assistenten: wie man eine Aufgabe vom Brett nimmt, einen Bericht
      einreicht und einen fremden prüft.
- [ ] Automatischer Zyklus für KI-Assistenten: Der Agent holt selbst neue Aufgaben vom Brett und
      übergibt sie dem lokalen Modell des Teilnehmers. Derzeit geschieht das manuell durch
      Befehle.
- [ ] Zweiter und dritter vollständiger Knoten bei verschiedenen Besitzern.
- [ ] Die veraltete Zeile in BOARD korrigieren („Agent 0.2.0 ist noch nicht veröffentlicht“).

### Phase 1. Genaue Formulierung

- [ ] Die Entscheidungen D1 und D2 sind getroffen und aufgeschrieben.
- [ ] Für eine offene Anfrage und einen Lernschritt sind aufgeschrieben: Annahmeregel, Arithmetik,
      Grundlage der Ausgabe von Credits, der Zeitpunkt, zu dem das Ergebnis im Verhältnis zur Auslosung festgelegt wird und der Zeitpunkt, ab dem das Ergebnis genutzt werden darf.
- [ ] Gegnermodell in einem Dokument: Absprache, viele Schlüssel, Weggang, gemietete
      Rechenleistung; was als Gewinn des Betrügers gilt und was als Schaden für das Netz.
- [ ] Die Tabelle der analysierten Angriffe ist im Repositorium in neun Sprachen veröffentlicht,
      mit dem Status jedes Angriffs für die Varianten A und B. Vor der Veröffentlichung die Zeilen
      abgleichen: In der Zusammenfassung von CURRENT_DESIGN ergibt die Summe der Kategorien
      18 + 6 + 19 + 16 = 59 bei angegebenen 60.
- [ ] Für jeden Angriff ist aufgeschrieben, anhand welcher unabhängig prüfbaren Daten ein Knoten
      eine falsche Meldung bei Absprache von Ausführendem und Prüfern verwirft.

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

- [ ] **Aufgaben mit billigem exaktem Richtigkeitsmerkmal.** Beispiel: Bei der Ridge-Regression
      prüft ein Knoten die Optimalitätsbedingung in einem Durchlauf über die Daten. Frage: Welcher
      Anteil der Netzarbeit passt in solche Aufgaben. Mit dieser Richtung beginnen: Sie schließt unberechtigte Auszahlungen aus.
- [ ] **Prüfung jeder Matrixmultiplikation mit einem Zufallsvektor** statt Neuberechnung. Der
      Vektor wird nach der Fixierung des Ergebnisses gewählt; die Wahrscheinlichkeit, einen Fehler
      zu übersehen, hängt nicht von der Absprache ab. Vorteilhaft für große Batches; bei der
      Erzeugung Token für Token gibt es keinen Gewinn. Die übrigen Operationen (Rundung,
      Aktivierungen, Cache, Optimierer) müssen gesondert geprüft werden.
- [ ] **Prüfung einer fertigen Antwort in einem Modelllauf** mit exaktem Profil und in der
      Aufgabe festgelegter Zufälligkeit. Die Zahl der Operationen ist von derselben Größenordnung
      wie bei der Erzeugung; ob dies in 5% passt, ist nicht festgestellt.
- [ ] **Tabellen exakter Teilsummen für unveränderliche Schichten:** Ein Knoten leitet einmal
      Tabellen aus den Gewichten ab und erhält danach die Ausgabe einer Schicht durch Lesen und
      Addieren. Auch auf einen einzelnen Token anwendbar; stößt an die Speichermenge.
- [ ] **Zertifikat des gewinnenden Tokens** für ein großes Vokabular: Der Ausführende übermittelt
      die Abdeckung des Vokabulars in Gruppen, der Knoten prüft die oberen Grenzen und steigt nur
      dort zu einzelnen Tokens hinab, wo die Grenze den Gewinner nicht trennt. Im schlimmsten Fall
      wird das gesamte Vokabular geprüft.
- [ ] **Lernschritt als exakte Aktualisierungsformel:** Die Knoten speichern und prüfen nicht die
      neue Gewichtsmatrix, sondern die Aktualisierungsfaktoren. Hergeleitet nur für eine lineare
      Schicht mit einfachem SGD.
- [ ] **Ein Streitfall, offen für jeden Teilnehmer innerhalb des Fensters.** Die Garantie ist
      bedingt: Es braucht mindestens einen Beobachter, der die Daten erhalten und rechtzeitig Einspruch erhoben hat. Wer die Beobachtung bei leerem Konto bezahlt, ist nicht entschieden.
      Als Reserve behalten.
- [ ] **Bezahlung für die gemessene Modellverbesserung** auf Aufgaben, die nach der Fixierung der
      Gewichte gewählt wurden. Ändert die Grundlage der Bezahlung und erfordert eine gesonderte
      Entscheidung. Geeignet für die Auswahl von Modellversionen.
- [ ] **Rechenbeweise für das Training (sumcheck, GKR)** für einen bestimmten Schritt:
      vollständiger Kostenvoranschlag mit Bereichen, Rundung und Bindung des Eingangs an die
      Aufgabe.
- [ ] **Untere Grenze:** zeigen, welche Klassen von Prüfungen nicht fehlerfrei sein können.
      Anfang: Ein fester Satz linearer Prüfungen, dessen Anzahl kleiner als die Größe des
      Ergebnisses ist, lässt immer irgendeinen Fehler durch; offen bleiben frische Zufälligkeit
      und Eingaben mit bekannter Struktur.
- [ ] Ideen von Teilnehmern und KI-Assistenten vom Brett: Jede durchläuft dieselbe Analyse,
      einschließlich des Falls `q = 1`.

Fertig, wenn: Für jede Richtung eine Konstruktion mit Kostenvoranschlag, ein Gegenbeispiel oder
eine bewiesene Grenze veröffentlicht ist. Als gefunden gilt eine Konstruktion, die alle Kriterien
aus Abschnitt 1 erfüllt.

### Phase 5. Grundlagen, die sich nur durch Erfahrung feststellen lassen (erfordert D5)

- [ ] Ganzzahliges Qwen3.5-4B auf zwei verschiedenen Grafikkarten: ob die Bits übereinstimmen.
- [ ] Seine Geschwindigkeit gegenüber dem gewöhnlichen Profil auf denselben Karten.
- [ ] Seine Qualität gegenüber dem gewöhnlichen Profil auf derselben Aufgabensammlung.
- [ ] Gesonderte Messpläne (außerhalb von D5): Energie der Prüfung, ganzzahliges Training.
- [ ] Preis des Streitfalls im Journal für das vollständige Modell. Davor sind nötig: die Wahl der
      Blockchain, die Referenzmaschine des vollständigen Modells, die Bindung der Eingabe, der Länge des Rechenablaufs und des Rechenpfads.

Fertig, wenn: Jede Zahl gemessen ist, die Messbedingungen aufgeschrieben sind und ein zweiter
Teilnehmer die Messung wiederholt hat. Die Übereinstimmung der Bits bezieht sich nur auf die
geprüften Konfigurationen.

### Phase 6. Zusammenführung und Abnahme

- [ ] Die Entscheidung D4 über den unveränderlichen Kern — vor der abschließenden Prüfung auf
      Mehrheitsübernahme.
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
