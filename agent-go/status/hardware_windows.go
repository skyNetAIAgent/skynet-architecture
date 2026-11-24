package status

import (
	"context"
	"syscall"
	"unsafe"
)

func Hardware(ctx context.Context) (string, int64, []GPU) {
	var mem struct {
		length, load                       uint32
		totalPhys, availPhys               uint64
		totalPageFile, availPageFile       uint64
		totalVirtual, availVirtual, unused uint64
	}
	mem.length = uint32(unsafe.Sizeof(mem))
	var ram int64
	proc := syscall.NewLazyDLL("kernel32.dll").NewProc("GlobalMemoryStatusEx")
	if proc.Find() == nil {
		if ok, _, _ := proc.Call(uintptr(unsafe.Pointer(&mem))); ok != 0 {
			ram = int64(mem.totalPhys >> 20)
		}
	}
	return windowsCPU(), ram, nvidiaGPUs(ctx)
}

func windowsCPU() string {
	path, _ := syscall.UTF16PtrFromString(`HARDWARE\DESCRIPTION\System\CentralProcessor\0`)
	var key syscall.Handle
	if err := syscall.RegOpenKeyEx(syscall.HKEY_LOCAL_MACHINE, path, 0, syscall.KEY_QUERY_VALUE, &key); err != nil {
		return ""
	}
	defer syscall.RegCloseKey(key)
	name, _ := syscall.UTF16PtrFromString("ProcessorNameString")
	var buf [256]uint16
	size := uint32(unsafe.Sizeof(buf))
	var typ uint32
	err := syscall.RegQueryValueEx(key, name, nil, &typ, (*byte)(unsafe.Pointer(&buf[0])), &size)
	if err != nil || typ != syscall.REG_SZ || size%2 != 0 || size > uint32(unsafe.Sizeof(buf)) {
		return ""
	}
	return modelName(syscall.UTF16ToString(buf[:size/2]))
}
