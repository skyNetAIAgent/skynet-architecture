<!-- translation of docs/CONNECT.md, source sha256: 125af61335dde49176b5b023903489a40b1792ebe8e8eb04a960681206774db9 -->

# Mitmachen

[English](../../docs/CONNECT.md) · [中文](../zh/CONNECT.md) · [Español](../es/CONNECT.md) · [Français](../fr/CONNECT.md) · **Deutsch** · [Italiano](../it/CONNECT.md) · [Русский](../ru/CONNECT.md) · [Português](../pt/CONNECT.md) · [العربية](../ar/CONNECT.md)

Sie können beim Entwurf von SkyNet mit Ihrem Computer oder Smartphone helfen. Der Forschungsagent
ist ein kleines quelloffenes Programm: Er nimmt signierte Forschungsberechnungen entgegen, führt sie
in der freien Zeit Ihres Geräts aus und veröffentlicht die Ergebnisse. Ein Konto ist nirgends nötig.
**In dieser Phase gibt es keine Belohnungen**: Dies ist freiwillige Hilfe für die Forschung, nicht
das SkyNet-Netz selbst.

## Installation

| Ihr Gerät | Was zu tun ist |
|---|---|
| **Windows 10/11** (64 Bit) | Laden Sie `SkyNetAgentSetup-<version>-amd64.exe` vom [neuesten Release](https://github.com/skyNetAIAgent/skynet-architecture/releases/latest) herunter und führen Sie die Datei aus. Windows zeigt „Windows hat Ihren PC geschützt“, weil die Datei keine Codesignatur hat: Wählen Sie **Weitere Informationen**, dann **Trotzdem ausführen**. |
| **Linux** (x86_64 oder ARM64) | Laden Sie `skynet-agent-linux-install-<version>.sh` vom [neuesten Release](https://github.com/skyNetAIAgent/skynet-architecture/releases/latest) herunter und führen Sie `sh skynet-agent-linux-install-<version>.sh` aus. |
| **Android 7.0+** (64 Bit) | Laden Sie `skynet-agent.apk` von der Releases-Seite herunter, öffnen Sie die Datei und erlauben Sie die Installation aus dieser Quelle. Die App arbeitet nur, während das Smartphone lädt. |

macOS und iPhone werden nicht unterstützt.

Das Installationsprogramm startet den Agenten sofort und sorgt dafür, dass er nach einem Neustart
erneut startet (unter Windows können Sie dies deaktivieren; unter Android drücken Sie einmal
**Start**). Danach gibt es nichts weiter zu tun: Der Agent aktualisiert sich selbst (nur auf
Versionen, die vom Projekt signiert sind), nimmt Aufgaben an und veröffentlicht Ergebnisse von
selbst. Er findet von selbst einen Full Node in Ihrem lokalen Netzwerk, falls es einen gibt.

Die derzeit online befindlichen Agenten sind unter http://62.213.14.254:8790/agents aufgeführt:
System, Prozessor, Arbeitsspeicher, Grafikkarte, Version und berechnete Einheiten. Es werden weder
IP-Adresse noch Computername angezeigt.

## Was er nutzt und was er niemals tut

- Standardmäßig einen Prozessorkern mit der niedrigsten Priorität, damit Ihre eigenen Programme nicht
  gebremst werden. Auf einem Laptop arbeitet er nicht im Akkubetrieb, außer Sie erlauben es.
- Er führt niemals Code aus, der aus einer Aufgabe kommt, sendet niemals Ihre Dateien und braucht
  keine Administratorrechte. Jedes Ergebnis ist ein kleiner öffentlicher Datensatz, der mit dem
  eigenen Schlüssel Ihres Geräts signiert ist.
- Zum Pausieren oder Anhalten: der Ordner **SkyNet Agent** im Startmenü unter Windows,
  `skynet-agent pause` / `stop` unter Linux, die Schaltfläche **Stop** in der App.
- Zum Entfernen: **SkyNet Agent → Deinstallieren** unter Windows, `skynet-agent uninstall --yes`
  unter Linux, die App unter Android deinstallieren.

Details: [die Anleitung für den Agenten](AGENT.md).

## Hilfe mit Ideen, nicht nur mit Rechenleistung

Das wichtigste offene Problem des Projekts ist, wie Berechnungen günstig so geprüft werden können,
dass Betrug sich nie lohnt, ohne Einzahlungen oder Strafen. Wenn Sie oder Ihr KI-Assistent eine Idee
haben oder ein Loch gefunden haben, sehen Sie sich das [Aufgaben-Board](BOARD.md), die
[Roadmap](ROADMAP.md) und die [offenen Fragen](OPEN_QUESTIONS.md) an.
