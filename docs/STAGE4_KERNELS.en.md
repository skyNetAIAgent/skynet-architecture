<!-- translation of docs/STAGE4_KERNELS.md, source sha256: e81d4e27191f3ce009ea9b71602c58405e742a7229fc972d8c69ae520e675812 -->

# Stage 4. Byte-exact contract of built-in computations

**English** · [中文](../i18n/zh/STAGE4_KERNELS.md) · [Español](../i18n/es/STAGE4_KERNELS.md) · [Français](../i18n/fr/STAGE4_KERNELS.md) · [Deutsch](../i18n/de/STAGE4_KERNELS.md) · [Italiano](../i18n/it/STAGE4_KERNELS.md) · [Русский](STAGE4_KERNELS.md) · [Português](../i18n/pt/STAGE4_KERNELS.md) · [العربية](../i18n/ar/STAGE4_KERNELS.md)

Status as of 24 November 2026. The document specifies the exact rules of four new built-in computations of the mini-agent (since agent version 1.2.0) for calculations M8, M10, M12 and M14 from [VERIFICATION_SEARCH](VERIFICATION_SEARCH.en.md), section 5.3. ChatGPT wrote the specification and the implementation in Go; DeepSeek independently checked the specification against the council's source papers and from it alone wrote a second implementation in Python ([tools/reference_stage4.py](../tools/reference_stage4.py)); all 73 task results matched byte for byte; Claude checked the code and the reconciliation. References of the form "claude1, §5.4" point to the model council's papers collected in VERIFICATION_SEARCH. This is an exact count by formulas, not a measurement: the match confirms the arithmetic, but not the models' assumptions. Calculations M5, M7 and M18 are deferred: the papers lack the rules to determine them unambiguously (section "Deferred calculations").

| Calculation from §5.3 | Version 1 kernel | What one unit can tell |
|---|---|---|
| M8 | `t4-scale` | How many training tokens per node are required for a given number of submitters and how many submitters the budget allows |
| M10 | `exam-thresholds` | In which rational interval each of the two exam thresholds lies |
| M12 | `merge-attribution` | How the sum of credits to a participant changes when exact or noisy copies are added |
| M14 | `verification-enumerations` | Which cases exhaustively passed or failed the packing, chain or field equality check |

The choice follows from the council's table in §5.3. Under D18 payment for improvement remains a research hypothesis. The input parameters suffice to reproduce all four calculations. [Council summary](VERIFICATION_SEARCH.en.md) · [Decisions D18–D20](ROADMAP.en.md)

## General rules of version 1

In the signed task, the kernel name and the integer `kernel_version: 1` are stored separately. The `params` input is an object with all the fields listed for the kernel. Extra and missing fields, a repeated JSON key, out-of-range values and wrong types cause an error. An integer is written as an integer JSON literal, without a decimal point or exponent. Strings and Boolean values in place of numbers are forbidden. Bounds are inclusive. Grid axes preserve the input order. The number of units is exactly equal to the grid size specified for the kernel, from 1 to 1 000 000. Unit numbering starts at zero. In the Cartesian product, the last axis changes fastest.

For reconciliation the entire result object is taken. In Python the canonical bytes equal `json.dumps(result, sort_keys=True, ensure_ascii=True, separators=(',', ':')).encode('ascii')`, without a trailing newline. The result hash is the SHA-256 of these bytes, 64 lowercase hexadecimal digits. The order of array elements is significant. A fraction in a string is written in the decimal system as `p/q` with a positive denominator after reduction, including `0/1` and integers with `/1`. There are no leading plus signs or zeros. For M14 the hash of the bytes *inside* the packing result is defined separately. [The agent's canonical encoder](../agent-go/canon/canon.go)

## M8. T4 scale with one update from each participant

`t4-scale@1` computes the minimum integer number of own training tokens per round at which the exam adds at most 20% of the computation. For a given token budget the kernel also finds the maximum number of submitters. In the model each node checks all `K=N` updates. The base costs one forward pass per position, each update of the upper layers costs a share `a=L_a/L` of a pass, and training one token costs three passes. These ratios are set by the proposal. claude1, §5.4 "Price" and §7.5, item 4 · critic_claude, §1.8 and §10.4, item 3 · [VERIFICATION_SEARCH, §5.3, M8](VERIFICATION_SEARCH.en.md)

| `params` field | Allowed values |
|---|---|
| `N` | Axis of integers from 1 to 1 000 000. Number of submitters in the round |
| `n` | Axis of integers from 1 to 1 000 000. Number of exam positions |
| `a` | Axis of integer pairs `[p,q]`, where `1 ≤ p ≤ q ≤ 1 000 000`. Share of a pass per update |
| `D_budget` | Axis of integers from 1 to 1 000 000 000 000. Budget of training tokens per node per round |
| `epsilon_bits` | A single integer from 1 to 256. Sets `ε=1/2^epsilon_bits` for a fixed exam. For a given `n`, the cost is the same for all `ε` |

All five fields are mandatory. Each axis is an array of length 1…32, values are unique taking fraction reduction into account, the order of the input array is preserved. The number of units equals the product of the axis lengths and does not exceed 1 000 000. Numbering from zero over the Cartesian product `N, n, a, D_budget` in nested-loop order, the budget changes fastest. One unit produces one object.

For the chosen point let `D=D_budget`, and reduce `a=p/q`. Measure the computation in units of `1/q` of a forward pass per position. Then the exam requires `E=n(q+Np)`, training requires `W=3Dq`, and the overhead share equals `E/W`. Division by the volume of own training follows from the wording "surcharge" in §5.4. The 20% condition is equivalent to `5E ≤ W`.

| Result field | Value |
|---|---|
| `kernel` | The string `t4-scale@1` |
| `N`, `n`, `D_budget` | Integers of the input point |
| `a`, `epsilon` | Reduced strings `p/q`; `epsilon` is written as `1/q`, where `q = 2^epsilon_bits` is a decimal integer (for example, `"1/4"` at `epsilon_bits = 2`) |
| `D_min` | The integer `(5E + 3q − 1) // (3q)`, where `//` is integer division rounding down. This is rounding the threshold up to a whole token |
| `fits` | The Boolean value `D_budget ≥ D_min`. Equality counts |
| `N_max` | `null` if `W < 5nq` and even the base pass exceeds the budget. Otherwise the integer `(W − 5nq) // (5np)`. Zero means that only the base fits. The limit may go beyond the input axis `N` |
| `overhead` | `E/W` as a reduced string `numerator/denominator` |

The inverse bound follows from the linear inequality `5npN ≤ W − 5nq` for positive `p`. For allowed parameters, `5E+3q−1 ≤ 5 000 005 000 002 999 999`, `W ≤ 3·10^18`. The denominators are positive. Signed 64-bit integers and fraction reduction via the GCD suffice. In Go, `big.Rat` is used for `overhead` and `big.Int` for `2^epsilon_bits`. Per unit there is parsing of at most 128 axis elements and a constant number of arithmetic operations.

For `n=3, N=4, a=1/2` the exam costs 9 passes; at 15 training tokens it takes exactly one fifth. At 14 tokens the limit drops to three submitters. At `epsilon_bits=2` the following canonical bytes are obtained.

```json
{"D_budget":15,"D_min":15,"N":4,"N_max":4,"a":"1/2","epsilon":"1/4","fits":true,"kernel":"t4-scale@1","n":3,"overhead":"1/5"}
```

As a benchmark for §5.4, at `n=100000, N=10000, a=4/36` the exact minimum equals 185 351 852 tokens. The physical price depends on prefix reuse, cache size, the output head, normalization, traffic and the actual cost of training the upper layers. The formula covers only the pass count described in §5.4. M10 serves to estimate the statistical threshold when `ε` changes. The proposed task sets `ε=2^-80` according to the numerical benchmark D19. critic_gpt, the section on claude1, "The hidden price of T4" · [ROADMAP, D18–D19](ROADMAP.en.md)

## M10. T4 exam threshold — `exam-thresholds@1`

M10 determines how large the average observed improvement on the exam must be for it to exceed the statistical threshold. For one candidate fixed in advance, `n` independent positions are taken with replacement. The loss difference at each position is clipped to `[−B/2, B/2]`. The input `V` is the sample variance of the clipped differences with divisor `n−1` (the square of the standard deviation). The bounds in nats per position are taken from step 6 of the T4 description. claude1, §5.4 · Claude critic, §1.8

| Method | Exact threshold `t` |
|---|---|
| Hoeffding | `B·√(ln(1/ε)/(2n))` |
| Empirical Bernstein | `√(2V·ln(2/ε)/n) + 7B·ln(2/ε)/(3(n−1))` |

**Parameters and units.** Five fields are mandatory. The fields `n`, `epsilon_bits`, `B`, `variance` are axes of length from 1 to 32, each in the order of the input array. Values on an axis are distinct; fractions are compared after reduction.

| Field | Allowed values |
|---|---|
| `n` | Number of positions, an integer from 2 to 1 000 000 |
| `epsilon_bits` | The integer `k` from 1 to 128, `ε = 2⁻ᵏ` per comparison |
| `B` | Width of the clipping range, an integer from 1 to 64 |
| `variance` | The fraction `[p,q]`, integers `0 ≤ p ≤ 10⁶` and `1 ≤ q ≤ 10⁶`. At all grid points `V=p/q ≤ B²·floor(n/2)·ceil(n/2)/(n(n−1))` |
| `digits` | A single integer `d` from 1 to 9. The guaranteed absolute width of each interval is less than `10⁻ᵈ` |

The maximum variance is attained at the ends of the range, since variance is convex in each observation. With `j` values at one end its numerator is proportional to `j(n−j)`, which gives the stated bound. The number of units equals the product of the lengths of the four axes and does not exceed 1 000 000. The numbering coincides with `itertools.product(n, epsilon_bits, B, variance)`, starting at zero.

**Byte-exact reproduction algorithm.** For both methods write `t = √(A·ln 2) + C·ln 2`. For Hoeffding `A=B²k/(2n), C=0`. For Bernstein `A=2V(k+1)/n, C=7B(k+1)/(3(n−1))`. All divisions here are rational.

1. Take `S=10^(d+1)`, `l=693147180559945309/10¹⁸`, `h=693147180559945310/10¹⁸`.
2. The lower bound equals `(floor(√(S²Al)) + floor(SCl))/S`. The upper bound equals `(ceil(√(S²Ah)) + ceil(SCh))/S`. Both terms are rounded **separately**.
3. For a non-negative fraction `x=p/q`, compute `r=isqrt(p//q)`. This is `floor(√x)`. For the upper bound, add one to `r` exactly when `r²q < p`. The ordinary `floor` and `ceil` are also performed by integer division. All resulting fractions are reduced.

**Accuracy certificate.** From the series for `2·atanh(1/3)=ln 2` we take `T=2·Σ 1/(j·3ʲ)` over odd `j=1,3,…,39`. The tail is positive and bounded by the first omitted term multiplied by `1/(1−1/9)`. By integer comparison we obtain `l < T < ln 2 ≤ T + 9/(4·41·3⁴¹) < h`. The monotonicity of both terms and directed rounding ensure that the true threshold is enclosed. In the given range `A ≤ 264192` and `C ≤ 19264`. Since `√h+√l > 1`, replacing `l` with `h` changes the unrounded threshold by less than `(515+19264)·10⁻¹⁸`. Rounding widens the interval by less than `4/S`. The sum is less than `10⁻ᵈ` even at `d=9`. Per unit, four integer square roots and a constant number of operations on integers and fractions of a few hundred bits suffice, independent of `n`.

**Answer.** The fields `n`, `epsilon_bits`, `B` and `digits` are the integer coordinates and the precision. `variance` is a string with the reduced fraction. `hoeffding` and `bernstein` are arrays of two such strings, the lower bound first. For `n=2, k=1, B=2, V=0, d=1` the kernel produces the following canonical bytes.

```json
{"B":2,"bernstein":["323/50","647/100"],"digits":1,"epsilon_bits":1,"hoeffding":["83/100","21/25"],"kernel":"exam-thresholds@1","n":2,"variance":"0/1"}
```

For a given limit threshold `τ`, the minimum exam size **on the grid** is established when at the chosen point the upper bound is `≤ τ`, and for all smaller `n` with the same parameters the lower bound is `> τ`. If the interval crosses the target, greater precision may be required. The numbers characterize a one-sided comparison of the truncated mean with fixing before an external beacon. The correction for selection among several candidates, quality outside the exam, the choice of `τ` and the size of the real effect require separate data or rules. Payment for improvement remains a research option under D18. [ROADMAP, D18–D20](ROADMAP.en.md) · GPT critic, T4 estimate

## M12. How the credit of the owner of duplicates changes under sum merging

The paper for M12 specifies linear-quadratic losses with a known gradient and Hessian, three attribution rules, exact duplicates and duplicates with noise. We choose the variant `merge = sum` explicitly analysed in §5.4. The critic gives a case where even repeated addition of the same step improves the loss function. The kernel `merge-attribution@1` checks this on explicit input coefficients. claude1, §5.4, steps 6–7 and item 2 "Attribution and duplicates", §7.5, item 7 · critic_gpt, the table on claude1, row T4

| `params` field | Meaning and inclusive bounds |
|---|---|
| `scale` | Common denominator `s`, an integer 1…10 000 |
| `g` | Vector of gradient numerators at the base point. Its length sets the dimension `d`, 1…8 |
| `hessian` | Symmetric matrix of Hessian numerators, an array of `d` rows of `d` components |
| `updates` | Array of `b=1…8` original numerator vectors of length `d`, in submission order. Identical vectors are allowed |
| `owner` | Integer index of the original submission of the participant being checked, from 0 to `b−1`. Other original submissions belong to other participants |
| `copies` | Axis of 1…8 distinct integers 1…8. The chosen `c` sets the number of added submissions of the same participant |
| `noise` | Axis of 1…32 pairwise distinct numerator vectors of length `d`. The zero vector gives an exact duplicate |
| `threshold` | Integer numerator 0…10 000 for the deduction `t=threshold/s` from the estimate of each submission |

Each component of `g`, `hessian`, `updates` and `noise` is an integer from −10 000 to 10 000. To obtain the mathematical value of each component, divide it by `s` **once**, including for the matrix. The version supports rational coefficients with a common denominator in the stated range. Symmetry is mandatory; the sign of the curvature is arbitrary. The input axes `copies, noise` form a grid. For unit `u`, take the indices `divmod(u,len(noise))` respectively. After the original `b` submissions, add `c` vectors, each equal to `updates[owner] + noise[j]` in numerators. The original vectors are preserved. The sets of submissions before and after the addition are considered separately.

**Calculation.** Let `U` be the set of submission indices of one set, and `x(S)` the sum of their **mathematical** update vectors over the subset `S`. The loss gain is defined as the reduction relative to the common base,

```text
v(S) = −gᵀx(S) − x(S)ᵀ H x(S)/2,     v(∅) = 0.
```

For each index `i`, compute three **signed** estimates. `separate[i]=v({i})`. The leave-one-out rule, `loo[i]=v(U)−v(U without i)`. The estimate `shapley[i]` equals the average increment `v(S∪{i})−v(S)` over all permutations of the indices, where `S` consists of the predecessors of `i`. This rule is applied to the full loss-reduction function. To compute without factorial enumeration let `q_i=v({i})`, `h_ij=−x_iᵀ H x_j`. Symmetry gives `v(S)=Σ q_i + Σ_{i<j} h_ij` over the participants `S`. When a participant is excluded, all of their pairwise terms disappear. In a uniform permutation every other participant precedes them in exactly half of the cases. Therefore

```text
loo[i]     = q_i + Σ_{j≠i} h_ij
shapley[i] = q_i + (Σ_{j≠i} h_ij)/2
v(U)       = Σ shapley[i].
```

Then, separately for each rule, the estimate `z` is converted into the credit `max(0,z−t)` in units of improvement (the payment coefficient κ is taken as one). First a credit is accrued per submission, then the owner's credits are summed. `gain` is the credit to the owner for their original and all added submissions after the addition minus the credit for their one submission before the addition. A positive sign means a gain from additional submissions in this example.

**Response format.** The keys `kernel` (the string `merge-attribution@1`), `owner`, `scale`, `copies` (the chosen integer from the axis), `noise` (the chosen vector of integer numerators), `baseline`, `with_copies` and `gain`. Each of the objects `baseline` and `with_copies` contains `value` — the fraction `v(U)` — and the fields `separate`, `loo`, `shapley` — arrays of fractions in the order of submission indices. The object `gain` contains one fraction under each of the three rule names. All output fractions are canonical strings.

**Arithmetic and limits.** The common denominator of the intermediate estimates is `2s³`. If `G, A, z_i` are the input integer numerators of the gradient, the Hessian and the step, the numerator of `q_i` equals `−2s Gᵀz_i−z_iᵀAz_i`. Half of the pairwise term corresponds to the integer numerator `−z_iᵀAz_j`. The numerator of the deduction equals `2s²·threshold`. After the addition there are up to 16 submissions and `|z_ij| ≤ 20 000`. Hence `|z_iᵀAz_j| ≤ 8²·20 000²·10 000 = 2,56·10¹⁴`, and the linear part is at most `3,2·10¹³` in absolute value. Even the sum of 16 full LOO estimates and deductions is less than `1,3·10¹⁷` in absolute value. All multiplications and partial sums fit in signed 64 bits. The implementation reduces fractions via `big.Rat`. Time `O(k d²+k²d)` at `k ≤ 16`, without a subset table. Memory is bounded by the input vectors, the matrix, three estimates per submission and the result.

**Manual check.** With `v(x)=3x−x²/2`, one submission `x=1` and a zero threshold, the original estimate equals `5/2` under all rules. After an exact duplicate `v(2)=4`. The rules give `5/2` per submission separately, `3/2` under exclusion and `2/1` under Shapley. The owner's total gain equals `5/2`, `1/2`, `3/2` respectively. This single example is enough to refute the absence of a gain for each of the three rules on the whole family of such models at zero threshold.

**Scope of the conclusion.** The set of participants being compared is fixed. The noise is given by an explicit vector, the threshold is given by the input. Acceptance, re-selection of the composition after deducting the threshold, submission costs, parameter training, external effects and the empirical exam are outside this model. The numerical gain refers to the sum of credits under the chosen rule. A full check of D1 requires comparing the coalition's utilities also with honest work and with inaction. [THREAT_MODEL, §§1.4–1.5](THREAT_MODEL.en.md) · [ROADMAP, D18 and D25](ROADMAP.en.md)

## M14. Checking formulas by finite enumeration

The kernel `verification-enumerations@1` repeats three small experiments. It allows checking whether packing preserves the distinction between allowed vectors and how many errors two kinds of sampling check miss. The input data, enumeration order and reference hashes are published in GPT2, §6.2 and "Control code for the first repetition". The chain is specified in the table "What to give to the mini-agents", the field skip condition — in §6.1. GPT2 paper · [Summary, §5.3](VERIFICATION_SEARCH.en.md)

The only parameter `cases` is an array of 1–4 distinct strings from the table below. `units = len(cases)`. Zero-based numbering, unit `u` computes the entire experiment `cases[u]`. The `case` key of the result contains this same string, `kernel` equals `"verification-enumerations@1"`. The format of the other fields depends on the experiment.

| `case` | Result fields besides `case` and `kernel` | Control values |
|---|---|---|
| `packing-8` | Integers `total`, `true_accepts`, `false_accepts`, the string `verdict_sha256` | 441, 9, 0, `a5c8a8d715fb5293a4dd12753d3483e848f63cb24891a3e584bfdc81954f377c` |
| `packing-4` | The same fields | 441, 9, 20, `fca92fea5a3148177517b737591e499ed021432078bd9803578a2eaad4074fc9` |
| `chain-8-2` | Integers `total`, `caught`, `missed` | 224, 56, 168 |
| `field-5` | Integers `total`, `caught`, `missed` | 25, 20, 5 |

**Bit packing.** Take the base `B` from the experiment label. Enumerate `(x,y,c,d)` lexicographically in ascending order, with `x,y ∈ {−1,0,1}`, `c,d ∈ {−3,…,3}`. The inner loop changes `d`. The true result `(s,t)=(2x−y,−x−y)`. The acceptance criterion is divisibility of `(c−s)+B(d−t)` by `B²` over the integers. When `(c,d)=(s,t)`, an acceptance increments `true_accepts`; in the remaining cases of acceptance it increments `false_accepts`. Write, in enumeration order, exactly 441 bytes, each with the value 1 on acceptance and 0 on rejection. `verdict_sha256` is the SHA-256 of these raw bytes as 64 lowercase hexadecimal digits. The usual unit result hash is computed separately from the whole canonical JSON. For a manual check at `B=4`, `x=−1`, `y=1`, the true answer `(−3,0)` and the submission `(1,−1)` give a difference of 0.

**Chain.** For each single defect `h=0,…,7`, enumerate all unordered pairs without replacement as `0 ≤ i < j < 8`. Increment `total` by 1 for each triple, and `caught` if `h=i` or `h=j`. The number of misses equals `missed=total−caught`. For each `h` there are 28 pairs, of which exactly 7 contain `h`.

**Field.** Enumerate the vectors `(x,y)∈{0,…,4}²`, including the zero one. The error `(1,−1)` is missed exactly when `(x−y) mod 5 = 0`. `total` counts all vectors, `missed` counts misses, `caught=total−missed`. Five diagonal pairs give five misses.

The longest unit checks 441 combinations and stores 441 bytes of verdicts for one SHA-256. The counters do not exceed 441, the absolute value of the packing expression does not exceed 46, the largest division modulus is 64. Signed 32-bit integers suffice. The results relate to the stated ranges, one fixed error and a complete enumeration of equally likely variants. Generalization to a real protocol would require justifying the distribution of calls and the independence of checks.

## Deferred calculations


| Calculation | What is already defined | Which data will allow an unambiguous result |
|---|---|---|
| M5. Waves of forgeries | For one cheap forgery with zero costs `π=m_s/(L+1)` and `H*=R(1/π−1)`. For example, at `L=36, m_s=2` the threshold equals 17,5R | For a wave, one must fix the joint distribution of checks and the balance transition under several simultaneous detections, including the moment of debiting and the availability of the previous wave's rewards. At `π=1/2` a common sample for two identical errors misses both with probability 1/2, independent samples — with probability 1/4. The proposed analogy with `exit-scam-a` also requires clarifying whether its separate probability of being assigned a check is preserved. (claude1, §1.3, §4.2 and §7.5, item 3) (THREAT_MODEL, §1.8) |
| M7. Economics of disclosure | For a fixed payment R and payment for the proof only in the successful branch, the income of one attempt is known: `p(R−Pe)−c_view−c_commit` | For a general limit ε, one needs the price of a discarded attempt, the payout rule under several successes and the joint distribution of the candidates' outcomes on a common exam. The number of keys by itself does not determine these quantities. ODU with a mandatory proof of each attempt gives a different budget, and in T4 the payout also depends on the size of the improvement. (claude2, §5.3) (critic_claude, §2.4) (critic_gpt, analysis of ODU) |
| M18. Payments and recovery | The atomicity of acceptance, the one-time redemption of the right in the canonical history and the list of scenarios are defined | To count paths, one needs a transition table on a branch switch, a finality criterion, recovery rules when data disappears and returns, and a finite bound on the number of repeated presentations. Different automata can satisfy the same invariants and give different numbers of payments over intermediate histories. (gpt1, §1 and §7) (critic_gpt, "Completeness, recovery and price") |
