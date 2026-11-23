"""apprentice-seats@1: exposure of the apprentice reward pool to a coalition.

Model: draw D=min(S,n+m) distinct keys uniformly each epoch. Of all C(n+m,D)
subsets, C(m,j)*C(n,D-j) give the coalition j seats. Each of those seats
earns one price with marginal probability f. Epoch expectations add even
without independence. Honest share is among filled seats (zero if D=0).
When D=0 the event that no honest key wins is certain. The m range includes
its endpoints when reached by the given positive step.
"""

from fractions import Fraction
from math import comb

from . import _grid

VERSION = 1
KIND = "compute"


def _axes(params):
    _grid.fields(params, "S n m f E")
    s = _grid.ints(params["S"], 0, 1000)
    n = _grid.ints(params["n"], 0, 10 ** 6)
    f = _grid.axis(params["f"], _grid.share)
    _grid.integer(params["E"], 0, 10 ** 6)
    m = params["m"]
    if not isinstance(m, list) or len(m) != 3:
        raise ValueError("m must be [first, last, step]")
    lo = _grid.integer(m[0], 0, 10 ** 6)
    hi = _grid.integer(m[1], lo, 10 ** 6)
    step = _grid.integer(m[2], 1, 10 ** 6)
    rows = (hi - lo) // step + 1
    # Bound the two decimal integers in the no-honest probability per row.
    population = max(n) + hi
    subsets = comb(population, min(max(s), population // 2))
    digits = subsets.bit_length() * 30103 // 100000 + 1
    if rows * (2 * digits + 220) > 36000:
        raise ValueError("seat table too large for one result")
    return s, n, f


def validate(params, units):
    _grid.size(_axes(params), units)


def run(params, unit, units, ctx=None):
    seats, honest, f = _grid.point(_axes(params), unit, units)
    lo, hi, step = params["m"]
    rows = []
    for m in range(lo, hi + 1, step):
        population = honest + m
        draws = min(seats, population)
        # First moment of the hypergeometric law: each key is in D/population
        # of all subsets. The zero-honest event counts all-coalition subsets.
        coalition = Fraction(draws * m, population) if population else Fraction(0)
        leak = coalition * f
        share = (draws - coalition) / draws if draws else Fraction(0)
        none = Fraction(comb(m, draws), comb(population, draws))
        rows.append([m, _grid.ratio(leak), _grid.ratio(leak * params["E"]),
                     _grid.ratio(share), _grid.ratio(none)])
    return {"kernel": "apprentice-seats@1", "S": seats, "n": honest, "f": _grid.ratio(f),
            "E": params["E"], "columns": ["m", "leak_epoch", "leak_total", "honest_share",
                                          "no_honest"], "rows": rows}
