<!-- translation of installer/linux/README.md, source sha256: cabcf2237fcb61f3ccddb3e461306c5030f018a0db5353bfe00e7a5f55dd389f -->

# Linux-Installationsprogramm

[English](../../installer/linux/README.md) · [中文](../zh/LINUX_INSTALLER.md) · [Español](../es/LINUX_INSTALLER.md) · [Français](../fr/LINUX_INSTALLER.md) · **Deutsch** · [Italiano](../it/LINUX_INSTALLER.md) · [Русский](../ru/LINUX_INSTALLER.md) · [Português](../pt/LINUX_INSTALLER.md) · [العربية](../ar/LINUX_INSTALLER.md)

Das Offline-Installationsprogramm enthält signierte Go-Programme für amd64, arm64 und ARMv7. Führen Sie es unter Ihrem Desktop-Benutzerkonto aus. Eine Neuinstallation verwendet das Datenverzeichnis des Benutzers und legt den Befehl in `~/.local/bin` ab.

~~~sh
sh skynet-agent-install.sh
~/.local/bin/skynet-agent verify-install
~~~

Verwenden Sie `--home DIR` für ein eigenes Profil. Die Einrichtung startet den Agenten sofort und registriert ihn als systemd-Benutzerdienst, sodass er nach einem Neustart wieder startet; außerdem versucht sie, ihn nach dem Abmelden weiterlaufen zu lassen (Linger). Mit `--no-autostart` wird nur installiert, oder Sie verwenden `--linger`, damit Linger erforderlich ist. Beim Entfernen des Agenten bleiben die Identität und die Warteschlangen erhalten. Mit `--purge` werden seine gespeicherten Daten ausdrücklich gelöscht.

~~~sh
~/.local/bin/skynet-agent uninstall --yes
~~~

Das Online-Bootstrap-Skript unter `agent/install.sh` verwendet curl, jq, xxd, sha256sum und OpenSSL mit Ed25519-Unterstützung. Beziehen Sie das Skript aus einer vertrauenswürdigen Veröffentlichung. Es prüft die Echtheit des Manifests, bevor es die architekturspezifische Binärdatei ausführt.

Um das Offline-Installationsprogramm aus signierten Dateien zu bauen, führen Sie im Hauptordner des Repositorys Folgendes aus. Das Manifest und die Signatur gehören in `agent/v2`. Das Bauprogramm prüft jede Ressource, bevor es sie einbettet.

~~~sh
sh installer/linux/build.sh --dir dist
~~~
