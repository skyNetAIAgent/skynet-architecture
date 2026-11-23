"""Exercise the APK manifest release tools without sockets."""

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


class ApkManifest(unittest.TestCase):
    def setUp(self):
        self.seed = bytes.fromhex(helpers.TEST_SEED_HEX)
        patch = mock.patch.object(trust, "RELEASE_KEYS", [helpers.TEST_PUBLIC_HEX])
        patch.start()
        self.addCleanup(patch.stop)
        self.doc = {"format": 1, "version_code": 3, "version_name": "0.3.0",
                    "url": apk_update.RELEASE_URL + "android-v0.3.0/skynet-agent.apk",
                    "size": 3, "sha256": hashlib.sha256(b"apk").hexdigest(),
                    "min_sdk": 24, "notes": "Test release."}

    def sign(self, raw, seed):
        return signed.format_sig_line(ed25519.public_key(seed), ed25519.sign(seed, raw)).encode()

    def check(self, installed=2, sdk=34):
        raw = json.dumps(self.doc).encode()
        return apk_update.manifest(raw, self.sign(raw, self.seed), installed, sdk)

    def test_only_a_newer_compatible_release_is_offered(self):
        self.assertEqual(json.loads(self.check(sdk=24)), self.doc)
        self.assertIsNone(self.check(installed=3))
        self.assertIsNone(self.check(installed=4))
        self.assertIsNone(self.check(sdk=23))

    def test_manifest_tampering_and_foreign_key(self):
        raw = json.dumps(self.doc).encode()
        with self.assertRaises(signed.SignatureError):
            apk_update.manifest(raw + b" ", self.sign(raw, self.seed), 2, 34)
        with self.assertRaises(signed.SignatureError):
            apk_update.manifest(raw, self.sign(raw, bytes(32)), 2, 34)

    def test_release_url(self):
        base = apk_update.RELEASE_URL
        for url in (self.doc["url"].replace("https:", "http:"), "https://example.org/v/a.apk",
                    base.replace("github.com", "github.com.example.org") + "v/a.apk",
                    base.replace("skynet-architecture", "another-repo") + "v/a.apk",
                    base + "../a.apk", base + "%2e%2e/a.apk", base + "v/a.apk?next=x",
                    base + "v%5Cfoo/a.apk", base + "v%2F..%2F../a.apk"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                self.doc["url"] = url
                self.check()

    def test_manifest_field_types_and_duplicate_keys(self):
        for key, value in (("format", True), ("version_code", "3"), ("version_name", ""),
                           ("size", 0), ("sha256", "z" * 64), ("min_sdk", 24.5), ("notes", [])):
            with self.subTest(key=key), mock.patch.dict(self.doc, {key: value}), self.assertRaises(ValueError):
                self.check()
        raw = json.dumps(self.doc).replace('{"format":', '{"format": 2, "format":').encode()
        with self.assertRaises(ValueError):
            apk_update.manifest(raw, self.sign(raw, self.seed), 2, 34)

    def test_downloaded_and_cached_file_integrity(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp, "update.apk")
            for content, valid in ((b"apk", True), (b"ap!", False), (b"ap", False), (b"apk!", False)):
                with self.subTest(content=content):
                    file.write_bytes(content)
                    self.assertEqual(apk_update.matches(file, self.doc["size"], self.doc["sha256"]), valid)
            self.assertFalse(apk_update.matches(file, 4, "0" * 64))

    def test_maintainer_cli_matches_the_app(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(helpers.copy_repo(Path(tmp, "repo")))
            (repo / "android").mkdir()
            apk = repo / "SkyNet Agent.apk"
            apk.write_bytes(b"apk")
            cmd = [sys.executable, "-IB", str(repo / "tools/make_apk_manifest.py"), "--apk", str(apk),
                   "--version-code", "3", "--version-name", "0.3.0", "--tag", "android-v0.3.0"]
            def run():
                return subprocess.run(cmd, env=helpers.tool_env(), capture_output=True, timeout=30)
            raw = repo / "android/latest.json"
            self.assertNotEqual(run().returncode, 0)  # test key is not pinned in the original repo
            self.assertFalse(raw.exists())
            helpers.build_test_release(str(repo), 1, "0.1.0")
            done = run()
            self.assertEqual(done.returncode, 0, done.stderr)
            sig = (repo / "android/latest.json.sig").read_bytes()
            doc = json.loads(apk_update.manifest(raw.read_bytes(), sig, 2, 34))
            self.assertEqual(doc["url"], apk_update.RELEASE_URL + "android-v0.3.0/SkyNet%20Agent.apk")
            self.assertEqual((doc["version_code"], doc["version_name"], doc["min_sdk"]), (3, "0.3.0", 24))
            self.assertTrue(apk_update.matches(apk, doc["size"], doc["sha256"]))
