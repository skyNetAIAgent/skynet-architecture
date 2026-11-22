<!-- translation of results/FIRST_RUN.md, source sha256: 786aa2e462922d0a3a2ec06d0da0e26d246a2563867e215a11cfbf5a799bfe0a -->

# Erster Lauf der ersten Aufgabenliste (ein Computer, noch nicht bestätigt)

[English](../../results/FIRST_RUN.md) · [中文](../zh/FIRST_RUN.md) · [Español](../es/FIRST_RUN.md) · [Français](../fr/FIRST_RUN.md) · **Deutsch** · [Italiano](../it/FIRST_RUN.md) · [Русский](../ru/FIRST_RUN.md) · [Português](../pt/FIRST_RUN.md) · [العربية](../ar/FIRST_RUN.md)

Am 22. November 2026 wurde jedes Stück der Aufgabenliste Nummer 1 einmal auf einem einzelnen Windows-Computer mit demselben Code berechnet, den die Agenten ausführen: 702 Stück, 15,5 CPU-Stunden, keine Ausfälle. Ein Computer ist keine Bestätigung. Die Zahlen unten werden erst dann zu Ergebnissen des Projekts, wenn andere Teilnehmer dieselben Hashes veröffentlichen (siehe [README.md](RESULTS.md)).

## Verlassen mit Fälschungen (Kernel `exit-scam-a@1`, Variante A des Entwurfs)

Ein Teilnehmer mit einem Betrag H0 „ausstehend“ reicht in ein paar schnellen Wellen gefälschte Ergebnisse ein und verlässt das Netz. Wenn er einfach ginge, bekäme er H0. Die Tabelle gibt den niedrigsten Anteil abgesprochener Prüfer an, ab dem eine Strategie in der untersuchten Familie eine erwartete Auszahlung über H0 hat. Das genaue Modell steht am Anfang von [exit_scam_a.py](../../agent/skynet_agent/kernels/exit_scam_a.py).

| Aufgabe | Untersuchte Strategien | Profitabel ab Abspracheanteil | Beste erwartete Auszahlung dort |
|---|---:|---|---|
| `exit-a-honest-check`: keine Absprache, beliebige Aufgabengröße, zwei Wellen | 92 169 600 | nie | 0,980 × H0 |
| `exit-a-uniform-h399`: gleiche kleine Aufgaben, 399 ausstehende Preise, eine Welle | 7 600 | 0,892 (nicht bei 0,890) | 1,0066 × H0 |
| `exit-a-uniform-h1200`: gleiche kleine Aufgaben, 1200 ausstehende Preise, eine Welle | 22 800 | 0,908 (nicht bei 0,906) | 1,0117 × H0 |
| `exit-a-uniform-cap-h399`: gleiche kleine Aufgaben, drei Wellen, „höchstens ein Drittel in Arbeit“ | 71 772 196 | 0,890 (nicht bei 0,888) | 1,0059 × H0 |
| `exit-a-sizes-cap`: beliebige Aufgabengröße, drei Wellen, „höchstens ein Drittel in Arbeit“ | 1 190 974 992 | 0,875 (nicht bei 0,870) | 1,00004 × H0; 1 034 × H0 bei 0,880 |
| `exit-a-sizes-nocap`: beliebige Aufgabengröße, zwei Wellen, ohne diese Begrenzung | 69 148 800 | 0,800 (nicht bei 0,780) | 1 218 × H0; 4,91 × H0 bei 0,850 |

Was das nahelegt:

- Die Schätzung des Entwurfs „Betrug ist verlustbringend, solange der Anteil der kolludierenden Prüfer unter etwa 91 % liegt“ stammt aus dem Durchschnitt über eine Fälschung. Sie berücksichtigt nicht, dass ein Teilnehmer höchstens den ausstehenden Betrag verlieren kann (es gibt keine Einlagen oder Strafen). Für jemanden, der geht, ist der Verlust begrenzt, der Gewinn aber nicht, was die Schwelle auf ungefähr 87,5–89% senkt.
- Die vorgeschlagene Regel „höchstens ein Drittel des ausstehenden Betrags gleichzeitig in Arbeit“ ist notwendig. Ohne sie erhöhen die ungeprüften Belohnungen der ersten Welle den ausstehenden Betrag und erlauben größere Aufgaben in der zweiten Welle, und die Schwelle fällt auf etwa 80%.
- Ohne Absprache wurde kein gewinnbringender Weg gefunden, mit Fälschungen abzugehen.

Grenzen: Dies ist eine Berechnung in einem formalen Modell der Regeln, keine Messung; die Suche deckt nur die aufgeführten Familien ab; das Raster der Abspracheanteile hat Schritte von 0,002 bis 0,02.

## Nur für geprüfte Aufgaben bezahlen (Kernel `lottery-b@1`, Variante B des Entwurfs)

Wahrscheinlichkeit, dass das Einkommen einer Periode unter den Kosten der darin geleisteten Arbeit liegt, wenn eine Aufgabe mit Wahrscheinlichkeit 1/P geprüft wird und eine geprüfte Aufgabe mit dem P-Fachen des Aufgabenpreises bezahlt wird. Exakte Binomialsummen.

| Aufgaben pro Monat | Geprüft | Kosten / Preis | Verlustmonate | Verlustquartale |
|---:|---|---:|---:|---:|
| 600 | 1 von 10 | 95% | 32,20% | 22,91% |
| 6 000 | 1 von 100 | 95% | 33,10% | 24,02% |
| 6 000 | 1 von 100 | 80% | 4,84% | |
| 60 000 | 1 von 100 | 95% | 10,47% | 1,55% |
| 200 000 | 1 von 100 | 95% | 1,15% | |
| 200 000 | 1 von 100 | 98% | 18,15% | |
| 600 | 1 von 100 | 95% | 44,49% | |

Bei 600 Aufgaben pro Monat und 1 von 100 geprüften wird in 0,24% der Monate gar nichts bezahlt. Die vollständige Tabelle hat 360 Zellen; sie erscheint in `summary.json`, sobald Agenten sie veröffentlichen.
