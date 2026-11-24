package main

import (
	"context"
	"errors"
	"flag"
	"fmt"
	"math/rand/v2"
	"os"
	"path/filepath"
	"sync"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/ai"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/outbox"
	agentstatus "github.com/skyNetAIAgent/skynet-architecture/agent-go/status"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/tasks"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/transport"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/update"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/worker"
)

type logFile struct {
	path    string
	verbose bool
}

func (l logFile) write(level, format string, args ...any) {
	if level == "DEBUG" && !l.verbose {
		return
	}
	line := fmt.Sprintf("%s %s %s\n", time.Now().Format("2006-01-02 15:04:05"), level, fmt.Sprintf(format, args...))
	fmt.Fprint(os.Stderr, line)
	if fi, e := os.Stat(l.path); e == nil && fi.Size()+int64(len(line)) >= 1<<20 {
		for i := 3; i >= 1; i-- {
			from := l.path
			if i > 1 {
				from = fmt.Sprintf("%s.%d", l.path, i-1)
			}
			os.Rename(from, fmt.Sprintf("%s.%d", l.path, i))
		}
	}
	f, e := os.OpenFile(l.path, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0600)
	if e == nil {
		f.WriteString(line)
		f.Close()
	}
}
func watchStop(ctx context.Context, cancel context.CancelFunc, path string) {
	t := time.NewTicker(200 * time.Millisecond)
	defer t.Stop()
	for {
		select {
		case <-ctx.Done():
			return
		case <-t.C:
			if _, e := os.Stat(path); e == nil {
				os.Remove(path)
				cancel()
				return
			}
		}
	}
}

type completion struct {
	task Object
	unit tasks.Unit
	out  Object
}

func expire(state Object, idx *tasks.Index, now int64) {
	ids := map[string]bool{}
	if idx != nil {
		for _, t := range idx.Tasks {
			ids[config.Str(t.Fields["id"])] = true
		}
	}
	for id, v := range config.Obj(state["skip"]) {
		if config.Num(config.Obj(v)["until"], 0) <= now || idx != nil && !ids[id] {
			delete(config.Obj(state["skip"]), id)
		}
	}
}
func finish(home string, c completion, cfg, state Object, log logFile) error {
	id := c.unit.ID
	if c.out["ok"] == true {
		if err := outbox.Save(home, c.task, c.unit.Number, c.out, cfg); err != nil {
			return err
		}
		outbox.Mark(state, id, c.unit.Number)
		log.write("INFO", "finished %s unit %d", id, c.unit.Number)
		return nil
	}
	counts := config.Obj(state["counters"])
	counts["units_failed"] = config.Num(counts["units_failed"], 0) + 1
	why := config.Str(c.out["error"])
	state["last_error"] = id + ": " + why
	delay := int64(0)
	if c.out["timeout"] == true {
		delay = 7 * 86400
		why = "too slow on this device"
	} else {
		fails := config.Obj(state["fails"])
		n := config.Num(fails[id], 0) + 1
		fails[id] = n
		if n >= 3 {
			delay = 86400
		}
	}
	if delay > 0 {
		config.Obj(state["skip"])[id] = Object{"reason": why, "until": time.Now().Unix() + delay}
	}
	log.write("WARNING", "%s unit %d failed: %s", id, c.unit.Number, why)
	return nil
}

type schedule struct {
	index    *tasks.Index
	coverage Object
	next     time.Time
	restart  bool
}

func (s *schedule) poll(ctx context.Context, n transport.Network, home string, cfg, state Object, mode string, log logFile) {
	floor := config.Num(state["index_seq"], 0)
	if s.index != nil {
		floor = max(floor, config.Num(s.index.Doc["seq"], 0))
	}
	release, relErr := update.Check(ctx, home, tasks.Base(), mode, int(config.Sequence))
	if relErr == nil || release.Halt != "" {
		state["halt"], state["halt_seq"] = release.Halt, config.Sequence
		state["halt_through"] = release.HaltThrough
	}
	if release.Installed {
		s.restart = true
		log.write("INFO", "installed release %d (%s); finishing active units", release.Seq, release.Version)
	} else if release.Note != "" {
		log.write("INFO", "release %d (%s): %s", release.Seq, release.Version, release.Note)
	}
	fresh, err := tasks.Fetch(ctx, n, home, floor)
	if err == nil {
		s.index = fresh
	}
	if s.index != nil {
		state["index_seq"] = s.index.Doc["seq"]
	}
	now := time.Now()
	gap := float64(config.Num(cfg["poll_minutes"], 30) * 60)
	pollErr := errors.Join(relErr, err)
	s.coverage = nil
	if pollErr != nil {
		fails := min(20, max(0, config.Num(state["poll_failures"], 0))+1)
		state["poll_failures"] = fails
		state["poll_error"] = pollErr.Error()
		gap = min(gap, float64(int64(15)<<(fails-1))) * (0.8 + rand.Float64()*0.2)
		state["retry_at"] = now.Unix() + int64(gap)
		log.write("WARNING", "repository check: %v", pollErr)
	} else {
		state["poll_failures"], state["poll_error"], state["retry_at"] = 0, "", 0
		gap *= 0.8 + rand.Float64()*0.4
		s.coverage = tasks.Coverage(ctx, n)
	}
	s.next = now.Add(time.Duration(gap * float64(time.Second)))
	state["last_poll"] = now.Unix()
	expire(state, s.index, now.Unix())
	log.write("DEBUG", "next repository check %s", s.next.Format(time.RFC3339))
}
func workWait(cfg, state Object, waiting int, on, known bool) (note, code string) {
	switch {
	case state["halt"] != "" && (config.Num(state["halt_seq"], 0) == config.Sequence || config.Num(state["halt_through"], 0) >= config.Sequence):
		return "paused by the maintainers", "halted"
	case cfg["paused"] == true:
		return "paused (run: skynet-agent resume)", "paused"
	case waiting >= outbox.Limit:
		return "the outbox is full", "outbox_full"
	case cfg["run_on_battery"] != true && (on || !known && android()):
		return "waiting for mains power", "not_charging"
	}
	return "", ""
}
func waitStatus(idx *tasks.Index, cfg, state Object, waiting int, on, known bool) (note, code string) {
	if idx == nil {
		return "no task list yet", "no_tasks"
	}
	if idx.Expired(time.Now()) {
		return "the task list has expired", "expired"
	}
	return workWait(cfg, state, waiting, on, known)
}
func run(ctx context.Context, home string, n transport.Network, args []string) (int, error) {
	f := flag.NewFlagSet("run", flag.ContinueOnError)
	once := f.Bool("once", false, "run one unit")
	noSubmit := f.Bool("no-submit", false, "keep results locally")
	noUpdate := f.Bool("no-update", false, "disable installation; still check signed pauses")
	verbose := f.Bool("verbose", false, "debug logging")
	if err := f.Parse(args); err != nil || f.NArg() > 0 {
		return 2, errors.New("invalid run arguments")
	}
	lock, err := config.Lock(filepath.Join(home, "agent.lock"))
	if err != nil {
		return 4, err
	}
	defer lock.Close()
	for _, dir := range []string{"outbox", "sent", "logs", "versions", "net"} {
		if err = os.MkdirAll(filepath.Join(home, dir), 0700); err != nil {
			return 1, err
		}
	}
	stopPath := filepath.Join(home, "stop")
	if err = os.Remove(stopPath); err != nil && !errors.Is(err, os.ErrNotExist) {
		return 1, err
	}
	ctx, cancel := context.WithCancel(ctx)
	defer agentstatus.Start(ctx, home, n)()
	var wg sync.WaitGroup
	defer func() { cancel(); wg.Wait() }()
	wg.Add(1)
	go func() { defer wg.Done(); watchStop(ctx, cancel, stopPath) }()
	log := logFile{filepath.Join(home, "logs", "agent.log"), *verbose}
	log.write("INFO", "SkyNet research agent %s (release %d), home %s", config.Version, config.Sequence, home)
	// The next poll can be delayed by an offline retry deadline.
	halt, err := update.CachedHalt(home, int(config.Sequence))
	if err != nil {
		return 1, err
	}
	state, err := changeState(ctx, home, func(st Object) error {
		if halt != "" {
			st["halt"], st["halt_seq"] = halt, config.Sequence
		}
		return outbox.Recover(home, st)
	})
	if err != nil {
		return 1, err
	}
	idx, _ := tasks.Cached(home, config.Num(state["index_seq"], 0))
	s := schedule{index: idx, next: time.Unix(config.Num(state["retry_at"], 0), 0)}
	busy := map[tasks.Unit]bool{}
	results := make(chan completion, 256)
	finished := 0
	last := ""
	var powerAt time.Time
	var on, known bool
	var ended *completion
	confirmed := false
	var boardDone <-chan boardPollResult
	var cancelBoard context.CancelFunc
	var boardOpts ai.Options
	var polledBoard, drafted bool
	for ctx.Err() == nil {
		cfg, err := config.Load(home)
		if err != nil {
			return 1, err
		}
		due := !s.restart && !time.Now().Before(s.next)
		completed := ended != nil && ended.out["ok"] == true
		if due || ended != nil {
			state, err = changeState(ctx, home, func(st Object) error {
				if due {
					mode := config.Str(cfg["update"])
					if *noUpdate {
						mode = "off"
					}
					s.poll(ctx, n, home, cfg, st, mode, log)
				}
				if ended != nil {
					if err := finish(home, *ended, cfg, st, log); err != nil {
						return err
					}
				}
				if !*noSubmit && ctx.Err() == nil && cfg["submit"] == "auto" {
					_, e := outbox.Flush(ctx, home, n, cfg, st, *once)
					if e != nil {
						log.write("WARNING", "publish: %v", e)
					}
				}
				return nil
			})
			if err != nil {
				if ctx.Err() != nil {
					break
				}
				return 1, err
			}
			ended = nil
		}
		if ctx.Err() != nil {
			break
		}
		if s.restart && len(busy) == 0 {
			return 75, nil
		}
		names, err := outbox.Names(home, "outbox")
		if err != nil {
			return 1, err
		}
		if time.Since(powerAt) >= time.Minute {
			on, known = worker.Battery()
			powerAt = time.Now()
		}
		// Model inference can take minutes. Keep the worker loop, repository
		// checks and human outbox commands responsive while a board poll runs.
		waiting := len(names) + len(busy)
		_, boardWait := workWait(cfg, state, waiting, on, known)
		enabled := config.Get(cfg, "ai.enabled") == true && !s.restart
		opts := aiOptions(cfg)
		if boardDone != nil && (!enabled || boardWait == "halted" || boardWait == "not_charging" || opts != boardOpts) {
			cancelBoard()
		}
		if due && enabled && boardWait == "" && boardDone == nil && (!*once || !polledBoard) {
			boardCtx, cancel := context.WithCancel(ctx)
			ch := make(chan boardPollResult, 1)
			boardDone, cancelBoard, boardOpts, polledBoard = ch, cancel, opts, true
			wg.Add(1)
			go func() {
				defer wg.Done()
				defer cancel()
				count, err := draftBoardAnswers(boardCtx, home, n, opts, "")
				ch <- boardPollResult{count, err}
			}()
		}
		reason, _ := waitStatus(s.index, cfg, state, len(names)+len(busy), on, known)
		slots := int(config.Num(cfg["workers"], 1))
		if *once {
			slots = 1 - finished
		}
		if s.restart {
			slots = 0
		}
		for reason == "" && len(busy) < slots && len(names)+len(busy) < outbox.Limit {
			task, u := tasks.Pick(s.index.Tasks, state, s.coverage, busy)
			if task == nil {
				reason = "all available tasks are done on this device"
				break
			}
			busy[u] = true
			log.write("INFO", "started %s unit %d of %d", u.ID, u.Number, task["units"])
			minutes := config.Num(cfg["max_task_minutes"], 120)
			wg.Add(1)
			go func() {
				defer wg.Done()
				r := worker.Run(ctx, task, u.Number, minutes)
				results <- completion{task, u, r}
			}()
		}
		if reason != "" && reason != last {
			log.write("INFO", "waiting: %s", reason)
		}
		last = reason
		if !confirmed && (completed || reason != "" && len(busy) == 0) {
			if err := update.Confirm(home, int(config.Sequence)); err != nil {
				log.write("WARNING", "confirm release: %v", err)
			} else {
				confirmed = true
			}
		}
		if *once && boardDone == nil && len(busy) == 0 {
			if finished > 0 || drafted {
				break
			}
			return 3, nil
		}
		select {
		case <-ctx.Done():
		case report := <-boardDone:
			boardDone = nil
			drafted = report.drafts > 0
			report.log(log)
		case c := <-results:
			if ctx.Err() == nil {
				delete(busy, c.unit)
				ended = &c
				finished++
			}
		case <-time.After(time.Second):
		}
	}
	return 0, nil
}
