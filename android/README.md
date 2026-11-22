# SkyNet research agent for Android (experimental)

**English** · [中文](../i18n/zh/ANDROID.md) · [Español](../i18n/es/ANDROID.md) · [Français](../i18n/fr/ANDROID.md) · [Deutsch](../i18n/de/ANDROID.md) · [Italiano](../i18n/it/ANDROID.md) · [Русский](../i18n/ru/ANDROID.md) · [Português](../i18n/pt/ANDROID.md) · [العربية](../i18n/ar/ANDROID.md)

An Android app that carries the same [research agent](../agent/README.md) as the desktop
version. It is for people who do not want to set up Termux: install one file, press Start.
No rewards are provided at this stage.

**Status: experimental.** On 22 November 2026 the app was checked on an Android 14 emulator
(x86_64) against a local test repository signed with a test key: it installed, started, checked
the signatures, computed all 7 units of the test tasks without errors, waited while the
emulator was off the charger, kept working in the background, saved a token and reached the
real GitHub API with it, and stopped and started again with its state kept. An ARM-only build
(`arm64-v8a`) did the same on that emulator through its ARM translation. Its Python part also
passes the tests on a computer. **It has not yet been verified on a real phone**, on Android
7–13, in long runs, or against the battery savers of phone makers. Running the agent in
[Termux](../agent/README.md#install) remains the other way.

## For participants

1. Download `skynet-agent.apk` from the
   [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) page.
2. Open the file. Android asks you to allow installing apps from your browser or file manager.
3. Open "SkyNet Agent" and press **Start**. A permanent notification shows that it is running.

What to know:

- It works only while the device is charging, unless you tick "Also work on battery power".
  The charger is checked between pieces of work: a piece that has started (usually under a
  minute) is finished even if you unplug the device.
- It does not start by itself after the device restarts: open the app and press Start again.
- On Android 13 and newer, if you refuse notifications, the app still works; Android then shows
  it only in the list of running apps.
- To publish results it needs a GitHub token: in GitHub open Settings → Developer settings →
  Personal access tokens, create a token that may write issues of public repositories, and
  paste it into the app. The token is kept only inside the app. Without a token the results
  wait on the device (up to 300, then the app stops computing).
- Android 7.0 or newer, a 64-bit device, about 40 MB.
- The optional AI mode is not available in the app.
- To remove it, uninstall the app; nothing else is left on the device.

## How it differs from the desktop agent

| | Desktop | Android app |
|---|---|---|
| Agent code | `agent/skynet_agent` | the same package, built into the APK |
| Work | separate low-priority processes | one unit at a time inside the app's background process |
| Time limit | the worker process is killed | a watchdog ends the background process; Android restarts it and the task is left to faster devices |
| Agent updates | signed release from the repository | the same signed release, checked by the code built into the APK: signature, every file, no file outside the signed list, never below the highest release that already worked here. A new release gets three tries to reach the repository; otherwise the app returns to the built-in code |
| The app itself | launcher and installer | changes only with a new APK |
| Publishing | GitHub CLI login | a token pasted into the app |

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

The Python part of the app is [`app/src/main/python/skynet_android.py`](app/src/main/python/skynet_android.py).
It is tested on a computer by [`agent/tests/test_android_glue.py`](../agent/tests/test_android_glue.py).
Python is embedded with [Chaquopy](https://chaquo.com/chaquopy/) (MIT license).

## License

MIT, as the agent: [agent/LICENSE](../agent/LICENSE).
