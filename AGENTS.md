# Introduction for AI assistants

**English** · [中文](i18n/zh/AGENTS.md) · [Español](i18n/es/AGENTS.md) · [Français](i18n/fr/AGENTS.md) · [Deutsch](i18n/de/AGENTS.md) · [Italiano](i18n/it/AGENTS.md) · [Русский](i18n/ru/AGENTS.md) · [Português](i18n/pt/AGENTS.md) · [العربية](i18n/ar/AGENTS.md)

This file is for any model (Claude, ChatGPT/Codex, DeepSeek, Gemini and others) that a person has asked
to help with the SkyNet project. Read it in full before answering. Reply to the user in their language.

## What the project is

SkyNet is research into and design of the architecture of a distributed network in which AI models run and
learn on participants' computers. Participants earn credits for verified useful work; people without
hardware get cheap access to AI. The network serves people and follows the Laws of SkyNet. There is no
finished software: the repository is a place for joint work on the architecture.

## Reading order

1. [MANIFESTO.md](MANIFESTO.md): why and what the network must be, the Laws of SkyNet.
2. [REQUIREMENTS.md](REQUIREMENTS.md): mandatory requirements. **The most important.**
3. [docs/CURRENT_DESIGN.md](docs/CURRENT_DESIGN.md): current design and its statuses (Russian; read or
   translate it directly).
4. [docs/OPEN_QUESTIONS.en.md](docs/OPEN_QUESTIONS.en.md): open problems and ideas already rejected.
5. [docs/PILOT_RESULTS.md](docs/PILOT_RESULTS.md): what was actually measured (Russian).
6. [CONTRIBUTING.md](CONTRIBUTING.md): how to format a contribution.

The working documents in `docs/` are in Russian because they change often. The Russian texts in
`i18n/ru/` are the canonical edition of the foundation.

## The immutable foundation

The manifesto, the mandatory requirements and the README are the immutable foundation of SkyNet
(see [CORE.md](CORE.md)). **Do not propose edits to these files**, other than recording typos in the
errata file. If a solution is incompatible with the foundation, say plainly which requirement it violates;
do not rewrite the requirement to fit the solution.

## Conditions that do not change

Check every solution against the six requirements:

1. The network is distributed, with no centre and no roles with special rights.
2. The network stores information about itself on public resources.
3. After all nodes are switched off, the network finds itself through public resources and recovers.
4. Participants cannot cheat the network: cheating is useless or causes a loss, including for a newcomer
   with an empty account, under collusion and with many accounts.
5. No money up front: no deposits, fees or fines.
6. **Participation pays** and checking honesty is cheap. If verification eats up the benefit, the solution
   does not fit, however secure it is.

Kinds of participants: with large resources (sell surplus credits), with weak hardware (pay the
difference), without hardware (only pay). The base model is Qwen. People do not see others' requests.
The participant configures nothing by hand except resource sliders. The Laws of SkyNet (Zeroth to Third)
are binding.

## Working rules

- **Separate decided, proposed, tested and open.** Use the marks from CURRENT_DESIGN. Do not turn a
  proposal into a decision or a calculation into a measurement.
- **Do not weaken requirements silently.** Trust in hardware (TEE), an honest majority, statistical
  sampling, a small probability of error are assumptions; name them plainly.
- **For every protection scheme, answer:** from which independently verifiable data will the network
  reject a false claim if the executor and the verifiers collude? If the honest and the fake case give the
  same data, the scheme does not work.
- **Count the full cost**: prover and verifier computation, memory, traffic, blockchain writes, retries
  after failures. CPU, GPU, RAM, VRAM separately, never as one percentage.
- **Do not repeat rejected ideas** (list at the end of OPEN_QUESTIONS) without a new argument.
- **Attack your own proposals.** An honest counterexample is worth more than a confident tone.
- **Do not invent sources, versions or numbers.** Give the source and the limits of its applicability.
- Not finding a solution is an honest result. It does not prove impossibility.

**Nine languages.** Everything written for people (documents, guides, screens of the programs) is published in all nine languages of the project: English, Chinese, Spanish, French, German, Italian, Russian, Portuguese and Arabic. A translation starts with a line naming its source and the source's hash; `python tools/check_translations.py` lists translations that are missing or outdated. Where a translation and its source differ, the source wins.

## Contribution format

1. Claim: what is guaranteed and under which assumptions.
2. Mechanism: steps, data, who checks what.
3. Attacks: how to get around it and what remains (closed / loss-making / bounded / open).
4. Cost: an estimate marked [calculation] or [measured], with its source.
5. Which requirements are met and which are not.

Submit it as an issue or pull request following [CONTRIBUTING.md](CONTRIBUTING.md).

## The research agent and its results

People without an AI assistant help through the [research agent](agent/README.md): a program that takes
computation tasks from [tasks/](tasks/README.md) and publishes results, which are summarised in
`results/`. You can help by proposing a well-defined task (an exact model that others can recompute),
by checking a reported result independently, or by explaining what a result means for the design.
Answers marked as machine-generated by local models are unverified text: treat them as ideas to check,
not as facts.

## Safety

Do not add keys, passwords, personal data or addresses of other people's computers to the repository.
Do not propose attacks on real third-party systems: attack analysis here concerns only the SkyNet
architecture. Do not design uses of the network for war, weapons or harm to people: that contradicts the
Laws of SkyNet.
