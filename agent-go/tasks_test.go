package agentgo_test

import (
	"testing"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/tasks"
)

func TestSignedIndex(t *testing.T) {
	raw, detached := fixture(t, "index.json"), fixture(t, "index.json.sig")
	list, err := tasks.ParseSigned(raw, detached, nil, 5)
	if err != nil || len(list) != 13 {
		t.Fatal(len(list), err)
	}
	unsupported := 0
	for _, task := range list {
		if task.Fields["kernel"] == "ai-answer" && task.Reason == "unsupported kernel or version" {
			unsupported++
			continue
		}
		if task.Reason != "" {
			t.Fatalf("%s: %s", task.Fields["id"], task.Reason)
		}
	}
	if unsupported != 1 {
		t.Fatal("unsupported task count", unsupported)
	}
	if _, err := tasks.ParseSigned(append(raw, ' '), detached, nil, 5); err == nil {
		t.Fatal("accepted modified signed index")
	}
}

func TestTaskFieldsAndUsability(t *testing.T) {
	base := `{"format":1,"seq":1,"tasks":[{"id":"x","kernel":"selftest","kernel_version":1,"units":1,"params":{}}]}`
	for key, val := range map[string]any{"id": "A", "units": true, "kernel_version": 0, "min_agent_seq": 0,
		"issue":-1, "max_seconds": 9, "title": 2, "priority": 101, "redundancy": 0, "params": nil, "unknown": 1} {
		idx := object(t, base)
		task := idx["tasks"].([]any)[0].(canon.Object)
		task[key] = val
		if _, err := tasks.ValidateIndex(idx, 5); err == nil {
			t.Error("accepted", key, val)
		}
	}
	idx := object(t, base)
	row := idx["tasks"].([]any)[0].(canon.Object)
	idx["tasks"] = []any{row, row}
	if _, err := tasks.ValidateIndex(idx, 5); err == nil {
		t.Fatal("accepted duplicate task id")
	}
	idx["tasks"] = []any{row}
	row["min_agent_seq"] = 6
	list, err := tasks.ValidateIndex(idx, 5)
	if err != nil || list[0].Reason != "needs a newer agent" {
		t.Fatal(list, err)
	}
	row["params"] = canon.Object{"rounds": 0}
	list, err = tasks.ValidateIndex(idx, 6)
	if err != nil || list[0].Reason == "" {
		t.Fatal("invalid kernel params marked usable")
	}
}
