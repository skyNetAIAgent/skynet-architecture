package agentgo_test

import (
	"bufio"
	"bytes"
	"compress/gzip"
	"encoding/json"
	"crypto/sha256"
	"encoding/hex"
	"os"
	"path/filepath"
	"testing"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/kernels"
)

func fixture(t *testing.T, name string) []byte {
	t.Helper()
	b, err := os.ReadFile(filepath.Join("testdata", name))
	if err != nil {
		t.Fatal(err)
	}
	return b
}

func scanFixture(t *testing.T, name string, visit func([]byte)) int {
	t.Helper()
	f, err := os.Open(filepath.Join("testdata", name))
	if err != nil {
		t.Fatal(err)
	}
	defer f.Close()
	gz, err := gzip.NewReader(f)
	if err != nil {
		t.Fatal(err)
	}
	defer gz.Close()
	s := bufio.NewScanner(gz)
	s.Buffer(make([]byte, 65536), 2 << 20)
	n := 0
	for s.Scan() {
		visit(s.Bytes())
		n++
	}
	if err := s.Err(); err != nil {
		t.Fatal(err)
	}
	return n
}

func TestReviewKernels(t *testing.T) {
	for _, v := range []struct{name, params, hash string}{
		{"selftest", `{"rounds":8}`, "7823a03918e86a7046e437fdf001dc40ff05fb1d241a8917baeae4d88b5629fa"},
		{"exit-scam-a", `{"H0":12,"q":[0,1],"batches":1,"n_max":2,"sizes":{"mode":"fixed","r":1}}`, "f2430908231caf486f262411b0f245a822f863e1e1eb208f908982eb68937d17"},
		{"lottery-b", `{"tasks":[1],"check_one_in":[2],"costs":[[1,1]],"months":[1]}`, "038e192fb90d21335e03a66bdb49ccef217f4d02a6f6a18dd65b6dcd4b8d5cc7"},
		{"exit-campaign-b", `{"H0":[0],"p":[[2,3]],"q":[[3,4]],"k":[2],"C":[2],"T":[2]}`, "36031ec6355f7afd5bea39f023f1105d5b7a24b11fe0d159edb7792c4065b59a"},
		{"apprentice-seats", `{"S":[2],"n":[3],"m":[0,4,1],"f":[[2,3]],"E":5}`, "c46ea36c26db3995448fb245c798c9004dd4600c7cf135ca23b40acfae5e9e6e"},
		{"lottery-adaptive", `{"N":[59],"P":[1,2],"R":7,"c":[[19,20]],"k":3}`, "f602881dd1ebdee8395ec06d0a2eb46b8c95c84e2fbf9b9d6c5d0fe29008f7ea"},
		{"token-certificate", `{"shapes":[[260,4,3]],"weights":[-2,3],"seed":42,"seeds":1}`, "37934b57be851f9b9db9e6aac6cb2663d620510f59056382a6dad7f05586efa7"},
	} {
		t.Run(v.name, func(t *testing.T) {
			got, err := kernels.Run(v.name, 1, object(t, v.params), 0, 1)
			if err != nil {
				t.Fatal(err)
			}
			h, err := canon.Hash(got)
			if err != nil || h != v.hash {
				t.Fatal(h, err)
			}
		})
	}
}

func TestKernelValidation(t *testing.T) {
	for _, v := range []struct{name, params string; units int64}{
		{"selftest", `{"rounds":true}`, 1}, {"selftest", "{}", 2},
		{"lottery-b", `{"tasks":[1,1],"check_one_in":[2],"costs":[[1,1]],"months":[1]}`, 1},
		{"exit-scam-a", `{"H0":3,"sizes":{"mode":"fixed","r":1},"n_max":5000,"verifiers":16,"q":[1,9999]}`, 1},
		{"exit-campaign-b", `{"H0":[1],"p":[[1,2],[2,4]],"q":[[0,1]],"k":[1],"C":[1],"T":[1]}`, 2},
		{"apprentice-seats", `{"S":[1000],"n":[1000000],"m":[0,10000,1],"f":[[1,1]],"E":1}`, 1},
		{"lottery-adaptive", `{"N":[1000000],"P":[10],"R":1,"c":[[1,1]],"k":1}`, 1},
		{"token-certificate", `{"shapes":[[150000,4096,3]],"weights":[0,0],"seed":0,"seeds":1}`, 1},
	} {
		if err := kernels.Validate(v.name, 1, object(t, v.params), v.units); err == nil {
			t.Error("accepted", v)
		}
	}
	if _, err := kernels.Run("selftest", 1, canon.Object{}, 1, 1); err == nil {
		t.Fatal("accepted unit outside task")
	}
}

func TestKernelBoundaries(t *testing.T) {
	r, err := kernels.Run("lottery-adaptive", 1, object(t, `{"N":[120],"P":[2],"R":1,"c":[[0,1]],"k":1}`), 0, 1)
	if err != nil || r["month"].(canon.Object)["loss"] != "0/1" {
		t.Fatal(r, err)
	}
	r, err = kernels.Run("token-certificate", 1, object(t, `{"shapes":[[129,1,1]],"weights":[0,0],"seed":4294967295,"seeds":1}`), 0, 1)
	if err != nil || r["winners"].([]int64)[0] != 0 || r["rows_read"] != int64(129) {
		t.Fatal(r, err)
	}
	r, err = kernels.Run("exit-scam-a", 1, object(t, `{"H0":3,"sizes":{"mode":"fixed","r":2},"n_max":4}`), 0, 1)
	if err != nil || r["count"] != int64(0) {
		t.Fatal(r, err)
	}
}

type unitKey struct { task string; unit int64 }

func golden(t *testing.T, mode string) {
	t.Helper()
	start := time.Now()
	var slowRows map[string][]int64
	if err := json.Unmarshal(fixture(t, "slow.json"), &slowRows); err != nil {
		t.Fatal(err)
	}
	slow := map[unitKey]bool{}
	for task, units := range slowRows {
		for _, unit := range units {
			slow[unitKey{task, unit}] = true
		}
	}
	seen := map[unitKey]bool{}
	checked := 0
	for _, file := range []struct{name string; rows int}{{"golden_list1.jsonl.gz", 702}, {"golden_list2.jsonl.gz", 497}} {
		n := scanFixture(t, file.name, func(raw []byte) {
			r := object(t, string(raw))
			name := r["kernel"].(string)
			unit := r["unit"].(int64)
			key := unitKey{r["task"].(string), unit}
			if seen[key] {
				t.Fatalf("duplicate %v", key)
			}
			seen[key] = true
			sample := name == "token-certificate" || (name == "exit-scam-a" && unit % 10 == 0)
			if (mode == "fast" && slow[key]) || (mode == "long" && !slow[key]) || (mode == "sample" && !sample) {
				return
			}
			got, err := kernels.Run(name, r["kernel_version"].(int64), r["params"].(canon.Object), unit, r["units"].(int64))
			if err != nil {
				t.Fatalf("%v: %v", key, err)
			}
			b, err := canon.Marshal(got, true)
			if err != nil {
				t.Fatal(err)
			}
			want, err := canon.Marshal(r["result"], true)
			if err != nil {
				t.Fatal(err)
			}
			digest := sha256.Sum256(b)
			h := hex.EncodeToString(digest[:])
			if !bytes.Equal(b, want) || h != r["result_sha256"] {
				t.Fatalf("%v: got %s, want %s", key, h, r["result_sha256"])
			}
			checked++
		})
		if n != file.rows {
			t.Fatalf("%s has %d rows", file.name, n)
		}
	}
	want := map[string]int{"fast": 513, "long": 686, "sample": 73, "all": 1199}[mode]
	if checked != want {
		t.Fatalf("%s: checked %d, expected %d", mode, checked, want)
	}
	t.Logf("%s: %d complete results and SHA-256 digests matched in %s", mode, checked, time.Since(start))
}

func TestGoldenFast(t *testing.T) {
	golden(t, "fast")
}

func TestGoldenLong(t *testing.T) {
	mode := os.Getenv("SKYNET_GOLDEN")
	switch mode {
	case "":
		t.Skip("set SKYNET_GOLDEN to sample, long or all")
	case "sample", "long", "all":
		golden(t, mode)
	default:
		t.Fatalf("unknown SKYNET_GOLDEN %q", mode)
	}
}
