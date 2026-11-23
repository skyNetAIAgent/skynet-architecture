package worker

import (
	"context"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strconv"
	"strings"
	"testing"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
)

// Run the test binary as the worker subprocess, just as the CLI does.
func TestMain(m *testing.M) {
	if len(os.Args) == 2 && os.Args[1] == "worker" {
		if os.Getenv("G2_TEST_SLOW_WORKER") == "1" {
			io.Copy(io.Discard, os.Stdin)
			time.Sleep(time.Minute)
		}
		if Work(os.Stdin, os.Stdout) != nil {
			os.Exit(1)
		}
		return
	}
	os.Exit(m.Run())
}

func TestWorkerProcess(t *testing.T) {
	job := canon.Object{"kernel": "selftest", "kernel_version": 1, "params": canon.Object{"rounds": 8}, "units": 1, "max_seconds": 10}
	ctx := context.Background()
	r := Run(ctx, job, 0, 1)
	if r["ok"] != true {
		t.Fatal(r)
	}
	if _, ok := r["elapsed_s"].(float64); !ok {
		t.Fatal("elapsed_s lost its float type")
	}
	t.Setenv("G2_TEST_SLOW_WORKER", "1")
	job["max_seconds"] = 1
	start := time.Now()
	if r := Run(ctx, job, 0, 1); r["timeout"] != true || time.Since(start) > 10*time.Second {
		t.Fatal("child outlived deadline", r)
	}
}

// TestChildProcessGroupKill checks that the hard timeout kills not only the
// direct worker child but also its own children: the worker starts in a
// dedicated process group and the group is killed when the context expires.
func TestChildProcessGroupKill(t *testing.T) {
	if runtime.GOOS == "windows" {
		t.Skip("process groups are a Unix mechanism")
	}
	dir := t.TempDir()
	helper := filepath.Join(dir, "helper")
	os.WriteFile(filepath.Join(dir, "main.go"), []byte(`package main

import (
	"fmt"
	"os/exec"
	"time"
)

func main() {
	cmd := exec.Command("sleep", "60")
	if err := cmd.Start(); err != nil {
		return
	}
	fmt.Println(cmd.Process.Pid)
	time.Sleep(time.Minute)
}
`), 0600)
	build := exec.Command("go", "build", "-buildvcs=false", "-o", helper, filepath.Join(dir, "main.go"))
	if out, err := build.CombinedOutput(); err != nil {
		t.Fatalf("building helper: %v\n%s", err, out)
	}
	ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
	defer cancel()
	start := time.Now()
	out, err := child(ctx, helper, nil)
	if err == nil || time.Since(start) > 20*time.Second {
		t.Fatalf("child outlived deadline: %v", err)
	}
	grandchild, err := strconv.Atoi(strings.TrimSpace(string(out)))
	if err != nil {
		t.Fatalf("helper did not report its child pid: %q", out)
	}
	deadline := time.Now().Add(2 * time.Second)
	for time.Now().Before(deadline) {
		if _, err := os.Stat(filepath.Join("/proc", strconv.Itoa(grandchild))); os.IsNotExist(err) {
			return // the whole tree is gone
		}
		time.Sleep(20 * time.Millisecond)
	}
	t.Fatalf("grandchild %d survived the timeout", grandchild)
}
