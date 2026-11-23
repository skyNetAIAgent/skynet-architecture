"""Stage the authenticated agent files for Inno Setup in a fresh build directory."""

from pathlib import Path
import runpy
import sys
import tempfile


def stage(build):
    agent = Path(__file__).resolve().parents[2] / "agent"
    installer = runpy.run_path(str(agent / "install.py"))
    get = installer["local_reader"](agent)
    release, raw, sig = installer["read_release"](get)
    build.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=build) as tmp:
        version = installer["prepare"](tmp, release, raw, sig, get)
        (Path(tmp) / version).rename(build / "release")


if __name__ == "__main__":
    stage(Path(sys.argv[1]))
