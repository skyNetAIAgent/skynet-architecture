import hashlib
import unittest

import helpers  # noqa: F401  (puts the agent on sys.path)
from skynet_agent.kernels import REGISTRY, exit_scam_a, lottery_b, selftest
from skynet_agent import worker


class SelfTestKernel(unittest.TestCase):
    def test_digest_is_the_same_everywhere(self):
        result = selftest.run({"rounds": 8}, 0, 1)
        self.assertTrue(result["ok"])
        # Pure integer arithmetic: this value must not depend on the device.
        self.assertEqual(result["digest"],
                         "a2e8f2c45179bfccb6a01d61ab527a86277215a6ee85ff824910fe27d3e9fe26")

    def test_validate(self):
        selftest.validate({"rounds": 4}, 1)
        for params, units in (({"rounds": 0}, 1), ({"rounds": 4}, 2), ({"x": 1}, 1), ({"rounds": True}, 1)):
            with self.assertRaises(ValueError):
                selftest.validate(params, units)


class ExitScamKernel(unittest.TestCase):
    # The example in the network specification: 1000 credits pending, fakes worth 1000
    # more submitted in one batch. The specification gives "about 78", "about 107", "about 17".
    SPEC = {"H0": 1000, "q": [0, 1], "cap_third": False, "batches": 1, "n_max": 1000,
            "sizes": {"mode": "list", "values": [1, 10, 100]}}

    def micro(self, path, params=None):
        num, den = exit_scam_a.evaluate_path(params or self.SPEC, path)
        return num * 10 ** 6 // den

    def test_reproduces_the_specification_table(self):
        self.assertEqual(self.micro([[10, 100]]), 77790311)     # about 78
        self.assertEqual(self.micro([[100, 10]]), 106934126)    # about 107
        self.assertEqual(self.micro([[1000, 1]]), 16784360)     # about 17

    def test_single_fake_loses_three_prices(self):
        # one fake of price r with H pending: expected payout is exactly H - 3r
        num, den = exit_scam_a.evaluate_path(self.SPEC, [[1, 100]])
        self.assertEqual(num, 700 * den)
        num, den = exit_scam_a.evaluate_path(self.SPEC, [[1, 10]])
        self.assertEqual(num, 970 * den)

    def test_rejects_strategies_the_rules_forbid(self):
        with self.assertRaises(ValueError):
            exit_scam_a.evaluate_path(self.SPEC, [[1, 500]])        # price above a third of pending
        capped = dict(self.SPEC, cap_third=True)
        with self.assertRaises(ValueError):
            exit_scam_a.evaluate_path(capped, [[10, 100]])          # batch above a third of pending
        with self.assertRaises(ValueError):
            exit_scam_a.evaluate_path(self.SPEC, [[1001, 1]])       # more than n_max

    def test_units_partition_the_search(self):
        params = {"H0": 300, "q": [1, 2], "cap_third": True, "batches": 2, "n_max": 6,
                  "sizes": {"mode": "grid", "points": 4}}
        whole = exit_scam_a.run(params, 0, 1)
        parts = [exit_scam_a.run(params, u, 5) for u in range(5)]
        self.assertEqual(sum(p["count"] for p in parts), whole["count"])
        self.assertEqual(sum(p["hits"] for p in parts), whole["hits"])
        self.assertEqual(max(p["by_q"][0]["best"]["ev_ppb"] for p in parts if p["by_q"][0]["best"]),
                         whole["by_q"][0]["best"]["ev_ppb"])
        self.assertEqual(len(set(p["digest"] for p in parts)), 5)
        self.assertEqual(exit_scam_a.run(params, 3, 5), parts[3])   # deterministic

    UNIFORM = {"H0": 399, "cap_third": False, "batches": 1, "n_max": 400,
               "sizes": {"mode": "fixed", "r": 1}}

    def test_collusion_boundary_for_leaving(self):
        # 399 prices pending, uniform tasks of price 1 (so the check probability is the 1% floor).
        def run(qn):
            return exit_scam_a.run(dict(self.UNIFORM, q=[qn, 1000]), 0, 1)
        self.assertEqual(run(0)["hits"], 0)
        self.assertEqual(run(890)["hits"], 0)
        hit = run(896)
        self.assertGreater(hit["hits"], 0)
        self.assertGreater(hit["by_q"][0]["best"]["ev_ppb"], 10 ** 9)
        # every reported hit can be confirmed by recomputing that single strategy
        params = dict(self.UNIFORM, q=[896, 1000])
        self.assertEqual(len(hit["by_q"][0]["top_hits"]), exit_scam_a.TOP_HITS)
        for h in hit["by_q"][0]["top_hits"]:
            num, den = exit_scam_a.evaluate_path(params, h["path"])
            self.assertGreater(num, 399 * den)
            self.assertEqual(num * 10 ** 9 // (399 * den), h["ev_ppb"])

    def test_several_collusion_shares_in_one_task(self):
        q_list = [[0, 1], [890, 1000], [896, 1000]]
        sweep = exit_scam_a.run(dict(self.UNIFORM, q_list=q_list), 0, 1)
        self.assertEqual([s["q"] for s in sweep["by_q"]], q_list)
        for entry in sweep["by_q"]:
            single = exit_scam_a.run(dict(self.UNIFORM, q=entry["q"]), 0, 1)["by_q"][0]
            self.assertEqual(entry, single)
        self.assertEqual(sweep["hits"], sweep["by_q"][2]["hits"])
        # units split the whole sweep
        parts = [exit_scam_a.run(dict(self.UNIFORM, q_list=q_list), u, 7) for u in range(7)]
        self.assertEqual(sum(p["count"] for p in parts), sweep["count"])
        self.assertEqual(sum(p["hits"] for p in parts), sweep["hits"])
        # a path must be evaluated for a named share when the task has several
        with self.assertRaises(ValueError):
            exit_scam_a.evaluate_path(dict(self.UNIFORM, q_list=q_list), [[306, 1]])
        num, den = exit_scam_a.evaluate_path(dict(self.UNIFORM, q_list=q_list), [[306, 1]], q=[896, 1000])
        self.assertGreater(num, 399 * den)

    def reference_digest(self, params, unit, units):
        """The same search, written the slow and obvious way with evaluate_path()."""
        h = hashlib.sha256()
        counted = [0]
        ordinal = 0
        for qi, q in enumerate(exit_scam_a.shares(params)):
            rules = exit_scam_a.Rules(params, q)

            def walk(path, pending):
                num, den = exit_scam_a.evaluate_path(params, path, q=q)
                ev_ppb = num * exit_scam_a.PPB // (rules.H0 * den)
                text = ";".join("%d,%d" % tuple(step) for step in path)
                h.update(("%d|%s:%d\n" % (qi, text, ev_ppb)).encode("ascii"))
                counted[0] += 1
                if len(path) < rules.m:
                    for r in rules.sizes_for(pending):
                        for n in range(1, rules.n_limit(pending, r) + 1):
                            walk(path + [(n, r)], pending + n * r)

            for r in rules.sizes_for(rules.H0):
                for n in range(1, rules.n_limit(rules.H0, r) + 1):
                    if ordinal % units == unit:
                        walk([(n, r)], rules.H0 + n * r)
                    ordinal += 1
        return h.hexdigest(), counted[0]

    def test_fast_search_equals_the_obvious_one(self):
        cases = [
            ({"H0": 300, "q": [0, 1], "cap_third": False, "batches": 2, "n_max": 7,
              "sizes": {"mode": "grid", "points": 5}}, 3),
            ({"H0": 399, "q_list": [[0, 1], [9, 10], [896, 1000]], "cap_third": False, "batches": 2,
              "n_max": 9, "sizes": {"mode": "fixed", "r": 1}}, 2),
            ({"H0": 1200, "q": [17, 20], "cap_third": True, "batches": 3, "n_max": 12,
              "sizes": {"mode": "grid", "points": 6}}, 4),
            ({"H0": 5000, "q": [1, 3], "cap_third": False, "batches": 3, "n_max": 3, "safety": 6,
              "p_min_den": 50, "verifiers": 2, "sizes": {"mode": "list", "values": [1, 7, 40, 500, 1600]}}, 1),
            ({"H0": 48, "q": [99, 100], "cap_third": False, "batches": 2, "n_max": 30,
              "sizes": {"mode": "list", "values": [1, 2, 16]}}, 5),
        ]
        for params, units in cases:
            for unit in sorted(set([0, units - 1])):
                result = exit_scam_a.run(params, unit, units)
                digest, counted = self.reference_digest(params, unit, units)
                self.assertEqual(result["count"], counted, params)
                self.assertEqual(result["digest"], digest, params)
                self.assertGreater(counted, 0)

    def test_work_limit(self):
        saved = exit_scam_a.MAX_NODES_PER_UNIT
        exit_scam_a.MAX_NODES_PER_UNIT = 50
        try:
            with self.assertRaises(ValueError):
                exit_scam_a.run({"H0": 1200, "cap_third": True, "batches": 3, "n_max": 12,
                                 "sizes": {"mode": "grid", "points": 6}}, 0, 1)
        finally:
            exit_scam_a.MAX_NODES_PER_UNIT = saved

    def test_validate(self):
        good = {"H0": 1200, "batches": 2, "n_max": 40, "sizes": {"mode": "grid", "points": 12},
                "cap_third": False}
        exit_scam_a.validate(good, 8)
        bad = [
            dict(good, extra=1),
            dict(good, H0=2),
            dict(good, q=[1, 1]),
            dict(good, q=[1.5, 2]),
            dict(good, q=[1, 2], q_list=[[1, 2]]),
            dict(good, q_list=[]),
            dict(good, q_list=[[1, 2], [1, 2]]),
            dict(good, q_list=[[1, 2], [3, 2]]),
            dict(good, batches=4),
            dict(good, sizes={"mode": "grid"}),
            dict(good, sizes={"mode": "list", "values": []}),
            dict(good, cap_third=1),
            dict(good, n_max=5000, sizes={"mode": "grid", "points": 2000}),   # far too large for 8 units
        ]
        for params in bad:
            with self.assertRaises(ValueError):
                exit_scam_a.validate(params, 8)
        # numbers that would not fit into the memory of a small device, however many units
        huge = {"H0": 10 ** 9, "batches": 1, "n_max": 5000, "verifiers": 16, "q": [9999, 10000],
                "sizes": {"mode": "fixed", "r": 1}, "cap_third": True}
        with self.assertRaisesRegex(ValueError, "memory"):
            exit_scam_a.validate(huge, 10 ** 6)
        exit_scam_a.validate(dict(huge, n_max=1500), 10 ** 6)                # the same question, smaller
        with self.assertRaises(ValueError):
            exit_scam_a.run(good, 8, 8)                                      # unit out of range


class LotteryKernel(unittest.TestCase):
    def test_known_cells(self):
        # one task, checked with probability 1/2: nothing is paid half of the time
        self.assertEqual(lottery_b.cell(1, 2, 1, 1, 1), (500000000, 500000000, 500000000))
        # 6000 tasks a month, 1% checked, cost 95% of the price: a losing month about one in three
        loss, half, zero = lottery_b.cell(6000, 100, 95, 100, 1)
        self.assertEqual(loss, 331000837)
        self.assertEqual(zero, 0)
        self.assertLess(half, loss)
        # a quarter is smoother than a month
        self.assertLess(lottery_b.cell(6000, 100, 95, 100, 3)[0], loss)

    def test_run_and_partition(self):
        params = {"tasks": [600, 6000], "check_one_in": [10, 100], "costs": [[1, 2], [95, 100]],
                  "months": [1, 3]}
        whole = lottery_b.run(params, 0, 1)
        self.assertEqual(len(whole["rows"]), 16)
        parts = [lottery_b.run(params, u, 3) for u in range(3)]
        self.assertEqual(sorted(sum((p["rows"] for p in parts), [])), sorted(whole["rows"]))
        self.assertEqual(lottery_b.run(params, 1, 3), parts[1])

    def test_validate(self):
        good = {"tasks": [600], "check_one_in": [100], "costs": [[95, 100]], "months": [1]}
        lottery_b.validate(good, 1)
        for params in (dict(good, tasks=[]), dict(good, costs=[[3, 2]]), dict(good, months=[0]),
                       dict(good, tasks=[3000000], months=[2]), dict(good, x=1),
                       dict(good, tasks=[600, 600])):
            with self.assertRaises(ValueError):
                lottery_b.validate(params, 1)


class WorkerTest(unittest.TestCase):
    def test_runs_a_job_and_reports_errors(self):
        ok = worker.run_job({"kernel": "selftest", "kernel_version": 1, "params": {"rounds": 2},
                             "unit": 0, "units": 1})
        self.assertTrue(ok["ok"])
        self.assertIn("digest", ok["result"])
        for job in ({"kernel": "nope", "kernel_version": 1, "params": {}, "unit": 0, "units": 1},
                    {"kernel": "selftest", "kernel_version": 2, "params": {}, "unit": 0, "units": 1},
                    {"kernel": "selftest", "kernel_version": 1, "params": {"rounds": 0}, "unit": 0, "units": 1}):
            self.assertFalse(worker.run_job(job)["ok"])

    def test_every_kernel_has_the_required_interface(self):
        for name, module in REGISTRY.items():
            self.assertIsInstance(module.VERSION, int, name)
            self.assertIn(module.KIND, ("compute", "ai"), name)
            self.assertTrue(callable(module.validate) and callable(module.run), name)


if __name__ == "__main__":
    unittest.main()
