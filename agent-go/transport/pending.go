package transport

import (
	"context"
	"errors"
	"os"
	"path/filepath"
	"strings"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/records"
)

func (n Network) retry(ctx context.Context, s *Store, seed []byte, env Object, path string) (bool, string, error) {
	if _, err := s.Add(env); err != nil {
		return false, "", err
	}
	ok, msg := n.Send(ctx, env, seed)
	if ok {
		return true, msg, os.Remove(path)
	}
	return false, msg, nil
}
func (n Network) Publish(ctx context.Context, s *Store, seed []byte, kind string, p Object) (Object, bool, string, error) {
	env, err := records.Make(seed, kind, p, time.Now().Unix())
	if err != nil {
		return nil, false, "", err
	}
	path := filepath.Join(s.Dir, "pending", config.Str(env["id"])+".json")
	if err = config.Write(path, env); err != nil {
		return nil, false, "", err
	}
	ok, msg, err := n.retry(ctx, s, seed, env, path)
	return env, ok, msg, err
}
func (n Network) Retry(ctx context.Context, s *Store, seed []byte) (int, error) {
	dir := filepath.Join(s.Dir, "pending")
	files, err := os.ReadDir(dir)
	if errors.Is(err, os.ErrNotExist) {
		return 0, nil
	}
	if err != nil {
		return 0, err
	}
	count := 0
	attempts := 0
	for _, f := range files {
		if attempts >= 200 {
			break
		}
		if !f.Type().IsRegular() || !strings.HasSuffix(f.Name(), ".json") {
			continue
		}
		path := filepath.Join(dir, f.Name())
		env, err := config.Read(path)
		if err != nil || records.Verify(env, time.Now().Unix()) != nil || f.Name() != config.Str(env["id"])+".json" {
			// Broken entries stay untouched for inspection, but must not
			// consume the retry budget and starve the rest of the queue.
			continue
		}
		attempts++
		ok, _, err := n.retry(ctx, s, seed, env, path)
		if err != nil {
			return count, err
		}
		if ok {
			count++
		}
	}
	return count, nil
}
