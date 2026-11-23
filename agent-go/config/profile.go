// Package config manages the shared Python and Go agent profile.
package config

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"reflect"
	"runtime"
	"slices"
	"strconv"
	"strings"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
)

type Object = canon.Object

// The CLI replaces these development defaults with the linked release metadata at startup.
var Version = "0.3.0"
var Sequence int64 = 5

func Home() (string, error) {
	if p := os.Getenv("SKYNET_AGENT_HOME"); p != "" {
		return filepath.Abs(p)
	}
	if runtime.GOOS == "windows" && os.Getenv("LOCALAPPDATA") != "" {
		return filepath.Join(os.Getenv("LOCALAPPDATA"), "SkyNetAgent"), nil
	}
	if runtime.GOOS != "windows" && runtime.GOOS != "darwin" && os.Getenv("XDG_DATA_HOME") != "" {
		return filepath.Join(os.Getenv("XDG_DATA_HOME"), "skynet-agent"), nil
	}
	user, err := os.UserHomeDir()
	if err != nil {
		return "", err
	}
	switch runtime.GOOS {
	case "windows":
		return filepath.Join(user, "AppData", "Local", "SkyNetAgent"), nil
	case "darwin":
		return filepath.Join(user, "Library", "Application Support", "SkyNetAgent"), nil
	}
	return filepath.Join(user, ".local", "share", "skynet-agent"), nil
}

func Defaults() Object {
	return Object{
		"workers": 1, "poll_minutes": 30, "update": "auto", "submit": "auto", "submit_via": "net",
		"run_on_battery": false, "paused": false, "max_task_minutes": 120, "batch_minutes": 60,
		"max_submissions_per_day": 48, "report_platform": true,
		"ai": Object{"enabled": false, "endpoint": "", "model": "", "allow_remote": false, "review_before_submit": true, "timeout_minutes": 30},
	}
}
func defaultState() Object {
	return Object{
		"done": Object{}, "skip": Object{}, "fails": Object{}, "index_seq": 0, "submitted": []any{}, "last_post": Object{},
		"publish_fails": 0, "publish_after": 0, "counters": Object{"units_done": 0, "units_failed": 0, "published": 0},
		"last_error": "", "last_poll": 0, "poll_error": "", "poll_failures": 0, "retry_at": 0, "halt": "", "halt_seq": 0,
	}
}

func Obj(v any) Object { o, _ := v.(Object); return o }
func Str(v any) string { s, _ := v.(string); return s }
func Num(v any, fallback int64) int64 {
	if n, ok := canon.Int64(v); ok {
		return n
	}
	return fallback
}
func Read(path string) (Object, error) {
	b, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	v, err := canon.Parse(b)
	if err != nil {
		return nil, fmt.Errorf("%s: %w", path, err)
	}
	if o := Obj(v); o != nil {
		return o, nil
	}
	return nil, fmt.Errorf("%s: expected JSON object", path)
}

// Write preserves distinctions such as 0 and 0.0 in signed objects.
func Write(path string, o Object) error {
	raw, err := canon.Marshal(o, false)
	if err != nil {
		return err
	}
	var data bytes.Buffer
	if err = json.Indent(&data, raw, "", "  "); err != nil {
		return err
	}
	data.WriteByte('\n')
	dir := filepath.Dir(path)
	if err = os.MkdirAll(dir, 0700); err != nil {
		return err
	}
	f, err := os.CreateTemp(dir, ".tmp-*")
	if err != nil {
		return err
	}
	defer os.Remove(f.Name())
	if _, err = f.Write(data.Bytes()); err == nil {
		err = f.Sync()
	}
	ce := f.Close()
	if err != nil {
		return err
	}
	if ce != nil {
		return ce
	}
	return os.Rename(f.Name(), path)
}

func merge(stored, defaults Object) Object {
	if stored == nil {
		stored = Object{}
	}
	for k, d := range defaults {
		v := stored[k]
		switch t := d.(type) {
		case Object:
			stored[k] = merge(Obj(v), t)
		case int:
			stored[k] = Num(v, int64(t))
		default:
			if reflect.TypeOf(v) != reflect.TypeOf(d) {
				stored[k] = d
			}
		}
	}
	return stored
}
func load(home, name string, d Object) (Object, error) {
	o, err := Read(filepath.Join(home, name))
	if err != nil && !errors.Is(err, os.ErrNotExist) {
		return nil, err
	}
	return merge(o, d), nil
}
func State(home string) (Object, error) { return load(home, "state.json", defaultState()) }

var limits = map[string][2]int64{"workers": {1, 256}, "poll_minutes": {5, 1440}, "max_task_minutes": {1, 1440}, "batch_minutes": {0, 1440}, "max_submissions_per_day": {0, 500}, "ai.timeout_minutes": {1, 240}}
var choices = map[string][]string{"update": {"auto", "notify", "off"}, "submit": {"auto", "manual"}, "submit_via": {"net", "github"}}

func field(o Object, key string) (Object, string) {
	if p, k, ok := strings.Cut(key, "."); ok {
		return Obj(o[p]), k
	}
	return o, key
}
func Get(o Object, key string) any { p, k := field(o, key); return p[k] }
func Load(home string) (Object, error) {
	d := Defaults()
	o, err := load(home, "config.json", d)
	if err != nil {
		return nil, err
	}
	for key, r := range limits {
		p, k := field(o, key)
		p[k] = min(r[1], max(r[0], Num(p[k], 0)))
	}
	for k, allowed := range choices {
		if !slices.Contains(allowed, Str(o[k])) {
			o[k] = d[k]
		}
	}
	return o, nil
}
func Set(o Object, key, value string) error {
	value = strings.TrimSpace(value)
	p, k := field(o, key)
	var v any
	switch Get(Defaults(), key).(type) {
	case bool:
		switch strings.ToLower(value) {
		case "1", "true", "on", "yes":
			v = true
		case "0", "false", "off", "no":
			v = false
		default:
			return fmt.Errorf("%s takes true or false", key)
		}
	case int:
		n, err := strconv.ParseInt(value, 10, 64)
		r := limits[key]
		if err != nil || n < r[0] || n > r[1] {
			return fmt.Errorf("%s must be between %d and %d", key, r[0], r[1])
		}
		v = n
	case string:
		if a := choices[key]; a != nil && !slices.Contains(a, value) {
			return fmt.Errorf("%s must be one of %s", key, strings.Join(a, ", "))
		}
		v = value
	default:
		return fmt.Errorf("unknown setting: %s", key)
	}
	p[k] = v
	return nil
}
func Channel(cfg Object) string {
	if v := os.Getenv("SKYNET_AGENT_SUBMIT_VIA"); slices.Contains(choices["submit_via"], v) {
		return v
	}
	return Str(cfg["submit_via"])
}

var ErrLocked = errors.New("already locked by another process")

// Lock holds the first byte on Windows and the whole file on Unix until Close.
func Lock(path string) (*os.File, error) {
	if err := os.MkdirAll(filepath.Dir(path), 0700); err != nil {
		return nil, err
	}
	f, err := os.OpenFile(path, os.O_RDWR|os.O_CREATE, 0600)
	if err != nil {
		return nil, err
	}
	if err = tryLock(f); err != nil {
		f.Close()
		return nil, fmt.Errorf("cannot lock %s: %w", path, err)
	}
	return f, nil
}
