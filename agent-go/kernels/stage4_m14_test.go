package kernels_test

import (
	"testing"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/kernels"
)

func TestVerificationEnumerations(t *testing.T) {
	// A reordered axis also checks that units follow the input array.
	params := canon.Object{"cases": []any{"field-5", "chain-8-2", "packing-8", "packing-4"}}
	want := []string{
		`{"case":"field-5","caught":20,"kernel":"verification-enumerations@1","missed":5,"total":25}`,
		`{"case":"chain-8-2","caught":56,"kernel":"verification-enumerations@1","missed":168,"total":224}`,
		`{"case":"packing-8","false_accepts":0,"kernel":"verification-enumerations@1","total":441,"true_accepts":9,"verdict_sha256":"a5c8a8d715fb5293a4dd12753d3483e848f63cb24891a3e584bfdc81954f377c"}`,
		`{"case":"packing-4","false_accepts":20,"kernel":"verification-enumerations@1","total":441,"true_accepts":9,"verdict_sha256":"fca92fea5a3148177517b737591e499ed021432078bd9803578a2eaad4074fc9"}`,
	}
	for i, expected := range want {
		result, err := kernels.Run("verification-enumerations", 1, params, int64(i), 4)
		if err != nil {
			t.Fatal(err)
		}
		wire, err := canon.Marshal(result, true)
		if err != nil || string(wire) != expected {
			t.Errorf("unit %d: got %s (%v), want %s", i, wire, err, expected)
		}
	}
}

func TestVerificationEnumerationParameters(t *testing.T) {
	for _, tc := range []struct {
		params canon.Object
		units  int64
	}{
		{canon.Object{}, 1},
		{canon.Object{"cases": "field-5"}, 1},
		{canon.Object{"cases": []any{}}, 1},
		{canon.Object{"cases": []any{4}}, 1},
		{canon.Object{"cases": []any{"packing-5"}}, 1},
		{canon.Object{"cases": []any{"field-5", "field-5"}}, 2},
		{canon.Object{"cases": []any{"packing-8"}, "base": 8}, 1},
		{canon.Object{"cases": []any{"field-5"}}, 2},
	} {
		if err := kernels.Validate("verification-enumerations", 1, tc.params, tc.units); err == nil {
			t.Errorf("accepted %v with %d units", tc.params, tc.units)
		}
	}
}
