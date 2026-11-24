<!-- translation of docs/VERIFICATION_SEARCH.md, source sha256: cdf54a57e7747ae1f862b5b29fa7a53eee7fca80d8bae17a0cbc60f022cec00b -->

# Suche nach einer Prüfung, die nicht vom Abspracheanteil abhängt

[English](../../docs/VERIFICATION_SEARCH.en.md) · [中文](../zh/VERIFICATION_SEARCH.md) · [Español](../es/VERIFICATION_SEARCH.md) · [Français](../fr/VERIFICATION_SEARCH.md) · **Deutsch** · [Italiano](../it/VERIFICATION_SEARCH.md) · [Русский](../../docs/VERIFICATION_SEARCH.md) · [Português](../pt/VERIFICATION_SEARCH.md) · [العربية](../ar/VERIFICATION_SEARCH.md)

Stand vom 24. November 2026.

Dieses Dokument ist das Ergebnis des Modellrats zu Phase 4 der Roadmap („Suche nach einer Garantie, die nicht
vom Abspracheanteil abhängt“, [ROADMAP](ROADMAP.md), Abschnitt 4). Der Rat suchte eine Prüfung, die jeder Knoten
selbst ausführt, sodass die Zustimmung oder Absprache anderer Prüfer nichts entscheidet. Gesucht wurde für zwei
Arten von Arbeit: die Antwort des Modells Qwen auf eine Anfrage des Nutzers und den Schritt des Nachtrainings.

**Status des Dokuments.** Dies ist das Ergebnis von Überlegung und Berechnung nach Formeln, keine Messung.
Experimente mit dem Modell, Netzstarts, Beweissysteme und Model Checking gab es dafür nicht.
Die Teilnehmer und Kritiker führten nur kurze Arithmetikprogramme und kleine Aufzählungen
auf dem Prozessor aus; zwei solche Aufzählungen aus den Arbeiten ChatGPT wurden von zwei Kritikern wiederholt, die Kontrollhashes
stimmten überein. Zahlen mit der Markierung [Berechnung] wurden nach Formeln aus ausdrücklich genannten Parametern ermittelt. Die Parameter
der Modelle und Grafikkarten setzten die Teilnehmer selbst ein; keine Arbeit glich sie mit der veröffentlichten
Konfiguration von Qwen3.5-4B oder eines Modells mit etwa 27 Mrd. Parametern ab. **Angenommene Entscheidungen sind
nur die Entscheidungen D1–D25** in [ROADMAP](ROADMAP.md), Abschnitt 3. Alles Übrige hier ist eine
Einschätzung des Rats. Wo die Kritiker sich widersprachen, steht „strittig“.

**Wie man liest.** Abschnitt 1 — was gesucht wird und unter welchen Bedingungen. Abschnitt 2 — was als unmöglich bewiesen
und welche Unmöglichkeitsaussagen widerlegt wurden. Abschnitte 3 und 4 — die Analyse der Mechanismen für die Modellantwort
und für den Trainingsschritt, mit dem besten Kandidaten und seinen Einschränkungen. Abschnitt 5 — was unbewiesen blieb
und welche Experimente und Berechnungen das entscheiden. Abschnitt 6 — Fragen an den Eigentümer. Abschnitt 7 — wer
beteiligt war.

**Kurzes Fazit.**

1. **Modellantwort.** Eine Prüfung, die nicht vom Abspracheanteil abhängt, gibt es nur dort, wo der Zahler, dessen Geld auf dem Spiel steht,
   die gesamte Antwort selbst prüft. Der beste Kandidat ist „PPS“: Der Zahler rechnet die Anfrage und die fertige Antwort in einem
   einzigen Durchlauf im exakten Ganzzahlprofil nach, die Bezahlung erfolgt nur aus seiner Vorauszahlung, einen Streitfall über den Fehlerbeweis
   prüft jeder Knoten. Der berechnete Preis beträgt
   1,2–3,8% der Generierungszeit, aber nur bei der Generierung einer Antwort nach der anderen [Berechnung]. Der Kandidat
   deckt den Verbraucher ohne Ausrüstung nicht ab und hängt von einer nicht gemessenen Bitübereinstimmung ab.
2. **Trainingsschritt.** Eine Prüfung des Schritts selbst im Rahmen von etwa 20%, die nicht vom Abspracheanteil abhängt,
   wurde nicht gefunden. Dem stimmen alle sechs Arbeiten und alle drei Kritiken zu.
3. **Der einzige übrig gebliebene Weg für das Training** ändert, wofür bezahlt wird: Das Netz zahlt
   für eine bewiesene Verbesserung des Modells in einem Examen, das nach der Fixierung der Aktualisierung gewählt wird. Nach Entscheidung D18 wird dieser Weg
   als Kandidat für eine neue Vergütungseinheit untersucht, ist aber noch nicht angenommen; nötig sind Berechnungen, ein Experiment und die von den
   Kritikern gefundenen Korrekturen.
4. **Entscheidend sind das Experiment D5** (Bitübereinstimmung des ganzzahligen Qwen3.5-4B auf zwei Grafikkarten und zwischen
   zwei Berechnungsmodi, Zeit, Qualität) **und die Berechnungen der Mini-Agenten** aus Abschnitt 5.3; nach ihnen wird
   die endgültige Entscheidung über die Bezahlung des Trainings getroffen (D18).

Ausgangsdokumente: die Entscheidungen D1–D17 und Phase 4 in [ROADMAP](ROADMAP.md); das Gegnermodell
und die formale Schreibweise von D1 in [THREAT_MODEL](THREAT_MODEL.md), Abschnitt 1.5; die Varianten A und B
in [CURRENT_DESIGN](CURRENT_DESIGN.md); [OPEN_QUESTIONS](OPEN_QUESTIONS.md);
[PILOT_RESULTS](PILOT_RESULTS.md); die [verbindlichen Anforderungen](../ru/REQUIREMENTS.md). Die Teilnehmer
lasen auch frühere Untersuchungen des Projekts zur exakten Arithmetik, zu sumcheck/GKR, Brakedown und zum Preis
des Zeugen für LoRA (die Dokumente `LORA_*` und `HONESTY_RESEARCH_GATE` des Forschungsarchivs; sie gehören nicht zu diesem
Repository). Die Entscheidungen D6–D17 lagen den Teilnehmern noch nicht vor: Sie wurden am selben Tag angenommen.
Bei der Zusammenführung wurden diese Entscheidungen auf die Schlussfolgerungen der Arbeiten angewandt; wo eine Entscheidung das Urteil ändert, ist das ausdrücklich gesagt.

---

## 1. Problemstellung

### 1.1. Was gesucht wird

Gesucht wird eine Prozedur, die der Knoten selbst nach Daten ausführt, die die Koalition nicht fälschen kann:
die Eingabe der Aufgabe, das festgeschriebene Modell, die festgeschriebenen Regeln und möglicherweise einen mathematischen
Beweis. Die Entscheidung des Knotens darf sich nicht auf Signaturen und Urteile anderer Knoten stützen. Dann
beeinflusst der Anteil der abgesprochenen Prüfer `q`, einschließlich `q = 1`, die Entscheidung nicht.

Zwei Arten von Arbeit:

- **(a) Modellantwort** von Qwen in der Größenordnung von 4–27 Mrd. Parametern auf eine Anfrage des Nutzers;
- **(b) Schritt des Nachtrainings** (LoRA oder vollständig) auf einer vorgegebenen Datencharge.

### 1.2. Verbindliche Bedingungen

| Bedingung | Was daraus für die Prüfung folgt |
|---|---|
| **D1** | Der erwartete Gewinn aus jeder falschen Meldung ist nicht größer als null, sowohl gegenüber der Untätigkeit (`Δ₀ ≤ 0`) als auch gegenüber ehrlicher Arbeit (`Δч ≤ 0`), für jede Koalition, einschließlich eines Neulings mit leerem Konto und beliebig vieler Schlüssel. Nötig sind **beide** Ungleichungen ([THREAT_MODEL](THREAT_MODEL.md), Abschnitt 1.5). Eine begrenzte positive Leckage wie `R·q^k` in Variante B genügt nicht |
| **D2** | Bezahlt wird nur ein prüfbares Ergebnis. Arbeitszeit, angegebene Leistung und eingeschaltete Ausrüstung sind keine Grundlage. Die Art, wie der Ausführende das richtige Ergebnis erhielt (Cache, andere Maschine), ist nicht wichtig |
| **D4** | Die Prüfung ist automatisch, ohne Abstimmungen; jeder Knoten führt sie selbst nach dem festgeschriebenen Fingerabdruck der Regeln aus |
| **D6** | Der Schaden gehört zu D1: Eine falsche Antwort darf dem Nutzer nicht als geprüft ausgegeben werden, ein falscher Schritt nicht in das Modell gelangen. Das Ergebnis wird erst nach einer Prüfung genutzt, die nicht vom Abspracheanteil abhängt, oder ausdrücklich als ungeprüft gekennzeichnet |
| **D7** | Gefordert ist eine Prüfung, die nicht vom Abspracheanteil abhängt. Eine Abschwächung von D1 auf „solange die Abgesprochenen weniger als `q*` sind“ ist nicht zulässig |
| **D8** | Bestreiten dürfen nur die durch Auslosung zugewiesenen Prüfer der Aufgabe und der Nutzer zu seiner eigenen Anfrage. Ohne Pfand. Die Übrigen melden einen Verdacht auf dem Board, ohne das Recht, die Auszahlung anzuhalten |
| **D15** | Eine einfache Neuberechnung, die sich kopieren lässt, wird nicht bezahlt |
| **R5** | Keine Pfänder, Einlagen und Strafen. Verloren gehen können nur noch nicht ausgereifte Belohnungen („ausstehender Betrag“ `H`) |
| **Richtwerte des Preises** | Der Aufschlag für die Prüfung beträgt etwa 5% der Arbeit für Anfragen und etwa 20% für das Training. Das sind Richtwerte, die durch die Anforderungen nicht bestätigt sind |

Verwandte Entscheidungen: D9 (der Trainingsplan wird durch eine Regel aus dem Katalog und den Ergebnissen des Examens abgeleitet,
Credits werden einmal je Inhalt der Aufgabe ausgegeben), D10 (der Austausch erfolgt mit einem einzigen Journal-Eintrag),
D12 (Fenster werden in der aktiven Zeit des Netzes gezählt), D14 (der Preis des Streitfalls richtet sich nach dem billigsten Netz der zweiten
Ebene), D16 (ein ehrlicher Hardware-Ausfall wird nicht bestraft), D17 (Auszahlungen für Anfragen in Variante B —
nur aus den Zahlungen der Nutzer).

Statistische Stichprobe, Vertrauen in die Hardware-Enklave und ein kleiner kryptografischer Fehler
nach den Anforderungen sind Annahmen: Man darf sie vorschlagen, muss sie aber ausdrücklich benennen.

### 1.3. Modelle und Parameter, die die Arbeiten verwendeten

Ein festgeschriebenes Manifest von Qwen3.5-4B gab es in den Materialien nicht. Jede Arbeit nahm ihre eigene angenommene
dichte Konfiguration, daher bedeutet „4B“ in verschiedenen Arbeiten verschiedene Zahlen. Wenn es in Qwen3.5
hybride Schichten linearer Attention gibt, ändern sich alle Attention-Anteile und die Schlussfolgerungen über die Übereinstimmung der Berechnungsmodi
(Abschnitt 5).

| Arbeit | Modellantwort (a) | Trainingsschritt (b) |
|---|---|---|
| claude1 | „4B“: 36 Schichten, Breite 2560, Attention-Abfragen 4096, Schlüssel/Werte 1024, MLP 9728, Vokabular 151 936, gemeinsamer Eingang und Kopf (4,022 Mrd. Parameter). „27B“: 64 Schichten, 5120, 6144, 1024, 20 480, 151 936, getrennt (26,386 Mrd.). Anfragen 500/500 und 2000/1000 Token | LoRA vom Rang 16 auf den Matrizen der oberen Schichten, Examen mit `n = 10⁴–10⁶` Positionen |
| claude2 | Dieselbe „4B“. Anfrage 1000 Token, Antwort 500; Arbeit der Anfrage 5,98·10¹² MAC [Berechnung] | LoRA vom Rang 16/64 auf allen sieben Matrizen, Kontext 4096, Charge von 64 oder 7680 Sequenzen |
| gpt1 | „S“: 36 Blöcke, 2560, KV 640, MLP 11 008, 151 936. „Lg“: 48, 5120, 1024, 31 232. Eingang 128, Ausgang 32 Token | 8 Mikropakete zu je 512 Token, LoRA vom Rang 8 auf Q, V |
| gpt2 | „Klein“: 36, 3072, KV 768, MLP 8192, Vokabular 150 000. „Groß“: 60, 6144, 1024, 18 432. Eingang 128, Ausgang 128 | Dasselbe wie gpt1 |
| ds1 | Klasse Qwen3-4B: 4·10⁹ Parameter, 36 Schichten, 2560, MLP 9728 | Profil Qwen2.5-1.5B aus früheren Untersuchungen: 28 Blöcke, 1536, MLP 8960, LoRA vom Rang 8 auf q/v, 512 Token × 8 Mikropakete |
| ds2 | 36 Schichten, 2560, MLP 8960, 32/8 Köpfe; Kontext 2048, Antwort 200 | Dasselbe 1.5B-Profil |

Ausrüstung (Datenblatt nach dem Speicher, nicht abgeglichen): Klasse RTX 2060 — 336 GB/s Speicher, etwa 103 TOPS
INT8, 6 GB; Klasse RTX 4090 — 1008 GB/s, etwa 660 TOPS, 24 GB. Die Anteile am Spitzenwert 0,8 für den Speicher und 0,4
für die Berechnungen sind Szenariowerte. Die einzige Geschwindigkeitsmessung ist 73,8 Token/s bei Qwen3-4B Q4_K_M
auf einer RTX 2060 im Piloten ([PILOT_RESULTS](PILOT_RESULTS.md)). Das ist ein anderes Gewichtsformat, und es
bestätigt oder widerlegt die obigen Modelle nicht.

Die gemeinsame Schreibweise von D1 für eine falsche Meldung, auf die sich die Arbeiten einigten: Bei einem Preis der Aufgabe `R`,
Selbstkosten der ehrlichen Arbeit `c`, Kosten der Fälschung `c_f` und Wahrscheinlichkeit ihrer Annahme `ε`
werden `Δ₀ = εR − c_f ≤ 0` und `Δч = εR − c_f − (R − c) ≤ 0` benötigt [Berechnung].


---

## 2. Untere Schranken: was als unmöglich bewiesen wurde

### 2.1. Von den Kritikern bestätigte Schranken

Das sind Aussagen über **Klassen** von Prüfungen. Keine von ihnen schließt alle denkbaren Prüfungen aus;
eine allgemeine untere Preisschranke für alle Algorithmen hat niemand bewiesen.

1. **Ununterscheidbarkeit.** Wenn der Knoten ein Ergebnis nur nach den Meldungen anderer Knoten annimmt, dann gibt es bei
   Absprache aller ihrer Urheber ein falsches Ergebnis, das er annimmt: Die Koalition sendet dieselben
   Signaturen und Fingerabdrücke wie bei einem ehrlichen Ergebnis. Bei `q = 1` ist der Knoten nur durch das geschützt, was er
   selbst geprüft hat. (claude1, Lemma 1; claude2, 3.1; gpt2, 9.4; ds2, 6.1. Alle Kritiker stimmen zu.)
2. **Der Maßstab „jeder Knoten selbst“.** Wenn eine Änderung des gemeinsamen Zustands (Ausgabe von Credits, Gewicht) für
   jeden der `N` vollständigen Knoten geschützt sein muss, prüft jeder von ihnen jedes solche Ergebnis,
   und der Gesamtpreis ist nicht kleiner als `N·v`, wobei `v` der Preis einer Prüfung ist. Um in 5% oder 20% zu bleiben, braucht man bei
   `N = 1000` `v/W ≤ 5·10⁻⁵` oder `2·10⁻⁴` der Arbeit [Berechnung]. Daraus ergeben sich drei Wege zur
   Unabhängigkeit von der Absprache: Es entscheidet der einzige Teilnehmer, dessen Geld auf dem Spiel steht; die Prüfung ist komprimiert
   (kurzer Beweis oder kleines Examen); das Ergebnis ändert den gemeinsamen Zustand überhaupt nicht.
   (claude1, Lemma 2; claude2, 3.4; gpt1, §2; ds2, 6.1. Alle Kritiker stimmen zu; der Kritiker ChatGPT
   korrigierte die Formel von ds2 auf `1 + n·a` statt `(1 + a)·n`.)
3. **Zellenstichprobe ohne Kodierung.** Wenn der Knoten im Mittel `s` von `N` unabhängig ersetzbaren
   Zellen (Schichten, Positionen, Sequenzen) liest, gibt es eine Zelle, die er mit einer Wahrscheinlichkeit von höchstens `s/N` prüft;
   ihre Ersetzung kommt mit einer Wahrscheinlichkeit von mindestens `1 − s/N` durch.
   (claude2, 3.2; gpt2, 9.2; gpt1, 5.4; claude1, I2. Der Kritiker Claude bemerkte eine Lücke in der Strenge für
   einen Prüfer, dessen Münzen von der Wurzel der Spur abhängen; die Schlussfolgerung ändert sich dadurch nicht.)
4. **Stichprobenprüfung und Marge des Ausführenden.** Für eine falsche Meldung `σ` mit Kosten `c_σ` und ausstehendem
   Betrag `H` verlangt D1 gegenüber der Untätigkeit `π(σ) ≥ (R − c_σ)/(R + H)`, wobei `π` die Wahrscheinlichkeit
   der Entdeckung ist. Für eine billige Fälschung und ein leeres Konto braucht man `π ≈ 1`, also eine vollständige Prüfung. Für
   eine nahezu ehrliche Fälschung ist ein Prüfanteil von mindestens `m/(1 + m)` bei einer Marge `m` nötig. Für einen Schlüssel
   mit `H > 0` und bei der Prüfung eines Blocks von `L + 1` braucht man `H ≥ R·((L+1)/m_s − 1)`: 36R für 36 Schichten
   und 64R für 64 Schichten bei einem geprüften Block [Berechnung]. Frische Zufälligkeit des Knotens macht `π`
   unabhängig von der Absprache, aber nicht gleich eins. (claude1, Lemma 3; claude2, 3.11, unabhängig erhalten.
   Alle Kritiker stimmen zu. Der Kritiker ChatGPT präzisierte: Bei obligatorischer Prüfung des Ausgabeblocks beträgt die Schwelle für einen nahezu kostenlosen Versuch 35R.)
5. **Feste lineare Prüfungen über einem Feld.** `t < n` im Voraus fixierte lineare Prüfungen haben einen gemeinsamen
   von null verschiedenen Kern: Einen Fehler daraus sehen sie nicht. Ein frischer gleichverteilter Vektor, der nach der Fixierung gewählt wird,
   lässt einen fixierten von null verschiedenen Fehler mit einer Wahrscheinlichkeit von höchstens `1/p` durch. Über beschränkten
   ganzen Zahlen ist die Schranke nicht anwendbar (siehe 2.2, Nr. 3). (gpt1, 5.2; gpt2, 9.1; claude2, 3.5; ds2, 5.2; claude1, B4.)
6. **Null Fehler ist gleichbedeutend mit Determinismus.** Eine Prüfung ohne falsche Annahmen bei beliebigen Münzen
   wird durch die Fixierung der Münzen zu einer deterministischen. (claude2, 3.6.)
7. **Gemeinsame Zufälligkeit bei vollständiger Absprache.** Bei `q = 1` ist eine für alle Knoten gemeinsame Zufälligkeit nur
   von außerhalb des Netzes möglich (externer Beacon oder Fiat–Shamir); der Austausch von Commitments zwischen SkyNet-Knoten
   hilft nicht. Persönliche Münzen verschiedener Knoten ergeben verschiedene Entscheidungen, und eine einheitliche Berechnung entsteht nicht.
   (claude2, 3.8; gpt2, 6.1. Der Kritiker ChatGPT ergänzte: Der Beacon muss unverschiebbar und verfügbar
   sein und sich streng nach der endgültigen Annahme des Blocks offenbaren; das ist bereits Angriff 1.5 und N13
   in [THREAT_MODEL](THREAT_MODEL.md).)
8. **Kostenlose Wiederholungen.** Wenn ein Versuch nahezu umsonst wiederholt werden kann (zum Beispiel wird die Zufälligkeit
   aus dem Hash der Meldung selbst abgeleitet), wächst die Erfolgswahrscheinlichkeit mit der Zahl der Versuche. Für die Auswahl der Zellen
   darf Fiat–Shamir nicht verwendet werden. (claude2, 3.3; ds2, 5.1.)
9. **Der Prüfer, der das Ergebnis selbst aufbaut.** Wenn der Knoten selbst den gesamten Zustand berechnet
   und die Meldung nur zum Vergleich liest, erhält man durch Weglassen des Vergleichs einen ehrlichen Ausführenden
   mit derselben Arbeit. Folglich kostet eine solche Prüfung nicht weniger als 100% der optimalen Arbeit. Billig
   kann nur eine Prüfung mit Hinweis sein: mit einer fertigen Antwort, einer Spur oder einem Beweis.
   (gpt2, 9.5. Die Kritiker Claude und DeepSeek nannten dies die beste Formulierung der allgemeinen Schranke.)
10. **Zertifikat des gewinnenden Tokens.** Für einen verborgenen Zustand in allgemeiner Lage kann man den
    Gewinner nicht bestätigen, ohne Informationen über jede Zeile des Vokabulars zu erhalten, die gewinnen kann. Im schlimmsten
    Fall wird das gesamte Vokabular geprüft. (claude1, B6; gpt2, 9.3.)
11. **Private Eingabe.** Ein fremder Knoten ohne die Anfrage kann die Antwort nicht prüfen, wenn es keinen
    Zero-Knowledge-Beweis gibt. Der Kritiker ChatGPT präzisierte die Schranke: Ein verbergendes
    Commitment zusammen mit einem solchen Beweis könnte die benötigte Eigenschaft übertragen, und das Lemma
    schließt das nicht aus. (claude2, 3.7; ds2, 6.2; gpt1, §1.)

### 2.2. Unmöglichkeitsaussagen, die die Kritiker widerlegten

1. **„Das wörtliche D1 verlangt einen Fehler von genau null“** (ds1, F1). Das gilt nur, wenn ein Versuch nichts
   kostet. Wenn die Zufälligkeit extern und unvorhersehbar ist und jeder Versuch eine neue Fixierung
   verlangt und `c_min > 0` kostet, dann gilt `Δ₀ ≤ εR − c_min ≤ 0` bei `ε ≤ c_min/R` (claude1, Lemma 4; ds2, 5.1).
   Der eigene Kandidat von ds1 stützt sich ebenfalls auf einen Hash mit einem Fehler größer als null. Widerlegt haben es alle drei
   Kritiker. Vorbehalt des Kritikers ChatGPT: Eine untere Schranke des Preises des billigsten Versuchs für jede
   Koalition hat das Projekt noch nicht festgestellt, daher ist ein kleiner Fehler mit D1 nur bedingt vereinbar
   (Frage 2 in Abschnitt 6).
2. **„Die Prüfung einer fertigen Antwort kostet definitionsgemäß +100% der Zeit“** (ds1, F2). Falsch für
   eine fertige Antwort: Bei der Prüfung aller Positionen in einem Durchlauf werden die Gewichte einmal gelesen, nicht für jedes
   Token. Nach der Zahl der Operationen ist die Prüfung tatsächlich gleich der Generierung, aber nach der Zeit kann sie bei der Generierung
   einer Antwort nach der anderen dutzendfach schneller sein. Außerdem verglich ds1 nicht vergleichbare Gewichtsprofile.
   Widerlegt haben es alle drei Kritiker.
3. **„Eine exakte lineare Prüfung verlangt mindestens `N` Formen und `N²` Operationen“** (ds1, F3). Falsch
   doppelt: Frische Koeffizienten nach der Fixierung ergeben einen Durchlass mit einer Wahrscheinlichkeit von etwa `Q^(−s)`, und über
   beschränkten ganzen Zahlen genügt eine Form mit Bitpacking `Σ y_i·B^i` bei `B > 2U`
   (gpt1, 5.3; gpt2, 6.2); die Einheitsmatrix liest die Koordinaten in `O(N)`. Widerlegt haben es alle drei
   Kritiker.
4. **„Der minimale Traffic der Prüfung einer Antwort entspricht der Größe der Berechnungsspur“** (Schlussfolgerung aus Lemma 5.3
   von ds2). Die Prüfung einer fertigen Antwort braucht nur die Token der Antwort, und der Prüfer eines kurzen Beweises
   liest den Beweis und die Wurzeln, nicht die Daten selbst. Widerlegt haben es alle drei Kritiker.
5. **„Jede ehrliche Generierung muss so viele Operationen ausführen wie die Prüfung in einem
   Durchlauf“** (claude1, §4.1 und B5). Das ist eine obere Schranke des Preises der Prüfung, keine untere (Kritiker
   Claude), und sie gilt nicht, wenn der Ausführende einen rechtmäßigen Cache des fertigen Ergebnisses hat
   (Kritiker ChatGPT).
6. **„Eine billige exakte Prüfung ist ohne geheime Zufälligkeit oder Kryptografie unmöglich“** (claude2, 3.5).
   Ein Gegenbeispiel ist die exakte Normalgleichung der Ridge-Regression über rationalen Zahlen, die deterministisch
   geprüft wird (Kritiker ChatGPT).

### 2.3. Strittige oder bedingte Schranken

- **Größe des Examens `n ≳ 2σ²·ln(1/ε)/δ²`** (claude2, 3.10). Die Kritiker Claude und DeepSeek verwenden sie
  als Arbeitswert. Der Kritiker ChatGPT zeigte, dass sich aus einer einzigen Varianz kein notwendiges
  `n` für jede Verteilung ableiten lässt: nötig sind vorgegebene Alternativen und eine unabhängige Stichprobeneinheit.
  **Strittig**: taugt als Schätzung im genannten Modell, nicht als Satz.
- **Quantitative Barriere eines vollständigen Beweises** (claude2, 3.9): Ein Budget von 5% lässt etwa 1–5,
  ein Budget von 20% etwa 6–18 Feldoperationen je nichtlinearer Zelle, während bekannte
  Rundungskonstruktionen Dutzende, softmax Hunderte kosten [Berechnung bei angenommenen Kosten]. Alle
  Kritiker stimmen zu, dass dies eine Schranke bekannter Konstruktionen ist, kein Satz.


---

## 3. Modellantwort (a)

### 3.1. Alle betrachteten Mechanismen

„Preis“ ist als Aufschlag auf die Arbeit der ehrlichen Ausführung angegeben; alle Zahlen sind [Berechnung] nach den Parametern
der Arbeiten. „Urteil“ ist das Ergebnis nach drei Kritiken und unter Berücksichtigung von D6–D17.

| Mechanismus (Arbeiten) | Wesen | Garantie und Annahmen | Daten des Knotens | Absprache und Gegenbeispiel | Preis [Berechnung] | Urteil |
|---|---|---|---|---|---|---|
| **Vollständige Wiederholung durch jeden Knoten**, kausaler Durchlauf über die fertige Antwort (alle sechs) | Der Knoten mit der Eingabe berechnet selbst alle Positionen und prüft jedes Token und den ersten Grund für den Abbruch | Fehler null bei exaktem Profil, echter Eingabe und fehlerfreiem Kern | Anfrage, Antwort, Modell, Profil, Seed | Absprache hilft nicht: Die eigene Neuberechnung entscheidet | Etwa 100% der Operationen für jeden der `N` Knoten; ein fremder Knoten sieht die private Anfrage nicht | **Hält** als Referenz stand; in 5% passt es bei Prüfung durch alle Knoten nicht |
| **I1 / PPS** (claude1): Der Zahler prüft | Der Zahler rechnet Anfrage und Antwort in einem Durchlauf im Ganzzahlprofil „INT-Kanon“ nach; Bezahlung nur aus seiner Vorauszahlung; für die bezahlte Anfrage gibt es keine Ausgabe von Credits und kein Gewicht | Fehler null unter A1 (gleiche Bits auf verschiedener Ausrüstung **und** bei punktweiser Dekodierung und Durchlauf der gesamten Sequenz auf einer Karte), A2 (das Journal speichert), A3 (Hash, Verschlüsselung), A4 (der Zahler veröffentlicht den Fehlerbeweis fristgerecht), A5 (die Daten des Streitfalls sind verfügbar) | Anfrage, Antwort (`T·4` Byte), Fingerabdrücke des Modells und des Profils, Seed; Gewichte im Speicher 4,02 GB für 4B W8, 12,8–25,6 GB für 27B | Es entscheidet der einzige Teilnehmer, dessen Geld auf dem Spiel steht; die Absprache „Zahler + Ausführender“ verschiebt nur ihre eigenen Credits | 4B, 500/500, RTX 2060: 3,98·10¹² MAC, 0,19 s gegen 7,5 s Generierung — etwa 2,5–2,6%; alle Szenarien 1,2–3,8% bei der Generierung einer Antwort nach der anderen; 8–22% bei Batch 8; 21–48% bei Batch 32. Ohne GPU etwa 8 s für 1000 Token auf dem Prozessor — 100–300% | **Hält mit Korrekturen stand** (alle drei Kritiker); die Korrekturen in 3.2 |
| **I8 — Streitfall über die Wurzeln der Schichten** (claude1) | Der Ausführende fixiert Fingerabdrücke des Residualstroms je Schicht. Der Zahler findet den ersten Block, in dem die Neuberechnung abweicht, und veröffentlicht dessen Eingabe; jeder Knoten rechnet einen Block nach. Ohne Beweis im Fenster geht die Bezahlung an den Ausführenden | Einen falschen Fehlerbeweis gibt es unter A1 nicht; eine falsche Ablehnung durch den Zahler ist unmöglich | Eingabe des Blocks (10–20 MB bei 1000 Positionen), Gewichte einer Schicht (101–388 MB) | Die Prüfung entscheidet jeder Knoten selbst. Gegenbeispiele: Der Ausführende legt nur den Fingerabdruck des Chiffretexts ins Journal und gibt die Antwort selbst nicht heraus; das Journal ist bei ausgelieferter und zurückgehaltener Antwort gleich; die Zensur des Blocks im Fenster hängt an externen Validatoren | Etwa 1,0·10¹¹ MAC je Knoten für 4B, 3,9·10¹¹ für 27B; bei 1000 Knoten ein falscher Streitfall — in der Größenordnung von 10–20 GB Netzverkehr (Schätzung des Kritikers Claude) | **Hält mit Korrekturen stand**: Chiffretext im Journal, Grenze falscher Streitfälle, Rechtzeitigkeit und Zensur als ausdrücklich genannte Annahmen |
| **M1 — Freivalds des Zahlers mit geheimem Vektor** (ds2) | Der Zahler rechnet die elementweisen Operationen nach und prüft die Matrizenmultiplikationen mit Skalarprodukten auf seinem frischen geheimen Vektor | Fehler nicht größer als `N/p` über alle Gleichungen, bei `p ≈ 2⁶¹` vernachlässigbar; nötig sind eine Bereichsprüfung und rohe Summen vor der Rundung | Berechnungsspur vom Ausführenden | Der Zahler prüft selbst. Gegenbeispiel zum Caching des Vektors: Kennt der Ausführende den Vektor einer Schicht, steuert er den Ausgang dieser Schicht in allen künftigen Anfragen (Kritiker DeepSeek) — der Vektor muss für jede Anfrage frisch sein | Angegeben 2,7%; nicht reproduzierbar: softmax 0,79% statt 2,45%, und bei einem Preis der Feldmultiplikation von 10–100 MAC ergeben die Projektionen +1,6–15,8% (Kritiker DeepSeek). Traffic — **strittig**: etwa 14 MB je Token mit rohen int32 und etwa 15 GB Spur einer Anfrage aus 1850 Token (Kritiker Claude); 7,419 MB je Token selbst in INT16 und 7,477 GB Prefill (Kritiker ChatGPT); etwa 2,4 MB je Token, wenn der Zahler die Attention-Bewertungen selbst nachrechnet (Kritiker DeepSeek) | **Hält als Prüfung stand** für einen Zahler ohne GPU, aber mit schnellem Kanal; der angegebene Preis ist widerlegt |
| **I2 — Stichprobenschichten** mit frischer Zufälligkeit des Knotens (claude1; ds1, 3.1; gpt2, §8) | Der Knoten prüft `m_s` zufällige Schichten von `L` anhand der Fingerabdrücke | Durchlass eines einzelnen Fehlers mit einer Wahrscheinlichkeit von `1 − m_s/(L+1)` | Eingabe der Schicht, Gewichte der Schicht | Fälschung: Antwort durch ein kleines Modell plus ehrliche Spur des großen; ein Übergang ist verfälscht, danach eine konsistente Fortsetzung | Hashing der Spur 0,38–4 GB; 1–8% beim Ausführenden je nach Hash-Geschwindigkeit | **Widerlegt** für ein leeres Konto (Schranke 2.1, Nr. 4); taugt nur für Schlüssel mit `H ≥ 35–64R` |
| **PVYa** (claude2): Der Nutzer prüft eine Stichprobe von Zellen „Block × Token“ mit seiner geheimen Zufälligkeit | Auswahl der Zelle proportional zu ihrem Anteil an den Operationen | Nur Geldgewinn, nicht der Schaden | Zellen der Spur, Pfad im Baum der Fingerabdrücke | Gegenbeispiel des Kritikers Claude: Antwort durch ein kleines Modell und ehrliche Prefill-Spur; eine zeitlich billige Fälschung wird mit einer Wahrscheinlichkeit von etwa 0,3–1% erkannt, `Δч ≈ +0,94c`. Kritiker ChatGPT: Im Modell gleicher Kosten `Δ₀/c = +0,019`; nötig ist auch die Bindung der Schlüssel und Werte der Attention an das Präfix | Für den Nutzer von <0,001% bis 2,7%, die strenge Variante etwa 5,6%; für den Ausführenden das Hashing von etwa 4 GB Spur — 2–4 s Prozessor, 30–50% der Zeit der Anfrage auf einer RTX 2060 | **Widerlegt** (Kritiker Claude und ChatGPT). Der Kritiker DeepSeek nahm ihn mit einer Trennung der strengen und der relativen Variante an, aber die relative Variante erfüllt die zweiseitige Schreibweise von D1 nicht, und nach D6 ist auch eine Garantie hinsichtlich des Schadens nötig, die PVYa nicht bietet |
| **I3 — Freivalds über die Spur** durch einen Netzknoten (claude1; ds1, 2.2; gpt1; gpt2, 6.1) | Prüfung jeder Multiplikation auf einen zufälligen Vektor anhand der gesandten Spur | `≤ 1/p` je Fehler; nötig sind rohe Ausgänge vor der Rundung | Die gesamte Spur | Absprache hilft nicht, wenn der Vektor frisch ist | Spur 4,4 GB je Antwort (4B), 15,2 GB (27B); für Prefill von 4096 Positionen allein gate/up — 5,74 GB in INT16 gegen 0,755 GB in der Kostenschätzung von ds1 (Kritiker ChatGPT) | **Widerlegt als billige Prüfung**: stößt an den Traffic, nicht an die Arithmetik |
| **I4 — Tabellen der Partialsummen** (alle sechs) | Der Knoten baut im Voraus Tabellen der Ausgänge einer Schicht nach Gruppen von Eingaben | Exakt bei kanonischen Gewichten | Tabellen | — | Gruppe 2: 859 GB für eine Matrix 4B, etwa 476 TB der gesamte Körper; Bitebenen — nicht weniger als 128 Modellgrößen | **Durch Berechnung widerlegt** (alle Kritiker) |
| **I5 — Zertifikat des gewinnenden Tokens** (claude1; ds1, 2.5; gpt1, 4.3; gpt2, 5.3) | Baum von Clustern der Zeilen des Kopfes mit bewiesenen oberen Schranken | Exakt für die gierige Auswahl bei vollständiger Abdeckung des Vokabulars und geprüftem verborgenen Zustand | Verborgener Zustand der letzten Schicht | Ein ersetzter verborgener Zustand bestätigt ein anderes Token | Spart nicht mehr als den Anteil des Kopfes: 2,10% / 0,60% (gpt1), 6,04% / 1,76% (gpt2), bis 9,67% (claude1); im schlimmsten Fall das gesamte Vokabular | **Hält als Teil** der Prüfung stand (gierige Auswahl) |
| **Gumbel-max als kanonischer Sampler** (claude1; claude2, 5.5) | Die Auswahl mit Temperatur reduziert sich auf `argmax(z/τ + g)` mit Rauschen aus einer PRF nach dem Seed | Die Identität gilt | Seed | Die Verteilung unterscheidet sich von der gewöhnlichen Top-p-/Top-k-Stichprobe — das ist eine Produktänderung | Frisches Rauschen für jedes Token: etwa `V` PRF-Werte und Gruppenmaxima, 75,97 Mio. PRF-Werte für 500 Token | **Hält** als Art, die Auswahl festzulegen; die Einsparung des Zertifikats für die Stichprobe ist **nicht begründet** (Kritiker DeepSeek und ChatGPT) |
| **Gumbel-Zertifikat „mit Spielraum“** (claude2, 5.5) | Der fast gewinnende Token wird innerhalb einer Toleranz angenommen | — | — | Gegenbeispiel: Bei gleichen Logits und einem Rauschunterschied kleiner als `2η` kommt ein falsches Token durch (Kritiker ChatGPT); jede Toleranz öffnet eine Ersetzung (ds2, 6.4) | — | **Widerlegt** |
| **Intervallzertifikat mit exakter Neuberechnung bei Mehrdeutigkeit** (gpt1, 4.4; gpt2, 5.4) | Niedrigrang-Approximation der eingefrorenen Matrix und bewiesene Schranke des Rests; wo das Intervall verschiedene Rundungen zulässt, rechnet der Knoten exakt nach | Fehler null bei unabhängig berechneten Normen des Rests und obligatorischer Neuberechnung | Eigene Faktoren und Normen der Reste | Schlüssel und Werte dürfen nicht aus der Meldung des Ausführenden genommen werden | Schneller Durchlauf 0,521% der Operationen der Schicht; für 5% beträgt der Anteil mehrdeutiger Ausgänge höchstens 4,479% bei einer warmen Schicht und 1,342% bei kalter Vorbereitung (Kritiker ChatGPT). Kritiker Claude: Bei Gewichten nahe dem vollen Rang überdecken die Intervalle fast sicher viele Zellen, und der Preis liegt nahe bei 100% | **Hält** mathematisch stand; der **Preis ist strittig**, nicht gezeigt |
| **Exaktes Bitpacking** (gpt1, 5.3; gpt2, 6.2) | Eine lineare Form `Σ y_i·B^i` über ganzen Zahlen | Exakt bei `B > 2U` und bewiesenen Bereichen | Rohe Summen | Kleine Aufzählung: bei `B = 8` 9 richtige Annahmen und 0 falsche, bei `B = 4` 20 falsche von 29 (von zwei Kritikern wiederholt, die Hashes stimmten überein) | Fast ohne Gewinn: für W8A16 bei einer Breite von 3072 ein 64-Bit-Wort je Ausgang | **Hält** als exaktes Primitiv stand, bringt keine Verbilligung |
| **Cache geprüfter Präfixe** (gpt2, 5.1) | Der Knoten verwendet einen Zustand wieder, den er selbst abgeleitet hat | Exakt für dieselbe Position und Version | Eigener Cache | Eine fremde Wurzel kann einen falschen Zustand binden | Gewinn nur bei Wiederholungen; derselbe Cache ist dem Ausführenden zugänglich | **Hält stand**, verbilligt im Allgemeinen nicht |
| **Kurze Beweise sumcheck/GKR** für die Antwort (claude1, I6; claude2, 4.9 und 5.7) | Der Ausführende beweist den gesamten Durchlauf; jeder Knoten prüft den Beweis | Rechengarantie; eine durchgängige Fehlerschranke für den Graphen von Qwen ist nicht abgeleitet | Beweis, Gewichte für die Auswertung an einem zufälligen Punkt | Absprache hilft nicht bei vollständigem Schema und geprüften Eingaben | Richtwert FlashProve 70–95× seines Profils (der Nenner ist unklar); Schätzung von claude2 — 6–20 Mal teurer als die Arbeit bei Kontext 2048; in der günstigsten Lesart etwa 16,8× (Kritiker ChatGPT) | **Hält** als bedingte Garantie stand; in 5% **passt es nicht** |
| **Die Aufgabe ändern: einen prüfbaren Ausgang bezahlen** (claude1, I7; claude2, 5.4; gpt1, 3.1; gpt2, 4) | Zum Beispiel ein Vektor, der eine SAT-Formel erfüllt, Code, der Tests besteht, eine Lösung mit prüfbarer Antwort | Exakt für ihr Prädikat | Aufgabe und Ergebnis | Der Ausführende kann ein richtiges Ergebnis senden, das das Modell nicht ausgegeben hat; nach D2 ist das zulässig | SAT-Prüfung — höchstens `3m` Lesezugriffe | **Hält für eine enge Klasse stand**; der Anteil solcher Anfragen ist unbekannt; der freie Dialog ist nicht abgedeckt |
| **P0 / M4 — eine bezahlte Anfrage ergibt keine Ausgabe und kein Gewicht** (claude1, claude2, ds2) | Das Geld geht nur vom Zahler zum Ausführenden über | Die Übertragung eigener Credits ist innerhalb der Koalition neutral | — | Ohne diese Regel schützt die Prüfung durch den Zahler das Netz nicht (Schranke 2.1, Nr. 2) | 0 | **Hält stand**; stimmt mit D17 überein |
| **Batch-Verifier eines dedizierten Knotens, Bezahlung nur des Prefills** (ds1, 3.3–3.4) | Ein Knoten prüft das Batch; bezahlt wird der exakte Prefill | — | — | Die Signatur des dedizierten Knotens ist bei echter und simulierter Prüfung gleich; ein exakter Prefill mit erfundener Antwort kommt durch | — | **Widerlegt** (Kritiker ChatGPT) |
| **Produkt der Fehlerwahrscheinlichkeiten verschiedener Knoten** (ds1, 3.2) | Jeder Knoten prüft mit seiner eigenen Zufälligkeit | — | — | Funktioniert nur bei obligatorischer Annahme durch alle ehrlichen Knoten; bei `q = 1` gibt es sie nicht | — | **Widerlegt** |
| **Offener Streitfall im Fenster** (alle sechs) | Jeder kann bis zum Ablauf des Fensters Einspruch erheben | Nötig ist ein ehrlicher Beobachter mit Daten und Zeit | — | Wenn alle, die die Daten sahen, schweigen, kommt ein falsches Ergebnis mit Wahrscheinlichkeit 1 durch; der Pilot zeigte das | Pilot: 93 Transaktionen und 5,8–6,3 Mio. gas im Streitfall Cartesi | **Widerlegt** als eine von der Absprache unabhängige Prüfung; D8 beschränkt zudem den Kreis der Bestreitenden |
| **Delegierung durch einen schwachen Zahler** (claude1, 4.10) | Der Zahler überträgt die Prüfung seinem Gerät oder einem gewählten Knoten | Das Vertrauen in den Gewählten ist eine Annahme des Zahlers | — | Bei zufälliger Wahl kommt die Abhängigkeit von `q` zurück | — | **Annahme**, keine Lösung |

### 3.2. Bester Kandidat für die Modellantwort und Korrekturen der Kritiker

**Kandidat.** Die gesamte Antwort prüft der Zahler selbst. Wenn er eine Grafikkarte hat, auf die
das Modell passt, ist das PPS (claude1). Wenn es keine Grafikkarte gibt, aber einen schnellen Kanal, ist das M1 (ds2)
mit einem frischen geheimen Vektor für jede Anfrage. In beiden Fällen ergibt eine bezahlte Anfrage keine Ausgabe
von Credits und kein Gewicht (P0; das stimmt mit D17 überein), und den Streitfall entscheidet jeder Knoten anhand des Fehlerbeweises
(I8). Warum die Absprache nicht hilft: Die Entscheidung trifft der einzige Teilnehmer, dessen Geld auf dem Spiel steht;
er hat die vollständigen Daten — Anfrage, Antwort und Modell; die Prüfung ist vollständig, nicht stichprobenartig.

**Korrekturen, ohne die der Kandidat nicht standhält.**

1. **Zurückhalten der Antwort.** Ins Journal muss der Chiffretext der Antwort selbst gelegt werden, nicht nur sein Fingerabdruck:
   etwa 2–4 KB je Antwort (Kritiker Claude). Das stimmt mit D10 überein: Austausch mit einem einzigen Journal-Eintrag.
2. **Falsche Streitfälle.** Die Koalition „Zahler = Ausführender“ kann beliebig viele kleine
   Anfragen erzeugen und zu jeder einen Streitfall einreichen, den alle Knoten herunterladen und nachrechnen. D8 begrenzt den
   Strom der Streitfälle durch die Zahl der Anfragen, aber selbst bezahlte Anfragen werden durch diese Grenze nicht beschränkt. Eine Lösung
   hat keine Arbeit gegeben (Abschnitt 5, Aufgabe M9).
3. **Rechtzeitigkeit und Zensur.** Der Zahler muss im Netz sein und es schaffen, den
   Beweis im Fenster zu veröffentlichen, und das Journal muss ihn annehmen. Die Zensur eines Blocks im Fenster hängt an der Ehrlichkeit
   der externen Validatoren des Journals. Das ist eine Annahme über eine Absprache in einer anderen Menge; man muss sie
   ausdrücklich benennen. Beim Telefon des Zahlers wird sie am häufigsten verletzt. Das Fenster wird nach D12 in der aktiven
   Zeit des Netzes gezählt.
4. **Bindung der Enden.** Ein Streitfall über die erste Schicht verlangt die Bindung an die ursprüngliche private Anfrage, ein Streitfall
   über die letzte — an den bezahlten Chiffretext (Kritiker ChatGPT).
5. **Abbruch.** Geprüft werden muss der erste Grund für den Abbruch. Die Bedingung „das letzte Token ist EOS oder
   das Limit ist erreicht“ lässt eine Antwort durch, die nach einem frühen EOS weitergeschrieben wurde (Kritiker ChatGPT).
6. **Arithmetik des INT-Kanons.** Das Produkt der Attention-Wahrscheinlichkeiten mit den Werten wird in der Spezifikation
   in int64 akkumuliert. Wenn man es nicht auf Tensor-Kernen ausführt, wächst der Preis des langen Szenarios
   2000/1000 von 3,8% auf etwa 8% (Schätzung des Kritikers Claude); der Ausweg ist, die 16-Bit-Wahrscheinlichkeit
   in zwei 8-Bit-Hälften zu zerlegen. Der Kritiker ChatGPT fand noch drei Lücken: Bei einem einzigen
   erlaubten Schlüssel ergibt softmax den Wert 65 536, der nicht in 16 Bit passt; die Quadratsumme
   in RMSNorm kann int64 überlaufen (drei Komponenten zu `2³¹−1` ergeben bereits mehr als `INT64_MAX`); nötig sind
   ausdrückliche Breiten, RoPE-Positionen und die Reihenfolge der Rundung. Das Prinzip selbst hält diese Korrekturen aus.
7. **Streaming-Ausgabe.** Nach D6 darf der Nutzer ungeprüften Text nicht als geprüft sehen.
   Bei der Streaming-Ausgabe muss jedes gezeigte Präfix geprüft werden, und die Häufigkeit solcher Prüfungen
   geht in den Preis ein (gpt2, §1).

**Einschränkungen des Kandidaten.**

- Der Preis von 1,2–3,8% gilt nur bei der Generierung einer Antwort nach der anderen. Für den Ausführenden ist es vorteilhaft,
  Anfragen zu Batches zusammenzufassen, und bei Batch 8–32 ergibt der ehrliche Vergleich 8–48% [Berechnung].
- Den Verbraucher ohne Ausrüstung deckt der Kandidat nicht ab. Für 27B braucht der Zahler mindestens
  13 GB Videospeicher. Der Hauptverbraucher nach den Anforderungen ist der Teilnehmer ohne Ausrüstung. Nach D6 kann seine
  Antwort nur mit der Markierung „nicht geprüft“ ausgegeben werden; wie dabei der Ausführende ohne Verletzung von D1
  bezahlt wird, hat keine Arbeit gelöst.
- Alles hängt an der nicht gemessenen Annahme A1: Übereinstimmung der Bits auf verschiedenen Grafikkarten **und** zwischen
  punktweiser Dekodierung und Durchlauf der gesamten Sequenz auf einer Karte. Wenn es in Qwen3.5
  rekurrente Schichten linearer Attention gibt, rundet ihre parallele Form anders, und der Preis
  der Prüfung kann auf etwa das Doppelte wachsen (claude1, 3.4, Schätzung bei angenommenen 10 µs je Schritt).
- Ein Streitfall offenbart die Anfrage: Die Eingabe des Blocks rekonstruiert den Text fast reversibel. Einen Streitfall ohne Offenlegung
  gibt es nicht.
- Die Energie ist nicht gemessen: Wenn die Berechnungen der Engpass sind, verbraucht die Grafikkarte mehr als wenn der Speicher der Engpass ist,
  daher kann der Anteil an der Energie größer sein als der Anteil an der Zeit.
- Beschleuniger (Intervallzertifikat, Gewinner-Zertifikat für die gierige Auswahl, Cache eigener
  Präfixe) sind nur zusätzlich zur vollständigen Prüfung zulässig, nicht an ihrer Stelle.


---

## 4. Trainingsschritt (b)

### 4.1. Alle betrachteten Mechanismen

Der Hauptunterschied zur Modellantwort: Beim Trainingsschritt gibt es keinen Zahler, dessen Geld auf dem Spiel steht. Die Bezahlung
erfolgt durch die Ausgabe von Credits, daher muss nach Schranke 2.1, Nr. 2 jeder vollständige
Knoten die Grundlage prüfen. Nach D15 wird eine solche einfache Neuberechnung zudem nicht bezahlt.

| Mechanismus (Arbeiten) | Wesen | Garantie und Annahmen | Daten des Knotens | Absprache und Gegenbeispiel | Preis [Berechnung] | Urteil |
|---|---|---|---|---|---|---|
| **T1 — vollständige Wiederholung des Übergangs** durch jeden Knoten (alle sechs) | Der Knoten wiederholt den Schritt aus dem angenommenen Elternmodell und vergleicht den gesamten nächsten Zustand, einschließlich der Master-Gewichte, der Momente m, v des Optimierers und der Schrittnummer | Fehler null bei exaktem Profil und echten Daten | Elternmodell, Datencharge, Regeln | Nur die Gewichte zu prüfen ist zu wenig: Dieselben Gewichte mit zurückgesetztem v ändern den nächsten Schritt (Kritiker ChatGPT) | +100% für jeden Knoten, insgesamt `N × 100%`; zum Beispiel etwa 2,62·10¹⁵ MAC für die Neuberechnung einer Charge von 64 × 4096 für 4B | **Hält** als Referenz stand; in 20% passt es nicht |
| **T2 — Stichprobenschichten, Mikropakete, Schritte** (claude1; ds1, 3.1) | Der Knoten prüft einen zufälligen Teil des Schritts | `1 − m_s/L` Durchlass | Teil der Spur | Fälschung: ein zufälliges oder kopiertes Update abgeben; einen Randgradienten ersetzen | Bei `N = 1000`, 36 Schichten und einer geprüften Schicht — etwa 28 Arbeiten je Schritt | **Widerlegt** (Schranke 2.1, Nr. 4) |
| **VYa-S** (claude2): Der Beacon wählt Zellen „Block × Sequenz“, jeder Knoten prüft ihren komprimierten Beweis | Wahrscheinlichkeit durchzukommen `(1 − f)^s` bei einem Fälschungsanteil `f` | Externer Beacon, Hash, Beweis der Zelle; nur Geldgewinn, nicht der Schaden | Beweise der gewählten Zellen | Kritiker Claude: Das Kopieren der Spur einer Sequenz auf die ganze Charge — inkonsistent sind nur die Bindungszellen (etwa 10,5% des Gewichts); bei `s = 30` `Δ₀ ≈ +0,036R`, bei `s = 10` `Δ₀ ≈ +0,33R` und `Δч ≈ +0,26c`. Kritiker ChatGPT: Ein Nullgradient an der Grenze des Blocks macht alle unteren Zellen intern richtig; in die Formel wurde der Anteil der gesparten Arbeit statt des Anteils falscher Gleichungen eingesetzt; selbst bei deren Gleichheit `Δ₀/c ≈ +0,096`. Kritiker DeepSeek: Erfüllt ist nur `Δч ≤ 0`, während D1 auch `Δ₀ ≤ 0` verlangt | Beweise 0,66%, erneute Zählung der Eingaben 0,39%, Hashing 3,7–10% bei `s = 30`; Schichtgrenzen — 96,64 GB je Aufgabe aus 64 Sequenzen und 11,60 TB je Aufgabe aus 7680 | **In der jetzigen Form widerlegt** (alle drei Kritiker). Die vorgeschlagene Reparatur ist eine gesonderte Prüfung der Bindung anhand zufälliger Sequenzen; nicht berechnet |
| **T3 — kurzer Beweis des Schritts** sumcheck/GKR mit Commitments (claude1, T3; claude2, 4.9; ds1, 2.9; gpt1, 6.3; gpt2, 7.2) | Der Ausführende beweist den gesamten Übergang, jeder Knoten prüft einen Beweis | Rechengarantie bei vollständigem Schema mit Bindung der Eingabe, Rundungen, Bereichen und Optimierer; eine durchgängige Fehlerschranke ist nicht abgeleitet | Beweis, Wurzeln, ein Durchlauf über die Gewichte je Batch | Absprache hilft nicht bei gemeinsamem Transkript | Richtwert VeriLoRA etwa 137× (121,93 s Beweis für 0,89 s Training, ein anderes Modell mit 3B); das Budget lässt 11,43% — eine Lücke von etwa 1200×. Für das 1.5B-Profil eine exakte softmax-Division — 11 973 394 432 Feldzellen und 10 998 054 912 Bereichsprüfungen, 356,835 GiB vor der Ausrichtung; Schreiben von 3,067 TB bei 100 GB/s — 30,67 s gegen 6,6 s des Budgets bei einem Schritt von 60 s | **Hält als Richtung stand**; konkrete Aufteilungen sind widerlegt, 20% sind nicht gezeigt. Der Kritiker ChatGPT hält dies für den stärksten Forschungszweig für den unveränderten Schritt |
| **M1 für das Training** (ds2) | Geheimer Vektor plus Neuberechnung der elementweisen Operationen | Wie in 3.1 | Spur | Keine Bindung der Spur an die zugewiesene Charge: Eine richtige Berechnung auf ersetzten Daten kommt durch (Kritiker DeepSeek) | Angegeben 1,5%; die elementweisen Rückwärtsoperationen (etwa ×2–2,5) und der Preis der Feldmultiplikation sind nicht berücksichtigt. Traffic 16,08 GB je Schritt in INT16, 64,318 GB in INT64 — nicht weniger als 514,5 s bei 1 Gbit/s | **Widerlegt** für das Training hinsichtlich Traffic und Bindung |
| **Freivalds über die Spur des Schritts** (ds1, 2.2; gpt2, 6.1) | Prüfung jeder Multiplikation des Schritts | `≤ p^(−t)` | Die gesamte Spur | — | 64,3 GB je Schritt (1.5B); 123,92–410,44 GB für LoRA und 369,72–2073,34 GB für vollständiges Training je Schritt (gpt2); nicht weniger als 991 s bei 1 Gbit/s | **Widerlegt** als billige Prüfung |
| **T5 — der Schritt als Update-Formel** (alle sechs) | Die Knoten prüfen die Update-Faktoren, nicht die neue Matrix | Prüft nur die letzte Addition | Faktoren | Gegenbeispiel: Ein gesandter Gradient `G = 0` bei einem wahren von null verschiedenen besteht die Prüfung der Formel | Etwa 10⁻⁶ der Arbeit | **Widerlegt** als Prüfung des Schritts; die Neuberechnung des Optimierers und der Addition gehört zum Kern |
| **Nur das LoRA-Delta** (ds1, 3.5) | Nur den Adapter prüfen | — | — | Der Ausgang des eingefrorenen Teils hängt von der neuen Eingabe ab | — | **Widerlegt** |
| **T4 — Bezahlung für die Verbesserung**, gemessen von jedem Knoten an einer frischen Stichprobe (claude1) | Die Aktualisierung wird vor der Runde fixiert; ein externer Beacon wählt `n` Positionen des Examens; jeder Knoten berechnet selbst die abgeschnittene Verlustdifferenz; bezahlt wird die Überschreitung der Vertrauensschwelle | Bezahlung einer Aktualisierung ohne Verbesserung mit einer Wahrscheinlichkeit von `≤ ε = 2⁻⁴⁰` bei externem Beacon, Stichprobe mit Zurücklegen, exaktem Profil und Fixierung vor dem Beacon; der Preis eines Versuchs muss mindestens `ε·κ·B/2` betragen | Examen-Pool, alle `K` Aktualisierungen der Runde | Es gibt keine Prüfer, jeder Knoten rechnet. Gegenbeispiele: (1) Das Abschneiden der Differenzen bezahlt eine schädliche Aktualisierung: +0,01 nat auf 99,5% der Positionen und −20 auf 0,5% ergeben nach dem Abschneiden +0,005 bei einem wahren Wert von −0,09 (Kritiker Claude); +0,1 auf 99% und −100 auf 1% ergeben +0,089 bei einem wahren Wert von −0,901 (Kritiker ChatGPT); (2) der öffentliche Pool erlaubt, direkt auf ihm zu lernen; (3) ein Duplikat mit Rauschen ergibt bei der Fusion durch Summe einen positiven Beitrag | Schwelle bei `B = 2`: 0,0745 nat bei `n = 10⁴`, 0,0236 bei `n = 10⁵` (Hoeffding). Um in 20% zu bleiben, braucht man `D ≥ n(1 + K·a)/0,6` Trainings-Token je Knoten und Runde; bei `K = N = 10⁴` sind das 1,85·10⁸ Token, etwa 26 h. Cache der Zustände — 0,51 GB nach Schätzung von claude1 oder 524,3 GB in int16, wenn die Positionen aus verschiedenen Präfixen zu je 1024 Token genommen werden (Kritiker ChatGPT) | **Hält mit Korrekturen stand** als neue Vergütungseinheit; prüft den Schritt nicht. Strittig ist, ob die selektive Offenlegung von Kandidaten nach dem Beacon gefährlich ist: Kritiker Claude — nein bei `ε = 2⁻⁴⁰`, Kritiker ChatGPT — nicht berücksichtigt |
| **ODU** (claude2): Bezahlung für eine bewiesene Verbesserung in einem Examen, das der Beacon nach der Fixierung wählt | Der Einreichende beweist das Examen; jeder Knoten prüft den Beweis und rechnet nicht nach | Wie T4, aber beseitigt das Wachsen des Preises mit der Zahl der Knoten; das Training kann in beliebiger Arithmetik erfolgen | Beweis des Examens | Kritiker Claude: Der Einreichende berechnet das Examen bei sich umsonst und beweist nur die gewinnenden Kandidaten, daher braucht man `ε ≲ 0,23%`, nicht 10%. Kritiker ChatGPT: dasselbe Argument, plus die adaptive Auswahl an einem gemeinsamen Examen und dass sich die Auszahlung nach der Vertrauensgrenze nicht teleskopartig addiert (0,16 statt 0,20 im Beispiel). Kritiker DeepSeek: `ε = 10%` besteht formal, aber nur auf Kosten des gesamten 20%-Budgets | Beweis des Examens etwa 2,4 h je Kandidat, nacheinander: Bei 100 Kandidaten dauert eine Epoche nicht kürzer als 10 Tage (Kritiker Claude). Anteil des Examens 0,655% der Trainings-Token, 0,327%, wenn auch das Elternmodell bewiesen wird — etwa 858 Token, weniger als eine Sequenz der Länge 4096 (Kritiker ChatGPT) | **Hält mit Korrekturen stand** als Gerüst; `ε` — **strittig** (2 von 3 Kritikern: nötig ist viel weniger als 10%); die Attribution ist nicht gelöst |
| **Examen von ds1** (ds1, 2.8): 20–82 Token, „Fehler null“ | Bezahlt wird die Verbesserung in einem kleinen Examen | „Fehler null“ nur per Definition | — | Das Rauschen des Mittelwerts beträgt etwa 0,28 nat auf 82 Token bei einer Verbesserung des Schritts von 10⁻⁴–10⁻³ (Kritiker DeepSeek) — bezahlt wird das Rauschen; die Quelle der Zufälligkeit ist nicht genannt; das Examen sieht die ersetzten Momente des Optimierers nicht | Angegeben +1–3%; beim vollen Kontext jedes der 20 bewerteten Token — 103,4% der Matrix-Kostenschätzung des Schritts (Kritiker ChatGPT) | **Widerlegt** |
| **Gedämpfter Gauß–Newton-Schritt mit dualem Zertifikat** (gpt1, 6.4) | Ein neuer Optimierer; der Ausführende gibt einen kurzen Vektor, der Knoten beweist jedes Bit des gerundeten Schritts bei `4λδ² > η²‖r‖²` | Fehler null für den neuen Schritt mit vorgegebenem linearen Modell | Exakter Forward und zwei Durchläufe der Ableitungen | Ein Gleichstand an der exakten Rundungsgrenze verlangt eine exakte Lösung (Kritiker ChatGPT) | `3N/(2k+2)`: 8,82% bei `k = 16` und `N = 1`, 75% bei `k = 1`; bei `N = 100` — Hunderte Prozent | **Hält** als geänderter Vertrag stand; der Preis wächst mit `N`, die Qualität ist unbekannt |
| **Exaktes Merkmal: Ridge-Regression, linearer Kopf** (claude1, T6; claude2, 4.1; gpt1, 3.2; gpt2, 4; ds1, 2.1; ds2, M2) | Der Knoten prüft die Optimalitätsbedingung `Xᵀ(Xw − y) + λw = 0` | Exakt bei echten Merkmalen | Merkmale, Labels | Die Merkmale müssen gesondert geprüft werden; in M2 von ds2 fehlt der Term `λw`, und ein falsches Optimum kommt durch (Kritiker ChatGPT) | 44,4% bei Rang 8 und 12,1% bei 32 relativ zum Aufbau der Matrix (gpt1); 0,390% in einer anderen Aufteilung (gpt2) | **Hält für eine enge Aufgabe stand**; das ist kein Training von Qwen, der Anteil solcher Arbeit ist unbekannt |
| **Mehrere verschiedene erste LoRA-Schritte** (gpt2, 7.3) | Bei einem Null-Adapter werden die gemeinsamen Teile einmal berechnet | Exakt | Gemeinsamer Cache | Auf die folgenden Schritte wird es nicht übertragen | 16,70% für sechs erlaubte Anfänge gegen sechs Kaltstarts | **Hält stand**, die Anwendbarkeit ist eng |
| **Training nullter Ordnung** (claude2, 5.8); **kleines Feld auf Tensor-Kernen** (claude2, 5.11); **Cache des eingefrorenen Präfixes und LoRA auf den oberen Blöcken** (claude1; claude2, 5.9) | Verbilligungen | — | — | Die nullte Ordnung ändert den Optimierer; ein kleines Feld ergibt ohne Bereichsgrenzen nicht den angegebenen Fehler | Cache des Präfixes — etwa 20,97 TB für eine Million Sequenzen der Länge 4096 | Ideen; **nicht bewiesen** |
| **T7 — offener Streitfall** (alle sechs) | — | Nötig ist ein Beobachter | — | Für das Training gibt es keinen interessierten Beobachter | — | **Widerlegt** |

### 4.2. Bester Kandidat für den Trainingsschritt und seine Einschränkungen

**Eine Prüfung des Schritts selbst im Rahmen von 20%, die nicht vom Abspracheanteil abhängt, gibt es nicht.** Das ist ein allgemeines
negatives Ergebnis, von verschiedenen Seiten bestätigt: der Maßstab `N·v`, eine Spur von 64 GB–2 TB je Schritt,
Beweise, die Dutzende- bis Hundertefach teurer sind als die Arbeit, das Budget elementweiser Operationen.

Bei **unveränderter Grundlage der Bezahlung** bleiben zwei Wege: die vollständige Wiederholung des Übergangs (Referenz, +100%
je Knoten) und langfristig ein obligatorischer Beweis des gesamten Schritts (T3). Für T3 braucht man einen konkreten
Graphen, eine bewiesene Stabilität der Komposition und eine vollständige Kostenschätzung; derzeit gibt es sie nicht.

Bei einem **Wechsel der Grundlage der Bezahlung** (Entscheidung des Eigentümers, Abschnitt 6, Frage 1) ist der beste Kandidat
die Kombination von T4 und ODU mit den Korrekturen der Kritiker:

1. Das Examen wählt ein externer Beacon streng nach der Fixierung aller Aktualisierungen und der endgültigen Annahme
   des Blocks.
2. Die Schwelle wird aus einer statistischen Schranke mit kryptografisch kleinem `ε` genommen (wie in T4), nicht 10%.
3. Das Examen wird durch einen Beweis geprüft (Gerüst von ODU), damit der Preis nicht mit der Zahl der Knoten wächst.
4. Die Verluste werden durch die Arithmetik selbst begrenzt (durch die minimale Wahrscheinlichkeit im Profil) und nicht abgeschnitten,
   sonst werden schädliche Aktualisierungen bezahlt.
5. Die Attribution von Duplikaten muss ohne eine sequenzielle Beweiskette gelöst werden. Keine Arbeit hat das
   gelöst.

**Einschränkungen.**

- Das ist keine Prüfung des Schritts. Das Examen sieht die Momente des Optimierers nicht, bestätigt nicht die Herkunft
  der Aktualisierung und schließt das Lernen am Examen selbst nicht aus.
- Nach D6 darf ein falscher Schritt nicht in das Modell gelangen. Eine Verbesserung im Examen beweist nicht, dass bei seltenen Anfragen kein Schaden entsteht
  und keine Hintertüren vorhanden sind (Q4 in [OPEN_QUESTIONS](OPEN_QUESTIONS.md)). Der Kandidat begrenzt
  den Geldgewinn, nicht den Schaden.
- Unbekannt ist, ob die ehrliche Verbesserung einer Aktualisierung die Schwelle überschreitet: Das Rauschen der Verlustdifferenz `σ`
  ist nicht gemessen. Wenn sie sie nicht überschreitet, erhalten ehrliche Teilnehmer keine Bezahlung, und R6 wird verletzt.
- Schwache Geräte mit kleiner Aktualisierung überschreiten die Schwelle nicht; „die gesamte freie Rechenleistung lernt“
  gilt nur als „lernt“, nicht als „erhält Bezahlung“.
- Zusammenhang mit D9: Der Trainingsplan wird bereits aus den Ergebnissen des Examens abgeleitet. Das macht das Examen zu einem Teil
  des Kerns, löst aber nicht die Frage, ob man für die Verbesserung statt für den Schritt bezahlen kann.

---

## 5. Was nicht bewiesen ist und womit man es prüfen kann

### 5.1. Was nicht bewiesen ist

1. Die Übereinstimmung der Bits des Ganzzahlprofils auf verschiedenen Grafikkarten und zwischen punktweiser Dekodierung
   und Durchlauf der gesamten Sequenz auf einer Karte (A1, Frage Q2). Davon hängen PPS, M1,
   das Intervallzertifikat und jede exakte Wiederholung ab.
2. Die Zeit der Prüfung einer fertigen Antwort relativ zur Generierung auf realen Karten bei Batches 1, 8, 32;
   die Energie; das Verhalten hybrider Schichten linearer Attention.
3. Die Qualität und Geschwindigkeit des Ganzzahlprofils von Qwen3.5-4B relativ zum gewöhnlichen.
4. Der Preis des Intervallzertifikats und des Gewinner-Zertifikats auf echten Gewichten.
5. Die Verfügbarkeit der Daten des Streitfalls, die Grenze falscher Streitfälle ohne Pfänder, die Rechtzeitigkeit und die Zensur des Journals.
6. Für die Bezahlung für die Verbesserung: die Größe der ehrlichen Verbesserung gegenüber der Schwelle, eine Attributionsregel ohne
   Gewinn durch Duplikate, die Verlustschranke ohne Abschneiden, der Preis des Beweises des Examens.
7. Für den kurzen Beweis des Schritts: eine vollständige Kostenschätzung eines Schritts und eine durchgängige Fehlerschranke.
8. Die genaue Konfiguration von Qwen3.5-4B und des Modells mit etwa 27B: Alle Zahlen der Arbeiten sind manuell eingesetzt.

### 5.2. Minimale Experimente

Die Entscheidung D5 erlaubt das erste Experiment: das ganzzahlige Qwen3.5-4B auf einer RTX 2060 des Heim-Linux
des Betreuers, auf seinem Computer und, mit Zustimmung, auf den Geräten anderer Teilnehmer über
Mini-Agenten, nach Phase 0. Profile, Metriken und Schwellen werden vor der Messung festgelegt. Die Bitübereinstimmung
bezieht sich nur auf die getesteten Konfigurationen.

| Nr. | Experiment | Was gemessen wird | Widerlegt den Kandidaten, wenn |
|---|---|---|---|
| O1 (D5) | Ganzzahliges Qwen3.5-4B auf zwei verschiedenen Grafikkarten | Hashes der Logits und Token auf einem Satz von Anfragen; das erste nicht übereinstimmende Token, EOS, Gleichstände, langer Kontext, Anfragen mit nahen Logits | Auch nur ein Bit unterscheidet sich bei derselben Spezifikation |
| O2 (D5) | Durchlauf der gesamten Sequenz gegen punktweise Dekodierung auf einer Karte | Derselbe Vergleich der Bits; gesondert für hybride Schichten, falls vorhanden | Auch nur ein Bit unterscheidet sich |
| O3 (D5) | Geschwindigkeit: Prüfung einer fertigen Antwort gegen Generierung | Zeit bei Batches 1, 8, 32 und Kombinationen Eingang/Ausgang 128/32, 128/128, 500/500, 2000/1000; Umsetzung des Attention-Produkts in 16 und 8 Bit; Speicher, Traffic | Der Prüfanteil bei Batch 1 ist größer als 5% |
| O4 (D5) | Geschwindigkeit des Ganzzahlprofils gegen das gewöhnliche auf denselben Karten | Token pro Sekunde, Speicher | Die Verlangsamung macht den Dienst unrentabel (Schwelle vor dem Experiment festlegen) |
| O5 (D5) | Qualität des Ganzzahlprofils gegen das gewöhnliche | Derselbe Satz von Aufgaben | Der Qualitätsverlust liegt über einer vorab festgelegten Schwelle |
| O6 (außerhalb von D5, gesonderte Genehmigung nötig) | Rauschen der Verbesserung eines LoRA-Adapters | Verteilung der Verlustdifferenz Basis/Adapter vom Rang 16 nach einem Tag Training, `σ` und `δ/σ` | Die ehrliche Verbesserung ist typischerweise kleiner als die Schwelle bei zulässiger Größe des Examens |
| O7 (außerhalb von D5; der Start von Beweissystemen ist derzeit durch eine Forschungsbeschränkung verboten) | Preis des Beweises eines Forward-Blocks auf 4096 Token | Koeffizient `P` | `P` ist größer als etwa 300 — dann passen ODU und VYa-S nicht (Schätzung von claude2) |
| O8 (außerhalb von D5) | Verhältnis des Preises der Feldmultiplikation zum Tensor-MAC auf RTX 2060 und RTX 4090 | Koeffizient `R_f` | Entscheidet alle Kostenschätzungen von Freivalds und GKR |
| O9 (außerhalb von D5) | Energie der Prüfung | Joule je Prüfung und je Generierung | Der Anteil an der Energie ist größer als der Richtwert |

### 5.3. Genaue Berechnungen, die man Mini-Agenten übertragen kann

Das sind deterministische Berechnungen ohne Messungen. Für jede Aufgabe werden die Version der Prozedur,
die Eingabebytes oder ein Generator mit Aufzählungsgrenzen, exakte ganze Zahlen oder Brüche, die Serialisierung der Antwort
und SHA-256 festgeschrieben; das Ergebnis wird auf einem zweiten Gerät wiederholt. Die Übereinstimmung bestätigt die Rechnung, aber nicht
die Semantik und nicht die ökonomische Ungleichung.

| Nr. | Aufgabe | Parameter | Was es entscheidet |
|---|---|---|---|
| M1 | Graphverzeichnis nach dem festgeschriebenen Manifest von Qwen3.5-4B und des Modells mit etwa 27B (veröffentlichte `config.json` mit Hash) | Formen und Typen aller Operationen des Füllens des Kontexts, der Generierung, der Prüfung der Antwort und des Trainingsschritts; MAC, Bytes der rohen Summen, Lebensdauer der Puffer; hybride Schichten; LoRA und vollständiges Training | Präzisiert die Zähler und Nenner aller Kostenschätzungen |
| M2 | Tabelle des Prüfanteils `ρ(B)` nach dem „Dach“-Modell | `L, d`, Breiten der Attention und MLP, Vokabular, `P, T`, Batch `B ∈ {1, 8, 32}`, Speicherbandbreite, TOPS, Anteile am Spitzenwert | Vorhersage für das Experiment O3 |
| M3 | Überlaufgrenzen des INT-Kanons | Alle Akkumulatoren nach der Spezifikation, einschließlich des Attention-Produkts bis `T ≤ 32 768`, der Quadratsumme von RMSNorm, der Größe der Wahrscheinlichkeit in softmax; Variante mit zwei 8-Bit-Hälften | Findet eine Eingabe mit Überlauf oder beweist dessen Abwesenheit |
| M4 | Genauer Traffic von M1 | Rohe int32 und Spur der Anfrage auf einem Raster (Eingang, Ausgang, Modell); mit Neuberechnung der Attention-Bewertungen durch den Zahler und ohne | Beseitigt die Meinungsverschiedenheit der Kritiker über den Traffic von M1 |
| M5 | Fälschungswelle für Stichprobenschemata mit `H > 0` | `π = m_s/(L+1)`, anfängliches `H₀`, `R`, Obergrenze offener Aufgaben; Aufzählung von Größe und Zahl der Wellen | Die minimale `H*`, bei der eine Fälschung vor dem Weggang unrentabel ist |
| M6 | VYa-S: Aufzählung von Kopierstrategien und entarteten Eingaben | Anteil `f`, Zahl der Zellen `s`, Gewichte der Zellen, Zahl der Bindungsprüfungen `s'`; vor und nach der Reparatur | Die größte `Δ₀`; ob die Reparatur standhält |
| M7 | Ökonomie des Stichprobenbeweises und der Offenlegung in ODU und T4 | `e/R`, `P`, Marge `m`, Zahl der Schlüssel und Kandidaten | Die größte zulässige `ε` |
| M8 | Maßstab von T4 | `D(N)` bei `K = N`, `n`, `a`, `ε` | Die Grenze der Zahl der Einreichenden für 20% |
| M9 | Preis eines falschen Streitfalls I8 | Traffic und Berechnungen des Netzes als Funktion von `N`, `P + T`, Schritt der Fingerabdrücke `k` | Ob und welche Grenze falscher Streitfälle nötig ist |
| M10 | Tabellen der Schwelle `t(n, ε, V̂)` | Hoeffding und empirische Bernstein-Ungleichung mit dem Term `B`; Raster `n, ε, B` | Das minimale Examen |
| M11 | Beschneidung der Verluste | Der größte bezahlte Anteil schädlicher Aktualisierungen bei `B, n, ε`; die Verlustschranke des INT-Kanons als Funktion der minimalen Wahrscheinlichkeit | Die Wahl von `B` ohne Bezahlung von Schaden |
| M12 | Attribution an einem Spielzeugmodell der Fusion | Linear-quadratische Verluste, bekannte Gradienten; Regeln „einzeln“, „einen behalten“, Shapley; Duplikate und Duplikate mit Rauschen; exakte Brüche | Ob es eine Regel ohne Gewinn durch Duplikate gibt |
| M13 | Hinweise und Gadgets des kurzen Beweises | Zahl der Werte mit Rundung, Division und Tabellen je Token und Schicht; Zellen, Tabellenzugriffe und Commitments für eine Rundungsoperation und softmax | Die Barriere 2.3 und die Kostenschätzung T3 |
| M14 | Kleine Aufzählungen zur Prüfung der Formeln | Bitpacking bei `B = 8` und `B = 4` (Wiederholung der Hashes); Kette aus 8 Übergängen mit Auswahl von 2: 224 Paare, 56 gefangen, 168 durchgelassen; Feld F₅ und Fehler (1, −1): 5 Durchlässe von 25 | Prüfung der Umsetzung der probabilistischen Modelle |
| M15 | Gewinner-Zertifikat auf synthetischen strukturierten Matrizen | Geclusterte Zeilen, vorgegebener Abstand der Logits, Gleichstände, gemeinsamer Maßstab | Einsparung bei verschiedenen Verteilungen; auf echten Gewichten — nach O1 |
| M16 | Intervallzertifikat auf fixierten Präfixen | Anteil mehrdeutiger Ausgänge `u`, Zahl der vollständigen Neuberechnungen, Preis der Vorbereitung je Zahl der Anfragen | Ob die Beschleunigung in 5% passt (nachdem die Gewichte verfügbar sind) |
| M17 | Gauß–Newton-Schritt auf einem kleinen Block | Explizite rationale Matrix `J`, Identität `⟨Jx, z⟩ = ⟨x, Jᵀz⟩`, Längen der ganzen Zahlen, Zahl der Verfeinerungen, Gleichstände | Der Preis des neuen Vertrags |
| M18 | Berechnung der Auszahlungen und Wiederherstellung | Endliche Aufzählung: eine Aufgabennummer, zwei Eltern, Gabelung, Verlust der Eingabe, Absprache aller Zugewiesenen, leeres Konto | Höchstens eine Auszahlung je Ergebnis; nichts wird vor der Annahme angewandt |

---

## 6. Entscheidungen, die diese Phase verlangt

Der Rat trifft keine Entscheidungen. Unten stehen die Fragen mit der Empfehlung des Rats. Der Eigentümer beauftragte den Betreuer, sie zu entscheiden;
die Entscheidungen D18–D25 wurden am 24. November 2026 angenommen und in [ROADMAP](ROADMAP.md),
Abschnitt 3, festgehalten. Jede Entscheidung ist nach der Frage angegeben.

1. **Soll die Grundlage der Bezahlung des Trainings auf „Bezahlung für eine bewiesene Verbesserung“ geändert werden?** Nach D2
   wird ein prüfbares Ergebnis bezahlt; eine Verbesserung im Examen ist formal eines, aber es ist ein anderer
   Gegenstand als der ausgeführte Schritt. Drei Arbeiten (claude1, claude2, ds1) halten es für den Hauptkandidaten,
   drei (gpt1, gpt2, ds2) für einen anderen Vertrag, nicht für eine Prüfung des Schritts. *Empfehlung des Rats:* erlauben,
   diesen Weg als Kandidaten für eine neue Vergütungseinheit des Trainings zu untersuchen, ohne ihn Prüfung des Schritts zu nennen.
   Endgültig entscheiden nach den Berechnungen M7, M8, M10–M12 und dem Experiment O6. Bedingungen: externer Beacon nach
   der Fixierung, kryptografisch kleines `ε`, Verluste ohne Abschneiden, Beweis des Examens, Attributionsregel
   ohne Gewinn durch Duplikate. Nach D6 festhalten, dass die Verbesserung die Abwesenheit von Schaden nicht beweist.
   **Entschieden — D18:** Der Weg wird als Kandidat für eine neue Vergütungseinheit des Trainings untersucht, ist aber nicht angenommen und wird nicht
   Prüfung des Schritts genannt. Die Entscheidung über die Annahme — nach M7, M8, M10–M12 und dem Experiment O6 (es liegt außerhalb von D5
   und verlangt die Genehmigung des Eigentümers). Das Modell
   wird nur nach der Regel D9 ausgegeben. Die Suche nach einer Prüfung des Schritts selbst (T3) geht weiter.
2. **Ist ein kleiner kryptografischer Fehler zulässig?** Die Anforderungen nennen ihn eine Annahme. Die Arbeiten
   claude1, claude2, ds2 und die Kritiker Claude und DeepSeek halten den Fehler `2⁻⁴⁰…2⁻¹²⁸` für vereinbar
   mit D1 als Erwartungswert, wenn die Zufälligkeit extern und unvorhersehbar ist und jeder Versuch mehr
   als `ε·R` kostet. Die Arbeiten gpt1, gpt2 und der Kritiker ChatGPT: Ein kleiner Fehler allein genügt für D1 nicht, nötig ist
   eine bewiesene untere Schranke des Preises des billigsten Versuchs. ds1 hält genau null für nötig.
   *Empfehlung des Rats:* den kleinen Fehler als ausdrücklich genannte Annahme unter drei Bedingungen annehmen —
   externer Beacon streng nach der endgültigen Annahme des Blocks, Verbot von Fiat–Shamir für die Stichprobe,
   festgeschriebene untere Schranke des Preises eines Versuchs. Ohne diese Entscheidung sind weder die Bezahlung für die Verbesserung
   noch kurze Beweise möglich.
   **Entschieden — D19:** Ein kleiner Fehler ist als ausdrückliche Annahme unter diesen drei Bedingungen zulässig,
   nicht mehr als `2⁻⁸⁰` je Versuch und mit `ε·R` kleiner als die festgeschriebene untere Schranke des Preises eines Versuchs. Eine gewöhnliche
   Stichprobenprüfung mit einem Fehler `q^k` wird dadurch nicht erlaubt.
3. **Welcher externe Beacon und wessen Vertrauen ist zulässig?** Ohne eine externe Quelle gemeinsamer Zufälligkeit funktioniert bei
   `q = 1` kein Schema mit Stichprobe nach der Fixierung (Schranke 2.1, Nr. 7). Die Quellen sind noch
   nicht gewählt (Angriff 1.5 und N13). *Empfehlung des Rats:* mehrere unabhängige Quellen wählen
   und das Vertrauen in sie als Annahme festhalten.
   **Entschieden — D20:** nicht weniger als zwei unabhängige öffentliche Quellen, der Wert wird zu einem im Voraus
   bestimmten Zeitpunkt nach der endgültigen Fixierung genommen, ohne Recht auf Auslassung. Die konkreten Quellen
   und der Preis des Einflusses auf sie — in Phase 2. Bis zur Wahl eines Schemas mit Stichprobe werden sie nicht einbezogen.
4. **Soll angenommen werden, dass es für die Modellantwort eine von der Absprache unabhängige Prüfung nur beim Zahler gibt,
   der selbst prüft?** *Empfehlung des Rats:* ja. Für den Verbraucher ohne Ausrüstung wird die Antwort
   mit der Markierung „nicht geprüft“ ausgegeben (das lässt D6 zu), und die Delegierung der Prüfung ist seine eigene
   Annahme. Gesondert zu entscheiden, wie der Ausführende für eine solche Antwort ohne Verletzung von D1 bezahlt wird: Es gibt keine Lösung.
   **Entschieden — D21:** ja. Eine Antwort ohne Prüfung bezahlt das Netz nicht. Ein Nutzer ohne Ausrüstung kann
   selbst einen Prüfer bestimmen; das ist seine eigene Annahme, und D1 verspricht das Netz für ihn nicht.
   Die Garantie D1 für einen solchen Nutzer bleibt eine offene Frage.
5. **Sollen Produktänderungen zugunsten einer billigen exakten Prüfung erlaubt werden?** Dazu gehören die kanonische
   Token-Auswahl über Gumbel-max (ändert die Verteilung im Vergleich zur gewöhnlichen Top-p-/Top-k-Stichprobe),
   das exakte Ganzzahlprofil (kann die Qualität verschlechtern), Aufgaben mit prüfbarem Ausgang (Formeln,
   Tests) und neue Optimierer mit exaktem Zertifikat (Gauß–Newton, Ridge-Regression).
   *Empfehlung des Rats:* als gesonderte Typen von Planaufgaben mit ausdrücklichem Vertrag erlauben, nach
   den Experimenten O5 und der Berechnung M17.
   **Entschieden — D22:** als gesonderte Typen von Planaufgaben mit ausdrücklichem Vertrag erlauben, nach O5 und M17.
   Die gewöhnliche Stichprobe bleibt mit der Markierung „nicht geprüft“ verfügbar.
6. **Wie lassen sich falsche Streitfälle des Zahlers ohne Pfänder begrenzen?** D8 begrenzt die Streitfälle durch die Zahl
   der Anfragen, aber eine Koalition, die Anfragen an sich selbst bezahlt, umgeht diese Grenze. *Empfehlung
   des Rats:* den Preis eines falschen Streitfalls (M9) vor der Entscheidung berechnen; der Rat fand keine Regel, die kein
   Pfand verlangt.
   **Entschieden — D23:** zuerst die Berechnung M9. PPS wird nicht einbezogen, solange für es keine Regel
   zur Begrenzung falscher Streitfälle ohne Pfand gewählt ist.
7. **Soll der Chiffretext der Antwort im Journal gespeichert werden?** Ohne das kann der Ausführende die Antwort zurückhalten.
   *Empfehlung des Rats:* ja, etwa 2–4 KB je Antwort; das stimmt mit D10 überein.
   **Entschieden — D24:** ja, der Chiffretext wird mit einer einzigen Aufzeichnung zusammen mit der Annahme ins Journal geschrieben.
8. **Wird die zweiseitige Schreibweise von D1 auch für eine teilweise Fälschung benötigt?** Die Arbeit claude2 fragte,
   ob eine Fälschung zulässig ist, die schlechter als ehrliche Arbeit, aber besser als Untätigkeit ist. Die formale Schreibweise
   von D1 in [THREAT_MODEL](THREAT_MODEL.md), Abschnitt 1.5, verlangt bereits beide Ungleichungen. *Empfehlung
   des Rats:* nicht ändern; daher sind VYa-S und PVYa in der relativen Variante verworfen.
   **Entschieden — D25:** nicht ändern.

---

## 7. Wer was getan hat

Der Modellrat arbeitete nach den Materialien des Projekts, ohne Zugang zum Netz und ohne Experimente.

- **Runde 1, sechs unabhängige Arbeiten:** zwei Arbeiten ChatGPT (gpt1, gpt2), zwei Arbeiten DeepSeek
  (ds1, ds2), zwei Arbeiten Claude (claude1, claude2). Jede analysierte die Richtungen von Phase 4
  aus der Roadmap, schlug eigene Mechanismen vor und berechnete ihren Preis. Kurze Arithmetikprogramme
  führten claude1, claude2, gpt1 und gpt2 aus; gpt1 und gpt2 legten kleine Aufzählungen
  mit Kontrollhashes bei.
- **Runde 2, drei Kritiken:** je eine von ChatGPT, DeepSeek und Claude. Jeder Kritiker las alle sechs
  Arbeiten, suchte Gegenbeispiele und rechnete die Schlüsselzahlen nach. Die Kritiker ChatGPT und DeepSeek wiederholten die kleinen
  Aufzählungen von gpt1 und gpt2 auf dem Prozessor; die Hashes stimmten überein.
- **Zusammenführung:** Dieses Dokument stellte Claude nach den Arbeiten und Kritiken zusammen. Wo die Kritiker sich widersprachen, steht
  „strittig“. Bei der Zusammenführung wurden auf die Schlussfolgerungen die Entscheidungen D6–D17 angewandt, die den Teilnehmern nicht vorlagen; neue
  Einschätzungen und Zahlen über die Arbeiten und Kritiken hinaus wurden nicht hinzugefügt.
