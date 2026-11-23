package main

import (
	"bytes"
	"context"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"testing"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/transport"
)

func TestAndroidPowerTransitions(t *testing.T) {
	h := androidHost{home: t.TempDir(), wake: make(chan struct{}, 1)}
	reader, writer := io.Pipe()
	defer writer.Close()
	ctx, stop := context.WithCancel(context.Background())
	defer stop()
	go h.readControl(reader, stop)
	send := func(line string) {
		t.Helper()
		if _, err := fmt.Fprintln(writer, line); err != nil {
			t.Fatal(err)
		}
		select {
		case <-h.wake:
		case <-time.After(time.Second):
			t.Fatal("service ignored power message")
		}
	}
	unit := func() context.Context {
		h.mu.Lock()
		defer h.mu.Unlock()
		var work context.Context
		work, h.stopUnit = context.WithCancel(ctx)
		return work
	}
	if h.isCharging() {
		t.Fatal("missing initial charging signal permitted computation")
	}
	send("charging 1")
	active := unit()
	send("charging 0")
	if active.Err() == nil {
		t.Fatal("disconnect did not cancel an active unit")
	}
	if err := config.Write(filepath.Join(h.home, "config.json"), Object{"run_on_battery": true}); err != nil {
		t.Fatal(err)
	}
	send("charging 1")
	active = unit()
	send("charging 0")
	if active.Err() != nil {
		t.Fatal("battery override did not keep an active unit")
	}
	if err := writer.Close(); err != nil {
		t.Fatal(err)
	}
	select {
	case <-active.Done():
	case <-time.After(time.Second):
		t.Fatal("loss of the Java service did not cancel its children")
	}
}

type serviceHTTP func(*http.Request) (*http.Response, error)

func (f serviceHTTP) RoundTrip(req *http.Request) (*http.Response, error) { return f(req) }

func TestAndroidPollPublishesMigratedQueue(t *testing.T) {
	h := androidHost{home: t.TempDir(), wake: make(chan struct{}, 1)}
	fixtures := filepath.Join("..", "..", "testdata")
	const entry = "1700000000000-old-task-0.json"
	if err := os.Mkdir(filepath.Join(h.home, "outbox"), 0700); err != nil {
		t.Fatal(err)
	}
	for _, name := range []string{"identity.key", "state.json", filepath.Join("outbox", entry)} {
		b, err := os.ReadFile(filepath.Join(fixtures, "python-home", fixtureFile(name)))
		if err != nil {
			t.Fatal(err)
		}
		if err = os.WriteFile(filepath.Join(h.home, name), b, 0600); err != nil {
			t.Fatal(err)
		}
	}
	t.Setenv("SKYNET_AGENT_BASE_URL", "https://repo.invalid")
	t.Setenv("SKYNET_AGENT_SUBMIT_VIA", "net")
	ctx, stop := context.WithTimeout(context.Background(), 5*time.Second)
	defer stop()
	// The Android service uses the same authenticated task index and the original
	// Python-signed envelope, even if its halt channel is temporarily unavailable.
	const id = "30544d061003188fad0b7fb3a6f8baa805886dbfd5be4d259f0e7394af39ddb3"
	network := serviceHTTP(func(req *http.Request) (*http.Response, error) {
		var body []byte
		var err error
		status := 200
		switch req.URL.Path {
		case "/agent/v2/release.json":
			status = 404
		case "/tasks/index.json", "/tasks/index.json.sig":
			body, err = os.ReadFile(filepath.Join(fixtures, filepath.Base(req.URL.Path)))
		case "/v1/records":
			body, err = io.ReadAll(req.Body)
			if err == nil && !bytes.Contains(body, []byte(id)) {
				t.Error("publication lost the queued record ID")
			}
			body = []byte(`{"ok":true,"id":"` + id + `"}`)
			stop()
		default:
			return nil, fmt.Errorf("unexpected request: %s", req.URL)
		}
		return &http.Response{StatusCode: status, Header: make(http.Header), Body: io.NopCloser(bytes.NewReader(body))}, err
	})
	saved := http.DefaultTransport
	http.DefaultTransport = network
	defer func() { http.DefaultTransport = saved }()
	err := h.loop(ctx, transport.Network{HTTP: network, Receivers: []string{"https://receiver.invalid"}}, io.Discard)
	if err != nil {
		t.Fatal(err)
	}
	for _, name := range []string{"task-list.json", filepath.Join("sent", entry)} {
		if _, err := os.Stat(filepath.Join(h.home, name)); err != nil {
			t.Fatal(err)
		}
	}
	status, err := config.Read(filepath.Join(h.home, "status.json"))
	if err != nil || status["code"] != "stopped" || config.Num(status["published"], 0) != 1 ||
		config.Num(status["units_done"], 0) != 1 || config.Num(status["outbox"], -1) != 0 {
		t.Fatalf("status after publication: %v (%v)", status, err)
	}
}
