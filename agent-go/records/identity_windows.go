//go:build windows

package records

import (
	"path/filepath"
	"strings"
	"syscall"
)

// MoveFileW is atomic on the same volume and fails if the destination exists.
func publishSeed(from, to string) error {
	path := func(s string) (*uint16, error) {
		p, err := filepath.Abs(s)
		if err != nil {
			return nil, err
		}
		if !strings.HasPrefix(p, `\\?\`) {
			if strings.HasPrefix(p, `\\`) {
				p = `\\?\UNC\` + p[2:]
			} else {
				p = `\\?\` + p
			}
		}
		return syscall.UTF16PtrFromString(p)
	}
	src, err := path(from)
	if err != nil {
		return err
	}
	dst, err := path(to)
	if err != nil {
		return err
	}
	return syscall.MoveFile(src, dst)
}
