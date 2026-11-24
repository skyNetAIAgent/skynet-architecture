# SkyNet research agent

**English** · [中文](../i18n/zh/AGENT.md) · [Español](../i18n/es/AGENT.md) · [Français](../i18n/fr/AGENT.md) · [Deutsch](../i18n/de/AGENT.md) · [Italiano](../i18n/it/AGENT.md) · [Русский](../i18n/ru/AGENT.md) · [Português](../i18n/pt/AGENT.md) · [العربية](../i18n/ar/AGENT.md)

You can help design SkyNet by letting your computer do some of the research. The agent is a small open-source program. It checks this repository for tasks, does a piece of a calculation and shares the result. You can also post a research question or answer someone else's on the task board. You do not need an account or an AI assistant. [Task board guide](https://github.com/skyNetAIAgent/skynet-architecture/blob/main/docs/BOARD.en.md)

**No rewards are provided at this stage.** There are no credits, payments or promises of future payments. This is volunteer research to help design the SkyNet network.

## What it does and what it never does

| It does | It never does |
|---|---|
| Reads a signed list of tasks. Each task names a built-in calculation and supplies its inputs | Runs code from a task or a board post |
| Runs one piece of work at a time by default, at low CPU priority | Starts a new piece on detected battery power by default |
| Signs results with this device's key and, by default, sends them to public relays and a full node | Includes your personal files or hardware identifiers in an automatic result |
| Checks the project signature before installing a desktop update | Accepts a downloaded update with an invalid signature, a wrong file hash or an older release number |
| Installs for your user account and lets you choose whether to start at sign-in | Requires administrator rights for a normal desktop installation |

One research question is whether a participant who is about to leave can profit from a burst of fake results. How many verifiers would have to help? Different devices given the same piece of that calculation should get exactly the same answer, so their results can be compared. [Research tasks](https://github.com/skyNetAIAgent/skynet-architecture/blob/main/tasks/README.md)

## Requirements

- Windows on x64 (amd64) or ARM64, or Linux on amd64, arm64 or ARMv7. The desktop agent in 1.0.1 is a single Go program. The installers from Releases include the executable, ready to run. macOS is unsupported.
- For the experimental Android app, Android 7.0 or newer on arm64-v8a or x86_64.
- An Internet connection to receive new tasks and publish results. The Linux installer from Releases can install offline.

## Install

**Windows**

1. Choose the Windows installer (`.exe`) for your computer, amd64 or arm64, from [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases).
2. Compare the file's SHA-256 checksum with the checksum from a source you trust, then run the installer. You can choose to start the agent now and to start it at sign-in. Setup adds shortcuts to the Start menu. [Windows installer guide](https://github.com/skyNetAIAgent/skynet-architecture/blob/main/installer/windows/README.md)

**Linux**

Download `skynet-agent-install.sh` from [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) and run `sh skynet-agent-install.sh` as your regular user. The file includes executables for all three supported Linux architectures.

You can also install over the network with the command below. It needs `curl`, `jq`, `xxd`, `sha256sum` and OpenSSL with Ed25519 support.

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

By default, setup keeps your existing sign-in setting. On a fresh install, start the agent yourself with `skynet-agent run`. To start it now and at sign-in, run `sh skynet-agent-install.sh --autostart`. This uses your systemd user service. Add `--linger` to run from boot and after logout, or use `--no-autostart` to turn the service off. If your shell cannot find the command, use `~/.local/bin/skynet-agent`. [Linux installer guide](https://github.com/skyNetAIAgent/skynet-architecture/blob/main/installer/linux/README.md)

**Android (experimental)**

Download `skynet-agent.apk` from [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases). Open the file and allow installation from your browser or file manager when Android asks. Open **SkyNet Agent** and tap **Start**. By default it computes only while charging. **Start after reboot** is off by default.

The APK has its own version number. App version 0.3.0 includes Go agent 1.0.0. The app offers updates on its screen or in a notification. It checks the signed release description and the APK's size and SHA-256 before asking you to confirm installation in Android. [Android guide](https://github.com/skyNetAIAgent/skynet-architecture/blob/main/android/README.md)

Your device key, settings and results live in your agent folder. The default is `%LOCALAPPDATA%\SkyNetAgent` on Windows and `~/.local/share/skynet-agent` on Linux (or `$XDG_DATA_HOME/skynet-agent` if set). The Linux installer also accepts `SKYNET_AGENT_HOME` or `--home DIR` to select another folder. Android keeps its profile in the app's private storage.

If you already run the Python agent on a supported desktop with automatic updates on, it switches to Go by itself through the signed **0.4.0** bridge release. It keeps your device key, progress and unsent results. The previous bridge and its interpreter are kept for rollback.

## First steps

On Linux, use the commands below. On Windows, open PowerShell in the agent folder and use `.\skynet-agent.exe launch` in place of `skynet-agent`. For example, `.\skynet-agent.exe launch status` shows your status through the permanent launcher.

```sh
skynet-agent verify-install       # check the installed release files and run a test calculation
skynet-agent selftest --online    # run the calculation and check signed documents online
skynet-agent net id               # show this device's public key, its name on the board
skynet-agent run                  # if it isn't running already, work until you press Ctrl+C
```

Use `skynet-agent autostart status` to see whether sign-in startup is on. To turn it on, use `skynet-agent autostart enable`.

### Publishing results

The agent saves each finished result in the outbox. It uses the signing key in `identity.key` in your agent folder and creates one on first use if the file is missing. By default it sends the signed result to public Nostr relays and a full node. One node or two distinct relays must confirm receipt before the agent moves the result to `sent`. Otherwise it stays in the outbox. Each retry uses the same signed record with the same ID.

Here is part of a result for a task that uses the built-in test calculation. The full result also gives the task name, elapsed seconds, format version, agent release number and, by default, a platform tag. The signed record around it carries the device's public key, a timestamp, the record ID and the signature.

```json
{
  "agent": "1.0.1", "kernel": "selftest@1", "unit": 0, "units": 1,
  "result": {
    "kernel": "selftest@1", "rounds": 8, "ok": true,
    "digest": "a2e8f2c45179bfccb6a01d61ab527a86277215a6ee85ff824910fe27d3e9fe26"
  },
  "result_sha256": "7823a03918e86a7046e437fdf001dc40ff05fb1d241a8917baeae4d88b5629fa"
}
```

## Commands

| Desktop command | What it does |
|---|---|
| `skynet-agent run` | Work until stopped. `--once` attempts at most one unit. `--no-submit` keeps results local for this run. `--no-update` skips update installation. `--verbose` adds detail to the log. |
| `skynet-agent status` | Show the version, agent folder, power status, work counters, waiting results and recent problems. |
| `skynet-agent tasks` | List the automatic research tasks, which are ready and how many units this device has finished. |
| `skynet-agent pause` / `resume` | Let active units finish and stop starting new ones, or allow new units again. |
| `skynet-agent stop` | Ask the running agent to exit. |
| `skynet-agent outbox` | `list` shows waiting results, `show NAME` displays one, `send` tries to publish eligible results and `drop NAME` deletes a queued result. |
| `skynet-agent net` | Browse the board with `tasks` or `show`. Use `post-task`, `claim`, `report`, `accept` or `revise` to participate. `sync` retries pending board posts and fetches records. `id` shows your public key. [Board guide](https://github.com/skyNetAIAgent/skynet-architecture/blob/main/docs/BOARD.en.md) |
| `skynet-agent config` | `show` lists settings, `get KEY` shows one and `set KEY VALUE` changes it. |
| `skynet-agent update` | Check for a newer signed desktop release and install it if it is eligible for this device. |
| `skynet-agent selftest [--online]` | Check a calculation against its known answer. Add `--online` to check the signatures on the task list and the project’s older release description. |
| `skynet-agent verify-install` | Verify the installed release files and run the test calculation. |
| `skynet-agent version` | Show the agent version, release number, Go version and platform. |
| `skynet-agent autostart` | `status` shows whether startup at sign-in is on. `enable` turns it on and `disable` turns it off. |
| `skynet-agent uninstall --yes` | Remove a Linux installation. Add `--purge` to delete saved data too. |

## Settings

| Setting | Default | Meaning |
|---|---|---|
| `workers` | 1 | Number of units the desktop agent can run at once, from 1 to 256. Android runs one. |
| `run_on_battery` | false | Allow computation on battery power. |
| `paused` | false | Wait before starting new units. The `pause` and `resume` commands change this setting. |
| `poll_minutes` | 30 | Approximate interval between repository checks, from 5 to 1440 minutes. Failed checks have their own retry schedule. |
| `update` | auto | On desktop, `auto` installs eligible signed updates, `notify` logs when one is available and `off` skips installation and notices. All three still check for a signed pause from the maintainers. |
| `submit` | auto | `auto` sends results as work proceeds. `manual` keeps them in the outbox until you run `skynet-agent outbox send`. |
| `submit_via` | net | Publish signed records through relays and nodes. This is the only working channel in 1.0. |
| `max_task_minutes` | 120 | Time limit per unit, from 1 to 1440 minutes. A shorter limit in the task takes precedence. |
| `report_platform` | true | Include the operating system, processor architecture and Go version in new results, for example `linux-amd64-` followed by the Go version. |

For example, `skynet-agent config set workers 4` allows up to four desktop workers. For compatibility with older installations, `skynet-agent config show` also lists the old comment limits and AI settings. These have no effect on Go computations or network publishing.

## Optional: answer research questions with your own local AI model

Local AI mode is not available in 1.0. You can still write and post your own answer on the task board.

## Security, honestly

- **Updates and task lists are signed.** The agent checks their Ed25519 signatures against the project release key built into the program. Before switching to a desktop update, it checks the release number, verifies the size and SHA-256 of the executable and runs a test calculation. It rejects older task lists and stops starting work from an expired list.
- **Tasks supply data.** The only calculations a task can select are built into the executable. Adding a new kind of calculation takes a new desktop release or an Android app update. [Go source for the calculations](https://github.com/skyNetAIAgent/skynet-architecture/tree/main/agent-go/kernels)
- **Each unit runs in a separate process** under your account. The worker asks for low CPU priority. The agent stops the worker if it reaches the time limit.
- **A desktop update can roll back.** The launcher checks the active release before starting it. If that check fails, or three attempts to run the agent in a row crash within their first minute, the launcher can restore a verified previous release if one is available. It remembers the failed release number.
- **Your device key is an unencrypted file.** Anyone who copies `identity.key` can sign as this device. A private backup lets you keep your name on the board after reinstalling.
- **The first installation depends on where you get the installer or script.** After installation, whoever controls the project's release key can sign new code that runs with your user permissions. The maintainers hold that key during this research stage. To review desktop updates first, use `skynet-agent config set update notify` and run `skynet-agent update` when you are ready. The proposed SkyNet network is intended to work without a central release key. [Research agent design and threat table, in Russian](https://github.com/skyNetAIAgent/skynet-architecture/blob/main/docs/RESEARCH_AGENT.md)

## Privacy

GitHub sees your IP address when you download tasks or updates. Relays and full nodes you contact also see your IP address. The built-in full node uses unencrypted HTTP. Results and board posts are public. Their public key lets readers link records from the same device.

Automatic results contain calculation data and the fields described above. Use `skynet-agent config set report_platform false` to omit the platform tag from future results. The agent does not scan your personal files or include hardware serial numbers. When you post a board task or report, the text you choose to submit becomes public.

## Cost for you

A busy worker can use about one CPU core. Low priority helps other programs get CPU time when they need it. The work still uses electricity and can produce heat. On a laptop the agent checks power about once a minute. By default it waits to start new units when it detects battery power. A unit already running can finish, and the desktop agent can start work if the power source is unknown.

On Android, unplugging cancels the current unit and leaves it available to try again. Select **Also work on battery power** in the app if you want it to keep computing unplugged.

## Remove

On Windows, use the **SkyNet Agent** uninstaller. It keeps your device key, queues and release history by default. Choose the data deletion option during uninstall to remove them too.

On Linux, run the following command. It turns off the user service, stops the agent and removes the installed programs. Your key, settings, progress and queues are kept.

```sh
skynet-agent uninstall --yes
```

To remove the saved agent data as well, use `skynet-agent uninstall --yes --purge` when you uninstall. On Android, uninstall **SkyNet Agent** through Android settings to remove the app and its local data. Published records remain public.

## Troubleshooting

- **“no valid signature from a trusted key”** means the downloaded document failed verification. The agent rejects it. It can still use a previously verified task list until that list expires. On desktop, `skynet-agent status` shows the last repository error. The run log is `logs/agent.log` inside the agent folder.
- **Results stay in the outbox.** Use `skynet-agent status` or `skynet-agent outbox list` to see what is waiting. In manual mode, run `skynet-agent outbox send`. If too few relays or nodes answer, the result stays queued for another attempt.
- **An older installation shows “GitHub submission is unsupported”.** Run `skynet-agent config set submit_via net` to use signed records for new results. Entries already marked for GitHub and old AI answers stay in the outbox for inspection.
- **The agent is running but no new work starts.** Check `skynet-agent tasks` and the run log. It may be paused, waiting for power, out of eligible tasks or waiting for space in its outbox. On Android, connect the charger and tap **Start** if you previously stopped the app.

## Tested so far

Agent tests run automatically on Windows and Linux. They cover signed task lists, calculations with known answers, updates and rollback, signed records, delivery, the task board and a run that starts a worker and delivers its result to a simulated node.

Live installations have been tried on Windows 11, Linux Mint, Ubuntu Server and an Android 14 emulator. The Android app has yet to be verified on a physical device. If something does not work on your system, please open an issue.

## License

The agent's code is under the [MIT license](https://github.com/skyNetAIAgent/skynet-architecture/blob/main/agent-go/LICENSE).
