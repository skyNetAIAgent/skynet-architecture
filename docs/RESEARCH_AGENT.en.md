<!-- translation of docs/RESEARCH_AGENT.md, source sha256: 5b9c405c6752d25fab4db09f92c07df1d7daa6bf9dfd8b40de30d40adb0236a4 -->

# The research agent: how to help the project without an AI assistant

**English** · [中文](../i18n/zh/RESEARCH_AGENT.md) · [Español](../i18n/es/RESEARCH_AGENT.md) · [Français](../i18n/fr/RESEARCH_AGENT.md) · [Deutsch](../i18n/de/RESEARCH_AGENT.md) · [Italiano](../i18n/it/RESEARCH_AGENT.md) · [Русский](RESEARCH_AGENT.md) · [Português](../i18n/pt/RESEARCH_AGENT.md) · [العربية](../i18n/ar/RESEARCH_AGENT.md)

Status as of 22 November 2026. Agent version 0.2.0 (being prepared for release). Instructions for the participant:
[agent/README.md](../agent/README.md) ([in Russian](../i18n/ru/AGENT.md)).

## Why

The repository is designed for people who have an AI assistant: it reads the documents and
helps design. Most people do not have such an assistant, but they do have a computer or a
phone. The research agent gives them a way to participate: it periodically looks into this
repository, takes tasks, performs them on the participant's device and publishes the results.

At this stage **there are no rewards**: no credits, no money and no promise of future
payments. The goal is to attract as much computing power and as many independent verifiers
as possible to designing the architecture.

The agent is a **research tool, not the SkyNet network**. It is arranged more simply and more
centrally than the network should be, and it does not itself meet the network's mandatory
requirements. This is stated plainly below in each place.

## How it is arranged

| Part | Where it lives | What it does |
|---|---|---|
| Task list | `tasks/index.json` and the signature `tasks/index.json.sig` | Names a built-in computation, its parameters and the number of independent units |
| Agent | `agent/skynet_agent/`, only the Python 3.9+ standard library | Checks signatures, picks a unit, computes, publishes, updates itself |
| Release description | `agent/release.json` and the signature | Lists the agent's files with size and SHA-256 |
| Launcher | `agent/launcher.py` | Runs the current version, switches to a new one, rolls back from a broken one |
| Results | Records signed with the device key, via public Nostr relays and full nodes ([task board](BOARD.en.md)); optionally, comments in a GitHub issue | A machine-readable record with the result hash |
| Summary | `results/`, built by `tools/collect_results.py` | Compares results from different people, re-checks the findings |

One cycle of the agent's work:

1. Every 30 minutes (with jitter) it downloads the release description and the task list.
2. It checks the signature of each of them with the release key built into the installed copy.
3. If there is a version with a higher number, it downloads its files, checks each against
   its hash, places it next to the current one and restarts.
4. It picks a random unit of a task that it has not yet computed.
5. It computes it in a separate lowest-priority process with a time limit.
6. It puts the result in the outbox and sends it as a record signed with this device's key,
   at once to several public Nostr relays and full nodes. No account is needed. A record
   counts as delivered when two relays or one node have confirmed it; otherwise it stays in
   the outbox, and the attempt is repeated: after a minute, then twice as long, but no more
   than an hour. A retry sends the same record, so a result is not counted twice. The
   previous way, comments in a GitHub issue under the participant's name, is enabled by the
   `submit_via github` setting. After 300 unsent results the agent stops taking work and
   reports this.

There is no scheduler: each agent picks a unit itself. Overlap of units between different
participants is intentional: all computational tasks are integer, so on any device the same
digits come out. A matching hash across different GitHub accounts counts as confirmation; a
match across different keys does not, because a key costs nothing and one person can create
any number of keys. Such units are confirmed by recomputation.

## A task is data, not a program

The agent never downloads or runs code from a task. A task names one of the computations
built into the agent (a "kernel") and passes it numbers. Each kernel checks the parameters
and limits the amount of work. A new kind of computation appears only with a new signed
version of the agent, whose source text lies in the repository and can be read by eye.

Version 0.1 kernels:

| Kernel | What it computes |
|---|---|
| `selftest` | A control integer calculation: the hash must match on all devices |
| `exit-scam-a` | The exact expected payment of a participant who submits fakes before leaving (variant A from [CURRENT_DESIGN](CURRENT_DESIGN.en.md)); it enumerates a family of strategies and reports those that are more profitable than leaving honestly |
| `lottery-b` | The exact probability of a loss-making month or quarter if only verified tasks are paid (variant B) |
| `ai-answer` | At the participant's option: a question for a local AI model that the participant runs themselves |

The exact model of each calculation is written at the top of the kernel's source file, so
that anyone can recompute the result independently. Tasks and their meaning:
[tasks/README.md](../tasks/README.md).

**The boundary with the project's rule about experiments.** The first tasks are
calculations from formulas in the documents (cost analysis and counterexample search) and
questions to language models. These are not measurements on hardware and not experiments
with the network. Measurement tasks (for example, whether the bits of an integer output
match on different GPUs) are published only after the project owner decides to open
experiments.

## AI mode (optional, experimental)

A participant who runs an open model locally (Ollama, the llama.cpp server, LM Studio and
the like with an OpenAI-compatible interface) can enable `ai.enabled`. The agent then passes
the model questions from the signed list and publishes the answers. Thus people without an
AI subscription but with a GPU become participants in the "council of models".

- The agent does not download or start a model, and by default it talks only to a server on
  the same computer.
- The question and the documents it quotes come from the signed list. Each document is
  checked against its hash, so a different text cannot be slipped to the model.
- By default the answer waits in the outbox until the participant approves it: the text is
  published under their name.
- The answer is marked as machine-generated and unverified. The number of answers per
  question is limited.

Verified only against a fake server in the automatic tests. With real model-serving
environments the mode has not yet been tested.

## Android app (experimental)

For those who do not want to set up Termux, there is an app: a single APK file and a
"Start" button. Source code and instructions: [android/README.md](../android/README.md). The
app embeds the same `skynet_agent` package and Python (via Chaquopy). Differences from the
agent on a computer:

- Android does not allow running separate Python processes, so a unit is computed in the
  app's own background process, one at a time. If a unit runs longer than the limit, a
  watchdog ends that process, Android starts the service again, and the task is left to
  faster devices.
- A new agent version is taken from the repository with the same release-key signature. The
  built-in copy checks it; if the new version does not start here or its files have been
  changed, the app returns to the built-in one.
- The app itself (screen, service, watchdog) changes only with a new APK. The APK is signed
  with a separate key of the project maintainers: this is a second single point of trust, which
  the network must not have.
- Results go out as signed records, as with the agent on a computer. A GitHub token is
  needed only if the participant chose the previous way of publishing.
- It works only while charging, unless the participant has allowed otherwise. There is no AI
  mode.

Status as of 22 November 2026: the app builds, and its Python part passes the tests on a
computer (`agent/tests/test_android_glue.py`). A test build with a test key passed on an
Android 14 (x86_64) emulator with a local test repository: installation, signature checks,
computing all 7 test units without errors, waiting without charging, working in the
background, saving the token and using it against the real GitHub API, stopping and starting
again with preserved state. On a real phone the app has not yet been run; the ARM
(`arm64-v8a`) build has not been verified. It is not distributed through Google Play: its
rules forbid apps that load executable code.

## What the agent trusts

| What | Trust |
|---|---|
| Ed25519 signature with the release key | Yes. Without it neither a version nor a task list is accepted |
| The channel (HTTPS, a mirror, GitHub itself, Nostr relays, full nodes) | No, for integrity: replacing a file breaks the signature or the hash, replacing a record breaks its signature |
| Task content | No: parameters are checked, the amount of work is limited, there is no code in a task |
| The local model's answer | No: it is text, and it is published as unverified |
| First installation | Yes, to the HTTPS channel to GitHub. You can check what is installed with `selftest --online` |

**The honest boundary.** Whoever holds the release key can ship the program to all installed
agents. Right now the key is with the project maintainers. This is a single point of trust that
the SkyNet network must not have: in the target project the program updates only to a
version whose hash has been accepted by a vote of the participants in the common ledger, and
a signature by someone's key is not enough ([CURRENT_DESIGN, section 8](CURRENT_DESIGN.en.md)).
A participant who does not want to trust the key sets `update` to `notify` and updates by
hand, after reading the changes.

## Threat table

| Threat | How it is covered | What remains |
|---|---|---|
| A repository or write-access account compromise: substituting the agent | A version is accepted only with a signature by a key that is not in the repository | Closed, until the key is stolen |
| Substituting a file in transit or on a mirror | The release description signature and the SHA-256 of each file | Closed |
| Rolling back to an old vulnerable version | The version number must be higher than the current one | Closed for installed agents. A new installation takes whatever lies in the repository |
| A harmful task | A task carries no code; the kernel checks the parameters and limits the amount of work and memory; there is a time limit | Limited: a signed task can occupy the CPU up to the time limit |
| Replaying an old signed task list | The list number must be no lower than one already seen; the list may have an expiry date | Limited: a fresh installation may get an old list and wastefully compute closed tasks |
| A broken version | The launcher returns to the previous version after three quick crashes or if the new version's files are gone, and remembers the unusable number. It honours repeated restart requests with a growing pause | Closed for crashes at startup. A silent error in a calculation is caught by result comparison |
| Release key theft | The key lies outside the repository; on Windows it is encrypted for the owner's account | **Open.** A thief can release a harmful version. Changing the key is done by a new version signed with the old key, and that too is available to the thief |
| Release key loss | A backup copy with the owner | Without the key the installed agents cannot be updated: participants will have to install the agent again |
| A faked result | The integer calculation is compared across different GitHub accounts; the collector counts all keys together as one vote; findings are recomputed during collection | Limited: one person with two accounts will "confirm" themselves. There are no rewards, so there is no profit in it, but a saboteur is possible. The maintainers recompute selectively |
| A stream of junk from other people's accounts and free keys | The collector accepts only records with a valid signature, a correct hash and a known task; a node limits the size, frequency and total volume | **Open for keys**: a key costs nothing, so junk can be sent without end. This is part of the project's main open question |
| Device key leak | The key lies in the agent folder and is sent nowhere | Whoever copies the file `identity.key` can sign on behalf of the device. A signature in pure Python is not protected against timing attacks |
| GitHub token leak (the previous way) | The agent stores no token, takes it from `gh` or from a variable, and sends it nowhere except GitHub over HTTPS, without redirects | A token with write access to public repositories remains the participant's responsibility |
| Foreign code next to the agent (a planted module in the current folder) | Python's isolated mode (`-I`) | Closed. There is no protection against a program with the same user's rights on the same computer |
| The participant's resource consumption | One process by default, the lowest priority, a pause on battery, a time limit, the `pause` and `stop` commands | The participant spends the electricity themselves and without reward |
| Stopping all agents by the maintainers | A signed `halt` mark in the release description; it applies even when updates are disabled | This is an intentional lever: stopping only, without starting anything |

## What the agent reports about itself

Only the contents of the published record: the task name, the unit number, the result
numbers, the calculation time and, unless disabled, a coarse platform tag like
`linux-amd64-py3.12`. Requests go to GitHub (tasks and versions) and to the relays and nodes
from `trust.py` (records). Records are public and signed with the device's permanent key, so
the results of one device can be linked to each other, and the recipient sees the sender's
network address. Information about the participant's files, network and hardware is not
collected.

## Procedure for maintainers

The release key is created once and kept outside the repository:

```
python tools/keytool.py generate
```

The owner makes a backup copy of the secret themselves, by hand, with the command
`python tools/keytool.py backup`, and keeps it outside the computer. The secret must not be
shown to assistants or pasted into chats and files.

A new agent version:

```
python tools/make_release.py --seq <next-number> --version <x.y.z>
```

then upload the changed `agent/` files to the repository. A new task list:

```
python tools/sign_tasks.py
```

then upload `tasks/index.json` and `tasks/index.json.sig`. Collecting results from both
sources (signed records and GitHub comments; `--net-only` or `--github-only` keeps one):

```
python tools/collect_results.py
```

To stop all agents until a bug is fixed: publish a release description with
`--halt-through <number>` and a reason.

## What is missing here, and why it is honest to say so

- **This is not a distributed network.** One repository hands out the tasks and versions and
  one key signs them. The results and the board tasks already go through several independent
  venues. The R1–R4 requirements from the [mandatory requirements](../i18n/ru/REQUIREMENTS.md)
  do not apply to the agent and are not met by it.
- **There is no protection against multiple keys and accounts.** For the no-reward stage
  this is acceptable; important results are confirmed by recomputation.
- **Android is not verified on a real device**; autostart on macOS, Linux and Android is
  verified only at the level of the files it creates. Two cases are accounted for from the
  documentation and are likewise not verified on real devices: Python from the Microsoft
  Store on Windows (it sees its own copy of `AppData` and the registry, so the agent folder
  lies in the profile, and autostart is added by hand) and Python from python.org on macOS
  without installed certificates (the agent retries the request with the system certificate
  file).
- **The first tasks are light.** The whole first batch (702 units) took 15.5 hours of CPU
  time on one desktop computer with 16 simultaneous lowest-priority processes, that is, about
  one hour by the clock [measured on one PC, 22 November 2026]. The mechanism is ready to
  accept heavy tasks. What came out: [results/FIRST_RUN.md](../results/FIRST_RUN.md).

## What comes next

1. Measurement tasks on different devices: the project's main unknown is whether the result
   matches to the bit on different GPUs. These are experiments, and they await the owner's
   decision.
2. Done in version 0.2.0: results and the [task board](BOARD.en.md) without an account.
3. Doing away with the single key: several independent signatures, then accepting versions by
   the rules of the network itself.
4. Managing the local model: downloading an open model with a hash check, so that AI mode can
   be turned on with one command.
