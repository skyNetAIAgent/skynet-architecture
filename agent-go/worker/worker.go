// Package worker runs one built-in kernel per child process.
package worker

import (
	"context"
	"errors"
	"io"
	"os"
	"runtime"
	"strconv"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/kernels"
)

func Work(in io.Reader, out io.Writer) error {
	runtime.GOMAXPROCS(1)
	// Linux nice values apply to the calling thread.
	runtime.LockOSThread()
	defer runtime.UnlockOSThread()
	lowPriority()
	start := time.Now()
	raw, err := io.ReadAll(io.LimitReader(in, (2<<20)+1))
	var v any
	if err == nil && len(raw) > 2<<20 {
		err = errors.New("oversized job")
	}
	if err == nil {
		v, err = canon.Parse(raw)
	}
	job := config.Obj(v)
	var result canon.Object
	if err == nil {
		result, err = kernels.Run(config.Str(job["kernel"]), config.Num(job["kernel_version"], -1), config.Obj(job["params"]), config.Num(job["unit"], -1), config.Num(job["units"], 0))
	}
	// Round the original binary float to three decimal places, as Python round(x, 3).
	elapsed, _ := strconv.ParseFloat(strconv.FormatFloat(time.Since(start).Seconds(), 'f', 3, 64), 64)
	resp := canon.Object{"ok": err == nil, "elapsed_s": elapsed}
	if err != nil {
		resp["error"] = err.Error()
	} else {
		resp["result"] = result
	}
	b, err := canon.Marshal(resp, true)
	if err != nil {
		return err
	}
	_, err = out.Write(append(b, '\n'))
	return err
}
func Run(ctx context.Context, task canon.Object, unit, minutes int64) canon.Object {
	limit := min(config.Num(task["max_seconds"], 3600), minutes*60)
	ctx, cancel := context.WithTimeout(ctx, time.Second*time.Duration(limit))
	defer cancel()
	job := canon.Object{"kernel": task["kernel"], "kernel_version": task["kernel_version"], "unit": unit, "units": task["units"], "params": task["params"]}
	input, err := canon.Marshal(job, false)
	var b []byte
	if err == nil {
		var exe string
		exe, err = os.Executable()
		if err == nil {
			b, err = child(ctx, exe, input)
		}
	}
	if errors.Is(ctx.Err(), context.DeadlineExceeded) {
		return canon.Object{"ok": false, "error": "timeout", "timeout": true}
	}
	if err == nil {
		var v any
		v, err = canon.Parse(b)
		if obj := config.Obj(v); obj != nil {
			if _, ok := obj["ok"].(bool); ok {
				return obj
			}
		}
		if err == nil {
			err = errors.New("invalid worker response")
		}
	}
	return canon.Object{"ok": false, "error": err.Error()}
}
