package worker

import "syscall"

func init() {
	// Linux (including Android) kills an outstanding worker if its supervisor dies.
	childAttrs = &syscall.SysProcAttr{Pdeathsig: syscall.SIGKILL}
}
