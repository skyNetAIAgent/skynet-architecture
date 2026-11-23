package agentgo_test

import (
	"testing"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/sig"
)

// FuzzCanonParse must never panic: any byte string either parses or returns
// an error. Run with:
//   go test -run=^$ -fuzz=FuzzCanonParse -fuzztime=45s .
func FuzzCanonParse(f *testing.F) {
	for _, seed := range []string{"{}", `{"a":1}`, "null", `"\ud800"`, "1e500", "[[[[[]]]]]", "\xff\xfe"} {
		f.Add([]byte(seed))
	}
	f.Fuzz(func(t *testing.T, data []byte) {
		v, err := canon.Parse(data)
		if err == nil && v != nil {
			_, _ = canon.Marshal(v, true)
			_, _ = canon.Marshal(v, false)
		}
	})
}

// FuzzSigLines parses arbitrary detached-signature files.
func FuzzSigLines(f *testing.F) {
	for _, seed := range []string{"ed25519:" + testPubHex + ":00", "garbage", ""} {
		f.Add([]byte(seed))
	}
	f.Fuzz(func(t *testing.T, data []byte) {
		sig.ParseLines(data)
		sig.VerifyDetached([]byte("x"), data, nil)
	})
}

const testPubHex = "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a"
