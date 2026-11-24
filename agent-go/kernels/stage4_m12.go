// Additive merge with an exact linear-quadratic loss (stage 4, M12).
package kernels

import "math/big"

type mergeVector [8]int64

func mergeAttribution(p obj, units int64) job {
	fields(p, "scale g hessian updates owner copies noise threshold", true)
	scale := number(p["scale"], 1, 10000)
	threshold := number(p["threshold"], 0, 10000)
	dim := len(list(p["g"], 1, 8))
	vector := func(value any) mergeVector {
		var out mergeVector
		for i, v := range list(value, dim, dim) {
			out[i] = number(v, -10000, 10000)
		}
		return out
	}
	g := vector(p["g"])
	hessian := axis(p["hessian"], dim, vector, false)
	require(len(hessian) == dim, "expected square Hessian")
	for i, row := range hessian {
		for j := 0; j < i; j++ {
			require(row[j] == hessian[j][i], "expected symmetric Hessian")
		}
	}
	updates := axis(p["updates"], 8, vector, false)
	owner := int(number(p["owner"], 0, int64(len(updates)-1)))
	copies := ints(p["copies"], 1, 8, 8)
	noises := axis(p["noise"], 32, vector, true)
	point := grid(units, len(copies), len(noises))

	return func(unit int64) obj {
		index := point(unit)
		count, noise := int(copies[index[0]]), noises[index[1]]
		delta := updates[owner]
		for j := 0; j < dim; j++ {
			delta[j] += noise[j]
		}
		extended := make([]mergeVector, len(updates), len(updates)+count)
		copy(extended, updates)
		for i := 0; i < count; i++ {
			extended = append(extended, delta)
		}

		den := 2 * scale * scale * scale
		cut := 2 * scale * scale * threshold
		before := mergeScores(g, hessian, updates, scale)
		after := mergeScores(g, hessian, extended, scale)
		baseResult, copyResult, gains := obj{}, obj{}, obj{}
		for name, original := range before {
			withCopies := after[name]
			baseResult[name] = mergeRatios(original, den)
			copyResult[name] = mergeRatios(withCopies, den)
			gain := max(0, withCopies[owner]-cut) - max(0, original[owner]-cut)
			for _, score := range withCopies[len(updates):] {
				gain += max(0, score-cut)
			}
			gains[name] = ratio(big.NewRat(gain, den))
		}
		// Shapley scores sum to the exact improvement of the full coalition.
		baseResult["value"] = mergeTotal(before["shapley"], den)
		copyResult["value"] = mergeTotal(after["shapley"], den)
		return obj{"kernel": "merge-attribution@1", "owner": owner, "copies": count,
			"noise": noise[:dim], "scale": scale, "baseline": baseResult,
			"with_copies": copyResult, "gain": gains}
	}
}

// In units of 1/(2*scale^3), the pair interaction is -2*x_i^T H x_j.
// Each partner contributes it in full to LOO and by half to Shapley.
func mergeScores(g mergeVector, hessian []mergeVector, updates []mergeVector, scale int64) map[string][]int64 {
	count := len(updates)
	separate, halfInteractions := make([]int64, count), make([]int64, count)
	for i, x := range updates {
		var hx mergeVector
		for j, row := range hessian {
			for k := range hessian {
				hx[j] += row[k] * x[k]
			}
			separate[i] -= x[j] * (2*scale*g[j] + hx[j])
		}
		for j, y := range updates[:i] {
			var half int64
			for k := range hessian {
				half -= y[k] * hx[k]
			}
			halfInteractions[i] += half
			halfInteractions[j] += half
		}
	}
	loo, shapley := make([]int64, count), make([]int64, count)
	for i, single := range separate {
		loo[i] = single + 2*halfInteractions[i]
		shapley[i] = single + halfInteractions[i]
	}
	return map[string][]int64{"separate": separate, "loo": loo, "shapley": shapley}
}

func mergeRatios(values []int64, den int64) []string {
	out := make([]string, len(values))
	for i, v := range values {
		out[i] = ratio(big.NewRat(v, den))
	}
	return out
}

func mergeTotal(values []int64, den int64) string {
	var total int64
	for _, v := range values {
		total += v
	}
	return ratio(big.NewRat(total, den))
}
