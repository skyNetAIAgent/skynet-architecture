package main

import (
	"context"
	"os"
	"path/filepath"
	"testing"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/tasks"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/transport"
)

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
