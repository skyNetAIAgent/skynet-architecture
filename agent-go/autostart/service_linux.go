package autostart

import (
	"bytes"
	"context"
	"errors"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"
)

const unit = "skynet-agent.service"

func ctl(args ...string) (string, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()
	b, err := exec.CommandContext(ctx, "systemctl", append([]string{"--user"}, args...)...).CombinedOutput()
	return strings.TrimSpace(string(b)), err
}
func unitWrite(p string, b []byte) error {
	f, err := os.CreateTemp(filepath.Dir(p), ".unit-")
	if err != nil {
		return err
	}
	defer os.Remove(f.Name())
	_, err = f.Write(b)
	ce := f.Close()
	if err != nil {
		return err
	}
	if ce != nil {
		return ce
	}
	return os.Rename(f.Name(), p)
}
func change(home, action string) (string, error) {
	base, err := os.UserConfigDir()
	if err != nil {
		return "", err
	}
	p := filepath.Join(base, "systemd", "user", unit)
	if strings.ContainsAny(home, "\n\r\x00") {
		return "", errors.New("invalid unit path")
	}
	quote := strings.NewReplacer("\\", "\\\\", "\"", "\\\"", "%", "%%", "$", "$$")
	line := "ExecStart=\"" + quote.Replace(filepath.Join(home, "skynet-agent")) + "\" launch run"
	_, unitErr := os.Lstat(p)
	if errors.Is(unitErr, os.ErrNotExist) && action != "enable" {
		return "off", nil
	}
	status, queryErr := ctl("is-enabled", unit)
	on := status == "enabled" || status == "enabled-runtime"
	if queryErr != nil && status != "disabled" && status != "not-found" && status != "masked" {
		if !errors.Is(unitErr, os.ErrNotExist) {
			return "", fmt.Errorf("systemctl is-enabled: %s: %w", status, queryErr)
		}
	}
	switch action {
	case "status":
		if on {
			return "on", nil
		}
		return "off", nil
	case "disable":
		if on {
			if out, err := ctl("disable", "--now", unit); err != nil {
				return out, err
			}
		}
		if err := os.Remove(p); err != nil && !errors.Is(err, os.ErrNotExist) {
			return "", err
		}
		return ctl("daemon-reload")
	case "migrate":
		if !on {
			return "off", nil
		}
	}
	old, err := os.ReadFile(p)
	if err != nil && !errors.Is(err, os.ErrNotExist) {
		return "", err
	}
	data := []byte("[Unit]\nDescription=SkyNet research agent\nAfter=network-online.target\n\n[Service]\n" + line + "\nRestart=on-failure\nRestartSec=60\nNice=19\n\n[Install]\nWantedBy=default.target\n")
	if action == "migrate" {
		lines := strings.Split(string(old), "\n")
		found := false
		for i, l := range lines {
			if strings.HasPrefix(l, "ExecStart=\"") && strings.HasSuffix(l, "\" \""+filepath.Join(home, "launcher.py")+"\" run") {
				lines[i] = line
				found = true
			}
		}
		if !found {
			return "existing registration retained", nil
		}
		data = []byte(strings.Join(lines, "\n"))
	}
	if err = os.MkdirAll(filepath.Dir(p), 0700); err != nil {
		return "", err
	}
	if !bytes.Equal(data, old) {
		if err = unitWrite(p, data); err != nil {
			return "", err
		}
		if out, err := ctl("daemon-reload"); err != nil {
			var restore error
			if old != nil {
				restore = unitWrite(p, old)
			} else {
				restore = os.Remove(p)
			}
			_, reload := ctl("daemon-reload")
			return out, errors.Join(err, restore, reload)
		}
	}
	if action == "enable" {
		return ctl("enable", "--now", unit)
	}
	return "on", nil
}
