# Results of the research agents

**English** · [中文](../i18n/zh/RESULTS.md) · [Español](../i18n/es/RESULTS.md) · [Français](../i18n/fr/RESULTS.md) · [Deutsch](../i18n/de/RESULTS.md) · [Italiano](../i18n/it/RESULTS.md) · [Русский](../i18n/ru/RESULTS.md) · [Português](../i18n/pt/RESULTS.md) · [العربية](../i18n/ar/RESULTS.md)

This folder is written by `tools/collect_results.py` from the public result comments of
[research agents](../agent/README.md):

- `REPORT.md`: a readable summary, including verified findings and conflicts;
- `summary.json`: the same per task, for programs;
- `coverage.json`: how many agreeing results each unit of each task has. Agents read it to
  prefer units that still lack results; it is only a hint and needs no signature;
- `ai/`: answers of participants' local AI models, machine-generated and unverified.

A unit is confirmed when the number of different GitHub accounts required by the task
published the same result hash. Every reported "hit" of the exit-scam search is recomputed
exactly by the collector before it is listed. What the tasks mean:
[tasks/README.md](../tasks/README.md).

Nothing has been collected from participants yet. A first run of the whole task list on one
computer, not yet confirmed by anyone else, is described in [FIRST_RUN.md](FIRST_RUN.md).
