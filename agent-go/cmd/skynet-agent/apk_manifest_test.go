package main

import (
	"bytes"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/skyNetAIAgent/skynet-architecture/agent-go/canon"
)

func TestPublishedAPKManifest(t *testing.T) {
	path := filepath.Join("..", "..", "..", "android", "latest.json")
	raw, err := os.ReadFile(path)
	if err != nil {
		t.Fatal(err)
	}
	signature, err := os.ReadFile(path + ".sig")
	if err != nil {
		t.Fatal(err)
	}
	value, err := canon.Parse(raw)
	if err != nil {
		t.Fatal(err)
	}
	doc := value.(Object)
	version := doc["version_code"].(int64)
	sdk := doc["min_sdk"].(int64)
	for _, tc := range []struct {
		installed, sdk int64
		offer          bool
	}{
		{version - 1, sdk, true}, {version, sdk, false}, {version + 1, sdk, false}, {version - 1, sdk - 1, false},
	} {
		offer, err := verifyAPKManifest(raw, signature, tc.installed, tc.sdk)
		if err != nil || offer != tc.offer {
			t.Errorf("installed=%d sdk=%d: offer=%t err=%v", tc.installed, tc.sdk, offer, err)
		}
	}
	if _, err := verifyAPKManifest(append(bytes.Clone(raw), ' '), signature, 0, sdk); err == nil {
		t.Error("accepted a modification to the signed bytes")
	}
	if _, err := verifyAPKManifest(raw, []byte("invalid"), 0, sdk); err == nil {
		t.Error("accepted an invalid signature")
	}
}

func TestAPKFields(t *testing.T) {
	for _, tc := range []struct {
		field string
		value any
	}{
		{"format", true}, {"version_code", "3"}, {"version_code", int64(1 << 31)}, {"size", int64(0)},
		{"size", 3.0}, {"notes", "a\u00a0b"}, {"notes", strings.Repeat("x", 501)}, {"version_name", " "},
		{"min_sdk", int64(-1)}, {"sha256", strings.Repeat("A", 64)}, {"url", apkReleaseURL + "%2e%2e/file.apk"},
		{"url", apkReleaseURL + "tag/%ff.apk"}, {"url", apkReleaseURL + "tag/file.apk?extra"},
		{"url", apkReleaseURL + "tag/file%5cname.apk"}, {"url", "https://example.org/tag/file.apk"},
	} {
		doc := Object{"format": int64(1), "version_code": int64(3), "size": int64(3), "min_sdk": int64(24),
			"version_name": "0.3.0", "notes": "Новое приложение", "sha256": strings.Repeat("0", 64),
			"url": apkReleaseURL + "tag/SkyNet%20Agent.APK", "future": true}
		if got, err := apkOffer(doc, 2, 24); !got || err != nil {
			t.Fatal(got, err)
		}
		doc[tc.field] = tc.value
		if _, err := apkOffer(doc, 2, 24); err == nil {
			t.Errorf("accepted %s=%v", tc.field, tc.value)
		}
	}
}
