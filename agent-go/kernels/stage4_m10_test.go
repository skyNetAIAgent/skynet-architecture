package kernels

import (
	"math/big"
	"slices"
	"testing"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
)

func examParams(t *testing.T, s string) obj {
	t.Helper()
	value, err := canon.Parse([]byte(s))
	if err != nil {
		t.Fatal(err)
	}
	return value.(obj)
}

func TestExamLogCertificate(t *testing.T) {
	// ln(2) = 2 * atanh(1/3). Bound the remaining positive series by
	// its first term times the sum of a geometric series with ratio 1/9.
	sum := new(big.Rat)
	for k := int64(1); k < 41; k += 2 {
		den := times(big.NewInt(k), pow(big.NewInt(3), k))
		sum.Add(sum, new(big.Rat).SetFrac(big.NewInt(2), den))
	}
	tail := new(big.Rat).SetFrac(big.NewInt(9), times(big.NewInt(4*41), pow(big.NewInt(3), 41)))
	if sum.Cmp(big.NewRat(examLogFloor, examLogDen)) <= 0 ||
		new(big.Rat).Add(sum, tail).Cmp(big.NewRat(examLogFloor+1, examLogDen)) >= 0 {
		t.Fatal("logarithm bounds failed")
	}
}

func TestExamThresholds(t *testing.T) {
	for _, tc := range []struct {
		params               string
		unit, units          int64
		hoeffding, bernstein []string
	}{
		// t_H = sqrt(ln(2)); with zero variance t_E is still (28/3) ln(2).
		{`{"n":[2],"epsilon_bits":[1],"B":[2],"variance":[[0,3],[1,2]],"digits":1}`, 0, 2,
			[]string{"83/100", "21/25"}, []string{"323/50", "647/100"}},
		// At V=1/2, t_E has the same radical as t_H.
		{`{"n":[2],"epsilon_bits":[1],"B":[2],"variance":[[0,3],[1,2]],"digits":1}`, 1, 2,
			[]string{"83/100", "21/25"}, []string{"729/100", "731/100"}},
		// Reproduce the n=10000, sd=0.01 entries in claude1 section 5.4.
		{`{"n":[10000],"epsilon_bits":[40],"B":[2],"variance":[[1,10000]],"digits":4}`, 0, 1,
			[]string{"3723/50000", "7447/100000"}, []string{"1401/100000", "1403/100000"}},
		// Maximum sample variance for n=2, B=64.
		{`{"n":[2],"epsilon_bits":[128],"B":[64],"variance":[[2048,1]],"digits":9}`, 0, 1,
			[]string{"3014169657639/10000000000", "75354241441/250000000"},
			[]string{"137807171169173/10000000000", "5512286846767/400000000"}},
	} {
		r, err := Run("exam-thresholds", 1, examParams(t, tc.params), tc.unit, tc.units)
		if err != nil {
			t.Fatal(err)
		}
		if !slices.Equal(r["hoeffding"].([]string), tc.hoeffding) ||
			!slices.Equal(r["bernstein"].([]string), tc.bernstein) {
			t.Fatalf("unit %d: %v", tc.unit, r)
		}
	}
}

func TestExamInvalidParameters(t *testing.T) {
	const valid = `{"n":[20],"epsilon_bits":[40],"B":[2],"variance":[[1,2]],"digits":6}`
	for _, tc := range []struct{ key, value string }{
		{"n", "[1]"}, {"n", "[1000001]"}, {"n", "[2,2]"},
		{"epsilon_bits", "[false]"}, {"epsilon_bits", "[0]"}, {"epsilon_bits", "[129]"},
		{"B", "[0]"}, {"variance", "[[1,0]]"}, {"variance", "[[-1,4]]"},
		{"variance", "[[1,2],[2,4]]"}, {"variance", "[[21,19]]"},
		{"variance", "[[0.5,1]]"}, {"variance", "[[1,2,3]]"},
		{"digits", "10"}, {"new_field", "1"},
	} {
		p := examParams(t, valid)
		replacement, err := canon.Parse([]byte(tc.value))
		if err != nil {
			t.Fatal(err)
		}
		p[tc.key] = replacement
		if Validate("exam-thresholds", 1, p, 1) == nil {
			t.Fatalf("accepted %s=%s", tc.key, tc.value)
		}
	}
	p := examParams(t, valid)
	if Validate("exam-thresholds", 1, p, 2) == nil {
		t.Fatal("accepted mismatched grid size")
	}
	delete(p, "variance")
	if Validate("exam-thresholds", 1, p, 1) == nil {
		t.Fatal("accepted missing variance")
	}
}
