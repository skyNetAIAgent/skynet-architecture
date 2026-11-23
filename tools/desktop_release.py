"""Pack or stage release assets after authenticating their exact bytes."""

from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "agent"))
from skynet_agent import bridge, ed25519, signed, trust


def asset(key):
    return "skynet-agent-" + key + (".exe" if key.startswith("windows") else "")


def build(root, directory, seq, version, tag, seed, through, reason):
    if not tag or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,100}", tag):
        raise ValueError("invalid immutable release tag")
    targets = {}
    for key in bridge.TARGETS:
        p = Path(directory, asset(key))
        if not p.exists():
            continue
        if p.is_symlink() or not p.is_file() or not 0 < p.stat().st_size <= bridge.LIMIT:
            raise ValueError("invalid asset " + str(p))
        targets[key] = dict(bridge.meta(p.read_bytes()), name=bridge.binary(key),
                            url=f"{trust.WEB_BASE}/releases/download/{tag}/{p.name}")
    rel = dict(format=2, seq=seq, version=version, min_bridge_seq=6, targets=targets,
               compat_files={k: bridge.meta(v) for k, v in bridge.COMPAT.items()})
    if through is not None:
        rel["halt"] = {"through_seq": through, "reason": reason}
    bridge.validate(rel)
    public = ed25519.public_key(seed)
    raw = (json.dumps(rel, sort_keys=True, indent=1) + "\n").encode()
    signature = signed.format_sig_line(public, ed25519.sign(seed, raw)).encode("ascii")
    signed.verify_detached(raw, signature)
    out = Path(root, "agent/v2")
    out.mkdir(exist_ok=True)
    (out / "release.json").write_bytes(raw)
    (out / "release.json.sig").write_bytes(signature)
    return 0


def stage(directory, dest, key):
    channel = ROOT / "agent/v2"
    raw = (channel / "release.json").read_bytes()
    signature = (channel / "release.json.sig").read_bytes()
    signed.verify_detached(raw, signature)
    rel = signed.strict_json_loads(raw)
    bridge.validate(rel)
    t = rel["targets"][key]
    p = Path(directory, asset(key))
    if p.is_symlink() or not p.is_file() or p.stat().st_size != t["size"]:
        raise ValueError("wrong asset size or type")
    data = p.read_bytes()
    if bridge.meta(data)["sha256"] != t["sha256"]:
        raise ValueError("wrong asset SHA-256")
    dest.mkdir(parents=True)
    (dest / t["name"]).write_bytes(data)
    (dest / "release.json").write_bytes(raw)
    (dest / "release.json.sig").write_bytes(signature)
    return rel
