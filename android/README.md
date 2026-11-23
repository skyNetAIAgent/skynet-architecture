# SkyNet research agent for Android (experimental)

**English** · [中文](../i18n/zh/ANDROID.md) · [Español](../i18n/es/ANDROID.md) · [Français](../i18n/fr/ANDROID.md) · [Deutsch](../i18n/de/ANDROID.md) · [Italiano](../i18n/it/ANDROID.md) · [Русский](../i18n/ru/ANDROID.md) · [Português](../i18n/pt/ANDROID.md) · [العربية](../i18n/ar/ANDROID.md)

An Android app that carries the same [research agent](../agent/README.md) as the desktop
version. Install one file and press Start. By default the agent signs each result on the
device and publishes it without an account or token.
No rewards are provided at this stage.

**Experimental.** The previous shell was tested on an Android 14 emulator on 22 November
2026. It completed all seven test units, waited for charging and kept its state across
stops and starts. Shell 0.2.0 includes agent 0.2.2. Its installation and reboot flows
still need testing on Android.

## For participants

1. Download `skynet-agent.apk` from the
   [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) page.
2. Open the file. Android asks you to allow installing apps from your browser or file manager.
3. Open "SkyNet Agent" and press **Start**. A permanent notification shows that it is running.

- It works only while the device is charging, unless you tick "Also work on battery power".
  The charger is checked between pieces of work: a piece that has started (usually under a
  minute) is finished even if you unplug the device.
- To resume after restarting the device, enable **Start after reboot**. It is off by
  default. Pressing **Stop** keeps the agent stopped across a reboot.
- On Android 13 and newer, if you refuse notifications, the app still works; Android then shows
  it only in the list of running apps.
- Advanced users who select `submit_via=github` can enter a GitHub token on the main screen.
- Android 7.0 or newer, a 64-bit device, about 40 MB.
- The optional AI mode is not available in the app.
- To remove it, uninstall the app; nothing else is left on the device.

## Updating the app

If you have version 0.1.0, install 0.2.0 from Releases over the existing app to keep your
settings and queued results. From 0.2.0 onward, opening the screen checks for a new APK.
Android also schedules a daily check when a network is available, even if the agent is
stopped. Battery restrictions can delay that check.

The app verifies the signed release manifest with the key bundled in the APK. For a newer
compatible version, it downloads the release asset into private cache and checks its size
and SHA-256. Tap the update button or notification to install it. On Android 8 and newer,
allow installation from SkyNet Agent if prompted, return to the app and confirm in the
Android installer. With notifications disabled, use the button on the main screen.

## How it differs from the desktop agent

| | Desktop | Android app |
|---|---|---|
| Agent code | `agent/skynet_agent` | the same package, built into the APK |
| Work | separate low-priority processes | one unit at a time inside the app's background process |
| Time limit | the worker process is killed | a watchdog ends the background process; Android restarts it and the task is left to faster devices |
| Agent updates | signed release from the repository | the APK verifies the signed files and release number. A new agent gets three starts to pass a local self-check and complete a loop step |
| The app itself | launcher and installer | a verified APK installed with your confirmation |
| Publishing | signed records by default | signed records by default |

Honest limits. The APK is signed with a key held by the project maintainers; Android accepts an
update of the app only if it is signed with the same key. The release key (for agent code and
task lists) and this APK key are two single points of trust that the target SkyNet network
must not have. The app loads signed Python code at run time, which the rules of Google Play
do not allow, so it is distributed as a file.

## Build it yourself

You need JDK 17, the Android SDK (platform 34, build-tools 34), Gradle 8.7 and Python 3.12 on
the build computer.

```sh
cd android
gradle assembleRelease
```

The result is `app/build/outputs/apk/release/app-release-unsigned.apk`. Sign it with your own
key (`zipalign`, then `apksigner sign`) before installing. An APK you sign yourself cannot be
installed over the project's one, and the other way round.

Build the app only from a commit in which `agent/skynet_agent/trust.py` lists the release key:
an agent without a release key accepts no tasks. The release build stops with an error in that
case; `-PallowNoReleaseKey` builds such an APK anyway, for tests only.

The agent bridge and the APK verifier have separate desktop Python tests.
[Agent tests](../agent/tests/test_android_glue.py) · [APK update tests](../agent/tests/test_apk_update.py)
Python is embedded with [Chaquopy](https://chaquo.com/chaquopy/) (MIT license).

## License

MIT, as the agent: [agent/LICENSE](../agent/LICENSE).
