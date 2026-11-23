package update

import (
	"os"
	"syscall"
	"unsafe"
)

var lockFile = syscall.NewLazyDLL("kernel32.dll").NewProc("LockFileEx")

func lock(f *os.File) error {
	var offset syscall.Overlapped
	ok, _, err := lockFile.Call(f.Fd(), 3, 0, 1, 0, uintptr(unsafe.Pointer(&offset)))
	if ok == 0 {
		return err
	}
	return nil
}
func isLink(s os.FileInfo) bool {
	return s.Sys().(*syscall.Win32FileAttributeData).FileAttributes&syscall.FILE_ATTRIBUTE_REPARSE_POINT != 0
}
