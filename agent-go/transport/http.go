// Package transport exchanges signed records with receivers and Nostr relays.
package transport

import (
	"bytes"
	"context"
	"errors"
	"fmt"
	"io"
	"net"
	"net/http"
	"net/url"
	"os"
	"strings"
	"sync"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
)

type Object = config.Object
type Network struct {
	HTTP              http.RoundTripper
	Receivers, Relays []string
}

// Keep in sync with RECEIVERS in agent/skynet_agent/trust.py.
var builtinReceivers = []string{"http://62.213.14.254:8790"}

func endpoints(key, defaults string) []string {
	s, ok := os.LookupEnv(key)
	if !ok {
		s = defaults
	}
	seen := map[string]bool{}
	var out []string
	for _, item := range strings.Split(s, ",") {
		item = strings.TrimRight(strings.TrimSpace(item), "/")
		if item != "" && item != "none" && !seen[item] {
			seen[item] = true
			out = append(out, item)
		}
	}
	return out
}
func Default() Network {
	return Network{HTTP: http.DefaultTransport, Receivers: endpoints("SKYNET_AGENT_RECEIVERS", strings.Join(builtinReceivers, ",")),
		Relays: endpoints("SKYNET_AGENT_RELAYS", "wss://nos.lol,wss://relay.primal.net,wss://relay.snort.social,wss://offchain.pub,wss://nostr.mom,wss://relay.nostr.net,wss://nostr.bitcoiner.social")}
}
func checkURL(u *url.URL) error {
	if u.Hostname() == "" || u.User != nil {
		return errors.New("invalid endpoint")
	}
	if u.Scheme == "https" {
		return nil
	}
	if u.Scheme == "http" {
		if host := u.Hostname(); strings.EqualFold(host, "localhost") || net.ParseIP(host).IsLoopback() {
			return nil
		}
	}
	return errors.New("HTTPS required outside loopback")
}

func checkReceiverURL(u *url.URL) error {
	if u.Scheme == "http" && u.User == nil {
		endpoint := u.Scheme + "://" + u.Host + u.EscapedPath()
		for _, base := range builtinReceivers {
			if endpoint == base+"/v1/records" || endpoint == base+"/v1/status" {
				return nil
			}
		}
	}
	return checkURL(u)
}

// SendStatus posts the same snapshot to each full node. Later snapshots supersede failed posts.
func (n Network) SendStatus(ctx context.Context, envelope []byte) {
	var pending sync.WaitGroup
	for _, base := range n.Receivers {
		pending.Add(1)
		go func() {
			defer pending.Done()
			n.request(ctx, http.MethodPost, base+"/v1/status", envelope, 4096, checkReceiverURL)
		}()
	}
	pending.Wait()
}

func (n Network) Request(ctx context.Context, method, address string, data []byte, limit int64) ([]byte, error) {
	return n.request(ctx, method, address, data, limit, checkURL)
}

func (n Network) request(ctx context.Context, method, address string, data []byte, limit int64, check func(*url.URL) error) ([]byte, error) {
	req, err := http.NewRequestWithContext(ctx, method, address, bytes.NewReader(data))
	if err != nil {
		return nil, err
	}
	if err = check(req.URL); err != nil {
		return nil, err
	}
	req.Header.Set("User-Agent", "skynet-agent/"+config.Version)
	if data != nil {
		req.Header.Set("Content-Type", "application/json")
	}
	client := http.Client{Transport: n.HTTP, Timeout: 30 * time.Second, CheckRedirect: func(r *http.Request, via []*http.Request) error {
		if method != http.MethodGet || len(via) >= 10 {
			return http.ErrUseLastResponse
		}
		return check(r.URL)
	}}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	if resp.StatusCode != 200 {
		return nil, fmt.Errorf("HTTP %d for %s", resp.StatusCode, address)
	}
	b, err := io.ReadAll(io.LimitReader(resp.Body, limit+1))
	if int64(len(b)) > limit {
		return nil, errors.New("response too large")
	}
	return b, err
}
