"""exit-scam-a@1: can a leaving participant profit from a burst of fake results?

Research question (docs/CURRENT_DESIGN.md, section 3, variant A; open question Q1).
A participant with H0 credits "pending" decides to leave. Just before leaving
they submit fake results in up to `batches` batches, fast enough that no check
finishes in between. If they simply left, they would receive H0. The design
claims that faking never pays while colluders hold less than about 91% of the
verifiers' weight. This kernel searches a family of strategies for a
counterexample, in exact integer arithmetic, so every device gets the same
answer bit for bit.

Model (all amounts are integers in minimal credit units):

  * Batch b holds n_b fake tasks of price r_b each.
  * Pending amount seen by the rules when batch b is submitted:
        H_b = H0 + sum of n_j * r_j over earlier batches j < b
    (earlier fake rewards are pending and not yet checked).
  * A task is only given if 3 * r_b <= H_b. With cap_third, additionally
    3 * n_b * r_b <= H_b ("at most a third of the pending amount in work").
  * Check probability   p_b = min(1, max(1/p_min_den, safety*r_b / (r_b + H_b))).
  * A checked fake is caught unless all `verifiers` verifiers collude:
        detection probability per fake = p_b * (1 - q**verifiers),
    where q is the colluders' share of the verifiers' weight.
  * A caught fake earns nothing and burns B_b = safety*r_b/p_b - r_b,
    but the total burned never exceeds what is pending.
  * Final payout = max(0, T - sum of k_b * c_b), where k_b is the number of
    caught fakes in batch b, T = H0 + sum n_b*r_b, and c_b = safety*r_b/p_b
    (the lost reward plus the burn).

A strategy is a "hit" if its expected payout is strictly greater than H0.
The second line of defence (anyone may recompute and challenge) and the cost
of computing are ignored, as in the design document's own estimate.

A task may ask for one collusion share ("q") or for several ("q_list"); the
same strategies are then examined for each share.

Result, for each share: the number of strategies examined, the number of hits,
the best strategy and its expected payout in parts per billion of H0 (rounded
down), up to three best hits; and one SHA-256 digest over every strategy's
value, so that two devices can be compared.
"""

import hashlib
from math import comb, gcd

VERSION = 1
KIND = "compute"

PPB = 10 ** 9
MAX_NODES_PER_UNIT = 10 ** 7   # a few minutes on an ordinary computer
MAX_NUMBER_BITS = 2 ** 32      # upper estimate of all big integers held at once (see validate)
TOP_HITS = 3
_ALLOWED = {"H0", "safety", "p_min_den", "verifiers", "q", "q_list", "cap_third", "batches",
            "n_max", "sizes"}


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _check_int(params, name, lo, hi, default=None):
    value = params.get(name, default)
    if not _is_int(value) or not lo <= value <= hi:
        raise ValueError("%s must be an integer from %d to %d" % (name, lo, hi))
    return value


def _check_q(q):
    if (not isinstance(q, list) or len(q) != 2 or not _is_int(q[0]) or not _is_int(q[1])
            or not 0 <= q[0] < q[1] <= 10 ** 4):
        raise ValueError("a collusion share is [numerator, denominator] with 0 <= share < 1")


def shares(params):
    """The collusion shares a task asks for, in the order of the task."""
    if "q_list" in params:
        return params["q_list"]
    return [params.get("q", [0, 1])]


def validate(params, units):
    if not isinstance(params, dict):
        raise ValueError("params must be an object")
    extra = set(params) - _ALLOWED
    if extra:
        raise ValueError("unknown parameters: %s" % sorted(extra))
    _check_int(params, "H0", 3, 10 ** 9)
    _check_int(params, "safety", 2, 64, 4)
    _check_int(params, "p_min_den", 2, 10 ** 6, 100)
    _check_int(params, "verifiers", 1, 16, 3)
    m = _check_int(params, "batches", 1, 3, 2)
    n_max = _check_int(params, "n_max", 1, 5000)
    if "q" in params and "q_list" in params:
        raise ValueError("give either q or q_list, not both")
    if "q_list" in params:
        q_list = params["q_list"]
        if not isinstance(q_list, list) or not 1 <= len(q_list) <= 64:
            raise ValueError("q_list must hold 1..64 collusion shares")
        for q in q_list:
            _check_q(q)
        if len(set((q[0], q[1]) for q in q_list)) != len(q_list):
            raise ValueError("q_list must not repeat a share")
    else:
        _check_q(params.get("q", [0, 1]))
    if not isinstance(params.get("cap_third", True), bool):
        raise ValueError("cap_third must be true or false")
    sizes = params.get("sizes")
    if not isinstance(sizes, dict):
        raise ValueError("sizes must be an object")
    mode = sizes.get("mode")
    if mode == "grid":
        if set(sizes) != {"mode", "points"}:
            raise ValueError("grid sizes take exactly: mode, points")
        width = _check_int(sizes, "points", 1, 2000)
    elif mode == "fixed":
        if set(sizes) != {"mode", "r"}:
            raise ValueError("fixed sizes take exactly: mode, r")
        _check_int(sizes, "r", 1, 10 ** 9)
        width = 1
    elif mode == "list":
        values = sizes.get("values")
        if (set(sizes) != {"mode", "values"} or not isinstance(values, list)
                or not 1 <= len(values) <= 2000
                or any(not _is_int(v) or not 1 <= v <= 10 ** 9 for v in values)):
            raise ValueError("list sizes take: mode, values (1..2000 positive integers)")
        width = len(set(values))
    else:
        raise ValueError("sizes.mode must be grid, fixed or list")
    if not _is_int(units) or not 1 <= units <= 10 ** 6:
        raise ValueError("units must be an integer from 1 to 1000000")
    # The exact probabilities are big integers: a batch of n fakes needs up to n numbers of
    # n * step_bits bits each. Bound a generous estimate of their total size, so that a task
    # with extreme parameters cannot use up the memory of a small device (a phone).
    q_bits = max(q[1].bit_length() for q in shares(params))
    h_bits = (params["H0"] * (n_max + 1) ** m).bit_length() + 1       # the pending amount can grow
    step_bits = (params.get("verifiers", 3) * q_bits
                 + max(h_bits, params.get("p_min_den", 100).bit_length()) + 1)
    if (m + 3) * (n_max + 1) ** 2 * step_bits > MAX_NUMBER_BITS:
        raise ValueError("task too large: its exact numbers would need too much memory "
                         "(lower n_max, verifiers or the denominators of the shares)")
    if not params.get("cap_third", True):
        # Without the cap the number of strategies is known in advance. With the cap it is
        # much smaller and depends on the amounts; run() then stops at the same limit.
        per_batch = width * n_max
        nodes = 0
        for depth in range(1, m + 1):
            nodes += per_batch ** depth
        nodes *= len(shares(params))
        if nodes > MAX_NODES_PER_UNIT * units:
            raise ValueError("task too large: about %d strategies per unit (limit %d)"
                             % (nodes // units, MAX_NODES_PER_UNIT))


class Rules:
    def __init__(self, params, q):
        self.H0 = params["H0"]
        self.s = params.get("safety", 4)
        self.pd = params.get("p_min_den", 100)
        v = params.get("verifiers", 3)
        qn, qd = q
        self.catch_num = qd ** v - qn ** v
        self.catch_den = qd ** v
        self.cap_third = params.get("cap_third", True)
        self.m = params.get("batches", 2)
        self.n_max = params["n_max"]
        self.sizes = params["sizes"]

    def sizes_for(self, H):
        """Task prices available when H is pending, ascending, each with 3*r <= H."""
        mode = self.sizes["mode"]
        if mode == "grid":
            points = self.sizes["points"]
            out = []
            for j in range(1, points + 1):
                r = (H * j) // (3 * points)
                if r >= 1 and (not out or out[-1] != r):
                    out.append(r)
            return out
        if mode == "fixed":
            r = self.sizes["r"]
            return [r] if 3 * r <= H else []
        return [r for r in sorted(set(self.sizes["values"])) if 3 * r <= H]

    def n_limit(self, H, r):
        if self.cap_third:
            return min(self.n_max, H // (3 * r))
        return self.n_max

    def batch(self, H, r):
        """Return (a, d, c): detection probability a/d per fake, and cost c per detection."""
        s, pd = self.s, self.pd
        if s * r * pd <= r + H:          # p = 1/pd (the floor)
            p_num, p_den, c = 1, pd, s * r * pd
        elif s * r >= r + H:             # p = 1
            p_num, p_den, c = 1, 1, s * r
        else:                            # p = s*r / (r + H)
            p_num, p_den, c = s * r, r + H, r + H
        a = p_num * self.catch_num
        d = p_den * self.catch_den
        g = gcd(a, d)
        return a // g, d // g, c


class Layer:
    """One batch: n fakes, each detected with probability a/d, each detection costs c."""

    __slots__ = ("n", "a", "miss", "c", "den", "_w")

    def __init__(self, n, a, d, c, den=None, known=None):
        self.n = n
        self.a = a
        self.miss = d - a
        self.c = c
        self.den = d ** n if den is None else den
        self._w = known if known is not None else {}

    def weight(self, k):
        """Numerator of P(exactly k detections); the denominator is self.den."""
        w = self._w.get(k)
        if w is None:
            w = comb(self.n, k) * self.a ** k * self.miss ** (self.n - k)
            self._w[k] = w
        return w


def _expected_numerator(layers, i, budget, weight):
    if i == len(layers):
        return weight * budget
    layer = layers[i]
    kmax = min(layer.n, (budget - 1) // layer.c)
    total = 0
    for k in range(kmax + 1):
        total += _expected_numerator(layers, i + 1, budget - k * layer.c, weight * layer.weight(k))
    return total


def expected_payout(layers, total):
    """Exact expected payout as (numerator, denominator)."""
    den = 1
    for layer in layers:
        den *= layer.den
    return _expected_numerator(layers, 0, total, 1), den


def evaluate_path(params, path, q=None):
    """Exact expected payout of one strategy [[n1, r1], [n2, r2], ...] as (num, den).

    q is the collusion share [numerator, denominator]; it may be omitted when the
    task has a single share. Raises ValueError if the rules do not allow the strategy.
    """
    if q is None:
        all_q = shares(params)
        if len(all_q) != 1:
            raise ValueError("say which collusion share to evaluate")
        q = all_q[0]
    _check_q(list(q))
    rules = Rules(params, q)
    H = rules.H0
    layers = []
    if not 1 <= len(path) <= rules.m:
        raise ValueError("a strategy has 1..%d batches" % rules.m)
    for n, r in path:
        if r not in rules.sizes_for(H) or not 1 <= n <= rules.n_limit(H, r):
            raise ValueError("strategy step (%d, %d) is not allowed with %d pending" % (n, r, H))
        a, d, c = rules.batch(H, r)
        layers.append(Layer(n, a, d, c))
        H += n * r
    return expected_payout(layers, H)


# ---------------------------------------------------------------------------
# The search uses a faster way to get exactly the same numbers as
# expected_payout() above. The last batch of a strategy is built step by step
# for n = 1, 2, 3, ... (class _Last), and the sum over its detections is taken
# with running totals instead of term by term. tests/test_kernels.py checks
# the two ways against each other for every strategy of several small tasks.
# ---------------------------------------------------------------------------

class _Last:
    """The last batch of a strategy, for growing n and a fixed price."""

    __slots__ = ("a", "miss", "d", "c", "n", "den", "kcap", "w", "apow")

    def __init__(self, a, d, c, kcap):
        self.a = a
        self.miss = d - a
        self.d = d
        self.c = c
        self.n = 0
        self.den = 1
        self.kcap = kcap      # no more than this many detections can leave a positive payout
        self.w = [1]          # w[k] = C(n, k) * a**k * miss**(n - k) for the current n
        self.apow = 1

    def step(self):
        """Go from n to n + 1 fakes."""
        n1 = self.n + 1
        miss = self.miss
        w = self.w
        for k in range(len(w)):
            # C(n+1, k) = C(n, k) * (n+1) / (n+1-k); the division is exact
            w[k] = w[k] * miss * n1 // (n1 - k)
        if n1 <= self.kcap:
            self.apow *= self.a
            w.append(self.apow)
        self.n = n1
        self.den *= self.d

    def totals(self, kmax):
        """Running totals of w[k] and of k * w[k] for k = 0..kmax."""
        p0, p1 = [], []
        s0 = s1 = 0
        w = self.w
        for k in range(kmax + 1):
            wk = w[k]
            s0 += wk
            s1 += k * wk
            p0.append(s0)
            p1.append(s1)
        return p0, p1


def _fast_numerator(outer, i, budget, weight, last, p0, p1):
    if i == len(outer):
        k = min(last.n, (budget - 1) // last.c)
        s = budget * p0[k] - last.c * p1[k]
        return s if weight is None else weight * s
    layer = outer[i]
    kmax = min(layer.n, (budget - 1) // layer.c)
    total = 0
    for k in range(kmax + 1):
        wk = layer.weight(k)
        total += _fast_numerator(outer, i + 1, budget - k * layer.c,
                                 wk if weight is None else weight * wk, last, p0, p1)
    return total


def _new_last(rules, H, r):
    a, d, c = rules.batch(H, r)
    limit = rules.n_limit(H, r)
    kcap = min(limit, (H + limit * r - 1) // c) if limit >= 1 else 0
    return _Last(a, d, c, kcap), limit


class _Search:
    def __init__(self, rules, hasher, prefix, budget):
        self.rules = rules
        self.h = hasher
        self.prefix = prefix
        self.budget = budget          # one-element list shared by all shares of the unit
        self.count = 0
        self.hits = 0
        self.best = None
        self.top_hits = []

    def node(self, path, outer, outer_den, last, H):
        """Examine the strategy `path` (its last batch is `last`) and everything that extends it.

        H is the amount pending before the last batch; outer are the earlier batches.
        """
        rules = self.rules
        self.budget[0] -= 1
        if self.budget[0] < 0:
            raise ValueError("this unit holds more than %d strategies; the task must be split "
                             "into more units" % MAX_NODES_PER_UNIT)
        n, r = path[-1]
        total = H + n * r
        p0, p1 = last.totals(min(n, (total - 1) // last.c))
        num = _fast_numerator(outer, 0, total, None, last, p0, p1)
        den = outer_den * last.den
        scaled = rules.H0 * den
        ev_ppb = (num * PPB) // scaled
        self.count += 1
        text = ";".join("%d,%d" % step for step in path)
        self.h.update(("%s%s:%d\n" % (self.prefix, text, ev_ppb)).encode("ascii"))
        if self.best is None or ev_ppb > self.best[0]:
            self.best = (ev_ppb, list(path))
        if num > scaled:
            self.hits += 1
            self.top_hits.append((ev_ppb, list(path)))
            if len(self.top_hits) > 64:
                self.trim()
        if len(path) < rules.m:
            outer.append(Layer(n, last.a, last.d, last.c, den=last.den, known=dict(enumerate(last.w))))
            for r2 in rules.sizes_for(total):
                child, limit = _new_last(rules, total, r2)
                for n2 in range(1, limit + 1):
                    child.step()
                    path.append((n2, r2))
                    self.node(path, outer, den, child, total)
                    path.pop()
            outer.pop()

    def trim(self):
        # highest value first; among equal values the earliest found
        self.top_hits = sorted(self.top_hits, key=lambda t: -t[0])[:TOP_HITS]

    def summary(self, q):
        self.trim()
        best = None
        if self.best is not None:
            best = {"ev_ppb": self.best[0], "path": [list(step) for step in self.best[1]]}
        return {"q": list(q), "count": self.count, "hits": self.hits, "best": best,
                "top_hits": [{"ev_ppb": ev, "path": [list(step) for step in path]}
                             for ev, path in self.top_hits]}


def run(params, unit, units, ctx=None):
    validate(params, units)
    if not _is_int(unit) or not 0 <= unit < units:
        raise ValueError("unit out of range")
    hasher = hashlib.sha256()
    by_q = []
    ordinal = 0
    budget = [MAX_NODES_PER_UNIT]
    for qi, q in enumerate(shares(params)):
        rules = Rules(params, q)
        search = _Search(rules, hasher, "%d|" % qi, budget)
        H0 = rules.H0
        for r in rules.sizes_for(H0):
            last, limit = _new_last(rules, H0, r)
            for n in range(1, limit + 1):
                last.step()
                mine = ordinal % units == unit
                ordinal += 1
                if mine:
                    search.node([(n, r)], [], 1, last, H0)
        by_q.append(search.summary(q))
    return {
        "kernel": "exit-scam-a@1",
        "count": sum(s["count"] for s in by_q),
        "hits": sum(s["hits"] for s in by_q),
        "by_q": by_q,
        "digest": hasher.hexdigest(),
    }
