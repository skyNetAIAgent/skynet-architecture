"""Repository outages, signed task cache and retry timing. No sockets are opened."""

import argparse
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock

import helpers
from skynet_agent import cli, config, ed25519, net, signed, tasks, trust, updater


class OfflineWork(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        for patch in (mock.patch.dict(os.environ, SKYNET_AGENT_HOME=tmp.name, SKYNET_AGENT_SUBMIT_VIA="net"),
                      mock.patch.object(trust, "RELEASE_KEYS", [helpers.TEST_PUBLIC_HEX])):
            patch.start()
            self.addCleanup(patch.stop)
        config.ensure_dirs()
        config.save_config(dict(config.load_config(), run_on_battery=True))
        self.args = argparse.Namespace(once=True, no_submit=True, no_update=True)
        self.index = {"format": 1, "seq": 3, "expires": "2030-01-01", "tasks": [
            {"id": "test", "kernel": "selftest", "kernel_version": 1, "units": 1, "params": {"rounds": 2}}]}

    def connected_poll(self, state):
        raw = json.dumps(self.index).encode()
        seed = bytes.fromhex(helpers.TEST_SEED_HEX)
        sig = signed.format_sig_line(bytes.fromhex(helpers.TEST_PUBLIC_HEX), ed25519.sign(seed, raw))
        def get(url, **kwargs):
            if url.endswith(tasks.INDEX_PATH):
                return raw
            if url.endswith(tasks.INDEX_PATH + ".sig"):
                return sig.encode()
            return b"{}"
        with mock.patch.object(net, "get", get), mock.patch.object(
                updater, "check_and_apply", return_value=updater.UpdateResult()):
            return cli._poll(self.args, config.load_config(), state, None)

    def test_offline_restart_works_and_status_shows_the_retry(self):
        state = config.load_state()
        self.connected_poll(state)
        config.save_state(state)
        with mock.patch.object(net, "get", side_effect=net.NetError("repository unreachable")), mock.patch.object(
                cli, "today_utc", return_value="2026-01-01"):
            self.assertEqual(cli._run_loop(self.args), 0)
            state = config.load_state()
            self.assertEqual(state["done"]["test"], [0])
            with redirect_stdout(io.StringIO()) as out:
                cli.cmd_status(None)
            self.assertIn("repository unreachable", out.getvalue())
            self.assertIn("retry in", out.getvalue())
            delays = []
            for _ in range(9):
                cli._poll(self.args, config.load_config(), state, None)
                with mock.patch.object(cli.random, "uniform", return_value=1.0):
                    delays.append(cli._next_poll(0, {"poll_minutes": 5}, state))
            self.assertEqual(delays[:3], [30, 60, 120])
            self.assertEqual(delays[-2:], [300, 300])
        self.connected_poll(state)
        cli._next_poll(0, config.load_config(), state)
        self.assertEqual((state["poll_failures"], state["retry_at"], state["poll_error"]), (0, 0, ""))

    def test_cached_work_respects_a_signed_pause_after_restart(self):
        state = config.load_state()
        self.connected_poll(state)
        state["halt"], state["halt_seq"] = "paused", updater.RELEASE_SEQ
        config.save_state(state)
        with mock.patch.object(net, "get", side_effect=net.NetError("offline")), mock.patch.object(
                cli, "today_utc", return_value="2026-01-01"):
            self.assertEqual(cli._run_loop(self.args), cli.EXIT_NOTHING)
        self.assertEqual(config.load_state()["done"], {})

    def test_rejects_tampered_older_and_expired_cache(self):
        state = config.load_state()
        self.connected_poll(state)
        config.save_state(state)
        self.assertIsNone(tasks.cached_index(4))
        with mock.patch.object(net, "get", side_effect=net.NetError("offline")), mock.patch.object(
                cli, "today_utc", return_value="2031-01-02"):
            self.assertEqual(cli._run_loop(self.args), cli.EXIT_NOTHING)
            self.assertEqual(config.load_state()["done"], {})
        path = config.path("task-list.json")
        cache = config.read_json(path)
        cache["raw"] += " "
        config.write_json_atomic(path, cache)
        self.assertIsNone(tasks.cached_index(0))
