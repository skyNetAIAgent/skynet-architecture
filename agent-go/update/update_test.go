package update

import (
	"crypto/ed25519"
	"encoding/hex"
	"encoding/json"
	"errors"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/sig"
	"os"
	"path/filepath"
	"runtime"
	"syscall"
	"testing"
	"time"
)

type fixture struct {
	home string
	installer
	private ed25519.PrivateKey
	data    []byte
}

func setup(t *testing.T) *fixture {
	f := &fixture{home: t.TempDir(), private: ed25519.NewKeyFromSeed(make([]byte, 32)), data: []byte("test binary")}
	// Windows can report ERROR_DIR_NOT_EMPTY while a deleted child is still closing.
	if runtime.GOOS == "windows" {
		t.Cleanup(func() {
			until := time.Now().Add(2 * time.Second)
			for {
				err := os.RemoveAll(f.home)
				if err == nil {
					return
				}
				if !errors.Is(err, syscall.Errno(145)) || time.Now().After(until) {
					t.Errorf("remove test profile: %v", err)
					return
				}
				time.Sleep(20 * time.Millisecond)
			}
		})
	}
	f.keys = []string{hex.EncodeToString(f.private.Public().(ed25519.PublicKey))}
	f.fetch = func(Target) ([]byte, error) { return f.data, nil }
	f.check = func(home, dir string) error { return nil }
	return f
}
func (f *fixture) doc(t *testing.T, seq int) document {
	t.Helper()
	r := Release{Format: 2, Seq: seq, Version: "1.0.0", MinBridge: 6, Targets: map[string]Target{
		Platform(): {File: File{int64(len(f.data)), digest(f.data)}, Name: Binary(), URL: "https://github.com/project/releases/download/v1/bin"}}}
	raw, err := json.Marshal(r)
	if err != nil {
		t.Fatal(err)
	}
	b := []byte(sig.FormatLine(f.private.Public().(ed25519.PublicKey), ed25519.Sign(f.private, raw)))
	d, err := parse(raw, b, f.keys)
	if err != nil {
		t.Fatal(err)
	}
	return d
}
func (f *fixture) apply(d document) error {
	return Locked(f.home, func() error { return f.install(f.home, d, 0, "") })
}
func TestActivationAndRollback(t *testing.T) {
	f := setup(t)
	seven := f.doc(t, 7)
	if err := f.apply(seven); err != nil {
		t.Fatal(err)
	}
	eight := f.doc(t, 8)
	if err := f.apply(eight); err != nil {
		t.Fatal(err)
	}
	cur, err := CurrentVersion(f.home)
	if err != nil || cur.Seq != 8 || cur.Previous == nil || cur.Previous.Seq != 7 {
		t.Fatal(cur, err)
	}
	for i := 1; i <= 3; i++ {
		changed, err := recordExit(f.home, cur, true, false, f.keys)
		if err != nil || changed != (i == 3) {
			t.Fatal(i, changed, err)
		}
	}
	c, h, err := state(f.home)
	if err != nil || c.Seq != 7 || h.Seq != 8 || !contains(h.Bad, 8) {
		t.Fatal(c, h, err)
	}
	if err = f.apply(eight); err == nil {
		t.Fatal("accepted bad release")
	}
	if err = f.apply(seven); err == nil {
		t.Fatal("accepted downgrade")
	}
}
func TestRejectBeforeSwitch(t *testing.T) {
	for _, problem := range []string{"signature", "hash", "truncated", "extra", "candidate", "preflight", "older"} {
		t.Run(problem, func(t *testing.T) {
			f := setup(t)
			if err := f.apply(f.doc(t, 7)); err != nil {
				t.Fatal(err)
			}
			d := f.doc(t, 8)
			switch problem {
			case "signature":
				if _, err := parse(d.raw, d.signature, nil); err == nil {
					t.Fatal("foreign key")
				}
				return
			case "hash":
				f.data[0] ^= 1
			case "truncated":
				f.data = f.data[:2]
			case "extra":
				dir := filepath.Join(f.home, "versions", "8-1.0.0")
				if err := os.Mkdir(dir, 0700); err != nil {
					t.Fatal(err)
				}
				for n, b := range map[string][]byte{Binary(): f.data, "release.json": d.raw, "release.json.sig": d.signature, "extra": {}} {
					if err := os.WriteFile(filepath.Join(dir, n), b, 0600); err != nil {
						t.Fatal(err)
					}
				}
			case "candidate":
				f.check = func(string, string) error { return errors.New("candidate refused") }
			case "preflight":
				f.probe = func(string, string) error { return errors.New("launcher refused") }
			case "older":
				d = f.doc(t, 6)
			}
			if err := f.apply(d); err == nil {
				t.Fatal("accepted", problem)
			}
			c, h, err := state(f.home)
			if err != nil || c.Seq != 7 || h.Seq != 7 {
				t.Fatal(c, h, err)
			}
		})
	}
}
func TestRedirectAndLock(t *testing.T) {
	for _, url := range []string{"https://github.com.evil.example/a", "https://user@github.com/a", "http://github.com/a", "https://github.com:80/a", "https://example.org/a"} {
		if assetURL(url) {
			t.Fatal(url)
		}
	}
	home := t.TempDir()
	if err := Locked(home, func() error {
		if err := Locked(home, func() error { return nil }); err == nil {
			t.Fatal("parallel transaction")
		}
		return nil
	}); err != nil {
		t.Fatal(err)
	}
}

// An older Python launcher imports the compat adapter without -B: the bytecode it
// leaves in the version folder must not make the signed tree look tampered with.
func TestCompatBytecodeIsRemoved(t *testing.T) {
	dir := t.TempDir()
	files := map[string]File{}
	for name, data := range adapters {
		p := filepath.Join(dir, filepath.FromSlash(name))
		if err := os.MkdirAll(filepath.Dir(p), 0700); err != nil {
			t.Fatal(err)
		}
		if err := os.WriteFile(p, data, 0600); err != nil {
			t.Fatal(err)
		}
		files[name] = File{int64(len(data)), digest(data)}
	}
	cache := filepath.Join(dir, "skynet_agent", "__pycache__")
	if err := os.MkdirAll(cache, 0700); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(filepath.Join(cache, "cli.cpython-312.pyc"), []byte("x"), 0600); err != nil {
		t.Fatal(err)
	}
	if err := checkedTree(dir, files); err != nil {
		t.Fatal(err)
	}
	if _, err := os.Stat(cache); !os.IsNotExist(err) {
		t.Fatal("bytecode folder kept", err)
	}
	// Anything else that is not signed is still refused.
	if err := os.WriteFile(filepath.Join(dir, "skynet_agent", "planted.py"), []byte("x"), 0600); err != nil {
		t.Fatal(err)
	}
	if err := checkedTree(dir, files); err == nil {
		t.Fatal("accepted an unsigned file")
	}
}
