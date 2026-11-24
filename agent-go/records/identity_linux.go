//go:build linux

package records

import (
	"errors"
	"os"
	"runtime"
	"syscall"
	"unsafe"
)

// renameat2 numbers for the architectures the agent is built for (the syscall package lacks some).
var renameat2 = map[string]uintptr{"amd64": 316, "arm64": 276, "arm": 382, "386": 353}

// publishSeed makes the finished temporary file the identity without replacing an existing one.
// A hard link is the portable way; Android forbids link() in app storage (SELinux), so there the
// same no-replace guarantee comes from renameat2(RENAME_NOREPLACE).
func publishSeed(from, to string) error {
	err := os.Link(from, to)
	if err == nil || errors.Is(err, os.ErrExist) {
		return err
	}
	if num, ok := renameat2[runtime.GOARCH]; ok {
		src, e1 := syscall.BytePtrFromString(from)
		dst, e2 := syscall.BytePtrFromString(to)
		if e1 == nil && e2 == nil {
			const atFDCWD, renameNoReplace = ^uintptr(99), 1 // AT_FDCWD = -100
			_, _, errno := syscall.Syscall6(num, atFDCWD, uintptr(unsafe.Pointer(src)), atFDCWD,
				uintptr(unsafe.Pointer(dst)), renameNoReplace, 0)
			runtime.KeepAlive(src)
			runtime.KeepAlive(dst)
			switch errno {
			case 0:
				return nil
			case syscall.EEXIST:
				return os.ErrExist
			}
		}
	}
	return err
}
