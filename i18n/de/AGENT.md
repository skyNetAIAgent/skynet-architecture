# SkyNet-Forschungsagent

[English](../../agent/README.md) · [中文](../zh/AGENT.md) · [Español](../es/AGENT.md) · [Français](../fr/AGENT.md) · **Deutsch** · [Italiano](../it/AGENT.md) · [Русский](../ru/AGENT.md) · [Português](../pt/AGENT.md) · [العربية](../ar/AGENT.md)

Übersetzung von [agent/README.md](../../agent/README.md).

Um beim Entwurf von SkyNet zu helfen, braucht man keinen KI-Assistenten. Der Forschungsagent ist ein kleines quelloffenes Programm. Er schaut regelmäßig in dieses Repository, holt sich Forschungsaufgaben, berechnet sie in der freien Zeit auf Ihrem Computer und veröffentlicht die Ergebnisse.

**In dieser Phase gibt es keine Belohnungen**: keine Credits, kein Geld und kein Versprechen künftiger Zahlungen. Es ist freiwillige Hilfe für die Forschung. Der Agent ist nicht das SkyNet-Netz, sondern ein Werkzeug, um es zu entwerfen.

## Was er tut und was er niemals tut

| Er tut | Er tut niemals |
|---|---|
| Liest die signierte Aufgabenliste und die signierte Versionsbeschreibung aus dem Repository | Code ausführen, der aus einer Aufgabe stammt. Eine Aufgabe ist der Name einer eingebauten Berechnung plus Zahlen |
| Führt eingebaute Berechnungen mit niedrigster CPU-Priorität aus, standardmäßig eine nach der anderen | Im Akkubetrieb arbeiten, außer Sie erlauben es |
| Veröffentlicht jedes Ergebnis als Kommentar auf GitHub unter Ihrem eigenen Konto | Ihre Dateien, Hardwarekennungen oder sonst etwas von Ihrem Computer senden |
| Aktualisiert sich selbst, aber nur auf eine Version, die mit dem Release-Schlüssel des Projekts signiert ist | Ein Update mit falscher Signatur, falschem Datei-Hash oder älterer Nummer installieren |
| Hält alles in einem Ordner in Ihrem Profil | Administratorrechte benötigen oder von selbst starten, solange Sie den Autostart nicht einschalten |

Die ersten Aufgaben sind exakte Berechnungen zu den Zahlungsregeln von SkyNet. Zum Beispiel: „Kann ein Teilnehmer, der das Netz verlässt, mit einem Schwung gefälschter Ergebnisse Gewinn machen, und ab welchem Anteil abgesprochener Prüfer?“ Jedes Gerät muss dieselben Ziffern erhalten, und die Ergebnisse verschiedener Menschen werden verglichen. Siehe [tasks/README.md](../../tasks/README.md).

## Voraussetzungen

- Python 3.9 oder neuer. Sonst nichts: Der Agent verwendet nur die Standardbibliothek von Python.
- Ein GitHub-Konto zum Veröffentlichen der Ergebnisse (kostenlos). Ohne Konto können Sie trotzdem rechnen und von Hand über einen Link veröffentlichen.
- Einige Megabyte Speicherplatz und eine Internetverbindung.

## Installation

**Windows** (PowerShell):

```powershell
irm https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.ps1 | iex
```

**Linux und macOS** (Terminal):

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

**Android, die App (experimentell)**: Laden Sie `skynet-agent.apk` von der Seite [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) herunter, erlauben Sie Ihrem Browser die Installation von Apps und öffnen Sie die Datei. Die App arbeitet nur, während das Gerät geladen wird; Ergebnisse werden mit einem GitHub-Token veröffentlicht, das Sie in die App einfügen. Auf einem echten Gerät noch nicht überprüft. Quelltext und Einzelheiten: [android/README.md](../../android/README.md).

**Android**: Installieren Sie die App [Termux](https://termux.dev) aus F-Droid, öffnen Sie sie und führen Sie aus:

```sh
pkg install python curl
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

Auf einem Telefon arbeitet der Agent nur, während es geladen wird. Kann er nicht feststellen, ob das Telefon lädt, wartet er und meldet das; installieren Sie dann die App Termux:API zusammen mit `pkg install termux-api`, oder erlauben Sie den Akkubetrieb: `skynet-agent config set run_on_battery true`.

Wenn Sie lieber erst lesen und dann ausführen: Laden Sie [`install.py`](../../agent/install.py) herunter, lesen Sie die Datei (sie ist kurz) und führen Sie `python3 -I install.py` aus.

Das Installationsprogramm legt den Agenten in einen Ordner (`%LOCALAPPDATA%\SkyNetAgent` unter Windows, `~/Library/Application Support/SkyNetAgent` unter macOS, `~/.local/share/skynet-agent` unter Linux und Android) und erstellt den Befehl `skynet-agent`. Es startet nichts.

## Erste Schritte

```sh
skynet-agent selftest --online    # Gerät und Signaturen prüfen
skynet-agent github               # prüfen, welches GitHub-Konto Ergebnisse veröffentlicht
skynet-agent run                  # arbeiten, bis Sie Strg+C drücken
skynet-agent autostart enable     # optional: beim Anmelden starten
```

Unter Windows ist der Befehl die Datei `skynet-agent.cmd` im Ordner des Agenten; das Installationsprogramm gibt die genaue Zeile aus.

### Ergebnisse veröffentlichen

Ergebnisse sind Kommentare im Tracking-Issue der Aufgabe in diesem Repository, veröffentlicht von Ihrem eigenen GitHub-Konto. Am einfachsten melden Sie sich mit dem Kommandozeilenwerkzeug von GitHub an:

1. Installieren Sie [GitHub CLI](https://cli.github.com) (`winget install GitHub.cli`, `brew install gh`, `pkg install gh` in Termux oder über den Paketmanager Ihres Linux).
2. Führen Sie `gh auth login` aus und folgen Sie den Anweisungen im Browser.
3. Führen Sie `skynet-agent github` aus. Der Befehl gibt den Kontonamen aus.

Der Agent fragt `gh` nach der Anmeldung, wenn er sie braucht, und speichert weder Passwort noch Token. Alternativen: ein Token in der Umgebungsvariablen `SKYNET_GITHUB_TOKEN`, oder von Hand veröffentlichen: `skynet-agent outbox link` gibt Links aus, die eine vorausgefüllte GitHub-Seite öffnen, auf der Sie nur einen Knopf drücken.

Damit die Issues lesbar bleiben, werden die Ergebnisse einer Aufgabe gemeinsam veröffentlicht: höchstens ein Kommentar pro Stunde, jeder mit mehreren Ergebnissen.

Ein veröffentlichtes Ergebnis sieht so aus und enthält nichts anderes:

```json
{"agent":"0.1.0","elapsed_s":41.2,"kernel":"exit-scam-a@1","platform":"linux-amd64-py3.12",
 "result":{"count":364838,"digest":"…","hits":0,"…":"…"},"result_sha256":"…","seq":1,
 "task":"exit-a-honest-check","unit":17,"units":256,"v":1}
```

## Befehle

| Befehl | Was er tut |
|---|---|
| `skynet-agent run` | Arbeitet bis zum Anhalten. `--once` erledigt ein Stück Arbeit und beendet sich |
| `skynet-agent status` | Version, Einstellungen, Zähler, wartende Ergebnisse, letztes Problem |
| `skynet-agent tasks` | Die aktuell veröffentlichten Aufgaben und was dieses Gerät erledigt hat |
| `skynet-agent pause` / `resume` | Keine neuen Aufgaben mehr annehmen / wieder annehmen |
| `skynet-agent stop` | Den laufenden Agenten bitten, sich zu beenden |
| `skynet-agent outbox` | Ergebnisse, die auf Veröffentlichung warten (`list`, `show`, `send`, `link`, `approve`, `drop`) |
| `skynet-agent config show` / `set SCHLÜSSEL WERT` | Einstellungen |
| `skynet-agent update` | Die neueste signierte Version jetzt installieren |
| `skynet-agent selftest [--online]` | Gerät, installierte Dateien und Signaturen prüfen |
| `skynet-agent autostart enable` / `disable` | Beim Anmelden starten oder nicht |
| `skynet-agent uninstall --yes` | Autostart ausschalten und anhalten; danach den Ordner des Agenten löschen |

## Einstellungen

| Einstellung | Standard | Bedeutung |
|---|---|---|
| `workers` | 1 | Gleichzeitig laufende Aufgaben; jede nutzt etwa einen CPU-Kern |
| `run_on_battery` | false | Im Akkubetrieb arbeiten |
| `poll_minutes` | 30 | Wie oft ins Repository geschaut wird |
| `update` | auto | `auto` installiert signierte Updates, `notify` meldet sie nur, `off` ignoriert sie. Eine von den Betreuern angeordnete Pause gilt in jedem Modus |
| `submit` | auto | `auto` veröffentlicht Ergebnisse, `manual` behält sie im Postausgang |
| `max_task_minutes` | 120 | Wie lange ein Stück Arbeit höchstens dauern darf |
| `batch_minutes` | 60 | Ergebnisse einer Aufgabe werden gemeinsam veröffentlicht, höchstens ein Kommentar in so vielen Minuten |
| `max_submissions_per_day` | 48 | Höchstzahl der pro Tag von diesem Gerät veröffentlichten Kommentare |
| `report_platform` | true | Den Ergebnissen eine grobe Kennung wie `windows-amd64-py3.12` beifügen |
| `ai.enabled` | false | Optionaler KI-Modus, siehe unten |

Beispiel: `skynet-agent config set workers 4`.

## Optional: Forschungsfragen mit dem eigenen lokalen KI-Modell beantworten

Wenn Sie auf Ihrem Computer ein offenes Modell betreiben (zum Beispiel mit Ollama, dem llama.cpp-Server oder LM Studio), kann der Agent ihm Forschungsfragen aus der Aufgabenliste übergeben und die Antworten veröffentlichen. Das ist standardmäßig aus und experimentell.

```sh
skynet-agent ai                               # zeigt den lokalen Server und das Modell, das er verwenden würde
skynet-agent config set ai.enabled true
```

- Der Agent lädt kein Modell herunter und startet keines. Er spricht nur mit einem Server auf Ihrem eigenen Computer, außer Sie setzen `ai.allow_remote`.
- Die Frage und die Dokumente, die sie zitiert, stammen aus der signierten Aufgabenliste; jedes Dokument wird gegen seinen Hash geprüft, bevor das Modell es sieht.
- Jede Antwort wartet im Postausgang, bis Sie sie ansehen: `skynet-agent outbox show NAME`, dann `skynet-agent outbox approve NAME`. Zum Veröffentlichen ohne Durchsicht: `skynet-agent config set ai.review_before_submit false`.
- Antworten werden als maschinell erzeugt und ungeprüft veröffentlicht.

## Sicherheit, ehrlich gesagt

- **Updates und Aufgabenlisten sind signiert** (Ed25519). Der Agent nimmt sie nur an, wenn die Signatur zu einem Release-Schlüssel passt, der in der installierten Kopie eingebaut ist, die Versionsnummer höher ist als die aktuelle und jede Datei zu ihrem SHA-256 passt. Ein Spiegel oder eine schlechte Verbindung ändern daran nichts.
- **Aufgaben sind Daten, keine Programme.** Neue Arten von Berechnungen kommen nur innerhalb einer signierten Version, als lesbarer Python-Quelltext in [`skynet_agent/kernels`](../../agent/skynet_agent/kernels).
- **Der Agent läuft im isolierten Modus von Python**, und jedes Stück Arbeit läuft in einem eigenen Prozess mit niedriger Priorität und Zeitlimit.
- **Startet eine neue Version nicht**, kehrt der Starter zur vorherigen zurück und merkt sich, diese Version nicht noch einmal zu installieren.
- **Worauf Sie vertrauen müssen.** Wer den Release-Schlüssel besitzt, kann Code an jeden installierten Agenten ausliefern. In dieser Forschungsphase liegt der Schlüssel bei den Betreuern des Projekts. Wenn Sie keine automatischen Updates wollen, führen Sie `skynet-agent config set update notify` aus und aktualisieren Sie von Hand, nachdem Sie die Änderungen gelesen haben. Die allererste Installation vertraut der HTTPS-Verbindung zu GitHub. Im SkyNet-Netz darf es einen solchen Schlüssel gar nicht geben; dieser Agent ist ein Forschungswerkzeug und erfüllt die Anforderungen von SkyNet selbst noch nicht. Einzelheiten und Bedrohungstabelle: [docs/RESEARCH_AGENT.md](../../docs/RESEARCH_AGENT.md) (auf Russisch).

## Privatsphäre

Der Agent kontaktiert nur GitHub: Er lädt öffentliche Dateien dieses Repositorys herunter (GitHub sieht Ihre IP-Adresse wie bei jedem Besuch) und veröffentlicht, wenn Sie angemeldet sind, Ergebnisse unter Ihrem Konto. Ein Ergebnis enthält den Namen der Aufgabe, die Nummer des Stücks, die berechneten Zahlen, die Dauer und, sofern Sie `report_platform` nicht ausschalten, eine grobe Plattformkennung. Über Ihre Dateien, Ihr Netzwerk oder Ihre Hardware wird nichts erfasst.

## Was es Sie kostet

Den Strom für standardmäßig einen ausgelasteten CPU-Kern, bei niedrigster Priorität, sodass andere Programme nicht gebremst werden. Auf einem Telefon wird der Akku nicht genutzt, außer Sie erlauben es; lassen Sie das Telefon am Ladegerät.

## Entfernen

```sh
skynet-agent uninstall --yes
```

Löschen Sie danach den Ordner des Agenten. Sonst wurde auf Ihrem Computer nichts verändert.

## Wenn etwas nicht klappt

- **„no valid signature from a trusted release key“**: Die heruntergeladene Datei ist nicht das, was die Betreuer signiert haben. Der Agent lehnt sie ab und arbeitet mit dem weiter, was er hat. Wiederholt sich das tagelang, sehen Sie in die Issues des Repositorys.
- **`CERTIFICATE_VERIFY_FAILED` unter macOS** mit Python von python.org: Der Agent versucht es dann selbst mit der Zertifikatsdatei des Systems. Bleibt der Fehler, führen Sie das mitgelieferte `Install Certificates.command` aus.
- **Python aus dem Microsoft Store (Windows)** arbeitet mit einer eigenen Kopie von `AppData` und der Registry. Der Ordner des Agenten ist dann `SkyNetAgent` in Ihrem Profilordner, und der Autostart muss von Hand eingerichtet werden: `skynet-agent autostart enable` zeigt, wie. Auf einem echten Gerät noch nicht überprüft.
- **Ergebnisse bleiben im Postausgang**: Führen Sie `skynet-agent github` aus; meist fehlt `gh auth login`.
- **Android beendet den Agenten im Hintergrund**: Führen Sie in Termux `termux-wake-lock` aus und nehmen Sie Termux von der Akkuoptimierung aus.

## Was bisher getestet ist

Die Testsuite ([`tests/`](../../agent/tests)) deckt Signaturen, Updates, Rückfall, Aufgaben, Veröffentlichung und einen Durchlauf von Anfang bis Ende ab und wird bei jeder Änderung automatisch unter Windows, Linux und macOS ausgeführt (Reiter „Actions“ des Repositorys). Von Hand geprüft wurde unter Windows 11. Noch nicht auf einem echten Gerät geprüft: Android (Termux) sowie der Autostart unter macOS, Linux und Android. Wenn bei Ihnen etwas nicht funktioniert, eröffnen Sie bitte ein Issue.

## Lizenz

Der Code des Agenten steht unter der [MIT-Lizenz](../../agent/LICENSE).
