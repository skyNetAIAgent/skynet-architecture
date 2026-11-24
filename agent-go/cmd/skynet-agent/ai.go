package main

import (
	"context"
	"errors"
	"fmt"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/ai"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/transport"
)

func aiOptions(cfg Object) ai.Options {
	settings := config.Obj(cfg["ai"])
	return ai.Options{
		Endpoint:       config.Str(settings["endpoint"]),
		Model:          config.Str(settings["model"]),
		AllowRemote:    settings["allow_remote"] == true,
		Timeout:        time.Duration(config.Num(settings["timeout_minutes"], 30)) * time.Minute,
		MaxAnswerChars: int(config.Num(settings["max_answer_chars"], ai.MaxAnswerChars)),
	}
}

func aiCmd(ctx context.Context, home string, n transport.Network, args []string) error {
	cfg, err := config.Load(home)
	if err != nil {
		return err
	}
	opts := aiOptions(cfg)
	if len(args) == 0 {
		server, err := ai.Discover(ctx, opts)
		if err != nil {
			return err
		}
		fmt.Printf("AI server: %s\nModel: %s\nAutomatic board answers: %v\n", clean(server.Endpoint), clean(server.Model), config.Get(cfg, "ai.enabled"))
		return nil
	}
	if len(args) != 2 || args[0] != "answer" || args[1] == "" {
		return errors.New("usage: skynet-agent ai [answer TASK-ID]")
	}
	if _, err := draftBoardAnswers(ctx, home, n, opts, args[1]); err != nil {
		return err
	}
	fmt.Println("Report draft saved. Run skynet-agent outbox list to review it.")
	return nil
}

type boardPollResult struct {
	drafts int
	err    error
}

func (r boardPollResult) log(log logFile) {
	if r.err != nil && !errors.Is(r.err, context.Canceled) {
		log.write("WARNING", "AI board poll: %v", r.err)
	}
	if r.drafts > 0 {
		log.write("INFO", "saved %d board report draft(s) for review", r.drafts)
	}
}
