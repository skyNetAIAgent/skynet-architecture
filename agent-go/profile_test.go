package agentgo_test

import (
	"bytes"
	"context"
	"errors"
	"fmt"
	"io"
	"io/fs"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/board"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/outbox"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/records"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/tasks"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/transport"
)

func pythonHome(t *testing.T) string {
	t.Helper()
	root := filepath.Join("testdata", "python-home")
	home := t.TempDir()
	err := filepath.WalkDir(root, func(p string, e fs.DirEntry, err error) error {
		if err != nil {
			return err
		}
		name, err := filepath.Rel(root, p)
		if err != nil {
			return err
		}
		out := filepath.Join(home, strings.TrimSuffix(name, ".fixture"))
		if e.IsDir() {
			return os.MkdirAll(out, 0700)
		}
		b, err := os.ReadFile(p)
		if err != nil {
			return err
		}
		return os.WriteFile(out, b, 0600)
	})
	if err != nil {
		t.Fatal(err)
	}
	return home
}

type roundTrip func(*http.Request) (*http.Response, error)

func (fn roundTrip) RoundTrip(r *http.Request) (*http.Response, error) { return fn(r) }
func TestPythonProfileRetry(t *testing.T) {
	home := pythonHome(t)
	seed, err := records.LoadSeed(home, false)
	if err != nil || len(seed) != 32 {
		t.Fatal(err)
	}
	cfg, err := config.Load(home)
	if err != nil {
		t.Fatal(err)
	}
	st, err := config.State(home)
	if err != nil {
		t.Fatal(err)
	}
	idx, err := tasks.Cached(home, 2)
	if err != nil || len(idx.Tasks) != 13 {
		t.Fatal(err)
	}
	if _, err = tasks.Cached(home, 3); err == nil {
		t.Fatal("accepted older cache")
	}
	jobs, u := tasks.Pick(idx.Tasks, st, nil, nil)
	if jobs == nil || u.ID != "selftest-1" || u.Number != 0 {
		t.Fatal("unexpected work", u)
	}
	if v, _ := tasks.Pick(idx.Tasks, st, nil, map[tasks.Unit]bool{u: true}); v != nil {
		t.Fatal("picked busy unit")
	}
	entries, err := outbox.Entries(home, "outbox")
	if err != nil || len(entries) != 1 {
		t.Fatal(err)
	}
	name := entries[0].Name
	path := filepath.Join(home, "outbox", name)
	original, _ := os.ReadFile(path)
	env := config.Obj(entries[0].Data["net_record"])
	wire, _ := records.Wire(env)
	// The first request reaches the receiver, but its acknowledgement is lost.
	tries := 0
	n := transport.Network{Receivers: []string{"http://127.0.0.1"}, HTTP: roundTrip(func(r *http.Request) (*http.Response, error) {
		raw, err := io.ReadAll(r.Body)
		if err != nil || !bytes.Equal(raw, wire) {
			return nil, errors.New("retry changed signed bytes")
		}
		tries++
		if tries == 1 {
			return nil, io.ErrUnexpectedEOF
		}
		return &http.Response{StatusCode: 200, Body: io.NopCloser(strings.NewReader(fmt.Sprintf(`{"ok":true,"id":"%s"}`, env["id"])))}, nil
	})}
	ctx := context.Background()
	cfg["submit_via"] = "github"
	if count, e := outbox.Flush(ctx, home, n, cfg, st, true); count != 0 || e != nil || tries != 0 {
		t.Fatal("GitHub item sent", e)
	}
	cfg["submit_via"] = "net"
	if count, e := outbox.Flush(ctx, home, n, cfg, st, true); count != 0 || e == nil || tries != 1 {
		t.Fatalf("lost ACK count=%d tries=%d err=%v", count, tries, e)
	}
	after, _ := os.ReadFile(path)
	if !bytes.Equal(after, original) {
		t.Fatal("existing signed entry rewritten")
	}
	if count, e := outbox.Flush(ctx, home, n, cfg, st, true); count != 1 || e != nil || tries != 2 {
		t.Fatalf("retry count=%d tries=%d err=%v", count, tries, e)
	}
	sent, err := config.Read(filepath.Join(home, "sent", name))
	if err != nil {
		t.Fatal(err)
	}
	saved := config.Obj(sent["net_record"])
	if saved["id"] != env["id"] || records.Verify(saved, time.Now().Unix()) != nil {
		t.Fatal("signature changed during archive")
	}
	for _, f := range []string{"identity.key", "config.json", "state.json", "task-list.json"} {
		before, _ := os.ReadFile(filepath.Join("testdata", "python-home", fixtureName(f)))
		after, err := os.ReadFile(filepath.Join(home, f))
		if err != nil || !bytes.Equal(before, after) {
			t.Fatal("rewritten", f, err)
		}
	}
	if err = config.Set(cfg, "workers", "2"); err != nil {
		t.Fatal(err)
	}
	if err = config.Write(filepath.Join(home, "config.json"), cfg); err != nil {
		t.Fatal(err)
	}
	cfg, err = config.Load(home)
	if err != nil || config.Get(cfg, "ai.extra") != "preserve" || fmt.Sprint(config.Get(cfg, "extra.big")) != "1180591620717411303424" {
		t.Fatal("unknown config lost", err)
	}
}
func TestPythonBoard(t *testing.T) {
	fixture, err := config.Read(filepath.Join("testdata", "python-board.json"))
	if err != nil {
		t.Fatal(err)
	}
	now := config.Num(fixture["now"], 0)
	var rows []canon.Object
	var task, report string
	for _, v := range fixture["records"].([]any) {
		e := config.Obj(v)
		if err := records.Verify(e, now); err != nil {
			t.Fatal(err)
		}
		rows = append(rows, e)
		switch board.Kind(e) {
		case "task":
			task = board.ID(e)
		case "report":
			report = board.ID(e)
		}
	}
	i := board.Build(rows, now)[task]
	if i.Status() != fixture["status"] || len(i.Claims) != 1 || len(i.Reports) != 1 || board.ID(i.Verdicts[report]) != fixture["verdict"] {
		t.Fatal("board differs from Python")
	}
}
func TestExpiryAndLocks(t *testing.T) {
	idx := tasks.Index{Doc: canon.Object{"expires": "2026-11-23"}}
	last := time.Date(2026, 11, 23, 23, 59, 59, 0, time.UTC)
	if idx.Expired(last) || !idx.Expired(last.Add(time.Second)) {
		t.Fatal("wrong UTC expiration boundary")
	}
	p := filepath.Join(t.TempDir(), "agent.lock")
	l, err := config.Lock(p)
	if err != nil {
		t.Fatal(err)
	}
	if l2, err := config.Lock(p); err == nil {
		l2.Close()
		t.Fatal("duplicate instance")
	}
	l.Close()
	l, err = config.Lock(p)
	if err != nil {
		t.Fatal(err)
	}
	l.Close()
}

func TestSignedIndexRefresh(t *testing.T) {
	home := t.TempDir()
	t.Setenv("SKYNET_AGENT_BASE_URL", "https://repository.invalid")
	tamper := false
	n := transport.Network{HTTP: roundTrip(func(r *http.Request) (*http.Response, error) {
		path := filepath.Join("testdata", filepath.Base(r.URL.Path))
		b, err := os.ReadFile(path)
		if err != nil {
			return nil, err
		}
		if tamper && r.URL.Path == "/tasks/index.json" {
			b = append(b, ' ')
		}
		return &http.Response{StatusCode: 200, Body: io.NopCloser(bytes.NewReader(b))}, nil
	})}
	ctx := context.Background()
	if _, err := tasks.Fetch(ctx, n, home, 2); err != nil {
		t.Fatal(err)
	}
	if _, err := tasks.Fetch(ctx, n, home, 3); err == nil {
		t.Fatal("accepted rollback")
	}
	tamper = true
	if _, err := tasks.Fetch(ctx, n, home, 2); err == nil {
		t.Fatal("accepted modified bytes")
	}
	if _, err := tasks.Cached(home, 2); err != nil {
		t.Fatal("lost verified cache", err)
	}
}

// fixtureName maps a profile file to its name in testdata: the device key is
// stored as identity.key.fixture so that release tools do not take it for a secret.
func fixtureName(name string) string {
	if name == "identity.key" {
		return "identity.key.fixture"
	}
	return name
}
