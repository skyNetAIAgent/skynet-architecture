#!/usr/bin/env python3
"""Describe the final, signed APK and sign its manifest with the release key."""

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path[:0] = [str(HERE), str(ROOT / "agent"), str(ROOT / "android/app/src/main/python")]

import apk_update
import keytool
from skynet_agent import ed25519, signed


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apk", required=True, type=Path)
    parser.add_argument("--version-code", required=True, type=int)
    parser.add_argument("--version-name", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--min-sdk", type=int, default=24)
    parser.add_argument("--notes", help="short release notes in English")
    parser.add_argument("--key", help="release key file (default: see keytool.py)")
    args = parser.parse_args(argv)
    try:
        doc = {"format": 1, "version_code": args.version_code, "version_name": args.version_name,
               "min_sdk": args.min_sdk, "notes": args.notes or "SkyNet Agent for Android.",
               "url": apk_update.RELEASE_URL + quote(args.tag, safe="") + "/" + quote(args.apk.name),
               "size": args.apk.stat().st_size, "sha256": apk_update.file_hash(args.apk)}
        apk_update.validate(doc)
        raw = (json.dumps(doc, indent=2) + "\n").encode("utf-8")
        seed = keytool.load_seed(args.key)
        sig = signed.format_sig_line(ed25519.public_key(seed), ed25519.sign(seed, raw)).encode("ascii")
        signed.verify_detached(raw, sig)
        for name, data in (("latest.json", raw), ("latest.json.sig", sig)):
            (ROOT / "android" / name).write_bytes(data)
    except (OSError, ValueError, signed.SignatureError) as e:
        parser.exit(1, "Cannot create APK manifest: %s\n" % e)
    print("Signed android/latest.json for %s." % args.apk.name)


if __name__ == "__main__":
    main()
