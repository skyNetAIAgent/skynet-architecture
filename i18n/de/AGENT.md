# SkyNet-Forschungsagent

[English](../../agent/README.md) · [中文](../zh/AGENT.md) · [Español](../es/AGENT.md) · [Français](../fr/AGENT.md) · **Deutsch** · [Italiano](../it/AGENT.md) · [Русский](../ru/AGENT.md) · [Português](../pt/AGENT.md) · [العربية](../ar/AGENT.md)

Sie können beim Entwurf von SkyNet helfen, indem Sie Ihren Computer einen Teil der Forschung erledigen lassen. Der Agent ist ein kleines quelloffenes Programm. Er prüft dieses Repository auf Aufgaben, erledigt ein Stück einer Berechnung und teilt das Ergebnis. Sie können auf dem Aufgaben-Board auch eine Forschungsfrage stellen oder die eines anderen beantworten. Sie brauchen weder ein Konto noch einen KI-Assistenten. [Anleitung für das Aufgaben-Board](BOARD.md)

**In dieser Phase gibt es keine Belohnungen.** Es gibt keine Credits, keine Zahlungen und keine Versprechen künftiger Zahlungen. Dies ist freiwillige Forschung, um beim Entwurf des SkyNet-Netzes zu helfen.

## Was er tut und was er niemals tut

| Er tut | Er tut niemals |
|---|---|
| Liest eine signierte Aufgabenliste. Jede Aufgabe nennt eine eingebaute Berechnung und liefert ihre Eingaben | Führt Code aus einer Aufgabe oder einem Board-Beitrag aus |
| Führt standardmäßig ein Stück Arbeit nach dem anderen aus, mit niedriger CPU-Priorität | Startet standardmäßig kein neues Stück, wenn Akkubetrieb erkannt wird |
| Signiert Ergebnisse mit dem Schlüssel dieses Geräts und sendet sie standardmäßig an öffentliche Relays und einen Vollknoten | Nimmt Ihre persönlichen Dateien oder Hardwarekennungen in ein automatisches Ergebnis auf |
| Prüft die Projektsignatur, bevor er ein Desktop-Update installiert | Akzeptiert ein heruntergeladenes Update mit ungültiger Signatur, falschem Datei-Hash oder älterer Release-Nummer |
| Installiert für Ihr Benutzerkonto und lässt Sie wählen, ob er bei der Anmeldung startet | Benötigt Administratorrechte für eine normale Desktop-Installation |

Eine Forschungsfrage ist, ob ein Teilnehmer, der das Netz verlassen will, mit einem Schwung gefälschter Ergebnisse Gewinn machen kann. Wie viele Prüfer müssten dabei helfen? Verschiedene Geräte, denen dasselbe Stück dieser Berechnung gegeben wird, sollten genau dieselbe Antwort erhalten, sodass ihre Ergebnisse verglichen werden können. [Forschungsaufgaben](../../tasks/README.md)

## Voraussetzungen

- Windows auf x64 (amd64) oder ARM64 oder Linux auf amd64, arm64 oder ARMv7. Der Desktop-Agent in 1.0.1 ist ein einzelnes Go-Programm. Die Installationsprogramme aus den Releases enthalten die ausführbare Datei, bereit zum Ausführen. macOS wird nicht unterstützt.
- Für die experimentelle Android-App: Android 7.0 oder neuer auf arm64-v8a oder x86_64.
- Eine Internetverbindung, um neue Aufgaben zu empfangen und Ergebnisse zu veröffentlichen. Das Linux-Installationsprogramm aus den Releases kann offline installieren.

## Installation

**Windows**

1. Wählen Sie das Windows-Installationsprogramm (`.exe`) für Ihren Computer, amd64 oder arm64, aus den [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases).
2. Vergleichen Sie die SHA-256-Prüfsumme der Datei mit der Prüfsumme aus einer Quelle, der Sie vertrauen, und führen Sie dann das Installationsprogramm aus. Sie können wählen, ob der Agent jetzt und bei der Anmeldung startet. Die Einrichtung fügt Verknüpfungen zum Startmenü hinzu. [Windows-Installationshandbuch](../../installer/windows/README.md)

**Linux**

Laden Sie `skynet-agent-install.sh` von den [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) herunter und führen Sie `sh skynet-agent-install.sh` als normaler Benutzer aus. Die Datei enthält ausführbare Dateien für alle drei unterstützten Linux-Architekturen.

Sie können auch mit dem folgenden Befehl über das Netzwerk installieren. Er benötigt `curl`, `jq`, `xxd`, `sha256sum` und OpenSSL mit Ed25519-Unterstützung.

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

Standardmäßig behält die Einrichtung Ihre bestehende Einstellung für die Anmeldung bei. Bei einer Neuinstallation starten Sie den Agenten selbst mit `skynet-agent run`. Um ihn jetzt und bei der Anmeldung zu starten, führen Sie `sh skynet-agent-install.sh --autostart` aus. Dies nutzt Ihren systemd-Benutzerdienst. Fügen Sie `--linger` hinzu, damit er ab dem Systemstart und nach der Abmeldung läuft, oder verwenden Sie `--no-autostart`, um den Dienst auszuschalten. Wenn Ihre Shell den Befehl nicht findet, verwenden Sie `~/.local/bin/skynet-agent`. [Linux-Installationshandbuch](../../installer/linux/README.md)

**Android (experimentell)**

Laden Sie `skynet-agent.apk` von den [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) herunter. Öffnen Sie die Datei und erlauben Sie die Installation aus Ihrem Browser oder Dateimanager, wenn Android danach fragt. Öffnen Sie **SkyNet Agent** und tippen Sie auf **Start**. Standardmäßig berechnet er nur, während das Gerät geladen wird. **Nach dem Neustart starten** ist standardmäßig ausgeschaltet.

Das APK hat eine eigene Versionsnummer. App-Version 0.3.0 enthält den Go-Agenten 1.0.0. Die App bietet Updates auf ihrem Bildschirm oder in einer Benachrichtigung an. Sie prüft die signierte Versionsbeschreibung sowie Größe und SHA-256 des APK, bevor sie Sie bittet, die Installation in Android zu bestätigen. [Android-Anleitung](../../android/README.md)

Ihr Geräteschlüssel, Ihre Einstellungen und Ihre Ergebnisse liegen im Ordner Ihres Agenten. Standardmäßig ist das `%LOCALAPPDATA%\SkyNetAgent` unter Windows und `~/.local/share/skynet-agent` unter Linux (oder `$XDG_DATA_HOME/skynet-agent`, falls gesetzt). Mit `SKYNET_AGENT_HOME` oder `--home DIR` können Sie beim Linux-Installationsprogramm außerdem einen anderen Ordner auswählen. Android bewahrt sein Profil im privaten Speicher der App auf.

Wenn Sie den Python-Agenten bereits auf einem unterstützten Desktop mit eingeschalteten automatischen Updates ausführen, wechselt er über die signierte **0.4.0**-Bridge-Version von selbst zu Go. Er behält Ihren Geräteschlüssel, Ihren Fortschritt und nicht gesendete Ergebnisse. Die vorherige Bridge und ihr Interpreter bleiben für einen Rückfall erhalten.

## Erste Schritte

Unter Linux verwenden Sie die folgenden Befehle. Unter Windows öffnen Sie PowerShell im Ordner des Agenten und verwenden `.\skynet-agent.exe launch` anstelle von `skynet-agent`. Zum Beispiel zeigt `.\skynet-agent.exe launch status` Ihren Status über den permanenten Starter an.

```sh
skynet-agent verify-install       # die installierten Release-Dateien prüfen und eine Testberechnung ausführen
skynet-agent selftest --online    # die Berechnung ausführen und signierte Dokumente online prüfen
skynet-agent net id               # den öffentlichen Schlüssel dieses Geräts anzeigen, seinen Namen auf dem Board
skynet-agent run                  # falls er noch nicht läuft, arbeiten, bis Sie Strg+C drücken
```

Verwenden Sie `skynet-agent autostart status`, um zu sehen, ob der Start bei der Anmeldung eingeschaltet ist. Um ihn einzuschalten, verwenden Sie `skynet-agent autostart enable`.

### Ergebnisse veröffentlichen

Der Agent speichert jedes fertige Ergebnis im Postausgang. Er verwendet den Signaturschlüssel in `identity.key` im Ordner des Agenten und erzeugt bei der ersten Verwendung einen, falls die Datei fehlt. Standardmäßig sendet er das signierte Ergebnis an öffentliche Nostr-Relays und einen Vollknoten. Ein Knoten oder zwei verschiedene Relays müssen den Empfang bestätigen, bevor der Agent das Ergebnis nach `sent` verschiebt. Andernfalls bleibt es im Postausgang. Jeder erneute Versuch verwendet denselben signierten Datensatz mit derselben ID.

Hier ist ein Teil eines Ergebnisses für eine Aufgabe, die die eingebaute Testberechnung verwendet. Das vollständige Ergebnis enthält außerdem den Aufgabennamen, die verstrichenen Sekunden, die Formatversion, die Release-Nummer des Agenten und standardmäßig eine Plattformkennung. Der signierte Datensatz darum herum trägt den öffentlichen Schlüssel des Geräts, einen Zeitstempel, die Datensatz-ID und die Signatur.

```json
{
  "agent": "1.0.1", "kernel": "selftest@1", "unit": 0, "units": 1,
  "result": {
    "kernel": "selftest@1", "rounds": 8, "ok": true,
    "digest": "a2e8f2c45179bfccb6a01d61ab527a86277215a6ee85ff824910fe27d3e9fe26"
  },
  "result_sha256": "7823a03918e86a7046e437fdf001dc40ff05fb1d241a8917baeae4d88b5629fa"
}
```

## Befehle

| Desktop-Befehl | Was er tut |
|---|---|
| `skynet-agent run` | Arbeitet bis zum Anhalten. `--once` versucht höchstens ein Stück. `--no-submit` behält Ergebnisse für diesen Lauf lokal. `--no-update` überspringt die Update-Installation. `--verbose` ergänzt Details im Protokoll. |
| `skynet-agent status` | Zeigt Version, Agentenordner, Energiezustand, Arbeitszähler, wartende Ergebnisse und letzte Probleme. |
| `skynet-agent tasks` | Listet die automatischen Forschungsaufgaben auf, welche bereit sind und wie viele Stücke dieses Gerät erledigt hat. |
| `skynet-agent pause` / `resume` | Lässt aktive Stücke zu Ende laufen und startet keine neuen mehr oder erlaubt wieder neue Stücke. |
| `skynet-agent stop` | Den laufenden Agenten bitten, sich zu beenden. |
| `skynet-agent outbox` | Listet Einträge in der Warteschlange auf, zeigt sie an, sendet sie oder verwirft sie. Verwenden Sie `edit` und `approve`, um KI-Berichtsentwürfe wie unten beschrieben zu prüfen. |
| `skynet-agent ai` | Zeigt den Modellserver und das ausgewählte Modell. Verwenden Sie `ai answer TASK-ID`, um einen Board-Bericht zu entwerfen. |
| `skynet-agent net` | Das Board mit `tasks` oder `show` durchsuchen. Mit `post-task`, `claim`, `report`, `accept` oder `revise` teilnehmen. `sync` versucht ausstehende Board-Beiträge erneut und ruft Datensätze ab. `id` zeigt Ihren öffentlichen Schlüssel. [Board-Anleitung](BOARD.md) |
| `skynet-agent config` | `show` listet Einstellungen auf, `get KEY` zeigt eine an und `set KEY VALUE` ändert sie. |
| `skynet-agent update` | Prüft auf eine neuere signierte Desktop-Version und installiert sie, wenn sie für dieses Gerät geeignet ist. |
| `skynet-agent selftest [--online]` | Prüft eine Berechnung gegen ihre bekannte Antwort. Mit `--online` werden die Signaturen auf der Aufgabenliste und der älteren Versionsbeschreibung des Projekts geprüft. |
| `skynet-agent verify-install` | Überprüft die installierten Release-Dateien und führt die Testberechnung aus. |
| `skynet-agent version` | Zeigt die Agentenversion, Release-Nummer, Go-Version und Plattform. |
| `skynet-agent autostart` | `status` zeigt, ob der Start bei der Anmeldung eingeschaltet ist. `enable` schaltet ihn ein und `disable` aus. |
| `skynet-agent uninstall --yes` | Entfernt eine Linux-Installation. Fügen Sie `--purge` hinzu, um auch gespeicherte Daten zu löschen. |

## Einstellungen

| Einstellung | Standard | Bedeutung |
|---|---|---|
| `workers` | 1 | Anzahl der Stücke, die der Desktop-Agent gleichzeitig ausführen kann, von 1 bis 256. Android führt eines aus. |
| `run_on_battery` | false | Berechnungen im Akkubetrieb erlauben. |
| `paused` | false | Vor dem Start neuer Stücke warten. Die Befehle `pause` und `resume` ändern diese Einstellung. |
| `poll_minutes` | 30 | Ungefähres Intervall zwischen Repository-Prüfungen, von 5 bis 1440 Minuten. Fehlgeschlagene Prüfungen haben ihren eigenen Wiederholungsplan. |
| `update` | auto | Auf dem Desktop installiert `auto` geeignete signierte Updates, `notify` protokolliert, wenn eines verfügbar ist, und `off` überspringt Installation und Hinweise. Alle drei prüfen weiterhin auf eine signierte Pause von den Betreuern. |
| `submit` | auto | `auto` sendet Ergebnisse, während die Arbeit fortschreitet. `manual` behält sie im Postausgang, bis Sie `skynet-agent outbox send` ausführen. |
| `submit_via` | net | Signierte Datensätze über Relays und Knoten veröffentlichen. Dies ist der einzige funktionierende Kanal in 1.0. |
| `max_task_minutes` | 120 | Zeitlimit pro Stück, von 1 bis 1440 Minuten. Ein kürzeres Limit in der Aufgabe hat Vorrang. |
| `report_platform` | true | Betriebssystem, Prozessorarchitektur und Go-Version in neue Ergebnisse aufnehmen, zum Beispiel `linux-amd64-` gefolgt von der Go-Version. |

Zum Beispiel erlaubt `skynet-agent config set workers 4` bis zu vier Desktop-Worker. Das Profil bewahrt außerdem die älteren Python-Kommentarlimits auf.

## Board-Berichte mit einem lokalen KI-Modell entwerfen

Starten Sie einen Modellserver und führen Sie `skynet-agent ai` aus, um zu sehen, welches Modell der Agent gefunden hat. Wenn `ai.endpoint` leer ist, versucht er Ollama auf Port 11434, llama.cpp auf 8080 und LM Studio auf 1234, alle über die Loopback-Schnittstelle. Verwenden Sie `config set ai.endpoint URL`, um einen Server auszuwählen, oder `config set ai.model NAME`, um ein aufgelistetes Modell auszuwählen. Standardmäßig wird das erste aufgelistete Modell verwendet. Ein Remote-Endpunkt erfordert `ai.allow_remote true` und empfängt den Aufgabentext.

Führen Sie `skynet-agent ai answer TASK-ID` für einen Entwurf aus, oder `skynet-agent config set ai.enabled true`, um das automatische Entwerfen während Board-Abfragen zu aktivieren. Automatisches Entwerfen ist standardmäßig ausgeschaltet. Der Agent überspringt Aufgaben mit einem akzeptierten Bericht, einem Bericht von diesem Gerät oder einem vorhandenen oder verworfenen Entwurf. Er übergibt den Titel, die Frage und die Akzeptanzkriterien als nicht vertrauenswürdigen Text an das Modell. Das Modell erhält keine Werkzeuge und keinen Dateizugriff. Das kombinierte Limit für eine Aufgabe beträgt 16.000 Zeichen. Die Standardwerte für `ai.timeout_minutes` und `ai.max_answer_chars` sind 30 Minuten und 8.000 Zeichen.

```sh
skynet-agent outbox list
skynet-agent outbox show NAME          # den Bericht und seinen SHA-256-Wert lesen
skynet-agent outbox approve NAME SHA256 # den von show ausgegebenen Digest verwenden
skynet-agent outbox send               # geeignete Einträge jetzt senden
```

Jeder Entwurf trägt die öffentliche Zusammenfassung `machine-generated, unverified`. Um den Text zu ersetzen, führen Sie `skynet-agent outbox edit NAME FILE` aus; zeigen Sie dann den bearbeiteten Entwurf an und genehmigen Sie ihn. Durch das Bearbeiten wird die vorherige Genehmigung ungültig. Ein genehmigter Bericht kann bei der nächsten automatischen Leerung des Postausgangs oder im manuellen Modus durch `outbox send` gesendet werden. Verwenden Sie `outbox drop NAME`, um den Entwurf zu verwerfen und diese Aufgabe bei künftigen Board-Abfragen zu überspringen.

## Sicherheit, ehrlich gesagt

- **Updates und Aufgabenlisten sind signiert.** Der Agent prüft ihre Ed25519-Signaturen gegen den Release-Schlüssel des Projekts, der in das Programm eingebaut ist. Bevor er zu einem Desktop-Update wechselt, prüft er die Release-Nummer, überprüft Größe und SHA-256 der ausführbaren Datei und führt eine Testberechnung aus. Er lehnt ältere Aufgabenlisten ab und beginnt keine Arbeit mehr aus einer abgelaufenen Liste.
- **Aufgaben liefern Daten.** Die einzigen Berechnungen, die eine Aufgabe auswählen kann, sind in die ausführbare Datei eingebaut. Eine neue Art von Berechnung erfordert eine neue Desktop-Version oder ein Android-App-Update. [Go-Quelltext für die Berechnungen](https://github.com/skyNetAIAgent/skynet-architecture/tree/main/agent-go/kernels)
- **Jedes Stück läuft in einem eigenen Prozess** unter Ihrem Konto. Der Worker fordert eine niedrige CPU-Priorität an. Der Agent stoppt den Worker, wenn er das Zeitlimit erreicht.
- **Ein Desktop-Update kann zurückgerollt werden.** Der Starter prüft die aktive Version, bevor er sie startet. Wenn diese Prüfung fehlschlägt oder wenn drei aufeinanderfolgende Startversuche des Agenten innerhalb ihrer ersten Minute abstürzen, kann der Starter eine überprüfte vorherige Version wiederherstellen, falls eine verfügbar ist. Er merkt sich die fehlgeschlagene Release-Nummer.
- **Ihr Geräteschlüssel ist eine unverschlüsselte Datei.** Wer `identity.key` kopiert, kann als dieses Gerät signieren. Eine private Sicherung ermöglicht es Ihnen, Ihren Namen auf dem Board nach einer Neuinstallation zu behalten.
- **Die erste Installation hängt davon ab, woher Sie das Installationsprogramm oder Skript beziehen.** Nach der Installation kann jeder, der den Release-Schlüssel des Projekts kontrolliert, neuen Code signieren, der mit Ihren Benutzerrechten läuft. In dieser Forschungsphase liegt dieser Schlüssel bei den Betreuern. Wenn Sie Desktop-Updates zuerst prüfen möchten, verwenden Sie `skynet-agent config set update notify` und führen Sie `skynet-agent update` aus, wenn Sie bereit sind. Das vorgeschlagene SkyNet-Netz soll ohne einen zentralen Release-Schlüssel funktionieren. [Entwurf des Forschungsagenten und Bedrohungstabelle, auf Russisch](../../docs/RESEARCH_AGENT.md)

## Privatsphäre

GitHub sieht Ihre IP-Adresse, wenn Sie Aufgaben oder Updates herunterladen. Relays und Vollknoten, die Sie kontaktieren, sehen ebenfalls Ihre IP-Adresse. Der eingebaute Vollknoten verwendet unverschlüsseltes HTTP. Ergebnisse und Board-Beiträge sind öffentlich. Anhand ihres öffentlichen Schlüssels können Leser Datensätze desselben Geräts einander zuordnen.

Automatische Ergebnisse enthalten Berechnungsdaten und die oben beschriebenen Felder. Verwenden Sie `skynet-agent config set report_platform false`, um die Plattformkennung aus künftigen Ergebnissen wegzulassen. Der Agent durchsucht Ihre persönlichen Dateien nicht und fügt keine Hardware-Seriennummern ein. Wenn Sie eine Board-Aufgabe oder einen Bericht veröffentlichen, wird der Text, den Sie einreichen, öffentlich.

## Was es Sie kostet

Ein ausgelasteter Worker kann etwa einen CPU-Kern nutzen. Die niedrige Priorität hilft anderen Programmen, CPU-Zeit zu bekommen, wenn sie sie brauchen. Die Arbeit verbraucht weiterhin Strom und kann Wärme erzeugen. Auf einem Laptop prüft der Agent die Stromversorgung etwa einmal pro Minute. Standardmäßig wartet er mit dem Start neuer Stücke, wenn er Akkubetrieb erkennt. Ein bereits laufendes Stück kann zu Ende laufen, und der Desktop-Agent kann Arbeit starten, wenn die Stromquelle unbekannt ist.

Unter Android bricht das Trennen des Ladegeräts das aktuelle Stück ab und lässt es für einen erneuten Versuch verfügbar. Wählen Sie in der App **Auch im Akkubetrieb arbeiten**, wenn sie ohne Ladegerät weiter berechnen soll.

## Entfernen

Unter Windows verwenden Sie das Deinstallationsprogramm von **SkyNet Agent**. Es behält standardmäßig Ihren Geräteschlüssel, Ihre Warteschlangen und Ihren Versionsverlauf. Wählen Sie während der Deinstallation die Option zum Löschen der Daten, um auch diese zu entfernen.

Unter Linux führen Sie den folgenden Befehl aus. Er schaltet den Benutzerdienst aus, stoppt den Agenten und entfernt die installierten Programme. Ihr Schlüssel, Ihre Einstellungen, Ihr Fortschritt und Ihre Warteschlangen bleiben erhalten.

```sh
skynet-agent uninstall --yes
```

Um auch die gespeicherten Agentendaten zu entfernen, verwenden Sie beim Deinstallieren `skynet-agent uninstall --yes --purge`. Unter Android deinstallieren Sie **SkyNet Agent** über die Android-Einstellungen, um die App und ihre lokalen Daten zu entfernen. Veröffentlichte Datensätze bleiben öffentlich.

## Wenn etwas nicht klappt

- **„no valid signature from a trusted key“** bedeutet, dass die Überprüfung des heruntergeladenen Dokuments fehlgeschlagen ist. Der Agent lehnt es ab. Er kann weiterhin eine zuvor überprüfte Aufgabenliste verwenden, bis diese abläuft. Auf dem Desktop zeigt `skynet-agent status` den letzten Repository-Fehler. Das Laufprotokoll ist `logs/agent.log` im Ordner des Agenten.
- **Ergebnisse bleiben im Postausgang.** Verwenden Sie `skynet-agent status` oder `skynet-agent outbox list`, um zu sehen, was wartet. Im manuellen Modus führen Sie `skynet-agent outbox send` aus. Wenn zu wenige Relays oder Knoten antworten, bleibt das Ergebnis für einen weiteren Versuch in der Warteschlange.
- **Eine ältere Installation zeigt „GitHub submission is unsupported“ an.** Führen Sie `skynet-agent config set submit_via net` aus, um signierte Datensätze für neue Ergebnisse zu verwenden. Bereits für GitHub markierte Einträge und alte KI-Antworten bleiben zur Prüfung im Postausgang.
- **Der Agent läuft, aber es beginnt keine neue Arbeit.** Prüfen Sie `skynet-agent tasks` und das Laufprotokoll. Er ist möglicherweise pausiert, wartet auf Strom, hat keine geeigneten Aufgaben mehr oder wartet auf Platz in seinem Postausgang. Unter Android schließen Sie das Ladegerät an und tippen auf **Start**, wenn Sie die App zuvor gestoppt haben.

## Was bisher getestet ist

Agententests laufen automatisch unter Windows und Linux. Sie decken signierte Aufgabenlisten, Berechnungen mit bekannten Antworten, Updates und Rückfall, signierte Datensätze, Zustellung, das Aufgaben-Board und einen Lauf ab, der einen Worker startet und sein Ergebnis an einen simulierten Knoten zustellt.

Live-Installationen wurden unter Windows 11, Linux Mint, Ubuntu Server und einem Android-14-Emulator ausprobiert. Die Android-App muss noch auf einem physischen Gerät überprüft werden. Wenn bei Ihnen etwas nicht funktioniert, eröffnen Sie bitte ein Issue.

## Lizenz

Der Code des Agenten steht unter der [MIT-Lizenz](https://github.com/skyNetAIAgent/skynet-architecture/blob/main/agent-go/LICENSE).
