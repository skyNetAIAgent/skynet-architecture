<!-- translation of installer/linux/README.md, source sha256: 7ece3bc522f30a5f0b62b4a6580a177b3d4725e5b1eaa5513e255f0772f27156 -->

# Programma di installazione per Linux

[English](../../installer/linux/README.md) · [中文](../zh/LINUX_INSTALLER.md) · [Español](../es/LINUX_INSTALLER.md) · [Français](../fr/LINUX_INSTALLER.md) · [Deutsch](../de/LINUX_INSTALLER.md) · **Italiano** · [Русский](../ru/LINUX_INSTALLER.md) · [Português](../pt/LINUX_INSTALLER.md) · [العربية](../ar/LINUX_INSTALLER.md)

Il programma di installazione offline contiene eseguibili Go firmati per amd64, arm64 e ARMv7. Eseguitelo come utente desktop. Una nuova installazione usa la directory dati per utente e colloca il comando in `~/.local/bin`.

~~~sh
sh skynet-agent-install.sh --no-autostart
~/.local/bin/skynet-agent verify-install
~~~

Usate `--home DIR` per un profilo personalizzato. Il programma di installazione conserva l'avvio all'accesso per impostazione predefinita. Usate `--autostart` per avviare subito il servizio utente systemd e all'accesso, oppure aggiungete `--linger` per mantenerlo in esecuzione al di fuori delle sessioni di accesso. La rimozione dell'agente conserva l'identità e le code. L'aggiunta di `--purge` rimuove esplicitamente i suoi dati salvati.

~~~sh
~/.local/bin/skynet-agent uninstall --yes
~~~

Il bootstrap online in `agent/install.sh` usa curl, jq, xxd, sha256sum e OpenSSL con supporto Ed25519. Ottenete lo script da una release attendibile. Autentica il manifest prima di eseguire il binario specifico per l'architettura.

Per compilare il programma di installazione offline dagli asset firmati, eseguite quanto segue dalla radice del repository. Il manifest e la firma risiedono in `agent/v2`. Lo strumento di compilazione verifica ogni asset prima di includerlo nel pacchetto.

~~~sh
sh installer/linux/build.sh --dir dist
~~~
