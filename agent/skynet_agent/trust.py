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

# Ed25519 public keys (hex, 32 bytes) allowed to sign releases and task lists.
# Written by tools/make_release.py from the maintainers' key. An empty list
# means "trust nobody": the agent then refuses every update and every task.
RELEASE_KEYS = ["33deadd767eddfb05d5646caa1b32727a73e261a071d8d4ca8530b7355d2ded9"]
