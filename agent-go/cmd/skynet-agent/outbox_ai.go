package main

import (
	"context"
	"errors"
	"fmt"
	"strings"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/outbox"
)

// Review and submission use the same lock as the worker's outbox flush.
// Read user input before acquiring it, since FILE may be standard input.
func reportQueue(ctx context.Context, home string, args []string) (bool, error) {
	if len(args) < 2 || !outbox.IsReportName(args[1]) {
		return false, nil
	}
	action, name := args[0], args[1]
	var replacement, hash string
	switch action {
	case "show":
		if len(args) != 2 {
			return true, errors.New("usage: outbox show NAME")
		}
		o, sha, err := outbox.ReviewReport(home, name)
		if err != nil {
			return true, err
		}
		fmt.Printf("Report for task %s\nSummary: %s\n\n", o["task"], o["summary"])
		// Quote every line, including lines that resemble the agent's own instructions.
		text := strings.ReplaceAll(config.Str(o["text"]), "\r\n", "\n")
		for _, line := range strings.Split(text, "\n") {
			fmt.Printf("| %s\n", line)
		}
		fmt.Printf("\nText SHA-256: %s\nApprove this text with: skynet-agent outbox approve %s %s\n", sha, name, sha)
		return true, nil
	case "drop":
		if len(args) != 2 {
			return true, fmt.Errorf("usage: outbox %s NAME", action)
		}
	case "approve":
		if len(args) != 3 {
			return true, errors.New("usage: outbox approve NAME SHA256 (copy the hash from outbox show NAME)")
		}
		hash = args[2]
	case "edit":
		if len(args) == 4 && args[2] == "--file" {
			args = []string{action, name, args[3]}
		}
		if len(args) != 3 {
			return true, errors.New("usage: outbox edit NAME FILE")
		}
		text, err := readTextFile(args[2])
		if err != nil {
			return true, err
		}
		replacement = text
	default:
		return false, nil
	}
	_, err := changeState(ctx, home, func(_ Object) error {
		switch action {
		case "approve":
			if err := outbox.ApproveReport(home, name, hash); err != nil {
				return err
			}
			fmt.Printf("Approved %s for publication.\n", name)
			return nil
		case "edit":
			if err := outbox.EditReport(home, name, replacement); err != nil {
				return err
			}
			fmt.Printf("Updated %s. Review the new text with outbox show.\n", name)
			return nil
		default: // drop
			if err := outbox.DropReport(home, name); err != nil {
				return err
			}
			fmt.Printf("Dropped %s.\n", name)
			return nil
		}
	})
	return true, err
}
