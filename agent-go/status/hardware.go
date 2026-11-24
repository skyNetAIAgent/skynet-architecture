package status

import (
	"bytes"
	"context"
	"encoding/csv"
	"io"
	"os/exec"
	"strconv"
	"strings"
	"time"
	"unicode/utf8"
)

type GPU struct {
	Name   string `json:"name"`
	VRAMMB int64  `json:"vram_mb"`
}

func modelName(raw string) string {
	name := strings.TrimSpace(raw)
	if !utf8.ValidString(name) {
		return ""
	}
	if utf8.RuneCountInString(name) > 128 {
		return string([]rune(name)[:128])
	}
	return name
}

func nonnegative(raw string) int64 {
	n, err := strconv.ParseInt(strings.TrimSpace(raw), 10, 64)
	if err != nil || n < 0 {
		return 0
	}
	return n
}

func nvidiaGPUs(ctx context.Context) []GPU {
	ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()
	cmd := exec.CommandContext(ctx, "nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits")
	cmd.WaitDelay = time.Second
	hideWindow(cmd)
	output, err := cmd.Output()
	if err != nil {
		return []GPU{}
	}
	return parseNvidia(bytes.NewReader(output))
}

func parseNvidia(r io.Reader) []GPU {
	reader := csv.NewReader(r)
	reader.TrimLeadingSpace = true
	reader.FieldsPerRecord = 2
	gpus := []GPU{}
	for {
		row, err := reader.Read()
		if err == io.EOF {
			return gpus
		}
		if err != nil {
			continue
		}
		if name := modelName(row[0]); name != "" {
			gpus = append(gpus, GPU{Name: name, VRAMMB: nonnegative(row[1])})
		}
	}
}
