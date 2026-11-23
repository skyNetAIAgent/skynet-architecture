package tasks

import (
	"context"
	"errors"
	"fmt"
	"math/rand/v2"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/sig"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/transport"
)

type Index struct {
	Doc   canon.Object
	Tasks []Task
}

func Base() string {
	s := os.Getenv("SKYNET_AGENT_BASE_URL")
	if s == "" {
		s = "https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main"
	}
	return strings.TrimRight(s, "/")
}
func download(ctx context.Context, n transport.Network, path string, limit int64) ([]byte, []byte, error) {
	raw, err := n.Request(ctx, "GET", Base()+"/"+path, nil, limit)
	if err != nil {
		return nil, nil, err
	}
	lines, err := n.Request(ctx, "GET", Base()+"/"+path+".sig", nil, 16384)
	return raw, lines, err
}
func decode(raw, lines []byte, floor int64) (*Index, error) {
	if len(raw) > 2<<20 {
		return nil, errors.New("oversized index")
	}
	o, err := sig.Document(raw, lines, nil)
	if err != nil {
		return nil, err
	}
	rows, err := ValidateIndex(o, config.Sequence)
	if err != nil {
		return nil, err
	}
	seq, ok := canon.Int64(o["seq"])
	if !ok || seq < floor {
		return nil, errors.New("invalid or older index sequence")
	}
	return &Index{o, rows}, nil
}
func Fetch(ctx context.Context, n transport.Network, home string, floor int64) (*Index, error) {
	raw, lines, err := download(ctx, n, "tasks/index.json", 2<<20)
	if err != nil {
		return nil, err
	}
	idx, err := decode(raw, lines, floor)
	if err != nil {
		return nil, err
	}
	if home != "" {
		err = config.Write(filepath.Join(home, "task-list.json"), canon.Object{"raw": string(raw), "signature": string(lines)})
	}
	return idx, err
}
func Cached(home string, floor int64) (*Index, error) {
	o, err := config.Read(filepath.Join(home, "task-list.json"))
	if err != nil {
		return nil, err
	}
	return decode([]byte(config.Str(o["raw"])), []byte(config.Str(o["signature"])), floor)
}
func (i *Index) Expired(now time.Time) bool {
	s := config.Str(i.Doc["expires"])
	return s != "" && now.UTC().Format("2006-01-02") > s
}
func Coverage(ctx context.Context, n transport.Network) canon.Object {
	b, err := n.Request(ctx, "GET", Base()+"/results/coverage.json", nil, 4<<20)
	if err != nil {
		return nil
	}
	v, _ := canon.Parse(b)
	return config.Obj(v)
}

var releaseVersion = regexp.MustCompile(`^[0-9]{1,4}\.[0-9]{1,4}\.[0-9]{1,4}$`)
var releasePath = regexp.MustCompile(`^[A-Za-z0-9_][A-Za-z0-9_./-]{0,159}$`)
var releaseHash = regexp.MustCompile(`^[0-9a-f]{64}$`)

func validRelease(o canon.Object) bool {
	seq := config.Num(o["seq"], 0)
	files := config.Obj(o["files"])
	if config.Num(o["format"], 0) != 1 || seq < 1 || seq > 999999999 ||
		!releaseVersion.MatchString(config.Str(o["version"])) || len(files) == 0 || len(files) > 200 {
		return false
	}
	if v, exists := o["min_python"]; exists {
		pair, ok := v.([]any)
		if !ok || len(pair) != 2 {
			return false
		}
		for _, part := range pair {
			if n := config.Num(part, -1); n < 0 || n > 99 {
				return false
			}
		}
	}
	for _, required := range []string{"launcher.py", "skynet_agent/cli.py", "skynet_agent/__init__.py"} {
		if files[required] == nil {
			return false
		}
	}
	for path, value := range files {
		if !releasePath.MatchString(path) || strings.Contains(path, "..") || strings.Contains(path, "/./") ||
			strings.Contains(path, "//") || path != "launcher.py" && !(strings.HasPrefix(path, "skynet_agent/") && strings.HasSuffix(path, ".py")) {
			return false
		}
		meta := config.Obj(value)
		size := config.Num(meta["size"], -1)
		if size < 0 || size > 2<<20 || !releaseHash.MatchString(config.Str(meta["sha256"])) {
			return false
		}
	}
	return true
}

func Release(ctx context.Context, n transport.Network) (canon.Object, string, error) {
	b, lines, err := download(ctx, n, "agent/release.json", 256<<10)
	if err != nil {
		return nil, "", err
	}
	o, err := sig.Document(b, lines, nil)
	if err != nil {
		return nil, "", err
	}
	if !validRelease(o) {
		return nil, "", errors.New("invalid release description")
	}
	if o["halt"] != nil {
		h := config.Obj(o["halt"])
		through, ok := canon.Int64(h["through_seq"])
		reason, isText := h["reason"].(string)
		_, hasReason := h["reason"]
		if !ok || hasReason && !isText || len([]rune(reason)) > 500 {
			return nil, "", fmt.Errorf("invalid signed halt")
		}
		if through >= config.Sequence {
			if reason == "" {
				reason = "the maintainers paused this version"
			}
			return o, reason, nil
		}
	}
	return o, "", nil
}

type Unit struct {
	ID     string
	Number int64
}

func Pick(rows []Task, state, coverage canon.Object, busy map[Unit]bool) (canon.Object, Unit) {
	var task canon.Object
	var taken map[int64]bool
	var weight int64
	for _, t := range rows {
		id := config.Str(t.Fields["id"])
		if t.Reason != "" || config.Obj(state["skip"])[id] != nil {
			continue
		}
		units := config.Num(t.Fields["units"], 0)
		used := map[int64]bool{}
		done, _ := config.Obj(state["done"])[id].([]any)
		for _, v := range done {
			if u, ok := canon.Int64(v); ok && u >= 0 && u < units {
				used[u] = true
			}
		}
		for u := range busy {
			if u.ID == id {
				used[u.Number] = true
			}
		}
		if int64(len(used)) >= units {
			continue
		}
		w := config.Num(t.Fields["priority"], 10)
		weight += w
		if rand.Int64N(weight) < w {
			task = t.Fields
			taken = used
		}
	}
	if task == nil {
		return nil, Unit{}
	}
	id := config.Str(task["id"])
	units := config.Num(task["units"], 0)
	cov := config.Obj(coverage[id])
	need := config.Num(task["redundancy"], 2)
	lacking := func(u int64) bool { return config.Num(cov[strconv.FormatInt(u, 10)], 0) < need }
	var fallback int64 = -1
	for i := 0; i < 64; i++ {
		u := rand.Int64N(units)
		if taken[u] {
			continue
		}
		if lacking(u) {
			return task, Unit{id, u}
		}
		fallback = u
	}
	if fallback < 0 {
		var count, missing int64
		for u := int64(0); u < units; u++ {
			if taken[u] {
				continue
			}
			count++
			if lacking(u) {
				missing++
				if rand.Int64N(missing) == 0 {
					fallback = u
				}
			} else if missing == 0 && rand.Int64N(count) == 0 {
				fallback = u
			}
		}
	}
	return task, Unit{id, fallback}
}
