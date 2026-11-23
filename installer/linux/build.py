"""Build the self-extracting Linux installer from a verified local agent release."""

import argparse
import base64
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import runpy
import shutil
import tarfile
import tempfile
import urllib.request

HERE = Path(__file__).resolve().parent
AGENT = HERE.parents[1] / "agent"
MARKER = b"# build.py inserts the offline payload here."
ARCHES = ("x86_64", "aarch64")


def runtimes(lock, stage, local):
    for arch in ARCHES:
        key = arch + "_sha256"
        digest = lock[key]
        if digest is None:
            digest = os.environ.get("SKYNET_PYTHON_SHA256_" + arch.upper())
            if not digest:
                print("No Python pin for %s. This build requires system Python on that architecture." % arch)
                continue
        if not re.fullmatch("[0-9a-f]{64}", digest):
            raise ValueError("Invalid SHA-256 for " + arch)
        name = "cpython-%s+%s-%s-unknown-linux-gnu-install_only_stripped.tar.gz" % (
            lock["version"], lock["release"], arch)
        if lock[arch + "_file"] != name or "/" in name or "\\" in name:
            raise ValueError("Invalid Python filename for " + arch)
        archive = stage / name
        if local:
            shutil.copyfile(local / name, archive)
        else:
            url = "https://github.com/astral-sh/python-build-standalone/releases/download/%s/%s"
            with urllib.request.urlopen(url % (lock["release"], name), timeout=120) as src, archive.open("wb") as out:
                shutil.copyfileobj(src, out)
        if hashlib.sha256(archive.read_bytes()).hexdigest() != digest:
            raise ValueError("Python SHA-256 mismatch: " + name)
        lock[key] = digest


def build(output, local=None):
    api = runpy.run_path(str(AGENT / "install.py"))
    get = api["local_reader"](AGENT)
    manifest, raw, sig = api["read_release"](get)
    with tempfile.TemporaryDirectory(dir=output.parent) as tmp:
        root = Path(tmp)
        stage = root / "bundle"
        stage.mkdir()
        version = api["prepare"](tmp, manifest, raw, sig, get)
        (root / version).rename(stage / "release")
        for name in ("install.py", "linux_setup.py", "LICENSE"):
            shutil.copyfile(AGENT / name, stage / name)
        lock = json.loads((HERE / "python.lock").read_bytes())
        runtimes(lock, stage, local)
        (stage / "python.lock").write_bytes((json.dumps(lock, indent=2) + "\n").encode("ascii"))

        archive = root / "bundle.tar.gz"
        with archive.open("wb") as out, gzip.GzipFile(filename="", fileobj=out, mode="wb", mtime=0) as gz:
            with tarfile.open(fileobj=gz, mode="w|", format=tarfile.USTAR_FORMAT) as tar:
                for path in sorted(stage.rglob("*")):
                    if path.is_file():
                        info = tarfile.TarInfo(path.relative_to(stage).as_posix())
                        info.size = path.stat().st_size
                        with path.open("rb") as src:
                            tar.addfile(info, src)
        before, after = (AGENT / "install.sh").read_bytes().split(MARKER)
        script = root / "setup.sh"
        with script.open("wb") as out, archive.open("rb") as src:
            out.write(before + b"base64 -d > \"$tmp/bundle.tar.gz\" <<'SKYNET_PAYLOAD'\n")
            base64.encode(src, out)
            out.write(b'SKYNET_PAYLOAD\ntar -xzf "$tmp/bundle.tar.gz" -C "$tmp"\n' + after)
        script.chmod(0o755)
        script.replace(output)
    print("Built %s with signed agent %s." % (output, manifest["version"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "skynet-agent-install.sh")
    parser.add_argument("--runtime-dir", type=Path, help="read pinned archives from this directory")
    args = parser.parse_args()
    build(args.output.resolve(), args.runtime_dir)
