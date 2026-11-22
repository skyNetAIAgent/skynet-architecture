<!-- translation of tasks/context/variant-b.md, source sha256: d864f6f9c0e7c95c19747b22ff09f14fb46b5fa2d6a049ca3891730657df8154 -->

# Variant B: the network pays only for what is verified

**English** · [Русский](variant-b.md)

This text is an immutable excerpt for agent tasks. It describes a proposal, not an
accepted decision. Numbers marked [calculation] are obtained from a formula, not measured.

## SkyNet in a nutshell

A distributed network with no owner and no coordinators. Participants compute tasks
(training steps of the open Qwen model and user requests) on their computers and receive
credits. Mandatory conditions: funds cannot be taken from a participant in advance (no
deposits and no fines from the account); cheating must be useless or unprofitable,
including for a newcomer with an empty account and under collusion; honesty verification
must cost a few percent of the useful work.

## Rules of variant B

1. The executor computes a small task and, before the draw is published, records a
   fingerprint of the result in the shared journal. The fingerprint cannot be replaced. The
   result itself has already gone to whoever needs it.
2. Then a public draw (a randomness beacon that no participant controls) decides whether
   the task is verified. Probability p, for example 1%.
3. Not selected: the executor receives nothing for this task. The work remains with the
   network.
4. Selected: k verifiers, assigned by the draw according to the weight of verified work,
   blindly compute the same thing. Until the simultaneous reveal, no verifier sees the executor's answer or another verifier's answer,
   submit their answers hidden and reveal them simultaneously. The executor cannot be its
   own verifier.
5. Matched bit for bit: the executor receives 1/p of the task price (at p = 1% that is one
   hundred times the price). The verifiers receive the usual pay for the recomputation.
6. Did not match: a dispute. It is resolved by recomputing the disputed spot according to
   the journal's rules, not by voting. The loser loses its entire amount "pending".
7. Everything accrued matures after the verification window (three days). Until then it
   lies "pending". Credits that are already available are never deducted.
8. A participant's weight is the sum of the prices of its results that passed verification
   over 30 days. The weight cannot be bought or transferred. The number of accounts gives
   no weight.
9. Computations are integer: honest participants on any hardware get identical bits; there
   is no tolerance in the comparison.
10. Crediting is single by content: model, input, program, output. Submitting the same
    result again under a new number is not paid.

## What has already been calculated

- Without collusion, a fake yields exactly zero: the unselected one is not paid, the
  selected one is caught.
- Under collusion, a fake passes only if all k verifiers of the task are colluders. With a
  share q of colluders in the verifiers' weight, the probability of this is at most q^k:
  0.1% at q = 10% and k = 3; 2.7% at q = 30%; 12.5% at q = 50% [calculation].
- Income becomes uneven. At 6000 tasks per month and p = 1%, on average 60 tasks are paid,
  the fluctuation of monthly income is about ±13% [calculation]. If the cost equals 95% of
  the price, roughly every third month turns out unprofitable [calculation].
- Verification cost: 3–4.5% of resources at p = 1% and three to four verifiers
  [calculation].

## Attacks already found and proposed fixes

| Attack | Fix |
|---|---|
| A newcomer with an empty account in collusion submits garbage: on average gets q^k of the price per attempt and loses nothing | New keys work only on apprentice seats from the shared budget per epoch; their answer is checked against an experienced participant's answer. The leak is bounded, but not zero |
| An "exit campaign": open many tasks at once and fake them all | Any caught fake voids all un-matured winnings of the key; open tasks are no more than the pending amount covers |
| A lazy verifier copies the executor's fingerprint or takes the answer from a shared cache | Hiding commitments with reveal; passing the answer inside collusion is already accounted for in q |
| Almost only machines of one group are admitted to the task (a rare large model) | Do not pay for a model while its circle of verifiers is below the threshold |
| Submitting a known result again under a new number | Single crediting by content |
| A group with three quarters of the weight sets p to the edge of the allowed range by voting | Joint limits on p × k and on the window length in the immutable core |
| A saboteur willing to act without financial gain corrupts unselected answers | Not closed: caught on average after 1/p corrupted answers |
| Poisoning the model through the training data | Not closed by computation verification |

## What variant B does not promise

Secrecy of a request on an ordinary computer, protection against a saboteur willing to act without financial gain,
protection against bad training data. Under collusion of all k verifiers of a task, the
guarantee is q^k, not zero.
