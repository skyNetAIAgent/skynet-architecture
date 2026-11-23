package main

import (
	"bufio"
	"context"
	"errors"
	"flag"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/outbox"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/tasks"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/transport"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/update"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/worker"
)

// The Java service owns stdin. Losing the service (EOF) also stops its children.
type androidHost struct {
	home string
	wake chan struct{}

	mu       sync.Mutex
	charging bool
	stopUnit context.CancelFunc
}

func (h *androidHost) readControl(in io.Reader, stop context.CancelFunc) {
	defer stop()
	sc := bufio.NewScanner(in)
	for sc.Scan() {
		h.mu.Lock()
		h.charging = sc.Text() == "charging 1"
		h.enforceBatteryLocked()
		h.mu.Unlock()
		select {
		case h.wake <- struct{}{}:
		default:
		}
	}
}

func (h *androidHost) enforceBatteryLocked() {
	if h.stopUnit != nil && !h.charging {
		// Read the current preference for this disconnect, including changes made
		// while the unit was running. An unreadable preference fails closed.
		cfg, err := config.Load(h.home)
		if err != nil || cfg["run_on_battery"] != true {
			h.stopUnit()
		}
	}
}

func (h *androidHost) monitor(ctx context.Context, stop context.CancelFunc) {
	t := time.NewTicker(250 * time.Millisecond)
	defer t.Stop()
	for {
		if _, err := os.Stat(filepath.Join(h.home, "stop")); err == nil {
			stop()
			return
		}
		h.mu.Lock()
		h.enforceBatteryLocked()
		h.mu.Unlock()
		select {
		case <-ctx.Done():
			return
		case <-t.C:
		}
	}
}

func (h *androidHost) isCharging() bool {
	h.mu.Lock()
	defer h.mu.Unlock()
	return h.charging
}

func (h *androidHost) compute(ctx context.Context, task Object, unit tasks.Unit, cfg Object, out io.Writer) (Object, error) {
	h.mu.Lock()
	unitCtx, cancel := context.WithCancel(ctx)
	h.stopUnit = cancel
	h.enforceBatteryLocked()
	h.mu.Unlock()
	defer cancel()

	var outcome Object
	var err error
	if unitCtx.Err() == nil {
		if _, err = fmt.Fprintln(out, "working 1"); err == nil {
			outcome = worker.Run(unitCtx, task, unit.Number, config.Num(cfg["max_task_minutes"], 120))
			_, err = fmt.Fprintln(out, "working 0")
		}
	}
	h.mu.Lock()
	h.stopUnit = nil
	interrupted := unitCtx.Err() != nil
	h.mu.Unlock()
	if interrupted {
		// A power transition or stop is neither a failure nor a completed unit.
		outcome = nil
	}
	return outcome, err
}

func androidCommand(ctx context.Context, args []string) (int, error) {
	flags := flag.NewFlagSet("android-service", flag.ContinueOnError)
	home := flags.String("home", "", "absolute path to the app's agent profile")
	if err := flags.Parse(args); err != nil || flags.NArg() != 0 || !filepath.IsAbs(*home) {
		return 2, errors.New("usage: android-service --home ABSOLUTE_DIRECTORY")
	}
	host := androidHost{home: filepath.Clean(*home), wake: make(chan struct{}, 1)}
	lock, err := config.Lock(filepath.Join(host.home, "agent.lock"))
	if err != nil {
		return 4, err
	}
	defer lock.Close()
	ctx, stop := context.WithCancel(ctx)
	defer stop()
	if _, err := os.Stat(filepath.Join(host.home, "stop")); err == nil {
		stop()
	} else {
		go host.readControl(os.Stdin, stop)
		go host.monitor(ctx, stop)
	}
	return 0, host.loop(ctx, transport.Default(), os.Stdout)
}

func androidStatus(home string, cfg, state Object, note, code, current string) error {
	names, err := outbox.Names(home, "outbox")
	if err != nil {
		return err
	}
	c := config.Obj(state["counters"])
	problem := config.Str(state["last_error"])
	report := Object{
		"time": time.Now().Unix(), "note": note, "code": code, "current": current,
		"version": config.Version, "release": config.Sequence, "downloaded": false,
		"units_done": config.Num(c["units_done"], 0), "units_failed": config.Num(c["units_failed"], 0),
		"published": config.Num(c["published"], 0), "outbox": len(names),
		"retry_at": config.Num(state["retry_at"], 0), "problem_code": "",
	}
	if config.Channel(cfg) == "github" {
		file, err := os.Stat(filepath.Join(home, "github-token"))
		report["login"] = err == nil && file.Mode().IsRegular() && file.Size() > 0
		report["problem_code"] = "github_unsupported"
		problem = "GitHub submission is unsupported; results stay on this device"
	} else if strings.Contains(problem, "GitHub CLI") || strings.Contains(problem, "gh auth login") {
		problem = ""
	}
	if problem == "" {
		problem = config.Str(state["poll_error"])
	}
	report["last_error"] = problem
	return config.Write(filepath.Join(home, "status.json"), report)
}

func (h *androidHost) loop(ctx context.Context, n transport.Network, out io.Writer) (err error) {
	home := h.home
	var state, cfg Object
	defer func() {
		note, code := "stopped", "stopped"
		if errors.Is(err, context.Canceled) && ctx.Err() != nil {
			err = nil
		}
		if err != nil {
			note, code = err.Error(), "error"
		}
		err = errors.Join(err, androidStatus(home, cfg, state, note, code, ""))
	}()
	for _, dir := range []string{"outbox", "sent", "logs", "net"} {
		if err = os.MkdirAll(filepath.Join(home, dir), 0700); err != nil {
			return err
		}
	}
	log := logFile{path: filepath.Join(home, "logs", "agent.log")}
	log.write("INFO", "Android service started, engine %s (release %d)", config.Version, config.Sequence)
	cfg, err = config.Load(home)
	if err != nil {
		return err
	}
	halt, err := update.CachedHalt(home, int(config.Sequence))
	if err != nil {
		return err
	}
	// Recover a watchdog marker left by 0.2.0 or an interrupted state save.
	timeoutPath := filepath.Join(home, "timed_out.json")
	marker, err := config.Read(timeoutPath)
	if err != nil && !errors.Is(err, os.ErrNotExist) {
		return err
	}
	state, err = changeState(ctx, home, func(st Object) error {
		if id := config.Str(marker["task"]); id != "" {
			config.Obj(st["skip"])[id] = Object{"reason": "too slow on this device", "until": time.Now().Add(7 * 24 * time.Hour).Unix()}
		}
		if halt != "" {
			st["halt"], st["halt_seq"] = halt, config.Sequence
		}
		return outbox.Recover(home, st)
	})
	if err != nil {
		return err
	}
	if marker != nil {
		if err = os.Remove(timeoutPath); err != nil {
			return err
		}
	}
	if err = androidStatus(home, cfg, state, "starting", "starting", ""); err != nil {
		return err
	}
	idx, _ := tasks.Cached(home, config.Num(state["index_seq"], 0))
	s := schedule{index: idx, next: time.Unix(config.Num(state["retry_at"], 0), 0)}
	publish := false
	lastCode := ""
	var lastStatus time.Time
	for ctx.Err() == nil {
		cfg, err = config.Load(home)
		if err != nil {
			return err
		}
		due := !time.Now().Before(s.next)
		if due || publish {
			state, err = changeState(ctx, home, func(st Object) error {
				if due {
					// Authenticate the signed halt policy. Only the package installer updates code.
					s.poll(ctx, n, home, cfg, st, "off", log)
				}
				if ctx.Err() == nil && cfg["submit"] == "auto" {
					if _, e := outbox.Flush(ctx, home, n, cfg, st, false); e != nil {
						log.write("WARNING", "publish: %v", e)
					}
				}
				return nil
			})
			if err != nil {
				return err
			}
			publish = false
			if ctx.Err() != nil {
				break
			}
		}
		names, err := outbox.Names(home, "outbox")
		if err != nil {
			return err
		}
		note, code := waitStatus(s.index, cfg, state, len(names), !h.isCharging(), true)
		var task Object
		var unit tasks.Unit
		if code == "" {
			task, unit = tasks.Pick(s.index.Tasks, state, s.coverage, nil)
			if task == nil {
				note, code = "all available tasks are done on this device", "all_done"
			}
		}
		if task == nil {
			if code != lastCode || due || time.Since(lastStatus) >= 30*time.Second {
				if err = androidStatus(home, cfg, state, note, code, ""); err != nil {
					return err
				}
				lastCode, lastStatus = code, time.Now()
			}
			select {
			case <-ctx.Done():
			case <-h.wake:
			case <-time.After(time.Second):
			}
			continue
		}
		current := fmt.Sprintf("%s, %d / %v", unit.ID, unit.Number, task["units"])
		if err = androidStatus(home, cfg, state, "working", "working", current); err != nil {
			return err
		}
		lastCode = "working"
		outcome, err := h.compute(ctx, task, unit, cfg, out)
		if err != nil {
			return err
		}
		if outcome == nil {
			continue
		}
		if outcome["timeout"] == true {
			if err = config.Write(timeoutPath, Object{"task": unit.ID, "unit": unit.Number}); err != nil {
				return err
			}
		}
		state, err = changeState(ctx, home, func(st Object) error {
			return finish(home, completion{task, unit, outcome}, cfg, st, log)
		})
		if err != nil {
			return err
		}
		if outcome["timeout"] == true {
			if err = os.Remove(timeoutPath); err != nil {
				return err
			}
		}
		// Save the queue and counters before attempting a network publication.
		publish = outcome["ok"] == true
	}
	return nil
}
