package kernels

import (
	"crypto/sha256"
	"encoding/hex"
)

// verificationEnumerations repeats the finite examples in GPT2 sections 6.1 and 6.2
// and its table of mini-agent tasks. Each unit runs one complete enumeration.
func verificationEnumerations(p obj, units int64) job {
	fields(p, "cases", true)
	cases := axis(p["cases"], 4, func(v any) string {
		name, _ := v.(string)
		switch name {
		case "packing-8", "packing-4", "chain-8-2", "field-5":
			return name
		default:
			panic(invalid("unknown enumeration case"))
		}
	}, true)
	require(int64(len(cases)) == units, "units must equal the number of cases")
	return func(unit int64) obj {
		name := cases[unit]
		var r obj
		switch name {
		case "packing-8":
			r = enumeratePacking(8)
		case "packing-4":
			r = enumeratePacking(4)
		case "chain-8-2":
			r = enumerateChain()
		case "field-5":
			r = enumerateField()
		}
		r["case"], r["kernel"] = name, "verification-enumerations@1"
		return r
	}
}

func enumeratePacking(base int) obj {
	verdicts := make([]byte, 0, 441)
	correct, falseAccepts := 0, 0
	for x := -1; x <= 1; x++ {
		for y := -1; y <= 1; y++ {
			wantC, wantD := 2*x-y, -x-y
			for c := -3; c <= 3; c++ {
				for d := -3; d <= 3; d++ {
					var verdict byte
					if (c-wantC+base*(d-wantD))%(base*base) == 0 {
						verdict = 1
						if c == wantC && d == wantD {
							correct++
						} else {
							falseAccepts++
						}
					}
					verdicts = append(verdicts, verdict)
				}
			}
		}
	}
	digest := sha256.Sum256(verdicts)
	return obj{"total": len(verdicts), "true_accepts": correct, "false_accepts": falseAccepts,
		"verdict_sha256": hex.EncodeToString(digest[:])}
}

func enumerateChain() obj {
	total, caught := 0, 0
	for defect := 0; defect < 8; defect++ {
		for first := 0; first < 8; first++ {
			for second := first + 1; second < 8; second++ {
				total++
				if first == defect || second == defect {
					caught++
				}
			}
		}
	}
	return obj{"total": total, "caught": caught, "missed": total - caught}
}

func enumerateField() obj {
	total, missed := 0, 0
	for x := 0; x < 5; x++ {
		for y := 0; y < 5; y++ {
			total++
			if (x-y)%5 == 0 {
				missed++
			}
		}
	}
	return obj{"total": total, "caught": total - missed, "missed": missed}
}
