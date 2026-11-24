package main

import (
	"context"
	"crypto/sha256"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/outbox"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/transport"
)

func TestOutboxReviewCommands(t *testing.T) {
	home := t.TempDir()
	name, err := outbox.SaveReportDraft(home, strings.Repeat("c", 64), "first")
	if err != nil {
		t.Fatal(err)
	}
	command := func(args ...string) error { return queue(context.Background(), home, transport.Network{}, args) }
	content := "  human revision\r\n"
	file := filepath.Join(home, "revision.txt")
	if err := os.WriteFile(file, []byte(content), 0600); err != nil {
		t.Fatal(err)
	}
	if err := command("edit", name, file); err != nil {
		t.Fatal(err)
	}
	if err := command("show", name); err != nil {
		t.Fatal(err)
	}
	if err := command("approve", name); err == nil {
		t.Fatal("approved without the reviewed digest")
	}
	if err := command("approve", name, fmt.Sprintf("%x", sha256.Sum256([]byte(content)))); err != nil {
		t.Fatalf("could not approve the exact bytes of the edited file: %v", err)
	}
	if err := command("drop", name); err != nil {
		t.Fatal(err)
	}
	if err := command("show", name); err == nil {
		t.Fatal("dropped report still in outbox")
	}
}
