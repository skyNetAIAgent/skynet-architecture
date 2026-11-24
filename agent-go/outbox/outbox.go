// Package outbox keeps Python-compatible results and retries their original signed bytes.
package outbox

import (
	"context"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"runtime"
	"sort"
	"strings"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/records"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/transport"
)

const Limit = 300

type Object = canon.Object
type Entry struct {
	Name string
	Data Object
}

func Names(home, dir string) ([]string, error) {
	rows, err := os.ReadDir(filepath.Join(home, dir))
	if errors.Is(err, os.ErrNotExist) {
		return nil, nil
	}
	var names []string
	for _, d := range rows {
		if d.Type().IsRegular() && strings.HasSuffix(d.Name(), ".json") {
			names = append(names, d.Name())
		}
	}
	return names, err
}
func Entries(home, dir string) ([]Entry, error) {
	names, err := Names(home, dir)
	if err != nil {
		return nil, err
	}
	var out []Entry
	for _, name := range names {
		o, e := config.Read(filepath.Join(home, dir, name))
		if e == nil && (config.Obj(o["record"]) != nil || o["kind"] == "report") {
			out = append(out, Entry{name, o})
		}
	}
	return out, nil
}
func Reason(cfg, o Object) string {
	if config.Channel(cfg) == "github" || o["submit_via"] == "github" {
		return "GitHub submission is unsupported"
	}
	if o["kind"] == "report" {
		if !reportApproved(o) {
			return "report waiting for approval of this text"
		}
		return ""
	}
	rec := config.Obj(o["record"])
	res := config.Obj(rec["result"])
	if o["kind"] == "ai" || o["text"] != nil || strings.HasPrefix(config.Str(rec["kernel"]), "ai-answer@") || res["output_sha256"] != nil {
		return "AI answers are unsupported"
	}
	return ""
}

func Save(home string, task Object, unit int64, outcome, cfg Object) error {
	result := config.Obj(outcome["result"])
	if result == nil {
		return errors.New("worker result is not an object")
	}
	hash, err := canon.Hash(result)
	if err != nil {
		return err
	}
	r := Object{"v": 1, "task": task["id"], "unit": unit, "units": task["units"], "kernel": fmt.Sprintf("%s@%d", task["kernel"], task["kernel_version"]),
		"agent": config.Version, "seq": config.Sequence, "elapsed_s": outcome["elapsed_s"], "result": result, "result_sha256": hash}
	if cfg["report_platform"] == true {
		r["platform"] = runtime.GOOS + "-" + runtime.GOARCH + "-" + runtime.Version()
	}
	now := time.Now()
	entry := Object{"record": r, "text": nil, "issue": config.Num(task["issue"], 0), "kind": "compute", "created": now.Unix(), "approved": true}
	if config.Channel(cfg) == "github" {
		entry["submit_via"] = "github"
	}
	name := fmt.Sprintf("%d-%s-%d.json", now.UnixMilli(), r["task"], unit)
	return config.Write(filepath.Join(home, "outbox", name), entry)
}

// Mark also repairs a crash between persisting the outbox entry and the progress file.
func Mark(state Object, id string, unit int64) {
	done := config.Obj(state["done"])
	units, _ := done[id].([]any)
	for _, v := range units {
		if config.Num(v, -1) == unit {
			return
		}
	}
	done[id] = append(units, unit)
	c := config.Obj(state["counters"])
	c["units_done"] = config.Num(c["units_done"], 0) + 1
	delete(config.Obj(state["fails"]), id)
}
func Recover(home string, state Object) error {
	for _, dir := range []string{"sent", "outbox"} {
		entries, err := Entries(home, dir)
		if err != nil {
			return err
		}
		for _, e := range entries {
			r := config.Obj(e.Data["record"])
			id := config.Str(r["task"])
			u := config.Num(r["unit"], -1)
			if id != "" && u >= 0 {
				Mark(state, id, u)
			}
		}
	}
	return nil
}
func archive(home string, e Entry, id string) error {
	e.Data["published"] = "record:" + id
	e.Data["published_at"] = time.Now().Unix()
	if err := config.Write(filepath.Join(home, "sent", e.Name), e.Data); err != nil {
		return err
	}
	if err := os.Remove(filepath.Join(home, "outbox", e.Name)); err != nil {
		return err
	}
	names, err := Names(home, "sent")
	if err != nil || len(names) <= Limit {
		return err
	}
	// Compute files have timestamp names and board reports have stable task-id
	// names. Prune by archive time and keep this newly committed entry even
	// if the filesystem clock has coarse resolution.
	type archivedFile struct {
		name string
		at   time.Time
	}
	var history []archivedFile
	for _, name := range names {
		if name == e.Name {
			continue
		}
		fi, err := os.Stat(filepath.Join(home, "sent", name))
		if err != nil {
			return err
		}
		history = append(history, archivedFile{name, fi.ModTime()})
	}
	sort.SliceStable(history, func(i, j int) bool { return history[i].at.Before(history[j].at) })
	for _, old := range history[:len(names)-Limit] {
		if err = os.Remove(filepath.Join(home, "sent", old.name)); err != nil {
			return err
		}
	}
	return nil
}
func Flush(ctx context.Context, home string, n transport.Network, cfg, state Object, force bool) (int, error) {
	if config.Channel(cfg) == "github" || (!force && (cfg["submit"] != "auto" || time.Now().Unix() < config.Num(state["publish_after"], 0))) {
		return 0, nil
	}
	entries, err := Entries(home, "outbox")
	if err != nil {
		return 0, err
	}
	var ready []Entry
	for _, e := range entries {
		if e.Data["kind"] == "report" {
			if e.Name != reportName(config.Str(e.Data["task"])) {
				continue
			}
			_, err := os.Stat(dismissedPath(home, e.Name))
			if err == nil {
				continue
			}
			if !errors.Is(err, os.ErrNotExist) {
				return 0, err
			}
		}
		if Reason(cfg, e.Data) == "" {
			ready = append(ready, e)
			if len(ready) == 50 {
				break
			}
		}
	}
	if len(ready) == 0 {
		return 0, nil
	}
	s, err := transport.Open(home)
	if err != nil {
		return 0, err
	}
	defer s.Close()
	seed, err := records.LoadSeed(home, true)
	if err != nil {
		return 0, err
	}
	count := 0
	for _, e := range ready {
		env := config.Obj(e.Data["net_record"])
		if e.Data["kind"] != "report" && e.Data["net_record"] == nil {
			env, err = records.Make(seed, "result", Object{"record": e.Data["record"]}, time.Now().Unix())
			if err != nil {
				return count, err
			}
			e.Data["net_record"] = env
			if err = config.Write(filepath.Join(home, "outbox", e.Name), e.Data); err != nil {
				return count, err
			}
		}
		if err = records.Verify(env, time.Now().Unix()); errors.Is(err, records.ErrFuture) {
			continue
		} else if err != nil {
			return count, err
		}
		if e.Data["kind"] == "report" {
			if err = prepareReport(home, e, seed); err != nil {
				return count, err
			}
		} else {
			body := config.Obj(env["body"])
			payload := config.Obj(body["payload"])
			inner := config.Obj(payload["record"])
			if body["type"] != "result" || inner == nil {
				return count, errors.New("invalid outbox net_record")
			}
			if Reason(cfg, Object{"record": inner, "text": payload["text"]}) != "" {
				continue
			}
			a, _ := canon.Hash(inner)
			b, _ := canon.Hash(e.Data["record"])
			if a != b {
				return count, errors.New("net_record does not match queued result")
			}
		}
		if _, err = s.Add(env); err != nil {
			return count, err
		}
		ok, summary := n.Send(ctx, env, seed)
		if !ok {
			fails := min(int64(10), max(0, config.Num(state["publish_fails"], 0))+1)
			state["publish_fails"] = fails
			state["publish_after"] = time.Now().Unix() + min(int64(3600), 60<<(fails-1))
			err = fmt.Errorf("no channel took the result (%s)", summary)
			state["last_error"] = err.Error()
			return count, err
		}
		if err = archive(home, e, config.Str(env["id"])); err != nil {
			return count, err
		}
		count++
		state["publish_fails"] = 0
		state["publish_after"] = 0
		c := config.Obj(state["counters"])
		c["published"] = config.Num(c["published"], 0) + 1
	}
	return count, nil
}
