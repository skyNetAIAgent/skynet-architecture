// Command skynet-agent runs the volunteer compute client.
package main

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"os"
	"os/signal"
	"path/filepath"
	"runtime"
	"strings"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/outbox"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/tasks"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/transport"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/worker"
)

type Object = config.Object

// Set by tools/build_go.py with -X main.version and -X main.releaseSeq.
var version, releaseSeq string

var desktopCommands = map[string]func([]string) int{}
var usage = "skynet-agent android-service | verify-apk-manifest | run | status | tasks | pause | resume | stop | outbox | net | config | selftest | version"

func init() {
	registerUpdateCommands(func(name, _ string, run func([]string) int) {
		desktopCommands[name] = run
		usage += " | " + name
	})
}

func android() bool {
	return runtime.GOOS == "android" || os.Getenv("ANDROID_ROOT") != "" || os.Getenv("TERMUX_VERSION") != ""
}
func printJSON(v any, indent string) error {
	b, err := canon.Marshal(v, false)
	if err != nil {
		return err
	}
	var out bytes.Buffer
	if err = json.Indent(&out, b, "", indent); err != nil {
		return err
	}
	fmt.Println(out.String())
	return nil
}

// Accept options on either side of the board action and record prefix.
func parseFlags(f *flag.FlagSet, args []string) ([]string, error) {
	var opts, pos []string
	for i := 0; i < len(args); i++ {
		arg := args[i]
		if arg == "--" {
			pos = append(pos, args[i+1:]...)
			break
		}
		if !strings.HasPrefix(arg, "-") || arg == "-" {
			pos = append(pos, arg)
			continue
		}
		key, _, value := strings.Cut(strings.TrimLeft(arg, "-"), "=")
		fl := f.Lookup(key)
		if fl == nil {
			return nil, fmt.Errorf("unknown option %s", arg)
		}
		opts = append(opts, arg)
		if _, ok := fl.Value.(interface{ IsBoolFlag() bool }); !value && !ok {
			if i+1 >= len(args) {
				return nil, fmt.Errorf("missing value for %s", arg)
			}
			i++
			opts = append(opts, args[i])
		}
	}
	return pos, f.Parse(opts)
}
func changeState(ctx context.Context, home string, fn func(Object) error) (Object, error) {
	// The runner and manual publication share counters and outbox files.
	var lock *os.File
	var err error
	for {
		lock, err = config.Lock(filepath.Join(home, "state.lock"))
		if !errors.Is(err, config.ErrLocked) {
			break
		}
		select {
		case <-ctx.Done():
			return nil, ctx.Err()
		case <-time.After(50 * time.Millisecond):
		}
	}
	if err != nil {
		return nil, err
	}
	defer lock.Close()
	st, err := config.State(home)
	if err == nil {
		err = fn(st)
	}
	if err == nil {
		err = config.Write(filepath.Join(home, "state.json"), st)
	}
	return st, err
}
func setConfig(home, key, value string) error {
	lock, err := config.Lock(filepath.Join(home, "config.lock"))
	if err != nil {
		return err
	}
	defer lock.Close()
	o, err := config.Load(home)
	if err != nil {
		return err
	}
	if err = config.Set(o, key, value); err != nil {
		return err
	}
	return config.Write(filepath.Join(home, "config.json"), o)
}
func configCmd(home string, args []string) error {
	if len(args) == 3 && args[0] == "set" {
		if err := setConfig(home, args[1], args[2]); err != nil {
			return err
		}
		fmt.Printf("Updated %s.\n", args[1])
		return nil
	}
	o, err := config.Load(home)
	if err != nil {
		return err
	}
	if len(args) == 0 || len(args) == 1 && args[0] == "show" {
		return printJSON(o, "  ")
	}
	if len(args) == 2 && args[0] == "get" {
		if v := config.Get(o, args[1]); v != nil {
			return printJSON(v, "")
		}
	}
	return errors.New("usage: config show | get KEY | set KEY VALUE")
}
func status(home string) error {
	cfg, err := config.Load(home)
	if err != nil {
		return err
	}
	s, err := config.State(home)
	if err != nil {
		return err
	}
	entries, err := outbox.Entries(home, "outbox")
	if err != nil {
		return err
	}
	c := config.Obj(s["counters"])
	on, known := worker.Battery()
	power := "unknown"
	if known {
		power = fmt.Sprint(on)
	}
	fmt.Printf("SkyNet research agent %s (release %d)\nHome folder:      %s\nWorkers:          %v   paused: %v   on battery: %s\n", config.Version, config.Sequence, home, cfg["workers"], cfg["paused"], power)
	fmt.Printf("Update mode:      %v   publish: %v (via %s)\nUnits done:       %v   failed: %v   published: %v\nOutbox:           %d result(s) waiting\n", cfg["update"], cfg["submit"], config.Channel(cfg), c["units_done"], c["units_failed"], c["published"], len(entries))
	if config.Channel(cfg) == "github" {
		fmt.Println("GitHub submission is unsupported. Results stay in the outbox.")
	}
	for _, e := range entries {
		if why := outbox.Reason(cfg, e.Data); why != "" {
			fmt.Printf("  %s  %s\n", e.Name, why)
		}
	}
	if t := config.Num(s["last_poll"], 0); t > 0 {
		fmt.Println("Last check:      ", stamp(t), "UTC")
	}
	for _, k := range []string{"halt", "poll_error", "last_error"} {
		if v := config.Str(s[k]); v != "" {
			fmt.Printf("%s: %s\n", k, clean(v))
		}
	}
	for _, k := range []string{"retry_at", "publish_after"} {
		if t := config.Num(s[k], 0); t > time.Now().Unix() {
			fmt.Printf("%s: %s UTC\n", k, stamp(t))
		}
	}
	return nil
}
func listTasks(ctx context.Context, home string, n transport.Network) error {
	s, err := config.State(home)
	if err != nil {
		return err
	}
	floor := config.Num(s["index_seq"], 0)
	idx, err := tasks.Fetch(ctx, n, "", floor)
	if err != nil {
		cached, e := tasks.Cached(home, floor)
		if e != nil {
			return err
		}
		idx = cached
	}
	fmt.Printf("Task list number %v, issued %v, expires %s\n", idx.Doc["seq"], idx.Doc["issued"], defaultText(idx.Doc["expires"], "never"))
	for _, t := range idx.Tasks {
		id := config.Str(t.Fields["id"])
		done, _ := config.Obj(s["done"])[id].([]any)
		why := t.Reason
		if why == "" {
			why = "ready"
			if skip := config.Obj(config.Obj(s["skip"])[id]); skip != nil {
				why = "skipped here: " + config.Str(skip["reason"])
			}
			if idx.Expired(time.Now()) {
				why = "expired"
			}
		}
		fmt.Printf("  %-28s %-14s units %-7d done here %-5d %s\n", id, fmt.Sprintf("%s@%v", t.Fields["kernel"], t.Fields["kernel_version"]), t.Fields["units"], len(done), why)
		if title := config.Str(t.Fields["title"]); title != "" {
			fmt.Println("      " + clean(title))
		}
	}
	return nil
}
func defaultText(v any, d string) string {
	if s, ok := v.(string); ok {
		return s
	}
	return d
}
func queue(ctx context.Context, home string, n transport.Network, args []string) error {
	action := "list"
	if len(args) > 0 {
		action = args[0]
	}
	cfg, err := config.Load(home)
	if err != nil {
		return err
	}
	if action == "send" && len(args) == 1 {
		var count int
		var sendErr error
		_, err = changeState(ctx, home, func(s Object) error { count, sendErr = outbox.Flush(ctx, home, n, cfg, s, true); return nil })
		if err != nil {
			return err
		}
		names, e := outbox.Names(home, "outbox")
		if e != nil {
			return e
		}
		fmt.Printf("Published %d result(s); %d left in the outbox.\n", count, len(names))
		// Python reports the failure and still exits with 0: a missing
		// channel must not look like a usage error.
		if sendErr != nil {
			fmt.Fprintln(os.Stderr, sendErr)
		}
		return nil
	}
	entries, err := outbox.Entries(home, "outbox")
	if err != nil {
		return err
	}
	if action == "list" && len(args) <= 1 {
		if len(entries) == 0 {
			fmt.Println("The outbox is empty.")
		}
		for _, e := range entries {
			r := config.Obj(e.Data["record"])
			fmt.Printf("%s  %s unit %v  %s\n", e.Name, r["task"], r["unit"], outbox.Reason(cfg, e.Data))
		}
		return nil
	}
	if len(args) != 2 {
		return errors.New("usage: outbox list | show NAME | send | drop NAME")
	}
	for _, e := range entries {
		if e.Name != args[1] {
			continue
		}
		switch action {
		case "show":
			r := config.Obj(e.Data["record"])
			b, err := canon.Marshal(r, true)
			if err != nil {
				return err
			}
			fmt.Printf("<!-- skynet-agent-result:1 -->\nSkyNet research agent · 1 result(s) · agent %s\n\n`%s` unit %v of %v\n\n```json\n%s\n```\n", r["agent"], r["task"], r["unit"], r["units"], b)
			if txt, ok := e.Data["text"].(string); ok {
				fmt.Printf("\nMachine-generated answer of a local AI model. Nobody has verified it.\n\n~~~~~~~~text\n%s\n~~~~~~~~\n", clean(txt))
			}
			return nil
		case "drop":
			_, err = changeState(ctx, home, func(st Object) error { return os.Remove(filepath.Join(home, "outbox", e.Name)) })
			if err == nil {
				fmt.Printf("Dropped %s.\n", e.Name)
			}
			return err
		}
	}
	return errors.New("no such action or entry")
}

func execute(ctx context.Context, args []string) (int, error) {
	if len(args) == 0 || args[0] == "--help" {
		fmt.Println(usage)
		return 0, nil
	}
	cmd, args := args[0], args[1:]
	if cmd == "worker" {
		return 0, worker.Work(os.Stdin, os.Stdout)
	}
	if cmd == "android-service" {
		return androidCommand(ctx, args)
	}
	if cmd == "verify-apk-manifest" {
		return verifyAPKCommand(args)
	}
	if run, ok := desktopCommands[cmd]; ok {
		return run(args), nil
	}
	home, err := config.Home()
	if err != nil && cmd != "selftest" && cmd != "version" {
		return 1, err
	}
	err = nil
	n := transport.Default()
	switch cmd {
	case "version":
		fmt.Printf("skynet-agent %s (release %d), %s, %s-%s\n", config.Version, config.Sequence, runtime.Version(), runtime.GOOS, runtime.GOARCH)
	case "run":
		return run(ctx, home, n, args)
	case "status":
		err = status(home)
	case "tasks":
		err = listTasks(ctx, home, n)
	case "config":
		err = configCmd(home, args)
	case "pause", "resume":
		err = setConfig(home, "paused", fmt.Sprint(cmd == "pause"))
		if err == nil {
			if cmd == "pause" {
				fmt.Println("Paused. Running tasks finish; no new ones start. Resume with: skynet-agent resume")
			} else {
				fmt.Println("Resumed.")
			}
		}
	case "stop":
		if err = os.MkdirAll(home, 0700); err == nil {
			err = os.WriteFile(filepath.Join(home, "stop"), []byte("stop\n"), 0600)
		}
		if err == nil {
			fmt.Println("Asked the running agent to stop.")
		}
	case "net":
		err = netCmd(ctx, home, n, args)
	case "outbox":
		err = queue(ctx, home, n, args)
	case "selftest":
		if len(args) > 1 || len(args) == 1 && args[0] != "--online" {
			return 2, errors.New("usage: selftest [--online]")
		}
		err = selftest()
		if err == nil && len(args) == 1 {
			_, _, err = tasks.Release(ctx, n)
			if err == nil {
				var idx *tasks.Index
				idx, err = tasks.Fetch(ctx, n, "", 0)
				if err == nil {
					fmt.Printf("Signed task list: number %v with %d task(s)\n", idx.Doc["seq"], len(idx.Tasks))
				}
			}
		}
		if err == nil {
			fmt.Println("OK")
		}
	default:
		return 2, fmt.Errorf("unknown command: %s", cmd)
	}
	return 0, err
}
func main() {
	if buildMetadataError != nil {
		fmt.Fprintln(os.Stderr, buildMetadataError)
		os.Exit(1)
	}
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
	code, err := execute(ctx, os.Args[1:])
	stop()
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		if code == 0 {
			code = 1
		}
	}
	os.Exit(code)
}
