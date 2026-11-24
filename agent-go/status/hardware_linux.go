package status

import (
	"bufio"
	"context"
	"os"
	"path/filepath"
	"runtime"
	"strconv"
	"strings"
)

func Hardware(ctx context.Context) (string, int64, []GPU) {
	cpu, ram := cpuAndRAM("/proc")
	if runtime.GOOS == "android" || os.Getenv("ANDROID_ROOT") != "" || os.Getenv("TERMUX_VERSION") != "" {
		return cpu, ram, []GPU{}
	}
	return cpu, ram, drmGPUs("/sys/class/drm", nvidiaGPUs(ctx))
}

func cpuAndRAM(proc string) (string, int64) {
	cpu := modelName(procValue(filepath.Join(proc, "cpuinfo"), "model name", "Hardware", "Processor", "cpu"))
	var ram int64
	fields := strings.Fields(procValue(filepath.Join(proc, "meminfo"), "MemTotal"))
	if len(fields) == 2 && fields[1] == "kB" {
		ram = nonnegative(fields[0]) / 1024
	}
	return cpu, ram
}

func procValue(path string, keys ...string) string {
	f, err := os.Open(path)
	if err != nil {
		return ""
	}
	defer f.Close()
	scanner := bufio.NewScanner(f)
	for scanner.Scan() {
		key, val, ok := strings.Cut(scanner.Text(), ":")
		if ok && strings.TrimSpace(val) != "" {
			for _, wanted := range keys {
				if strings.TrimSpace(key) == wanted {
					return strings.TrimSpace(val)
				}
			}
		}
	}
	return ""
}

func drmGPUs(root string, gpus []GPU) []GPU {
	haveNvidia := len(gpus) > 0
	cards, _ := filepath.Glob(filepath.Join(root, "card[0-9]*"))
	for _, card := range cards {
		// Connector entries such as card0-HDMI-A-1 refer to the same GPU.
		if _, err := strconv.ParseUint(strings.TrimPrefix(filepath.Base(card), "card"), 10, 32); err != nil {
			continue
		}
		attribute := func(key string) string {
			data, _ := os.ReadFile(filepath.Join(card, "device", key))
			return strings.TrimSpace(string(data))
		}
		vendorID := attribute("vendor")
		vendor := vendorID
		switch vendor {
		case "0x10de":
			if haveNvidia {
				continue
			}
			vendor = "NVIDIA"
		case "0x1002":
			vendor = "AMD"
		case "0x8086":
			vendor = "Intel"
		default:
			continue // virtual display adapters (QEMU, VirtualBox, ...) are not compute GPUs
		}
		name := attribute("product_name")
		if name == "" {
			name = pciName(pciIDFiles, vendorID, attribute("device"))
		}
		if name == "" {
			name = strings.TrimSpace(vendor + " " + attribute("device"))
		}
		vram := nonnegative(attribute("mem_info_vram_total")) >> 20
		if name != "" || vram != 0 {
			gpus = append(gpus, GPU{Name: modelName(name), VRAMMB: vram})
		}
	}
	return gpus
}

// The PCI ID database that lspci uses; present on most desktop distributions.
var pciIDFiles = []string{"/usr/share/hwdata/pci.ids", "/usr/share/misc/pci.ids", "/usr/share/pci.ids"}

// pciName looks up a device name such as "Ellesmere [Radeon RX 470/480/570/570X/580/580X/590]".
func pciName(files []string, vendor, device string) string {
	vendor = strings.TrimPrefix(strings.ToLower(vendor), "0x")
	device = strings.TrimPrefix(strings.ToLower(device), "0x")
	if len(vendor) != 4 || len(device) != 4 {
		return ""
	}
	for _, path := range files {
		f, err := os.Open(path)
		if err != nil {
			continue
		}
		scanner := bufio.NewScanner(f)
		inVendor := false
		for scanner.Scan() {
			line := scanner.Text()
			switch {
			case line == "" || strings.HasPrefix(line, "#") || strings.HasPrefix(line, "\t\t"):
			case !strings.HasPrefix(line, "\t"):
				if inVendor || strings.HasPrefix(line, "C ") {
					if inVendor {
						f.Close()
						return ""
					}
				}
				inVendor = strings.HasPrefix(strings.ToLower(line), vendor+"  ")
			case inVendor && strings.HasPrefix(strings.ToLower(line), "\t"+device+"  "):
				f.Close()
				return strings.TrimSpace(line[1+4:])
			}
		}
		f.Close()
	}
	return ""
}
