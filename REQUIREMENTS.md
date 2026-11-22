# Mandatory requirements for SkyNet

**English** · [中文](i18n/zh/REQUIREMENTS.md) · [Español](i18n/es/REQUIREMENTS.md) · [Français](i18n/fr/REQUIREMENTS.md) · [Deutsch](i18n/de/REQUIREMENTS.md) · [Italiano](i18n/it/REQUIREMENTS.md) · [Русский](i18n/ru/REQUIREMENTS.md) · [Português](i18n/pt/REQUIREMENTS.md) · [العربية](i18n/ar/REQUIREMENTS.md)

*Version 1, 22 November 2026. Part of the immutable foundation of SkyNet. English translation;
the [Russian text](i18n/ru/REQUIREMENTS.md) is canonical.*

These requirements, together with the [manifesto](MANIFESTO.md) and
the Laws of SkyNet they form the **immutable foundation of the network**: they cannot be changed by a vote,
or by a decision of the creators, the developers or a majority of participants. A solution that violates
even one requirement does not suit SkyNet. It may be discussed as research, but with a plain note saying
which requirement it violates.

## The six main conditions

| No. | Requirement | How to check a solution |
|---|---|---|
| R1 | **The network is distributed.** | Devices of different participants jointly keep it running. Losing any node, any server, including one owned by the creators of the project, or a publication site does not stop the others from continuing. |
| R2 | **The network stores information about itself on public resources.** | Installed software obtains from outside enough information to recognise the network and find returning nodes. This information survives all nodes being switched off at once. There are several sources. |
| R3 | **The network finds itself and recovers after a complete shutdown.** | Returning programs find each other through public resources on their own, without the address of a live coordinator and without a manual list of nodes. |
| R4 | **Participants cannot cheat the network.** | A false claim does not lead to an accepted result, someone else's authority, an undeserved reward or a rewritten history. Collusion and multiple accounts (Sybil) are taken into account. For each solution it is shown which independently verifiable data let the network reject a false claim. **Working meaning:** cheating is useless or causes a loss, including for a newcomer with an empty account. |
| R5 | **No money up front.** | No fees, no deposits, no fines taken from an account. Deposits and fines scare participants away. |
| R6 | **Participation pays.** | Providing resources (GPU, VRAM, CPU, RAM, SSD, HDD) is profitable. Checking honesty is cheap: its cost suits everyone, especially owners of large rigs and expensive electricity. |

**R6 is the most important.** If checking honesty takes a lot of computation, participation stops paying
and the network loses its point.

## Kinds of participants

| Participant | What they do |
|---|---|
| With large resources | Earns enough credits for their own needs and sells the surplus to other participants |
| With weak hardware | Earns less than they spend on the network's models and pays the difference in cryptocurrency or money |
| Without hardware | Consumer only: pays to use the models |

One person can be both a resource provider and a user.

## Additional adopted conditions

- **State is preserved.** Confirmed rights, obligations, the history of accepted tasks, the latest accepted
  model version and the data needed to resume training survive a complete stop. Repeating an unfinished
  step gives no second reward.
- **Network split.** When histories conflict, disputed credits wait for the canonical history. One
  contribution is never paid twice.
- **Replaceable sites and keys.** Losing one account, mirror or key does not stop recovery forever.
- **Decisions verifiable after restart.** For credits, rule changes and acceptance of a model version, data
  are kept from which any node can check the grounds of the decision.
- **Public minimum.** The open catalogue holds only what is needed for discovery and authenticity checks.
  Private keys, private requests and personal data are not published.
- **Privacy.** People do not see other people's requests or personal data.
- **Independent of individuals.** Nobody has special rights, the developer included. The network sets and
  changes its training plan itself; voting over a list of options is allowed.
- **Simple for the participant.** The participant chooses nothing by hand: installs the software, accepts
  the terms, sets resource sliders, presses "Start".
- **Separate resource limits.** CPU, GPU, RAM, VRAM and disk are limited separately; they cannot be added
  up into one percentage.
- **All spare power trains.** Power not busy with requests goes into training.
- **Base model.** At the start, Qwen with open weights and a free licence. A switch to another model is
  possible only to a model with open weights and a free licence.
- **Laws of SkyNet.** The four laws of the [manifesto](MANIFESTO.md) are binding both on the
  model's behaviour and on the network's rules. The network serves people and is not built as an
  instrument of war.

## What cannot replace the requirements

- Uptime, the number of reports and the checkpoint period are **not** grounds for payment.
- A participant's signature, even together with another node's signature, does **not** prove that a
  resource was provided: colluders will sign anything.
- Statistical sampling, trust in a hardware enclave (TEE) or a small cryptographic error are assumptions.
  They may be proposed, but must be named plainly, not passed off as meeting R4.
- A successful test does not prove protection against cheating.
