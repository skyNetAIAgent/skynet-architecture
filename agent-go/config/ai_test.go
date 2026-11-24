package config

import (
	"path/filepath"
	"testing"
)

func TestAIProfile(t *testing.T) {
	home := t.TempDir()
	cfg, err := Load(home)
	if err != nil {
		t.Fatal(err)
	}
	if Get(cfg, "ai.enabled") != false || Get(cfg, "ai.endpoint") != "" ||
		Get(cfg, "ai.model") != "" || Get(cfg, "ai.allow_remote") != false ||
		Get(cfg, "ai.timeout_minutes") != int64(30) || Get(cfg, "ai.max_answer_chars") != int64(8000) {
		t.Fatalf("unexpected AI defaults: %v", cfg["ai"])
	}
	python := Object{"ai": Object{"enabled": true, "endpoint": "http://localhost:8080/v1",
		"model": "local-model", "review_before_submit": false, "extra": "keep"}}
	if err = Write(filepath.Join(home, "config.json"), python); err != nil {
		t.Fatal(err)
	}
	cfg, err = Load(home)
	if err != nil {
		t.Fatal(err)
	}
	if Get(cfg, "ai.enabled") != true || Get(cfg, "ai.model") != "local-model" ||
		Get(cfg, "ai.endpoint") != "http://localhost:8080/v1" || Get(cfg, "ai.extra") != "keep" {
		t.Fatalf("lost Python settings: %v", cfg["ai"])
	}
	if Get(cfg, "ai.review_before_submit") != nil || Set(cfg, "ai.review_before_submit", "false") == nil {
		t.Fatal("legacy approval switch is still exposed")
	}
	if err = Set(cfg, "ai.max_answer_chars", "40"); err != nil || Get(cfg, "ai.max_answer_chars") != int64(40) {
		t.Fatal(cfg["ai"], err)
	}
	for _, invalid := range []string{"0", "8001", "3.5"} {
		if Set(cfg, "ai.max_answer_chars", invalid) == nil {
			t.Errorf("accepted ai.max_answer_chars=%s", invalid)
		}
	}
}
