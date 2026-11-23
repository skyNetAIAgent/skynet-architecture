package main

import (
	"context"
	"errors"
	"fmt"
	"io"
	"net"
	"net/http"
	"net/netip"
	"os"
	"strings"
	"time"
)

// The pure-Go resolver has no access to Android's per-network DNS settings.
// Resolve hostnames through the service, which uses the system resolver (also
// for VPN and Private DNS). HTTP retains the original host for TLS and SNI.
func init() {
	socket := os.Getenv("SKYNET_ANDROID_RESOLVER")
	if socket == "" || len(os.Args) < 2 || os.Args[1] != "android-service" {
		return
	}
	tr := http.DefaultTransport.(*http.Transport).Clone()
	tr.DialContext = func(ctx context.Context, network, address string) (net.Conn, error) {
		ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
		defer cancel()
		host, port, err := net.SplitHostPort(address)
		if err != nil {
			return nil, err
		}
		var dialer net.Dialer
		if _, err := netip.ParseAddr(host); err == nil {
			return dialer.DialContext(ctx, network, address)
		}
		addrs, err := androidLookup(ctx, socket, host)
		if err != nil {
			return nil, err
		}
		// Budget time for the other address family if the first route stalls.
		for i, ip := range addrs {
			deadline, _ := ctx.Deadline()
			attempt, stop := context.WithTimeout(ctx, time.Until(deadline)/time.Duration(len(addrs)-i))
			conn, dialErr := dialer.DialContext(attempt, network, net.JoinHostPort(ip.String(), port))
			stop()
			if dialErr == nil {
				return conn, nil
			}
			err = dialErr
		}
		return nil, err
	}
	http.DefaultTransport = tr
}

func androidLookup(ctx context.Context, socket, host string) ([]netip.Addr, error) {
	if len(host) > 254 || strings.ContainsAny(host, "\r\n") {
		return nil, errors.New("invalid hostname")
	}
	var dialer net.Dialer
	conn, err := dialer.DialContext(ctx, "unix", "@"+socket)
	if err != nil {
		return nil, err
	}
	defer conn.Close()
	stop := context.AfterFunc(ctx, func() { conn.Close() })
	defer stop()
	if _, err := fmt.Fprintln(conn, host); err != nil {
		return nil, err
	}
	const limit = 16 << 10
	reply, err := io.ReadAll(io.LimitReader(conn, limit+1))
	if err != nil {
		return nil, err
	}
	if len(reply) > limit {
		return nil, errors.New("oversized Android DNS response")
	}
	var addrs []netip.Addr
	for _, line := range strings.Fields(string(reply)) {
		ip, err := netip.ParseAddr(line)
		if err != nil {
			return nil, err
		}
		addrs = append(addrs, ip)
	}
	if len(addrs) == 0 {
		return nil, &net.DNSError{Err: "Android resolver returned no addresses", Name: host}
	}
	return addrs, nil
}
