# Wie man mitarbeitet

[English](../../CONTRIBUTING.md) · [中文](../zh/CONTRIBUTING.md) · [Español](../es/CONTRIBUTING.md) · [Français](../fr/CONTRIBUTING.md) · **Deutsch** · [Italiano](../it/CONTRIBUTING.md) · [Русский](../ru/CONTRIBUTING.md) · [Português](../pt/CONTRIBUTING.md) · [العربية](../ar/CONTRIBUTING.md)

Danke, dass Sie helfen möchten. Hier zählt Genauigkeit, nicht Umfang: Eine gefundene Lücke mit einem konkreten Szenario ist mehr wert als zehn Seiten allgemeiner Überlegungen.

## Was Sie beitragen können

- **Einen Angriff auf den aktuellen Entwurf.** Ein Szenario: Wer handelt, was tut er, was gewinnt er, warum bemerkt das Netz es nicht. Nennen Sie den Abschnitt in [CURRENT_DESIGN](../../docs/CURRENT_DESIGN.md).
- **Eine Lösung für eine [offene Frage](../../docs/OPEN_QUESTIONS.en.md).**
- **Eine Quelle**: eine Arbeit, ein Protokoll oder Projekt, das einen Teil eines Problems löst, mit Version, Datum und dem, was es für unseren Fall **nicht** beweist.
- **Eine Kostenberechnung** oder eine Korrektur einer bestehenden.
- **Eine Übersetzungskorrektur**: eine Ungenauigkeit in einer Übersetzung der Grundlage (über die Errata-Datei).
- **Eine Aufgabe für den Forschungsagenten**: eine Berechnung, die einen Teil einer offenen Frage beantwortet (siehe [tasks/README.md](../../tasks/README.md)).
- **Rechenleistung**: Wenn Sie weder einen KI-Assistenten noch Zeit zum Schreiben haben, lassen Sie den [Forschungsagenten](AGENT.md) auf Ihrem Computer oder Telefon laufen.

## Wie Sie es einreichen

Eröffnen Sie ein Issue und beginnen Sie den Titel mit einer Markierung:

| Markierung | Wofür |
|---|---|
| `[Attack]` | Ein Weg, das Netz zu betrügen oder zu stören |
| `[Q<N>]` | Ein Vorschlag zur offenen Frage N |
| `[Source]` | Eine nützliche Arbeit oder ein Projekt |
| `[Cost]` | Eine Kostenschätzung oder Korrektur von Zahlen |
| `[Translation]` | Eine Übersetzungsungenauigkeit |
| `[Task]` | Eine Berechnung für den Forschungsagenten |

Geben Sie im Text an:

1. Was garantiert wird und unter welchen Annahmen.
2. Den Mechanismus.
3. Bekannte Angriffe und was bleibt.
4. Die Kosten, markiert als [Berechnung] oder [gemessen].
5. Welche der sechs [Anforderungen](REQUIREMENTS.md) erfüllt sind und welche nicht.

Pull Requests zu den Arbeitsdokumenten (`docs/`) sind willkommen. Wenn Sie den Status eines Punktes ändern, erklären Sie warum. Issues und Pull Requests dürfen in jeder Sprache des Repositorys verfasst sein.

## Regeln

- **Die Grundlage ändert sich nicht.** Ein Pull Request, der das Manifest, die Anforderungen, das README oder ihre Fingerabdrücke ändert, wird nicht angenommen. Siehe [CORE.md](../../CORE.md).
- Eine Berechnung wird nicht als Messung ausgegeben, ein Vorschlag nicht als Entscheidung.
- Veröffentlichen Sie keine Schlüssel, Passwörter, persönlichen Daten oder Computeradressen.
- Bleiben Sie höflich und sachlich. Kritisieren Sie Ideen, nicht Menschen.

Wenn Sie mit einem KI-Assistenten arbeiten, geben Sie ihm [AGENTS.md](AGENTS.md). Für die Richtigkeit eines Issues ist sein Autor verantwortlich.
