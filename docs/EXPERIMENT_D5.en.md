<!-- translation of docs/EXPERIMENT_D5.md, source sha256: 8c74b11b335ebd7a0797e908c40ed9e4c2b98395835bb319e3272b464224875d -->

# Experiment D5: integer Qwen3.5-4B

**English** · [中文](../i18n/zh/EXPERIMENT_D5.md) · [Español](../i18n/es/EXPERIMENT_D5.md) · [Français](../i18n/fr/EXPERIMENT_D5.md) · [Deutsch](../i18n/de/EXPERIMENT_D5.md) · [Italiano](../i18n/it/EXPERIMENT_D5.md) · [Русский](EXPERIMENT_D5.md) · [Português](../i18n/pt/EXPERIMENT_D5.md) · [العربية](../i18n/ar/EXPERIMENT_D5.md)

Status as of 24 November 2026: **experiment plan, no measurements yet.** The experiment is authorized by decision D5
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
