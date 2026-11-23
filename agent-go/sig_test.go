package agentgo_test

import (
	"bytes"
	"crypto/ed25519"
	"encoding/hex"
	"strings"
	"testing"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/sig"
)

func unhex(s string) []byte {
	b, err := hex.DecodeString(s)
	if err != nil {
		panic(err)
	}
	return b
}

func TestRFC8032(t *testing.T) {
	for _, v := range []struct{ seed, pub, msg, signature string }{
		{"9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60", "d75a980182b10ab7d54bfed3c964073a0ee172f3daa62325af021a68f707511a", "",
			"e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b"},
		{"4ccd089b28ff96da9db6c346ec114e0f5b8a319f35aba624da8cf6ed4fb8a6fb", "3d4017c3e843895a92b70aa74d1b7ebc9c982ccf2ec4968cc0cd55f12af4660c", "72",
			"92a009a9f0d4cab8720e820b5f642540a2b27b5416503f8fb3762223ebdb69da085ac1e43e15996e458f3613d0f11d8c387b2eaeb4302aeeb00d291612bb0c00"},
		{"c5aa8df43f9f837bedb7442f31dcb7b166d38535076f094b85ce3a2e0b4458f7", "fc51cd8e6218a1a38da47ed00230f0580816ed13ba3303ac5deb911548908025", "af82",
			"6291d657deec24024827e69c3abe01a30ce548a284743a445e3680d7db5ac3ac18ff9b538d16f290ae67f760984dc6594a7c15e9716ed28dc027beceea1ec40a"},
	} {
		key := ed25519.NewKeyFromSeed(unhex(v.seed))
		public := unhex(v.pub)
		msg := unhex(v.msg)
		signed := ed25519.Sign(key, msg)
		if !bytes.Equal(public, key.Public().(ed25519.PublicKey)) || hex.EncodeToString(signed) != v.signature ||
			!sig.IsStrongPublic(public) || !sig.Verify(public, msg, signed) || sig.Verify(public, append(msg, 0), signed) { t.Fatal(v.pub) }
		// S plus the group order gives a non-reduced scalar.
		order := unhex("edd3f55c1a631258d69cf7a2def9de1400000000000000000000000000000010")
		carry := 0
		for i, v := range order {
			sum := int(signed[32 + i]) + int(v) + carry
			signed[32 + i] = byte(sum)
			carry = sum >> 8
		}
		if sig.Verify(public, msg, signed) {
			t.Fatal("accepted unreduced S")
		}
	}
}

func TestEdwardsEncodings(t *testing.T) {
	// Both signs of an order-eight point and order-four points have small order.
	for _, key := range []string{
		strings.Repeat("00", 32), strings.Repeat("00", 31) + "80", "01" + strings.Repeat("00", 31),
		"01" + strings.Repeat("00", 30) + "80", "ec" + strings.Repeat("ff", 30) + "7f",
		"ed" + strings.Repeat("ff", 30) + "7f", "26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc05",
		"26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc85", "ff", "02" + strings.Repeat("00", 31),
	} {
		if sig.IsStrongPublic(unhex(key)) {
			t.Fatalf("accepted public key %s", key)
		}
	}
	pub := ed25519.NewKeyFromSeed(make([]byte, 32)).Public().(ed25519.PublicKey)
	signature := append(unhex("ed" + strings.Repeat("ff", 30) + "7f"), make([]byte, 32)...)
	if sig.Verify(pub, nil, signature) || sig.Verify(pub[:31], nil, signature) || sig.Verify(pub, nil, signature[:63]) {
		t.Fatal("accepted malformed signature")
	}
}

func TestDetachedDocument(t *testing.T) {
	key := ed25519.NewKeyFromSeed(make([]byte, 32))
	pub := key.Public().(ed25519.PublicKey)
	raw := []byte("{\"x\": 1}\n")
	line := []byte("# comment\ninvalid\n" + sig.FormatLine(pub, ed25519.Sign(key, raw)))
	keys := []string{strings.ToUpper(hex.EncodeToString(pub))}
	if _, err := sig.Document(raw, line, keys); err != nil {
		t.Fatal(err)
	}
	if _, err := sig.Document(raw[:len(raw) - 1], line, keys); err == nil {
		t.Fatal("accepted changed bytes")
	}
	if _, err := sig.Document(raw, line, []string{}); err == nil {
		t.Fatal("accepted untrusted signer")
	}
	for _, raw := range [][]byte{[]byte("[]"), []byte(`{"a":1,"a":2}`)} {
		line := []byte(sig.FormatLine(pub, ed25519.Sign(key, raw)))
		if _, err := sig.Document(raw, line, keys); err == nil {
			t.Fatal("accepted invalid signed document")
		}
	}
}
