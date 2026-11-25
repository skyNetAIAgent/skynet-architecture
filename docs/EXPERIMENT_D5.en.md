<!-- translation of docs/EXPERIMENT_D5.md, source sha256: a043f1ab15bdb60165b5430029b58928dbd99d6807c243175827dd51c9421af4 -->

# Experiment D5: integer Qwen3.5-4B

**English** · [中文](../i18n/zh/EXPERIMENT_D5.md) · [Español](../i18n/es/EXPERIMENT_D5.md) · [Français](../i18n/fr/EXPERIMENT_D5.md) · [Deutsch](../i18n/de/EXPERIMENT_D5.md) · [Italiano](../i18n/it/EXPERIMENT_D5.md) · [Русский](EXPERIMENT_D5.md) · [Português](../i18n/pt/EXPERIMENT_D5.md) · [العربية](../i18n/ar/EXPERIMENT_D5.md)

Status as of 25 November 2026: **the bits match on six performers, including long context;
O3 and O4 have been measured and did not meet the thresholds; quality (O5) has not yet been measured** (section 7). The experiment is authorized by decision D5
([ROADMAP](ROADMAP.en.md), section 3) and is part of stage 5 of the roadmap. It tests the main unmeasured
assumption of the best candidate of stage 4 — verification of the response by the payer themselves (PPS,
[VERIFICATION_SEARCH](VERIFICATION_SEARCH.en.md), sections 3.2 and 5.2).

## 1. What is tested

The payer who has the model must, in one pass, recompute the request and the received response
and obtain **the very same bits** as the performer during generation. This is possible only if all
the model's arithmetic is specified in integers with pinned rounding: a sum of integers does not depend
on the order of addition as long as there is no overflow. The experiment answers five questions; the refutation criteria
are pinned before the run:

| Experiment | Question | What refutes it |
|---|---|---|
| O1 | Do the bits match on different GPUs and on the processor | At least one differing bit of the logits, the selected token, the reason for stopping or the control hashes with the same input. Before the conclusion — a search for the first divergence and a repeat on the shortest input. The conclusion applies only to the tested devices and implementation version |
| O2 | Do the bits match between generation one token at a time and a single pass over the finished sequence on one card | Any differing bit, including the hash of the recurrent state of the Gated DeltaNet layers at the control points |
| O3 | How much does verifying a response cost compared with generating it | The median share `ρ(1)` is greater than 5% for at least one of the four pre-named pairs of request and response lengths at batch 1. Batches 8 and 32 are measured separately |
| O4 | How much slower the integer profile is than the usual 8-bit one on the same card | The median slowdown is greater than 1,25 times in a comparable cell (the threshold is diagnostic: O3 and O5 decide) |
| O5 | How much quality is lost | An accuracy loss greater than 3 percentage points on 320 pre-selected tasks (64 each from the four MMLU sections and from Russian MGSM) compared with the usual 8-bit profile of the same model |

The calculated 1,2–3,8% from stage 4 do not count as a result of O3: only this experiment confirms or refutes
them.

## 2. Model and hardware

- **Model:** the official Qwen/Qwen3.5-4B repository on Hugging Face, pinned revision
  `851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a`. Two weight files of 5 329 398 688 and 3 990 429 408
  bytes, about 9,3 GB in total. After download, the SHA-256 from the repository's inventory is verified.
- **Architecture** (according to the published `config.json`): 32 blocks, hidden vector 2560, MLP 9216.
  Every fourth block (indices 3, 7, …, 31) is full attention: 16 query heads, 4 key and value
  heads, head size 256, output gate, rotation of the first 64 coordinates. The remaining
  24 blocks are Gated DeltaNet: recurrent state 32 × 128 × 128 per block, causal convolution
  of depth 4. Vocabulary 248 320, the input and output matrices are shared. The usual transformer
  "INT-canon" from stage 4 is insufficient for it; the profile is defined anew (section 3).
- **Devices:** RTX 2060 6 GB (Turing) on the accompanying person's home Linux; RTX 4070 Laptop
  8 GB (Ada) on the owner's computer; the processor as a third independent performer. By agreement —
  other participants' devices through a mini-agent.
- **Memory** [calculation]: the main 8-bit weights are 4010 MiB. At batch 1 and a length of up to 3000 tokens
  everything fits in 6 GB; batch 32 at length 3000 requires about 7064 MiB even before working buffers
  and is possible on the RTX 2060 only with the history offloaded to RAM.

## 3. Integer profile

The profile receives a separate name and version and is frozen until O1–O5. The basis is the numerical graph
from the ChatGPT project with corrections by both critics:

1. **Weights and activations.** Weights are 8-bit per row, the row scale is an exact binary number.
   Activations are 16-bit fixed-point (1024 = one). Rounding is the same for all
   operations: to nearest, ties to even, on the absolute value with the sign restored.
2. **Normalizations and nonlinearities** (RMSNorm, L2, SiLU, sigmoid, softplus, exponential) — integer
   formulas with an integer square root, and tables. The tables are built outside the program with proven
   correct rounding (MPFR) and published with SHA-256.
3. **Full attention.** Scores, exponential from a table, shares in 16 bits. The ChatGPT critic found
   an error in the original project: with equal values, adding one more identical key
   changed the output from 1365 to 683. Fix: divide the weighted sum by the sum of the rounded
   shares themselves, then a constant value is preserved exactly.
4. **Gated DeltaNet.** Decay, correction and state update — five integer assignments
   per token in one canonical order in time. The formula from the DeepSeek project
   described a different recursion and is rejected. The accelerated "block" form is allowed only
   if it reproduces the same bits at every token.
5. **Token selection.** Maximum over the pair (score, −number) across the whole vocabulary, greedily. A separate mode is
   canonical Gumbel-max with HMAC-SHA256 pseudorandomness from the request seed (D22).
   Stopping is the first reason: EOS or the limit.
6. **Overflow bounds** are specified for each accumulator; where 32 bits are not enough, 64 are used.
   Separate tests check the extreme values.

All ambiguous places ("forks") are closed before the first run by reading the model source of the pinned
Transformers version; the hash of this source is included in the profile manifest.

## 4. Order of work

1. **P0, preparation (2–4 days).** Download and verification of the model; inventory of all tensors; closing of the
   forks according to the source; tables; control vectors with hand-computed values.
2. **Reduced step (1–1,5 weeks).** A reference on the processor for the whole model on short inputs;
   comparison with the usual floating-point computation (only to catch an import error,
   not for O1/O2). A simple version for the GPU without tensor cores. Answers to O2 on one card
   and to O1 "processor versus RTX 2060" on a short context. Then the same batch on the RTX 4070
   Laptop — the first answer to O1 for two different GPUs.
3. **Full step (3–4 weeks).** Fast 8-bit multiplications, a fused DeltaNet recursion kernel,
   batches 1/8/32, experiments O3, O4, O5, a repeat on the second device.

All work takes place in a separate directory on the home Linux, with its own Python environment
(CuPy with CUDA 12 libraries from pip packages, without a system installation). Running services
and directories of other experiments are not affected. The overall estimate is 4–6 weeks of work by one
developer; the main risks are the cost of the DeltaNet recursion (O3 will show it), ambiguities
before P0 and Qwen3.5 support in ordinary engines for O4/O5.

## 5. What will be published

For each run: the manifest of the profile and versions, the inputs, hashes of logits and per-layer states,
raw times and measurement conditions, the original failures together with the fixes. Bit match
applies only to the tested devices and versions. The result of each experiment is entered into the roadmap
(stage 5) and into this document; an experiment is considered complete when a second participant has repeated it.

## 6. Who did what

- **Experiment projects:** two independent projects — ChatGPT and DeepSeek.
- **Cross-critique:** ChatGPT analyzed both projects, DeepSeek analyzed both projects;
  recalculations of memory and bounds, checking of the short recursion and of the attention corrections on small brute-force searches.
- **Reconciliation and decisions on the plan:** Claude.
- **Preparation, profiles v1 and v2, the processor reference and the GPU version:** ChatGPT.
- **Independent checks:** DeepSeek — model import with the official forward, the unambiguity
  and overflow bounds of profile v2.
- **GPU runs and verification of the results:** Claude (the GPU is unavailable from the model
  sandbox).

## 7. Results

**24 November 2026, short inputs.** Inputs: two histories of 8 + 8 tokens each and six short
texts (Russian, English, Chinese, arithmetic, code, a recipe), depth 4 and 32 blocks; batch 1.

- **Model import.** The usual floating-point computation, written according to the source, matched
  the official Transformers 5.24.0 forward: the same selected token in 130 of 130 positions,
  logit deviation no greater than 3,6·10⁻⁵ (checked by ChatGPT and independently by DeepSeek).
- **Profile v1 rejected.** It reproduced bit for bit, but the 1/1024 scale was too coarse:
  the output of the DeltaNet recursion was almost entirely rounded to zero, the match of the selected token
  with the model — 5 of 8, the logit correlation about 0,8.
- **Profile v2** (activations with a binary exponent per vector and a 16-bit mantissa, the remainder
  and the recursion state with step 2⁻²⁰, attention keys and values in 32 bits): the same token as
  the official model in 90 of 90 positions, mean logit correlation 0,9996, minimum
  0,998. The state and cache occupy 238 MiB at 3000 positions versus 95 for v1; the number of multiplications
  per token is the same — 4,2 billion.
- **O2 (one device).** Generation one token at a time and a pass over the finished response split
  into 1, 3 and 8 positions give the same bits of all logits, selected tokens and state hashes.
- **O1 (different devices).** The processor (Xeon, Linux), RTX 2060 (Turing, Linux, CuPy) and RTX 4070
  Laptop (Ada, Windows, CuPy): 88 comparisons on each card, 242 360 320 logits each,
  976 selected tokens and 37 152 state hashes — **not a single difference**.

**25 November 2026, a different architecture and a different kernel language.** A third
implementation on OpenCL (ChatGPT), the same inputs and 88 comparisons: the processor via pocl,
the RTX 2060 via NVIDIA OpenCL and **AMD Radeon RX 580** (Polaris, Mesa rusticl, Linux) — again
not a single difference in any one of the 242 360 320 logits, 976 tokens and 37 152 hashes. In total,
the same bits on six performers: the processor (NumPy), the processor (pocl), the RTX 2060 (CUDA
and OpenCL), the RTX 4070 Laptop (CUDA), the RX 580 (OpenCL).

**25 November 2026, long context.** Request + response: 512 + 64, 2048 + 256 and 4096 + 64 tokens
(real texts), all 32 blocks; the logit hashes of each position, the selected tokens
and the state hashes every 64 positions were compared. The RTX 2060 (CUDA), the RTX 2060 (OpenCL) and the RTX 4070 Laptop
(CUDA) matched each other in all three cases, and on each card generation one token at a time matched
the pass over the finished response in chunks of 64 and 512 positions. For 512 + 64 the same was given by the independent
processor reference and the RX 580. On the RX 580, generation one token at a time matched the other cards
also for 2048 + 256 and 4096 + 64, but the pass over the finished response on long inputs is interrupted
by the driver (a reset of a GPU task that takes too long); the attention kernel needs to be split into parts.
This is a limitation of execution, not a divergence of bits.

**25 November 2026, fast kernels, O3 and O4.** ChatGPT wrote fast kernels for NVIDIA
(DP4A for multiplying 8-bit weights by 16-bit activations, tiled multiplications for the pass
over the response, a fused DeltaNet recursion). On the RTX 2060 and the RTX 4070 Laptop each of the four
acceleration stages gave the same bits: 88 of 88 short comparisons and the long case 512 + 64 against the
processor reference.

O3 — the time of verifying the response in one pass as a share of the generation time, the median
of nine pairs after two warm-ups:

| Request / response | RTX 2060, batch 1 | RTX 4070 Laptop, batch 1 | RTX 2060, batch 8 | RTX 4070 Laptop, batch 8 |
|---|---:|---:|---:|---:|
| 128 / 32 | 0,40 | 0,24 | 0,64 | 0,46 |
| 128 / 128 | 0,21 | 0,11 | 0,42 | 0,26 |
| 500 / 500 | 0,21 | 0,10 | 0,43 | 0,28 |
| 2000 / 1000 | 0,31 | 0,15 | did not fit | 0,48 |

At batch 32 on the RTX 4070 Laptop — 0,59–0,84, on the RTX 2060 it did not fit in memory.
**The 5% threshold is refuted** for this implementation on both cards (the criterion was written down
before the experiment). The earlier estimate of 1,2–3,8% assumed 8-bit activations and tensor cores;
profile v2 needs 16-bit activations, therefore there are about twice as many multiplications.

O4 — on the RTX 2060 the integer profile is 1,52–1,78 times slower than llama.cpp Q8_0 (b11960, the same
model) at batch 1 and 2,47–2,79 times slower at batch 8. The threshold 1,25 is not met.
What follows from this for the choice of verification was analyzed by the council of models:
[STRATEGY_SEARCH](STRATEGY_SEARCH.en.md).

Limitations: short inputs and batch 1; simple integer kernels without tensor cores; the time
of these runs is not a measurement of O3 and O4. Next — a long context of up to thousands of tokens,
fast kernels with the same arithmetic, then O3–O5.
