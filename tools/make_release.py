#!/usr/bin/env python3
"""Build and sign a release of the SkyNet research agent (for maintainers).

    python tools/make_release.py --seq 2 --version 0.1.1

It writes the version and release number into agent/skynet_agent/__init__.py,
lists every agent file with its size and SHA-256 in agent/release.json and
signs that file with the release key (agent/release.json.sig).

Options:
    --set-trust           write the public key of the signing key into trust.py
                          (first release, or when the key changes)
    --halt-through N      ask agents with a release number up to N to stop taking tasks
    --halt-reason TEXT    reason shown to participants
    --key FILE            release key file (default: see tools/keytool.py)
    --root DIR            repository root (default: the parent of tools/)

After a release is uploaded, installed agents pick it up at their next check.
A release number can never be reused or lowered.
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "agent"))

import keytool  # noqa: E402
from skynet_agent import ed25519, signed, updater  # noqa: E402


def _replace_line(path, pattern, replacement):
    with open(path, "r", encoding="utf-8", newline="") as f:
        text = f.read()
    new, n = re.subn(pattern, lambda m: replacement, text, count=1, flags=re.MULTILINE)
    if n != 1:
        raise SystemExit("cannot find %r in %s" % (pattern, path))
    if new != text:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new)


def collect_files(agent_dir):
    files = {}
    paths = ["launcher.py"]
    package = os.path.join(agent_dir, "skynet_agent")
    for folder, dirs, names in os.walk(package):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__")
        for name in sorted(names):
            if name.endswith(".py"):
                full = os.path.join(folder, name)
                paths.append(os.path.relpath(full, agent_dir).replace(os.sep, "/"))
    for path in sorted(paths):
        with open(os.path.join(agent_dir, *path.split("/")), "rb") as f:
            data = f.read()
        if b"\r" in data or data.startswith(b"\xef\xbb\xbf"):
            raise SystemExit("%s must use LF line ends and no byte-order mark" % path)
        if not updater.safe_path(path):
            raise SystemExit("file name not allowed in a release: %s" % path)
        files[path] = {"sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}
    return files


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--seq", type=int, required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--key")
    parser.add_argument("--root", default=os.path.join(HERE, ".."))
    parser.add_argument("--set-trust", action="store_true")
    parser.add_argument("--halt-through", type=int)
    parser.add_argument("--halt-reason", default="")
    parser.add_argument("--date", help="issue date YYYY-MM-DD (default: today, UTC)")
    args = parser.parse_args(argv)

    root = os.path.abspath(args.root)
    agent_dir = os.path.join(root, "agent")
    if not re.match(r"^\d{1,4}\.\d{1,4}\.\d{1,4}$", args.version) or args.seq < 1:
        raise SystemExit("--version must look like 1.2.3 and --seq must be positive")

    seed = keytool.load_seed(args.key)
    public = ed25519.public_key(seed)

    init_py = os.path.join(agent_dir, "skynet_agent", "__init__.py")
    _replace_line(init_py, r'^__version__ = "[^"]*"$', '__version__ = "%s"' % args.version)
    _replace_line(init_py, r"^RELEASE_SEQ = \d+$", "RELEASE_SEQ = %d" % args.seq)
    trust_py = os.path.join(agent_dir, "skynet_agent", "trust.py")
    if args.set_trust:
        _replace_line(trust_py, r"^RELEASE_KEYS = \[[^\]]*\]$", 'RELEASE_KEYS = ["%s"]' % public.hex())
    with open(trust_py, "r", encoding="utf-8") as f:
        if public.hex() not in f.read():
            print("WARNING: trust.py of this release does not list the signing key.")
            print("         Agents installed from it will not accept releases signed with this key.")

    release = {
        "format": 1,
        "seq": args.seq,
        "version": args.version,
        "min_python": [3, 9],
        "issued": args.date or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d"),
        "files": collect_files(agent_dir),
    }
    if args.halt_through is not None:
        release["halt"] = {"through_seq": args.halt_through, "reason": args.halt_reason}
    updater.validate_release(release)

    raw = (json.dumps(release, indent=1, sort_keys=True) + "\n").encode("utf-8")
    sig_line = signed.format_sig_line(public, ed25519.sign(seed, raw)).encode("ascii")
    signed.verify_detached(raw, sig_line, keys=[public.hex()])
    with open(os.path.join(agent_dir, "release.json"), "wb") as f:
        f.write(raw)
    with open(os.path.join(agent_dir, "release.json.sig"), "wb") as f:
        f.write(sig_line)
    print("Release %d (version %s): %d files, signed with %s" % (
        args.seq, args.version, len(release["files"]), public.hex()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
