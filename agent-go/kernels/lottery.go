package kernels

import (
	"crypto/sha256"
	"fmt"
	"math/big"
	"strconv"
	"strings"
)

// Accumulate exact binomial weights through two inclusive cutoffs.
func binomial(n, p, last, half int64) (sum, halfSum, zero, den *big.Int) {
	zero = pow(big.NewInt(p - 1), n)
	den = pow(big.NewInt(p), n)
	w := new(big.Int).Set(zero)
	sum, halfSum = new(big.Int), new(big.Int)
	for k := int64(0); k <= last; k++ {
		sum.Add(sum, w)
		if k == half {
			halfSum.Set(sum)
		}
		if k < last {
			w.Mul(w, big.NewInt(n - k))
			w.Quo(w, big.NewInt((k + 1) * (p - 1)))
		}
	}
	return
}

// For large grids, bound the same sum from both sides using directed rounding.
// If a ppb boundary falls in the interval, fall back to the exact integer sum.
func bounds(n, p, last, half int64, mode big.RoundingMode) [3]int64 {
	value := func(i int64) *big.Float { return new(big.Float).SetPrec(192).SetMode(mode).SetInt64(i) }
	base := value(p - 1)
	base.Quo(base, value(p))
	w := value(1)
	for e := n; e > 0; e /= 2 {
		if e&1 != 0 {
			w.Mul(w, base)
		}
		base.Mul(base, base)
	}
	ppb := func(v *big.Float) int64 { scaled := value(1000000000); n, _ := scaled.Mul(scaled, v).Int64(); return n }
	out := [3]int64{0, 0, ppb(w)}
	sum := value(0)
	factor := value(0)
	for k := int64(0); k <= last; k++ {
		sum.Add(sum, w)
		if k == half {
			out[1] = ppb(sum)
		}
		if k < last {
			w.Mul(w, factor.SetInt64(n - k))
			w.Quo(w, factor.SetInt64((k + 1) * (p - 1)))
		}
	}
	out[0] = ppb(sum)
	return out
}

func lotteryCell(n, p int64, cost pair) [3]int64 {
	last := (cost.n * n - 1) / (p * cost.d)
	half := (cost.n * n - 1) / (2 * p * cost.d)
	if n >= 1000 {
		lo := bounds(n, p, last, half, big.ToNegativeInf)
		if lo == bounds(n, p, last, half, big.ToPositiveInf) {
			return lo
		}
	}
	l, h, z, den := binomial(n, p, last, half)
	scale := func(v *big.Int) int64 { return v.Quo(v.Mul(v, big.NewInt(1000000000)), den).Int64() }
	return [3]int64{scale(l), scale(h), scale(z)}
}

func lottery(p obj, units int64) job {
	fields(p, "tasks check_one_in costs months", true)
	ns, ps := ints(p["tasks"], 1, 3000000, 200), ints(p["check_one_in"], 2, 1000000, 200)
	cs := axis(p["costs"], 200, func(v any) pair { return fraction(v, 1000000, false, false, false) }, false)
	ms := ints(p["months"], 1, 36, 12)
	require(highest(ns) * highest(ms) <= 3000000, "too many trials")
	size := int64(len(ns)) * int64(len(ps)) * int64(len(cs)) * int64(len(ms))
	require(size <= 300 * units, "too many cells per unit")
	point := grid(size, len(ns), len(ps), len(cs), len(ms))
	return func(unit int64) obj {
		h := sha256.New()
		rows := [][]int64{}
		for j := unit; j < size; j += units {
			i := point(j)
			n, p, c, m := ns[i[0]], ps[i[1]], cs[i[2]], ms[i[3]]
			probs := lotteryCell(n * m, p, c)
			row := []int64{n, p, c.n, c.d, m, probs[0], probs[1], probs[2]}
			rows = append(rows, row)
			words := make([]string, len(row))
			for j, v := range row {
				words[j] = strconv.FormatInt(v, 10)
			}
			fmt.Fprintln(h, strings.Join(words, ","))
		}
		return obj{"kernel": "lottery-b@1", "columns": strings.Fields("tasks check_one_in cost_num cost_den months loss_ppb half_ppb zero_ppb"),
			"rows": rows, "digest": fmt.Sprintf("%x", h.Sum(nil))}
	}
}
