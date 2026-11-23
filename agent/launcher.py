#!/usr/bin/env python3
"""Launcher of the SkyNet research agent: a small, stable outer loop.

It lives in the agent's home folder next to current.json and does three things:

  * starts the version named in current.json, in Python's isolated mode;
  * starts the new version when the agent reports that it has updated itself;
  * goes back to the previous version if a new one cannot start three times
    or its files are missing.

It contains no network code and no cryptography. Updates are downloaded and
verified by the agent itself (see skynet_agent/updater.py).
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import time

EXIT_RESTART = 75           # the agent installed a new version: start it
EXIT_NOTHING = 3            # "run --once" found nothing to do
EXIT_ALREADY_RUNNING = 4    # another agent holds the lock
FAST_FAILURE_SECONDS = 60
MAX_FAST_FAILURES = 3
MAX_QUICK_RESTARTS = 5      # more restarts in a row than any real chain of updates needs

STUB = ("import sys; sys.path.insert(0, sys.argv[1]); "
        "sys.argv = [sys.argv[0]] + sys.argv[2:]; "
        "from skynet_agent.cli import main; sys.exit(main())")

_DIR_RE = re.compile(r"^versions/[0-9]{1,9}-[0-9.]{1,20}$")


def home():
    return os.path.dirname(os.path.abspath(__file__))


def read_json(path, default=None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def write_json(path, obj):
    fd, tmp = tempfile.mkstemp(prefix=".tmp-", dir=os.path.dirname(path))
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(tmp, path)


def version_dir(h, entry):
    """Absolute directory of a version entry, or None if the entry is not usable."""
    if not isinstance(entry, dict):
        return None
    rel = entry.get("dir")
    if not isinstance(rel, str) or not _DIR_RE.match(rel):
        return None
    path = os.path.join(h, *rel.split("/"))
    if not os.path.isfile(os.path.join(path, "skynet_agent", "cli.py")):
        return None
    return path


def rollback(h, cur):
    """Return to the previous version and remember that this release is bad here."""
    with open(os.path.join(h, "update.lock"), "a+b") as lock:
        try:
            if os.name == "nt":
                import msvcrt
                lock.seek(0)
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            time.sleep(1)
            return True  # an installer is switching versions; re-read the pointer
        if read_json(os.path.join(h, "current.json")) != cur:
            return True
        return _restore(h, cur)


def _restore(h, cur):
    prev = cur.get("previous")
    if version_dir(h, prev) is None:
        return False
    bad_path = os.path.join(h, "bad_seqs.json")
    bad = read_json(bad_path, [])
    if not isinstance(bad, list):
        bad = []
    seq = cur.get("seq")
    if isinstance(seq, int) and not isinstance(seq, bool) and seq not in bad:
        bad.append(seq)
    write_json(bad_path, bad)
    write_json(os.path.join(h, "current.json"), {
        "seq": prev.get("seq"), "version": prev.get("version"), "dir": prev.get("dir"),
        "previous": None, "activated": int(time.time()), "rolled_back_from": cur.get("seq")})
    return True


def main():
    h = home()
    args = sys.argv[1:] or ["run"]
    long_running = args[0] == "run" and "--once" not in args
    try:
        backoff = float(os.environ.get("SKYNET_AGENT_BACKOFF", "10"))
    except ValueError:
        backoff = 10.0
    fast_failures = 0
    quick_restarts = 0
    while True:
        cur = read_json(os.path.join(h, "current.json"))
        if isinstance(cur, dict) and cur.get("runtime") == "go":
            exe = os.path.join(h, "skynet-agent.exe" if os.name == "nt" else "skynet-agent")
            try:
                return subprocess.call([exe, "launch", *args], env=dict(os.environ, SKYNET_AGENT_HOME=h))
            except OSError as exc:
                print("Could not start the Go launcher:", exc, file=sys.stderr)
                return 1
        path = version_dir(h, cur)
        if path is None:
            # The files of the current version are missing or damaged: go back if we can.
            if isinstance(cur, dict) and rollback(h, cur):
                continue
            if sys.stderr is not None:   # None when started without a console (pythonw)
                sys.stderr.write("The agent is not installed correctly in %s. "
                                 "Run the installer again.\n" % h)
            return 1
        env = dict(os.environ)
        env["SKYNET_AGENT_HOME"] = h
        started = time.time()
        try:
            code = subprocess.call([sys.executable, "-IB", "-c", STUB, path] + args, env=env)
        except KeyboardInterrupt:
            return 130
        if code == EXIT_RESTART:
            if not long_running:
                return 0
            fast_failures = 0
            quick_restarts = quick_restarts + 1 if time.time() - started < FAST_FAILURE_SECONDS else 0
            if quick_restarts >= MAX_QUICK_RESTARTS:
                # Something keeps asking for a restart. Never spin: slow down.
                try:
                    time.sleep(min(300.0, backoff * quick_restarts))
                except KeyboardInterrupt:
                    return 130
            continue
        quick_restarts = 0
        if not long_running or code in (0, EXIT_NOTHING, EXIT_ALREADY_RUNNING):
            return code
        # The agent died. Wait a little and start it again; after three quick
        # deaths in a row assume the version is broken and go back.
        if time.time() - started < FAST_FAILURE_SECONDS:
            fast_failures += 1
            if fast_failures >= MAX_FAST_FAILURES:
                if not rollback(h, cur):
                    return code
                fast_failures = 0
                continue
        else:
            fast_failures = 0
        try:
            time.sleep(min(300.0, backoff * (fast_failures + 1)))
        except KeyboardInterrupt:
            return 130


if __name__ == "__main__":
    sys.exit(main())
