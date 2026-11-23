package kernels

import (
	"math/big"
	"math/bits"
	"strings"
)

func seats(p obj, units int64) job {
	fields(p, "S n m f E", true)
	s, h, f := ints(p["S"], 0, 1000, 256), ints(p["n"], 0, 1000000, 256), shares(p["f"])
	epochs := number(p["E"], 0, 1000000)
	m := list(p["m"], 3, 3)
	lo := number(m[0], 0, 1000000)
	hi, step := number(m[1], lo, 1000000), number(m[2], 1, 1000000)
	pop := highest(h) + hi
	digits := int64(comb(pop, min(highest(s), pop / 2)).BitLen()) * 30103 / 100000 + 1
	require(((hi - lo) / step + 1) * (2 * digits + 220) <= 36000, "seat table too large")
	point := grid(units, len(s), len(h), len(f))
	return func(unit int64) obj {
		idx := point(unit)
		seats, honest, share := s[idx[0]], h[idx[1]], f[idx[2]]
		rows := [][]any{}
		for m := lo; m <= hi; m += step {
			pop := honest + m
			draws := min(seats, pop)
			leak := big.NewRat(draws * m, max(1, pop))
			leak.Mul(leak, share.rat())
			honestShare := new(big.Rat)
			if draws != 0 {
				honestShare.SetFrac64(honest, pop)
			}
			none := new(big.Rat).SetFrac(comb(m, draws), comb(pop, draws))
			total := new(big.Rat).Mul(leak, big.NewRat(epochs, 1))
			rows = append(rows, []any{m, ratio(leak), ratio(total), ratio(honestShare), ratio(none)})
		}
		return obj{"kernel": "apprentice-seats@1", "S": seats, "n": honest, "f": share.String(), "E": epochs,
			"columns": strings.Fields("m leak_epoch leak_total honest_share no_honest"), "rows": rows}
	}
}

func campaign(p obj, units int64) job {
	fields(p, "H0 p q k C T", true)
	h, ps, qs := ints(p["H0"], 0, 1000000000, 256), shares(p["p"]), shares(p["q"])
	ks, cs, ts := ints(p["k"], 1, 8, 256), ints(p["C"], 0, 48, 256), ints(p["T"], 0, 16, 256)
	for _, v := range ps {
		require(v.n > 0, "p must be positive")
	}
	require((denBits(ps) + highest(ks) * denBits(qs)) * highest(cs) * highest(ts) <= 45000, "campaign result too large")
	point := grid(units, len(h), len(ps), len(qs), len(ks), len(cs), len(ts))
	return func(unit int64) obj {
		i := point(unit)
		h, p, q, k, c, t := h[i[0]], ps[i[1]], qs[i[2]], ks[i[3]], cs[i[4]], ts[i[5]]
		gain, first := optimum(h, p, q, k, c, t)
		return obj{"kernel": "exit-campaign-b@1", "H0": h, "p": p.String(), "q": q.String(),
			"k": k, "C": c, "T": t, "gain": ratio(gain), "first_wave": first, "profitable": gain.Sign() > 0}
	}
}

func optimum(h int64, p, q pair, k, cap, waves int64) (*big.Rat, int64) {
	// Both outcome weights use the same denominator. A common factor cancels
	// in the final gain, so no reduction is needed during the dynamic program.
	qd := pow(big.NewInt(q.d), k)
	den := times(big.NewInt(p.d), qd)
	miss := times(big.NewInt(p.d - p.n), qd)
	win := times(big.NewInt(p.n), pow(big.NewInt(q.n), k))
	powers := make([]*big.Int, cap + 1)
	for i := range powers {
		powers[i] = pow(den, int64(i))
	}
	pending := make([]*big.Int, cap * waves + 1)
	for j := range pending {
		pending[j] = big.NewInt(h * p.n + int64(j) * p.d)
	}
	values := pending
	scale := big.NewInt(1)
	var first int64
	for remaining := int64(1); remaining <= waves; remaining++ {
		width := (waves - remaining) * cap + 1
		scale.Mul(scale, powers[cap])
		best := make([]*big.Int, width)
		for j := range best {
			best[j] = times(pending[j], scale)
		}
		after := values
		for n := int64(1); n <= cap; n++ {
			next := make([]*big.Int, len(after) - 1)
			for j := range next {
				next[j] = new(big.Int).Add(times(miss, after[j]), times(win, after[j + 1]))
				if int64(j) < width {
					payout := times(next[j], powers[cap - n])
					if payout.Cmp(best[j]) > 0 {
						best[j] = payout
						if remaining == waves {
							first = n
						}
					}
				}
			}
			after = next
		}
		values = best
	}
	gain := new(big.Rat).SetFrac(values[0], times(scale, big.NewInt(p.n)))
	return gain.Sub(gain, big.NewRat(h, 1)), first
}

func choose(n int64, grid []int64) int64 {
	var p int64
	for _, x := range grid {
		if n >= 60 * x {
			p = max(p, x)
		}
	}
	return p
}

func adaptive(p obj, units int64) job {
	fields(p, "N P R c k", true)
	ns, ps, cs := ints(p["N"], 0, 1000000, 256), ints(p["P"], 1, 1000000, 256), shares(p["c"])
	price, k := number(p["R"], 1, 1000000000), number(p["k"], 1, 64)
	for _, n := range ns {
		if v := choose(n, ps); v > 0 {
			require(16 * n * int64(bits.Len64(uint64(v - 1))) * 30103 <= 37000 * 100000, "lottery fractions too large")
		}
	}
	point := grid(units, len(ns), len(cs))
	return func(unit int64) obj {
		i := point(unit)
		n, c := ns[i[0]], cs[i[1]]
		p := choose(n, ps)
		r := obj{"kernel": "lottery-adaptive@1", "N": n, "c": c.String(), "R": price, "k": k, "reachable": p > 0}
		if p == 0 {
			return r
		}
		r["p"] = ratio(big.NewRat(1, p))
		r["recomputations"] = ratio(big.NewRat(k * n, p))
		for name, trials := range map[string]int64{"month": n, "quarter": 3 * n} {
			loss, zero := "0/1", "0/1"
			if p > 1 {
				cut := int64(-1)
				if c.n > 0 {
					cut = (trials * c.n - 1) / (p * c.d)
				}
				sum, _, z, den := binomial(trials, p, cut, -1)
				loss = ratio(new(big.Rat).SetFrac(sum, den))
				zero = ratio(new(big.Rat).SetFrac(z, den))
			}
			r[name] = obj{"loss": loss, "zero": zero}
		}
		return r
	}
}
