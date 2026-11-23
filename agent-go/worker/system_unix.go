//go:build !windows

package worker

import (
	"bytes"
	"context"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
	"sync/atomic"
	"syscall"
)

func lowPriority() { syscall.Setpriority(syscall.PRIO_PROCESS, 0, 19) }
func Battery() (on, known bool) {
	dirs, _ := filepath.Glob("/sys/class/power_supply/*")
	for _, dir := range dirs {
		read := func(k string) string {
			b, _ := os.ReadFile(filepath.Join(dir, k))
			return strings.ToLower(strings.TrimSpace(string(b)))
		}
		switch read("type") {
		case "mains", "usb", "usb_pd", "usb_c", "wireless":
			switch read("online") {
			case "1":
				return false, true
			case "0":
				on, known = true, true
			}
		case "battery":
			if read("status") == "discharging" {
				on, known = true, true
			}
		}
	}
	return
}

var childAttrs *syscall.SysProcAttr

func child(ctx context.Context, exe string, input []byte) ([]byte, error) {
	// The worker gets its own process group: on timeout the whole tree is
	// killed, not just the direct child. Linux also kills it if the
	// supervisor dies (Pdeathsig, tied to the spawning OS thread).
	attrs := &syscall.SysProcAttr{Setpgid: true}
	if childAttrs != nil {
		attrs.Pdeathsig = childAttrs.Pdeathsig
		runtime.LockOSThread()
		defer runtime.UnlockOSThread()
	}
	cmd := exec.Command(exe, "worker")
	cmd.SysProcAttr = attrs
	cmd.Env = append(os.Environ(), "GOMAXPROCS=1")
	cmd.Stdin = bytes.NewReader(input)
	var out bytes.Buffer
	cmd.Stdout = &out
	if err := cmd.Start(); err != nil {
		return nil, err
	}
	done := make(chan struct{})
	var reaped atomic.Bool
	go func() {
		select {
		case <-ctx.Done():
			// The child is the group leader: a negative pid targets the group.
			if !reaped.Load() {
				_ = syscall.Kill(-cmd.Process.Pid, syscall.SIGKILL)
			}
		case <-done:
		}
	}()
	err := cmd.Wait()
	reaped.Store(true)
	close(done)
	return out.Bytes(), err
}
