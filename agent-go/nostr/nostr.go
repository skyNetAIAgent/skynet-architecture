// Package nostr implements the offline BIP-340 envelope. Scalar arithmetic
// uses math/big and is not constant-time.
package nostr

import (
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"math/big"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
	"github.com/skyNetAIAgent/skynet-architecture/agent-go/records"
)

func hexInt(s string) *big.Int {
	n, _ := new(big.Int).SetString(s, 16)
	return n
}

var (
	p = hexInt("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F")
	order = hexInt("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141")
	generator = &point{
		hexInt("79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798"),
		hexInt("483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8"),
	}
)

type point struct { x, y *big.Int }

func field(x *big.Int) *big.Int {
	return x.Mod(x, p)
}

func fixed(n *big.Int) []byte {
	return n.FillBytes(make([]byte, 32))
}

func add(a, b *point) *point {
	if a == nil {
		return b
	}
	if b == nil {
		return a
	}
	var num, den big.Int
	if a.x.Cmp(b.x) == 0 {
		if a.y.Cmp(b.y) != 0 || a.y.Sign() == 0 {
			return nil
		}
		num.Mul(a.x, a.x)
		num.Mul(&num, big.NewInt(3))
		den.Lsh(a.y, 1)
	} else {
		num.Sub(b.y, a.y)
		den.Sub(b.x, a.x)
	}
	den.ModInverse(&den, p)
	slope := field(num.Mul(&num, &den))
	x := new(big.Int).Mul(slope, slope)
	field(x.Sub(x.Sub(x, a.x), b.x))
	y := new(big.Int).Sub(a.x, x)
	field(y.Sub(y.Mul(slope, y), a.y))
	return &point{x, y}
}

func multiply(a *point, k *big.Int) *point {
	var sum *point
	for i := 0; i < k.BitLen(); i++ {
		if k.Bit(i) != 0 {
			sum = add(sum, a)
		}
		a = add(a, a)
	}
	return sum
}

func tagged(tag string, parts ...[]byte) []byte {
	t := sha256.Sum256([]byte("BIP0340/" + tag))
	h := sha256.New()
	h.Write(t[:])
	h.Write(t[:])
	for _, part := range parts {
		h.Write(part)
	}
	return h.Sum(nil)
}

func scalar(hash []byte) *big.Int {
	k := new(big.Int).SetBytes(hash)
	return k.Mod(k, order)
}

func SecretFromSeed(seed []byte) ([]byte, error) {
	if len(seed) != 32 {
		return nil, errors.New("invalid identity seed")
	}
	sum := sha256.Sum256(append([]byte("skynet-nostr-key:1"), seed...))
	k := new(big.Int).SetBytes(sum[:])
	k.Mod(k, new(big.Int).Sub(order, big.NewInt(1)))
	return fixed(k.Add(k, big.NewInt(1))), nil
}

func keyPoint(secret []byte) (*big.Int, *point, error) {
	d := new(big.Int).SetBytes(secret)
	if len(secret) != 32 || d.Sign() == 0 || d.Cmp(order) >= 0 {
		return nil, nil, errors.New("invalid secret")
	}
	return d, multiply(generator, d), nil
}

func Public(secret []byte) ([]byte, error) {
	_, pub, err := keyPoint(secret)
	if err != nil {
		return nil, err
	}
	return fixed(pub.x), nil
}

func Sign(msg, secret, aux []byte) ([]byte, error) {
	d, pub, err := keyPoint(secret)
	if err != nil {
		return nil, err
	}
	if len(msg) != 32 {
		return nil, errors.New("invalid message length")
	}
	if aux == nil {
		aux = make([]byte, 32)
		if _, err := rand.Read(aux); err != nil {
			return nil, err
		}
	}
	if len(aux) != 32 {
		return nil, errors.New("invalid aux length")
	}
	if pub.y.Bit(0) != 0 {
		d.Sub(order, d)
	}
	t := tagged("aux", aux)
	for i, v := range fixed(d) {
		t[i] ^= v
	}
	pk := fixed(pub.x)
	k := scalar(tagged("nonce", t, pk, msg))
	if k.Sign() == 0 {
		return nil, errors.New("zero nonce")
	}
	r := multiply(generator, k)
	if r.y.Bit(0) != 0 {
		k.Sub(order, k)
	}
	rx := fixed(r.x)
	s := scalar(tagged("challenge", rx, pk, msg))
	s.Mod(s.Add(k, s.Mul(s, d)), order)
	sig := append(rx, fixed(s)...)
	if !Verify(msg, pk, sig) {
		return nil, errors.New("Schnorr self-check failed")
	}
	return sig, nil
}

func Verify(msg, public, sig []byte) bool {
	if len(msg) != 32 || len(public) != 32 || len(sig) != 64 {
		return false
	}
	x := new(big.Int).SetBytes(public)
	r := new(big.Int).SetBytes(sig[:32])
	s := new(big.Int).SetBytes(sig[32:])
	if x.Cmp(p) >= 0 || r.Cmp(p) >= 0 || s.Cmp(order) >= 0 {
		return false
	}
	y2 := new(big.Int).Exp(x, big.NewInt(3), p)
	y := new(big.Int).ModSqrt(field(y2.Add(y2, big.NewInt(7))), p)
	if y == nil {
		return false
	}
	if y.Bit(0) != 0 {
		y.Sub(p, y)
	}
	e := scalar(tagged("challenge", sig[:32], public, msg))
	check := add(multiply(generator, s), multiply(&point{x, y}, e.Sub(order, e)))
	return check != nil && check.y.Bit(0) == 0 && check.x.Cmp(r) == 0
}

// MakeEvent uses the record's timestamp unless the caller supplies an override.
func MakeEvent(secret []byte, env canon.Object, created *int64, aux []byte) (canon.Object, error) {
	pub, err := Public(secret)
	if err != nil {
		return nil, err
	}
	body, _ := env["body"].(canon.Object)
	ts, ok := canon.Int64(body["created"])
	if created != nil {
		ts, ok = *created, true
	}
	kind, isString := body["type"].(string)
	if !ok || !isString {
		return nil, errors.New("invalid record body")
	}
	wire, err := records.Wire(env)
	if err != nil {
		return nil, err
	}
	tags := [][]string{{"t", "skynet-architecture-v1"}, {"x", kind}}
	pk := hex.EncodeToString(pub)
	raw, err := canon.Marshal([]any{0, pk, ts, 9467, tags, string(wire)}, false)
	if err != nil {
		return nil, err
	}
	id := sha256.Sum256(raw)
	signature, err := Sign(id[:], secret, aux)
	if err != nil {
		return nil, err
	}
	return canon.Object{"id": hex.EncodeToString(id[:]), "pubkey": pk, "created_at": ts, "kind": 9467,
		"tags": tags, "content": string(wire), "sig": hex.EncodeToString(signature)}, nil
}
