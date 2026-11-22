"""Ed25519 signatures (RFC 8032), pure Python, standard library only.

This follows the reference implementation in RFC 8032, section 6. The agent
uses only verify(): every update and every task list must carry a signature
made with a release key pinned in trust.py.

sign() is here for the maintainers' offline tools and for tests. It is not
constant-time and must not be used on a machine an attacker can observe.
"""

import hashlib

_p = 2 ** 255 - 19
_q = 2 ** 252 + 27742317777372353535851937790883648493


def _sha512(data):
    return hashlib.sha512(data).digest()


def _inv(x):
    return pow(x, _p - 2, _p)


_d = -121665 * _inv(121666) % _p
_sqrt_m1 = pow(2, (_p - 1) // 4, _p)


def _sha512_modq(data):
    return int.from_bytes(_sha512(data), "little") % _q


# Points are (X, Y, Z, T) in extended coordinates: x = X/Z, y = Y/Z, x*y = T/Z.
def _add(P, Q):
    A = (P[1] - P[0]) * (Q[1] - Q[0]) % _p
    B = (P[1] + P[0]) * (Q[1] + Q[0]) % _p
    C = 2 * P[3] * Q[3] * _d % _p
    D = 2 * P[2] * Q[2] % _p
    E, F, G, H = B - A, D - C, D + C, B + A
    return (E * F % _p, G * H % _p, F * G % _p, E * H % _p)


def _mul(s, P):
    Q = (0, 1, 1, 0)
    while s > 0:
        if s & 1:
            Q = _add(Q, P)
        P = _add(P, P)
        s >>= 1
    return Q


def _equal(P, Q):
    if (P[0] * Q[2] - Q[0] * P[2]) % _p != 0:
        return False
    if (P[1] * Q[2] - Q[1] * P[2]) % _p != 0:
        return False
    return True


def _recover_x(y, sign):
    if y >= _p:
        return None
    x2 = (y * y - 1) * _inv(_d * y * y + 1) % _p
    if x2 == 0:
        return None if sign else 0
    x = pow(x2, (_p + 3) // 8, _p)
    if (x * x - x2) % _p != 0:
        x = x * _sqrt_m1 % _p
    if (x * x - x2) % _p != 0:
        return None
    if (x & 1) != sign:
        x = _p - x
    return x


_g_y = 4 * _inv(5) % _p
_g_x = _recover_x(_g_y, 0)
_G = (_g_x, _g_y, 1, _g_x * _g_y % _p)


def _compress(P):
    zinv = _inv(P[2])
    x = P[0] * zinv % _p
    y = P[1] * zinv % _p
    return int.to_bytes(y | ((x & 1) << 255), 32, "little")


def _decompress(s):
    if len(s) != 32:
        return None
    y = int.from_bytes(s, "little")
    sign = y >> 255
    y &= (1 << 255) - 1
    x = _recover_x(y, sign)
    if x is None:
        return None
    return (x, y, 1, x * y % _p)


def _secret_expand(secret):
    if len(secret) != 32:
        raise ValueError("an Ed25519 seed is 32 bytes")
    h = _sha512(secret)
    a = int.from_bytes(h[:32], "little")
    a &= (1 << 254) - 8
    a |= (1 << 254)
    return a, h[32:]


def public_key(secret):
    """Return the 32-byte public key for a 32-byte seed."""
    a, _ = _secret_expand(secret)
    return _compress(_mul(a, _G))


def sign(secret, msg):
    """Return the 64-byte signature of msg. Offline use only (not constant-time)."""
    a, prefix = _secret_expand(secret)
    A = _compress(_mul(a, _G))
    r = _sha512_modq(prefix + msg)
    Rs = _compress(_mul(r, _G))
    h = _sha512_modq(Rs + A + msg)
    s = (r + h * a) % _q
    return Rs + int.to_bytes(s, 32, "little")


def is_strong_public(public):
    """True if public is a canonical encoding of a point that is not of small order.

    The identity and the other points of order 1, 2, 4 or 8 make the verification
    equation say nothing about who signed, so they must never serve as an identity.
    """
    if not isinstance(public, (bytes, bytearray)) or len(public) != 32:
        return False
    A = _decompress(bytes(public))
    if A is None or _compress(A) != bytes(public):
        return False
    return not _equal(_mul(8, A), (0, 1, 1, 0))


def verify(public, msg, signature):
    """Return True only if signature is a valid Ed25519 signature of msg."""
    if not isinstance(public, (bytes, bytearray)) or len(public) != 32:
        return False
    if not isinstance(signature, (bytes, bytearray)) or len(signature) != 64:
        return False
    A = _decompress(bytes(public))
    if A is None:
        return False
    Rs = bytes(signature[:32])
    R = _decompress(Rs)
    if R is None:
        return False
    s = int.from_bytes(signature[32:], "little")
    if s >= _q:
        return False
    h = _sha512_modq(Rs + bytes(public) + bytes(msg))
    sB = _mul(s, _G)
    hA = _mul(h, A)
    return _equal(sB, _add(R, hA))
