"""Build deterministic desktop release binaries with a local Go toolchain."""

import argparse
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ("windows-amd64", "windows-arm64", "linux-amd64", "linux-arm64", "linux-arm")


def build(directory, seq, version, go="go"):
    if not 1 <= seq <= 999999999 or not re.fullmatch(r"[0-9]{1,4}(\.[0-9]{1,4}){2}", version):
        raise ValueError("invalid build metadata")
    directory.mkdir(parents=True, exist_ok=True)
    for target in TARGETS:
        system, arch = target.split("-")
        env = dict(os.environ, GOOS=system, GOARCH=arch, CGO_ENABLED="0", GOTOOLCHAIN="local",
                   GOFLAGS="-mod=mod", GOPROXY="off", GOARM="7", GOAMD64="v1", GOARM64="v8.0",
                   GOEXPERIMENT="", GOWORK="off")
        name = "skynet-agent-" + target + (".exe" if system == "windows" else "")
        subprocess.run([go, "build", "-trimpath", "-buildvcs=false", "-ldflags",
                        f"-s -w -X main.version={version} -X main.releaseSeq={seq}",
                        "-o", str((directory / name).resolve()), "./cmd/skynet-agent"],
                       cwd=ROOT / "agent-go", env=env, check=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", type=Path, required=True)
    parser.add_argument("--seq", type=int, required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--go", default="go")
    args = parser.parse_args()
    build(args.dir, args.seq, args.version, args.go)
