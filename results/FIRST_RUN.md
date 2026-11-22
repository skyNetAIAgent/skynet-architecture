# First run of the first task list (one computer, not yet confirmed)

**English** · [中文](../i18n/zh/FIRST_RUN.md) · [Español](../i18n/es/FIRST_RUN.md) · [Français](../i18n/fr/FIRST_RUN.md) · [Deutsch](../i18n/de/FIRST_RUN.md) · [Italiano](../i18n/it/FIRST_RUN.md) · [Русский](../i18n/ru/FIRST_RUN.md) · [Português](../i18n/pt/FIRST_RUN.md) · [العربية](../i18n/ar/FIRST_RUN.md)

On 22 November 2026 every unit of task list number 1 was computed once on a single Windows
computer with the same code the agents run: 702 units, 15.5 CPU-hours, no failures. One
computer is not a confirmation. The numbers below become results of the project only when
other participants publish the same hashes (see [README.md](README.md)).

## Leaving with fakes (kernel `exit-scam-a@1`, variant A of the design)

A participant with an amount H0 "pending" submits fake results in a few quick waves and
leaves. If they simply left, they would get H0. The table gives the lowest share of colluding
verifiers at which some strategy in the searched family has an expected payout above H0.
The exact model is at the top of
[exit_scam_a.py](../agent/skynet_agent/kernels/exit_scam_a.py).

| Task | Strategies examined | Profitable from collusion share | Best expected payout there |
|---|---:|---|---|
| `exit-a-honest-check`: no collusion, any task size, two waves | 92,169,600 | never | 0.980 × H0 |
| `exit-a-uniform-h399`: equal small tasks, 399 prices pending, one wave | 7,600 | 0.892 (not at 0.890) | 1.0066 × H0 |
| `exit-a-uniform-h1200`: equal small tasks, 1200 prices pending, one wave | 22,800 | 0.908 (not at 0.906) | 1.0117 × H0 |
| `exit-a-uniform-cap-h399`: equal small tasks, three waves, "at most a third in work" | 71,772,196 | 0.890 (not at 0.888) | 1.0059 × H0 |
| `exit-a-sizes-cap`: any task size, three waves, "at most a third in work" | 1,190,974,992 | 0.875 (not at 0.870) | 1.00004 × H0; 1.034 × H0 at 0.880 |
| `exit-a-sizes-nocap`: any task size, two waves, without that limit | 69,148,800 | 0.800 (not at 0.780) | 1.218 × H0; 4.91 × H0 at 0.850 |

What it suggests:

- The design's estimate "cheating is loss-making while colluders hold less than about 91%" comes
  from the average over one fake. It does not count that a participant can lose no more than
  the pending amount (there are no deposits or fines). For someone who leaves, the loss is
  capped and the gain is not, which lowers the threshold to roughly 87.5–89%.
- The proposed rule "at most a third of the pending amount in work at once" is necessary.
  Without it, unverified rewards of the first wave raise the pending amount and allow larger
  tasks in the second wave, and the threshold falls to about 80%.
- Without collusion no profitable way of leaving with fakes was found.

Limits: this is a calculation in a formal model of the rules, not a measurement; the search
covers the listed families only; the grid of collusion shares has steps of 0.002 to 0.02.

## Paying only for checked tasks (kernel `lottery-b@1`, variant B of the design)

Probability that the income of a period is below the cost of the work done in it, when a
task is checked with probability 1/P and a checked task is paid P prices. Exact binomial sums.

| Tasks per month | Checked | Cost / price | Losing months | Losing quarters |
|---:|---|---:|---:|---:|
| 600 | 1 in 10 | 95% | 32.20% | 22.91% |
| 6,000 | 1 in 100 | 95% | 33.10% | 24.02% |
| 6,000 | 1 in 100 | 80% | 4.84% | |
| 60,000 | 1 in 100 | 95% | 10.47% | 1.55% |
| 200,000 | 1 in 100 | 95% | 1.15% | |
| 200,000 | 1 in 100 | 98% | 18.15% | |
| 600 | 1 in 100 | 95% | 44.49% | |

With 600 tasks a month and 1 in 100 checked, nothing at all is paid in 0.24% of months. The
full table has 360 cells; it will appear in `summary.json` once agents publish it.
