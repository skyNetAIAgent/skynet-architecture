import logging
import os
import random
import shutil
import tempfile
import time
import unittest

import helpers
from skynet_agent import config, submit, tasks

SELF = {"id": "selftest-1", "kernel": "selftest", "kernel_version": 1, "units": 1,
        "params": {"rounds": 2}, "issue": 7}
EXIT = {"id": "exit-a", "kernel": "exit-scam-a", "kernel_version": 1, "units": 5, "issue": 8,
        "params": {"H0": 300, "batches": 1, "n_max": 6, "sizes": {"mode": "grid", "points": 4}}}
AI = {"id": "ask-1", "kernel": "ai-answer", "kernel_version": 1, "units": 1, "issue": 9,
      "params": {"question": "Find an attack."}}


def index(*task_list, **extra):
    out = {"format": 1, "seq": 3, "issued": "2026-11-22", "tasks": [dict(t) for t in task_list]}
    out.update(extra)
    return out


def fresh_state():
    return {"done": {}, "skip": {}, "fails": {}, "submitted": [], "last_error": "",
            "counters": {"units_done": 0, "units_failed": 0, "published": 0}}


class TaskList(unittest.TestCase):
    def test_validate_index(self):
        self.assertEqual(len(tasks.validate_index(index(SELF, EXIT, AI))), 3)
        bad = [
            index(SELF, SELF),                                  # duplicate id
            index(dict(SELF, id="Bad Id")),
            index(dict(SELF, units=0)),
            index(dict(SELF, surprise=1)),
            index(dict(SELF, params=[])),
            index(dict(SELF, priority=1000)),
            index(SELF, format=2),
            index(SELF, seq=0),
            index(SELF, expires="tomorrow"),
            {"format": 1, "seq": 1, "tasks": "none"},
            [],
        ]
        for item in bad:
            with self.assertRaises(tasks.IndexError_):
                tasks.validate_index(item)

    def test_expiry(self):
        self.assertFalse(tasks.is_expired(index(SELF), "2030-01-01"))
        self.assertFalse(tasks.is_expired(index(SELF, expires="2027-01-01"), "2027-01-01"))
        self.assertTrue(tasks.is_expired(index(SELF, expires="2027-01-01"), "2027-01-02"))

    def test_usable(self):
        cfg = {"ai": {"enabled": False}}
        self.assertIsNone(tasks.usable(SELF, cfg))
        self.assertIsNone(tasks.usable(EXIT, cfg))
        self.assertEqual(tasks.usable(AI, cfg), "AI mode is off")
        self.assertIsNone(tasks.usable(AI, {"ai": {"enabled": True}}))
        self.assertEqual(tasks.usable(dict(SELF, priority=0), cfg), "closed")
        self.assertIn("unknown kernel", tasks.usable(dict(SELF, kernel="future"), cfg))
        self.assertIn("kernel version", tasks.usable(dict(SELF, kernel_version=2), cfg))
        self.assertIn("newer agent", tasks.usable(dict(SELF, min_agent_seq=10 ** 6), cfg))
        self.assertIn("rejected", tasks.usable(dict(SELF, params={"rounds": 0}), cfg))

    def test_pick(self):
        cfg = {"ai": {"enabled": False}}
        rng = random.Random(1)
        state = fresh_state()
        seen = set()
        for _ in range(6):
            task, unit = tasks.pick(index(SELF, EXIT, AI), cfg, state, rng=rng)
            self.assertNotEqual(task["id"], "ask-1")          # AI mode is off
            self.assertNotIn((task["id"], unit), seen)
            seen.add((task["id"], unit))
            state["done"].setdefault(task["id"], []).append(unit)
        self.assertEqual(len(seen), 6)                        # 1 + 5 units, each exactly once
        self.assertIsNone(tasks.pick(index(SELF, EXIT, AI), cfg, state, rng=rng))

    def test_pick_respects_busy_skip_and_coverage(self):
        cfg = {"ai": {"enabled": False}}
        state = fresh_state()
        busy = [("exit-a", u) for u in range(4)]
        task, unit = tasks.pick(index(EXIT), cfg, state, busy=busy, rng=random.Random(2))
        self.assertEqual(unit, 4)
        state["skip"]["exit-a"] = {"reason": "too slow", "until": 2 ** 40}
        self.assertIsNone(tasks.pick(index(EXIT), cfg, state))
        state = fresh_state()
        coverage = {"exit-a": {"0": 2, "1": 2, "2": 0, "3": 5, "4": 2}}
        for seed in range(20):
            _, unit = tasks.pick(index(dict(EXIT, redundancy=2)), cfg, state, coverage, rng=random.Random(seed))
            self.assertEqual(unit, 2)                         # the only unit still lacking results


class Records(unittest.TestCase):
    def outcome(self):
        return {"ok": True, "elapsed_s": 1.5,
                "result": {"kernel": "exit-scam-a@1", "count": 8, "hits": 0, "digest": "ab" * 32,
                           "best": {"ev_ppb": 917500000, "path": [[1, 25]]}, "top_hits": []}}

    def test_roundtrip(self):
        record, text = submit.make_record(EXIT, 3, self.outcome(), {"report_platform": True})
        self.assertIsNone(text)
        self.assertIn("platform", record)
        body = submit.format_comment(record)
        parsed, parsed_text = submit.parse_comment(body)
        self.assertEqual(parsed, record)
        self.assertIsNone(parsed_text)
        # GitHub may return CRLF line ends
        self.assertEqual(submit.parse_comment(body.replace("\n", "\r\n"))[0], record)
        record2, _ = submit.make_record(EXIT, 3, self.outcome(), {"report_platform": False})
        self.assertNotIn("platform", record2)
        self.assertEqual(record2["result_sha256"], record["result_sha256"])

    def test_tampering_is_detected(self):
        record, _ = submit.make_record(EXIT, 3, self.outcome(), {})
        body = submit.format_comment(record)
        self.assertIsNone(submit.parse_comment(body.replace('"hits":0', '"hits":1')))
        self.assertIsNone(submit.parse_comment(body.replace(submit.MARKER, "")))
        self.assertIsNone(submit.parse_comment("just a comment"))
        self.assertIsNone(submit.parse_comment(submit.MARKER + "\n```json\nnot json\n```\n"))
        self.assertIsNone(submit.parse_comment(None))

    def test_several_results_in_one_comment(self):
        records = []
        for unit in range(3):
            outcome = self.outcome()
            outcome["result"]["count"] = unit
            records.append(submit.make_record(EXIT, unit, outcome, {})[0])
        body = submit.format_batch(records)
        self.assertEqual([r for r, _ in submit.parse_all(body)], records)
        # one damaged result does not hide the others
        damaged = body.replace('"count":1', '"count":7')
        self.assertEqual([r["unit"] for r, _ in submit.parse_all(damaged)], [0, 2])
        with self.assertRaises(ValueError):
            submit.format_batch([])
        with self.assertRaises(ValueError):
            submit.format_batch(records * 20)                  # more than a comment may hold

    def test_ai_answer_text(self):
        nasty = ("Attack:\n```json\n{\"v\": 1}\n```\n```python\nprint(1)\n```\n" + "~" * 20
                 + "\n@someone <!-- x --> " + "я" * 50)
        outcome = {"ok": True, "elapsed_s": 9,
                   "result": {"kernel": "ai-answer@1", "model": "qwen `evil` <b>", "local": True,
                              "prompt_sha256": "cd" * 32, "output": nasty}}
        record, text = submit.make_record(AI, 0, outcome, {})
        self.assertNotIn("output", record["result"])
        self.assertNotIn("`", record["result"]["model"])
        self.assertNotIn("~" * 8, text)
        body = submit.format_comment(record, text)
        parsed, parsed_text = submit.parse_comment(body)
        self.assertEqual(parsed, record)
        self.assertEqual(parsed_text, text)
        # changing the answer text breaks the hash
        self.assertIsNone(submit.parse_comment(body.replace("Attack:", "Defence:")))

    def test_too_large(self):
        outcome = {"ok": True, "result": {"blob": "x" * 70000}}
        record, _ = submit.make_record(SELF, 0, outcome, {})
        with self.assertRaises(ValueError):
            submit.format_comment(record)

    def test_manual_link(self):
        record, _ = submit.make_record(EXIT, 3, self.outcome(), {})
        url = submit.manual_issue_url({"record": record, "text": None})
        self.assertTrue(url.startswith("https://github.com/skyNetAIAgent/skynet-architecture/issues/new?"))
        self.assertLess(len(url), submit.MAX_URL_CHARS)
        big, _ = submit.make_record(SELF, 0, {"ok": True, "result": {"blob": "x" * 9000}}, {})
        self.assertIsNone(submit.manual_issue_url({"record": big, "text": None}))


class Publishing(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="skynet-test-")
        self.github = helpers.FakeGitHub()
        self._saved = dict((k, os.environ.get(k)) for k in
                           ("SKYNET_AGENT_HOME", "SKYNET_AGENT_API_URL", "SKYNET_GITHUB_TOKEN"))
        os.environ["SKYNET_AGENT_HOME"] = self.tmp
        os.environ["SKYNET_AGENT_API_URL"] = self.github.url
        os.environ["SKYNET_GITHUB_TOKEN"] = "test-token"
        self.log = logging.getLogger("skynet-test")
        self.log.addHandler(logging.NullHandler())
        self.log.propagate = False
        self.cfg = {"submit": "auto", "max_submissions_per_day": 48, "batch_minutes": 60,
                    "ai": {"review_before_submit": True}}

    def tearDown(self):
        self.github.close()
        for key, value in self._saved.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value
        shutil.rmtree(self.tmp, ignore_errors=True)

    def put(self, task, unit, result=None, kind="compute"):
        outcome = {"ok": True, "elapsed_s": 1, "result": result or {"digest": "ab" * 32, "n": unit}}
        record, text = submit.make_record(task, unit, outcome, {})
        return submit.save_to_outbox(task, record, text, kind)

    def test_publishes_together_and_moves_to_sent(self):
        self.put(EXIT, 0)
        self.put(EXIT, 1)
        state = fresh_state()
        self.assertEqual(submit.flush_outbox(self.cfg, state, self.log, min_gap=0), 2)
        self.assertEqual(len(self.github.posts), 1)            # two results of one task: one comment
        path, auth, body = self.github.posts[0]
        self.assertEqual(path, "/repos/skyNetAIAgent/skynet-architecture/issues/8/comments")
        self.assertEqual(auth, "Bearer test-token")
        self.assertEqual([r["unit"] for r, _ in submit.parse_all(body)], [0, 1])
        self.assertIsNone(submit.parse_comment(body))          # not a single-result comment
        self.assertEqual(submit.outbox_entries(), [])
        self.assertEqual(submit.outbox_count(), 0)
        self.assertEqual(len(os.listdir(config.path("sent"))), 2)
        self.assertEqual(state["counters"]["published"], 2)

    def test_at_most_one_partly_filled_comment_per_interval(self):
        state = fresh_state()
        self.put(EXIT, 0)
        self.assertEqual(submit.flush_outbox(self.cfg, state, self.log, min_gap=0), 1)   # the first goes at once
        self.put(EXIT, 1)
        self.put(EXIT, 2)
        self.assertEqual(submit.flush_outbox(self.cfg, state, self.log, min_gap=0), 0)   # too soon
        self.assertEqual(submit.outbox_count(), 2)
        state["last_post"]["8"] -= 3601                         # an hour later
        self.assertEqual(submit.flush_outbox(self.cfg, state, self.log, min_gap=0), 2)
        self.put(EXIT, 3)
        self.assertEqual(submit.flush_outbox(self.cfg, state, self.log, min_gap=0), 0)
        self.assertEqual(submit.flush_outbox(self.cfg, state, self.log, min_gap=0, force=True), 1)
        self.put(EXIT, 4)
        at_once = dict(self.cfg, batch_minutes=0)
        self.assertEqual(submit.flush_outbox(at_once, state, self.log, min_gap=0), 1)
        self.assertEqual(len(self.github.posts), 4)

    def test_full_comments_do_not_wait(self):
        state = fresh_state()
        self.put(EXIT, 0)
        self.assertEqual(submit.flush_outbox(self.cfg, state, self.log, min_gap=0), 1)
        big = {"digest": "ab" * 32, "padding": "x" * 25000}
        for unit in range(1, 5):                               # 4 results of 25 kB: two fit into a comment
            self.put(EXIT, unit, dict(big, n=unit))
        self.assertEqual(submit.flush_outbox(self.cfg, state, self.log, min_gap=0), 2)   # the full one only
        self.assertEqual(submit.outbox_count(), 2)
        for path, auth, body in self.github.posts:
            self.assertLessEqual(len(body), submit.MAX_COMMENT_CHARS)

    def test_oversized_result_is_dropped_not_stuck(self):
        state = fresh_state()
        self.put(EXIT, 0, {"blob": "x" * 70000})
        self.put(EXIT, 1)
        self.assertEqual(submit.flush_outbox(self.cfg, state, self.log, min_gap=0), 1)
        self.assertEqual(submit.outbox_count(), 0)

    def test_daily_limit_manual_mode_and_missing_issue(self):
        for issue in range(20, 25):                            # five tasks, five tracking issues
            self.put(dict(EXIT, id="exit-%d" % issue, issue=issue), 0)
        self.put(dict(SELF, issue=0), 0)                       # no tracking issue yet
        state = fresh_state()
        manual = dict(self.cfg, submit="manual")
        limited = dict(self.cfg, max_submissions_per_day=3)
        self.assertEqual(submit.flush_outbox(manual, state, self.log, min_gap=0), 0)
        self.assertEqual(submit.flush_outbox(limited, state, self.log, min_gap=0), 3)   # the daily limit
        self.assertEqual(submit.flush_outbox(limited, state, self.log, min_gap=0), 0)
        self.assertEqual(len(submit.outbox_entries()), 3)

    def test_result_computed_before_the_task_had_an_issue(self):
        self.put(dict(SELF, issue=0), 0)
        state = fresh_state()
        self.assertEqual(submit.flush_outbox(self.cfg, state, self.log, min_gap=0, issues={"other": 3}), 0)
        self.assertEqual(submit.flush_outbox(self.cfg, state, self.log, min_gap=0,
                                             issues={"selftest-1": 41}), 1)
        self.assertTrue(self.github.posts[0][0].endswith("/issues/41/comments"))

    def test_ai_answers_wait_for_approval(self):
        name = self.put(AI, 0, {"kernel": "ai-answer@1", "model": "m", "output": "text"}, kind="ai")
        state = fresh_state()
        self.assertEqual(submit.flush_outbox(self.cfg, state, self.log, min_gap=0), 0)
        entry = dict(submit.outbox_entries()[0][1], approved=True)
        config.write_json_atomic(config.path("outbox", name), entry)
        self.assertEqual(submit.flush_outbox(self.cfg, state, self.log, min_gap=0), 1)
        self.assertIn("~~~~~~~~text\ntext\n~~~~~~~~", self.github.posts[0][2])

    def test_failure_keeps_the_result(self):
        self.github.fail_status = 403
        self.put(EXIT, 0)
        state = fresh_state()
        self.assertEqual(submit.flush_outbox(self.cfg, state, self.log, min_gap=0), 0)
        self.assertEqual(len(submit.outbox_entries()), 1)
        self.assertIn("403", state["last_error"])

    def test_after_a_failure_the_next_attempt_waits(self):
        self.github.fail_status = 403
        self.put(EXIT, 0)
        state = fresh_state()
        before = time.time()
        self.assertEqual(submit.flush_outbox(self.cfg, state, self.log, min_gap=0), 0)
        self.assertEqual(state["publish_fails"], 1)
        self.assertGreaterEqual(state["publish_after"], int(before) + 60)
        # GitHub works again, but an automatic attempt comes only after the wait ...
        self.github.fail_status = None
        self.assertEqual(submit.flush_outbox(self.cfg, state, self.log, min_gap=0), 0)
        self.assertEqual(self.github.posts, [])
        # ... while a command typed by the participant goes out at once and clears the wait
        self.assertEqual(submit.flush_outbox(self.cfg, state, self.log, min_gap=0, force=True), 1)
        self.assertEqual((state["publish_fails"], state["publish_after"]), (0, 0))
        # the wait doubles with every failure in a row and is capped at an hour
        waits = []
        for _ in range(8):
            now = int(time.time())
            submit._publish_failed(state, now)
            waits.append(state["publish_after"] - now)
        self.assertEqual(waits, [60, 120, 240, 480, 960, 1920, 3600, 3600])
        # when the wait is over, the automatic attempt is made
        state["publish_after"] = int(time.time()) - 1
        self.put(EXIT, 1)
        state["last_post"] = {}
        self.assertEqual(submit.flush_outbox(self.cfg, state, self.log, min_gap=0), 1)

    def test_no_login(self):
        os.environ.pop("SKYNET_GITHUB_TOKEN")
        saved_path = os.environ.get("PATH", "")
        os.environ["PATH"] = self.tmp                         # hide a real "gh" during this test
        try:
            self.put(EXIT, 0)
            state = fresh_state()
            self.assertEqual(submit.flush_outbox(self.cfg, state, self.log, min_gap=0), 0)
            self.assertIn("GitHub", state["last_error"])
            self.assertEqual(self.github.posts, [])
            self.assertGreater(state["publish_after"], time.time())    # it does not ask again at once
        finally:
            os.environ["PATH"] = saved_path

    def test_whoami_and_count(self):
        self.assertEqual(submit.whoami("test-token"), "tester")
        self.github.existing = [submit.MARKER + " x", "hello", submit.MARKER + " y"] + ["z"] * 150
        self.assertEqual(submit.count_results(9), 2)

    def test_token_is_never_sent_without_encryption(self):
        os.environ["SKYNET_AGENT_API_URL"] = "http://example.invalid"
        ok, info = submit.post_comment("secret", 1, "body")
        self.assertFalse(ok)
        self.assertIn("unencrypted", info)


if __name__ == "__main__":
    unittest.main()
