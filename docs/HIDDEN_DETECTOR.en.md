<!-- translation of docs/HIDDEN_DETECTOR.md, source sha256: a695d12d2972002373f749a618c390c3e937e344afd1e816d8c46319fe1127cb -->

# Hidden and changing detector: what the secrecy of rules gives

**English** · [中文](../i18n/zh/HIDDEN_DETECTOR.md) · [Español](../i18n/es/HIDDEN_DETECTOR.md) · [Français](../i18n/fr/HIDDEN_DETECTOR.md) · [Deutsch](../i18n/de/HIDDEN_DETECTOR.md) · [Italiano](../i18n/it/HIDDEN_DETECTOR.md) · [Русский](HIDDEN_DETECTOR.md) · [Português](../i18n/pt/HIDDEN_DETECTOR.md) · [العربية](../i18n/ar/HIDDEN_DETECTOR.md)

Status as of 25 November 2026. The result of the sixth model council.

## 1. The question and a brief summary

The project owner asked, verbatim:

> "With open rules (D4) the fraudster knows the detector and forges exactly where it is calm. What if the detector is hidden? For example, the network will at random times randomly generate new honesty verification rules and agents will verify by them. Given the distributed and open architecture of the skynet network, no one should know the verification rules, and they must be encrypted, with the encryption key changing. Think with a council of models in this direction. Earlier I raised the question of using a blockchain — is there an option to make a dynamic detector based on a blockchain? Maybe besides the blockchain there are some other technologies or algorithms?"

**Document status.** This is reasoning and calculation, not measurement. There was no network during the council's work, no experiments were conducted; scientific papers are named from memory and were not checked. Measurements are taken only from the results of experiment D5 as of 25 November ([EXPERIMENT_D5](EXPERIMENT_D5.en.md), section 7) and from the previous consolidation [STRATEGY_SEARCH](STRATEGY_SEARCH.en.md). Only D1–D25 remain adopted project decisions ([ROADMAP](ROADMAP.en.md)); everything below called a "recommendation" must be explicitly accepted or rejected by the owner. Markings: [measured] — measured in D5; [calculation] — follows from a formula with named parameters; [assumption] — a quantity taken for an estimate and not measured.

Notation found below: `R` — payment for one task; `H_lock` — the performer's unmatured amount that burns upon a proven forgery; `c_f` — the cost of forgery; `p` — the probability of full verification of a task; `ρ` — the time of verifying a finished response in one pass divided by the generation time; `γ` — how many times slower the exact integer profile is than ordinary llama.cpp Q8_0 generation; `q` — the collusion share; `n_w` — the number of key tasks per maturation window.

**Brief summary.**

1. **A hidden detector gives no more than open verification with secret randomness of the same cost.** If the fraudster knows by which law the rules are chosen (and under D4 the agent's code is open, so he knows it), then the probability of catching any forgery of his under a hidden rule equals the probability of catching under the open program "after fixing the response, toss a coin and apply the rule that comes up." All eleven papers independently obtained this, all four critiques confirmed it. Hence secrecy does not allow lowering the verification frequency below the previous threshold `R/(R + H_lock)`.
2. **A rule that lives longer than one task is worse than a fresh coin.** The fraudster learns from his outcomes ("caught / not caught"), probes the detector with free new keys, learns the rule through any accomplice who was given it to apply. Even without any leakage, a rule common to an epoch is more dangerous: in ChatGPT's example a wave of ten forgeries gives `+8.1R` versus `−2.38R` with independent coins [calculation]. "Changing rules at random times" is therefore worse than changing the choice on every task.
3. **Exactly one form of secrecy is useful:** the secrecy of the random choice *before* the performer irrevocably fixed the response, and the secrecy of *the role* — whether this payer verifies and who is appointed as verifier. The rules, the family of verifications and the selection law remain open. This form already exists in the previous council's strategy ("the payer's secret coin").
4. **What to take from the blockchain and cryptography.** The blockchain is a ledger of fixations, order, disclosures and burning of amounts; there are no secrets in it and there cannot be. An external threshold randomness beacon and a VDF delay from the final block are sources of randomness for common samples under D20 (training audit, exam, appointment of verifiers), mixed by a hash. VRF and a commitment to a salt before fixing — where the coin's outcome affects other people's money. A "dynamic detector on a blockchain" in the correct form is **an open rule generator in the core plus fresh randomness after fixing**, not encrypted rules.
5. **What to reject as a basis for a guarantee.** Threshold storage of secret rules by participants (disclosed or blocked by collusion, at `q = 1` there is no protection — a violation of D7), trusted execution environments TEE (trust in the manufacturer, they are absent on the D5 experiment GPUs), fully homomorphic encryption FHE (according to the critics' estimate, from 19 hours to 15 days of computation per response), multi-party computation MPC (hundreds of megabytes and more of traffic per token and again dependence on `q`), indistinguishability obfuscation iO (impractical and still leaves the fraudster a "trial run"), functional encryption and PIR (solve other problems). Traps, secret thresholds and statistics are admissible only as a signal for *additional* verification.
6. **An error was found in previous tables.** In STRATEGY_SEARCH 5.3 and in most papers of this council, the cell "lazy payer, performer distinguishes him" × "newcomer" contains 0. The correct value is **up to `+R`**: the rule "a newcomer is always verified" is executed by the payer's program, and a lazy payer does not execute it. Worse, new keys allow finding out for free which payer is lazy. Only the unlinkability of payers between requests protects against this, and it has yet to be built.
7. **The council does not propose new decisions on the guarantee.** What is proposed is a clarification of D4 ("the core accepts future randomness, but not a long-lived secret") and a clarification of D20 ("sources are mixed by a hash, not by choice; the beacon is for common decisions, not for the payer's money"). The cost of verification does not change because of secrecy: the main item is still the slowdown of the exact profile `γ` (+50…+82% over Q8_0 at batch 1 [measured γ, calculation]), not verification itself.

---

## 2. Why the secrecy of rules does not help: statements and counterexamples

### 2.1. A hidden rule equals an open rule with a secret coin

**Model.** The defender chooses a verification rule `r` from a distribution `D`. Rule `r` catches forgery `x` with probability `π_r(x)`. The fraudster knows the distribution `D` (under D4 the rule generator is part of the open core), but does not know the drawn `r`, and chooses the forgery before `r` is drawn.

**Statement 1 (equivalence).** The probability of catching forgery `x` equals `π̄(x) = E_{r~D}[π_r(x)]`, the average verification cost equals the average cost of the rules. The open program "after irrevocable fixing of the response, take fresh randomness, choose `r` according to the law `D` and apply it" gives for **each** forgery the same probability of catching and the same cost. Hence the secrecy of the implementation adds zero to protection.

The proof is averaging over `r`: the outcomes of the two experiments coincide for each value of the randomness. It was independently carried out by gpt1, gpt2, ds1, ds2, claude1, claude2, mm1–mm5; the ChatGPT, DeepSeek, Claude and MiniMax critics confirmed it. This is the same result as the previous council's bound `E_F[π] − E_P[π] ≤ TV(F, P)` ([STRATEGY_SEARCH](STRATEGY_SEARCH.en.md), section 2.1): the quantity `π̄` is an ordinary function of observations with values from 0 to 1, and secrecy does not change it.

**Statement 2 (information about the secret only harms the defender).** If the fraudster before the forgery receives any signal `Z` about the drawn rule — from a past dispute, a probe, through a share of the key, from an enclave leak — his best result does not worsen: `E_Z[min_x E[π_r(x) | Z]] ≤ min_x π̄(x)`. He can always ignore the signal (claude1, claude2; confirmed by the critics).

The ChatGPT critic clarified the boundary of this statement: the inequality is non-strict. If all rules have the same "worst for the defender" forgery, disclosure of the rule may change nothing. claude1's phrase "any leak strictly worsens" is therefore incorrect; "never improves" is correct.

**How this differs from randomization.** Several papers (ds1, ds2, mm2) wrote the consequence as "a hidden detector equals verification of the whole response with probability `p`." This is imprecise. The equivalent of a hidden detector is *a mixture of the same rules*. A mixture of partial verifications is sometimes stronger than full verification at the same cost, but the gain comes from randomization, not from secrecy, and it persists with an open algorithm:

- **gpt1's counterexample.** The result has three independently verifiable parts of one cost, and by the design of the task any admissible forgery spoils at least two. Verifying one random part at a third of the full cost catches at least 2/3 of forgeries; a full recomputation with probability 1/3 — only 1/3.
- **gpt2's variant.** Three tests at half the cost of a full recomputation, each catches two classes of errors out of three: the mixture catches 2/3, full recomputation of half the tasks — 1/2. If a fourth class is added that no test catches, the guarantee of the mixture falls to 0.

For Qwen such coverage of error classes has not been proven: one incorrect position of the response is already a forgery, and for it any partial verification catches no more than its share. Therefore the practical gain from the mixture is now zero (the Claude and ChatGPT critics). mm2's statement "a mixture is always more expensive than the decisive type" is incorrect in general; moreover, its formula has an extra factor (the numbers 0.2111 / 0.22 / 0.2333 are computed by the correct formula, the wrong one is written — the Claude and DeepSeek critics).

**Where secrecy does not reduce to a coin.** This is the defender's private label tied to the correct answer: the trap reference that only the payer knows (gpt1, gpt2). It cannot be replaced by a random bit. But, as shown in section 3, it costs no less than one generation and therefore does not make verification cheaper.

**Against a "fixed" rule secrecy is indeed better.** claude1 gives an example: if the open rule always looks at positions 1–8, a forgery at position 9 is never caught. But the same gain is given by the open rule "choose 8 positions uniformly after fixing" (mm3, theorem 2: a fresh position catches `e/N` forgeries, where `e` is the number of corrupted positions out of `N`, regardless of whether the fraudster knows the rule). The MiniMax critic called this the main error of the round: many papers compared a hidden detector with a fixed open rule and attributed to secrecy a gain that belongs to randomness.

### 2.2. The fraudster's learning from outcomes and probes with new keys

A secret that is used more than once is learned. The adversary does not need to know the whole rule for this — it is enough to find one safe place.

- **Two positions out of ten (claude1).** A hidden rule verifies 2 positions out of 10, catching a single-position forgery is 1/5. After one dispute has revealed one verifiable position, catching falls to 1/9, after revealing the second — to 0. If the rule is revealed by the very first dispute, then the expected number of caught out of 100 forgeries is `1 − 0.8¹⁰⁰ = 0.9999999998`, that is, practically one, whereas a fresh coin would catch on average 20 [calculation, confirmed by the critics]. The ChatGPT critic noted that this is true for a specific order of probes and full disclosure at the first catch; in the general case one dispute reveals at least the verified position, but not necessarily the whole set.
- **Eight positions out of a thousand (ds2).** With a hidden constant subset of 8 positions out of 1000, the very first single-position forgery passes with probability 0.992, just as with a public fresh sample of the same share. The difference is that with a hidden constant subset the position that passed remains safe forever. ds2's number "≈ 2718 attempts to recover the whole set" is computed by a wrong model (with replacement); without replacement about 890 attempts are needed, and most importantly, one safe position is enough for the adversary (the Claude, DeepSeek and ChatGPT critics).
- **The epoch rule and a mature key (claude2).** A deterministic rule for an epoch of 100 tasks, `p = 1%`, `H_lock = 99R`: a fraudster who has found a safe area by probing receives about `0.99·100R − 0.01·99R = 98.01R` per epoch versus `≤ 0` with a fresh coin [calculation, confirmed].
- **The common epoch bit (gpt2).** `R = 1`, `9R` locked, ten forgeries of one wave, the first proven forgery annuls the wave and `9R`, the verification frequency of an individual request is 1/10. If one hidden epoch bit decides "verify everything" or "skip everything", the wave's gain is `0.9·10R − 0.1·9R = +8.1R` — a violation of D1 **before any leakage**. With ten independent coins at the same costs `(0.9¹⁰·10 − (1 − 0.9¹⁰)·9)R = −2.3751096381R` [calculation, repeated by all critics]. Similarly with the ChatGPT critic: at `R = 1`, `H = 4`, `p = 0.2` and ten forgeries a common coin for the whole wave gives `+7.2R` even if the whole wave is annulled.

**Sybil keys.** New keys are free. A key with an empty account loses nothing when caught, so probes of the detector from it cost almost nothing. Protection holds only where a newcomer is really always verified (`p = 1`). The ChatGPT critic stipulated that the freeness of keys does not imply that adaptation is instantaneous: every informative outcome requires a paid task and time, and with noisy feedback — several attempts. The conclusion does not change: a secret that lives long is sooner or later learned, and a fresh coin teaches nothing, because the next toss is independent of previous ones.

**Conclusion.** The choice must be made anew for each task, not on a schedule. That is exactly why "the network generates new rules at random times" is worse than "a fresh coin on every task", which regenerates itself and for free (ds1).

### 2.3. The rule leaks through those who apply it

"A rule that no one knows but everyone executes" is impossible in an open network. The node that applies the rule knows it at the moment of application: the code and keys lie in the machine's memory, and the machine's owner, under the adversary model, can read them ([THREAT_MODEL](THREAT_MODEL.en.md), section 1.3). claude1 formulated a complete list of carriers of the secret:

1. the rule does not exist yet — it will be derived from future randomness (beacon, VDF);
2. the rule is executed in hardware that the owner cannot open (TEE) — then trust is transferred to the manufacturer, and R4 calls this an assumption;
3. the rule is encrypted so that it can be executed without knowing it (iO, FHE, MPC) — see section 3;
4. the rule is known to a committee of participants — then collusion discloses or blocks it.

The ChatGPT critic supplemented the list: MPC over shares and evaluation of an open circuit over an encrypted parameter allow the operator not to see the result at all. This does not change the conclusion, because such schemes again rest on a share of honest participants or on the key holder.

**A threshold key protects storage, but not application** (claude2, the council's strongest argument against a secret rule at a committee). Even if the key is split reliably, the decrypted epoch rule is executed by a specific node. With `m` independent applications, the probability that at least one applying node is from the coalition equals `1 − (1 − q)^m`: over 10 applications this is 0.65 / 0.97 / 0.999 at `q` = 0.1 / 0.3 / 0.5. The probability that the epoch rule is *not* learned by the coalition over 100 applications at `q = 0.1` is `0.9¹⁰⁰ ≈ 2.7·10⁻⁵` [calculation, confirmed by the critics].

**Hiding from the verifier is pointless** (claude2, corollary 4.2). A colluding verifier may not verify at all and say "clean"; an honest one has nothing to hide. The only one from whom the decision must be hidden is the performer before fixing the response. claude2 added theorem 4: if the verifier must not know which positions he verifies, he has to "touch" all positions, and the saving from sampling disappears. The ChatGPT critic noted that this conclusion is valid in a special model (one server, no preprocessing), and under other models of memory access it may change; the Claude critic — that the theorem refutes a variant that no one defended.

**A hidden secret does not give a verifiable verdict.** mm2 noticed that the statement "there exists a secret rule that accepted the result" is always true for the rule "accept everything". The Claude and ChatGPT critics clarified: a zero-knowledge proof can certify a meaningful statement "the rule was derived from a commitment recorded before fixing, and it accepted the result". But such a proof requires an open relation in the core, that is, it brings us back to the open generator, and its cost for Qwen has not been calculated.

### 2.4. A threshold key at collusion share q

Let the key be split among `n` holders, and `t` shares are needed for decryption. Then the coalition learns the secret early if it has `t` or more places, and can stop operation if it has `n − t + 1` or more places. If the places are chosen independently and each with probability `q` belongs to the coalition, these are binomial tails. Table by the Claude critic, checked by the ChatGPT and DeepSeek critics; in each cell "disclosure / stopping" [calculation]:

| `n`, `t` | `q = 0.1` | `q = 0.3` | `q = 0.5` | `q = 1` |
|---|---|---|---|---|
| 5, 3 | 0.856% / 0.856% | 16.3% / 16.3% | 50% / 50% | 1 / 1 |
| 7, 5 | 0.0177% / 2.57% | 2.88% / 35.3% | 22.7% / 77.3% | 1 / 1 |
| 16, 11 | 2.7·10⁻⁸ / 0.33% | 0.157% / 34.0% | 10.5% / 89.5% | 1 / 1 |
| 30, 16 | 3.66·10⁻⁹ / 3.56·10⁻⁸ | 0.637% / 1.69% | 42.8% / 57.2% | 1 / 1 |
| 64, 43 | 4.75·10⁻²⁸ / 1.20·10⁻⁷ | 9.43·10⁻¹⁰ / 26.2% | 0.41% / 99.6% | 1 / 1 |
| 100, 51 | 6.3·10⁻²⁵ / 5.8·10⁻²⁴ | 9.0·10⁻⁶ / 2.2·10⁻⁵ | 46.0% / 54.0% | 1 / 1 |
| 100, 67 | 9.6·10⁻⁴³ / 7.0·10⁻¹¹ | 2.7·10⁻¹⁴ / 22.1% | 0.044% / ≈1 | 1 / 1 |

What follows from it:

1. **No row gives protection at `q = 1`.** D7 requires verification independent of the collusion share, therefore secrecy at a committee does not fulfil D7 at any threshold.
2. **A high threshold holds the secret well, but is easily blocked.** Row 16/11: at `q = 0.3` disclosure is 0.157%, but with probability 34% the coalition stops issuance simply by not sending shares.
3. **Epochs add up.** With a disclosure probability of 0.856% per epoch (3 out of 5, `q = 0.1`), over 30 independent epochs at least one disclosure will occur with probability 22.7% (gpt1) [calculation].
4. **The table is optimistic.** Independent choice of places is an assumption. It breaks if holders are selected by weight, and weight can be accumulated by self-paid verified requests; if a rare model has a collusion share above average; under bribery after appointment; with common owners of places. [THREAT_MODEL](THREAT_MODEL.en.md) (section 1.7) already has an example: 42.1% of the total weight gives `q_eff = 88.9%` among those admitted to the task (the MiniMax critic drew attention to this).
5. **Errors in papers.** claude1 recorded the condition "`q < min(t/n, 1 − t/n) ≤ 1/2`" as a theorem; this is not a theorem: at `t = n` the secret holds as long as there is at least one honest member in the committee, and blocking may have a safe fallback outcome (the Claude critic). mm4 confused the disclosure and blocking thresholds; mm2 erroneously believed that threshold decryption requires all holders; ds1 inconsistently wrote "restored by `t + 1` shares". mm3's statement "at `q ≥ t` the coalition forges the rule" is true only where the verdict is a threshold signature without verifiable content; if a pre-fixed ciphertext is decrypted, the coalition learns the rule, but cannot substitute it.

**How to read requirements R2/R3.** ds1, mm1, mm3 and mm4 wrote that the requirement of recovery after a complete stop "fundamentally prohibits" common secrets. The Claude and ChatGPT critics consider this an overstatement: holders' shares can survive a stop on their disks; R2/R3 prohibit dependence on the address of a live coordinator, not on the return of some participants. The exact boundary (claude2): a secret without which the basis of a **past** decision cannot be verified is incompatible with verifiability after a restart. Hence any secret rule must be disclosed no later than payment, and its secret lives no longer than the secret of the coin. The conclusion about the unsuitability of secret rules is the same; ds1's, mm1's, mm3's basis was overstated.

### 2.5. Kerckhoffs's principle, security games, banks and CAPTCHA

**Kerckhoffs.** Kerckhoffs's principle (from memory) allows an open algorithm with a closed key. In this game the closed "key" must be the implementation of the verification call unpredictable before fixing, not the algorithm. Changing a long-lived key is useful after a compromise, but does not erase what the fraudster has already learned about the function that this key decrypted (the ChatGPT critic).

**Security games.** A defender with a limited budget randomizes — this is classic Stackelberg games and inspection games (from memory). But there the defender's distribution is usually considered known to the attacker, and all the benefit comes from randomness, not from secrecy of the distribution. The DeepSeek critic corrected mm3: the fraudster's ignorance of the distribution cannot raise his gain above the best response to the true distribution, and under D4 he is obliged to know this distribution anyway. For a mixture of different tests gpt1 wrote a linear programming problem: maximize the smallest over forgeries probability of catching `min_f Σ w_j D(j,f)` under the budget `Σ w_j c_j ≤ B`.

**"Moving target".** The idea of moving target defense (from memory) is valuable when the observer needs time to adapt to a new configuration. In SkyNet the best "moving target" is a new configuration on every task, that is, a fresh coin (mm4, mm5).

**Why secrecy works in a bank and in CAPTCHA, but not in SkyNet.** The papers and critics agreed on the following differences (claude2, ds2, mm3, mm5, the ChatGPT critic):

| | Bank anti-fraud, CAPTCHA | SkyNet |
|---|---|---|
| Who holds the verification model | One organization on its own server | No center; the agent's code is open (D4) |
| Feedback to the attacker | Often non-attributable, delayed | The outcome is visible immediately and tied to the task |
| Cost of an attempt | Opening an account, documents, limit on repeats | The key is free (Sybil) |
| Sanctions | Non-monetary: blocking, court, external information | Only burning of the unmatured amount (R5) |
| Goal of protection | Reduce losses on average | Expected gain of any coalition no higher than zero (D1) |
| Verifiability of the decision | Not required by third parties | Every node verifies the basis itself |

At the bank there are private labels of outcomes, the cost of opening an account and a limit on repeats; at CAPTCHA — an external verifier. These are additional information and costs of the attacker. They do not appear in SkyNet by changing the encrypted rules file. ds2 and mm5 accurately named the essence: where secrecy works, the secret is effectively one-time, that is, it is the same coin.

**The main premise of the question in SkyNet is partly incorrect** (mm3). The project's main verification is bitwise comparison with exact recomputation. It has no "place where the detector is calm": an honest response matches everywhere, a forgery diverges where it is forged. "Quiet zones" exist only in statistical detectors and in partial verifications. Statistical detectors against the main forgery (ordinary Q8_0 generation instead of the exact profile) are almost useless, and for partial verifications a fresh choice after fixing helps.

---

## 3. Analysis of technologies

Prices below are [calculation] from explicitly named parameters and [assumption] about the speed of cryptography from memory; none of these technologies has been measured in the project. Basic measurements: `ρ = 0.10–0.40` at batch 1 and `0.26–0.64` at batch 8; `γ = 1.5–1.8` at batch 1 and `2.5–2.8` at batch 8 [measured, O3 and O4]. D5 model: 32 blocks, hidden size 2560, MLP 9216, 24 Gated DeltaNet blocks with state `32×128×128`, vocabulary 248,320, about 4.2·10⁹ multiply-adds per token.

| Technology | What it gives | What it does not give | Cost [calculation / assumption] | Verdict |
|---|---|---|---|---|
| **Blockchain ledger** | Order, final fixation of the response (D24, 2–4 KB of ciphertext), commitments, disclosures, one-time calculation, burning | Secrecy: everything in a block is seen by everyone. Non-manipulable randomness: the block producer can withhold an inconvenient block (H13) | Pilot dispute: 93 transactions, 5.8–6.3 million gas, at 1 gwei and $3000/ETH — $17.4–18.9, at 20 gwei — $348–378 (ChatGPT critic per THREAT_MODEL, H3) | **Take as a ledger** |
| **Smart contract as detector** | Automatic calculation from an already verified basis | Neither storage of a secret nor model computation | Recalculation of a token inside the contract: `4.2·10⁹ × 3 gas ≈ 1.26·10¹⁰ gas` ≈ $37,800 per token at 1 gwei and $3000/ETH (ds1, confirmed). Claude critic: this is about 420 blocks of 30 million gas (limit from memory). ChatGPT critic: a simple MUL operation costs 5 gas from memory, so this is a scenario, not a strict lower bound | **Reject as a detector** |
| **External threshold beacon** (drand class, from memory) | Public randomness that no one knows in advance, if the threshold of its committee is honest | Secrecy: the round is published for all. A coalition inside the beacon committee learns the round earlier or can fail to release it | Hundreds of bytes per round per batch and waiting one round (from memory, 30 s for the main chain and about 3 s for a fast one) | **Take as one of the two sources of D20** for common samples |
| **VDF from the final block** | A delay during which the block producer cannot select a convenient block | Independent entropy: a VDF from the same block is not a second independent source (ChatGPT critic) | Sequential work of the computer; verification is fast | **Take as a supplement to the beacon**, record the assumption about the superiority of fast hardware |
| **Timelock encryption via the beacon** | Delayed disclosure of common references, exam tasks | Secrecy longer than a round; inherits the beacon's threshold | As with the beacon | **Only for delayed disclosure of common data**; do not disclose private data this way |
| **Time-lock puzzle** (Rivest–Shamir–Wagner, from memory) | A delay of disclosure | The creator knows the answer immediately; a coin is simpler | Sequential work | **Reject** |
| **VRF** | A unique and verifiable value for a pre-registered key and input | Secrecy from the key holder: he computes the value whenever he wants. Verification of the VRF proof discloses the value (mm4's error). It does not prove the fact of recomputation of the VRF | One call and hundreds of bytes per response | **Take**: for appointing verifiers (against bribery after appointment) and as the payer's coin where someone else's payment depends on its outcome; the key is registered per order before fixing |
| **Commit–reveal** | Binding a salt to one order before fixing the response | Protection from a "last revealer" who can stay silent | gpt2: 448 bytes per scheme | **Take narrowly**: a commitment before fixing, without the right to choose the outcome |
| **Threshold cryptography** (Shamir, DKG, threshold decryption) | Storage of a key without a single holder | Independence from `q` (section 2.4); protection when applying the rule (section 2.3) | DKG at `n = 7`, `t = 5`: `7·6·32 + 7·5·48 = 3024` bytes of payload (gpt2), threshold BLS signature — 288 bytes; without replication and complaints | **Reject for secret rules**; an internal threshold beacon of participants — only as one of the sources, not the only one |
| **TEE** (SGX, SEV, TDX, protected GPUs) | Execution of code hidden from the machine's owner, with trust in the manufacturer | Independence from the manufacturer and his attestation chain; there are no protected GPUs in the D5 fleet (RTX 2060, RTX 4070 Laptop, RX 580) | Scenario of the ChatGPT critic: protected verification 1.2 times longer than open, `p = 0.1` — about 3.20% of generation time with weight loading; a model on CPU — about 50–100 ms per token versus 15–50 ms on GPU (Claude critic) [assumption]. MiniMax critic: the owner can use the enclave as an oracle, the secret rests on limiting the number of requests | **Only as a privacy mode at the user's choice**, not a basis for the guarantee |
| **FHE** | Computation over encrypted data and, through a universal scheme, over an encrypted program | Verification of the correctness of the computation; the result is opened by the key holder (again `q`). The approximate CKKS scheme does not reproduce the bits of profile v2 | 1.4·10⁷–2.6·10⁷ bootstraps per token, at 10⁴–10⁵ bootstraps per second [assumption] — 140–2600 s per token, from 19 hours to 15 days per 500-token response; multiplier to open verification `Φ ≈ 3·10³…2·10⁵` (claude2, Claude, ChatGPT, MiniMax critics). Addition `p·ρ·Φ` at `n_w = 300`: from 2.1 to 139 generations per response | **Reject for verification**; study only for privacy |
| **MPC** | Computation without assembling the secret in one place | Independence from `q`: protection rests on an honest majority or on "at least one honest" with the right to abort the work; at `q = 1` there is no protection | To hide *the choice* of verification, everything must be processed — `1/p` = 31 / 303 / 4329 times more expensive than a coin at `n_w` = 30 / 300 / 4320 (Claude critic). Hiding *the request*: Claude critic — from 151 MB per token of the lower bound to 0.15–1 GB, 10–67 minutes per response at 1 Gbit/s; ChatGPT critic — 448 MB per position, 224 GB per 500 positions; MiniMax critic — up to 180 TB per response (estimates differ by orders of magnitude, see section 7) | **Reject for verification** |
| **iO** (indistinguishability obfuscation) | In theory — execution of a program without revealing its design | No practical implementation for the model; even ideal iO leaves the fraudster a "trial run" of his forgery through the detector | Not estimated | **Reject** |
| **Point function obfuscation** | Verification "did it match the reference" without revealing the reference | Protection with a small answer space: brute force; it is the same trap | Hash | Only as part of a trap |
| **Functional encryption** | Obtaining the value of a function by the holder of a functional key | Hiding the function from the key holder (a separate scheme is needed); an issuer of keys is needed | Not estimated | **Reject** for this task |
| **PIR, ORAM** | Hiding the read index from the server | Hiding the rule; evidence of the origin of data | ChatGPT critic: in two-server PIR for 10,000 records of 32 bytes — a lookup of about 320 KB per server and non-collusion of servers | **Reject** for this task |
| **Traps** (a request with a known answer) | New information: a reference correlated with the truth | A reduction in cost. A trap of the same strength as a coin costs the performer's work (≈ one generation, paid for and needed by no one) and the reference (one generation, if it is fresh). The coalition recognizes a repeat of an old request | Ratio of the trap price to the coin price `≥ 1/((1 − σ)ρ)`, where `σ` is the probability of recognizing the trap: at `ρ = 0.21` — 5.3 / 6.8 / 9.5 / ∞ times at `σ = q` = 0.1 / 0.3 / 0.5 / 1; at `ρ = 0.40` — 2.8 / 3.6 / 5.0 / ∞ (claude2). gpt2: one-time traps for 1% of work with two generations add 2.02% | **Only a "signal upward"**, without lowering the frequency and without the mark "verified" |
| **Secret statistical tests and thresholds** | Diagnostics of mass failures and implementation errors | A reduction in frequency: the `TV` bound; the threshold is learned by probes | Little | **Only a "signal upward"** |
| **Hidden verifier, unlinkable payers** | Against bribery after appointment (VRF appointment) and against distinguishing lazy payers (one-time payer keys, claude1) | Independence from `q` under verification by a committee. Unlinkable payment needs an issuer or another mechanism without special rights — not built | Kilobytes and seconds (claude1), not fully estimated | **Take VRF appointment; study unlinkable payers** |
| **ZK proof of computation** | The only path to a publicly verifiable verdict on a private witness | Not about the secrecy of rules; the cost for Qwen has not been calculated. Pilot experience: zkVM execution 17,700 times slower even without building a proof | Not estimated | **Study** separately |
| **"Moving target defense"** | The value of changing the configuration while the observer has not adapted | In SkyNet the best change is on every task, that is, a fresh coin | Zero beyond the coin | Reduce to a fresh coin |
| **Bank anti-fraud, CAPTCHA** | They work through a closed server, the cost of an attempt, non-monetary sanctions and one-time challenges | None of this appears in SkyNet by changing the rules file (section 2.5) | — | Do not transfer |

**Separate finding of claude1 (not about secrecy): Freivalds' check.** Checking a matrix-vector multiplication by a random projection can be cheaper than the multiplication itself: the ratio is about 1740 per token and block [calculation, confirmed by the Claude critic]. But the ChatGPT critic noted that this is not a speedup of the response: intermediate activations must be transmitted, non-linearities, rounding of profile v2 and the freshness of the vector for each request must be taken into account. claude1's conclusion "the traffic of activations makes this worse than a full pass" is correct. One cannot declare the whole of Qwen verified by a single multiplication.

---

## 4. Recommended strategy

### 4.1. Steps

This is the previous council's strategy ("payer-inspector"), refined by the papers and critics of this council. No step requires secret rules. Steps 3, 4 and 9 depend on decisions not yet adopted (section 5).

1. **Open core.** The generator of the verification instance, the family of admissible verifications and the selection law are the open part of the core with a pinned fingerprint (D4). "New rules at random times" are new values of randomness, not new algorithms.
2. **Fixing.** The performer computes in exact profile v2 and, in one record with acceptance, puts the ciphertext of the response into the ledger (D24). Until that moment no choice of verification is made.
3. **The payer's secret coin.** After irrevocable fixing, the payer's program takes fresh randomness and decides whether to verify the response, with probability `p = max(p_user, (R − c_f)/(R + H_lock))`; at `c_f ≈ 0` this is `R/(R + H_lock)`; at `H_lock = 0` (newcomer) — always. For the payer's own money a beacon is not needed.
4. **A verifiable coin where other people's money depends on it.** If someone else's payment depends on the coin's outcome (a lottery with a common prize, disputes of third nodes), the coin must be verifiable: a VRF of a key registered per order before fixing, or a commitment to a salt published before fixing (gpt2, claude2). A commitment made after fixing is meaningless: the payer chooses the outcome already seeing the response (mm5's error in the D28 proposal).
5. **The amount lock.** `H_lock` is only the amount that matures after the dispute deadline; the verification deadline `δ` is much less than the maturation window `W` (in active time, D12). The first proven forgery atomically burns the key's entire unmatured amount, including the rewards of the same wave; the victim is refunded no more than their payment (candidate D26). Without atomicity the formulas do not withstand a wave: 10 parallel forgeries at `R = 1`, `H = 4`, `p = 0.2` give `+4.4295R` instead of `−2.49676R` [calculation].
6. **Marks.** "Verified" — only a response fully verified before display; everything else — "unverified" by default. An unverified training step does not enter the released model (D6).
7. **Common samples under D20.** The training audit, the exam, the lottery with a common prize and the appointment of verifiers take randomness from no fewer than two independent sources (an external threshold beacon and a VDF from the final block), mixed by a hash; the round is appointed before fixing and begins after it. Appointed nodes learn of the choice through a VRF.
8. **Signals only upward.** Traps, anomalies and statistical tests can appoint an additional verification, but do not lower the frequency and do not give the mark "verified".
9. **Payer unlinkability** (a research element). One-time payer keys and a relay so that the performer cannot distinguish a verifying payer from a lazy one (claude1). Until the mechanism is built, the risk table contains the row "lazy are distinguishable: up to `+R`, including for a newcomer".
10. **What is not in the basis.** Secret rules, network verification keys, threshold committees of holders, TEE, FHE, MPC, iO.

### 4.2. The role of the blockchain and the beacon: a "dynamic detector on a blockchain" in the correct form

The owner's question about a dynamic detector on a blockchain receives the following answer. The blockchain does well what is required of a detector, *except* secrecy:

- **fixes the response before the choice of verification** — without this no randomness helps;
- **stores commitments** to future rounds and salts, so that no one can choose a convenient outcome;
- **makes the choice reproducible**: any node after the round itself computes what was chosen, and verifies the basis of the decision even after a complete stop of the network;
- **executes burning and one-time calculation**.

"Dynamism" is given not by encryption of the rules, but by the fact that the verification instance is each time derived from randomness that did not yet exist at the moment of fixing the response. For a private response this randomness is the payer's coin; for common decisions — the beacon under D20. The papers named it thus: "an open rule generator in the core plus a rule instance derived from the beacon, whose round is appointed before fixing" (claude1); "the rules are open, the secret is only in the choice: who, when and which rule to apply" (mm4); "unpredictable, not secret" (mm3).

Two mistakes to avoid:

- **A beacon in the payer's monetary decision** (mm3, mm4). A public lottery says *what* to verify, but the same payer verifies; a lazy payer will not verify even by a public lottery, and there is no sanction for not verifying without a deposit (R5). A public lottery here only adds an assumption about the beacon's honesty and a round delay (the Claude and DeepSeek critics; mm2 and claude2 say the same). mm3 and mm4 disagree with this (section 7).
- **A fallback mode "by the last available value"** (mm3). If the beacon is unavailable and the epoch's verifications proceed by an already known value, the fraudster knows in advance what will not be verified. This directly violates D20. If the round is unavailable, the disputed transaction waits or verification is mandatory.

One more clarification: "choose the convenient one of two independent bits" lowers the probability of mandatory verification from `p` to `p²` (the ChatGPT critic), whereas *mixing* two sources by a unique hash is exactly what D20 requires. mm5's proposed addition to D19 "the secret coin and the beacon are not mixed" confuses these two actions and would contradict D20 (the Claude critic).

### 4.3. Cost

The secrecy of rules does not change the cost: it touches neither `ρ` nor `γ`.

| `n_w` | `p = R/(R + H_lock)` | Verification `p·ρ` at `ρ` = 0.10 / 0.21 / 0.40 | Total versus Q8_0, batch 1 | Batch 8 |
|---|---|---|---|---|
| 30 | 3.23% | 0.32% / 0.68% / 1.29% | +50.5…+82.3% | +152…+186% |
| 300 | 0.33% | 0.033% / 0.070% / 0.133% | +50.0…+80.2% | +150…+181% |
| 4320 | 0.023% | 0.0023% / 0.0049% / 0.0093% | +50.0…+80.0% | +150…+180% |

The table is [calculation] by the formula `γ(1 + pρ) − 1` and the measured `ρ`, `γ` (the MiniMax critic, checked by the DeepSeek and Claude critics). The ChatGPT critic reminds us that the extreme points of the ranges of `γ` and `ρ` are taken from different cards and were not measured as a pair; this is an envelope, not a measurement.

- **Newcomer.** The first response — full verification, 10–40% of its generation. Under strictly sequential honest work and growth of `H_lock` by `R` per task, the expected number of full verifications over the first 30 tasks equals `1 + 1/2 + … + 1/30 ≈ 3.995`; this is 1.33% / 2.80% / 5.33% of the window's work at `ρ` = 0.10 / 0.21 / 0.40 (mm1, ChatGPT critic) [calculation]. With a parallel start from an empty account, every request costs a full verification.
- **The 5% benchmark.** As a surcharge for verification it is achievable: `p·ρ ≤ 0.05` requires `p` no greater than 50% / 23.81% / 12.5%, that is, `H_lock/R ≥ ρ/0.05 − 1` = 1 / 3.2 / 7 (gpt1, gpt2) [calculation]. As "5% over ordinary generation" — no: the exact profile itself costs +50…+80% [measured γ]. The only path to 5% is faster bitwise identical kernels.
- **Additions of the strategy.** 32–64 bytes of commitment or hundreds of bytes of VRF per response where coin verifiability is needed; the beacon — hundreds of bytes per round per batch and a delay of one round only for common samples (Claude critic) [calculation].
- **Who pays** (mm4, MiniMax critic). The surcharge of the exact profile `γ − 1` is borne by the performer on every paid response; verification `p·ρ` — by the payer from their prepayment. Moving verification to the payer removes the role of "verifier who is paid for verification" from [CURRENT_DESIGN](CURRENT_DESIGN.en.md), section 1. Then either the price `R` rises by 50–80%, or the performer's margin tends to zero. This is a separate question for the owner (section 5).
- **Lottery B** (only selected and fully verified responses are paid, a variant of gpt1, gpt2 and the ChatGPT critic). With a selection share of 5%, verification costs on average 0.5 / 1.05 / 2% of exact generation time, but 95% of responses remain unverified and unpaid; the variance of an individual payment is `19R²`; the probability of receiving no payment at all over 20 independent requests is `0.95²⁰ ≈ 35.85%`, over 30 — 21.46% [calculation].
- **Training.** A full repeat of the step costs about 100% of the step for each verifying node; no scheme has shown the 20% benchmark. With `N = 1000` receiving nodes, even at zero other costs, no more than 0.0002 of the step's work remains for one verification (ChatGPT critic) [calculation].

### 4.4. Residual risk

Expected gain of a single forgery against inaction; "harm" — the share of undetected forgeries of the harmer, all with the mark "unverified". The table is assembled from the tables of the Claude, DeepSeek, ChatGPT and MiniMax critics and STRATEGY_SEARCH 5.3; **the cells corrected by this council are highlighted**. A hidden detector does not improve a single row [calculation].

| Case | `q = 0.1` | `q = 0.3` | `q = 0.5` | `q = 1` | Newcomer, `H = 0` |
|---|---|---|---|---|---|
| Money, payer verifies themselves; ledger alive, D26 and D23 resolved | ≤ 0 | ≤ 0 | ≤ 0 | ≤ 0 | `−c_f` (always verified) |
| Same, but the coalition `q = 1` includes block producers and censors the dispute | — | — | — | up to `+R` | up to `+R` |
| False response with the mark "verified" | 0 | 0 | 0 | 0 | 0 |
| Harm at `p = R/(R + H)`: the entire series of `n_w` forgeries will pass | ≈ 50% | ≈ 50% | ≈ 50% | ≈ 50% | 0 for an honest payer |
| Harm at `p = 3R/(R + H)` | ≈ 12.5% | same | same | same | 0 |
| Lazy payers of share `λ`, the performer does not distinguish them | ≤ 0 at `p(1 − λ) ≥ R/(R + H)` | same | same | same | **`+λR`** |
| Lazy payers are distinguishable (by probes with new keys — for free) | up to `+R` | up to `+R` | up to `+R` | up to `+R` | **up to `+R`** |
| A payer without equipment delegated verification to a random triple | +0.001R | +0.027R | +0.125R | +R | same |
| Common sample under D20, at least one source honest | ≤ 0 | ≤ 0 | ≤ 0 | ≤ 0 with an honest external; otherwise up to `+R` | same |
| Only an internal beacon of participants 64/43 | ≤ 0 except 4.8·10⁻²⁸ | except 9.4·10⁻¹⁰ | except 0.41% | up to `+R` | same |
| For comparison: a secret epoch rule at a committee | leaks over 10 applications with probability 0.65; then about `(1 − p)·E·R` per epoch | 0.97 | 0.999 | up to `+R` per forgery | probes are free: up to `+R` |
| Training without a self-verifying node | up to `+R` | up to `+R` | up to `+R` | up to `+R` | up to `+R` |

How to read the table:

- **The row "≤ 0 at any `q`"** is true only under the named conditions: `q` is the collusion share among outside verifiers; if the same coalition controls block production or the beacon, it can delay or censor the proof (gpt1 and gpt2 said this directly). Also needed are `δ ≪ W`, atomic burning (D26), resolution of the conflict with D16 and the false-dispute rule (D23, calculation M9).
- **Execution of verification matters no less than frequency.** Example of the ChatGPT critic: `R = 1`, `H = 3`, `p = 1/4`, `c_f = 0` give exactly zero expectation; if the payer executes only 90% of appointed verifications, the probability of catching is 0.225 and the gain is `+0.1R` [calculation]. If the first forgery can be explained as a failure under the current D16 and `H` is preserved, the expectation `(1 − p)R − c_f` is positive.
- **"≈ 50%"** is the probability that *the entire series* of `n_w = H/R` forgeries passes as `H` grows after each skip (`h/(h + n)` at `n = h`). One targeted forgery of a mature key passes with probability `1 − p`: at `H = 4320R` this is about 99.977% (ChatGPT critic per ds2).
- **The "lazy" rows** have been corrected: the previous value 0 for a newcomer is incorrect (section 1, item 6). Scenario: a fresh key submits a forgery to payer `X`; if `X` verifies, only `c_f` is lost, there is nothing to burn; if `X` is lazy, the key receives `R` and the knowledge "`X` is lazy"; then the coalition's mature keys submit forgeries only to lazy ones (Claude critic). The ChatGPT critic added that even with complete indistinguishability the condition `p(1 − λ) ≥ 1` for a newcomer is unfulfillable at `λ > 0`, and unlinkable keys close only one channel of distinction: text, time, request size and the associated payment remain.

### 4.5. Newcomer

A newcomer with an empty account (`H_lock = 0`) against an honest payer is always verified and loses `c_f`. Secrecy of rules adds nothing here. Two caveats of this council: against a lazy payer a newcomer receives up to `+R` (section 4.4), and free new keys can raise the share of fully verified requests: if the share of work on the first orders of empty keys equals `f`, and on the rest `p = 0.1`, the surcharge equals `ρ[f + 0.1(1 − f)]`, and the 5% condition at `ρ = 0.21` gives `f ≤ 0.1534` (ChatGPT critic) [calculation]. No scheme of the council yet withstands a stream of new keys and self-payment at the same time.

### 4.6. Lazy payer

The strategy rests on the payer actually tossing the coin and verifying. A lazy payer whom the performer can distinguish gives up to `+R` to any key. Means in descending order of strength: (a) the payer's program by default executes the core rule, and disabling verification removes the mark "verified" from the response; (b) unlinkable payer keys (claude1) — a payment mechanism without an issuer with special rights is needed: a blind signature needs an issuer, Privacy Pass (from memory) — a scheme with a server-side issuer; a threshold issuer again introduces `q` (Claude critic); (c) a public beacon lottery does *not* correct a lazy payer (section 4.2). How to combine unlinkability with the false-dispute rule without a deposit (D23) has not been resolved.

### 4.7. User without equipment

A user who cannot recompute the response themselves is not protected by this strategy. If they delegate verification to a random triple, the coalition receives `q³R`: +0.001R / +0.027R / +0.125R / +R; with one assistant — `qR`, and with a deliberately chosen accomplice — up to `+R` at any average share (ChatGPT critic) [calculation]. A limited positive leakage is directly prohibited by D1, so this is an open hole in D21. A hidden detector does not close it: claude1 showed a counterexample with "secret canaries" — a colluding verifier honestly passes all others' control tasks and lies only on their own forgeries, which they recognize by the performer's key or by freedom of choice (a forgery need not be deterministic, the exact answer is deterministic). The honest option is to sell two service tiers with a clearly written difference: "verified by me" and "verified by appointed ones, leakage `R·q^k`" (mm1).

### 4.8. Harm

A harmer does not need profit. At any frequency `p < 1` some of his forgeries pass. The only protection is the mark "unverified" by default and "verified" only after full verification before display. A hidden detector does not change the harm row (all papers). mm1 found the only place where *fresh choice* substantially changes the picture of harm: under partial verification (primarily of the training step), against an open fixed sample the fraudster finds unverifiable cells in one exact run and forges only them, catching 0; a fresh choice of the sample after fixing gives catching `s` (the share of the verified part) for one deviation and `1 − (1 − s)^m` for `m` deviations. The DeepSeek and Claude critics clarified: this is fresh randomness, not secrecy of rules; the motive for such forgery is harm, not money (against honest work an exact forgery gains about zero); and the conclusion rests on an unestablished assumption that the cells of the training step can be forged independently.

---

## 5. Decisions

The formulations below are **recommendations**, not adopted decisions. The immutable requirements R1–R6 are not changed by editing a roadmap line. According to D4, after launch with a pinned fingerprint, a change in the set of admissible transitions requires a transition to a new network; changing a key does not give such a right (ChatGPT critic).

### 5.1. D4 — supplement, do not change the meaning

The current text of D4: verification is automatic, without votings; each node itself executes verification according to the pinned fingerprint of the rules. The council is unanimously against weakening D4 for the sake of secret rules: a secret rule requires accepting the verdict of key holders, an enclave or a group, which the node itself cannot verify. The ChatGPT critic showed what such a weakening would look like: "the node accepts the verdict of the current program chosen by the epoch's key holders", "the node accepts the report of a measured program along the manufacturer's trusted chain" or "the node accepts a bit issued by a group".

**Proposed supplement** (merger of variants by the Claude and ChatGPT critics, claude1, claude2, gpt1, mm5's D27 proposal):

> "The core may accept as input randomness unknown to the performer until the final fixing of the result: (a) the secret coin of the party whose own decision is protected, tossed after fixing; (b) the values of D20 sources in rounds appointed before fixing and beginning after it. The generator of the verification instance, the family of admissible verifications and the selection law are the open part of the core with a pinned fingerprint; new rules at random times are new values of randomness, not new algorithms. A realized instance that affects other people's rights is published no later than payment and recomputed by every node. The payer's local mark by itself does not create a network evidence of work. The basis of a common decision contains no long-lived secret rules and verification keys, threshold committees, TEE attestations or closed verdicts; they are admissible only as additional verifications that raise the frequency."

**What does not change:** the immutability of the core, the absence of votings, independent verification by every node. **What it breaks:** nothing; the supplement closes the direction of "secret detectors" as a basis for the guarantee. The possibility of a publicly verifiable proof of a pinned relation (ZK) remains open and does not require an amendment to D4 (ChatGPT critic).

### 5.2. D20 — clarify

The current text of D20: no fewer than two independent public sources, a value at a pre-appointed moment after final fixing, without the right to skip.

**Proposed clarification** (Claude critic with additions of the ChatGPT critic):

> "No fewer than two independent public sources; their values are combined by a unique hash function with a domain label and a batch identifier, and not by choosing one of the values. The round of each source is appointed before final fixing and begins after the final acceptance of the block with the fixing. Skipping, re-drawing, replacing a source or switching to a previously known value are prohibited; if the round is unavailable, the disputed transaction waits, and a new request does not receive a ticket for this round. The beacon is used for samples that affect other people's rights (training, exam, lottery with a common prize, appointment of verifiers); for private verification by the payer of their own money it is not required. An internal threshold beacon of participants can be one of the sources only with a recorded assumption about the collusion share of its holders and cannot be the only one. A VDF from the same block is not considered an independent source. Trust in the sources is an assumption under R4."

**What it excludes:** the fallback mode "last available value" (mm3), mm5's amendment to D19 ("do not mix sources"), a beacon in the payer's monetary decision (mm3, mm4). **Open risk:** if "wait for the round" means an infinite delay, this is an unclosed risk R1/R6 (ChatGPT critic); the MiniMax critic proposes that instead of waiting, verification be considered mandatory.

### 5.3. What does not change

- **D1** — do not change and do not weaken to "while `q` is small"; a limited positive leakage remains a violation (all papers and critics).
- **D7** — a secret rule does not fulfil it at any threshold (section 2.4).
- **D19** — do not change: mm5's addition is erroneous (section 4.2).
- **D6** — secrecy does not change the harm row; the marks are clarified under question 3 of the previous consolidation.

### 5.4. Relation to the eight questions of the previous consolidation

The eight questions of [STRATEGY_SEARCH](STRATEGY_SEARCH.en.md), section 6, remain open. This council added to them:

| Question of the previous consolidation | What the sixth council added |
|---|---|
| 1. D21, D11, D2: whether to pay for a response skipped by the coin | No new arguments. The cell "lazy payer × newcomer" has been corrected (up to `+R`): if payment for the skipped one is allowed, protection against distinguishing the lazy is needed. The ChatGPT critic still favours full verification as the main contract and Lottery B as a separate one |
| 2. D7: which verification is admissible for payment | It is confirmed that neither secrecy, nor attestation, nor a committee can lower the lower frequency; raising it is allowed. Added: the share of *executed* verifications matters, not only the frequency (example `+0.1R`) |
| 3. D6: marks | A trap, statistics and a hidden detector do not give the mark "verified" |
| 4. D16: honest failure | If the first forgery can be declared a failure and `H` preserved, the coin does not deter: `(1 − p)R − c_f > 0`. A decision on D16 is needed before any enabling of payment for the skipped one |
| 5. D8: deadline and rights of dispute | The condition `δ ≪ W` and liveness of the ledger enter the row "≤ 0" (section 4.4) |
| 6. D23: block until M9 | None of the eleven papers calculated M9; the block is retained. Payer unlinkability adds a new question to M9 |
| 7. New D26: amount lock | The necessity of atomic burning of the wave is confirmed; the common epoch bit is a new counterexample (`+8.1R`) |
| 8. D1: whether to change | Do not change |

### 5.5. New decision questions of this council

**Question A (D4).** Should the supplement to D4 from section 5.1 be adopted? *Recommendation of the Claude, ChatGPT and DeepSeek critics:* yes; the meaning of D4 does not change. *Where they diverged:* the ChatGPT critic proposes a more detailed wording that explicitly speaks of verification "by a publicly verifiable proof of the pinned statement"; the DeepSeek critic considers a short note about randomness after fixing sufficient; the MiniMax critic (like mm2 and mm5) considers that D4 need not be changed at all, because the verification rule is open anyway.

**Question B (D20).** Should the clarification of D20 from section 5.2 be adopted? *Recommendation:* yes. *Where they diverged:* what to do when the round is unavailable — wait (the Claude and ChatGPT critics) or consider verification mandatory (the DeepSeek and MiniMax critics). Waiting may become an infinite delay; mandatory verification changes the price and, in a lottery, the composition of winners.

**Question C (beacon or coin in the monetary decision).** Should it be recorded that the beacon is not used for private verification by the payer of their own money? *Recommendation* of the Claude and DeepSeek critics, as well as claude1, gpt1, gpt2, ds1, ds2, mm1, mm2: yes. *Against:* mm3, mm4, mm5 (public lottery instead of a coin), claude2 (payer's VRF plus a beacon for common affairs). The DeepSeek critic proposes first comparing both schemes with a mini-agent on identical attacks (section 6).

**Question D (unlinkable payers).** Should a mechanism be included in the research programme under which the performer cannot link the requests of one payer? *Recommendation* of the Claude critic: yes, as research; until it is built the risk table contains the row "lazy are distinguishable: up to `+R`". *Open:* payment without an issuer with special rights, compatibility with D23, distinction by text and time.

**Question E (weight).** Should the weight specification ([CURRENT_DESIGN](CURRENT_DESIGN.en.md), section 4) record that the weight by which holders or verifiers are selected does not grow from self-paid requests? *Recommendation* of the Claude critic: yes. claude2 proposed selection "by the weight of verified work" without such a caveat.

**Question F (who pays for the exact profile).** How should the surcharge `γ − 1` be distributed if the role of the paid verifier disappears? *Raised* by mm4 and the MiniMax critic; no solution has been proposed.

**Question G (new decisions of mm5).** Should D27 ("secrecy of choice, not secrecy of verification") and D28 ("coin with delayed disclosure") be adopted? *Recommendation of the critics:* D27 in meaning is part of the D4 supplement (section 5.1); D28 duplicates the coin commitment of gpt2 and claude1 and makes sense only if the commitment is published *before* fixing the response.

---

## 6. What to calculate with mini-agents and what to check by experiment

### 6.1. Mini-agents (exact fractions, control hash, repeat on a second device)

The common list of the four critics. For each calculation, preserve the description of the rules, inputs, exact fractions, worst history, version and control hash (ChatGPT critic).

1. **Epoch rule versus fresh coin.** Wave, `H_lock`, burning of the entire amount, adaptive sequence. Reference values: `+8.1R` / `−2.3751096381R` (gpt2), `98.01R` (claude2), 1/5 → 1/9 → 0 (claude1), `+4.4295R` / `−2.49676R` / `+7.2R` (previous council and ChatGPT critic).
2. **Probes of lazy payers with new keys.** Expectation of a probe, time to recognition of the payer, gain of mature keys; with linkable and unlinkable payers. Expectation of the Claude critic: with linkability, deterrence against the lazy equals zero.
3. **Secret coin versus public beacon lottery** on identical attacks (DeepSeek critic). Expectation: equal monetary outcomes and a higher cost for the public lottery.
4. **Linear program of a mixture of tests** (gpt1, gpt2): reference "three classes → 2/3 versus 1/2", adding an uncovered class → 0; minimax over the matrix "test × forgery".
5. **Threshold tails:** binomial, without replacement, by weight with self-payment, with bribery after appointment. Reference "3 out of 5": `107/12500`, `4077/25000`, `1/2`, `1`; control SHA-256 of gpt1's four lines, repeated by the ChatGPT critic: `fd83fbdd42baa56d982eba3be90888cf3ec5a6261b5daa53d42fdc42b99c8323`.
6. **Traps:** `1/((1 − σ)ρ)` on the grid of `ρ` and `σ`; recognition of a repeat; amortization of a bank of references against recomputation; verification of mm2's statement about the almost zero price of repeating a verified request.
7. **Deviations in the VRF and the payer's commitment:** refusal to disclose, several keys, interruption after disclosure, lottery with a common prize.
8. **Mixture of D20 sources:** bias with one honest source, with withholding of a block, with unavailability of the round; prohibition of the "last value".
9. **mm1's "surgical" forgery** against an open fixed and a fresh sample: catching 0 versus `s`; threshold `p·s ≥ (R − c)/(R + H_lock)`.
10. **Count of non-linear operations per token** by the pinned D5 configuration for FHE and MPC estimates (now 1.4·10⁷–2.6·10⁷ approximately); estimates of DKG, commit–reveal, VRF in bytes and messages.
11. **Batch 8 at the payer** (mm3): `ρ` is measured relative to batch generation, and recomputation of one response by the payer does not become cheaper that way.
12. **Correction of tables:** mm1 (`k = 10`, `H_lock = 10R`), mm5 (`p·ρ`), the cell "lazy × newcomer" in STRATEGY_SEARCH 5.3.
13. **M9** — the price of a dispute for rule D7 and the condition for removing the D23 block; self-dispute, refund limit, stream of new keys.

### 6.2. Experiments

**No experiment is needed for the conclusion about a hidden detector:** these are theorems, and measurement does not refute them (claude1, claude2, ds2, the Claude and DeepSeek critics). Experiments with FHE, MPC and TEE are not needed either: their best outcome does not change the theorems.

**Within D5 (permitted):** O5 — quality on 320 tasks; O3 and O4 with faster bitwise identical kernels — the only path to the 5% benchmark.

**Outside D5 — only with separate permission from the owner:**

- time of one verification pass on a laptop CPU and on a phone, cold and warm start, energy;
- how much the request metadata (time, size, text) allow the performer to distinguish a verifying payer — the price of unlinkable keys depends on this;
- the frequency of silent hardware discrepancies `P_f` — before any amendment to D16;
- the share of matching tokens of Q8_0 and the exact profile (for estimating a cheap forgery and for exact speculative decoding);
- the delay and cost of a round of a real beacon, behaviour with a silent source;
- for traps — whether verification is recognized and how much the references cost;
- exact repetition of the training step as a prerequisite for any verification of it.

---

## 7. Disagreements not resolved by the council, and questionable references

### 7.1. Disagreements

1. **Paying for a response skipped by the coin versus full verification of every paid response.** claude1, claude2, ds1, ds2 and mm1–mm5 rely on payment for the skipped one under the risk of burning the unmatured amount; gpt1, gpt2 and the ChatGPT critic — on full verification as the main contract and Lottery B as a separate one. Inherited from the previous council; the owner's decision on D21, D11, D7.
2. **Beacon or coin in the payer's monetary decision** — section 5.5, question C. mm3 and mm4 believe that a public lottery removes the assumption of an honest payer; the Claude and DeepSeek critics consider this an error (a lazy payer will not verify even by a public lottery). Not calculated.
3. **`R/(R + H_lock)` or `R/H`.** The first is exact for money; the second gives a margin and a finite expected number of forgeries before catching at a fixed `H`, but costs about twice as much at a small `H`. The ChatGPT critic showed that as `H` grows after each skip, for both rules the average number of skips before the first catch is infinite. The council gave no new arguments.
4. **A trap as an independent gain.** mm2 (a secret reference is the only real gain) and ds1 (saving of a cached reference) versus claude2, mm4, mm5, gpt1 and the Claude and DeepSeek critics. The ChatGPT critic took an intermediate position: a reference already known to an honest payer can lower the marginal price, and for fresh indistinguishable traps `σ` can be 0 even at `q = 1` among outside performers. The calculation has not been performed.
5. **A mixture of verification types as a means of saving.** gpt1, gpt2, claude2 — possible with proven coverage of error classes; mm2 — never. For Qwen coverage has not been proven.
6. **Internal threshold beacon of participants.** mm3 — the best primitive; mm5 — external only; claude1, claude2 and the Claude critic — admissible only as one of the sources.
7. **To what extent R2/R3 prohibit common secrets.** ds1, mm1, mm3 — fundamentally; claude2, the Claude and ChatGPT critics — only secrets needed to verify past decisions.
8. **The cost of MPC.** Estimates differ by orders of magnitude: ds1 — 2.4–14 MB per token (the critics believe this is the price of a verification trace, not of MPC); Claude critic — 0.15–1 GB per token; ChatGPT critic — 448 MB per position; MiniMax critic — up to 180 TB per response (he considers all multiplications network-based, while the ChatGPT critic notes that multiplication of an open weight by a split activation is performed locally in many protocols). The conclusion "MPC is outside the budget and depends on `q`" does not change because of this.
9. **FHE multipliers:** ds1 `10³–10⁶`, claude2 `3·10³–2·10⁵`; the ChatGPT critic believes that multiplying the bootstrap estimate by `ρ` of a finished pass is incorrect, and an estimate of an identical pass under a specific scheme is needed. The conclusions do not depend on this.
10. **A hidden sample under partial verification** (mm1): "secret detector" or fresh coin — a difference in words; applicability to the training step depends on the unmeasured independence of cells.
11. **D16.** Burn `H_lock` for any proven discrepancy with compensation to the honest from the network fee (the line of claude1 and the Claude and DeepSeek critics) versus preservation of previous rewards in an honest failure (gpt1, gpt2, ChatGPT critic). A measurement of `P_f` is needed.
12. **Training.** No scheme fulfils D7 at `q = 1` within 20%.
13. **The main class of forgeries:** expensive "surgical" (mm1) or cheap Q8_0 (mm3, mm4). Not measured.

### 7.2. Errors found in the papers' numbers

So that erroneous numbers do not get into other documents:

| Paper | Statement | Correct [critics' calculation] |
|---|---|---|
| mm1 | At `H_lock = 10R` frequency 0.0909 and verification cost 0.005–0.009% | `0.0909·ρ` = 0.91–3.64% |
| mm1 | Leakage of "tens" at `q = 0.1`: `1·10⁻⁵R` | `10⁻¹⁰R` |
| mm1 | Threshold 25% at `H_lock = R` | 29.29% under mm1's own parameters |
| mm5 | `p·ρ` = 0.021–0.042% at `p = 0.1` | 2.1–4.0% (mm5's own table is correct) |
| mm5 | "FHE is deterministic, the observer builds a dictionary" | Secure FHE schemes are probabilistic |
| mm5 | "VRF is unpredictable for the owner" | The owner computes the VRF whenever he wants |
| mm5 | Full repeat of the training step ≈ 36.8% | 36.8% is an example of mixed load; repeat of the step ≈ 100% |
| mm2 | "5% is achievable at `p ≤ 0.33%`" | At `ρ = 0.21`, `p ≤ 23.8%` is admissible |
| mm4 | "VRF does not disclose the choice" | Verification of the VRF proof discloses the value |
| ds2 | `N·H_s ≈ 2718` attempts | About 890 without replacement; one safe position is needed |
| ds1 | A trap costs `φ·ρ`, a cached reference saves | A trap costs no less than the performer's generation; the cache must first be obtained |
| ds1, ds2 | Traps add catching `φ` at any `q` | No more than `φ(1 − q)` on a repeat; at `q = 1` — 0 |
| claude1, claude2, mm3, mm4, STRATEGY_SEARCH | Lazy payer × newcomer = 0 | Up to `+R` |
| claude2 | Formula of the epoch example `(1 − p)(E − 1)R` | `(1 − p)·E·R − p·H_lock = 98.01R`; the coincidence is accidental |

### 7.3. Questionable references (critics' estimates from memory, without checking)

| Paper | Statement | Assessment |
|---|---|---|
| mm5 | "RandAILight" as a beacon | Questionable; the name is unknown to the critics |
| mm5 | "iO is theoretically possible, Barak and co-authors ~2001" | Confused: Barak and co-authors 2001 — impossibility of "black-box" obfuscation; iO candidates — Garg and co-authors 2013 |
| mm1 | "iO roadmap of Barak and co-authors, 2019" | Questionable |
| mm2 | Appendix F: "Ben-Or and co-authors", "Allingham, Melvin, Temple 1992", "Dwork ~1999", "Hashcash — Khoumstein", "Awasthi", "Randcast Bader ~2020" | Questionable on almost all points; do not transfer to the consolidation |
| mm3 | "Cui, Wang et al., Skoglid et al." on moving target defense | Questionable |
| ds1 | "Canetti 1997 — point functions in the random oracle model" | Questionable (from memory — a DDH-type assumption) |
| ds1 | "Bishop–Jain–Kowalczyk 2018" | Questionable as to the year (from memory 2015) |
| ds1, ds2 | "drand ~30 s" | Partially: from memory different chains have 30 s and 3 s |
| ds2 | "MPC 5.98·10¹² MAC (claude2)" | The reference is imprecise |
| claude1 | "SGX.Fail, Secret Network master key, 2022" | Questionable in details (the author marked it himself) |
| claude1 | Privacy Pass as a model of issuance without a special party | From memory — a scheme with a server-side issuer |
| claude2 | PIR lower bound — Beimel, Ishai, Malkin | Questionable: their works are on PIR with preprocessing; the classical bound, from memory, is due to Chor and co-authors |
| claude2 | Lowd–Meek, Tramèr: `d` binary queries suffice for any classifier | Questionable in general form |

The remaining references of the papers (Shamir, Feldman, Pedersen, Gennaro–Jarecki–Krawczyk–Rabin, Micali–Rabin–Vadhan, Boneh and co-authors on VDF, Rivest–Shamir–Wagner, Aumann–Lindell, Asharov–Orlandi, inspection games, Barak and co-authors on the impossibility of "black box") seem to the critics to be correctly attributed in direction; the primary sources were not checked.

---

## 8. Who did what

The council worked from the project materials, without network access and without experiments.

- **Eleven independent papers:** ChatGPT — two (gpt1, gpt2), DeepSeek — two (ds1, ds2), Claude — two (claude1, claude2), MiniMax — five (mm1 with emphasis on economics, mm2 — on protection against fraud, mm3 — on distribution and recovery, mm4 — on counterexamples, mm5 — on non-standard solutions). Each paper analysed six directions from the assignment: who holds the key, how to verify by an unknown rule, what can be a secret detector, theory, cost and compatibility with decisions.
- **Four critiques:** one each from ChatGPT, DeepSeek, Claude and MiniMax (the MiniMax critique is formatted as a proposal with criticism). Each critic read all eleven papers, looked for errors and counterexamples, and recalculated the key numbers. The DeepSeek critic checked arithmetic with local programs on exact fractions, the Claude critic — with short Python calculations, the ChatGPT critic reproduced the control hash of gpt1's table.
- **Consolidation:** this document was compiled by Claude from the papers and critiques. No new estimates or numbers beyond the papers, critiques, D5 results and STRATEGY_SEARCH were added; where the critics diverged, this is stated.
