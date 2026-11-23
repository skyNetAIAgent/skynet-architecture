"""Independent finite-outcome checks for the four stage 2 models."""

import json
import unittest
from fractions import Fraction as F
from itertools import combinations, product
from math import prod
from pathlib import Path
from unittest.mock import patch

import helpers
from skynet_agent import records, submit, tasks, worker
from skynet_agent.kernels import (REGISTRY, apprentice_seats, exit_campaign_b,
                                  lottery_adaptive, lottery_b, token_certificate)


CAMPAIGN = dict(H0=[0], p=[[2, 3]], q=[[3, 4]], k=[2], C=[2], T=[2])
SEATS = dict(S=[2], n=[3], m=[0, 4, 1], f=[[2, 3]], E=5)
LOTTERY = dict(N=[600], P=[11, 3, 10], R=7, c=[[19, 20]], k=3)
TOKEN = dict(shapes=[[260, 4, 3]], weights=[-2, 3], seed=42, seeds=1)


def campaign_tree(h, p, q, k, cap, t):
    best = (h, 0)
    if t:
        chances = [1 - p, p * q ** k, p * (1 - q ** k)]
        for n in range(1, cap + 1):
            value = F(0)
            for outcomes in product(range(3), repeat=n):
                if 2 not in outcomes:
                    pending = h + F(outcomes.count(1), p)
                    later, _ = campaign_tree(pending, p, q, k, cap, t - 1)
                    value += prod(chances[i] for i in outcomes) * later
            if value > best[0]:
                best = value, n
    return best


class Campaign(unittest.TestCase):
    def test_all_wave_outcomes_and_decisions(self):
        for h, p, q, k in product([0, 1, 3], [F(2, 3), F(1)], [F(0), F(3, 4), F(1)], [1, 2]):
            with self.subTest(h=h, p=p, q=q, k=k):
                payout, first = campaign_tree(h, p, q, k, 2, 2)
                self.assertEqual(exit_campaign_b.optimum(h, p, q, k, 2, 2), (payout - h, first))

    def test_boundary_policies(self):
        p = F(2, 5)
        for h, cap, t in product([0, 7, 50], [0, 1, 3], [0, 1, 4]):
            self.assertEqual(exit_campaign_b.optimum(h, p, F(0), 3, cap, t), (0, 0))
        for q in [F(0), F(1, 7), F(1)]:
            self.assertEqual(exit_campaign_b.optimum(0, p, q, 3, 1, 1)[0], q ** 3)
        for cap in range(1, 5):
            self.assertEqual(exit_campaign_b.optimum(17, p, F(1), 2, cap, 3), (3 * cap, cap))


class ApprenticeSeats(unittest.TestCase):
    def test_all_seat_allocations(self):
        for seats, n in product(range(5), repeat=2):
            res = apprentice_seats.run(dict(SEATS, S=[seats], n=[n]), 0, 1)
            for m, epoch, total, honest, none in res["rows"]:
                draws = min(seats, n + m)
                counts = [sum(i >= n for i in group)
                          for group in combinations(range(n + m), draws)]
                expected = F(sum(counts), len(counts)) * F(2, 3)
                self.assertEqual(F(epoch), expected)
                self.assertEqual(F(total), 5 * expected)
                self.assertEqual(F(none), F(counts.count(draws), len(counts)))
                share = F(sum(draws - j for j in counts), draws * len(counts)) if draws else 0
                self.assertEqual(F(honest), share)
                self.assertLessEqual(F(epoch), seats * F(2, 3))
                if not m:
                    self.assertEqual(F(epoch), 0)

    def test_many_coalition_keys(self):
        rows = apprentice_seats.run(dict(SEATS, m=[0, 1000000, 50000]), 0, 1)["rows"]
        shares = [F(row[3]) for row in rows]
        self.assertTrue(all(a > b for a, b in zip(shares, shares[1:])))
        self.assertLess(shares[-1], F(1, 100000))


class AdaptiveLottery(unittest.TestCase):
    def test_every_draw(self):
        for n, p, c in product(range(6), [1, 2, 3], [F(0), F(2, 3), F(1)]):
            # Each of the p equiprobable labels is equally likely at each trial.
            hits = [outcomes.count(0) for outcomes in product(range(p), repeat=n)]
            self.assertEqual(lottery_adaptive.period(n, p, c),
                             (F(sum(x * p < n * c for x in hits), len(hits)),
                              F(hits.count(0), len(hits))))

    def test_first_run_and_grid_selection(self):
        res = lottery_adaptive.run(LOTTERY, 0, 1)
        self.assertEqual((res["p"], res["recomputations"]), ("1/10", "180/1"))
        for name, months, basis_points in [("month", 1, 3220), ("quarter", 3, 2291)]:
            loss, zero = (F(res[name][key]) for key in ("loss", "zero"))
            ppb, _, zero_ppb = lottery_b.cell(600, 10, 19, 20, months)
            self.assertEqual((loss * 10 ** 9 // 1, zero * 10 ** 9 // 1), (ppb, zero_ppb))
            self.assertEqual(round(loss * 10000), basis_points)
        self.assertFalse(lottery_adaptive.run(dict(LOTTERY, N=[59], P=[1, 2]), 0, 1)["reachable"])
        self.assertEqual(lottery_adaptive.run(dict(LOTTERY, R=1), 0, 1)["month"], res["month"])

    def test_long_fractions_fit_a_result_record(self):
        task = dict(id="adaptive", units=1, kernel="lottery-adaptive", kernel_version=1)
        params = dict(LOTTERY, N=[1800], P=[16])
        res = lottery_adaptive.run(params, 0, 1)
        num, den = res["quarter"]["zero"].split("/")
        self.assertGreater(len(den), 4300)
        # Parse by chunks without changing the interpreter's conversion limit.
        for s, expected in [(num, 15 ** 5400), (den, 16 ** 5400)]:
            value = 0
            for i in range(0, len(s), 500):
                part = s[i:i + 500]
                value = value * 10 ** len(part) + int(part)
            self.assertEqual(value, expected)
        record, _ = submit.make_record(task, 0, {"result": res}, {})
        envelope = records.make(bytes(32), "result", {"record": record}, created=1)
        self.assertLess(len(records.wire(envelope)), records.MAX_WIRE_BYTES)


class TokenCertificate(unittest.TestCase):
    def test_all_small_matrices_queries_and_claims(self):
        with patch.object(token_certificate, "LEAF", 2):
            for weights in product([-1, 0, 1], repeat=4):
                rows = [(w,) for w in weights]
                queries = [(-1,), (0,), (1,)]
                root, leaves, winners = token_certificate.index_and_claims(rows.__getitem__, 4, queries)
                for h, winner in zip(queries, winners):
                    expected = max(range(4), key=lambda i: weights[i] * h[0])
                    self.assertEqual(winner, expected)
                    for claim in range(4):
                        actual, _, _ = token_certificate.verify(rows.__getitem__, root, leaves, h, claim)
                        self.assertEqual(actual, expected)

    def test_pruning_and_tied_upper_bound(self):
        rows = [(-8,)] * 128 + [(5,)] * 129
        root, leaves, winners = token_certificate.index_and_claims(rows.__getitem__, 257, [(1,)])
        self.assertEqual(root, ((-8,), 13))
        self.assertEqual(winners, [128])
        accesses = []

        def read(i):
            accesses.append(i)
            return rows[i]

        self.assertEqual(token_certificate.verify(read, root, leaves, (1,), 256), (128, 129, 137))
        self.assertEqual(sorted(accesses), list(range(128, 257)))

    def test_generated_instance(self):
        res = token_certificate.run(TOKEN, 0, 1)
        self.assertEqual(res["winners"], [221, 151, 25])
        self.assertEqual((res["verify_mults"], res["full_mults"], res["verify_over_full"]),
                         (3180, 3120, "53/52"))


class Integration(unittest.TestCase):
    def test_worker_determinism_and_validation(self):
        for name, params, bad in [
                ("exit-campaign-b", CAMPAIGN, [dict(p=[[0, 1]]), dict(q=[[2, 1]]), dict(C=[False])]),
                ("apprentice-seats", SEATS, [dict(m=[3, 2, 1]), dict(m=[0, 1, 0]), dict(f=[[1, 0]])]),
                ("lottery-adaptive", LOTTERY, [dict(P=[0]), dict(R=0), dict(c=[[1, 2], [2, 4]])]),
                ("token-certificate", TOKEN, [dict(shapes=[[0, 1, 1]]), dict(weights=[3, -2]), dict(seed=-1)])]:
            job = dict(kernel=name, kernel_version=1, unit=0, units=1, params=params)
            a = worker.run_job(job)
            self.assertTrue(a["ok"], a)
            b = worker.run_job(job)["result"]
            self.assertEqual(json.dumps(a["result"], sort_keys=True), json.dumps(b, sort_keys=True))
            for change in bad + [dict(extra=1)]:
                with self.subTest(kernel=name, change=change), self.assertRaises(ValueError):
                    REGISTRY[name].validate(dict(params, **change), 1)
            for unit, units in [(0, 2), (1, 1), (False, 1)]:
                with self.assertRaises(ValueError):
                    REGISTRY[name].run(params, unit, units)

    def test_seq2_and_older_agent(self):
        index = json.loads(Path(helpers.REPO_ROOT, "tasks/index.json").read_bytes())
        new = [t for t in tasks.validate_index(index) if t.get("min_agent_seq") == 5]
        self.assertEqual(index["seq"], 2)
        self.assertEqual({t["kernel"] for t in new}, {
            "exit-campaign-b", "apprentice-seats", "lottery-adaptive", "token-certificate"})
        with patch.object(tasks, "RELEASE_SEQ", 5):
            for t in new:
                self.assertIsNone(tasks.usable(t, {}))
        old = {k: REGISTRY[k] for k in ["selftest", "exit-scam-a", "lottery-b", "ai-answer"]}
        with patch.object(tasks, "RELEASE_SEQ", 4), patch.object(tasks, "REGISTRY", old):
            self.assertIsNone(tasks.pick({"tasks": new}, {}, {}))
            for t in new:
                self.assertIn("newer agent", tasks.usable(t, {}))
                self.assertIn("unknown kernel", tasks.usable(dict(t, min_agent_seq=4), {}))
