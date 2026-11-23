// Package autostart manages the current user's login registration.
package autostart

import (
	"errors"
	"path/filepath"
)

const name = "SkyNetAgent"

func Change(home, action string) (string, error) {
	h, err := filepath.Abs(home)
	if err != nil {
		return "", err
	}
	switch action {
	case "enable", "disable", "status", "migrate":
		return change(h, action)
	}
	return "", errors.New("expected enable, disable or status")
}
