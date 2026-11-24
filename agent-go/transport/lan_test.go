package transport

import (
	"context"
	"net"
	"testing"
	"time"
)

func TestParseAnswerOnlyPrivate(t *testing.T) {
	for _, c := range []struct {
		text, ip, want string
	}{
		{"SKYNET-NODE v1 8790", "192.168.20.200", "http://192.168.20.200:8790"},
		{"SKYNET-NODE v1 8790", "127.0.0.1", "http://127.0.0.1:8790"},
		{"SKYNET-NODE v1 8790", "8.8.8.8", ""},
		{"SKYNET-NODE v1 0", "10.0.0.2", ""},
		{"something else", "10.0.0.2", ""},
	} {
		got, _ := parseAnswer(c.text, net.ParseIP(c.ip))
		if got != c.want {
			t.Errorf("%q from %s = %q", c.text, c.ip, got)
		}
	}
}

func TestDiscoverReturnsNothingWithoutNodes(t *testing.T) {
	start := time.Now()
	DiscoverLAN(context.Background(), 200*time.Millisecond)
	if time.Since(start) > 2*time.Second {
		t.Fatal("discovery does not respect its wait")
	}
}

func TestExplicitReceiversAreKept(t *testing.T) {
	t.Setenv("SKYNET_AGENT_RECEIVERS", "http://127.0.0.1:1")
	n := Network{Receivers: []string{"http://127.0.0.1:1"}}.WithLAN(context.Background())
	if len(n.Receivers) != 1 {
		t.Fatalf("receivers = %v", n.Receivers)
	}
}
