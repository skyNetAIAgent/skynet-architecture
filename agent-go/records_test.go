package agentgo_test

import (
	"bytes"
	"crypto/ed25519"
	"encoding/hex"
	"errors"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/records"
)

func exampleRecord(t *testing.T) canon.Object {
	t.Helper()
	r, err := records.Make(make([]byte, 32), "task", canon.Object{"title": "Я😀<&", "text": "x", "accept": "y"}, 1)
	if err != nil {
		t.Fatal(err)
	}
	return r
}

func TestRecordVector(t *testing.T) {
	r := exampleRecord(t)
	if r["id"] != "ecb71b4b02abdb3910e33c7af2148a40d9f541cc7406868e986507b1d55f5276" {
		t.Fatal(r["id"])
	}
	raw, err := records.Wire(r)
	if err != nil || !bytes.Contains(raw, []byte("Я😀<&")) {
		t.Fatal(err, string(raw))
	}
	if _, err := records.Parse(raw, 1); err != nil {
		t.Fatal(err)
	}
	r["sig"] = strings.Repeat("00", 64)
	if err := records.Verify(r, 1); err == nil {
		t.Fatal("accepted wrong signature")
	}
}

func TestRecordPayloads(t *testing.T) {
	id := strings.Repeat("0", 64)
	hash, _ := canon.Hash(canon.Object{})
	inner := canon.Object{"v": 1, "task": "t", "agent": "a", "kernel": "k", "unit": 0, "units": 1, "result": canon.Object{}, "result_sha256": hash}
	for kind, payload := range map[string]canon.Object{
		"result": {"record": inner}, "task": {"title": "t", "text": "x", "accept": "a"},
		"claim": {"task": id, "until": 1}, "report": {"task": id, "summary": "s", "text": "x"},
		"accept": {"task": id, "report": id}, "revise": {"task": id, "report": id, "note": "n"},
	} {
		r, err := records.Make(make([]byte, 32), kind, payload, 1)
		if err != nil {
			t.Fatal(kind, err)
		}
		b, err := records.Wire(r)
		if err != nil {
			t.Fatal(err)
		}
		if _, err := records.Parse(b, 1); err != nil {
			t.Fatal(err)
		}
		payload["unexpected"] = 0
		if _, err := records.Make(make([]byte, 32), kind, payload, 1); err == nil {
			t.Fatal("accepted extra field", kind)
		}
	}
}

func TestRecordLimits(t *testing.T) {
	seed := make([]byte, 32)
	payload := canon.Object{"title": "t", "text": "x", "accept": "y"}
	r, err := records.Make(seed, "task", payload, 86402)
	if err != nil {
		t.Fatal(err)
	}
	if !errors.Is(records.Verify(r, 1), records.ErrFuture) || records.Verify(r, 2) != nil {
		t.Fatal("future boundary")
	}
	body := r["body"].(canon.Object)
	body["net"] = "other"
	if records.Verify(r, 2) == nil {
		t.Fatal("accepted other network")
	}
	for _, val := range []string{strings.Repeat("x", 20001), strings.Repeat("😀", 10000)} {
		payload["text"] = val
		if _, err := records.Make(seed, "task", payload, 1); err == nil {
			t.Fatal("accepted oversize")
		}
	}
	payload["text"] = "ok"
	pub := ed25519.NewKeyFromSeed(seed).Public().(ed25519.PublicKey)
	key := hex.EncodeToString(pub)
	for _, deputies := range []any{nil, []any{key, key}, []any{strings.Repeat("00", 32)}, []any{2}} {
		payload["deputies"] = deputies
		if _, err := records.Make(seed, "task", payload, 1); err == nil {
			t.Fatal("invalid deputies")
		}
	}
	payload["deputies"] = []any{key}
	if _, err := records.Make(seed, "task", payload, 1); err != nil {
		t.Fatal(err)
	}
}

func TestResultTextFingerprint(t *testing.T) {
	result := canon.Object{"output_sha256": "2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881"}
	hash, _ := canon.Hash(result)
	inner := canon.Object{"v": 1, "task": "t", "kernel": "k", "agent": "a", "unit": 0, "units": 1, "result": result, "result_sha256": hash}
	p := canon.Object{"record": inner, "text": "x"}
	if _, err := records.Make(make([]byte, 32), "result", p, 1); err != nil {
		t.Fatal(err)
	}
	p["text"] = "y"
	if _, err := records.Make(make([]byte, 32), "result", p, 1); err == nil {
		t.Fatal("accepted wrong AI answer")
	}
}

func TestIdentityFile(t *testing.T) {
	dir := t.TempDir()
	if b, err := records.LoadSeed(dir, false); err != nil || b != nil {
		t.Fatal(b, err)
	}
	type result struct { seed []byte; err error }
	ch := make(chan result, 8)
	for i := 0; i < cap(ch); i++ {
		go func() {
			seed, err := records.LoadSeed(dir, true)
			ch <- result{seed, err}
		}()
	}
	var seed []byte
	for i := 0; i < cap(ch); i++ {
		r := <- ch
		if r.err != nil || len(r.seed) != 32 || (seed != nil && !bytes.Equal(seed, r.seed)) {
			t.Fatal(r.err, "inconsistent identity")
		}
		seed = r.seed
	}
	path := filepath.Join(dir, "identity.key")
	raw, err := os.ReadFile(path)
	if err != nil || string(raw) != hex.EncodeToString(seed) + "\n" {
		t.Fatal(err)
	}
	if err := os.WriteFile(path, []byte("damaged\n"), 0600); err != nil {
		t.Fatal(err)
	}
	if _, err := records.LoadSeed(dir, true); err == nil {
		t.Fatal("replaced damaged key")
	}
}

func TestRecordCorpus(t *testing.T) {
	n := scanFixture(t, "records.jsonl.gz", func(line []byte) {
		if _, err := records.Parse(line, 1800000000); err != nil {
			t.Fatal(err)
		}
	})
	if n != 1261 {
		t.Fatal("record count", n)
	}
}
