package main

import (
	"bytes"
	"context"
	"io"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"testing"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/outbox"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/records"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/transport"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/worker"
)

// The worker subprocess runs this test binary with a single "worker" argument.
func TestMain(m *testing.M) {
	if len(os.Args) == 2 && os.Args[1] == "worker" {
		if err := worker.Work(os.Stdin, os.Stdout); err != nil {
			os.Exit(1)
		}
		return
	}
	os.Exit(m.Run())
}

type roundTrip func(*http.Request) (*http.Response, error)

func (fn roundTrip) RoundTrip(r *http.Request) (*http.Response, error) { return fn(r) }

// TestRunOnceEndToEnd drives the whole G2 loop in memory: a Python-created
// profile, the signed task index over an in-memory HTTP transport, one worker
// child process, the outbox entry with a single signed net_record and the
// state update. Network sockets are unavailable in the sandbox, so the HTTP
// layer is a RoundTripper stub exactly like the repository's own tests.
func TestRunOnceEndToEnd(t *testing.T) {
	t.Setenv("SKYNET_AGENT_BASE_URL", "https://127.0.0.1:1")
	t.Setenv("SKYNET_AGENT_RECEIVERS", "none")
	t.Setenv("SKYNET_AGENT_RELAYS", "none")
	t.Setenv("SKYNET_AGENT_HOME", "")
	home := t.TempDir()
	fixture := filepath.Join("..", "..", "testdata", "python-home")
	for _, name := range []string{"identity.key", "config.json", "state.json", "task-list.json"} {
		b, err := os.ReadFile(filepath.Join(fixture, fixtureFile(name)))
		if err != nil {
			t.Fatal(err)
		}
		if err := os.WriteFile(filepath.Join(home, name), b, 0600); err != nil {
			t.Fatal(err)
		}
	}
	old, err := os.ReadFile(filepath.Join(fixture, "outbox", "1700000000000-old-task-0.json"))
	if err != nil {
		t.Fatal(err)
	}
	if err := os.MkdirAll(filepath.Join(home, "outbox"), 0700); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(filepath.Join(home, "outbox", "1700000000000-old-task-0.json"), old, 0600); err != nil {
		t.Fatal(err)
	}
	cfg, err := config.Load(home)
	if err != nil {
		t.Fatal(err)
	}
	cfg["submit"] = "auto"
	if err := config.Write(filepath.Join(home, "config.json"), cfg); err != nil {
		t.Fatal(err)
	}
	n := transport.Network{Receivers: []string{"http://127.0.0.1:9"}, HTTP: roundTrip(func(r *http.Request) (*http.Response, error) {
		if r.Method == "POST" {
			body, err := io.ReadAll(r.Body)
			if err != nil {
				t.Fatal(err)
			}
			v, err := canon.Parse(body)
			if err != nil {
				t.Fatal(err)
			}
			env := config.Obj(v)
			return &http.Response{StatusCode: 200, Body: io.NopCloser(bytes.NewReader([]byte(
				`{"ok":true,"id":"` + config.Str(env["id"]) + `"}`)))}, nil
		}
		path := filepath.Join("..", "..", "testdata", filepath.Base(r.URL.Path))
		b, err := os.ReadFile(path)
		if err != nil {
			// The page query of the receiver sync.
			return &http.Response{StatusCode: 200, Body: io.NopCloser(bytes.NewReader([]byte(
				`{"records":[],"next":` + r.URL.Query().Get("after") + `}`)))}, nil
		}
		return &http.Response{StatusCode: 200, Body: io.NopCloser(bytes.NewReader(b))}, nil
	})}
	ctx, cancel := context.WithTimeout(context.Background(), 60*time.Second)
	defer cancel()
	code, err := run(ctx, home, n, []string{"--once", "--no-update"})
	if err != nil || code != 0 {
		t.Fatalf("run returned %d, %v", code, err)
	}
	state, err := config.State(home)
	if err != nil {
		t.Fatal(err)
	}
	counters := config.Obj(state["counters"])
	if config.Num(counters["units_done"], 0) != 2 {
		t.Fatalf("units_done = %v", counters["units_done"])
	}
	if config.Num(counters["published"], 0) != 2 {
		t.Fatalf("published = %v", counters["published"])
	}
	left, err := outbox.Entries(home, "outbox")
	if err != nil || len(left) != 0 {
		t.Fatalf("outbox entries left: %v, %v", len(left), err)
	}
	sent, err := outbox.Entries(home, "sent")
	if err != nil || len(sent) != 2 {
		t.Fatalf("sent entries: %v, %v", len(sent), err)
	}
	var fresh outbox.Entry
	for _, e := range sent {
		if config.Str(config.Obj(e.Data["record"])["task"]) != "old-task" {
			fresh = e
		}
	}
	if fresh.Name == "" {
		t.Fatal("no fresh sent entry")
	}
	task := config.Str(config.Obj(fresh.Data["record"])["task"])
	unit := config.Num(config.Obj(fresh.Data["record"])["unit"], -1)
	done, _ := config.Obj(state["done"])[task].([]any)
	if len(done) != 1 || config.Num(done[0], -1) != unit {
		t.Fatalf("state.done[%s] = %v, outbox unit %d", task, done, unit)
	}
	env := config.Obj(fresh.Data["net_record"])
	if env == nil {
		t.Fatal("no signed net_record")
	}
	if err := records.Verify(env, time.Now().Unix()); err != nil {
		t.Fatal(err)
	}
	payload := config.Obj(config.Obj(env["body"])["payload"])
	inner := config.Obj(payload["record"])
	if inner["result"] == nil || inner["result_sha256"] == nil || inner["agent"] != "0.3.0" {
		t.Fatalf("inner record: %v", inner)
	}
	if config.Num(state["publish_fails"], 0) != 0 || config.Num(state["publish_after"], 0) != 0 {
		t.Fatalf("backoff after success: %v", state)
	}
	// The reference implementation must accept what the Go agent produced.
	if testing.Short() {
		return
	}
	python := ""
	for _, name := range []string{"python3", "python"} {
		// On Windows "python3" may be a Store stub that only prints a hint.
		if exec.Command(name, "-c", "pass").Run() == nil {
			python = name
			break
		}
	}
	if python == "" {
		t.Skip("Python unavailable for the cross-check")
	}
	pyAgent := filepath.Join("..", "..", "..", "agent")
	if _, err := os.Stat(pyAgent); err != nil {
		t.Skipf("Python reference agent not present at %s; skipping cross-check", pyAgent)
	}
	py := filepath.Join(home, "fresh-entry.json")
	raw, err := os.ReadFile(filepath.Join(home, "sent", fresh.Name))
	if err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(py, raw, 0600); err != nil {
		t.Fatal(err)
	}
	script := `import json, sys
sys.path.insert(0, sys.argv[1])
from skynet_agent import records, submit
entry = json.load(open(sys.argv[2], encoding="utf-8"))
env = records.verify(entry["net_record"])
rec = entry["record"]
assert rec["result_sha256"] == submit.result_hash(rec["result"]), "result hash"
assert env["body"]["payload"]["record"] == rec, "inner record"
print("PY_OK", env["id"])
`
	cmd := exec.Command(python, "-c", script, pyAgent, py)
	out, err := cmd.CombinedOutput()
	if err != nil {
		t.Fatalf("Python rejected the Go output: %v\n%s", err, out)
	}
	if !bytes.Contains(out, []byte("PY_OK")) {
		t.Fatalf("unexpected Python output: %s", out)
	}
}

// fixtureFile maps a profile file to its name in testdata (the device key is
// stored as identity.key.fixture so that release tools do not take it for a secret).
func fixtureFile(name string) string {
	if name == "identity.key" {
		return "identity.key.fixture"
	}
	return name
}
