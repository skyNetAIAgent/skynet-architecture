"""Authenticate the Go bootstrap before delegating activation to the shared installer."""

import hashlib
import os
import platform
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urljoin, urlsplit

from . import deployment, net, signed

CHANNEL = "agent/v2/release.json"
LIMIT = 64 << 20
TARGETS = ("windows-amd64", "windows-arm64", "linux-amd64", "linux-arm64", "linux-arm")
HOSTS = {"github.com", "objects.githubusercontent.com", "release-assets.githubusercontent.com"}
ADAPTER = b"""import os
import subprocess
import sys


def main(argv=None):
    home = os.environ['SKYNET_AGENT_HOME']
    exe = 'skynet-agent.exe' if os.name == 'nt' else 'skynet-agent'
    return subprocess.call([os.path.join(home, exe), 'launch'] + (sys.argv[1:] if argv is None else argv))
"""
COMPAT = {"skynet_agent/__init__.py": b"", "skynet_agent/cli.py": ADAPTER}
Error = deployment.ReleaseError


def target():
    if hasattr(sys, "getandroidapilevel") or "TERMUX_VERSION" in os.environ or os.getenv("PREFIX", "").startswith("/data/data/"):
        return None
    system = platform.system().lower()
    machine = platform.machine().lower()
    if system == "windows":
        # IsWow64Process2 reports the native architecture even under x64 emulation.
        import ctypes
        import sysconfig
        try:
            proc, native = ctypes.c_ushort(), ctypes.c_ushort()
            kernel = ctypes.WinDLL("kernel32")
            if kernel.IsWow64Process2(ctypes.c_void_p(-1), ctypes.byref(proc), ctypes.byref(native)):
                machine = {0x8664: "amd64", 0xaa64: "arm64"}.get(native.value, "")
        except (AttributeError, OSError):
            machine = os.getenv("PROCESSOR_ARCHITEW6432") or machine or sysconfig.get_platform().removeprefix("win-")
        machine = machine.lower()
    arch = {"x86_64": "amd64", "amd64": "amd64", "arm64": "arm64",
            "aarch64": "arm64", "armv7l": "arm"}.get(machine)
    return system + "-" + str(arch)


def binary(key):
    return "skynet-agent.exe" if key.startswith("windows-") else "skynet-agent"


def check_url(url):
    if not isinstance(url, str):
        raise Error("missing asset URL")
    u = urlsplit(url)
    if u.scheme != "https" or u.netloc not in HOSTS or not u.path or u.fragment:
        raise Error("unexpected release asset URL")


def meta(data):
    return {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def validate(rel):
    def number(value, low, high):
        return type(value) is int and low <= value <= high

    if (not isinstance(rel, dict) or rel.keys() - {"format", "seq", "version", "min_bridge_seq", "targets", "compat_files", "halt"}
            or not number(rel.get("format"), 2, 2) or not number(rel.get("seq"), 1, 999999999)
            or not number(rel.get("min_bridge_seq"), 1, 999999999)
            or not isinstance(rel.get("version"), str) or not re.fullmatch(r"[0-9]{1,4}(\.[0-9]{1,4}){2}", rel["version"])):
        raise Error("invalid v2 release")
    targets = rel.get("targets")
    if not isinstance(targets, dict) or not targets:
        raise Error("empty target table")
    for key, t in targets.items():
        if (key not in TARGETS or not isinstance(t, dict) or set(t) != {"name", "url", "size", "sha256"}
                or t["name"] != binary(key) or not number(t["size"], 1, LIMIT)
                or not isinstance(t["sha256"], str) or not re.fullmatch("[0-9a-f]{64}", t["sha256"])):
            raise Error("invalid binary target")
        check_url(t["url"])
    if "compat_files" in rel and rel["compat_files"] != {k: meta(v) for k, v in COMPAT.items()}:
        raise Error("unexpected bridge adapters")
    if "halt" in rel:
        h = rel["halt"]
        if (not isinstance(h, dict) or h.keys() - {"through_seq", "reason"}
                or not number(h.get("through_seq"), 0, 999999999)
                or not isinstance(h.get("reason", ""), str) or len(h.get("reason", "")) > 500):
            raise Error("invalid halt")


def download(t):
    url = t["url"]
    for _ in range(4):
        check_url(url)
        status, data, headers = net.request(url, max_bytes=t["size"], follow_redirects=False)
        if status == 200:
            if meta(data) != {k: t[k] for k in ("size", "sha256")}:
                raise Error("incorrect binary size or SHA-256")
            return data
        if status not in (301, 302, 303, 307, 308):
            raise Error("asset HTTP %d" % status)
        location = next((v for k, v in headers.items() if k.lower() == "location"), None)
        if not location:
            raise Error("missing redirect location")
        url = urljoin(url, location)
    raise Error("too many redirects")


def stored_policy(home):
    p = deployment.read_local(os.path.join(home, "release-policy.json"))
    if p is None:
        return None
    if not isinstance(p, dict) or not all(isinstance(p.get(k), str) for k in ("raw", "signature")):
        raise Error("invalid cached release policy")
    raw, signature = p["raw"].encode(), p["signature"].encode("ascii")
    signed.verify_detached(raw, signature)
    rel = signed.strict_json_loads(raw)
    validate(rel)
    return rel


def remember(home, rel, raw, signature):
    with deployment.update_lock(home):
        old = stored_policy(home)
        if rel["seq"] < deployment.sequence_floor(home) or old and (
                old["seq"] > rel["seq"] or old["seq"] == rel["seq"] and deployment.read_local(os.path.join(home, "release-policy.json"))["raw"].encode() != raw):
            raise Error("stale or conflicting release policy")
        deployment.write_local(home, "release-policy.json",
                               {"raw": raw.decode(), "signature": signature.decode("ascii")})


def install(home, rel, raw, signature, *, automatic=True):
    # Only a pinned signature and the hash of the exact downloaded bytes authorize execution.
    signed.verify_detached(raw, signature)
    if signed.strict_json_loads(raw) != rel:
        raise Error("manifest changed")
    validate(rel)
    t = rel["targets"][target()]
    if not rel.get("compat_files"):
        raise Error("release lacks bridge adapters")
    home = os.path.abspath(home)
    versions = Path(home, "versions")
    deployment.real_directory(home)
    versions.mkdir(exist_ok=True)
    deployment.real_directory(versions)
    with tempfile.TemporaryDirectory(prefix=".stage-bootstrap-", dir=versions) as tmp:
        exe = Path(tmp, t["name"])
        data = download(t)
        if meta(data) != {k: t[k] for k in ("size", "sha256")}:
            raise Error("bootstrap hash mismatch")
        exe.write_bytes(data)
        Path(tmp, "release.json").write_bytes(raw)
        Path(tmp, "release.json.sig").write_bytes(signature)
        exe.chmod(0o700)
        env = dict(os.environ, SKYNET_AGENT_HOME=home)
        # CreateProcess limits the parsed executable name when lpApplicationName is NULL.
        application = str(exe)
        if os.name == "nt" and not application.startswith("\\\\?\\"):
            application = ("\\\\?\\UNC\\" + application[2:] if application.startswith("\\\\")
                           else "\\\\?\\" + application)
        try:
            subprocess.run([str(exe), "verify-install"], check=True, timeout=60, env=env, executable=application)
            args = [str(exe), "install-bundle", tmp, home, sys.executable]
            if automatic:
                args.append("--automatic")
            subprocess.run(args,
                           check=True, timeout=180, env=env, executable=application)
        except (OSError, subprocess.SubprocessError) as exc:
            raise Error("Go installation failed: %s" % exc) from exc
