package agentgo_test

import (
	"bytes"
	"testing"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/nostr"
)

func TestBIP340(t *testing.T) {
	zero := make([]byte, 32)
	three := append(make([]byte, 31), 3)
	pub, err := nostr.Public(three)
	if err != nil || !bytes.Equal(pub, unhex("F9308A019258C31049344F85F89D5229B531C845836F99B08601F113BCE036F9")) {
		t.Fatal(err, pub)
	}
	for _, v := range []struct{ key, msg, aux []byte; want string }{
		{three, zero, zero, "E907831F80848D1069A5371B402410364BDF1C5F8307B0084C55F1CE2DCA821525F66A4A85EA8B71E482A74F382D2CE5EBEEE8FDB2172F477DF4900D310536C0"},
		{unhex("B7E151628AED2A6ABF7158809CF4F3C762E7160F38B4DA56A784D9045190CFEF"),
			unhex("243F6A8885A308D313198A2E03707344A4093822299F31D0082EFA98EC4E6C89"), append(make([]byte, 31), 1),
			"6896BD60EEAE296DB48A229FF71DFE071BDE413E6D43F917DC8DCF8C78DE33418906D11AC976ABCCB20B091292BFF4EA897EFCB639EA871CFA95F6DE339E4B0A"},
	} {
		pk, err := nostr.Public(v.key)
		if err != nil {
			t.Fatal(err)
		}
		s, err := nostr.Sign(v.msg, v.key, v.aux)
		if err != nil || !bytes.Equal(s, unhex(v.want)) || !nostr.Verify(v.msg, pk, s) {
			t.Fatal(err)
		}
		s[63] ^= 1
		if nostr.Verify(v.msg, pk, s) || nostr.Verify(v.msg, bytes.Repeat([]byte{255}, 32), s) {
			t.Fatal("accepted invalid signature")
		}
	}
}

func TestNostrEvent(t *testing.T) {
	seed := make([]byte, 32)
	key, err := nostr.SecretFromSeed(seed)
	if err != nil {
		t.Fatal(err)
	}
	event, err := nostr.MakeEvent(key, exampleRecord(t), nil, seed)
	if err != nil {
		t.Fatal(err)
	}
	if event["id"] != "20876c711f71a33f9fc894ef1b5c878a10cd3c15a6c3b32c23f9330c144c814e" {
		t.Fatal(event["id"])
	}
	if !nostr.Verify(unhex(event["id"].(string)), unhex(event["pubkey"].(string)), unhex(event["sig"].(string))) {
		t.Fatal("invalid event signature")
	}
}
