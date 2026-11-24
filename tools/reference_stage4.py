#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Independent reference implementation of the stage 4 kernels (M8, M10, M12, M14)
written from docs/STAGE4_KERNELS.md only.

Standard library, exact integer and fraction arithmetic, no float.

Usage: python tools/reference_stage4.py [tasks/index.json] [results-stage4.jsonl]
Writes one line {"task", "unit", "result"} per unit of every stage 4 task.
"""

import json
import sys
from fractions import Fraction
from math import gcd, isqrt


# --------------------------------------------------------------------------
# Canonical fraction strings
# --------------------------------------------------------------------------

def frac_str(num, den=1):
    """Canonical 'p/q' string with a positive denominator after reduction."""
    if isinstance(num, Fraction):
        den = num.denominator
        num = num.numerator
    num, den = int(num), int(den)
    if den == 0:
        raise ValueError("zero denominator")
    g = gcd(abs(num), abs(den))
    num //= g
    den //= g
    if den < 0:
        num, den = -num, -den
    return "%d/%d" % (num, den)


def canonical_line(obj):
    """Canonical bytes of one jsonl line (as in the specification)."""
    return json.dumps(obj, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":")).encode("ascii")


# --------------------------------------------------------------------------
# M8: t4-scale@1
# --------------------------------------------------------------------------

def kernel_t4_scale(params):
    ns = params["N"]
    n_axis = params["n"]
    a_axis = params["a"]
    budgets = params["D_budget"]
    k = params["epsilon_bits"]
    eps_str = "1/%d" % (2 ** k)
    out = []
    for N in ns:
        for n in n_axis:
            for (p0, q0) in a_axis:
                g = gcd(p0, q0)
                p, q = p0 // g, q0 // g
                for D in budgets:
                    E = n * (q + N * p)          # exam, units of 1/q per pass
                    W = 3 * D * q                # training, same units
                    dmin = (5 * E + 3 * q - 1) // (3 * q)
                    fits = D >= dmin
                    if W >= 5 * n * q:
                        n_max = (W - 5 * n * q) // (5 * n * p)
                    else:
                        n_max = None
                    out.append({
                        "kernel": "t4-scale@1",
                        "N": N,
                        "n": n,
                        "D_budget": D,
                        "a": frac_str(p, q),
                        "epsilon": eps_str,
                        "D_min": dmin,
                        "fits": fits,
                        "N_max": n_max,
                        "overhead": frac_str(E, W),
                    })
    return out


def check_t4_scale_example():
    res = kernel_t4_scale({
        "N": [4], "n": [3], "a": [[1, 2]], "D_budget": [15], "epsilon_bits": 2,
    })[0]
    expect = {"D_budget": 15, "D_min": 15, "N": 4, "N_max": 4, "a": "1/2",
              "epsilon": "1/4", "fits": True, "kernel": "t4-scale@1", "n": 3,
              "overhead": "1/5"}
    got = canonical_line(res)
    want = canonical_line(expect)
    assert got == want, "M8 example mismatch: %r != %r" % (got, want)


# --------------------------------------------------------------------------
# M10: exam-thresholds@1  (intervals with certified ln 2)
# --------------------------------------------------------------------------

L_LN2 = Fraction(693147180559945309, 10 ** 18)
H_LN2 = Fraction(693147180559945310, 10 ** 18)


def _fl(fr):
    return fr.numerator // fr.denominator


def _ce(fr):
    return -((-fr.numerator) // fr.denominator)


def _floor_sqrt(fr):
    return isqrt(fr.numerator // fr.denominator)


def _ceil_sqrt(fr):
    r = isqrt(fr.numerator // fr.denominator)
    if r * r * fr.denominator < fr.numerator:
        r += 1
    return r


def threshold_interval(A, C, d):
    """Rational interval [lower, upper] that is guaranteed to contain
    t = sqrt(A*ln2) + C*ln2. A, C >= 0 — Fraction."""
    S = 10 ** (d + 1)
    lo = _floor_sqrt(S * S * A * L_LN2) + _fl(S * C * L_LN2)
    hi = _ceil_sqrt(S * S * A * H_LN2) + _ce(S * C * H_LN2)
    return Fraction(lo, S), Fraction(hi, S)


def kernel_exam_thresholds(params):
    ns = params["n"]
    ks = params["epsilon_bits"]
    bs = params["B"]
    vars_axis = params["variance"]
    d = params["digits"]
    out = []
    for n in ns:
        for k in ks:
            for B in bs:
                for (p0, q0) in vars_axis:
                    g = gcd(p0, q0)
                    p, q = p0 // g, q0 // g
                    V = Fraction(p, q)
                    # Hoeffding: t = sqrt(A ln2), A = B^2 k / (2n)
                    a_h = Fraction(B * B * k, 2 * n)
                    lo_h, hi_h = threshold_interval(a_h, Fraction(0), d)
                    # Bernstein: t = sqrt(A ln2) + C ln2
                    a_b = Fraction(2 * p * (k + 1), q * n)
                    c_b = Fraction(7 * B * (k + 1), 3 * (n - 1))
                    lo_b, hi_b = threshold_interval(a_b, c_b, d)
                    # Specification guarantee: width < 10^-d
                    assert hi_h - lo_h < Fraction(1, 10 ** d), (n, k, B, V)
                    assert hi_b - lo_b < Fraction(1, 10 ** d), (n, k, B, V)
                    out.append({
                        "kernel": "exam-thresholds@1",
                        "n": n,
                        "epsilon_bits": k,
                        "B": B,
                        "digits": d,
                        "variance": frac_str(p, q),
                        "hoeffding": [frac_str(lo_h), frac_str(hi_h)],
                        "bernstein": [frac_str(lo_b), frac_str(hi_b)],
                    })
    return out


def check_exam_example():
    res = kernel_exam_thresholds({
        "n": [2], "epsilon_bits": [1], "B": [2], "variance": [[0, 1]],
        "digits": 1,
    })[0]
    assert res["hoeffding"] == ["83/100", "21/25"], res
    assert res["bernstein"] == ["323/50", "647/100"], res
    assert res["variance"] == "0/1", res


# --------------------------------------------------------------------------
# M12: merge-attribution@1  (sum merge, three attribution rules)
# --------------------------------------------------------------------------

def _mv(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]


def _dot(u, v):
    return sum(u[i] * v[i] for i in range(len(u)))


def merge_payoffs(zlist, g, hessian, s, threshold):
    """Estimates separate/loo/shapley and v(U) for a set of integer requests zlist.

    Common denominator 2*s^3:
      q_i   = -2s g.z_i - z_i.A.z_i
      h_ij  = -z_i.A.z_j          (numerator of half of the pairwise term)
      loo    = q_i + 2*sum h_ij
      shapley= q_i + sum h_ij
      v(U)   = sum shapley[i]
    Charging: max(0, z - t), t = threshold/s.
    """
    m = len(zlist)
    az = [_mv(hessian, z) for z in zlist]
    q = [(-2 * s * _dot(g, z) - _dot(z, az[i])) for i, z in enumerate(zlist)]
    h = [[-_dot(zlist[i], az[j]) for j in range(m)] for i in range(m)]
    separate = [q[i] for i in range(m)]
    loo = [q[i] + 2 * sum(h[i][j] for j in range(m) if j != i) for i in range(m)]
    shapley = [q[i] + sum(h[i][j] for j in range(m) if j != i) for i in range(m)]
    value = sum(shapley)
    denom = 2 * s ** 3
    thr_num = 2 * s * s * threshold  # t = thr_num/denom
    def pay(num):
        return num - thr_num if num > thr_num else 0
    return (value, separate, loo, shapley, denom, pay)


def kernel_merge_attribution(params):
    s = params["scale"]
    g = params["g"]
    hessian = params["hessian"]
    updates = params["updates"]
    owner = params["owner"]
    copies_axis = params["copies"]
    noise_axis = params["noise"]
    threshold = params["threshold"]
    b = len(updates)
    out = []
    for ci, c in enumerate(copies_axis):
        for j, noise in enumerate(noise_axis):
            added = [updates[owner][t] + noise[t] for t in range(len(noise))]
            pre = [list(z) for z in updates]
            post = pre + [list(added) for _ in range(c)]

            v_pre, sep_pre, loo_pre, sh_pre, den_pre, pay_pre = \
                merge_payoffs(pre, g, hessian, s, threshold)
            v_post, sep_post, loo_post, sh_post, den_post, pay_post = \
                merge_payoffs(post, g, hessian, s, threshold)
            assert den_pre == den_post
            den = den_pre

            def owner_total(sep, loo, sh, idxs, pay):
                return (sum(pay(sep[i]) for i in idxs),
                        sum(pay(loo[i]) for i in idxs),
                        sum(pay(sh[i]) for i in idxs))

            base_own = owner_total(sep_pre, loo_pre, sh_pre, [owner], pay_pre)
            post_own = owner_total(sep_post, loo_post, sh_post,
                                   [owner] + list(range(b, b + c)), pay_post)
            gain = {
                "separate": frac_str(post_own[0] - base_own[0], den),
                "loo": frac_str(post_own[1] - base_own[1], den),
                "shapley": frac_str(post_own[2] - base_own[2], den),
            }
            out.append({
                "kernel": "merge-attribution@1",
                "owner": owner,
                "scale": s,
                "copies": c,
                "noise": noise,
                "baseline": {
                    "value": frac_str(v_pre, den),
                    "separate": [frac_str(x, den) for x in sep_pre],
                    "loo": [frac_str(x, den) for x in loo_pre],
                    "shapley": [frac_str(x, den) for x in sh_pre],
                },
                "with_copies": {
                    "value": frac_str(v_post, den),
                    "separate": [frac_str(x, den) for x in sep_post],
                    "loo": [frac_str(x, den) for x in loo_post],
                    "shapley": [frac_str(x, den) for x in sh_post],
                },
                "gain": gain,
            })
    return out


def check_merge_example():
    # Manual check from the specification: v(x)=3x-x^2/2 => g=-3, H=1, x=1.
    res = kernel_merge_attribution({
        "scale": 1, "g": [-3], "hessian": [[1]], "updates": [[1]],
        "owner": 0, "copies": [1], "noise": [[0]], "threshold": 0,
    })[0]
    assert res["baseline"]["value"] == "5/2", res
    assert res["baseline"]["separate"] == ["5/2"], res
    assert res["with_copies"]["value"] == "4/1", res
    assert res["with_copies"]["separate"] == ["5/2", "5/2"], res
    assert res["with_copies"]["loo"] == ["3/2", "3/2"], res
    assert res["with_copies"]["shapley"] == ["2/1", "2/1"], res
    assert res["gain"] == {"separate": "5/2", "loo": "1/2", "shapley": "3/2"}, res


# --------------------------------------------------------------------------
# M14: verification-enumerations@1
# --------------------------------------------------------------------------

import hashlib


def case_packing(B):
    verdicts = bytearray()
    total = true_acc = false_acc = 0
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            s, t = 2 * x - y, -x - y
            for c in range(-3, 4):
                for d in range(-3, 4):
                    total += 1
                    ok = ((c - s) + B * (d - t)) % (B * B) == 0
                    verdicts.append(1 if ok else 0)
                    if ok:
                        if (c, d) == (s, t):
                            true_acc += 1
                        else:
                            false_acc += 1
    return {
        "kernel": "verification-enumerations@1",
        "case": "packing-%d" % B,
        "total": total,
        "true_accepts": true_acc,
        "false_accepts": false_acc,
        "verdict_sha256": hashlib.sha256(bytes(verdicts)).hexdigest(),
    }


def case_chain():
    total = caught = 0
    for h in range(8):
        for i in range(8):
            for j in range(i + 1, 8):
                total += 1
                if h == i or h == j:
                    caught += 1
    return {
        "kernel": "verification-enumerations@1",
        "case": "chain-8-2",
        "total": total,
        "caught": caught,
        "missed": total - caught,
    }


def case_field():
    total = caught = missed = 0
    for x in range(5):
        for y in range(5):
            total += 1
            if (x - y) % 5 == 0:
                missed += 1
    caught = total - missed
    return {
        "kernel": "verification-enumerations@1",
        "case": "field-5",
        "total": total,
        "caught": caught,
        "missed": missed,
    }


PACKING_REF = {
    "packing-8": ("a5c8a8d715fb5293a4dd12753d3483e848f63cb24891a3e584bfdc81954f377c",
                  441, 9, 0),
    "packing-4": ("fca92fea5a3148177517b737591e499ed021432078bd9803578a2eaad4074fc9",
                  441, 9, 20),
}


def kernel_verification_enumerations(params):
    handlers = {
        "packing-8": lambda: case_packing(8),
        "packing-4": lambda: case_packing(4),
        "chain-8-2": case_chain,
        "field-5": case_field,
    }
    out = []
    for name in params["cases"]:
        res = handlers[name]()
        if name in PACKING_REF:
            ref_hash, ref_total, ref_true, ref_false = PACKING_REF[name]
            assert res["verdict_sha256"] == ref_hash, (name, res)
            assert (res["total"], res["true_accepts"], res["false_accepts"]) == \
                (ref_total, ref_true, ref_false), (name, res)
        out.append(res)
    return out


# --------------------------------------------------------------------------
# Kernel dispatcher and result writing
# --------------------------------------------------------------------------

KERNELS = {
    "t4-scale": kernel_t4_scale,
    "exam-thresholds": kernel_exam_thresholds,
    "merge-attribution": kernel_merge_attribution,
    "verification-enumerations": kernel_verification_enumerations,
}


def main():
    tasks_path = sys.argv[1] if len(sys.argv) > 1 else "tasks/index.json"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "results-stage4.jsonl"
    with open(tasks_path, "r", encoding="utf-8") as fh:
        tasks = json.load(fh)["tasks"]

    # Self-checks of examples from the specification (not written to the file).
    check_t4_scale_example()
    check_exam_example()
    check_merge_example()

    lines = []
    counts = []
    for task in tasks:
        kernel = task["kernel"]
        if kernel not in KERNELS:
            continue
        results = KERNELS[kernel](task["params"])
        declared = task["units"]
        if len(results) != declared:
            raise SystemExit("unit count mismatch for %s: computed %d, declared %d"
                             % (task["id"], len(results), declared))
        counts.append((task["id"], len(results)))
        for u, res in enumerate(results):
            lines.append({"task": task["id"], "unit": u, "result": res})

    with open(out_path, "w", encoding="utf-8") as fh:
        for line in lines:
            fh.write(canonical_line(line).decode("ascii") + "\n")

    print("ok: %d lines total" % len(lines))
    for tid, n in counts:
        print("  %-32s %d units" % (tid, n))


if __name__ == "__main__":
    main()
