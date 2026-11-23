// Command canoncheck compares the canon package against the Python-generated
// corpus: go run ./cmd/canoncheck corpus.jsonl
package main

import (
	"bufio"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"os"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
)

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: canoncheck corpus.jsonl")
		os.Exit(2)
	}
	f, err := os.Open(os.Args[1])
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(2)
	}
	defer f.Close()
	scanner := bufio.NewScanner(f)
	scanner.Buffer(make([]byte, 1<<20), 1<<20)
	ok, rejected, failed := 0, 0, 0
	for scanner.Scan() {
		var row struct {
			Text      string `json:"text"`
			Kind      string `json:"kind"`
			Canonical string `json:"canonical"`
			WireHex   string `json:"wire_hex"`
			Sha256    string `json:"sha256"`
		}
		if err := json.Unmarshal(scanner.Bytes(), &row); err != nil {
			fmt.Fprintln(os.Stderr, "bad corpus row:", err)
			failed++
			continue
		}
		value, err := canon.Parse([]byte(row.Text))
		if row.Kind == "ok" {
			ok++
			if err != nil {
				fmt.Fprintf(os.Stderr, "parse %q: %v\n", row.Text, err)
				failed++
				continue
			}
			ascii, _ := canon.Marshal(value, true)
			wire, _ := canon.Marshal(value, false)
			sum := sha256.Sum256(ascii)
			if string(ascii) != row.Canonical || hex.EncodeToString(wire) != row.WireHex ||
				hex.EncodeToString(sum[:]) != row.Sha256 {
				fmt.Fprintf(os.Stderr, "mismatch %q:\n  got canonical %s\n  want %s\n", row.Text, ascii, row.Canonical)
				failed++
			}
		} else {
			rejected++
			if err == nil {
				fmt.Fprintf(os.Stderr, "accepted %q (kind %s)\n", row.Text, row.Kind)
				failed++
			}
		}
	}
	if err := scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		failed++
	}
	fmt.Printf("corpus: %d ok, %d must-reject, %d failures\n", ok, rejected, failed)
	if failed > 0 || ok < 2000 {
		os.Exit(1)
	}
}
