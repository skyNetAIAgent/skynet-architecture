package kernels

import "math/big"

// t4Scale models one full exam forward plus N fractional adapter forwards
// per position. Training costs three forwards per token (claude1, 5.4).
func t4Scale(p obj, units int64) job {
	fields(p, "N n a D_budget epsilon_bits", true)
	submitters := ints(p["N"], 1, 1000000, 32)
	positions := ints(p["n"], 1, 1000000, 32)
	parts := axis(p["a"], 32, func(v any) pair {
		return fraction(v, 1000000, false, false, true)
	}, true)
	budgets := ints(p["D_budget"], 1, 1000000000000, 32)
	epsilonBits := number(p["epsilon_bits"], 1, 256)
	epsilon := "1/" + pow(big.NewInt(2), epsilonBits).String()
	point := grid(units, len(submitters), len(positions), len(parts), len(budgets))
	return func(unit int64) obj {
		i := point(unit)
		count, n, a, budget := submitters[i[0]], positions[i[1]], parts[i[2]], budgets[i[3]]

		// Use units of 1/a.d forward. The 20% cap is 5*exam <= training.
		base, perAdapter := n*a.d, n*a.n
		exam := base + count*perAdapter
		training := 3 * budget * a.d
		perToken := 3 * a.d
		minTokens := (5*exam + perToken - 1) / perToken
		var maxSubmitters any
		if training >= 5*base {
			maxSubmitters = (training - 5*base) / (5 * perAdapter)
		}
		return obj{
			"kernel": "t4-scale@1", "N": count, "n": n, "a": a.String(),
			"D_budget": budget, "epsilon": epsilon, "D_min": minTokens,
			"N_max": maxSubmitters, "fits": budget >= minTokens,
			"overhead": ratio(big.NewRat(exam, training)),
		}
	}
}
