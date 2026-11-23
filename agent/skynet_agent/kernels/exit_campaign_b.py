"""exit-campaign-b@1: optimal payout from a leaving key under variant B.

Model: R=1. Waves settle before the next decision. Catching any fake ends
the campaign with zero payout. Otherwise j successful checks leave H0+j/p
pending. Stopping pays it immediately, also at the horizon. Idle waves
cannot improve a policy because the rules are stationary. Action zero means
stop. Equal optima prefer stopping, then the smallest positive wave.
"""

from fractions import Fraction
from math import lcm

from . import _grid

VERSION = 1
KIND = "compute"


def _axes(params):
    _grid.fields(params, "H0 p q k C T")
    h = _grid.ints(params["H0"], 0, 10 ** 9)
    p = _grid.axis(params["p"], _grid.share)
    q = _grid.axis(params["q"], _grid.share)
    k = _grid.ints(params["k"], 1, 8)
    c = _grid.ints(params["C"], 0, 48)
    t = _grid.ints(params["T"], 0, 16)
    if 0 in p:
        raise ValueError("p must be positive")
    bits = max(x.denominator.bit_length() for x in p)
    bits += max(k) * max(x.denominator.bit_length() for x in q)
    if bits * max(c) * max(t) > 45000:
        raise ValueError("campaign result too large")
    return h, p, q, k, c, t


def validate(params, units):
    _grid.size(_axes(params), units)


def optimum(h, p, q, k, cap, waves):
    miss, win = 1 - p, p * q ** k
    den = lcm(miss.denominator, win.denominator)
    miss, win = int(miss * den), int(win * den)
    powers = [den ** i for i in range(cap + 1)]
    pending = [h * p.numerator + j * p.denominator for j in range(cap * waves + 1)]
    values = pending
    scale = 1
    first = 0
    for remaining in range(1, waves + 1):
        width = (waves - remaining) * cap + 1
        scale *= powers[cap]
        best = [v * scale for v in pending[:width]]
        after = values
        for n in range(1, cap + 1):
            # Add one independent fake. Caught paths contribute zero.
            after = [miss * a + win * b for a, b in zip(after, after[1:])]
            factor = powers[cap - n]
            for j in range(width):
                payout = after[j] * factor
                if payout > best[j]:
                    best[j] = payout
                    if remaining == waves:
                        first = n
        values = best
    gain = Fraction(values[0], scale * p.numerator) - h
    return gain, first


def run(params, unit, units, ctx=None):
    h, p, q, k, cap, waves = _grid.point(_axes(params), unit, units)
    gain, first = optimum(h, p, q, k, cap, waves)
    return {"kernel": "exit-campaign-b@1", "H0": h, "p": _grid.ratio(p), "q": _grid.ratio(q),
            "k": k, "C": cap, "T": waves, "gain": _grid.ratio(gain),
            "first_wave": first, "profitable": gain > 0}
