package transport

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"errors"
	"fmt"
	"net/url"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/nostr"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/records"
)

func (n Network) post(ctx context.Context, base string, env Object) bool {
	b, err := records.Wire(env)
	if err != nil {
		return false
	}
	b, err = n.request(ctx, "POST", base+"/v1/records", b, 65536, checkReceiverURL)
	if err != nil {
		return false
	}
	v, err := canon.Parse(b)
	o := config.Obj(v)
	return err == nil && o["ok"] == true && o["id"] == env["id"]
}
func (n Network) publish(ctx context.Context, relay string, event Object) bool {
	ws, err := n.connect(ctx, relay)
	if err != nil {
		return false
	}
	defer ws.close()
	if ws.send([]any{"EVENT", event}) != nil {
		return false
	}
	for {
		m, err := ws.recv()
		if err != nil || len(m) > 0 && m[0] == "AUTH" {
			return false
		}
		if len(m) >= 3 && m[0] == "OK" && m[1] == event["id"] {
			return m[2] == true
		}
	}
}

// Distinct relay spellings for one endpoint count only once.
func distinct(relays []string) []string {
	var out []string
	seen := map[string]bool{}
	for _, r := range relays {
		u, err := url.Parse(r)
		if err != nil {
			continue
		}
		u.Host = strings.ToLower(u.Host)
		if u.Scheme == "wss" {
			u.Host = strings.TrimSuffix(u.Host, ":443")
		} else if u.Scheme == "ws" {
			u.Host = strings.TrimSuffix(u.Host, ":80")
		}
		u.Fragment = ""
		if u.Path == "" {
			u.Path = "/"
		}
		key := u.String()
		if !seen[key] {
			out = append(out, r)
			seen[key] = true
		}
	}
	return out
}
func (n Network) Send(ctx context.Context, env Object, seed []byte) (bool, string) {
	if err := records.Verify(env, time.Now().Unix()); err != nil {
		return false, err.Error()
	}
	relays := distinct(n.Relays)
	var event Object
	if len(relays) > 0 {
		secret, err := nostr.SecretFromSeed(seed)
		if err == nil {
			event, _ = nostr.MakeEvent(secret, env, nil, nil)
		}
	}
	nodes, acks := make(chan bool, len(n.Receivers)), make(chan bool, len(relays))
	for _, base := range n.Receivers {
		go func() { nodes <- n.post(ctx, base, env) }()
	}
	for _, r := range relays {
		go func() { acks <- (event != nil && n.publish(ctx, r, event)) }()
	}
	a, b := 0, 0
	for range n.Receivers {
		if <-nodes {
			a++
		}
	}
	for range relays {
		if <-acks {
			b++
		}
	}
	return a >= 1 || b >= 2, fmt.Sprintf("%d of %d receivers, %d of %d relays", a, len(n.Receivers), b, len(relays))
}
func (n Network) receiver(ctx context.Context, s *Store, base string, after int64) (int64, error) {
	for i := 0; i < 20; i++ {
		address := fmt.Sprintf("%s/v1/records?after=%d&limit=200", base, after)
		b, err := n.request(ctx, "GET", address, nil, 12<<20, checkReceiverURL)
		if err != nil {
			return after, err
		}
		v, err := canon.Parse(b)
		o := config.Obj(v)
		rows, ok := o["records"].([]any)
		if err != nil || !ok || len(rows) > 200 || config.Num(o["next"], -1) != after+int64(len(rows)) {
			return after, errors.New("invalid receiver page")
		}
		for _, v := range rows {
			env := config.Obj(v)
			err = records.Verify(env, time.Now().Unix())
			if errors.Is(err, records.ErrFuture) {
				return after, nil
			}
			if err == nil {
				if _, err = s.Add(env); err != nil {
					return after, err
				}
			}
			after++
		}
		if len(rows) == 0 {
			break
		}
	}
	return after, nil
}
func topic(tags any) bool {
	a, _ := tags.([]any)
	for _, v := range a {
		pair, _ := v.([]any)
		if len(pair) == 2 && pair[0] == "t" && pair[1] == "skynet-architecture-v1" {
			return true
		}
	}
	return false
}
func (n Network) page(ctx context.Context, s *Store, r string, since, until int64) (oldest int64, complete bool, err error) {
	ws, err := n.connect(ctx, r)
	if err != nil {
		return 0, false, err
	}
	defer ws.close()
	var nonce [8]byte
	if _, err = rand.Read(nonce[:]); err != nil {
		return 0, false, err
	}
	sub := hex.EncodeToString(nonce[:])
	q := Object{"kinds": []int{9467}, "#t": []string{"skynet-architecture-v1"}, "limit": 500}
	if since > 0 {
		q["since"] = since
	}
	if until > 0 {
		q["until"] = until
	}
	if err = ws.send([]any{"REQ", sub, q}); err != nil {
		return
	}
	for seen := 0; seen < 500; {
		m, e := ws.recv()
		if e != nil {
			return oldest, false, e
		}
		if len(m) < 2 || m[1] != sub {
			continue
		}
		switch m[0] {
		case "EOSE":
			return oldest, true, nil
		case "CLOSED":
			return oldest, false, errors.New("relay subscription closed")
		case "EVENT":
			if len(m) < 3 {
				continue
			}
			ev := config.Obj(m[2])
			if config.Num(ev["kind"], 0) != 9467 || !topic(ev["tags"]) {
				continue
			}
			seen++
			t := config.Num(ev["created_at"], 0)
			if t > 0 && (oldest == 0 || t < oldest) {
				oldest = t
			}
			env, e := records.Parse([]byte(config.Str(ev["content"])), time.Now().Unix())
			if errors.Is(e, records.ErrFuture) {
				return oldest, false, e
			}
			if e == nil {
				if _, e = s.Add(env); e != nil {
					return oldest, false, e
				}
			}
		}
	}
	return oldest, false, nil
}
func (n Network) Sync(ctx context.Context, s *Store) (int, error) {
	p := filepath.Join(s.Dir, "cursors.json")
	c, err := config.Read(p)
	if errors.Is(err, os.ErrNotExist) {
		c = Object{}
	} else if err != nil {
		return 0, err
	}
	before := len(s.Items)
	now := time.Now().Unix()
	var issues []error
	for _, base := range n.Receivers {
		k := "receiver " + base
		next, e := n.receiver(ctx, s, base, max(0, config.Num(c[k], 0)))
		c[k] = next
		if e != nil {
			issues = append(issues, e)
		}
	}
	for _, r := range distinct(n.Relays) {
		k := "relay " + r
		since := max(0, config.Num(c[k], 0)-3600)
		var until int64
		for i := 0; i < 20; i++ {
			old, done, e := n.page(ctx, s, r, since, until)
			if e != nil {
				issues = append(issues, e)
				break
			}
			if done {
				c[k] = now
				break
			}
			if old == 0 || until != 0 && old >= until {
				break
			}
			until = old
		}
	}
	return len(s.Items) - before, errors.Join(append(issues, config.Write(p, c))...)
}
