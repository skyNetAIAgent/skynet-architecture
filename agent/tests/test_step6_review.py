"""Reviewer's independent checks for the four stage-6 kernels.

Every quantity is recomputed with a method that differs from both the kernel
and the implementer's own tests:
  * exit-campaign-b: memoised recursion over (pending, waves) with an
    explicit zero-risk idle action and a binomial success distribution, plus
    a full enumeration of per-fake outcomes for a tiny instance;
  * apprentice-seats: exact hypergeometric pmf sums over all coalition seat
    counts (the kernel uses the first-moment shortcut);
  * lottery-adaptive: direct pmf sums over all X values;
  * token-certificate: an independent SHA-256 row generator, an independent
    full argmax and an independent count of reads and multiplications,
    brute-forced over every possible claim.

The file also checks the spec's mandatory campaign properties, cross-platform
safety (no floats, no hash(), no wall-clock input), JSON determinism across
repeated runs, the task index volume, and that a seq-4 agent skips the new
tasks.
"""

import ast
import json
import math
import struct
import unittest
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from unittest.mock import patch

import helpers
from skynet_agent import tasks
from skynet_agent.kernels import (REGISTRY, apprentice_seats, exit_campaign_b,
                                  lottery_adaptive, token_certificate)


CAMPAIGN = dict(H0=[0, 25, 100], p=[[1, 10], [1, 50]],
                q=[[0, 1], [1, 4], [1, 2], [2, 3], [3, 4], [4, 5],
                   [9, 10], [19, 20], [1, 1]],
                k=[1, 3], C=[4, 32], T=[3, 12])
SEATS = dict(S=[8, 64, 256], n=[0, 32, 128, 1024], m=[0, 2048, 64],
             f=[[1, 10], [1, 2], [1, 1]], E=30)
LOTTERY = dict(N=[30, 60, 119, 120, 300, 599, 600, 1200, 1800],
               P=[1, 2, 5, 10, 16], R=1, c=[[4, 5], [19, 20], [49, 50]], k=3)
TOKEN = dict(shapes=[[32000, 1024, 8], [150000, 4096, 1]],
             weights=[-8, 7], seed=0, seeds=10)


def parse_big(text):
    """Decimal string -> int without touching the interpreter's digit cap."""
    value = 0
    for i in range(0, len(text), 500):
        part = text[i:i + 500]
        value = value * 10 ** len(part) + int(part)
    return value


def same_fraction(text, fraction):
    num, den = text.split("/")
    return parse_big(num) * fraction.denominator == parse_big(den) * fraction.numerator


class CampaignReview(unittest.TestCase):
    """exit-campaign-b against an independent memoised recursion."""

    @staticmethod
    def dp(h, p, q, k, cap, waves):
        win, miss = p * q ** k, 1 - p
        memo = {}

        def value(pending, left):
            key = (pending, left)
            if key in memo:
                return memo[key]
            if left == 0:
                memo[key] = (pending, 0)
                return memo[key]
            best, action = pending, 0
            idle, _ = value(pending, left - 1)   # zero fakes, zero risk
            if idle > best:
                best, action = idle, -1
            for n in range(1, cap + 1):
                total = F(0)
                for s in range(n + 1):
                    prob = F(math.comb(n, s)) * win ** s * miss ** (n - s)
                    total += prob * value(pending + F(s, p), left - 1)[0]
                if total > best:
                    best, action = total, n
            memo[key] = (best, action)
            return memo[key]

        return value(h, waves)

    def test_independent_points(self):
        for h, p, q, k, c, t in [
                (0, F(1, 10), F(9, 10), 3, 4, 3),
                (25, F(1, 50), F(19, 20), 1, 32, 3),
                (100, F(1, 10), F(1, 2), 1, 4, 4),
                (7, F(2, 5), F(1), 2, 6, 3),
                (3, F(2, 3), F(0), 2, 4, 5),
                (0, F(1, 3), F(2, 3), 2, 8, 4)]:
            with self.subTest(h=h, p=p, q=q, k=k, C=c, T=t):
                expected = self.dp(h, p, q, k, c, t)
                self.assertEqual(exit_campaign_b.optimum(h, p, q, k, c, t),
                                 (expected[0] - h, expected[1]))

    def test_full_outcome_enumeration(self):
        # Any caught fake zeroes the whole wave and the campaign; stop pays
        # the pending amount; every checked fake adds R/p = 1/p.
        h, p, q, k = 1, F(2, 3), F(3, 4), 1
        chances = [1 - p, p * q ** k, p * (1 - q ** k)]

        def brute(pending, left):
            if left == 0:
                return pending, 0
            best, action = pending, 0
            for n in range(1, 3):
                total = F(0)
                for outcomes in product(range(3), repeat=n):
                    if 2 in outcomes:
                        continue
                    later, _ = brute(pending + F(outcomes.count(1), p), left - 1)
                    total += math.prod(chances[i] for i in outcomes) * later
                if total > best:
                    best, action = total, n
            return best, action

        expected = brute(h, 2)
        self.assertEqual(exit_campaign_b.optimum(h, p, q, k, 2, 2),
                         (expected[0] - h, expected[1]))

    def test_mandatory_properties_on_published_grid(self):
        # q = 0: never profitable, any parameters.
        for h, p, k, c, t in product([0, 25, 100], [F(1, 10), F(1, 50)],
                                     [1, 3], [4, 32], [3, 12]):
            self.assertLessEqual(exit_campaign_b.optimum(h, p, F(0), k, c, t)[0], 0)
        # H0 = 0, C = 1, T = 1: gain equals R * q^k = q^k.
        for q, k in product([F(1, 4), F(2, 3), F(9, 10), F(1)], [1, 3]):
            self.assertEqual(exit_campaign_b.optimum(0, F(1, 10), q, k, 1, 1)[0], q ** k)
        # q = 1: the gain grows with C.
        for cap in range(1, 5):
            gain, first = exit_campaign_b.optimum(17, F(2, 5), F(1), 2, cap, 3)
            self.assertEqual((gain, first), (3 * cap, cap))

    def test_determinism_and_json_types(self):
        a = exit_campaign_b.run(CAMPAIGN, 0, 432)
        b = exit_campaign_b.run(CAMPAIGN, 0, 432)
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))
        self.assertEqual(a["first_wave"], 0)
        self.assertFalse(a["profitable"])          # q=0 at unit 0
        self.assertEqual(a["gain"], "0/1")


class SeatsReview(unittest.TestCase):
    """apprentice-seats against exact hypergeometric sums."""

    @staticmethod
    def expected(seats, n, m, f, epochs):
        draws = min(seats, n + m)
        if n + m == 0:
            return F(0), F(0), F(0), F(1)
        if draws == 0:
            return F(0), F(0), F(0), F(1)
        den = math.comb(n + m, draws)
        total = F(0)
        for j in range(draws + 1):
            total += F(j) * F(math.comb(m, j) * math.comb(n, draws - j), den)
        leak = total * f
        return leak, leak * epochs, F(n, n + m), F(math.comb(m, draws), den)

    def test_pmf_sums(self):
        for seats, n, m, f in product(range(5), repeat=4):
            rows = apprentice_seats.run(
                dict(S=[seats], n=[n], m=[m, m, 1], f=[[f, 5]], E=7), 0, 1)["rows"]
            leak, total, share, none = self.expected(seats, n, m, F(f, 5), 7)
            row = rows[0]
            self.assertEqual(F(row[1]), leak)
            self.assertEqual(F(row[2]), total)
            self.assertEqual(F(row[3]), share)
            self.assertEqual(F(row[4]), none)

    def test_grid_invariants(self):
        rows = apprentice_seats.run(dict(SEATS, S=[64], n=[128], f=[[1, 2]]), 0, 1)["rows"]
        shares = [F(row[3]) for row in rows]
        self.assertTrue(all(a >= b for a, b in zip(shares, shares[1:])))
        self.assertTrue(all(F(row[1]) <= 64 * F(1, 2) for row in rows))
        self.assertTrue(all(F(row[1]) == 0 for row in rows if row[0] == 0))
        # The honest share is exactly n/(n+m).
        self.assertTrue(all(F(row[3]) == F(128, 128 + row[0]) for row in rows))

    def test_determinism(self):
        a = apprentice_seats.run(SEATS, 0, 36)
        b = apprentice_seats.run(SEATS, 0, 36)
        self.assertEqual(a, b)
        self.assertEqual(len(a["rows"]), 33)


class LotteryReview(unittest.TestCase):
    """lottery-adaptive against direct pmf sums and the FIRST_RUN row."""

    @staticmethod
    def expected(n, p, cost):
        loss = zero = 0
        for x in range(n + 1):
            weight = math.comb(n, x) * (p - 1) ** (n - x)
            if x == 0:
                zero += weight
            if x * p < n * cost:
                loss += weight
        return F(loss, p ** n), F(zero, p ** n)

    def test_pmf_sums(self):
        for n, p, c in [(600, 10, F(19, 20)), (119, 1, F(4, 5)),
                        (1800, 16, F(49, 50)), (300, 5, F(4, 5))]:
            res = lottery_adaptive.run(
                dict(N=[n], P=[p], R=1, c=[[c.numerator, c.denominator]], k=3), 0, 1)
            ml, mz = self.expected(n, p, c)
            ql, qz = self.expected(3 * n, p, c)
            self.assertTrue(same_fraction(res["month"]["loss"], ml))
            self.assertTrue(same_fraction(res["month"]["zero"], mz))
            self.assertTrue(same_fraction(res["quarter"]["loss"], ql))
            self.assertTrue(same_fraction(res["quarter"]["zero"], qz))

    def test_first_run_row(self):
        res = lottery_adaptive.run(dict(N=[600], P=[10], R=1, c=[[19, 20]], k=3), 0, 1)
        self.assertEqual(res["p"], "1/10")
        self.assertEqual(res["recomputations"], "180/1")   # k*N*p = 3*600/10
        self.assertEqual(round(F(res["month"]["loss"]) * 10000), 3220)     # 32.20%
        self.assertEqual(round(F(res["quarter"]["loss"]) * 10000), 2291)   # 22.91%

    def test_unreachable_and_determinism(self):
        res = lottery_adaptive.run(
            dict(N=[30], P=[1, 2, 5, 10, 16], R=1, c=[[19, 20]], k=3), 0, 1)
        self.assertFalse(res["reachable"])
        self.assertEqual(set(res), {"kernel", "N", "c", "R", "k", "reachable"})
        a = lottery_adaptive.run(LOTTERY, 26, 27)
        b = lottery_adaptive.run(LOTTERY, 26, 27)
        self.assertEqual(a, b)
        self.assertEqual(a["N"], 1800)
        self.assertEqual(a["p"], "1/16")


class TokenReview(unittest.TestCase):
    """token-certificate: independent generator, argmax and op counting."""

    @staticmethod
    def table(lo, hi):
        return bytes((lo + i * (hi - lo + 1) // 256) % 256 for i in range(256))

    @staticmethod
    def rows(seed, tag, index, dim, lo, hi, table):
        import hashlib
        prefix = tag + struct.pack(">II", seed, index)
        data = b"".join(hashlib.sha256(prefix + struct.pack(">I", i)).digest()
                        for i in range((dim + 31) // 32))
        return [table[b] - 256 if table[b] >= 128 else table[b] for b in data[:dim]]

    def test_small_instance(self):
        lo, hi, seed, v, d, count = -2, 3, 42, 260, 4, 3
        table = self.table(lo, hi)
        weights = [self.rows(seed, b"W", i, d, lo, hi, table) for i in range(v)]
        queries = [self.rows(seed, b"h", j, d, lo, hi, table) for j in range(count)]
        self.assertTrue(all(lo <= x <= hi for row in weights + queries for x in row))

        winners = []
        for h in queries:
            best, index = None, None
            for i, w in enumerate(weights):
                score = sum(a * b for a, b in zip(w, h))
                if best is None or score > best:
                    best, index = score, i
            winners.append(index)
        root, leaves, reported = token_certificate.index_and_claims(
            weights.__getitem__, v, queries)
        self.assertEqual(reported, winners)

        for j, h in enumerate(queries):
            norm = max(map(abs, h))
            true = winners[j]
            for claim in range(v):
                winner, reads, mults = token_certificate.verify(
                    weights.__getitem__, root, leaves, h, claim)
                self.assertEqual(winner, true)
                score = sum(a * b for a, b in zip(weights[claim], h))
                my_reads, my_bounds = 1, 1
                if (sum(a * b for a, b in zip(root[0], h)) + root[1] * norm >= score):
                    for centre, radius, first, end in leaves:
                        my_bounds += 1
                        if sum(a * b for a, b in zip(centre, h)) + radius * norm >= score:
                            for i in range(first, end):
                                if i != claim:
                                    my_reads += 1
                self.assertEqual((reads, mults),
                                 (my_reads, my_reads * d + my_bounds * (d + 1)))

    def test_known_instance_and_determinism(self):
        a = token_certificate.run(dict(shapes=[[260, 4, 3]], weights=[-2, 3],
                                       seed=42, seeds=1), 0, 1)
        b = token_certificate.run(dict(shapes=[[260, 4, 3]], weights=[-2, 3],
                                       seed=42, seeds=1), 0, 1)
        self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True))
        self.assertEqual(a["winners"], [221, 151, 25])
        self.assertEqual(a["verify_mults"], 3180)
        self.assertEqual(a["full_mults"], 3120)


class PlatformSafety(unittest.TestCase):
    """The four kernels must not depend on floats, hash(), dict order or time."""

    def test_no_risky_constructs_in_sources(self):
        roots = [Path(helpers.REPO_ROOT, "agent", "skynet_agent", "kernels")]
        banned = ["float", "random", "hash(", "time.time", "time.monotonic",
                  "os.environ", "locale", "socket"]
        for module in ["exit_campaign_b", "apprentice_seats", "lottery_adaptive",
                       "token_certificate", "_grid"]:
            text = Path(roots[0], module + ".py").read_text(encoding="utf-8")
            for token in banned:
                self.assertNotIn(token, text, (module, token))

    def test_results_use_only_int_and_fraction_strings(self):
        for module, params, units, unit in [
                (exit_campaign_b, CAMPAIGN, 432, 423),
                (apprentice_seats, SEATS, 36, 35),
                (lottery_adaptive, LOTTERY, 27, 26)]:
            result = module.run(params, unit, units)
            for value in json.loads(json.dumps(result)).values():
                if isinstance(value, list):
                    for row in value:
                        for cell in row:
                            self.assertIn(type(cell), (int, str))


class IndexReview(unittest.TestCase):
    """Task list volume, preservation, and old-agent gating."""

    def test_index_structure(self):
        index = json.loads(Path(helpers.REPO_ROOT, "tasks", "index.json").read_text())
        task_list = tasks.validate_index(index)
        self.assertEqual(index["seq"], 2)
        self.assertEqual(len(task_list), 13)
        new = [t for t in task_list if t.get("min_agent_seq") == 5]
        self.assertEqual([t["kernel"] for t in new],
                         ["exit-campaign-b", "apprentice-seats",
                          "lottery-adaptive", "token-certificate"])
        self.assertEqual(sum(t["units"] for t in new), 515)
        self.assertTrue(300 <= 515 <= 1000)
        self.assertTrue(all("issue" not in t for t in new))

        self.assertEqual([t["id"] for t in task_list[:9]][0], "selftest-1")   # list 1 kept in front

    def test_old_agent_skips_new_tasks(self):
        index = json.loads(Path(helpers.REPO_ROOT, "tasks", "index.json").read_text())
        new = [t for t in tasks.validate_index(index) if t.get("min_agent_seq") == 5]
        old = {k: REGISTRY[k] for k in
               ["selftest", "exit-scam-a", "lottery-b", "ai-answer"]}
        with patch.object(tasks, "RELEASE_SEQ", 4), patch.object(tasks, "REGISTRY", old):
            self.assertIsNone(tasks.pick({"tasks": new}, {}, {}))
            for task in new:
                self.assertIn("newer agent", tasks.usable(task, {}))
        with patch.object(tasks, "RELEASE_SEQ", 5):
            for task in new:
                self.assertIsNone(tasks.usable(task, {}))

    def test_grid_volume_matches_parameters(self):
        self.assertEqual(
            math.prod(len(CAMPAIGN[k]) for k in ["H0", "p", "q", "k", "C", "T"]), 432)
        self.assertEqual(math.prod(len(SEATS[k]) for k in ["S", "n", "f"]), 36)
        self.assertEqual(len(LOTTERY["N"]) * len(LOTTERY["c"]), 27)
        self.assertEqual(len(TOKEN["shapes"]) * TOKEN["seeds"], 20)


if __name__ == "__main__":
    unittest.main()
