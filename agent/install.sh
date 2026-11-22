#!/bin/sh
# Installer of the SkyNet research agent for Linux, macOS and Android (Termux).
#
# It only finds Python, downloads agent/install.py from the project repository
# and runs it. It does not need root, does not start the agent and does not
# turn autostart on. Read agent/README.md first.

set -eu

BASE="${SKYNET_AGENT_BASE_URL:-https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main}"
BASE="${BASE%/}"

PY=""
for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1 &&
        "$candidate" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' 2>/dev/null; then
        PY="$candidate"
        break
    fi
done

if [ -z "$PY" ]; then
    echo "Python 3.9 or newer was not found."
    if [ -n "${TERMUX_VERSION:-}" ]; then
        echo "Install it with:  pkg install python"
    elif [ "$(uname -s)" = "Darwin" ]; then
        echo "Install it with:  xcode-select --install   (or: brew install python)"
    else
        echo "Install it with your package manager, for example:  sudo apt install python3"
    fi
    echo "Then run this installer again."
    exit 1
fi

TMP="$(mktemp "${TMPDIR:-/tmp}/skynet-agent-install.XXXXXX")"
trap 'rm -f "$TMP"' EXIT

if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$BASE/agent/install.py" -o "$TMP"
elif command -v wget >/dev/null 2>&1; then
    wget -q -O "$TMP" "$BASE/agent/install.py"
else
    "$PY" -c 'import sys, urllib.request; open(sys.argv[2], "wb").write(urllib.request.urlopen(sys.argv[1], timeout=60).read())' "$BASE/agent/install.py" "$TMP"
fi

"$PY" -I "$TMP" "$@"
