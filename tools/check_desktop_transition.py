"""Exercise the live 0.3.0 supervisor against a file-backed signed test channel."""

import argparse
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "agent/tests"))
sys.path.insert(0, str(ROOT / "tools"))
import helpers
import desktop_release
from skynet_agent import bridge, trust

# Replace the work loop with one local poll. The original supervisor and both updaters run.
POLL = """
import os
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from skynet_agent import cli
if not hasattr(cli, "updater"):
    raise SystemExit(cli.main(["run"]))
from skynet_agent import updater, net

def get(url, **kwargs):
    assert url.startswith("https://fixture/")
    return (Path(os.environ["MIRROR"]) / url.removeprefix("https://fixture/")).read_bytes()

net.get = get
net.request = lambda url, **kw: (200, Path(os.environ["ASSET"]).read_bytes(), {})
result = updater.check_and_apply(os.environ["SKYNET_AGENT_HOME"], "https://fixture", {"update": "auto"})
assert result.installed, result.note
raise SystemExit(75)
"""

MAIN = """
package main
import "os"
var version = "1.0.0"
var releaseSeq = "7"
func main() {
    if len(os.Args) < 2 { os.Exit(2) }
    if os.Args[1] == "run" {
        if releaseSeq == "8" {
            f, err := os.OpenFile(os.Getenv("G3_CRASH_LOG"), os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0600)
            if err != nil { os.Exit(2) }
            f.WriteString("crash\\n")
            f.Close()
            os.Exit(23)
        }
        return
    }
    registerUpdateCommands(func(name, help string, run func([]string) int) {
        if name == os.Args[1] { os.Exit(run(os.Args[2:])) }
    })
    os.Exit(2)
}
"""


def build_fixture(temp, go, key):
    module = ROOT / "agent-go"
    test = temp / "cmd"
    test.mkdir()
    path = (module / "go.mod").read_text().split()[1]
    (test / "go.mod").write_text(
        'module transition-test\n\ngo 1.22\n\nrequire %s v0.0.0\nreplace %s => "%s"\n'
        % (path, path, module.as_posix()))
    (test / "main.go").write_text(MAIN)
    shutil.copyfile(module / "cmd/skynet-agent/update_cmds.go", test / "commands.go")
    signer = module / "sig/sig.go"
    pins = temp / "sig.txt"
    pins.write_text(signer.read_text().replace(trust.RELEASE_KEYS[0], helpers.TEST_PUBLIC_HEX))
    service = "run_windows.go" if os.name == "nt" else "service_linux.go"
    stub = temp / "autostart.txt"
    stub.write_text('package autostart\nfunc change(home, action string)(string,error){return "off",nil}\n')
    overlay = temp / "overlay.json"
    overlay.write_text(json.dumps({"Replace": {
        str(signer): str(pins), str(module / "autostart" / service): str(stub)}}))
    assets = temp / "assets"
    assets.mkdir()
    asset = assets / desktop_release.asset(key)
    subprocess.run([go, "build", "-mod=mod", "-buildvcs=false", "-overlay", str(overlay),
                    "-o", str(asset), "."], cwd=test, check=True, timeout=300,
                   env=dict(os.environ, CGO_ENABLED="0", GOPROXY="off", GOTOOLCHAIN="local", GOWORK="off"))
    return asset


def crash_trial(temp, go, key, seed, asset, mirror):
    # A second native release dies three times. Its previous release exits normally.
    home = temp / "trial"
    exe = bridge.binary(key)
    scoped = dict(os.environ, SKYNET_AGENT_HOME=str(home), G3_CRASH_LOG=str(temp / "crashes"),
                  GOTOOLCHAIN="local", GOPROXY="off", CGO_ENABLED="0", GOWORK="off")

    def install(seq):
        bundle = temp / ("bundle-%d" % seq)
        desktop_release.stage(asset.parent, bundle, key)
        candidate = bundle / exe
        candidate.chmod(0o700)
        subprocess.run([str(candidate), "install-bundle", str(bundle), str(home)],
                       env=scoped, timeout=60, check=True)

    with patch.object(desktop_release, "ROOT", mirror), patch.object(trust, "RELEASE_KEYS", [helpers.TEST_PUBLIC_HEX]):
        install(7)
        subprocess.run([go, "build", "-mod=mod", "-buildvcs=false", "-overlay", str(temp / "overlay.json"),
                        "-ldflags", "-X main.releaseSeq=8 -X main.version=1.1.0",
                        "-o", str(asset), "."], cwd=temp / "cmd", env=scoped, check=True, timeout=300)
        desktop_release.build(mirror, asset.parent, 8, "1.1.0", "v1.1.0", seed, None, "")
        install(8)
    subprocess.run([str(home / exe), "launch", "run"], env=scoped, timeout=90, check=True)
    assert (temp / "crashes").read_text().splitlines() == ["crash"] * 3
    assert json.loads((home / "current.json").read_bytes())["seq"] == 7
    assert json.loads((home / "max_seq.json").read_bytes()) == 8
    assert json.loads((home / "bad_seqs.json").read_bytes()) == [8]


def exercise(temp, legacy, go):
    key = bridge.target()
    if key not in bridge.TARGETS:
        raise ValueError("a supported desktop host is required")
    home = temp / "profile"
    asset = build_fixture(temp, go, key)
    old, mirror = temp / "old", temp / "mirror"
    for name in ("agent", "tools"):
        shutil.copytree(legacy / name, old / name)
    helpers.build_test_release(str(old), 5, "0.3.0")
    api = runpy.run_path(str(old / "agent/install.py"))
    get = api["local_reader"](old / "agent")
    with patch.dict(api["install"].__globals__, RELEASE_KEYS=[helpers.TEST_PUBLIC_HEX]):
        rel, raw, sig = api["read_release"](get)
        with api["update_lock"](str(home)):
            relative = api["prepare"](str(home), rel, raw, sig, get)
            api["check_candidate"](str(home), str(home / relative), rel)
            api["switch_version"](str(home), rel, relative)
    launcher = home / "launcher.py"
    assert launcher.read_bytes() == (legacy / "agent/launcher.py").read_bytes()
    helpers.copy_repo(str(mirror))
    helpers.build_test_release(str(mirror), 6, "0.4.0")
    seed = bytes.fromhex(helpers.TEST_SEED_HEX)
    with patch.object(trust, "RELEASE_KEYS", [helpers.TEST_PUBLIC_HEX]):
        desktop_release.build(mirror, asset.parent, 7, "1.0.0", "v1.0.0", seed, None, "")
    poll = temp / "poll.py"
    poll.write_text(POLL)
    real_call = subprocess.call
    calls = 0

    def dispatch(argv, **kwargs):
        nonlocal calls
        calls += 1
        if calls > 5:
            raise AssertionError("unexpected supervisor restart loop")
        if argv[:3] == [sys.executable, "-IB", "-c"]:
            argv = [sys.executable, "-IB", str(poll), argv[4]]
        return real_call(argv, timeout=60, **kwargs)

    queue = home / "outbox/keep"
    queue.parent.mkdir()
    queue.write_bytes(b"existing queue")
    supervisor = runpy.run_path(str(launcher))
    with patch.dict(os.environ, MIRROR=str(mirror), ASSET=str(asset), SKYNET_AGENT_HOME=str(home),
                    SKYNET_AGENT_BACKOFF="0.01"), patch.object(sys, "argv", ["launcher.py", "run"]), \
            patch("subprocess.call", side_effect=dispatch):
        assert supervisor["main"]() == 0
    current = json.loads((home / "current.json").read_bytes())
    assert (current["runtime"], current["seq"], current["previous"]["seq"]) == ("go", 7, 6)
    binary = bridge.binary(key)
    cmd = [str(home / binary), "launch"]
    env = dict(os.environ, SKYNET_AGENT_HOME=str(home))
    subprocess.run(cmd + ["verify-install"], env=env, check=True, timeout=60)
    (home / current["dir"] / binary).unlink()
    subprocess.run(cmd + ["version"], env=env, check=True, timeout=60)
    assert json.loads((home / "bad_seqs.json").read_bytes()) == [7]
    assert json.loads((home / "max_seq.json").read_bytes()) == 7
    assert json.loads((home / "current.json").read_bytes())["seq"] == 6
    assert queue.read_bytes() == b"existing queue"
    crash_trial(temp, go, key, seed, asset, mirror)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--legacy", type=Path, required=True, help="original 0.3.0 repository snapshot")
    parser.add_argument("--go", default="go")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="g3-") as tmp:
        exercise(Path(tmp), args.legacy.resolve(), args.go)
    print("5 -> 6 -> 7 -> 6, cold start, queue, sequence floor and three-crash 8 -> 7 rollback: OK")
