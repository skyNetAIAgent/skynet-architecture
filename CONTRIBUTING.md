# How to contribute

**English** · [中文](i18n/zh/CONTRIBUTING.md) · [Español](i18n/es/CONTRIBUTING.md) · [Français](i18n/fr/CONTRIBUTING.md) · [Deutsch](i18n/de/CONTRIBUTING.md) · [Italiano](i18n/it/CONTRIBUTING.md) · [Русский](i18n/ru/CONTRIBUTING.md) · [Português](i18n/pt/CONTRIBUTING.md) · [العربية](i18n/ar/CONTRIBUTING.md)

Thank you for wanting to help. What matters here is precision, not volume: one hole found with a concrete
scenario is worth more than ten pages of general reasoning.

## What to bring

- **An attack on the current design.** A scenario: who acts, what they do, what they gain, why the network
  does not notice. Name the section of [CURRENT_DESIGN](docs/CURRENT_DESIGN.md).
- **A solution to an open question** from [OPEN_QUESTIONS](docs/OPEN_QUESTIONS.en.md).
- **A source**: a paper, protocol or project that solves part of a problem, with version, date and what it
  does **not** prove for our case.
- **A cost calculation** or a correction to an existing one.
- **A translation fix**: an inaccuracy in a translation of the foundation (via the errata file).
- **A task for the research agent**: a computation that would answer part of an open question
  (see [tasks/README.md](tasks/README.md)).
- **Computing power**: if you have no AI assistant and no time to write, run the
  [research agent](agent/README.md) on your computer or phone.

## How to format it

Open an issue and start the title with a tag:

| Tag | For |
|---|---|
| `[Attack]` | A way to cheat or disrupt the network |
| `[Q<N>]` | A proposal for open question N |
| `[Source]` | A useful paper or project |
| `[Cost]` | A cost estimate or correction to numbers |
| `[Translation]` | A translation inaccuracy |
| `[Task]` | A computation for the research agent |

In the text, state:

1. What is guaranteed and under which assumptions.
2. The mechanism.
3. Known attacks and what remains.
4. The cost, marked [calculation] or [measured].
5. Which of the six [requirements](REQUIREMENTS.md) are met and which are not.

Pull requests to the working documents (`docs/`) are welcome. When you change the status of an item,
explain why. Issues and pull requests may be written in any of the repository's languages.

## Rules

- **The foundation does not change.** A pull request that changes the manifesto, the requirements, the
  README or their fingerprints will not be accepted. See [CORE.md](CORE.md).
- A calculation is not passed off as a measurement, a proposal not as a decision.
- Do not publish keys, passwords, personal data or computer addresses.
- Be polite and to the point. Criticise ideas, not people.

If you work with an AI assistant, give it [AGENTS.md](AGENTS.md). The author of an issue is responsible
for the accuracy of its text.
