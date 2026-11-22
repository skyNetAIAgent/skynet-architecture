# Einführung für KI-Assistenten

[English](../../AGENTS.md) · [中文](../zh/AGENTS.md) · [Español](../es/AGENTS.md) · [Français](../fr/AGENTS.md) · **Deutsch** · [Italiano](../it/AGENTS.md) · [Русский](../ru/AGENTS.md) · [Português](../pt/AGENTS.md) · [العربية](../ar/AGENTS.md)

Diese Datei richtet sich an jedes Modell (Claude, ChatGPT/Codex, DeepSeek, Gemini und andere), das von einem Menschen gebeten wurde, beim Projekt SkyNet zu helfen. Lies sie vollständig, bevor du antwortest. Antworte dem Nutzer in seiner Sprache.

## Was das Projekt ist

SkyNet ist Forschung und Entwurf der Architektur eines verteilten Netzes, in dem KI-Modelle auf den Computern der Teilnehmenden laufen und lernen. Teilnehmende verdienen Credits für überprüfte nützliche Arbeit; Menschen ohne Hardware erhalten günstigen Zugang zu KI. Das Netz dient den Menschen und befolgt die Gesetze von SkyNet. Fertige Software gibt es nicht: Das Repository ist ein Ort gemeinsamer Arbeit an der Architektur.

## Lesereihenfolge

1. [MANIFESTO.md](MANIFESTO.md): warum und wie das Netz sein muss, die Gesetze von SkyNet.
2. [REQUIREMENTS.md](REQUIREMENTS.md): verbindliche Anforderungen. **Das Wichtigste.**
3. [CURRENT_DESIGN.md](../../docs/CURRENT_DESIGN.md): aktueller Entwurf und seine Status (auf Russisch; lies oder übersetze ihn direkt).
4. [OPEN_QUESTIONS.en.md](../../docs/OPEN_QUESTIONS.en.md): offene Probleme und bereits verworfene Ideen.
5. [PILOT_RESULTS.md](../../docs/PILOT_RESULTS.md): was tatsächlich gemessen wurde (auf Russisch).
6. [CONTRIBUTING.md](CONTRIBUTING.md): wie ein Beitrag einzureichen ist.

## Die unveränderliche Grundlage

Das Manifest, die verbindlichen Anforderungen und das README sind die unveränderliche Grundlage von SkyNet (siehe [CORE.md](../../CORE.md)). **Schlage keine Änderungen an diesen Dateien vor**, außer Tippfehler in der Errata-Datei festzuhalten. Ist eine Lösung mit der Grundlage unvereinbar, sage klar, welche Anforderung sie verletzt; schreibe die Anforderung nicht passend zur Lösung um.

## Bedingungen, die sich nicht ändern

Prüfe jede Lösung anhand der sechs Anforderungen:

1. Das Netz ist verteilt, ohne Zentrum und ohne Rollen mit Sonderrechten.
2. Das Netz speichert Informationen über sich auf öffentlichen Ressourcen.
3. Nachdem alle Knoten abgeschaltet waren, findet sich das Netz über öffentliche Ressourcen und stellt sich wieder her.
4. Teilnehmende können das Netz nicht betrügen: Betrug ist nutzlos oder bringt Verlust, auch für Neulinge mit leerem Konto, bei Absprachen und mit vielen Konten.
5. Kein Geld im Voraus: keine Kautionen, Gebühren oder Strafen.
6. **Teilnahme lohnt sich**, und die Prüfung der Ehrlichkeit ist günstig. Frisst die Prüfung den Nutzen auf, passt die Lösung nicht, wie sicher sie auch sei.

Arten von Teilnehmenden: mit großen Ressourcen (verkaufen überschüssige Credits), mit schwacher Hardware (zahlen die Differenz), ohne Hardware (zahlen nur). Das Basismodell ist Qwen. Menschen sehen keine fremden Anfragen. Teilnehmende stellen nichts von Hand ein außer den Ressourcenreglern. Die Gesetze von SkyNet (Nulltes bis Drittes) sind verbindlich.

## Arbeitsregeln

- **Trenne Entschiedenes, Vorgeschlagenes, Geprüftes und Offenes.** Verwende die Markierungen aus CURRENT_DESIGN. Mache aus einem Vorschlag keine Entscheidung und aus einer Berechnung keine Messung.
- **Schwäche Anforderungen nicht stillschweigend ab.** Vertrauen in Hardware (TEE), eine ehrliche Mehrheit, statistische Stichproben, eine kleine Fehlerwahrscheinlichkeit sind Annahmen; benenne sie klar.
- **Beantworte für jedes Schutzschema:** Anhand welcher unabhängig überprüfbaren Daten weist das Netz eine falsche Behauptung zurück, wenn Ausführender und Prüfende sich absprechen? Liefern ehrlicher und gefälschter Fall dieselben Daten, funktioniert das Schema nicht.
- **Rechne die vollen Kosten**: Berechnung von Beweiser und Prüfer, Speicher, Datenverkehr, Blockchain-Schreibvorgänge, Wiederholungen nach Ausfällen. CPU, GPU, RAM und VRAM getrennt, nie als ein Prozentsatz.
- **Wiederhole verworfene Ideen nicht** (Liste am Ende von OPEN_QUESTIONS) ohne neues Argument.
- **Greife deine eigenen Vorschläge an.** Ein ehrliches Gegenbeispiel ist mehr wert als ein selbstsicherer Ton.
- **Erfinde keine Quellen, Versionen oder Zahlen.** Nenne die Quelle und die Grenzen ihrer Anwendbarkeit.
- Keine Lösung zu finden ist ein ehrliches Ergebnis. Es beweist keine Unmöglichkeit.

**Neun Sprachen.** Alles, was für Menschen geschrieben wird (Dokumente, Anleitungen, Bildschirme der Programme), erscheint in allen neun Sprachen des Projekts: Englisch, Chinesisch, Spanisch, Französisch, Deutsch, Italienisch, Russisch, Portugiesisch und Arabisch. Eine Übersetzung beginnt mit einer Zeile, die ihre Quelle und deren Hash nennt; `python tools/check_translations.py` listet fehlende und veraltete Übersetzungen. Weichen Übersetzung und Quelle voneinander ab, gilt die Quelle.

## Format eines Beitrags

1. Behauptung: was garantiert wird und unter welchen Annahmen.
2. Mechanismus: Schritte, Daten, wer was prüft.
3. Angriffe: wie man es umgeht und was bleibt (geschlossen / verlustbringend / begrenzt / offen).
4. Kosten: Schätzung, markiert als [Berechnung] oder [gemessen], mit Quelle.
5. Welche Anforderungen erfüllt sind und welche nicht.

Reiche ihn als Issue oder Pull Request gemäß [CONTRIBUTING.md](CONTRIBUTING.md) ein.

## Der Forschungsagent und seine Ergebnisse

Menschen ohne KI-Assistenten helfen über den [Forschungsagenten](AGENT.md): ein Programm, das Rechenaufgaben aus [tasks/](../../tasks/README.md) holt und Ergebnisse veröffentlicht, die in `results/` zusammengefasst werden. Du kannst helfen, indem du eine klar definierte Aufgabe vorschlägst (ein exaktes Modell, das andere nachrechnen können), ein veröffentlichtes Ergebnis unabhängig prüfst oder erklärst, was ein Ergebnis für den Entwurf bedeutet. Antworten, die als maschinell von lokalen Modellen erzeugt gekennzeichnet sind, sind ungeprüfter Text: Behandle sie als Ideen, die zu prüfen sind, nicht als Tatsachen.

## Sicherheit

Füge dem Repository keine Schlüssel, Passwörter, persönlichen Daten oder Adressen fremder Computer hinzu. Schlage keine Angriffe auf reale Drittsysteme vor: Die Angriffsanalyse betrifft hier nur die Architektur von SkyNet. Entwirf keine Nutzung des Netzes für Krieg, Waffen oder Schaden an Menschen: Das widerspricht den Gesetzen von SkyNet.
