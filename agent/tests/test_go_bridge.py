"""Exercise the bridge without a network connection or a real login registration."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import helpers
from skynet_agent import bridge, ed25519, net, signed, trust, updater


class GoBridge(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.home = tmp.name
        self.binary = b"mock signed binary"
        self.rel = dict(format=2, seq=7, version="1.0.0", min_bridge_seq=6,
                        targets={"linux-amd64": dict(name="skynet-agent", url="https://github.com/test/v7",
                                                     **bridge.meta(self.binary))},
                        compat_files={k: bridge.meta(v) for k, v in bridge.COMPAT.items()})
        for patch in (mock.patch.object(trust, "RELEASE_KEYS", [helpers.TEST_PUBLIC_HEX]),
                      mock.patch.object(bridge, "target", return_value="linux-amd64"),
                      mock.patch.object(updater, "is_installed_layout", return_value=True),
                      mock.patch.object(net, "get", side_effect=self.get)):
            patch.start()
            self.addCleanup(patch.stop)
        self.seed = bytes.fromhex(helpers.TEST_SEED_HEX)

    def get(self, url, **kw):
        if bridge.CHANNEL not in url:
            raise net.NetError("unavailable")
        raw = json.dumps(self.rel).encode()
        if url.endswith(".sig"):
            return signed.format_sig_line(ed25519.public_key(self.seed), ed25519.sign(self.seed, raw)).encode()
        return raw

    def apply(self, mode="auto"):
        return updater.check_and_apply(self.home, "https://test.invalid", {"update": mode})

    def test_authenticated_bootstrap(self):
        calls = []
        def run(args, **kwargs):
            self.assertEqual(Path(args[0]).read_bytes(), self.binary)
            self.assertEqual(kwargs["env"]["SKYNET_AGENT_HOME"], self.home)
            self.assertGreater(kwargs["timeout"], 0)
            calls.append(args[1])
        with mock.patch.object(net, "request", return_value=(200, self.binary, {})), mock.patch.object(bridge.subprocess, "run", run):
            self.assertTrue(self.apply().installed)
        self.assertEqual(calls, ["verify-install", "install-bundle"])

    def test_bad_binary_and_foreign_signature(self):
        with mock.patch.object(net, "request", return_value=(200, b"x", {})), mock.patch.object(bridge.subprocess, "run") as run:
            with self.assertRaises(bridge.Error):
                self.apply()
            run.assert_not_called()
            self.seed = bytes(32)
            with self.assertRaises(signed.SignatureError):
                self.apply()

    def test_no_target_mode_and_halt(self):
        with mock.patch.object(bridge, "install") as install:
            self.assertFalse(self.apply("notify").installed)
            with mock.patch.object(bridge, "target", return_value=None):
                self.assertFalse(self.apply().installed)
            self.rel.update(seq=8, halt=dict(through_seq=7, reason="pause"))
            self.assertEqual(self.apply("off").halt, "pause")
            with mock.patch.object(net, "get", side_effect=net.NetError("offline")):
                self.assertEqual(self.apply().halt, "pause")
            install.assert_not_called()
