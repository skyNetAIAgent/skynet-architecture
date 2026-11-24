<!-- translation of docs/ROADMAP.md, source sha256: 179a6350fb2d665a7c94f5f2cfa6b2e520f28c4174e3b619f3a31299f63f53ff -->

# Roadmap: protection against cheating

**English** · [中文](../i18n/zh/ROADMAP.md) · [Español](../i18n/es/ROADMAP.md) · [Français](../i18n/fr/ROADMAP.md) · [Deutsch](../i18n/de/ROADMAP.md) · [Italiano](../i18n/it/ROADMAP.md) · [Русский](ROADMAP.md) · [Português](../i18n/pt/ROADMAP.md) · [العربية](../i18n/ar/ROADMAP.md)

Status as of 23 November 2026 (updated after the release of v0.2.2). This is a **work plan, not a promise of a result**. The `[x]` mark
means "done, and this can be verified against the repository or the network's records"; `[ ]` means
"not done". Numbers marked [calculated] are obtained from a formula, not measured. The map is
updated on every status change.

## 1. Goal and readiness criteria

**The goal of the current project stage:** to find a way to check honesty under which the mandatory
requirements ([REQUIREMENTS](../i18n/ru/REQUIREMENTS.md)) are met at the same time:

- the network cannot be cheated: cheating is useless or unprofitable, including for a newcomer
  with an empty account, under collusion, and with many keys;
- no funds up front: no deposits, no contributions, no fines;
- participation is profitable, and checking honesty is cheap. Reference points for the verification
  overhead: about 5% of work for model requests and about 20% for training (unconfirmed).

**The work is considered done when all of the following exist:**

1. **It is recorded exactly what is guaranteed** (decision D1): for the result of a request, a
   training step, a payout, and history; for an empty account, an arbitrary number of keys, leaving,
   and full collusion of task verifiers. The requirement allows "cheating is useless"; a strict loss
   on every attempt need not be proven.
2. **For each attack from the attack table, the rule by which a node rejects a false claim is
   recorded, along with the data from which it does so.** Separately stated are the probability of
   false acceptance, the damage to the network, and the coalition's net gain relative to inaction and
   relative to honest work. A counterexample to the rule: honest and false cases in which the node
   sees the same data. Sampling, a small probability of error, and "an honest observer will be
   found" are recorded as assumptions.
3. **The full price of verification is calculated** relative to the same task without verification:
   the work of the performer and the verifiers, memory, traffic, storage, writing to the ledger,
   disputes, repeats after failures. Derived are the net income of a participant with large resources
   under expensive electricity, the extra payment of a participant with weak equipment, and the price
   for a consumer without equipment. Writing and dispute are available from a zero account; only
   not-yet-matured rewards can be lost.
4. **The calculations are reproducible:** the version of the rules and the kernel, the inputs, the
   enumeration bounds, the output, and the hash are attached; the calculation is repeated on a second
   device. The repeat confirms the computation, but not the correctness of the model itself: that is
   justified separately.
5. **What cannot be established by reasoning is measured:** bit-for-bit match of the result on
   different GPUs, the speed and quality of the integer model, the price of a dispute. Profiles,
   metrics, and thresholds are fixed before the measurement.
6. **The remaining requirements are not violated:** the network works without any single node or
   venue, can re-form after a full shutdown as its nodes rediscover one another, the bases of accruals are restored; under a network
   partition, a disputed payout waits for the common history, and a repeat is not paid twice.

An honest outcome is also a result: if for some class of tasks a cheap check is impossible, this is
shown by a proof with the named class of tasks and the named data of the verifier, not by the absence
of ideas.

## 2. Where we are now

| What | Status | Where it is recorded |
|---|---|---|
| From signatures and short answers it cannot be established which device worked and for how long: a proxy, a cache, and an idle card give the same data | Established by reasoning | [OPEN_QUESTIONS](OPEN_QUESTIONS.md), "What has already been rejected" |
| The network pays for a verifiable result, not for a resource | Accepted (D2); the unit of result and the acceptance condition are not yet defined | [CURRENT_DESIGN](CURRENT_DESIGN.md), section 1 |
| Deferred payment instead of a deposit: a participant can lose only the pending amount | Accepted | CURRENT_DESIGN, section 2 |
| Variant A: verification by sampling, with cancellation of pending rewards when fraud is detected | Current specification | CURRENT_DESIGN, section 3 |
| Variant B: the network pays only for verified tasks, paying `1/p` times the base price for each | Main candidate; the choice after comparison (D3) | CURRENT_DESIGN, section 3 |
| Bit-for-bit match of the result through integer arithmetic | Candidate, not measured | OPEN_QUESTIONS, Q2 |
| Dispute by halving with recomputation of one step in the ledger | Measured for one row of the model; not built for the full model | [PILOT_RESULTS](PILOT_RESULTS.md) |
| Verification of matrix multiplication with a random vector inside a dispute | Candidate, only a calculated estimate exists | CURRENT_DESIGN, section 3 |
| An unchangeable verification core that cannot be revoked by a vote | Accepted (D4) | CURRENT_DESIGN, section 8 |

**What is known about the strength of the defense.**

- Variant A, without collusion: in the enumerated family (two waves of fakes, 92 million
  strategies), submitting fake results and then leaving brings no more than ordinary leaving [calculated].
- Variant A, collusion: the first grid points where submitting fake results and then leaving is profitable are a collusion
  share of 87.5% (tasks of arbitrary size) and 89.0% (equal tasks) under the rule "at most one third may be in progress at any one time", and 80% without that rule. Grid step 0.002–0.02; other families of strategies were
  not enumerated [calculated, [FIRST_RUN](../results/FIRST_RUN.md)].
- Variant B, without collusion: with exact comparison, a fake is not paid.
- Variant B, collusion: `q` is the fraction of the total verifier weight for that model held by the coalition. A fake is paid only if the task is selected and all `k` verifiers are in collusion. The
  average payout for one submitted fake equals `R·q^k` (`R` is the price of the task) and does not
  depend on `p` [calculated]. At `q = 1` this is the full price. A newcomer with an empty account has no pending rewards to cancel.
- A zero false payout under full collusion of verifiers is shown neither for Variant A nor for
  Variant B. It is given by checking every paid result against data that any node checks itself. A
  full recomputation adds about 100% of work. Pilot measurements: the RISC Zero proof for one row of
  the model took 22 min 10 s to build; executing eight rows in the zkVM ran about 17,700 times
  slower than usual, without building a proof. These measurements give no general lower bound on the
  price.
- Income unevenness in Variant B: with 6,000 tasks per month, verification of 1 in 100, and a cost of
  95% of the price, the probability of a loss-making month is 33.10% [calculated, FIRST_RUN].
- The first run of the calculations (702 chunks) was done on one computer. By 23 November a second
  device had recomputed all 702 chunks; all matched. Its records are signed with the key `46000d30…`
  and are available on the full node. Both devices belong to the maintainers, so this is not yet
  confirmation by an independent participant.

**What is not solved.**

1. A newcomer with an empty account in collusion (Variant B): average gain `R·q^k` per attempt, no
   losses.
2. "Honest for a long time, then a big cheat and leaving": the loss is limited by the pending amount,
   the gain grows with the number of fakes. Fixes for Variant B are proposed, not calculated.
3. A flood of garbage from free keys. A key costs nothing; paying with CPU work puts weak devices in
   a worse position.
4. A result used before verification. The answer has already been read by the user, the step has
   already entered training; limiting payouts does not fix this. In Variant B this applies to
   unselected tasks as well.
5. Training tasks paid by issuing credits: who approves them and by what rule. A correctly performed
   but self-assigned task must not yield credits.
6. A rare model: the circle of verifiers is small, and `q` for it can be close to one.
7. Data availability and a dispute over a private request without revealing the request.
8. Bit-for-bit match and the speed of the integer model are not measured.
9. A saboteur who needs no profit, and poisoning of training data. Economic defense does not act
   against them.

## 3. Decisions

Decisions D1–D5 were made on 23 November 2026.

| № | Question | Decision |
|---|---|---|
| D1 | What is accepted as a guarantee | **The cheater does not get what they want.** Attempts to cheat cannot be excluded, but any attempt must be useless for the one who makes it: the expected gain from a fake is not greater than zero compared with honest work and with inaction, for any coalition, including a newcomer with an empty account and any number of keys. The goal is for a false result not to be paid at all. A strict loss on every attempt is not required. A limited but positive leakage (for example, `R·q^k` for a newcomer in Variant B) does **not satisfy** the criterion and remains an open hole |
| D2 | The basis of payment | **Accepted: only a verifiable result is paid.** Switched-on equipment, operating time, and claimed power are not a basis of payment: a GPU can be loaded with something extraneous as well |
| D3 | Variant A or B | **The decision is made after comparison on the same attacks and the same price (stage 2).** The main candidate is Variant B |
| D4 | The unchangeable verification core | **Accepted in a strengthened form.** The check runs automatically, without human involvement and without votes. The rules of the check are not changed by vote. Each node itself executes the check according to the pinned fingerprint of the rules, so replacing the algorithm on one node or at one program vendor does not change the decisions of others. Open: how to fix an error in the core itself (only by moving to a new network) and how a participant can make sure their program matches the published fingerprint (a reproducible build). The release key with which mini-agents are currently signed is a research tool; it must not exist in the target network |
| D5 | The first experiment with integer Qwen3.5-4B | **Permitted:** an RTX 2060 GPU on the maintainer's home Linux, their computer, and, with consent, the devices of other participants via mini-agents. It is carried out after stage 0 |

**Order of work.** Stage 0 is completed first — mini-agents and smartphone apps, so that other people can join the work. Then stages 1–5 according to this map.

## 4. Stages and checklist

Stage 0 is completed first. Then stages 1–4 run in parallel: these are calculations and reasoning. Stage 5 (the experiment permitted by decision D5) runs after stage 0. Stage 6 brings the results together.

### Stage 0. Mini-agents and smartphone apps (done first)

**The goal of the stage.** On every supported platform a person goes through the path "downloaded → installed → launched", and after that the mini-agent, without human involvement, updates itself, takes tasks, and returns the result. Without an account, without administrator rights, without pre-installed Python. Each step is checked on a live device, not only by automatic tests.

**Done when** for each platform from the list below: a person without experience has gone through the path using one page of instructions; the agent on that device received a new release by itself, took a task from a new list by itself, its result appeared on the full node and matched the result of another device. Recorded are the system, the architecture, the versions before and after, and the identifier of the record on the node.

Platforms: Windows, Linux, Android (decision of 23 November 2026). No mini-agents are made or
checked for macOS and iOS. The installation command for Linux possibly works on macOS as well,
but this is not supported. The Windows version is released without code signing: on installation
Windows shows a SmartScreen warning that must be confirmed manually; the authenticity of the file
is checked against the published hash and the project signature.

Already done:

- [x] A public repository, an unchangeable basis in nine languages (label `core-v1`).
- [x] An agent program for Windows and Linux: signed tasks and updates, automatic
      checks in CI (release 0.2.0). Installation with one command
      in the terminal; Python 3.9+ is required.
- [x] Results and the [task board](BOARD.md) without an account.
- [x] The first full node storing the history of records.
- [x] The first research task "Defense against cheaters" on the board, in nine languages.
- [x] A trial Android app 0.1.0 (checked only on the emulator).

**Step 1. Update reliability (release 0.2.1, without new tasks)**

- [x] The first installation checks the release signature with a key embedded in the installer
      itself, **before** the downloaded code runs (previously the downloaded agent checked itself).
- [x] Switching to a new version in one atomic operation: first the new directory is prepared and
      checked, then one pointer is changed; the previous healthy bundle is kept.
- [x] The highest accepted release number is stored outside the version directories and is also
      checked on reinstall (protection against rollback to an old release).
- [x] The device key, settings, progress, and unsent results are stored outside the version
      directories and survive an update and a reinstall.
- [x] Without the network the agent keeps working on the last healthy version and retries the
      connection with a growing interval.
- [x] An automatic check in CI: a substituted file, a foreign key, an old number, an extra file,
      an interrupted download, and an incompatible Python are rejected, and the working version
      remains.
- [x] **Live check on the server:** the 0.2.0 installation upgraded to 0.2.2 by itself on
      23 November 2026, with the device key and progress preserved. On the home Linux the agent was
      installed anew with the new installer (0.2.2); its self-update will be checked by the next
      release.
- [x] Live check of self-update on Windows: the owner's installation went through 0.2.2 → 0.3.0 →
      Go 1.0.1 by itself (23 November 2026).

**Step 2. Android: an app without a token**

- [x] A new APK 0.2.0 with the embedded agent 0.2.2: publication by signed records, the token screen
      and the token hints are removed.
- [x] Fix the false rollback without the network: previously three launches without a connection
      marked a healthy new version as failed. Now the version is confirmed by a local self-check.
- [x] Once a day the app checks for new APK versions, compares the hash and the project signature,
      and offers to install; installation is confirmed by a person (this is how Android outside the
      store works).
- [x] Starting after a reboot by a user toggle (tested on the emulator).
- [x] Checking the update on top of APK 0.1.0 on the Android 14 emulator: the data is preserved.
- [ ] Checking the new-APK offer by the app itself (will work with the next APK version).
- [ ] **Live check on a real phone** (a participant with a phone is needed): installation,
      working while charging, reboot, the manufacturer's power saving.

**Step 3. Windows: a one-file installer**

- [x] `SkyNetAgentSetup.exe` is built in GitHub Actions, without code signing; inside are the
      embeddable Python from python.org, the agent, and a signed release. Its hash and the project
      signature are published alongside. Installs into the user profile, without administrator
      rights, works without the network.
- [x] Shortcuts in the "Start" menu: agent status, pause, resume, stop, uninstall.
- [x] A "start at login" checkbox in the installer; the choice is preserved on update.
- [x] Uninstalling via "Apps"; when uninstalling, the device key can be kept.
- [x] An automatic check in CI on a clean Windows without Python: installation, self-check,
      uninstallation.
- [x] Live check on a person's computer: the owner installed the agent from Releases (release v0.2.2).

**Step 4. Linux**

- [x] The installer uses the system Python 3.9+, and if there is none, installs a portable Python
      and checks its hash. There is also a one-file installer that works without the network
      (release v0.2.2).
- [x] A systemd user service with the user's consent; running without logging in is a separate
      checkbox.
- [x] A check in CI: Debian 12 without Python and Ubuntu 24.04 with Python; a live installation
      on Linux Mint.
- [ ] A live check with a participant not connected with the maintainers.

**Step 5. A Go agent instead of Python (owner's decision of 23 November 2026)**

The agent has been rewritten in Go: one small program, Python is not needed. The embedded Python and
its update are no longer required, so the previous step "updating the embedded Python" has been
removed.

- [x] Signatures, tasks, seven computational kernels, records, Nostr, the board, the work loop,
      updating via the second channel (`agent/v2/release.json`), the launcher, and autostart — in Go,
      standard library only (code written by ChatGPT, checked by DeepSeek).
- [x] Go results match Python bit for bit on all fast chunks of the reference and on all checked
      heavy chunks; cross-checking of all 1,199 chunks continues.
- [x] Reproducible build: identical program hashes when built on Windows and Linux.
- [x] The Python bridge 0.4.0 itself migrates installed agents to Go while preserving the device
      key, progress, and queue. Live transition: the server, the home Linux, and the owner's Windows
      switched to Go 1.0.1 by themselves.
- [x] Installers in Go: Windows 4.7 MB, Linux as a single file; the Android app 0.3.0 with a Go
      engine, about 8 MB instead of 40 (checked on the Android 14 emulator).
- [ ] Remove the bridge and the Python copies after two verified releases in Go.

**Step 6. Task flow**

- [x] Four new computational tasks of stage 2 (the exit campaign of Variant B, apprentice seats,
      a lottery with a chosen verification share, the winning-token certificate) — new built-in
      kernels of agent 0.3.0, 515 chunks in task list No. 2. The mathematics was verified
      independently by another method at 111 points. The certificate gives no savings on random
      matrices (about 0.8% extra work), so 20 chunks were left as a basis for comparison with the
      weights of the real model.
- [x] New tasks require agent 0.3.0 and above; an old agent skips an incompatible task and keeps
      working (verified by a test).
- [ ] When all tasks are computed, the agent waits and picks up the next list by itself.
- [ ] The result collector runs on a schedule on the full node and publishes a summary.
- [ ] Independent confirmation of all 702 chunks of the first list. A second device (the
      maintainers' server) has recomputed all 702, all matched; there is not yet a participant
      unconnected with the maintainers.

**Step 7. Pilot with other people**

- [ ] The "How to connect" page in nine languages: one link per system.
- [ ] One participant per platform not connected with the maintainers; the stage readiness
      criteria are met.
- [ ] Second and third full nodes with different owners.

**Step 8. AI agents**

- [ ] The agent itself picks up new board tasks and passes them to the participant's local model;
      the answer is sent only after a person approves. The task text is considered untrusted.
- [ ] Instructions for an AI assistant: how to take a task from the board, submit a report, and
      check someone else's.
- [ ] A report for a board task from a participant not connected with the maintainers.

**Owner's decisions for stage 0** (23 November 2026): macOS and iOS are not made; the Windows version is released without code signing.

### Stage 1. Precise formulation

- [x] Decisions D1 and D2 are made and recorded (section 3).
- [ ] For one public request and one training step the following are recorded: the acceptance rule,
      the arithmetic, the basis for issuing credits, the moment the result is fixed relative to the
      draw, and the moment when the result may be used.
- [ ] The adversary model in one document: collusion, many keys, leaving, renting capacity; what
      counts as the cheater's gain and what counts as damage to the network.
- [ ] The table of analyzed attacks is published in the repository in nine languages with the status
      of each attack for Variants A and B. Before publication, check the rows: in the CURRENT_DESIGN
      summary the sum of the categories is 18 + 6 + 19 + 16 = 59 against the claimed 60.
- [ ] For each attack it is recorded from which independently checkable data a node will reject a
      false claim under collusion of the performer and the verifiers.

Done when: any participant can use the table to name an attack the defenses do not yet cover and verify that it remains unaddressed.

### Stage 2. Economics: calculations performed by mini-agents

Each task is an exact model with a finite grid of inputs; probabilities and sums are computed as
exact fractions, and the hash of each chunk is cross-checked between devices.

- [x] Variant A, submitting fake results and then leaving: first run.
- [x] Variant B, income unevenness at a constant verification share: first run.
- [ ] Independent confirmation of both calculations (see stage 0).
- [ ] **Exit campaign in Variant B.** Inputs: pending amount `H₀`, price `R`, verification share
      `p`, collusion `q` and `k`, cap on simultaneous tasks `C`, number of waves `T`. One caught
      fake zeroes the entire pending amount, including the wave's winnings. Find the largest expected
      payout above `H₀`, including at `H₀ = 0`, `q = 0`, and `q = 1`.
- [ ] **Apprentice seats.** Per epoch, `S` seats are distributed among `n` honest and `m` coalition
      keys. Find the expected leakage over `E` epochs and the share of seats that goes to honest
      newcomers as `m` grows.
- [ ] **A lottery with a chosen verification share.** For `N` tasks per month, take the smallest `p`
      at which at least 60 tasks are paid on average. Find the probability of a loss-making month
      and quarter, the probability of a month without a single payout, and the number of
      recomputations for the network.
- [ ] **Winning-token certificate** (see stage 4): the number of verification operations relative to
      a full recomputation of the output layer on a given set of inputs.
- [ ] The formula for the full price of verification for three kinds of participants; after stage 5,
      measurements are substituted into it.
- [ ] Comparison of Variants A and B on the same attacks and the same price, then decision D3.
      A possible outcome: both variants remain research variants.

Done when: for each variant there is a table "collusion share → the cheater's largest expected gain",
recomputed on no fewer than two independent devices.

### Stage 3. Close the known holes

- [ ] **Newcomer with an empty account.** Candidate: a newcomer's first tasks are such that any node
      checks them exactly itself, and only after that are the reward and weight credited. Fallback: a
      shared budget of apprentice payouts per epoch; it limits leakage but does not make it zero, and
      collusion can take all the seats.
- [ ] **"Honest for a long time, then a big cheat".** Candidate: a cap on the sum of all open
      commitments of a key, counting the largest possible winnings. This is a bound of one wave, not
      zero leakage.
- [ ] **Garbage from free keys.** Candidate: a node accepts data only for allowed task numbers, and
      limits the size, the queue, and the work per epoch. The channel can still be filled; a
      guaranteed place for an honest newcomer at an arbitrary number of keys has not been obtained.
- [ ] **A result used before verification.** Candidate: check the answer block before handing it
      out; keep the training step in a separate branch and promote only a verified descendant. Price:
      delay and memory.
- [ ] Training tasks: an approval rule without a participant with special rights.
- [ ] A rare model: a threshold derived from the distribution of weight, below which the network does
      not pay for the model.
- [ ] A lazy verifier and re-submission of a known result: hiding commitments with reveal, one-time
      crediting by content.
- [ ] An equipment failure at an honest participant: a rule that gives no gain to a cheater.
- [ ] Data availability and a dispute over a private request without revealing it.
- [ ] The dispute window when the network is stopped, protection against outdated history, network
      partition.

Done when: for each item there is published a construction with assumptions, an attack on it, and a
price, or a counterexample, or an "open" status with a reason.

### Stage 4. Search for a guarantee independent of the collusion share

We seek a check that every node performs itself, so that the agreement of verifiers decides nothing.
The directions are not approved. For each one it is necessary to specify the operations to be
checked, the data, the probability of error, and the price of a whole request or step; then either
carry it to a construction or close it with a counterexample.

- [ ] **Tasks with a cheap exact correctness criterion.** Example: for ridge regression, a node
      checks the optimality condition in one pass over the data. Question: what share of the
      network's work fits into such tasks. Start from this direction: it gives a zero false payout.
- [ ] **Checking every matrix multiplication with a random vector** instead of recomputation. The
      vector is chosen after the result is fixed; the probability of missing an error does not depend
      on collusion. Beneficial for large batches; when generating one token at a time there is no
      gain. The remaining operations (rounding, activations, cache, optimizer) need to be checked
      separately.
- [ ] **Checking a ready answer with one pass of the model** with an exact profile and the randomness
      specified in the task. The number of operations is of the same order as generation; whether
      this fits into 5% is not established.
- [ ] **Tables of exact partial sums for unchanged layers:** a node derives the tables from the
      weights once and then obtains the layer's output by reads and additions. Applicable to a single
      token as well; limited by the amount of memory.
- [ ] **Winning-token certificate** for a large vocabulary: the performer sends a covering of the
      vocabulary by groups, the node checks the upper bounds and descends to individual tokens only
      where the bound does not separate the winner. In the worst case the whole vocabulary is
      checked.
- [ ] **A training step as an exact update formula:** nodes store and check not the new weight
      matrix but the update multipliers. Derived only for a linear layer with simple SGD.
- [ ] **A dispute open to any participant within the window.** The guarantee is conditional: at
      least one observer is needed who received the data and had time to object. Who pays for
      observation with an empty account is not decided. Keep as a fallback.
- [ ] **Payment for a measured improvement of the model** on tasks chosen after the weights are
      fixed. Changes the basis of payment and requires a separate decision. Suitable for selecting
      model versions.
- [ ] **Proofs of computation for training (sumcheck, GKR)** for one specific step: a full estimate
      with ranges, rounding, and binding of the input to the task.
- [ ] **A lower bound:** show which classes of checks cannot be error-free. A start: a fixed set of
      linear checks fewer in number than the size of the result always misses some error; fresh
      randomness and inputs with a known structure remain open.
- [ ] Ideas from participants and AI assistants from the board: each goes through the same analysis,
      including the case `q = 1`.

Done when: for each direction there is published a construction with an estimate, a counterexample,
or a proven bound. A construction is considered found if it satisfies all the criteria of section 1.

### Stage 5. Grounds established only by experiment (permitted by D5)

- [ ] Integer Qwen3.5-4B on two different GPUs: whether the bits match.
- [ ] Its speed relative to the usual profile on the same cards.
- [ ] Its quality relative to the usual profile on the same set of tasks.
- [ ] Separate measurement plans (outside D5): verification energy, integer training.
- [ ] The price of a dispute in the ledger for the full model. Before it, the following are needed:
      the choice of the blockchain, a reference machine for the full model, input binding, lengths
      and paths of computation.

Done when: each number is measured, the measurement conditions are recorded, and a second participant
repeated the measurement. Bit match applies only to the tested configurations.

### Stage 6. Consolidation and acceptance

- [x] Decision D4 on the unchangeable core (section 3).
- [ ] The composition of the core and the way a participant makes sure their program matches the published fingerprint.
- [ ] Update CURRENT_DESIGN and the attack table based on the results of stages 1–5.
- [ ] One claim is traced on paper from task approval to the use of the result, including rejection,
      repeat, and network partition.
- [ ] Open review of the final construction: a council of models and a task on the board.
- [ ] For each requirement there is published a proof, a measurement, a counterexample, or an "open"
      status. A check against the six criteria of section 1.

## 5. How the work goes

1. A checklist item becomes a task: a computational one (mini-agents calculate it, the result is
   cross-checked by matching) or a research one (it is published on the board).
2. Participants and their AI assistants submit reports. A report is accepted only if it can be
   checked: by recomputation, a counterexample, or a reference to a source. The number of agreeing
   keys proves nothing; the decision of the task's author on the board does not confirm a
   computation.
3. Based on the check, the task is closed, refined, or gives rise to new tasks.
4. A status change is made in this map and in CURRENT_DESIGN in a single edit, with a date.

## 6. What this map does not promise

- That a solution exists under the given conditions. This is the subject of the search.
- Deadlines. The project has no paid performers; the speed depends on the participants.
- Rewards for participating in the design.
