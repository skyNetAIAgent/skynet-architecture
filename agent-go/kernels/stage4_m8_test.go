package kernels_test

import (
	"testing"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/kernels"
)

func TestT4Scale(t *testing.T) {
	p := canon.Object{
		"N": []any{1, 4}, "n": []any{3}, "a": []any{[]any{2, 4}},
		"D_budget": []any{15, 14, 5, 4}, "epsilon_bits": 2,
	}
	for _, v := range []struct {
		unit   int64
		result string
	}{
		{4, `{"D_budget":15,"D_min":15,"N":4,"N_max":4,"a":"1/2","epsilon":"1/4","fits":true,"kernel":"t4-scale@1","n":3,"overhead":"1/5"}`},
		{5, `{"D_budget":14,"D_min":15,"N":4,"N_max":3,"a":"1/2","epsilon":"1/4","fits":false,"kernel":"t4-scale@1","n":3,"overhead":"3/14"}`},
		{2, `{"D_budget":5,"D_min":8,"N":1,"N_max":0,"a":"1/2","epsilon":"1/4","fits":false,"kernel":"t4-scale@1","n":3,"overhead":"3/10"}`},
		{3, `{"D_budget":4,"D_min":8,"N":1,"N_max":null,"a":"1/2","epsilon":"1/4","fits":false,"kernel":"t4-scale@1","n":3,"overhead":"3/8"}`},
	} {
		got, err := kernels.Run("t4-scale", 1, p, v.unit, 8)
		if err != nil {
			t.Fatal(err)
		}
		raw, err := canon.Marshal(got, true)
		if err != nil || string(raw) != v.result {
			t.Errorf("unit %d: got %s (%v), want %s", v.unit, raw, err, v.result)
		}
	}
}

func TestT4ScaleLarge(t *testing.T) {
	for _, tc := range []struct {
		N, n, aNum, aDen, budget int64
		Dmin, Nmax               int64
	}{
		{10000, 100000, 4, 36, 185351852, 185351852, 10000},
		{1000000, 1000000, 999999, 1000000, 1000000000000, 1666666666667, 599999},
		{1, 1, 1, 1000000, 1000000000000, 2, 599999999999000000},
	} {
		p := canon.Object{
			"N": []any{tc.N}, "n": []any{tc.n}, "a": []any{[]any{tc.aNum, tc.aDen}},
			"D_budget": []any{tc.budget}, "epsilon_bits": 80,
		}
		got, err := kernels.Run("t4-scale", 1, p, 0, 1)
		if err != nil || got["D_min"] != tc.Dmin || got["N_max"] != tc.Nmax ||
			got["epsilon"] != "1/1208925819614629174706176" {
			t.Error(got, err)
		}
	}
}

func TestT4ScaleRejects(t *testing.T) {
	for _, v := range []struct {
		key   string
		value any
		units int64
	}{
		{"n", []any{0}, 1}, {"N", []any{1.0}, 1}, {"N", []any{1000001}, 1},
		{"a", []any{[]any{1, 2}, []any{2, 4}}, 2},
		{"a", []any{[]any{0, 1}}, 1}, {"a", []any{[]any{2, 1}}, 1},
		{"a", []any{[]any{1, 1000001}}, 1}, {"D_budget", []any{0}, 1},
		{"epsilon_bits", true, 1}, {"epsilon_bits", 257, 1},
		{"epsilon_bits", nil, 1}, {"extra", 1, 1}, {"n", []any{1, 2}, 1},
	} {
		p := canon.Object{
			"N": []any{1}, "n": []any{1}, "a": []any{[]any{1, 2}},
			"D_budget": []any{1}, "epsilon_bits": 40,
		}
		if v.value == nil {
			delete(p, v.key)
		} else {
			p[v.key] = v.value
		}
		if err := kernels.Validate("t4-scale", 1, p, v.units); err == nil {
			t.Errorf("accepted %s=%v, units=%d", v.key, v.value, v.units)
		}
	}
}
