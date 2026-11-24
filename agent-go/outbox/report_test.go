package outbox

import (
	"bytes"
	"context"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/records"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/transport"
)

type receiverFunc func(*http.Request) (*http.Response, error)

func (f receiverFunc) RoundTrip(r *http.Request) (*http.Response, error) { return f(r) }

func TestReportReviewAndRetry(t *testing.T) {
	home := t.TempDir()
	ctx := context.Background()
	taskID := strings.Repeat("3", 64)
	name, err := SaveReportDraft(home, taskID, "original answer")
	if err != nil {
		t.Fatal(err)
	}
	cfg := config.Defaults()
	config.Obj(cfg["ai"])["review_before_submit"] = false // legacy Python profile
	state, err := config.State(home)
	if err != nil {
		t.Fatal(err)
	}
	var attempts int
	var first []byte
	var sendErr error
	n := transport.Network{Receivers: []string{"http://127.0.0.1"}, HTTP: receiverFunc(func(req *http.Request) (*http.Response, error) {
		b, err := io.ReadAll(req.Body)
		if err != nil {
			return nil, err
		}
		env, err := records.Parse(b, time.Now().Unix())
		if err != nil {
			sendErr = err
			return nil, err
		}
		body := config.Obj(env["body"])
		p := config.Obj(body["payload"])
		if body["type"] != "report" || p["task"] != taskID || p["summary"] != "machine-generated, unverified" || p["text"] != "human revision" {
			sendErr = fmt.Errorf("incorrect published payload %v", p)
			return nil, sendErr
		}
		attempts++
		if attempts == 1 {
			first = b
			return nil, io.ErrUnexpectedEOF // receiver accepted it, but lost the ACK
		}
		if !bytes.Equal(first, b) {
			sendErr = errors.New("retry changed approved report bytes")
			return nil, sendErr
		}
		return &http.Response{StatusCode: 200, Body: io.NopCloser(strings.NewReader(fmt.Sprintf(`{"ok":true,"id":"%s"}`, env["id"])))}, nil
	})}
	unsent := func(force bool) {
		t.Helper()
		count, err := Flush(ctx, home, n, cfg, state, force)
		if err != nil || count != 0 || attempts != 0 || sendErr != nil {
			t.Fatalf("unapproved delivery attempt: count=%d attempts=%d err=%v %v", count, attempts, err, sendErr)
		}
		if _, err := os.Stat(filepath.Join(home, "net", "records.jsonl")); !errors.Is(err, os.ErrNotExist) {
			t.Fatal("unapproved report touched journal", err)
		}
	}
	unsent(false)
	unsent(true)
	_, oldHash, err := ReviewReport(home, name)
	if err != nil {
		t.Fatal(err)
	}
	if err = ApproveReport(home, name, oldHash); err != nil {
		t.Fatal(err)
	}
	// A manual file edit leaves stale approval fields; even a matching
	// boolean/hash cannot authorize text different from the signed payload.
	path := filepath.Join(home, "outbox", name)
	o, err := config.Read(path)
	if err != nil {
		t.Fatal(err)
	}
	o["text"] = "file replacement"
	o["approved_sha256"] = reportHash(o)
	if err = config.Write(path, o); err != nil {
		t.Fatal(err)
	}
	unsent(true)
	if err = ApproveReport(home, name, oldHash); err == nil {
		t.Fatal("approved text changed since show")
	}
	if err = EditReport(home, name, "human revision"); err != nil {
		t.Fatal(err)
	}
	if err = ApproveReport(home, name, oldHash); err == nil {
		t.Fatal("accepted stale review hash")
	}
	unsent(false)
	_, hash, err := ReviewReport(home, name)
	if err != nil {
		t.Fatal(err)
	}
	if err = ApproveReport(home, name, hash); err != nil {
		t.Fatal(err)
	}
	if count, err := Flush(ctx, home, n, cfg, state, true); count != 0 || err == nil || attempts != 1 || sendErr != nil {
		t.Fatalf("missing first attempt or retry: %d %d %v %v", count, attempts, err, sendErr)
	}
	if err := EditReport(home, name, "changed after possible delivery"); err == nil {
		t.Fatal("edited after publication began")
	}
	if count, err := Flush(ctx, home, n, cfg, state, true); err != nil || count != 1 || attempts != 2 || sendErr != nil {
		t.Fatalf("retry: %d %d %v %v", count, attempts, err, sendErr)
	}
	s, err := transport.Open(home)
	if err != nil {
		t.Fatal(err)
	}
	defer s.Close()
	if len(s.Items) != 1 {
		t.Fatalf("expected one report in the journal, got %d", len(s.Items))
	}
}

func TestReportDropAndLimits(t *testing.T) {
	home := t.TempDir()
	task := strings.Repeat("b", 64)
	cfg := config.Defaults()
	config.Obj(cfg["ai"])["max_answer_chars"] = 3
	if err := config.Write(filepath.Join(home, "config.json"), cfg); err != nil {
		t.Fatal(err)
	}
	for _, bad := range []string{"", "四个汉字", "a\x1bb", "a\rb", "a\u202eb"} {
		if _, err := SaveReportDraft(home, task, bad); err == nil {
			t.Fatalf("accepted invalid text %q", bad)
		}
	}
	name, err := SaveReportDraft(home, task, "三汉字")
	if err != nil {
		t.Fatal(err)
	}
	if _, err := SaveReportDraft(home, task, "two"); err == nil {
		t.Fatal("overwrote pending draft")
	}
	if err := DropReport(home, name); err != nil {
		t.Fatal(err)
	}
	if seen, err := ReportSeen(home, task); !seen || err != nil {
		t.Fatal("forgot dismissal", err)
	}
	if _, err := SaveReportDraft(home, task, "new"); err == nil {
		t.Fatal("recreated dropped draft")
	}
	if _, _, err := ReviewReport(home, filepath.Join("..", "ai-dismissed", name)); err == nil {
		t.Fatal("read outside outbox")
	}
	if _, err := SaveReportDraft(home, "../path", "new"); err == nil {
		t.Fatal("invalid task id became a file name")
	}
}

func TestPruneDismissedBoundsGrowth(t *testing.T) {
	home := t.TempDir()
	onBoard, offBoard := strings.Repeat("a", 64), strings.Repeat("b", 64)
	for _, id := range []string{onBoard, offBoard} {
		if err := config.Write(dismissedPath(home, reportName(id)), Object{"task": id}); err != nil {
			t.Fatal(err)
		}
	}
	if err := os.WriteFile(filepath.Join(home, "net", "ai-dismissed", "odd.json"), []byte("{}"), 0600); err != nil {
		t.Fatal(err)
	}
	if err := PruneDismissed(home, map[string]bool{onBoard: true}); err != nil {
		t.Fatal(err)
	}
	for _, id := range []string{onBoard, offBoard} {
		seen, err := ReportSeen(home, id)
		if err != nil || seen != (id == onBoard) {
			t.Fatalf("marker for task on board=%v: seen=%v, err=%v", id == onBoard, seen, err)
		}
	}
	if _, err := os.Stat(filepath.Join(home, "net", "ai-dismissed", "odd.json")); err != nil {
		t.Fatal("unrelated marker file removed", err)
	}
}

func TestArchiveRetainsNewResultAlongsideReports(t *testing.T) {
	home := t.TempDir()
	sent := filepath.Join(home, "sent")
	if err := os.Mkdir(sent, 0700); err != nil {
		t.Fatal(err)
	}
	for i := 0; i < Limit; i++ {
		path := filepath.Join(sent, reportName(fmt.Sprintf("%064x", i)))
		if err := os.WriteFile(path, []byte("{}"), 0600); err != nil {
			t.Fatal(err)
		}
	}
	state, err := config.State(home)
	if err != nil {
		t.Fatal(err)
	}
	name := "1770000000000-worker-0.json"
	e := Entry{name, Object{"record": Object{"task": "worker", "unit": 0}}}
	if err := config.Write(filepath.Join(home, "outbox", name), e.Data); err != nil {
		t.Fatal(err)
	}
	if err := archive(home, e, strings.Repeat("0", 64)); err != nil {
		t.Fatal(err)
	}
	if err := Recover(home, state); err != nil || config.Obj(state["done"])["worker"] == nil {
		t.Fatal("could not recover recently archived compute result", err)
	}
	if names, err := Names(home, "sent"); err != nil || len(names) != Limit {
		t.Fatal("wrong archive size", len(names), err)
	}
}
