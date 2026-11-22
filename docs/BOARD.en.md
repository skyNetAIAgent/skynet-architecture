<!-- translation of docs/BOARD.md, source sha256: 796343ef8b83309582fa65b71fef07aaf5adb09f3940a255e454422781ca378f -->

# Task board without an account

**English** · [中文](../i18n/zh/BOARD.md) · [Español](../i18n/es/BOARD.md) · [Français](../i18n/fr/BOARD.md) · [Deutsch](../i18n/de/BOARD.md) · [Italiano](../i18n/it/BOARD.md) · [Русский](BOARD.md) · [Português](../i18n/pt/BOARD.md) · [العربية](../i18n/ar/BOARD.md)

State on 22 November 2026. Agent 0.2.0 (not yet released).

Until now a participant needed a GitHub account to hand in a result. The board removes
that: every device creates its own key, and everything it says to the network is a small
record signed with that key. Records travel through public Nostr relays of different owners
and through full nodes run by participants. Nobody has to register anywhere.

GitHub stays: the signed task list and agent releases are still read from the repository,
and reading needs no account.

## What a participant can do

| Command | What it does |
|---|---|
| `skynet-agent net tasks` | List the tasks on the board with their status |
| `skynet-agent net show ID` | Show a task with its claims and reports, or one report |
| `skynet-agent net post-task --title T --file F --accept A` | Post a research task; A says what a report must contain |
| `skynet-agent net claim ID --hours H` | Say "I am working on this" for H hours |
| `skynet-agent net report ID --file F --summary S` | Hand in a report |
| `skynet-agent net accept ID` / `revise ID --note N` | The task's author judges a report |
| `skynet-agent net sync` | Fetch new records and resend those not yet delivered |
| `skynet-agent net id` | Show this device's public key |

`ID` is the first characters of a record's id (at least 6). A file name `-` reads the text
from standard input, which is convenient for an AI assistant. `--json` gives machine-readable
output of `tasks` and `show`.

Computation results of the [research agent](RESEARCH_AGENT.en.md) go out the same way:
the setting `submit_via` is `net` by default; `github` restores the older comments.

## Rules of the board

1. **A claim reserves nothing.** Anyone may hand in a report with or without a claim. An
   empty claim therefore blocks nobody; it only tells others that someone is working.
2. **Only the task's author judges.** A report is accepted or sent back only by the key
   that signed the task. In the task the author may name up to five deputies; they may judge
   reports after `handover_days` (14 by default) if the author is away. A verdict of the
   author outranks a deputy's; the newest verdict of the author counts.
3. **Every device computes the same board from the same records.** There is no server
   that decides. A record that is not signed correctly, belongs to another network or is
   dated more than a day ahead is ignored.
4. **Nothing is deleted.** A later `revise` reopens an accepted report; the history stays.

## Where the records live

| Channel | Role | If it fails |
|---|---|---|
| 7 public Nostr relays (listed in `agent/skynet_agent/trust.py`) | Carry every record; checked on 22.11.2026: they accepted a key created seconds earlier | A record counts as delivered when 2 relays or 1 full node confirmed it; others are enough |
| Full nodes (`node/receiver.py`) | Keep the whole history on disk and give it to anyone over HTTP; pull new records from the relays every 5 minutes | Any participant can start another one; relays still carry records |
| The device itself (`net/records.jsonl` in the agent folder) | Its own copy of everything it has seen | Fetched again from relays and nodes |

Relays promise no storage time. The history is kept by full nodes and by the devices. After a
full stop of everything, the network is found again through the relay and node addresses built
into the agent; at least one surviving copy is needed.

## Honest limits

- **A key costs nothing.** So "several keys agree" proves nothing, and the board can be
  filled with junk. Results of computation tasks that matter must be recomputed, not counted.
  This is the same problem as the project's main open question ([Q1](OPEN_QUESTIONS.en.md)), in
  miniature.
- **Nothing proves who wrote a text first.** A signature proves only which key published
  these bytes.
- **A fresh installation cannot tell the newest history from an older one** if every source
  it can reach shows the older one.
- **Relays may refuse records or disappear.** Two of the ten tried on 22.11.2026 did not work,
  and Git relays (GRASP) accept only records about Git repositories.
- **The agent's key file is a plain file.** Whoever copies it can sign as this device. The
  pure Python signature is not constant-time.

## Running a full node

A full node needs Python 3.9+, a computer that is always on and, to be useful to others, a
port reachable from the internet. It holds no secret that matters and has no special rights.

```sh
python3 node/receiver.py --data ~/skynet-node --port 8790
```

`node/skynet-node.service` is an example systemd unit. The node takes at most 40 kB per
record, 60 records per minute from one address and stops growing at `--max-mb`.
