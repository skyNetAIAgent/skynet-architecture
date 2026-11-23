package records

import (
	"bufio"
	"crypto/rand"
	"encoding/hex"
	"errors"
	"os"
	"path/filepath"
	"strings"
)

func readSeed(path string) ([]byte, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	s := bufio.NewScanner(f)
	if !s.Scan() && s.Err() != nil {
		return nil, s.Err()
	}
	b := hexField(strings.TrimSpace(s.Text()), 32)
	if b == nil {
		return nil, errors.New("damaged identity.key")
	}
	return b, nil
}

// LoadSeed publishes a flushed private file without replacing another writer's key.
func LoadSeed(home string, create bool) ([]byte, error) {
	path := filepath.Join(home, "identity.key")
	seed, err := readSeed(path)
	if !errors.Is(err, os.ErrNotExist) {
		return seed, err
	}
	if !create {
		return nil, nil
	}
	if err := os.MkdirAll(home, 0700); err != nil {
		return nil, err
	}
	seed = make([]byte, 32)
	if _, err := rand.Read(seed); err != nil {
		return nil, err
	}
	f, err := os.CreateTemp(home, "identity-*.tmp")
	if err != nil {
		return nil, err
	}
	defer os.Remove(f.Name())
	_, err = f.WriteString(hex.EncodeToString(seed) + "\n")
	if err == nil {
		err = f.Sync()
	}
	closeErr := f.Close()
	if err != nil {
		return nil, err
	}
	if closeErr != nil {
		return nil, closeErr
	}
	if err := publishSeed(f.Name(), path); err != nil && !errors.Is(err, os.ErrExist) {
		return nil, err
	}
	return readSeed(path)
}
