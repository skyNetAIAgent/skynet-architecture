# Linux installer

**English** · [中文](../../i18n/zh/LINUX_INSTALLER.md) · [Español](../../i18n/es/LINUX_INSTALLER.md) · [Français](../../i18n/fr/LINUX_INSTALLER.md) · [Deutsch](../../i18n/de/LINUX_INSTALLER.md) · [Italiano](../../i18n/it/LINUX_INSTALLER.md) · [Русский](../../i18n/ru/LINUX_INSTALLER.md) · [Português](../../i18n/pt/LINUX_INSTALLER.md) · [العربية](../../i18n/ar/LINUX_INSTALLER.md)

The offline installer contains signed Go executables for amd64, arm64 and ARMv7. Run it as the desktop user. A fresh installation uses the per-user data directory and places the command in `~/.local/bin`.

~~~sh
sh skynet-agent-install.sh
~/.local/bin/skynet-agent verify-install
~~~

Use `--home DIR` for a custom profile. Setup starts the agent right away and registers it as a systemd user service, so it starts again after a reboot; it also tries to keep it running after logout (linger). Use `--no-autostart` to only install, or `--linger` to require linger. Removing the agent preserves the identity and queues. Adding `--purge` explicitly removes its saved data.

~~~sh
~/.local/bin/skynet-agent uninstall --yes
~~~

The online bootstrap at `agent/install.sh` uses curl, jq, xxd, sha256sum and OpenSSL with Ed25519 support. Obtain the script from a trusted release. It authenticates the manifest before executing the architecture-specific binary.

To build the offline installer from signed assets, run the following from the repository root. The manifest and signature belong in `agent/v2`. The builder verifies each asset before packing it.

~~~sh
sh installer/linux/build.sh --dir dist
~~~
