<!-- translation of installer/linux/README.md, source sha256: 7ece3bc522f30a5f0b62b4a6580a177b3d4725e5b1eaa5513e255f0772f27156 -->

# Linux-Installationsprogramm

[English](../../installer/linux/README.md) · [中文](../zh/LINUX_INSTALLER.md) · [Español](../es/LINUX_INSTALLER.md) · [Français](../fr/LINUX_INSTALLER.md) · **Deutsch** · [Italiano](../it/LINUX_INSTALLER.md) · [Русский](../ru/LINUX_INSTALLER.md) · [Português](../pt/LINUX_INSTALLER.md) · [العربية](../ar/LINUX_INSTALLER.md)

Das Offline-Installationsprogramm enthält signierte Go-Programme für amd64, arm64 und ARMv7. Führen Sie es unter Ihrem Desktop-Benutzerkonto aus. Eine Neuinstallation verwendet das Datenverzeichnis des Benutzers und legt den Befehl in `~/.local/bin` ab.

~~~sh
sh skynet-agent-install.sh --no-autostart
~/.local/bin/skynet-agent verify-install
~~~

Verwenden Sie `--home DIR` für ein eigenes Profil. Die Einrichtung behält den Start bei der Anmeldung standardmäßig bei. Mit `--autostart` starten Sie den systemd-Benutzerdienst sofort und bei der Anmeldung, oder Sie fügen `--linger` hinzu, damit er auch außerhalb von Anmeldesitzungen weiterläuft. Beim Entfernen des Agenten bleiben die Identität und die Warteschlangen erhalten. Mit `--purge` werden seine gespeicherten Daten ausdrücklich gelöscht.

~~~sh
~/.local/bin/skynet-agent uninstall --yes
~~~

Das Online-Bootstrap-Skript unter `agent/install.sh` verwendet curl, jq, xxd, sha256sum und OpenSSL mit Ed25519-Unterstützung. Beziehen Sie das Skript aus einer vertrauenswürdigen Veröffentlichung. Es prüft die Echtheit des Manifests, bevor es die architekturspezifische Binärdatei ausführt.

Um das Offline-Installationsprogramm aus signierten Dateien zu bauen, führen Sie im Hauptordner des Repositorys Folgendes aus. Das Manifest und die Signatur gehören in `agent/v2`. Das Bauprogramm prüft jede Ressource, bevor es sie einbettet.

~~~sh
sh installer/linux/build.sh --dir dist
~~~
