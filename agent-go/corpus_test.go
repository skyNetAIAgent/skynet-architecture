package agentgo_test

import (
	"bufio"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"os"
	"path/filepath"
	"testing"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
)

// TestCorpusCompat checks the randomly generated JSON corpus against the
// Python reference results recorded in the file (outputs/corpus/corpus.jsonl
// is copied here as testdata/corpus.jsonl).
func TestCorpusCompat(t *testing.T) {
	f, err := os.Open(filepath.Join("testdata", "corpus.jsonl"))
	if err != nil {
		t.Fatal(err)
	}
	defer f.Close()
	scanner := bufio.NewScanner(f)
	scanner.Buffer(make([]byte, 1<<20), 1<<20)
	ok, rejected, checked := 0, 0, 0
	for scanner.Scan() {
		var row struct {
			Text      string `json:"text"`
			Kind      string `json:"kind"`
			Canonical string `json:"canonical"`
			WireHex   string `json:"wire_hex"`
			Sha256    string `json:"sha256"`
		}
		if err := json.Unmarshal(scanner.Bytes(), &row); err != nil {
			t.Fatal(err)
		}
		value, err := canon.Parse([]byte(row.Text))
		switch row.Kind {
		case "ok":
			ok++
			if err != nil {
				t.Fatalf("rejected %q: %v", row.Text, err)
			}
			ascii, err := canon.Marshal(value, true)
			if err != nil || string(ascii) != row.Canonical {
				t.Fatalf("%q: canonical %q, want %q (%v)", row.Text, ascii, row.Canonical, err)
			}
			wire, err := canon.Marshal(value, false)
			if err != nil || hex.EncodeToString(wire) != row.WireHex {
				t.Fatalf("%q: wire %x, want %s (%v)", row.Text, wire, row.WireHex, err)
			}
			sum := sha256.Sum256(ascii)
			if hex.EncodeToString(sum[:]) != row.Sha256 {
				t.Fatalf("%q: sha256 mismatch", row.Text)
			}
		case "reject", "divergent":
			// Both classes must be rejected by the strict Go parser; for the
			// "divergent" rows Python is more lenient and this difference is
			// documented in REVIEW.md.
			rejected++
			if err == nil {
				t.Fatalf("accepted %q", row.Text)
			}
		default:
			t.Fatalf("unknown kind %q", row.Kind)
		}
		checked++
	}
	if err := scanner.Err(); err != nil {
		t.Fatal(err)
	}
	if ok < 2000 || checked != ok+rejected {
		t.Fatalf("corpus too small: ok=%d rejected=%d checked=%d", ok, rejected, checked)
	}
}
