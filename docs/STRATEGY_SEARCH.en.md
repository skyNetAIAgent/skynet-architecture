<!-- translation of docs/STRATEGY_SEARCH.md, source sha256: 9c3fdac8710ac98433828b793ab6aad7fd31da5661c1fecb590bb7c63a2cdd26 -->

# Verification "not by brute force": what mathematics gives instead of full recomputation

**English** · [中文](../i18n/zh/STRATEGY_SEARCH.md) · [Español](../i18n/es/STRATEGY_SEARCH.md) · [Français](../i18n/fr/STRATEGY_SEARCH.md) · [Deutsch](../i18n/de/STRATEGY_SEARCH.md) · [Italiano](../i18n/it/STRATEGY_SEARCH.md) · [Русский](STRATEGY_SEARCH.md) · [Português](../i18n/pt/STRATEGY_SEARCH.md) · [العربية](../i18n/ar/STRATEGY_SEARCH.md)

Status as of 25 November 2026.

This document is the result of the fifth model council. The project owner asked, verbatim:

> "Maybe it makes sense to choose a different strategy? For example, bring in some
> mathematics? So as not to check everything in a row, but to predict an attempt at fraud and check only
> in that case? Or perform intelligent analysis of the operation of the skynet network and find suspicious
> behaviour? Think in this direction, what else is there in science that can help avoid solving by brute force."

The council examined the theory of inspection games, risk-based verification, anomaly detection, traps, sampled
verification, mechanisms without verification, cryptography and economics without deposits, and then proposed a
strategy and revisions of decisions.

**Document status.** This is the result of reasoning and calculation by formulas, not a measurement.
There were no experiments, network runs or installations for it. Participants and critics ran only
short arithmetic programs and small brute-force searches on a CPU. Measured numbers are taken only
from the [results of experiment D5](EXPERIMENT_D5.en.md) (D5_RESULTS summary as of 25 November 2026) and are marked
[measured]; numbers obtained by formulas from explicitly named parameters are marked [calculation]. Scientific
works are cited **from memory**: there was no network access, and the texts of primary sources were not checked. **The only adopted
decisions are decisions D1–D25** in [ROADMAP](ROADMAP.en.md), section 3. Everything else
here is the council's estimate and recommendations. Where critics disagreed, this is stated directly.

## 1. Brief summary

1. **"Predict fraud and verify only the suspicious" does not save verifications when the rules are open.**
   The verification rules are the same for all nodes and are known to the fraudster (D4). He submits a
   forgery only where the detector says "safe", and until the moment of fraud behaves like
   an honest participant. It has been rigorously proven: the detector raises the probability of verifying a forgery above the average
   verification of honest work by no more than the distance between their observable distributions
   (section 2). Therefore prediction, anomalies, history-based trust and graphs can only **add**
   verifications above the lower bound, but cannot lower the frequency below it. All six
   papers and all three critics agree on this.
2. **There are exactly two unforgeable features:** the result of exact recomputation after the response
   has been irrevocably fixed, and the burnable pending amount — the key's not-yet-paid rewards,
   which will be lost upon detection. All real savings come from the second feature, not from
   "intelligence".
3. **The best strategy found for model responses:** the payer verifies their response in one
   pass, and makes the decision "to verify or not" **with their own secret coin** after fixing the
   response, with probability not lower than `R/(R + H_lock)`. Here `R` is the task price, `H_lock` is the part
   of the performer's unmatured rewards that will not mature before the end of verification. A newcomer's response
   with an empty account is always verified. Then, under the conditions of section 4, forgery is not profitable
   for any collusion share of the others, including full collusion. Two of the three critics support this strategy;
   the ChatGPT critic prefers full verification of every response (section 6).
4. **The cost of verification itself is a fraction of a percent:** about 0.005–2% of work depending
   on the schedule and key load; for low-activity keys with a harm cap — up to 6.7%
   [calculation]. The main cost shifts to the exact profile: it is
   1.5–1.8 times slower than ordinary 8-bit generation at batch 1 and 2.5–2.8 times at
   batch 8 [measured]. Together this is +50…+82% over ordinary generation at batch 1 [calculation]. The 5%
   benchmark runs into the speed of the exact profile, not verification.
5. **Harm is not covered by economics.** A harmer does not need profit: under sampled verification, some
   of his forgeries pass (about half under the cheapest schedule, section 4). Therefore
   an unverified response must have the mark "unverified", and "verified" is set only after
   full verification before display. The council found no new guarantee for the training step.
6. **A user without equipment** is not protected by this strategy: if random third-party nodes verify
   on their behalf, the leakage equals `R·q^k` and under full collusion — the entire price (section 5).
   This remains open question D21.
7. **What the owner must decide:** whether to allow payment for the unverified under the coin rule
   (D21, D11, D7); what to do with free honest failures (D16), which are incompatible
   with sampled verification; whether to adopt new decision D26 on the "lock" of the pending amount and the limit
   of refund to the victim; the false-dispute rule (D23, calculation M9) remains a condition for enabling.
   The questions are formulated in section 6.

**Notation.** `R` — task price; `c` — cost of honest work; `c_f` — costs
of forgery (worst case — almost zero); `H` — pending amount of the performer's key;
`H_lock` — its part that will not mature before the final outcome of verification of this task;
`p` — probability of verifying the task; `q` — collusion share among verifiers; `k` — number of assigned
verifiers; `n_w` — number of key tasks per maturation window; `ρ` — time of verifying a response in one
pass divided by the time of its generation (0.10–0.40 at batch 1, 0.26–0.64 at batch 8
[measured]); `γ` — slowdown of the exact profile against llama.cpp Q8_0 (1.5–1.8 at batch 1, 2.5–2.8
at batch 8 [measured]); PPS — verification by the payer themselves. `Δ₀` and `Δh` — expected difference
in gain of forgery against inaction and against honest work; D1 and D25 require both to be
no greater than zero.

**How to read.** Section 2 — why predicting fraud does not work. Section 3 — a table of all approaches.
Section 4 — formulas that withstood criticism, and errors found. Section 5 — the recommended strategy,
its cost and residual risk. Section 6 — decision questions. Section 7 — calculations and experiments. Section 8 —
unresolved disagreements and questionable references. Section 9 — who did what.

## 2. Why "predicting fraud" does not work with open rules

### 2.1. A bound via total variation

Let the verification decision be made by any rule `π(x)` with a value from 0 to 1, where `x` is
everything the network or payer sees before the decision: response time, text, statistics, key history,
graph of connections. Honest work produces observations with distribution `P`, forgery — with distribution `F`.
Then

`E_F[π] − E_P[π] = Σ_x π(x)·(F(x) − P(x)) ≤ Σ_{x: F(x) > P(x)} (F(x) − P(x)) = TV(F, P)`.

The inequality holds because `π ≤ 1` where `F > P`, and `π ≥ 0` where `F < P`. The quantity
`TV` is the total variation distance: how distinguishable the two distributions are at all. Hence
(theorem T4 of paper claude2; the same inequality in gpt1 and gpt2):

1. **A forgery is verified no more often than honest work on average, plus `TV`.** If a forgery
   is hard to distinguish by observations (`TV ≈ 0`), the detector verifies it as rarely as honest
   work.
2. **Against a knowledgeable adversary it is still worse.** The rules are open (D4), so the adversary himself
   computes `π` and chooses the observation under which verification is least likely. The probability
   of detecting his best forgery equals the smallest `π(x)` among the observations that he can
   cheaply create.
3. **Implication for savings.** For forgery to be unprofitable, it must be verified with probability
   not lower than `R/(R + H_lock)` (section 4). At `TV ≈ 0`, the same frequency would have to be maintained for
   honest work as well, that is, there is no saving. According to claude2's estimate, the gain from "intelligence" is no greater than
   the factor `R/(R − c*)`, where `c*` is the price of the cheapest indistinguishable forgery; for a plausible
   `c* ≈ 0.5R` this is no more than a factor of two, but `c*` is chosen by the adversary, and it has not been measured.
4. **Key history says nothing about the moment of fraud.** A key that decides to defraud
   on the next task has, before that task, the same history as an honest one (likelihood
   ratio exactly 1; theorem T5 of claude2, counterexample of gpt1). Therefore sequential tests
   (Wald's SPRT, Page's CUSUM), bandit algorithms and Bayesian "trust" learn about it only
   after the fraud. A small brute-force search by claude1 showed: if the verification frequency based on trust is lowered
   by 10% below the threshold, a profitable strategy "accumulate trust and defraud" appears
   (+1.7R…+2.5R per 60 tasks); when lowered by half — +14.4R…+19.4R [calculation]. The Claude critic
   reproduced these numbers; the DeepSeek critic, in the closest model, obtained a different value (+0.085R),
   but the same sign (section 8).

### 2.2. An example on D5 measurements

The most natural cheap forgery is **the same Qwen run in llama.cpp Q8_0**. The exact
profile is slower than it by a factor of 1.5–1.8 at batch 1 and 2.5–2.8 at batch 8 [measured], so
the forgery is noticeably cheaper than honest work. At the same time, it is a response of the same model: time, style,
perplexity under a small model are the same as for an honest response, and the performer
can add delay himself. If the Q8_0 response matched the exact response token for token, it is not a forgery:
under D2 the result matters. If it diverged in at least one token, only exact
recomputation will detect this, because the bits of the exact profile match on any device tested [measured].

Caveat of the ChatGPT critic: D5 measured the closeness of the exact profile to the official model
(the same token in 90 out of 90 positions, logit correlation 0.9996 [measured]), while the closeness of the Q8_0 forgery
to the exact profile by cheap features was not measured. For the guarantee this is unimportant: it is enough that
no one has shown a feature distinguishing every available forgery from an honest response.

### 2.3. Where detectors are still useful

Detectors, traps and network analysis are admissible if they **only increase** the verification frequency:

- as a queue of additional voluntary verifications by the payer, which do not count
  towards the guarantee but increase real detection;
- against careless harmers who do not optimise their behaviour;
- for diagnosing hardware and driver failures; a participant can run CUSUM on their
  self-checks and stop before losing the pending amount;
- on a non-adaptive stream of errors they find more errors per hour of verification. Example by gpt1
  [calculation]: with a forgery share of 2%, sensitivity 90% and 5% false alarms, 8.57% of
  tasks are verified, 90.2% of this family of forgeries is caught, cost 1.80% versus 18.94% for uniform verification.
  But the family of forgeries that the detector does not flag is missed in 98% of cases.

There is also a reverse attack (claude2): requests for which an honest response looks "anomalous" force
verifications to be spent on honest participants. If the one who caused the verification pays for it, this is self-limiting;
if the network pays, it is a transfer of load.

## 3. Analysis of approaches

In the table, "guarantees" — what strictly follows under the named assumptions; "under `q`" — behaviour
under the collusion share of verifiers; "empty account" — a newcomer with `H = 0` and many free keys;
"verdict" — the result after three criticisms.

| Approach | Essence | What it guarantees | Under `q` and at `q = 1` | Empty account, many keys | Cost | Verdict after criticism |
|---|---|---|---|---|---|---|
| Inspection games (Dresher, Maschler, the Avenhaus–von Stengel–Zamir survey; security games of Tambe and co-authors — from memory) | A pre-announced random verification at a frequency at which fraud does not pay | `Δ₀ ≤ 0` at `p ≥ (R − c_f)/(R + H_lock)`, including for a batch of forgeries before leaving (under the conditions of section 4) | If the payer verifies, does not depend on `q`, including `q = 1`. If assigned verifiers — detection `p·(1 − q^k)`, at `q = 1` zero | `H = 0` ⇒ `p = 1`; each key answers with its own amount; Sybil does not help | `p·ρ`: hundredths to tenths of a percent for active keys; full verification for a newcomer [calculation] | **The basis of the strategy**, if the frequency is executed by the one whose money is at stake |
| Risk-based verification: SPRT, CUSUM, bandits, Bayesian trust | Verify newcomers and the suspicious more often, long-standing keys less often | Quickly catches a persistent noisy fraudster; against a strategist, nothing | The verdict by verifiers' opinions breaks under collusion; at `q = 1` zero | New keys are free; a "long-standing" key accumulates trust and defrauds at the end | The 40–70% saving (ds1) applies to a noisy adversary, not to SkyNet | Lowering the frequency below the threshold **is not allowed** (counterexample in section 2.1); additional verifications can be distributed |
| Anomalies, graphs, Sybil (time, logits, entropy, perplexity of a small model, watermarks, consistency of repeats, collusion graphs, SybilGuard/SybilLimit/SybilRank) | Look for suspicious behaviour and connections | Against a knowledgeable detector — nothing (bound of section 2.1) | Coherent forgery looks like honest agreement; at `q = 1` there is no protection | SybilRank requires trusted initial nodes and a small number of "attacker" edges; the coalition buys edges with honest work | Perplexity of a small model — about 1.3–5% of **every** response according to claude1's estimate (ChatGPT critic: at ds2's edges 1.875–9%) [calculation], more expensive than rule-based verification; a watermark certifies only the sampler | Only a **signal for additional verifications** and failure diagnostics |
| Traps, gold questions, Dawid–Skene model | Tasks with a known answer, indistinguishable from real ones | Only if the trap is indistinguishable and the answer is secret. In a public network, only the payer can keep the secret, and the trap coincides with their verification (T9 claude2) | Collusion instantly shares traps; Dawid–Skene assumes independent errors | One-time keys learn traps by probing; the task type (D22) is visible to the performer | A fresh reference for free text costs a full generation, more than verification (`ρ < 1`); for the `2⁻⁸⁰` level with a 10% trap share, 526–527 assignments are needed [calculation] | Not cheaper than verification by the payer; an admissible form is a repeat of an already verified payer request |
| Sampled verification and lottery (part of tokens or layers after fixing; BOINC, TrueBit, opML, proof of sampling — from memory) | Verify a small part of the computation; or pay only for what is selected by lottery (Lottery B) | Tokens: a single defect is missed with probability `1 − s/N` (99.2% with 8 positions out of 1000 [calculation]). Lottery B with verification of the selected one by the payer: `Δ₀ = −c_f` for any `p` | A lottery with a committee gives a newcomer `R·q^k`: 0.001R / 0.027R / 0.125R / R at `q` = 0.1 / 0.3 / 0.5 / 1, `k = 3` [calculation] | Lottery B with the payer is suitable for a newcomer; token sampling is not | Qwen3.5-4B state: 48 MiB + 64 KiB per position; one sample at position 500/1500/4000 — 79/142/298 MiB [calculation]; the lottery gives uneven income and requires prepayment `R/p` | Tokens and layers are **worse** than a full pass both in traffic and in guarantee; Lottery B with the payer is an admissible option. External systems rest on a deposit or on "one honest out of N" |
| Peer prediction (Prelec's Bayesian Truth Serum, peer truth serum, DMI — from memory) | Pay for consistency of reports without verification | Truthfulness is an equilibrium only without collusion; there are uninformative equilibria | At `q > 0` the group agrees; at `q = 1` the mechanism pays for anything | Free tickets from each key | No verification, but it is unknown what is paid for | **Inapplicable** to deterministic computation; payment for matching is payment for a copy, prohibited by D15 |
| Cryptography without a full proof, TEE, seed | Commitments and selective disclosures, dispute by halving, sumcheck/GKR, TEE attestation, deterministic generation | Sampling without encoding — the same bound `1 − s/N`; a full proof — yes under D19, but according to the stage 4 estimate, 16.8 times more expensive and more expensive for the response; TEE — trust in the manufacturer | Dispute and determinism do not depend on `q`; in TEE one extracted key compromises the entire fleet | Lowering the frequency by attestation would give the reduced frequency to all of the adversary's keys | Commitment to the response — 2–4 KB in the ledger (D24) | A commitment to the response, a secret coin and a split-half dispute are needed; TEE — only to increase verification or for privacy. ds1's proposal to lower the frequency by TEE was rejected by all critics |
| Economics without deposits (deferred payments, reputation as capital, insurance, price of a key by work) | Punish by loss of unmatured rewards and future income | The pending amount is the only lever compatible with R5. Future income upon leaving is zero. Insurance compensates the victim but does not reduce the fraudster's gain | Works if the frequency is executed by the payer | `H = 0` ⇒ full verification. Entry by work is a hidden deposit, useless upon leaving; with committee leakage `R·q³` and `q = 0.3`, the entry price `10R` is repaid by about 370 attempts (ds1) [calculation] | Delay of payment by the maturation window | `H_lock` is a mandatory part of the strategy; the rest does not serve as a basis for the guarantee |

## 4. Lower bounds and formulas that withstood criticism

### 4.1. A single forgery: threshold `R/(R + H_lock)`, not `R/H`

A caught forgery is not paid for and burns the pending amount (nothing more can be written off
under R5). Then

`Δ₀ = (1 − p)·R − p·H_lock − c_f ≤ 0  ⇔  p ≥ (R − c_f)/(R + H_lock)`,

and with an almost free forgery — `p ≥ R/(R + H_lock)`. Against honest work
`Δh = Δ₀ − (R − c) ≤ Δ₀`, so the second condition of D25 holds by itself. For a newcomer `H_lock = 0`,
and `p = 1`. Minimum frequency [calculation, claude2]: 0.5 at `H_lock = R`; 0.25 at `3R`; 0.0909
at `10R`; 0.01 at `99R`; 0.000231 at `4320R`.

Paper claude1 proposed the rule `p = min(1, R/H)` and called it exact. The Claude critic showed
by brute force that the exact threshold is `R/(R + H)`: with it the greatest forgery gain is exactly 0, while
with `0.99·R/(R + H)` it is from +0.225R to +0.299R [calculation]. The rule `R/H` contains a margin. The DeepSeek
critic noted that this margin is useful for harm: with `R/H` the expected number of forgeries before detection
is finite (about `H/R + 1`), with `R/(R + H)` — infinite (section 4.4). Which formula to take
into the core has not been decided (section 8).

### 4.2. Condition: the amount does not mature before the verification outcome

Only what has not yet been paid at the time of a proven dispute can be burned. If part of `H` manages to
mature earlier, the rule breaks. Counterexamples [calculation]:

- claude2: a key with `H = 99R`, maturing before the outcome, submits `n` forgeries at `p = 1%`;
  gain 0.99R at `n = 1`, 9.04R at 10, 36.6R at 100;
- Claude critic: a key with `H₀ = 100R` stops honest work and submits forgeries, while payers
  verify late; gain +0.99R, +9.1R, +49.7R, +74.4R at `n` = 1, 10, 100, 300. With a "lock"
  (everything burns), the same strategies yield from −0.01R to −0.75R.

Therefore the denominator of the frequency for task `i` includes only that part of the amount that will mature
**after** the dispute deadline for `i`, and the payer's verification deadline `δ` must be much less than the
maturation window `W`; both deadlines are counted in active time (D12). This is the
"timely verification" assumption; for a phone that rarely comes online, it is violated first.

### 4.3. Waves of forgeries before leaving

The single-forgery formula covers a batch of forgeries before leaving only under the rule
**"the first proven detection burns the key's entire unmatured amount, including the rewards of the same wave"**.

- Without this rule (gpt1): 10 parallel forgeries at `R = 1`, `B = 4R`, `d = 0.2`, when
  each missed one is paid for and the old amount is lost once, give
  `10·0.8 − 4·(1 − 0.8¹⁰) = +4.4295R`, although a single forgery gives zero. If detection annuls the entire
  wave, the same strategy gives −2.49676R [calculation; repeated by critics].
- The ChatGPT critic added a second example: at `H = R`, `p = 1/2`, two forgeries with independent
  coins and a one-time write-off of the old amount, the gain is `R/4` [calculation]. Hence the protocol must
  atomically bind all open obligations of the key to its entire unmatured revenue.

Under this rule, claude2's proof (T2) is correct: each new forgery multiplies the expected
outcome by `(1 − p_j)·(1 + α_j/(H_lock + A)) ≤ 1`, where `α_j` is the payment for the unverified, and `A` is the
already accumulated burnable amount. Induction over the number of forgeries gives `E[outcome] ≤ H_lock` for any batch
and any adaptive sequence. For a homogeneous batch the same follows from
`(1 + R/H)ⁿ ≥ 1 + nR/H`. A check on a grid of exact fractions gave a maximum excess of exactly 0
[calculation].

### 4.4. Verification by a committee: the factor `1 − q^k`

If detection must be recorded by at least one of the `k` assigned verifiers, and each
belongs to the coalition with probability `q`, the detection probability falls to `p·(1 − q^k)`, and the threshold
becomes `p ≥ R/((R + H_lock)·(1 − q^k))`. It is infeasible when `1 − q^k < R/(R + H_lock)`
and always infeasible at `q = 1`. In Lottery B with a committee, a newcomer receives `R·q^k` per attempt:
0.001R / 0.027R / 0.125R / R at `q` = 0.1 / 0.3 / 0.5 / 1 and `k = 3` [calculation]. This matches
the adversary model. Independence of choices is also an assumption: when choosing `k` different out of `N`
participants, of whom `C` are in collusion, the probability of full collusion equals `C(C,k)/C(N,k)`;
with general unavailability of data or selective disclosure it can reach `q` or 1
(ChatGPT critic, according to the adversary model). The conclusion of all papers: **the frequency must be executed by the one whose
decision is protected** — the payer for their money, each node for its own accounting.

### 4.5. Harm: the share of the undetected

A harmer does not need profit, so harm is measured by the share of his forgeries that pass undetected.

- **The cheapest schedule makes harm unlimited.** At `p = R/(R + H)`, unverified
  forgeries themselves increase `H`, and the frequency falls. The probability of surviving `n` forgeries from the start
  `h = H/R` equals `h/(h + n)`; the expected number of forgeries before detection is infinite (T8 claude2).
  claude1's estimate "`e^{−m}`" underestimates the miss: at `H₀ = 4320R` and 4320 forgeries the exact miss is
  0.50 instead of 0.37 at frequency `m·R/H` with `m = 1`; 0.125 instead of 0.050 at `m = 3`;
  0.0078 instead of 0.0009 at `m = 7` [calculation, Claude critic].
- **A single targeted forgery** passes with probability `1 − p`: for a mature key at
  `n_w = 4320` about 99.977% (ChatGPT critic) [calculation].
- **The fix based on the verified part of the amount did not hold.** claude2 proposed calculating the frequency
  from `H_ver` — rewards only for verified tasks; then for an honest key `p ≈ 1/√n_w`
  (fixed point `p²·n_w + p − 1 = 0`) and the harmer's forgery share about `p`: 5.6% at
  `n_w = 300`, 1.8% at 3000, 0.58% at 30,000 [calculation]. The Claude critic showed that `H_ver`
  is inflated by coalition self-paid requests; the ChatGPT critic — that a harmer with a new key
  after one verified response at `p = 1/2` achieves that approximately half of his delivered responses are false.
  No paper found an economic harm bound that withstands self-payment and new keys.

Conclusion: for any `p < 1`, part of the harmer's responses are false. For requests this is admissible only
with the mark "unverified" (text D6); for the training step — no.

### 4.6. Other formulas that withstood criticism

- **Free failures are incompatible with sampled verification** (claude1). If an honest failure
  does not burn the amount (D16), a caught fraudster calls the forgery a failure, and
  `Δ₀ = (1 − p)·R − c_f > 0`. With `b` free failures per window, the leakage is of order `b·H` per window
  [calculation].
- **Lazy payers** (claude2). If a share `λ` of payers do not verify, and the performer
  does not distinguish them, `p·(1 − λ) ≥ R/(R + H_lock)` is needed. If he does distinguish them — forgery against them
  brings up to `R` without risk. Deterrence is a public good: a payer who disables verification
  saves a fraction of a percent and loses nothing. This is the assumption that "payers on average execute
  the core's coin".
- **Cost and unevenness of Lottery B** (claude2, T7, with a correction by the ChatGPT critic). Payment `R/p`
  with probability `p` gives a coefficient of variation of income `√((1 − p)/(pT))` over `T` tasks.
  For a given spread `v`, `p ≥ 1/(1 + T·v²)` is needed; at `T = 6000`, `v = 10%`, `ρ = 0.21`
  the minimum verification cost is 0.3443% [calculation]. With verification "by each of 1000 nodes" the same cost
  is multiplied by the number of nodes, so a lottery with verification by all nodes is unsuitable for issuing credits.
- **Collusion of payer and performer** reduces to transferring their own money within the coalition, as long as
  the paid request does not create issuance of credits, weight and a right to compensation from the common pool.

### 4.7. Errors in the papers' formulas (briefly)

| Paper | Error | Correction |
|---|---|---|
| ds2 | The second threshold is written as `(c − c_f)/R` | It should be `(c − c_f)/(R + H)`; this threshold never binds. Pass only the corrected version to the mini-agents |
| ds1 | In the game the loss is taken as `L = H + V` without accounting for the already spent `c_f` | Threshold `(R − c_f)/(R + H + V)`; at `H = 0`, `c_f = 0.1R` — 90%, not 100% |
| claude1 | Inspection game equilibrium with `L = H + R` (double counting `R`) | Indifference point `(R − c_f)/(R + H)`: at `H = R`, `c_f = 0` — 1/2, not 1/3 |
| claude1 | "The rule `R/H` is exact"; harm `e^{−m}` | Exact threshold `R/(R + H)`; the miss is higher (section 4.5) |
| claude1 | Speculative generation "about `1 + ρ·s`" | Not derived; according to the DeepSeek critic — double counting; at batch 8 it comes out to 1.65–2.79 |
| claude2 | T7: "`κ·CV²` does not depend on `p`" | There is a factor `1 − p`; exact threshold `p ≥ 1/(1 + T·v²)` |
| claude2 | The summary cost 0.2–1.2% was taken at `n_w = 3000` | At `n_w = 300` — 0.56–2.24% (up to 3.6% at batch 8), at `n_w = 30` — 1.7–6.7% [calculation] |
| claude2 | State snapshots of 0.33 and 2.9 GiB per response | With attention cache 0.651 GiB (500/500, step 64) and 12.38 GiB (2000/1000, step 16) [calculation, ChatGPT critic] |
| claude2 | In S1, payment for the unverified `α` under the rule by `H_ver` is always equal to `R` | There is no smooth transition A/B in S1; a common beacon is not needed for the verification decision |
| ds1, gpt1, gpt2 | Strategy estimates without the slowdown of the exact profile | The full cost is 1.5–1.8 times higher already at batch 1 (section 5.2) |
| ds1 | "Verification of `k` tokens is not cheaper than a full pass" | In computation it is cheaper; it loses in state traffic and in guarantee |
| gpt2 | Certificate by logit bounds: 6.25% | The bounds require the true state of the last layer; the head is about 15% of multiplications, the saving is no greater than its share |
| ds2 | Steady fraud share against CUSUM `θ = d_h/(d_h + d_f)` | This is an approximation by average drift, not a theorem |
| ds1 | SPRT: 65 and 133 observations | Exact recalculation by the ChatGPT critic: 132.73 and 76.70, fixed test — 229 [calculation]; does not apply to a strategic adversary |

## 5. Recommended strategy

### 5.1. Model responses: "payer-inspector with a stake"

The core is taken from papers claude1 and claude2, corrections — from gpt1 and three criticisms.

1. **Exact profile.** Every paid response is generated in exact profile v2 (greedy choice
   or canonical Gumbel-max), and the ciphertext of the response is written to the ledger in one entry
   with acceptance (D24).
2. **The payer's secret coin.** After the response has been irrevocably fixed, the payer's program
   with its own secret randomness decides whether to verify it in one pass, with probability
   `p_i = max(p_user, R_i/(R_i + H_lock))`. `p_user` is chosen by the user themselves; at
   `p_user = 1` they see only verified responses. At `H_lock = 0` (newcomer) verification is always.
   A common beacon is not needed for this as long as payment does not depend on the coin's outcome; the decision does not wait for a
   public block.
3. **Lock of the amount.** `H_lock` for task `i` — the key's unmatured rewards that will mature after
   the dispute deadline for `i`; the verification deadline `δ` is much less than the maturation window (section 4.2).
4. **Burning.** Any proven discrepancy burns the **entire** unmatured amount of the key, including
   the rewards of the same wave. The victim is refunded no more than their payment `R`, the rest
   is destroyed. Otherwise a "self-dispute" attack is possible: a coalition, using its payer key, catches
   a deliberately forged self-paid request and takes others' amounts bypassing the maturation window
   (Claude critic).
5. **Marks.** "Verified" — only a response fully verified before display. Everything else
   is "unverified" by default. The mark "selectively verified" (claude1) was rejected by all
   critics as misleading.
6. **Signals only upward.** Anomalies, perplexity, graphs, repeats of verified requests
   (traps) trigger only additional voluntary verifications. Lowering the frequency by history,
   reputation, anomalies, attestation or the number of keys is prohibited.
7. **Disputes** — only by a proof of discrepancy, which every node verifies itself (I8).
   The strategy is not enabled without a false-dispute rule (D23, calculation M9).
8. **Option for keys with a small amount.** Where frequent verification is expensive for the payer, Lottery B is admissible:
   only the response selected by lottery is paid for, and its payer verifies it in full (gpt1,
   claude2). In it, a free honest failure (D16) is preserved unchanged, but the performer's income
   is uneven, and the payer holds a prepayment `R/p`.

The strategy requires changing D16 and D21 (section 6). All zeros of the guarantee are conditional: bit matching
on the devices tested, not on any devices; timely verification; ledger liveness and absence of
censorship of the proof; correctness of the core; honest execution of the coin by the payer's program;
the false-dispute rule.

### 5.2. Cost

Parameters: `p = R/(R + H)` at steady-state `H ≈ n_w·R`; `ρ` = 0.10 / 0.21 / 0.40 (batch 1);
`γ` = 1.5–1.8 (batch 1) and 2.5–2.8 (batch 8). The full cost against Q8_0 is `γ·(1 + p·ρ) − 1`.
Table of the Claude critic [calculation]:

| `n_w` (key tasks per window) | Steady `p` | Verification at `ρ` = 0.10 / 0.21 / 0.40 | Total against Q8_0, batch 1 | Total, batch 8 | Verifications in the first window of a new key |
|---|---|---|---|---|---|
| 30 | 3.23% | 0.32% / 0.68% / 1.29% | +50.5% … +82.3% | +152% … +186% | about 4.0 |
| 300 | 0.33% | 0.033% / 0.070% / 0.133% | +50.0% … +80.2% | +150% … +181% | about 6.3 |
| 4320 | 0.023% | 0.002% / 0.005% / 0.009% | +50.0% … +80.0% | +150% … +180% | about 9.0 |

Other schedules [calculation]: at the minimum frequency in money terms `p ≈ t_task/t_lock ≈ 2.3·10⁻⁴`
verification costs about 0.005% of work (DeepSeek critic); at the harm-limited frequency
`p ≈ 1/√n_w` — 0.18–0.72% at `n_w = 3000` and 0.56–2.2% at `n_w = 300`; with Lottery B at `p = 5%` —
0.5–2.0% at batch 1. If a harm floor by `H_ver` is added to the money rule, verification
grows to 0.15–2.2% at `n_w` = 300–4320 and to 6.7% at `n_w = 30` (Claude critic). A newcomer's first task
costs full verification, 10–40% of its generation.
For comparison: full verification of every response (the main contract of gpt1, gpt2, ds2) costs
`γ·(1 + ρ) − 1` = +65…+152% against Q8_0; at `γ = 1.65`, `ρ = 0.21` — +99.65% [calculation].

Not calculated: writing 2–4 KB per response to the ledger, false disputes (M9), energy, verification
on payers' devices. **The bottleneck of the 5% benchmark is the slowdown of the exact profile, not
verification.** Fast bit-for-bit identical kernels and exact speculative decoding can reduce it:
a draft is generated by fast Q8_0, and the exact profile accepts the prefix up to the first divergence.
claude2's estimate at 99% token match and block 32 — about 0.78 of the exact token time, that is,
+28% over Q8_0 instead of +65%; at 95% match — 1.33 of the exact token time, worse than direct generation
(Claude critic) [calculation; the match has not been measured].

### 5.3. Residual risk

Expected gain per forgery; "harm" — the share of the harmer's undetected forgeries, all of them
with the mark "unverified". Summary of the Claude critic and the DeepSeek critic [calculation].

| Case | `q = 0.1` | `q = 0.3` | `q = 0.5` | `q = 1` | Newcomer, `H = 0` |
|---|---|---|---|---|---|
| Money, payer verifies themselves | ≤ 0 | ≤ 0 | ≤ 0 | ≤ 0 | `−c_f` (verification always) |
| False response shown as "verified" | 0 | 0 | 0 | 0 | 0 |
| Harm at `p = R/(R + H)`: not caught after `n_w` forgeries | about 50% | about 50% | about 50% | about 50% | 0 (the first ones are verified) |
| Same at `p = 3R/(R + H)` | about 12.5% | same | same | same | 0 |
| Payer without equipment delegates verification to a random triple | +0.001R | +0.027R | +0.125R | +R | same |
| Payer does not verify, performer distinguishes them | up to +R | up to +R | up to +R | up to +R | 0 |
| Training, there is an honest auditor of full frequency | ≤ 0 | ≤ 0 | ≤ 0 | — | `−c_f` |
| Training, there is no honest auditor | up to +R | up to +R | up to +R | up to +R | up to +R |

The rows "payer verifies themselves" do not depend on `q`. This is the main result of the council:
verification independent of the collusion share is cheap for the payer if they verify selectively,
and the performer's burnable amount is locked until the end of verification.

### 5.4. Newcomer

A key with an empty account is always verified, so forgery by it gives `−c_f`. As the locked
amount accumulates, the frequency falls: under the rule `R/(R + H)`, in the first window about 4.0 / 6.3 / 9.0 full
verifications at `n_w` = 30 / 300 / 4320 (Claude critic), under the rule `R/H` — 5.0 / 7.3 / 10.0
(claude1) [calculation]. The cost of the first window at `n_w = 30` — 1.7 / 3.5 / 6.6% at `ρ` = 0.10 / 0.21 / 0.40
(claude1) [calculation]. The "entry price" is useful work verified in full, not an entrance
fee. The reverse side is load: a coalition of new keys forces payers to verify every
one of their responses. This hits the cost (R6), but not D1; the magnitude must be calculated (section 7).

### 5.5. User without equipment

The strategy does not protect them. If they delegate verification to a random triple of third-party nodes, the expected
leakage `R·q³`: 0.001R / 0.027R / 0.125R / R at `q` = 0.1 / 0.3 / 0.5 / 1 [calculation]. If they
delegate it to their own device or an acquaintance's node, this is their assumption under D21; if the helper colludes
with the performer, false assurance is possible with probability 1. The Claude critic proposes to check
by experiment how much verification in one pass costs on a laptop and phone CPU: at a frequency
of about one verification per key window, a rare slow verification may turn out to be acceptable.
The guarantee for such a user remains open question D21.

### 5.6. Training

For the training step the council found no new guarantee. A step has no payer whose money is at stake,
so sampled verification must be executed by every node that needs the guarantee, and the cost
is multiplied by the number of such nodes. Options:

- **Full repeat of the step** from the accepted parent — about 100% of the step's work for each verifying
  node. Example of the ChatGPT critic: if inference is 80% of the base work, `ρ = 0.21` and each step
  is repeated once, the result is 0.8·0.21 + 0.2·1 = 36.8% above the base work [calculation]; with `N`
  independently verifying nodes the second term is multiplied by `N`.
- **Sampled verification of the step by all full nodes** (claude2, S2): for money only, with a window
  of 3 days — 0.23% / 2.3% / 23% of the network's work at 10 / 100 / 1000 verifying nodes; with a harm
  limit of 10% — 10 times more expensive [calculation; the harm column is not rigorously derived]. It requires exact
  integer training, which has not been built or measured.
- **Audit "one honest out of N"** (claude1, S2) — this is an assumption that stage 4 has already rejected for
  training; without a paid audit, the equilibrium is "there are no auditors".
- **Payment for proven improvement (D18)** — not verification of the step; calculation M12 has already shown that an exact
  duplicate of a submission increases the owner's accrual under all three attribution rules (calculation
  of the mini-agents, D5_RESULTS summary).

Robust aggregation of contributions (Krum, median, trimmed mean — from memory) limits the harm
of the undetected share, but does not protect against coordinated harmers with a noticeable share of weight and does not satisfy
D1. An unverified step must not enter the released version of the model (D6).

## 6. Decisions that need to be changed or adopted

The formulations below are **council recommendations**, not adopted decisions. Each question must be adopted
or rejected explicitly. The immutable requirements R1–R6 are not changed by editing a roadmap line
(reminder by gpt1).

**Question 1 (D21, as well as D11 and D2). Should the payer be allowed to pay from their prepayment for a response
that their program, under the core rule, did not verify?** Currently D21 says: "The network does not pay for a response without
verification", and D11 — "only the verified is paid for".
*Recommendation (Claude critic, based on papers claude1 and claude2):* yes. The proposed second sentence of D21:
"The payer pays from their prepayment for a response that they verified or skipped under rule D7
with their secret coin; a skipped response has the mark "unverified". There is no issuance of credits and weight
for the paid request". At the same time D11 must be clarified (and, according to a remark of the DeepSeek critic,
D2), otherwise the amendments contradict each other.
*Where they disagreed:* the DeepSeek critic — do not change D21 yet (the strategy is anyway blocked by D23)
and use Lottery B (`α = 0`, payment `R/p` to the selected one), compatible with the current D2, D11, D21.
The ChatGPT critic — keep full verification of every response by the payer as the main contract,
and introduce payment for selected ones from a batch by a separate contract; without independent verification there is no network payment.

**Question 2 (D7). How should it be written down which verification is admissible for payment?**
*Recommendation (Claude critic):* "Verification independent of the collusion share is mandatory for the mark
"verified", for issuing credits and for weight. Payment for a request from the payer's funds is allowed
after verification by the payer or after skipping verification under the core rule: the payer's secret coin,
tossed after fixing the response, with probability not lower than `R_i/(R_i + H_lock)`.
Lowering this probability by history, reputation, anomalies, attestation or the number of keys is prohibited;
raising it is allowed. Verification by assigned verifiers does not serve as a basis for payment. D1
is not weakened to `q < q*`". Separately, one must choose `R/(R + H_lock)` (exact threshold) or `R/H`
(with a margin, a finite number of the harmer's forgeries before detection).
*Where they disagreed:* the DeepSeek and ChatGPT critics propose not to change the text of D7, but to add the scope
of application: the guarantee to the party that performs verification itself does not depend on `q`; the party
that delegated verification is protected only if the collusion share of the assigned ones is below `q*`, and this is shown
to it (DeepSeek critic). The ChatGPT critic adds: rating, quorum, expiry of the term
and the assumption `q_eff < q*` do not give a right to independent status.

**Question 3 (D6). Should the result marks be clarified?**
*Recommendation (common to the critics, wording based on ds1):* "A false response is not issued as
"verified". There are two marks: "verified" — full verification before display by a method independent of the collusion
share (for a request — by the payer personally, or by a proof accepted by the core); "unverified" —
by default, set automatically; only such verification can remove it. Streaming output —
by verified blocks or with this mark. An unverified training step does not enter the released
version of the model". The ChatGPT critic clarifies: an unverified step and its descendants can only be
in an isolated research branch without payment for the transition.
*Where they disagreed:* in substance they did not disagree; claude1 proposed a third mark "selectively verified" —
it was rejected by all three critics.

**Question 4 (D16). What to do with an honest hardware failure?** Currently a failure is not punished, and the amount
pending does not burn. Under sampled verification with payment for the unverified this is a direct leakage
(section 4.6).
*Recommendation (Claude and DeepSeek critics, based on claude1):* "Under full verification or Lottery B, an honest
failure is not punished (the previous rule). Under sampled verification with payment for the unverified, any
proven discrepancy burns the key's `H_lock` regardless of the cause, since the cause cannot be established
from an identical erroneous output. The expected loss of the honest participant (about `P_f·R` per task, where
`P_f` is the probability of a silent failure) is compensated by an unconditional surcharge from the network fee. The rule
is enabled only after measuring `P_f`".
*Where they disagreed:* ChatGPT critic — preserve protection against honest failure: a failure leaves the result without
payment, previous rewards are preserved, the number of failures per key is limited, and the reliability of the calculation
must not depend on writing off previous rewards. He also notes that a surcharge from others' collection
for each task increases the payment to forgery as well and changes the threshold. The Claude critic adds: burning
an income window for unmeasured instability hits weak nodes (R6), and the surcharge compensates the average,
not the risk of ruin. The dispute is resolved by the choice of payment structure (Lottery B preserves D16, payment
for the unverified does not) and by measuring `P_f`.

**Question 5 (D8). How should the dispute deadline and rights be arranged?**
*Recommendation (Claude critic):* "The payer submits a proof of discrepancy no later than the deadline `δ`
of active time after receiving the response; the dispute is resolved only by a proof that every
node verifies itself". *Addition (ChatGPT critic):* the performer has the right to demand settlement
for their fixed order in case of an unjustified refusal or silence of the buyer; both parties
dispute from a zero account without a deposit; a duplicate does not launch a new expensive verification; until a decision
the disputed amount remains pending. Here there is an open fork: if payment is made after the expiry of the term
without objection, the payer's absence pays for the forgery; if one refuses on silence, a dishonest
payer receives a correct response for free.
*Where they disagreed:* claude2 and the DeepSeek critic propose, after M9, to allow any node to dispute
a task selected by the beacon, with a quota of false disputes; the Claude critic considers this empty for a private
request (an outside node has no request) and useful only for training.

**Question 6 (D23). Should the block until calculation M9 be retained?**
*Recommendation (all three critics):* retain it. Add (Claude critic): "M9 is calculated for rule
D7: disputes are rare in equilibrium, but a coalition "payer = performer" can submit them as many
as it likes for self-paid requests; the burned amount is destroyed, and the victim is refunded
no more than their payment". The ChatGPT critic proposes to write down the criterion for removing the block: upper
bounds on bytes, computations, messages and deadlines per case, a limit on simultaneously open cases,
the source of load coverage, a check of format and uniqueness before expensive recomputation, resistance
to self-paid requests, collusion of both parties, false refusal of the buyer, network partition
and unavailability of data.

**Question 7 (new D26). Should a decision be adopted on the lock of the pending amount and the refund limit?**
*Recommendation (Claude critic, with the corrections of section 4):* "`H_lock` of task `i` — the key's unmatured
rewards that will mature after the dispute deadline for `i`; the payer's verification deadline
is much less than the maturation window. A proven discrepancy burns the entire unmatured amount of the key, including
the rewards of tasks submitted after the disputed one and in the same wave. The victim payer is refunded
no more than their payment for the disputed response; the rest is destroyed; the first dispute does not take amounts
due to other payers". Without this rule the strategy of sections 5.1–5.3 does not hold
(counterexamples +4.4295R and up to +74.4R in sections 4.2–4.3).
*Where they disagreed:* the ChatGPT critic does not discuss the lock in this form, since he does not support payment
for the unverified; but he himself requires atomically binding open obligations to the entire unmatured
revenue.

**Question 8 (D1). Should D1 be changed?**
*Recommendation (all three critics):* do not weaken the text. The variants "D1 while the collusion share is less than `q*`"
and "leakage no more than `ε` of turnover" (claude1, ds1, ds2, gpt1) were rejected: at `q = 1` they give
the coalition the entire unverified output, contradict D19 and immutable R4, and "turnover" is inflated
by self-dealing. The Claude critic proposes a note: for a model response, D1 is ensured with respect
to the payer who executes the core verification; sampled verification with their secret coin fulfils
D1 as an expectation and is recorded as an assumption about a rational adversary (under R4, statistical sampling is
an assumption); for a consumer who does not verify, the network does not promise D1. The DeepSeek critic — a note that
the guarantee D1 applies to every result with the mark "verified" and to every issuance of credits.

## 7. What the mini-agents should calculate and what should be checked by experiment

### 7.1. Exact calculations (fractions, control hash, repeat on a second device)

1. Complete brute-force search of rule D7 with amount maturation, waves, several keys, different prices
   in a wave and retrospective verifications. Reference values: `κ = 1` → 0; `κ = 0.9` at `H₀ = 0` → +1.734R
   (reproduced by the Claude critic, not reproduced by the DeepSeek critic — the brute-force search must decide);
   `0.99·R/(R + H)` → +0.225R; maturation counterexample +0.99R / +9.08R / +49.7R / +74.4R.
2. gpt1's wave formula: +4.4295R with separate write-off and −2.49676R with burning of the entire wave.
3. The "self-dispute" attack: at what refund share to the victim the gain becomes positive.
4. Leakage of free failures (`b` per window) and the surcharge `P_f·R` with a spread of honest losses.
5. Harm under schedules `H_lock`, `H_old`, `H_ver`, `m·R/(R + H)` with self-payment and new keys;
   reference values 0.50 / 0.125 / 0.0078 at `n_w = 4320`.
6. Lazy payers: the share `λ` and distinguishability at which deterrence disappears.
7. The load of a coalition of new keys on payers at `p = 1` for newcomers.
8. M9 (false disputes) for rule D7 — condition D23.
9. Summary cost `γ·(1 + p·ρ)` on a grid of measured `γ`, `ρ` and the distribution of `n_w`.
10. Probability of full collusion with selection without replacement (`C(C,k)/C(N,k)`) and with lottery rounds.
11. Sizes of state snapshots under the pinned model configuration (M1) — the dispute about the cost of sampled
    tokens and snapshots.
12. The corrected ds2 threshold and the gpt2 control script (SHA-256 begins with `58aec3b0`
    and ends with `cd07ba`; it matched for the Claude and DeepSeek critics).
13. Exact SPRT and CUSUM chains on finite grids, including a change of behaviour after a good history.
14. Trap tables `(1 − g·θ·d)^m` for the levels `10⁻³`, `10⁻⁹`, `2⁻⁸⁰`.

### 7.2. Only by experiment

Experiment D5 permits work with integer Qwen3.5-4B within the scope O1–O5 of its protocol. **Everything else —
only with separate permission from the owner.**

1. Within D5: fast bit-for-bit identical kernels (O3, O4) — the only path to approach 5%;
   the verification share on payers' devices and at batches 1, 8, 32; O5 — quality on 320 tasks.
2. Outside D5: exact speculative decoding — the distribution of the matching prefix length of Q8_0
   and the exact profile on long responses.
3. Outside D5: the frequency of silent discrepancies `P_f` during long operation on voluntary devices — before
   any change to D16.
4. Outside D5: time and memory of verification in one pass on a laptop and phone CPU.
5. Bit matching on edge inputs (overflow, ties, early end of response) and on new
   drivers; on the RX 580 a long pass over a finished response was interrupted by the driver [measured].
6. Outside D5: O9 (energy), O6 (LoRA improvement noise), O7 (cost of a block proof), integer
   training — a prerequisite of any step verification scheme.
7. Outside D5, optionally: how distinguishable cheap forgeries are by features. This does not give a guarantee
   for any outcome, but only refines the ceiling of section 2.1.

## 8. Unresolved disagreements and questionable references

### 8.1. Disagreements

1. **Whether sampled verification by the payer fulfils literal D1.** claude1, claude2, the Claude
   and DeepSeek critics — yes for money, no for harm. ds1 and ds2 — full verification is needed (the critics
   believe they did not notice verification by the payer at a frequency based on the locked amount). gpt1, gpt2
   and the ChatGPT critic — full verification of every response, and payment for selected ones — only by a separate
   contract for batches. The decision whether the expected gain is sufficient under the first sentence of R4 is for
   the owner.
2. **`R/(R + H_lock)` or `R/H`.** The first is exact for money, the second gives a margin and a finite expected
   number of forgeries before detection; the difference in cost is about a factor of two at a small amount.
3. **Whether to pay for the unverified** (`α = R` or claude2's smooth G(α)) **or only for the selected**
   (`α = 0`, Lottery B). Depends on the amendment of D2, D11, D21 and on the unmeasured unevenness of income.
4. **Beacon or secret coin.** claude2 — a common beacon (D20); claude1 and the Claude and DeepSeek critics —
   the payer's secret coin, the beacon is needed only at `α < R` and for disputes of third nodes. The ChatGPT
   critic: a secret coin is suitable for personal verification, but cannot dispose of the common prize;
   when choosing the convenient of two independent beacon outcomes, detection falls from `p` to `p²`.
5. **D16** — section 6, question 4.
6. **Harm bound** — no scheme withstood self-payment and new keys.
7. **Training** — audit "one out of N" (claude1), verification by each full node with branch rollback
   (claude2), D18 or full repeat (ds1, ds2, gpt1, gpt2); no scheme fulfils D7 at
   `q = 1`.
8. **claude1's brute-force values** (+1.73R at `κ = 0.9`): reproduced by the Claude critic,
   not reproduced by the DeepSeek critic (+0.085R in the closest model); the sign is the same for both.
9. **Speculative decoding:** 1.15–1.38 (claude1) versus about 0.78 of the exact token time
   (claude2); both have not been measured.
10. **Traps:** ds2 calculates the required number of traps, claude1 and claude2 prove that
    in a public network a trap coincides with verification by the payer. The conclusions are compatible.

### 8.2. References to literature marked by critics as questionable

All references are given from memory, without checking the texts.

- SybilGuard and SybilRank under the common "Yu and co-authors" (ds1): according to the critics' memory, SybilGuard and SybilLimit —
  Yu and co-authors (2006, 2008), SybilRank — Cao and co-authors (2012); the year of SybilRank itself is marked
  by the Claude critic as uncertain.
- "Proof of Sampling (2024)" and "Verde (Gensyn, 2025)" (claude1, claude2) — the papers themselves write
  "not sure"; the design of the mechanism has not been confirmed.
- Peer Truth Serum as a work of Witkowski and Parkes (2012) (ds2): the Claude critic considers this
  questionable (according to his memory, they have "robust BTS", while the name belongs to Radanovic
  and Faltings), the DeepSeek critic — correct. Disagreement.
- DMI as a work of Kong and Schönbeck (2019) (ds1, ds2): questionable according to the memory of the Claude
  and ChatGPT critics (DMI is a work of Kong around 2020); the DeepSeek critic considers the attribution correct.
- "Self-prediction attacks on BTS by Radanovic and Faltings" (ds1) — questionable.
- "Gao, Wright and Leighton-Brown (2016)" on the superiority of sampled verification over peer prediction
  (claude2) — the year is not confirmed (DeepSeek critic), the unconditionality of the conclusion is questionable (ChatGPT critic).
- Kreps and Wilson (1982) as the basis for "reputation works only over a long horizon" (claude1) —
  questionable (ChatGPT critic).
- DetectGPT as a justification for the perplexity threshold of a small model (ds1) — incorrect: it studies another
  property (ChatGPT critic).
- The general miss formula `(1 − f)^s` as a property of BOINC, TrueBit, opML (ds1, ds2) — does not follow from their
  protocols.
- The references of ds1 and ds2 to "0.3–0.7% / 0.33–0.66% of exam tokens" and "about 2.4 hours per candidate"
  were not found in the input documents.

## 9. Who did what

The model council worked from the project materials, without network access and without experiments.

- **Six independent papers:** two papers by ChatGPT (gpt1, gpt2), two papers by DeepSeek (ds1, ds2),
  two papers by Claude (claude1, claude2). Each analysed seven directions from the assignment, added
  its own, checked them against decisions D1, D6, D7 and proposed strategies with cost and residual risk.
  Short arithmetic programs and small brute-force searches were run by claude1 (brute-force search of strategies
  against the frequency rule), claude2 (grid of exact fractions), gpt1 and gpt2 (gpt2 attached a control
  script with a hash).
- **Three criticisms:** one each from ChatGPT, DeepSeek and Claude. Each critic read all six papers,
  looked for errors and counterexamples, and recalculated the key numbers. The Claude and DeepSeek critics repeated
  gpt2's control script, the hash matched; the Claude critic repeated claude1's brute-force search, the DeepSeek critic
  did not reproduce its values.
- **Consolidation:** this document was compiled by Claude from the papers and criticisms. No new estimates or numbers beyond
  the papers, criticisms and D5 measurements were added; where the critics disagreed, this is stated.
