package transport

import (
	"bufio"
	"bytes"
	"context"
	"crypto/sha1"
	"encoding/base64"
	"encoding/binary"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net"
	"net/http"
	"net/http/httptest"
	"net/url"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"testing"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/records"
)

// Route real HTTP and upgraded WebSocket connections entirely through memory.
type memoryListener struct {
	in   chan net.Conn
	done chan struct{}
	once sync.Once
}

func (l *memoryListener) Accept() (net.Conn, error) {
	select {
	case c := <-l.in:
		return c, nil
	case <-l.done:
		return nil, net.ErrClosed
	}
}
func (l *memoryListener) Close() error   { l.once.Do(func() { close(l.done) }); return nil }
func (l *memoryListener) Addr() net.Addr { return &net.TCPAddr{IP: net.IPv4(127, 0, 0, 1), Port: 9001} }
func (l *memoryListener) dial(ctx context.Context, _, _ string) (net.Conn, error) {
	// Give both directions independent buffering, including simultaneous TLS close alerts.
	client, a := net.Pipe()
	b, server := net.Pipe()
	pump := func(dst, src net.Conn) { io.Copy(dst, src); dst.Close(); src.Close() }
	go pump(a, b)
	go pump(b, a)
	select {
	case l.in <- server:
		return client, nil
	case <-ctx.Done():
		client.Close()
		server.Close()
		return nil, ctx.Err()
	}
}
func server(t *testing.T, h http.Handler) (Network, string) {
	t.Helper()
	l := &memoryListener{in: make(chan net.Conn), done: make(chan struct{})}
	s := &httptest.Server{Listener: l, EnableHTTP2: true, Config: &http.Server{Handler: h}}
	s.StartTLS()
	tr := s.Client().Transport.(*http.Transport).Clone()
	tr.DialContext = l.dial
	tr.Proxy = nil
	t.Cleanup(func() { tr.CloseIdleConnections(); s.Close() })
	return Network{HTTP: tr}, s.URL
}
func testRecord(t *testing.T) (Object, []byte) {
	t.Helper()
	seed := make([]byte, 32)
	e, err := records.Make(seed, "task", Object{"title": "title", "text": "text", "accept": "done"}, 1700000000)
	if err != nil {
		t.Fatal(err)
	}
	return e, seed
}
func masked(r io.Reader) (byte, []byte, error) {
	var h [2]byte
	if _, err := io.ReadFull(r, h[:]); err != nil {
		return 0, nil, err
	}
	if h[1]&128 == 0 {
		return 0, nil, errors.New("client frame without mask")
	}
	n := uint64(h[1] & 127)
	switch n {
	case 126:
		var k uint16
		if err := binary.Read(r, binary.BigEndian, &k); err != nil {
			return 0, nil, err
		}
		n = uint64(k)
	case 127:
		if err := binary.Read(r, binary.BigEndian, &n); err != nil {
			return 0, nil, err
		}
	}
	if n > wsLimit {
		return 0, nil, errors.New("oversized client frame")
	}
	var mask [4]byte
	if _, err := io.ReadFull(r, mask[:]); err != nil {
		return 0, nil, err
	}
	p := make([]byte, int(n))
	if _, err := io.ReadFull(r, p); err != nil {
		return 0, nil, err
	}
	for i := range p {
		p[i] ^= mask[i%4]
	}
	return h[0] & 15, p, nil
}
func sendFrame(w io.Writer, op byte, p []byte) error {
	h := []byte{op}
	if len(p) < 126 {
		h = append(h, byte(len(p)))
	} else {
		h = binary.BigEndian.AppendUint16(append(h, 126), uint16(len(p)))
	}
	_, err := w.Write(append(h, p...))
	return err
}

type relayHandler func(*http.Request, []any, io.Writer) error

func relay(t *testing.T, answer relayHandler) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if r.Header.Get("Sec-WebSocket-Version") != "13" {
			t.Error("wrong WebSocket version")
			return
		}
		c, buf, err := w.(http.Hijacker).Hijack()
		if err != nil {
			t.Error(err)
			return
		}
		defer c.Close()
		c.SetDeadline(time.Now().Add(3 * time.Second))
		sum := sha1.Sum([]byte(r.Header.Get("Sec-WebSocket-Key") + magic))
		fmt.Fprintf(buf, "HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: %s\r\n\r\n", base64.StdEncoding.EncodeToString(sum[:]))
		buf.Flush()
		op, p, err := masked(buf)
		if err != nil || op != 1 {
			t.Errorf("client message %d: %v", op, err)
			return
		}
		v, err := canon.Parse(p)
		if err != nil {
			t.Error(err)
			return
		}
		if err := sendFrame(c, 0x89, []byte("ping")); err != nil {
			t.Error(err)
			return
		}
		op, p, err = masked(buf)
		if err != nil || op != 10 || string(p) != "ping" {
			t.Errorf("pong %d %s %v", op, p, err)
			return
		}
		if err := answer(r, v.([]any), c); err != nil {
			t.Error(err)
			return
		}
		op, _, err = masked(buf)
		if err != nil || op != 8 {
			t.Errorf("close %d: %v", op, err)
		}
	}
}
func TestDelivery(t *testing.T) {
	env, seed := testRecord(t)
	mux := http.NewServeMux()
	mux.HandleFunc("/node/v1/records", func(w http.ResponseWriter, r *http.Request) {
		b, e := io.ReadAll(r.Body)
		wire, _ := records.Wire(env)
		if e != nil || r.Method != "POST" || !bytes.Equal(wire, b) {
			t.Error("wrong record POST")
		}
		json.NewEncoder(w).Encode(Object{"ok": true, "id": env["id"]})
	})
	mux.HandleFunc("/wrong/v1/records", func(w http.ResponseWriter, r *http.Request) { fmt.Fprint(w, `{"ok":true,"id":"wrong"}`) })
	mux.Handle("/relay", relay(t, func(r *http.Request, m []any, w io.Writer) error {
		event := config.Obj(m[1])
		if m[0] != "EVENT" || config.Num(event["kind"], 0) != 9467 {
			return errors.New("wrong EVENT")
		}
		id := event["id"]
		if r.URL.Query().Get("bad") != "" {
			id = "wrong"
		}
		b, _ := canon.Marshal([]any{"OK", id, true, ""}, false)
		if err := sendFrame(w, 1, b[:4]); err != nil {
			return err
		}
		if err := sendFrame(w, 0x80, b[4:]); err != nil {
			return err
		}
		if id == "wrong" {
			b, _ = canon.Marshal([]any{"OK", event["id"], false, "refused"}, false)
			return sendFrame(w, 0x81, b)
		}
		return nil
	}))
	n, base := server(t, mux)
	r1 := "wss://127.0.0.1:9001/relay"
	r2 := "wss://127.0.0.1:9002/relay"
	for _, tc := range []struct {
		name          string
		nodes, relays []string
		want          bool
	}{
		{"node", []string{base + "/node"}, nil, true}, {"wrong node", []string{base + "/wrong"}, nil, false},
		{"one relay", nil, []string{r1}, false}, {"duplicate", nil, []string{r1, r1}, false}, {"wrong relay id", nil, []string{r1, r2 + "?bad=1"}, false}, {"two relays", nil, []string{r1, r2}, true},
	} {
		t.Run(tc.name, func(t *testing.T) {
			n.Receivers, n.Relays = tc.nodes, tc.relays
			if got, msg := n.Send(context.Background(), env, seed); got != tc.want {
				t.Fatalf("%t: %s", got, msg)
			}
		})
	}
}

type localHandler http.HandlerFunc

func (h localHandler) RoundTrip(r *http.Request) (*http.Response, error) {
	w := httptest.NewRecorder()
	h(w, r)
	return w.Result(), nil
}

func TestBuiltinHTTPReceiver(t *testing.T) {
	const base = "http://62.213.14.254:8790"
	env, seed := testRecord(t)
	t.Setenv("SKYNET_AGENT_RECEIVERS", "")
	if err := os.Unsetenv("SKYNET_AGENT_RECEIVERS"); err != nil {
		t.Fatal(err)
	}
	t.Setenv("SKYNET_AGENT_RELAYS", "none")
	n := Default()
	if len(n.Receivers) != 1 || n.Receivers[0] != base {
		t.Fatalf("default receivers: %v", n.Receivers)
	}
	n.HTTP = localHandler(func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case "POST":
			json.NewEncoder(w).Encode(Object{"ok": true, "id": env["id"]})
		case "GET":
			json.NewEncoder(w).Encode(Object{"records": []any{}, "next": 0})
		}
	})
	ctx := context.Background()
	if ok, msg := n.Send(ctx, env, seed); !ok {
		t.Fatal(msg)
	}
	store, err := Open(t.TempDir())
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	if _, err := n.Sync(ctx, store); err != nil {
		t.Fatal(err)
	}
	if _, err := n.Request(ctx, "GET", base+"/v1/records", nil, 65536); err == nil {
		t.Fatal("general downloads inherited the receiver exception")
	}
}

func TestReceiverURLPolicy(t *testing.T) {
	t.Setenv("SKYNET_AGENT_RECEIVERS", "http://example.org:8790")
	for _, tc := range []struct {
		address string
		allowed bool
	}{
		{"http://62.213.14.254:8790/v1/records?after=0", true},
		{"http://127.0.0.1:9000/v1/records", true},
		{"http://127.0.0.2:9000/v1/records", true},
		{"http://[::1]:9000/v1/records", true},
		{"https://example.org/v1/records", true},
		{"http://example.org:8790/v1/records", false},
		{"http://62.213.14.254:8791/v1/records", false},
		{"http://62.213.14.254/v1/records", false},
		{"http://62.213.14.254.example.org:8790/v1/records", false},
		{"http://user@62.213.14.254:8790/v1/records", false},
		{"http://62.213.14.254:8790/tasks/index.json", false},
		{"http://62.213.14.254:8790/%76%31/records", false},
	} {
		u, err := url.Parse(tc.address)
		if err != nil {
			t.Fatal(err)
		}
		if got := checkReceiverURL(u); (got == nil) != tc.allowed {
			t.Errorf("%s: %v (allowed=%v)", tc.address, got, tc.allowed)
		}
	}
}

func TestReceiverHTTPRedirect(t *testing.T) {
	base := builtinReceivers[0]
	n := Network{HTTP: localHandler(func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Host != "62.213.14.254:8790" {
			t.Errorf("contacted redirect target %s", r.URL.Host)
		}
		w.Header().Set("Location", "http://example.org/v1/records")
		w.WriteHeader(http.StatusFound)
	})}
	store, err := Open(t.TempDir())
	if err != nil {
		t.Fatal(err)
	}
	defer store.Close()
	if _, err := n.receiver(context.Background(), store, base, 0); err == nil {
		t.Fatal("followed plaintext redirect to another host")
	}
}

func TestSyncAndRecovery(t *testing.T) {
	env, _ := testRecord(t)
	home := t.TempDir()
	s, err := Open(home)
	if err != nil {
		t.Fatal(err)
	}
	mux := http.NewServeMux()
	mux.HandleFunc("/v1/records", func(w http.ResponseWriter, r *http.Request) {
		switch r.URL.Query().Get("after") {
		case "0":
			json.NewEncoder(w).Encode(Object{"records": []any{env}, "next": 1})
		case "1":
			json.NewEncoder(w).Encode(Object{"records": []any{}, "next": 1})
		default:
			t.Error("bad cursor")
		}
	})
	var since int64
	mux.Handle("/relay", relay(t, func(r *http.Request, m []any, w io.Writer) error {
		q := config.Obj(m[2])
		if m[0] != "REQ" {
			return errors.New("expected REQ")
		}
		since = config.Num(q["since"], 0)
		wire, _ := records.Wire(env)
		event := Object{"kind": 9467, "tags": [][]string{{"t", "skynet-architecture-v1"}}, "content": string(wire), "created_at": 1700000000}
		b, _ := canon.Marshal([]any{"EVENT", m[1], event}, false)
		if err := sendFrame(w, 0x81, b); err != nil {
			return err
		}
		b, _ = canon.Marshal([]any{"EOSE", m[1]}, false)
		return sendFrame(w, 0x81, b)
	}))
	n, base := server(t, mux)
	n.Receivers = []string{base}
	r := strings.Replace(base, "https", "wss", 1) + "/relay"
	n.Relays = []string{r}
	ctx := context.Background()
	s.limit = 1
	if _, err := n.Sync(ctx, s); !errors.Is(err, ErrFull) {
		t.Fatal(err)
	}
	cursors := filepath.Join(s.Dir, "cursors.json")
	c, err := config.Read(cursors)
	if err != nil || config.Num(c["receiver "+base], -1) != 0 || c["relay "+r] != nil {
		t.Fatal(c, err)
	}
	s.limit = MaxStore
	count, err := n.Sync(ctx, s)
	if count != 1 || err != nil {
		t.Fatal(count, err)
	}
	c, err = config.Read(cursors)
	if err != nil {
		t.Fatal(err)
	}
	count, err = n.Sync(ctx, s)
	if count != 0 || err != nil || since != config.Num(c["relay "+r], 0)-3600 {
		t.Fatal(count, err, since)
	}
	s.Close()
	path := filepath.Join(home, "net", "records.jsonl")
	f, err := os.OpenFile(path, os.O_APPEND|os.O_WRONLY, 0600)
	if err != nil {
		t.Fatal(err)
	}
	fmt.Fprint(f, "broken")
	f.Close()
	s, err = Open(home)
	if err != nil {
		t.Fatal(err)
	}
	defer s.Close()
	file, err := os.Open(path)
	if err != nil {
		t.Fatal(err)
	}
	defer file.Close()
	sc := bufio.NewScanner(file)
	if !sc.Scan() || sc.Scan() || sc.Err() != nil || len(s.Items) != 1 {
		t.Error("journal tail not repaired")
	}
}

// TestRetrySkipsBrokenPending checks that a corrupt pending entry keeps its
// place on disk but does not consume the 200-attempt budget, so the entries
// behind it are still delivered.
func TestRetrySkipsBrokenPending(t *testing.T) {
	home := t.TempDir()
	seed := make([]byte, 32)
	first, err := records.Make(seed, "task", Object{"title": "a", "text": "a", "accept": "a"}, 1700000000)
	if err != nil {
		t.Fatal(err)
	}
	second, err := records.Make(seed, "task", Object{"title": "b", "text": "b", "accept": "b"}, 1700000001)
	if err != nil {
		t.Fatal(err)
	}
	dir := filepath.Join(home, "net", "pending")
	if err := os.MkdirAll(dir, 0700); err != nil {
		t.Fatal(err)
	}
	if err := config.Write(filepath.Join(dir, "0-corrupt.json"), Object{"id": "broken"}); err != nil {
		t.Fatal(err)
	}
	for _, env := range []Object{first, second} {
		if err := config.Write(filepath.Join(dir, config.Str(env["id"])+".json"), env); err != nil {
			t.Fatal(err)
		}
	}
	delivered := map[string]bool{}
	n := Network{Receivers: []string{"http://127.0.0.1:9000"}, HTTP: localHandler(func(w http.ResponseWriter, r *http.Request) {
		b, e := io.ReadAll(r.Body)
		if e != nil {
			return
		}
		v, e := canon.Parse(b)
		if e != nil {
			return
		}
		delivered[config.Str(config.Obj(v)["id"])] = true
		json.NewEncoder(w).Encode(Object{"ok": true, "id": config.Str(config.Obj(v)["id"])})
	})}
	s, err := Open(home)
	if err != nil {
		t.Fatal(err)
	}
	defer s.Close()
	ctx := context.Background()
	count, err := n.Retry(ctx, s, seed)
	if err != nil || count != 2 {
		t.Fatalf("retry count = %d, %v", count, err)
	}
	if !delivered[config.Str(first["id"])] || !delivered[config.Str(second["id"])] {
		t.Fatalf("delivered = %v", delivered)
	}
	if _, err := os.Stat(filepath.Join(dir, "0-corrupt.json")); err != nil {
		t.Fatalf("broken entry was removed: %v", err)
	}
}
