"""Signed records, the task board, the full node and publishing without an account."""

import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import urllib.request

import helpers  # noqa: F401  (sets the test environment)

from skynet_agent import board, config, ed25519, nostr, records, submit, transport

NODE = os.path.join(helpers.REPO_ROOT, "node", "receiver.py")


def seed(n):
    return bytes([n]) * 32


class Home(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.old = {k: os.environ.get(k) for k in ("SKYNET_AGENT_HOME", "SKYNET_AGENT_RECEIVERS",
                                                   "SKYNET_AGENT_RELAYS", "SKYNET_AGENT_SUBMIT_VIA")}
        os.environ["SKYNET_AGENT_HOME"] = self.tmp

    def tearDown(self):
        for k, v in self.old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        shutil.rmtree(self.tmp, ignore_errors=True)


class Records(Home):
    def test_roundtrip_and_tamper(self):
        env = records.make(seed(1), "task", {"title": "T", "text": "Do it", "accept": "a table"})
        self.assertEqual(records.parse(records.wire(env))["id"], env["id"])
        for path, value in ((("body", "payload", "title"), "X"), (("body", "author"), "00" * 32),
                            (("body", "created"), env["body"]["created"] + 1), (("body", "net"), "other")):
            bad = json.loads(json.dumps(env))
            obj = bad
            for key in path[:-1]:
                obj = obj[key]
            obj[path[-1]] = value
            with self.assertRaises(records.RecordError):
                records.verify(bad)
        bad = json.loads(json.dumps(env))
        bad["sig"] = "00" * 64
        with self.assertRaises(records.RecordError):
            records.verify(bad)

    def test_resigned_by_another_key_is_another_record(self):
        env = records.make(seed(1), "task", {"title": "T", "text": "x", "accept": "y"})
        forged = json.loads(json.dumps(env))
        forged["body"]["author"] = records.public_hex(seed(2))
        forged["id"] = records.record_id(forged["body"])
        forged["sig"] = ed25519.sign(seed(2), bytes.fromhex(forged["id"])).hex()
        records.verify(forged)                      # valid, but it is a different author
        self.assertNotEqual(forged["id"], env["id"])

    def test_payload_rules(self):
        s = seed(1)
        tid = "ab" * 32
        for rtype, payload in (("task", {"title": "", "text": "x", "accept": "y"}),
                               ("task", {"title": "t", "text": "x", "accept": "y", "extra": 1}),
                               ("task", {"title": "t", "text": "x", "accept": "y", "deputies": ["zz"]}),
                               ("claim", {"task": "nothex", "until": 5}),
                               ("report", {"task": tid, "summary": "s"}),
                               ("accept", {"task": tid}),
                               ("result", {"record": {"v": 1}}),
                               ("task", {"title": "t", "text": "x" * 20001, "accept": "y"})):
            with self.assertRaises(records.RecordError, msg="%s %r" % (rtype, payload)):
                records.make(s, rtype, payload)

    def test_future_and_size_and_duplicates(self):
        with self.assertRaises(records.RecordError):
            records.make(seed(1), "claim", {"task": "ab" * 32, "until": 10}, created=int(time.time()) + 3 * 86400)
        env = records.make(seed(1), "claim", {"task": "ab" * 32, "until": 10})
        raw = records.wire(env).decode("utf-8")
        with self.assertRaises(records.RecordError):
            records.parse(raw.replace('"until":10', '"until":10,"until":11'))
        with self.assertRaises(records.RecordError):
            records.parse("[" * 100000)

    def test_identity_is_created_once_and_kept(self):
        a = records.load_seed()
        b = records.load_seed()
        self.assertEqual(a, b)
        self.assertEqual(len(a), 32)

    def test_result_record_carries_the_ai_text(self):
        record = {"v": 1, "task": "q", "unit": 0, "units": 1, "kernel": "ai-answer@1", "agent": "0.1.0",
                  "result": {"output_sha256": __import__("hashlib").sha256(b"hello").hexdigest(), "chars": 5}}
        record["result_sha256"] = submit.result_hash(record["result"])
        records.make(seed(1), "result", {"record": record, "text": "hello"})
        with self.assertRaises(records.RecordError):
            records.make(seed(1), "result", {"record": record, "text": "other"})
        with self.assertRaises(records.RecordError):
            records.make(seed(1), "result", {"record": record})

    def test_review_findings(self):
        env = records.make(seed(1), "task", {"title": "T", "text": "x", "accept": "y"})
        # version 1.0, trailing newline in hex, nested junk in deputies: refused, never a crash
        for mutate in (lambda e: e["body"].__setitem__("v", 1.0),
                       lambda e: e.__setitem__("id", e["id"] + "\n"),
                       lambda e: e["body"]["payload"].__setitem__("deputies", [[1], {"a": 2}])):
            bad = json.loads(json.dumps(env))
            mutate(bad)
            with self.assertRaises(records.RecordError):
                records.verify(bad)
        with self.assertRaises(records.RecordError):
            records.parse("\ud800")                       # a lone surrogate
        # small-order keys are not identities: the identity point and a point of order 8
        for weak in ("01" + "00" * 31, "c7176a703d4dd84fba3c0b760d10670f2a2053fa2c39ccc64ec7fd7792ac037a"):
            self.assertFalse(ed25519.is_strong_public(bytes.fromhex(weak)))
            with self.assertRaises(records.RecordError):
                records.make(seed(1), "task", {"title": "T", "text": "x", "accept": "y", "deputies": [weak]})
        self.assertTrue(ed25519.is_strong_public(bytes.fromhex(records.public_hex(seed(1)))))
        # a record dated too far ahead is "later", not "broken"
        with self.assertRaises(records.RecordFromFuture):
            records.verify(env, now=env["body"]["created"] - 3 * 86400)

    def test_store_survives_a_torn_line(self):
        store = transport.Store(os.path.join(self.tmp, "s"))
        a = records.make(seed(1), "task", {"title": "A", "text": "x", "accept": "y"})
        b = records.make(seed(1), "task", {"title": "B", "text": "x", "accept": "y"})
        self.assertEqual(store.add(a), "new")
        with open(store.file, "ab") as f:
            f.write(b'{"id":"half')                      # a crash in the middle of a line
        store = transport.Store(os.path.join(self.tmp, "s"))
        self.assertEqual(store.add(b), "new")
        store = transport.Store(os.path.join(self.tmp, "s"))
        self.assertEqual(sorted(store.items), sorted([a["id"], b["id"]]))
        small = transport.Store(os.path.join(self.tmp, "t"), max_bytes=100)
        self.assertEqual(small.add(a), "full")


class Schnorr(unittest.TestCase):
    def test_bip340_vectors(self):
        # test vectors 0 and 1 of BIP-340
        sk = (3).to_bytes(32, "big")
        self.assertEqual(nostr.schnorr_public(sk).hex().upper(),
                         "F9308A019258C31049344F85F89D5229B531C845836F99B08601F113BCE036F9")
        sig = nostr.schnorr_sign(bytes(32), sk, aux=bytes(32))
        self.assertEqual(sig.hex().upper(),
                         "E907831F80848D1069A5371B402410364BDF1C5F8307B0084C55F1CE2DCA8215"
                         "25F66A4A85EA8B71E482A74F382D2CE5EBEEE8FDB2172F477DF4900D310536C0")
        sk = bytes.fromhex("B7E151628AED2A6ABF7158809CF4F3C762E7160F38B4DA56A784D9045190CFEF")
        msg = bytes.fromhex("243F6A8885A308D313198A2E03707344A4093822299F31D0082EFA98EC4E6C89")
        aux = bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000001")
        self.assertEqual(nostr.schnorr_sign(msg, sk, aux=aux).hex().upper(),
                         "6896BD60EEAE296DB48A229FF71DFE071BDE413E6D43F917DC8DCF8C78DE3341"
                         "8906D11AC976ABCCB20B091292BFF4EA897EFCB639EA871CFA95F6DE339E4B0A")

    def test_event_wraps_the_record(self):
        env = records.make(seed(1), "task", {"title": "T", "text": "x", "accept": "y"})
        event = nostr.make_event(nostr.secret_from_seed(seed(1)), env)
        self.assertTrue(nostr.schnorr_verify(bytes.fromhex(event["id"]), bytes.fromhex(event["pubkey"]),
                                             bytes.fromhex(event["sig"])))
        self.assertEqual(records.parse(event["content"])["id"], env["id"])


class Board(unittest.TestCase):
    def setUp(self):
        self.author, self.worker, self.other, self.deputy = seed(1), seed(2), seed(3), seed(4)
        self.t0 = 1_700_000_000
        self.task = records.make(self.author, "task", {"title": "T", "text": "x", "accept": "y",
                                                       "deputies": [records.public_hex(self.deputy)],
                                                       "handover_days": 7}, created=self.t0)

    def rec(self, s, rtype, payload, dt):
        return records.make(s, rtype, payload, created=self.t0 + dt)

    def test_claim_reserves_nothing_and_author_decides(self):
        tid = self.task["id"]
        claim = self.rec(self.worker, "claim", {"task": tid, "until": self.t0 + 3600}, 10)
        r1 = self.rec(self.other, "report", {"task": tid, "summary": "s", "text": "without a claim"}, 20)
        fake = self.rec(self.other, "accept", {"task": tid, "report": r1["id"]}, 30)
        b = board.build([self.task, claim, r1, fake], now=self.t0 + 100)[tid]
        self.assertEqual(len(b["claims"]), 1)
        self.assertEqual(len(b["reports"]), 1)
        self.assertEqual(b["accepted"], [])                 # a stranger cannot accept
        self.assertEqual(board.status(b), "reported")
        ok = self.rec(self.author, "accept", {"task": tid, "report": r1["id"]}, 40)
        b = board.build([self.task, claim, r1, fake, ok], now=self.t0 + 100)[tid]
        self.assertEqual(b["accepted"], [r1["id"]])
        later = board.build([self.task, claim, r1, ok], now=self.t0 + 7200)[tid]
        self.assertEqual(later["claims"], [])                # the claim has expired

    def test_newest_author_verdict_wins_and_deputy_waits(self):
        tid = self.task["id"]
        r1 = self.rec(self.worker, "report", {"task": tid, "summary": "s", "text": "t"}, 20)
        too_soon = self.rec(self.deputy, "accept", {"task": tid, "report": r1["id"]}, 30)
        b = board.build([self.task, r1, too_soon], now=self.t0 + 8 * 86400)[tid]
        self.assertEqual(b["accepted"], [])                  # signed before the handover: never counts
        dep = self.rec(self.deputy, "accept", {"task": tid, "report": r1["id"]}, 7 * 86400 + 30)
        early = board.build([self.task, r1, dep], now=self.t0 + 86400)[tid]
        self.assertEqual(early["accepted"], [])              # read before the handover
        late = board.build([self.task, r1, dep], now=self.t0 + 8 * 86400)[tid]
        self.assertEqual(late["accepted"], [r1["id"]])
        rev = self.rec(self.author, "revise", {"task": tid, "report": r1["id"], "note": "no"}, 7 * 86400 + 40)
        b = board.build([self.task, r1, dep, rev], now=self.t0 + 8 * 86400)[tid]
        self.assertEqual(b["accepted"], [])                  # the author outranks the deputy
        acc = self.rec(self.author, "accept", {"task": tid, "report": r1["id"]}, 7 * 86400 + 50)
        b = board.build([self.task, r1, dep, rev, acc], now=self.t0 + 8 * 86400)[tid]
        self.assertEqual(b["accepted"], [r1["id"]])

    def test_a_newer_claim_replaces_an_older_one(self):
        tid = self.task["id"]
        long = self.rec(self.worker, "claim", {"task": tid, "until": self.t0 + 10 * 86400}, 10)
        short = self.rec(self.worker, "claim", {"task": tid, "until": self.t0 + 3600}, 20)
        b = board.build([self.task, long, short], now=self.t0 + 7200)[tid]
        self.assertEqual(b["claims"], [])             # the short one expired; the long one does not come back

    def test_verdict_older_than_report_is_ignored(self):
        tid = self.task["id"]
        r1 = self.rec(self.worker, "report", {"task": tid, "summary": "s", "text": "t"}, 100)
        early = self.rec(self.author, "accept", {"task": tid, "report": r1["id"]}, 50)
        self.assertEqual(board.build([self.task, r1, early], now=self.t0 + 200)[tid]["accepted"], [])

    def test_terminal_text_is_cleaned(self):
        self.assertEqual(board.clean("ok\x1b[2J‮not"), "ok�[2J�not")

    def test_verdict_must_match_the_task_of_the_report(self):
        other = records.make(self.worker, "task", {"title": "O", "text": "x", "accept": "y"}, created=self.t0)
        r_other = self.rec(self.worker, "report", {"task": other["id"], "summary": "s", "text": "t"}, 5)
        wrong = self.rec(self.author, "accept", {"task": self.task["id"], "report": r_other["id"]}, 10)
        b = board.build([self.task, other, r_other, wrong], now=self.t0 + 100)
        self.assertEqual(b[self.task["id"]]["accepted"], [])
        self.assertEqual(b[other["id"]]["accepted"], [])


class Node(Home):
    """The full node over real HTTP on this machine, without public relays."""

    @classmethod
    def setUpClass(cls):
        cls.data = tempfile.mkdtemp()
        cls.proc = subprocess.Popen([sys.executable, "-I", NODE, "--data", cls.data, "--host", "127.0.0.1",
                                     "--port", "0", "--no-relays", "--rate", "1000"],
                                    stderr=subprocess.PIPE, stdout=subprocess.DEVNULL)
        line = cls.proc.stderr.readline().decode("utf-8")
        threading.Thread(target=cls.proc.stderr.read, daemon=True).start()
        port = int(line.split("listening on 127.0.0.1:")[1].split(",")[0])
        cls.base = "http://127.0.0.1:%d" % port

    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate()
        cls.proc.wait(10)
        shutil.rmtree(cls.data, ignore_errors=True)

    def setUp(self):
        super().setUp()
        os.environ["SKYNET_AGENT_RECEIVERS"] = self.base
        os.environ["SKYNET_AGENT_RELAYS"] = "none"

    def test_post_fetch_and_reject(self):
        env = records.make(seed(5), "task", {"title": "Node", "text": "x", "accept": "y"})
        self.assertEqual(transport.post_to_receiver(self.base, env), (True, ""))
        self.assertEqual(transport.post_to_receiver(self.base, env), (True, ""))       # a copy is fine
        bad = json.loads(json.dumps(env))
        bad["body"]["payload"]["title"] = "changed"
        ok, why = transport.post_to_receiver(self.base, bad)
        self.assertFalse(ok)
        self.assertIn("400", why)
        got, nxt, err = transport.fetch_from_receiver(self.base)
        self.assertEqual(err, "")
        self.assertEqual([e["id"] for e in got].count(env["id"]), 1)
        with urllib.request.urlopen(self.base + "/v1/records/" + env["id"]) as r:
            self.assertEqual(json.loads(r.read())["id"], env["id"])

    def test_http_edges(self):
        import http.client
        import socket
        host, port = self.base[len("http://"):].split(":")
        env = records.make(seed(6), "task", {"title": "Edges", "text": "x", "accept": "y"})
        body = records.wire(env)
        # a body shorter than its Content-Length is not stored
        s = socket.create_connection((host, int(port)))
        s.sendall(b"POST /v1/records HTTP/1.1\r\nHost: x\r\nContent-Length: %d\r\n\r\n" % (len(body) + 10) + body)
        s.shutdown(socket.SHUT_WR)
        answer = s.recv(1000)
        s.close()
        self.assertNotIn(b" 200 ", answer.split(b"\r\n")[0])
        conn = http.client.HTTPConnection(host, int(port), timeout=10)
        conn.request("GET", "/v1/records/" + env["id"])
        self.assertEqual(conn.getresponse().status, 404)
        conn.close()
        # chunked bodies and double lengths are refused
        for head in (b"Transfer-Encoding: chunked\r\n", b"Content-Length: 5\r\nContent-Length: 5\r\n"):
            s = socket.create_connection((host, int(port)))
            s.sendall(b"POST /v1/records HTTP/1.1\r\nHost: x\r\n" + head + b"\r\nhello")
            self.assertIn(b" 4", s.recv(1000).split(b"\r\n")[0])
            s.close()

    def test_a_fake_ok_is_not_delivery(self):
        import http.server

        class Liar(http.server.BaseHTTPRequestHandler):
            def do_POST(self):
                self.rfile.read(int(self.headers["Content-Length"]))
                self.send_response(200)
                self.send_header("Content-Length", "2")
                self.end_headers()
                self.wfile.write(b"ok")

            def log_message(self, *a):
                pass

        srv = http.server.HTTPServer(("127.0.0.1", 0), Liar)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        try:
            env = records.make(seed(7), "task", {"title": "L", "text": "x", "accept": "y"})
            ok, why = transport.post_to_receiver("http://127.0.0.1:%d" % srv.server_address[1], env)
            self.assertFalse(ok)
        finally:
            srv.shutdown()

    def test_whole_cycle_through_the_command_line(self):
        out = []
        say = out.append

        class A:
            pass

        def run(action, ref=None, **kw):
            a = A()
            for k in ("title", "file", "accept", "summary", "note", "deputy", "parent", "base", "revises"):
                setattr(a, k, None)
            a.hours, a.handover_days, a.json, a.offline = 24, 14, False, False
            a.action, a.ref = action, ref
            for k, v in kw.items():
                setattr(a, k, v)
            out.clear()
            code = board.cmd_net(a, say)
            self.assertEqual(code, 0, "\n".join(out))
            return out[0].split()[-1] if out else ""

        text = os.path.join(self.tmp, "t.txt")
        with open(text, "w", encoding="utf-8") as f:
            f.write("Проверить вариант Б.")
        tid = run("post-task", title="Задача", file=text, accept="таблица")
        author_home = self.tmp
        # a second device: its own home and key, the same receiver
        os.environ["SKYNET_AGENT_HOME"] = tempfile.mkdtemp(dir=self.tmp)
        run("claim", tid[:10])
        rid = run("report", tid[:10], file=text, summary="готово")
        a = A()
        a.action, a.ref, a.note, a.offline, a.json = "accept", rid[:10], None, False, False
        self.assertEqual(board.cmd_net(a, say), 1)          # the worker cannot accept its own report
        os.environ["SKYNET_AGENT_HOME"] = author_home
        run("sync")
        run("accept", rid[:10])
        store = transport.Store()
        transport.sync(store)
        info = board.build(store.all())[tid]
        self.assertEqual(info["accepted"], [rid])
        self.assertEqual(len(info["claims"]), 1)

    def test_agent_publishes_results_without_an_account(self):
        os.environ["SKYNET_AGENT_SUBMIT_VIA"] = "net"
        task = {"id": "selftest", "kernel": "selftest", "kernel_version": 1, "units": 4, "params": {}, "issue": 0}
        record = {"v": 1, "task": "selftest", "unit": 2, "units": 4, "kernel": "selftest@1", "agent": "0.1.0",
                  "result": {"digest": "ab"}}
        record["result_sha256"] = submit.result_hash(record["result"])
        submit.save_to_outbox(task, record, None, "compute")
        state = config.load_state()
        log = logging.getLogger("test")
        cfg = {"submit": "auto", "ai": {}}
        self.assertEqual(submit.flush_outbox(cfg, state, log), 1)
        self.assertEqual(submit.outbox_count(), 0)
        got, _, _ = transport.fetch_from_receiver(self.base)
        mine = [e for e in got if e["body"]["type"] == "result" and e["body"]["payload"]["record"]["unit"] == 2]
        self.assertEqual(len(mine), 1)

    def test_nothing_is_lost_when_every_channel_is_down(self):
        os.environ["SKYNET_AGENT_SUBMIT_VIA"] = "net"
        os.environ["SKYNET_AGENT_RECEIVERS"] = "http://127.0.0.1:9"
        task = {"id": "selftest", "kernel": "selftest", "kernel_version": 1, "units": 4, "params": {}, "issue": 0}
        record = {"v": 1, "task": "selftest", "unit": 1, "units": 4, "kernel": "selftest@1", "agent": "0.1.0",
                  "result": {"digest": "cd"}}
        record["result_sha256"] = submit.result_hash(record["result"])
        submit.save_to_outbox(task, record, None, "compute")
        state = config.load_state()
        log = logging.getLogger("test")
        self.assertEqual(submit.flush_outbox({"submit": "auto", "ai": {}}, state, log), 0)
        self.assertEqual(submit.outbox_count(), 1)
        first = submit.outbox_entries()[0][1]["net_record"]["id"]
        os.environ["SKYNET_AGENT_RECEIVERS"] = self.base
        self.assertEqual(submit.flush_outbox({"submit": "auto", "ai": {}}, state, log, force=True), 1)
        got, _, _ = transport.fetch_from_receiver(self.base)
        self.assertIn(first, [e["id"] for e in got])         # the retry sent the same record


if __name__ == "__main__":
    unittest.main()
