"""lottery-b@1: how uneven is the income when only checked tasks are paid?

Research question (docs/CURRENT_DESIGN.md, section 3, variant B; open question Q9).
In variant B a task is checked with probability 1/P and only checked tasks are
paid, P prices each. On average an honest participant earns the same as with
ordinary payment, but the income of a period becomes a lottery. This kernel
computes exactly, for each cell of a parameter grid:

  * loss_ppb:  probability that the income of the period is below the cost of
               the work done in it (cost = cost_num/cost_den of the price);
  * half_ppb:  probability that the income is below half of that cost;
  * zero_ppb:  probability that nothing at all is paid in the period.

A cell is (tasks per month N, P, cost ratio, number of months M). The number
of paid tasks K is Binomial(N*M, 1/P); income = K*P prices; cost = cost*N*M.
All sums are exact big-integer sums; the three results are rounded down to
parts per billion. The same parameters give the same digits on every device.
"""

import hashlib

VERSION = 1
KIND = "compute"

PPB = 10 ** 9
MAX_TRIALS = 3 * 10 ** 6
MAX_CELLS_PER_UNIT = 300   # keeps one result small enough for a single GitHub comment
_ALLOWED = {"tasks", "check_one_in", "costs", "months"}


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _int_list(params, name, lo, hi, max_len):
    values = params.get(name)
    if (not isinstance(values, list) or not 1 <= len(values) <= max_len
            or any(not _is_int(v) or not lo <= v <= hi for v in values)):
        raise ValueError("%s must be a list of 1..%d integers from %d to %d" % (name, max_len, lo, hi))
    if len(set(values)) != len(values):
        raise ValueError("%s must not repeat values" % name)
    return values


def validate(params, units):
    if not isinstance(params, dict):
        raise ValueError("params must be an object")
    extra = set(params) - _ALLOWED
    if extra:
        raise ValueError("unknown parameters: %s" % sorted(extra))
    tasks = _int_list(params, "tasks", 1, MAX_TRIALS, 200)
    check = _int_list(params, "check_one_in", 2, 10 ** 6, 200)
    months = _int_list(params, "months", 1, 36, 12)
    costs = params.get("costs")
    if not isinstance(costs, list) or not 1 <= len(costs) <= 200:
        raise ValueError("costs must be a list of [numerator, denominator] pairs")
    for c in costs:
        if (not isinstance(c, list) or len(c) != 2 or not _is_int(c[0]) or not _is_int(c[1])
                or not 0 < c[0] <= c[1] <= 10 ** 6):
            raise ValueError("each cost is [numerator, denominator] with 0 < cost <= 1")
    if max(tasks) * max(months) > MAX_TRIALS:
        raise ValueError("tasks * months must not exceed %d" % MAX_TRIALS)
    if not _is_int(units) or not 1 <= units <= 10 ** 6:
        raise ValueError("units must be an integer from 1 to 1000000")
    cells = len(tasks) * len(check) * len(costs) * len(months)
    if cells > MAX_CELLS_PER_UNIT * units:
        raise ValueError("task too large: %d cells per unit (limit %d)"
                         % (cells // units, MAX_CELLS_PER_UNIT))


def cell(n_month, P, cost_num, cost_den, months):
    """Return (loss_ppb, half_ppb, zero_ppb) for one cell, exactly rounded down."""
    n = n_month * months
    # loss:  K*P < cost*n      <=>  K*P*cost_den   < cost_num*n
    # half:  K*P < cost*n/2    <=>  2*K*P*cost_den < cost_num*n
    rhs = cost_num * n
    k_loss = (rhs - 1) // (P * cost_den)          # largest K with K*P*cost_den < rhs
    k_half = (rhs - 1) // (2 * P * cost_den)
    k_loss = min(k_loss, n)
    k_half = min(k_half, n)
    den = P ** n
    w = (P - 1) ** n                              # weight of K = 0
    zero = w
    acc = 0
    loss = half = None
    k = 0
    while True:
        acc += w
        if k == k_half:
            half = acc
        if k == k_loss:
            loss = acc
            break
        # w(k+1) = w(k) * (n - k) / ((k + 1) * (P - 1)), exact in this order
        w = (w // (P - 1)) * (n - k) // (k + 1)
        k += 1
    if half is None:
        half = 0
    return (loss * PPB) // den, (half * PPB) // den, (zero * PPB) // den


def cells(params):
    """All cells in canonical order."""
    for n_month in params["tasks"]:
        for P in params["check_one_in"]:
            for cost_num, cost_den in params["costs"]:
                for months in params["months"]:
                    yield n_month, P, cost_num, cost_den, months


def run(params, unit, units, ctx=None):
    validate(params, units)
    if not _is_int(unit) or not 0 <= unit < units:
        raise ValueError("unit out of range")
    h = hashlib.sha256()
    rows = []
    for ordinal, c in enumerate(cells(params)):
        if ordinal % units != unit:
            continue
        loss, half, zero = cell(*c)
        row = [c[0], c[1], c[2], c[3], c[4], loss, half, zero]
        h.update((",".join(str(v) for v in row) + "\n").encode("ascii"))
        rows.append(row)
    return {
        "kernel": "lottery-b@1",
        "columns": ["tasks", "check_one_in", "cost_num", "cost_den", "months",
                    "loss_ppb", "half_ppb", "zero_ppb"],
        "rows": rows,
        "digest": h.hexdigest(),
    }
