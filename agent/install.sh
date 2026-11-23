#!/bin/sh
# Install the SkyNet research agent in the current user's profile.
set -eu

base=${SKYNET_AGENT_BASE_URL:-https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main}
base=${base%/}
py=
tmp=$(mktemp -d "${TMPDIR:-/tmp}/skynet-install.XXXXXXXX")
stage=
trap 'rm -rf "$tmp"; if [ -n "$stage" ]; then rm -rf "$stage"; fi' 0
trap 'exit 1' HUP INT TERM

die() { echo "$*" >&2; exit 1; }

download() {
    if command -v curl >/dev/null 2>&1; then
        curl -fsSL "$1" -o "$2"
    elif command -v wget >/dev/null 2>&1; then
        wget -q -O "$2" "$1"
    elif [ -n "$py" ]; then
        "$py" -I -c 'import sys, urllib.request; urllib.request.urlretrieve(*sys.argv[1:])' "$1" "$2"
    else
        die "Install curl or wget and rerun setup."
    fi
}

# build.py inserts the offline payload here.

linux=no
if [ "$(uname -s)" = Linux ] && [ -z "${TERMUX_VERSION:-}" ]; then
    case ${PREFIX:-} in /data/data/com.termux*) ;; *) linux=yes ;; esac
fi
py=
for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1 &&
        "$candidate" -I -c 'import sys; sys.exit(sys.version_info < (3, 9))' 2>/dev/null; then
        py=$candidate
        break
    fi
done

# The lock uses one scalar per line so the bootstrap can read it without Python or jq.
lock_string() {
    sed -n "s/^[[:space:]]*\"$1\"[[:space:]]*:[[:space:]]*\"\([A-Za-z0-9.+_-]*\)\"[,[:space:]]*$/\1/p" "$tmp/python.lock"
}

if [ -z "$py" ]; then
    [ "$linux" = yes ] || die "Install Python 3.9 or newer and rerun setup."
    arch=$(uname -m)
    case $arch in x86_64|aarch64) ;; *) die "This architecture needs system Python 3.9 or newer." ;; esac
    getconf GNU_LIBC_VERSION >/dev/null 2>&1 || die "This system needs glibc or system Python 3.9 or newer."
    if [ ! -d "$tmp/release" ]; then download "$base/installer/linux/python.lock" "$tmp/python.lock"; fi
    hash=$(lock_string "${arch}_sha256")
    case $hash in ''|*[!0-9a-f]*) die "No verified Python hash for $arch. Install system Python 3.9 or newer." ;; esac
    [ "${#hash}" -eq 64 ] || die "Invalid Python SHA-256 in python.lock."
    tag=$(lock_string release)
    version=$(lock_string version)
    asset=$(lock_string "${arch}_file")
    [ "$asset" = "cpython-$version+$tag-$arch-unknown-linux-gnu-install_only_stripped.tar.gz" ] ||
        die "Invalid Python archive name in python.lock."

    agent_home=${SKYNET_AGENT_HOME:-${XDG_DATA_HOME:-$HOME/.local/share}/skynet-agent}
    next_home=no
    for arg do
        if [ "$next_home" = yes ]; then agent_home=$arg; next_home=no; continue; fi
        case $arg in --home) next_home=yes ;; --home=*) agent_home=${arg#--home=} ;; esac
    done
    if [ -z "$agent_home" ] || [ "$next_home" = yes ]; then die "Missing --home directory."; fi
    runtime=$agent_home/python/$hash
    if [ ! -x "$runtime/bin/python3" ]; then
        archive=$tmp/$asset
        if [ ! -d "$tmp/release" ]; then
            download "https://github.com/astral-sh/python-build-standalone/releases/download/$tag/$asset" "$archive"
        fi
        [ -f "$archive" ] || die "The offline installer is missing the pinned Python archive."
        actual=$(sha256sum < "$archive")
        [ "${actual%% *}" = "$hash" ] || die "Python SHA-256 mismatch. Installation stopped."
        mkdir -p "$agent_home/python"
        stage=$(mktemp -d "$agent_home/python/.stage-XXXXXXXX")
        tar -xzf "$archive" -C "$stage"
        [ -x "$stage/python/bin/python3" ] || die "Missing Python executable in the archive."
        # A concurrent installer may already have published the same verified runtime.
        mv -T "$stage/python" "$runtime" || [ -x "$runtime/bin/python3" ] || exit 1
    fi
    py=$runtime/bin/python3
fi

if [ -d "$tmp/release" ]; then
    set -- "$@" --from-dir "$tmp/release" --keep-newer
else
    download "$base/agent/install.py" "$tmp/install.py"
    if [ "$linux" = yes ]; then download "$base/agent/linux_setup.py" "$tmp/linux_setup.py"; fi
fi
if [ "$linux" = yes ]; then set -- "$@" --linux-setup; fi
"$py" -I "$tmp/install.py" "$@"
