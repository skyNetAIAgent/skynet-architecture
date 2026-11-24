package kernels_test

import (
	"testing"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/kernels"
)

func mergeExample() canon.Object {
	return canon.Object{"scale": 2, "g": []any{-6}, "hessian": []any{[]any{2}},
		"updates": []any{[]any{2}}, "owner": 0, "copies": []any{1},
		"noise": []any{[]any{0}, []any{-1}}, "threshold": 0}
}

func TestMergeAttribution(t *testing.T) {
	// v(x) = 3x - x^2/2. A second unit step increases v from 5/2 to 4.
	p := mergeExample()
	exact, err := kernels.Run("merge-attribution", 1, p, 0, 2)
	if err != nil {
		t.Fatal(err)
	}
	wire, err := canon.Marshal(exact, true)
	want := `{"baseline":{"loo":["5/2"],"separate":["5/2"],"shapley":["5/2"],"value":"5/2"},"copies":1,"gain":{"loo":"1/2","separate":"5/2","shapley":"3/2"},"kernel":"merge-attribution@1","noise":[0],"owner":0,"scale":2,"with_copies":{"loo":["3/2","3/2"],"separate":["5/2","5/2"],"shapley":["2/1","2/1"],"value":"4/1"}}`
	if err != nil || string(wire) != want {
		t.Fatal(string(wire), err)
	}

	// At threshold 1 the half-step copy has zero LOO payout (score 7/8).
	// Standalone it scores 11/8. Its Shapley score is (11/8 + 7/8)/2.
	p["threshold"] = 2
	noisy, err := kernels.Run("merge-attribution", 1, p, 1, 2)
	if err != nil {
		t.Fatal(err)
	}
	gain := noisy["gain"].(canon.Object)
	if gain["separate"] != "3/8" || gain["loo"] != "-1/2" || gain["shapley"] != "-1/8" {
		t.Fatal(gain)
	}
}

func TestMergeAttributionLimits(t *testing.T) {
	row := make([]any, 8)
	matrix := make([]any, 8)
	for i := range row {
		row[i], matrix[i] = 10000, row
	}
	p := canon.Object{"scale": 10000, "g": row, "hessian": matrix, "updates": matrix,
		"owner": 7, "copies": []any{8}, "noise": []any{row}, "threshold": 10000}
	result, err := kernels.Run("merge-attribution", 1, p, 0, 1)
	if err != nil {
		t.Fatal(err)
	}
	// The full update has eight coordinates of 24, giving -192 - 192^2/2.
	if result["with_copies"].(canon.Object)["value"] != "-18624/1" {
		t.Fatal(result)
	}
}

func TestMergeAttributionRejects(t *testing.T) {
	for _, tc := range []struct {
		key   string
		value any
	}{
		{"scale", true}, {"scale", 0}, {"g", []any{}}, {"g", []any{-10001}},
		{"hessian", []any{[]any{1, 2}}}, {"updates", []any{}},
		{"updates", []any{[]any{0.5}}}, {"owner", -1}, {"owner", 1}, {"copies", []any{9}},
		{"copies", []any{0}}, {"copies", []any{1, 1}}, {"noise", []any{[]any{2}, []any{2}}},
		{"threshold", -1}, {"extra", 1},
	} {
		p := mergeExample()
		p[tc.key] = tc.value
		units := len(p["copies"].([]any)) * len(p["noise"].([]any))
		if err := kernels.Validate("merge-attribution", 1, p, int64(units)); err == nil {
			t.Errorf("accepted %s = %v", tc.key, tc.value)
		}
	}
	p := mergeExample()
	if err := kernels.Validate("merge-attribution", 1, p, 1); err == nil {
		t.Fatal("accepted the wrong number of units")
	}
	delete(p, "noise")
	if err := kernels.Validate("merge-attribution", 1, p, 1); err == nil {
		t.Fatal("accepted a missing axis")
	}
	p = canon.Object{"scale": 1, "g": []any{0, 0}, "hessian": []any{[]any{1, 0}, []any{1, 1}},
		"updates": []any{[]any{1, 1}}, "owner": 0, "copies": []any{1}, "noise": []any{[]any{0, 0}}, "threshold": 0}
	if err := kernels.Validate("merge-attribution", 1, p, 1); err == nil {
		t.Fatal("accepted an asymmetric Hessian")
	}
}
