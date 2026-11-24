//go:build linux

package records

import (
	"errors"
	"os"
	"path/filepath"
	"testing"
)

func TestPublishSeedNeverReplaces(t *testing.T) {
	dir := t.TempDir()
	a, b, key := filepath.Join(dir, "a"), filepath.Join(dir, "b"), filepath.Join(dir, "identity.key")
	os.WriteFile(a, []byte("first"), 0600)
	os.WriteFile(b, []byte("second"), 0600)
	if err := publishSeed(a, key); err != nil {
		t.Fatal(err)
	}
	if err := publishSeed(b, key); !errors.Is(err, os.ErrExist) {
		t.Fatalf("second publish: %v", err)
	}
	if got, _ := os.ReadFile(key); string(got) != "first" {
		t.Fatalf("identity replaced: %q", got)
	}
}
