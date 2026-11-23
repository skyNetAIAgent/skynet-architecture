// Package launch supervises the active runtime selected by current.json.
package launch

import (
	"errors"
	"fmt"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/update"
	"os"
	"os/exec"
	"path/filepath"
	"slices"
	"time"
)

const stub = "import sys; sys.path.insert(0, sys.argv[1]); sys.argv = [sys.argv[0]] + sys.argv[2:]; from skynet_agent.cli import main; sys.exit(main())"

func Run(home string, args []string) (int, error) {
	home, err := filepath.Abs(home)
	if err != nil {
		return 1, err
	}
	if len(args) == 0 {
		args = []string{"run"}
	}
	// The installer holds update.lock during this read-only preflight.
	if args[0] == "--check" {
		c, err := update.CurrentVersion(home)
		if err != nil {
			return 1, err
		}
		if _, err = update.VerifiedPath(home, c.Entry); err != nil {
			return 1, err
		}
		return 0, nil
	}
	if err = update.Recover(home); err != nil {
		return 1, err
	}
	long := args[0] == "run" && !slices.Contains(args, "--once")
	restarts := 0
	for {
		c, err := update.CurrentVersion(home)
		if err != nil {
			return 1, err
		}
		dir, err := update.VerifiedPath(home, c.Entry)
		if err != nil {
			if c.Previous == nil {
				return 1, err
			}
			if _, err = update.RecordExit(home, c, false, true); err != nil {
				return 1, err
			}
			continue
		}
		exe := filepath.Join(dir, update.Binary())
		childArgs := args
		if c.Runtime != "go" {
			exe = c.Python
			if !filepath.IsAbs(exe) {
				return 1, errors.New("missing bridge interpreter")
			}
			childArgs = append([]string{"-IB", "-c", stub, dir}, args...)
		}
		cmd := exec.Command(exe, childArgs...)
		cmd.Env = append(os.Environ(), "SKYNET_AGENT_HOME="+home)
		cmd.Stdin, cmd.Stdout, cmd.Stderr = os.Stdin, os.Stdout, os.Stderr
		start := time.Now()
		err = cmd.Run()
		fast := time.Since(start) < 60*time.Second
		code := 0
		if err != nil {
			code = 1
			var ex *exec.ExitError
			if errors.As(err, &ex) {
				code = ex.ExitCode()
			} else {
				fmt.Fprintln(os.Stderr, err)
			}
		}
		if code == 75 {
			if !long {
				return 0, nil
			}
			if fast {
				restarts++
			} else {
				restarts = 0
			}
			if restarts >= 5 {
				time.Sleep(time.Minute)
			}
			continue
		}
		if !long {
			return code, nil
		}
		restarts = 0
		normal := code == 0 || code == 3 || code == 4
		changed, err := update.RecordExit(home, c, fast && !normal, false)
		if err != nil {
			return 1, err
		}
		if normal {
			return code, nil
		}
		if !changed {
			time.Sleep(10 * time.Second)
		}
	}
}
