package main

import (
	"bytes"
	"context"
	"io"
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/records"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/tasks"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/transport"
)

// The board is independent of the compute repository. Ensure --once waits
// for the board poll even when there is no index and no compute worker.
func TestRunOnceBoardPoll(t *testing.T) {
	t.Setenv("SKYNET_AGENT_BASE_URL", "https://repository.invalid")
	task, err := records.Make(bytes.Repeat([]byte{7}, 32), "task", Object{
		"title": "Question", "text": "Research question", "accept": "Provide evidence",
	}, time.Now().Unix())
	if err != nil {
		t.Fatal(err)
	}
	wire, err := records.Wire(task)
	if err != nil {
		t.Fatal(err)
	}
	for _, tc := range []struct {
		name            string
		enabled, paused bool
		wantBoard       bool
	}{{"default", false, false, false}, {"paused", true, true, false}, {"enabled", true, false, true}} {
		t.Run(tc.name, func(t *testing.T) {
			home := t.TempDir()
			cfg := config.Defaults()
			cfg["run_on_battery"], cfg["paused"] = true, tc.paused
			settings := config.Obj(cfg["ai"])
			settings["enabled"], settings["endpoint"] = tc.enabled, "https://model.invalid/v1"
			if err := config.Write(filepath.Join(home, "config.json"), cfg); err != nil {
				t.Fatal(err)
			}
			reads := 0
			rt := roundTrip(func(r *http.Request) (*http.Response, error) {
				w := httptest.NewRecorder()
				if r.Method != http.MethodGet {
					t.Errorf("unexpected publication %s %s", r.Method, r.URL)
				}
				if r.URL.Path != "/v1/records" {
					w.WriteHeader(http.StatusServiceUnavailable)
				} else if reads == 0 {
					reads++
					io.WriteString(w, `{"records":[`+string(wire)+`],"next":1}`)
				} else {
					reads++
					io.WriteString(w, `{"records":[],"next":1}`)
				}
				return w.Result(), nil
			})
			old := http.DefaultTransport
			http.DefaultTransport = rt // release-policy fetch
			t.Cleanup(func() { http.DefaultTransport = old })
			n := transport.Network{HTTP: rt, Receivers: []string{"http://127.0.0.1"}}
			code, err := run(context.Background(), home, n, []string{"--once", "--no-update"})
			if err != nil || code != 3 {
				t.Fatalf("run returned %d, %v", code, err)
			}
			log, err := os.ReadFile(filepath.Join(home, "logs", "agent.log"))
			if err != nil {
				t.Fatal(err)
			}
			rejectedRemote := strings.Contains(string(log), "loopback")
			if (reads == 2) != tc.wantBoard || rejectedRemote != tc.wantBoard {
				t.Fatalf("board reads=%d, model policy applied=%v, log=%s", reads, rejectedRemote, log)
			}
		})
	}
}

func TestHaltInheritedFromPreviousRuntime(t *testing.T) {
	state := Object{"halt": "pause", "halt_seq": config.Sequence - 1, "halt_through": config.Sequence}
	if reason, _ := waitStatus(&tasks.Index{}, config.Defaults(), state, 0, false, true); reason != "paused by the maintainers" {
		t.Fatalf("ignored the pause covering this release: %q", reason)
	}
	state["halt_through"] = config.Sequence - 1
	if reason, _ := waitStatus(&tasks.Index{}, config.Defaults(), state, 0, false, true); reason != "" {
		t.Fatalf("applied a pause for an older release: %q", reason)
	}
}

func TestConfirmOfflineGoRuntime(t *testing.T) {
	for _, runtime := range []string{"go", "python"} {
		t.Run(runtime, func(t *testing.T) {
			home := t.TempDir()
			if err := config.Write(filepath.Join(home, "current.json"), Object{"runtime": runtime, "seq": config.Sequence}); err != nil {
				t.Fatal(err)
			}
			if err := config.Write(filepath.Join(home, "state.json"), Object{"retry_at": time.Now().Add(time.Hour).Unix()}); err != nil {
				t.Fatal(err)
			}
			code, err := run(context.Background(), home, transport.Network{}, []string{"--once", "--no-update"})
			if err != nil || code != 3 {
				t.Fatalf("offline wait returned %d, %v", code, err)
			}
			path := filepath.Join(home, "launch-trial.json")
			if runtime == "python" {
				if _, err := os.Stat(path); !os.IsNotExist(err) {
					t.Fatalf("unexpected change to the Python installation: %v", err)
				}
				return
			}
			trial, err := config.Read(path)
			if err != nil || trial["confirmed"] != true || config.Num(trial["seq"], 0) != config.Sequence {
				t.Fatalf("Go release confirmation: %v, %v", trial, err)
			}
		})
	}
}
