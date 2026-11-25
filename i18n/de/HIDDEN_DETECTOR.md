<!-- translation of docs/HIDDEN_DETECTOR.md, source sha256: a695d12d2972002373f749a618c390c3e937e344afd1e816d8c46319fe1127cb -->

# Der verborgene und sich verändernde Detektor: Was die Geheimhaltung der Regeln bringt

[English](../../docs/HIDDEN_DETECTOR.en.md) · [中文](../zh/HIDDEN_DETECTOR.md) · [Español](../es/HIDDEN_DETECTOR.md) · [Français](../fr/HIDDEN_DETECTOR.md) · **Deutsch** · [Italiano](../it/HIDDEN_DETECTOR.md) · [Русский](../../docs/HIDDEN_DETECTOR.md) · [Português](../pt/HIDDEN_DETECTOR.md) · [العربية](../ar/HIDDEN_DETECTOR.md)

Stand vom 25. November 2026. Ergebnis des sechsten Modellrats.

## 1. Frage und kurzes Fazit

Der Eigentümer des Projekts fragte wörtlich:

> „Bei offenen Regeln (D4) kennt der Betrüger den Detektor und fälscht genau dort, wo dieser
> ruhig ist. Und was, wenn man den Detektor verbirgt? Zum Beispiel erzeugt das Netz zu zufälligen
> Zeiten auf zufällige Weise neue Regeln für die Ehrlichkeitsprüfung, und die Agenten prüfen nach
> ihnen. Angesichts der verteilten und offenen Architektur des Netzes SkyNet darf niemand die
> Prüfregeln kennen, und sie müssen verschlüsselt werden, der Chiffrierschlüssel muss wechseln.
> Denken Sie als Modellrat in diese Richtung nach. Früher habe ich die Frage der Nutzung einer
> Blockchain aufgeworfen — gibt es eine Variante, einen dynamischen Detektor auf Basis einer
> Blockchain zu bauen? Gibt es außer der Blockchain vielleicht noch andere Technologien oder
> Algorithmen?“

**Status des Dokuments.** Dies ist eine Überlegung und eine Berechnung, keine Messung. Ein Netz gab es beim Lauf des Rats nicht, Experimente wurden nicht durchgeführt; wissenschaftliche Arbeiten sind aus dem Gedächtnis genannt und nicht abgeglichen. Messungen stammen nur aus den Ergebnissen des Experiments D5 vom 25. November ([EXPERIMENT_D5](EXPERIMENT_D5.md), Abschnitt 7) und aus der vorangegangenen Zusammenfassung [STRATEGY_SEARCH](STRATEGY_SEARCH.md). Angenommene Entscheidungen des Projekts bleiben nur D1–D25 ([ROADMAP](ROADMAP.md)); alles, was unten als „Empfehlung“ bezeichnet wird, muss der Eigentümer ausdrücklich annehmen oder verwerfen. Kennzeichnungen: [gemessen] — in D5 gemessen; [Berechnung] — folgt aus einer Formel mit genannten Parametern; [Annahme] — der Wert wurde für die Schätzung genommen und nicht gemessen.

Bezeichnungen, die unten vorkommen: `R` — Bezahlung einer Aufgabe; `H_lock` — noch nicht ausgereifter Betrag des Ausführenden, der bei nachgewiesener Fälschung verbrennt; `c_f` — Kosten der Fälschung; `p` — Wahrscheinlichkeit der vollständigen Prüfung einer Aufgabe; `ρ` — Zeit der Prüfung einer fertigen Antwort in einem Durchlauf, geteilt durch die Zeit der Generierung; `γ` — um wie viel Mal langsamer das exakte ganzzahlige Profil als die gewöhnliche Generierung von llama.cpp Q8_0 ist; `q` — Abspracheanteil; `n_w` — Zahl der Aufgaben des Schlüssels je Ausreifungsfenster.

**Kurzes Fazit.**

1. **Ein verborgener Detektor bringt nicht mehr als eine offene Prüfung mit geheimer Zufälligkeit desselben Preises.** Wenn der Betrüger weiß, nach welchem Gesetz die Regeln gewählt werden (und nach D4 ist der Code des Agenten offen, also weiß er es), so ist die Wahrscheinlichkeit, irgendeine seiner Fälschungen bei einer verborgenen Regel zu fangen, gleich der Fangwahrscheinlichkeit bei einem offenen Programm „nach der Fixierung der Antwort eine Münze werfen und die gefallene Regel anwenden“. Das haben alle elf Arbeiten unabhängig erhalten, alle vier Kritiker haben es bestätigt. Die Verborgenheit erlaubt es also nicht, die Prüfhäufigkeit unter die frühere Schwelle `R/(R + H_lock)` zu senken.
2. **Eine Regel, die länger als eine Aufgabe lebt, ist schlechter als eine frische Münze.** Der Betrüger lernt aus seinen Ausgängen („gefangen / nicht gefangen“), probiert den Detektor mit kostenlosen neuen Schlüsseln aus und erfährt die Regel über jeden Mitverschworenen, dem man sie zur Anwendung gegeben hat. Selbst ohne jede Leckage ist eine für die Epoche gemeinsame Regel gefährlicher: im Beispiel von ChatGPT ergibt eine Welle von zehn Fälschungen `+8,1R` gegen `−2,38R` bei unabhängigen Münzen [Berechnung]. „Die Regeln zu zufälligen Zeiten wechseln“ ist daher schlechter, als die Wahl bei jeder Aufgabe zu wechseln.
3. **Genau eine Form der Verborgenheit ist nützlich:** das Geheimnis der zufälligen Wahl *bevor* der Ausführende die Antwort unwiderruflich fixiert hat, und das Geheimnis der *Rolle* — ob dieser Zahler prüft und wer als Prüfer bestimmt ist. Die Regeln, die Familie der Prüfungen und das Wahlgesetz bleiben offen. Diese Form gibt es bereits in der Strategie des vorigen Rats („die geheime Münze des Zahlers“).
4. **Was aus Blockchain und Kryptografie zu übernehmen ist.** Die Blockchain ist ein Journal von Fixierungen, der Ordnung, der Offenlegungen und des Verbrennens von Beträgen; Geheimnisse gibt es in ihr nicht und kann es nicht geben. Ein externer Schwellen-Leuchtturm der Zufälligkeit und die VDF-Verzögerung vom finalen Block — Quellen der Zufälligkeit für gemeinsame Stichproben nach D20 (Audit des Trainings, Examen, Bestimmung der Prüfer), mit einem Hash vermischt. VRF und eine Verpflichtung zur Salz vor der Fixierung — dort, wo der Ausgang der Münze fremdes Geld betrifft. „Ein dynamischer Detektor auf der Blockchain“ in der richtigen Form ist ein **offener Regelgenerator im Kern plus frische Zufälligkeit nach der Fixierung**, und nicht verschlüsselte Regeln.
5. **Was als Grundlage der Garantie zu verwerfen ist.** Die Schwellenspeicherung geheimer Regeln bei Teilnehmern (wird durch Absprache aufgedeckt oder blockiert, bei `q = 1` gibt es keinen Schutz — Verletzung von D7), vertrauenswürdige Ausführungsumgebungen TEE (Vertrauen in den Hersteller, auf den Karten der Erfahrung D5 gibt es sie nicht), homomorphe Verschlüsselung FHE (nach Einschätzung der Kritiker 19 Stunden bis 15 Tage Berechnung für eine Antwort), Mehrparteienberechnungen MPC (Hunderte Megabyte und mehr Verkehr pro Token und wieder die Abhängigkeit von `q`), ununterscheidbare Obfuskation iO (nicht praktikabel und lässt dem Betrüger trotzdem einen „Probelauf“), funktionale Verschlüsselung und PIR (lösen andere Aufgaben). Fallen, geheime Schwellen und Statistik sind nur als Signal für eine *zusätzliche* Prüfung zulässig.
6. **Ein Fehler in den früheren Tabellen wurde gefunden.** In STRATEGY_SEARCH 5.3 und in den meisten Arbeiten dieses Rats enthält die Zelle „fauler Zahler, der Ausführende unterscheidet ihn“ × „Neuling“ eine 0. Richtig ist **bis `+R`**: die Regel „den Neuling prüft man immer“ vollstreckt das Programm des Zahlers, und ein fauler Zahler vollstreckt es nicht. Schlimmer noch, neue Schlüssel erlauben es, kostenlos herauszufinden, welcher Zahler faul ist. Davor schützt nur die Unverknüpfbarkeit der Zahler zwischen Anfragen, und die muss erst noch gebaut werden.
7. **Neue Entscheidungen über die Garantie schlägt der Rat nicht vor.** Vorgeschlagen werden eine Präzisierung von D4 („der Kern nimmt künftige Zufälligkeit an, aber kein langlebiges Geheimnis“) und eine Präzisierung von D20 („die Quellen werden mit einem Hash vermischt, nicht durch Auswahl; der Leuchtturm — für gemeinsame Entscheidungen, nicht für das Geld des Zahlers“). Der Preis der Prüfung ändert sich durch die Verborgenheit nicht: der Hauptposten bleibt die Verlangsamung des exakten Profils `γ` (+50…+82% gegenüber Q8_0 bei Paket 1 [gemessen γ, Berechnung]), und nicht die Prüfung selbst.

---

## 2. Warum die Geheimhaltung der Regeln nicht hilft: Aussagen und Gegenbeispiele

### 2.1. Eine verborgene Regel ist gleich einer offenen Regel mit geheimer Münze

**Modell.** Der Verteidiger wählt die Prüfregel `r` aus der Verteilung `D`. Die Regel `r` fängt die Fälschung `x` mit der Wahrscheinlichkeit `π_r(x)`. Der Betrüger kennt die Verteilung `D` (nach D4 ist der Regelgenerator Teil des offenen Kerns), aber kennt das gefallene `r` nicht und wählt die Fälschung, bevor `r` gefallen ist.

**Aussage 1 (Äquivalenz).** Die Wahrscheinlichkeit, die Fälschung `x` zu fangen, ist gleich `π̄(x) = E_{r~D}[π_r(x)]`, der mittlere Preis der Prüfung ist gleich dem mittleren Preis der Regeln. Das offene Programm „nach der unwiderruflichen Fixierung der Antwort eine frische Zufälligkeit nehmen, `r` nach dem Gesetz `D` wählen und es anwenden“ ergibt für **jede** Fälschung dieselbe Fangwahrscheinlichkeit und denselben Preis. Die Verborgenheit der Implementierung fügt der Verteidigung also null hinzu.

Der Beweis ist eine Mittelung über `r`: die Ausgänge zweier Experimente stimmen für jeden Wert der Zufälligkeit überein. Ihn haben gpt1, gpt2, ds1, ds2, claude1, claude2, mm1–mm5 unabhängig geführt; die Kritiker ChatGPT, DeepSeek, Claude und MiniMax haben ihn bestätigt. Das ist dasselbe Ergebnis wie die Schranke des vorigen Rats `E_F[π] − E_P[π] ≤ TV(F, P)` ([STRATEGY_SEARCH](STRATEGY_SEARCH.md), Abschnitt 2.1): die Größe `π̄` ist eine gewöhnliche Funktion der Beobachtungen mit Werten von 0 bis 1, und das Geheimnis ändert sie nicht.

**Aussage 2 (Kenntnisse über das Geheimnis schaden dem Verteidiger nur).** Wenn der Betrüger vor der Fälschung irgendein Signal `Z` über die gefallene Regel erhält — aus einem früheren Streit, einer Probe, über einen Schlüsselanteil, aus einer Leckage des Enklaves —, wird sein bestes Ergebnis nicht schlechter: `E_Z[min_x E[π_r(x) | Z]] ≤ min_x π̄(x)`. Er kann das Signal immer ignorieren (claude1, claude2; von den Kritikern bestätigt).

Der Kritiker ChatGPT präzisierte die Grenze dieser Aussage: die Ungleichung ist nicht streng. Wenn alle Regeln dieselbe „für den Verteidiger schlechteste“ Fälschung haben, kann die Offenlegung der Regel nichts ändern. Die Formulierung von claude1 „jede Leckage verschlechtert streng“ ist daher falsch; richtig ist „verschlechtert nie“.

**Wodurch sich das von der Randomisierung unterscheidet.** Mehrere Arbeiten (ds1, ds2, mm2) haben die Folge als „ein verborgener Detektor ist gleich der Prüfung der ganzen Antwort mit der Wahrscheinlichkeit `p`“ notiert. Das ist ungenau. Das Äquivalent des verborgenen Detektors ist eine *Mischung derselben Regeln*. Eine Mischung teilweiser Prüfungen ist manchmal stärker als eine vollständige Prüfung desselben Preises, aber den Gewinn bringt die Randomisierung, nicht das Geheimnis, und er bleibt bei einem offenen Algorithmus erhalten:

- **Gegenbeispiel von gpt1.** Das Ergebnis hat drei unabhängig prüfbare Teile eines Preises, und nach dem Aufbau der Aufgabe verdirbt jede zulässige Fälschung mindestens zwei. Die Prüfung eines zufälligen Teils für ein Drittel des vollen Preises fängt nicht weniger als 2/3 der Fälschungen; eine vollständige Neuberechnung mit der Wahrscheinlichkeit 1/3 — nur 1/3.
- **Variante von gpt2.** Drei Tests zu je der Hälfte des Preises einer vollständigen Neuberechnung, jeder fängt zwei Fehlerklassen von drei: die Mischung fängt 2/3, die vollständige Neuberechnung der Hälfte der Aufgaben — 1/2. Fügt man eine vierte Klasse hinzu, die kein Test fängt, fällt die Garantie der Mischung auf 0.

Für Qwen ist eine solche Abdeckung der Fehlerklassen nicht bewiesen: eine falsche Position der Antwort ist bereits eine Fälschung, und für sie fängt jede teilweise Prüfung nicht mehr als ihren Anteil. Der praktische Gewinn aus der Mischung ist daher derzeit null (Kritiker Claude und ChatGPT). Die Aussage von mm2 „die Mischung ist immer teurer als der entscheidende Typ“ ist in allgemeiner Form falsch; in ihrer Formel steht außerdem ein überflüssiger Faktor (die Zahlen 0,2111 / 0,22 / 0,2333 sind nach der richtigen Formel gerechnet, aufgeschrieben ist die falsche — Kritiker Claude und DeepSeek).

**Wo das Geheimnis nicht auf eine Münze zurückgeführt wird.** Das ist eine private Marke des Verteidigers, die mit der richtigen Antwort verbunden ist: der Referenzwert einer Falle, den nur der Zahler kennt (gpt1, gpt2). Man kann sie nicht durch ein zufälliges Bit ersetzen. Aber wie in Abschnitt 3 gezeigt wird, kostet sie nicht weniger als eine Generierung und macht die Prüfung daher nicht billiger.

**Gegenüber einer „fixierten“ Regel ist die verborgene tatsächlich besser.** claude1 führt ein Beispiel an: wenn die offene Regel immer die Positionen 1–8 ansieht, wird eine Fälschung an Position 9 nie gefangen. Denselben Gewinn bringt aber die offene Regel „nach der Fixierung 8 Positionen gleichmäßig wählen“ (mm3, Theorem 2: eine frische Position fängt `e/N` der Fälschungen, wobei `e` die Zahl der verdorbenen Positionen von `N` ist, unabhängig davon, ob der Betrüger die Regel kennt). Der Kritiker MiniMax nannte das den Hauptfehler der Runde: viele Arbeiten verglichen den verborgenen Detektor mit einer fixierten offenen Regel und schrieben dem Geheimnis einen Gewinn zu, der der Zufälligkeit gehört.

### 2.2. Das Lernen des Betrügers aus den Ausgängen und Proben mit neuen Schlüsseln

Ein Geheimnis, das mehr als einmal verwendet wird, wird erlernt. Dafür muss der Gegner die Regel nicht vollständig kennen — es genügt, eine sichere Stelle zu finden.

- **Zwei Positionen von zehn (claude1).** Die verborgene Regel prüft 2 Positionen von 10, die Fangwahrscheinlichkeit einer Ein-Positionen-Fälschung ist 1/5. Nachdem ein Streit eine prüfbare Position offengelegt hat, fällt die Fangwahrscheinlichkeit auf 1/9, nach der Offenlegung der zweiten — auf 0. Wenn die Regel schon durch den ersten Streit offengelegt wird, ist die erwartete Zahl der gefangenen von 100 Fälschungen gleich `1 − 0,8¹⁰⁰ = 0,9999999998`, also praktisch eine, während eine frische Münze im Mittel 20 gefangen hätte [Berechnung, von den Kritikern bestätigt]. Der Kritiker ChatGPT bemerkte, dass dies für eine konkrete Reihenfolge der Proben und eine vollständige Offenlegung bei der ersten Fangung gilt; im allgemeinen Fall legt ein Streit mindestens die geprüfte Position offen, aber nicht unbedingt die ganze Menge.
- **Acht Positionen von tausend (ds2).** Bei einer verborgenen festen Teilmenge von 8 Positionen aus 1000 geht die erste Ein-Positionen-Fälschung mit der Wahrscheinlichkeit 0,992 durch, ebenso wie bei einer öffentlichen frischen Auswahl desselben Anteils. Der Unterschied ist, dass bei einer verborgenen festen Teilmenge die durchgegangene Position für immer sicher bleibt. Die Zahl von ds2 „≈ 2718 Versuche zur Wiederherstellung der ganzen Menge“ ist nach einem falschen Modell (mit Zurücklegen) gerechnet; ohne Zurücklegen braucht man etwa 890 Versuche, und vor allem genügt dem Gegner eine sichere Position (Kritiker Claude, DeepSeek und ChatGPT).
- **Epochenregel und ausgereifter Schlüssel (claude2).** Eine deterministische Regel für eine Epoche von 100 Aufgaben, `p = 1%`, `H_lock = 99R`: ein Betrüger, der durch eine Probe einen sicheren Bereich gefunden hat, erhält etwa `0,99·100R − 0,01·99R = 98,01R` je Epoche gegen `≤ 0` bei einer frischen Münze [Berechnung, bestätigt].
- **Gemeinsames Bit der Epoche (gpt2).** `R = 1`, gesperrt sind `9R`, zehn Fälschungen einer Welle, die erste nachgewiesene Fälschung annulliert die Welle und die `9R`, die Prüfhäufigkeit einer einzelnen Anmeldung ist 1/10. Wenn ein verborgenes Bit der Epoche „alles prüfen“ oder „alles durchlassen“ entscheidet, ist der Gewinn der Welle `0,9·10R − 0,1·9R = +8,1R` — eine Verletzung von D1 **vor jeder Leckage**. Mit zehn unabhängigen Münzen bei denselben Kosten `(0,9¹⁰·10 − (1 − 0,9¹⁰)·9)R = −2,3751096381R` [Berechnung, von allen Kritikern wiederholt]. Analog beim Kritiker ChatGPT: bei `R = 1`, `H = 4`, `p = 0,2` und zehn Fälschungen ergibt eine gemeinsame Münze für die ganze Welle `+7,2R`, selbst bei Annullierung der ganzen Welle.

**Sybil-Schlüssel.** Neue Schlüssel sind kostenlos. Ein Schlüssel mit leerem Konto verliert bei einer Fangung nichts, daher kosten Proben des Detektors mit ihm fast nichts. Der Schutz hält nur dort, wo der Neuling tatsächlich immer geprüft wird (`p = 1`). Der Kritiker ChatGPT räumte ein, dass aus der Kostenlosigkeit der Schlüssel nicht folgt, dass die Anpassung augenblicklich ist: jeder informative Ausgang verlangt eine bezahlte Aufgabe und Zeit, und bei verrauschter Rückmeldung — mehrere Versuche. Die Schlussfolgerung ändert sich dadurch nicht: ein lange lebendes Geheimnis wird früher oder später erlernt, und eine frische Münze lehrt nichts, weil der nächste Wurf von den früheren unabhängig ist.

**Fazit.** Die Wahl muss für jede Aufgabe neu getroffen werden, nicht nach einem Zeitplan. Genau deshalb ist „das Netz erzeugt zu zufälligen Zeiten neue Regeln“ schlechter als „eine frische Münze bei jeder Aufgabe“, die sich selbst und kostenlos neu erzeugt (ds1).

### 2.3. Die Regel leckt durch diejenigen, die sie anwenden

„Eine Regel, die niemand kennt und alle ausführen“ ist in einem offenen Netz unmöglich. Ein Knoten, der die Regel anwendet, kennt sie im Moment der Anwendung: Code und Schlüssel liegen im Speicher der Maschine, und der Eigentümer der Maschine kann sie nach dem Gegnermodell lesen ([THREAT_MODEL](THREAT_MODEL.md), Abschnitt 1.3). claude1 formulierte die vollständige Liste der Träger des Geheimnisses:

1. die Regel gibt es noch nicht — sie wird aus künftiger Zufälligkeit abgeleitet (Leuchtturm, VDF);
2. die Regel wird in Hardware ausgeführt, die der Eigentümer nicht öffnen kann (TEE) — dann geht das Vertrauen auf den Hersteller über, und R4 nennt das eine Annahme;
3. die Regel ist so verschlüsselt, dass man sie ausführen kann, ohne sie zu kennen (iO, FHE, MPC) — siehe Abschnitt 3;
4. die Regel kennt ein Komitee von Teilnehmern — dann legt eine Absprache sie offen oder blockiert sie.

Der Kritiker ChatGPT ergänzte die Liste: MPC über Anteile und die Berechnung eines offenen Verfahrens über einem verschlüsselten Parameter erlauben es dem Betreiber, das Ergebnis gar nicht zu sehen. Das ändert die Schlussfolgerung nicht, weil solche Verfahren wieder auf einem Anteil ehrlicher Teilnehmer oder auf dem Schlüsselhalter beruhen.

**Ein Schwellenschlüssel schützt die Speicherung, aber nicht die Anwendung** (claude2, das stärkste Argument des Rats gegen eine geheime Regel bei einem Komitee). Selbst wenn der Schlüssel zuverlässig geteilt ist, führt ein konkreter Knoten die entschlüsselte Epochenregel aus. Bei `m` unabhängigen Anwendungen ist die Wahrscheinlichkeit, dass mindestens ein anwendender Knoten zur Koalition gehört, gleich `1 − (1 − q)^m`: für 10 Anwendungen sind das 0,65 / 0,97 / 0,999 bei `q` = 0,1 / 0,3 / 0,5. Die Wahrscheinlichkeit, dass die Epochenregel der Koalition über 100 Anwendungen *nicht* bekannt wird, ist bei `q = 0,1` gleich `0,9¹⁰⁰ ≈ 2,7·10⁻⁵` [Berechnung, von den Kritikern bestätigt].

**Vor dem Prüfer zu verbergen ist sinnlos** (claude2, Folgerung 4.2). Ein mitverschworener Prüfer kann gar nicht prüfen und „sauber“ sagen; ein ehrlicher hat nichts zu verbergen. Der Einzige, vor dem die Entscheidung verborgen werden muss, ist der Ausführende vor der Fixierung der Antwort. claude2 fügte Theorem 4 hinzu: wenn der Prüfer nicht wissen soll, welche Positionen er prüft, muss er alle Positionen „berühren“, und die Ersparnis aus der Auswahl verschwindet. Der Kritiker ChatGPT bemerkte, dass diese Schlussfolgerung in einem speziellen Modell gilt (ein Server, keine Vorverarbeitung) und sich bei anderen Modellen des Speicherzugriffs ändern kann; der Kritiker Claude — dass das Theorem eine Variante widerlegt, die niemand verteidigt hat.

**Ein verborgenes Geheimnis ergibt kein prüfbares Urteil.** mm2 bemerkte, dass die Aussage „es gibt eine geheime Regel, die das Ergebnis angenommen hat“ für die Regel „alles annehmen“ immer wahr ist. Die Kritiker Claude und ChatGPT präzisierten: ein Beweis mit null Offenlegung kann die inhaltliche Aussage „die Regel wurde aus einer vor der Fixierung aufgezeichneten Verpflichtung abgeleitet, und sie hat das Ergebnis angenommen“ bezeugen. Aber ein solcher Beweis verlangt eine offene Relation im Kern, das heißt, er führt uns zum offenen Generator zurück, und sein Preis für Qwen ist nicht berechnet.

### 2.4. Der Schwellenschlüssel bei einem Abspracheanteil q

Der Schlüssel sei zwischen `n` Haltern geteilt, zur Entschlüsselung seien `t` Anteile nötig. Dann erfährt die Koalition das Geheimnis vorzeitig, wenn sie `t` und mehr Plätze hat, und kann die Arbeit stoppen, wenn sie `n − t + 1` und mehr Plätze hat. Wenn die Plätze unabhängig gewählt sind und jeder mit der Wahrscheinlichkeit `q` der Koalition gehört, sind das binomiale Schwänze. Die Tabelle des Kritikers Claude, abgeglichen von den Kritikern ChatGPT und DeepSeek; in jeder Zelle „Offenlegung / Stopp“ [Berechnung]:

| `n`, `t` | `q = 0,1` | `q = 0,3` | `q = 0,5` | `q = 1` |
|---|---|---|---|---|
| 5, 3 | 0,856% / 0,856% | 16,3% / 16,3% | 50% / 50% | 1 / 1 |
| 7, 5 | 0,0177% / 2,57% | 2,88% / 35,3% | 22,7% / 77,3% | 1 / 1 |
| 16, 11 | 2,7·10⁻⁸ / 0,33% | 0,157% / 34,0% | 10,5% / 89,5% | 1 / 1 |
| 30, 16 | 3,66·10⁻⁹ / 3,56·10⁻⁸ | 0,637% / 1,69% | 42,8% / 57,2% | 1 / 1 |
| 64, 43 | 4,75·10⁻²⁸ / 1,20·10⁻⁷ | 9,43·10⁻¹⁰ / 26,2% | 0,41% / 99,6% | 1 / 1 |
| 100, 51 | 6,3·10⁻²⁵ / 5,8·10⁻²⁴ | 9,0·10⁻⁶ / 2,2·10⁻⁵ | 46,0% / 54,0% | 1 / 1 |
| 100, 67 | 9,6·10⁻⁴³ / 7,0·10⁻¹¹ | 2,7·10⁻¹⁴ / 22,1% | 0,044% / ≈1 | 1 / 1 |

Was daraus folgt:

1. **Keine Zeile ergibt einen Schutz bei `q = 1`.** D7 verlangt eine Prüfung, die nicht vom Abspracheanteil abhängt, daher erfüllt das Geheimnis bei einem Komitee D7 bei keinem Schwellenwert.
2. **Ein hoher Schwellenwert hält das Geheimnis gut, ist aber leicht zu blockieren.** Zeile 16/11: bei `q = 0,3` beträgt die Offenlegung 0,157%, dafür stoppt die Koalition mit der Wahrscheinlichkeit 34% die Ausgabe, indem sie einfach keine Anteile schickt.
3. **Epochen addieren sich.** Bei einer Offenlegungswahrscheinlichkeit von 0,856% je Epoche (3 von 5, `q = 0,1`) geschieht über 30 unabhängige Epochen mindestens eine Offenlegung mit der Wahrscheinlichkeit 22,7% (gpt1) [Berechnung].
4. **Die Tabelle ist optimistisch.** Die unabhängige Wahl der Plätze ist eine Annahme. Sie bricht, wenn die Halter nach Gewicht ausgewählt werden und das Gewicht durch selbst bezahlte geprüfte Anfragen gesammelt werden kann; wenn bei einem seltenen Modell der Abspracheanteil über dem Durchschnitt liegt; bei Bestechung nach der Bestimmung; bei gemeinsamen Eigentümern der Plätze. In [THREAT_MODEL](THREAT_MODEL.md) (Abschnitt 1.7) gibt es bereits ein Beispiel: 42,1% des Gesamtgewichts ergeben `q_eff = 88,9%` unter den zur Aufgabe Zugelassenen (darauf hat der Kritiker MiniMax aufmerksam gemacht).
5. **Fehler in den Arbeiten.** claude1 schrieb die Bedingung „`q < min(t/n, 1 − t/n) ≤ 1/2`“ als Theorem auf; das ist kein Theorem: bei `t = n` hält das Geheimnis, solange im Komitee auch nur ein Ehrlicher ist, und die Blockierung kann einen sicheren Ersatzausgang haben (Kritiker Claude). mm4 verwechselte die Schwellen der Offenlegung und der Blockierung; mm2 meinte fälschlich, die Schwellenentschlüsselung verlange alle Halter; ds1 schrieb widersprüchlich „sie stellen `t + 1` Anteile wieder her“. Die Aussage von mm3 „bei `q ≥ t` fälscht die Koalition die Regel“ gilt nur dort, wo das Urteil eine Schwellensignatur ohne prüfbaren Inhalt ist; wenn ein vorher fixierter Chiffretext entschlüsselt wird, erfährt die Koalition die Regel, kann sie aber nicht ersetzen.

**Wie die Anforderungen R2/R3 zu lesen sind.** ds1, mm1, mm3 und mm4 schrieben, die Anforderung der Wiederherstellung nach einem vollständigen Stopp „verbiete grundsätzlich“ gemeinsame Geheimnisse. Die Kritiker Claude und ChatGPT halten das für übertrieben: die Anteile der Halter können einen Stopp auf ihren Festplatten überleben; R2/R3 verbieten die Abhängigkeit von der Adresse eines lebenden Koordinators, nicht von der Rückkehr eines Teils der Teilnehmer. Die genaue Grenze (claude2): ein Geheimnis, ohne das die Grundlage einer **vergangenen** Entscheidung nicht geprüft werden kann, ist mit der Prüfbarkeit nach einem Neustart unvereinbar. Also muss jede geheime Regel nicht später als die Auszahlung offengelegt werden, und ihr Geheimnis lebt nicht länger als das Geheimnis der Münze. Die Schlussfolgerung über die Untauglichkeit geheimer Regeln ist dieselbe, die Begründung bei ds1, mm1, mm3 war überzogen.

### 2.5. Das Kerckhoffs-Prinzip, Sicherheitsspiele, Banken und CAPTCHA

**Kerckhoffs.** Das Kerckhoffs-Prinzip (aus dem Gedächtnis) erlaubt einen offenen Algorithmus mit einem geschlossenen Schlüssel. In diesem Spiel muss der geschlossene „Schlüssel“ die bis zur Fixierung unvorhersagbare Realisierung des Aufrufs der Prüfung sein, nicht der Algorithmus. Der Wechsel eines langlebigen Schlüssels ist nach einer Kompromittierung nützlich, löscht aber nicht, was der Betrüger bereits über die Funktion erfahren hat, die dieser Schlüssel entschlüsselte (Kritiker ChatGPT).

**Sicherheitsspiele.** Ein Verteidiger mit begrenztem Budget randomisiert — das ist die Klassik der Stackelberg-Spiele und der Inspektionsspiele (aus dem Gedächtnis). Dort gilt die Verteilung des Verteidigers aber gewöhnlich als dem Angreifer bekannt, und der ganze Nutzen kommt von der Zufälligkeit, nicht vom Geheimnis der Verteilung. Der Kritiker DeepSeek korrigierte mm3: die Unkenntnis der Verteilung durch den Betrüger kann seinen Gewinn nicht über die beste Antwort auf die wahre Verteilung heben, und nach D4 muss er diese Verteilung ohnehin kennen. Für eine Mischung verschiedener Tests schrieb gpt1 ein Problem der linearen Programmierung auf: die über die Fälschungen kleinste Fangwahrscheinlichkeit `min_f Σ w_j D(j,f)` bei einem Budget `Σ w_j c_j ≤ B` maximieren.

**„Bewegtes Ziel“.** Die Idee der Moving Target Defense (aus dem Gedächtnis) ist wertvoll, wenn der Beobachter Zeit braucht, um sich an eine neue Konfiguration anzupassen. In SkyNet ist das beste „bewegte Ziel“ eine neue Konfiguration bei jeder Aufgabe, also eine frische Münze (mm4, mm5).

**Warum Verborgenheit in der Bank und bei CAPTCHA funktioniert, in SkyNet aber nicht.** Die Arbeiten und Kritiker einigten sich auf folgende Unterschiede (claude2, ds2, mm3, mm5, Kritiker ChatGPT):

| | Bank-Antifraud, CAPTCHA | SkyNet |
|---|---|---|
| Wer hält das Prüfmodell | Eine Organisation auf ihrem Server | Kein Zentrum; der Code des Agenten ist offen (D4) |
| Rückmeldung an den Angreifer | Oft nicht attribuierbar, mit Verzögerung | Der Ausgang ist sofort sichtbar und an die Aufgabe gebunden |
| Preis eines Versuchs | Kontoeröffnung, Dokumente, Begrenzung der Wiederholungen | Der Schlüssel ist kostenlos (Sybil) |
| Sanktionen | Nicht monetär: Sperrung, Gericht, externe Informationen | Nur das Verbrennen des nicht ausgereiften Betrags (R5) |
| Ziel der Verteidigung | Verluste im Mittel senken | Der erwartete Gewinn jeder Koalition ist nicht höher als null (D1) |
| Prüfbarkeit der Entscheidung | Von Dritten nicht verlangt | Jeder Knoten prüft die Grundlage selbst |

Die Bank hat private Marken der Ausgänge, den Preis einer Kontoeröffnung und eine Begrenzung der Wiederholungen; CAPTCHA hat einen externen Prüfer. Das sind zusätzliche Informationen und Kosten des Angreifers. Durch den Wechsel einer verschlüsselten Datei mit Regeln entstehen sie in SkyNet nicht. ds2 und mm5 nannten das Wesen genau: dort, wo Verborgenheit funktioniert, ist das Geheimnis faktisch einmalig, das heißt, es ist dieselbe Münze.

**Die Hauptprämisse der Frage in SkyNet ist teilweise falsch** (mm3). Die Hauptprüfung des Projekts ist der bitweise Vergleich mit einer exakten Neuberechnung. Sie hat keine „Stelle, wo der Detektor ruhig ist“: eine ehrliche Antwort stimmt überall überein, eine Fälschung weicht dort ab, wo sie gefälscht ist. „Stille Zonen“ gibt es nur bei statistischen Detektoren und bei teilweisen Prüfungen. Statistische Detektoren gegen die Hauptfälschung (gewöhnliche Generierung Q8_0 statt des exakten Profils) sind fast nutzlos, und für teilweise Prüfungen hilft eine frische Wahl nach der Fixierung.

---

## 3. Analyse der Technologien

Die Preise unten sind [Berechnung] nach ausdrücklich genannten Parametern und [Annahme] über die Geschwindigkeit der Kryptografie aus dem Gedächtnis; keine dieser Technologien wurde im Projekt gemessen. Basismessungen: `ρ = 0,10–0,40` bei Paket 1 und `0,26–0,64` bei Paket 8; `γ = 1,5–1,8` bei Paket 1 und `2,5–2,8` bei Paket 8 [gemessen, O3 und O4]. Modell D5: 32 Blöcke, verborgene Größe 2560, MLP 9216, 24 Blöcke Gated DeltaNet mit Zustand `32×128×128`, Vokabular 248 320, etwa 4,2·10⁹ Multiplikationen-Additionen pro Token.

| Technologie | Was sie gibt | Was sie nicht gibt | Preis [Berechnung / Annahme] | Urteil |
|---|---|---|---|---|
| **Blockchain-Journal** | Ordnung, endgültige Fixierung der Antwort (D24, 2–4 KB Chiffretext), Verpflichtungen, Offenlegungen, einmalige Berechnung, Verbrennen | Geheimhaltung: alles im Block sehen alle. Unverschiebbare Zufälligkeit: der Produzent eines Blocks kann einen unpassenden Block zurückhalten (N13) | Pilotstreit: 93 Transaktionen, 5,8–6,3 Mio. Gas, bei 1 Gwei und 3000 $/ETH — 17,4–18,9 $, bei 20 Gwei — 348–378 $ (Kritiker ChatGPT nach THREAT_MODEL, N3) | **Als Journal übernehmen** |
| **Smart Contract als Detektor** | Automatische Berechnung nach einer bereits geprüften Grundlage | Weder Speicherung eines Geheimnisses noch Berechnung des Modells | Neuberechnung eines Tokens im Vertrag: `4,2·10⁹ × 3 gas ≈ 1,26·10¹⁰ gas` ≈ 37 800 $ pro Token bei 1 Gwei und 3000 $/ETH (ds1, bestätigt). Kritiker Claude: das sind etwa 420 Blöcke zu 30 Mio. Gas (Grenze aus dem Gedächtnis). Kritiker ChatGPT: eine einfache MUL-Operation kostet aus dem Gedächtnis 5 Gas, daher ist das ein Szenario und keine strenge untere Schranke | **Als Detektor verwerfen** |
| **Externer Schwellen-Leuchtturm** (Klasse drand, aus dem Gedächtnis) | Eine öffentliche Zufälligkeit, die niemand vorher kennt, wenn die Schwelle seines Komitees ehrlich ist | Geheimhaltung: die Runde wird für alle veröffentlicht. Eine Koalition innerhalb des Leuchtturm-Komitees erfährt die Runde früher oder kann sie nicht herausgeben | Hunderte Byte pro Runde pro Paket und das Warten auf eine Runde (aus dem Gedächtnis 30 s bei der Hauptkette und etwa 3 s bei der schnellen) | **Als eine der beiden Quellen von D20 übernehmen** für gemeinsame Stichproben |
| **VDF vom finalen Block** | Eine Verzögerung, in der der Produzent des Blocks keinen passenden Block rechtzeitig finden kann | Unabhängige Entropie: ein VDF vom selben Block ist keine zweite unabhängige Quelle (Kritiker ChatGPT) | Sequenzielle Arbeit des Rechners; die Prüfung ist schnell | **Als Ergänzung zum Leuchtturm übernehmen**, die Annahme über die Überlegenheit schneller Hardware aufschreiben |
| **Timelock-Verschlüsselung über den Leuchtturm** | Verzögerte Offenlegung gemeinsamer Referenzwerte, Aufgaben des Examens | Geheimhaltung länger als eine Runde; erbt die Schwelle des Leuchtturms | Wie beim Leuchtturm | **Nur für die verzögerte Offenlegung gemeinsamer Daten**; private Daten so nicht offenlegen |
| **Rätsel mit Zeitverriegelung** (Rivest–Shamir–Wagner, aus dem Gedächtnis) | Eine Verzögerung der Offenlegung | Der Ersteller kennt die Antwort sofort; die Münze ist einfacher | Sequenzielle Arbeit | **Verwerfen** |
| **VRF** | Einen eindeutigen und prüfbaren Wert für einen vorab registrierten Schlüssel und Eingang | Geheimhaltung vor dem Eigentümer des Schlüssels: er berechnet den Wert, wann er will. Die Prüfung des VRF-Beweises legt den Wert offen (Fehler von mm4). Die Tatsache einer Neuberechnung des VRF beweist sie nicht | Ein Aufruf und Hunderte Byte pro Antwort | **Übernehmen**: für die Bestimmung der Prüfer (gegen Bestechung nach der Bestimmung) und als Münze des Zahlers dort, wo der Ausgang fremde Auszahlungen betrifft; der Schlüssel wird vor der Bestellung, vor der Fixierung registriert |
| **Commit–reveal** | Die Bindung des Salzes an eine Bestellung vor der Fixierung der Antwort | Schutz vor dem „letzten Offenlegenden“, der schweigen kann | gpt2: 448 Byte pro Schema | **Eng übernehmen**: Verpflichtung vor der Fixierung, ohne das Recht, den Ausgang zu wählen |
| **Schwellenkryptografie** (Shamir, DKG, Schwellenentschlüsselung) | Speicherung eines Schlüssels ohne einen einzigen Halter | Unabhängigkeit von `q` (Abschnitt 2.4); Schutz bei der Anwendung der Regel (Abschnitt 2.3) | DKG bei `n = 7`, `t = 5`: `7·6·32 + 7·5·48 = 3024` Byte Nutzlast (gpt2), Schwellensignatur BLS — 288 Byte; ohne Replikation und Beschwerden | **Für geheime Regeln verwerfen**; ein interner Schwellen-Leuchtturm der Teilnehmer — nur als eine der Quellen, nicht als einzige |
| **TEE** (SGX, SEV, TDX, geschützte GPUs) | Die Ausführung von Code, der vor dem Eigentümer der Maschine verborgen ist, bei Vertrauen in den Hersteller | Unabhängigkeit vom Hersteller und seiner Attestierungskette; geschützte GPUs gibt es im Park D5 (RTX 2060, RTX 4070 Laptop, RX 580) nicht | Szenario des Kritikers ChatGPT: geschützte Prüfung 1,2 Mal länger als eine offene, `p = 0,1` — etwa 3,20% der Generierungszeit mit Laden der Gewichte; das Modell auf der CPU — etwa 50–100 ms pro Token gegen 15–50 ms auf der GPU (Kritiker Claude) [Annahme]. Kritiker MiniMax: der Eigentümer kann das Enklave als Orakel benutzen, das Geheimnis hängt an der Begrenzung der Zahl der Anfragen | **Nur als Privatsphäremodus nach Wahl des Nutzers**, nicht als Grundlage der Garantie |
| **FHE** | Berechnung über verschlüsselten Daten und, über ein universelles Schema, über einem verschlüsselten Programm | Prüfung der Korrektheit der Berechnung; das Ergebnis legt der Schlüsselhalter offen (wieder `q`). Das approximative Schema CKKS reproduziert die Bits des Profils v2 nicht | 1,4·10⁷–2,6·10⁷ Bootstraps pro Token, bei 10⁴–10⁵ Bootstraps pro Sekunde [Annahme] — 140–2600 s pro Token, von 19 Stunden bis 15 Tagen für eine Antwort von 500 Token; der Multiplikator gegenüber der offenen Prüfung `Φ ≈ 3·10³…2·10⁵` (claude2, Kritiker Claude, ChatGPT, MiniMax). Zuschlag `p·ρ·Φ` bei `n_w = 300`: von 2,1 bis 139 Generierungen pro Antwort | **Für die Prüfung verwerfen**; nur für Privatsphäre untersuchen |
| **MPC** | Berechnung ohne Zusammenführung des Geheimnisses an einem Ort | Unabhängigkeit von `q`: der Schutz hängt an einer ehrlichen Mehrheit oder an „mindestens einem Ehrlichen“ mit dem Recht, die Arbeit zu vereiteln; bei `q = 1` gibt es keinen Schutz | Um die *Wahl* der Prüfung zu verbergen, muss man alles verarbeiten — in `1/p` = 31 / 303 / 4329 Mal teurer als die Münze bei `n_w` = 30 / 300 / 4320 (Kritiker Claude). Die *Anfrage* verbergen: Kritiker Claude — von 151 MB pro Token der unteren Schranke bis 0,15–1 GB, 10–67 Minuten pro Antwort bei 1 Gbit/s; Kritiker ChatGPT — 448 MB pro Position, 224 GB pro 500 Positionen; Kritiker MiniMax — bis 180 TB pro Antwort (die Schätzungen weichen um Größenordnungen ab, siehe Abschnitt 7) | **Für die Prüfung verwerfen** |
| **iO** (ununterscheidbare Obfuskation) | In der Theorie — die Ausführung eines Programms ohne Offenlegung seines Aufbaus | Eine praktische Implementierung für ein Modell gibt es nicht; selbst ein ideales iO lässt dem Betrüger einen „Probelauf“ seiner Fälschung durch den Detektor | Nicht bewertet | **Verwerfen** |
| **Obfuskation von Punktfunktionen** | Die Prüfung „stimmt es mit dem Referenzwert überein“ ohne Offenlegung des Referenzwerts | Schutz bei einem kleinen Antwortraum: Ausprobieren; das ist dieselbe Falle | Hash | Nur als Teil einer Falle |
| **Funktionale Verschlüsselung** | Der Erhalt des Werts einer Funktion durch den Eigentümer eines funktionalen Schlüssels | Das Verbergen der Funktion vor dem Eigentümer des Schlüssels (nötig ist ein eigenes Schema); nötig ist ein Aussteller der Schlüssel | Nicht bewertet | **Für diese Aufgabe verwerfen** |
| **PIR, ORAM** | Das Verbergen des Leseindex vor dem Server | Das Verbergen der Regel; den Nachweis der Herkunft der Daten | Kritiker ChatGPT: bei einem Zwei-Server-PIR mit 10 000 Einträgen zu 32 Byte — ein Blick von etwa 320 KB pro Server und die Nichtabsprache der Server | **Für diese Aufgabe verwerfen** |
| **Fallen** (eine Anfrage mit vorher bekannter Antwort) | Neue Informationen: einen mit der Wahrheit korrelierten Referenzwert | Eine Verbilligung. Eine Falle derselben Stärke wie die Münze kostet die Arbeit des Ausführenden (≈ eine Generierung, bezahlt und niemandem nützlich) und den Referenzwert (eine Generierung, wenn er frisch ist). Die Wiederholung einer alten Anfrage erkennt die Koalition | Das Verhältnis des Preises der Falle zum Preis der Münze `≥ 1/((1 − σ)ρ)`, wobei `σ` die Wahrscheinlichkeit ist, die Falle zu erkennen: bei `ρ = 0,21` — 5,3 / 6,8 / 9,5 / ∞ Mal bei `σ = q` = 0,1 / 0,3 / 0,5 / 1; bei `ρ = 0,40` — 2,8 / 3,6 / 5,0 / ∞ (claude2). gpt2: einmalige Fallen für 1% der Arbeiten mit zwei Generierungen fügen 2,02% hinzu | **Nur „Signal nach oben“**, ohne Senkung der Häufigkeit und ohne die Markierung „geprüft“ |
| **Geheime statistische Tests und Schwellen** | Die Diagnose massiver Ausfälle und Implementierungsfehler | Eine Senkung der Häufigkeit: die Grenze `TV`; die Schwelle wird durch Proben erlernt | Wenig | **Nur „Signal nach oben“** |
| **Verborgener Prüfer, unverknüpfbare Zahler** | Gegen Bestechung nach der Bestimmung (VRF-Bestimmung) und gegen die Unterscheidung fauler Zahler (Einmalschlüssel des Zahlers, claude1) | Unabhängigkeit von `q` bei der Prüfung durch ein Komitee. Für eine unverknüpfbare Zahlung braucht man einen Aussteller oder einen anderen Mechanismus ohne Sonderrechte — nicht gebaut | Kilobyte und Sekunden (claude1), nicht vollständig bewertet | **VRF-Bestimmung übernehmen; unverknüpfbare Zahler untersuchen** |
| **ZK-Beweis der Berechnung** | Den einzigen Weg zu einem öffentlich prüfbaren Urteil über einen geschlossenen Zeugen | Nichts über die Geheimhaltung der Regeln; der Preis für Qwen ist nicht berechnet. Erfahrung des Piloten: die Ausführung der zkVM war 17 700 Mal langsamer, selbst ohne den Aufbau des Beweises | Nicht bewertet | **Separat untersuchen** |
| **„Moving target defense“** | Den Wert des Wechsels der Konfiguration, solange der Beobachter sich nicht angepasst hat | In SkyNet ist der beste Wechsel — bei jeder Aufgabe, das heißt eine frische Münze | Null über die Münze hinaus | Auf die frische Münze zurückführen |
| **Bank-Antifraud, CAPTCHA** | Funktionieren dank eines geschlossenen Servers, des Preises eines Versuchs, nicht monetärer Sanktionen und einmaliger Aufrufe | Nichts davon entsteht in SkyNet durch den Wechsel einer Datei mit Regeln (Abschnitt 2.5) | — | Nicht übertragen |

**Eine separate Entdeckung von claude1 (nicht über Geheimhaltung): die Freivalds-Prüfung.** Die Multiplikation einer Matrix mit einem Vektor anhand einer zufälligen Projektion lässt sich billiger prüfen als die Multiplikation selbst: das Verhältnis beträgt etwa 1740 pro Token und Block [Berechnung, vom Kritiker Claude bestätigt]. Aber der Kritiker ChatGPT bemerkte, dass das keine Beschleunigung der Antwort ist: man muss die Zwischenaktivierungen übertragen, die Nichtlinearitäten, die Rundungen des Profils v2 und die Frische des Vektors für jede Anfrage berücksichtigen. Die Schlussfolgerung von claude1 „der Verkehr der Aktivierungen macht das schlechter als ein vollständiger Durchlauf“ ist richtig. Man kann nicht das ganze Qwen anhand einer einzigen Multiplikation als geprüft erklären.

---

## 4. Empfohlene Strategie

### 4.1. Schritte

Dies ist die Strategie des vorigen Rats („Zahler als Inspektor“), präzisiert durch die Arbeiten und Kritiker dieses Rats. Kein Schritt verlangt geheime Regeln. Die Schritte 3, 4 und 9 hängen von noch nicht angenommenen Entscheidungen ab (Abschnitt 5).

1. **Offener Kern.** Der Generator der Prüfungsinstanz, die Familie zulässiger Prüfungen und das Wahlgesetz sind ein offener Teil des Kerns mit festgeschriebenem Fingerabdruck (D4). „Neue Regeln zu zufälligen Zeiten“ sind neue Werte der Zufälligkeit, nicht neue Algorithmen.
2. **Fixierung.** Der Ausführende rechnet im exakten Profil v2 und legt mit einem einzigen Eintrag samt Abnahme den Chiffretext der Antwort ins Journal (D24). Bis zu diesem Moment wird keine Wahl der Prüfung getroffen.
3. **Die geheime Münze des Zahlers.** Nach der unwiderruflichen Fixierung nimmt das Programm des Zahlers eine frische Zufälligkeit und entscheidet, ob die Antwort geprüft wird, mit der Wahrscheinlichkeit `p = max(p_nutzer, (R − c_f)/(R + H_lock))`; bei `c_f ≈ 0` ist das `R/(R + H_lock)`; bei `H_lock = 0` (Neuling) — immer. Für das Geld des Zahlers selbst ist der Leuchtturm nicht nötig.
4. **Eine prüfbare Münze dort, wo fremdes Geld von ihr abhängt.** Wenn der Ausgang der Münze eine fremde Auszahlung betrifft (Lotterie mit gemeinsamem Preis, Streitigkeiten dritter Knoten), muss die Münze prüfbar sein: eine VRF eines vor der Bestellung, vor der Fixierung registrierten Schlüssels oder eine Verpflichtung zum Salz, die vor der Fixierung veröffentlicht wurde (gpt2, claude2). Eine nach der Fixierung gemachte Verpflichtung ist sinnlos: der Zahler wählt den Ausgang, während er die Antwort schon sieht (Fehler von mm5 im Vorschlag D28).
5. **Der Schlossbetrag.** `H_lock` — nur der Betrag, der nach der Frist des Streits ausreift; die Prüffrist `δ` ist viel kleiner als das Ausreifungsfenster `W` (in aktiver Zeit, D12). Die erste nachgewiesene Fälschung verbrennt atomar den gesamten nicht ausgereiften Betrag des Schlüssels, einschließlich der Belohnungen derselben Welle; dem Geschädigten wird nicht mehr als seine Bezahlung zurückgegeben (Kandidat D26). Ohne Atomarität halten die Formeln eine Welle nicht aus: 10 parallele Fälschungen bei `R = 1`, `H = 4`, `p = 0,2` ergeben `+4,4295R` statt `−2,49676R` [Berechnung].
6. **Markierungen.** „Geprüft“ — nur eine bis zur Anzeige vollständig geprüfte Antwort; alles andere ist standardmäßig „nicht geprüft“. Ein ungeprüfter Trainingsschritt geht nicht in das ausgelieferte Modell ein (D6).
7. **Gemeinsame Stichproben nach D20.** Audit des Trainings, Examen, Lotterie mit gemeinsamem Preis und Bestimmung der Prüfer nehmen die Zufälligkeit aus nicht weniger als zwei unabhängigen Quellen (ein externer Schwellen-Leuchtturm und ein VDF vom finalen Block), mit einem Hash vermischt; die Runde ist vor der Fixierung bestimmt und tritt nach ihr ein. Die bestimmten Knoten erfahren die Wahl über eine VRF.
8. **Signale nur nach oben.** Fallen, Anomalien, statistische Tests können eine zusätzliche Prüfung ansetzen, senken aber die Häufigkeit nicht und geben nicht die Markierung „geprüft“.
9. **Unverknüpfbarkeit des Zahlers** (Forschungselement). Einmalschlüssel des Zahlers und ein Relais, damit der Ausführende einen prüfenden Zahler nicht von einem faulen unterscheiden kann (claude1). Solange der Mechanismus nicht gebaut ist, steht in der Risikotabelle die Zeile „die Faulen sind unterscheidbar: bis `+R`, auch für den Neuling“.
10. **Was es in der Grundlage nicht gibt.** Geheime Regeln, Netzschlüssel der Prüfung, Schwellenkomitees von Hütern, TEE, FHE, MPC, iO.

### 4.2. Die Rolle von Blockchain und Leuchtturm: „ein dynamischer Detektor auf der Blockchain“ in der richtigen Form

Die Frage des Eigentümers nach einem dynamischen Detektor auf der Blockchain erhält folgende Antwort. Die Blockchain macht das, was von einem Detektor verlangt wird, gut, *außer* dem Geheimnis:

- **sie fixiert die Antwort vor der Wahl der Prüfung** — ohne das hilft keine Zufälligkeit;
- **sie speichert Verpflichtungen** zu künftigen Runden und Salzen, damit niemand einen passenden Ausgang wählen kann;
- **sie macht die Wahl reproduzierbar**: jeder Knoten berechnet nach der Runde selbst, was gewählt wurde, und prüft die Grundlage der Entscheidung auch nach einem vollständigen Stopp des Netzes;
- **sie vollzieht das Verbrennen und die einmalige Berechnung**.

Die „Dynamik“ gibt nicht die Verschlüsselung der Regeln, sondern dass die Prüfungsinstanz jedes Mal aus einer Zufälligkeit abgeleitet wird, die im Moment der Fixierung der Antwort noch nicht existierte. Für eine private Antwort ist diese Zufälligkeit die Münze des Zahlers; für gemeinsame Entscheidungen — der Leuchtturm nach D20. Die Arbeiten nannten das so: „ein offener Regelgenerator im Kern plus eine Instanz der Regel, abgeleitet aus dem Leuchtturm, dessen Runde vor der Fixierung bestimmt ist“ (claude1); „die Regeln sind offen, das Geheimnis liegt nur in der Wahl: wer, wann und welche Regel anwendet“ (mm4); „unvorhersagbar und nicht geheim“ (mm3).

Zwei Fehler, die zu vermeiden sind:

- **Der Leuchtturm in der Geldentscheidung des Zahlers** (mm3, mm4). Das öffentliche Los sagt, *was* zu prüfen ist, aber es prüft derselbe Zahler; ein fauler Zahler prüft auch nach einem öffentlichen Los nicht, und eine Sanktion für die Nichtprüfung ohne Pfand gibt es nicht (R5). Das öffentliche Los fügt hier nur eine Annahme über die Ehrlichkeit des Leuchtturms und die Verzögerung einer Runde hinzu (Kritiker Claude, DeepSeek; mm2 und claude2 sagen dasselbe). mm3 und mm4 stimmen dem nicht zu (Abschnitt 7).
- **Der Ersatzmodus „nach dem letzten verfügbaren Wert“** (mm3). Wenn der Leuchtturm nicht verfügbar ist und die Prüfungen der Epoche nach einem bereits bekannten Wert laufen, weiß der Betrüger im Voraus, dass nicht geprüft wird. Das verletzt D20 direkt. Bei Nichtverfügbarkeit der Runde wartet die strittige Leitung oder die Prüfung ist obligatorisch.

Noch eine Präzisierung: „aus zwei unabhängigen Bits das passende wählen“ senkt die Wahrscheinlichkeit einer obligatorischen Prüfung von `p` auf `p²` (Kritiker ChatGPT), und zwei Quellen mit einem eindeutigen Hash *zu vermischen* — ist genau das, was D20 verlangt. Die von mm5 vorgeschlagene Ergänzung zu D19 „geheime Münze und Leuchtturm werden nicht vermischt“ verwechselt diese beiden Handlungen und würde D20 widersprechen (Kritiker Claude).

### 4.3. Preis

Das Geheimnis der Regeln ändert den Preis nicht: es berührt weder `ρ` noch `γ`.

| `n_w` | `p = R/(R + H_lock)` | Prüfung `p·ρ` bei `ρ` = 0,10 / 0,21 / 0,40 | Insgesamt gegenüber Q8_0, Paket 1 | Paket 8 |
|---|---|---|---|---|
| 30 | 3,23% | 0,32% / 0,68% / 1,29% | +50,5…+82,3% | +152…+186% |
| 300 | 0,33% | 0,033% / 0,070% / 0,133% | +50,0…+80,2% | +150…+181% |
| 4320 | 0,023% | 0,0023% / 0,0049% / 0,0093% | +50,0…+80,0% | +150…+180% |

Die Tabelle ist [Berechnung] nach der Formel `γ(1 + pρ) − 1` und den gemessenen `ρ`, `γ` (Kritiker MiniMax, abgeglichen von den Kritikern DeepSeek und Claude). Der Kritiker ChatGPT erinnert daran, dass die Extrempunkte des Bereichs von `γ` und `ρ` von verschiedenen Karten stammen und nicht als Paar gemessen wurden; das ist eine Einhüllende, keine Messung.

- **Neuling.** Die erste Antwort — eine vollständige Prüfung, 10–40% seiner Generierung. Bei streng sequenzieller ehrlicher Arbeit und einem Wachstum von `H_lock` um `R` je Aufgabe ist die erwartete Zahl vollständiger Prüfungen in den ersten 30 Aufgaben gleich `1 + 1/2 + … + 1/30 ≈ 3,995`; das sind 1,33% / 2,80% / 5,33% der Arbeit des Fensters bei `ρ` = 0,10 / 0,21 / 0,40 (mm1, Kritiker ChatGPT) [Berechnung]. Bei einem parallelen Start mit leerem Konto kostet jede Anmeldung eine vollständige Prüfung.
- **Richtwert 5%.** Als Aufschlag für die Prüfung ist er erreichbar: `p·ρ ≤ 0,05` verlangt `p` nicht größer als 50% / 23,81% / 12,5%, das heißt `H_lock/R ≥ ρ/0,05 − 1` = 1 / 3,2 / 7 (gpt1, gpt2) [Berechnung]. Als „5% über der gewöhnlichen Generierung“ — nicht: das exakte Profil selbst kostet +50…+80% [gemessen γ]. Der einzige Weg zu 5% sind schnellere bitweise gleiche Kerne.
- **Zuschläge der Strategie.** 32–64 Byte einer Verpflichtung oder Hunderte Byte einer VRF pro Antwort dort, wo die Prüfbarkeit der Münze nötig ist; der Leuchtturm — Hunderte Byte pro Runde pro Paket und die Verzögerung einer Runde nur für gemeinsame Stichproben (Kritiker Claude) [Berechnung].
- **Wer zahlt** (mm4, Kritiker MiniMax). Den Aufschlag des exakten Profils `γ − 1` trägt der Ausführende bei jeder bezahlten Antwort; die Prüfung `p·ρ` — der Zahler aus seiner Vorauszahlung. Die Verlagerung der Prüfung auf den Zahler entfernt die Rolle „Prüfer, dem für die Prüfung bezahlt wird“ aus [CURRENT_DESIGN](CURRENT_DESIGN.md), Abschnitt 1. Dann steigt entweder der Preis `R` um 50–80%, oder die Marge des Ausführenden strebt gegen null. Das ist eine separate Frage des Eigentümers (Abschnitt 5).
- **Lotterie B** (bezahlt werden nur die gewählten und vollständig geprüften Antworten, Variante von gpt1, gpt2 und des Kritikers ChatGPT). Bei einem Auswahlanteil von 5% kosten die Prüfungen im Mittel 0,5 / 1,05 / 2% der Zeit der exakten Generierung, aber 95% der Antworten bleiben ungeprüft und unbezahlt; die Streuung einer einzelnen Auszahlung `19R²`; die Wahrscheinlichkeit, über 20 unabhängige Anmeldungen keine einzige Auszahlung zu erhalten, `0,95²⁰ ≈ 35,85%`, über 30 — 21,46% [Berechnung].
- **Training.** Eine vollständige Wiederholung des Schritts kostet etwa 100% des Schritts für jeden prüfenden Knoten; der Richtwert 20% ist durch kein Schema gezeigt. Bei `N = 1000` annehmenden Knoten bleiben selbst bei null sonstigen Kosten für eine Prüfung nicht mehr als 0,0002 der Arbeit des Schritts (Kritiker ChatGPT) [Berechnung].

### 4.4. Restrisiko

Der erwartete Gewinn einer Fälschung gegenüber Untätigkeit; „Schaden“ — der Anteil der nicht aufgedeckten Fälschungen des Schädigers, alle mit der Markierung „nicht geprüft“. Die Tabelle ist aus den Tabellen der Kritiker Claude, DeepSeek, ChatGPT und MiniMax und aus STRATEGY_SEARCH 5.3 zusammengestellt; **hervorgehoben sind die von diesem Rat korrigierten Zellen**. Der verborgene Detektor verbessert keine Zeile [Berechnung].

| Fall | `q = 0,1` | `q = 0,3` | `q = 0,5` | `q = 1` | Neuling, `H = 0` |
|---|---|---|---|---|---|
| Geld, der Zahler prüft selbst; das Journal lebt, D26 und D23 gelöst | ≤ 0 | ≤ 0 | ≤ 0 | ≤ 0 | `−c_f` (Prüfung immer) |
| Dasselbe, aber die Koalition `q = 1` umfasst die Blockproduzenten und zensiert den Streit | — | — | — | bis `+R` | bis `+R` |
| Falsche Antwort mit der Markierung „geprüft“ | 0 | 0 | 0 | 0 | 0 |
| Schaden bei `p = R/(R + H)`: die ganze Serie von `n_w` Fälschungen geht durch | ≈ 50% | ≈ 50% | ≈ 50% | ≈ 50% | 0 beim ehrlichen Zahler |
| Schaden bei `p = 3R/(R + H)` | ≈ 12,5% | ebenso | ebenso | ebenso | 0 |
| Faule Zahler mit dem Anteil `λ`, der Ausführende unterscheidet sie nicht | ≤ 0 bei `p(1 − λ) ≥ R/(R + H)` | ebenso | ebenso | ebenso | **`+λR`** |
| Faule Zahler sind unterscheidbar (durch Proben mit neuen Schlüsseln — kostenlos) | bis `+R` | bis `+R` | bis `+R` | bis `+R` | **bis `+R`** |
| Ein Zahler ohne Ausrüstung hat die Prüfung einem zufälligen Tripel übertragen | +0,001R | +0,027R | +0,125R | +R | ebenso |
| Gemeinsame Stichprobe nach D20, mindestens eine Quelle ist ehrlich | ≤ 0 | ≤ 0 | ≤ 0 | ≤ 0 bei einer ehrlichen externen; sonst bis `+R` | ebenso |
| Nur der interne Leuchtturm der Teilnehmer 64/43 | ≤ 0 außer 4,8·10⁻²⁸ | außer 9,4·10⁻¹⁰ | außer 0,41% | bis `+R` | ebenso |
| Zum Vergleich: die geheime Epochenregel bei einem Komitee | leckt über 10 Anwendungen mit der Wahrscheinlichkeit 0,65; danach etwa `(1 − p)·E·R` je Epoche | 0,97 | 0,999 | bis `+R` pro Fälschung | Proben sind kostenlos: bis `+R` |
| Training ohne selbst prüfenden Knoten | bis `+R` | bis `+R` | bis `+R` | bis `+R` | bis `+R` |

Wie die Tabelle zu lesen ist:

- **Die Zeile „≤ 0 bei beliebigem `q`“** ist nur unter den genannten Bedingungen richtig: `q` — der Abspracheanteil unter den fremden Prüfern; wenn dieselbe Koalition die Produktion der Blöcke oder den Leuchtturm kontrolliert, kann sie den Beweis verzögern oder zensieren (das sagten gpt1 und gpt2 direkt). Nötig sind auch `δ ≪ W`, das atomare Verbrennen (D26), die Lösung des Konflikts mit D16 und die Regel für falsche Streitigkeiten (D23, Berechnung M9).
- **Die Vollstreckung der Prüfung ist nicht weniger wichtig als die Häufigkeit.** Beispiel des Kritikers ChatGPT: `R = 1`, `H = 3`, `p = 1/4`, `c_f = 0` ergeben genau den Erwartungswert null; wenn der Zahler nur 90% der angesetzten Prüfungen vollstreckt, ist die Fangwahrscheinlichkeit 0,225 und der Gewinn `+0,1R` [Berechnung]. Wenn man die erste Fälschung nach dem derzeitigen D16 als Ausfall erklären und `H` bewahren kann, ist der Erwartungswert `(1 − p)R − c_f` positiv.
- **„≈ 50%“** ist die Wahrscheinlichkeit, dass *die ganze Serie* von `n_w = H/R` Fälschungen durchgeht, wenn `H` nach jedem Durchlass wächst (`h/(h + n)` bei `n = h`). Eine gezielte Fälschung eines ausgereiften Schlüssels geht mit der Wahrscheinlichkeit `1 − p` durch: bei `H = 4320R` sind das etwa 99,977% (Kritiker ChatGPT nach ds2).
- **Die Zeilen „faul“** sind korrigiert: der frühere Wert 0 für den Neuling ist falsch (Abschnitt 1, Punkt 6). Szenario: ein frischer Schlüssel reicht dem Zahler `X` eine Fälschung ein; wenn `X` prüft, geht nur `c_f` verloren, es gibt nichts zu verbrennen; wenn `X` faul ist, erhält der Schlüssel `R` und das Wissen „`X` ist faul“; danach reichen die ausgereiften Schlüssel der Koalition Fälschungen nur den Faulen ein (Kritiker Claude). Der Kritiker ChatGPT ergänzte, dass selbst bei vollständiger Ununterscheidbarkeit die Bedingung `p(1 − λ) ≥ 1` für den Neuling bei `λ > 0` unerfüllbar ist, und unverknüpfbare Schlüssel nur einen Kanal der Unterscheidung schließen: Text, Zeit, Größe der Anfrage und die verbundene Zahlung bleiben.

### 4.5. Neuling

Ein Neuling mit leerem Konto (`H_lock = 0`) wird gegen einen ehrlichen Zahler immer geprüft und verliert `c_f`. Die Verborgenheit der Regeln fügt hier nichts hinzu. Zwei Vorbehalte dieses Rats: gegen einen faulen Zahler erhält der Neuling bis `+R` (Abschnitt 4.4), und kostenlose neue Schlüssel können den Anteil vollständig geprüfter Anmeldungen erhöhen: wenn der Anteil der Arbeit der ersten Bestellungen leerer Schlüssel gleich `f` ist und bei den übrigen `p = 0,1` gilt, ist der Aufschlag gleich `ρ[f + 0,1(1 − f)]`, und die Bedingung 5% ergibt bei `ρ = 0,21` `f ≤ 0,1534` (Kritiker ChatGPT) [Berechnung]. Kein Schema des Rats hält bisher den Strom neuer Schlüssel und die Selbstbezahlung gleichzeitig aus.

### 4.6. Fauler Zahler

Die Strategie beruht darauf, dass der Zahler tatsächlich eine Münze wirft und prüft. Ein fauler Zahler, den der Ausführende unterscheiden kann, gibt jedem Schlüssel bis `+R`. Mittel nach abnehmender Stärke: (a) das Programm des Zahlers vollstreckt standardmäßig die Regel des Kerns, und das Abschalten der Prüfung nimmt der Antwort die Markierung „geprüft“; (b) unverknüpfbare Schlüssel des Zahlers (claude1) — nötig ist ein Zahlungsmechanismus ohne Aussteller mit Sonderrechten: eine blinde Signatur braucht einen Aussteller, Privacy Pass (aus dem Gedächtnis) — ein Schema mit einem Server-Aussteller; ein Schwellen-Aussteller führt wieder `q` ein (Kritiker Claude); (c) das öffentliche Los des Leuchtturms *korrigiert* den faulen Zahler nicht (Abschnitt 4.2). Wie man die Unverknüpfbarkeit mit der Regel für falsche Streitigkeiten ohne Pfand (D23) verbindet, ist nicht gelöst.

### 4.7. Nutzer ohne Ausrüstung

Ein Nutzer, der die Antwort nicht selbst nachrechnen kann, ist durch diese Strategie nicht geschützt. Wenn er die Prüfung einem zufälligen Tripel überträgt, erhält die Koalition `q³R`: +0,001R / +0,027R / +0,125R / +R; bei einem einzigen Helfer — `qR`, und bei einem absichtlich gewählten Mitverschworenen — bis `+R` bei jedem mittleren Anteil (Kritiker ChatGPT) [Berechnung]. Eine begrenzte positive Leckage ist durch D1 direkt verboten, daher ist das ein offenes Loch von D21. Ein verborgener Detektor schließt es nicht: claude1 zeigte ein Gegenbeispiel mit „geheimen Kanarienvögeln“ — ein mitverschworener Prüfer besteht ehrlich alle fremden Kontrollaufgaben und lügt nur bei seinen eigenen Fälschungen, die er am Schlüssel des Ausführenden oder an der Freiheit der Wahl erkennt (eine Fälschung muss nicht deterministisch sein, die exakte Antwort ist deterministisch). Eine ehrliche Variante ist, zwei Serviceebenen mit klar geschriebenem Unterschied zu verkaufen: „von mir geprüft“ und „von Bestimmten geprüft, Leckage `R·q^k`“ (mm1).

### 4.8. Schaden

Der Schädiger braucht keinen Gewinn. Bei jeder Häufigkeit `p < 1` geht ein Teil seiner Fälschungen durch. Der einzige Schutz ist die Markierung „nicht geprüft“ standardmäßig und „geprüft“ nur nach einer vollständigen Prüfung vor der Anzeige. Der verborgene Detektor ändert die Zeile des Schadens nicht (alle Arbeiten). mm1 fand die einzige Stelle, wo eine *frische Wahl* das Bild des Schadens wesentlich ändert: bei einer teilweisen Prüfung (vor allem des Trainingsschritts) gegen eine offene fixierte Probe findet der Betrüger mit einem einzigen exakten Durchlauf die nicht prüfbaren Zellen und fälscht nur diese, die Fangwahrscheinlichkeit ist 0; eine frische Wahl der Probe nach der Fixierung ergibt eine Fangwahrscheinlichkeit `s` (der Anteil des geprüften Teils) für eine Abweichung und `1 − (1 − s)^m` für `m` Abweichungen. Die Kritiker DeepSeek und Claude präzisierten: das ist frische Zufälligkeit und nicht das Geheimnis der Regeln; das Motiv einer solchen Fälschung ist Schaden und nicht Geld (gegen ehrliche Arbeit gewinnt eine exakte Fälschung etwa null); und die Schlussfolgerung beruht auf der ungeklärten Annahme, dass sich die Zellen des Trainingsschritts unabhängig fälschen lassen.

---

## 5. Entscheidungen

Die Formulierungen unten sind **Empfehlungen** und keine angenommenen Entscheidungen. Die unveränderlichen Anforderungen R1–R6 ändern sich durch die Änderung von Zeilen der Roadmap nicht. Nach D4 verlangt nach dem Start mit festgeschriebenem Fingerabdruck die Änderung der Menge zulässiger Übergänge den Wechsel auf ein neues Netz; der Wechsel eines Schlüssels gibt dieses Recht nicht (Kritiker ChatGPT).

### 5.1. D4 — ergänzen, den Sinn nicht ändern

Der derzeitige Text von D4: die Prüfung ist automatisch, ohne Abstimmungen; jeder Knoten führt die Prüfung selbst nach dem festgeschriebenen Fingerabdruck der Regeln aus. Der Rat ist einstimmig dagegen, D4 um geheimer Regeln willen zu schwächen: eine geheime Regel verlangt, das Urteil der Halter eines Schlüssels, eines Enklaves oder einer Gruppe anzunehmen, das der Knoten selbst nicht prüfen kann. Der Kritiker ChatGPT zeigte, wie eine solche Schwächung aussehen würde: „der Knoten nimmt das Urteil des aktuellen Programms an, das die Halter des Epochenschlüssels gewählt haben“, „der Knoten nimmt den Bericht eines gemessenen Programms über die vertrauenswürdige Kette des Herstellers an“ oder „der Knoten nimmt das von der Gruppe ausgegebene Bit an“.

**Vorgeschlagene Ergänzung** (Zusammenführung der Varianten der Kritiker Claude und ChatGPT, claude1, claude2, gpt1, der Vorschläge D27 von mm5):

> „Der Kern kann als Eingang eine Zufälligkeit annehmen, die dem Ausführenden bis zur endgültigen Fixierung des Ergebnisses unbekannt ist: (a) die geheime Münze der Seite, deren eigene Entscheidung geschützt wird, geworfen nach der Fixierung; (b) die Werte der Quellen von D20 in Runden, die vor der Fixierung bestimmt sind und nach ihr eintreten. Der Generator der Prüfungsinstanz, die Familie zulässiger Prüfungen und das Wahlgesetz sind ein offener Teil des Kerns mit festgeschriebenem Fingerabdruck; neue Regeln zu zufälligen Zeiten sind neue Werte der Zufälligkeit und nicht neue Algorithmen. Eine realisierte Instanz, die fremde Rechte betrifft, wird nicht später als die Auszahlung veröffentlicht und von jedem Knoten nachgerechnet. Eine lokale Markierung des Zahlers erzeugt für sich kein Netzzeugnis über die Arbeit. Langlebige geheime Regeln und Prüfschlüssel, Schwellenkomitees, TEE-Attestierungen und geschlossene Urteile enthält die Grundlage einer gemeinsamen Entscheidung nicht; sie sind nur als zusätzliche Prüfungen zulässig, die die Häufigkeit erhöhen.“

**Was sich nicht ändert:** die Unveränderlichkeit des Kerns, das Fehlen von Abstimmungen, die selbstständige Prüfung durch jeden Knoten. **Was es bricht:** nichts; die Ergänzung schließt die Richtung „geheime Detektoren“ als Grundlage der Garantie. Die Möglichkeit eines öffentlich prüfbaren Beweises einer festgeschriebenen Relation (ZK) bleibt offen und verlangt keine Änderung von D4 (Kritiker ChatGPT).

### 5.2. D20 — präzisieren

Der derzeitige Text von D20: nicht weniger als zwei unabhängige öffentliche Quellen, ein Wert zu einem vorher bestimmten Moment nach der endgültigen Fixierung, ohne Recht auf Überspringen.

**Vorgeschlagene Präzisierung** (Kritiker Claude mit Ergänzungen des Kritikers ChatGPT):

> „Nicht weniger als zwei unabhängige öffentliche Quellen; ihre Werte werden mit einer eindeutigen Hash-Funktion mit Domänenmarke und Kennung der Partie vereinigt und nicht durch Auswahl eines der Werte. Die Runde jeder Quelle wird vor der endgültigen Fixierung bestimmt und tritt nach der endgültigen Annahme des Blocks mit der Fixierung ein. Überspringen, erneute Auslosung, Ersatz einer Quelle oder der Übergang auf einen früher bekannten Wert sind verboten; bei Nichtverfügbarkeit der Runde wartet die strittige Leitung, eine neue Anmeldung erhält kein Los für diese Runde. Der Leuchtturm wird für Stichproben verwendet, die fremde Rechte betreffen (Training, Examen, Lotterie mit gemeinsamem Preis, Bestimmung der Prüfer); für die private Prüfung des Zahlers über sein eigenes Geld ist er nicht nötig. Ein interner Schwellen-Leuchtturm der Teilnehmer kann nur eine der Quellen sein, mit einer aufgeschriebenen Annahme über den Abspracheanteil seiner Halter, und kann nicht die einzige sein. Ein VDF vom selben Block gilt nicht als unabhängige Quelle. Das Vertrauen in die Quellen ist eine Annahme nach R4.“

**Was es ausschließt:** den Ersatzmodus „letzter verfügbarer Wert“ (mm3), die Änderung von mm5 an D19 („die Quellen nicht vermischen“), den Leuchtturm in der Geldentscheidung des Zahlers (mm3, mm4). **Offenes Risiko:** wenn „auf die Runde warten“ eine unendliche Verzögerung bedeutet, ist das ein nicht geschlossenes Risiko R1/R6 (Kritiker ChatGPT); der Kritiker MiniMax schlägt vor, statt zu warten die Prüfung als obligatorisch zu betrachten.

### 5.3. Was sich nicht ändert

- **D1** — nicht ändern und nicht auf „solange `q` klein ist“ abschwächen; eine begrenzte positive Leckage bleibt eine Verletzung (alle Arbeiten und Kritiker).
- **D7** — eine geheime Regel erfüllt es bei keinem Schwellenwert (Abschnitt 2.4).
- **D19** — nicht ändern: die Ergänzung von mm5 ist falsch (Abschnitt 4.2).
- **D6** — die Verborgenheit ändert die Zeile des Schadens nicht; die Markierungen werden nach Frage 3 des vorigen Rats präzisiert.

### 5.4. Der Zusammenhang mit den acht Fragen des vorigen Rats

Die acht Fragen [STRATEGY_SEARCH](STRATEGY_SEARCH.md), Abschnitt 6, bleiben offen. Dieser Rat hat ihnen hinzugefügt:

| Frage des vorigen Rats | Was der sechste Rat hinzugefügt hat |
|---|---|
| 1. D21, D11, D2: soll eine mit der Münze übersprungene Antwort bezahlt werden | Keine neuen Argumente. Korrigiert wurde die Zelle „fauler Zahler × Neuling“ (bis `+R`): wenn die Bezahlung des Übersprungenen erlaubt ist, braucht man Schutz vor der Unterscheidung der Faulen. Der Kritiker ChatGPT ist weiterhin für die vollständige Prüfung als Hauptvertrag und für die Lotterie B als separaten |
| 2. D7: welche Prüfung für die Bezahlung zulässig ist | Bestätigt, dass weder Verborgenheit noch Attestierung noch ein Komitee die untere Häufigkeit senken können; erhöhen darf man. Hinzugefügt: wichtig ist der Anteil der *vollstreckten* Prüfungen und nicht nur die Häufigkeit (Beispiel `+0,1R`) |
| 3. D6: Markierungen | Falle, Statistik und verborgener Detektor geben nicht die Markierung „geprüft“ |
| 4. D16: ehrlicher Ausfall | Wenn man die erste Fälschung als Ausfall erklären und `H` bewahren kann, hält die Münze nicht zurück: `(1 − p)R − c_f > 0`. Eine Entscheidung zu D16 ist vor jeder Einschaltung der Bezahlung des Übersprungenen nötig |
| 5. D8: Frist und Rechte des Streits | Die Bedingung `δ ≪ W` und die Lebendigkeit des Journals gehören in die Zeile „≤ 0“ (Abschnitt 4.4) |
| 6. D23: Blockierung bis M9 | Keine der elf Arbeiten hat M9 berechnet; die Blockierung bleibt. Die Unverknüpfbarkeit der Zahler fügt M9 eine neue Frage hinzu |
| 7. Neues D26: Schloss des Betrags | Die Notwendigkeit des atomaren Verbrennens der Welle ist bestätigt; das gemeinsame Bit der Epoche — ein neues Gegenbeispiel (`+8,1R`) |
| 8. D1: ändern oder nicht | Nicht ändern |

### 5.5. Neue Fragen-Entscheidungen dieses Rats

**Frage A (D4).** Soll die Ergänzung von D4 aus Abschnitt 5.1 angenommen werden? *Empfehlung der Kritiker Claude, ChatGPT und DeepSeek:* ja; der Sinn von D4 ändert sich nicht. *Wo sie sich trennten:* der Kritiker ChatGPT schlägt eine ausführlichere Fassung vor, die ausdrücklich von der Prüfung „nach einem öffentlich prüfbaren Beweis einer festgeschriebenen Aussage“ spricht; der Kritiker DeepSeek hält eine kurze Anmerkung über die Zufälligkeit nach der Fixierung für ausreichend; der Kritiker MiniMax (wie mm2 und mm5) meint, D4 müsse gar nicht geändert werden, weil die Prüfregel ohnehin offen sei.

**Frage B (D20).** Soll die Präzisierung von D20 aus Abschnitt 5.2 angenommen werden? *Empfehlung:* ja. *Wo sie sich trennten:* was bei Nichtverfügbarkeit der Runde zu tun ist — warten (Kritiker Claude und ChatGPT) oder die Prüfung als obligatorisch betrachten (Kritiker DeepSeek und MiniMax). Das Warten kann zu einer unendlichen Verzögerung werden; die obligatorische Prüfung ändert den Preis und, in der Lotterie, die Zusammensetzung der Gewinner.

**Frage C (Leuchtturm oder Münze in der Geldentscheidung).** Soll festgeschrieben werden, dass für die private Prüfung des Zahlers über sein eigenes Geld kein Leuchtturm verwendet wird? *Empfehlung* der Kritiker Claude und DeepSeek sowie von claude1, gpt1, gpt2, ds1, ds2, mm1, mm2: ja. *Dagegen:* mm3, mm4, mm5 (öffentliches Los statt der Münze), claude2 (VRF des Zahlers plus Leuchtturm für gemeinsame Angelegenheiten). Der Kritiker DeepSeek schlägt vor, zuerst beide Schemata mit einem Mini-Agenten an denselben Angriffen zu vergleichen (Abschnitt 6).

**Frage D (unverknüpfbare Zahler).** Soll in das Forschungsprogramm ein Mechanismus aufgenommen werden, bei dem der Ausführende die Anfragen eines Zahlers nicht verknüpfen kann? *Empfehlung* des Kritikers Claude: ja, als Forschung; bis zu seinem Bau enthält die Risikotabelle die Zeile „die Faulen sind unterscheidbar: bis `+R`“. *Offen:* eine Zahlung ohne Aussteller mit Sonderrechten, die Vereinbarkeit mit D23, die Unterscheidung nach Text und Zeit.

**Frage E (Gewicht).** Soll in der Spezifikation des Gewichts ([CURRENT_DESIGN](CURRENT_DESIGN.md), Abschnitt 4) festgeschrieben werden, dass das Gewicht, nach dem Halter oder Prüfer ausgewählt werden, nicht durch selbst bezahlte Anfragen wächst? *Empfehlung* des Kritikers Claude: ja. claude2 schlug eine Auswahl „nach dem Gewicht geprüfter Arbeit“ ohne diesen Vorbehalt vor.

**Frage F (wer zahlt für das exakte Profil).** Wie soll der Aufschlag `γ − 1` verteilt werden, wenn die Rolle des bezahlten Prüfers verschwindet? *Gestellt* von mm4 und dem Kritiker MiniMax; eine Lösung wurde nicht vorgeschlagen.

**Frage G (neue Entscheidungen von mm5).** Sollen D27 („Geheimnis der Wahl, nicht Geheimnis der Prüfung“) und D28 („Münze mit verzögerter Offenlegung“) angenommen werden? *Empfehlung der Kritiker:* D27 geht dem Sinn nach in die Ergänzung von D4 ein (Abschnitt 5.1); D28 dupliziert die Verpflichtung zur Münze von gpt2 und claude1 und ist nur sinnvoll, wenn die Verpflichtung *vor* der Fixierung der Antwort veröffentlicht wird.

---

## 6. Was mit Mini-Agenten zu berechnen und was durch Experimente zu prüfen ist

### 6.1. Mini-Agenten (exakte Brüche, Kontroll-Hash, Wiederholung auf einem zweiten Gerät)

Die gemeinsame Liste der vier Kritiker. Für jede Berechnung sind die Beschreibung der Regeln, die Eingänge, die exakten Brüche, die schlechteste Historie, die Version und der Kontroll-Hash zu speichern (Kritiker ChatGPT).

1. **Epochenregel gegen frische Münze.** Welle, `H_lock`, Verbrennen des ganzen Betrags, adaptive Folge. Referenzwerte: `+8,1R` / `−2,3751096381R` (gpt2), `98,01R` (claude2), 1/5 → 1/9 → 0 (claude1), `+4,4295R` / `−2,49676R` / `+7,2R` (voriger Rat und Kritiker ChatGPT).
2. **Proben fauler Zahler mit neuen Schlüsseln.** Erwartung der Probe, Zeit bis zur Erkennung des Zahlers, Gewinn der ausgereiften Schlüssel; mit verknüpfbaren und unverknüpfbaren Zahlern. Erwartung des Kritikers Claude: bei Verknüpfbarkeit ist die Zurückhaltung gegenüber den Faulen gleich null.
3. **Geheime Münze gegen das öffentliche Los des Leuchtturms** bei denselben Angriffen (Kritiker DeepSeek). Erwartung: gleiche Geldausgänge und ein höherer Preis beim öffentlichen Los.
4. **Lineares Programm einer Mischung von Tests** (gpt1, gpt2): Referenz „drei Klassen → 2/3 gegen 1/2“, Hinzufügen einer nicht abgedeckten Klasse → 0; Minimax über die Matrix „Test × Fälschung“.
5. **Schwänze der Schwelle:** binomial, ohne Zurücklegen, nach Gewicht mit Selbstbezahlung, mit Bestechung nach der Bestimmung. Referenz „3 aus 5“: `107/12500`, `4077/25000`, `1/2`, `1`; Kontroll-SHA-256 der vier Zeilen von gpt1, vom Kritiker ChatGPT wiederholt: `fd83fbdd42baa56d982eba3be90888cf3ec5a6261b5daa53d42fdc42b99c8323`.
6. **Fallen:** `1/((1 − σ)ρ)` auf einem Gitter von `ρ` und `σ`; Erkennung einer Wiederholung; Amortisierung einer Bank von Referenzwerten gegen die Neuberechnung; Prüfung der Aussage von mm2 über den fast null Preis einer Wiederholung einer geprüften Anfrage.
7. **Abweichungen bei VRF und Verpflichtung des Zahlers:** Weigerung, offenzulegen, mehrere Schlüssel, Abbruch nach der Offenlegung, Lotterie mit gemeinsamem Preis.
8. **Mischung der Quellen von D20:** Verzerrung bei einer ehrlichen Quelle, beim Zurückhalten eines Blocks, bei Nichtverfügbarkeit der Runde; Verbot des „letzten Werts“.
9. **„Chirurgische“ Fälschung von mm1** gegen eine offene fixierte und eine frische Probe: Fangwahrscheinlichkeit 0 gegen `s`; Schwelle `p·s ≥ (R − c)/(R + H_lock)`.
10. **Zählung nichtlinearer Operationen pro Token** nach der festgeschriebenen Konfiguration D5 für die Schätzungen von FHE und MPC (derzeit 1,4·10⁷–2,6·10⁷ ungefähr); Schätzungen von DKG, commit–reveal, VRF in Byte und Nachrichten.
11. **Paket 8 beim Zahler** (mm3): `ρ` ist relativ zur paketierten Generierung gemessen, und die Neuberechnung einer Antwort durch den Zahler wird dadurch nicht billiger.
12. **Korrektur der Tabellen:** mm1 (`k = 10`, `H_lock = 10R`), mm5 (`p·ρ`), die Zelle „faul × Neuling“ in STRATEGY_SEARCH 5.3.
13. **M9** — der Preis des Streits für die Regel D7 und die Bedingung der Aufhebung der Blockierung D23; Selbststreit, Rückzahlungsgrenze, Strom neuer Schlüssel.

### 6.2. Experimente

**Für die Schlussfolgerung über den verborgenen Detektor ist kein Experiment nötig:** das sind Theoreme, eine Messung widerlegt sie nicht (claude1, claude2, ds2, Kritiker Claude und DeepSeek). Experimente mit FHE, MPC und TEE sind ebenfalls nicht nötig: ihr bestes Ergebnis ändert die Theoreme nicht.

**Im Rahmen von D5 (erlaubt):** O5 — Qualität auf 320 Aufgaben; O3 und O4 mit schnelleren bitweise gleichen Kernen — der einzige Weg zum Richtwert 5%.

**Außerhalb von D5 — nur mit einer gesonderten Erlaubnis des Eigentümers:**

- die Zeit eines Durchlaufs der Prüfung auf der CPU eines Laptops und auf einem Telefon, Kalt- und Warmstart, Energie;
- inwieweit die Metadaten einer Anfrage (Zeit, Größe, Text) es dem Ausführenden erlauben, einen prüfenden Zahler zu unterscheiden — davon hängt der Preis unverknüpfbaren Schlüssel ab;
- die Häufigkeit stiller Hardwarediskrepanzen `P_f` — vor jeder Änderung von D16;
- der Anteil übereinstimmender Token von Q8_0 und dem exakten Profil (für die Schätzung einer billigen Fälschung und für die exakte spekulative Dekodierung);
- die Verzögerung und die Kosten einer Runde eines realen Leuchtturms, das Verhalten bei einer schweigenden Quelle;
- für Fallen — ob die Prüfung erkannt wird und was die Referenzwerte kosten;
- die exakte Wiederholung des Trainingsschritts als Voraussetzung jeder seiner Prüfungen.

---

## 7. Meinungsverschiedenheiten, die der Rat nicht gelöst hat, und zweifelhafte Verweise

### 7.1. Meinungsverschiedenheiten

1. **Die Bezahlung einer mit der Münze übersprungenen Antwort gegen die vollständige Prüfung jeder bezahlten Antwort.** claude1, claude2, ds1, ds2 und mm1–mm5 stützen sich auf die Bezahlung des Übersprungenen unter dem Risiko des Verbrennens des nicht ausgereiften Betrags; gpt1, gpt2 und der Kritiker ChatGPT — auf die vollständige Prüfung als Hauptvertrag und die Lotterie B als separate. Vom vorigen Rat übernommen; Entscheidung des Eigentümers zu D21, D11, D7.
2. **Leuchtturm oder Münze in der Geldentscheidung des Zahlers** — Abschnitt 5.5, Frage C. mm3 und mm4 meinen, das öffentliche Los nehme die Annahme eines ehrlichen Zahlers weg; die Kritiker Claude und DeepSeek halten das für einen Fehler (ein fauler Zahler prüft auch nach einem öffentlichen Los nicht). Nicht berechnet.
3. **`R/(R + H_lock)` oder `R/H`.** Das Erste ist für das Geld genau; das Zweite gibt einen Puffer und eine endliche erwartete Zahl von Fälschungen bis zur Fangung bei festem `H`, kostet aber bei kleinem `H` etwa doppelt so viel. Der Kritiker ChatGPT zeigte, dass bei einem Wachstum von `H` nach jedem Durchlass bei beiden Regeln die mittlere Zahl der Durchlässe bis zur ersten Fangung unendlich ist. Neue Argumente hat der Rat nicht geliefert.
4. **Die Falle als eigenständiger Gewinn.** mm2 (ein geheimer Referenzwert — der einzige wirkliche Gewinn) und ds1 (Ersparnis eines zwischengespeicherten Referenzwerts) gegen claude2, mm4, mm5, gpt1 und die Kritiker Claude und DeepSeek. Der Kritiker ChatGPT nahm eine Zwischenposition ein: ein dem ehrlichen Zahler bereits bekannter Referenzwert kann den Grenzpreis senken, und für frische ununterscheidbare Fallen kann `σ` selbst bei `q = 1` unter fremden Ausführenden 0 sein. Die Berechnung wurde nicht ausgeführt.
5. **Eine Mischung von Prüfungstypen als Mittel der Ersparnis.** gpt1, gpt2, claude2 — möglich bei nachgewiesener Abdeckung der Fehlerklassen; mm2 — niemals. Für Qwen ist die Abdeckung nicht bewiesen.
6. **Ein interner Schwellen-Leuchtturm der Teilnehmer.** mm3 — das beste Primitiv; mm5 — nur ein externer; claude1, claude2 und der Kritiker Claude — zulässig nur als eine der Quellen.
7. **Inwieweit R2/R3 gemeinsame Geheimnisse verbieten.** ds1, mm1, mm3 — grundsätzlich; claude2, die Kritiker Claude und ChatGPT — nur Geheimnisse, die zur Prüfung vergangener Entscheidungen nötig sind.
8. **Der Preis von MPC.** Die Schätzungen weichen um Größenordnungen ab: ds1 — 2,4–14 MB pro Token (die Kritiker meinen, das sei der Preis der Spur der Prüfung und nicht von MPC); Kritiker Claude — 0,15–1 GB pro Token; Kritiker ChatGPT — 448 MB pro Position; Kritiker MiniMax — bis 180 TB pro Antwort (er betrachtet alle Multiplikationen als netzwerkgebunden, und der Kritiker ChatGPT bemerkt, dass die Multiplikation eines offenen Gewichts mit einer geteilten Aktivierung in vielen Protokollen lokal ausgeführt wird). Die Schlussfolgerung „MPC ist außerhalb des Budgets und hängt von `q` ab“ ändert sich dadurch nicht.
9. **Die Multiplikatoren von FHE:** ds1 `10³–10⁶`, claude2 `3·10³–2·10⁵`; der Kritiker ChatGPT meint, dass es falsch ist, die Schätzung nach Bootstraps mit `ρ` eines fertigen Durchlaufs zu multiplizieren, und dass eine Schätzung desselben Durchlaufs unter einem konkreten Schema nötig ist. Die Schlussfolgerungen hängen davon nicht ab.
10. **Eine verborgene Probe bei einer teilweisen Prüfung** (mm1): „geheimer Detektor“ oder frische Münze — ein Streit um Worte; die Anwendbarkeit auf den Trainingsschritt hängt von der nicht gemessenen Unabhängigkeit der Zellen ab.
11. **D16.** Das Verbrennen von `H_lock` für jede nachgewiesene Abweichung mit einer Entschädigung der Ehrlichen aus einer Netzabgabe (Linie von claude1 und der Kritiker Claude und DeepSeek) gegen die Bewahrung der früheren Belohnungen bei einem ehrlichen Ausfall (gpt1, gpt2, Kritiker ChatGPT). Nötig ist eine Messung von `P_f`.
12. **Training.** Kein Schema erfüllt D7 bei `q = 1` innerhalb von 20%.
13. **Die Hauptklasse der Fälschungen:** die teure „chirurgische“ (mm1) oder die billige Q8_0 (mm3, mm4). Nicht gemessen.

### 7.2. Gefundene Fehler in den Zahlen der Arbeiten

Damit falsche Zahlen nicht in andere Dokumente gelangen:

| Arbeit | Aussage | Richtig [Berechnung der Kritiker] |
|---|---|---|
| mm1 | Bei `H_lock = 10R` Häufigkeit 0,0909 und Preis der Prüfung 0,005–0,009% | `0,0909·ρ` = 0,91–3,64% |
| mm1 | Leckage der „Zehner“ bei `q = 0,1`: `1·10⁻⁵R` | `10⁻¹⁰R` |
| mm1 | Schwelle 25% bei `H_lock = R` | 29,29% bei den eigenen Parametern von mm1 |
| mm5 | `p·ρ` = 0,021–0,042% bei `p = 0,1` | 2,1–4,0% (die eigene Tabelle von mm5 ist richtig) |
| mm5 | „FHE ist deterministisch, der Beobachter baut ein Wörterbuch“ | Stabile FHE-Schemata sind probabilistisch |
| mm5 | „VRF ist für den Eigentümer unvorhersagbar“ | Der Eigentümer berechnet die VRF, wann er will |
| mm5 | Eine vollständige Wiederholung des Trainingsschritts ≈ 36,8% | 36,8% — ein Beispiel gemischter Last; die Wiederholung des Schritts ≈ 100% |
| mm2 | „5% sind bei `p ≤ 0,33%` erreichbar“ | Bei `ρ = 0,21` ist `p ≤ 23,8%` zulässig |
| mm4 | „VRF legt die Wahl nicht offen“ | Die Prüfung des VRF-Beweises legt den Wert offen |
| ds2 | `N·H_s ≈ 2718` Versuche | Etwa 890 ohne Zurücklegen; eine sichere Position genügt |
| ds1 | Die Falle kostet `φ·ρ`, ein zwischengespeicherter Referenzwert spart | Die Falle kostet nicht weniger als eine Generierung des Ausführenden; der Cache muss zuerst beschafft werden |
| ds1, ds2 | Fallen fügen eine Fangung `φ` bei beliebigem `q` hinzu | Nicht mehr als `φ(1 − q)` bei einer Wiederholung; bei `q = 1` — 0 |
| claude1, claude2, mm3, mm4, STRATEGY_SEARCH | Fauler Zahler × Neuling = 0 | Bis `+R` |
| claude2 | Die Formel des Epochenbeispiels `(1 − p)(E − 1)R` | `(1 − p)·E·R − p·H_lock = 98,01R`; die Übereinstimmung ist zufällig |

### 7.3. Zweifelhafte Verweise (Schätzungen der Kritiker aus dem Gedächtnis, ohne Abgleich)

| Arbeit | Aussage | Bewertung |
|---|---|---|
| mm5 | „RandAILight“ als Leuchtturm | Zweifelhaft; der Name ist den Kritikern unbekannt |
| mm5 | „iO ist theoretisch möglich, Barak und Mitautoren ~2001“ | Verwechselt: Barak und Mitautoren 2001 — die Unmöglichkeit der Obfuskation einer „Blackbox“; Kandidaten für iO — Garg und Mitautoren 2013 |
| mm1 | „Die Roadmap von iO bei Barak und Mitautoren, 2019“ | Zweifelhaft |
| mm2 | Anhang F: „Ben-Or und Mitautoren“, „Allingham, Melvin, Temple 1992“, „Dwork ~1999“, „Hashcash — Homestein“, „Awasthi“, „Randcast Bader ~2020“ | Fast in allen Punkten zweifelhaft; nicht in die Zusammenfassung übernehmen |
| mm3 | „Cui, Wang u. a., Skoglid u. a.“ über Moving Target Defense | Zweifelhaft |
| ds1 | „Canetti 1997 — Punktfunktionen im Modell des zufälligen Orakels“ | Zweifelhaft (aus dem Gedächtnis — eine Annahme vom Typ DDH) |
| ds1 | „Bishop–Jain–Kowalczyk 2018“ | Zweifelhaft beim Jahr (aus dem Gedächtnis 2015) |
| ds1, ds2 | „drand ~30 s“ | Teilweise: aus dem Gedächtnis bei verschiedenen Ketten 30 s und 3 s |
| ds2 | „MPC 5,98·10¹² MAC (claude2)“ | Der Verweis ist ungenau |
| claude1 | „SGX.Fail, der Master-Schlüssel von Secret Network, 2022“ | In den Details zweifelhaft (der Autor hat es selbst markiert) |
| claude1 | Privacy Pass als Vorbild einer Emission ohne eine besondere Seite | Aus dem Gedächtnis — ein Schema mit einem Server-Aussteller |
| claude2 | Die untere Schranke von PIR — Beimel, Ishai, Malkin | Zweifelhaft: ihre Arbeiten betreffen PIR mit Vorverarbeitung; die klassische Schranke stammt aus dem Gedächtnis von Chor und Mitautoren |
| claude2 | Lowd–Meek, Tramèr: `d` binäre Anfragen genügen für jeden Klassifikator | In allgemeiner Form zweifelhaft |

Die übrigen Verweise der Arbeiten (Shamir, Feldman, Pedersen, Gennaro–Jarecki–Krawczyk–Rabin, Micali–Rabin–Vadhan, Boneh und Mitautoren über VDF, Rivest–Shamir–Wagner, Aumann–Lindell, Asharov–Orlandi, Inspektionsspiele, Barak und Mitautoren über die Unmöglichkeit einer „Blackbox“) erscheinen den Kritikern der Richtung nach richtig zugeordnet; die Primärquellen wurden nicht abgeglichen.

---

## 8. Wer was getan hat

Der Rat arbeitete nach den Materialien des Projekts, ohne Zugang zum Netz und ohne Experimente.

- **Elf unabhängige Arbeiten:** ChatGPT — zwei (gpt1, gpt2), DeepSeek — zwei (ds1, ds2), Claude — zwei (claude1, claude2), MiniMax — fünf (mm1 mit Schwerpunkt auf der Ökonomie, mm2 — auf dem Schutz vor Betrug, mm3 — auf der Verteiltheit und der Wiederherstellung, mm4 — auf Gegenbeispielen, mm5 — auf ungewöhnlichen Lösungen). Jede Arbeit behandelte sechs Richtungen aus dem Auftrag: wer den Schlüssel hält, wie man nach einer unbekannten Regel prüft, was ein geheimer Detektor sein kann, die Theorie, den Preis und die Vereinbarkeit mit den Entscheidungen.
- **Vier Kritiken:** je eine von ChatGPT, DeepSeek, Claude und MiniMax (die Kritik von MiniMax ist als Vorschlag mit Kritik gestaltet). Jeder Kritiker las alle elf Arbeiten, suchte Fehler und Gegenbeispiele und rechnete die Schlüsselzahlen nach. Der Kritiker DeepSeek prüfte die Arithmetik mit lokalen Programmen auf exakten Brüchen, der Kritiker Claude — mit kurzen Berechnungen in Python, der Kritiker ChatGPT reproduzierte den Kontroll-Hash der Tabelle von gpt1.
- **Zusammenfassung:** dieses Dokument stellte Claude nach den Arbeiten und Kritiken zusammen. Neue Bewertungen und Zahlen über die Arbeiten, die Kritiken, die Ergebnisse von D5 und STRATEGY_SEARCH hinaus wurden nicht hinzugefügt; wo die Kritiker sich trennten, ist das angegeben.
