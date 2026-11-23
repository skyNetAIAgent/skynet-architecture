//go:build !windows && !linux

package autostart

import "errors"

func change(home, action string) (string, error) {
	return "", errors.New("autostart unsupported on this platform")
}
