// Package update authenticates and installs signed desktop releases.
package update

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"net/url"
	"regexp"
	"runtime"
	"strings"
	"unicode/utf8"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/sig"
)

const BaseURL = "https://raw.githubusercontent.com/skyNetAIAgent/skynet-architecture/main"
const Channel = "/agent/v2/release.json"
const maxManifest = 256 << 10
const maxBinary = 64 << 20
const maxSeq = 999999999

var versionRE = regexp.MustCompile(`^[0-9]{1,4}\.[0-9]{1,4}\.[0-9]{1,4}$`)
var hashRE = regexp.MustCompile(`^[0-9a-f]{64}$`)
var platformRE = regexp.MustCompile(`^(windows-(amd64|arm64)|linux-(amd64|arm64|arm))$`)

func Platform() string { return runtime.GOOS + "-" + runtime.GOARCH }
func binaryName(platform string) string {
	if strings.HasPrefix(platform, "windows-") {
		return "skynet-agent.exe"
	}
	return "skynet-agent"
}
func Binary() string { return binaryName(Platform()) }

type File struct {
	Size   int64  `json:"size"`
	SHA256 string `json:"sha256"`
}
type Target struct {
	File
	Name string `json:"name"`
	URL  string `json:"url"`
}
type Halt struct {
	Through int    `json:"through_seq"`
	Reason  string `json:"reason"`
}

func (h *Halt) Message(seq int) string {
	if h == nil || h.Through < seq {
		return ""
	}
	if h.Reason == "" {
		return "release paused by the maintainers"
	}
	return h.Reason
}

type Release struct {
	Format    int               `json:"format"`
	Seq       int               `json:"seq"`
	Version   string            `json:"version"`
	MinBridge int               `json:"min_bridge_seq"`
	Targets   map[string]Target `json:"targets"`
	Compat    map[string]File   `json:"compat_files,omitempty"`
	Halt      *Halt             `json:"halt,omitempty"`
}
type document struct {
	Release
	raw, signature []byte
}

func assetURL(s string) bool {
	u, err := url.Parse(s)
	if err != nil || u.Scheme != "https" || u.User != nil || u.Fragment != "" || u.Path == "" {
		return false
	}
	switch u.Host {
	case "github.com", "objects.githubusercontent.com", "release-assets.githubusercontent.com":
		return true
	}
	return false
}

// encoding/json accepts mixed-case field names and null scalars. The signed format does not.
func validFields(obj map[string]any) bool {
	for name, v := range obj {
		if v == nil || name != strings.ToLower(name) {
			return false
		}
		if child, ok := v.(map[string]any); ok && !validFields(child) {
			return false
		}
	}
	return true
}
func parse(raw, signature []byte, keys []string) (document, error) {
	var d document
	if len(raw) > maxManifest || len(signature) > 16384 {
		return d, errors.New("release document too large")
	}
	obj, err := sig.Document(raw, signature, keys)
	if err != nil {
		return d, err
	}
	if !validFields(obj) {
		return d, errors.New("invalid signed release fields")
	}
	dec := json.NewDecoder(bytes.NewReader(raw))
	dec.DisallowUnknownFields()
	if err = dec.Decode(&d.Release); err != nil {
		return d, err
	}
	if d.Format != 2 || d.Seq < 1 || d.Seq > maxSeq || !versionRE.MatchString(d.Version) || d.MinBridge < 1 || d.MinBridge > maxSeq || len(d.Targets) == 0 {
		return d, errors.New("invalid release header")
	}
	for p, t := range d.Targets {
		if !platformRE.MatchString(p) || t.Name != binaryName(p) || !assetURL(t.URL) || t.Size <= 0 || t.Size > maxBinary || !hashRE.MatchString(t.SHA256) {
			return d, fmt.Errorf("invalid target %q", p)
		}
	}
	if d.Compat != nil {
		if len(d.Compat) != 2 {
			return d, errors.New("invalid compatibility file set")
		}
		for _, path := range []string{"skynet_agent/__init__.py", "skynet_agent/cli.py"} {
			f, ok := d.Compat[path]
			meta, _ := obj["compat_files"].(map[string]any)[path].(map[string]any)
			if !ok || len(meta) != 2 || !matches(adapters[path], f) {
				return d, errors.New("invalid compatibility file")
			}
		}
	}
	if _, exists := obj["halt"]; exists {
		h, ok := obj["halt"].(map[string]any)
		if !ok || h["through_seq"] == nil || d.Halt == nil || d.Halt.Through < 0 || d.Halt.Through > maxSeq || utf8.RuneCountInString(d.Halt.Reason) > 500 {
			return d, errors.New("invalid halt")
		}
	}
	d.raw, d.signature = raw, signature
	return d, nil
}
