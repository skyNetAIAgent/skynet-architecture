"""Verify the local release before running any candidate code."""

import contextlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock

import helpers
import install
from skynet_agent import ed25519, signed


class LocalInstall(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.bundle = Path(tmp.name, "release")
        self.home = Path(tmp.name, "home")
        agent = Path(helpers.AGENT_DIR)
        self.rel = json.loads((agent / "release.json").read_bytes())
        for name in ["release.json", "release.json.sig", *self.rel["files"]]:
            target = self.bundle / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(agent / name, target)
        self.args = ["--from-dir", str(self.bundle), "--home", str(self.home), "--no-shim"]
        network = mock.patch.object(install, "fetch", side_effect=AssertionError("unexpected download"))
        network.start()
        self.addCleanup(network.stop)

    def run_cli(self, *options):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            return install.main(self.args + list(options)), output.getvalue()

    def rejected(self, reason):
        with mock.patch.object(install, "check_candidate") as check:
            code, text = self.run_cli()
        self.assertNotEqual(code, 0)
        self.assertIn(reason, text)
        check.assert_not_called()

    def test_signed_local_install(self):
        code, text = self.run_cli()
        self.assertEqual(code, 0, text)
        self.assertEqual(json.loads((self.home / "current.json").read_bytes())["seq"], self.rel["seq"])

    def test_changed_file(self):
        path = self.bundle / "launcher.py"
        data = path.read_bytes()
        path.write_bytes(b"!" + data[1:])
        self.rejected("changed file")

    def test_foreign_signature(self):
        seed = bytes.fromhex(helpers.TEST_SEED_HEX)
        raw = (self.bundle / "release.json").read_bytes()
        signature = signed.format_sig_line(ed25519.public_key(seed), ed25519.sign(seed, raw))
        (self.bundle / "release.json.sig").write_bytes(signature.encode("ascii"))
        self.rejected("no valid signature")

    def test_extra_file_even_on_reinstall(self):
        self.assertEqual(self.run_cli()[0], 0)
        (self.bundle / "skynet_agent" / "extra.py").touch()
        self.rejected("unexpected entry")

    def test_lower_sequence(self):
        self.home.mkdir()
        current = self.home / "current.json"
        pointer = json.dumps({"seq": self.rel["seq"] + 1}).encode()
        current.write_bytes(pointer)
        self.rejected("older than")
        with mock.patch.object(install, "check_candidate") as check:
            self.assertEqual(self.run_cli("--keep-newer")[0], 0)
            check.assert_not_called()
        self.assertEqual(current.read_bytes(), pointer)
        self.assertFalse((self.home / "versions").exists())

    def test_floor_only_refuses_even_with_keep_newer(self):
        self.home.mkdir()
        (self.home / "max_seq.json").write_text(str(self.rel["seq"] + 1))
        self.assertNotEqual(self.run_cli("--keep-newer")[0], 0)
        self.assertFalse((self.home / "current.json").exists())
