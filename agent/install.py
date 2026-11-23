#!/usr/bin/env python3
"""Installer of the SkyNet research agent. Standard library only.

    python3 -I install.py            install into the default folder
    python3 -I install.py --home DIR install somewhere else
    python3 -I install.py --from-dir DIR install a signed local release

The installer authenticates release.json with its pinned public key before it
downloads any code. It checks the files and runs verify-install locally before
switching versions. Download the installer itself from a trusted source.
"""

from contextlib import contextmanager
import argparse
import hashlib
import json
import os
import re
import runpy
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import ssl
import urllib.parse
import urllib.error
import urllib.request

REPO_RAW = "https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main"
MIN_PYTHON = (3, 9)
MAX_FILE_BYTES = 2 << 20

_PATH_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_./-]{0,159}$")
_VERSION_RE = re.compile(r"^\d{1,4}\.\d{1,4}\.\d{1,4}$")


# Shared with skynet_agent/deployment.py; CI checks the standalone copy.
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
    history = read_local(os.path.join(home, "release-history.json"), {})
    if not isinstance(history, dict) or type(history.get("seq", 0)) is not int:
        raise ReleaseError("invalid durable release history")
    return max(highest, history.get("seq", 0))


def write_local(home, name, value):
    path = os.path.join(home, name)
    with open(path + ".tmp", "w", encoding="utf-8") as f:
        json.dump(value, f, sort_keys=True)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(path + ".tmp", path)


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
        previous = {k: cur[k] for k in ("seq", "version", "dir", "runtime", "python", "compat", "manifest_sha256") if k in cur}
    new = dict(runtime="python", python=sys.executable, seq=rel["seq"], version=rel["version"], dir=relative,
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


InstallError = ReleaseError

RELEASE_KEYS = ["33deadd767eddfb05d5646caa1b32727a73e261a071d8d4ca8530b7355d2ded9"]

# Verify-only subset of skynet_agent/ed25519.py (RFC 8032).
_p = 2 ** 255 - 19
_q = 2 ** 252 + 27742317777372353535851937790883648493


def _sha512(data):
    return hashlib.sha512(data).digest()


def _inv(x):
    return pow(x, _p - 2, _p)


_d = -121665 * _inv(121666) % _p
_sqrt_m1 = pow(2, (_p - 1) // 4, _p)


def _sha512_modq(data):
    return int.from_bytes(_sha512(data), "little") % _q


# Points are (X, Y, Z, T) in extended coordinates: x = X/Z, y = Y/Z, x*y = T/Z.
def _add(P, Q):
    A = (P[1] - P[0]) * (Q[1] - Q[0]) % _p
    B = (P[1] + P[0]) * (Q[1] + Q[0]) % _p
    C = 2 * P[3] * Q[3] * _d % _p
    D = 2 * P[2] * Q[2] % _p
    E, F, G, H = B - A, D - C, D + C, B + A
    return (E * F % _p, G * H % _p, F * G % _p, E * H % _p)


def _mul(s, P):
    Q = (0, 1, 1, 0)
    while s > 0:
        if s & 1:
            Q = _add(Q, P)
        P = _add(P, P)
        s >>= 1
    return Q


def _equal(P, Q):
    if (P[0] * Q[2] - Q[0] * P[2]) % _p != 0:
        return False
    if (P[1] * Q[2] - Q[1] * P[2]) % _p != 0:
        return False
    return True


def _recover_x(y, sign):
    if y >= _p:
        return None
    x2 = (y * y - 1) * _inv(_d * y * y + 1) % _p
    if x2 == 0:
        return None if sign else 0
    x = pow(x2, (_p + 3) // 8, _p)
    if (x * x - x2) % _p != 0:
        x = x * _sqrt_m1 % _p
    if (x * x - x2) % _p != 0:
        return None
    if (x & 1) != sign:
        x = _p - x
    return x


_g_y = 4 * _inv(5) % _p
_g_x = _recover_x(_g_y, 0)
_G = (_g_x, _g_y, 1, _g_x * _g_y % _p)


def _decompress(s):
    if len(s) != 32:
        return None
    y = int.from_bytes(s, "little")
    sign = y >> 255
    y &= (1 << 255) - 1
    x = _recover_x(y, sign)
    if x is None:
        return None
    return (x, y, 1, x * y % _p)


def verify(public, msg, signature):
    """Return True only if signature is a valid Ed25519 signature of msg."""
    if not isinstance(public, (bytes, bytearray)) or len(public) != 32:
        return False
    if not isinstance(signature, (bytes, bytearray)) or len(signature) != 64:
        return False
    A = _decompress(bytes(public))
    if A is None:
        return False
    Rs = bytes(signature[:32])
    R = _decompress(Rs)
    if R is None:
        return False
    s = int.from_bytes(signature[32:], "little")
    if s >= _q:
        return False
    h = _sha512_modq(Rs + bytes(public) + bytes(msg))
    sB = _mul(s, _G)
    hA = _mul(h, A)
    return _equal(sB, _add(R, hA))

def verify_manifest(raw, signature, test_key=None):
    keys = RELEASE_KEYS or ([test_key] if test_key else [])
    for line in signature.splitlines():
        fields = line.strip().split(b":")
        if len(fields) != 3 or fields[0] != b"ed25519":
            continue
        try:
            public, sig = (bytes.fromhex(x.decode("ascii")) for x in fields[1:])
        except ValueError:
            continue
        if public.hex() in keys and verify(public, raw, sig):
            return
    raise InstallError("no valid signature from a trusted release key")



def is_store_python():
    """Python from the Microsoft Store: it sees a private copy of AppData and of the registry."""
    where = (sys.executable + "|" + getattr(sys, "base_prefix", "")).lower()
    return sys.platform == "win32" and "\\windowsapps\\pythonsoftwarefoundation." in where


def default_home():
    env = os.environ.get("SKYNET_AGENT_HOME")
    if env:
        return os.path.abspath(env)
    if sys.platform == "win32":
        if is_store_python():
            # A folder in AppData would exist only inside the Store package's private view,
            # and the start script written there could not be found from a normal window.
            return os.path.join(os.path.expanduser("~"), "SkyNetAgent")
        base = os.environ.get("LOCALAPPDATA") or os.path.join(os.path.expanduser("~"), "AppData", "Local")
        return os.path.join(base, "SkyNetAgent")
    if sys.platform == "darwin":
        return os.path.join(os.path.expanduser("~"), "Library", "Application Support", "SkyNetAgent")
    base = os.environ.get("XDG_DATA_HOME") or os.path.join(os.path.expanduser("~"), ".local", "share")
    return os.path.join(base, "skynet-agent")


def system_ca_context():
    """A TLS context that also trusts the operating system's certificate file, or None.

    Python from python.org on macOS cannot see the system certificates until its
    "Install Certificates" script has been run. The server is still verified.
    """
    files = ["/etc/ssl/cert.pem", "/etc/ssl/certs/ca-certificates.crt",
             "/etc/pki/tls/certs/ca-bundle.crt", "/etc/ssl/ca-bundle.pem"]
    if os.environ.get("PREFIX"):
        files.append(os.path.join(os.environ["PREFIX"], "etc", "tls", "cert.pem"))
    context = ssl.create_default_context()
    loaded = False
    for name in files:
        if os.path.isfile(name):
            try:
                context.load_verify_locations(cafile=name)
                loaded = True
            except (OSError, ssl.SSLError):
                pass
    return context if loaded else None


_fallback = {"context": None}   # set once Python's own certificates have failed


def check_url(url, allow_local_http):
    parts = urllib.parse.urlsplit(url)
    local = parts.scheme == "http" and parts.hostname in ("localhost", "127.0.0.1", "::1")
    if not parts.hostname or not (parts.scheme == "https" or (allow_local_http and local)):
        raise InstallError("unsupported address: %s" % url)


class _Redirect(urllib.request.HTTPRedirectHandler):
    def __init__(self, allow_local_http):
        self.allow_local_http = allow_local_http

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_url(newurl, self.allow_local_http)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _open(req, context, allow_local_http):
    opener = urllib.request.build_opener(_Redirect(allow_local_http), urllib.request.HTTPSHandler(context=context))
    return opener.open(req, timeout=60)


def fetch(url, max_bytes=MAX_FILE_BYTES, *, allow_local_http=False):
    check_url(url, allow_local_http)
    req = urllib.request.Request(url, headers={"User-Agent": "skynet-agent-installer"})
    context = _fallback["context"]
    while True:
        try:
            with _open(req, context, allow_local_http) as resp:
                data = resp.read(max_bytes + 1)
            break
        except (urllib.error.URLError, OSError) as e:
            bad_certificate = (isinstance(e, ssl.SSLCertVerificationError)
                               or isinstance(getattr(e, "reason", None), ssl.SSLCertVerificationError))
            if context is None and bad_certificate:
                context = system_ca_context()
                if context is not None:
                    _fallback["context"] = context
                    continue
            raise InstallError("cannot download %s: %s" % (url, e))
    if len(data) > max_bytes:
        raise InstallError("%s is larger than expected" % url)
    return data


def safe_path(path):
    if not isinstance(path, str) or not _PATH_RE.fullmatch(path):
        return False
    if "/./" in path or ".." in path or "//" in path or path.endswith("/"):
        return False
    return path == "launcher.py" or (path.startswith("skynet_agent/") and path.endswith(".py"))


def is_termux():
    return "TERMUX_VERSION" in os.environ or os.environ.get("PREFIX", "").startswith("/data/data/com.termux")


def write_shim(home, bin_dir=None, uninstaller=None):
    """Create a small start script. Returns (path, hint for the user)."""
    launcher = os.path.join(home, "launcher.py")
    if os.name == "nt":
        folder = bin_dir or home
        os.makedirs(folder, exist_ok=True)
        shim = os.path.join(folder, "skynet-agent.cmd")
        exe = sys.executable
        if os.path.normcase(folder) == os.path.normcase(home):
            launcher = r"%~dp0launcher.py"
            if os.path.normcase(exe) == os.path.normcase(os.path.join(home, "python", "python.exe")):
                exe = r"%~dp0python\python.exe"
        with open(shim, "w", encoding="ascii", errors="replace", newline="\r\n") as f:
            f.write('@echo off\nsetlocal DisableDelayedExpansion\n"%s" -I "%s" %%*\n' % (exe, launcher))
        return shim, 'Run it as:  & "%s" status' % shim
    if bin_dir:
        pass
    elif is_termux():
        bin_dir = os.path.join(os.environ.get("PREFIX", "/data/data/com.termux/files/usr"), "bin")
    else:
        bin_dir = os.path.join(os.path.expanduser("~"), ".local", "bin")
    os.makedirs(bin_dir, exist_ok=True)
    shim = os.path.join(bin_dir, "skynet-agent")
    py = shlex.quote(sys.executable)
    with tempfile.NamedTemporaryFile(mode="w", dir=bin_dir, delete=False, encoding="utf-8", newline="\n") as f:
        f.write("#!/bin/sh\n")
        if uninstaller:
            f.write('if [ "${1:-}" = uninstall ]; then\n    shift\n')
            f.write('    exec %s -I %s "$0" "$@"\nfi\n' % (py, shlex.quote(uninstaller)))
        f.write('exec %s -I %s "$@"\n' % (py, shlex.quote(launcher)))
    os.chmod(f.name, 0o755)
    os.replace(f.name, shim)
    on_path = bin_dir in os.environ.get("PATH", "").split(os.pathsep)
    hint = "Run it as:  skynet-agent status"
    if not on_path:
        hint = "Run it as:  %s status   (or add %s to your PATH)" % (shim, bin_dir)
    return shim, hint


def read_release(get, test_key=None):
    raw = get("release.json", 256 * 1024)
    sig = get("release.json.sig", 16384)
    verify_manifest(raw, sig, test_key)
    try:
        rel = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as e:
        raise InstallError("the release description is not valid JSON: %s" % e)
    if (not isinstance(rel, dict) or type(rel.get("seq")) is not int or not 1 <= rel["seq"] <= 999999999
            or rel.get("format") != 1
            or not isinstance(rel.get("version"), str) or not _VERSION_RE.fullmatch(rel["version"])
            or not isinstance(rel.get("files"), dict) or not rel["files"]):
        raise InstallError("the release description has an unexpected shape")
    minpy = rel.get("min_python", [3, 9])
    if (not isinstance(minpy, list) or len(minpy) != 2
            or not all(isinstance(v, int) and not isinstance(v, bool) for v in minpy)):
        raise InstallError("the release description has an unexpected shape")
    if sys.version_info[:2] < tuple(minpy):
        raise InstallError("this release needs Python %d.%d or newer" % tuple(minpy))

    files = rel["files"]
    required = {"launcher.py", "skynet_agent/cli.py", "skynet_agent/__init__.py"}
    if len(files) > 200 or not required.issubset(files):
        raise InstallError("unexpected release file list")
    for path, meta in files.items():
        if (not safe_path(path) or not isinstance(meta, dict) or type(meta.get("size")) is not int
                or not 0 <= meta["size"] <= MAX_FILE_BYTES
                or not isinstance(meta.get("sha256"), str) or not re.fullmatch(r"[0-9a-f]{64}", meta["sha256"])):
            raise InstallError("invalid file description: %r" % path)
    halt = rel.get("halt")
    if halt is not None and (not isinstance(halt, dict) or type(halt.get("through_seq")) is not int):
        raise InstallError("invalid halt description")
    if halt and rel["seq"] <= halt["through_seq"]:
        raise InstallError("this release is paused by the maintainers")
    return rel, raw, sig


def local_reader(directory):
    def get(path, limit=MAX_FILE_BYTES):
        filename = os.path.join(directory, *path.split("/"))
        info = os.lstat(filename)
        if (not stat.S_ISREG(info.st_mode)
                or getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT):
            raise InstallError("unexpected file: " + path)
        with open(filename, "rb") as stream:
            data = stream.read(limit + 1)
        if len(data) > limit:
            raise InstallError("file is larger than expected: " + path)
        return data
    return get


class NewerInstalled(InstallError):
    """Setup can keep a newer active release when installing its runtime."""


def install(home, base, *, from_dir=None, allow_local_http=False, allow_downgrade=False, test_key=None):
    if allow_downgrade:
        raise InstallError('downgrade is disabled')
    if from_dir is None:
        def get(path, limit=MAX_FILE_BYTES):
            return fetch(base.rstrip("/") + "/agent/" + path, limit, allow_local_http=allow_local_http)
    else:
        get = local_reader(from_dir)
    rel, raw, sig = read_release(get, test_key)
    if from_dir is not None:
        problems = tree_problems(from_dir, rel["files"])
        if problems:
            raise InstallError(", ".join(problems))
    with update_lock(home):
        floor = sequence_floor(home)
        if rel["seq"] < floor:
            message = "release %d is older than %d" % (rel["seq"], floor)
            current = read_local(os.path.join(home, "current.json"), {})
            if from_dir is not None and current.get("seq", 0) > rel["seq"]:
                raise NewerInstalled(message)
            raise InstallError(message)
        history = read_local(os.path.join(home, "release-history.json"), {})
        bad = read_local(os.path.join(home, "bad_seqs.json"), [])
        if rel["seq"] in bad or rel["seq"] in (history.get("bad_seqs") or []):
            raise InstallError("release previously failed on this device")
        relative = prepare(home, rel, raw, sig, get)
        check_candidate(home, os.path.join(home, *relative.split("/")), rel)
        switch_version(home, rel, relative)
    return rel


def main(argv=None):
    parser = argparse.ArgumentParser(description="Install the SkyNet research agent.")
    parser.add_argument("--home", help="folder to install into (default: a folder in your profile)")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--base", help="address of the repository files (for mirrors and tests)")
    source.add_argument("--from-dir", help="directory containing only the signed release")
    parser.add_argument("--keep-newer", action="store_true", help="keep a newer active release and refresh its shim")
    parser.add_argument("--bin-dir", help="folder for the skynet-agent start script")
    parser.add_argument("--no-shim", action="store_true", help="do not create a start script")
    parser.add_argument("--linux-setup", action="store_true", help=argparse.SUPPRESS)
    startup = parser.add_mutually_exclusive_group()
    startup.add_argument("--autostart", dest="autostart", action="store_true", default=None)
    startup.add_argument("--no-autostart", dest="autostart", action="store_false")
    parser.add_argument("--linger", action="store_true", help="allow the Linux user service to run before login")
    parser.add_argument("--allow-local-http", action="store_true", help="allow HTTP on loopback for tests")
    parser.add_argument("--test-release-key", help="test public key for a development installer with empty pins")
    args = parser.parse_args(argv)
    if args.linger and args.autostart is False:
        parser.error("--linger conflicts with --no-autostart")
    if (args.linger or args.autostart is not None) and not args.linux_setup:
        parser.error("use install.sh for Linux autostart options")
    if sys.version_info[:2] < MIN_PYTHON:
        print("Python %d.%d or newer is needed; this is %d.%d." % (MIN_PYTHON + tuple(sys.version_info[:2])))
        return 1
    home = os.path.abspath(args.home) if args.home else default_home()
    base = args.base or os.environ.get("SKYNET_AGENT_BASE_URL") or REPO_RAW
    print("Installing the SkyNet research agent into %s" % home)
    try:
        os.makedirs(home, exist_ok=True)
        try:
            rel = install(home, base, from_dir=args.from_dir, allow_local_http=args.allow_local_http,
                          test_key=args.test_release_key)
            message = "Installed version %s." % rel["version"]
        except NewerInstalled as e:
            if not args.keep_newer:
                raise
            message = "Keeping the installed release: %s" % e
        uninstaller = None
        if args.linux_setup:
            uninstaller = os.path.join(home, "uninstall.py")
            helper = os.path.join(os.path.dirname(__file__), "linux_setup.py")
            with tempfile.NamedTemporaryFile(dir=home, delete=False) as f:
                with open(helper, "rb") as source_file:
                    shutil.copyfileobj(source_file, f)
            os.replace(f.name, uninstaller)
        if args.no_shim:
            hint = 'Run it as:  "%s" "%s" status' % (sys.executable, os.path.join(home, "launcher.py"))
        else:
            _, hint = write_shim(home, args.bin_dir, uninstaller)
    except (InstallError, OSError, subprocess.SubprocessError) as e:
        print("Installation failed: %s" % e)
        return 1
    print(message)
    print(hint)
    if args.linux_setup:
        return runpy.run_path(uninstaller)["configure"](home, args.autostart, args.linger)
    print("")
    print("Next steps:")
    print("  1. skynet-agent selftest --online    check that everything works")
    print("  2. skynet-agent run                  start working (Ctrl+C stops it)")
    print("  3. skynet-agent autostart enable     optional: start when you log in")
    print("Nothing runs until you start it. No rewards are provided at this stage.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
