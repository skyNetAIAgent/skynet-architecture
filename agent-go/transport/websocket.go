package transport

import (
	"bytes"
	"context"
	"crypto/rand"
	"crypto/sha1"
	"crypto/tls"
	"encoding/base64"
	"encoding/binary"
	"errors"
	"io"
	"net/http"
	"net/url"
	"strings"
	"time"
	"unicode/utf8"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
)

const wsLimit = 256 << 10
const magic = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

type socket struct {
	io.ReadWriteCloser
	cancel context.CancelFunc
	stop   func() bool
}

func (n Network) connect(ctx context.Context, address string) (*socket, error) {
	u, err := url.Parse(address)
	if err != nil {
		return nil, err
	}
	switch u.Scheme {
	case "ws":
		u.Scheme = "http"
	case "wss":
		u.Scheme = "https"
	default:
		return nil, errors.New("expected WebSocket URL")
	}
	if err = checkURL(u); err != nil {
		return nil, err
	}
	ctx, cancel := context.WithTimeout(ctx, 15*time.Second)
	ready := false
	defer func() {
		if !ready {
			cancel()
		}
	}()
	req, err := http.NewRequestWithContext(ctx, "GET", u.String(), nil)
	if err != nil {
		return nil, err
	}
	var nonce [16]byte
	if _, err = rand.Read(nonce[:]); err != nil {
		return nil, err
	}
	key := base64.StdEncoding.EncodeToString(nonce[:])
	req.Header.Set("Connection", "Upgrade")
	req.Header.Set("Upgrade", "websocket")
	req.Header.Set("Sec-WebSocket-Version", "13")
	req.Header.Set("Sec-WebSocket-Key", key)
	tr := n.HTTP
	if tr == nil {
		tr = http.DefaultTransport
	}
	// RFC 6455 upgrades require HTTP/1.1 even when the relay offers HTTP/2.
	if base, ok := tr.(*http.Transport); ok {
		h1 := base.Clone()
		h1.ForceAttemptHTTP2 = false
		h1.TLSNextProto = map[string]func(string, *tls.Conn) http.RoundTripper{}
		if h1.TLSClientConfig == nil {
			h1.TLSClientConfig = &tls.Config{}
		}
		h1.TLSClientConfig.NextProtos = []string{"http/1.1"}
		defer h1.CloseIdleConnections()
		tr = h1
	}
	resp, err := tr.RoundTrip(req)
	if err != nil {
		return nil, err
	}
	sum := sha1.Sum([]byte(key + magic))
	stream, ok := resp.Body.(io.ReadWriteCloser)
	if !ok || resp.StatusCode != 101 || !strings.EqualFold(resp.Header.Get("Upgrade"), "websocket") ||
		!hasToken(resp.Header.Values("Connection"), "upgrade") || resp.Header.Get("Sec-WebSocket-Accept") != base64.StdEncoding.EncodeToString(sum[:]) || resp.Header.Get("Sec-WebSocket-Extensions") != "" {
		resp.Body.Close()
		return nil, errors.New("invalid WebSocket upgrade")
	}
	ready = true
	return &socket{stream, cancel, context.AfterFunc(ctx, func() { stream.Close() })}, nil
}
func hasToken(fields []string, token string) bool {
	for _, field := range fields {
		for _, v := range strings.Split(field, ",") {
			if strings.EqualFold(strings.TrimSpace(v), token) {
				return true
			}
		}
	}
	return false
}
func (s *socket) close() { s.frame(8, nil); s.stop(); s.cancel(); s.Close() }
func (s *socket) frame(op byte, p []byte) error {
	if len(p) > wsLimit {
		return errors.New("frame too large")
	}
	h := []byte{0x80 | op}
	switch {
	case len(p) < 126:
		h = append(h, 0x80|byte(len(p)))
	case len(p) <= 65535:
		h = binary.BigEndian.AppendUint16(append(h, 0xfe), uint16(len(p)))
	default:
		h = binary.BigEndian.AppendUint64(append(h, 0xff), uint64(len(p)))
	}
	var mask [4]byte
	if _, err := rand.Read(mask[:]); err != nil {
		return err
	}
	h = append(h, mask[:]...)
	for i, b := range p {
		h = append(h, b^mask[i%4])
	}
	_, err := s.Write(h)
	return err
}
func (s *socket) send(v []any) error {
	b, err := canon.Marshal(v, false)
	if err != nil {
		return err
	}
	return s.frame(1, b)
}
func (s *socket) recv() ([]any, error) {
	var msg bytes.Buffer
	started := false
	for frames := 0; frames < 4096; frames++ {
		var h [2]byte
		if _, err := io.ReadFull(s, h[:]); err != nil {
			return nil, err
		}
		op := h[0] & 15
		fin := h[0]&128 != 0
		if h[0]&0x70 != 0 || h[1]&128 != 0 {
			return nil, errors.New("invalid server frame")
		}
		size := uint64(h[1])
		switch size {
		case 126:
			var n uint16
			if err := binary.Read(s, binary.BigEndian, &n); err != nil {
				return nil, err
			}
			if n < 126 {
				return nil, errors.New("invalid length")
			}
			size = uint64(n)
		case 127:
			if err := binary.Read(s, binary.BigEndian, &size); err != nil {
				return nil, err
			}
			if size <= 65535 {
				return nil, errors.New("invalid length")
			}
		}
		if op >= 8 && (!fin || size > 125) || size > wsLimit || op < 8 && size > uint64(wsLimit-msg.Len()) {
			return nil, errors.New("invalid frame size")
		}
		data := make([]byte, int(size))
		if _, err := io.ReadFull(s, data); err != nil {
			return nil, err
		}
		switch op {
		case 8:
			return nil, io.EOF
		case 9:
			if err := s.frame(10, data); err != nil {
				return nil, err
			}
			continue
		case 10:
			continue
		case 1:
			if started {
				return nil, errors.New("unexpected text frame")
			}
			started = true
		case 0:
			if !started {
				return nil, errors.New("unexpected continuation")
			}
		default:
			return nil, errors.New("unsupported opcode")
		}
		msg.Write(data)
		if fin {
			if !utf8.Valid(msg.Bytes()) {
				return nil, errors.New("invalid text")
			}
			v, err := canon.Parse(msg.Bytes())
			a, ok := v.([]any)
			if err != nil || !ok {
				return nil, errors.New("invalid relay message")
			}
			return a, nil
		}
	}
	return nil, errors.New("too many frames")
}
