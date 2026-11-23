package update

import (
	"crypto/sha256"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"io/fs"
	"os"
	"path/filepath"
	"runtime"
	"strings"
)

type Entry struct {
	Seq     int    `json:"seq"`
	Version string `json:"version"`
	Dir     string `json:"dir"`
	Runtime string `json:"runtime,omitempty"`
	Python  string `json:"python,omitempty"`
	Compat  bool   `json:"compat,omitempty"`
	Digest  string `json:"manifest_sha256,omitempty"`
}

func (e Entry) path(home string) (string, error) {
	if e.Seq < 1 || e.Seq > maxSeq || !versionRE.MatchString(e.Version) || e.Dir != fmt.Sprintf("versions/%d-%s", e.Seq, e.Version) {
		return "", errors.New("invalid version pointer")
	}
	if e.Runtime != "" && e.Runtime != "python" && e.Runtime != "go" {
		return "", errors.New("unknown runtime")
	}
	if err := directory(filepath.Join(home, "versions")); err != nil {
		return "", err
	}
	p := filepath.Join(home, filepath.FromSlash(e.Dir))
	return p, directory(p)
}

type Current struct {
	Entry
	Previous   *Entry `json:"previous"`
	Activated  int64  `json:"activated"`
	RolledBack int    `json:"rolled_back_from,omitempty"`
}
type history struct {
	Launcher string `json:"launcher_sha256"`
	Seq      int    `json:"seq"`
	Digest   string `json:"manifest_sha256"`
	Bad      []int  `json:"bad_seqs"`
}

func directory(path string) error {
	s, err := os.Lstat(path)
	if err != nil {
		return err
	}
	if !s.IsDir() || isLink(s) {
		return fmt.Errorf("unexpected directory %s", path)
	}
	return nil
}
func regular(path string) error {
	s, err := os.Lstat(path)
	if err != nil {
		return err
	}
	if !s.Mode().IsRegular() || isLink(s) {
		return fmt.Errorf("unexpected file %s", path)
	}
	return nil
}
func limited(r io.Reader, limit int64) ([]byte, error) {
	b, err := io.ReadAll(io.LimitReader(r, limit+1))
	if int64(len(b)) > limit {
		return nil, errors.New("size limit exceeded")
	}
	return b, err
}
func read(path string, limit int64) ([]byte, error) {
	if err := regular(path); err != nil {
		return nil, err
	}
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	return limited(f, limit)
}
func load(path string, v any) error {
	b, err := read(path, maxManifest)
	if errors.Is(err, os.ErrNotExist) {
		return nil
	}
	if err != nil {
		return err
	}
	if strings.TrimSpace(string(b)) == "null" {
		return fmt.Errorf("invalid state in %s", path)
	}
	return json.Unmarshal(b, v)
}
func CurrentVersion(home string) (Current, error) {
	var c Current
	b, err := read(filepath.Join(home, "current.json"), maxManifest)
	if errors.Is(err, os.ErrNotExist) {
		return c, nil
	}
	if err != nil {
		return c, err
	}
	if err = json.Unmarshal(b, &c); err != nil {
		return c, err
	}
	if c.Seq < 1 || c.Seq > maxSeq || c.Previous != nil && (c.Previous.Seq < 1 || c.Previous.Seq >= c.Seq) {
		return c, errors.New("invalid current release sequence")
	}
	return c, nil
}
func syncDir(path string) error {
	if runtime.GOOS == "windows" {
		return nil
	}
	f, err := os.Open(path)
	if err != nil {
		return err
	}
	defer f.Close()
	return f.Sync()
}
func write(path string, b []byte, mode fs.FileMode) error {
	dir := filepath.Dir(path)
	f, err := os.CreateTemp(dir, ".tmp-")
	if err != nil {
		return err
	}
	defer os.Remove(f.Name())
	if _, err = f.Write(b); err == nil {
		err = f.Chmod(mode)
	}
	if err == nil {
		err = f.Sync()
	}
	closeErr := f.Close()
	if err != nil {
		return err
	}
	if closeErr != nil {
		return closeErr
	}
	if err = os.Rename(f.Name(), path); err != nil {
		return err
	}
	return syncDir(dir)
}
func save(home, name string, v any) error {
	b, err := json.Marshal(v)
	if err != nil {
		return err
	}
	return write(filepath.Join(home, name), append(b, '\n'), 0600)
}
func digest(b []byte) string        { return fmt.Sprintf("%x", sha256.Sum256(b)) }
func matches(b []byte, f File) bool { return int64(len(b)) == f.Size && digest(b) == f.SHA256 }
func state(home string) (Current, history, error) {
	c, err := CurrentVersion(home)
	var h history
	if err != nil {
		return c, h, err
	}
	if err = load(filepath.Join(home, "release-history.json"), &h); err != nil {
		return c, h, err
	}
	var floor int
	if err = load(filepath.Join(home, "max_seq.json"), &floor); err != nil {
		return c, h, err
	}
	if floor < 0 || h.Seq < 0 {
		return c, h, errors.New("invalid sequence floor")
	}
	if c.Previous != nil {
		floor = max(floor, c.Previous.Seq)
	}
	h.Seq = max(h.Seq, floor, c.Seq)
	var bad []int
	if err = load(filepath.Join(home, "bad_seqs.json"), &bad); err != nil {
		return c, h, err
	}
	for _, n := range bad {
		if !contains(h.Bad, n) {
			h.Bad = append(h.Bad, n)
		}
	}
	return c, h, nil
}
func contains(a []int, n int) bool {
	for _, i := range a {
		if i == n {
			return true
		}
	}
	return false
}
func Locked(home string, fn func() error) error {
	if err := os.MkdirAll(home, 0700); err != nil {
		return err
	}
	if err := directory(home); err != nil {
		return err
	}
	path := filepath.Join(home, "update.lock")
	if err := regular(path); err != nil && !errors.Is(err, os.ErrNotExist) {
		return err
	}
	f, err := os.OpenFile(path, os.O_CREATE|os.O_RDWR, 0600)
	if err != nil {
		return err
	}
	defer f.Close()
	if err = lock(f); err != nil {
		return fmt.Errorf("update lock: %w", err)
	}
	return fn()
}
