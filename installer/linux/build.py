"""Build a self-extracting installer from locally authenticated Go assets."""

import argparse
import base64
import gzip
from pathlib import Path
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import desktop_release

MARKER = b"# build.py inserts the offline payload here."


def build(output, assets):
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as tmp:
        tmp = Path(tmp)
        bundle = tmp / "bundle"
        for arch in ("amd64", "arm64", "arm"):
            desktop_release.stage(assets, bundle / arch, "linux-" + arch)
        archive = tmp / "bundle.tar.gz"
        with archive.open("wb") as out, gzip.GzipFile(fileobj=out, filename="", mode="wb", mtime=0) as gz:
            with tarfile.open(fileobj=gz, mode="w|", format=tarfile.USTAR_FORMAT) as tar:
                for path in sorted(bundle.rglob("*")):
                    if path.is_file():
                        info = tarfile.TarInfo(path.relative_to(tmp).as_posix())
                        info.size = path.stat().st_size
                        info.mode = 0o700 if path.name == "skynet-agent" else 0o600
                        with path.open("rb") as src:
                            tar.addfile(info, src)
        before, after = (ROOT / "agent/install.sh").read_bytes().split(MARKER)
        script = tmp / "setup.sh"
        with script.open("wb") as out, archive.open("rb") as src:
            out.write(before + b"base64 -d > \"$tmp/bundle.tgz\" <<'PAYLOAD'\n")
            base64.encode(src, out)
            out.write(b'PAYLOAD\ntar -xzf "$tmp/bundle.tgz" -C "$tmp"\n' + after)
        script.chmod(0o755)
        script.replace(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("skynet-agent-install.sh"))
    parser.add_argument("--dir", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    build(args.output.resolve(), args.dir)
