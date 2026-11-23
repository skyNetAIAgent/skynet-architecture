#!/bin/sh
set -eu
setup=/bundle/skynet-agent-install.sh
home="$HOME/.local/share/skynet-agent"
cmd="$HOME/.local/bin/skynet-agent"

case "$1" in
    system) python3 -I -c 'import sys; assert sys.version_info >= (3, 9)' ;;
    portable|unpinned)
        if command -v python3 || command -v python; then exit 1; fi ;;
    *) exit 2 ;;
esac
if [ "$1" = unpinned ]; then
    if dash "$setup" --no-autostart >/tmp/setup.log 2>&1; then exit 1; fi
    grep -F 'Install system Python 3.9 or newer' /tmp/setup.log
    test ! -e "$home/current.json"
    exit 0
fi

dash "$setup" --no-autostart
"$cmd" selftest
"$cmd" version
if [ "$1" = portable ]; then grep -F "$home/python/" "$cmd"; else test ! -e "$home/python"; fi
test ! -e "$HOME/.config/systemd/user/skynet-agent.service"
mkdir -p "$home/outbox"
echo key > "$home/identity.key"
echo pending > "$home/outbox/saved.json"
"$cmd" uninstall --yes
test ! -e "$cmd"
test ! -e "$home/launcher.py"
test ! -e "$home/python"
grep -Fx key "$home/identity.key"
grep -Fx pending "$home/outbox/saved.json"
dash "$setup" --no-autostart
"$cmd" uninstall --yes --purge
test ! -e "$home"
