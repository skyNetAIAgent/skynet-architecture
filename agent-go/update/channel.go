package update

import (
	"context"
	"errors"
	"fmt"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"time"
)

type Result struct {
	Seq         int
	Version     string
	Halt        string
	HaltThrough int
	Installed   bool
	Note        string
}

func (r *Result) setHalt(h *Halt, running int) {
	r.Halt = h.Message(running)
	r.HaltThrough = 0
	if h != nil {
		r.HaltThrough = h.Through
	}
}

type policy struct {
	Raw       string `json:"raw"`
	Signature string `json:"signature"`
}

func cached(home string, keys []string) (document, error) {
	var p policy
	if err := load(filepath.Join(home, "release-policy.json"), &p); err != nil {
		return document{}, err
	}
	if p.Raw == "" {
		return document{}, nil
	}
	return parse([]byte(p.Raw), []byte(p.Signature), keys)
}

// CachedHalt authenticates the last observed policy even when the channel is offline.
func CachedHalt(home string, running int) (string, error) {
	d, err := cached(home, nil)
	return d.Halt.Message(running), err
}
func get(ctx context.Context, s string, limit int64, asset bool) ([]byte, error) {
	u, err := url.Parse(s)
	if err != nil || u.Scheme != "https" || u.User != nil || asset && !assetURL(s) {
		return nil, errors.New("invalid release URL")
	}
	client := http.Client{Timeout: 90 * time.Second, CheckRedirect: func(r *http.Request, via []*http.Request) error {
		if !asset || len(via) > 3 || !assetURL(r.URL.String()) {
			return errors.New("release redirect refused")
		}
		return nil
	}}
	req, err := http.NewRequestWithContext(ctx, "GET", s, nil)
	if err != nil {
		return nil, err
	}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	if resp.StatusCode != 200 || resp.ContentLength > limit {
		return nil, fmt.Errorf("release HTTP status %d or excessive length", resp.StatusCode)
	}
	return limited(resp.Body, limit)
}
func remember(home string, d document, keys []string) error {
	prior, err := cached(home, keys)
	if err != nil {
		return err
	}
	_, h, err := state(home)
	if err != nil {
		return err
	}
	if d.Seq < max(h.Seq, prior.Seq) || d.Seq == prior.Seq && string(prior.raw) != string(d.raw) {
		return errors.New("stale or conflicting release policy")
	}
	return save(home, "release-policy.json", policy{string(d.raw), string(d.signature)})
}

// Check reads the channel in every mode. On error callers retain the cached halt.
func Check(ctx context.Context, home, base, mode string, running int) (Result, error) {
	var result Result
	previous, err := cached(home, nil)
	if err != nil {
		return result, err
	}
	result.setHalt(previous.Halt, running)
	if mode != "manual" && mode != "auto" && mode != "notify" && mode != "off" {
		return result, errors.New("invalid update mode")
	}
	raw, err := get(ctx, base+Channel, maxManifest, false)
	if err != nil {
		return result, err
	}
	s, err := get(ctx, base+Channel+".sig", 16384, false)
	if err != nil {
		return result, err
	}
	d, err := parse(raw, s, nil)
	if err != nil {
		return result, err
	}
	err = Locked(home, func() error {
		if d.Seq < running {
			return errors.New("release older than running version")
		}
		if err := remember(home, d, nil); err != nil {
			return err
		}
		result.setHalt(d.Halt, running)
		if mode == "auto" {
			var err error
			mode, err = configuredMode(home)
			if err != nil {
				return err
			}
		}
		if mode == "off" || result.Halt != "" || d.Seq == running {
			return nil
		}
		result.Seq, result.Version = d.Seq, d.Version
		if _, ok := d.Targets[Platform()]; !ok {
			result.Note = "no target for " + Platform()
			return nil
		}
		if mode == "notify" || d.Halt.Message(d.Seq) != "" {
			result.Note = "release available, installation deferred"
			return nil
		}
		c, err := CurrentVersion(home)
		if err != nil {
			return err
		}
		exe, err := os.Executable()
		if err != nil {
			return err
		}
		if filepath.Clean(filepath.Dir(exe)) != filepath.Join(home, c.Dir) || c.Runtime != "go" {
			return errors.New("not the active installed version")
		}
		i := installer{fetch: func(t Target) ([]byte, error) { return get(ctx, t.URL, t.Size, true) }, check: checkCandidate, probe: checkLauncher}
		if err = i.install(home, d, running, ""); err != nil {
			return err
		}
		result.Installed = true
		return nil
	})
	return result, err
}
