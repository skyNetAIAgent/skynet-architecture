<!-- translation of docs/EXPERIMENT_D5.md, source sha256: 3aaab08790ed9745e86dcaed1c7bbebd15df48ba863df50aac4f965c117afbe1 -->

# Experiment D5: ganzzahliges Qwen3.5-4B

[English](../../docs/EXPERIMENT_D5.en.md) · [中文](../zh/EXPERIMENT_D5.md) · [Español](../es/EXPERIMENT_D5.md) · [Français](../fr/EXPERIMENT_D5.md) · **Deutsch** · [Italiano](../it/EXPERIMENT_D5.md) · [Русский](../../docs/EXPERIMENT_D5.md) · [Português](../pt/EXPERIMENT_D5.md) · [العربية](../ar/EXPERIMENT_D5.md)

Stand vom 25. November 2026: **erste Ergebnisse bei kurzen Eingaben (Abschnitt 7); langer Kontext,
Geschwindigkeit und Qualität sind noch nicht gemessen.** Das Experiment ist durch die Entscheidung D5
([ROADMAP](ROADMAP.md), Abschnitt 3) erlaubt und gehört zu Phase 5 der Roadmap. Es prüft die wichtigste ungemessene
Annahme des besten Kandidaten aus Phase 4 — der Prüfung der Antwort durch den Zahler selbst (PPS,
[VERIFICATION_SEARCH](VERIFICATION_SEARCH.md), Abschnitte 3.2 und 5.2).

## 1. Was geprüft wird

Ein Zahler, der über das Modell verfügt, muss die Anfrage und die erhaltene Antwort in einem einzigen Durchlauf nachrechnen
und **genau dieselben Bits** erhalten wie der Ausführende bei der Generierung. Das ist nur möglich, wenn die gesamte
Arithmetik des Modells durch ganze Zahlen mit festgeschriebener Rundung festgelegt ist: Die Summe ganzer Zahlen hängt nicht
von der Reihenfolge der Addition ab, solange es keinen Überlauf gibt. Das Experiment beantwortet fünf Fragen; die Widerlegungskriterien
werden vor dem Start festgeschrieben:

| Experiment | Frage | Was es widerlegt |
|---|---|---|
| O1 | Stimmen die Bits auf verschiedenen Grafikkarten und auf dem Prozessor überein | Mindestens ein unterschiedliches Bit der Logits, des gewählten Tokens, des Abbruchgrunds oder der Kontrollhashes bei gleicher Eingabe. Vor der Schlussfolgerung — Suche nach der ersten Abweichung und Wiederholung mit der kürzesten Eingabe. Die Schlussfolgerung bezieht sich nur auf die getesteten Geräte und die Version der Implementierung |
| O2 | Stimmen die Bits bei der Generierung Token für Token und bei einem einzigen Durchlauf über die fertige Sequenz auf einer Karte überein | Jedes unterschiedliche Bit, einschließlich des Hashes des rekurrenten Zustands der Gated-DeltaNet-Schichten an den Kontrollpunkten |
| O3 | Wie viel die Prüfung einer Antwort im Vergleich zu ihrer Generierung kostet | Der Median des Anteils `ρ(1)` ist größer als 5% für mindestens eines der vier vorab genannten Paare von Längen der Anfrage und der Antwort bei Batch 1. Die Batches 8 und 32 werden gesondert gemessen |
| O4 | Um wie viel langsamer das Ganzzahlprofil als das gewöhnliche 8-Bit-Profil auf derselben Karte ist | Der Median der Verlangsamung ist in einer vergleichbaren Zelle größer als das 1,25-Fache (der Schwellenwert ist diagnostisch: entscheidend sind O3 und O5) |
| O5 | Wie viel Qualität verloren geht | Der Genauigkeitsverlust beträgt mehr als 3 Prozentpunkte bei 320 vorab ausgewählten Aufgaben (je 64 aus vier Abschnitten von MMLU und aus dem russischen MGSM) im Vergleich zum gewöhnlichen 8-Bit-Profil desselben Modells |

Die berechneten 1,2–3,8% aus Phase 4 gelten nicht als Ergebnis von O3: Sie werden nur durch dieses Experiment bestätigt oder widerlegt.

## 2. Modell und Ausrüstung

- **Modell:** das offizielle Repository Qwen/Qwen3.5-4B auf Hugging Face, festgeschriebene Revision
  `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`. Zwei Gewichtsdateien mit 5 329 398 688 bzw. 3 990 429 408
  Byte, insgesamt etwa 9,3 GB. Nach dem Herunterladen werden die SHA-256 aus der Dateiliste des Repositorys abgeglichen.
- **Architektur** (nach der veröffentlichten `config.json`): 32 Blöcke, verborgener Vektor 2560, MLP 9216.
  Jeder vierte Block (Indizes 3, 7, …, 31) — volle Attention: 16 Abfrage-Köpfe, 4 Köpfe
  für Schlüssel und Werte, Kopfgröße 256, Ausgangs-Gate, Rotation der ersten 64 Koordinaten. Die übrigen
  24 Blöcke — Gated DeltaNet: rekurrenter Zustand 32 × 128 × 128 je Block, kausale Faltung
  der Tiefe 4. Vokabular 248 320, Eingangs- und Ausgangsmatrix gemeinsam. Der gewöhnliche Transformer-
  „INT-Kanon“ aus Phase 4 reicht für sie nicht aus; das Profil wird neu festgelegt (Abschnitt 3).
- **Geräte:** RTX 2060 6 GB (Turing) auf dem Heim-Linux des Betreuers; RTX 4070 Laptop
  8 GB (Ada) auf dem Computer des Eigentümers; der Prozessor als dritter unabhängiger Ausführender. Mit Zustimmung —
  Geräte anderer Teilnehmer über einen Mini-Agenten.
- **Speicher** [Berechnung]: die wesentlichen 8-Bit-Gewichte — 4010 MiB. Bei Batch 1 und einer Länge bis 3000 Token
  passt alles in 6 GB; Batch 32 erfordert bei einer Länge von 3000 etwa 7064 MiB noch vor den Arbeitspuffern
  und ist auf der RTX 2060 nur mit Auslagerung der Historie in den Arbeitsspeicher möglich.

## 3. Ganzzahlprofil

Das Profil erhält einen eigenen Namen und eine eigene Version und wird bis O1–O5 eingefroren. Die Grundlage ist der numerische Graph
aus dem Projekt ChatGPT mit den Korrekturen beider Kritiker:

1. **Gewichte und Aktivierungen.** Die Gewichte sind 8 Bit zeilenweise, der Zeilenmaßstab ist eine exakte Binärzahl.
   Die Aktivierungen sind 16 Bit mit Festkomma (1024 = Einheit). Für alle Operationen gilt eine einzige
   Rundung: zum Nächsten, bei der Hälfte zur geraden Zahl, im Betrag mit Rückgabe des Vorzeichens.
2. **Normierungen und Nichtlinearitäten** (RMSNorm, L2, SiLU, Sigmoid, Softplus, Exponentialfunktion) — ganzzahlige
   Formeln mit ganzzahliger Quadratwurzel und Tabellen. Die Tabellen werden außerhalb des Programms mit bewiesen
   korrekter Rundung (MPFR) erzeugt und mit SHA-256 veröffentlicht.
3. **Volle Attention.** Bewertungen, Exponentialfunktion nach Tabelle, Anteile in 16 Bit. Der Kritiker ChatGPT fand
   im Ausgangsprojekt einen Fehler: Bei gleichen Werten änderte das Hinzufügen eines weiteren gleichen Schlüssels
   den Ausgang von 1365 auf 683. Die Korrektur: die gewichtete Summe durch die Summe der gerundeten
   Anteile selbst zu teilen, dann bleibt ein konstanter Wert exakt erhalten.
4. **Gated DeltaNet.** Dämpfung, Korrektur und Aktualisierung des Zustands — fünf ganzzahlige Zuweisungen
   für jedes Token in einer kanonischen zeitlichen Reihenfolge. Die Formel aus dem Projekt DeepSeek
   beschrieb eine andere Rekurrenz und wurde verworfen. Die beschleunigte „Blockform“ ist nur zulässig,
   wenn sie bei jedem Token dieselben Bits reproduziert.
5. **Token-Auswahl.** Das Maximum über das Paar (Bewertung, −Nummer) über das gesamte Vokabular, gierig. Ein gesonderter Modus —
   kanonisches Gumbel-max mit Pseudozufälligkeit HMAC-SHA256 aus dem Seed der Anfrage (D22).
   Der Abbruch — der erste Grund: EOS oder das Limit.
6. **Überlaufgrenzen** sind für jeden Akkumulator festgelegt; wo 32 Bit nicht ausreichen, werden 64 verwendet.
   Gesonderte Tests prüfen die Extremwerte.

Alle mehrdeutigen Stellen („Verzweigungen“) werden vor dem ersten Lauf durch Lesen des Modellquelltexts der
festgeschriebenen Version von Transformers geschlossen; der Hash dieses Quelltexts gehört zum Manifest des Profils.

## 4. Ablauf der Arbeiten

1. **P0, Vorbereitung (2–4 Tage).** Herunterladen und Abgleich des Modells; ein Verzeichnis aller Tensoren; das Schließen
   der Verzweigungen anhand des Quelltexts; Tabellen; Kontrollvektoren mit von Hand berechneten Werten.
2. **Verkürzter Schritt (1–1,5 Wochen).** Eine Referenz auf dem Prozessor für das gesamte Modell bei kurzen Eingaben;
   Abgleich mit der gewöhnlichen Gleitkommaberechnung (nur um einen Importfehler zu finden,
   nicht für O1/O2). Eine einfache Version für die Grafikkarte ohne Tensor-Kerne. Antworten auf O2 auf einer Karte
   und auf O1 „Prozessor gegen RTX 2060“ bei kurzem Kontext. Dann derselbe Batch auf der RTX 4070
   Laptop — die erste Antwort auf O1 für zwei verschiedene Grafikkarten.
3. **Vollständiger Schritt (3–4 Wochen).** Schnelle 8-Bit-Multiplikationen, ein fusionierter Kernel der DeltaNet-Rekurrenz,
   die Batches 1/8/32, die Experimente O3, O4, O5, Wiederholung auf einem zweiten Gerät.

Die gesamte Arbeit läuft in einem gesonderten Verzeichnis auf dem Heim-Linux, mit einer eigenen Python-Umgebung
(CuPy mit CUDA-12-Bibliotheken aus pip-Paketen, ohne Systeminstallation). Laufende Dienste
und Verzeichnisse anderer Experimente werden nicht berührt. Die Gesamtschätzung — 4–6 Wochen Arbeit eines
Entwicklers; die Hauptrisiken — der Preis der DeltaNet-Rekurrenz (ihn zeigt O3), Mehrdeutigkeiten
bis P0 und die Unterstützung von Qwen3.5 in gewöhnlichen Engines für O4/O5.

## 5. Was veröffentlicht wird

Für jeden Lauf: das Manifest des Profils und der Versionen, die Eingaben, die Hashes der Logits und der Zustände je Schicht,
die Rohzeiten und die Messbedingungen, die ursprünglichen Fehler zusammen mit den Korrekturen. Die Übereinstimmung der Bits
bezieht sich nur auf die getesteten Geräte und Versionen. Das Ergebnis jedes Experiments wird in die Roadmap
(Phase 5) und in dieses Dokument eingetragen; das Experiment gilt als abgeschlossen, wenn ein zweiter Teilnehmer es wiederholt hat.

## 6. Wer was getan hat

- **Projekte des Experiments:** zwei unabhängige Projekte — ChatGPT und DeepSeek.
- **Gegenseitige Kritik:** ChatGPT analysierte beide Projekte, DeepSeek analysierte beide Projekte;
  Nachrechnungen des Speichers und der Grenzen, Prüfung der kurzen Rekurrenz und der Attention-Korrektur an kleinen Aufzählungen.
- **Zusammenführung und Entscheidungen zum Plan:** Claude.
- **Vorbereitung, Profile v1 und v2, Referenz auf dem Prozessor und Version für die Grafikkarte:** ChatGPT.
- **Unabhängige Prüfungen:** DeepSeek — Import des Modells mit dem offiziellen forward, Eindeutigkeit
  und Überlaufgrenzen des Profils v2.
- **Läufe auf den Grafikkarten und Prüfung der Ergebnisse:** Claude (aus der Sandbox der Modelle ist die Grafikkarte
  nicht erreichbar).

## 7. Ergebnisse

**24. November 2026, kurze Eingaben.** Eingaben: zwei Verläufe mit je 8 + 8 Token und sechs kurze
Texte (Russisch, Englisch, Chinesisch, Arithmetik, Code, Rezept), Tiefe 4 und 32 Blöcke; Batch 1.

- **Import des Modells.** Die gewöhnliche Gleitkommaberechnung, geschrieben nach dem Quelltext, stimmte
  mit dem offiziellen forward von Transformers 5.24.0 überein: dasselbe gewählte Token an 130 von 130 Positionen,
  Abweichung der Logits nicht größer als 3,6·10⁻⁵ (geprüft von ChatGPT und unabhängig von DeepSeek).
- **Profil v1 abgelehnt.** Es war bitgenau reproduzierbar, aber die Skala 1/1024 war zu grob:
  der Ausgang der DeltaNet-Rekurrenz wurde fast vollständig auf null gerundet, Übereinstimmung des gewählten Tokens
  mit dem Modell — 5 von 8, Korrelation der Logits etwa 0,8.
- **Profil v2** (Aktivierungen mit einem binären Exponenten pro Vektor und einer 16-Bit-Mantisse, Rest
  und Rekurrenzzustand mit Schritt 2⁻²⁰, Schlüssel und Werte der Attention in 32 Bit): dasselbe Token wie
  beim offiziellen Modell an 90 von 90 Positionen, mittlere Korrelation der Logits 0,9996, minimale
  0,998. Zustand und Cache belegen 238 MiB bei 3000 Positionen gegenüber 95 bei v1; die Zahl der Multiplikationen
  pro Token ist dieselbe — 4,2 Mrd.
- **O2 (ein Gerät).** Die Generierung Token für Token und ein Durchlauf über die fertige Antwort mit Aufteilung
  in 1, 3 und 8 Positionen ergeben dieselben Bits aller Logits, der gewählten Token und der Zustands-Hashes.
- **O1 (verschiedene Geräte).** Prozessor (Xeon, Linux), RTX 2060 (Turing, Linux, CuPy) und RTX 4070
  Laptop (Ada, Windows, CuPy): 88 Vergleiche auf jeder Karte, je 242 360 320 Logits,
  976 gewählte Token und 37 152 Zustands-Hashes — **kein einziger Unterschied**.

**25. November 2026, eine andere Architektur und eine andere Sprache der Kerne.** Eine dritte
Implementierung auf OpenCL (ChatGPT), dieselben Eingaben und 88 Vergleiche: der Prozessor über pocl,
die RTX 2060 über NVIDIA OpenCL und **AMD Radeon RX 580** (Polaris, Mesa rusticl, Linux) — wieder
kein einziger Unterschied in einem der 242 360 320 Logits, 976 Token und 37 152 Hashes. Insgesamt
dieselben Bits auf sechs Ausführenden: Prozessor (NumPy), Prozessor (pocl), RTX 2060 (CUDA und
OpenCL), RTX 4070 Laptop (CUDA), RX 580 (OpenCL).

**25. November 2026, langer Kontext.** Anfrage + Antwort: 512 + 64, 2048 + 256 und 4096 + 64 Token
(echte Texte), alle 32 Blöcke; verglichen wurden die Hashes der Logits jeder Position, die gewählten Token
und die Zustands-Hashes alle 64 Positionen. RTX 2060 (CUDA), RTX 2060 (OpenCL) und RTX 4070 Laptop
(CUDA) stimmten in allen drei Fällen untereinander überein, und auf jeder Karte stimmte die Generierung
Token für Token mit dem Durchlauf über die fertige Antwort in Stücken von 64 und 512 Positionen überein.
Für 512 + 64 lieferten die unabhängige Referenz auf dem Prozessor und die RX 580 dasselbe. Auf der RX 580
stimmte die Generierung Token für Token auch für 2048 + 256 und 4096 + 64 mit den übrigen Karten überein,
doch der Durchlauf über die fertige Antwort wird bei langen Eingaben vom Treiber abgebrochen (Zurücksetzen
einer zu langen Aufgabe der Grafikkarte); der Attention-Kernel muss in Teile zerlegt werden.
Das ist eine Einschränkung der Ausführung, kein Unterschied in den Bits.

Einschränkungen: kurze Eingaben und Batch 1; einfache ganzzahlige Kerne ohne Tensor-Kerne; die Zeit
dieser Läufe ist keine Messung von O3 und O4. Weiter — langer Kontext bis zu Tausenden Token,
schnelle Kerne mit derselben Arithmetik, danach O3–O5.
