package transport

import (
	"context"
	"net"
	"os"
	"strconv"
	"strings"
	"time"
)

// Full nodes answer this question on UDP port 8790 inside a private network.
const (
	lanQuestion = "SKYNET-NODE? v1"
	lanAnswer   = "SKYNET-NODE v1 "
	lanPort     = 8790
)

// WithLAN adds full nodes found on the local network to the receivers.
//
// A computer in the same private network as a full node often cannot reach the node's
// public address (many routers do not loop it back). The agent then would wait for
// timeouts and never deliver its status. Nodes answer a broadcast question on the LAN,
// and only answers from private addresses are used. An explicit SKYNET_AGENT_RECEIVERS
// list is left as it is.
func (n Network) WithLAN(ctx context.Context) Network {
	if _, set := os.LookupEnv("SKYNET_AGENT_RECEIVERS"); set {
		return n
	}
	found := DiscoverLAN(ctx, 1500*time.Millisecond)
	seen := map[string]bool{}
	for _, r := range n.Receivers {
		seen[r] = true
	}
	out := append([]string{}, n.Receivers...)
	for _, r := range found {
		if !seen[r] {
			seen[r] = true
			out = append(out, r)
		}
	}
	n.Receivers = out
	return n
}

// DiscoverLAN broadcasts the question and collects "http://IP:PORT" of the nodes that answer.
func DiscoverLAN(ctx context.Context, wait time.Duration) []string {
	conn, err := net.ListenUDP("udp4", &net.UDPAddr{})
	if err != nil {
		return nil
	}
	defer conn.Close()
	deadline := time.Now().Add(wait)
	if d, ok := ctx.Deadline(); ok && d.Before(deadline) {
		deadline = d
	}
	conn.SetDeadline(deadline)
	for _, target := range broadcastAddresses() {
		conn.WriteToUDP([]byte(lanQuestion), &net.UDPAddr{IP: target, Port: lanPort})
	}
	var found []string
	seen := map[string]bool{}
	buf := make([]byte, 128)
	for len(found) < 8 {
		k, from, err := conn.ReadFromUDP(buf)
		if err != nil {
			break
		}
		if url, ok := parseAnswer(string(buf[:k]), from.IP); ok && !seen[url] {
			seen[url] = true
			found = append(found, url)
		}
	}
	return found
}

func parseAnswer(text string, from net.IP) (string, bool) {
	if !strings.HasPrefix(text, lanAnswer) || !(from.IsPrivate() || from.IsLoopback()) {
		return "", false
	}
	port, err := strconv.Atoi(strings.TrimSpace(strings.TrimPrefix(text, lanAnswer)))
	if err != nil || port < 1 || port > 65535 {
		return "", false
	}
	return "http://" + net.JoinHostPort(from.String(), strconv.Itoa(port)), true
}

// broadcastAddresses gives the limited broadcast and the directed broadcast of each private IPv4 network.
func broadcastAddresses() []net.IP {
	out := []net.IP{net.IPv4bcast}
	addrs, _ := net.InterfaceAddrs()
	for _, a := range addrs {
		ipnet, ok := a.(*net.IPNet)
		if !ok {
			continue
		}
		ip := ipnet.IP.To4()
		if ip == nil || !ip.IsPrivate() || len(ipnet.Mask) != net.IPv4len {
			continue
		}
		b := make(net.IP, net.IPv4len)
		for i := range b {
			b[i] = ip[i] | ^ipnet.Mask[i]
		}
		out = append(out, b)
	}
	return out
}
