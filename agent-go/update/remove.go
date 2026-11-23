package update

import (
	"errors"
	"os"
	"path/filepath"
	"regexp"
	"runtime"
	"strings"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/autostart"
)

// Remove stops a Linux installation before removing its executables and owned shim.
func Remove(home string, purge bool) error {
	if runtime.GOOS != "linux" {
		return errors.New("use the Windows installer to uninstall")
	}
	return Locked(home, func() error {
		c, err := CurrentVersion(home)
		if err != nil {
			return err
		}
		if _, err = VerifiedPath(home, c.Entry); err != nil {
			return err
		}
		if _, err = autostart.Change(home, "disable"); err != nil {
			return err
		}
		path := filepath.Join(home, "agent.lock")
		if err = regular(path); err != nil && !errors.Is(err, os.ErrNotExist) {
			return err
		}
		f, err := os.OpenFile(path, os.O_RDWR|os.O_CREATE, 0600)
		if err != nil {
			return err
		}
		defer f.Close()
		if err = lock(f); err != nil {
			if err = write(filepath.Join(home, "stop"), []byte("stop\n"), 0600); err != nil {
				return err
			}
			until := time.Now().Add(time.Minute)
			for err = lock(f); err != nil; err = lock(f) {
				if time.Now().After(until) {
					return errors.New("agent is still running")
				}
				time.Sleep(250 * time.Millisecond)
			}
		}
		user, err := os.UserHomeDir()
		if err != nil {
			return err
		}
		shim := filepath.Join(user, ".local", "bin", "skynet-agent")
		expected := "#!/bin/sh\nexec '" + strings.ReplaceAll(filepath.Join(home, Binary()), "'", "'\\''") + "' launch \"$@\"\n"
		if b, err := read(shim, 8192); err == nil && string(b) == expected {
			if err = os.Remove(shim); err != nil {
				return err
			}
		}
		if err = removeVersions(home, "versions", `^[0-9]+-[0-9]+\.[0-9]+\.[0-9]+$`); err != nil {
			return err
		}
		if err = removeVersions(home, "python", `^[0-9a-f]{64}$`); err != nil {
			return err
		}
		names := []string{Binary(), "current.json", "launcher.py", "launch-trial.json", "uninstall.py", "stop"}
		if purge {
			names = append(names, "identity.key", "outbox", "net", "sent", "logs", "config.json", "state.json", "task-list.json", "github-token", "bad_seqs.json", "max_seq.json", "release-history.json", "release-policy.json")
		}
		for _, name := range names {
			if err = os.RemoveAll(filepath.Join(home, name)); err != nil {
				return err
			}
		}
		// Keep the lock inodes so concurrent installers cannot acquire a different lock.
		return nil
	})
}

func removeVersions(home, name, pattern string) error {
	dir := filepath.Join(home, name)
	if err := directory(dir); err != nil {
		if errors.Is(err, os.ErrNotExist) {
			return nil
		}
		return err
	}
	children, err := os.ReadDir(dir)
	if err != nil {
		return err
	}
	owned := regexp.MustCompile(pattern)
	for _, child := range children {
		if owned.MatchString(child.Name()) {
			if err = os.RemoveAll(filepath.Join(dir, child.Name())); err != nil {
				return err
			}
		}
	}
	children, err = os.ReadDir(dir)
	if err == nil && len(children) == 0 {
		return os.Remove(dir)
	}
	return err
}
