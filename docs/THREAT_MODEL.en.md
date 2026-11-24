<!-- translation of docs/THREAT_MODEL.md, source sha256: ad971a2fe29f57d18ba6e2f6d8b4b6eedb8fb813c17a1cd1343ca6b141c990a8 -->

# Adversary model and attack table

**English** · [中文](../i18n/zh/THREAT_MODEL.md) · [Español](../i18n/es/THREAT_MODEL.md) · [Français](../i18n/fr/THREAT_MODEL.md) · [Deutsch](../i18n/de/THREAT_MODEL.md) · [Italiano](../i18n/it/THREAT_MODEL.md) · [Русский](THREAT_MODEL.md) · [Português](../i18n/pt/THREAT_MODEL.md) · [العربية](../i18n/ar/THREAT_MODEL.md)

Status as of 24 November 2026.

This document is the result of the model council on stage 1 of the roadmap ("Precise formulation",
[ROADMAP](ROADMAP.en.md), section 4). It collects the adversary model, the reconciliation of the number
of attacks, the status of each of the 60 specification attacks for Variants A and B, new attacks found
by the council, and the questions that only the project owner can decide.

**Document status.** This is the result of reasoning and calculation by formulas, not a measurement.
No experiments, network runs or software recomputations were performed for it. Numbers marked
[calculated] were obtained from the formulas in the council's papers and checked manually by the
critics; they have not been repeated on a second device. Only what the project owner approves becomes
an adopted decision. Everything else here is the council's estimate, and where there is disagreement
it is marked "disputed".

**How to read.** Section 1 defines who attacks and what counts as a gain. Section 2 explains the
discrepancy between 59 and 60. Section 3 is the main table: using it, any participant can name an
unclosed attack and verify it against the source documents. Section 4 is a brief summary, section 5
contains questions for the owner, section 6 lists who took part.

Source documents: decisions D1–D5 in [ROADMAP](ROADMAP.en.md), section 3; Variants A and B in
[CURRENT_DESIGN](CURRENT_DESIGN.en.md), section 3; [OPEN_QUESTIONS](OPEN_QUESTIONS.en.md);
[PILOT_RESULTS](PILOT_RESULTS.en.md); the first run [FIRST_RUN](../results/FIRST_RUN.md);
the mandatory requirements [REQUIREMENTS](../REQUIREMENTS.md). The table of 60 attacks is
taken from the specification of the network without coordinators of 20 November 2026 (hereinafter
SPEC); row numbers 1.1–7.4 are its numbers.

---

## 1. Adversary model

### 1.1. Notation and variants

| Symbol | Meaning |
|---|---|
| `R`, `c` | Task price and the cost of honest execution, `c ≤ R` |
| `H` | The pending amount: not-yet-matured rewards of the key for the last three days. Only this can be cancelled (there are no deposits or fines, requirement R5) |
| `p` | Verification share: in A `p = 4R/(R+H)`, but not less than 1%; in B it is constant, for example 1% |
| `B` | Cancellation in A: `B = 4R/p − R`, not more than `H`; at `p > 1%` this is `B = H`, otherwise `B = 399R` |
| `k` | The number of verifiers of a task, 3 (with lottery rounds, on average 3,5–4,5) |
| `q`, `q_eff` | The coalition's share of the total verifier weight for the model and among those actually verifying the task (section 1.7) |
| `G` | The full price of a dispute in the ledger |

**Variant A** (current specification): verification by sampling with cancellation from `H`; an
undisputed unverified submission is paid. **Variant B** (proposal): only tasks selected by lottery
and confirmed are paid, at the price `R/p`; an unselected task is paid to no one; a caught fake burns
the key's entire `H`. B is described in outline, and the council analysed "B as described": the
newcomer path, admission of verifiers by `H`, the verifier tariff and the source of `R/p` for
requests are not in the description.

### 1.2. Who attacks

The profiles are merged across all six papers. Combinations are mandatory: a coalition with free
keys, a renter that has become a coalition, a long-honest participant under collusion, a user in
collusion with verifiers, a saboteur with free keys.

| Profile | What they have | What they want |
|---|---|---|
| Lone actor | Their own keys, their own device, a modified program | Credits without work or beyond work |
| Coalition with share `q` | Keys under common control; instant transfer of results, computation steps, states and requests; a common treasury | To pass a fake, to receive verification payment without recomputation, to win votes |
| Owner of many keys | Any number of keys almost for free; the weight and `H` of new keys are zero | Queues, apprentice seats, data giveaways, assignments, Variant B tickets |
| Capacity renter | GPU-hours at the market price, the work is honest and paid by the network | A share of weight, then collusion, a rare model or the rules |
| Saboteur without profit | Ready to lose all not-yet-matured rewards | The harm itself: the model, answers, a backdoor, a shutdown |
| Participant with an empty account | `H = 0`, no weight | Any payout without work |
| Long honest, then leaving | Large `H` and weight; chooses the moment, size and number of waves | More than `H` plus honest payment for the last tasks |
| User | Their own request, credits, the right to dispute, collusion with the performer or verifiers | A free answer, a refund for a correct answer, others' data |
| Operators of relays, meeting points, ledger nodes, blockchain access points, data custodians | See addresses and times, delay, fail to forward, show a false environment | Censorship, isolating a node, identity disclosure, fees for records |
| External parties | The randomness beacon, the block producer, checkpoint providers, the maker of the protected mode, the distributor of the program | To shift the sample, to slip in a false history or program |
| Owner of others' devices | Stolen or infected worker keys | To confirm fakes, risking someone else's `H` |

### 1.3. What the adversary can and cannot do

**Can:** create any number of keys; run a modified program and read everything on their device,
including private requests in the normal mode; transfer any data within the coalition; turn off,
choose the submission time, stay silent, give data to some nodes and not to others, keep a single
copy; rent capacity; vote and buy votes; openly offer a bribe through a smart contract (confirmations
lie in the ledger, the payment can be executed without trust); as a block producer — not publish a
block and choose one of two randomness values; hold some of the relays and surround a node; have an
external benefit or value the harm itself.

**Cannot** (these are assumptions, and they must be stated explicitly): forge the signature of
someone else's unstolen key, find a hash collision, open a commitment in two ways, forge the secret
lottery (VRF); rewrite the final blocks of a public blockchain — the ledger has no administrator key
and is correct (premise 1 of SPEC; the program is not written); predict or shift the randomness after
the package is fixed (premise 2; the sources are not chosen; mixing protects against prediction but
not against selection by the last source, N13); obtain a bit-for-bit match without computation
(premise 3; not verified); change the outcome of a step recomputation in the ledger (premise 4; not
built for the full model); change the program of someone else's node (D4); cancel someone else's
available credits, receive a second payout for the same number, revoke a submitted package.

**What the network cannot see in principle:** who owns the keys and whether the participants are
independent; whether a node gave data to another; what runs on someone else's computer; how a
recomputation differs from a copy of someone else's state. If the honest and false cases give the
node the same data, no rule will distinguish them ([OPEN_QUESTIONS](OPEN_QUESTIONS.en.md)).

### 1.4. Adversary gain and damage to the network

The gain is calculated for the whole coalition from one initial state, with the same rights, tasks
and horizon until the final settlement, including leaving. Matured credits, reimbursements, the value
of the service received and of new rights are added; real costs (work, energy, rent, gas, external
payments) are subtracted. Transfers within the coalition cancel out, one credit is not counted twice,
and the victim's loss is not in itself coalition income. Types of gain: credits for a false claim
(a fake, a copy, a confirmation without recomputation, someone else's row); saved costs at the same
payment; weight and places in the lottery; a refund for a correct answer or an unpaid part of the
data; effect gain — influence on the answer or model, reading someone else's request, control over
the rules, issuance, catalogue, plan, the harm itself.

Damage to the network is calculated separately, in its own units: a wrong result was accepted; a
result was used before verification; credits were issued without work; an honest participant lost
`H`; payouts or entry for newcomers were frozen; private data was disclosed; history, rules, program
or model version were substituted; the network spent work on imposed verifications and disputes.
Damage without gain does not violate D1, but may violate other requirements; in the table this is
"n/a" with the name of the requirement.

### 1.5. Formal statement of D1

D1 (adopted on 23 November 2026): "the cheater does not get what they want"; the expected gain from
a fake is not greater than zero compared with honest work and with inaction, for any coalition,
including a newcomer with an empty account and any number of keys; a limited positive leakage does
not satisfy the criterion.

Let `U(σ)` be the expected utility of the coalition under strategy `σ`. For every strategy with a
false claim, **both** inequalities are required:

- `Δ₀ = E[U(σ) − U(inaction)] ≤ 0` — each false claim is replaced by refusing the task
  (the already earned `H₀` matures in this case);
- `Δh = E[U(σ) − U(honest work)] ≤ 0` — each false claim is replaced by honest execution.

The requirement applies at any `q` from 0 to 1, at `H = 0` and for any number of keys. To refute it,
one admissible state and one positive difference are enough. One must not compare with the larger of
the two bases: with inaction 0, an honest gain of 0,60 and a false claim of 0,20, such a comparison
gives "no violation", although `Δ₀ = +0,20` [calculated].

One paper proposed splitting D1 into an economic level (credits only) and an effect level (influence
on the answer and model, reading the request, harm). The council does not adopt this itself: the
question is referred to the owner (section 5, question 1). In the table, effect-only gain is marked
"no (effect)".

### 1.6. General principle of the "data for rejection" column

When the performer colludes with all assigned verifiers, the node sees only agreed data: fingerprints
of the result and the step, revealed states with inclusion proofs. All of them are compatible with a
fake. Only the input and the pinned model remain independently verifiable, from which the node can
recompute the task itself — about +100% of work [calculated]; neither A nor B requires this, and for
a private request an outside node does not even have the input. That is why the table often says
"no, except for full recomputation".

### 1.7. Collusion share `q_eff`

All thresholds of the form "up to 91%" refer to the coalition's share among those who actually
verify the task. `q_eff` is the coalition's share among the verifiers who (1) are admitted to the
task (under rule 2.6 of SPEC, for a task of a long-standing performer `H_v ≥ B` is required, up to
`399R`), (2) answered by the round deadline and (3) received the data for verification. Example
[calculated]: 3000 honest home devices at 8 hours and 100 honest round-the-clock ones against 800
rented round-the-clock ones. The adversary's share of the total weight is 42,1% (19 200 out of
45 600 device-hours per day); a home device accrues about `144R < 399R` and is not admitted to tasks
of long-standing performers; among those admitted `q_eff = 800/900 = 88,9%`, `q_eff³ ≈ 0,70`. The
critics' caveat: this applies to tasks with `B = 399R`. Condition (3) can raise `q_eff` to one at any
overall share (N2). The formula `q^k` is valid only for independent selections; in SPEC the rounds
continue until three answers, and for partial collusion the distribution of those who answered is
needed.

### 1.8. Basic formulas [calculated]

- **A, one fake:** gain `R − 4R(1 − q³)`; loss-making at `q < 0,9086`. **A newcomer:**
  `p = 1`, `B = H = 3R`, gain `R(4q³ − 3)`.
- **A, leaving with fakes** (FIRST_RUN enumeration on one device, not confirmed): profitable from
  `q = 0,875` (any sizes, three waves, the rule "no more than a third of `H` in progress";
  1,00004·H₀ at 0,875, 1,034·H₀ at 0,880), from 0,890 (equal tasks), from 0,800 without the
  one-third rule; without collusion, in 92 million strategies there is no profitable leaving
  (the best is 0,980·H₀). This is an enumeration of families, not a proof.
- **B, one fake** is profitable at `q^k > pH/(R + pH)`; at `p = 1%`, `k = 3`: `q ≈ 0,928` for
  `H = 400R`, `0,659` for `40R`, any `q > 0` for `H = 0`. The average gross payout for a fake is
  `R·q^k`, independent of `p`.
- **B, a wave of `N` fakes:** `E = a^N·H₀ + N·a^(N−1)·q^k·R`, `a = 1 − p(1 − q^k)`. The first
  fake is profitable at `H₀` below 2,8R / 14,3R / 52R / 105R / 269R for `q` = 0,3 / 0,5 / 0,7 /
  0,8 / 0,9. At `H₀ = 0` the largest gain per key is about `q^k·R/(e·p·(1 − q^k))`: 0,037R / 1,0R /
  5,3R / 19R for `q` = 0,1 / 0,3 / 0,5 / 0,7. One wave without enumeration is a lower bound.
- **Probability of a false payout** per task without an external dispute: in A `1 − p + p·s`, in B
  `p·s` (`s` is the probability of full collusion in the selection); at `p = 0,01`, `s = 0,125` —
  0,99125 and 0,00125, and the gross false payout at `R = 1` — 0,99125 and 0,125. Variants cannot
  be compared by the frequency of false payout alone.

---

## 2. Reconciliation of "60 and 59"

SPEC has exactly 60 rows (12 + 12 + 10 + 5 + 11 + 6 + 4): 18 closed, 6 loss-making, 19 limited,
16 open and **one "not an attack" — row 1.9** (submitting a correct result computed on someone else's
equipment is allowed by decision D2); the CURRENT_DESIGN summary, section 9, and the "In brief"
paragraph in SPEC added only four categories and lost the fifth, hence 59. All six papers and all
three critics reached this independently. The correct record is: 60 = 18 + 6 + 19 + 16 + 1.

---

## 3. Attack table

### 3.1. Notation

**Status:** closed — the node rejects the attack using ledger data under the stated premises;
loss-making — the attack is possible but on average loss-making up to the stated boundary;
limited — possible, but the damage or gain is limited by a rule; open — there is no solution;
not an attack.

**D1:** yes — the gain is not greater than zero for any coalition; **no** — there is a strategy with
a positive gain against at least one base; cond. — satisfied only under the stated premises that do
not depend on the collusion share (premises 1–4 of SPEC, not yet built); no (effect) — there is no
monetary gain or it has not been established, but effect gain is achieved (section 1.5); n/a — the
attack has no false claim for gain, and the stated requirement is affected; ? — the rule is not
specified, the sign of the gain is not established.

**Data** — the independently verifiable data by which the node will reject a false claim when the
performer colludes with all verifiers. "disputed" — the papers or critics disagreed, and the dispute
is not resolved. References "N…" lead to new attacks in section 3.9.

### 3.2. Performer

| № | Brief | A | D1 in A | B | D1 in B | Data for rejection under collusion | What is needed to close |
|---|---|---|---|---|---|---|---|
| 1.1 | A newcomer with an empty account submits a fake | loss-making up to `q ≈ 0,909`: the first tasks are always verified, gain `R(4q³−3)`. Disputed: the ChatGPT critic considers the row open, since the starting `3R` can be obtained by copying (2.2, N1) | **no** at `q ≥ 0,909`, and at any `q > 0` — through payment for apprentice re-checks | open: `R·q^k` per attempt without losses, any number of keys | **no** at any `q > 0` | No, except for full recomputation from the open input; for a request — only the user has it | Verify the first paid results by a method that every node performs itself; before that — only unpaid work. In B — admission by `H` (N16) |
| 1.2 | A long-standing participant fakes some of the tasks | loss-making up to `q ≈ 0,909`; 99% of fakes are not verified and remain in the network | **no** at high `q` | loss-making at `q^k R < p(1−q^k)H`: 0,928 at `H = 400R`, 0,659 at `40R`, any `q` at `H = 0` or from an empty key (N16) | **no** | No, except for full recomputation | Verification of a paid result independent of the collusion share (stage 4). In B — `p` and admission depending on `H` |
| 1.3 | Honest for a long time, then a major cheat and leaving | loss-making only in the enumerated families below 0,875 / 0,890 / 0,800 (section 1.8) | **no** at `q ≥ 0,875`; not proven below | open: the exit campaign has not been calculated; at small `H` it is profitable from any `q > 0` | **no** | No, except for recomputation | A proof for all strategies in A; a calculation of the exit campaign in B, including `H₀ = 0` (stage 2) |
| 1.4 | Submits a fake and disappears upon seeing the sample | closed: the package is not revoked, disappearance after the sample is a wrong result | cond. | same | cond. | The package row and the absence of a reveal by the deadline | An honest communication failure is indistinguishable (a cost for the honest); for a private request — input availability |
| 1.5 | Learns or selects the sample in advance | open today: closed only under premise 2, and the sources are not chosen (so the ChatGPT papers assessed it; the Claude and ChatGPT critics agree) | cond.; **no** when selected by the last source (N13) | same | same | The public values of the beacon and the block; collusion at the beacon threshold or withholding a block is not visible from them | Choose the sources; the beacon round strictly after final acceptance of the block; record trust in external parties as an assumption |
| 1.6 | Double payment or someone else's task | limited: the number is unique, but the ledger rejects a row with someone else's task only on an objection; if the performer is off for the whole window, the row matures. All three critics confirmed this | **no**: payment of `R` to someone else's key | same | **no** | The assignment is computable if the list of those admitted to the lottery is in the ledger | The ledger itself checks the assignment when accepting the row (cheap) |
| 1.7 | Assigns tasks to itself, invents work | open: the performer is chosen by lottery (this part is closed), but the rule for approving the training plan has not been adopted (ROADMAP, "What is not solved", item 5); repetition of content gives several payments (N22). DeepSeek critic: "closed for a fixed plan, open for a plan" | **no** | same | **no** | The node checks that the task is in the plan; the right to issue and non-repetition — no | The plan rule in the unchangeable core; issuance only for an authorised plan slot; crediting once by content |
| 1.8 | Takes profitable tasks, abandons the rest | limited: an abandoned task goes to another | yes at equal costs; disputed whether the small gain from selection at unequal costs violates D1 | limited; selection after the lottery is impossible | same | Assignment and deadline in the ledger | Equal task cost; the quota decreases after abandoned tasks |
| 1.9 | The result is computed on someone else's equipment | not an attack (D2) | n/a | not an attack | n/a | — | Distinguish from repeated submission of the same result (N1, N22) |
| 1.10 | Drags out a dispute or stays silent | limited: silence is a loss; at small `H` the network pays the difference in dispute costs | n/a; disputed when the dispute is expensive (N3) | limited; `H` is often near zero | same | Move timers in the ledger | Move deadlines; a dispute price estimate |
| 1.11 | Fakes before a network shutdown | closed: the window does not run while the network is down; the threshold is not chosen | cond. | same | cond. | The window time from packages with a weight share not below the threshold | Choose the threshold (3.10); keep the rows during downtime (N7) |
| 1.12 | Hides a fake by not providing the data | open for large data: the ledger does not see "gave or did not give"; for training the state of the previous step is needed | **no** | open; not paid, but already used | **no** | For small data — publication in the blockchain; for large data — none | Data availability before the lottery; "no data by the deadline means wrong" also for the training state (N2, M3) |

### 3.3. Verifier

| № | Brief | A | D1 in A | B | D1 in B | Data for rejection under collusion | What is needed to close |
|---|---|---|---|---|---|---|---|
| 2.1 | Confirms without recomputing | Disputed. Closed for a verifier outside the coalition (four papers, the Claude and DeepSeek critics); open according to the assessment of the ChatGPT papers and the ChatGPT critic: inside the coalition the same data are compatible with the absence of recomputation | yes for an unconnected one; inside the coalition — 2.2 | same | same | One's own state at a random point and an inclusion proof; the origin of the computation is not verifiable | Do not publish intermediate states for availability (N11) |
| 2.2 | Payment for verifying one's own group without recomputation | limited: about 0,3% of income at 10% weight [calculation: 0,01·3·0,1] | **no** at any `q > 0`: saving on recomputation (five papers, all three critics) | limited if verification in B is paid as in A (the tariff is not specified) | **no** at the same payment | No: recomputation and a copy give the same data | Do not pay for a repeat; the fix "pay from the reward of the verified task" does not zero the gain (section 4.5) |
| 2.3 | Collusion of the performer with all verifiers | loss-making up to `q_eff ≈ 0,909` (leaving — 0,875) | **no** | loss-making by the formula of section 1.8 | **no** | No, except for full recomputation; a private request — only the user has it | Verification independent of the collusion share (stage 4), or an explicit weakening of D1 (question 2) |
| 2.4 | Bribery or pressure after the sample | open: the request verifier reveals itself to the performer; a bribe through a contract (N4); with M1 the bribed verifier risks nothing. All three critics confirmed the downgrade | **no** | same; at `H = 0` bribery is cheaper | **no** | No | A request to verifiers without contact with the performer; consequences of non-reveal (M1) |
| 2.5 | A group answers first and takes the places | closed: all answers by the deadline are counted; the deadline is not chosen | cond. | same | cond. | Answer times in the ledger | The round deadline is not shorter than a daily cycle; account for the growth of `q_eff` |
| 2.6 | A record with weight but without `H` confirms fakes | closed: admission only at `H_v ≥ B`; a side effect is the growth of `q_eff` (N5) | yes | open: there is no admission rule in B | **no**: the coalition receives `R/p` without risk | The verifier's `H` in the ledger (in A) | Its own measure of verifier responsibility in B |
| 2.7 | Falsely accuses an honest performer | closed under premise 4 (not built) | cond. | same | cond. | Recomputation of the step in the ledger | A reference machine for the full model; refund on timeout — 2.8, 4.2 |
| 2.8 | Accuses a performer who is off | limited: for a private request there is no defender, the honest performer's `H` is burned | **no** for the "user + verifiers" combination (a refund for a correct answer received); n/a for pure damage | same | same | For training, anyone can defend from the open input; for a private request there is no data | A copy of the request available to the defender without disclosure |
| 2.9 | A flood of false disputes | limited by the attacker's `H` cost | n/a (cheap verification) | limited; in B `H` is often 0 | n/a | The outcome of the dispute in the ledger | Resolve contradiction N23 |
| 2.10 | Interception of someone else's find | open: the order is not worked out | **no**: a share of what is cancelled goes to the interceptor | open; the bonus in B is not specified | ? | A hidden objection `hash(find ‖ key)` with a block mark | Hidden submission with reveal and key binding (cheap); certifies the priority of fixation, not the time of opening |
| 2.11 | Reports its own fake for a share of the cancellation | closed for a selected task; a separate self-report is loss-making | yes | the bonus in B is not specified | ? | The ledger does not pay the finder until the assigned verification ends | A bonus rule for B |
| 2.12 | Refuses verifications | limited: the lottery proceeds to the next round | n/a; disputed: at `G > B` it is more profitable for a dissenter to stay silent (N3), depends on the estimate of `G` | same | same | — | An estimate of `G`; consequences of non-appearance without deposits |

### 3.4. Set of records, weight and voting

| № | Brief | A | D1 in A | B | D1 in B | Data for rejection under collusion | What is needed to close |
|---|---|---|---|---|---|---|---|
| 3.1 | Thousands of accounts | closed for weight and votes; limited overall: apprentice payouts, the giveaway and assignments grow with the number of keys (the Claude and DeepSeek critics). ChatGPT critic: the number of paid attempts depends on assigned slots, not on registrations | **no** | open: every key with an assignment is a ticket with expectation `R·q^k` | **no** | No data link the keys | Entry without payouts until independent verification; in B — admission by `H` (N16) |
| 3.2 | Inflating weight with fakes or requests to oneself | loss-making up to the threshold; unverified fakes that pass the window receive weight | **no** at the boundary | open: at `H = 0` a selected fake gives weight almost for free | **no** | No, except for recomputation | Weight only for independently verified work; reconcile "passed the window" (SPEC) and "passed verification" (CURRENT_DESIGN) |
| 3.3 | Rents capacity and honestly accrues weight | open in a small network: for ¾ of the weight — a month and a half at three times the work of the others, for 91% — ten times [SPEC calculation] | n/a (renting is allowed by D2); leads to 2.3 and 3.7 | same | n/a | No: the work is honest | Verification independent of the weight share; the unchangeable core (D4) |
| 3.4 | Large tasks that only the performer will verify | closed by the rule of an equal small size; capture of small tasks of a rare model — row 3.5 | yes | same | yes | Task size is a core rule | — |
| 3.5 | Capture of verifications of a rare model | open: `q_eff ≈ 1` is achievable | **no** | same | **no** | No | Do not pay for a model without a threshold of independent verifiers on other equipment |
| 3.6 | Empty records in apprentice seats | open: a queue of honest newcomers; payment to an apprentice for a copy (2.2) | **no** through a copy; n/a for the queue | open; the seat budget is taken by whoever has more keys | **no** | No | Do not pay for an apprentice re-check; a deadline for freeing a seat (N28) |
| 3.7 | ¾ of the weight changes the rules in its favour | Disputed. The Claude and DeepSeek critics: open — D4 protects the verification core, but not issuance, the rate, the fee, the brake and the catalogue. ChatGPT critic: limited — D4 takes priority over the old SPEC, profit requires a concrete change | **no** (capture of issuance), disputed | same | same | The core fingerprint: the node rejects a version that changes the core | List the composition of the core (question 5) |
| 3.8 | Blocks decisions (½ — model, ¼ — rules) | limited: reversible, but an error cannot be fixed | n/a (liveness) | same | n/a | — | — |
| 3.9 | Buys votes | limited: ¾ of the total weight is needed; the contract executes the bribe | as 3.7: **no** if the majority changes issuance; disputed | same | same | No | As 3.7 |
| 3.10 | Stops submitting packages to freeze the window | open: a high threshold — freezing of payouts; a low one — the coalition holds the window with its own packages and fakes mature (N14) | **no** (low-threshold branch) | same; a selected fake receives `R/p` | **no** | Time and weight shares of packages | A threshold with a proof for both bounds; distinguish the active weight of the network from the composition of verifiers |

### 3.5. User

| № | Brief | A | D1 in A | B | D1 in B | Data for rejection under collusion | What is needed to close |
|---|---|---|---|---|---|---|---|
| 4.1 | Does not pay for the answer, spends credits twice | limited by one part of the answer; double spending is closed | **no**: the unpaid part is a positive leakage (question 3) | same | **no** | Fixing of credits; the ledger does not see the transfer of a part | An honest exchange without a trusted party is impossible in the general case: reduce the part or accept an assumption |
| 4.2 | Disputes a correct answer for a refund | open in two ways: the dispute is closed by the coincidence of verifiers from the lottery (N17); a refund on timeout when the performer is off. All three critics considered the "closed" assessment in three papers overstated | **no** | same | **no** | Recomputation in the ledger — only if the dispute reached it | The right to bring a dispute to recomputation; a timeout rule; a defender with data |
| 4.3 | The user and the performer issue credits through requests | closed: requests do not issue credits | yes | closed if `R/p` is paid only from user payments; the source is not recorded | cond. | The issuance rule | Record the source of `R/p` in B (question 12) |
| 4.4 | Floods the network with requests | limited by the wallet | n/a | same | n/a | — | — |
| 4.5 | Copies the model and serves outside the network | open in the SPEC count (included in 16) | n/a: a risk to demand | same | n/a | — | — |

### 3.6. Ledger, program and communication

| № | Brief | A | D1 in A | B | D1 in B | Data for rejection under collusion | What is needed to close |
|---|---|---|---|---|---|---|---|
| 5.1 | Rewrites history or accounts | closed under premise 1 | cond. | same | cond. | Final blocks through independent points | Formal verification of the ledger program |
| 5.2 | A ledger node does not pass or distorts records | limited for censorship (one's own record costs blockchain coins, unavailable to an empty account); open for a row with a wrong price or recipient without an objection (the DeepSeek and ChatGPT critics) | **no** | same | **no** | The price and recipient are verifiable, but currently only on an objection | Check the row on acceptance; reimburse records without issuance (N12) |
| 5.3 | A fake program for a newcomer | open: the address and the reference come from one source | n/a (authenticity) | same | n/a | None before the first installation | Independent sources of the address and fingerprint; a reproducible build |
| 5.4 | A malicious update | limited: D4 allows rejecting someone else's core fingerprint; there is no reproducible build of the node program, so the SPEC "closed" does not hold; for the rest of the program — open | n/a | same | n/a | A fingerprint in the ledger without a verifiable link to the source | A reproducible build; matching the approved text does not prove its safety |
| 5.5 | Payment for nonexistent storage or for giving to oneself | closed: nothing is issued for storage | yes | same | yes | The issuance rule | — |
| 5.6 | Takes payment but does not give the data | limited by one part | **no**: leakage of one part on the recipient's side without a receipt (question 3) | same | **no** | The fingerprint of the part; a receipt confirms payment, not delivery | As 4.1 |
| 5.7 | Blocks all meeting paths | open when all paths are blocked | n/a (distribution) | same | n/a | — | — |
| 5.8 | Surrounds a node with a false state | limited by trust in two of three providers; if they collude — open (N29) | cond. | same | cond. | A final block through independent points | A light client with consensus verification |
| 5.9 | Splits the network for two payouts | closed: one ledger | yes | same | yes | The task number in one ledger | Rule split — N15 |
| 5.10 | Steals a worker key | limited: the key does not spend the wallet's credits | Disputed: n/a (harm to the victim) or **no** — stolen keys confirm fakes at someone else's `H` (N9, supported by the Claude critic) | same | same | The signature does not show the operator | Key revocation; hardware storage |
| 5.11 | Exhausts the free giveaway | open: whether there will be enough for newcomers has not been verified | n/a (denial of service); disputed if the benefit is defined as "to the first comer" | same | same | A new owner is indistinguishable from a new key of the previous one | Giveaway only for already assigned tasks |

### 3.7. Model and training

| № | Brief | A | D1 in A | B | D1 in B | Data for rejection under collusion | What is needed to close |
|---|---|---|---|---|---|---|---|
| 6.1 | A saboteur submits incorrect contributions | limited: about `x/3` contributions at a work share `x` [SPEC calculation]; not proven under full collusion; the contribution takes effect immediately (N21) | n/a for credits; no (effect) | open: an unselected fake is free, the `x/3` bound does not apply (the Claude and ChatGPT critics) | **no** | No, except for recomputation | Advance only verified contributions (the cost is delay and memory) |
| 6.2 | Hidden behaviour | open: the exam catches degradation, not a backdoor | no (effect) | same | no (effect) | No; a backdoor is possible even with a correct step | A research task |
| 6.3 | A harmful dataset or someone else's license | open: a correct computation on harmful data cannot be fixed | n/a; no (effect) | same | same | No: the hash and the label are the same for the rights holder and for an outsider | Limit the catalogue to verifiable sources |
| 6.4 | Fitting to the exam | limited: tasks are chosen after fixation | no (effect) within the unmeasurable | same | same | The time of task selection | — |
| 6.5 | Forgery of exam results | loss-making up to the threshold of 2.3; the exam is always verified, without a lottery | **no** at high `q` | as in A; the formula `R·q^k` is inapplicable to the exam (section 4.5) | **no** | The exam is small and open: every node can recompute it itself | Recomputation of the exam by every node (recommended by the DeepSeek critic; ChatGPT critic: the price and mandatory status are not established) |
| 6.6 | Capture of the vote on the plan | limited: a property of the scheme | n/a; **no** in combination with 1.7 | same | same | No | See 1.7 |

### 3.8. Privacy

| № | Brief | A | D1 in A | B | D1 in B | Data for rejection under collusion | What is needed to close |
|---|---|---|---|---|---|---|---|
| 7.1 | The device owner reads requests | open in the normal mode | n/a; no (effect) — privacy is violated | same | same | No | A protected mode at the cost of trusting the manufacturer (N25) |
| 7.2 | Mass collection of others' requests | limited by the share of assignments and verification slots | n/a; no (effect) | same | same | — | — |
| 7.3 | Linking a user's requests | open: the pseudonym and addresses are at the relay | n/a | same | n/a | — | Unlinkable payment |
| 7.4 | Reading a request through verification or a dispute | open: about 1% of requests are seen by three more devices; a false dispute publishes a fragment | n/a; no (effect) | same; the share `p` does not limit disclosure — the user opens the dispute | same | — | A dispute without disclosure (a zero-knowledge proof of the step) |

### 3.9. New attacks found by the council

Duplicates from different papers are merged. "Papers" — how many of the six papers of round 1
identified the attack; "Critics" — the conclusion of round 2. The numbers N1… are local to this
document and do not coincide with the local numbers in the papers. There are no refuted new attacks;
where the justification is refuted, this is stated.

| № | Attack | Papers | Critics | A · D1 | B · D1 | What is needed to close |
|---|---|---|---|---|---|---|
| N1 | **One computation — many payments.** A coalition key recomputes someone else's (even honest) task once and distributes the step to all its keys that came up as verifiers or apprentices for that task. Generalises 2.2: collusion with the performer is not needed | 1 | All three confirmed; the gain grows with the number of assigned paid slots, not keys | open · **no** | open · **no** | There are no data. No payout should depend on a repeat of work already done |
| N2 | **Data starvation of honest verifiers.** A verifier takes a request from the performer and reveals itself; a coalition performer gives the request only to its own; an honest "did not receive" does not answer and loses nothing; rounds continue until three coalition answers are collected | 1 (partly 3 more) | Correct with a caveat: about `3/(λ·q)` daily rounds are needed — about 15 days at `q = 5%`, `λ ≈ 4`, about 75 days at `q = 1%` [calculated]; the attack is noticeable in the ledger. The mechanism "publication of an encrypted copy" is named in SPEC but not defined. For training — only with a single copy of the input | open · **no** for requests | open · **no** | The ledger does not see the transfer. Availability of inputs before the lottery; there is no solution for a private request; see M3 |
| N3 | **A dispute costs more than the stake.** The dispute game in the pilot is 93 transactions, 5,8–6,3 million gas: about $18 at 1 gwei and $3000 per ETH, about $360 at 20 gwei [calculated; the prices are assumptions]. Repeating a row is 14,1 million gas, a different prototype, the two cannot be added | 1 (3 more adjacent) | Correct as a dilemma, the numbers are conditional: either the party in the right bears `G − B`, and an honest dissenter stays silent; or the network reimburses `G` (as 1.10 of SPEC is read), and a saboteur forces the network to pay `G` for every caught fake | open · **no** | open · **no** | An estimate of `G` for the chosen chain; tasks whose error requires a dispute — only at `H ≥ G` |
| N4 | **The "P+ε" bribe:** the contract pays the verifier ε for confirmation and promises to reimburse `H_v` if caught. A subtype of 2.4 | 1 | DeepSeek critic: material; ChatGPT critic: enforceability and equilibrium are not proven | open · **no** | open · **no** | Verification where agreement decides nothing; see M1 |
| N5 | **Growth of `q_eff` through admission `H_v ≥ B`:** 42,1% of the total weight gives 88,9% among those admitted (section 1.7) | 2 | Confirmed; only for tasks with `B = 399R` | limited · **no** on capture | open (2.6) | Compute the bounds by `q_eff`; calculate the trade-off between the cancellation size and the breadth of the round |
| N6 | **Weight disappears after 30 calendar days of shutdown:** the window stands still, weight is counted "over 30 days"; the first group to return gets all the weight | 1 | Correct by the letter of SPEC, but conditional: it does not say calendar or active time; if everyone's weight is zero, the lottery is undefined | open · **no** | open · **no** | Count weight by active network time (cheap) and define the initial accrual |
| N7 | **Package rows live about 18 days, the window may stand longer:** after downtime only a root without rows remains, there is nothing to dispute with | 3 | All confirmed | open · ? | open · ? | Keep the rows and the grounds of transitions for the entire verification and dispute period; without data a disputed entry waits |
| N8 | **One's own model in the catalogue gives `q = 1`:** a model that only the coalition's equipment can run | 1 | ChatGPT critic: this is a combination of 1.7, 3.5 and 6.6; that a small weight share gets a model into the catalogue is not proven | open · **no** | open · **no** | Do not pay for a model without a minimum circle of verifiers on other equipment |
| N9 | **Others' devices as free verifier weight:** stolen worker keys confirm fakes, the victims' `H` burns. An extension of 5.10 | 1 | Confirmed; the increase in `q` is by the weight of the captured keys, not the number of devices | open · **no** | open · **no** | Hardware key storage; account for compromise in the admissible `q` |
| N10 | **Instant submission of fakes increases the flow of assignments** (B) | 1 | Conditional: a 10–100-fold increase does not follow from the rules of SPEC | limited · yes | open · **no** | The rate of assignments only by verified work |
| N11 | **Availability versus 2.1:** publishing intermediate states for N2 allows confirming without recomputation | 1 | A limitation of the proposed change, not a standalone attack | — | — | Publish only inputs; intermediate states — in a dispute |
| N12 | **A fee for writing to the ledger above costs:** reimbursement of garbage records or a cartel of ledger nodes | 2 | The reimbursement rule is not defined in SPEC; an intermediary's ordinary income does not violate D1 | open · cond. | open · cond. | Reimburse only records with accepted results and not above the actual commission |
| N13 | **Selection by the last randomness source:** if the beacon round is known before the deciding block, its producer chooses from two values; in A `p → p²`, the gain is about +0,96R per fake [calculated]. Claude critic: with a known-in-advance schedule of producers, the coalition submits packages under its own blocks | 4 | All confirmed; the numbers apply only with the wrong order of sources | open · **no** with the wrong order | same | The beacon round strictly after final acceptance of the block |
| N14 | **The window runs without a majority:** a 40% coalition, with half of the honest switched off, gets 40/70 = 57% among the active [calculated]. A subtype of 3.10 | 2 | Confirmed as a subtype of 3.10 | loss-making · **no** for B-type leakages | open · **no** | See 3.10 |
| N15 | **Rule split:** not-yet-matured amounts mature in both branches | 1 | Conditional: doubling of one obligation is not proven | open · ? | open · ? | A separate contract with separated balances |
| N16 | **In B, deterrence is tied to the key, but access to tasks is not:** fakes from a separate empty key give `R·q^k` without losses. The common root of 1.1-B, 1.2-B, 1.3-B, 3.1-B | 2 + Claude critic | Two papers justified the hole by the fact that an ordinary participant in B has `H = 0` in 23,5–54,7% of windows; this argument is refuted (section 4.5). The correct form was given by the Claude critic | — | open · **no** | Admission to tickets at `H` not less than the expected payout for a fake; then B loses the constant low verification share (question 8) |
| N17 | **A user's dispute is decided by the sample, not by arithmetic:** the dispute is closed if the verifiers from the lottery coincide with the performer | 1 | The Claude and DeepSeek critics confirmed; ChatGPT critic: correct, but 4.2 concerns the opposite claim | open · **no** | open · **no** | The right to bring a dispute to recomputation in the ledger |
| N18 | **Fakes → weight → `q`.** An extension of 3.2 | 1 | Confirmed; the monetary conclusion requires accounting for future payouts | limited · **no** at the boundary | open · **no** | Weight only for independently verified work |
| N19 | **Garbage from free keys before assignment** overloads nodes and queues | 4 | Confirmed; a place for an honest newcomer is not guaranteed in either variant. The estimate "garbage costs the network 3–4,5 of work at almost zero attacker cost in A" was refuted by the Claude critic | open · n/a | open · **no** in combination with free tickets | Reject messages without an assignment before expensive processing; the path from a zero account is mandatory |
| N20 | **An imposed divergence of the arithmetic** of the performer and the arbiter | 2 | Confirmed; the divergence itself does not prove a gain | open · ? | open · ? | A single executable semantics of operations and verification of implementations against the reference |
| N21 | **Use of a result before verification:** the answer has been read, the step is taken as the next step and remains in the model lineage | 5 (+1 in 6.1) | All confirmed; harm is possible even at `q = 0`; `1 − p` is the share of unselected, not of applied | open · no (effect) | open · no (effect) | Verify the block before delivery; advance only a verified descendant (the cost is delay and memory) |
| N22 | **One issuance right under different numbers** (identical trial runs, repetition of a step after a restart) | 3 | Confirmed; two legitimate orders may have the same output | open · **no** | open · **no** | Crediting once by the canonical right to a plan slot |
| N23 | **Contradiction in the rules for a dispute from a zero account** (ROADMAP requires it, SPEC does not) | 1 | The DeepSeek and ChatGPT critics confirmed | open · n/a | open · n/a | A decision by the owner (question 4) |
| N24 | **Appropriation of an off performer's task** — an expansion of 1.6 | 2 | Confirmed | see 1.6 | see 1.6 | Check the assignment when accepting the row |
| N25 | **Collusion with the maker of the protected mode** | 1 | Correct within 7.1 | open · n/a | open · n/a | Record the assumption of trust in the manufacturer |
| N26 | **False receipts for data transfer** | 1 | There is no external income: the coalition pays itself | open · n/a | open · n/a | There is no sign of large-data delivery |
| N27 | **Selective non-delivery by a relay** | 1 | Confirmed for availability | limited · n/a | limited · n/a | Several relays, backup paths |
| N28 | **The "eternal apprentice"** occupies a seat and does not complete the re-check (to 3.6) | 1 | Confirmed | open · n/a | open · n/a | A deadline and automatic freeing of the seat |
| N29 | **Collusion of two of three checkpoint providers** (to 5.8) | 1 | Confirmed; "more providers" does not solve collusion of the required majority | limited · cond. | limited · cond. | A light client with consensus verification |
| N30 | **The user is given a block different from the pinned one** | 1 | Confirmed | open · ? | open · ? | Bind the delivered block to a commitment and verify it before use |
| N31 | **A common error in the core itself** accepts a wrong transition at all nodes | 1 | Confirmed; different from N20 | open · ? | open · ? | An independent specification of the transition; under D4 the fix is only by moving to a new network |
| N32 | **Recognition of a short private request by its public fingerprint** | 2 | Confirmed conditionally: a deterministic hash and a small set of texts | open · no (effect) | same | Hiding commitments with fresh randomness |

**Found only by the critics** (not checked by the other participants):

| № | Attack | Who | A · D1 | B · D1 | What is needed to close |
|---|---|---|---|---|---|
| M1 | **Free refusal to reveal.** Coalition verifiers submit a hidden "I confirm" and reveal it only if all submitted answers are its own; otherwise they stay silent and lose nothing. Bribing an outside verifier becomes risk-free: instead of a risk of `399R` — zero [calculated]. Condition: whether hidden answers are visible before the reveal is not defined in SPEC | Claude critic | open · **no** | open · **no** | Consequences of non-reveal without deposits (loss of payment and weight for the round) or hiding the number and authorship of answers; the cost for honest switched-off participants is not calculated |
| M3 | **Load through the availability mechanism.** If "did not receive" is answered by mandatory publication of a copy, a coalition verifier always claims "did not receive"; at `q = 10%`, `λ ≈ 4` this is about 34% of selected tasks [calculated] | Claude critic | open · n/a | same | A claim of non-delivery must cost the claimant no less than the publication it causes (from their `H`) |
| M4 | **A failure and a cheat under one cancellation rule:** the cause cannot be verified from an identical erroneous output | ChatGPT critic | ? | ? | No rule fair to both sides has been presented (question 11) |

(M2 of the Claude critic is N16.)

---

## 4. Summary

### 4.1. How many attacks violate D1

A count from the table of sections 3.2–3.8 [calculation from the table]. Rows marked "disputed" are
included and named separately.

| | Variant A | Variant B |
|---|---|---|
| Monetary gain ("**no**"), out of 60 rows | 24 (and 2 more conditionally: 1.5 with the wrong order of sources, 6.6 in combination with 1.7): 1.1, 1.2, 1.3, 1.6, 1.7, 1.12, 2.2, 2.3, 2.4, 2.8, 2.10, 3.1, 3.2, 3.5, 3.6, 3.7*, 3.9*, 3.10, 4.1, 4.2, 5.2, 5.6, 5.10*, 6.5 | 25: the same without 2.10 (in B "?"), plus 2.6 and 6.1 (and the same 2 conditionally) |
| Effect gain only ("no (effect)") | 7: 6.1, 6.2, 6.3, 6.4, 7.1, 7.2, 7.4 | 6: the same without 6.1 |
| New attacks with a monetary "**no**" (N1–N32, M1) | 14 | 16 |

An asterisk marks disputed rows (3.7, 3.9, 5.10). Without them, 21 remains in A and 22 in B.
The number of rows cannot be added up as the number of independent ways to cheat: one scheme is
often described by several rows. The main conclusion does not depend on the count: **in its literal
form D1 is satisfied by neither Variant A nor Variant B**, and all six papers and all three critics
agree with this.

**Comparison of A and B.** B as described is worse than A on empty and low `H` at
`0 < q < 0,909`: an empty key receives `R·q^k` for an attempt without losses (N16). At `q = 0` B is
better: an unselected fake brings nothing, even on leaving. At `q ≥ 0,909` both lose. If A's newcomer
path is transferred to B (full verification of the first tasks), the difference on empty keys
disappears (`q^k R − (1 − q^k)·3R`, as in A [calculated]), but B loses the constant low verification
share. This is an input for decision D3 at stage 2, not the decision itself.

### 4.2. Critical for launching the network with real credits

A summary of the assessments of the papers and critics. A closed start on training credits is not
blocked by these items, except for privacy, recovery (N6, N7) and the items without which the pilot
does not test what it must test (N2, N3).

1. **Collusion by `q_eff`:** 1.1, 1.2, 1.3, 2.3, 3.2, 3.5, 6.5 and N5. In both variants acceptance
   relies on the agreement of a sample of participants.
2. **Payment for a repeat:** 2.2, 3.6, N1. Violates D1 at any `q > 0`; no cheap fix has been found.
3. **Empty keys in B:** N16, 1.1-B, 3.1-B.
4. **The right to issue and the recipient:** 1.7, 1.6, 5.2, N22, and also 3.7 for issuance outside
   the core.
5. **Data availability:** 1.12, N2, N7.
6. **Disputes:** 4.2 and N17; the price of a dispute N3, the related 2.12; contradiction N23; M1.
7. **Use before verification:** N21, 6.1, N30 (if the owner includes effect in D1).
8. **Recovery:** N6 (weight after a shutdown) and N7 (package rows).
9. **Input and program:** 5.3, 5.4, N19.
10. **Privacy:** 7.1, 7.4, N32 — violate a mandatory condition regardless of money.

### 4.3. Common root

In both variants the ordinary acceptance of a result relies on the agreement of a random sample of
participants, that is, on signatures that prove nothing under collusion. Therefore the boundary of
protection is always expressed through the collusion share `q_eff`, and `q_eff` can be raised by
renting capacity, capturing a rare model, the admission rule by `H` (N5), data starvation (N2),
stolen keys (N9) or a long shutdown (N6). Independently verifiable data under full collusion are
only the input and the model, from which the node can recompute the task itself; neither A nor B
requires this, and for a private request the node does not even have the input. D1 is achievable
only by verification that does not depend on the collusion share (stage 4 [ROADMAP](ROADMAP.en.md)),
or by an explicit weakening of D1 to "at `q < q*`" by a decision of the owner.

### 4.4. Cheap fixes confirmed by the critics

| Fix | Closes | Caveat |
|---|---|---|
| The ledger itself checks the assignment, price and recipient of a row on acceptance, not on an objection | 1.6, 5.2, N24 | The list of those admitted to the lottery must be in the ledger |
| Crediting once by the canonical right to a plan slot and the content fingerprint | N22, part of 1.7 | Two legitimate orders may give the same output; the main hole of 1.7 — the plan rule — remains |
| Hidden submission of an objection with reveal and key binding | 2.10 | Certifies the priority of fixation, not the time of opening |
| Count weight and the window by active network time, not by the calendar | N6 | A rule for the initial accrual after a shutdown is needed |
| The beacon round strictly after final acceptance of the block | 1.5 (part), N13 | The sources are not yet chosen |
| Every node recomputes the exam itself before accepting a version | 6.5 | Recommended by one critic; the price and mandatory status are not yet established |
| Fix the CURRENT_DESIGN summary: 60 = 18 + 6 + 19 + 16 + 1 | Reconciliation 59/60 | — |

### 4.5. Refuted conclusions

The critics found these statements from the papers of round 1 erroneous; they were not carried into
the table.

| Statement | Where | Why it is wrong |
|---|---|---|
| The profitability threshold of a fake in B `q^k > H/(H+R)` | one DeepSeek paper | The factor `p` is lost. The correct form is `q^k > pH/(R+pH)`. At `p = 1%`, `H = 400R`, `q = 0,95`: gain `0,857R`, expected loss `0,01·0,143·400R = 0,572R`, the result is +0,285R per fake, while by the wrong formula it is a loss [calculated]. The error overstates the protection almost to complete (0,999 instead of 0,93) |
| The 90,9% threshold for an A newcomer "is valid under the assumption that 3R was accumulated by collusion" | the same paper | The threshold does not depend on how `3R` was obtained |
| Forging the exam in B gives `R·q^k` | both DeepSeek papers | The exam is always verified, without a lottery; the lottery formula is inapplicable to it |
| Fix 2.2 "pay verifiers from the reward of the verified task" zeroes the gain | one Claude paper | The copier still saves on recomputation; against inaction the gain is also positive; copying on someone else's honest task (N1) is not affected by the fix. It removes only the issuance of credits for an empty verification |
| "An ordinary participant in B has `H = 0` in 23,5–54,7% of windows, and at that time a fake is not threatened by anything" | both Claude papers | The numbers `0,99^60 ≈ 54,7%`, `0,99^144 ≈ 23,5%`, `0,99^432 ≈ 1,3%` are correct, but this is the share of windows after the fact. `H` burns at the moment of capture, including winnings that arrived after submission. The conclusion about the hole is correct for a different reason — through an empty key (N16) |
| D1 is checked by comparison with the larger of the two bases | one Claude paper | It misses the case of a positive gain against inaction (example in section 1.5) |
| "Garbage costs the network 3–4,5 of work at almost zero attacker cost" (Variant A) | one Claude paper | In A a key receives tasks only at `H ≥ 3R`, and every garbage result burns these `3R`; there is no multiple amplification. Amplification exists only in B without admission by `H` |
| Statuses corrected in the table: 2.6-B "closed" (DeepSeek and Claude papers); 1.7 "closed / yes", 1.6 and 4.2 "closed / yes", 4.1 and 5.6 "D1 yes", 2.2 "does not violate D1" (DeepSeek papers, partly Claude); 3.4 "no", 2.7 "open / no", 5.11 "no" (ChatGPT papers) | various | The grounds are in the corresponding rows of the table: there is no admission rule in B; the plan rule is open; checking the assignment and a user's dispute give a gain; D1 forbids limited leakage; the gain in 3.4 and 2.7 was taken from neighbouring rows; there is no personal benefit in SPEC |
| 1.3: gain 1,034·H₀ at the point 0,875 | one Claude paper | 1,034·H₀ refers to the point 0,880; at 0,875 it is 1,00004·H₀ |

The assessments 2.1 "open" in both ChatGPT papers and 3.7 "limited" remain disputed (not refuted):
the critics disagreed (rows 2.1 and 3.7 of the table).

---

## 5. Questions for the owner

Decisions without which stage 1 cannot be closed. The council does not make them. All twelve questions were decided on 24 November 2026 at the owner's instruction (decisions D6–D17 in [ROADMAP](ROADMAP.en.md), section 3).

1. **Is effect included in D1?** *(Decided — D6: yes.)* One paper proposed distinguishing economic D1 (credits only)
   and effect D1 (influence on the answer and model, reading the request, the harm itself). The words
   "the cheater does not get what they want" in their literal sense include effect; then the use of a
   result before verification (N21) violates D1 in both variants at any `q`, and it can be closed only
   by verification before delivery and promotion (the cost is delay and memory).
2. **Require verification independent of the collusion share, or weaken D1 to "at `q < q*`"?** *(Decided — D7: verification independent of the collusion share is required.)*
   Without one of the two, D1 is unachievable in either A or B.
3. **Leakage of one part during an exchange** *(Decided — D10: a violation of D1; exchange only through one ledger record.)* (4.1, 5.6): an honest exchange without a trusted party
   is impossible in the general case. Should it be recognised as an explicit assumption or considered
   a violation of D1?
4. **A dispute from a zero account** *(Decided — D8: only assigned verifiers and the user for their own request.)* (N23): ROADMAP requires it, SPEC does not. What then limits the
   flow of false disputes without deposits?
5. **The composition of the unchangeable core** *(Decided — D11: verification, payment for verified work, issuance, dispute and ledger rules; the rest within limits.)* (3.7): does it include the issuance rule, the rate,
   the network fee, the brake and the catalogue, or only verification?
6. **The rule for approving the training plan** *(Decided — D9: the plan is derived by a rule from the catalogue and the exam.)* (1.7, ROADMAP "What is not solved", item 5): who and
   how authorises a task to issue credits.
7. **Time for weight and the window** *(Decided — D12: active network time.)* (N6): calendar time or active network time.
8. **Admission to tasks in B** *(Decided — D13: yes, the newcomer path from Variant A.)* (N16): should B introduce access depending on `H`, knowing that then
   B loses the constant low verification share. This is an input for D3.
9. **The price of a dispute** *(Decided — D14: the cheapest second-layer network; the network fee pays the difference.)* (N3): which chain to consider for the estimate of `G`, and who bears the
   difference `G − B` — the party in the right or the network.
10. **Should one pay for repeated verification and apprentice re-checks** *(Decided — D15: simple recomputation that can be copied is not paid.)* (2.2, N1), if a copy cannot
    be distinguished from a recomputation?
11. **An honest hardware failure:** *(Decided — D16: no; the task is not paid, the pending amount does not burn.)* should it be cancelled in the same way as cheating.
12. **The source of the `R/p` payment in B for requests** *(Decided — D17: only from user payments.)* (4.3): only from user payments or with issuance.

---

## 6. Who did what

The model council worked from the project materials, without network access and without experiments.

- **Round 1, six independent papers:** two ChatGPT papers, two DeepSeek papers, two Claude papers.
  Each compiled an adversary model, a reconciliation of the 60 rows, statuses for Variants A and B,
  data for rejection and new attacks.
- **Round 2, three critiques:** one each from ChatGPT, DeepSeek and Claude. Each critic read all six
  papers, checked the statements against the source documents, recalculated the formulas manually
  and pointed out discrepancies and errors.
- **Consolidation:** this document was compiled by Claude from the papers and critiques. Where the
  critics disagreed, the table says "disputed"; no new assessments of its own were added during
  consolidation.
