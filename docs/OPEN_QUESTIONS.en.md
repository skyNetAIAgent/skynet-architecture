<!-- translation of docs/OPEN_QUESTIONS.md, source sha256: 399c8aa1465bb599179acb60130b35242d9b6d03a63de6f016bc462e968b83eb -->

# Open questions

**English** · [中文](../i18n/zh/OPEN_QUESTIONS.md) · [Español](../i18n/es/OPEN_QUESTIONS.md) · [Français](../i18n/fr/OPEN_QUESTIONS.md) · [Deutsch](../i18n/de/OPEN_QUESTIONS.md) · [Italiano](../i18n/it/OPEN_QUESTIONS.md) · [Русский](OPEN_QUESTIONS.md) · [Português](../i18n/pt/OPEN_QUESTIONS.md) · [العربية](../i18n/ar/OPEN_QUESTIONS.md)

English translation of [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md) (Russian). These are the problems SkyNet
cannot work without, ordered by importance. For each we note what is known and what has **already been
rejected**, so that nobody goes in circles.

A good contribution: a concrete construction, assumptions named plainly, an attack on it worked through,
the cost counted (computation, memory, traffic, blockchain writes). Even more valuable: a hole in the
current design with a concrete scenario.

Some questions can be advanced by computation. Such computations are run by the
[research agent](../agent/README.md) on volunteers' computers; the task list and its meaning are in
[tasks/README.md](../tasks/README.md), and results are summarised in the `results/` folder. The current
tasks belong to questions Q1, Q5 and Q9.

---

## Q1. Cheap verification under which cheating is useless even with collusion

**The central question of the project.** A false result must bring no gain, and verification must cost
a few percent of the useful work. Target guidelines: about 5% for inference, about 20% for training
(not confirmed).

What is known:

- Sampled verification with forfeiture, or "pay only for verified tasks", give an economic guarantee up to
  a collusion threshold (see [CURRENT_DESIGN, section 3](CURRENT_DESIGN.md)). They do not give zero when all
  verifiers of a task collude.
- Zero under collusion requires verifying **every** paid result. Recomputation costs +100% work.
  Cryptographic proofs are still hundreds to thousands of times more expensive than the work itself.

Measurements from the project pilot (on specific CPUs, see [PILOT_RESULTS](PILOT_RESULTS.md)): a RISC Zero
proof for one row of a Qwen projection took 22 minutes; executing a batch of eight rows in a zkVM took
~17,700 times longer than native; fully recomputing one row's arithmetic in the EVM cost 14.1 million gas.
The published FlashProve work (2026) reports 70–95× GPU time for its integer inference profile.

Wanted: a verification scheme for LLM inference and a training step (LoRA or full) whose full cost
(prover + verifier + data + blockchain) fits the budget, or a proof that this is impossible for a given
class of tasks.

## Q2. Bit-exact results on different GPUs

The whole verification scheme relies on exact comparison. With floating point, different GPUs add in
different orders and produce different bits; a tolerance opens "quiet" cheating with a cheaper model.

Candidate: a fully integer model (int8 weights and activations, int32 accumulation, scales as integer
multiplier and shift, integer non-linearities or tables). For training: splitting into 8-bit parts
(Ozaki scheme).

Open: quality of an integer Qwen, its speed on consumer GPUs (AMD, NVIDIA, Intel), integer training.
Wanted: concrete kernels, quality-loss estimates, known prior work.

## Q3. Dispute with on-chain recomputation for a full model

A dispute is narrowed by bisection down to one operation that the contract recomputes itself. This has
been built only for one row of a model (successful challenge ~14 million gas, a 93-transaction game
~6 million gas). Needed: a reference integer machine for the full model, a proof that the game cannot be
sidetracked (substituted input, length, path), move deadlines, cost under load, choice of blockchain or L2.

## Q4. What to learn and how to keep the model from being spoiled

- How the network itself, without people with special rights, chooses its training plan.
- How to defend against a saboteur willing to lose credits: undetected fakes affect training immediately.
- How to catch hidden behavioural backdoors that a quality exam does not see.
- How to vet datasets in the catalogue: correct computation on harmful data is not fixed by verification.

A known narrow guarantee: if the base model is frozen and the trained part changes logits by at most `b`,
then wherever the gap between the two best tokens exceeds `2b`, poisoning cannot change the answer.

## Q5. Majority capture

Weight measures work, not independence. An owner of a thousand rented GPUs looks like a thousand
participants. A group with 3/4 of the weight could change operating rules. Needed: mechanisms that bound
the damage from an honestly earned majority: an immutable core, per-model thresholds, rules for a closed
start and conditions for opening the network.

## Q6. Privacy of requests on ordinary devices

A device owner can read a request their device computes. Splitting layers does not help: hidden vectors
can be inverted. Needed: cheap partial measures, rules for admission to others' requests, disputes over a
private request without publishing intermediate data, payment that cannot be linked to the payer.

## Q7. Data availability

A verifier says "I was not given the data", the holder says "I gave it", and the ledger did not see the
transfer. For small data, publication on the blockchain helps; for large data (model state) there is no
solution. Also: how many independent copies are needed and how to ensure they belong to different owners.

## Q8. Resistance to blocking and first installation

- How a newcomer obtains genuine software and the ledger address if the main sites are blocked.
- Which independent public "meeting places" to use so that one decision cannot close them all.
- How to work through NAT and relays without central servers.

## Q9. Economics

- A unit of work and a training reward rate at which issuing credits does not devalue them to zero.
- Whether participation pays for owners of large rigs at real electricity prices.
- Income variance when only verified tasks are paid.
- Buying and selling credits for money and cryptocurrency.

## Q10. How a self-learning model will follow the Laws of SkyNet

The manifesto requires that the model not harm humanity or a human, serve people's requests within the
higher laws, and protect itself. Reliably building such rules into a model is an unsolved scientific
problem, and it is harder still in a network with no moderators and with self-training. Needed: how the
laws enter the exam before a model version is replaced, how training does not erode them, who decides
borderline cases and how, without people with special rights, and how to keep the laws from turning into
censorship of useful knowledge.

---

## Already rejected, and why

| Idea | Why it does not fit |
|---|---|
| Paying for uptime or claimed power based on reports and signatures | Colluding agent and verifier will sign anything; an idle GPU produces the same messages |
| Short tasks with answer checks as proof that a specific GPU worked | The answer can be computed on another machine or taken from a cache: the verifier sees identical data |
| A deposit or entry fee | Forbidden by requirement R5 |
| Fines from the available balance | Forbidden by requirement R5 |
| Trust in one honest verifier as a guarantee under full collusion | Replaces requirement R4 with an assumption |
| Majority vote on whether a result is correct | A majority can be captured; correctness must be decided by arithmetic |

General principle: **if the honest and the fake case give the verifier the same data, no algorithm over
that data can tell them apart.** A new signature or blockchain record does not add such data. That is why
the network pays for a verifiable result, not for a resource.
