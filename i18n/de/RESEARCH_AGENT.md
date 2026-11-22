<!-- translation of docs/RESEARCH_AGENT.md, source sha256: be3193497fd35b1568b634f7647119965e68e6e665fea52b5a8ecb8aa477aa9e -->

# Programm-Agent: Wie man dem Projekt ohne KI-Assistenten hilft

[English](../../docs/RESEARCH_AGENT.en.md) · [中文](../zh/RESEARCH_AGENT.md) · [Español](../es/RESEARCH_AGENT.md) · [Français](../fr/RESEARCH_AGENT.md) · **Deutsch** · [Italiano](../it/RESEARCH_AGENT.md) · [Русский](../../docs/RESEARCH_AGENT.md) · [Português](../pt/RESEARCH_AGENT.md) · [العربية](../ar/RESEARCH_AGENT.md)

Stand: 22. November 2026. Version des Agenten 0.1.0. Anleitung für den Teilnehmer:
[agent/README.md](../../agent/README.md) ([auf Russisch](../ru/AGENT.md)).

## Wozu

Das Repository richtet sich an Menschen, die einen KI-Assistenten haben: Er liest Dokumente und hilft
beim Entwerfen. Die meisten Menschen haben keinen solchen Assistenten, aber einen Computer oder ein Telefon.
Der Programm-Agent gibt ihnen eine Möglichkeit mitzumachen: Er schaut regelmäßig in dieses Repository,
nimmt Aufgaben, führt sie auf dem Gerät des Teilnehmers aus und veröffentlicht die Ergebnisse.

In dieser Phase **gibt es keine Belohnungen**: keine Credits, kein Geld und keine Versprechen künftiger
Gutschriften. Das Ziel ist, zum Entwurf der Architektur möglichst viele Rechenressourcen
und unabhängige Prüfer heranzuziehen.

Der Agent ist **ein Forschungswerkzeug, nicht das SkyNet-Netz**. Er ist einfacher und zentralisierter
aufgebaut, als das Netz sein muss, und erfüllt dessen verbindliche Anforderungen selbst nicht.
Weiter unten wird das an jeder Stelle offen gesagt.

## Wie es aufgebaut ist

| Teil | Wo es liegt | Was es tut |
|---|---|---|
| Aufgabenliste | `tasks/index.json` und die Signatur `tasks/index.json.sig` | Nennt die eingebaute Berechnung, ihre Parameter und die Zahl der unabhängigen Stücke |
| Agent | `agent/skynet_agent/`, nur die Standardbibliothek von Python 3.9+ | Prüft Signaturen, wählt ein Stück, rechnet, veröffentlicht, aktualisiert sich |
| Versionsbeschreibung | `agent/release.json` und die Signatur | Listet die Dateien des Agenten mit Größe und SHA-256 auf |
| Starter | `agent/launcher.py` | Startet die aktuelle Version, wechselt auf eine neue, kehrt von einer kaputten zurück |
| Ergebnisse | Kommentare im GitHub-Issue der Aufgabe im Namen des Teilnehmers | Maschinenlesbarer Eintrag mit dem Fingerabdruck des Ergebnisses |
| Zusammenfassung | `results/`, erstellt von `tools/collect_results.py` | Gleicht die Ergebnisse verschiedener Menschen ab und prüft Funde erneut |

Ein Arbeitszyklus des Agenten:

1. Alle 30 Minuten (mit Streuung) lädt er die Versionsbeschreibung und die Aufgabenliste herunter.
2. Er prüft die Signatur jeder der beiden mit dem Release-Schlüssel, der in die installierte Kopie eingebaut ist.
3. Gibt es eine Version mit höherer Nummer, lädt er deren Dateien herunter, gleicht jede mit dem Fingerabdruck ab,
   legt sie neben die aktuelle und startet sich neu.
4. Er wählt ein zufälliges Stück einer Aufgabe, das er noch nicht gerechnet hat.
5. Er rechnet es in einem eigenen Prozess mit niedrigster Priorität und Zeitlimit.
6. Er legt das Ergebnis in den «Postausgang» und veröffentlicht es als Kommentar im GitHub-Issue. Die Ergebnisse einer
   Aufgabe werden gemeinsam veröffentlicht, höchstens ein Kommentar pro Stunde, um das Issue
   und seine Abonnenten nicht mit Benachrichtigungen zu überfluten. Nach einem fehlgeschlagenen Versuch wird der nächste
   aufgeschoben: um eine Minute, dann doppelt so lange, aber höchstens eine Stunde. Kann nicht veröffentlicht werden
   (keine GitHub-Anmeldung), hört der Agent nach dreihundert unveröffentlichten Ergebnissen auf, Arbeit anzunehmen,
   und meldet das.

Es gibt keinen Planer: Jeder Agent wählt sein Stück selbst. Dass sich Stücke bei verschiedenen Teilnehmern
überschneiden, ist beabsichtigt: Alle Rechenaufgaben sind ganzzahlig, daher ergeben sich auf jedem Gerät
dieselben Ziffern, und ein Stück gilt als bestätigt, wenn denselben Fingerabdruck
so viele verschiedene Konten veröffentlicht haben, wie die Aufgabe verlangt.

## Eine Aufgabe sind Daten, kein Programm

Der Agent lädt niemals Code aus einer Aufgabe herunter und führt ihn auch nicht aus. Eine Aufgabe nennt eines der
in den Agenten eingebauten Berechnungen („Kern“) und übergibt ihr Zahlen. Jeder Kern prüft die
Parameter und begrenzt den Arbeitsumfang. Eine neue Art von Berechnung erscheint nur mit einer neuen
signierten Version des Agenten, deren Quelltext im Repository liegt und von Menschen gelesen werden kann.

Die Kerne der Version 0.1:

| Kern | Was er rechnet |
|---|---|
| `selftest` | Eine ganzzahlige Kontrollrechnung: Der Fingerabdruck muss auf allen Geräten übereinstimmen |
| `exit-scam-a` | Die exakte Auszahlungserwartung eines Teilnehmers, der vor seinem Abgang Fälschungen abgibt (Variante A aus [CURRENT_DESIGN](CURRENT_DESIGN.md)); geht eine Familie von Strategien durch und meldet die, die vorteilhafter sind als ein ehrlicher Abgang |
| `lottery-b` | Die exakte Wahrscheinlichkeit eines verlustreichen Monats oder Quartals, wenn nur für geprüfte Aufgaben gezahlt wird (Variante B) |
| `ai-answer` | Auf Wunsch des Teilnehmers: eine Frage an ein lokales KI-Modell, das er selbst betreibt |

Das genaue Modell jeder Berechnung steht am Anfang der Quelldatei des Kerns, damit jeder das Ergebnis
unabhängig nachrechnen kann. Die Aufgaben und ihre Bedeutung: [tasks/README.md](../../tasks/README.md).

**Grenze zur Projektregel über Experimente.** Die ersten Aufgaben sind Berechnungen nach Formeln
aus den Dokumenten (Kostenanalyse und Suche nach Gegenbeispielen) sowie Fragen an Sprachmodelle.
Das sind keine Messungen an Geräten und keine Experimente mit dem Netz. Messaufgaben (zum Beispiel,
ob die Bits einer ganzzahligen Ausgabe auf verschiedenen Grafikkarten übereinstimmen) werden erst veröffentlicht,
nachdem der Eigentümer des Projekts entschieden hat, Experimente zuzulassen.

## KI-Modus (optional, experimentell)

Ein Teilnehmer, der bei sich ein offenes Modell betreibt (Ollama, llama.cpp-Server, LM Studio
und Ähnliches mit einer zu OpenAI kompatiblen Schnittstelle), kann `ai.enabled` einschalten. Dann übergibt der Agent
dem Modell Fragen aus der signierten Liste und veröffentlicht die Antworten. So werden Menschen ohne KI-Abonnement,
aber mit Grafikkarte zu Teilnehmern des „Modellrats“.

- Der Agent lädt kein Modell herunter und startet keines und wendet sich standardmäßig nur an einen Server
  auf demselben Computer.
- Die Frage und die Dokumente, die sie zitiert, sind durch die signierte Liste vorgegeben. Jedes Dokument
  wird gegen seinen Fingerabdruck geprüft, daher kann dem Modell kein anderer Text untergeschoben werden.
- Die Antwort wartet standardmäßig im «Postausgang», bis der Teilnehmer sie genehmigt: Der Text wird
  in seinem Namen veröffentlicht.
- Die Antwort wird als maschinell erzeugt und von niemandem geprüft gekennzeichnet. Die Zahl der Antworten
  pro Frage ist begrenzt.

Geprüft wurde das nur auf einem vorgetäuschten Server in automatischen Tests. Mit echten Umgebungen
zum Betreiben von Modellen wurde der Modus noch nicht geprüft.

## Android-App (experimentell)

Für die, die Termux nicht einrichten wollen, gibt es eine App: eine APK-Datei, eine Taste „Start“.
Quelltext und Anleitung: [android/README.md](ANDROID.md). In die App ist dasselbe
Paket `skynet_agent` und Python (über Chaquopy) eingebaut. Unterschiede zum Agenten auf dem Computer:

- Android erlaubt keine eigenen Python-Prozesse, daher wird das Stück im Hintergrundprozess
  der App selbst gerechnet, eines nach dem anderen. Dauert ein Stück länger als das Limit, beendet der Wächter
  diesen Prozess, Android startet den Dienst erneut, und die Aufgabe bleibt schnelleren Geräten überlassen.
- Eine neue Version des Agenten wird aus dem Repository mit derselben Signatur des Release-Schlüssels geholt. Geprüft
  wird sie von der eingebauten Kopie; startet die neue Version hier nicht oder sind ihre Dateien verändert, kehrt
  die App zur eingebauten zurück.
- Die App selbst (Bildschirm, Dienst, Wächter) ändert sich nur durch eine neue APK. Die APK ist mit einem eigenen
  Schlüssel der Betreuer des Projekts signiert: Das ist ein zweiter einzelner Vertrauenspunkt, den es im Netz nicht geben darf.
- Ergebnisse werden mit einem GitHub-Token veröffentlicht, den der Teilnehmer in die App einfügt.
- Die App arbeitet nur am Ladegerät, sofern der Teilnehmer nichts anderes erlaubt hat. Einen KI-Modus gibt es nicht.

Stand: 22. November 2026: Die App lässt sich bauen, ihr Python-Teil besteht die Tests auf dem
Computer (`agent/tests/test_android_glue.py`). Ein Prüfbuild mit Testschlüssel lief auf dem Emulator
Android 14 (x86_64) mit lokalem Testrepository durch: Installation, Prüfung der Signaturen,
Berechnung aller 7 Teststücke ohne Fehler, Warten ohne Laden, Arbeit im Hintergrund, Speichern des Tokens
und dessen Verwendung gegenüber der echten GitHub-API, Anhalten und erneuter Start mit erhaltenem Zustand.
Auf einem echten Telefon lief die App noch nicht, der Build für ARM (`arm64-v8a`) wurde nicht geprüft. Über Google Play
wird sie nicht vertrieben: Dessen Regeln verbieten Apps, die ausführbaren Code laden.

## Worauf der Agent vertraut

| Was | Vertrauen |
|---|---|
| Signatur mit dem Ed25519-Release-Schlüssel | Ja. Ohne sie wird weder eine Version noch eine Aufgabenliste angenommen |
| Kanal (HTTPS, Spiegel, GitHub selbst) | Nein für die Integrität: Eine vertauschte Datei bricht die Signatur oder den Fingerabdruck |
| Inhalt der Aufgabe | Nein: Parameter werden geprüft, der Arbeitsumfang ist begrenzt, in der Aufgabe ist kein Code |
| Antwort des lokalen Modells | Nein: Das ist Text, er wird als ungeprüft veröffentlicht |
| Erste Installation | Ja, dem HTTPS-Kanal zu GitHub. Das Installierte lässt sich mit dem Befehl `selftest --online` prüfen |

**Ehrliche Grenze.** Wer den Release-Schlüssel besitzt, kann das Programm an alle installierten
Agenten ausliefern. Derzeit liegt der Schlüssel bei den Betreuern des Projekts. Das ist ein einzelner Vertrauenspunkt,
den es im SkyNet-Netz nicht geben darf: Im Zielprojekt wird das Programm nur auf eine Version aktualisiert,
deren Fingerabdruck durch Abstimmung der Teilnehmer im gemeinsamen Journal angenommen wurde, und die Signatur
mit irgendjemandes Schlüssel genügt nicht ([CURRENT_DESIGN, Abschnitt 8](CURRENT_DESIGN.md)). Ein Teilnehmer,
der dem Schlüssel nicht vertrauen möchte, setzt `update` auf `notify` und aktualisiert von Hand, nachdem er die
Änderungen gelesen hat.

## Bedrohungstabelle

| Bedrohung | Wodurch sie abgedeckt ist | Was bleibt |
|---|---|---|
| Kompromittierung des Repositorys oder eines Kontos mit Schreibrecht: Austausch des Agenten | Eine Version wird nur mit der Signatur eines Schlüssels angenommen, der nicht im Repository liegt | Abgedeckt, solange der Schlüssel nicht gestohlen ist |
| Austausch einer Datei unterwegs oder auf einem Spiegel | Signatur der Versionsbeschreibung und SHA-256 jeder Datei | Abgedeckt |
| Rückfall auf eine alte verwundbare Version | Die Versionsnummer muss höher sein als die aktuelle | Abgedeckt für installierte Agenten. Eine neue Installation nimmt, was im Repository liegt |
| Schädliche Aufgabe | Eine Aufgabe enthält keinen Code; der Kern prüft die Parameter und begrenzt den Arbeits- und Speicherumfang; es gibt ein Zeitlimit | Begrenzt: Eine signierte Aufgabe kann den Prozessor bis zum Zeitlimit belegen |
| Wiederholung einer alten signierten Aufgabenliste | Die Nummer der Liste muss mindestens so groß sein wie die bereits gesehene; die Liste kann ein Ablaufdatum haben | Begrenzt: Eine frische Installation kann eine alte Liste erhalten und bereits geschlossene Aufgaben umsonst rechnen |
| Kaputte Version | Der Starter kehrt nach drei schnellen Abstürzen zur vorherigen Version zurück oder wenn die Dateien der neuen Version fehlen, und merkt sich die unbrauchbare Nummer. Wiederholte Neustartanforderungen führt er mit wachsender Pause aus | Abgedeckt für Abstürze beim Start. Einen stillen Rechenfehler fängt der Abgleich der Ergebnisse |
| Diebstahl des Release-Schlüssels | Der Schlüssel liegt außerhalb des Repositorys, unter Windows verschlüsselt für das Konto des Eigentümers | **Offen.** Ein Dieb kann eine schädliche Version herausgeben. Der Schlüsselwechsel erfolgt durch eine mit dem alten Schlüssel signierte neue Version, und auch sie ist dem Dieb zugänglich |
| Verlust des Release-Schlüssels | Eine Sicherungskopie liegt beim Eigentümer | Ohne Schlüssel lassen sich installierte Agenten nicht aktualisieren: Die Teilnehmer müssen den Agenten neu installieren |
| Gefälschtes Ergebnis | Die ganzzahlige Berechnung wird zwischen verschiedenen Konten abgeglichen; Funde werden beim Einsammeln nachgerechnet | Begrenzt: Eine Person mit zwei Konten „bestätigt“ sich selbst. Es gibt keine Belohnungen, daher bringt es keinen Nutzen, aber ein Schädling ist möglich. Die Betreuer rechnen stichprobenartig nach |
| Strom von Müllkommentaren fremder Konten | Der Sammler nimmt nur Einträge mit korrektem Fingerabdruck und bekannter Aufgabe an | Begrenzt durch die Mittel von GitHub |
| Leck eines GitHub-Tokens | Der Agent speichert das Token nicht, holt es von `gh` oder aus einer Variable und sendet es nirgendwohin außer zu GitHub über HTTPS, ohne Weiterleitungen | Ein Token mit Schreibrecht auf öffentliche Repositories bleibt in der Verantwortung des Teilnehmers |
| Fremder Code neben dem Agenten (untergeschobenes Modul im aktuellen Ordner) | Isolierter Modus von Python (`-I`) | Abgedeckt. Gegen ein Programm mit den Rechten desselben Benutzers auf demselben Computer gibt es keinen Schutz |
| Ressourcenverbrauch des Teilnehmers | Standardmäßig ein Prozess, niedrigste Priorität, Pause im Akkubetrieb, Zeitlimit, die Befehle `pause` und `stop` | Die Teilnehmenden tragen die Stromkosten selbst |
| Stopp aller Agenten durch die Betreuer | Eine signierte Markierung `halt` in der Versionsbeschreibung; sie wirkt auch bei ausgeschalteten Updates | Das ist ein bewusster Hebel: nur ein Stopp, ohne etwas zu starten |

## Was der Agent über sich mitteilt

Nur der Inhalt des veröffentlichten Eintrags: der Name der Aufgabe, die Nummer des Stücks, die Zahlen des Ergebnisses,
die Rechenzeit und, sofern nicht abgeschaltet, eine grobe Plattformkennung der Form `linux-amd64-py3.12`.
Anfragen gehen nur an GitHub. Angaben über die Dateien, das Netz und die Geräte des Teilnehmers werden nicht erfasst.

## Vorgehen für die Betreuer

Der Release-Schlüssel wird einmal erzeugt und außerhalb des Repositorys aufbewahrt:

```
python tools/keytool.py generate
```

Eine Sicherungskopie des Geheimnisses macht der Eigentümer selbst, von Hand, mit dem Befehl
`python tools/keytool.py backup`, und bewahrt sie außerhalb des Computers auf. Das Geheimnis darf Assistenten
nicht gezeigt und nicht in Chats und Dateien eingefügt werden.

Neue Version des Agenten:

```
python tools/make_release.py --seq <nächste Nummer> --version <x.y.z>
```

dann das Hochladen der geänderten Dateien `agent/` ins Repository. Neue Aufgabenliste:

```
python tools/sign_tasks.py
```

dann das Hochladen von `tasks/index.json` und `tasks/index.json.sig`. Einsammeln der Ergebnisse:

```
python tools/collect_results.py
```

Die Arbeit aller Agenten bis zur Fehlerbehebung stoppen: eine Versionsbeschreibung mit
`--halt-through <Nummer>` und einer Begründung herausgeben.

## Was hier fehlt und warum es ehrlich ist, das zu sagen

- **Das ist kein verteiltes Netz.** Aufgaben und Versionen verteilt ein einziges Repository, signiert ein einziger
  Schlüssel, Ergebnisse nimmt eine einzige Plattform an. Die Anforderungen R1–R4 aus
  den [verbindlichen Anforderungen](../ru/REQUIREMENTS.md) werden auf den Agenten nicht angewandt
  und von ihm nicht erfüllt.
- **Ein GitHub-Konto ist nötig.** Ohne es werden Ergebnisse nur von Hand über einen Link veröffentlicht.
- **Es gibt keinen Schutz vor vielen Konten.** Für die unentgeltliche Phase ist das annehmbar.
- **Android ist auf einem echten Gerät nicht geprüft**; der Autostart unter macOS, Linux und Android
  ist nur auf der Ebene der erzeugten Dateien geprüft. Zwei Fälle sind nach der Dokumentation berücksichtigt
  und ebenfalls nicht auf echten Geräten geprüft: Python aus dem Microsoft Store unter Windows (es sieht
  eine eigene Kopie von `AppData` und der Registry, daher liegt der Ordner des Agenten im Profil, und der Autostart
  wird von Hand hinzugefügt) und Python von python.org unter macOS ohne installierte Zertifikate
  (der Agent wiederholt die Anfrage mit der Systemzertifikatsdatei).
- **Die ersten Aufgaben sind leicht.** Die gesamte erste Charge (702 Stücke) brauchte auf einem einzelnen
  Desktop-Computer 15,5 Stunden Prozessorzeit bei 16 gleichzeitigen Prozessen mit niedrigster
  Priorität, also etwa eine Stunde nach der Uhr [gemessen auf einem PC, 22. November 2026].
  Der Mechanismus ist bereit, schwere Aufgaben anzunehmen. Was dabei herauskam: [results/FIRST_RUN.md](../../results/FIRST_RUN.md).

## Wie es weitergeht

1. Messaufgaben auf verschiedenen Geräten: die größte Unbekannte des Projekts ist die bitgenaue
   Übereinstimmung des Ergebnisses auf verschiedenen Grafikkarten. Das sind Experimente, sie warten
   auf die Entscheidung des Eigentümers.
2. Verzicht auf das GitHub-Konto: Annahme der Ergebnisse über mehrere unabhängige öffentliche
   Plattformen, wie im Zielprojekt des Netzes.
3. Verzicht auf den einzelnen Schlüssel: mehrere unabhängige Signaturen, dann die Annahme von Versionen
   nach den Regeln des Netzes selbst.
4. Verwaltung des lokalen Modells: Herunterladen eines offenen Modells mit Prüfung des Fingerabdrucks,
   damit der KI-Modus mit einem Befehl eingeschaltet wird.
