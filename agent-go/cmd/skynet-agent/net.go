package main

import (
	"context"
	"crypto/ed25519"
	"encoding/hex"
	"errors"
	"flag"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"time"
	"unicode/utf8"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/board"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/records"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/transport"
)

func clean(s string) string {
	return strings.Map(func(r rune) rune {
		if r != '\t' && r != '\n' && (r < 32 || r >= 127 && r < 160 || r >= 0x2028 && r <= 0x202e || r >= 0x2066 && r <= 0x2069) {
			return '\uFFFD'
		}
		return r
	}, s)
}
func short(v any, n int) string {
	r := []rune(strings.Join(strings.Fields(clean(config.Str(v))), " "))
	if len(r) > n {
		return string(r[:n-1]) + "…"
	}
	return string(r)
}
func stamp(t int64) string { return time.Unix(t, 0).UTC().Format("2006-01-02 15:04") }
func taskList(store *transport.Store, tasks map[string]*board.Info, me string, jsonMode bool) error {
	var list []*board.Info
	for _, env := range store.Ordered {
		if info := tasks[board.ID(env)]; info != nil {
			list = append(list, info)
		}
	}
	sort.SliceStable(list, func(i, j int) bool { return board.Created(list[i].Task) > board.Created(list[j].Task) })
	rows := []any{}
	for _, i := range list {
		task := i.Task
		title := board.Payload(task)["title"]
		own := ""
		if board.Author(task) == me {
			own = "  (mine)"
		}
		if !jsonMode {
			fmt.Printf("%s  %-8s  %s  claims %d, reports %d%s  %s\n", board.ID(task)[:12], i.Status(), stamp(board.Created(task))[:10], len(i.Claims), len(i.Reports), own, short(title, 70))
			continue
		}
		rows = append(rows, Object{"id": board.ID(task), "status": i.Status(), "author": board.Author(task), "created": board.Created(task), "title": title, "claims": len(i.Claims), "reports": len(i.Reports), "accepted": i.Accepted})
	}
	if jsonMode {
		return printJSON(rows, " ")
	}
	if len(list) == 0 {
		fmt.Println("No tasks on the board yet.")
	}
	return nil
}
func show(env Object, i *board.Info, me string, jsonMode bool) error {
	if jsonMode {
		row := Object{"record": env}
		if i != nil {
			v := Object{}
			for k, e := range i.Verdicts {
				v[k] = e
			}
			row["status"], row["claims"], row["reports"], row["verdicts"], row["accepted"] = i.Status(), i.Claims, i.Reports, v, i.Accepted
		}
		return printJSON(row, " ")
	}
	p := board.Payload(env)
	own := ""
	if board.Author(env) == me {
		own = "  (this device)"
	}
	fmt.Printf("%s %s\nauthor  %s%s\ncreated %s UTC\n", board.Kind(env), board.ID(env), board.Author(env), own, stamp(board.Created(env)))
	switch board.Kind(env) {
	case "task":
		fmt.Printf("status  %s\ntitle   %s\n\n%s\n\nAccepted when: %s\n", i.Status(), short(p["title"], 200), clean(config.Str(p["text"])), clean(config.Str(p["accept"])))
		for _, c := range i.Claims {
			fmt.Printf("claim   by %s until %s UTC\n", board.Author(c)[:12], stamp(config.Num(board.Payload(c)["until"], 0)))
		}
		for _, r := range i.Reports {
			v := board.Kind(i.Verdicts[board.ID(r)])
			if v == "" {
				v = "not judged"
			}
			fmt.Printf("report  %s by %s: %s  [%s]\n", board.ID(r)[:12], board.Author(r)[:12], short(board.Payload(r)["summary"], 60), v)
		}
	case "report":
		fmt.Printf("task    %s\nsummary %s\n\n%s\n", p["task"], clean(config.Str(p["summary"])), clean(config.Str(p["text"])))
	default:
		return printJSON(p, " ")
	}
	return nil
}
func readText(name string) (string, error) {
	var r io.Reader = os.Stdin
	if name != "-" {
		f, err := os.Open(name)
		if err != nil {
			return "", err
		}
		defer f.Close()
		r = f
	}
	b, err := io.ReadAll(io.LimitReader(r, 120004))
	if err != nil {
		return "", err
	}
	if !utf8.Valid(b) || len(b) >= 120004 {
		return "", errors.New("invalid or oversized UTF-8 text")
	}
	return strings.TrimSpace(strings.TrimPrefix(string(b), "\uFEFF")), nil
}
func netCmd(ctx context.Context, home string, n transport.Network, args []string) error {
	f := flag.NewFlagSet("net", flag.ContinueOnError)
	jsonMode := f.Bool("json", false, "JSON output")
	offline := f.Bool("offline", false, "use local records")
	opts := map[string]*string{}
	for _, k := range []string{"title", "file", "accept", "summary", "note", "parent", "base", "revises"} {
		opts[k] = f.String(k, "", k)
	}
	var deputies []string
	f.Func("deputy", "deputy key", func(v string) error { deputies = append(deputies, strings.ToLower(v)); return nil })
	hours := f.Int64("hours", 24, "claim hours")
	days := f.Int64("handover-days", 14, "days until handover")
	pos, err := parseFlags(f, args)
	if err != nil {
		return err
	}
	action, ref := "tasks", ""
	if len(pos) > 0 {
		action = pos[0]
	}
	if len(pos) > 1 {
		ref = pos[1]
	}
	if len(pos) > 2 {
		return errors.New("too many net arguments")
	}
	seed, err := records.LoadSeed(home, true)
	if err != nil {
		return err
	}
	me := hex.EncodeToString(ed25519.NewKeyFromSeed(seed).Public().(ed25519.PublicKey))
	if action == "id" {
		fmt.Printf("This device's public key (its name on the board):\n  %s\nThe secret key is in %s. Whoever copies that file can sign as this device.\n", me, filepath.Join(home, "identity.key"))
		return nil
	}
	s, err := transport.Open(home)
	if err != nil {
		return err
	}
	defer s.Close()
	if action == "sync" {
		sent, err := n.Retry(ctx, s, seed)
		if err != nil {
			return err
		}
		count, err := n.Sync(ctx, s)
		fmt.Printf("%d new record(s), %d waiting record(s) delivered, %d record(s) in the local copy.\n", count, sent, len(s.Items))
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
		}
		return nil
	}
	if !*offline {
		_, err = n.Sync(ctx, s)
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
		}
	}
	now := time.Now().Unix()
	tasks := board.Build(s.Ordered, now)
	if action == "tasks" {
		return taskList(s, tasks, me, *jsonMode)
	}
	if action == "show" {
		e, err := board.Find(s.Ordered, ref, "")
		if err != nil {
			return err
		}
		return show(e, tasks[board.ID(e)], me, *jsonMode)
	}
	get := func(k string) string { return strings.TrimSpace(*opts[k]) }
	p := Object{}
	kind := action
	switch action {
	case "post-task", "report":
		txt, err := readText(*opts["file"])
		if err != nil {
			return err
		}
		p["text"] = txt
		if action == "post-task" {
			kind = "task"
			p["title"], p["accept"], p["handover_days"] = get("title"), get("accept"), *days
			if len(deputies) > 0 {
				p["deputies"] = deputies
			}
			if get("base") != "" {
				p["base"] = get("base")
			}
			if get("parent") != "" {
				e, err := board.Find(s.Ordered, get("parent"), "task")
				if err != nil {
					return err
				}
				p["parent"] = board.ID(e)
			}
		} else {
			e, err := board.Find(s.Ordered, ref, "task")
			if err != nil {
				return err
			}
			p["task"], p["summary"] = board.ID(e), get("summary")
			if get("revises") != "" {
				r, err := board.Find(s.Ordered, get("revises"), "report")
				if err != nil {
					return err
				}
				p["revises"] = board.ID(r)
			}
		}
	case "claim":
		e, err := board.Find(s.Ordered, ref, "task")
		if err != nil {
			return err
		}
		p["task"], p["until"] = board.ID(e), now+*hours*3600
	case "accept", "revise":
		r, err := board.Find(s.Ordered, ref, "report")
		if err != nil {
			return err
		}
		id := config.Str(board.Payload(r)["task"])
		t := tasks[id]
		if t == nil {
			return errors.New("the task of this report is not in the local copy (run: skynet-agent net sync)")
		}
		if board.Rank(t.Task, me, now, now) == 0 {
			return errors.New("only the task author or a deputy after handover may judge this report")
		}
		p["task"], p["report"] = id, board.ID(r)
		if get("note") != "" {
			p["note"] = get("note")
		} else if action == "revise" {
			return errors.New("revise needs --note with the remarks")
		}
	default:
		return fmt.Errorf("unknown net action: %s", action)
	}
	env, ok, msg, err := n.Publish(ctx, s, seed, kind, p)
	if err != nil {
		return err
	}
	answer := "yes"
	if !ok {
		answer = "NOT YET, will be retried by: skynet-agent net sync"
	}
	fmt.Printf("%s %s\n  delivered: %s (%s)\n", kind, board.ID(env), answer, msg)
	return nil
}
