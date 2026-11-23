// Package records constructs and validates signed network records.
package records

import (
	"crypto/ed25519"
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"fmt"
	"math/big"
	"strings"
	"time"
	"unicode"
	"unicode/utf8"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/sig"
)

type Object = canon.Object
const Network = "skynet-architecture/core-v1"
const MaxWire = 40000
const maxTime = 1 << 40
var ErrFuture = errors.New("record dated in the future")

func Wire(record Object) ([]byte, error) {
	return canon.Marshal(record, false)
}

func ID(body Object) (string, error) {
	raw, err := canon.Marshal(body, true)
	if err != nil {
		return "", err
	}
	sum := sha256.Sum256(append([]byte("skynet-record:1\n"), raw...))
	return hex.EncodeToString(sum[:]), nil
}

func Make(seed []byte, kind string, payload Object, created int64) (Object, error) {
	if len(seed) != 32 {
		return nil, errors.New("invalid seed length")
	}
	// Freeze the caller's data and normalize typed Go slices to JSON arrays.
	raw, err := canon.Marshal(payload, false)
	if err != nil || len(raw) > MaxWire {
		return nil, errors.New("invalid or oversized payload")
	}
	value, err := canon.Parse(raw)
	if err != nil {
		return nil, err
	}
	payload = value.(Object)
	key := ed25519.NewKeyFromSeed(seed)
	body := Object{"v": 1, "net": Network, "type": kind, "created": created, "payload": payload,
		"author": hex.EncodeToString(key.Public().(ed25519.PublicKey))}
	id, err := ID(body)
	if err != nil {
		return nil, err
	}
	data, _ := hex.DecodeString(id)
	record := Object{"body": body, "id": id, "sig": hex.EncodeToString(ed25519.Sign(key, data))}
	if err := Verify(record, time.Now().Unix()); err != nil {
		return nil, err
	}
	return record, nil
}

func only(obj Object, fields string) bool {
	for k := range obj {
		if k == "" || strings.Contains(k, " ") || !strings.Contains(" " + fields + " ", " " + k + " ") {
			return false
		}
	}
	return true
}

func hexField(value any, size int) []byte {
	s, ok := value.(string)
	if !ok || len(s) != size * 2 || strings.ToLower(s) != s {
		return nil
	}
	b, err := hex.DecodeString(s)
	if err != nil {
		return nil
	}
	return b
}

func within(v any, lo, hi int64) bool {
	n, ok := canon.Int64(v)
	return ok && lo <= n && n <= hi
}

func textOK(p Object, key string, limit int, optional bool) bool {
	if optional && p[key] == nil {
		return true
	}
	s, ok := p[key].(string)
	return ok && utf8.RuneCountInString(s) <= limit && strings.TrimFunc(s, func(r rune) bool {
		return unicode.IsSpace(r) || (r >= 28 && r <= 31)
	}) != ""
}

func ref(p Object, key string, optional bool) bool {
	return (optional && p[key] == nil) || hexField(p[key], 32) != nil
}

func integer(v any) bool {
	if n, ok := v.(*big.Int); ok {
		return n != nil
	}
	_, ok := canon.Int64(v)
	return ok
}

func resultOK(p Object) bool {
	rec, ok := p["record"].(Object)
	if !ok || !only(p, "record text") {
		return false
	}
	// The legacy inner format compares v numerically with Python's 1.
	if !within(rec["v"], 1, 1) && rec["v"] != true && rec["v"] != 1.0 {
		return false
	}
	for _, k := range []string{"agent", "task", "kernel", "result_sha256"} {
		if _, ok := rec[k].(string); !ok {
			return false
		}
	}
	result, ok := rec["result"].(Object)
	if !ok || !integer(rec["unit"]) || !integer(rec["units"]) {
		return false
	}
	hash, err := canon.Hash(result)
	if err != nil || hash != rec["result_sha256"] {
		return false
	}
	want, exists := result["output_sha256"]
	if !exists {
		return p["text"] == nil
	}
	s, ok := p["text"].(string)
	return ok && want == fmt.Sprintf("%x", sha256.Sum256([]byte(s)))
}

func taskOK(p Object) bool {
	if !only(p, "title text accept base parent deputies handover_days lang") ||
		!textOK(p, "title", 200, false) || !textOK(p, "text", 20000, false) || !textOK(p, "accept", 4000, false) ||
		!textOK(p, "base", 200, true) || !textOK(p, "lang", 16, true) || !ref(p, "parent", true) {
		return false
	}
	if days, exists := p["handover_days"]; exists && !within(days, 1, 365) {
		return false
	}
	v, exists := p["deputies"]
	if !exists {
		return true
	}
	deputies, ok := v.([]any)
	if !ok || len(deputies) > 5 {
		return false
	}
	seen := map[string]bool{}
	for _, value := range deputies {
		pub := hexField(value, 32)
		if !sig.IsStrongPublic(pub) || seen[string(pub)] {
			return false
		}
		seen[string(pub)] = true
	}
	return true
}

func payloadOK(kind string, p Object) bool {
	switch kind {
	case "task":
		return taskOK(p)
	case "result":
		return resultOK(p)
	case "claim":
		return only(p, "task until") && ref(p, "task", false) && within(p["until"], 1, maxTime - 1)
	case "report":
		return only(p, "task summary text revises") && ref(p, "task", false) && ref(p, "revises", true) &&
			textOK(p, "summary", 2000, false) && textOK(p, "text", 30000, false)
	case "accept", "revise":
		return only(p, "task report note") && ref(p, "task", false) && ref(p, "report", false) && textOK(p, "note", 4000, true)
	}
	return false
}

func Verify(record Object, now int64) error {
	body, ok := record["body"].(Object)
	if !ok || len(record) != 3 || !only(record, "id sig body") || len(body) != 6 ||
		!only(body, "v net type author created payload") || body["net"] != Network || !within(body["v"], 1, 1) {
		return errors.New("invalid record envelope, version or network")
	}
	p, ok := body["payload"].(Object)
	kind, _ := body["type"].(string)
	if !ok || !within(body["created"], 1, maxTime - 1) {
		return errors.New("invalid record fields")
	}
	key, id, signature := hexField(body["author"], 32), hexField(record["id"], 32), hexField(record["sig"], 64)
	if key == nil || id == nil || signature == nil {
		return errors.New("invalid key, id or signature field")
	}
	raw, err := Wire(record)
	if err != nil || len(raw) > MaxWire {
		return errors.New("invalid record wire encoding or size")
	}
	want, err := ID(body)
	if err != nil || record["id"] != want {
		return errors.New("record id mismatch")
	}
	if !payloadOK(kind, p) {
		return errors.New("invalid record payload")
	}
	if !sig.IsStrongPublic(key) || !sig.Verify(key, id, signature) {
		return errors.New("invalid record signature or author")
	}
	created, _ := canon.Int64(body["created"])
	if created - 86400 > now {
		return ErrFuture
	}
	return nil
}

func Parse(raw []byte, now int64) (Object, error) {
	if len(raw) > MaxWire + 1024 {
		return nil, errors.New("record input too large")
	}
	v, err := canon.Parse(raw)
	if err != nil {
		return nil, err
	}
	record, ok := v.(Object)
	if !ok {
		return nil, errors.New("expected record object")
	}
	if err := Verify(record, now); err != nil {
		return nil, err
	}
	return record, nil
}
