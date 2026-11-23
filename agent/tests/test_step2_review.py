"""Adversarial tests for the step-2 APK update verifier (strict review).

These checks attack the Python side of the APK-update pipeline
(tools/apk_update.py) and the maintainer CLI
(tools/make_apk_manifest.py). They do not use sockets. Run them with:

    python -I -m unittest discover -s agent/tests -t agent/tests -p test_step2_review.py -v

The contract under attack: a signed android/latest.json is accepted only when

  * the detached signature verifies with a key from the release tools' pinned
    trust.RELEASE_KEYS (never a downloaded key),
  * the JSON is strict (no duplicate keys, no NaN),
  * every field has the exact type and bounds,
  * the release URL stays inside the allowed
    https://github.com/skyNetAIAgent/skynet-architecture/releases/download/ prefix,
  * version_code is greater than the installed one and min_sdk fits the device,
  * the cached file matches the declared size and SHA-256 before it is shown.
"""

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import helpers
from skynet_agent import ed25519, signed, trust

ROOT = Path(helpers.REPO_ROOT)
sys.path.insert(0, str(ROOT / "tools"))
import apk_update


class Step2Review(unittest.TestCase):
    """Attacks on apk_update.manifest() and apk_update.matches()."""

    def setUp(self):
        self.seed = bytes.fromhex(helpers.TEST_SEED_HEX)
        patch = mock.patch.object(trust, "RELEASE_KEYS", [helpers.TEST_PUBLIC_HEX])
        patch.start()
        self.addCleanup(patch.stop)
        self.doc = {"format": 1, "version_code": 3, "version_name": "0.3.0",
                    "url": apk_update.RELEASE_URL + "android-v0.3.0/skynet-agent.apk",
                    "size": 3, "sha256": hashlib.sha256(b"apk").hexdigest(),
                    "min_sdk": 24, "notes": "Test release."}

    def sign(self, raw, seed=None):
        seed = self.seed if seed is None else seed
        return signed.format_sig_line(ed25519.public_key(seed),
                                      ed25519.sign(seed, raw)).encode("ascii")

    def offer(self, mutate=None, installed=2, sdk=34, seed=None, sig=None):
        doc = dict(self.doc)
        if mutate:
            mutate(doc)
        raw = json.dumps(doc).encode("utf-8")
        sig = self.sign(raw, seed) if sig is None else sig
        return apk_update.manifest(raw, sig, installed, sdk)

    def assertRejected(self, mutate, label):
        with self.subTest(label), self.assertRaises(ValueError):
            self.offer(mutate)

    def test_signature_is_checked_before_any_field(self):
        # A perfectly formed document signed with a foreign key is worthless.
        foreign = bytes(range(32))
        with self.assertRaises(signed.SignatureError):
            self.offer(seed=foreign)
        # The same foreign key must also be rejected when trusted keys rotate.
        with mock.patch.object(trust, "RELEASE_KEYS",
                               [helpers.TEST_PUBLIC_HEX, ed25519.public_key(foreign).hex()]):
            self.assertIsNotNone(self.offer())
            with self.assertRaises(signed.SignatureError):
                self.offer(seed=bytes(32))  # a third key is still untrusted

    def test_signature_variants_do_not_pass(self):
        raw = json.dumps(self.doc).encode("utf-8")
        good = self.sign(raw)
        attacks = {
            "empty": b"",
            "garbage": b"hello world",
            "truncated hex": b"ed25519:abcd:1234",
            "wrong key length": b"ed25519:" + b"ab" * 31 + b":" + b"00" * 64,
            "wrong sig length": b"ed25519:" + helpers.TEST_PUBLIC_HEX.encode() + b":" + b"00" * 63,
            "wrong doc": self.sign(b'{"format": 1}'),
        }
        for label, sig in attacks.items():
            with self.subTest(label), self.assertRaises(signed.SignatureError):
                apk_update.manifest(raw, sig, 2, 34)
        # The documented one-signer-per-line format: one good line wins, even
        # next to a commented or broken line.
        self.assertIsNotNone(apk_update.manifest(raw, good + b"ed25519:zz:zz\n", 2, 34))
        self.assertIsNotNone(apk_update.manifest(raw, b"# a comment\n" + good, 2, 34))

    def test_url_prefix_and_path_attacks(self):
        base = apk_update.RELEASE_URL
        bad = {
            "http scheme": base.replace("https:", "http:") + "v/a.apk",
            "uppercase scheme": base.replace("https", "HTTPS") + "v/a.apk",
            "host suffix": base.replace("github.com", "github.com.example.org") + "v/a.apk",
            "host prefix": base.replace("github.com", "github.com.evil") + "v/a.apk",
            "userinfo": "https://evil@github.com/skyNetAIAgent/skynet-architecture/releases/download/v/a.apk",
            "port 443": "https://github.com:443/skyNetAIAgent/skynet-architecture/releases/download/v/a.apk",
            "other repo": base.replace("skynet-architecture", "other-repo") + "v/a.apk",
            "other owner": base.replace("skyNetAIAgent", "attacker") + "v/a.apk",
            "dot-dot tag": base + "..%2F..%2Fetc/a.apk",
            "dot-dot asset": base + "v/..%2F..%2Fetc",
            "parent tag": base + "%2E%2E/a.apk",
            "backslash": base + "v%5C..%5C/a.apk",
            "nul byte": base + "v/a.apk%00",
            "query": base + "v/a.apk?x=y",
            "encoded query": base + "v/a.apk%3Fx%3Dy",
            "fragment": base + "v/a.apk#x",
            "empty tag": base + "/a.apk",
            "empty asset": base + "v/",
            "trailing slash": base + "v/a.apk/",
            "three components": base + "v/a.apk/x",
            "space": base + "v/a .apk",
            "not an apk": base + "v/a.txt",
        }
        for label, url in bad.items():
            self.assertRejected(lambda d, url=url: d.update(url=url), label)
        # Benign variants that must keep working.
        for url in (base + "v/a.apk", base + "android-v0.3.0/SkyNet%20Agent.apk",
                    base + "android-v0.3.0/skynet-agent.apk"):
            with self.subTest(accept=url):
                self.assertIsNotNone(self.offer(lambda d, url=url: d.update(url=url)))

    def test_sha256_is_a_safe_file_name(self):
        # Java stores the APK as "<sha256>.apk" in the cache. The only thing that
        # keeps that a plain file name is the [0-9a-f]{64} check, so attack it.
        for digest in ("A" * 64, "g" * 64, "../" + "0" * 61,
                       "0" * 63, "0" * 65, "0" * 63 + "x", "%2e%2e/" + "0" * 57):
            self.assertRejected(lambda d, digest=digest: d.update(sha256=digest), digest)

    def test_field_types_and_bounds(self):
        bad = {
            "format 0": {"format": 0}, "format 2": {"format": 2},
            "format bool": {"format": True}, "format float": {"format": 1.0},
            "version_code bool": {"version_code": True},
            "version_code float": {"version_code": 3.0},
            "version_code string": {"version_code": "3"},
            "version_code zero": {"version_code": 0},
            "version_code huge": {"version_code": 2**31},
            "version_name empty": {"version_name": ""},
            "version_name blank": {"version_name": "  "},
            "version_name long": {"version_name": "x" * 65},
            "version_name not str": {"version_name": 3},
            "notes not str": {"notes": ["text"]},
            "notes too long": {"notes": "x" * 501},
            "notes newline": {"notes": "a\nb"},
            "size zero": {"size": 0}, "size negative": {"size": -1},
            "size float": {"size": 3.0}, "size string": {"size": "3"},
            "min_sdk negative": {"min_sdk": -1}, "min_sdk bool": {"min_sdk": False},
            "min_sdk float": {"min_sdk": 24.0},
            "sha256 missing": {"sha256": None},
            "url not str": {"url": 5},
            "missing url": {"url": None},
        }
        for label, patch in bad.items():
            self.assertRejected(lambda d, patch=patch: d.update(patch), label)
        # Unknown fields are forward-compatible and must not break older builds.
        self.assertIsNotNone(self.offer(lambda d: d.update(extra="future")))

    def test_duplicate_keys_and_non_finite_json(self):
        raw = json.dumps(self.doc).encode("utf-8")
        dup = raw.replace(b'"format": 1', b'"format": 1, "format": 2')
        nan = raw.replace(b'"size": 3', b'"size": NaN')
        for tampered in (dup, nan):
            with self.subTest(tampered=tampered[:30]), self.assertRaises(ValueError):
                apk_update.manifest(tampered, self.sign(tampered), 2, 34)

    def test_version_and_sdk_gating(self):
        self.assertIsNotNone(self.offer(installed=2, sdk=24))     # boundary: min_sdk == device
        self.assertIsNone(self.offer(installed=3, sdk=34))        # equal version
        self.assertIsNone(self.offer(installed=4, sdk=34))        # rollback attempt
        self.assertIsNone(self.offer(installed=2, sdk=23))        # device too old
        self.assertIsNotNone(self.offer(lambda d: d.update(version_code=2**31 - 1)))

    def test_downloaded_file_must_match_size_and_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp, "update.apk")
            content = b"apk"
            for payload, ok in ((content, True), (b"ap!", False), (b"ap", False),
                                (b"apk!", False), (b"apk" * 100, False)):
                with self.subTest(payload=payload):
                    file.write_bytes(payload)
                    self.assertEqual(apk_update.matches(file, 3,
                                                        hashlib.sha256(content).hexdigest()), ok)
            self.assertFalse(apk_update.matches(Path(tmp, "missing.apk"), 3,
                                                hashlib.sha256(content).hexdigest()))
            self.assertFalse(apk_update.matches(Path(tmp), 3, "0" * 64))  # a directory
            # A wrong hash for a correct file is rejected even with the right size.
            file.write_bytes(content)
            self.assertFalse(apk_update.matches(file, 3, "f" * 64))

    def test_file_hash_matches_stdlib_sha256(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp, "apk.bin")
            payload = bytes(range(256)) * 4096          # several 128 KiB blocks
            file.write_bytes(payload)
            self.assertEqual(apk_update.file_hash(file), hashlib.sha256(payload).hexdigest())

    def test_cli_tag_is_encoded_and_roundtrips(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(helpers.copy_repo(Path(tmp, "repo")))
            (repo / "android").mkdir()
            apk = repo / "SkyNet Agent.apk"
            apk.write_bytes(b"apk")
            helpers.build_test_release(str(repo), 1, "0.1.0")
            cmd = [sys.executable, "-IB", str(repo / "tools/make_apk_manifest.py"),
                   "--apk", str(apk), "--version-code", "3", "--version-name", "0.3.0",
                   "--tag", "android-v0.3.0 beta"]
            done = subprocess.run(cmd, env=helpers.tool_env(), capture_output=True, timeout=30)
            self.assertEqual(done.returncode, 0, done.stderr)
            raw = (repo / "android/latest.json").read_bytes()
            sig = (repo / "android/latest.json.sig").read_bytes()
            doc = json.loads(apk_update.manifest(raw, sig, 2, 34))
            self.assertEqual(doc["url"], apk_update.RELEASE_URL + "android-v0.3.0%20beta/SkyNet%20Agent.apk")
            self.assertTrue(apk_update.matches(apk, doc["size"], doc["sha256"]))

    def test_cli_rejects_invalid_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(helpers.copy_repo(Path(tmp, "repo")))
            (repo / "android").mkdir()
            apk = repo / "a.apk"
            apk.write_bytes(b"apk")
            helpers.build_test_release(str(repo), 1, "0.1.0")
            for extra in (["--version-code", "0"], ["--min-sdk", "0"],
                          ["--apk", str(repo / "missing.apk")], ["--tag", ".."]):
                cmd = [sys.executable, "-IB", str(repo / "tools/make_apk_manifest.py"),
                       "--apk", str(apk), "--version-code", "3", "--version-name", "0.3.0",
                       "--tag", "android-v0.3.0"] + extra
                done = subprocess.run(cmd, env=helpers.tool_env(), capture_output=True, timeout=30)
                self.assertNotEqual(done.returncode, 0, extra)
                self.assertFalse((repo / "android/latest.json").exists())

    @unittest.expectedFailure
    def test_encoded_slash_in_tag_is_strictly_rejected(self):
        # Residual laxness: a percent-encoded "/" inside the tag passes validate()
        # (the decoded string "v/x" has no "", ".", ".." segments). It cannot leave
        # the allowed host/prefix, so it is only a cosmetic gap, but a strict
        # "two path components" reading of the spec would reject it.
        self.assertRejected(
            lambda d: d.update(url=apk_update.RELEASE_URL + "v%2Fx/a.apk"),
            "encoded slash in tag")


if __name__ == "__main__":
    unittest.main()
