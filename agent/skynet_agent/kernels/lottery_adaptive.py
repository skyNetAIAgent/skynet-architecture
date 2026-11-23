"""lottery-adaptive@1: check as seldom as the monthly target allows.

Model: choose the largest listed P with N >= 60*P. Use that P for every
independent trial in the month and quarter. R is a positive price and c is
the cost as a fraction of R, so R cancels from X*P*R < n*c*R. Breaking even
does not count as a loss. Network recomputations are additional checks k*N/P.
"""

from fractions import Fraction

from . import _grid

VERSION = 1
KIND = "compute"


def choose(n, grid):
    return max((p for p in grid if n >= 60 * p), default=None)


def _axes(params):
    _grid.fields(params, "N P R c k")
    counts = _grid.ints(params["N"], 0, 10 ** 6)
    grid = _grid.ints(params["P"], 1, 10 ** 6)
    costs = _grid.axis(params["c"], _grid.share)
    _grid.integer(params["R"], 1, 10 ** 9)
    _grid.integer(params["k"], 1, 64)
    for n in counts:
        p = choose(n, grid)
        # All four fractions together need at most 16*N*log10(P) digits.
        # 30103/100000 is an upper bound on log10(2).
        if p and 16 * n * (p - 1).bit_length() * 30103 > 37000 * 100000:
            raise ValueError("exact lottery fractions too large for one result")
    return counts, costs


def validate(params, units):
    _grid.size(_axes(params), units)


def period(n, p, cost):
    if p == 1:
        return Fraction(n < n * cost), Fraction(n == 0)
    den = p ** n
    zero = weight = (p - 1) ** n
    last = (cost.numerator * n - 1) // (p * cost.denominator)
    total = 0
    for x in range(last + 1):
        total += weight
        weight = weight * (n - x) // ((x + 1) * (p - 1))
    return Fraction(total, den), Fraction(zero, den)


def run(params, unit, units, ctx=None):
    n, cost = _grid.point(_axes(params), unit, units)
    p = choose(n, params["P"])
    result = {"kernel": "lottery-adaptive@1", "N": n, "c": _grid.ratio(cost),
              "R": params["R"], "k": params["k"], "reachable": p is not None}
    if p is not None:
        result["p"] = _grid.ratio(Fraction(1, p))
        for name, trials in (("month", n), ("quarter", 3 * n)):
            loss, zero = period(trials, p, cost)
            result[name] = {"loss": _grid.ratio(loss), "zero": _grid.ratio(zero)}
        result["recomputations"] = _grid.ratio(Fraction(params["k"] * n, p))
    return result
