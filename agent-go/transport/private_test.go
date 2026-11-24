package transport

import (
	"net/url"
	"testing"
)

func TestPlainHTTPOnlyOnLoopbackAndPrivateNetworks(t *testing.T) {
	for raw, ok := range map[string]bool{
		"http://127.0.0.1:8790/v1/status":      true,
		"http://192.168.20.200:8790/v1/status": true,
		"http://10.1.2.3/v1/records":           true,
		"https://node.example/v1/records":      true,
		"http://8.8.8.8:8790/v1/status":        false,
		"http://node.example/v1/records":       false,
	} {
		u, _ := url.Parse(raw)
		if err := checkURL(u); (err == nil) != ok {
			t.Errorf("%s: err = %v", raw, err)
		}
	}
}
