package kernels

import (
	"math/big"
	"slices"
)

// One comparison in T4, claude1 section 5.4. The supplied variance uses n-1.
func examThresholds(p obj, units int64) job {
	fields(p, "n epsilon_bits B variance digits", true)
	ns := ints(p["n"], 2, 1000000, 32)
	ks := ints(p["epsilon_bits"], 1, 128, 32)
	widths := ints(p["B"], 1, 64, 32)
	variances := axis(p["variance"], 32, func(value any) pair {
		parts := list(value, 2, 2)
		num := number(parts[0], 0, 1000000)
		den := number(parts[1], 1, 1000000)
		r := big.NewRat(num, den)
		return pair{r.Num().Int64(), r.Denom().Int64()}
	}, true)
	digits := number(p["digits"], 1, 9)
	point := grid(units, len(ns), len(ks), len(widths), len(variances))

	// The maximum sample variance occurs with a balanced split between endpoints.
	// Its bound decreases with n and increases with B. Check the tightest grid point.
	n, width := highest(ns), slices.Min(widths)
	maxVariance := big.NewRat(width*width*(n/2)*((n+1)/2), n*(n-1))
	for _, v := range variances {
		require(v.rat().Cmp(maxVariance) <= 0, "variance exceeds the sample maximum")
	}
	scale := pow(big.NewInt(10), digits+1)
	return func(unit int64) obj {
		i := point(unit)
		n, k, width, variance := ns[i[0]], ks[i[1]], widths[i[2]], variances[i[3]]
		hoeffdingRoot := big.NewRat(width*width*k, 2*n)
		bernsteinRoot := new(big.Rat).Mul(variance.rat(), big.NewRat(2*(k+1), n))
		bernsteinLinear := big.NewRat(7*width*(k+1), 3*(n-1))
		return obj{
			"kernel": "exam-thresholds@1", "n": n, "epsilon_bits": k,
			"B": width, "variance": variance.String(), "digits": digits,
			"hoeffding": examInterval(hoeffdingRoot, new(big.Rat), scale),
			"bernstein": examInterval(bernsteinRoot, bernsteinLinear, scale),
		}
	}
}

// The atanh series at 1/3 certifies these bounds on ln(2).
const examLogFloor int64 = 693147180559945309
const examLogDen int64 = 1000000000000000000

// Enclose sqrt(a*ln(2)) + c*ln(2).
func examInterval(a, c *big.Rat, scale *big.Int) []string {
	endpoint := func(logNum int64, upper bool) string {
		scaledLog := new(big.Rat).Mul(big.NewRat(logNum, examLogDen), new(big.Rat).SetInt(scale))
		x := new(big.Rat).Mul(a, scaledLog)
		x.Mul(x, new(big.Rat).SetInt(scale))
		root := new(big.Int).Quo(x.Num(), x.Denom())
		root.Sqrt(root)

		y := new(big.Rat).Mul(c, scaledLog)
		linear := new(big.Int).Quo(y.Num(), y.Denom())
		if upper {
			if !x.IsInt() || times(root, root).Cmp(x.Num()) != 0 {
				root.Add(root, big.NewInt(1))
			}
			if !y.IsInt() {
				linear.Add(linear, big.NewInt(1))
			}
		}
		return ratio(new(big.Rat).SetFrac(root.Add(root, linear), scale))
	}
	return []string{endpoint(examLogFloor, false), endpoint(examLogFloor+1, true)}
}
