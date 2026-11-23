"""token-certificate@1: multiplication counts for checking an output-layer winner.

Model: the root covers the vocabulary and its children cover 128 consecutive
rows each. The first row represents each group's integer centre. Its radius
is the exact largest L1 distance to a member. SHA-256 counter blocks generate
rows and queries on demand (distinct tags). Each byte selects an integer from
the inclusive weight range by floor(byte * width / 256), also used for h.

The claimant supplies the full argmax. The verifier reads it once, then pays
d multiplications per centre or new row dot product and one per radius bound.
Rows read counts weight rows only. Generation, index construction and finding
the claim are outside verification. Counts sum over queries. Ties go to the
lowest index. Synthetic weights need not admit any pruning.
"""

import hashlib
from fractions import Fraction
from operator import mul, sub
from struct import pack

from . import _grid

VERSION = 1
KIND = "compute"
LEAF = 128


def _shape(value):
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError("each shape is [vocabulary, dimension, queries]")
    v, d, queries = value
    _grid.integer(v, 1, 150000)
    _grid.integer(d, 1, 4096)
    _grid.integer(queries, 1, 64)
    if v * d * queries > 150000 * 4096 * 2:
        raise ValueError("too many logits per unit")
    return v, d, queries


def _axes(params):
    _grid.fields(params, "shapes weights seed seeds")
    bounds = params["weights"]
    if not isinstance(bounds, list) or len(bounds) != 2:
        raise ValueError("weights must be [minimum, maximum]")
    _grid.integer(bounds[1], _grid.integer(bounds[0], -128, 127), 127)
    count = _grid.integer(params["seeds"], 1, 1000)
    start = _grid.integer(params["seed"], 0, 2 ** 32 - count)
    return _grid.axis(params["shapes"], _shape), range(start, start + count)


def validate(params, units):
    _grid.size(_axes(params), units)


def vector(seed, tag, index, dimension, table):
    prefix = tag + pack(">II", seed, index)
    data = b"".join(hashlib.sha256(prefix + pack(">I", i)).digest()
                    for i in range((dimension + 31) // 32))
    return memoryview(data[:dimension].translate(table)).cast("b")


def dot(row, h):
    return sum(map(mul, row, h))


def index_and_claims(row_at, v, queries):
    root = row_at(0)
    root_radius = 0
    leaves = []
    best = [None] * len(queries)
    for first in range(0, v, LEAF):
        centre = row_at(first)
        radius = 0
        end = min(first + LEAF, v)
        for i in range(first, end):
            row = centre if i == first else row_at(i)
            distance = sum(map(abs, map(sub, row, centre)))
            radius = max(radius, distance)
            if first:
                distance = sum(map(abs, map(sub, row, root)))
            root_radius = max(root_radius, distance)
            for j, h in enumerate(queries):
                score = dot(row, h)
                if best[j] is None or score > best[j][0]:
                    best[j] = (score, i)
        leaves.append((centre, radius, first, end))
    return (root, root_radius), leaves, [i for score, i in best]


def verify(row_at, root, leaves, h, claim):
    score = dot(row_at(claim), h)
    best = (score, -claim)
    rows = 1
    bounds = 1
    norm = max(map(abs, h))
    if dot(root[0], h) + root[1] * norm >= score:
        for centre, radius, first, end in leaves:
            bounds += 1
            if dot(centre, h) + radius * norm < score:
                continue
            for i in range(first, end):
                if i != claim:
                    best = max(best, (dot(row_at(i), h), -i))
                    rows += 1
    return -best[1], rows, rows * len(h) + bounds * (len(h) + 1)


def run(params, unit, units, ctx=None):
    (v, d, count), seed = _grid.point(_axes(params), unit, units)
    lo, hi = params["weights"]
    table = bytes((lo + i * (hi - lo + 1) // 256) % 256 for i in range(256))

    def row_at(i):
        return vector(seed, b"W", i, d, table)

    queries = [vector(seed, b"h", j, d, table) for j in range(count)]
    root, leaves, winners = index_and_claims(row_at, v, queries)
    rows = checks = 0
    for h, claim in zip(queries, winners):
        winner, read, multiplications = verify(row_at, root, leaves, h, claim)
        if winner != claim:
            raise ValueError("certificate disagrees with full argmax")
        rows += read
        checks += multiplications
    full = v * d * count
    return {"kernel": "token-certificate@1", "V": v, "d": d, "vectors": count,
            "seed": seed, "winners": winners, "rows_read": rows,
            "verify_mults": checks, "full_mults": full,
            "verify_over_full": _grid.ratio(Fraction(checks, full))}
