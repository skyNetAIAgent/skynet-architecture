// Package sig verifies signed documents against explicitly trusted keys.
package sig

import (
	"bytes"
	"crypto/ed25519"
	"encoding/hex"
	"errors"
	"fmt"
	"math/big"
	"strings"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
)

const ReleaseKey = "33deadd767eddfb05d5646caa1b32727a73e261a071d8d4ca8530b7355d2ded9"

var prime = new(big.Int).Sub(new(big.Int).Lsh(big.NewInt(1), 255), big.NewInt(19))
var curveD = new(big.Int).Mod(new(big.Int).Mul(big.NewInt(-121665),
	new(big.Int).ModInverse(big.NewInt(121666), prime)), prime)
// Ed25519 group order l = 2^252 + 27742317777372353535851937790883648493.
var groupOrder, _ = new(big.Int).SetString("7237005577332262213973186563042994240857116359379907606001950938285454250989", 10)

// Decode y and test whether x exists. doubling gives y'=(y²+x²)/(1-d*x²*y²).
// The torsion subgroup has order eight: x=0, y=0 or y'=0 identifies all eight points.
func point(encoded []byte) (canonical, strong bool) {
	if len(encoded) != 32 {
		return false, false
	}
	var be [32]byte
	for i, v := range encoded {
		be[31 - i] = v
	}
	sign := be[0] >> 7
	be[0] &= 127
	y := new(big.Int).SetBytes(be[:])
	if y.Cmp(prime) >= 0 {
		return false, false
	}
	yy := new(big.Int).Mul(y, y)
	den := new(big.Int).Mul(curveD, yy)
	den.Add(den, big.NewInt(1))
	if den.ModInverse(den, prime) == nil {
		return false, false
	}
	xx := new(big.Int).Sub(yy, big.NewInt(1))
	xx.Mod(xx.Mul(xx, den), prime)
	if xx.Sign() == 0 {
		return sign == 0, false
	}
	if big.Jacobi(xx, prime) != 1 {
		return false, false
	}
	sum := new(big.Int).Add(xx, yy)
	return true, y.Sign() != 0 && sum.Mod(sum, prime).Sign() != 0
}

func IsStrongPublic(key []byte) bool {
	_, strong := point(key)
	return strong
}

func Verify(key, data, signature []byte) bool {
	if len(signature) != ed25519.SignatureSize {
		return false
	}
	a, _ := point(key)
	r, _ := point(signature[:32])
	// Python ed25519.verify rejects S >= l. RFC 8032 requires the same.
	// Check it explicitly so that acceptance does not depend on whether
	// crypto/ed25519 internally reduces S modulo l.
	var le [32]byte // S is little-endian
	for i, v := range signature[32:] {
		le[31-i] = v
	}
	s := new(big.Int).SetBytes(le[:])
	if s.Cmp(groupOrder) >= 0 {
		return false
	}
	return a && r && ed25519.Verify(key, data, signature)
}

func FormatLine(key, signature []byte) string {
	return fmt.Sprintf("ed25519:%x:%x\n", key, signature)
}

type Entry struct { Public, Signature []byte }

// Python bytes.fromhex permits ASCII whitespace between full bytes.
func fromHex(s string) ([]byte, bool) {
	var out []byte
	for _, word := range strings.Fields(s) {
		b, err := hex.DecodeString(word)
		if err != nil {
			return nil, false
		}
		out = append(out, b...)
	}
	return out, true
}

func ParseLines(raw []byte) []Entry {
	for _, c := range raw {
		if c > 127 {
			return nil
		}
	}
	var out []Entry
	lines := bytes.FieldsFunc(raw, func(c rune) bool {
		return c == '\n' || c == '\r' || c == '\v' || c == '\f' || (c >= 28 && c <= 30)
	})
	for _, line := range lines {
		parts := strings.Split(strings.TrimSpace(string(line)), ":")
		if len(parts) != 3 || parts[0] != "ed25519" {
			continue
		}
		key, ok := fromHex(parts[1])
		s, valid := fromHex(parts[2])
		if ok && valid && len(key) == 32 && len(s) == 64 {
			out = append(out, Entry{key, s})
		}
	}
	return out
}

// A nil key list selects the release key. An explicitly empty list trusts nobody.
func VerifyDetached(data, lines []byte, keys []string) (string, error) {
	if keys == nil {
		keys = []string{ReleaseKey}
	}
	for _, entry := range ParseLines(lines) {
		pub := hex.EncodeToString(entry.Public)
		for _, k := range keys {
			if strings.EqualFold(pub, k) && Verify(entry.Public, data, entry.Signature) {
				return pub, nil
			}
		}
	}
	return "", errors.New("no valid signature from a trusted key")
}

func Document(raw, lines []byte, keys []string) (canon.Object, error) {
	if _, err := VerifyDetached(raw, lines, keys); err != nil {
		return nil, err
	}
	value, err := canon.Parse(raw)
	if err != nil {
		return nil, err
	}
	obj, ok := value.(canon.Object)
	if !ok {
		return nil, errors.New("expected a signed JSON object")
	}
	return obj, nil
}
