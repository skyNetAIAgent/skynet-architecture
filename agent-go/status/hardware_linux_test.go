package status

import (
	"context"
	"os"
	"path/filepath"
	"reflect"
	"testing"
)

func writeAttribute(t *testing.T, dir, name, value string) {
	t.Helper()
	path := filepath.Join(dir, name)
	if err := os.MkdirAll(filepath.Dir(path), 0755); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(path, []byte(value), 0644); err != nil {
		t.Fatal(err)
	}
}

func TestProcHardware(t *testing.T) {
	dir := t.TempDir()
	if name, ram := cpuAndRAM(dir); name != "" || ram != 0 {
		t.Fatalf("missing hardware = %q, %d", name, ram)
	}
	writeAttribute(t, dir, "cpuinfo", "processor : 0\nSerial : identifier\nmodel name\t: Test CPU\n")
	writeAttribute(t, dir, "meminfo", "MemTotal: 8388608 kB\nMemFree: 123 kB\n")
	if name, ram := cpuAndRAM(dir); name != "Test CPU" || ram != 8192 {
		t.Fatalf("hardware = %q, %d", name, ram)
	}
	writeAttribute(t, dir, "cpuinfo", "processor : 0\nHardware: ARM board\n")
	writeAttribute(t, dir, "meminfo", "MemTotal: -1 kB\n")
	if name, ram := cpuAndRAM(dir); name != "ARM board" || ram != 0 {
		t.Fatalf("hardware = %q, %d", name, ram)
	}
}

func TestDRMAndNvidia(t *testing.T) {
	dir := t.TempDir()
	writeAttribute(t, dir, "card0/device/vendor", "0x10de\n")
	writeAttribute(t, dir, "card0/device/device", "0x1234\n")
	writeAttribute(t, dir, "card1/device/vendor", "0x1002\n")
	writeAttribute(t, dir, "card1/device/product_name", "Radeon test\n")
	writeAttribute(t, dir, "card1/device/mem_info_vram_total", "4294967296\n")
	writeAttribute(t, dir, "card1-HDMI-A-1/device/vendor", "0x1002\n")
	writeAttribute(t, dir, "renderD128/device/vendor", "0x1002\n")
	writeAttribute(t, dir, "card2/device/vendor", "0x1234\n") // QEMU standard VGA: not a compute GPU
	nvidia := GPU{Name: "NVIDIA test", VRAMMB: 2048}
	amd := GPU{Name: "Radeon test", VRAMMB: 4096}
	want := []GPU{nvidia, amd}
	if got := drmGPUs(dir, []GPU{nvidia}); !reflect.DeepEqual(got, want) {
		t.Fatalf("mixed GPUs = %#v", got)
	}
	want[0] = GPU{Name: "NVIDIA 0x1234"}
	if got := drmGPUs(dir, []GPU{}); !reflect.DeepEqual(got, want) {
		t.Fatalf("DRM GPUs = %#v", got)
	}
}

func TestTermuxSkipsGPU(t *testing.T) {
	t.Setenv("TERMUX_VERSION", "test")
	dir := t.TempDir()
	marker := filepath.Join(dir, "invoked")
	t.Setenv("GPU_TEST_MARKER", marker)
	t.Setenv("PATH", dir)
	program := "#!/bin/sh\n: > \"$GPU_TEST_MARKER\"\n"
	if err := os.WriteFile(filepath.Join(dir, "nvidia-smi"), []byte(program), 0755); err != nil {
		t.Fatal(err)
	}
	_, _, gpus := Hardware(context.Background())
	if gpus == nil || len(gpus) != 0 {
		t.Fatalf("Android GPUs = %#v", gpus)
	}
	if _, err := os.Stat(marker); !os.IsNotExist(err) {
		t.Fatalf("unexpected nvidia-smi invocation, stat error = %v", err)
	}
}
