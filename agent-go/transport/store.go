package transport

import (
	"bufio"
	"bytes"
	"errors"
	"io"
	"os"
	"path/filepath"
	"time"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/config"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/records"
)

const MaxStore = 256 << 20

var ErrFull = errors.New("local record store full")

// Store holds the journal lock until Close. One caller owns its cursors and pending files.
type Store struct {
	Dir         string
	Items       map[string]Object
	Ordered     []Object
	limit, size int64
	file, lock  *os.File
}

func Open(home string) (*Store, error) {
	dir := filepath.Join(home, "net")
	lock, err := config.Lock(filepath.Join(dir, "store.lock"))
	if err != nil {
		return nil, err
	}
	f, err := os.OpenFile(filepath.Join(dir, "records.jsonl"), os.O_CREATE|os.O_RDWR, 0600)
	if err != nil {
		lock.Close()
		return nil, err
	}
	s := &Store{Dir: dir, file: f, lock: lock, limit: MaxStore, Items: map[string]Object{}}
	r := bufio.NewReaderSize(f, records.MaxWire+1025)
	var pos int64
	oversize := false
	for {
		line, err := r.ReadSlice('\n')
		pos += int64(len(line))
		if errors.Is(err, bufio.ErrBufferFull) {
			oversize = true
			continue
		}
		if errors.Is(err, io.EOF) {
			if pos != s.size {
				err = f.Truncate(s.size)
				if err != nil {
					s.Close()
					return nil, err
				}
			}
			break
		}
		if err != nil {
			s.Close()
			return nil, err
		}
		if !oversize {
			if env, err := records.Parse(bytes.TrimSuffix(line, []byte{'\n'}), 1<<40); err == nil {
				s.remember(env)
			}
		}
		s.size = pos
		oversize = false
	}
	_, err = f.Seek(s.size, io.SeekStart)
	if err != nil {
		s.Close()
		return nil, err
	}
	return s, nil
}
func (s *Store) remember(env Object) {
	id := env["id"].(string)
	if s.Items[id] == nil {
		s.Items[id] = env
		s.Ordered = append(s.Ordered, env)
	}
}
func (s *Store) Close() { s.file.Close(); s.lock.Close() }
func (s *Store) Add(env Object) (bool, error) {
	if err := records.Verify(env, time.Now().Unix()); err != nil {
		return false, err
	}
	if s.Items[env["id"].(string)] != nil {
		return false, nil
	}
	raw, err := records.Wire(env)
	if err != nil {
		return false, err
	}
	raw = append(raw, '\n')
	if s.size+int64(len(raw)) > s.limit {
		return false, ErrFull
	}
	if _, err = s.file.Write(raw); err == nil {
		err = s.file.Sync()
	}
	if err != nil {
		s.file.Truncate(s.size)
		s.file.Seek(s.size, io.SeekStart)
		return false, err
	}
	s.size += int64(len(raw))
	s.remember(env)
	return true, nil
}
