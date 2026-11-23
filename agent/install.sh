#!/bin/sh
# The network bootstrap trusts this script and the release key embedded here.
set -eu
umask 077
die() { echo "$*" >&2; exit 1; }
[ "$(uname -s)" = Linux ] && [ -z "${TERMUX_VERSION:-}" ] || die "Use the Python installer for this platform."
case $(uname -m) in
    x86_64) arch=amd64 ;;
    aarch64|arm64) arch=arm64 ;;
    armv7l) arch=arm ;;
    *) die "No Go target for this architecture." ;;
esac
home=${SKYNET_AGENT_HOME:-${XDG_DATA_HOME:-$HOME/.local/share}/skynet-agent}
startup=keep
linger=no
while [ "$#" -gt 0 ]; do
    case $1 in
        --home) shift; home=${1:?missing home} ;;
        --home=*) home=${1#*=} ;;
        --autostart) startup=enable ;;
        --no-autostart) startup=disable ;;
        --linger) linger=yes; startup=enable ;;
        *) die "Unknown option $1" ;;
    esac
    shift
done
[ -n "$home" ] || die "Missing home"
tmp=$(mktemp -d "${TMPDIR:-/tmp}/skynet-install.XXXXXXXX")
trap 'rm -rf "$tmp"' EXIT
trap 'exit 1' HUP INT TERM

# build.py inserts the offline payload here.

bundle=$tmp/bundle/$arch
if [ ! -d "$bundle" ]; then
    for tool in curl jq openssl xxd sha256sum; do
        command -v "$tool" >/dev/null || die "Network setup requires $tool. The offline installer embeds a verified binary."
    done
    mkdir -p "$bundle"
    base=https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main/agent/v2
    for file in release.json release.json.sig; do
        limit=262144
        [ "$file" != release.json.sig ] || limit=16384
        curl -q --fail --silent --show-error --proto '=https' --max-time 45 --max-filesize "$limit" "$base/$file" -o "$bundle/$file"
    done
    key=33deadd767eddfb05d5646caa1b32727a73e261a071d8d4ca8530b7355d2ded9
    printf '302a300506032b6570032100%s' "$key" | xxd -r -p > "$tmp/key.der"
    awk -F: -v k="$key" '$1=="ed25519" && $2==k && length($3)==128 && $3~/^[0-9a-fA-F]+$/ {print $3}' \
        "$bundle/release.json.sig" > "$tmp/signatures"
    verified=no
    while IFS= read -r signature; do
        printf '%s' "$signature" | xxd -r -p > "$tmp/signature"
        if openssl pkeyutl -verify -rawin -pubin -keyform DER -inkey "$tmp/key.der" \
                -sigfile "$tmp/signature" -in "$bundle/release.json" >/dev/null; then verified=yes; break; fi
    done < "$tmp/signatures"
    [ "$verified" = yes ] || die "Untrusted release signature."
    target=$(jq -ce --arg k "linux-$arch" 'select(.format==2) | .targets[$k] | select(.name=="skynet-agent")' "$bundle/release.json")
    size=$(printf '%s' "$target" | jq -er '.size | select(type=="number" and floor==. and .>0 and .<=67108864)')
    hash=$(printf '%s' "$target" | jq -er '.sha256 | select(test("^[0-9a-f]{64}$"))')
    url=$(printf '%s' "$target" | jq -er '.url')
    for attempt in 0 1 2 3; do
        case $url in https://github.com/*|https://objects.githubusercontent.com/*|https://release-assets.githubusercontent.com/*) ;; *) die "Unexpected asset URL." ;; esac
        response=$(curl -q --silent --show-error --proto '=https' --max-time 90 --max-filesize "$size" \
            -o "$bundle/skynet-agent" -w '%{http_code} %{redirect_url}' "$url")
        case $response in
            "200 "*) break ;;
            301\ *|302\ *|303\ *|307\ *|308\ *) url=${response#* } ;;
            *) die "Asset download failed." ;;
        esac
    done
    case $response in "200 "*) ;; *) die "Too many redirects." ;; esac
    [ "$(wc -c < "$bundle/skynet-agent")" -eq "$size" ] || die "Incorrect binary size."
    actual=$(sha256sum < "$bundle/skynet-agent")
    [ "${actual%% *}" = "$hash" ] || die "Incorrect binary SHA-256."
    chmod 700 "$bundle/skynet-agent"
fi
mkdir -p "$home"
home=$(cd "$home" && pwd -P)
"$bundle/skynet-agent" install-bundle "$bundle" "$home"
mkdir -p "$HOME/.local/bin"
shim=$HOME/.local/bin/skynet-agent
# Quote the absolute path once when generating the installed wrapper.
escaped=$(printf '%s' "$home/skynet-agent" | sed "s/'/'\\\\''/g")
wrapper=$(mktemp "$HOME/.local/bin/.skynet-XXXXXXXX")
printf '%s\n' '#!/bin/sh' "exec '$escaped' launch \"\$@\"" > "$wrapper"
chmod 700 "$wrapper"
mv -f "$wrapper" "$shim"
if [ "$startup" != keep ]; then "$home/skynet-agent" launch autostart "$startup"; fi
if [ "$linger" = yes ]; then loginctl --no-ask-password enable-linger "$(id -un)"; fi
printf 'Installed. Run %s status\n' "$shim"
