package update

import (
	"bytes"
	"context"
	"errors"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"time"
)

type installer struct {
	keys  []string
	fetch func(Target) ([]byte, error)
	check func(string, string) error
	probe func(string, string) error
}

func checkCandidate(home, dir string) error {
	return checkCommand(home, filepath.Join(dir, Binary()), "verify-install")
}

func checkLauncher(home, executable string) error {
	return checkCommand(home, executable, "launch", "--check")
}

func checkCommand(home, executable string, args ...string) error {
	ctx, cancel := context.WithTimeout(context.Background(), 60*time.Second)
	defer cancel()
	cmd := exec.CommandContext(ctx, executable, args...)
	cmd.Dir = filepath.Dir(executable)
	cmd.Env = append(os.Environ(), "SKYNET_AGENT_HOME="+home)
	cmd.Stderr = os.Stderr
	return cmd.Run()
}
func (i installer) prepare(home string, d document, e Entry) (string, error) {
	versions := filepath.Join(home, "versions")
	if err := os.MkdirAll(versions, 0700); err != nil {
		return "", err
	}
	if err := directory(versions); err != nil {
		return "", err
	}
	final := filepath.Join(home, filepath.FromSlash(e.Dir))
	if _, err := os.Lstat(final); err == nil {
		if err = verify(final, e, i.keys); err != nil {
			return "", err
		}
		raw, s, err := manifestBytes(final)
		if err != nil || !bytes.Equal(raw, d.raw) || !bytes.Equal(s, d.signature) {
			return "", errors.New("conflicting installed manifest")
		}
		return final, i.check(home, final)
	} else if !errors.Is(err, os.ErrNotExist) {
		return "", err
	}
	stage, err := os.MkdirTemp(versions, ".stage-")
	if err != nil {
		return "", err
	}
	defer os.RemoveAll(stage)
	files, err := d.files(e.Compat)
	if err != nil {
		return "", err
	}
	target := d.Targets[Platform()]
	b, err := i.fetch(target)
	if err != nil {
		return "", err
	}
	if !matches(b, target.File) {
		return "", errors.New("binary size or SHA-256 mismatch")
	}
	if err = write(filepath.Join(stage, Binary()), b, 0700); err != nil {
		return "", err
	}
	if e.Compat {
		if err = os.Mkdir(filepath.Join(stage, "skynet_agent"), 0700); err != nil {
			return "", err
		}
		for name, data := range adapters {
			if err = write(filepath.Join(stage, name), data, 0600); err != nil {
				return "", err
			}
		}
	}
	for name, data := range map[string][]byte{"release.json": d.raw, "release.json.sig": d.signature} {
		if err = write(filepath.Join(stage, name), data, 0600); err != nil {
			return "", err
		}
	}
	if err = checkedTree(stage, files); err != nil {
		return "", err
	}
	if err = i.check(home, stage); err != nil {
		return "", fmt.Errorf("verify-install: %w", err)
	}
	if err = verify(stage, e, i.keys); err != nil {
		return "", err
	}
	if err = os.Rename(stage, final); err != nil {
		return "", err
	}
	return final, syncDir(versions)
}

// install runs under the same update.lock as the Python bridge and local installers.
func (i installer) install(home string, d document, running int, python string) error {
	c, h, err := state(home)
	if err != nil {
		return err
	}
	hash := digest(d.raw)
	if d.Seq < max(running, h.Seq) || contains(h.Bad, d.Seq) {
		return errors.New("release rejected by local sequence history")
	}
	if d.Halt.Message(d.Seq) != "" || d.Halt.Message(max(c.Seq, running)) != "" && max(c.Seq, running) > 0 {
		return errors.New("signed release is paused")
	}
	if d.Seq == h.Seq && hash != h.Digest && !(c.Seq == d.Seq && c.Digest == hash) {
		return errors.New("sequence already used")
	}
	compat := c.Compat
	if c.Seq != 0 && c.Runtime != "go" {
		if c.Seq < d.MinBridge || c.Seq != 6 {
			return errors.New("install the signed Python bridge first")
		}
		if python == "" {
			python = c.Python
		}
		if !filepath.IsAbs(python) {
			return errors.New("bridge interpreter required")
		}
		dir, err := verifiedPath(home, c.Entry, i.keys)
		if err != nil {
			return err
		}
		launcher, err := read(filepath.Join(dir, "launcher.py"), 2<<20)
		if err != nil {
			return err
		}
		if err = write(filepath.Join(home, "launcher.py"), launcher, 0700); err != nil {
			return err
		}
		c.Python = python
		c.Runtime = "python"
		compat = true
	}
	e := Entry{Seq: d.Seq, Version: d.Version, Dir: fmt.Sprintf("versions/%d-%s", d.Seq, d.Version), Runtime: "go", Compat: compat, Digest: hash}
	dir, err := i.prepare(home, d, e)
	if err != nil {
		return err
	}
	// Never replace an active Windows launcher. Its digest is retained across upgrades.
	root := filepath.Join(home, Binary())
	old, err := read(root, maxBinary)
	switch {
	case errors.Is(err, os.ErrNotExist):
		b, err := read(filepath.Join(dir, Binary()), maxBinary)
		if err != nil {
			return err
		}
		if !matches(b, d.Targets[Platform()].File) {
			return errors.New("launcher hash mismatch")
		}
		if err = write(root, b, 0700); err != nil {
			return err
		}
		h.Launcher = digest(b)
	case err != nil:
		return err
	case h.Launcher != "" && h.Launcher == digest(old):
	case matches(old, d.Targets[Platform()].File):
		h.Launcher = digest(old)
	default:
		return errors.New("unrecognized permanent launcher")
	}
	if c.Seq != 0 && i.probe != nil {
		if err := i.probe(home, root); err != nil {
			return fmt.Errorf("launcher preflight: %w", err)
		}
	}
	prev := c.Previous
	if c.Seq != 0 && c.Seq != e.Seq {
		if _, err = verifiedPath(home, c.Entry, i.keys); err != nil {
			return err
		}
		var t trial
		if err = load(filepath.Join(home, "launch-trial.json"), &t); err != nil {
			return err
		}
		if c.Runtime != "go" || prev == nil || t.Seq == c.Seq && t.Confirmed || c.RolledBack != 0 {
			prev = &c.Entry
		}
	}
	h.Seq = d.Seq
	h.Digest = hash
	// The signed fingerprint permits an interrupted activation to retry only these bytes.
	if err = save(home, "release-history.json", h); err != nil {
		return err
	}
	if err = save(home, "current.json", Current{Entry: e, Previous: prev, Activated: time.Now().Unix()}); err != nil {
		return err
	}
	return save(home, "max_seq.json", h.Seq)
}
func verifiedPath(home string, e Entry, keys []string) (string, error) {
	dir, err := e.path(home)
	if err != nil {
		return "", err
	}
	return dir, verify(dir, e, keys)
}
func configuredMode(home string) (string, error) {
	cfg := struct{ Update string }{Update: "auto"}
	if err := load(filepath.Join(home, "config.json"), &cfg); err != nil {
		return "", err
	}
	switch cfg.Update {
	case "auto", "notify", "off":
		return cfg.Update, nil
	}
	return "", errors.New("invalid configured update mode")
}

func InstallBundle(home, dir, python string, automatic bool) error {
	raw, s, err := manifestBytes(dir)
	if err != nil {
		return err
	}
	d, err := parse(raw, s, nil)
	if err != nil {
		return err
	}
	t, ok := d.Targets[Platform()]
	if !ok {
		return errors.New("unsupported platform")
	}
	if err = checkedTree(dir, map[string]File{t.Name: t.File}); err != nil {
		return err
	}
	i := installer{fetch: func(t Target) ([]byte, error) { return read(filepath.Join(dir, t.Name), t.Size) }, check: checkCandidate, probe: checkLauncher}
	return Locked(home, func() error {
		if automatic {
			mode, err := configuredMode(home)
			if err != nil {
				return err
			}
			if mode != "auto" {
				return errors.New("automatic installation is disabled")
			}
		}
		if err := remember(home, d, nil); err != nil {
			return err
		}
		return i.install(home, d, 0, python)
	})
}
