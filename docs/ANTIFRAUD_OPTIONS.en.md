<!-- translation of docs/ANTIFRAUD_OPTIONS.md, source sha256: 63c43d6864c5cccb6fa61953c9ba9594e26e3dba1a4c8241129e6f346bc08f20 -->

# Options against fraud: the result of audits and the model council

**English** · [中文](../i18n/zh/ANTIFRAUD_OPTIONS.md) · [Español](../i18n/es/ANTIFRAUD_OPTIONS.md) · [Français](../i18n/fr/ANTIFRAUD_OPTIONS.md) · [Deutsch](../i18n/de/ANTIFRAUD_OPTIONS.md) · [Italiano](../i18n/it/ANTIFRAUD_OPTIONS.md) · [Русский](ANTIFRAUD_OPTIONS.md) · [Português](../i18n/pt/ANTIFRAUD_OPTIONS.md) · [العربية](../i18n/ar/ANTIFRAUD_OPTIONS.md)

State as of 27 November 2026.

**What has been done.** The project owner collected six independent completeness audits and two maps
of anti-fraud mechanisms and proposed three ideas of his own: to build verifiability into the model
itself, to borrow techniques from games and to "crossbreed" verification workarounds with useful work. The model
council wrote eleven independent papers and four cross-criticisms and consolidated all this
into the options described below.

**Status.** This document is reasoning and calculation. Measured quantities are taken only from experiment D5
([EXPERIMENT_D5](EXPERIMENT_D5.en.md)) and are marked [measured]. Everything else is marked [calculation] or
called an assumption. The only adopted decisions remain D1–D25 ([ROADMAP](ROADMAP.en.md),
section 3); everything that is proposed here to be changed is a council proposal, not a decision. The council
performed no new experiments, prototypes or installations. The literature is cited from the models' memory or
from the audits' data and has not been checked against primary sources. Previous summaries:
[STRATEGY_SEARCH](STRATEGY_SEARCH.en.md) and [HIDDEN_DETECTOR](HIDDEN_DETECTOR.en.md).

**Notation.** `R` — task price; `c` — cost of honest work in the exact
(integer) profile; `c_f` — the fraudster's cost of forgery; `H_lock` — the key's locked
unmatured amount; `p` — probability of verifying a response; `q` — the share of the coalition's weight among
assigned verifiers; `ρ` — time to verify a finished response in one pass as a fraction of the time
of its exact generation: 0.10–0.40 at batch 1 and 0.26–0.64 at batch 8 [measured]; `γ` — slowdown
of the exact profile relative to ordinary Q8_0: 1.52–1.78 at batch 1 and 2.47–2.79 at batch 8
[measured, RTX 2060 only].

## Brief summary

1. **The expensive part is not verification but exact computation.** Verifying one response costs 10–40% of its
   generation [measured], but the main surcharge is the slowdown of the exact profile by a factor of 1.52–1.78
   [measured]. The "about 5%" benchmark is unattainable with the current kernels in any option, however
   rare the verification [calculation].
2. **The idea of "fingerprints and recomputation of a random chunk" works, but not as a way to make the guarantee cheaper.**
   If `s` chunks out of `N` are revealed, one deliberately substituted cell passes
   with probability at least `1 − s/N`. The estimate "30 times cheaper, while fraud is still caught"
   actually means "30 times less detection". Fingerprints are useful in another role: a short trace
   root allows a dispute to be resolved by halving down to one step and gives a weak device
   a partial verification with an honest mark.
3. **The idea of "verifiability inside the model" works in one form:** fine-tune or rewrite
   the kernels so that the exact profile becomes fast. This reduces `γ` and does not weaken the guarantee.
   Fingerprints are written by a program, not by the model, and fine-tuning is not needed for them. Checksums
   in layers protect an honest performer from hardware failures, but not from intent.
4. **Only the order of moves transfers from games:** "sealed → final fixing → secret
   choice → reveal → recomputation". Only two moves are coupled to the calculation: recomputation of the revealed chunk
   and verification of the task witness. A separate game next to useful work proves nothing.
5. **There are four options and one add-on:** full verification of every response by the payer;
   a lottery over whole orders; the payer's secret coin with a locked amount; tasks
   with a verifiable outcome; and exact speculative decoding as a possible way to cheapen
   the first and third options.
6. **Recommendation.** The main contract is full verification of every response by the payer in the exact
   profile. It alone fulfils the adopted decisions without amending them. Tasks with a verifiable outcome are
   a separate type of task and so far the only strict guarantee for training. The lottery is a tariff
   for batches. The coin with a locked amount remains a candidate until calculation M9 and the owner's decisions.
7. **The first step.** One calculation: M9 — false disputes without a deposit, all branches of silence and refusal.
   One experiment (with the owner's permission): on the already assembled profile v2 and llama.cpp Q8_0, measure
   token agreement under a common prefix. It decides three questions at once (section 5).
8. **Literally infeasible:** to protect a consumer without equipment under full collusion of
   verifiers; to verify the training step under full collusion within a 20% surcharge; to fit
   a verified response into 5% at the measured `γ`. The minimal relaxations are formulated
   as questions to the owner in section 7.

## 1. What the audits found

Audit labels: RU — `SkyNet_audit_completeness_RU`; SC — `skynet_completeness_audit`; GPT —
`gpt-SkyNet-audit`; DS — `deepseek-AUDIT_REPORT`; GEM — `gemini_report`; CR — `chat_responses`;
maps — `mehanizmy-anti-obman` (MEH) and `mechanisms_map_report` (MAP). Where the council's papers
disagree on who named what, this is marked with the word "disputable".

### 1.1. Missed approaches

| Approach | Which audit named it | Council's assessment |
|---|---|---|
| Activation fingerprints, TOPLOC | SC, GPT, GEM, CR, DS (in one line), MAP; MEH — disputable | Not a basis for payment; only a signal for additional exact verification (section 2.4) |
| Optimistic schemes, dispute with an arbiter, halving | All six and both maps | A necessary dispute layer; under full collusion there is no one to dispute with, so not a replacement for the payer's verification |
| Statistical tests of model substitution | GPT, DS, GEM, CR, MAP; SC and RU — disputable | Only a signal for increasing the verification frequency; not part of the core |
| Reproducible floating-point arithmetic, integer kernels of the Ozaki type | SC, GEM, DS, GPT, RU; CR calls them RepOps | Floating-point arithmetic does not replace the integer profile; kernel acceleration is a hypothesis for experiment |
| ABFT checksums | SC, GEM, DS, GPT, RU | Self-check of an honest node against failures; covers only linear multiplications |
| Freivalds verification | SC, CR, GPT, GEM, maps | Works for the linear part of exact arithmetic with a fresh secret vector after fixing |
| Data availability | SC, DS, GPT; GEM — against; RU and maps — disputable | Engineering of dispute and training, not an R4 guarantee |
| Mechanism design with expensive verification | GEM, DS, GPT, SC | Confirms the threshold `R/(R + H_lock)`; gives no new lever |
| Hardware attestation of GPU, TEE | Almost all | An additional signal and a privacy mode; the verification frequency cannot be lowered based on it |
| Surety and insurance without a participant's deposit | SC, GEM, DS, GPT, RU | Someone else's lock is essentially a third party's deposit, a question for R5; an insurance fund opens self-dispute |
| Experience of Bittensor, Gensyn, Prime Intellect, Hyperbolic, Ritual, Atoma, Golem | All six and the maps | All rest on a deposit, trusted validators, TEE or "one honest"; individual techniques are transferable |

Named by only one audit: layer-wise sampling proofs as a basis (RU), binding the response
ciphertext to the commitment via DLEQ (SC), a coupon pool (SC; according to one paper —
also GEM and GPT).

### 1.2. Weak points of previous conclusions

- The threshold `p ≥ R/(R + H_lock)` is correct under three conditions that had not been named before: the price
  is not below cost, the coin is actually tossed, the amount is available for burning
  (GPT, SC, GEM, RU).
- The conclusion "the 5% benchmark is refuted" applies to one implementation of kernels (GEM, SC, DS).
- The succinct-proof barrier is calculated for one layout (SC, GEM, DS, GPT).
- Bit agreement is shown on six configurations, not "on any hardware" (DS, GEM, SC, GPT).
  The critics clarified: for a long pass over a finished response — on three.
- The statement "a lazy payer and a newcomer together give zero" was an error: the gain is up to `+R`.
- The brute force of "92 million strategies" does not prove completeness (RU).
- The literature of previous councils is cited from memory (RU, GEM, DS, GPT).

### 1.3. Contradictions of requirements and decisions

- **D16 versus sampled verification.** If an honest failure is not punished, the fraudster declares
  the forgery a failure and receives `(1 − p)·R − c_f` (DS, GEM, RU, SC).
- **D19.** The third condition — "the error multiplied by `R` is less than the price of the attempt" — is inapplicable
  when the attempt is free (DS, RU; in the council — ChatGPT).
- **Issuing credits for training at zero demand**, full collusion, a 20% surcharge and verification
  by every node are not fulfilled together (DS, SC, GEM, GPT, CR, MEH).
- **A consumer without equipment and R4** (SC, GEM, RU, CR).
- **Literal D1 excludes any sampling** (RU, DS).
- **A dispute without a deposit and a finite dispute fund** (SC, GEM, GPT, RU).
- **"First full confidence, then experiments"** was called a vicious circle: `γ`, `ρ`, quality
  and the failure rate are established only by measurement (DS, GPT). This is the opinion of the audits and one
  critic; the council did not violate and does not cancel the current restriction on experiments.

### 1.4. New attacks

- **Lazy payer.** If a share `λ` of payers do not verify, the threshold becomes
  `R/((1 − λ)(R + H_lock))`; with an empty account it is greater than one, and a fraudster who has recognised
  a lazy payer receives up to `+R` (SC) [calculation].
- **The coin is not enforced:** the payer's program can be rebuilt with `p = 0` (GEM, SC).
- **Resale of a response between sessions** ("mafia attack"): an intermediary takes an order, buys the response
  from an honest performer and does not pay. It works without collusion of verifiers; it is cured by the order
  "prepayment locked → response → verification on time → payment" (GEM; developed in the council).
- **Sale of an unmatured amount** before leaving (RU). Cured by a ban on transfer.
- **Self-payment** increases the locked amount and lowers the verification frequency. Criticism showed
  that this does not open the money (the fraudster's own money burns upon detection),
  but it cheapens targeted harm.
- **Flooding with free keys:** each new key requires full verification
  and loads the payer; this is a denial of service, not theft.
- **Substitution of one or two tokens inside the TOPLOC fingerprint window** (SC).

### 1.5. What is doubtful in the audits' references and numbers

- **Ozaki's kernel acceleration to `γ` = 1.05–1.20.** Doubtful: D5's fast kernels already use
  the same 8-bit instructions, and with them 1.52–1.78 was measured; 24 blocks out of 32 are recursion, which
  the decomposition does not accelerate. This number cannot be put into estimates next to measured ones.
- **TOPLOC:** "258 bytes per 32 tokens", "10–100 times faster", "overhead 1–3%". Two papers
  confirm from memory, three — "cannot verify"; for SkyNet none of this has been measured.
- **Could not verify:** the DeepProve and FlashProve numbers, Verde (three different sets of
  surcharges in the audits), TEE losses on H100, the price of DLEQ in gas, the statuses and incidents of Bittensor and other
  networks, a number of arXiv numbers.
- **Incorrect attributions:** the Krum algorithm is attributed to the wrong authors (MEH); one audit has
  an arithmetic error in the threshold (`c_f ≈ 0.3c`, `p ≥ 0.73`).
- The same number in two audits is not two independent measurements: both may be retelling
  one source.

## 2. The owner's ideas developed into constructions

### 2.1. Verifiability inside the model and fine-tuning

- **"The model protects itself" does not work.** Weights and code are open; the fraudster is not obliged to run
  the model. All eleven papers confirmed this.
- **"The model writes fingerprints"** is a hashing program around unchanged weights.
  Fine-tuning is not needed and adds nothing.
- **Checksums in layers (ABFT)** catch random failure. A knowledgeable adversary selects
  an error that preserves the sum. Recursion, lookup tables and division in attention are not covered by sums.
  The thesis of several papers that "ABFT removes the D16 conflict" was recognised by the critics as overstated.
- **Fine-tuning makes sense only to reduce `γ`:** make the exact profile coincide
  with fast 8-bit kernels ("coarsened canon", DeepSeek's proposal). Bits remain
  bits, the guarantee does not change. Risk: the first 8-bit profile in D5 has already been rejected for quality
  [measured]; the cost of training and the loss of quality have not been measured, and the GPU hours named in the papers are
  assumptions.
- **Fine-tuning "for robustness to rounding"**, so that the fast profile is verified by tolerance,
  returns to the tolerance contract (section 2.4) and gives no provable bound.
- **A model with less state** reduces the traffic of verifying a chunk, but does not increase the share
  of detectable substitutions.

**Verdict:** one form works — acceleration of the exact profile. It is decided by experiment.

### 2.2. Fingerprints and recomputation of a random chunk

**Construction.** Before the choice of verifier, the performer seals the tokens
and intermediate states with one root. The verifier secretly chooses a chunk, receives the sealed input
of the chunk and recomputes it in the exact profile. The chunk can be verified without recomputing the whole
beginning of the response: D5 also confirms this, where a pass in chunks gives the same state hashes [measured].
The statement of several papers that "a chunk cannot be recomputed without the prefix" was rejected by criticism.

**Why the bound `1 − s/N` is not bypassed.** The fraudster honestly computes everything except one cell,
and honestly continues from the substituted value. The trace is consistent everywhere except one transition.
If `s` of `N` transitions are revealed, there is a transition that is verified with probability
no greater than `s/N`. Fingerprints make the lie discoverable, but do not multiply it. Only verification in which any lie violates a large share of equalities (succinct proofs)
can bypass the bound, and its price is the same.

**Two kinds of slices** [calculation from the D5 configuration]:

| Slice | What it certifies | What must be transmitted | What it does not catch |
|---|---|---|---|
| By layers: one block over the whole sequence | One transition of the block from the presented input; a block is about 2.65% of the pass, the output head is about 15.1% | 0.78 / 4.9 / 14.6 MiB at 160 / 1000 / 3000 positions | A substitution assembled in another layer: a chance of 1 in 32–33 |
| By positions: all layers on a segment of 64 positions | The tokens of the segment equal the exact choice given the sealed state of the left boundary | 48 MiB of state and 64 KiB per each previous position: 58 / 110 / 236 MiB | One substituted position outside the segment: passes with probability `1 − L/T`, for example 93.6% at 500 + 500 tokens |

At the same time the performer must store 0.13–2.38 GiB of checkpoints per response for the duration of the dispute
window [calculation]. Only a 32-byte root can go into the ledger: the state itself is 3–5 orders of magnitude
larger than a D24 entry.

**The forgery "draft by a fast profile + exact pass".** It was found by the Claude critic. The fraudster
generates a response in Q8_0, then makes one exact pass over the finished tokens and prints the trace.
In such a trace all transitions of all blocks are consistent; only the positions where the draft token differs from the exact choice do not agree.

- The price of the forgery is `c·(1/γ + ρ)`, the saving against honest work is `1 − 1/γ − ρ`: 18.4% at
  `γ = 1.65`, `ρ = 0.21`; the forgery is profitable when `ρ < 1 − 1/γ` (0.34 / 0.39 / 0.44 at `γ` =
  1.52 / 1.65 / 1.78) [calculation].
- The slice by layers does not catch it (except for a 1 in 32–33 chance on the output head).
- A slice by positions of length 64 catches it with probability 97% if the tokens of Q8_0 and the exact profile
  agree at 95% of positions; 49% at 99% agreement; 29% at 99.5%; 6.5% at 99.9% [calculation].
  The agreement share has not been measured.
- Full verification always catches it. The hole applies only to schemes where the slice **replaces**
  the full pass.

Consequence: the slice certifies "the performer paid for at least an exact pass", not "the response
was generated by the exact profile". The critics disagreed here: DeepSeek believes that the slice
by positions catches the substitution of the whole response by Q8_0 with probability 1; MiniMax — that this probability
has not been measured; Claude gave the calculation above. The measurement of token agreement decides.

MiniMax's criticism added: the free forgery "truncate the response earlier" creates no false cells
at all. The response length and the stop reason must be part of the subject of verification.

**What the trace root still gives:**

- **Dispute by halving.** Two parties with different traces converge in a logarithmic number of moves
  to one step, which each node recomputes itself. Criticism clarified: the claimed
  15–23 moves suffice only down to a cell; inside a block about 27 more halvings are needed; the rule
  "silence is a loss" requires calculation M9.
- **Weak device.** A payer without a video card can verify one segment per
  response. This gives the mark "partially verified", not "verified". The cost for them is traffic
  of 52–300 MiB per response and CPU time; not measured on a phone.
- **Immutability of the performer's history** and a dispute over a private request with disclosure of one cell.

**Verdict:** the construction is possible and useful for dispute and a weak device, but it does not make guarantee D1
and D25. For a targeted substitution to become less profitable than inaction, with 32 blocks one must
reveal 2 / 4 / 7 / 10 blocks at a margin of 5 / 10 / 20 / 30% [calculation], and even this does not help against harm (D6).

### 2.3. Techniques from games

| Technique | Where the move is coupled to the calculation | Where it is not coupled |
|---|---|---|
| "Sealed — revealed" | The revealed chunk must match the recomputation from the sealed input | The sealing itself proves nothing: a consistent lie can also be sealed |
| "One cuts — another chooses" | The choice is made after fixing with the verifier's secret coin | The cutter spoils one part out of `N`; there is no saving against full verification |
| Common coin of two parties | Not needed when one payer's money is at stake: their secret coin suffices | The one who reveals last disrupts an unfavourable outcome; under full collusion all contributions are known to the coalition |
| Cards without a dealer (mental poker) | — | For choosing the chunk number it is redundant: one verifiable random function does the same |
| "Everyone watches the opponent" | The payer verifies their response — all options of section 3 are built on this | The performer cannot punish a dishonest payer without a deposit (calculation M9) |
| Marked cards, a secret buyer | — | In an open network only the payer keeps the trap's secret, so the trap coincides with their verification and is more expensive than it |

A common public source of randomness is needed only where other people's money is verified; then
D20 applies (at least two independent sources).

**Verdict:** from games the order of moves and the main principle "the one whose money is at stake verifies" are taken.
A game does not turn sampling into full verification.

### 2.4. A fast performer and an exact judge

**Tolerance contract.** The performer computes in fast Q8_0, the payer makes an exact pass
and accepts the response if at each position the score of the selected token lags behind the maximum
by no more than `m`. The advantage over the previously rejected "certificate with a margin": the verdict
is computed in integers and is the same on any device. But criticism found four flaws.

- **Tolerance legitimises other people's responses.** Any draft plus one exact pass shows
  the performer all scores; they correct positions outside the tolerance and get an admissible response. The cheapest
  producer of such a response is the cheapest draft model, not Q8_0 of the same model.
- **Freedom of choice is a channel of harm.** At positions with a gap less than `m`, the token is chosen by
  the performer, including early stopping. Example: the scores "continue" and "stop" are
  100 and 99; at `m = 1` a truncated response passes full verification. Such text would receive
  the mark "verified with tolerance" — in essence this is a violation of D6. The previous council
  already rejected a similar mark.
- **An honest performer is forced to verify themselves**, otherwise they lose the amount on one outlier,
  including on an input chosen by the payer. Then the price is `1 + ρ·γ`: +15…+71% at batch 1,
  and at batch 8 there is no gain against exact generation [calculation].
- **The declared price "+0.01…+2.3%" did not hold:** to reveal chunks the performer needs
  state hashes of the exact profile, that is, an exact pass for each generation [calculation].

Even with a fast performer, the judge's full exact pass costs at least 31.9% of the time of ordinary generation on an RTX 2060 [calculation], so this contract does not fit every response into 5%.

**Exact speculative decoding** — the same contract at `m = 0`. The draft is obtained by any
means; only a response bit-for-bit equal to the exact one is paid for. The contract and the guarantee do not change,
D6 is not affected. The price depends on the token agreement share and the length of matching runs; the lower estimate
is `1 + ρ·γ`. Not measured; with agreement below about 95% it comes out worse than direct exact generation.

**TOPLOC and fingerprints with tolerance in floating-point arithmetic.** A fingerprint certifies that
the activations are consistent with the text, not where the text came from. Forgery: text by any model,
then one pass of the declared model over this text — the fingerprints are genuine. A verdict with tolerance
depends on the equipment: two honest nodes may diverge, so the amount cannot be burned based on it, and D4 is violated literally.
For a tolerance tariff to be cheap, the verifier needs a reference that they do not have until they themselves have computed the exact pass.

**Verdict:** the tolerance contract and tolerance fingerprints are not included in the list of options: they
change the product and put a mark on text chosen by the performer. They are admissible only as a signal
for additional exact verification. Exact speculative decoding is a candidate for
reducing the cost, decided by one measurement.

## 3. End-to-end options

The price is the full computational surcharge relative to ordinary Q8_0 generation without verification
[calculation from D5 measurements]. It does not include the ledger, disputes, storage, traffic and energy: they
have not been measured. The gain is expected, per one submitted forgery. The lower edge "+67%" combines `ρ`
of the RTX 4070 Laptop card with `γ` of the RTX 2060 card; on a single RTX 2060 the range starts at +84%.

| No. | Option | Price at batch 1 | The fraudster's money at `q` = 0.1 / 0.3 / 0.5 / 1 | Newcomer with an empty account | Harmer without profit | Main residual risk |
|---|---|---|---|---|---|---|
| V1 | Full verification of every response by the payer | +67…+149% (on a single RTX 2060 +84…+149%) | `−c_f` at all `q` | `−c_f` | There is no false "verified" mark; can disrupt delivery | Lazy payer; false refusals of the payer (M9) |
| V2 | Lottery over whole orders | +53…+82% and the buyer's reserve `R/p` | `−c_f` at all `q` | 0 | A share `1 − p` of responses is unverified and not restrained by anything | Uneven income; the reserve is a question for R5 |
| V3 | The payer's secret coin and the locked amount | +50…+82%; verification itself 0.005–3.6% | No more than zero at all `q`, if the payer tosses the coin on time | `−c_f` (verification always) | A share `1 − p` passes: up to 99.98% | A recognised lazy payer — up to `+R`; an honest failure burns the amount |
| V4 | Tasks with a verifiable outcome | `(N − 1)·v/w`, not measured | `−c_f` at all `q` | 0 | An incorrect witness does not pass | This is not a model response and not a training step |
| V5 | Add-on: exact speculative decoding on top of V1 or V3 | Not measured; lower estimate +15…+71% | As in the host option | Same | Same | Token agreement not measured |

**A payer without equipment** has no guarantee under any option. If they delegate verification
to a triple of assigned nodes, the expected false payment equals `R·q³`: 0.001`R` / 0.027`R` / 0.125`R`
/ `R` at `q` = 0.1 / 0.3 / 0.5 / 1 [calculation]. This is already written in D21.

### V1. Full verification of every response by the payer

**Steps.** The order fixes the model, profile, seed, length limits and acceptance condition.
The performer computes the response in the exact profile and fixes the ciphertext and the trace root in one entry.
Before display, the payer recomputes the whole response in one pass, including the length and the stop reason.
A discrepancy means non-payment; the pending amount does not burn. The mark "verified"
is set only after the pass.

**Guarantee and assumptions.** A false response is not paid for and receives no mark at any collusion share,
for a newcomer and for any number of keys. Assumptions: the bits agree on the payer's device (shown on six performers [measured], not on phones); the verification kernel
is correct; the payer actually verifies.

**Price.** `γ·(1 + ρ) − 1`: +67…+149% at batch 1; +211…+358% at batch 8 (on a single RTX 2060
+251…+358%). Example `γ = 1.65`, `ρ = 0.21`: +99.65%. Verification costs the payer 15–71%
of the time of their own ordinary generation [calculation].

**What to change in the decisions.** Nothing; clarifications are needed for D6 (two marks, no intermediate ones),
D16 (under full verification a discrepancy entails only non-payment) and D22 (section 4).

**Not measured.** The quality of the exact profile (experiment O5); `γ` on other cards; time and memory
on a laptop and phone; the price of a dispute; behaviour under false refusals of the payer.

### V2. Lottery over whole orders

**Steps.** The buyer reserves the prize in advance. All results of the batch are fixed before the draw.
The draw selects a share `p` of orders; the payer verifies the selected ones in full and pays `R/p`;
the rest are not paid and are marked "unverified".

**Guarantee and assumptions.** A false payment is impossible even with an empty account and without burning
amounts; D16 does not need to be changed. Assumptions: the draw is by D20; the buyer's reserve is not considered a deposit.

**Price.** `γ·(1 + p·ρ) − 1`: +53…+82% at batch 1; example `p = 0.05`, `γ = 1.65`, `ρ = 0.21`:
+66.73%. But per one **verified** result there is `1/p` times more work.

**Weak points.** Income is uneven: at `p = 0.1` an honest newcomer with probability 34.87% will receive
nothing for the first ten orders; with 6000 tasks per month, `p = 0.01` and a cost of 95% of the price,
the probability of an unprofitable month is 33.10% [calculation]. Unverified responses are not restrained by anything: a harmer
with free keys supplies garbage for free.

**What to change.** Answer whether the reserve `R/p` is "funds in advance" under R5; choose sources
of randomness under D20.

**Not measured.** The exact probability of ruin along the path, the size of the reserve, the demand for such a tariff.

### V3. The payer's secret coin and the locked amount

This is the strategy of council 5 ([STRATEGY_SEARCH](STRATEGY_SEARCH.en.md)) with amendments.

**Steps.** The response is fixed in the exact profile. After fixing, the payer's program tosses
its secret coin and verifies the response in full with probability not lower than `R/(R + H_lock)`;
for a newcomer — always. A proven discrepancy burns the entire unmatured amount of the key with one action, including the rewards of the same wave; the victim is refunded no more than `R`. The unmatured
amount cannot be transferred, sold or pledged. A response skipped by the coin is paid for
and marked "unverified".

**Guarantee and assumptions.** The expected outcome of any series of forgeries does not exceed the locked amount
at any collusion share: the control example — a wave of ten forgeries gives +4.4295`R` without
burning and −2.49676`R` with it [calculation, reproduced by critics]. Assumptions: the payer
actually tosses the coin and verifies on time; the ledger is available; the amount is actually
lost.

**Price.** +50…+82% at batch 1; verification itself for mature keys is 0.005–3.6% of work. A newcomer's first
window costs 1.3–5.3% of the window's work in units of exact generation [calculation].

**Weak points.** The lazy-payer hole is not closed by any fix: with an empty account
and `λ > 0` the threshold is impossible to fulfil. Under the current D16 the fraudster declares the forgery a failure and receives
`(1 − p)·R − c_f`. A harmer passes with probability `1 − p`. A cheap addition is a lower bound
on the frequency (for example, `p ≥ 1/11` costs 0.9–3.6% of work), but even then 90.9% of the harmer's forgeries
pass [calculation].

**What to change.** D2, D11 and D21 (payment for a response skipped by the coin); D7; cancellation of D16 for
a published discrepancy; a new decision on the locked amount; an answer whether burning
is a penalty under R5; calculation M9.

**Not measured.** The rate of silent hardware failures — how many honest participants
will lose the amount depends on it; the share of payers who actually perform verification.

### V4. Tasks with a verifiable outcome

**Steps.** The plan (D9) pre-authorises a task whose result is accompanied by a witness
verifiable by machine: tests, a formal proof, a solution to a problem with an optimality certificate.
The bid is sealed before the witness is revealed so that it cannot be
intercepted. Each node verifies the witness itself; payment — once per task content.

**Guarantee.** An incorrect witness does not pass under full collusion, an empty account and any number of
keys.

**Price.** If `N − 1` nodes verify at `v` with a generation cost `w`, the surcharge is
`(N − 1)·v/w`. At `N = 1000` it fits into 20% only at `v/w ≤ 2·10⁻⁴`; at `v/w = 10⁻³`
it is already 99.9% [calculation]. The ratio `v/w` is taken from the audits and has not been measured.

**Weak points.** This is a different product: not a free response of the model and not a gradient step. The task
can be solved without a model and without a video card. A rule generating useful hard tasks
has not been presented. Verification of the witness is copyable, so under D15 it is not paid for: the idea "a phone
earns by verifying certificates" contradicts this.

**What to change.** Supplement D9 and D15; D18 remains research.

**Not measured.** What share of the network's work falls into this class.

### V5. Add-on: exact speculative decoding

The draft is obtained by any fast method; the performer themselves checks it with an exact pass
and corrects discrepancies; only a bit-for-bit exact response is paid for. The guarantee is the same as
that of the host option V1 or V3; the decisions, apart from the clarification of D22, do not change. A gain is possible
only if the tokens of the fast and exact profiles agree often and in long runs. None
of this has been measured.

## 4. The council's recommendation and the first step

**Recommendation (summary).** The main contract is **V1**. It alone fulfils D1, D6, D7 and D25 for
a response without new assumptions about frequency, the locked amount and burning, and does not require amending the adopted
decisions. All eleven papers give the same price formula for it. **V4** is a separate type of
plan task. **V2** is a tariff for coordinated batches. **V3** is a candidate: enable only
after calculation M9 and explicit decisions of the owner. **V5** and acceleration of exact kernels are ways
to reduce the price, not separate contracts.

**Clarifications of decisions for V1** (proposals, not decisions):

- D6: there are two marks — "verified" after full bitwise verification before display and "unverified".
- D16: under verification of every response by the payer, a discrepancy entails only non-payment.
- D19: if the attempt is free, the assumption of D19 does not apply.
- D22: the draft may be obtained by any means; only a response bit-for-bit
  equal to the exact one is paid for. The response length and the stop reason are part of the subject of verification.
- Do not change D12: replacing active time with the block height of an external chain allows unmatured
  amounts to mature while the network is unavailable.
- A new decision on price: in which profile the volume of computation is counted. At a price of 1.10 times
  the cost of the ordinary profile, honest work in the exact profile is loss-making by 42–68%
  of cost [calculation]; this premise itself has not been approved in the project.

**One calculation.** M9: false disputes without a deposit for a one-time order — silence of each
party, self-dispute, self-order with a false dispute, limits of bytes and computations per case, source of
funds. Without it no option is enabled (D23).

**One experiment** (the owner's permission is needed; an extension of the already conducted O3 and O4). On the assembled
profile v2 and llama.cpp Q8_0 with a common prefix, measure the token agreement share, the distribution
of the score gap of the selected token and the lengths of matching runs. It decides three questions:
whether V5 pays off; whether the tolerance contract is viable; whether a slice by positions catches the forgery
"draft + exact pass", that is, whether a payer without a video card has any protection at all.
First it is worth checking whether the full scores of both profiles have been preserved in the D5 records.

**Where critics and papers disagreed.**

1. **Which contract is the main one.** Critics Claude and ChatGPT — V1. Critic DeepSeek — V3 with fixes,
   and V1 as an expensive tariff and newcomer mode. Critic MiniMax — V1 as the base tariff and the coin
   for mature keys, but the network pays only for the verified.
2. **Whether to pay for a response skipped by the coin.** For — the majority of papers; against — both
   ChatGPT papers and one MiniMax paper. If not to pay, an honest performer receives `p·R`
   per task, and this is a lottery without the `1/p` multiplier. There is no third way; this is the owner's choice.
3. **Which experiment is first.** Critics Claude and ChatGPT — token agreement of the two profiles.
   Critics DeepSeek and MiniMax — a microbenchmark of 8-bit Ozaki-type kernels with bitwise comparison:
   it shows whether the 5% benchmark is achievable at all. The summary puts it second.
4. **Achievable `γ`.** 1.05–1.20, 1.1–1.3 or "will not decrease". Not measured.
5. **Whether it is a deposit under R5** — the burning of the unmatured amount, the dispute reserve, the lottery reserve,
   the long maturation period and surety.
6. **Whether to cap the locked amount.** A ceiling of 10`R` limits the expected number of
   forgeries, but makes verification of mature keys about 400 times more expensive [calculation of one
   critic, not rechecked].
7. **The third mark.** Critic MiniMax proposes "partially verified"; critic Claude — only
   two marks.

## 5. Training: what exists and what does not

**What is absent.** No paper gives a guarantee for the training step. Training has no payer:
the basis for issuing credits must be verified by every full node. Integer training
has not been built or measured; D5 measurements relate only to the forward pass and do not transfer to the backward
pass and the optimizer.

**What exists.**

- **Full repetition of the step by every node** — strict, but costs `N` additional steps: with ten
  nodes about 1000% [calculation].
- **Slices of the step:** a node verifies one cell out of about four thousand. The price is 0.24% / 2.4% /
  24% at 10 / 100 / 1000 nodes [calculation], but under full collusion detection is zero.
- **Payment for a verifiable outcome** (V4): a strict guarantee for a narrow statement. The task witness is verified,
  not the gradient step; the papers' formulations "training is solved" and "harm is excluded"
  were recognised by criticism as overstated.
- **Payment for a proven improvement on an exam** (D18) remains research: the exam
  certifies a score on a given set, but not the absence of a backdoor in the weights.

**Limit.** With 1000 nodes and a 20% surcharge, all independent verification of one node must cost
no more than 0.0002 of the step's work [calculation]. A succinct proof of the step, by all estimates of the project,
is orders of magnitude more expensive.

**Council recommendation.** Issue credits only for results that each node verifies
itself; do not include an unverified step in the model version (this is already D6).

## 6. What is literally infeasible: questions to the owner

The council does not propose to change the texts of R1–R6. The proposals of two papers to amend R4 and R6 were
rejected by criticism: this is an immutable foundation. The general impossibility of combining R4 and R6 for all conceivable
algorithms has not been proven; below is what is infeasible under the constructions found.

| No. | What is infeasible | Minimal relaxation | Council recommendation |
|---|---|---|---|
| 1 | Protect a consumer without equipment under full collusion of verifiers: the honest and false cases give them identical messages | The guarantee is promised only to the party that verifies itself; the response is shown to others with the mark "unverified", and the magnitude of the risk `R·q³` is named directly | Adopt: this is already written in D21, it only needs to be transferred to the user description |
| 2 | Verify the training step under full collusion within 20% | (a) pay for a verifiable outcome, not for the step; (b) allow "at least one honest full node"; (c) remove the 20% benchmark for a small network | (a): the only path with a strict guarantee; at the same time part of the free capacity remains without paid training |
| 3 | Fit a verified response into 5% at the measured `γ` = 1.52–1.78 | Treat the 5% benchmark as an engineering goal, publish the actual price and pursue the reduction of `γ` as a separate task | Adopt; 5% is a roadmap benchmark, not the text of R6 |
| 4 | Restrain by economics a harmer who does not need a gain, at `p < 1` | Only marks and a ban on using the unverified (D6) | Already adopted; there are no new measures |
| 5 | A dispute without a deposit with a finite dispute fund | Decide whether the buyer's locked prepayment is considered a deposit under R5 | Decide after calculation M9 |
| 6 | Be fully confident in the decision before any measurements | Allow a limited list of measurements on which the choice depends | The owner's decision; the council names two measurements from section 4 and experiment O5 |

Additional questions: whether to pay for a response skipped by the coin (section 4, item 2);
in which profile the task price is counted; whether to allow third-party surety.

## 7. What the mini-agents should calculate and what should be checked by experiment

**Calculations** (exact fractions, control hash, repeat on a second device; they are not experiments on the protocol):

1. M9 for all branches of a one-time order.
2. The gain of the forgery "draft + exact pass" under slices on a grid of `γ`, `ρ`, the agreement share,
   the segment and response lengths, and the margin.
3. The coin with a lower frequency bound and a share of lazy payers, including an empty account.
4. A mixed forgery "everything honest except one column" and the forgery by truncating the response.
5. The lottery: the exact probability of ruin along the path and the size of the buyer's reserve.
6. The exact sizes of the cell input and the dispute step according to the profile v2 specification (check 48 MiB and 64 KiB).
7. Flooding with new keys: the load on the payer and the derivation of a quota of new keys.
8. Brute force of the smallest false sets of cells on a small model.
9. Reconciling `ρ` and `γ` on one card and equal lengths; the cost per one verified result.

**Experiments.** O5 is authorised by decision D5. The rest are outside D5 and require the owner's permission:

1. Token agreement and score gap of Q8_0 against v2 — the first experiment.
2. O5 — the quality of profile v2 on 320 tasks.
3. A microbenchmark of 8-bit kernels with bitwise comparison — a check of Ozaki's estimate.
4. `γ` and `ρ` in pairs on one card, including RTX 4070 Laptop.
5. Time and memory of the pass and the segment on a laptop CPU and on a phone.
6. The cost of printing the trace, ABFT coverage and the rate of silent failures.
7. Experiments on training O6 and O7 — separately, after the decision on D18.

## 8. Who did what

- **ChatGPT:** two independent papers and a criticism of all papers.
- **DeepSeek:** two independent papers and a criticism with recalculation of numbers in exact arithmetic.
- **Claude:** two independent papers, a criticism and this summary.
- **MiniMax:** five independent papers and a criticism.
- **Gemini** did not participate in the council: there was no key in the model hub; its audit was among
  the input data.
- **External audits and mechanism maps** — input data collected by the owner; the council
  did not recheck them against primary sources.

Limitations of the summary: the ChatGPT critic analysed ten papers out of eleven; the Claude critic read
one of the papers not in full; the critics' calculations were performed on one computer each and await repetition by mini-agents.
