"""Self-update from the repository, accepted only with a valid signature.

A release is agent/release.json plus agent/release.json.sig. It lists every
file of the agent with its size and SHA-256. The agent installs a release only
if all of this holds:

  * the signature is valid for a key pinned in trust.py;
  * the release number (seq) is higher than the running one (no rollback);
  * every downloaded file matches its size and hash;
  * the release did not already fail to start on this device.

The new version goes to its own directory; the previous one is kept, and the
launcher returns to it if the new one cannot start.
"""

import hashlib
import os
import re
import shutil
import sys
import time

from . import RELEASE_SEQ, config, net, signed, trust

RELEASE_PATH = "agent/release.json"
MAX_RELEASE_BYTES = 256 * 1024
MAX_FILE_BYTES = 2 << 20
MAX_FILES = 200

_PATH_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_./-]{0,159}$")
_SHA_RE = re.compile(r"^[0-9a-f]{64}$")
_VERSION_RE = re.compile(r"^\d{1,4}\.\d{1,4}\.\d{1,4}$")
_REQUIRED = ("skynet_agent/__init__.py", "skynet_agent/cli.py", "launcher.py")


class ReleaseError(Exception):
    pass


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def safe_path(path):
    """True if a release may contain this file path (relative to agent/)."""
    if not isinstance(path, str) or not _PATH_RE.match(path):
        return False
    if ".." in path or "//" in path or path.endswith("/"):
        return False
    if path == "launcher.py":
        return True
    return path.startswith("skynet_agent/") and path.endswith(".py")


def validate_release(rel):
    if not isinstance(rel, dict) or rel.get("format") != 1:
        raise ReleaseError("unknown release format")
    if not _is_int(rel.get("seq")) or rel["seq"] < 1:
        raise ReleaseError("seq must be a positive integer")
    if not isinstance(rel.get("version"), str) or not _VERSION_RE.match(rel["version"]):
        raise ReleaseError("version must look like 1.2.3")
    minpy = rel.get("min_python", [3, 9])
    if (not isinstance(minpy, list) or len(minpy) != 2
            or not all(_is_int(v) and 0 <= v < 100 for v in minpy)):
        raise ReleaseError("min_python must be [major, minor]")
    files = rel.get("files")
    if not isinstance(files, dict) or not 1 <= len(files) <= MAX_FILES:
        raise ReleaseError("files must list 1..%d files" % MAX_FILES)
    for path, meta in files.items():
        if not safe_path(path):
            raise ReleaseError("file path not allowed: %r" % (path,))
        if (not isinstance(meta, dict) or not isinstance(meta.get("sha256"), str)
                or not _SHA_RE.match(meta["sha256"])
                or not _is_int(meta.get("size")) or not 0 <= meta["size"] <= MAX_FILE_BYTES):
            raise ReleaseError("bad size or hash for %s" % path)
    for path in _REQUIRED:
        if path not in files:
            raise ReleaseError("release lacks %s" % path)
    halt = rel.get("halt")
    if halt is not None:
        if (not isinstance(halt, dict) or not _is_int(halt.get("through_seq"))
                or not isinstance(halt.get("reason", ""), str) or len(halt.get("reason", "")) > 500):
            raise ReleaseError("halt must be {through_seq, reason}")


def fetch_release(base_url):
    """Return (release, raw bytes, signature bytes) after checking the signature."""
    rel, raw, sig = signed.fetch_signed_json(base_url, RELEASE_PATH, max_bytes=MAX_RELEASE_BYTES)
    validate_release(rel)
    return rel, raw, sig


def halt_reason(rel):
    """Text if the maintainers asked agents of this version to stop taking work."""
    halt = rel.get("halt")
    if halt and RELEASE_SEQ <= halt["through_seq"]:
        return halt.get("reason") or "the maintainers paused this version"
    return ""


def python_ok(rel):
    major, minor = rel.get("min_python", [3, 9])
    return sys.version_info[:2] >= (major, minor)


def version_dir_name(rel):
    return "%d-%s" % (rel["seq"], rel["version"])


def download_release(home, base_url, rel, raw, sig):
    """Download and check every file. Returns the directory relative to home."""
    name = version_dir_name(rel)
    final = os.path.join(home, "versions", name)
    tmp = final + ".tmp"
    shutil.rmtree(tmp, ignore_errors=True)
    agent_base = base_url.rstrip("/") + "/agent/"
    try:
        for path in sorted(rel["files"]):
            meta = rel["files"][path]
            data = net.get(agent_base + path, max_bytes=MAX_FILE_BYTES)
            if len(data) != meta["size"] or hashlib.sha256(data).hexdigest() != meta["sha256"]:
                raise ReleaseError("downloaded %s does not match the signed release" % path)
            target = os.path.join(tmp, *path.split("/"))
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "wb") as f:
                f.write(data)
        with open(os.path.join(tmp, "release.json"), "wb") as f:
            f.write(raw)
        with open(os.path.join(tmp, "release.json.sig"), "wb") as f:
            f.write(sig)
        shutil.rmtree(final, ignore_errors=True)
        os.replace(tmp, final)
    except BaseException:
        shutil.rmtree(tmp, ignore_errors=True)
        raise
    return "versions/" + name


def verify_installed(version_dir, keys=None):
    """Check an installed version against its own signed release. Returns a list of problems."""
    problems = []
    try:
        with open(os.path.join(version_dir, "release.json"), "rb") as f:
            raw = f.read()
        with open(os.path.join(version_dir, "release.json.sig"), "rb") as f:
            sig = f.read()
    except OSError as e:
        return ["cannot read the release description: %s" % e]
    try:
        signed.verify_detached(raw, sig, keys=keys)
        rel = signed.strict_json_loads(raw)
        validate_release(rel)
    except (signed.SignatureError, ReleaseError, ValueError) as e:
        return ["release description: %s" % e]
    for path, meta in sorted(rel["files"].items()):
        try:
            with open(os.path.join(version_dir, *path.split("/")), "rb") as f:
                data = f.read()
        except OSError:
            problems.append("missing file: %s" % path)
            continue
        if len(data) != meta["size"] or hashlib.sha256(data).hexdigest() != meta["sha256"]:
            problems.append("changed file: %s" % path)
    return problems


def read_current(home):
    cur = config.read_json(os.path.join(home, "current.json"))
    return cur if isinstance(cur, dict) else None


def activate(home, rel, rel_dir):
    """Point current.json at the new version and refresh the launcher."""
    cur = read_current(home)
    previous = None
    if cur and cur.get("dir") != rel_dir:
        previous = {"seq": cur.get("seq"), "version": cur.get("version"), "dir": cur.get("dir")}
    elif cur and isinstance(cur.get("previous"), dict):
        previous = cur["previous"]      # activated twice: keep the version to go back to
    new = {"seq": rel["seq"], "version": rel["version"], "dir": rel_dir,
           "previous": previous, "activated": int(time.time())}
    src = os.path.join(home, *rel_dir.split("/"), "launcher.py")
    if os.path.exists(src):
        tmp = os.path.join(home, "launcher.py.tmp")
        shutil.copyfile(src, tmp)
        os.replace(tmp, os.path.join(home, "launcher.py"))
    config.write_json_atomic(os.path.join(home, "current.json"), new)
    keep = {rel_dir.split("/")[-1]}
    if previous and previous.get("dir"):
        keep.add(str(previous["dir"]).split("/")[-1])
    versions = os.path.join(home, "versions")
    try:
        for name in os.listdir(versions):
            if name not in keep:
                shutil.rmtree(os.path.join(versions, name), ignore_errors=True)
    except OSError:
        pass
    return new


def running_dir():
    """Directory of the version this code runs from."""
    return os.path.realpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def is_installed_layout(home):
    """True if this code runs from <home>/versions/..., i.e. it may update itself."""
    versions = os.path.realpath(os.path.join(home, "versions"))
    try:
        return os.path.commonpath([running_dir(), versions]) == versions and read_current(home) is not None
    except ValueError:
        return False


class UpdateResult:
    def __init__(self):
        self.halt = ""          # non-empty: stop taking tasks
        self.available = None   # (seq, version) of a newer release, if any
        self.installed = False  # True: a new version is in place, restart needed
        self.note = ""


def bad_seqs(home):
    """Releases the launcher had to roll back from on this device."""
    data = config.read_json(os.path.join(home, "bad_seqs.json"), [])
    return [x for x in data if _is_int(x)] if isinstance(data, list) else []


def check_and_apply(home, base_url, cfg):
    """Look for a newer signed release and, in "auto" mode, install it.

    The release description is read in every update mode, because it also carries the
    maintainers' request to pause ("halt"). The mode only decides what happens to a
    newer version.
    """
    result = UpdateResult()
    rel, raw, sig = fetch_release(base_url)
    result.halt = halt_reason(rel)
    if cfg.get("update") == "off" or rel["seq"] <= RELEASE_SEQ:
        return result
    result.available = (rel["seq"], rel["version"])
    if rel["seq"] in bad_seqs(home):
        result.note = "release %d failed to start here earlier; waiting for the next one" % rel["seq"]
        return result
    if not python_ok(rel):
        result.note = "release %s needs Python %d.%d or newer" % (
            rel["version"], rel["min_python"][0], rel["min_python"][1])
        return result
    if cfg.get("update") != "auto":
        result.note = "update mode is %r, not installing" % cfg.get("update")
        return result
    if not is_installed_layout(home):
        result.note = "not an installed copy (development run), not installing"
        return result
    target = "versions/" + version_dir_name(rel)
    cur = read_current(home)
    if cur and cur.get("seq") == rel["seq"] and cur.get("dir") == target:
        # Already in place, for example installed by "skynet-agent update" while this copy
        # was running. Downloading it again would also drop the version to go back to.
        if running_dir() == os.path.realpath(os.path.join(home, *target.split("/"))):
            # This very copy claims an older number than its description: never loop on it.
            result.note = "release %d is already running, not installing it again" % rel["seq"]
            return result
        result.installed = True
        return result
    rel_dir = download_release(home, base_url, rel, raw, sig)
    activate(home, rel, rel_dir)
    result.installed = True
    return result


def base_url():
    return (os.environ.get("SKYNET_AGENT_BASE_URL") or trust.RAW_BASE).rstrip("/")
