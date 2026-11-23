//go:build windows

package worker

import (
	"bytes"
	"context"
	"os"
	"os/exec"
	"syscall"
	"unsafe"
)

var kernel32 = syscall.NewLazyDLL("kernel32.dll")

func lowPriority() {
	p, err := syscall.GetCurrentProcess()
	if err == nil {
		kernel32.NewProc("SetPriorityClass").Call(uintptr(p), 0x40)
	}
}
func Battery() (on, known bool) {
	var status struct {
		AC, Flag, Percent, Reserved byte
		Life, Full                  uint32
	}
	ok, _, _ := kernel32.NewProc("GetSystemPowerStatus").Call(uintptr(unsafe.Pointer(&status)))
	return status.AC == 0, ok != 0 && status.AC <= 1
}
func child(ctx context.Context, exe string, input []byte) ([]byte, error) {
	cmd := exec.CommandContext(ctx, exe, "worker")
	cmd.Env = append(os.Environ(), "GOMAXPROCS=1")
	cmd.SysProcAttr = &syscall.SysProcAttr{CreationFlags: 0x08000040}
	cmd.Stdin = bytes.NewReader(input)
	return cmd.Output()
}
