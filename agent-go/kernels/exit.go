package kernels

import (
	"crypto/sha256"
	"fmt"
	"hash"
	"math/big"
	"math/bits"
	"sort"
	"strconv"
)

const nodeLimit = 10000000

type rules struct {
	h, safety, floor, verifiers, levels, limit int64
	capped bool
	points int64
	prices []int64
	qs []pair
}

func parseRules(p obj, units int64) rules {
	fields(p, "H0 safety p_min_den verifiers q q_list cap_third batches n_max sizes", false)
	r := rules{
		h:number(p["H0"], 3, 1000000000), safety:number(get(p, "safety", 4), 2, 64),
		floor: number(get(p, "p_min_den", 100), 2, 1000000), verifiers: number(get(p, "verifiers", 3), 1, 16),
		levels:number(get(p, "batches", 2), 1, 3), limit:number(p["n_max"], 1, 5000),
	}
	var ok bool
	r.capped, ok = get(p, "cap_third", true).(bool)
	require(ok, "invalid cap_third")
	parseShare := func(v any) pair { return fraction(v, 10000, true, true, false) }
	if v, exists := p["q_list"]; exists {
		_, single := p["q"]
		require(!single, "q and q_list are mutually exclusive")
		r.qs = axis(v, 64, parseShare, true)
	} else { r.qs = []pair{parseShare(get(p, "q", []any{0, 1}))} }
	s, ok := p["sizes"].(obj)
	require(ok, "invalid sizes")
	var width int64
	switch s["mode"] {
	case "grid":
		fields(s, "mode points", true)
		r.points = number(s["points"], 1, 2000)
		width = r.points
	case "fixed":
		fields(s, "mode r", true)
		r.prices = []int64{number(s["r"], 1, 1000000000)}
		width = 1
	case "list":
		fields(s, "mode values", true)
		seen := map[int64]bool{}
		for _, v := range list(s["values"], 1, 2000) {
			x := number(v, 1, 1000000000)
			if !seen[x] {
				r.prices = append(r.prices, x)
				seen[x] = true
			}
		}
		sort.Slice(r.prices, func(i, j int) bool { return r.prices[i] < r.prices[j] })
		width = int64(len(r.prices))
	default:
		panic(invalid("unknown size mode"))
	}
	maxH := times(big.NewInt(r.h), pow(big.NewInt(r.limit + 1), r.levels))
	step := r.verifiers * denBits(r.qs) + int64(max(maxH.BitLen() + 1, bits.Len64(uint64(r.floor)))) + 1
	require((r.levels + 3) * (r.limit + 1) * (r.limit + 1) * step <= 1 << 32, "exact numbers exceed memory budget")
	if !r.capped {
		total := new(big.Int)
		for depth := int64(1); depth <= r.levels; depth++ {
			total.Add(total, pow(big.NewInt(width * r.limit), depth))
		}
		total.Mul(total, big.NewInt(int64(len(r.qs))))
		require(total.Cmp(big.NewInt(nodeLimit * units)) <= 0, "too many strategies per unit")
	}
	return r
}

func (r rules) sizes(h int64) []int64 {
	if r.points == 0 {
		i := sort.Search(len(r.prices), func(i int) bool { return r.prices[i] > h / 3 })
		return r.prices[:i]
	}
	var out []int64
	var last int64
	den := 3 * r.points
	for j := int64(1); j <= r.points; j++ {
		x := (h / den) * j + (h % den) * j / den
		if x > last {
			out = append(out, x)
			last = x
		}
	}
	return out
}

type batch struct {
	n, limit, cost, kcap int64
	a, d, miss, den *big.Int
	weights []*big.Int
}

type search struct {
	r rules
	qIndex int
	catch, denom *big.Int
	digest hash.Hash
	budget *int64
	count, hits int64
	best *candidate
	top []candidate
}

type candidate struct { value *big.Int; path [][2]int64 }

func (c candidate) object() obj {
	return obj{"ev_ppb": c.value, "path": c.path}
}

func (s *search) batch(h, price int64) *batch {
	r := s.r
	n, d, cost := r.safety * price, h + price, h + price
	switch {
	case n <= d / r.floor:
		n, d, cost = 1, r.floor, n * r.floor
	case n >= d:
		n, d, cost = 1, 1, n
	}
	prob := new(big.Rat).SetFrac(times(big.NewInt(n), s.catch), times(big.NewInt(d), s.denom))
	limit := r.limit
	if r.capped {
		limit = min(limit, h / (3 * price))
	}
	return &batch{limit: limit, cost: cost, kcap: min(limit, (h + limit * price - 1) / cost),
		a: prob.Num(), d: prob.Denom(), miss: new(big.Int).Sub(prob.Denom(), prob.Num()),
		den: big.NewInt(1), weights: []*big.Int{big.NewInt(1)}}
}

// The truncated binomial distribution advances by convolution with one trial.
// Ancestors occasionally need higher coefficients after a later batch enlarges the payout.
func (b *batch) advance() {
	b.n++
	if b.n <= b.kcap {
		b.weights = append(b.weights, new(big.Int))
	}
	var term big.Int
	for k := len(b.weights) - 1; k > 0; k-- {
		w := b.weights[k]
		w.Add(w.Mul(w, b.miss), term.Mul(b.weights[k - 1], b.a))
	}
	b.weights[0].Mul(b.weights[0], b.miss)
	b.den.Mul(b.den, b.d)
}

func (b *batch) weight(k int64) *big.Int {
	if k < int64(len(b.weights)) {
		return b.weights[k]
	}
	return times(comb(b.n, k), times(pow(b.a, k), pow(b.miss, b.n - k)))
}

func numerator(outer []*batch, budget int64, last *batch, mass, moment []*big.Int) *big.Int {
	if len(outer) == 0 {
		k := min(last.n, (budget - 1) / last.cost)
		v := times(big.NewInt(budget), mass[k])
		return v.Sub(v, times(big.NewInt(last.cost), moment[k]))
	}
	b := outer[0]
	sum := new(big.Int)
	for k := int64(0); k <= min(b.n, (budget - 1) / b.cost); k++ {
		w := b.weight(k)
		if w.Sign() == 0 {
			continue
		}
		x := numerator(outer[1:], budget - k * b.cost, last, mass, moment)
		sum.Add(sum, x.Mul(x, w))
	}
	return sum
}

func (s *search) visit(path [][2]int64, outer []*batch, outerDen *big.Int, last *batch, h int64) {
	*s.budget -= 1
	require(*s.budget >= 0, "strategy budget exceeded")
	step := path[len(path) - 1]
	total := h + step[0] * step[1]
	count := min(last.n, (total - 1) / last.cost) + 1
	mass, moment := make([]*big.Int, count), make([]*big.Int, count)
	m0, m1 := new(big.Int), new(big.Int)
	for i := range mass {
		w := last.weights[i]
		m0 = new(big.Int).Add(m0, w)
		m1 = new(big.Int).Add(m1, times(big.NewInt(int64(i)), w))
		mass[i], moment[i] = m0, m1
	}
	num := numerator(outer, total, last, mass, moment)
	den := times(outerDen, last.den)
	scaled := times(big.NewInt(s.r.h), den)
	ev := times(num, big.NewInt(1000000000))
	ev.Quo(ev, scaled)
	s.count++
	line := strconv.AppendInt(nil, int64(s.qIndex), 10)
	line = append(line, '|')
	for i, step := range path {
		if i > 0 {
			line = append(line, ';')
		}
		line = strconv.AppendInt(line, step[0], 10)
		line = append(line, ',')
		line = strconv.AppendInt(line, step[1], 10)
	}
	line = append(line, ':')
	line = ev.Append(line, 10)
	s.digest.Write(append(line, '\n'))
	keep := func() candidate { return candidate{ev, append([][2]int64(nil), path...)} }
	if s.best == nil || ev.Cmp(s.best.value) > 0 {
		c := keep()
		s.best = &c
	}
	if num.Cmp(scaled) > 0 {
		s.hits++
		if len(s.top) < 3 || ev.Cmp(s.top[2].value) > 0 {
			s.top = append(s.top, keep())
			sort.SliceStable(s.top, func(i, j int) bool { return s.top[i].value.Cmp(s.top[j].value) > 0 })
			if len(s.top) > 3 {
				s.top = s.top[:3]
			}
		}
	}
	if int64(len(path)) == s.r.levels {
		return
	}
	outer = append(outer, last)
	for _, price := range s.r.sizes(total) {
		child := s.batch(total, price)
		for child.n < child.limit {
			child.advance()
			s.visit(append(path, [2]int64{child.n, price}), outer, den, child, total)
		}
	}
}

func exitScam(p obj, units int64) job {
	r := parseRules(p, units)
	return func(unit int64) obj {
		h := sha256.New()
		budget := int64(nodeLimit)
		var ordinal, count, hits int64
		byQ := []obj{}
		for qi, q := range r.qs {
			d := pow(big.NewInt(q.d), r.verifiers)
			s := search{r: r, qIndex: qi, catch: new(big.Int).Sub(d, pow(big.NewInt(q.n), r.verifiers)), denom: d, digest: h, budget:&budget}
			for _, price := range r.sizes(r.h) {
				last := s.batch(r.h, price)
				// Skip an entire price if this unit owns none of its roots.
				first := (unit - ordinal % units + units) % units
				if first < last.limit {
					for n := first + 1; n <= last.limit; n += units {
						for last.n < n {
							last.advance()
						}
						s.visit([][2]int64{{n, price}}, nil, big.NewInt(1), last, r.h)
					}
				}
				ordinal += last.limit
			}
			count += s.count
			hits += s.hits
			var best any
			if s.best != nil {
				best = s.best.object()
			}
			top := []obj{}
			for _, c := range s.top {
				top = append(top, c.object())
			}
			byQ = append(byQ, obj{"q":[]int64{q.n, q.d}, "count": s.count, "hits": s.hits, "best": best, "top_hits": top})
		}
		return obj{"kernel": "exit-scam-a@1", "digest": fmt.Sprintf("%x", h.Sum(nil)), "count": count, "hits": hits, "by_q": byQ}
	}
}
