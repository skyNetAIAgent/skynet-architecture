# Linux installer

**English** · [中文](../../i18n/zh/LINUX_INSTALLER.md) · [Español](../../i18n/es/LINUX_INSTALLER.md) · [Français](../../i18n/fr/LINUX_INSTALLER.md) · [Deutsch](../../i18n/de/LINUX_INSTALLER.md) · [Italiano](../../i18n/it/LINUX_INSTALLER.md) · [Русский](../../i18n/ru/LINUX_INSTALLER.md) · [Português](../../i18n/pt/LINUX_INSTALLER.md) · [العربية](../../i18n/ar/LINUX_INSTALLER.md)

Run the single file from the project's Releases page under your own account.

```sh
sh skynet-agent-install.sh
```

The file carries the signed agent release. Installation verifies its Ed25519 signature and file hashes offline. If Python 3.9+ is on your PATH, setup uses that interpreter. Otherwise it needs a pinned glibc build of CPython for x86_64 or aarch64. **Both hashes are currently pending. This build requires system Python.**

The online installer uses the same setup procedure. With a verified pin it can fetch the matching runtime from python-build-standalone and check SHA-256 before extraction. Portable interpreters live under `$XDG_DATA_HOME/skynet-agent/python/<sha256>`, normally `~/.local/share/skynet-agent/python/<sha256>`. The command in `~/.local/bin` and the systemd user service use the selected executable.

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

## Start and remove

In a terminal, Enter at the first prompt starts the service now and at sign-in. Enter at the second keeps it tied to login sessions. Without a terminal, setup skips the prompts. These commands make the choices explicitly.

```sh
sh skynet-agent-install.sh --autostart           # Run now and at sign-in
sh skynet-agent-install.sh --autostart --linger  # Also run before login and after logout
sh skynet-agent-install.sh --no-autostart        # Install for manual use
```

The service needs a running systemd user manager. The signed 0.2.2 service writer supports paths with spaces. Setup asks for manual start if an interpreter or agent path contains a double quote, backslash, dollar sign, percent sign or line break. If local policy denies lingering, setup reports it and the service still runs during login sessions. Account-wide lingering can be changed separately with `loginctl disable-linger "$(id -un)"`. For a manual installation, start work with `~/.local/bin/skynet-agent run`.

```sh
~/.local/bin/skynet-agent selftest
~/.local/bin/skynet-agent version
~/.local/bin/skynet-agent uninstall --yes
```

Removal turns off the service, requests a stop and waits for the agent lock. Your identity key, outbox, pending relay records and settings stay in the agent directory for reinstallation. To erase the agent's saved data as well, use `uninstall --yes --purge`. Lingering is a setting for the whole account and persists across removal.

## Build and verify

From the repository root, use Python 3.9+ on the build machine.

```sh
sh installer/linux/build.sh
shellcheck -s sh agent/install.sh installer/linux/build.sh installer/linux/smoke.sh
dash -n installer/linux/skynet-agent-install.sh
python3 -I -m unittest discover -s agent/tests -t agent/tests
```

The builder authenticates the release with the public key in `agent/install.py` and produces `installer/linux/skynet-agent-install.sh`. To enable portable Python, verify each upstream archive independently and record its SHA-256 in `python.lock` (one field per line). For a null entry only, CI can supply a verified digest through `SKYNET_PYTHON_SHA256_X86_64` or `SKYNET_PYTHON_SHA256_AARCH64`. These are build-time settings. The builder verifies and embeds each pinned archive. To build offline with pins, use `sh installer/linux/build.sh --runtime-dir /path/to/archives`.

The Linux installer workflow runs the bundle as an unprivileged user with networking disabled. Ubuntu 24.04 exercises system Python. Debian 12 slim exercises the portable interpreter when the x86_64 digest is available, and checks the refusal when it is pending. Successful installations run the self-test, report the version and exercise both removal modes. The workflow uploads the script as a build artifact for manual distribution.
