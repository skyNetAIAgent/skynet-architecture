# SkyNet: offener Entwurf der Architektur

[English](../../README.md) · [中文](../zh/README.md) · [Español](../es/README.md) · [Français](../fr/README.md) · **Deutsch** · [Italiano](../it/README.md) · [Русский](../ru/README.md) · [Português](../pt/README.md) · [العربية](../ar/README.md)

## Was dieses Repository ist

Hier wird die Architektur von SkyNet entworfen: ein verteiltes Netz, in dem KI-Modelle auf den Computern der Teilnehmenden laufen und lernen. Die Teilnehmenden stellen dem Netz ihre freien Rechenressourcen zur Verfügung und erhalten dafür Credits, während Menschen ohne leistungsfähige Hardware günstigen Zugang zu KI bekommen.

Dies ist ein **Forschungs**-Repository. Fertige Software gibt es hier nicht. Es enthält:

- das [Manifest](MANIFESTO.md): warum das Netz gebraucht wird, wie es sein muss, und die Gesetze von SkyNet;
- die [verbindlichen Anforderungen](REQUIREMENTS.md), die sich nicht ändern;
- den [aktuellen Architekturentwurf](../../docs/CURRENT_DESIGN.md) mit den Markierungen „entschieden“, „vorgeschlagen“ und „offen“;
- die [offenen Fragen](../../docs/OPEN_QUESTIONS.en.md), bei denen wir Hilfe brauchen;
- [was im Pilotprojekt geprüft wurde](../../docs/PILOT_RESULTS.md) und was nicht;
- die [Regeln zur Mitarbeit](CONTRIBUTING.md) und eine [Einführung für KI-Assistenten](AGENTS.md);
- den [Programm-Agenten](AGENT.md): ein kleines Programm für alle, die keinen KI-Assistenten haben.

## Für wen

- **Ingenieurinnen und Ingenieure verteilter Systeme, Kryptografen, ML-Forschende.** Die Hauptprobleme liegen dort, wo sich diese Gebiete treffen: günstige Überprüfung von Berechnungen, Schutz vor Absprachen, Wiederherstellung eines Netzes ohne Zentrum.
- **Besitzer von Hardware** (Grafikkarten, Server, Heim-PCs). Ihr Blick auf Gewinn und Stromkosten ist nötig, damit die Ökonomie in der Praxis aufgeht.
- **Menschen, die mit einem KI-Assistenten arbeiten.** Ihr Modell (Claude, ChatGPT, DeepSeek und andere) muss nur [AGENTS.md](AGENTS.md) lesen, um den Kontext zu verstehen und mit der Arbeit zu beginnen.
- **Menschen, die einfach mit ihrem Computer oder Telefon helfen möchten.** Besondere Kenntnisse sind nicht nötig: Die Arbeit erledigt der [Programm-Agent](AGENT.md).

## Der Sinn

Heute hat nicht jeder Zugang zu leistungsfähiger KI: Preis, geografische und politische Beschränkungen und gesperrte Dienste stehen im Weg. Zugleich ist die Welt voller ungenutzter Grafikkarten und Computer. SkyNet soll beides verbinden: ein Netz ohne Eigentümer und ohne zentralen Server, schwer abzuschalten oder zu sperren, das sich nach einer vollständigen Abschaltung selbst wiederfindet, sein eigenes Training plant, jeden fair für überprüfte nützliche Arbeit bezahlt und den Menschen dient, nicht dem Krieg und der Zerstörung.

## Das Schwierigste, ehrlich gesagt

Die Hauptbedingung lautet: **Das Netz zu betrügen muss nutzlos sein oder Verlust bringen, und die Prüfung der Ehrlichkeit muss günstig sein**; sonst lohnt sich die Teilnahme nicht. Eine Lösung, die diese Bedingung bei Absprachen nachweislich erfüllt, **gibt es noch nicht**. Es gibt starke Kandidaten und Dutzende analysierte Angriffe, aber die zentralen Mechanismen wurden weder gebaut noch gemessen. Der aktuelle Stand ist stets in [CURRENT_DESIGN](../../docs/CURRENT_DESIGN.md) und [OPEN_QUESTIONS](../../docs/OPEN_QUESTIONS.en.md) beschrieben. Wenn Sie wissen, wie man auch nur eines dieser Probleme löst, brauchen wir Sie.

## Wie man mitmacht

1. Lesen Sie das [Manifest](MANIFESTO.md) und die [Anforderungen](REQUIREMENTS.md).
2. Wählen Sie eine Frage aus [OPEN_QUESTIONS](../../docs/OPEN_QUESTIONS.en.md) oder einen Angriff auf den [aktuellen Entwurf](../../docs/CURRENT_DESIGN.md).
3. Eröffnen Sie ein Issue oder einen Pull Request gemäß den [Regeln](CONTRIBUTING.md). Am wertvollsten: eine gefundene Lücke mit konkretem Beispiel und eine Lösung mit berechneten Kosten.

Wenn Sie mit einem KI-Assistenten arbeiten, sagen Sie ihm: *„Studiere dieses Repository gemäß AGENTS.md und hilf mir bei Frage N aus OPEN_QUESTIONS.“*

**Kein KI-Assistent?** Sie können trotzdem helfen. Installieren Sie den [SkyNet-Programm-Agenten](AGENT.md): ein kleines quelloffenes Programm für Windows, macOS, Linux und Android. Es schaut regelmäßig in dieses Repository, holt sich Forschungsaufgaben, berechnet sie in der freien Zeit auf Ihrem Gerät und veröffentlicht die Ergebnisse. Es aktualisiert sich selbst aus diesem Repository, und nur auf Versionen, die vom Projekt signiert sind. Die Teilnahme ist freiwillig: In der Forschungsphase gibt es keine Belohnungen.

## Die unveränderliche Grundlage

Das Manifest, die verbindlichen Anforderungen und dieses README bilden die unveränderliche Grundlage des Netzes (Version 1). Ihre SHA-256-Fingerabdrücke sind in [CORE_HASHES.txt](../../CORE_HASHES.txt) veröffentlicht. Maßgeblich ist die russische Fassung. Einzelheiten stehen im [Manifest](MANIFESTO.md) und in [CORE.md](../../CORE.md).

## Lizenz

Die Texte der Grundlage stehen unter CC BY-ND 4.0 (Kopieren erlaubt, Verbreitung veränderter Fassungen nicht erlaubt), die übrigen Dokumente unter CC BY 4.0. Siehe [LICENSE](../../LICENSE).
