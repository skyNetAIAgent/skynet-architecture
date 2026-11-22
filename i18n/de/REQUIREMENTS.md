# Verbindliche Anforderungen an SkyNet

[English](../../REQUIREMENTS.md) · [中文](../zh/REQUIREMENTS.md) · [Español](../es/REQUIREMENTS.md) · [Français](../fr/REQUIREMENTS.md) · **Deutsch** · [Italiano](../it/REQUIREMENTS.md) · [Русский](../ru/REQUIREMENTS.md) · [Português](../pt/REQUIREMENTS.md) · [العربية](../ar/REQUIREMENTS.md)

*Version 1, 22. November 2026. Kanonische Fassung, Teil der unveränderlichen Grundlage von SkyNet.*

Diese Anforderungen bilden zusammen mit dem [Manifest](MANIFESTO.md) und den Gesetzen von SkyNet die **unveränderliche Grundlage des Netzes**: Sie können weder durch Abstimmung noch durch Entscheidung der Schöpfer, der Entwickler oder einer Mehrheit der Teilnehmenden geändert werden. Eine Lösung, die auch nur eine Anforderung verletzt, ist für SkyNet ungeeignet. Sie kann als Forschung diskutiert werden, aber mit dem klaren Hinweis, welche Anforderung sie verletzt.

## Die sechs Hauptbedingungen

| Nr. | Anforderung | Wie man eine Lösung prüft |
|---|---|---|
| R1 | **Das Netz ist verteilt.** | Geräte verschiedener Teilnehmender halten den Betrieb gemeinsam aufrecht. Der Verlust eines Knotens, eines beliebigen Servers, auch eines, der den Schöpfern des Projekts gehört, oder einer Veröffentlichungsplattform hindert die anderen nicht am Weitermachen. |
| R2 | **Das Netz speichert Informationen über sich selbst auf öffentlichen Ressourcen.** | Die installierte Software erhält von außen genügend Informationen, um das Netz zu erkennen und zurückkehrende Knoten zu finden. Diese Informationen überstehen das gleichzeitige Abschalten aller Knoten. Es gibt mehrere Quellen. |
| R3 | **Das Netz findet sich nach einer vollständigen Abschaltung selbst und stellt sich wieder her.** | Zurückkehrende Programme finden einander selbstständig über öffentliche Ressourcen, ohne die Adresse eines aktiven Koordinators und ohne manuelle Knotenliste. |
| R4 | **Teilnehmende können das Netz nicht betrügen.** | Eine falsche Behauptung führt weder zu einem angenommenen Ergebnis noch zu fremden Befugnissen, einer unverdienten Belohnung oder einer umgeschriebenen Historie. Absprachen und Mehrfachkonten (Sybil) werden berücksichtigt. Für jede Lösung wird gezeigt, anhand welcher unabhängig überprüfbaren Daten das Netz eine falsche Behauptung zurückweist. **Praktische Bedeutung:** Betrug ist nutzlos oder bringt Verlust, auch für Neulinge mit leerem Konto. |
| R5 | **Kein Geld im Voraus.** | Keine Gebühren, keine Kautionen, keine vom Konto abgebuchten Strafen. Kautionen und Strafen schrecken Teilnehmende ab. |
| R6 | **Teilnahme lohnt sich.** | Ressourcen bereitzustellen (GPU, VRAM, CPU, RAM, SSD, HDD) ist profitabel. Die Prüfung der Ehrlichkeit ist günstig: Ihre Kosten sind für alle annehmbar, besonders für Besitzer großer Anlagen und teuren Stroms. |

**R6 ist die wichtigste.** Wenn die Prüfung der Ehrlichkeit viel Rechenaufwand erfordert, lohnt sich die Teilnahme nicht mehr, und das Netz verliert seinen Sinn.

## Arten von Teilnehmenden

| Teilnehmende | Was sie tun |
|---|---|
| Mit großen Ressourcen | Verdienen genug Credits für den eigenen Bedarf und verkaufen den Überschuss an andere |
| Mit schwacher Hardware | Verdienen weniger, als sie für die Modelle des Netzes ausgeben, und zahlen die Differenz in Kryptowährung oder Geld |
| Ohne Hardware | Nur Verbraucher: zahlen für die Nutzung der Modelle |

Ein und dieselbe Person kann Ressourcenanbieter und Nutzer zugleich sein.

## Weitere beschlossene Bedingungen

- **Der Zustand bleibt erhalten.** Bestätigte Rechte, Verpflichtungen, die Historie angenommener Aufgaben, die zuletzt angenommene Modellversion und die Daten zur Fortsetzung des Trainings überstehen einen vollständigen Stillstand. Die Wiederholung eines unvollendeten Schritts bringt keine zweite Belohnung.
- **Spaltung des Netzes.** Widersprechen sich Historien, warten strittige Gutschriften auf die kanonische Historie. Ein Beitrag wird nie zweimal bezahlt.
- **Austauschbare Plattformen und Schlüssel.** Der Verlust eines Kontos, Spiegels oder Schlüssels verhindert die Wiederherstellung nicht für immer.
- **Entscheidungen nach Neustart überprüfbar.** Für Gutschriften, Regeländerungen und die Annahme einer Modellversion werden Daten aufbewahrt, mit denen jeder Knoten die Grundlage der Entscheidung prüfen kann.
- **Öffentliches Minimum.** Der offene Katalog enthält nur das, was für das Auffinden und die Echtheitsprüfung nötig ist. Private Schlüssel, private Anfragen und persönliche Daten werden nicht veröffentlicht.
- **Privatsphäre.** Menschen sehen keine fremden Anfragen und keine persönlichen Daten anderer.
- **Unabhängigkeit von Einzelnen.** Niemand hat Sonderrechte, auch nicht der Entwickler. Das Netz legt seinen Trainingsplan selbst fest und ändert ihn; eine Abstimmung über eine Liste von Optionen ist zulässig.
- **Einfach für Teilnehmende.** Teilnehmende wählen nichts von Hand: Software installieren, Bedingungen annehmen, Ressourcenregler einstellen, „Start“ drücken.
- **Getrennte Ressourcengrenzen.** CPU, GPU, RAM, VRAM und Festplatte werden getrennt begrenzt; sie lassen sich nicht zu einem Prozentsatz addieren.
- **Alle freie Leistung trainiert.** Leistung, die nicht von Anfragen belegt ist, fließt ins Training.
- **Basismodell.** Anfangs Qwen mit offenen Gewichten und freier Lizenz. Ein Wechsel ist nur zu einem anderen Modell mit offenen Gewichten und freier Lizenz möglich.
- **Gesetze von SkyNet.** Die vier Gesetze aus dem [Manifest](MANIFESTO.md) binden sowohl das Verhalten des Modells als auch die Regeln des Netzes. Das Netz dient den Menschen und wird nicht als Kriegswerkzeug gebaut.

## Was die Anforderungen nicht ersetzen kann

- Laufzeit, Anzahl der Berichte und Checkpoint-Intervall sind **keine** Grundlage für Bezahlung.
- Die Signatur eines Teilnehmenden, selbst zusammen mit der Signatur eines anderen Knotens, **beweist nicht**, dass eine Ressource bereitgestellt wurde: Wer sich abspricht, unterschreibt alles.
- Statistische Stichproben, Vertrauen in eine Hardware-Enklave (TEE) oder ein kleiner kryptografischer Fehler sind Annahmen. Man darf sie vorschlagen, muss sie aber klar benennen und darf sie nicht als Erfüllung von R4 ausgeben.
- Ein erfolgreicher Test beweist keinen Schutz vor Betrug.
