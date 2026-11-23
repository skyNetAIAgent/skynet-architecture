"""Install an authenticated release in a private directory, then switch the pointer."""

from contextlib import contextmanager
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time


class ReleaseError(Exception):
    pass


@contextmanager
def update_lock(home):
    os.makedirs(home, exist_ok=True)
    with open(os.path.join(home, "update.lock"), "a+b") as lock:
        try:
            if os.name == "nt":
                import msvcrt
                lock.seek(0)
                msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as e:
            raise ReleaseError("another installation is in progress") from e
        yield


def read_local(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except ValueError as e:
        raise ReleaseError("invalid JSON in %s" % path) from e


def sequence_floor(home):
    highest = read_local(os.path.join(home, "max_seq.json"), 0)
    cur = read_local(os.path.join(home, "current.json"), {})
    if type(highest) is not int or highest < 0 or not isinstance(cur, dict):
        raise ReleaseError("invalid local release state")
    for entry in (cur, cur.get("previous")):
        if entry:
            if not isinstance(entry, dict) or type(entry.get("seq")) is not int:
                raise ReleaseError("invalid local release number")
            highest = max(highest, entry["seq"])
    return highest


def write_local(home, name, value):
    path = os.path.join(home, name)
    with open(path + ".tmp", "w", encoding="utf-8") as f:
        json.dump(value, f, sort_keys=True)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(path + ".tmp", path)


def remove_bytecode(root):
    """Delete __pycache__ folders that Python wrote into a version started by an older launcher."""
    for base, dirs, _names in os.walk(root):
        for name in list(dirs):
            path = os.path.join(base, name)
            if name == "__pycache__" and not os.path.islink(path):
                shutil.rmtree(path, ignore_errors=True)
                dirs.remove(name)


def tree_problems(root, files, exact=True):
    root_info = os.lstat(root)
    if (not stat.S_ISDIR(root_info.st_mode) or stat.S_ISLNK(root_info.st_mode)
            or getattr(root_info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT):
        return ["unexpected version directory"]
    problems = []
    allowed = set(files) | {"release.json", "release.json.sig"}
    if exact:
        def walk_error(error):
            raise error
        for base, dirs, names in os.walk(root, onerror=walk_error):
            for name in dirs + names:
                path = os.path.join(base, name)
                rel = os.path.relpath(path, root).replace(os.sep, "/")
                info = os.lstat(path)
                linked = (stat.S_ISLNK(info.st_mode) or
                          getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT)
                if linked or (name in dirs and not any(f.startswith(rel + "/") for f in files)):
                    problems.append("unexpected entry: " + rel)
                    if name in dirs:
                        dirs.remove(name)
                elif name in names and (rel not in allowed or not stat.S_ISREG(info.st_mode)):
                    problems.append("unexpected entry: " + rel)
        if problems:
            return sorted(problems)
    for path, meta in sorted(files.items()):
        try:
            with open(os.path.join(root, *path.split("/")), "rb") as f:
                data = f.read(meta["size"] + 1)
        except OSError:
            problems.append("missing file: " + path)
            continue
        if len(data) != meta["size"] or hashlib.sha256(data).hexdigest() != meta["sha256"]:
            problems.append("changed file: " + path)
    return problems


def prepare(home, rel, raw, sig, fetch_file):
    """Call under update_lock, after authenticating the manifest and validating its paths."""
    name = "%d-%s" % (rel["seq"], rel["version"])
    relative = "versions/" + name
    versions = os.path.join(home, "versions")
    os.makedirs(versions, exist_ok=True)
    final = os.path.join(versions, name)
    if os.path.lexists(final):
        problems = tree_problems(final, rel["files"])
        if problems:
            raise ReleaseError(", ".join(problems))
        for filename, expected in (("release.json", raw), ("release.json.sig", sig)):
            with open(os.path.join(final, filename), "rb") as f:
                if f.read(len(expected) + 1) != expected:
                    raise ReleaseError("changed file: " + filename)
        return relative
    stage = tempfile.mkdtemp(prefix=".stage-", dir=versions)
    try:
        for path, meta in sorted(rel["files"].items()):
            data = fetch_file(path)
            if len(data) != meta["size"] or hashlib.sha256(data).hexdigest() != meta["sha256"]:
                raise ReleaseError("downloaded %s does not match the signed release" % path)
            target = os.path.join(stage, *path.split("/"))
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "wb") as f:
                f.write(data)
        for name, data in (("release.json", raw), ("release.json.sig", sig)):
            with open(os.path.join(stage, name), "wb") as f:
                f.write(data)
        problems = tree_problems(stage, rel["files"])
        if problems:
            raise ReleaseError(", ".join(problems))
        os.rename(stage, final)
    finally:
        shutil.rmtree(stage, ignore_errors=True)
    return relative


def check_candidate(home, directory, rel):
    stub = """import sys
sys.path.insert(0, sys.argv[1])
from skynet_agent import RELEASE_SEQ, __version__
if (RELEASE_SEQ, __version__) != (int(sys.argv[2]), sys.argv[3]):
    sys.exit("candidate reports a different release")
from skynet_agent.cli import main
sys.exit(main(["verify-install"]))
"""
    try:
        result = subprocess.run([sys.executable, "-IB", "-c", stub, directory,
                                 str(rel["seq"]), rel["version"]], timeout=300, capture_output=True,
                                env=dict(os.environ, SKYNET_AGENT_HOME=home))
    except subprocess.SubprocessError as e:
        raise ReleaseError("verify-install failed: %s" % e) from e
    if result.returncode:
        detail = (result.stdout + result.stderr).decode("utf-8", "replace").strip()
        raise ReleaseError("verify-install failed: %s" % detail)


def switch_version(home, rel, relative, confirmed=True):
    """Commit a prepared version under update_lock. Either launcher accepts either pointer."""
    cur = read_local(os.path.join(home, "current.json"), {})
    previous = cur.get("previous")
    if cur and cur["dir"] != relative:
        previous = {k: cur[k] for k in ("seq", "version", "dir")}
    new = dict(seq=rel["seq"], version=rel["version"], dir=relative,
               previous=previous, activated=int(time.time()))
    highest = sequence_floor(home)
    if confirmed:
        highest = max(highest, rel["seq"])
    write_local(home, "max_seq.json", highest)
    tmp = os.path.join(home, "launcher.py.tmp")
    shutil.copyfile(os.path.join(home, *relative.split("/"), "launcher.py"), tmp)
    write_local(home, "current.json", new)
    os.replace(tmp, os.path.join(home, "launcher.py"))
    obsolete = cur.get("previous") or {}
    old_dir = obsolete.get("dir", "")
    if (re.fullmatch(r"versions/[0-9]{1,9}-[0-9.]{1,20}", old_dir)
            and old_dir not in (relative, (previous or {}).get("dir"))):
        shutil.rmtree(os.path.join(home, *old_dir.split("/")), ignore_errors=True)
    return new
