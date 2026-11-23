# SkyNet research agent for Android (experimental)

**English** · [中文](../i18n/zh/ANDROID.md) · [Español](../i18n/es/ANDROID.md) · [Français](../i18n/fr/ANDROID.md) · [Deutsch](../i18n/de/ANDROID.md) · [Italiano](../i18n/it/ANDROID.md) · [Русский](../i18n/ru/ANDROID.md) · [Português](../i18n/pt/ANDROID.md) · [العربية](../i18n/ar/ANDROID.md)

An Android app that carries the same [Go compute kernels](../agent-go/README.md) as the desktop
version. Install one file and press Start. By default the agent signs each result on the
device and publishes it without an account or token.
No rewards are provided at this stage.

**Experimental.** Shell 0.3.0 includes Go agent 1.0.0 (engine release 7) in the APK. Installation over 0.2.0,
the service lifecycle and reboot still need testing on Android.

## For participants

1. Download `skynet-agent.apk` from the
   [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) page.
2. Open the file. Android asks you to allow installing apps from your browser or file manager.
3. Open "SkyNet Agent" and press **Start**. A permanent notification shows that it is running.

- It works only while the device is charging, unless you tick "Also work on battery power".
  Unplugging cancels the current unit and leaves it available for a later run.
- To resume after restarting the device, enable **Start after reboot**. It is off by
  default. Pressing **Stop** keeps the agent stopped across a reboot.
- On Android 13 and newer, if you refuse notifications, the app still works; Android then shows
  it only in the list of running apps.
- If an existing profile uses `submit_via=github`, its results stay queued. This version
  supports publication via signed network records.
- Android 7.0 or newer on arm64-v8a or x86_64.
- The optional AI mode is not available in the app.
- To remove it, uninstall the app; nothing else is left on the device.

## Updating the app

Install 0.3.0 over the existing app with the same package signature to keep your device
identity, settings, progress and queued results. From 0.2.0 onward, opening the screen checks for a new APK.
Android also schedules a daily check when a network is available, even if the agent is
stopped. Battery restrictions can delay that check.

The app verifies the signed release manifest with the key bundled in the APK. For a newer
compatible version, it downloads the release asset into private cache and checks its size
and SHA-256. Tap the update button or notification to install it. On Android 8 and newer,
allow installation from SkyNet Agent if prompted, return to the app and confirm in the
Android installer. With notifications disabled, use the button on the main screen.

## Agent and updates

The foreground service starts the extracted executable in the native library directory.
It runs one low-priority worker at a time and holds a wake lock during computation. A
timed-out worker is stopped and the agent temporarily skips that task. New tasks arrive
through the signed task index. New executable code arrives with an app update.

Android checks the APK signing certificate during installation. The separate release key
authenticates the task index and the APK download manifest. The app checks the APK's
size, SHA-256, package name and version code before opening the installer.

## Build it yourself

On Linux, install Go 1.27.4 with sources, Bash, GNU patch, coreutils, file and readelf
(binutils). Building the APK also requires JDK 17, Gradle 8.7 and Android SDK 34.

```sh
cd android
gradle assembleRelease
```

Gradle invokes `./build-go.sh`. Run that script directly to build just the two
`app/src/main/jniLibs/<abi>/libskynet.so` executables. It uses `GOOS=android`,
`CGO_ENABLED=0` and PIE for both ABIs. The arm64 build uses stock Go. For the
x86_64 emulator build the script enables internal linking in a temporary copy of
Go 1.27.4's host build tools. It verifies the architecture, entry point and
`/system/bin/linker64` interpreter before installing either file.

The release APK is `app/build/outputs/apk/release/app-release-unsigned.apk`. Use
`zipalign`, then `apksigner sign` with the same key as the previous APK for in-place
upgrades. Generate and sign `android/latest.json` from the final signed APK with
`tools/make_apk_manifest.py`.

## License

MIT, as the agent: [agent/LICENSE](../agent/LICENSE).
