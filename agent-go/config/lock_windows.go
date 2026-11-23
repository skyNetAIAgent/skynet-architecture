//go:build windows

package config

import (
	"os"
	"syscall"
	"unsafe"
)

var lockFile = syscall.NewLazyDLL("kernel32.dll").NewProc("LockFileEx")

func tryLock(f *os.File) error {
	var offset syscall.Overlapped
	ok, _, err := lockFile.Call(f.Fd(), 3, 0, 1, 0, uintptr(unsafe.Pointer(&offset)))
	if ok == 0 {
		if err == syscall.Errno(33) {
			return ErrLocked
		}
		return err
	}
	return nil
}
