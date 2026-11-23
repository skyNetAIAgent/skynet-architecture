// Package tasks checks the structure, signature and local usability of a task index.
package tasks

import (
	"errors"
	"fmt"
	"math/big"
	"regexp"
	"strings"
	"unicode/utf8"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/kernels"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/sig"
)

var idPattern = regexp.MustCompile("^[a-z0-9][a-z0-9._-]{0,63}$")
// Python validates dates with the ASCII \d class; keep exactly the same set
// of digits instead of \p{Nd}, which would also accept e.g. Arabic-Indic
// digits and diverge from Python.
var datePattern = regexp.MustCompile("^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
var ranges = map[string][2]int64{
	"issue": {0, 1000000000}, "max_seconds": {10, 86400}, "priority": {0, 100},
	"redundancy": {1, 100}, "min_agent_seq": {1, 1000000000},
}

type Task struct {
	Fields canon.Object
	// Empty when the local agent can execute the task.
	Reason string
}

// Python re.match with a terminal $ also permits one final newline.
func matches(pattern *regexp.Regexp, s string) bool {
	return pattern.MatchString(strings.TrimSuffix(s, "\n"))
}

func positive(v any) bool {
	if n, ok := v.(*big.Int); ok {
		return n != nil && n.Sign() > 0
	}
	n, ok := canon.Int64(v)
	return ok && n > 0
}

func validFields(t canon.Object) error {
	for k, v := range t {
		if r, ok := ranges[k]; ok {
			n, ok := canon.Int64(v)
			if !ok || n < r[0] || n > r[1] {
				return fmt.Errorf("invalid %s", k)
			}
			continue
		}
		switch k {
		case "id", "kernel", "kernel_version", "params", "units":
		case "title":
			s, ok := v.(string)
			if !ok || utf8.RuneCountInString(s) > 200 {
				return errors.New("invalid title")
			}
		default:
			return fmt.Errorf("unknown task field %q", k)
		}
	}
	return nil
}

func ValidateIndex(index canon.Object, agentSeq int64) ([]Task, error) {
	format, _ := canon.Int64(index["format"])
	if (format != 1 && index["format"] != true && index["format"] != 1.0) || !positive(index["seq"]) {
		return nil, errors.New("invalid index format or sequence")
	}
	for _, k := range []string{"issued", "expires"} {
		if v := index[k]; v != nil {
			s, ok := v.(string)
			if !ok || !matches(datePattern, s) {
				return nil, fmt.Errorf("invalid %s", k)
			}
		}
	}
	rows, ok := index["tasks"].([]any)
	if !ok || len(rows) > 500 {
		return nil, errors.New("invalid task list")
	}
	out := make([]Task, 0, len(rows))
	seen := map[string]bool{}
	for _, v := range rows {
		t, ok := v.(canon.Object)
		if !ok {
			return nil, errors.New("expected task object")
		}
		id, _ := t["id"].(string)
		kernel, _ := t["kernel"].(string)
		if !matches(idPattern, id) || seen[id] || !matches(idPattern, kernel) {
			return nil, fmt.Errorf("invalid task id or kernel in %q", id)
		}
		seen[id] = true
		if err := validFields(t); err != nil {
			return nil, fmt.Errorf("%s: %w", id, err)
		}
		version, _ := canon.Int64(t["kernel_version"])
		units, _ := canon.Int64(t["units"])
		params, ok := t["params"].(canon.Object)
		if !ok || !positive(t["kernel_version"]) || units < 1 || units > 1000000 {
			return nil, fmt.Errorf("invalid task parameters in %s", id)
		}
		task := Task{Fields: t}
		priority, hasPriority := canon.Int64(t["priority"])
		minSeq, hasMin := canon.Int64(t["min_agent_seq"])
		if !hasMin {
			minSeq = 1
		}
		switch {
		case hasPriority && priority == 0:
			task.Reason = "closed"
		case minSeq > agentSeq:
			task.Reason = "needs a newer agent"
		case !kernels.Supported(kernel, version):
			task.Reason = "unsupported kernel or version"
		default:
			if err := kernels.Validate(kernel, version, params, units); err != nil {
				task.Reason = "rejected: " + err.Error()
			}
		}
		out = append(out, task)
	}
	return out, nil
}

func ParseSigned(raw, detached []byte, keys []string, agentSeq int64) ([]Task, error) {
	if len(raw) > 2 << 20 {
		return nil, errors.New("index too large")
	}
	index, err := sig.Document(raw, detached, keys)
	if err != nil {
		return nil, err
	}
	return ValidateIndex(index, agentSeq)
}
