package agentgo_test

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"testing"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/kernels"
)

// The Python reference rows store each result in its wire encoding. RawMessage
// preserves those bytes, including the field order and the representation of numbers.
func TestStage4Golden(t *testing.T) {
	lines := bytes.Split(bytes.TrimSpace(fixture(t, "golden_stage4.jsonl")), []byte("\n"))
	if len(lines) != 4 {
		t.Fatalf("got %d reference rows, want 4", len(lines))
	}
	for _, line := range lines {
		var row struct {
			Kernel        string
			KernelVersion int64 `json:"kernel_version"`
			Unit, Units   int64
			Params        json.RawMessage
			Result        json.RawMessage
			Hash          string `json:"result_sha256"`
		}
		if err := json.Unmarshal(line, &row); err != nil {
			t.Fatal(err)
		}
		t.Run(row.Kernel, func(t *testing.T) {
			got, err := kernels.Run(row.Kernel, row.KernelVersion, object(t, string(row.Params)), row.Unit, row.Units)
			if err != nil {
				t.Fatal(err)
			}
			wire, err := canon.Marshal(got, true)
			if err != nil {
				t.Fatal(err)
			}
			digest := sha256.Sum256(wire)
			if !bytes.Equal(wire, row.Result) || hex.EncodeToString(digest[:]) != row.Hash {
				t.Fatalf("got %s (%x), want %s (%s)", wire, digest, row.Result, row.Hash)
			}
		})
	}
}
