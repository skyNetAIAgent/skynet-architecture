// Command taskcheck checks a task list with the agent's own rules (for maintainers).
//
//	go run ./cmd/taskcheck ../tasks/index.json
//
// It parses the list strictly, then validates every task as an agent of the newest
// sequence would. A task that such an agent would skip for any reason other than
// being closed is reported, and the command exits with status 1.
package main

import (
	"fmt"
	"os"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/tasks"
)

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: taskcheck <tasks/index.json>")
		os.Exit(2)
	}
	raw, err := os.ReadFile(os.Args[1])
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(2)
	}
	v, err := canon.Parse(raw)
	index, ok := v.(canon.Object)
	if err != nil || !ok {
		fmt.Fprintln(os.Stderr, "task list is not a strict JSON object:", err)
		os.Exit(1)
	}
	rows, err := tasks.ValidateIndex(index, 999999999)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	bad := 0
	for _, t := range rows {
		if t.Reason != "" && t.Reason != "closed" {
			fmt.Printf("PROBLEM %v: %s\n", t.Fields["id"], t.Reason)
			bad++
		}
	}
	fmt.Printf("%d task(s), %d problem(s)\n", len(rows), bad)
	if bad > 0 {
		os.Exit(1)
	}
}
