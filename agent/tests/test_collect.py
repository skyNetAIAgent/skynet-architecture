import json
import os
import shutil
import sys
import tempfile
import unittest

import helpers
from skynet_agent import submit
from skynet_agent.kernels import exit_scam_a, lottery_b, selftest

sys.path.insert(0, os.path.join(helpers.REPO_ROOT, "tools"))
import collect_results  # noqa: E402

UNIFORM = {"H0": 399, "cap_third": False, "batches": 1, "n_max": 400,
           "sizes": {"mode": "fixed", "r": 1}, "q_list": [[890, 1000], [896, 1000]]}
INDEX = {"format": 1, "seq": 4, "tasks": [
    {"id": "selftest-1", "kernel": "selftest", "kernel_version": 1, "units": 1, "issue": 5,
     "params": {"rounds": 2}, "redundancy": 2},
    {"id": "exit-uniform", "kernel": "exit-scam-a", "kernel_version": 1, "units": 2, "issue": 6,
     "params": UNIFORM, "redundancy": 2},
    {"id": "ask-1", "kernel": "ai-answer", "kernel_version": 1, "units": 1, "issue": 7,
     "params": {"question": "Find an attack."}},
]}


def comment(author, task, unit, result, text_kind="compute"):
    record, text = submit.make_record(task, unit, {"ok": True, "elapsed_s": 1, "result": result}, {})
    return {"author": author, "body": submit.format_comment(record, text), "url": "https://example.invalid/c"}


class CollectResults(unittest.TestCase):
    def setUp(self):
        self_task, exit_task, ai_task = INDEX["tasks"]
        good_self = selftest.run({"rounds": 2}, 0, 1)
        unit0 = exit_scam_a.run(UNIFORM, 0, 2)
        unit1 = exit_scam_a.run(UNIFORM, 1, 2)
        forged = json.loads(json.dumps(unit1))
        forged["by_q"][0]["top_hits"] = [{"ev_ppb": 2 * 10 ** 9, "path": [[5, 1]]}]   # a false "hit"
        forged["hits"] = 1
        batch = submit.format_batch([
            submit.make_record(self_task, 0, {"ok": True, "elapsed_s": 1, "result": good_self}, {})[0],
            submit.make_record(exit_task, 0, {"ok": True, "elapsed_s": 1, "result": unit0}, {})[0],
        ])
        self.batch_comment = {"author": "bob", "body": batch, "url": "https://example.invalid/b"}
        self.comments = [
            comment("alice", self_task, 0, good_self),
            comment("bob", self_task, 0, good_self),
            comment("alice", exit_task, 0, unit0),
            comment("alice", exit_task, 0, unit0),            # the same person twice counts once
            comment("alice", exit_task, 1, unit1),
            comment("mallory", exit_task, 1, forged),         # disagrees with alice
            comment("carol", ai_task, 0, {"kernel": "ai-answer@1", "model": "m", "output": "An idea."}),
            {"author": "dave", "body": "nice project!", "url": ""},
            {"author": "eve", "body": submit.MARKER + "\n```json\n{\"v\": 1}\n```\n", "url": ""},
            comment("frank", dict(exit_task, id="unknown-task"), 0, unit0),
        ]

    def test_grouping_confirmation_conflicts_and_hits(self):
        grouped, rejected = collect_results.collect(INDEX, self.comments)
        self.assertEqual(rejected, 2)                          # eve's malformed one and the unknown task
        coverage, summary = collect_results.summarise(INDEX, grouped)
        self.assertEqual(coverage["selftest-1"], {"0": 2})
        self.assertEqual(summary["selftest-1"]["units_confirmed"], 1)
        self.assertEqual(coverage["exit-uniform"], {"0": 1, "1": 1})
        entry = summary["exit-uniform"]
        self.assertEqual(entry["units_confirmed"], 0)          # one account is not a confirmation
        self.assertEqual([c["unit"] for c in entry["conflicts"]], [1])
        # real hits exist only for the share 0.896, and the forged hit did not survive recomputation
        self.assertTrue(entry["verified_hits"])
        self.assertTrue(all(h["q"] == [896, 1000] for h in entry["verified_hits"]))
        self.assertEqual(entry["lowest_q_with_hit"], [896, 1000])
        self.assertEqual([b["q"] for b in entry["best_by_q"]], [[890, 1000], [896, 1000]])
        self.assertEqual(summary["ask-1"]["answers"], 1)

    def test_a_comment_with_several_results(self):
        grouped, rejected = collect_results.collect(INDEX, self.comments + [self.batch_comment])
        self.assertEqual(rejected, 2)
        coverage, summary = collect_results.summarise(INDEX, grouped)
        self.assertEqual(coverage["selftest-1"], {"0": 2})          # bob twice still counts once
        self.assertEqual(coverage["exit-uniform"]["0"], 2)          # alice and bob now agree on unit 0
        self.assertEqual(summary["exit-uniform"]["units_confirmed"], 1)

    def test_lottery_table_is_merged(self):
        params = {"tasks": [600, 6000], "check_one_in": [100], "costs": [[95, 100]], "months": [1, 3]}
        task = {"id": "lottery", "kernel": "lottery-b", "kernel_version": 1, "units": 2, "issue": 8,
                "params": params}
        index = {"format": 1, "seq": 5, "tasks": [task]}
        comments = [comment("alice", task, u, lottery_b.run(params, u, 2)) for u in range(2)]
        grouped, rejected = collect_results.collect(index, comments)
        self.assertEqual(rejected, 0)
        _, summary = collect_results.summarise(index, grouped)
        rows = summary["lottery"]["rows"]
        self.assertEqual(len(rows), 4)
        self.assertEqual(rows, sorted(lottery_b.run(params, 0, 1)["rows"]))
        self.assertIn([6000, 100, 95, 100, 1, 331000837], [r[:6] for r in rows])

    def test_writes_files(self):
        tmp = tempfile.mkdtemp(prefix="skynet-test-")
        try:
            os.makedirs(os.path.join(tmp, "tasks"))
            with open(os.path.join(tmp, "tasks", "index.json"), "w", encoding="utf-8") as f:
                json.dump(INDEX, f)
            source = os.path.join(tmp, "comments.json")
            with open(source, "w", encoding="utf-8") as f:
                json.dump(self.comments, f)
            self.assertEqual(collect_results.main(["--root", tmp, "--from", source]), 0)
            with open(os.path.join(tmp, "results", "coverage.json"), encoding="utf-8") as f:
                self.assertEqual(json.load(f)["selftest-1"], {"0": 2})
            with open(os.path.join(tmp, "results", "REPORT.md"), encoding="utf-8") as f:
                report = f.read()
            self.assertIn("CONFLICT in exit-uniform unit 1", report)
            self.assertIn("Lowest collusion share with a verified hit so far: 896/1000", report)
            with open(os.path.join(tmp, "results", "ai", "ask-1.md"), encoding="utf-8") as f:
                self.assertIn("An idea.", f.read())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
