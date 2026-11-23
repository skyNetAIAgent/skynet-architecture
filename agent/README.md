# SkyNet research agent

**English** · [中文](../i18n/zh/AGENT.md) · [Español](../i18n/es/AGENT.md) · [Français](../i18n/fr/AGENT.md) · [Deutsch](../i18n/de/AGENT.md) · [Italiano](../i18n/it/AGENT.md) · [Русский](../i18n/ru/AGENT.md) · [Português](../i18n/pt/AGENT.md) · [العربية](../i18n/ar/AGENT.md)

You do not need an AI assistant to help design SkyNet. The research agent is a small
open-source program. It periodically looks at this repository, takes research tasks,
computes them on your computer in its spare time and publishes the results. It also gives you
a [task board](../docs/BOARD.en.md) where people and their AI assistants post research tasks and
answer them. No account anywhere is needed.

**No rewards are provided at this stage**: no credits, no money and no promise of
future payments. This is volunteer help for the research. The agent is not the SkyNet
network; it is a tool for designing it.

## What it does and what it never does

| It does | It never does |
|---|---|
| Reads the signed task list and the signed release description from this repository | Runs code that comes from a task. A task is a name of a built-in computation plus numbers |
| Runs built-in computations at the lowest CPU priority, one at a time by default | Works on battery power, unless you allow it |
| Publishes each result as a record signed with this device's own key, through public relays and full nodes | Sends your files, your hardware identifiers or anything else from your computer |
| Updates itself, but only to a version signed with the project's release key | Installs an update with a wrong signature, a wrong file hash or an older number |
| Installs in your profile and lets you choose whether to start at sign-in | Needs administrator rights |

The first tasks are exact calculations about SkyNet's payment rules, for example: "can a
participant who leaves the network profit from a burst of fake results, and from what share
of colluding verifiers?" Every device must get the same digits, and different people's
results are compared. See [tasks/README.md](../tasks/README.md).

## Requirements

- The Windows x64 installer includes Python. Linux uses Python 3.9+ from your system or a verified portable runtime on glibc x86_64 and aarch64. The current Linux runtime checksums are pending, so this build needs system Python. Other platforms need Python 3.9+.
- An Internet connection to receive tasks and publish results. The single-file Linux installer works offline.

## Install

**Windows x64**

1. Download `SkyNetAgentSetup-<version>.exe` from [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) and run it. Setup offers to start the agent now and at Windows sign-in. Both boxes are checked by default. For checksum and SmartScreen instructions, see the [Windows installer guide](../installer/windows/README.md).
2. If you already have Python, you can install from PowerShell.

```powershell
irm https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.ps1 | iex
```

**Linux**

Download `skynet-agent-install.sh` from the project's [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) and run `sh skynet-agent-install.sh`. To install directly from the repository, run:

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

At the first prompt, press Enter to run the agent now and at sign-in using your systemd user service. The second prompt offers to run it from boot, even before you sign in. For unattended setup, use `--autostart`, `--autostart --linger`, or `--no-autostart`. If your shell cannot find `skynet-agent`, use `~/.local/bin/skynet-agent`. See the [Linux installer guide](../installer/linux/README.md).

**macOS** (terminal):

```sh
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

**Android, the app (experimental)**: download `skynet-agent.apk` from the [Releases](https://github.com/skyNetAIAgent/skynet-architecture/releases) page, allow your browser to install apps and open the file. The app works only while the device is charging; results are published as signed records, no account needed. Not yet verified on a real device. Source and details: [android/README.md](../android/README.md).

**Android**: install the [Termux](https://termux.dev) app from F-Droid, open it and run:

```sh
pkg install python curl
curl -fsSL https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/install.sh | sh
```

On a phone the agent works only while the phone is charging. If it cannot tell whether the
phone is charging, it waits and says so; in that case install the Termux:API app together with
`pkg install termux-api`, or allow battery use: `skynet-agent config set run_on_battery true`.

If you prefer to read before you run: download
[`install.py`](install.py), read it (it is short), and run `python3 -I install.py`.

The installer puts the agent into one folder (`%LOCALAPPDATA%\SkyNetAgent` on Windows,
`~/Library/Application Support/SkyNetAgent` on macOS, `~/.local/share/skynet-agent` on Linux
and Android) and creates a `skynet-agent` command. Use `skynet-agent run` to start it manually.

## First steps

```sh
skynet-agent selftest --online    # check the device and the signatures
skynet-agent net id               # this device's public key: its name on the network
skynet-agent run                  # work until you press Ctrl+C
skynet-agent autostart enable     # optional: start when you log in
```

On Windows, run `.\skynet-agent.cmd` from the agent folder. The EXE installer adds status,
pause, resume and stop shortcuts under **SkyNet Agent** in the Start menu. The agent updates
its own files from signed releases. Run a newer installer to update its bundled Python.

### Publishing results

When the agent starts, it creates a key for this device (the file `identity.key` in the agent
folder). Every result is a small record signed with that key. The agent sends it at once to
several public Nostr relays of different owners and to the full nodes listed in the agent; a
result counts as delivered when two relays or one node confirmed it. Otherwise it stays in the
outbox and is sent again later, the very same record, so it is never counted twice.

Records are public and carry this device's public key, so results of one device can be linked
to each other. If you prefer the older way, comments in the task's GitHub issue under your
own account, run `skynet-agent config set submit_via github` and log in with
[GitHub CLI](https://cli.github.com) (`gh auth login`), then check with `skynet-agent github`.

A published result looks like this and contains nothing else:

```json
{"agent":"0.2.0","elapsed_s":41.2,"kernel":"exit-scam-a@1","platform":"linux-amd64-py3.12",
 "result":{"count":364838,"digest":"…","hits":0,"…":"…"},"result_sha256":"…","seq":1,
 "task":"exit-a-honest-check","unit":17,"units":256,"v":1}
```

## Commands

| Command | What it does |
|---|---|
| `skynet-agent run` | Work until stopped. `--once` does one piece of work and exits |
| `skynet-agent status` | Version, settings, counters, waiting results, last problem |
| `skynet-agent tasks` | The tasks published now and what this device has done |
| `skynet-agent pause` / `resume` | Stop taking new tasks / take them again |
| `skynet-agent stop` | Ask the running agent to exit |
| `skynet-agent outbox` | Results waiting to be published (`list`, `show`, `send`, `link`, `approve`, `drop`) |
| `skynet-agent net ...` | The task board: `tasks`, `show`, `post-task`, `claim`, `report`, `accept`, `revise`, `sync`, `id`; see [the board guide](../docs/BOARD.en.md) |
| `skynet-agent config show` / `set KEY VALUE` | Settings |
| `skynet-agent update` | Install the newest signed version now |
| `skynet-agent selftest [--online]` | Check the device, the installed files and the signatures |
| `skynet-agent autostart enable` / `disable` | Start at login, or not |
| `skynet-agent uninstall --yes` | Turn autostart off and stop the agent. The Linux shell installation also removes its program files |

## Settings

| Setting | Default | Meaning |
|---|---|---|
| `workers` | 1 | Tasks run at the same time; each uses about one CPU core |
| `run_on_battery` | false | Work while on battery power |
| `poll_minutes` | 30 | How often to look at the repository |
| `update` | auto | `auto` installs signed updates, `notify` only reports them, `off` ignores them. A pause requested by the maintainers applies in every mode |
| `submit` | auto | `auto` publishes results, `manual` keeps them in the outbox |
| `submit_via` | net | `net`: signed records, no account; `github`: comments under your GitHub account |
| `max_task_minutes` | 120 | The longest one piece of work may take |
| `batch_minutes` | 60 | With `submit_via github`: results of one task are published together, at most one comment per this many minutes |
| `max_submissions_per_day` | 48 | With `submit_via github`: the most comments published per day from this device |
| `report_platform` | true | Add a coarse tag like `windows-amd64-py3.12` to results |
| `ai.enabled` | false | Optional AI mode, see below |

Example: `skynet-agent config set workers 4`.

## Optional: answer research questions with your own local AI model

If you run an open model on your computer (for example with Ollama, the llama.cpp server or
LM Studio), the agent can pass it research questions from the task list and publish the
answers. This is off by default and experimental.

```sh
skynet-agent ai                               # shows the local server and the model it would use
skynet-agent config set ai.enabled true
```

- The agent does not download or start a model. It talks only to a server on your own
  computer, unless you set `ai.allow_remote`.
- The question and the documents it quotes come from the signed task list; each document is
  checked against a hash before the model sees it.
- Each answer waits in the outbox until you look at it: `skynet-agent outbox show NAME`, then
  `skynet-agent outbox approve NAME`. To publish without review:
  `skynet-agent config set ai.review_before_submit false`.
- Answers are published as machine-generated and unverified.

## Security, honestly

- **Updates and task lists are signed** (Ed25519). The agent accepts them only if the
  signature matches a release key built into the installed copy, the release number is higher
  than the current one, and every file matches its SHA-256. A download from a mirror or over a
  bad connection cannot change this.
- **Tasks are data, not programs.** New kinds of computation arrive only inside a signed
  release, as readable Python source in [`skynet_agent/kernels`](skynet_agent/kernels).
- **The agent runs in Python's isolated mode**, with a time limit for every piece of work, in a
  separate low-priority process.
- **If a new version cannot start**, the launcher returns to the previous one and remembers
  not to install that release again.
- **Your device key** is a plain file in the agent folder. Whoever copies it can sign as this
  device; keep a copy if you want to keep your name on the board after reinstalling.
- **What you have to trust.** Whoever holds the release key can ship code to every installed
  agent. At this research stage the key is held by the project maintainers. If you do not want
  automatic updates, run `skynet-agent config set update notify` and update by hand after
  reading the changes. The very first installation trusts the HTTPS connection to GitHub.
  The target SkyNet network must not have such a key at all; this agent is a research tool
  and does not yet meet SkyNet's own requirements. Details and the threat table:
  [docs/RESEARCH_AGENT.md](../docs/RESEARCH_AGENT.md) (in Russian).

## Privacy

The agent downloads public files from this repository (GitHub sees your IP address, as for any
visit) and sends results and board records to the relays and nodes listed in the agent (they see
your IP address too). A result holds the task name, the piece number, the computed numbers, how
long it took and, unless you switch `report_platform` off, a coarse platform tag. It is public and
signed with this device's key. Nothing about your files, your network or your hardware is collected.

## Cost for you

Electricity for one busy CPU core by default, at the lowest priority, so other programs are
not slowed down. On a phone the battery is not used unless you allow it; keep the phone on a
charger.

## Remove

For an EXE installation, choose **SkyNet Agent → Uninstall** in the Start menu. The
uninstaller keeps your device key and unsent results by default. Select the data deletion
checkbox to remove them as well. For a command-line installation, run the following command.

```sh
skynet-agent uninstall --yes
```

The Linux shell installer keeps the device key, settings and saved results. To delete those too, use `skynet-agent uninstall --yes --purge` when uninstalling. For other command-line installations, delete the agent folder after the command exits.

## Troubleshooting

- **"no valid signature from a trusted release key"**: the downloaded file is not what the
  maintainers signed. The agent refuses it and keeps working with what it has. If it repeats
  for days, look at the repository's issues.
- **`CERTIFICATE_VERIFY_FAILED` on macOS** with Python from python.org: the agent then tries
  the system's certificate file by itself. If the error stays, run the
  `Install Certificates.command` that comes with that Python.
- **Python from the Microsoft Store (Windows)** keeps a private copy of `AppData` and of the
  registry. With it the agent folder is `SkyNetAgent` in your profile folder, and autostart has
  to be added by hand: `skynet-agent autostart enable` prints how. Not yet verified on a real
  device.
- **Results stay in the outbox**: run `skynet-agent status`. With `submit_via net` the relays or
  nodes were not reachable (a firewall?); with `submit_via github`, usually `gh auth login` is missing.
- **Android stops the agent in the background**: run `termux-wake-lock` in Termux and exclude
  Termux from battery optimisation.

## Tested so far

The test suite ([`tests/`](tests)) covers signatures, updates, rollback, tasks, publishing, signed records, the task board, a full
node and an end-to-end run, and is executed automatically on Windows, Linux and macOS for every change
(see the repository's Actions tab). By hand it has been verified on Windows 11. Not yet
verified on a real device: Android (Termux), and autostart on macOS, Linux and Android. If
something does not work on your system, please open an issue.

## License

The agent's code is under the [MIT license](LICENSE).
