#!/bin/sh
# Run as a disposable user with the signed offline installer mounted at /bundle.
set -eu
setup=/bundle/skynet-agent-install.sh
home="$HOME/agent profile"
cmd="$HOME/.local/bin/skynet-agent"
dash "$setup" --home "$home" --no-autostart
"$cmd" verify-install
"$cmd" version
test ! -e "$home/python"
test ! -e "$HOME/.config/systemd/user/skynet-agent.service"
mkdir -p "$home/outbox"
echo key > "$home/identity.key"
echo pending > "$home/outbox/saved.json"
"$cmd" uninstall --yes
test ! -e "$cmd"
test ! -e "$home/versions"
grep -Fx key "$home/identity.key"
grep -Fx pending "$home/outbox/saved.json"
test -f "$home/max_seq.json"
dash "$setup" --home "$home" --no-autostart
"$cmd" uninstall --yes --purge
test ! -e "$home/identity.key"
test ! -e "$home/outbox"
test ! -e "$cmd"
