package agentgo_test

import (
	"math"
	"testing"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
)

func object(t *testing.T, raw string) canon.Object {
	t.Helper()
	v, err := canon.Parse([]byte(raw))
	if err != nil {
		t.Fatal(err)
	}
	obj, ok := v.(canon.Object)
	if !ok {
		t.Fatalf("expected object: %s", raw)
	}
	return obj
}

func TestCanonicalHash(t *testing.T) {
	obj := object(t, `{"n":9007199254740993,"t":"Я😀<&","x":1.0}`)
	hash, err := canon.Hash(obj)
	if err != nil || hash != "b962271506f6b47ca1574e7faa7b6183093d545465b231670aeec715a55c6d0e" {
		t.Fatal(hash, err)
	}
}

func TestCanonicalStrings(t *testing.T) {
	for _, tc := range []struct { raw, ascii, wire string }{
		{`"\u007f\u2028\u2029<&>"`, `"\u007f\u2028\u2029<&>"`, "\"\x7f\u2028\u2029<&>\""},
		{`{"😀":1,"\uffff":2,"e\u0301":3,"é":4}`, `{"e\u0301":3,"\u00e9":4,"\uffff":2,"\ud83d\ude00":1}`, "{\"e\u0301\":3,\"é\":4,\"\uffff\":2,\"😀\":1}"},
		{`"\\\"\u0000\b\t\n\f\r"`, `"\\\"\u0000\b\t\n\f\r"`, `"\\\"\u0000\b\t\n\f\r"`},
		{`"\\ud800"`, `"\\ud800"`, `"\\ud800"`},
	} {
		v, err := canon.Parse([]byte(tc.raw))
		if err != nil {
			t.Fatal(err)
		}
		for ascii, want := range map[bool]string{true: tc.ascii, false: tc.wire} {
			got, err := canon.Marshal(v, ascii)
			if err != nil || string(got) != want {
				t.Fatalf("%s: got %q want %q: %v", tc.raw, got, want, err)
			}
		}
	}
}

func TestCanonicalNumbers(t *testing.T) {
	for raw, want := range map[string]string{
		"-0": "0", "-0e0": "-0.0", "1.000": "1.0", "1e-7": "1e-07", "1e20": "1e+20",
		"1e-4": "0.0001", "1e-5": "1e-05", "1e15": "1000000000000000.0", "1e16": "1e+16",
		"4.9406564584124654e-324": "5e-324", "-1e-500": "-0.0",
		"9999999999999999999999999999999": "9999999999999999999999999999999",
	} {
		v, err := canon.Parse([]byte(raw))
		if err != nil {
			t.Fatal(err)
		}
		b, err := canon.Marshal(v, true)
		if err != nil || string(b) != want {
			t.Fatalf("%s: %s, %v", raw, b, err)
		}
	}
}

func TestStrictJSON(t *testing.T) {
	for _, s := range []string{`[{"a":0,"\u0061":1}]`, `"\ud800"`, `"\udc00"`, `"\ud800\u0000"`,
		"null false", "[1,]", "NaN", "Infinity", "-Infinity", "1e500", "\xff", "", `{"x":}`} {
		if _, err := canon.Parse([]byte(s)); err == nil {
			t.Errorf("accepted %q", s)
		}
	}
	for _, f := range []float64{math.NaN(), math.Inf(1), math.Inf(-1)} {
		if _, err := canon.Marshal(f, true); err == nil {
			t.Fatal("encoded non-finite value")
		}
	}
}
