# Tasks for research agents

**English** · [中文](../i18n/zh/TASKS.md) · [Español](../i18n/es/TASKS.md) · [Français](../i18n/fr/TASKS.md) · [Deutsch](../i18n/de/TASKS.md) · [Italiano](../i18n/it/TASKS.md) · [Русский](../i18n/ru/TASKS.md) · [Português](../i18n/pt/TASKS.md) · [العربية](../i18n/ar/TASKS.md)

This folder holds the work that [research agents](../agent/README.md) take:

- [`index.json`](index.json): the current task list;
- `index.json.sig`: its signature (agents ignore a list without a valid one);
- [`context/`](context): frozen texts that AI questions quote.

Results appear as comments in each task's tracking issue and are summarised in
[`results/`](../results) by `tools/collect_results.py`.

## What a task is

A task is data: the name of a computation that is built into the agent (a "kernel"), its
parameters, and the number of independent pieces ("units") the work is split into. A task
cannot carry code. A new kind of computation needs a new signed release of the agent.

```json
{"id": "exit-a-honest-check", "kernel": "exit-scam-a", "kernel_version": 1,
 "units": 256, "redundancy": 2, "issue": 12,
 "params": {"H0": 1200, "q": [0, 1], "cap_third": false, "batches": 2, "n_max": 200,
            "sizes": {"mode": "grid", "points": 48}}}
```

There is no scheduler. Every agent picks a random unit it has not done. Several agents
landing on the same unit is intended: all compute kernels are exact integer arithmetic, so
equal work gives equal digits on every device, and a unit counts as confirmed when
`redundancy` different GitHub accounts publish the same hash. Different hashes for one unit
are a conflict that a maintainer settles by recomputing it.

## Kernels in agent 0.1

| Kernel | What it computes | Source |
|---|---|---|
| `selftest@1` | A fixed integer workload; every device must return the same digest | [selftest.py](../agent/skynet_agent/kernels/selftest.py) |
| `exit-scam-a@1` | Exact expected payout of a participant who submits fake results and leaves, over a family of strategies; reports strategies that beat honest leaving | [exit_scam_a.py](../agent/skynet_agent/kernels/exit_scam_a.py) |
| `lottery-b@1` | Exact probability of a losing month or quarter when only checked tasks are paid | [lottery_b.py](../agent/skynet_agent/kernels/lottery_b.py) |
| `ai-answer@1` | Optional: a question for a local AI model the participant runs | [ai_answer.py](../agent/skynet_agent/kernels/ai_answer.py) |

Each source file starts with the exact model it implements, so that anyone can recompute a
result independently.

## The tasks published now, and why

All of them concern the main open question of the project: can cheating be made useless
cheaply ([OPEN_QUESTIONS, Q1](../docs/OPEN_QUESTIONS.en.md)).

| Task | Question |
|---|---|
| `selftest-1` | Does the pipeline work on your device? |
| `exit-a-honest-check` | Without collusion, is there any way to profit from fakes before leaving? The design says no |
| `exit-a-uniform-h399`, `exit-a-uniform-h1200` | With equal small tasks: from what share of colluding verifiers does leaving with fakes pay? The design's estimate is about 91% |
| `exit-a-uniform-cap-h399` | The same with the proposed limit "at most a third of the pending amount in work", in three waves |
| `exit-a-sizes-cap`, `exit-a-sizes-nocap` | The same when tasks may have any size, with and without that limit |
| `lottery-b-table` | If only checked tasks are paid, how often does a small participant have a losing month? |
| `ask-variant-b-attack` | For local AI models: find a new attack on "the network pays only for checked work" |

These are calculations on the rules as written in the design documents. They are not
measurements of hardware and not experiments with the network. Measurement tasks (for
example, whether integer inference gives the same bits on different graphics cards) will be
published only after the project maintainers open experiments.

## Propose a task

Open an issue titled `[Task] …` and say:

1. the question the computation answers and which open question it belongs to;
2. the exact model, so that it can be recomputed independently;
3. which kernel and parameters would do it, or what a new kernel must compute;
4. how a wrong or forged result would be noticed.

Maintainers check the task with `tools/sign_tasks.py --check`, add it to `index.json` and sign
the list. Only the holder of the release key can sign; see
[docs/RESEARCH_AGENT.md](../docs/RESEARCH_AGENT.md).
