<!-- translation of docs/PILOT_RESULTS.md, source sha256: 73d115fb10056d64e4cee61811cfd158629d32514eaa0ca4ca9c7939d3700489 -->

# What was verified in the pilot

**English** · [中文](../i18n/zh/PILOT_RESULTS.md) · [Español](../i18n/es/PILOT_RESULTS.md) · [Français](../i18n/fr/PILOT_RESULTS.md) · [Deutsch](../i18n/de/PILOT_RESULTS.md) · [Italiano](../i18n/it/PILOT_RESULTS.md) · [Русский](PILOT_RESULTS.md) · [Português](../i18n/pt/PILOT_RESULTS.md) · [العربية](../i18n/ar/PILOT_RESULTS.md)

Before choosing the architecture without coordinators, the project built a **trusted pilot** with a central server
and several research prototypes for verification. Below is what was actually run and measured,
and where the limits of these results are. The pilot's source code is not included in this repository.

The pilot is a closed system with a trusted operator. It is not protected against cheating in an open network
and does not implement the target architecture. All payments in it are training ones (TEST_CREDIT, no withdrawal).

## Inference and accounting

| What | Result |
|---|---|
| Server circuit | API, queue, PostgreSQL, agent, separate verification of the result and training credit in one transaction. A repeated submission does not give a second credit; an outdated task lease is rejected |
| Weak GPU | Qwen2.5-0.5B-Instruct Q4_K_M via llama.cpp (Vulkan) on integrated Intel Arrow Lake-P: accepted task, rejected answer substitution |
| Second GPU | Qwen3-4B-Instruct-2507 Q4_K_M on RTX 2060 6 GB: all layers on the GPU, about 2.4 GiB VRAM, median 73.8 tokens/s on a short profile |
| Model on several computers | Qwen3-4B layers were distributed over the local network between the RTX 2060 and a participant's GPU (RTX 4070 Laptop, then Intel Arrow Lake-P). The participant received only the assigned part of the weights into memory. The RTX 2060 + RTX 4070 Laptop pair gave about 38–40 tokens/s against 69.5 on a single RTX 2060: extra memory does not guarantee speedup |
| Recovery | Pause, resume and automatic recovery of the group after a tunnel break |

Verification in the pilot is a repeat of generation on the **same trusted** GPU. This is not proof of honesty
of an unfamiliar node.

## Computation verification prototypes

| What | Result | Limit |
|---|---|---|
| Groth16 for two integer matmuls + Solidity verifier | Real proofs and a one-time payment in a local EVM | A small task on CPU |
| RISC Zero for one Q4_K row of a Qwen projection on real data | Proof 22 min 10 s, verification 117 ms, inputs 11.7 KB | One row, not the whole graph; far over budget |
| A batch of eight rows in a zkVM | 350 ms of execution against 19.8 µs natively (~17 700×) | Without building a proof |
| Cartesi: a dispute over a Qwen result | A one-bit substitution found; dispute 93 transactions, 5.8–6.3 million gas | Requires a timely honest challenger |
| Full re-execution of a row's arithmetic in the EVM | 14.1 million gas per submission | One row |
| Automatic auditors | A third-party auditor refuted a false vector despite two that agreed | Without a watcher, the error passed under the optimistic rule |
| Collusion of performer and verifier | Received a payment for an incorrect result | Shows why voting by verifiers is no guarantee |

## What there was not

- Distributed training.
- Strict hardware quotas for CPU/GPU/RAM/VRAM.
- Real monetary payments.
- Verification on independent hardware in an open network.
- Energy measurement.
- Experiments on the new architecture without coordinators: it is so far only designed.
