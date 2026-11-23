<!-- translation of installer/linux/README.md, source sha256: abf22229c4680552dec4357a2de39a59a6c18c9238e2ff76b46a2952e7d8f0b0 -->

# Linux-Installationsprogramm

[English](../../installer/linux/README.md) · [中文](../zh/LINUX_INSTALLER.md) · [Español](../es/LINUX_INSTALLER.md) · [Français](../fr/LINUX_INSTALLER.md) · **Deutsch** · [Italiano](../it/LINUX_INSTALLER.md) · [Русский](../ru/LINUX_INSTALLER.md) · [Português](../pt/LINUX_INSTALLER.md) · [العربية](../ar/LINUX_INSTALLER.md)

Führen Sie die einzelne Datei von der Seite Releases des Projekts unter Ihrem eigenen Benutzerkonto aus.

```sh
sh skynet-agent-install.sh
```

Die Datei enthält die signierte Version des Agenten. Die Installation prüft ihre Ed25519-Signatur und die Datei-Hashes offline. Wenn Python 3.9 oder neuer im PATH liegt, verwendet die Einrichtung diesen Interpreter. Andernfalls braucht sie eine festgeschriebene CPython-Compilierung mit glibc für x86_64 oder aarch64. **Beide Hashes stehen derzeit noch aus. Dieser Build benötigt das System-Python.**

Das Online-Installationsprogramm verwendet dasselbe Verfahren zur Einrichtung. Mit einer geprüften Festlegung kann es die passende Laufzeitumgebung von python-build-standalone herunterladen und vor dem Entpacken die SHA-256-Prüfsumme kontrollieren. Portable Interpreter liegen unter `$XDG_DATA_HOME/skynet-agent/python/<sha256>`, normalerweise `~/.local/share/skynet-agent/python/<sha256>`. Der Befehl in `~/.local/bin` und der systemd-Dienst des Benutzers verwenden die ausgewählte ausführbare Datei.

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

## Starten und Entfernen

In einem Terminal startet die Eingabetaste bei der ersten Frage den Dienst sofort und bei der Anmeldung. Bei der zweiten Frage bleibt er an die Anmeldesitzungen gebunden. Ohne Terminal überspringt die Einrichtung die Fragen. Diese Befehle legen die Auswahl ausdrücklich fest.

```sh
sh skynet-agent-install.sh --autostart           # Run now and at sign-in
sh skynet-agent-install.sh --autostart --linger  # Also run before login and after logout
sh skynet-agent-install.sh --no-autostart        # Install for manual use
```

Der Dienst braucht einen laufenden systemd-Benutzermanager. Das signierte Programm zum Anlegen des Dienstes in Version 0.2.2 unterstützt Pfade mit Leerzeichen. Die Einrichtung verlangt einen manuellen Start, wenn ein Pfad zum Interpreter oder zum Agenten ein doppeltes Anführungszeichen, einen Backslash, ein Dollarzeichen, ein Prozentzeichen oder einen Zeilenumbruch enthält. Wenn die lokale Richtlinie den Dauerbetrieb nicht zulässt, meldet die Einrichtung das, und der Dienst läuft trotzdem während der Anmeldesitzungen. Der Dauerbetrieb für das ganze Konto lässt sich getrennt mit `loginctl disable-linger "$(id -un)"` ändern. Bei einer manuellen Installation beginnen Sie die Arbeit mit `~/.local/bin/skynet-agent run`.

```sh
~/.local/bin/skynet-agent selftest
~/.local/bin/skynet-agent version
~/.local/bin/skynet-agent uninstall --yes
```

Beim Entfernen wird der Dienst ausgeschaltet, ein Stopp angefordert und auf die Sperre des Agenten gewartet. Ihr Identitätsschlüssel, der Postausgang, wartende Relay-Datensätze und die Einstellungen bleiben für eine Neuinstallation im Ordner des Agenten. Um auch die gespeicherten Daten des Agenten zu löschen, verwenden Sie `uninstall --yes --purge`. Der Dauerbetrieb ist eine Einstellung für das ganze Konto und bleibt nach dem Entfernen bestehen.

## Bauen und Prüfen

Verwenden Sie im Hauptordner des Repositorys Python 3.9 oder neuer auf dem Rechner, auf dem gebaut wird.

```sh
sh installer/linux/build.sh
shellcheck -s sh agent/install.sh installer/linux/build.sh installer/linux/smoke.sh
dash -n installer/linux/skynet-agent-install.sh
python3 -I -m unittest discover -s agent/tests -t agent/tests
```

Das Bauprogramm prüft die Echtheit der Version mit dem öffentlichen Schlüssel in `agent/install.py` und erzeugt `installer/linux/skynet-agent-install.sh`. Um portables Python zu ermöglichen, prüfen Sie jedes Upstream-Archiv unabhängig und tragen Sie seine SHA-256-Prüfsumme in `python.lock` ein (ein Feld pro Zeile). Nur für einen leeren Eintrag kann die CI eine geprüfte Prüfsumme über `SKYNET_PYTHON_SHA256_X86_64` oder `SKYNET_PYTHON_SHA256_AARCH64` liefern. Das sind Einstellungen für den Bau. Das Bauprogramm prüft jedes festgelegte Archiv und bettet es ein. Um mit festgelegten Archiven offline zu bauen, verwenden Sie `sh installer/linux/build.sh --runtime-dir /path/to/archives`.

Der Workflow des Linux-Installationsprogramms führt das Bündel als Benutzer ohne besondere Rechte mit abgeschaltetem Netzwerk aus. Ubuntu 24.04 erprobt das System-Python. Debian 12 slim erprobt den portablen Interpreter, wenn die x86_64-Prüfsumme verfügbar ist, und prüft die Ablehnung, wenn sie noch aussteht. Erfolgreiche Installationen führen den Selbsttest aus, melden die Version und erproben beide Arten des Entfernens. Der Workflow lädt das Skript als Build-Artefakt für die manuelle Verteilung hoch.
