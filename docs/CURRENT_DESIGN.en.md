<!-- translation of docs/CURRENT_DESIGN.md, source sha256: a4c162fa040254e708d1d2a816f908416be83f27576a99e7dd1174c85218fced -->

# Current architecture design

**English** · [中文](../i18n/zh/CURRENT_DESIGN.md) · [Español](../i18n/es/CURRENT_DESIGN.md) · [Français](../i18n/fr/CURRENT_DESIGN.md) · [Deutsch](../i18n/de/CURRENT_DESIGN.md) · [Italiano](../i18n/it/CURRENT_DESIGN.md) · [Русский](CURRENT_DESIGN.md) · [Português](../i18n/pt/CURRENT_DESIGN.md) · [العربية](../i18n/ar/CURRENT_DESIGN.md)

Status as of 22 November 2026. This is a **design, not an implementation**. No experiments
have been run on it. Numbers marked [calculated] are obtained from a formula, not measured.

## Where we are now

The idea is formulated in the [manifesto](../MANIFESTO.md), the mandatory requirements
are approved, the basis of the architecture is chosen: a network without coordinators, a
general ledger on a public blockchain, payment for verified work and deferred payment instead
of a deposit. A small trusted pilot has already run the Qwen model on several computers
([pilot results](PILOT_RESULTS.md)).

The hardest part is ahead. A cheap way to verify work so that cheating is useless even with
collusion has not yet been found. A model that reliably improves itself and follows the laws of
SkyNet remains a research goal for now. Tasks for co-authors are in the
[open questions](OPEN_QUESTIONS.md).

Status markers:

| Marker | Meaning |
|---|---|
| **Accepted** | Approved in the project as a decision |
| **Candidate** | The chosen option, not yet approved or built |
| **Proposal** | Put up for a decision, not approved |
| **Open** | No decision |

## 1. General scheme (accepted as the basis)

The network has **no coordinators** and no roles with special rights. All participants run
the same program. Within the resource sliders it does on its own:

| Work | What it does | What it is paid for |
|---|---|---|
| Computes | Performs a training step or a user request | The accepted result |
| Verifies | Recomputes someone else's result if the draw selects this participant as a verifier | The verification performed |
| Watches | May recompute any result and challenge it | A share of what is slashed when a fake is found |
| Stores and serves | Holds the data it works with | Paid by the recipient of the data |
| Writes to the ledger | Collects participants' records into the blockchain | Reimbursement of costs |
| Helps get found | Relays connections for devices behind a router | Included in the delivery payment |

**The general ledger** is a contract on an existing public blockchain with no administrator key.
It stores the rules and the program hash, the accounts (available credits, pending amount, weight
of verified work), the hashes of submitted results, disputes, votes, the model catalog and the
training plan. The ledger works even when all SkyNet nodes are switched off. The blockchain is
**not chosen** (Open).

**Public randomness** decides who gets a task, what is verified and who verifies. It appears
after the result has been committed. Candidate: a mix of the drand beacon and blockchain
randomness (Candidate, sources not chosen).

## 2. Life of a task (candidate)

1. A training task is derived from the network's overall plan; a request comes from a user
   with payment.
2. Randomness assigns the performer from among devices with suitable resources.
3. The program computes and records hashes of intermediate states.
4. The result hash goes into a package, the package goes into the ledger. The reward goes
   into the "pending" amount.
5. Randomness after submission decides whether the task is verified.
6. The selected task is independently recomputed by three random participants, blind.
7. Matched bit-for-bit — confirmed. Did not match — a dispute, resolved by recomputing the
   disputed elementary step **in the ledger itself**, not by a vote.
8. The verification window is three days: anyone may challenge the result.
9. After the window the reward becomes available.

**Deferred payment instead of a deposit (accepted).** A participant answers for a result only
with the pending amount — their rewards of the last three days. Nothing is taken upfront;
credits that are already available are never deducted.

## 3. How to make cheating unprofitable: two variants

### Variant A. Selective verification with slashing (the current specification)

The verification share `p = 4R / (R + H)`, but no less than 1%; the slash for an incorrect
result `B = 4R/p − R`, no more than the pending amount `H` (`R` is the price of the task).
Then every fake costs, on average, four prices of the task at any verification frequency
[calculated]. A fake passes only if all three verifiers are in collusion: with a collusion
share `q` the probability is `q³`.
Cheating is unprofitable while the colluding group holds less than ~91% of the verifiers'
weight [calculated].

**Weakness.** An unverified fake gets paid and stays in the network. It is a bet that has
outcomes where the cheater wins.

**Preliminary calculation (22 November 2026, one computer, not confirmed by other
participants).** The "91%" estimate is obtained from the average over a single fake. It does
not take into account that a participant can lose no more than the pending amount: there are no
deposits and no fines. For a participant who leaves and submits fakes in batches before the
checks finish, an exact enumeration of strategies in the `exit-scam-a` model gives a lower
bound [calculated]:

| Rules | Leaving with fakes becomes profitable starting from a collusion share of |
|---|---|
| Equal small tasks, 399 prices pending, one batch | 89,2% |
| Equal small tasks, 1200 prices pending, one batch | 90,8% |
| Equal small tasks, three batches, the rule "no more than a third in work" | 89,0% |
| Tasks of arbitrary size, three batches, the rule "no more than a third" | 87,5% |
| Tasks of arbitrary size, two batches of up to 100 tasks, without the rule "no more than a third" | 80% |
| Without collusion, tasks of arbitrary size, two batches (92 million strategies) | not profitable |

Without the rule "no more than a third", the unverified rewards of the first batch increase
the pending amount and the allowed size of the second batch's tasks, so this rule is mandatory.
The model is written at the beginning of the kernel file
[exit_scam_a.py](../agent/skynet_agent/kernels/exit_scam_a.py) and reproduces the numbers from
the specification example ("about 78, 107 and 17"). The tasks are described in
[tasks/README.md](../tasks/README.md); the first run is in
[results/FIRST_RUN.md](../results/FIRST_RUN.md). These numbers will become a project result
after independent confirmation by other participants.

### Variant B. The network pays only for what is verified (proposal, awaiting a decision)

A task becomes a lottery ticket. The draw selects a share `p` of tasks (for example, 1%);
only these are verified and **only these are paid, each at `1/p` times the task price**. On average an honest
participant receives the same, and an unselected fake brings **nothing**.

- Without collusion, a fake brings exactly zero.
- With collusion, a false payout happens no more often than `q^k` per verified task (k is the
  number of verifiers): 0,1% at q = 10% and k = 3 [calculated]. Every failed attempt burns the
  entire pending amount.
- Holes found: a newcomer in collusion receives on average `q^k` of the price per attempt and
  loses nothing; an "exit campaign" from many fakes at once. Fixes are proposed: apprentice seats
  from a limited budget, cancellation of all not-yet-matured winnings of a key when a fake is
  caught, a cap on open tasks.
- Cost: income becomes uneven. For a weak device, about ±13% per month [calculated].

Both schemes require a **bit-for-bit match of the result** across different devices. The proposed
path: integer (int8/int32) model arithmetic, where the order of addition does not affect the
result. **The speed and quality of integer Qwen are not measured**; one known reproducible
int8 profile was 5,2 times slower than the usual one (Open).

A cheap dispute: by splitting the calculation in half down to a single operation, then verifying
matrix multiplication with a random vector (Freivalds' algorithm). Savings of about 100 times in
the number of multiplications on large matrices, 2,6 times on LoRA, no gain when generating one
token at a time [calculated] (Candidate).

## 4. Weight and new participants (candidate)

- **Weight** is the sum of the prices of results that passed verification over 30 days. It
  cannot be bought, transferred or accumulated. The number of accounts gives nothing: chances
  and votes are proportional to weight.
- **A newcomer** first does "apprentice" rechecks of others' tasks: their answer decides nothing
  and is paid only if it matched the accepted result. Then they receive tasks that are always
  verified, then ever more rarely.
- Weight is counted per model separately. For a model that few devices can run, the circle of
  verifiers is small and easier to capture (Open).

## 5. Peer discovery and recovery (candidate)

| Where | What survives a full shutdown |
|---|---|
| Ledger on the public blockchain | Rules, accounts, weight, model hash, training plan, disputes, addresses of the nodes that wrote |
| Participants' disks and public mirrors | Model weights, training state, data; any copy is checked against the hash from the ledger |
| Program distribution | Network identifier, ledger address, initial list of meeting places |

Three independent ways to be found, any one is enough: signed records on external venues
("meeting places"), open node-discovery networks (for example, DHT libp2p), addresses in the
ledger itself. The verification window does not run while the network is down; otherwise a fake
could be submitted just before the shutdown.

Weak spots: the authenticity of the first installation (a newcomer learns the ledger address
from outside); complete blocking of all paths at once; trust in two of three checkpoint providers
after a long downtime.

## 6. Requests and privacy (candidate)

A request is encrypted for the performer's device and goes directly or through a relay under a
pseudonym. Only hashes are in the ledger. About 1% of requests are also seen by three verifiers.

**An honest caveat.** On an ordinary computer, the owner of a device with a modified program can
read the request it computes. Fully homomorphic computation for such models is thousands of times
slower. Hence two modes: ordinary (cheap) and protected (only on hardware that proves the owner
cannot look inside; more expensive; rests on trust in the manufacturer).

## 7. Training and plan selection (proposal)

An open catalog of models and datasets with free licenses, pinned by hashes. By a rule, the
network composes training variants, gives each a trial run, and divides the free capacity by the
results and the weight vote. A new model version replaces the previous one only if it passed the
exam better, the tasks of which are chosen by randomness after the weights are fixed. The
contribution of a single task to the weight update is bounded; the "light" part of the step
(adding up the contributions) is always recomputed.

A model that **reliably and endlessly improves itself** is a research goal, not a ready
technology. A realistic first stage: automatic fine-tuning and selection by the exam.

## 8. Changing the rules (candidate)

The rules are changed only by a new program version accepted by 3/4 of **all** the weight after
a vote no shorter than 14 days and an announced 30-day notice period. A general brake (more than
half of the weight) can only stop a new model version. Proposal: an unchangeable verification
core that cannot be revoked by a vote (awaiting a decision).

## 9. Summary of attacks

Of the 60 analyzed ways to cheat: 18 are closed, 6 are unprofitable, 19 are limited, 16 are open
(for variant A). The main open spots:

1. **Weight majority.** A group with 3/4 of the weight can change the rules; in a small network
   such a share can be gained by honest work on rented capacity. Therefore the start is closed,
   on training credits.
2. **Unbuilt foundations.** A bit-for-bit match and recomputing a dispute in the ledger for a
   full model are not built.
3. **A saboteur who needs no profit.** Can spoil training within the share of their work; the
   exam does not catch hidden backdoors.
4. **Others' requests** in the ordinary mode and during disputes.
5. **Data availability.** There is nothing to adjudicate a dispute over "whether large data was
   served or not".
6. **Joining the network.** The queue for apprentice seats and the authenticity of the first
   installation.

Details and tasks for co-authors are in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.en.md).
