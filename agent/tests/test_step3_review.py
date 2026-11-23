"""Adversarial review tests for install.py --from-dir (step 3 of stage 0).

These tests attack the local offline installer: tampered files, foreign
signatures, extra entries, junctions, downgrade attempts and paths with
spaces, Cyrillic letters and a percent sign. Every refusal must happen
before any candidate code runs.
"""

import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

import helpers
import install
from skynet_agent import ed25519, signed


class FromDirAttacks(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        base = Path(tmp.name)
        # The strongest realistic paths: spaces, Cyrillic letters, percent sign.
        self.bundle = base / "сборочный пакет 100%"
        self.home = base / "агент дом 100%"
        self.rel = helpers.make_local_bundle(self.bundle)
        keys = mock.patch.object(install, "RELEASE_KEYS", [helpers.TEST_PUBLIC_HEX])
        keys.start()
        self.addCleanup(keys.stop)
        self.args = ["--from-dir", str(self.bundle), "--home", str(self.home), "--bin-dir", str(self.home)]
        network = mock.patch.object(install, "fetch", side_effect=AssertionError("network was used"))
        network.start()
        self.addCleanup(network.stop)

    def run_cli(self, *options):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            code = install.main(self.args + list(options))
        return code, output.getvalue()

    def rejected_without_run(self, fragment):
        with mock.patch.object(install, "check_candidate") as check:
            code, text = self.run_cli()
        self.assertNotEqual(code, 0)
        self.assertIn(fragment, text)
        check.assert_not_called()
        self.assertFalse((self.home / "versions").exists())

    @unittest.skipUnless(os.name == "nt", "the start script for Windows")
    def test_valid_bundle_installs_offline_in_tricky_path(self):
        code, text = self.run_cli()
        self.assertEqual(code, 0, text)
        current = json.loads((self.home / "current.json").read_bytes())
        self.assertEqual(current["seq"], self.rel["seq"])
        self.assertTrue((self.home / "launcher.py").is_file())
        shim = (self.home / "skynet-agent.cmd").read_text()
        self.assertIn('"%~dp0launcher.py"', shim)

    def test_tampered_file_same_size_rejected(self):
        path = self.bundle / "launcher.py"
        data = path.read_bytes()
        path.write_bytes(b"!" + data[1:])
        self.rejected_without_run("changed file")

    def test_tampered_file_grown_rejected(self):
        path = self.bundle / "launcher.py"
        path.write_bytes(path.read_bytes() + b"!")
        self.rejected_without_run("changed file")

    def test_foreign_signature_rejected(self):
        seed = bytes(32)
        raw = (self.bundle / "release.json").read_bytes()
        signature = signed.format_sig_line(ed25519.public_key(seed), ed25519.sign(seed, raw))
        (self.bundle / "release.json.sig").write_bytes(signature.encode("ascii"))
        self.rejected_without_run("no valid signature")

    def test_modified_manifest_rejected_before_json(self):
        # A byte flip in release.json also breaks the signature: nothing may run.
        path = self.bundle / "release.json"
        path.write_bytes(b"!" + path.read_bytes()[1:])
        self.rejected_without_run("no valid signature")

    def test_extra_file_rejected_even_after_install(self):
        self.assertEqual(self.run_cli()[0], 0)
        (self.bundle / "skynet_agent" / "extra.py").touch()
        with mock.patch.object(install, "check_candidate") as check:
            code, text = self.run_cli()
        self.assertNotEqual(code, 0)
        self.assertIn("unexpected entry", text)
        check.assert_not_called()

    def test_extra_top_level_file_rejected(self):
        (self.bundle / "README.txt").touch()
        self.rejected_without_run("unexpected entry")

    def test_missing_file_rejected(self):
        (self.bundle / "launcher.py").unlink()
        self.rejected_without_run("missing file")

    def test_missing_signature_rejected(self):
        (self.bundle / "release.json.sig").unlink()
        with mock.patch.object(install, "check_candidate") as check:
            code, text = self.run_cli()
        self.assertNotEqual(code, 0)
        check.assert_not_called()

    def test_junction_rejected(self):
        target = self.bundle / "skynet_agent" / "junk"
        target.mkdir(parents=True)
        try:
            done = subprocess.run(["cmd", "/d", "/c", "mklink", "/J",
                                   str(self.bundle / "junk"), str(target)],
                                  capture_output=True, timeout=60)
        except (OSError, subprocess.SubprocessError):
            self.skipTest("cannot create junctions here")
        if done.returncode != 0:
            self.skipTest("cannot create junctions here: %s" % done.stderr.decode("utf-8", "replace"))
        self.rejected_without_run("unexpected entry")

    def test_downgrade_without_keep_newer(self):
        self.home.mkdir()
        (self.home / "current.json").write_text(json.dumps({"seq": self.rel["seq"] + 1}))
        self.rejected_without_run("older than")
        self.assertTrue((self.home / "current.json").exists())

    @unittest.skipUnless(os.name == "nt", "the start script for Windows")
    def test_downgrade_with_keep_newer_keeps_everything(self):
        self.home.mkdir()
        launcher = self.home / "launcher.py"
        launcher.write_text("# keep this launcher\n")
        current = json.dumps({"seq": self.rel["seq"] + 1, "version": "9.9.9",
                              "dir": "versions/9-9.9.9"})
        (self.home / "current.json").write_text(current)
        with mock.patch.object(install, "check_candidate") as check:
            code, text = self.run_cli("--keep-newer")
            check.assert_not_called()
        self.assertEqual(code, 0, text)
        self.assertEqual((self.home / "current.json").read_text(), current)
        self.assertEqual(launcher.read_text(), "# keep this launcher\n")
        self.assertFalse((self.home / "versions").exists())
        self.assertIn('"%~dp0launcher.py"', (self.home / "skynet-agent.cmd").read_text())

    def test_floor_refuses_even_with_keep_newer(self):
        self.home.mkdir()
        (self.home / "max_seq.json").write_text(str(self.rel["seq"] + 1))
        self.rejected_without_run("older than")
        self.assertFalse((self.home / "current.json").exists())

    @unittest.skipUnless(os.name == "nt", "the start script for Windows")
    def test_shim_uses_bundled_python_when_installed_with_it(self):
        self.home.mkdir()
        fake = str(Path(self.home, "python", "python.exe"))
        with mock.patch.object(install.sys, "executable", fake):
            path, _ = install.write_shim(str(self.home))
        content = Path(path).read_text()
        self.assertIn('"%~dp0python\\python.exe" -I "%~dp0launcher.py"', content)
        self.assertNotIn(fake, content)


if __name__ == "__main__":
    unittest.main()
