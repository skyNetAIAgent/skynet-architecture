"""Stage the signed native release for Inno Setup."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from desktop_release import stage

if __name__ == "__main__":
    build, assets, arch = sys.argv[1:]
    stage(Path(assets), Path(build, "release"), "windows-" + arch)
