# SkyNet: open design of the architecture

**English** · [中文](i18n/zh/README.md) · [Español](i18n/es/README.md) · [Français](i18n/fr/README.md) · [Deutsch](i18n/de/README.md) · [Italiano](i18n/it/README.md) · [Русский](i18n/ru/README.md) · [Português](i18n/pt/README.md) · [العربية](i18n/ar/README.md)

## What this repository is

This is where the architecture of SkyNet is designed: a distributed network in which AI models run and
learn on participants' computers. Participants give the network their spare computing resources and earn
credits for it, while people without powerful hardware get cheap access to AI.

This is a **research** repository. There is no finished software here. It contains:

- the [manifesto](MANIFESTO.md): why the network is needed, what it must be like, and the Laws of SkyNet;
- the [mandatory requirements](REQUIREMENTS.md), which do not change;
- the [current architecture design](docs/CURRENT_DESIGN.md) with "decided", "proposed" and "open" marks (in Russian);
- the [open questions](docs/OPEN_QUESTIONS.en.md) we need help with;
- [what the pilot tested](docs/PILOT_RESULTS.md) and what it did not (in Russian);
- [contribution rules](CONTRIBUTING.md) and an [introduction for AI assistants](AGENTS.md);
- the [research agent](agent/README.md): a small program for those who have no AI assistant.

## Who it is for

- **Distributed-systems engineers, cryptographers, ML researchers.** The main problems sit where these
  fields meet: cheap verification of computation, protection against collusion, recovery of a network
  with no centre.
- **Owners of hardware** (GPUs, servers, home PCs). Their view of profit and electricity costs is needed
  for the economics to work in practice.
- **People who work with an AI assistant.** Your model (Claude, ChatGPT, DeepSeek and others) only needs
  to read [AGENTS.md](AGENTS.md) to get into context and start working.
- **People who simply want to help with their computer or phone.** No special knowledge is needed: the
  [research agent](agent/README.md) does the work.

## The point

Today not everyone gets access to strong AI: price, geographic and political restrictions and blocked
services stand in the way. At the same time the world is full of idle GPUs and computers. SkyNet is meant
to connect the two: a network with no owner and no central server, hard to switch off or block, that finds
itself after a complete shutdown, plans its own training, pays everyone fairly for verified useful work,
and serves people, not war and destruction.

## The hardest part, honestly

The main condition is that **cheating the network must be useless or cause a loss, and checking honesty
must be cheap**; otherwise participation does not pay. A solution that provably meets this condition under
collusion **does not exist yet**. There are strong candidates and dozens of analysed attacks, but key
mechanisms have not been built or measured. The current state is always described in
[CURRENT_DESIGN](docs/CURRENT_DESIGN.md) and [OPEN_QUESTIONS](docs/OPEN_QUESTIONS.en.md).
If you know how to solve even one of these problems, we need you.

## How to join

1. Read the [manifesto](MANIFESTO.md) and the [requirements](REQUIREMENTS.md).
2. Pick a question in [OPEN_QUESTIONS](docs/OPEN_QUESTIONS.en.md) or an attack on the
   [current design](docs/CURRENT_DESIGN.md).
3. Open an issue or pull request following the [rules](CONTRIBUTING.md). Most valuable: a hole found with
   a concrete example, and a solution with its cost worked out.

If you work with an AI assistant, tell it: *"Study this repository following AGENTS.md and help me with
question N from OPEN_QUESTIONS."*

**No AI assistant?** You can still help. Install the [SkyNet research agent](agent/README.md): a small
open-source program for Windows, macOS, Linux and Android. It periodically checks this repository, takes
research tasks, computes them on your device in its spare time and publishes the results. It updates
itself from this repository, and only to versions signed by the project. Participation is voluntary:
the research stage provides no rewards.

## The immutable foundation

The manifesto, the mandatory requirements and this README form the immutable foundation of the network
(version 1). Their SHA-256 fingerprints are published in [CORE_HASHES.txt](CORE_HASHES.txt). The canonical
edition is Russian. Details are in the [manifesto](MANIFESTO.md) and in [CORE.md](CORE.md).

## License

The foundation texts are licensed under CC BY-ND 4.0 (copying allowed, distributing modified versions
not allowed); the other documents under CC BY 4.0. See [LICENSE](LICENSE).
