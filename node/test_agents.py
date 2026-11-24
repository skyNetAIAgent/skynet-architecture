"""Offline HTTP and persistence tests for the agent inventory."""

import io
import json
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import Mock, patch

import receiver
from skynet_agent import ed25519, records, submit


NOW = 1_800_000_000
SEED = bytes(range(32))


def status(seed=SEED, **changes):
    data = {
        "v": 1, "agent": records.public_hex(seed), "version": "0.4.0", "release_seq": 6,
        "os": "linux", "arch": "amd64", "cpu_model": "Nova <X>™", "cpu_threads": 8,
        "ram_mb": 8192, "gpus": [{"name": "A&B", "vram_mb": 4096}],
        "units_done": 47, "started": NOW - 9000, "sent": NOW - 60,
    }
    data.update(changes)
    signature = ed25519.sign(seed, records.canonical(data).encode("ascii"))
    return {"status": data, "sig": signature.hex()}


def result(seed, created, unit=0):
    output = {"score": unit}
    record = {"v": 1, "task": "sample", "kernel": "selftest@1", "agent": "0.2.0",
              "unit": unit, "units": 8, "result": output, "result_sha256": submit.result_hash(output)}
    return records.make(seed, "result", {"record": record}, created=created)


class AgentsTest(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.folder = Path(folder.name)
        self.posts = receiver.Budget(60, 600)
        self.reads = receiver.Budget(120, 1200)
        clock = patch.object(receiver.time, "time", return_value=NOW)
        self.clock = clock.start()
        self.addCleanup(clock.stop)
        self.open_store()

    def open_store(self):
        self.store = receiver.NodeStore(str(self.folder), 2 ** 20)
        self.addCleanup(self.store.reader.close)
        self.handler = receiver.make_handler(self.store, self.posts, self.reads, None)

    def http(self, method, path, data=b""):
        if not isinstance(data, bytes):
            data = json.dumps(data, ensure_ascii=False).encode("utf-8")
        head = f"{method} {path} HTTP/1.1\r\nHost: localhost\r\nContent-Length: {len(data)}\r\n\r\n"
        sock = Mock()
        sock.makefile.return_value = io.BytesIO(head.encode("ascii") + data)
        reply = io.BytesIO()
        sock.sendall.side_effect = reply.write
        self.handler(sock, ("192.0.2.1", 1234), None)
        headers, body = reply.getvalue().split(b"\r\n\r\n", 1)
        return int(headers.split()[1]), headers, body

    def rows(self):
        code, _, data = self.http("GET", "/v1/agents")
        self.assertEqual(200, code)
        return json.loads(data)

    def post(self, path, data, code=200):
        self.assertEqual(code, self.http("POST", path, data)[0])

    def test_signed_status_size_limits_and_shared_budget(self):
        payload = records.wire(status())
        self.posts.per_address = 1
        self.post("/v1/status", payload.ljust(4097), 413)
        self.post("/v1/status", payload.ljust(4096))
        self.post("/v1/records", b"{}", 429)
        self.post("/v1/status", payload, 429)
        row, = self.rows()
        self.assertEqual(status()["status"], {k: row[k] for k in status()["status"]})
        self.assertEqual((False, NOW, NOW), (row["legacy"], row["first_seen"], row["last_seen"]))
        self.assertNotIn(b"192.0.2.1", (self.folder / "agents.json").read_bytes())

    def test_invalid_status_does_not_enter_inventory(self):
        tampered = status()
        tampered["status"]["units_done"] += 1
        wrong_key = status(agent=records.public_hex(b"z" * 32))
        duplicate = records.wire(status()).replace(b'"v":1', b'"v":1,"v":1')
        for invalid in (b"{", [], tampered, wrong_key, duplicate, status(hostname="private"),
                        status(cpu_threads=True), status(ram_mb=-1),
                        status(gpus=[{"name": "GPU", "vram_mb": 4, "path": "/private"}]),
                        {**status(), "address": "private"}):
            with self.subTest(invalid=type(invalid)):
                self.post("/v1/status", invalid, 400)
        self.assertEqual([], self.rows())
        self.assertIn(b"No agent is online right now", self.http("GET", "/agents")[2])

    def test_latest_state_survives_restart_and_stale_delivery(self):
        self.post("/v1/status", status())
        self.clock.return_value = NOW + 3600
        self.post("/v1/status", status(sent=NOW + 3590, units_done=51))
        self.clock.return_value = NOW + 3700
        self.post("/v1/status", status())
        self.store.reader.close()
        self.open_store()
        row, = self.rows()
        self.assertEqual((NOW, NOW + 3600, 51), (row["first_seen"], row["last_seen"], row["units_done"]))

    def test_failed_replace_preserves_previous_status(self):
        self.post("/v1/status", status())
        path = self.folder / "agents.json"
        original = path.read_bytes()
        with patch.object(receiver.os, "replace", side_effect=OSError("disk full")):
            self.post("/v1/status", status(sent=NOW, units_done=48), 507)
        self.assertEqual(original, path.read_bytes())
        row, = self.rows()
        self.assertEqual(47, row["units_done"])
        self.post("/v1/status", status(sent=NOW, units_done=48))
        self.assertEqual(48, self.rows()[0]["units_done"])

    def test_concurrent_agents_persist(self):
        packets = [status(bytes([i]) * 32) for i in range(4)]
        with ThreadPoolExecutor(max_workers=4) as pool:
            codes = list(pool.map(lambda p: self.http("POST", "/v1/status", p)[0], packets))
        self.assertEqual([200] * 4, codes)
        self.store.reader.close()
        self.open_store()
        self.assertEqual({p["status"]["agent"] for p in packets}, {r["agent"] for r in self.rows()})

    def test_legacy_results_reindex_and_upgrade(self):
        first = result(SEED, NOW - 7200)
        later = result(SEED, NOW - 60, 1)
        task = records.make(b"t" * 32, "task", {"title": "A", "text": "B", "accept": "C"})
        self.post("/v1/records", later)
        self.post("/v1/records", first)
        self.post("/v1/records", later)
        self.post("/v1/records", task)
        self.store.reader.close()
        self.open_store()
        old, = self.rows()
        self.assertEqual((True, 2, NOW - 7200, NOW - 60),
                         (old["legacy"], old["result_count"], old["first_seen"], old["last_seen"]))
        _, _, page = self.http("GET", "/agents")
        for value in (b"No status (results only)", b"2 results", b"1 min 0 s ago", old["agent"][:12].encode()):
            self.assertIn(value, page)
        self.post("/v1/status", status())
        upgraded, = self.rows()
        self.assertFalse(upgraded["legacy"])
        self.assertEqual((old["agent"], 2, 47, NOW - 7200, NOW),
                         (upgraded["agent"], upgraded["result_count"], upgraded["units_done"],
                          upgraded["first_seen"], upgraded["last_seen"]))

    def test_page_shows_only_agents_online_in_last_five_minutes(self):
        self.post("/v1/status", status())
        self.clock.return_value = NOW + 1
        self.post("/v1/status", status(b"b" * 32, gpus=[{"name": "B", "vram_mb": 128},
                                                        {"name": "C", "vram_mb": 256}]))
        self.clock.return_value = NOW + 300
        code, headers, raw = self.http("GET", "/agents")
        self.assertEqual(200, code)
        self.assertIn(b"text/html", headers)
        page = raw.decode()
        for label, value in (("Online agents", "1"), ("VRAM (MiB)", "384")):
            self.assertIn(f"<dt>{label}</dt><dd>{value}</dd>", page)
        self.assertIn("4 min 59 s ago", page)
        self.assertEqual(1, page.count("<tr><td"))
        self.clock.return_value = NOW + 301
        page = self.http("GET", "/agents")[2].decode()
        self.assertIn("No agent is online right now.", page)

if __name__ == "__main__":
    unittest.main()
