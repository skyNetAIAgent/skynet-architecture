<!-- translation of docs/STRATEGY_SEARCH.md, source sha256: 9c3fdac8710ac98433828b793ab6aad7fd31da5661c1fecb590bb7c63a2cdd26 -->

# Prüfung ohne Holzhammermethode: Was Mathematik statt vollständiger Neuberechnung leistet

[English](../../docs/STRATEGY_SEARCH.en.md) · [中文](../zh/STRATEGY_SEARCH.md) · [Español](../es/STRATEGY_SEARCH.md) · [Français](../fr/STRATEGY_SEARCH.md) · **Deutsch** · [Italiano](../it/STRATEGY_SEARCH.md) · [Русский](../../docs/STRATEGY_SEARCH.md) · [Português](../pt/STRATEGY_SEARCH.md) · [العربية](../ar/STRATEGY_SEARCH.md)

Stand vom 25. November 2026.

Dieses Dokument ist das Ergebnis des fünften Modellrats. Der Eigentümer des Projekts fragte wörtlich:

> „Vielleicht ist es sinnvoll, eine andere Strategie zu wählen? Zum Beispiel irgendeine
> Mathematik einzubeziehen? Um nicht alles der Reihe nach zu prüfen, sondern einen Betrugsversuch
> vorherzusagen und nur in diesem Fall zu prüfen? Oder eine intelligente Analyse der Arbeit des Netzes
> SkyNet durchzuführen und verdächtiges Verhalten zu finden? Denken Sie in dieser Richtung nach, was es in der Wissenschaft noch gibt, das helfen kann, nicht mit dem Holzhammer zu lösen.“

Der Rat untersuchte die Theorie der Inspektionsspiele, die risikobasierte Prüfung, die Anomaliesuche, Fallen, die Stichprobenprüfung, Mechanismen ohne Prüfung, Kryptografie und die Ökonomie ohne Pfänder und schlug dann eine Strategie und Fassungen von Entscheidungen vor.

**Status des Dokuments.** Dies ist das Ergebnis von Überlegung und Berechnung nach Formeln, keine Messung. Experimente, Netzstarts und Installationen gab es dafür nicht. Die Teilnehmer und Kritiker führten nur kurze Arithmetikprogramme und kleine Aufzählungen auf dem Prozessor aus. Gemessene Zahlen stammen nur aus den [Ergebnissen des Experiments D5](EXPERIMENT_D5.md) (Zusammenfassung D5_RESULTS vom 25. November 2026) und sind mit [gemessen] gekennzeichnet; Zahlen, die nach Formeln aus ausdrücklich genannten Parametern gewonnen wurden, sind mit [Berechnung] gekennzeichnet. Die Arbeiten der Wissenschaftler sind **aus dem Gedächtnis** genannt: Es gab kein Netz, die Texte der Primärquellen wurden nicht abgeglichen. **Angenommene Entscheidungen sind nur die Entscheidungen D1–D25** in [ROADMAP](ROADMAP.md), Abschnitt 3. Alles Übrige hier ist eine Einschätzung und Empfehlung des Rats. Wo die Kritiker sich widersprachen, ist das ausdrücklich gesagt.

## 1. Kurzes Fazit

1. **„Betrug vorhersagen und nur die Verdächtigen prüfen“ spart bei offenen Regeln keine Prüfungen.** Die Prüfregeln sind bei allen Knoten gleich und dem Betrüger bekannt (D4). Er reicht eine Fälschung nur dort ein, wo der Detektor „sicher“ sagt, und bis zum Betrugszeitpunkt verhält er sich wie ein ehrlicher Teilnehmer. Streng bewiesen: Der Detektor hebt die Wahrscheinlichkeit der Prüfung einer Fälschung über die durchschnittliche Prüfung ehrlicher Arbeit um nicht mehr als den Abstand zwischen ihren beobachtbaren Verteilungen an (Abschnitt 2). Daher können Prognose, Anomalien, Vertrauen aus der Historie und Graphen nur **zusätzliche** Prüfungen über der unteren Schranke **hinzufügen**, aber die Häufigkeit nicht unter sie senken. Dem stimmen alle sechs Arbeiten und alle drei Kritiker zu.
2. **Es gibt genau zwei nicht fälschbare Merkmale:** das Ergebnis einer exakten Neuberechnung, nachdem die Antwort unwiderruflich fixiert wurde, und der verbrennbare Betrag im Ausstand — noch nicht ausgezahlte Belohnungen des Schlüssels, die bei einer Entdeckung verloren gehen. Die gesamte reale Ersparnis stammt aus dem zweiten Merkmal, nicht aus „Intelligenz“.
3. **Die beste gefundene Strategie für Modellantworten:** Der Zahler prüft seine Antwort selbst in einem Durchlauf und trifft die Entscheidung „prüfen oder nicht“ **mit seiner geheimen Münze** nach der Fixierung der Antwort, mit einer Wahrscheinlichkeit nicht unter `R/(R + H_lock)`. Dabei ist `R` der Preis der Aufgabe, `H_lock` der Teil der noch nicht ausgereiften Belohnungen des Ausführenden, der bis zum Ende der Prüfung nicht ausreifen wird. Die Antwort eines Neulings mit leerem Konto wird immer geprüft. Dann ist unter den Bedingungen von Abschnitt 4 eine Fälschung bei keinem Abspracheanteil der Übrigen vorteilhaft, auch nicht bei vollständiger Absprache. Diese Strategie unterstützen zwei von drei Kritikern; der Kritiker ChatGPT bevorzugt die vollständige Prüfung jeder Antwort (Abschnitt 6).
4. **Der Preis der Prüfung selbst beträgt dabei Bruchteile eines Prozents:** etwa 0,005–2% der Arbeit je nach Zeitplan und Belastung des Schlüssels, bei wenig aktiven Schlüsseln mit Schadensbegrenzung — bis 6,7% [Berechnung]. Der Hauptpreis geht in das exakte Profil über: Es ist 1,5–1,8 Mal langsamer als die gewöhnliche 8-Bit-Generierung bei Batch 1 und 2,5–2,8 Mal bei Batch 8 [gemessen]. Zusammen sind das +50…+82% gegenüber der gewöhnlichen Generierung bei Batch 1 [Berechnung]. Der Richtwert von 5% stößt an die Geschwindigkeit des exakten Profils, nicht an die Prüfung.
5. **Der Schaden lässt sich durch Ökonomie nicht schließen.** Ein Saboteur braucht keinen Gewinn: Bei der Stichprobenprüfung kommt ein Teil seiner Fälschungen durch (etwa die Hälfte beim billigsten Zeitplan, Abschnitt 4). Deshalb muss eine ungeprüfte Antwort die Markierung „nicht geprüft“ tragen, und „geprüft“ wird erst nach vollständiger Prüfung vor der Anzeige gesetzt. Für den Trainingsschritt hat der Rat keine neue Garantie gefunden.
6. **Ein Nutzer ohne Ausrüstung** ist durch diese Strategie nicht geschützt: Wenn für ihn zufällige fremde Knoten prüfen, beträgt die Leckage `R·q^k` und bei vollständiger Absprache — den gesamten Preis (Abschnitt 5). Das bleibt die offene Frage D21.
7. **Was der Eigentümer entscheiden muss:** ob die Bezahlung des Ungeprüften nach der Münzregel erlaubt wird (D21, D11, D7); was mit kostenlosen ehrlichen Ausfällen geschieht (D16), die mit der Stichprobenprüfung unvereinbar sind; ob die neue Entscheidung D26 über die „Sperre“ des Betrags im Ausstand und die Obergrenze der Rückerstattung an den Geschädigten angenommen wird; die Regel für falsche Streitfälle (D23, Berechnung M9) bleibt Bedingung für die Inbetriebnahme. Die Fragen sind in Abschnitt 6 formuliert.

**Bezeichnungen.** `R` — Preis der Aufgabe; `c` — Selbstkosten ehrlicher Arbeit; `c_f` — Kosten der Fälschung (schlimmster Fall — fast null); `H` — ausstehender Betrag des Schlüssels des Ausführenden; `H_lock` — sein Teil, der bis zum endgültigen Ergebnis der Prüfung dieser Aufgabe nicht ausreift; `p` — Wahrscheinlichkeit der Prüfung einer Aufgabe; `q` — Abspracheanteil unter den Prüfern; `k` — Zahl der zugewiesenen Prüfer; `n_w` — Zahl der Aufgaben des Schlüssels je Ausreifungsfenster; `ρ` — Zeit der Prüfung einer Antwort in einem Durchlauf, geteilt durch die Zeit ihrer Generierung (0,10–0,40 bei Batch 1, 0,26–0,64 bei Batch 8 [gemessen]); `γ` — Verlangsamung des exakten Profils gegenüber llama.cpp Q8_0 (1,5–1,8 bei Batch 1, 2,5–2,8 bei Batch 8 [gemessen]); PPS — Prüfung durch den Zahler selbst. `Δ₀` und `Δч` — erwartete Differenz des Gewinns einer Fälschung gegenüber Untätigkeit und gegenüber ehrlicher Arbeit; D1 und D25 verlangen, dass beide nicht größer als null sind.

**Wie man liest.** Abschnitt 2 — warum die Betrugsprognose nicht funktioniert. Abschnitt 3 — eine Tabelle aller Ansätze. Abschnitt 4 — Formeln, die der Kritik standhielten, und gefundene Fehler. Abschnitt 5 — die empfohlene Strategie, ihr Preis und das Restrisiko. Abschnitt 6 — Fragen und Entscheidungen. Abschnitt 7 — Berechnungen und Experimente. Abschnitt 8 — ungelöste Meinungsverschiedenheiten und zweifelhafte Verweise. Abschnitt 9 — wer was getan hat.

## 2. Warum „Betrug vorhersagen“ bei offenen Regeln nicht funktioniert

### 2.1. Schranke über die totale Variation

Es treffe ein beliebiges Regelwerk `π(x)` mit Werten von 0 bis 1 die Prüfentscheidung, wobei `x` alles ist, was das Netz oder der Zahler vor der Entscheidung sieht: Antwortzeit, Text, Statistik, Historie des Schlüssels, Beziehungsgraph. Ehrliche Arbeit liefert Beobachtungen mit der Verteilung `P`, eine Fälschung — mit der Verteilung `F`. Dann gilt

`E_F[π] − E_P[π] = Σ_x π(x)·(F(x) − P(x)) ≤ Σ_{x: F(x) > P(x)} (F(x) − P(x)) = TV(F, P)`.

Die Ungleichung gilt, weil `π ≤ 1` dort, wo `F > P`, und `π ≥ 0` dort, wo `F < P`. Die Größe `TV` ist der Abstand der totalen Variation: wie weit zwei Verteilungen überhaupt unterscheidbar sind. Daraus folgt (Theorem T4 der Arbeit claude2; dieselbe Ungleichung bei gpt1 und gpt2):

1. **Eine Fälschung wird nicht häufiger geprüft als ehrliche Arbeit im Durchschnitt, plus `TV`.** Ist eine Fälschung an den Beobachtungen schwer zu unterscheiden (`TV ≈ 0`), prüft der Detektor sie ebenso selten wie ehrliche Arbeit.
2. **Gegen einen wissenden Gegner ist es noch schlimmer.** Die Regeln sind offen (D4), daher berechnet der Gegner `π` selbst und wählt die Beobachtung, bei der die Prüfung am unwahrscheinlichsten ist. Die Entdeckungswahrscheinlichkeit seiner besten Fälschung ist gleich dem kleinsten `π(x)` unter den Beobachtungen, die er billig erzeugen kann.
3. **Folge für die Ersparnis.** Damit eine Fälschung unrentabel ist, muss sie mit einer Wahrscheinlichkeit nicht unter `R/(R + H_lock)` geprüft werden (Abschnitt 4). Bei `TV ≈ 0` muss dieselbe Häufigkeit auch für ehrliche Arbeit gehalten werden, das heißt, es gibt keine Ersparnis. Nach Einschätzung von claude2 ist der Gewinn aus „Intelligenz“ nicht größer als der Faktor `R/(R − c*)`, wobei `c*` der Preis der billigsten ununterscheidbaren Fälschung ist; bei einem plausiblen `c* ≈ 0,5R` ist das nicht mehr als das Doppelte, aber `c*` wählt der Gegner, und sie ist nicht gemessen.
4. **Die Historie des Schlüssels sagt nichts über den Zeitpunkt des Betrugs.** Ein Schlüssel, der bei der nächsten Aufgabe betrügen will, hat vor dieser Aufgabe dieselbe Historie wie ein ehrlicher (Likelihood-Verhältnis genau 1; Theorem T5 von claude2, Gegenbeispiel gpt1). Daher erkennen sequenzielle Tests (SPRT von Wald, CUSUM von Page), Banditenalgorithmen und bayessches „Vertrauen“ ihn erst nach dem Betrug. Eine kleine Aufzählung von claude1 zeigte: Senkt man die Prüfhäufigkeit nach Vertrauen um 10% unter die Schwelle, entsteht eine vorteilhafte Strategie „Vertrauen ansammeln und betrügen“ (+1,7R…+2,5R für 60 Aufgaben), bei Halbierung — +14,4R…+19,4R [Berechnung]. Der Kritiker Claude reproduzierte diese Zahlen, der Kritiker DeepSeek erhielt im nächstliegenden Modell eine andere Größe (+0,085R), aber dasselbe Vorzeichen (Abschnitt 8).

### 2.2. Beispiel an den Messungen D5

Die natürlichste billige Fälschung ist **dasselbe Qwen, gestartet in llama.cpp Q8_0**. Das exakte Profil ist 1,5–1,8 Mal langsamer als sie bei Batch 1 und 2,5–2,8 Mal bei Batch 8 [gemessen], daher ist die Fälschung deutlich billiger als ehrliche Arbeit. Dabei ist es die Antwort desselben Modells: Zeit, Stil und Perplexität unter dem kleinen Modell sind bei ihr dieselben wie bei einer ehrlichen Antwort, und die Verzögerung kann der Ausführende selbst hinzufügen. Wenn die Antwort von Q8_0 Token für Token mit der exakten Antwort übereinstimmte, ist das keine Fälschung: Nach D2 zählt das Ergebnis. Wenn sie in mindestens einem Token abwich, entdeckt das nur eine exakte Neuberechnung, weil die Bits des exakten Profils auf jedem getesteten Gerät übereinstimmen [gemessen].

Vorbehalt des Kritikers ChatGPT: In D5 wurde die Nähe des exakten Profils zum offiziellen Modell gemessen (dasselbe Token an 90 von 90 Positionen, Korrelation der Logits 0,9996 [gemessen]), aber die Nähe der Fälschung Q8_0 zum exakten Profil an billigen Merkmalen wurde nicht gemessen. Für die Garantie ist das nicht wichtig: Es genügt, dass niemand ein Merkmal gezeigt hat, das jede verfügbare Fälschung von einer ehrlichen Antwort unterscheidet.

### 2.3. Wo Detektoren dennoch nützlich sind

Detektoren, Fallen und Netzananalyse sind zulässig, wenn sie die Prüfhäufigkeit **nur erhöhen**:

- als Warteschlange zusätzlicher freiwilliger Prüfungen des Zahlers, die nicht auf die Garantie angerechnet werden, aber die reale Entdeckung erhöhen;
- gegen unvorsichtige Saboteure, die ihr Verhalten nicht optimieren;
- zur Diagnose von Ausfällen der Ausrüstung und der Treiber; ein Teilnehmer kann CUSUM über seine Selbstprüfungen führen und vor dem Verlust des ausstehenden Betrags anhalten;
- bei einem nicht adaptiven Fehlerstrom finden sie mehr Fehler pro Prüfstunde. Beispiel gpt1 [Berechnung]: Bei einem Fälschungsanteil von 2%, einer Sensitivität von 90% und 5% falschen Alarmen werden 8,57% der Aufgaben geprüft, 90,2% dieser Fälschungsfamilie gefangen, der Preis beträgt 1,80% gegen 18,94% bei gleichmäßiger Prüfung. Aber eine Fälschungsfamilie, die der Detektor nicht markiert, wird in 98% der Fälle durchgelassen.

Es gibt auch die umgekehrte Attacke (claude2): Anfragen, auf die eine ehrliche Antwort „anomal“ aussieht, zwingen dazu, Prüfungen für ehrliche Teilnehmer zu verbrauchen. Wenn die Prüfung der bezahlt, der sie ausgelöst hat, ist das von selbst begrenzt; wenn das Netz — ist das eine Lastverschiebung.

## 3. Analyse der Ansätze

In der Tabelle bedeutet „garantiert“ — was unter den genannten Annahmen streng folgt; „bei `q`“ — das Verhalten beim Abspracheanteil der Prüfer; „leeres Konto“ — ein Neuling mit `H = 0` und vielen kostenlosen Schlüsseln; „Urteil“ — das Ergebnis nach drei Kritiken.

| Ansatz | Wesen | Was garantiert wird | Bei `q` und bei `q = 1` | Leeres Konto, viele Schlüssel | Preis | Urteil nach der Kritik |
|---|---|---|---|---|---|---|
| Inspektionsspiele (Dresher, Maschler, Übersicht Avenhaus–von Stengel–Zamir; Sicherheitsspiele von Tambe und Mitautoren — aus dem Gedächtnis) | Eine im Voraus angekündigte zufällige Prüfung mit einer Häufigkeit, bei der Betrug sich nicht lohnt | `Δ₀ ≤ 0` bei `p ≥ (R − c_f)/(R + H_lock)`, auch für eine Fälschungsserie vor dem Weggang (unter den Bedingungen von Abschnitt 4) | Wenn der Zahler prüft, hängt es nicht von `q` ab, einschließlich `q = 1`. Wenn zugewiesene Prüfer prüfen — Entdeckung `p·(1 − q^k)`, bei `q = 1` null | `H = 0` ⇒ `p = 1`; jeder Schlüssel haftet mit seinem Betrag, Sybil hilft nicht | `p·ρ`: Hundertstel–Zehntel Prozent bei aktiven Schlüsseln; vollständige Prüfung beim Neuling [Berechnung] | **Grundlage der Strategie**, wenn die Häufigkeit der vollstreckt, dessen Geld auf dem Spiel steht |
| Risikobasierte Prüfung: SPRT, CUSUM, Banditen, bayessches Vertrauen | Neulinge und Verdächtige häufiger prüfen, langjährige seltener | Fängt einen dauerhaft lauten Betrüger schnell; gegen einen Strategen nichts | Das Urteil nach Meinungen der Prüfer bricht bei Absprache zusammen; bei `q = 1` null | Neue Schlüssel sind kostenlos; ein „langjähriger“ Schlüssel sammelt Vertrauen und betrügt am Ende | Die Ersparnis von 40–70% (ds1) bezieht sich auf einen lauten Gegner, nicht auf SkyNet | Die Häufigkeit unter die Schwelle zu senken ist **unzulässig** (Gegenbeispiel in Abschnitt 2.1); zusätzliche Prüfungen dürfen verteilt werden |
| Anomalien, Graphen, Sybil (Zeit, Logits, Entropie, Perplexität des kleinen Modells, Wasserzeichen, Konsistenz der Wiederholungen, Absprachegraphen, SybilGuard/SybilLimit/SybilRank) | Verdächtiges Verhalten und Beziehungen suchen | Gegen einen Detektor, der die Regeln kennt — nichts (Schranke von Abschnitt 2.1) | Eine abgestimmte Fälschung sieht wie ehrliche Zustimmung aus; bei `q = 1` gibt es keinen Schutz | SybilRank verlangt vertrauenswürdige Startknoten und eine kleine Zahl „angreifender“ Kanten; Kanten kauft die Koalition mit ehrlicher Arbeit | Die Perplexität des kleinen Modells kostet etwa 1,3–5% **jeder** Antwort nach Einschätzung von claude1 (Kritiker ChatGPT: an den Rändern ds2 1,875–9%) [Berechnung], teurer als die Prüfung nach der Regel; ein Wasserzeichen beglaubigt nur den Sampler | Nur **Signal für zusätzliche Prüfungen** und Diagnose von Ausfällen |
| Fallen, Goldfragen, Modell Dawid–Skene | Aufgaben mit bekannter Antwort, die von echten nicht unterscheidbar sind | Nur wenn die Falle nicht unterscheidbar und die Antwort geheim ist. In einem öffentlichen Netz kann das Geheimnis nur der Zahler halten, und die Falle fällt mit seiner Prüfung zusammen (T9 claude2) | Absprache teilt Fallen sofort auf; Dawid–Skene setzt unabhängige Fehler voraus | Einwegschlüssel lernen Fallen durch Proben; die Art der Aufgabe (D22) ist für den Ausführenden sichtbar | Ein frischer Referenztext freier Form kostet eine vollständige Generierung, mehr als die Prüfung (`ρ < 1`); für das Niveau `2⁻⁸⁰` bei einem Fallenanteil von 10% sind 526–527 Zuweisungen nötig [Berechnung] | Nicht billiger als die Prüfung durch den Zahler; zulässige Form — Wiederholung einer bereits geprüften Anfrage des Zahlers |
| Stichprobenprüfung und Lotterie (ein Teil der Token oder Schichten nach der Fixierung; BOINC, TrueBit, opML, Proof of Sampling — aus dem Gedächtnis) | Einen kleinen Teil der Berechnung prüfen; oder nur das durch Los gewählte bezahlen (Lotterie B) | Token: Ein Defekt wird mit der Wahrscheinlichkeit `1 − s/N` durchgelassen (99,2% bei 8 Positionen von 1000 [Berechnung]). Lotterie B mit Prüfung des Gewählten durch den Zahler: `Δ₀ = −c_f` bei beliebigem `p` | Eine Lotterie mit Komitee gibt dem Neuling `R·q^k`: 0,001R / 0,027R / 0,125R / R bei `q` = 0,1 / 0,3 / 0,5 / 1, `k = 3` [Berechnung] | Lotterie B mit dem Zahler eignet sich für den Neuling; die Token-Stichprobe — nicht | Zustand von Qwen3.5-4B: 48 MiB + 64 KiB je Position, eine Stichprobe an Position 500/1500/4000 — 79/142/298 MiB [Berechnung]; die Lotterie gibt ungleichmäßiges Einkommen und verlangt eine Vorauszahlung `R/p` | Token und Schichten sind **schlechter** als ein vollständiger Durchlauf, sowohl im Traffic als auch in der Garantie; Lotterie B mit dem Zahler — eine zulässige Variante. Externe Systeme beruhen auf einem Pfand oder auf „einem Ehrlichen von N“ |
| Peer Prediction (Bayesian Truth Serum von Prelec, Peer Truth Serum, DMI — aus dem Gedächtnis) | Für die Übereinstimmung der Berichte ohne Prüfung bezahlen | Wahrhaftigkeit ist nur ohne Absprache ein Gleichgewicht; es gibt nichtinformative Gleichgewichte | Bei `q > 0` verständigt sich die Gruppe; bei `q = 1` zahlt der Mechanismus für Beliebiges | Kostenlose Tickets von jedem Schlüssel | Es gibt keine Prüfung, aber es wird für Unbekanntes gezahlt | **Nicht anwendbar** auf deterministische Berechnung; die Zahlung für Übereinstimmung ist eine Zahlung für eine Kopie, die D15 verbietet |
| Kryptografie ohne vollständigen Beweis, TEE, Seed | Commitments und selektive Offenlegungen, Streit durch Halbierung, sumcheck/GKR, TEE-Attestierung, deterministische Generierung | Stichprobe ohne Kodierung — dieselbe Schranke `1 − s/N`; ein vollständiger Beweis — ja bei D19, aber nach der Schätzung von Phase 4 um das 16,8-Fache und teurer für eine Antwort; TEE — Vertrauen in den Hersteller | Streit und Determinismus hängen nicht von `q` ab; bei TEE zerstört ein extrahierter Schlüssel den gesamten Park | Eine Senkung der Häufigkeit nach Attestierung würde allen Schlüsseln des Gegners die gesenkte Häufigkeit geben | Ein Commitment auf die Antwort — 2–4 KB im Journal (D24) | Nötig sind ein Commitment auf die Antwort, eine geheime Münze und ein Streit durch Halbierung; TEE — nur zur Erhöhung der Prüfung oder für Privatsphäre. Der Vorschlag von ds1, die Häufigkeit nach TEE zu senken, wurde von allen Kritikern verworfen |
| Ökonomie ohne Pfänder (aufgeschobene Auszahlungen, Reputation als Kapital, Versicherung, Preis des Schlüssels durch Arbeit) | Mit dem Verlust nicht ausgereifter Belohnungen und künftigen Einkommens bestrafen | Der ausstehende Betrag ist der einzige mit R5 vereinbare Hebel. Das künftige Einkommen beim Weggang ist null. Eine Versicherung entschädigt das Opfer, verringert aber nicht den Gewinn des Betrügers | Funktioniert, wenn der Zahler die Häufigkeit vollstreckt | `H = 0` ⇒ vollständige Prüfung. Der Eintritt durch Arbeit — ein verstecktes Pfand, nutzlos beim Weggang; bei einem Komitee-Leck `R·q³` und `q = 0,3` zahlen etwa 370 Versuche den Eintrittspreis `10R` (ds1) [Berechnung] | Verzögerung der Auszahlung um das Ausreifungsfenster | `H_lock` — ein obligatorischer Teil der Strategie; das Übrige dient nicht als Grundlage der Garantie |

## 4. Untere Schranken und Formeln, die der Kritik standhielten

### 4.1. Einzelne Fälschung: Schwelle `R/(R + H_lock)`, nicht `R/H`

Eine entdeckte Fälschung wird nicht bezahlt und verbrennt den ausstehenden Betrag (mehr kann nach R5 nicht abgebucht werden). Dann

`Δ₀ = (1 − p)·R − p·H_lock − c_f ≤ 0  ⇔  p ≥ (R − c_f)/(R + H_lock)`,

und bei einer fast kostenlosen Fälschung — `p ≥ R/(R + H_lock)`. Gegenüber ehrlicher Arbeit ist `Δч = Δ₀ − (R − c) ≤ Δ₀`, daher ist die zweite Bedingung von D25 von selbst erfüllt. Beim Neuling ist `H_lock = 0`, und `p = 1`. Minimale Häufigkeit [Berechnung, claude2]: 0,5 bei `H_lock = R`; 0,25 bei `3R`; 0,0909 bei `10R`; 0,01 bei `99R`; 0,000231 bei `4320R`.

Die Arbeit claude1 schlug die Regel `p = min(1, R/H)` vor und nannte sie exakt. Der Kritiker Claude zeigte durch Aufzählung, dass die exakte Schwelle `R/(R + H)` ist: Mit ihr ist der größte Gewinn einer Fälschung genau 0, und schon mit `0,99·R/(R + H)` — von +0,225R bis +0,299R [Berechnung]. Die Regel `R/H` enthält einen Puffer. Der Kritiker DeepSeek bemerkte, dass dieser Puffer für den Schaden nützlich ist: Bei `R/H` ist die erwartete Zahl der Fälschungen bis zur Entdeckung endlich (etwa `H/R + 1`), bei `R/(R + H)` — unendlich (Abschnitt 4.4). Welche Formel in den Kern aufgenommen wird, ist nicht entschieden (Abschnitt 8).

### 4.2. Bedingung: Der Betrag reift nicht bis zum Ergebnis der Prüfung

Verbrennen kann man nur, was zum Zeitpunkt des bewiesenen Streitfalls noch nicht ausgezahlt ist. Wenn ein Teil von `H` früher ausreift, bricht die Regel. Gegenbeispiele [Berechnung]:

- claude2: Ein Schlüssel mit `H = 99R`, der früher als das Ergebnis ausreift, reicht `n` Fälschungen bei `p = 1%` ein; Gewinn 0,99R bei `n = 1`, 9,04R bei 10, 36,6R bei 100;
- Kritiker Claude: Ein Schlüssel mit `H₀ = 100R` beendet ehrliche Arbeit und reicht Fälschungen ein, und die Zahler prüfen spät; Gewinn +0,99R, +9,1R, +49,7R, +74,4R bei `n` = 1, 10, 100, 300. Mit „Sperre“ (alles verbrennt) ergeben dieselben Strategien von −0,01R bis −0,75R.

Deshalb geht in den Nenner der Häufigkeit für Aufgabe `i` nur der Teil des Betrags ein, der **nach** der äußersten Streitfrist für `i` ausreift, und die Prüffrist des Zahlers `δ` muss viel kleiner als das Ausreifungsfenster `W` sein; beide Fristen werden in der aktiven Zeit gezählt (D12). Das ist die Annahme der „rechtzeitigen Prüfung“; bei einem Telefon, das selten ins Netz geht, wird sie zuerst verletzt.

### 4.3. Wellen von Fälschungen vor dem Weggang

Eine Serie von Fälschungen vor dem Weggang deckt die Formel der einzelnen Fälschung nur bei der Regel **„die erste bewiesene Entdeckung verbrennt den gesamten nicht ausgereiften Betrag des Schlüssels, einschließlich der Belohnungen derselben Welle“** ab.

- Ohne diese Regel (gpt1): 10 parallele Fälschungen bei `R = 1`, `B = 4R`, `d = 0,2`, wenn jede durchgelassene bezahlt wird und der alte Betrag einmal verloren geht, ergeben `10·0,8 − 4·(1 − 0,8¹⁰) = +4,4295R`, obwohl eine einzelne Fälschung null ergibt. Wenn die Entdeckung die ganze Welle annulliert, ergibt dieselbe Strategie −2,49676R [Berechnung; von den Kritikern wiederholt].
- Der Kritiker ChatGPT fügte ein zweites Beispiel hinzu: bei `H = R`, `p = 1/2`, zwei Fälschungen mit unabhängigen Münzen und einmaliger Abbuchung des alten Betrags beträgt der Gewinn `R/4` [Berechnung]. Also muss das Protokoll alle offenen Commitments des Schlüssels atomar mit seinem gesamten nicht ausgereiften Erlös verbinden.

Bei dieser Regel ist der Beweis von claude2 (T2) richtig: Jede neue Fälschung multipliziert das erwartete Ergebnis mit `(1 − p_j)·(1 + α_j/(H_lock + A)) ≤ 1`, wobei `α_j` — die Auszahlung für das Ungeprüfte und `A` — das bereits angesammelte Verbrennbare. Induktion über die Zahl der Fälschungen ergibt `E[Ergebnis] ≤ H_lock` für jede Serie und jede adaptive Folge. Für eine homogene Serie folgt dasselbe aus `(1 + R/H)ⁿ ≥ 1 + nR/H`. Die Prüfung auf einem Gitter exakter Brüche ergab eine größte Überschreitung von genau 0 [Berechnung].

### 4.4. Prüfung durch ein Komitee: Faktor `1 − q^k`

Wenn die Entdeckung von mindestens einem der `k` zugewiesenen Prüfer festgehalten werden muss und jeder mit der Wahrscheinlichkeit `q` zur Koalition gehört, sinkt die Entdeckungswahrscheinlichkeit auf `p·(1 − q^k)`, und die Schwelle wird `p ≥ R/((R + H_lock)·(1 − q^k))`. Sie ist bei `1 − q^k < R/(R + H_lock)` unerfüllbar und immer unerfüllbar bei `q = 1`. In Lotterie B mit Komitee erhält der Neuling `R·q^k` je Versuch: 0,001R / 0,027R / 0,125R / R bei `q` = 0,1 / 0,3 / 0,5 / 1 und `k = 3` [Berechnung]. Das stimmt mit dem Gegnermodell überein. Die Unabhängigkeit der Auswahl ist ebenfalls eine Annahme: Bei der Wahl von `k` verschiedenen Teilnehmern aus `N`, von denen `C` in Absprache sind, ist die Wahrscheinlichkeit vollständiger Absprache `C(C,k)/C(N,k)`; bei allgemeiner Nichtverfügbarkeit der Daten oder selektiver Herausgabe kann sie `q` oder 1 erreichen (Kritiker ChatGPT nach dem Gegnermodell). Die Schlussfolgerung aller Arbeiten: **Die Häufigkeit muss der vollstrecken, dessen Entscheidung geschützt wird** — der Zahler für sein Geld, jeder Knoten für seine Abrechnung.

### 4.5. Schaden: Anteil des Nichtgefangenen

Ein Saboteur braucht keinen Gewinn, daher wird der Schaden am Anteil seiner Fälschungen bewertet, die ohne Entdeckung durchkommen.

- **Der billigste Zeitplan macht den Schaden unbegrenzt.** Bei `p = R/(R + H)` erhöhen ungeprüfte Fälschungen selbst `H`, und die Häufigkeit sinkt. Die Wahrscheinlichkeit, `n` Fälschungen ab dem Start `h = H/R` zu überleben, ist `h/(h + n)`; die erwartete Zahl der Fälschungen bis zur Entdeckung ist unendlich (T8 claude2). Die Schätzung von claude1 „`e^{−m}`“ unterschätzt den Durchlass: bei `H₀ = 4320R` und 4320 Fälschungen beträgt der exakte Durchlass 0,50 statt 0,37 bei der Häufigkeit `m·R/H` mit `m = 1`; 0,125 statt 0,050 bei `m = 3`; 0,0078 statt 0,0009 bei `m = 7` [Berechnung, Kritiker Claude].
- **Eine gezielte Fälschung** kommt mit der Wahrscheinlichkeit `1 − p` durch: bei einem ausgereiften Schlüssel mit `n_w = 4320` etwa 99,977% (Kritiker ChatGPT) [Berechnung].
- **Die Reparatur über den geprüften Teil des Betrags hielt nicht.** claude2 schlug vor, die Häufigkeit nach `H_ver` zu berechnen — Belohnungen nur für geprüfte Aufgaben; dann ist bei einem ehrlichen Schlüssel `p ≈ 1/√n_w` (Fixpunkt `p²·n_w + p − 1 = 0`) und der Anteil der Fälschungen des Saboteurs etwa `p`: 5,6% bei `n_w = 300`, 1,8% bei 3000, 0,58% bei 30 000 [Berechnung]. Der Kritiker Claude zeigte, dass `H_ver` durch selbstbezahlte Anfragen der Koalition aufgebläht wird; der Kritiker ChatGPT — dass ein Saboteur mit einem neuen Schlüssel nach einer geprüften Antwort bei `p = 1/2` erreicht, dass etwa die Hälfte seiner gelieferten Antworten falsch ist. Eine ökonomische Schadensgrenze, die Selbstbezahlung und neue Schlüssel aushält, hat keine Arbeit gefunden.

Fazit: Bei beliebigem `p < 1` ist ein Teil der Antworten des Saboteurs falsch. Für Anfragen ist das nur mit der Markierung „nicht geprüft“ zulässig (Text D6), für den Trainingsschritt — nicht.

### 4.6. Andere Formeln, die der Kritik standhielten

- **Kostenlose Ausfälle sind mit der Stichprobenprüfung unvereinbar** (claude1). Wenn ein ehrlicher Ausfall den Betrag nicht verbrennt (D16), nennt ein entdeckter Betrüger die Fälschung einen Ausfall, und `Δ₀ = (1 − p)·R − c_f > 0`. Bei `b` kostenlosen Ausfällen je Fenster ist die Leckage in der Größenordnung `b·H` je Fenster [Berechnung].
- **Faule Zahler** (claude2). Wenn ein Anteil `λ` der Zahler nicht prüft und der Ausführende sie nicht unterscheidet, ist `p·(1 − λ) ≥ R/(R + H_lock)` nötig. Wenn er sie unterscheidet — bringt eine Fälschung gegen sie bis zu `R` ohne Risiko. Abschreckung ist ein öffentliches Gut: Ein Zahler, der die Prüfung abschaltet, spart Bruchteile eines Prozents und verliert nichts. Das ist die Annahme „die Zahler vollstrecken im Durchschnitt die Münze des Kerns“.
- **Preis und Ungleichmäßigkeit der Lotterie B** (claude2, T7, mit der Korrektur des Kritikers ChatGPT). Die Auszahlung `R/p` mit der Wahrscheinlichkeit `p` ergibt einen Variationskoeffizienten des Einkommens `√((1 − p)/(pT))` für `T` Aufgaben. Für eine vorgegebene Streuung `v` ist `p ≥ 1/(1 + T·v²)` nötig; bei `T = 6000`, `v = 10%`, `ρ = 0,21` beträgt der minimale Prüfpreis 0,3443% [Berechnung]. Bei der Prüfung „durch jeden der 1000 Knoten“ wird derselbe Preis mit der Zahl der Knoten multipliziert, daher ist eine Lotterie mit Prüfung durch alle Knoten für die Ausgabe von Credits unbrauchbar.
- **Absprache von Zahler und Ausführendem** reduziert sich auf die Übertragung eigenen Geldes innerhalb der Koalition, solange eine bezahlte Anfrage keine Ausgabe von Credits, Gewicht und Anspruch auf Erstattung aus der gemeinsamen Kasse erzeugt.

### 4.7. Fehler in den Formeln der Arbeiten (kurz)

| Arbeit | Fehler | Korrektur |
|---|---|---|
| ds2 | Der zweite Schwellenwert ist als `(c − c_f)/R` geschrieben | Es muss `(c − c_f)/(R + H)` sein; dieser Schwellenwert bindet nie. An die Mini-Agenten nur die korrigierte Fassung übergeben |
| ds1 | Im Spiel ist der Verlust als `L = H + V` genommen, ohne die bereits ausgegebene `c_f` zu berücksichtigen | Schwelle `(R − c_f)/(R + H + V)`; bei `H = 0`, `c_f = 0,1R` — 90%, nicht 100% |
| claude1 | Gleichgewicht des Inspektionsspiels mit `L = H + R` (doppelte Zählung von `R`) | Indifferenzpunkt `(R − c_f)/(R + H)`: bei `H = R`, `c_f = 0` — 1/2, nicht 1/3 |
| claude1 | „Die Regel `R/H` ist exakt“; Schaden `e^{−m}` | Exakte Schwelle `R/(R + H)`; der Durchlass ist höher (Abschnitt 4.5) |
| claude1 | Spekulative Generierung „etwa `1 + ρ·s`“ | Nicht hergeleitet; nach dem Kritiker DeepSeek — doppelte Zählung; bei Batch 8 ergibt sich 1,65–2,79 |
| claude2 | T7: „`κ·CV²` hängt nicht von `p` ab“ | Es gibt den Faktor `1 − p`; exakte Schwelle `p ≥ 1/(1 + T·v²)` |
| claude2 | Der zusammengefasste Preis 0,2–1,2% ist bei `n_w = 3000` genommen | Bei `n_w = 300` — 0,56–2,24% (bis 3,6% bei Batch 8), bei `n_w = 30` — 1,7–6,7% [Berechnung] |
| claude2 | Zustands-Schnappschüsse 0,33 und 2,9 GiB je Antwort | Mit Attention-Cache 0,651 GiB (500/500, Schritt 64) und 12,38 GiB (2000/1000, Schritt 16) [Berechnung, Kritiker ChatGPT] |
| claude2 | In S1 ist die Zahlung des Ungeprüften `α` bei der Regel nach `H_ver` immer gleich `R` | Es gibt keinen fließenden Übergang A/B in S1; ein gemeinsamer Beacon für die Prüfentscheidung ist nicht nötig |
| ds1, gpt1, gpt2 | Kostenschätzungen der Strategien ohne Verlangsamung des exakten Profils | Der vollständige Preis ist bereits bei Batch 1 um das 1,5–1,8-Fache höher (Abschnitt 5.2) |
| ds1 | „Die Prüfung von `k` Token ist nicht billiger als ein vollständiger Durchlauf“ | Nach den Berechnungen ist sie billiger; sie verliert beim Traffic des Zustands und bei der Garantie |
| gpt2 | Zertifikat nach den Logit-Schranken: 6,25% | Die Schranken verlangen den wahren Zustand der letzten Schicht; der Kopf — etwa 15% der Multiplikationen, die Ersparnis nicht größer als sein Anteil |
| ds2 | Stabile Betrugsquote gegen CUSUM `θ = d_h/(d_h + d_f)` | Das ist eine Näherung nach der mittleren Drift, kein Theorem |
| ds1 | SPRT: 65 und 133 Beobachtungen | Genaue Neuberechnung des Kritikers ChatGPT: 132,73 und 76,70, fester Test — 229 [Berechnung]; auf einen strategischen Gegner trifft das nicht zu |

## 5. Empfohlene Strategie

### 5.1. Modellantworten: „Zahler als Inspektor mit Einsatz“

Der Kern ist den Arbeiten claude1 und claude2 entnommen, die Korrekturen — gpt1 und drei Kritiken.

1. **Exaktes Profil.** Jede bezahlte Antwort wird im exakten Profil v2 generiert (gierige Auswahl oder kanonisches Gumbel-max), der Chiffretext der Antwort wird mit einer Aufzeichnung mit Annahme ins Journal geschrieben (D24).
2. **Geheime Münze des Zahlers.** Nachdem die Antwort unwiderruflich fixiert ist, entscheidet das Programm des Zahlers mit seiner geheimen Zufälligkeit, ob es sie in einem Durchlauf prüft, mit der Wahrscheinlichkeit `p_i = max(p_nutzer, R_i/(R_i + H_lock))`. `p_nutzer` wählt der Nutzer selbst; bei `p_nutzer = 1` sieht er nur geprüfte Antworten. Bei `H_lock = 0` (Neuling) wird immer geprüft. Ein gemeinsamer Beacon ist dafür nicht nötig, solange die Bezahlung nicht vom Ausgang der Münze abhängt; die Entscheidung wartet nicht auf einen öffentlichen Block.
3. **Sperre des Betrags.** `H_lock` für Aufgabe `i` — die nicht ausgereiften Belohnungen des Schlüssels, die nach der äußersten Streitfrist für `i` ausreifen; die Prüffrist `δ` ist viel kleiner als das Ausreifungsfenster (Abschnitt 4.2).
4. **Verbrennung.** Jede bewiesene Abweichung verbrennt **den gesamten** nicht ausgereiften Betrag des Schlüssels, einschließlich der Belohnungen derselben Welle. Dem Geschädigten wird nicht mehr als seine Zahlung `R` erstattet, der Rest wird vernichtet. Sonst ist eine „Selbststreit“-Attacke möglich: Die Koalition fängt mit ihrem Zahlerschlüssel eine absichtlich gefälschte selbstbezahlte Anfrage ab und nimmt fremde Beträge unter Umgehung des Ausreifungsfensters (Kritiker Claude).
5. **Markierungen.** „Geprüft“ — nur eine Antwort, die vor der Anzeige vollständig geprüft wurde. Alles Übrige ist standardmäßig „nicht geprüft“. Die Markierung „stichprobenartig geprüft“ (claude1) wurde von allen Kritikern als irreführend verworfen.
6. **Signale nur nach oben.** Anomalien, Perplexität, Graphen, Wiederholungen geprüfter Anfragen (Fallen) lösen nur zusätzliche freiwillige Prüfungen aus. Die Häufigkeit nach Historie, Reputation, Anomalien, Attestierung oder Zahl der Schlüssel zu senken ist verboten.
7. **Streitfälle** — nur durch den Beweis einer Abweichung, den jeder Knoten selbst prüft (I8). Die Strategie wird ohne die Regel für falsche Streitfälle nicht eingeschaltet (D23, Berechnung M9).
8. **Variante für Schlüssel mit kleinem Betrag.** Wo eine häufige Prüfung für den Zahler teuer ist, ist Lotterie B zulässig: Es wird nur die durch Los gewählte Antwort bezahlt, ihr Zahler prüft sie vollständig (gpt1, claude2). In ihr bleibt ein kostenloser ehrlicher Ausfall (D16) unverändert, aber das Einkommen des Ausführenden ist ungleichmäßig, und der Zahler hält eine Vorauszahlung `R/p`.

Die Strategie verlangt, D16 und D21 zu ändern (Abschnitt 6). Alle Nullen der Garantie sind bedingt: Übereinstimmung der Bits auf getesteten, nicht auf beliebigen Geräten; rechtzeitige Prüfung; Lebendigkeit des Journals und Fehlen einer Zensur des Beweises; Korrektheit des Kerns; ehrliche Ausführung der Münze durch das Programm des Zahlers; die Regel für falsche Streitfälle.

### 5.2. Preis

Parameter: `p = R/(R + H)` bei eingeschwungenem `H ≈ n_w·R`; `ρ` = 0,10 / 0,21 / 0,40 (Batch 1); `γ` = 1,5–1,8 (Batch 1) und 2,5–2,8 (Batch 8). Der vollständige Preis gegenüber Q8_0 — `γ·(1 + p·ρ) − 1`. Tabelle des Kritikers Claude [Berechnung]:

| `n_w` (Aufgaben des Schlüssels je Fenster) | `p` eingeschwungen | Prüfung bei `ρ` = 0,10 / 0,21 / 0,40 | Insgesamt gegenüber Q8_0, Batch 1 | Insgesamt, Batch 8 | Prüfungen im ersten Fenster eines neuen Schlüssels |
|---|---|---|---|---|---|
| 30 | 3,23% | 0,32% / 0,68% / 1,29% | +50,5% … +82,3% | +152% … +186% | etwa 4,0 |
| 300 | 0,33% | 0,033% / 0,070% / 0,133% | +50,0% … +80,2% | +150% … +181% | etwa 6,3 |
| 4320 | 0,023% | 0,002% / 0,005% / 0,009% | +50,0% … +80,0% | +150% … +180% | etwa 9,0 |

Andere Zeitpläne [Berechnung]: Bei der geldminimalen Häufigkeit `p ≈ t_task/t_lock ≈ 2,3·10⁻⁴` kostet die Prüfung etwa 0,005% der Arbeit (Kritiker DeepSeek); bei der Häufigkeit mit Schadensbegrenzung `p ≈ 1/√n_w` — 0,18–0,72% bei `n_w = 3000` und 0,56–2,2% bei `n_w = 300`; bei Lotterie B mit `p = 5%` — 0,5–2,0% bei Batch 1. Fügt man zur Geldregel einen Schadensboden nach `H_ver` hinzu, wächst die Prüfung auf 0,15–2,2% bei `n_w` = 300–4320 und auf 6,7% bei `n_w = 30` (Kritiker Claude). Die erste Aufgabe eines Neulings kostet eine vollständige Prüfung, 10–40% seiner Generierung.
Zum Vergleich: Die vollständige Prüfung jeder Antwort (Hauptvertrag gpt1, gpt2, ds2) kostet `γ·(1 + ρ) − 1` = +65…+152% gegenüber Q8_0, bei `γ = 1,65`, `ρ = 0,21` — +99,65% [Berechnung].

Nicht berechnet: die Aufzeichnung von 2–4 KB je Antwort im Journal, falsche Streitfälle (M9), Energie, die Prüfung auf den Geräten der Zahler. **Der Engpass des Richtwerts von 5% ist die Verlangsamung des exakten Profils, nicht die Prüfung.** Senken können ihn schnelle bitgleiche Kerne und exakte spekulative Dekodierung: Der Entwurf generiert ein schnelles Q8_0, und das exakte Profil übernimmt das Präfix bis zur ersten Abweichung. Schätzung von claude2 bei 99% übereinstimmenden Token und Block 32 — etwa 0,78 der Zeit eines exakten Tokens, das heißt +28% über Q8_0 statt +65%; bei 95% Übereinstimmung — 1,33 der Zeit eines exakten Tokens, schlechter als die direkte Generierung (Kritiker Claude) [Berechnung; die Übereinstimmung ist nicht gemessen].

### 5.3. Restrisiko

Erwarteter Gewinn je Fälschung; „Schaden“ — der Anteil der nicht entdeckten Fälschungen des Saboteurs, alle mit der Markierung „nicht geprüft“. Zusammenfassung des Kritikers Claude und des Kritikers DeepSeek [Berechnung].

| Fall | `q = 0,1` | `q = 0,3` | `q = 0,5` | `q = 1` | Neuling, `H = 0` |
|---|---|---|---|---|---|
| Geld, der Zahler prüft selbst | ≤ 0 | ≤ 0 | ≤ 0 | ≤ 0 | `−c_f` (Prüfung immer) |
| Falsche Antwort als „geprüft“ angezeigt | 0 | 0 | 0 | 0 | 0 |
| Schaden bei `p = R/(R + H)`: nach `n_w` Fälschungen nicht gefangen | etwa 50% | etwa 50% | etwa 50% | etwa 50% | 0 (die ersten werden geprüft) |
| Dasselbe bei `p = 3R/(R + H)` | etwa 12,5% | ebenso | ebenso | ebenso | 0 |
| Zahler ohne Ausrüstung beauftragt ein zufälliges Trio mit der Prüfung | +0,001R | +0,027R | +0,125R | +R | ebenso |
| Zahler prüft nicht, der Ausführende unterscheidet ihn | bis +R | bis +R | bis +R | bis +R | 0 |
| Training, es gibt einen ehrlichen Auditor voller Häufigkeit | ≤ 0 | ≤ 0 | ≤ 0 | — | `−c_f` |
| Training, es gibt keinen ehrlichen Auditor | bis +R | bis +R | bis +R | bis +R | bis +R |

Die Zeilen „der Zahler prüft selbst“ hängen nicht von `q` ab. Das ist das Hauptergebnis des Rats: Eine vom Abspracheanteil unabhängige Prüfung ist beim Zahler billig, wenn er stichprobenartig prüft und der verbrennbare Betrag des Ausführenden bis zum Ende der Prüfung gesperrt ist.

### 5.4. Neuling

Ein Schlüssel mit leerem Konto wird immer geprüft, daher ergibt eine Fälschung bei ihm `−c_f`. Mit der Ansammlung des gesperrten Betrags sinkt die Häufigkeit: bei der Regel `R/(R + H)` im ersten Fenster etwa 4,0 / 6,3 / 9,0 vollständige Prüfungen bei `n_w` = 30 / 300 / 4320 (Kritiker Claude), bei der Regel `R/H` — 5,0 / 7,3 / 10,0 (claude1) [Berechnung]. Der Preis des ersten Fensters bei `n_w = 30` — 1,7 / 3,5 / 6,6% bei `ρ` = 0,10 / 0,21 / 0,40 (claude1) [Berechnung]. Als „Eintrittspreis“ dient nützliche, vollständig geprüfte Arbeit, nicht ein Eintrittsbeitrag. Die Kehrseite ist die Last: Eine Koalition neuer Schlüssel zwingt die Zahler, jede ihrer Antworten zu prüfen. Das trifft den Preis (R6), aber nicht D1; die Größe muss berechnet werden (Abschnitt 7).

### 5.5. Nutzer ohne Ausrüstung

Die Strategie schützt ihn nicht. Wenn er die Prüfung einem zufälligen Trio fremder Knoten überträgt, ist die erwartete Leckage `R·q³`: 0,001R / 0,027R / 0,125R / R bei `q` = 0,1 / 0,3 / 0,5 / 1 [Berechnung]. Wenn er sie seinem Gerät oder einem bekannten Knoten überträgt, ist das seine Annahme nach D21; bei Absprache des Helfers mit dem Ausführenden ist eine falsche Zusicherung mit Wahrscheinlichkeit 1 möglich. Der Kritiker Claude schlägt vor, durch ein Experiment zu prüfen, was eine Prüfung in einem Durchlauf auf dem Prozessor eines Laptops und eines Telefons kostet: Bei einer Häufigkeit von etwa einer Prüfung je Fenster des Schlüssels kann eine seltene langsame Prüfung akzeptabel sein. Die Garantie für einen solchen Nutzer bleibt die offene Frage D21.

### 5.6. Training

Für den Trainingsschritt hat der Rat keine neue Garantie gefunden. Der Schritt hat keinen Zahler, dessen Geld auf dem Spiel steht, daher muss die Stichprobenprüfung jeder Knoten vollstrecken, der die Garantie braucht, und der Preis multipliziert sich mit der Zahl solcher Knoten. Varianten:

- **Vollständige Wiederholung des Schritts** vom angenommenen Elternmodell — etwa 100% der Arbeit des Schritts für jeden prüfenden Knoten. Beispiel des Kritikers ChatGPT: Wenn die Inferenz 80% der Basisarbeit ausmacht, `ρ = 0,21` und jeder Schritt einmal wiederholt wird, ergibt sich 0,8·0,21 + 0,2·1 = 36,8% über der Basisarbeit [Berechnung]; bei `N` selbst prüfenden Knoten wird der zweite Summand mit `N` multipliziert.
- **Stichprobenprüfung des Schritts durch alle vollständigen Knoten** (claude2, S2): nur für Geld bei einem Fenster von 3 Tagen — 0,23% / 2,3% / 23% der Arbeit des Netzes bei 10 / 100 / 1000 prüfenden Knoten; mit einer Schadensbegrenzung von 10% — 10 Mal teurer [Berechnung; die Schadensspalte ist nicht streng hergeleitet]. Verlangt exaktes ganzzahliges Training, das nicht gebaut und nicht gemessen ist.
- **Audit „ein Ehrlicher von N“** (claude1, S2) — eine Annahme, die Phase 4 für das Training bereits verworfen hat; ohne bezahltes Audit ist das Gleichgewicht — „es gibt keine Auditoren“.
- **Bezahlung für eine bewiesene Verbesserung (D18)** — keine Prüfung des Schritts; die Berechnung M12 zeigte bereits, dass ein exaktes Duplikat der Einreichung die Anrechnung des Eigentümers nach allen drei Attributionsregeln erhöht (Berechnung der Mini-Agenten, Zusammenfassung D5_RESULTS).

Robuste Addition von Beiträgen (Krum, Median, getrimmtes Mittel — aus dem Gedächtnis) begrenzt den Schaden des nicht entdeckten Anteils, schützt aber nicht vor abgestimmten Saboteuren mit merklichem Gewichtsanteil und erfüllt D1 nicht. Ein ungeprüfter Schritt darf nicht in die ausgegebene Version des Modells gelangen (D6).

## 6. Entscheidungen, die geändert oder angenommen werden müssen

Die Formulierungen unten sind **Empfehlungen des Rats**, keine angenommenen Entscheidungen. Jede Frage muss ausdrücklich angenommen oder verworfen werden. Die unveränderlichen Anforderungen R1–R6 ändern sich durch eine Änderung der Zeile der Roadmap nicht (Erinnerung gpt1).

**Frage 1 (D21 sowie D11 und D2). Soll dem Zahler erlaubt werden, aus seiner Vorauszahlung eine Antwort zu bezahlen, die sein Programm nach der Regel des Kerns nicht geprüft hat?** Derzeit sagt D21: „Eine Antwort ohne Prüfung bezahlt das Netz nicht“, und D11 — „bezahlt wird nur Geprüftes“.
*Empfehlung (Kritiker Claude, nach den Arbeiten claude1 und claude2):* ja. Der vorgeschlagene zweite Satz von D21: „Der Zahler bezahlt aus seiner Vorauszahlung eine Antwort, die er geprüft oder nach der Regel D7 mit seiner geheimen Münze übersprungen hat; eine übersprungene Antwort trägt die Markierung ‚nicht geprüft‘. Eine Ausgabe von Credits und Gewicht für die bezahlte Anfrage gibt es nicht“. Gleichzeitig muss D11 (und nach der Bemerkung des Kritikers DeepSeek D2) präzisiert werden, sonst widersprechen sich die Änderungen.
*Wo sie sich widersprachen:* Kritiker DeepSeek — D21 vorerst nicht ändern (die Strategie ist ohnehin durch D23 blockiert) und Lotterie B verwenden (`α = 0`, Auszahlung `R/p` an den Gewählten), vereinbar mit den derzeitigen D2, D11, D21. Kritiker ChatGPT — als Hauptvertrag die vollständige Prüfung jeder Antwort durch den Zahler lassen und die Bezahlung der aus der Charge Gewählten durch einen gesonderten Vertrag einführen; ohne selbstständige Prüfung gibt es keine Netzzahlung.

**Frage 2 (D7). Wie soll festgeschrieben werden, welche Prüfung für die Bezahlung zulässig ist?**
*Empfehlung (Kritiker Claude):* „Eine vom Abspracheanteil unabhängige Prüfung ist obligatorisch für die Markierung ‚geprüft‘, für die Ausgabe von Credits und für das Gewicht. Die Bezahlung einer Anfrage aus Mitteln des Zahlers ist nach der Prüfung durch den Zahler oder nach dem Überspringen der Prüfung nach der Regel des Kerns zulässig: geheime Münze des Zahlers, geworfen nach der Fixierung der Antwort, Wahrscheinlichkeit nicht unter `R_i/(R_i + H_lock)`. Diese Wahrscheinlichkeit nach Historie, Reputation, Anomalien, Attestierung oder Zahl der Schlüssel zu senken ist verboten; zu erhöhen ist erlaubt. Eine Prüfung durch zugewiesene Prüfer dient nicht als Grundlage der Bezahlung. D1 wird nicht auf `q < q*` abgeschwächt“. Gesondert muss `R/(R + H_lock)` (exakte Schwelle) oder `R/H` (mit Puffer, endliche Zahl der Fälschungen des Saboteurs bis zur Entdeckung) gewählt werden.
*Wo sie sich widersprachen:* Die Kritiker DeepSeek und ChatGPT schlagen vor, den Text von D7 nicht zu ändern, sondern einen Geltungsbereich hinzuzufügen: Die Garantie für die Seite, die die Prüfung selbst ausführt, hängt nicht von `q` ab; die Seite, die die Prüfung delegiert hat, ist nur geschützt, wenn der Abspracheanteil der Zugewiesenen unter `q*` liegt, und das wird ihr gezeigt (Kritiker DeepSeek). Der Kritiker ChatGPT ergänzt: Ranking, Quorum, Fristablauf und die Annahme `q_eff < q*` geben kein Recht auf einen unabhängigen Status.

**Frage 3 (D6). Sollen die Markierungen des Ergebnisses präzisiert werden?**
*Empfehlung (gemeinsam für die Kritiker, Formulierung nach ds1):* „Eine falsche Antwort wird nicht als ‚geprüft‘ ausgegeben. Es gibt zwei Markierungen: ‚geprüft‘ — vollständige Prüfung vor der Anzeige auf eine vom Abspracheanteil unabhängige Weise (für eine Anfrage — durch den Zahler persönlich oder durch einen vom Kern angenommenen Beweis); ‚nicht geprüft‘ — standardmäßig, wird automatisch gesetzt, nur eine solche Prüfung kann sie entfernen. Die Streaming-Ausgabe — in geprüften Blöcken oder mit dieser Markierung. Ein ungeprüfter Trainingsschritt gelangt nicht in die ausgegebene Version des Modells“. Der Kritiker ChatGPT präzisiert: Ein ungeprüfter Schritt und seine Nachkommen können nur in einem isolierten Forschungszweig ohne Zahlung für den Übergang sein.
*Wo sie sich widersprachen:* im Wesentlichen nicht; claude1 schlug eine dritte Markierung „stichprobenartig geprüft“ vor — sie wurde von allen drei Kritikern verworfen.

**Frage 4 (D16). Was soll mit einem ehrlichen Hardware-Ausfall geschehen?** Derzeit wird ein Ausfall nicht bestraft, und der ausstehende Betrag verbrennt nicht. Bei der Stichprobenprüfung mit Bezahlung des Ungeprüften ist das eine direkte Leckage (Abschnitt 4.6).
*Empfehlung (Kritiker Claude und DeepSeek, nach claude1):* „Bei vollständiger Prüfung oder Lotterie B wird ein ehrlicher Ausfall nicht bestraft (frühere Regel). Bei der Stichprobenprüfung mit Bezahlung des Ungeprüften verbrennt jede bewiesene Abweichung `H_lock` des Schlüssels unabhängig von der Ursache, da die Ursache bei einem gleichen fehlerhaften Ausgang nicht feststellbar ist. Den erwarteten Verlust des Ehrlichen (etwa `P_f·R` je Aufgabe, wobei `P_f` — die Wahrscheinlichkeit eines stillen Ausfalls) ersetzt ein unbedingter Zuschlag aus der Netzabgabe. Die Regel wird erst nach der Messung von `P_f` eingeschaltet“.
*Wo sie sich widersprachen:* Kritiker ChatGPT — den Schutz vor einem ehrlichen Ausfall bewahren: Ein Ausfall lässt das Ergebnis ohne Bezahlung, frühere Belohnungen bleiben erhalten, die Zahl der Ausfälle je Schlüssel ist begrenzt, und die Zuverlässigkeit der Berechnung darf nicht von der Abbuchung früherer Belohnungen abhängen. Er bemerkt auch, dass der Zuschlag aus fremder Abgabe für jede Aufgabe die Auszahlung auch an eine Fälschung erhöht und die Schwelle ändert. Der Kritiker Claude ergänzt: Das Verbrennen eines Einkommensfensters wegen einer nicht gemessenen Instabilität trifft schwache Knoten (R6), der Zuschlag ersetzt den Durchschnitt, nicht das Risiko des Ruins. Der Streit wird durch die Wahl der Zahlungsstruktur (Lotterie B bewahrt D16, die Bezahlung des Ungeprüften — nicht) und die Messung von `P_f` gelöst.

**Frage 5 (D8). Wie sollen Frist und Rechte des Streitfalls gestaltet werden?**
*Empfehlung (Kritiker Claude):* „Der Zahler reicht den Beweis einer Abweichung nicht später als die Frist `δ` aktiver Zeit nach Erhalt der Antwort ein; der Streit wird nur durch einen Beweis entschieden, den jeder Knoten selbst prüft“. *Ergänzung (Kritiker ChatGPT):* Der Ausführende darf bei unbegründeter Ablehnung oder Schweigen des Käufers eine Abrechnung nach seiner fixierten Bestellung verlangen; beide Seiten streiten von einem Nullkonto ohne Pfand; ein Duplikat startet keine neue teure Prüfung; bis zur Entscheidung bleibt der strittige Betrag im Ausstand. Hier gibt es eine offene Gabelung: Wenn man nach Fristablauf ohne Einspruch zahlt, bezahlt die Abwesenheit des Zahlers die Fälschung; wenn man wegen Schweigen ablehnt, erhält ein unehrlicher Zahler die richtige Antwort kostenlos.
*Wo sie sich widersprachen:* claude2 und der Kritiker DeepSeek schlagen vor, nach M9 jedem Knoten einen Streit über eine durch den Beacon gewählte Aufgabe mit einer Quote falscher Streitfälle zu erlauben; der Kritiker Claude hält das für eine private Anfrage für leer (ein fremder Knoten hat keine Anfrage) und nur für das Training nützlich.

**Frage 6 (D23). Soll die Blockierung bis zur Berechnung M9 bleiben?**
*Empfehlung (alle drei Kritiker):* bleiben lassen. Ergänzen (Kritiker Claude): „M9 wird für die Regel D7 berechnet: Streitfälle sind im Gleichgewicht selten, aber die Koalition ‚Zahler = Ausführender‘ kann sie beliebig oft über selbstbezahlte Anfragen einreichen; der verbrannte Betrag wird vernichtet, dem Geschädigten wird nicht mehr als seine Zahlung erstattet“. Der Kritiker ChatGPT schlägt vor, das Kriterium für die Aufhebung der Blockierung festzuschreiben: Obergrenzen der Bytes, Berechnungen, Nachrichten und Fristen je Fall, die Grenze gleichzeitig offener Fälle, die Quelle der Deckung der Last, die Prüfung von Format und Eindeutigkeit vor der teuren Neuberechnung, die Widerstandsfähigkeit gegen selbstbezahlte Anfragen, die Absprache beider Seiten, die falsche Ablehnung des Käufers, die Netztrennung und die Nichtverfügbarkeit der Daten.

**Frage 7 (neues D26). Soll die Entscheidung über die Sperre des Betrags im Ausstand und die Obergrenze der Rückerstattung angenommen werden?**
*Empfehlung (Kritiker Claude, mit den Korrekturen von Abschnitt 4):* „`H_lock` der Aufgabe `i` — die nicht ausgereiften Belohnungen des Schlüssels, die nach der äußersten Streitfrist für `i` ausreifen; die Prüffrist des Zahlers ist viel kleiner als das Ausreifungsfenster. Eine bewiesene Abweichung verbrennt den gesamten nicht ausgereiften Betrag des Schlüssels, einschließlich der Belohnungen der Aufgaben, die nach der strittigen und in derselben Welle abgegeben wurden. Dem geschädigten Zahler wird nicht mehr als seine Zahlung für die strittige Antwort erstattet; der Rest wird vernichtet; der erste Streit nimmt keine Beträge weg, die anderen Zahlern zustehen“. Ohne diese Regel hält die Strategie der Abschnitte 5.1–5.3 nicht (Gegenbeispiele +4,4295R und bis +74,4R in den Abschnitten 4.2–4.3).
*Wo sie sich widersprachen:* Der Kritiker ChatGPT erörtert die Sperre in dieser Form nicht, da er die Bezahlung des Ungeprüften nicht unterstützt; aber er selbst verlangt, offene Commitments atomar mit dem gesamten nicht ausgereiften Erlös zu verbinden.

**Frage 8 (D1). Muss D1 geändert werden?**
*Empfehlung (alle drei Kritiker):* den Text nicht abschwächen. Die Varianten „D1 bei einem Abspracheanteil unter `q*`“ und „Leckage nicht größer als `ε` des Umsatzes“ (claude1, ds1, ds2, gpt1) sind verworfen: Bei `q = 1` geben sie der Koalition die gesamte ungeprüfte Ausgabe, widersprechen D19 und dem unveränderlichen R4, und der „Umsatz“ wird durch Selbstgeschäfte aufgebläht. Der Kritiker Claude schlägt eine Anmerkung vor: Für eine Modellantwort wird D1 gegenüber dem Zahler gewährleistet, der die Prüfung des Kerns ausführt; die Stichprobenprüfung mit seiner geheimen Münze erfüllt D1 als Erwartung und wird als Annahme über einen rationalen Gegner festgeschrieben (nach R4 ist die statistische Stichprobe eine Annahme); für einen nicht prüfenden Verbraucher verspricht das Netz D1 nicht. Kritiker DeepSeek — eine Anmerkung, dass die Garantie D1 sich auf jedes Ergebnis mit der Markierung „geprüft“ und auf jede Ausgabe von Credits bezieht.

## 7. Was die Mini-Agenten berechnen und was durch Experimente geprüft werden soll

### 7.1. Genaue Berechnungen (Brüche, Kontrollhash, Wiederholung auf einem zweiten Gerät)

1. Vollständige Aufzählung der Regel D7 mit Ausreifung des Betrags, Wellen, mehreren Schlüsseln, verschiedenen Preisen in der Welle und Prüfungen im Nachhinein. Referenzen: `κ = 1` → 0; `κ = 0,9` bei `H₀ = 0` → +1,734R (vom Kritiker Claude reproduziert, vom Kritiker DeepSeek nicht reproduziert — die Aufzählung muss entscheiden); `0,99·R/(R + H)` → +0,225R; Gegenbeispiel der Ausreifung +0,99R / +9,08R / +49,7R / +74,4R.
2. Formel der Welle gpt1: +4,4295R bei getrennter Abbuchung und −2,49676R beim Verbrennen der ganzen Welle.
3. „Selbststreit“-Attacke: bei welchem Anteil der Rückerstattung an den Geschädigten der Gewinn positiv wird.
4. Leckage kostenloser Ausfälle (`b` je Fenster) und Zuschlag `P_f·R` mit der Streuung der Verluste des Ehrlichen.
5. Schaden bei den Zeitplänen `H_lock`, `H_old`, `H_ver`, `m·R/(R + H)` mit Selbstbezahlung und neuen Schlüsseln; Referenzen 0,50 / 0,125 / 0,0078 bei `n_w = 4320`.
6. Faule Zahler: Anteil `λ` und Unterscheidbarkeit, bei denen die Abschreckung verschwindet.
7. Last einer Koalition neuer Schlüssel auf die Zahler bei `p = 1` für Neulinge.
8. M9 (falsche Streitfälle) für die Regel D7 — Bedingung D23.
9. Zusammengefasster Preis `γ·(1 + p·ρ)` auf einem Gitter gemessener `γ`, `ρ` und der Verteilung von `n_w`.
10. Wahrscheinlichkeit vollständiger Absprache bei der Wahl ohne Zurücklegen (`C(C,k)/C(N,k)`) und bei Auslosungsrunden.
11. Größen der Zustands-Schnappschüsse nach der festgeschriebenen Konfiguration des Modells (M1) — Streit über den Preis der Stichproben-Token und Schnappschüsse.
12. Korrigierte Schwelle ds2 und Kontrollskript gpt2 (SHA-256 beginnt mit `58aec3b0` und endet auf `cd07ba`; stimmte bei den Kritikern Claude und DeepSeek überein).
13. Genaue SPRT- und CUSUM-Ketten auf endlichen Gittern, einschließlich der Verhaltensänderung nach einer guten Historie.
14. Tabellen der Fallen `(1 − g·θ·d)^m` für die Niveaus `10⁻³`, `10⁻⁹`, `2⁻⁸⁰`.

### 7.2. Nur durch Experimente

Das Experiment D5 erlaubt die Arbeit mit dem ganzzahligen Qwen3.5-4B im Umfang O1–O5 seines Protokolls. **Alles Übrige — nur mit gesonderter Genehmigung des Eigentümers.**

1. Im Rahmen von D5: schnelle bitgleiche Kerne (O3, O4) — der einzige Weg, sich 5% zu nähern; der Prüfanteil auf den Geräten der Zahler und bei Batches 1, 8, 32; O5 — Qualität an 320 Aufgaben.
2. Außerhalb von D5: exakte spekulative Dekodierung — Verteilung der Länge des übereinstimmenden Präfixes von Q8_0 und exaktem Profil bei langen Antworten.
3. Außerhalb von D5: Häufigkeit stiller Abweichungen `P_f` bei langer Arbeit auf freiwilligen Geräten — vor jeder Änderung von D16.
4. Außerhalb von D5: Zeit und Speicher der Prüfung in einem Durchlauf auf dem Prozessor eines Laptops und eines Telefons.
5. Übereinstimmung der Bits an Randfällen (Überlauf, Gleichstände, frühes Antwortende) und bei neuen Treibern; auf einer RX 580 wurde der lange Durchlauf über eine fertige Antwort vom Treiber unterbrochen [gemessen].
6. Außerhalb von D5: O9 (Energie), O6 (Rauschen der LoRA-Verbesserung), O7 (Preis des Beweises eines Blocks), ganzzahliges Training — Voraussetzung jedes Schemas der Prüfung des Schritts.
7. Außerhalb von D5, optional: wie gut billige Fälschungen an Merkmalen unterscheidbar sind. Eine Garantie gibt das bei keinem Ausgang, sondern präzisiert nur die Obergrenze von Abschnitt 2.1.

## 8. Ungelöste Meinungsverschiedenheiten und zweifelhafte Quellen

### 8.1. Meinungsverschiedenheiten

1. **Erfüllt die Stichprobenprüfung durch den Zahler das wörtliche D1.** claude1, claude2, die Kritiker Claude und DeepSeek — ja für das Geld, nein für den Schaden. ds1 und ds2 — eine vollständige Prüfung ist nötig (die Kritiker meinen, sie hätten die Prüfung durch den Zahler mit Häufigkeit nach dem gesperrten Betrag nicht bemerkt). gpt1, gpt2 und der Kritiker ChatGPT — vollständige Prüfung jeder Antwort, und die Bezahlung der Gewählten — nur durch einen gesonderten Vertrag für Chargen. Die Entscheidung, ob der erwartete Gewinn beim ersten Satz von R4 ausreicht, liegt beim Eigentümer.
2. **`R/(R + H_lock)` oder `R/H`.** Das erste ist exakt für das Geld, das zweite gibt einen Puffer und eine endliche erwartete Zahl der Fälschungen bis zur Entdeckung; der Unterschied im Preis beträgt etwa das Doppelte bei kleinem Betrag.
3. **Das Ungeprüfte bezahlen** (`α = R` oder fließendes G(α) bei claude2) **oder nur das Gewählte** (`α = 0`, Lotterie B). Hängt von der Änderung von D2, D11, D21 und von der nicht gemessenen Ungleichmäßigkeit des Einkommens ab.
4. **Beacon oder geheime Münze.** claude2 — gemeinsamer Beacon (D20); claude1 und die Kritiker Claude und DeepSeek — geheime Münze des Zahlers, der Beacon ist nur bei `α < R` und für Streitfälle dritter Knoten nötig. Kritiker ChatGPT: Die geheime Münze eignet sich für die persönliche Prüfung, kann aber nicht über den gemeinsamen Preis verfügen; bei der Wahl des bequemen von zwei unabhängigen Ausgängen des Beacons sinkt die Entdeckung von `p` auf `p²`.
5. **D16** — Abschnitt 6, Frage 4.
6. **Schadensgrenze** — kein Schema hielt der Selbstbezahlung und neuen Schlüsseln stand.
7. **Training** — Audit „einer von N“ (claude1), Prüfung durch jeden vollständigen Knoten mit Rückrollung des Zweigs (claude2), D18 oder vollständige Wiederholung (ds1, ds2, gpt1, gpt2); kein Schema erfüllt D7 bei `q = 1`.
8. **Die Größen der Aufzählung von claude1** (+1,73R bei `κ = 0,9`): vom Kritiker Claude reproduziert, vom Kritiker DeepSeek nicht reproduziert (+0,085R im nächstliegenden Modell); das Vorzeichen ist bei beiden gleich.
9. **Spekulative Dekodierung:** 1,15–1,38 (claude1) gegen etwa 0,78 der Zeit eines exakten Tokens (claude2); beide nicht gemessen.
10. **Fallen:** ds2 berechnet die nötige Zahl der Fallen, claude1 und claude2 beweisen, dass in einem öffentlichen Netz die Falle mit der Prüfung durch den Zahler zusammenfällt. Die Schlussfolgerungen sind vereinbar.

### 8.2. Literaturverweise, die von den Kritikern als zweifelhaft markiert wurden

Alle Verweise sind aus dem Gedächtnis gegeben, ohne Abgleich der Texte.

- SybilGuard und SybilRank unter dem gemeinsamen „Yu und Mitautoren“ (ds1): nach dem Gedächtnis der Kritiker sind SybilGuard und SybilLimit — Yu und Mitautoren (2006, 2008), SybilRank — Cao und Mitautoren (2012); das Jahr von SybilRank selbst ist vom Kritiker Claude als unsicher markiert.
- „Proof of Sampling (2024)“ und „Verde (Gensyn, 2025)“ (claude1, claude2) — die Arbeiten selbst schreiben „nicht sicher“; die Funktionsweise des Mechanismus ist nicht bestätigt.
- Peer Truth Serum als Arbeit von Witkowski und Parkes (2012) (ds2): Der Kritiker Claude hält das für zweifelhaft (nach seinem Gedächtnis haben sie „robustes BTS“, und der Name gehört Radanovic und Faltings), der Kritiker DeepSeek — für richtig. Meinungsverschiedenheit.
- DMI als Arbeit von Kong und Schönbeck (2019) (ds1, ds2): zweifelhaft nach dem Gedächtnis der Kritiker Claude und ChatGPT (DMI — eine Arbeit von Kong um 2020); der Kritiker DeepSeek hält die Zuordnung für korrekt.
- „Angriffe durch Selbstvorhersage auf BTS bei Radanovic und Faltings“ (ds1) — zweifelhaft.
- „Gao, Wright und Leyton-Brown (2016)“ über die Überlegenheit der Stichprobenprüfung gegenüber Peer Prediction (claude2) — das Jahr ist nicht bestätigt (Kritiker DeepSeek), die Unbedingtheit der Schlussfolgerung ist zweifelhaft (Kritiker ChatGPT).
- Kreps und Wilson (1982) als Grundlage „Reputation funktioniert nur bei einem langen Horizont“ (claude1) — zweifelhaft (Kritiker ChatGPT).
- DetectGPT als Begründung der Perplexitätsschwelle des kleinen Modells (ds1) — nicht korrekt: Es untersucht eine andere Eigenschaft (Kritiker ChatGPT).
- Die allgemeine Formel des Durchlasses `(1 − f)^s` als Eigenschaft von BOINC, TrueBit, opML (ds1, ds2) — folgt nicht aus ihren Protokollen.
- Die Verweise von ds1 und ds2 auf „0,3–0,7% / 0,33–0,66% der Token des Examens“ und „etwa 2,4 Stunden je Kandidat“ wurden in den Eingabedokumenten nicht gefunden.

## 9. Wer was getan hat

Der Modellrat arbeitete nach den Materialien des Projekts, ohne Netzzugang und ohne Experimente.

- **Sechs unabhängige Arbeiten:** zwei Arbeiten von ChatGPT (gpt1, gpt2), zwei Arbeiten von DeepSeek (ds1, ds2), zwei Arbeiten von Claude (claude1, claude2). Jede untersuchte sieben Richtungen aus dem Auftrag, fügte eigene hinzu, glich sie mit den Entscheidungen D1, D6, D7 ab und schlug Strategien mit Preis und Restrisiko vor. Kurze Arithmetikprogramme und kleine Aufzählungen führten claude1 (Aufzählung von Strategien gegen die Häufigkeitsregel), claude2 (Gitter exakter Brüche), gpt1 und gpt2 aus (gpt2 legte ein Kontrollskript mit Hash bei).
- **Drei Kritiken:** je eine von ChatGPT, DeepSeek und Claude. Jeder Kritiker las alle sechs Arbeiten, suchte Fehler und Gegenbeispiele, rechnete die Schlüsselzahlen nach. Die Kritiker Claude und DeepSeek wiederholten das Kontrollskript von gpt2, der Hash stimmte überein; der Kritiker Claude wiederholte die Aufzählung von claude1, der Kritiker DeepSeek reproduzierte ihre Größen nicht.
- **Zusammenführung:** Dieses Dokument stellte Claude nach den Arbeiten und Kritiken zusammen. Neue Einschätzungen und Zahlen über die Arbeiten, Kritiken und Messungen D5 hinaus wurden nicht hinzugefügt; wo die Kritiker sich widersprachen, ist das angegeben.
