# Windows desktop installer

**English** · [中文](../../i18n/zh/WINDOWS_INSTALLER.md) · [Español](../../i18n/es/WINDOWS_INSTALLER.md) · [Français](../../i18n/fr/WINDOWS_INSTALLER.md) · [Deutsch](../../i18n/de/WINDOWS_INSTALLER.md) · [Italiano](../../i18n/it/WINDOWS_INSTALLER.md) · [Русский](../../i18n/ru/WINDOWS_INSTALLER.md) · [Português](../../i18n/pt/WINDOWS_INSTALLER.md) · [العربية](../../i18n/ar/WINDOWS_INSTALLER.md)

Choose the amd64 or arm64 installer for your computer. Verify its SHA-256 using a checksum obtained through a trusted channel. Setup installs the signed native release in the current user’s profile. Login startup and immediate launch are optional. Start menu shortcuts invoke the permanent launcher.

The uninstaller keeps the identity, queues and release history by default. Select the data deletion option to remove them. During migration the previous signed Python bridge and its interpreter are kept for rollback.

## Build and test

Use Python 3.9+ and Inno Setup 6 on the build machine. Stage the release manifest and detached signature under `agent/v2` and its matching release binaries under `dist`. Use a fresh build directory. The smoke test needs a disposable Windows account.

~~~powershell
./installer/windows/build.ps1 -BuildDir build -AssetDir dist -Arch amd64
./installer/windows/smoke.ps1 -BuildDir build
~~~
