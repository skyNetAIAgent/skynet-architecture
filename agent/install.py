#!/usr/bin/env python3
"""Installer of the SkyNet research agent. Standard library only.

    python3 -I install.py            install into the default folder
    python3 -I install.py --home DIR install somewhere else

What it does, and nothing more:
  1. downloads the release description (agent/release.json) and the files it lists;
  2. checks every file against the size and SHA-256 in the release description;
  3. asks the downloaded agent to verify the release signature and to run a self-test;
  4. writes the launcher, current.json and a small "skynet-agent" start script.

It does not start the agent, does not turn autostart on and does not need
administrator rights. Honest note: the very first installation trusts the
HTTPS connection to GitHub; every later update is checked against the release
key that is built into the installed agent.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.request

REPO_RAW = "https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main"
MIN_PYTHON = (3, 9)
MAX_FILE_BYTES = 2 << 20

STUB = ("import sys; sys.path.insert(0, sys.argv[1]); "
        "sys.argv = [sys.argv[0]] + sys.argv[2:]; "
        "from skynet_agent.cli import main; sys.exit(main())")

_PATH_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_./-]{0,159}$")
_VERSION_RE = re.compile(r"^\d{1,4}\.\d{1,4}\.\d{1,4}$")


class InstallError(Exception):
    pass


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


def fetch(url, max_bytes=MAX_FILE_BYTES):
    if not (url.startswith("https://") or url.startswith("http://")):
        raise InstallError("unsupported address: %s" % url)
    req = urllib.request.Request(url, headers={"User-Agent": "skynet-agent-installer"})
    context = _fallback["context"]
    while True:
        try:
            with urllib.request.urlopen(req, timeout=60, context=context) as resp:
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
    if not isinstance(path, str) or not _PATH_RE.match(path):
        return False
    if ".." in path or "//" in path or path.endswith("/"):
        return False
    return path == "launcher.py" or (path.startswith("skynet_agent/") and path.endswith(".py"))


def is_termux():
    return "TERMUX_VERSION" in os.environ or os.environ.get("PREFIX", "").startswith("/data/data/com.termux")


def write_shim(home, bin_dir=None):
    """Create a small start script. Returns (path, hint for the user)."""
    launcher = os.path.join(home, "launcher.py")
    if os.name == "nt":
        folder = bin_dir or home
        os.makedirs(folder, exist_ok=True)
        shim = os.path.join(folder, "skynet-agent.cmd")
        with open(shim, "w", encoding="ascii", errors="replace", newline="\r\n") as f:
            f.write('@echo off\n"%s" "%s" %%*\n' % (sys.executable, launcher))
        return shim, 'Run it as:  & "%s" status' % shim
    if bin_dir:
        pass
    elif is_termux():
        bin_dir = os.path.join(os.environ.get("PREFIX", "/data/data/com.termux/files/usr"), "bin")
    else:
        bin_dir = os.path.join(os.path.expanduser("~"), ".local", "bin")
    os.makedirs(bin_dir, exist_ok=True)
    shim = os.path.join(bin_dir, "skynet-agent")
    with open(shim, "w", encoding="utf-8", newline="\n") as f:
        f.write('#!/bin/sh\nexec "%s" "%s" "$@"\n' % (sys.executable, launcher))
    os.chmod(shim, 0o755)
    on_path = bin_dir in os.environ.get("PATH", "").split(os.pathsep)
    hint = "Run it as:  skynet-agent status"
    if not on_path:
        hint = "Run it as:  %s status   (or add %s to your PATH)" % (shim, bin_dir)
    return shim, hint


def install(home, base):
    base = base.rstrip("/")
    raw = fetch(base + "/agent/release.json", 256 * 1024)
    sig = fetch(base + "/agent/release.json.sig", 16384)
    try:
        rel = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as e:
        raise InstallError("the release description is not valid JSON: %s" % e)
    if (not isinstance(rel, dict) or not isinstance(rel.get("seq"), int)
            or not isinstance(rel.get("version"), str) or not _VERSION_RE.match(rel["version"])
            or not isinstance(rel.get("files"), dict) or not rel["files"]):
        raise InstallError("the release description has an unexpected shape")
    minpy = rel.get("min_python", [3, 9])
    if (not isinstance(minpy, list) or len(minpy) != 2
            or not all(isinstance(v, int) and not isinstance(v, bool) for v in minpy)):
        raise InstallError("the release description has an unexpected shape")
    if sys.version_info[:2] < tuple(minpy):
        raise InstallError("this release needs Python %d.%d or newer" % tuple(minpy))

    name = "%d-%s" % (rel["seq"], rel["version"])
    final = os.path.join(home, "versions", name)
    tmp = final + ".tmp"
    os.makedirs(os.path.join(home, "versions"), exist_ok=True)
    shutil.rmtree(tmp, ignore_errors=True)
    try:
        for path in sorted(rel["files"]):
            meta = rel["files"][path]
            if not safe_path(path) or not isinstance(meta, dict):
                raise InstallError("the release lists a file it must not contain: %r" % (path,))
            data = fetch(base + "/agent/" + path)
            if len(data) != meta.get("size") or hashlib.sha256(data).hexdigest() != meta.get("sha256"):
                raise InstallError("downloaded %s does not match the release description" % path)
            target = os.path.join(tmp, *path.split("/"))
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, "wb") as f:
                f.write(data)
        with open(os.path.join(tmp, "release.json"), "wb") as f:
            f.write(raw)
        with open(os.path.join(tmp, "release.json.sig"), "wb") as f:
            f.write(sig)
        env = dict(os.environ)
        env["SKYNET_AGENT_HOME"] = home
        check = subprocess.run([sys.executable, "-I", "-c", STUB, tmp, "verify-install"],
                               env=env, capture_output=True, timeout=300)
        if check.returncode != 0:
            detail = (check.stdout + check.stderr).decode("utf-8", "replace").strip()
            raise InstallError("the downloaded agent did not pass its own check: %s" % detail)
        shutil.rmtree(final, ignore_errors=True)
        os.replace(tmp, final)
    except BaseException:
        shutil.rmtree(tmp, ignore_errors=True)
        raise

    shutil.copyfile(os.path.join(final, "launcher.py"), os.path.join(home, "launcher.py.tmp"))
    os.replace(os.path.join(home, "launcher.py.tmp"), os.path.join(home, "launcher.py"))
    current = {"seq": rel["seq"], "version": rel["version"], "dir": "versions/" + name,
               "previous": None, "activated": int(time.time())}
    with open(os.path.join(home, "current.json.tmp"), "w", encoding="utf-8") as f:
        json.dump(current, f, indent=2, sort_keys=True)
        f.write("\n")
    os.replace(os.path.join(home, "current.json.tmp"), os.path.join(home, "current.json"))
    return rel


def main(argv=None):
    parser = argparse.ArgumentParser(description="Install the SkyNet research agent.")
    parser.add_argument("--home", help="folder to install into (default: a folder in your profile)")
    parser.add_argument("--base", help="address of the repository files (for mirrors and tests)")
    parser.add_argument("--bin-dir", help="folder for the skynet-agent start script")
    parser.add_argument("--no-shim", action="store_true", help="do not create a start script")
    args = parser.parse_args(argv)
    if sys.version_info[:2] < MIN_PYTHON:
        print("Python %d.%d or newer is needed; this is %d.%d." % (MIN_PYTHON + tuple(sys.version_info[:2])))
        return 1
    home = os.path.abspath(args.home) if args.home else default_home()
    base = args.base or os.environ.get("SKYNET_AGENT_BASE_URL") or REPO_RAW
    print("Installing the SkyNet research agent into %s" % home)
    try:
        os.makedirs(home, exist_ok=True)
        rel = install(home, base)
        if args.no_shim:
            hint = 'Run it as:  "%s" "%s" status' % (sys.executable, os.path.join(home, "launcher.py"))
        else:
            _, hint = write_shim(home, args.bin_dir)
    except (InstallError, OSError, subprocess.SubprocessError) as e:
        print("Installation failed: %s" % e)
        return 1
    print("Installed version %s." % rel["version"])
    print(hint)
    print("")
    print("Next steps:")
    print("  1. skynet-agent selftest --online    check that everything works")
    print("  2. skynet-agent github               check the GitHub login used to publish results")
    print("  3. skynet-agent run                  start working (Ctrl+C stops it)")
    print("  4. skynet-agent autostart enable     optional: start when you log in")
    print("Nothing runs until you start it. No rewards are provided at this stage.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
