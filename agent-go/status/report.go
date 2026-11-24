// Package status reports the volunteer agent's public identity and compute capacity.
package status

import (
	"context"
	"crypto/ed25519"
	"encoding/hex"
	"errors"
	"runtime"
	"strings"
	"sync"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/records"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/transport"
)

// Envelope signs the canonical ASCII status and returns its UTF-8 wire representation.
func Envelope(seed []byte, started, sent, unitsDone int64, cpuModel string, ramMB int64, gpus []GPU) ([]byte, error) {
	if len(seed) != ed25519.SeedSize {
		return nil, errors.New("invalid seed length")
	}
	key := ed25519.NewKeyFromSeed(seed)
	body := canon.Object{
		"v": 1, "agent": hex.EncodeToString(key.Public().(ed25519.PublicKey)),
		"version": config.Version, "release_seq": config.Sequence,
		"os": runtime.GOOS, "arch": runtime.GOARCH, "cpu_threads": runtime.NumCPU(),
		"cpu_model": cpuModel, "ram_mb": ramMB, "gpus": []canon.Object{},
		"units_done": unitsDone, "started": started, "sent": sent,
	}
	// Reserve the fixed-width signature before filling the remaining wire budget with GPUs.
	env := canon.Object{"status": body, "sig": strings.Repeat("0", hex.EncodedLen(ed25519.SignatureSize))}
	base, err := canon.Marshal(env, false)
	if err != nil {
		return nil, err
	}
	remaining := 4096 - len(base)
	if remaining < 0 {
		return nil, errors.New("status exceeds 4096 bytes")
	}
	var devices []canon.Object
	for _, gpu := range gpus {
		device := canon.Object{"name": gpu.Name, "vram_mb": gpu.VRAMMB}
		entry, err := canon.Marshal(device, false)
		if err != nil {
			return nil, err
		}
		if len(devices) > 0 {
			remaining-- // comma
		}
		remaining -= len(entry)
		if remaining < 0 {
			break
		}
		devices = append(devices, device)
	}
	body["gpus"] = devices
	raw, err := canon.Marshal(body, true)
	if err != nil {
		return nil, err
	}
	env["sig"] = hex.EncodeToString(ed25519.Sign(key, raw))
	return canon.Marshal(env, false)
}

var (
	hardwareOnce sync.Once
	hwCPU        string
	hwRAM        int64
	hwGPUs       []GPU
)

// cachedHardware asks the system once per process: the hardware does not change between reports.
func cachedHardware(ctx context.Context) (string, int64, []GPU) {
	hardwareOnce.Do(func() { hwCPU, hwRAM, hwGPUs = Hardware(ctx) })
	return hwCPU, hwRAM, hwGPUs
}

func send(ctx context.Context, home string, n transport.Network, started int64) {
	cfg, err := config.Load(home)
	if err != nil || config.Get(cfg, "status.enabled") != true || len(n.Receivers) == 0 {
		return
	}
	state, err := config.State(home)
	if err != nil {
		return
	}
	seed, err := records.LoadSeed(home, true)
	if err != nil {
		return
	}
	cpu, ram, gpus := cachedHardware(ctx)
	units := config.Num(config.Obj(state["counters"])["units_done"], 0)
	data, err := Envelope(seed, started, time.Now().Unix(), units, cpu, ram, gpus)
	if err == nil && ctx.Err() == nil {
		n.SendStatus(ctx, data)
	}
}

// Start runs alongside the compute loop and returns a function that stops and joins it.
func Start(parent context.Context, home string, n transport.Network) func() {
	ctx, cancel := context.WithCancel(parent)
	done := make(chan struct{})
	started := time.Now().Unix()
	go func() {
		defer close(done)
		schedule(ctx, 10*time.Second, 2*time.Minute, func() { send(ctx, home, n, started) })
	}()
	return func() {
		cancel()
		<-done
	}
}

func schedule(ctx context.Context, first, interval time.Duration, report func()) {
	timer := time.NewTimer(first)
	defer timer.Stop()
	for ctx.Err() == nil {
		select {
		case <-ctx.Done():
			return
		case <-timer.C:
			timer.Reset(interval)
			report()
		}
	}
}
