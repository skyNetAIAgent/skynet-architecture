//go:build !windows

package status

import "os/exec"

func hideWindow(cmd *exec.Cmd) {}
