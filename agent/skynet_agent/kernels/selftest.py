"""selftest@1: does this device compute exactly what every other device computes?

All work is integer arithmetic, so the answer does not depend on the CPU,
the operating system or the Python build. Every device must return the same
digest. A different digest means a broken installation or broken hardware.
"""

import hashlib
from fractions import Fraction

from .. import ed25519

VERSION = 1
KIND = "compute"

_MASK64 = (1 << 64) - 1


def validate(params, units):
    rounds = params.get("rounds", 4)
    if not isinstance(rounds, int) or isinstance(rounds, bool) or not 1 <= rounds <= 64:
        raise ValueError("rounds must be an integer from 1 to 64")
    if units != 1:
        raise ValueError("selftest has exactly one unit")
    extra = set(params) - {"rounds"}
    if extra:
        raise ValueError("unknown parameters: %s" % sorted(extra))


def _matrix(seed, n):
    x = seed & _MASK64
    rows = []
    for _ in range(n):
        row = []
        for _ in range(n):
            x = (x * 6364136223846793005 + 1442695040888963407) & _MASK64
            row.append((x >> 33) - (1 << 30))
        rows.append(row)
    return rows


def _matmul(a, b):
    n = len(a)
    cols = [[b[k][j] for k in range(n)] for j in range(n)]
    return [[sum(x * y for x, y in zip(row, col)) for col in cols] for row in a]


def run(params, unit, units, ctx=None):
    rounds = params.get("rounds", 4)
    h = hashlib.sha256()
    n = 32
    m = _matrix(2026, n)
    for r in range(rounds):
        m2 = _matmul(m, _matrix(1000 + r, n))
        for row in m2:
            h.update((",".join(str(v) for v in row) + "\n").encode("ascii"))
        # keep the numbers bounded: fold back to 32-bit signed values
        m = [[((v + (1 << 31)) & 0xFFFFFFFF) - (1 << 31) for v in row] for row in m2]

    checks = {}
    # big integers
    checks["pow"] = pow(3, 10 ** 4, 2 ** 255 - 19) == pow(pow(3, 5000, 2 ** 255 - 19), 2, 2 ** 255 - 19)
    # exact fractions
    acc = Fraction(0)
    for k in range(1, 60):
        acc += Fraction(1, k * (k + 1))
    checks["fraction"] = acc == Fraction(59, 60)
    h.update(("%d/%d\n" % (acc.numerator, acc.denominator)).encode("ascii"))
    # hash function
    checks["sha256"] = hashlib.sha256(b"abc").hexdigest() == (
        "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")
    # signature check (RFC 8032, test 2)
    pub = bytes.fromhex("3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c")
    sig = bytes.fromhex(
        "92a009a9f0d4cab8720e820b5f642540a2b27b5416503f8fb3762223ebdb69da"
        "085ac1e43e15996e458f3613d0f11d8c387b2eaeb4302aeeb00d291612bb0c00")
    checks["ed25519"] = ed25519.verify(pub, b"\x72", sig) and not ed25519.verify(pub, b"\x73", sig)
    for name in sorted(checks):
        h.update(("%s=%d\n" % (name, 1 if checks[name] else 0)).encode("ascii"))
    return {"kernel": "selftest@1", "rounds": rounds, "digest": h.hexdigest(),
            "ok": all(checks.values())}
