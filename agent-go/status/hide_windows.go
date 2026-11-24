package status

import (
	"os/exec"
	"syscall"
)

// hideWindow keeps nvidia-smi from opening a console window: the agent runs without one.
func hideWindow(cmd *exec.Cmd) {
	cmd.SysProcAttr = &syscall.SysProcAttr{CreationFlags: 0x08000000} // CREATE_NO_WINDOW
}
