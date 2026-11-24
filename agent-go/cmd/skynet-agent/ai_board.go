package main

import (
	"context"
	"crypto/ed25519"
	"encoding/hex"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/ai"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/board"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/outbox"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/records"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/transport"
)

// The journal is append-only. Keep a verified snapshot while waiting for a
// model, without holding the store lock over an inference request.
type aiBoard struct {
	home, journal, author string
	file                  os.FileInfo
	tasks                 map[string]*board.Info
	candidates            []string // task IDs from the original poll
}

func (b *aiBoard) snapshot(s *transport.Store) error {
	file, err := os.Stat(b.journal)
	if err != nil {
		return err
	}
	b.file, b.tasks = file, board.Build(s.Ordered, time.Now().Unix())
	return nil
}

func (b *aiBoard) refresh() error {
	file, err := os.Stat(b.journal)
	if err != nil {
		return err
	}
	if os.SameFile(file, b.file) && file.Size() == b.file.Size() && file.ModTime().Equal(b.file.ModTime()) {
		return nil
	}
	s, err := transport.Open(b.home)
	if err != nil {
		return err
	}
	defer s.Close()
	return b.snapshot(s)
}

func (b *aiBoard) ineligible(id string) (string, error) {
	i := b.tasks[id]
	if i == nil {
		return "task no longer on the board", nil
	}
	if len(i.Accepted) != 0 {
		return "the task already has an accepted report", nil
	}
	for _, report := range i.Reports {
		if board.Author(report) == b.author {
			return "this device has already reported on the task", nil
		}
	}
	seen, err := outbox.ReportSeen(b.home, id)
	if seen {
		return "this task already has a draft or was dismissed", nil
	}
	return "", err
}

// Recheck eligibility after acquiring the lock: a publication or sync may
// have recorded an acceptance or this device's own report during inference.
func (b *aiBoard) save(ctx context.Context, id, answer string, manual bool) (bool, error) {
	saved := false
	_, err := changeState(ctx, b.home, func(Object) error {
		if err := ctx.Err(); err != nil {
			return err
		}
		if err := b.refresh(); err != nil {
			return err
		}
		reason, err := b.ineligible(id)
		if err != nil {
			return err
		}
		if reason != "" {
			if manual {
				return errors.New(reason)
			}
			return nil
		}
		_, err = outbox.SaveReportDraft(b.home, id, answer)
		saved = err == nil
		return err
	})
	return saved, err
}

func readAIBoard(ctx context.Context, home string, n transport.Network, ref string) (*aiBoard, error) {
	s, err := transport.Open(home)
	if err != nil {
		return nil, err
	}
	defer s.Close()
	if _, err := n.Sync(ctx, s); err != nil {
		if ctx.Err() != nil {
			return nil, ctx.Err()
		}
		fmt.Fprintf(os.Stderr, "Board sync: %v (using available local records)\n", err)
	}
	entries := s.Ordered
	if ref != "" {
		task, err := board.Find(entries, ref, "task")
		if err != nil {
			return nil, err
		}
		entries = []Object{task}
	}
	seed, err := records.LoadSeed(home, true)
	if err != nil {
		return nil, err
	}
	b := &aiBoard{home: home, journal: filepath.Join(s.Dir, "records.jsonl"),
		author: hex.EncodeToString(ed25519.NewKeyFromSeed(seed).Public().(ed25519.PublicKey))}
	if err := b.snapshot(s); err != nil {
		return nil, err
	}
	onBoard := map[string]bool{}
	for id := range b.tasks {
		onBoard[id] = true
	}
	if err := outbox.PruneDismissed(home, onBoard); err != nil {
		return nil, err
	}
	for _, entry := range entries {
		if board.Kind(entry) == "task" {
			b.candidates = append(b.candidates, board.ID(entry))
		}
	}
	return b, nil
}

type boardModel interface {
	Answer(context.Context, string, string, string) (string, error)
}

func draftBoardAnswers(ctx context.Context, home string, n transport.Network, opts ai.Options, ref string) (int, error) {
	return generateBoardDrafts(ctx, home, n, opts, ref, func() (boardModel, error) { return ai.Discover(ctx, opts) })
}

func generateBoardDrafts(ctx context.Context, home string, n transport.Network, opts ai.Options, ref string, discover func() (boardModel, error)) (int, error) {
	// A manual answer can race the daemon. Exclude a second generator without
	// holding the state lock used by human review and publication.
	lock, err := config.Lock(filepath.Join(home, "net", "ai-generation.lock"))
	if err != nil {
		if ref == "" && errors.Is(err, config.ErrLocked) {
			return 0, nil
		}
		return 0, err
	}
	defer lock.Close()
	b, err := readAIBoard(ctx, home, n, ref)
	if err != nil {
		return 0, err
	}
	names, err := outbox.Names(home, "outbox")
	if err != nil {
		return 0, err
	}
	var model boardModel
	var firstFailure error
	failures, count := 0, 0
	for _, id := range b.candidates {
		if err := ctx.Err(); err != nil {
			return count, err
		}
		reason, err := b.ineligible(id)
		if err != nil {
			return count, err
		}
		if reason != "" {
			if ref != "" {
				return count, errors.New(reason)
			}
			continue
		}
		if len(names)+count >= outbox.Limit {
			if ref != "" {
				return count, errors.New("the outbox is full")
			}
			break
		}
		if ref == "" {
			cfg, err := config.Load(home)
			if err != nil {
				return count, err
			}
			if config.Get(cfg, "ai.enabled") != true || cfg["paused"] == true || aiOptions(cfg) != opts {
				break
			}
		}
		if model == nil {
			model, err = discover()
			if err != nil {
				return count, err
			}
		}
		p := board.Payload(b.tasks[id].Task)
		answer, err := model.Answer(ctx, config.Str(p["title"]), config.Str(p["text"]), config.Str(p["accept"]))
		if err != nil {
			if ctx.Err() != nil {
				return count, ctx.Err()
			}
			if firstFailure == nil {
				firstFailure = fmt.Errorf("task %.12s: %w", id, err)
			}
			failures++
			continue
		}
		saved, err := b.save(ctx, id, answer, ref != "")
		if err != nil {
			return count, err
		}
		if saved {
			count++
		}
	}
	if failures > 1 {
		return count, fmt.Errorf("%d tasks failed, first error: %w", failures, firstFailure)
	}
	return count, firstFailure
}
