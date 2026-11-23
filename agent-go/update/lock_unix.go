//go:build !windows && (linux || darwin || freebsd || openbsd || netbsd)

package update

import (
	"os"
	"syscall"
)

func lock(f *os.File) error     { return syscall.Flock(int(f.Fd()), syscall.LOCK_EX|syscall.LOCK_NB) }
func isLink(s os.FileInfo) bool { return s.Mode()&os.ModeSymlink != 0 }
