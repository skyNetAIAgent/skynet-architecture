# How to join

**English** · [中文](../i18n/zh/CONNECT.md) · [Español](../i18n/es/CONNECT.md) · [Français](../i18n/fr/CONNECT.md) · [Deutsch](../i18n/de/CONNECT.md) · [Italiano](../i18n/it/CONNECT.md) · [Русский](../i18n/ru/CONNECT.md) · [Português](../i18n/pt/CONNECT.md) · [العربية](../i18n/ar/CONNECT.md)

You can help design SkyNet with your computer or phone. The research agent is a small open-source
program: it takes signed research computations, runs them in your device's spare time and publishes
the results. No account is needed anywhere. **No rewards are provided at this stage**: this is
volunteer help for the research, not the SkyNet network itself.

## Install

| Your device | What to do |
|---|---|
| **Windows 10/11** (64-bit) | Download `SkyNetAgentSetup-<version>-amd64.exe` from the [latest release](https://github.com/skyNetAIAgent/skynet-architecture/releases/latest) and run it. Windows shows "Windows protected your PC" because the file has no code signature: choose **More info**, then **Run anyway**. |
| **Linux** (x86_64 or ARM64) | Download `skynet-agent-linux-install-<version>.sh` from the [latest release](https://github.com/skyNetAIAgent/skynet-architecture/releases/latest) and run `sh skynet-agent-linux-install-<version>.sh`. |
| **Android 7.0+** (64-bit) | Download `skynet-agent.apk` from the releases page, open it and allow installing from this source. The app works only while the phone is charging. |

macOS and iPhone are not supported.

The installer asks whether to start the agent now and at sign-in. After that there is nothing else
to do: the agent updates itself (only to versions signed by the project), takes tasks and publishes
results on its own.

## What it uses and what it never does

- One processor core at the lowest priority by default, so your own programs are not slowed down.
  On a laptop it does not work on battery unless you allow it.
- It never runs code that comes from a task, never sends your files, and needs no administrator
  rights. Each result is a small public record signed with your device's own key.
- To pause or stop: the **SkyNet Agent** folder in the Start menu on Windows,
  `skynet-agent pause` / `stop` on Linux, the **Stop** button in the app.
- To remove: **SkyNet Agent → Uninstall** on Windows, `skynet-agent uninstall --yes` on Linux,
  uninstall the app on Android.

Details: [the agent guide](../agent/README.md).

## Help with ideas, not only with computing

The project's main open problem is how to check computations so that cheating never pays, cheaply,
without deposits or fines. If you, or your AI assistant, have an idea or have found a hole, see the
[task board](BOARD.en.md), the [roadmap](ROADMAP.en.md) and the [open questions](OPEN_QUESTIONS.en.md).
