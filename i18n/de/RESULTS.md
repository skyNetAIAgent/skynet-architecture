<!-- translation of results/README.md, source sha256: 45df5513ecce206740e2354af46f84e5f3ecf7faccd93a990f4a851df0f249c9 -->

# Ergebnisse der Forschungsagenten

[English](../../results/README.md) · [中文](../zh/RESULTS.md) · [Español](../es/RESULTS.md) · [Français](../fr/RESULTS.md) · **Deutsch** · [Italiano](../it/RESULTS.md) · [Русский](../ru/RESULTS.md) · [Português](../pt/RESULTS.md) · [العربية](../ar/RESULTS.md)

Dieser Ordner wird von `tools/collect_results.py` aus den öffentlichen Ergebniskommentaren der
[Forschungsagenten](../../agent/README.md):

- `REPORT.md`: eine lesbare Zusammenfassung mit bestätigten Erkenntnissen und Konflikten;
- `summary.json`: dasselbe je Aufgabe, für Programme;
- `coverage.json`: wie viele übereinstimmende Ergebnisse jede Einheit jeder Aufgabe hat. Agenten lesen sie, um
  Einheiten zu bevorzugen, zu denen noch Ergebnisse fehlen; sie ist nur ein Hinweis und benötigt keine Signatur;
- `ai/`: Antworten der lokalen KI-Modelle der Teilnehmer, maschinell erzeugt und ungeprüft.

Eine Einheit ist bestätigt, wenn die von der Aufgabe geforderte Anzahl verschiedener GitHub-Konten
denselben Ergebnis-Hash veröffentlicht hat. Jeder gemeldete „Treffer“ der Exit-Scam-Suche wird
vom Sammler exakt neu berechnet, bevor er aufgelistet wird. Was die Aufgaben bedeuten:
[tasks/README.md](TASKS.md).

Bisher wurde noch nichts von Teilnehmern gesammelt. Ein erster Durchlauf der gesamten Aufgabenliste auf einem
Computer, noch von niemand anderem bestätigt, ist in [FIRST_RUN.md](FIRST_RUN.md) beschrieben.
