package status

import (
	"bytes"
	"context"
	"crypto/ed25519"
	"encoding/hex"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"reflect"
	"runtime"
	"strings"
	"sync"
	"testing"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/records"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/transport"
)

func verified(t *testing.T, data, seed []byte) canon.Object {
	t.Helper()
	value, err := canon.Parse(data)
	if err != nil {
		t.Fatal(err)
	}
	env := config.Obj(value)
	body := config.Obj(env["status"])
	raw, err := canon.Marshal(body, true)
	pub := ed25519.NewKeyFromSeed(seed).Public().(ed25519.PublicKey)
	sig, hexErr := hex.DecodeString(config.Str(env["sig"]))
	if len(env) != 2 || err != nil || hexErr != nil || body["agent"] != hex.EncodeToString(pub) || !ed25519.Verify(pub, raw, sig) {
		t.Fatal("unexpected envelope or invalid signature")
	}
	return body
}

func TestSignedStatus(t *testing.T) {
	seed := bytes.Repeat([]byte{17}, 32)
	data, err := Envelope(seed, 1700000000, 1700000060, 123, "CPU®", 4096, []GPU{{Name: "Graphics™", VRAMMB: 1024}})
	if err != nil {
		t.Fatal(err)
	}
	body := verified(t, data, seed)
	want := canon.Object{
		"v": int64(1), "agent": body["agent"], "version": config.Version, "release_seq": config.Sequence,
		"os": runtime.GOOS, "arch": runtime.GOARCH, "cpu_model": "CPU®", "cpu_threads": int64(runtime.NumCPU()),
		"ram_mb": int64(4096), "gpus": []any{canon.Object{"name": "Graphics™", "vram_mb": int64(1024)}},
		"units_done": int64(123), "started": int64(1700000000), "sent": int64(1700000060),
	}
	if !reflect.DeepEqual(body, want) {
		t.Fatalf("unexpected status: %v", body)
	}
}

func TestStatusSizeLimit(t *testing.T) {
	var gpus []GPU
	for i := 0; i < 128; i++ {
		gpus = append(gpus, GPU{Name: strings.Repeat("雪", 60), VRAMMB: 16384})
	}
	seed := make([]byte, ed25519.SeedSize)
	data, err := Envelope(seed, 1, 2, 0, "", 0, gpus)
	if err != nil || len(data) > 4096 {
		t.Fatalf("wire size %d, error %v", len(data), err)
	}
	count := len(verified(t, data, seed)["gpus"].([]any))
	if count == 0 || count >= len(gpus) {
		t.Fatalf("unexpected device count %d", count)
	}
}

type postFunc func(*http.Request) (*http.Response, error)

func (f postFunc) RoundTrip(r *http.Request) (*http.Response, error) { return f(r) }

func TestSendUsesConfiguredReceiversAndPersistedCounter(t *testing.T) {
	home := t.TempDir()
	t.Setenv("PATH", t.TempDir())
	if err := config.Write(filepath.Join(home, "state.json"), canon.Object{"counters": canon.Object{"units_done": 901}}); err != nil {
		t.Fatal(err)
	}
	var mu sync.Mutex
	posts := map[string][]byte{}
	n := transport.Network{
		Receivers: []string{"http://62.213.14.254:8790", "https://second.invalid"},
		Relays:    []string{"wss://relay.invalid"},
		HTTP: postFunc(func(r *http.Request) (*http.Response, error) {
			if r.Method != "POST" || r.URL.Path != "/v1/status" || r.Header.Get("Content-Type") != "application/json" {
				t.Errorf("unexpected request %s %s", r.Method, r.URL)
			}
			data, err := io.ReadAll(r.Body)
			r.Body.Close()
			if err != nil {
				return nil, err
			}
			mu.Lock()
			posts[r.URL.Host] = data
			mu.Unlock()
			return &http.Response{StatusCode: 200, Body: io.NopCloser(strings.NewReader(`{"ok":true}`))}, nil
		}),
	}
	cfg := config.Defaults()
	if err := config.Set(cfg, "status.enabled", "false"); err != nil {
		t.Fatal(err)
	}
	path := filepath.Join(home, "config.json")
	if err := config.Write(path, cfg); err != nil {
		t.Fatal(err)
	}
	send(context.Background(), home, n, 100)
	if _, err := os.Stat(filepath.Join(home, "identity.key")); !os.IsNotExist(err) || len(posts) != 0 {
		t.Fatal("disabled status generated an identity or made a request")
	}
	if err := os.Remove(path); err != nil {
		t.Fatal(err)
	}
	send(context.Background(), home, n, 100)
	seed, err := records.LoadSeed(home, false)
	if err != nil || len(seed) != ed25519.SeedSize {
		t.Fatal("missing identity", err)
	}
	first, second := posts["62.213.14.254:8790"], posts["second.invalid"]
	if len(posts) != 2 || !bytes.Equal(first, second) {
		t.Fatal("full nodes did not get identical snapshots")
	}
	body := verified(t, first, seed)
	if body["units_done"] != int64(901) || body["started"] != int64(100) {
		t.Fatal("profile counter or process start time missing")
	}
}

func TestSchedule(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()
	start := time.Now()
	var ticks []time.Time
	schedule(ctx, 10*time.Millisecond, 20*time.Millisecond, func() {
		ticks = append(ticks, time.Now())
		if len(ticks) == 2 {
			cancel()
		}
	})
	if len(ticks) != 2 || ticks[0].Sub(start) < 10*time.Millisecond || ticks[1].Sub(start) < 30*time.Millisecond {
		t.Fatalf("unexpected reporting schedule: %v", ticks)
	}
}
