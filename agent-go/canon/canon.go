// Package canon implements the two compact JSON encodings used by the agent.
package canon

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"math"
	"math/big"
	"reflect"
	"sort"
	"strconv"
	"strings"
	"unicode/utf8"
)

type Object = map[string]any

// Parse preserves integer precision and rejects ambiguous object and string encodings.
func Parse(raw []byte) (any, error) {
	if !utf8.Valid(raw) || !validEscapes(raw) {
		return nil, errors.New("invalid Unicode in JSON")
	}
	d := json.NewDecoder(bytes.NewReader(raw))
	d.UseNumber()
	v, err := read(d, 0)
	if err != nil {
		return nil, err
	}
	if _, err := d.Token(); err != io.EOF {
		return nil, errors.New("trailing JSON data")
	}
	return v, nil
}

// encoding/json replaces unpaired surrogates with U+FFFD. Check them before decoding.
func validEscapes(raw []byte) bool {
	for i := 0; i < len(raw); i++ {
		if raw[i] != '\\' {
			continue
		}
		i++
		if i >= len(raw) || raw[i] != 'u' {
			continue
		}
		if i + 4 >= len(raw) {
			return false
		}
		r, err := strconv.ParseUint(string(raw[i + 1:i + 5]), 16, 16)
		if err != nil {
			return false
		}
		i += 4
		if r >= 0xdc00 && r <= 0xdfff {
			return false
		}
		if r < 0xd800 || r > 0xdbff {
			continue
		}
		if i + 6 >= len(raw) || string(raw[i + 1:i + 3]) != "\\u" {
			return false
		}
		low, err := strconv.ParseUint(string(raw[i + 3:i + 7]), 16, 16)
		if err != nil || low < 0xdc00 || low > 0xdfff {
			return false
		}
		i += 6
	}
	return true
}

func read(d *json.Decoder, depth int) (any, error) {
	if depth > 1000 {
		return nil, errors.New("JSON nesting limit")
	}
	token, err := d.Token()
	if err != nil {
		return nil, err
	}
	switch t := token.(type) {
	case json.Number:
		s := string(t)
		if strings.ContainsAny(s, ".eE") {
			f, err := strconv.ParseFloat(s, 64)
			if err != nil {
				// Python json.loads accepts underflowing literals ("-1e-500"
				// -> -0.0, "1e-320" -> nearest subnormal) and rejects only
				// via the canonical encoder for non-finite results. Accept
				// finite results that merely underflowed so that parsing
				// matches Python byte for byte; overflow still yields Inf
				// and is rejected here (Python rejects it when encoding).
				if num, ok := err.(*strconv.NumError); !ok || num.Err != strconv.ErrRange ||
					math.IsInf(f, 0) || math.IsNaN(f) {
					return nil, errors.New("invalid float")
				}
			}
			if math.IsInf(f, 0) {
				return nil, errors.New("invalid float")
			}
			return f, nil
		}
		if n, err := t.Int64(); err == nil {
			return n, nil
		}
		n, ok := new(big.Int).SetString(s, 10)
		if !ok {
			return nil, errors.New("invalid integer")
		}
		return n, nil
	case json.Delim:
		switch t {
		case '{':
			obj := Object{}
			for d.More() {
				k, err := d.Token()
				if err != nil {
					return nil, err
				}
				key, ok := k.(string)
				if !ok {
					return nil, errors.New("expected object key")
				}
				if _, seen := obj[key]; seen {
					return nil, fmt.Errorf("duplicate key %q", key)
				}
				obj[key], err = read(d, depth + 1)
				if err != nil {
					return nil, err
				}
			}
			_, err := d.Token()
			return obj, err
		case '[':
			a := []any{}
			for d.More() {
				v, err := read(d, depth + 1)
				if err != nil {
					return nil, err
				}
				a = append(a, v)
			}
			_, err := d.Token()
			return a, err
		}
		return nil, errors.New("unexpected delimiter")
	default:
		return t, nil
	}
}

func Int64(v any) (int64, bool) {
	switch n := v.(type) {
	case int:
		return int64(n), true
	case int64:
		return n, true
	case *big.Int:
		if n != nil && n.IsInt64() {
			return n.Int64(), true
		}
	}
	return 0, false
}

func quoted(b *bytes.Buffer, s string, ascii bool) error {
	if !utf8.ValidString(s) {
		return errors.New("invalid UTF-8")
	}
	b.WriteByte('"')
	for _, r := range s {
		switch r {
		case '"', '\\':
			b.WriteByte('\\')
			b.WriteRune(r)
		case '\b':
			b.WriteString("\\b")
		case '\f':
			b.WriteString("\\f")
		case '\n':
			b.WriteString("\\n")
		case '\r':
			b.WriteString("\\r")
		case '\t':
			b.WriteString("\\t")
		default:
			switch {
			case ascii && r > 0xffff:
				n := r - 0x10000
				fmt.Fprintf(b, "\\u%04x\\u%04x", 0xd800 + n / 1024, 0xdc00 + n % 1024)
			case r < 32 || (ascii && r >= 127):
				fmt.Fprintf(b, "\\u%04x", r)
			default:
				b.WriteRune(r)
			}
		}
	}
	b.WriteByte('"')
	return nil
}

func floatRepr(f float64) (string, error) {
	if math.IsNaN(f) || math.IsInf(f, 0) {
		return "", errors.New("non-finite float")
	}
	s := strconv.FormatFloat(f, 'e', -1, 64)
	exp, _ := strconv.Atoi(s[strings.IndexByte(s, 'e') + 1:])
	if exp < -4 || exp >= 16 {
		return s, nil
	}
	s = strconv.FormatFloat(f, 'f', -1, 64)
	if !strings.Contains(s, ".") {
		s += ".0"
	}
	return s, nil
}

func encode(b *bytes.Buffer, v any, ascii bool, depth int) error {
	if depth > 1000 {
		return errors.New("JSON nesting limit")
	}
	switch x := v.(type) {
	case nil:
		b.WriteString("null")
	case bool:
		b.WriteString(strconv.FormatBool(x))
	case string:
		return quoted(b, x, ascii)
	case float64:
		s, err := floatRepr(x)
		if err != nil {
			return err
		}
		b.WriteString(s)
	case *big.Int:
		if x == nil {
			return errors.New("nil integer")
		}
		b.WriteString(x.String())
	case Object:
		keys := make([]string, 0, len(x))
		for k := range x {
			keys = append(keys, k)
		}
		sort.Strings(keys) // Valid UTF-8 sorts in code point order.
		b.WriteByte('{')
		for i, k := range keys {
			if i > 0 {
				b.WriteByte(',')
			}
			if err := quoted(b, k, ascii); err != nil {
				return err
			}
			b.WriteByte(':')
			if err := encode(b, x[k], ascii, depth + 1); err != nil {
				return err
			}
		}
		b.WriteByte('}')
	default:
		r := reflect.ValueOf(v)
		switch r.Kind() {
		case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
			b.WriteString(strconv.FormatInt(r.Int(), 10))
		case reflect.Uint, reflect.Uint8, reflect.Uint16, reflect.Uint32, reflect.Uint64:
			b.WriteString(strconv.FormatUint(r.Uint(), 10))
		case reflect.Array, reflect.Slice:
			b.WriteByte('[')
			for i := 0; i < r.Len(); i++ {
				if i > 0 {
					b.WriteByte(',')
				}
				if err := encode(b, r.Index(i).Interface(), ascii, depth + 1); err != nil {
					return err
				}
			}
			b.WriteByte(']')
		default:
			return fmt.Errorf("unsupported JSON type %T", v)
		}
	}
	return nil
}

func Marshal(v any, ascii bool) ([]byte, error) {
	var b bytes.Buffer
	if err := encode(&b, v, ascii, 0); err != nil {
		return nil, err
	}
	return b.Bytes(), nil
}

func Hash(v any) (string, error) {
	b, err := Marshal(v, true)
	if err != nil {
		return "", err
	}
	h := sha256.Sum256(b)
	return hex.EncodeToString(h[:]), nil
}
