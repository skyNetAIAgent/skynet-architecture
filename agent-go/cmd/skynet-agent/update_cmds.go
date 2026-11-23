package main

import (
	"context"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strconv"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/autostart"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/kernels"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/launch"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/tasks"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/update"
)

var buildMetadataError = loadBuildMetadata()

func loadBuildMetadata() error {
	if releaseSeq != "" {
		seq, err := strconv.ParseInt(releaseSeq, 10, 32)
		if err != nil || seq < 1 || seq > 999999999 {
			return errors.New("invalid linked release sequence")
		}
		config.Sequence = seq
	}
	if version != "" {
		config.Version = version
	}
	return nil
}

func selftest() error {
	r, err := kernels.Run("selftest", 1, canon.Object{"rounds": 8}, 0, 1)
	if err != nil {
		return err
	}
	fmt.Println("Self-test digest:", r["digest"])
	h, err := canon.Hash(r)
	if err != nil {
		return err
	}
	if r["ok"] != true || h != "7823a03918e86a7046e437fdf001dc40ff05fb1d241a8917baeae4d88b5629fa" {
		return errors.New("self-test failed")
	}
	return nil
}

func desktopCommand(command string, args []string) (int, error) {
	exe, err := os.Executable()
	if err != nil {
		return 1, err
	}
	if command == "verify-install" {
		if len(args) != 0 {
			return 1, errors.New("unexpected verify-install arguments")
		}
		if err = update.VerifyCandidate(filepath.Dir(exe), config.Version, int(config.Sequence)); err != nil {
			return 1, err
		}
		return 0, selftest()
	}
	home, err := config.Home()
	if err != nil {
		return 1, err
	}
	switch command {
	case "launch":
		if os.Getenv("SKYNET_AGENT_HOME") == "" {
			home = filepath.Dir(exe)
		}
		// Retry an interrupted migration without enabling a disabled registration.
		if len(args) == 0 || args[0] == "run" {
			if _, err := autostart.Change(home, "migrate"); err != nil {
				fmt.Fprintln(os.Stderr, "autostart migration:", err)
			}
		}
		return launch.Run(home, args)
	case "install-bundle":
		automatic := len(args) == 4 && args[3] == "--automatic"
		if automatic {
			args = args[:3]
		}
		if len(args) < 2 || len(args) > 3 {
			return 1, errors.New("install-bundle DIRECTORY HOME [BRIDGE-PYTHON]")
		}
		home, err = filepath.Abs(args[1])
		if err != nil {
			return 1, err
		}
		py := ""
		if len(args) == 3 {
			py = args[2]
		}
		if err = update.InstallBundle(home, args[0], py, automatic); err != nil {
			return 1, err
		}
		// Activation is durable. A failed login registration can be retried independently.
		if _, err = autostart.Change(home, "migrate"); err != nil {
			fmt.Fprintln(os.Stderr, "release installed, autostart migration:", err)
		}
	case "uninstall":
		if len(args) < 1 || args[0] != "--yes" || len(args) > 2 || len(args) == 2 && args[1] != "--purge" {
			return 1, errors.New("uninstall --yes [--purge]")
		}
		if err := update.Remove(home, len(args) == 2); err != nil {
			return 1, err
		}
	case "autostart":
		action := "status"
		if len(args) > 1 {
			return 1, errors.New("autostart [enable|disable|status]")
		}
		if len(args) == 1 {
			action = args[0]
		}
		status, err := autostart.Change(home, action)
		if err != nil {
			return 1, err
		}
		fmt.Println(status)
	case "update":
		if len(args) != 0 {
			return 1, errors.New("unexpected update arguments")
		}
		r, err := update.Check(context.Background(), home, tasks.Base(), "manual", int(config.Sequence))
		if err != nil {
			return 1, err
		}
		switch {
		case r.Halt != "":
			fmt.Println(r.Halt)
		case r.Installed:
			fmt.Println("Installed", r.Version)
			return 75, nil
		case r.Note != "":
			fmt.Println(r.Note)
		default:
			fmt.Println("Up to date")
		}
	}
	return 0, nil
}

func registerUpdateCommands(add func(name, help string, run func(args []string) int)) {
	for _, cmd := range []struct{ name, help string }{
		{"launch", "run the selected version"}, {"update", "install a signed release"},
		{"verify-install", "verify the installed tree and selftest"}, {"install-bundle", "install a verified local bundle"},
		{"autostart", "manage login startup"}, {"uninstall", "remove the Linux installation"},
	} {
		add(cmd.name, cmd.help, func(args []string) int {
			code, err := desktopCommand(cmd.name, args)
			if err != nil {
				fmt.Fprintln(os.Stderr, err)
				return 1
			}
			return code
		})
	}
}
