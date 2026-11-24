<!-- translation of docs/STAGE4_KERNELS.md, source sha256: e81d4e27191f3ce009ea9b71602c58405e742a7229fc972d8c69ae520e675812 -->

# Phase 4. Bytegenauer Vertrag der eingebauten Berechnungen

[English](../../docs/STAGE4_KERNELS.en.md) · [中文](../zh/STAGE4_KERNELS.md) · [Español](../es/STAGE4_KERNELS.md) · [Français](../fr/STAGE4_KERNELS.md) · **Deutsch** · [Italiano](../it/STAGE4_KERNELS.md) · [Русский](../../docs/STAGE4_KERNELS.md) · [Português](../pt/STAGE4_KERNELS.md) · [العربية](../ar/STAGE4_KERNELS.md)

Stand vom 24. November 2026. Das Dokument legt die genauen Regeln der vier neuen eingebauten Berechnungen des Mini-Agenten (ab Version 1.2.0 des Agenten) für die Berechnungen M8, M10, M12 und M14 aus [VERIFICATION_SEARCH](VERIFICATION_SEARCH.md), Abschnitt 5.3, fest. Die Spezifikation und die Implementierung in Go schrieb ChatGPT; DeepSeek prüfte die Spezifikation unabhängig anhand der ursprünglichen Arbeiten des Rats und schrieb allein danach eine zweite Implementierung in Python ([tools/reference_stage4.py](../../tools/reference_stage4.py)); alle 73 Ergebnisse der Aufgaben stimmten bytegenau überein; Claude prüfte den Code und den Abgleich. Verweise der Form „claude1, §5.4“ bezeichnen die Arbeiten des Modellrats, die in VERIFICATION_SEARCH zusammengeführt sind. Das ist eine genaue Rechnung nach Formeln, keine Messung: Die Übereinstimmung bestätigt die Arithmetik, aber nicht die Annahmen der Modelle. Die Berechnungen M5, M7 und M18 sind zurückgestellt: In den Arbeiten fehlen die Regeln, um sie eindeutig zu bestimmen (Abschnitt „Zurückgestellte Berechnungen“).

| Berechnung aus §5.3 | Kern der Version 1 | Was sich aus einer unit erfahren lässt |
|---|---|---|
| M8 | `t4-scale` | Wie viele Trainings-Token je Knoten bei gegebener Zahl der Einreichenden nötig sind und wie viele Einreichende das Budget zulässt |
| M10 | `exam-thresholds` | In welchem rationalen Intervall jede der beiden Schwellen des Examens liegt |
| M12 | `merge-attribution` | Wie sich die Summe der Gutschriften an einen Teilnehmer beim Hinzufügen genauer oder verrauschter Kopien ändert |
| M14 | `verification-enumerations` | Welche Fälle die Prüfung des Bitpackings, der Kette oder der Feldgleichheit vollständig bestanden oder nicht bestanden haben |

Die Auswahl folgt aus der Tabelle des Rats in §5.3. Nach D18 bleibt die Bezahlung für die Verbesserung eine Forschungshypothese. Zur Wiederholung aller vier Berechnungen genügen die Eingabeparameter. [Ergebnis des Rats](VERIFICATION_SEARCH.md) · [Entscheidungen D18–D20](ROADMAP.md)

## Allgemeine Regeln der Version 1

In der zu signierenden Aufgabe werden der Name des Kerns und die Ganzzahl `kernel_version: 1` getrennt gespeichert. Die Eingabe `params` ist ein Objekt mit allen für den Kern aufgeführten Feldern. Überzählige und fehlende Felder, ein wiederholter JSON-Schlüssel, Werte außerhalb des Bereichs und falsche Typen führen zu einem Fehler. Eine Ganzzahl wird als ganzzahliges JSON-Literal geschrieben, ohne Dezimalpunkt und Exponent. Zeichenketten und Wahrheitswerte statt Zahlen sind nicht zulässig. Die Grenzen sind einschließlich. Die Achsen des Rasters behalten die Reihenfolge der Eingabe. Die Zahl der units entspricht genau der für den Kern angegebenen Größe des Rasters, von 1 bis 1 000 000. Die Nummer einer unit beginnt bei null. Im kartesischen Produkt ändert sich die letzte Achse am schnellsten.

Zum Abgleich wird das gesamte Ergebnisobjekt genommen. In Python sind die kanonischen Bytes gleich `json.dumps(result, sort_keys=True, ensure_ascii=True, separators=(',', ':')).encode('ascii')`, ohne abschließenden Zeilenumbruch. Der Hash des Ergebnisses ist SHA-256 dieser Bytes, 64 Hexadezimalziffern in Kleinbuchstaben. Die Reihenfolge der Elemente von Arrays ist bedeutsam. Ein Bruch wird in einer Zeichenkette im Dezimalsystem als `p/q` mit positivem Nenner nach dem Kürzen geschrieben, einschließlich `0/1` und ganzer Zahlen mit `/1`. Es gibt keine führenden Pluszeichen oder Nullen. Für M14 ist gesondert der Hash der Bytes *innerhalb* des Ergebnisses des Bitpackings definiert. [Kanonischer Kodierer des Agenten](../../agent-go/canon/canon.go)

## M8. Maßstab von T4 bei einer Aktualisierung von jedem Teilnehmer

`t4-scale@1` berechnet die minimale ganze Zahl von Token des eigenen Trainings je Runde, bei der das Examen nicht mehr als 20% der Berechnungen hinzufügt. Für ein gegebenes Token-Budget findet der Kern außerdem die Grenzzahl der Einreichenden. Im Modell prüft jeder Knoten alle `K=N` Aktualisierungen. Die Basis kostet einen Vorwärtsdurchlauf je Position, jede Aktualisierung der oberen Schichten einen Anteil `a=L_a/L` eines Durchlaufs, und das Training eines Tokens kostet drei Durchläufe. Diese Verhältnisse sind durch den Vorschlag vorgegeben. claude1, §5.4 „Preis“ und §7.5, Nr. 4 · critic_claude, §1.8 und §10.4, Nr. 3 · [VERIFICATION_SEARCH, §5.3, M8](VERIFICATION_SEARCH.md)

| Feld `params` | Zulässige Werte |
|---|---|
| `N` | Achse von Ganzzahlen von 1 bis 1 000 000. Zahl der Einreichenden in der Runde |
| `n` | Achse von Ganzzahlen von 1 bis 1 000 000. Zahl der Examenpositionen |
| `a` | Achse von Paaren ganzer Zahlen `[p,q]`, wobei `1 ≤ p ≤ q ≤ 1 000 000`. Anteil eines Durchlaufs je Aktualisierung |
| `D_budget` | Achse von Ganzzahlen von 1 bis 1 000 000 000 000. Budget der Trainings-Token je Knoten und Runde |
| `epsilon_bits` | Eine Ganzzahl von 1 bis 256. Legt `ε=1/2^epsilon_bits` für ein fixiertes Examen fest. Bei gegebenem `n` ist der Preis für alle `ε` gleich |

Alle fünf Felder sind obligatorisch. Jede Achse ist ein Array der Länge 1…32, die Werte sind unter Berücksichtigung des Kürzens von Brüchen eindeutig, die Reihenfolge des Eingabearrays bleibt erhalten. Die Zahl der units ist gleich dem Produkt der Längen der Achsen und überschreitet 1 000 000 nicht. Die Nummerierung beginnt bei null über das kartesische Produkt `N, n, a, D_budget` in der Reihenfolge verschachtelter Schleifen, am schnellsten ändert sich das Budget. Eine unit liefert ein Objekt.

Für den gewählten Punkt setzen wir `D=D_budget` und kürzen `a=p/q`. Wir messen die Berechnungen in Einheiten von `1/q` eines Vorwärtsdurchlaufs je Position. Dann erfordert das Examen `E=n(q+Np)`, das Training erfordert `W=3Dq`, der Anteil des Overheads ist gleich `E/W`. Die Division durch den Umfang des eigenen Trainings folgt aus der Formulierung „Aufschlag“ in §5.4. Die Bedingung von 20% ist äquivalent zu `5E ≤ W`.

| Ergebnisfeld | Wert |
|---|---|
| `kernel` | Zeichenkette `t4-scale@1` |
| `N`, `n`, `D_budget` | Ganzzahlen des Eingabepunkts |
| `a`, `epsilon` | Gekürzte Zeichenketten `p/q`; `epsilon` wird als `1/q` geschrieben, wobei `q = 2^epsilon_bits` eine Dezimalganzzahl ist (zum Beispiel `"1/4"` bei `epsilon_bits = 2`) |
| `D_min` | Ganzzahl `(5E + 3q − 1) // (3q)`, wobei `//` die ganzzahlige Division abwärts ist. Das ist die Aufrundung der Schwelle auf ein ganzes Token |
| `fits` | Wahrheitswert `D_budget ≥ D_min`. Gleichheit wird als erfüllt gezählt |
| `N_max` | `null`, wenn `W < 5nq` und selbst der Basisdurchlauf das Budget überschreitet. Sonst die Ganzzahl `(W − 5nq) // (5np)`. Null bedeutet, dass nur die Basis hineinpasst. Die Grenze kann über die Eingabeachse `N` hinausgehen |
| `overhead` | `E/W` als gekürzte Zeichenkette `Zähler/Nenner` |

Die Schranke in umgekehrter Richtung folgt aus der linearen Ungleichung `5npN ≤ W − 5nq` bei positivem `p`. Bei zulässigen Parametern gilt `5E+3q−1 ≤ 5 000 005 000 002 999 999`, `W ≤ 3·10^18`. Die Nenner sind positiv. Vorzeichenbehaftete 64-Bit-Ganzzahlen und das Kürzen des Bruchs über den ggT genügen. In Go wird für `overhead` `big.Rat` verwendet, für `2^epsilon_bits` `big.Int`. Auf eine unit entfallen das Einlesen von höchstens 128 Elementen der Achsen und eine konstante Zahl arithmetischer Operationen.

Für `n=3, N=4, a=1/2` kostet das Examen 9 Durchläufe, bei 15 Trainings-Token nimmt es genau ein Fünftel ein. Bei 14 Token sinkt die Grenze auf drei Einreichende. Bei `epsilon_bits=2` ergeben sich die folgenden kanonischen Bytes.

```json
{"D_budget":15,"D_min":15,"N":4,"N_max":4,"a":"1/2","epsilon":"1/4","fits":true,"kernel":"t4-scale@1","n":3,"overhead":"1/5"}
```

Für den Richtwert aus §5.4 bei `n=100000, N=10000, a=4/36` ist das genaue Minimum gleich 185 351 852 Token. Der physische Preis hängt von der Wiederverwendung von Präfixen, dem Umfang des Caches, dem Ausgangskopf, der Normierung, dem Traffic und dem tatsächlichen Preis des Trainings der oberen Schichten ab. Die Formel umfasst nur die in §5.4 beschriebene Zählung der Durchläufe. Zur Schätzung der statistischen Schwelle bei Änderung von `ε` dient M10. Die vorgeschlagene Aufgabe setzt `ε=2^-80` gemäß dem numerischen Richtwert D19. critic_gpt, Abschnitt über claude1, „Der verborgene Preis von T4“ · [ROADMAP, D18–D19](ROADMAP.md)

## M10. Schwelle des Examens T4 — `exam-thresholds@1`

M10 bestimmt, wie groß die mittlere beobachtete Verbesserung im Examen sein muss, damit sie die statistische Schwelle überschreitet. Für einen im Voraus fixierten Kandidaten werden `n` unabhängige Positionen mit Zurücklegen genommen. Die Verlustdifferenz an jeder Position wird auf `[−B/2, B/2]` beschnitten. Die Eingabe `V` ist die Stichprobenvarianz der beschnittenen Differenzen mit dem Divisor `n−1` (das Quadrat der Standardabweichung). Die Grenzen in nat je Position stammen aus Schritt 6 der Beschreibung von T4. claude1, §5.4 · Kritiker Claude, §1.8

| Methode | Genäue Schwelle `t` |
|---|---|
| Hoeffding | `B·√(ln(1/ε)/(2n))` |
| Empirische Bernstein-Ungleichung | `√(2V·ln(2/ε)/n) + 7B·ln(2/ε)/(3(n−1))` |

**Parameter und units.** Fünf Felder sind obligatorisch. Die Felder `n`, `epsilon_bits`, `B`, `variance` sind Achsen der Länge 1 bis 32, jede in der Reihenfolge des Eingabearrays. Die Werte auf einer Achse sind verschieden, Brüche werden nach dem Kürzen verglichen.

| Feld | Zulässige Werte |
|---|---|
| `n` | Zahl der Positionen, Ganzzahl von 2 bis 1 000 000 |
| `epsilon_bits` | Ganzzahl `k` von 1 bis 128, `ε = 2⁻ᵏ` je Vergleich |
| `B` | Breite des Beschnittbereichs, Ganzzahl von 1 bis 64 |
| `variance` | Bruch `[p,q]`, Ganzzahlen `0 ≤ p ≤ 10⁶` und `1 ≤ q ≤ 10⁶`. An allen Punkten des Rasters `V=p/q ≤ B²·floor(n/2)·ceil(n/2)/(n(n−1))` |
| `digits` | Eine Ganzzahl `d` von 1 bis 9. Die garantierte absolute Breite jedes Intervalls ist kleiner als `10⁻ᵈ` |

Das Maximum der Varianz wird an den Enden des Bereichs erreicht, da die Varianz in jeder Beobachtung konvex ist. Bei `j` Werten an einem Ende ist ihr Zähler proportional zu `j(n−j)`, was die angegebene Schranke ergibt. Die Zahl der units ist gleich dem Produkt der Längen der vier Achsen und überschreitet 1 000 000 nicht. Die Nummerierung entspricht `itertools.product(n, epsilon_bits, B, variance)` und beginnt bei null.

**Algorithmus der bytegenauen Wiederholung.** Für beide Methoden ist `t = √(A·ln 2) + C·ln 2` zu schreiben. Bei Hoeffding `A=B²k/(2n), C=0`. Bei Bernstein `A=2V(k+1)/n, C=7B(k+1)/(3(n−1))`. Alle Divisionen hier sind rational.

1. `S=10^(d+1)`, `l=693147180559945309/10¹⁸`, `h=693147180559945310/10¹⁸` nehmen.
2. Die untere Schranke ist gleich `(floor(√(S²Al)) + floor(SCl))/S`. Die obere ist gleich `(ceil(√(S²Ah)) + ceil(SCh))/S`. Beide Summanden werden **einzeln** gerundet.
3. Für einen nichtnegativen Bruch `x=p/q` ist `r=isqrt(p//q)` zu berechnen. Das ist `floor(√x)`. Für die obere Schranke ist zu `r` genau dann eins zu addieren, wenn `r²q < p`. Die gewöhnlichen `floor` und `ceil` werden ebenfalls durch ganzzahlige Division ausgeführt. Alle erhaltenen Brüche werden gekürzt.

**Genauigkeitszertifikat.** Aus der Reihe für `2·atanh(1/3)=ln 2` nehmen wir `T=2·Σ 1/(j·3ʲ)` über ungerade `j=1,3,…,39`. Der Rest ist positiv und durch das erste weggelassene Glied, multipliziert mit `1/(1−1/9)`, beschränkt. Durch einen ganzzahligen Vergleich erhalten wir `l < T < ln 2 ≤ T + 9/(4·41·3⁴¹) < h`. Die Monotonie beider Summanden und die gerichtete Rundung gewährleisten die Einschließung der wahren Schwelle. Im vorgegebenen Bereich gilt `A ≤ 264192` und `C ≤ 19264`. Da `√h+√l > 1`, ändert der Austausch von `l` durch `h` die ungerundete Schwelle um weniger als `(515+19264)·10⁻¹⁸`. Die Rundung erweitert das Intervall um weniger als `4/S`. Die Summe ist kleiner als `10⁻ᵈ` auch bei `d=9`. Je unit genügen vier ganzzahlige Quadratwurzeln und eine konstante Zahl von Operationen über Ganzzahlen und Brüche von einigen hundert Bit, unabhängig von `n`.

**Antwort.** Die Felder `n`, `epsilon_bits`, `B` und `digits` sind ganzzahlige Koordinaten und die Genauigkeit. `variance` ist eine Zeichenkette mit einem gekürzten Bruch. `hoeffding` und `bernstein` sind Arrays aus zwei solchen Zeichenketten, die untere Schranke an erster Stelle. Für `n=2, k=1, B=2, V=0, d=1` liefert der Kern die folgenden kanonischen Bytes.

```json
{"B":2,"bernstein":["323/50","647/100"],"digits":1,"epsilon_bits":1,"hoeffding":["83/100","21/25"],"kernel":"exam-thresholds@1","n":2,"variance":"0/1"}
```

Für eine vorgegebene Grenzschwelle `τ` ist der minimale Umfang des Examens **auf dem Raster** dann festgelegt, wenn am gewählten Punkt die obere Schranke `≤ τ` ist und bei allen kleineren `n` mit denselben Parametern die untere Schranke `> τ` ist. Wenn das Intervall das Ziel schneidet, kann eine größere Genauigkeit nötig sein. Die Zahlen kennzeichnen einen einseitigen Vergleich des gestutzten Mittels bei Fixierung vor dem externen Beacon. Die Korrektur für die Auswahl unter mehreren Kandidaten, die Qualität außerhalb des Examens, die Wahl von `τ` und die Größe des realen Effekts verlangen gesonderte Daten oder Regeln. Die Auszahlung für die Verbesserung bleibt nach D18 eine Forschungsvariante. [ROADMAP, D18–D20](ROADMAP.md) · Kritiker GPT, Einschätzung von T4

## M12. Wie sich die Gutschrift des Eigentümers der Duplikate bei der Fusion durch Summe ändert

In der Arbeit zu M12 sind linear-quadratische Verluste mit bekanntem Gradienten und bekannter Hesse-Matrix, drei Attributionsregeln, genaue Duplikate und Duplikate mit Rauschen angegeben. Wir wählen die in §5.4 ausdrücklich behandelte Variante `merge = sum`. Der Kritiker führt einen Fall an, in dem selbst das wiederholte Hinzufügen desselben Schritts die Verlustfunktion verbessert. Der Kern `merge-attribution@1` prüft dies an ausdrücklichen Eingabekoeffizienten. claude1, §5.4, Schritte 6–7 und Nr. 2 „Attribution und Duplikate“, §7.5, Nr. 7 · critic_gpt, Tabelle über claude1, Zeile T4

| Feld `params` | Bedeutung und einschließende Grenzen |
|---|---|
| `scale` | Gemeinsamer Nenner `s`, Ganzzahl 1…10 000 |
| `g` | Vektor der Zähler des Gradienten im Basispunkt. Seine Länge legt die Dimension `d` fest, 1…8 |
| `hessian` | Symmetrische Matrix der Zähler der Hesse-Matrix, ein Array aus `d` Zeilen mit je `d` Komponenten |
| `updates` | Array aus `b=1…8` ursprünglichen Vektoren von Zählern der Länge `d`, in der Reihenfolge der Einreichung. Gleiche Vektoren sind zulässig |
| `owner` | Ganzzahliger Index der ursprünglichen Einreichung des geprüften Teilnehmers, von 0 bis `b−1`. Die übrigen ursprünglichen Einreichungen gehören anderen Teilnehmern |
| `copies` | Achse aus 1…8 verschiedenen Ganzzahlen 1…8. Das gewählte `c` legt die Zahl der hinzugefügten Einreichungen desselben Teilnehmers fest |
| `noise` | Achse aus 1…32 paarweise verschiedenen Vektoren von Zählern der Länge `d`. Der Nullvektor ergibt ein genaues Duplikat |
| `threshold` | Ganzzahliger Zähler 0…10 000 für den Abzug `t=threshold/s` von der Bewertung jeder Einreichung |

Jede Komponente von `g`, `hessian`, `updates` und `noise` ist eine Ganzzahl von −10 000 bis 10 000. Um den mathematischen Wert jeder Komponente zu erhalten, ist sie **ein einziges Mal** durch `s` zu teilen, auch bei der Matrix. Die Version unterstützt rationale Koeffizienten mit gemeinsamem Nenner im angegebenen Bereich. Die Symmetrie ist obligatorisch, das Vorzeichen der Krümmung ist beliebig. Die Eingabeachsen `copies, noise` bilden ein Raster. Für die unit `u` sind die Indizes `divmod(u,len(noise))` entsprechend zu nehmen. Nach den ursprünglichen `b` Einreichungen sind `c` Vektoren hinzuzufügen, jeder gleich `updates[owner] + noise[j]` in den Zählern. Die ursprünglichen Vektoren bleiben erhalten. Die Mengen der Einreichungen vor und nach dem Hinzufügen werden getrennt betrachtet.

**Berechnung.** Sei `U` die Menge der Indizes der Einreichungen einer Menge und `x(S)` die Summe ihrer **mathematischen** Aktualisierungsvektoren über die Teilmenge `S`. Der Gewinn an Verlusten ist als Senkung gegenüber der gemeinsamen Basis definiert,

```text
v(S) = −gᵀx(S) − x(S)ᵀ H x(S)/2,     v(∅) = 0.
```

Für jeden Index `i` sind drei **vorzeichenbehaftete** Bewertungen zu berechnen. `separate[i]=v({i})`. Die Regel des Ausschlusses eines Elements, `loo[i]=v(U)−v(U без i)`. Die Bewertung `shapley[i]` ist gleich dem mittleren Zuwachs `v(S∪{i})−v(S)` über alle Permutationen der Indizes, wobei `S` aus den Vorgängern von `i` besteht. Diese Regel wird auf die vollständige Funktion der Verlustsenkung angewandt. Zur Berechnung ohne faktorielles Durchprobieren setzen wir `q_i=v({i})`, `h_ij=−x_iᵀ H x_j`. Die Symmetrie ergibt `v(S)=Σ q_i + Σ_{i<j} h_ij` über die Teilnehmer in `S`. Beim Ausschluss eines Teilnehmers verschwinden alle seine Paarterme. In einer gleichverteilten Permutation steht jeder andere Teilnehmer genau in der Hälfte der Fälle vor ihm. Daher

```text
loo[i]     = q_i + Σ_{j≠i} h_ij
shapley[i] = q_i + (Σ_{j≠i} h_ij)/2
v(U)       = Σ shapley[i].
```

Danach wird für jede Regel gesondert die Bewertung `z` in eine Gutschrift `max(0,z−t)` in Einheiten der Verbesserung umgerechnet (der Vergütungskoeffizient κ wird als eins angenommen). Zuerst wird je Einreichung gutgeschrieben, dann werden die Gutschriften des Eigentümers addiert. `gain` ist die Gutschrift an den Eigentümer für seine ursprüngliche und alle hinzugefügten Einreichungen nach dem Hinzufügen minus die Gutschrift für seine eine Einreichung vor dem Hinzufügen. Ein positives Vorzeichen bedeutet in diesem Beispiel einen Gewinn aus zusätzlichen Einreichungen.

**Format der Antwort.** Die Schlüssel `kernel` (Zeichenkette `merge-attribution@1`), `owner`, `scale`, `copies` (die gewählte Ganzzahl aus der Achse), `noise` (der gewählte Vektor ganzer Zähler), `baseline`, `with_copies` und `gain`. Jedes der Objekte `baseline` und `with_copies` enthält `value` — den Bruch `v(U)` — und die Felder `separate`, `loo`, `shapley` — Arrays von Brüchen in der Reihenfolge der Indizes der Einreichungen. Das Objekt `gain` enthält je einen Bruch unter jedem der drei Regelnamen. Alle Ausgabebrüche sind kanonische Zeichenketten.

**Arithmetik und Grenzen.** Der gemeinsame Nenner der Zwischenbewertungen ist `2s³`. Wenn `G, A, z_i` die eingegebenen ganzzahligen Zähler des Gradienten, der Hesse-Matrix und des Schritts sind, ist der Zähler von `q_i` gleich `−2s Gᵀz_i−z_iᵀAz_i`. Der Hälfte des Paarterms entspricht der ganzzahlige Zähler `−z_iᵀAz_j`. Der Zähler des Abzugs ist gleich `2s²·threshold`. Nach dem Hinzufügen gibt es bis zu 16 Einreichungen, und `|z_ij| ≤ 20 000`. Daraus folgt `|z_iᵀAz_j| ≤ 8²·20 000²·10 000 = 2,56·10¹⁴`, der lineare Teil beträgt im Betrag höchstens `3,2·10¹³`. Selbst die Summe von 16 vollständigen LOO-Bewertungen und Abzügen ist im Betrag kleiner als `1,3·10¹⁷`. Alle Multiplikationen und Teilsummen passen in vorzeichenbehaftete 64 Bit. Die Implementierung kürzt Brüche über `big.Rat`. Zeit `O(k d²+k²d)` bei `k ≤ 16`, ohne Tabelle der Teilmengen. Der Speicher ist durch die Eingabevektoren, die Matrix, drei Bewertungen je Einreichung und das Ergebnis begrenzt.

**Manuelle Prüfung.** Bei `v(x)=3x−x²/2`, einer Einreichung `x=1` und einer Schwelle von null ist die ursprüngliche Bewertung nach allen Regeln gleich `5/2`. Nach einem genauen Duplikat ist `v(2)=4`. Die Regeln ergeben je Einreichung `5/2` einzeln, `3/2` beim Ausschluss und `2/1` nach Shapley. Der Gesamtgewinn des Eigentümers ist entsprechend `5/2`, `1/2`, `3/2`. Dieses eine Beispiel genügt, um die Abwesenheit eines Gewinns für jede der drei Regeln in der gesamten Familie solcher Modelle bei einer Schwelle von null zu widerlegen.

**Bereich der Aussage.** Die Menge der Teilnehmer des Vergleichs ist fixiert. Das Rauschen ist durch einen ausdrücklichen Vektor vorgegeben, die Schwelle durch die Eingabe. Die Annahme, die erneute Auswahl der Zusammensetzung nach dem Abzug der Schwelle, die Kosten der Einreichung, das Training der Parameter, externe Effekte und das empirische Examen liegen außerhalb dieses Modells. Der numerische Gewinn bezieht sich auf die Summe der Gutschriften nach der gewählten Regel. Die vollständige Prüfung von D1 verlangt, die Nützlichkeit der Koalition auch mit ehrlicher Arbeit und mit Untätigkeit zu vergleichen. [THREAT_MODEL, §§1.4–1.5](THREAT_MODEL.md) · [ROADMAP, D18 und D25](ROADMAP.md)

## M14. Prüfung der Formeln durch endliche Aufzählung

Der Kern `verification-enumerations@1` wiederholt drei kleine Experimente. Es erlaubt zu prüfen, ob das Bitpacking den Unterschied zwischen zulässigen Vektoren erhält und wie viele Fehler zwei Arten der Stichprobenprüfung durchlassen. Die Ausgangsdaten, die Reihenfolge der Aufzählung und die Referenzhashes sind in GPT2, §6.2 und „Kontrollcode für die erste Wiederholung“ veröffentlicht. Die Kette ist in der Tabelle „Was man den Mini-Agenten übergibt“ vorgegeben, die Bedingung des Durchlasses im Feld in §6.1. Arbeit GPT2 · [Zusammenfassung, §5.3](VERIFICATION_SEARCH.md)

Der einzige Parameter `cases` ist ein Array aus 1–4 verschiedenen Zeichenketten aus der Tabelle unten. `units = len(cases)`. Die Nummerierung beginnt bei null, die unit `u` berechnet das gesamte Experiment `cases[u]`. Der Schlüssel `case` des Ergebnisses enthält dieselbe Zeichenkette, `kernel` ist gleich `"verification-enumerations@1"`. Das Format der übrigen Felder hängt vom Experiment ab.

| `case` | Ergebnisfelder außer `case` und `kernel` | Kontrollwerte |
|---|---|---|
| `packing-8` | Ganzzahlen `total`, `true_accepts`, `false_accepts`, Zeichenkette `verdict_sha256` | 441, 9, 0, `a5c8a8d715fb5293a4dd12753d3483e848f63cb24891a3e584bfdc81954f377c` |
| `packing-4` | Dieselben Felder | 441, 9, 20, `fca92fea5a3148177517b737591e499ed021432078bd9803578a2eaad4074fc9` |
| `chain-8-2` | Ganzzahlen `total`, `caught`, `missed` | 224, 56, 168 |
| `field-5` | Ganzzahlen `total`, `caught`, `missed` | 25, 20, 5 |

**Bitpacking.** Die Basis `B` ist aus der Bezeichnung des Experiments zu nehmen. `(x,y,c,d)` ist lexikographisch aufsteigend aufzuzählen, wobei `x,y ∈ {−1,0,1}`, `c,d ∈ {−3,…,3}`. Die innere Schleife ändert `d`. Das wahre Ergebnis ist `(s,t)=(2x−y,−x−y)`. Das Annahmekriterium ist die Teilbarkeit von `(c−s)+B(d−t)` durch `B²` über den ganzen Zahlen. Bei Übereinstimmung `(c,d)=(s,t)` erhöht die Annahme `true_accepts`, in den übrigen Fällen der Annahme `false_accepts`. In der Reihenfolge der Aufzählung sind genau 441 Bytes zu schreiben, jedes mit dem Wert 1 bei Annahme und 0 bei Ablehnung. `verdict_sha256` ist SHA-256 dieser rohen Bytes in Form von 64 Hexadezimalziffern in Kleinbuchstaben. Der gewöhnliche Hash des Ergebnisses der unit wird gesondert vom gesamten kanonischen JSON berechnet. Zur manuellen Prüfung ergeben bei `B=4`, `x=−1`, `y=1` die wahre Antwort `(−3,0)` und die Einreichung `(1,−1)` die Differenz 0.

**Kette.** Für jeden einzelnen Defekt `h=0,…,7` sind alle ungeordneten Paare ohne Zurücklegen als `0 ≤ i < j < 8` aufzuzählen. `total` ist um 1 je Tripel zu erhöhen, `caught` — wenn `h=i` oder `h=j`. Die Zahl der Durchlässe ist gleich `missed=total−caught`. Für jedes `h` gibt es 28 Paare, von denen genau 7 `h` enthalten.

**Feld.** Die Vektoren `(x,y)∈{0,…,4}²` sind aufzuzählen, einschließlich des Nullvektors. Der Fehler `(1,−1)` wird genau dann durchgelassen, wenn `(x−y) mod 5 = 0`. `total` zählt alle Vektoren, `missed` zählt die Durchlässe, `caught=total−missed`. Fünf diagonale Paare ergeben fünf Durchlässe.

Die längste unit prüft 441 Kombinationen und speichert 441 Bytes von Urteilen für einen SHA-256. Die Zähler überschreiten 441 nicht, der Betrag des Ausdrucks des Bitpackings überschreitet 46 nicht, der größte Betrag einer Division ist gleich 64. Vorzeichenbehaftete 32-Bit-Ganzzahlen genügen. Die Ergebnisse beziehen sich auf die angegebenen Bereiche, einen einzigen fixierten Fehler und die vollständige Aufzählung gleichwahrscheinlicher Varianten. Eine Verallgemeinerung auf ein reales Protokoll würde erfordern, die Verteilung der Aufrufe und die Unabhängigkeit der Prüfungen zu begründen.

## Zurückgestellte Berechnungen


| Berechnung | Was bereits festgelegt ist | Welche Daten ein eindeutiges Ergebnis ermöglichen |
|---|---|---|
| M5. Fälschungswellen | Für eine einzige billige Fälschung mit Kosten von null gilt `π=m_s/(L+1)` und `H*=R(1/π−1)`. Zum Beispiel ist bei `L=36, m_s=2` die Schwelle gleich 17,5R | Für eine Welle muss die gemeinsame Verteilung der Prüfungen und der Übergang des Kontostands bei mehreren gleichzeitigen Entdeckungen festgeschrieben werden, einschließlich des Zeitpunkts der Abbuchung und der Verfügbarkeit der Belohnungen der vorherigen Welle. Bei `π=1/2` lässt eine gemeinsame Stichprobe für zwei gleiche Fehler beide mit Wahrscheinlichkeit 1/2 durch, unabhängige Stichproben — mit Wahrscheinlichkeit 1/4. Die vorgeschlagene Analogie zu `exit-scam-a` verlangt außerdem zu klären, ob seine gesonderte Wahrscheinlichkeit der Zuweisung einer Prüfung erhalten bleibt. (claude1, §1.3, §4.2 und §7.5, Nr. 3) (THREAT_MODEL, §1.8) |
| M7. Ökonomie der Offenlegung | Für eine fixierte Auszahlung R und eine Vergütung des Beweises nur im erfolgreichen Zweig ist der Ertrag eines Versuchs `p(R−Pe)−c_view−c_commit` bekannt | Für die allgemeine Grenze ε sind der Preis eines verworfenen Versuchs, die Auszahlungsregel bei mehreren Erfolgen und das gemeinsame Verteilungsgesetz der Ausgänge der Kandidaten in einem gemeinsamen Examen nötig. Die Zahl der Schlüssel bestimmt diese Größen für sich allein nicht. ODU mit einem obligatorischen Beweis jedes Versuchs ergibt ein anderes Budget, und bei T4 hängt die Auszahlung zusätzlich von der Größe der Verbesserung ab. (claude2, §5.3) (critic_claude, §2.4) (critic_gpt, Analyse von ODU) |
| M18. Auszahlungen und Wiederherstellung | Vorgegeben sind die Atomarität der Annahme, die einmalige Einlösung des Rechts in der kanonischen Historie und die Liste der Szenarien | Zur Zählung der Pfade sind eine Übergangstabelle beim Wechsel des Zweigs, ein Finalitätskriterium, Regeln der Wiederherstellung beim Verschwinden und Zurückkehren von Daten und eine endliche Grenze der Zahl wiederholter Vorlage nötig. Verschiedene Automaten können dieselben Invarianten erfüllen und verschiedene Zahlen von Auszahlungen über Zwischenhistorien ergeben. (gpt1, §1 und §7) (critic_gpt, „Vollständigkeit, Wiederherstellung und Preis“) |
