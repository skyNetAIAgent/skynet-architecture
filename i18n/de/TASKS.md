<!-- translation of tasks/README.md, source sha256: f0685cfe87baef739cff7ff9121f8ab2fd0aed86866b5638fd79dcdd347c1916 -->

# Aufgaben für Forschungsagenten

[English](../../tasks/README.md) · [中文](../zh/TASKS.md) · [Español](../es/TASKS.md) · [Français](../fr/TASKS.md) · **Deutsch** · [Italiano](../it/TASKS.md) · [Русский](../ru/TASKS.md) · [Português](../pt/TASKS.md) · [العربية](../ar/TASKS.md)

Dieser Ordner enthält die Arbeit, die [Forschungsagenten](../../agent/README.md) übernehmen:

- [`index.json`](../../tasks/index.json): die aktuelle Aufgabenliste;
- `index.json.sig`: ihre Signatur (Agenten ignorieren eine Liste ohne gültige Signatur);
- [`context/`](../../tasks/context): eingefrorene Texte, die KI-Fragen zitieren.

Ergebnisse erscheinen als Kommentare im Tracking-Issue jeder Aufgabe und werden von
`tools/collect_results.py` in [`results/`](../../results) zusammengefasst.

## Was eine Aufgabe ist

Eine Aufgabe ist Daten: der Name einer in den Agenten eingebauten Berechnung (ein „Kernel"), ihre
Parameter und die Zahl der unabhängigen Stücke („Units"), in die die Arbeit aufgeteilt ist. Eine
Aufgabe kann keinen Code enthalten. Eine neue Art von Berechnung braucht eine neue signierte
Version des Agenten.

```json
{"id": "exit-a-honest-check", "kernel": "exit-scam-a", "kernel_version": 1,
 "units": 256, "redundancy": 2, "issue": 12,
 "params": {"H0": 1200, "q": [0, 1], "cap_third": false, "batches": 2, "n_max": 200,
            "sizes": {"mode": "grid", "points": 48}}}
```

Es gibt keinen Scheduler. Jeder Agent wählt ein zufälliges Stück, das er noch nicht erledigt hat.
Dass mehrere Agenten auf demselben Stück landen, ist gewollt: Alle Rechen-Kernel sind exakte
Ganzzahl-Arithmetik, gleiche Arbeit ergibt also auf jedem Gerät dieselben Ziffern, und ein Stück
gilt als bestätigt, wenn `redundancy` verschiedene GitHub-Konten denselben Hash veröffentlichen.
Unterschiedliche Hashes für ein Stück sind ein Konflikt, den ein Betreuer durch Nachrechnen beilegt.

## Kernel in Agent 0.1

| Kernel | Was er berechnet | Quelle |
|---|---|---|
| `selftest@1` | Eine feste Ganzzahl-Arbeitslast; jedes Gerät muss denselben Digest zurückgeben | [selftest.py](../../agent/skynet_agent/kernels/selftest.py) |
| `exit-scam-a@1` | Exakte erwartete Auszahlung eines Teilnehmers, der gefälschte Ergebnisse einreicht und geht, über eine Familie von Strategien; meldet Strategien, die ehrliches Verlassen übertreffen | [exit_scam_a.py](../../agent/skynet_agent/kernels/exit_scam_a.py) |
| `lottery-b@1` | Exakte Wahrscheinlichkeit eines Verlustmonats oder -quartals, wenn nur geprüfte Aufgaben bezahlt werden | [lottery_b.py](../../agent/skynet_agent/kernels/lottery_b.py) |
| `ai-answer@1` | Optional: eine Frage für ein lokales KI-Modell, das der Teilnehmer betreibt | [ai_answer.py](../../agent/skynet_agent/kernels/ai_answer.py) |

Jede Quelldatei beginnt mit dem genauen Modell, das sie umsetzt, sodass jeder ein Ergebnis
unabhängig nachrechnen kann.

## Die jetzt veröffentlichten Aufgaben und warum

Alle betreffen die zentrale offene Frage des Projekts: Kann Betrug billig wirkungslos gemacht
werden ([OPEN_QUESTIONS, Q1](../../docs/OPEN_QUESTIONS.en.md)).

| Aufgabe | Frage |
|---|---|
| `selftest-1` | Funktioniert die Pipeline auf Ihrem Gerät? |
| `exit-a-honest-check` | Gibt es ohne Absprache irgendeine Möglichkeit, vor dem Verlassen von Fälschungen zu profitieren? Der Entwurf sagt nein |
| `exit-a-uniform-h399`, `exit-a-uniform-h1200` | Bei gleichen kleinen Aufgaben: Ab welchem Anteil abgesprochener Prüfer lohnt sich das Verlassen mit Fälschungen? Die Schätzung des Entwurfs liegt bei etwa 91% |
| `exit-a-uniform-cap-h399` | Dasselbe mit der vorgeschlagenen Begrenzung „höchstens ein Drittel des ausstehenden Betrags an Arbeit", in drei Wellen |
| `exit-a-sizes-cap`, `exit-a-sizes-nocap` | Dasselbe, wenn Aufgaben jede Größe haben dürfen, mit und ohne diese Begrenzung |
| `lottery-b-table` | Wenn nur geprüfte Aufgaben bezahlt werden, wie oft hat ein kleiner Teilnehmer einen Verlustmonat? |
| `ask-variant-b-attack` | Für lokale KI-Modelle: Finden Sie einen neuen Angriff auf „das Netz zahlt nur für geprüfte Arbeit" |

Das sind Berechnungen zu den Regeln, so wie sie in den Entwurfsdokumenten stehen. Sie sind keine
Messungen der Hardware und keine Experimente mit dem Netz. Messaufgaben (zum Beispiel, ob
Ganzzahl-Inferenz auf verschiedenen Grafikkarten dieselben Bits ergibt) werden erst veröffentlicht,
nachdem die Betreuer des Projekts Experimente freigeben.

## Eine Aufgabe vorschlagen

Eröffnen Sie ein Issue mit dem Titel `[Task] …` und geben Sie an:

1. die Frage, die die Berechnung beantwortet, und zu welcher offenen Frage sie gehört;
2. das genaue Modell, damit es unabhängig nachgerechnet werden kann;
3. welcher Kernel und welche Parameter es erledigen würden oder was ein neuer Kernel berechnen muss;
4. woran ein falsches oder gefälschtes Ergebnis erkannt würde.

Die Betreuer prüfen die Aufgabe mit `tools/sign_tasks.py --check`, fügen sie in `index.json` ein und
signieren die Liste. Signieren kann nur der Inhaber des Release-Schlüssels; siehe
[docs/RESEARCH_AGENT.md](RESEARCH_AGENT.md).
