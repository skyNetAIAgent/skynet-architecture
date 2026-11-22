"""What this agent trusts: where the project lives and who may sign for it.

Everything that can change the agent's behaviour (a new version, a task list)
is accepted only with a valid Ed25519 signature made by one of RELEASE_KEYS.
The transport (HTTPS, mirrors) is not trusted for integrity.

Honest limit: whoever holds a release key can ship code to every installed
agent. At this research stage the key is held by the project maintainers. The
target SkyNet network must not have such a key at all (see docs/RESEARCH_AGENT.md).
"""

REPO_OWNER = "skyNetAIAgent"
REPO_NAME = "skynet-architecture"
BRANCH = "main"

RAW_BASE = "https://raw.githubusercontent.com/%s/%s/%s" % (REPO_OWNER, REPO_NAME, BRANCH)
API_BASE = "https://api.github.com"
WEB_BASE = "https://github.com/%s/%s" % (REPO_OWNER, REPO_NAME)

# Channels for signed records (records.py). None of them is trusted: a record is believed
# only because of its own signature, and every channel can be replaced by a new release.
# NET_ID separates this network's records from any other use of the same format.
NET_ID = "skynet-architecture/core-v1"
NOSTR_KIND = 9467
NOSTR_TOPIC = "skynet-architecture-v1"
# Public Nostr relays of different owners that accepted a brand-new key on 22 November 2026.
RELAYS = [
    "wss://nos.lol",
    "wss://relay.primal.net",
    "wss://relay.snort.social",
    "wss://offchain.pub",
    "wss://nostr.mom",
    "wss://relay.nostr.net",
    "wss://nostr.bitcoiner.social",
]
# Receivers: full nodes run by participants (node/receiver.py). The first one is announced here;
# more can be added by later releases.
RECEIVERS = ["http://62.213.14.254:8790"]

# Ed25519 public keys (hex, 32 bytes) allowed to sign releases and task lists.
# Written by tools/make_release.py from the maintainers' key. An empty list
# means "trust nobody": the agent then refuses every update and every task.
RELEASE_KEYS = ["33deadd767eddfb05d5646caa1b32727a73e261a071d8d4ca8530b7355d2ded9"]
