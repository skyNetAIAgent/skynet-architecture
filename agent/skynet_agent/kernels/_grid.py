"""Validation and unit numbering for Cartesian parameter grids."""

from fractions import Fraction
from math import prod


def integer(value, lo, hi):
    if type(value) is not int or not lo <= value <= hi:
        raise ValueError("expected an integer from %d to %d" % (lo, hi))
    return value


def fields(params, names):
    if not isinstance(params, dict) or set(params) != set(names.split()):
        raise ValueError("expected parameters: " + names)


def axis(values, check):
    if not isinstance(values, list) or not 1 <= len(values) <= 256:
        raise ValueError("a grid axis needs 1..256 entries")
    values = [check(v) for v in values]
    if len(set(values)) != len(values):
        raise ValueError("duplicate grid point")
    return values


def ints(values, lo, hi):
    return axis(values, lambda v: integer(v, lo, hi))


def share(pair):
    if not isinstance(pair, list) or len(pair) != 2:
        raise ValueError("expected a [numerator, denominator] pair")
    den = integer(pair[1], 1, 1000)
    return Fraction(integer(pair[0], 0, den), den)


def size(axes, units):
    if integer(units, 1, 10 ** 6) != prod(map(len, axes)):
        raise ValueError("units must equal the number of grid points")


def point(axes, unit, units):
    size(axes, units)
    integer(unit, 0, units - 1)
    values = []
    for values_on_axis in reversed(axes):
        unit, i = divmod(unit, len(values_on_axis))
        values.append(values_on_axis[i])
    return tuple(reversed(values))


def _digits(n):
    # Small decimal chunks also work with Python's optional int-to-string limit.
    if n < 10 ** 600:
        return str(n)
    chunks = []
    while n:
        n, tail = divmod(n, 10 ** 600)
        chunks.append(tail)
    return str(chunks[-1]) + "".join("%0600d" % v for v in reversed(chunks[:-1]))


def ratio(value):
    """Canonical p/q for nonnegative exact results, including integers."""
    return _digits(value.numerator) + "/" + _digits(value.denominator)
