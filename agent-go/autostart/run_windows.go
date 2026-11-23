package autostart

import (
	"errors"
	"path/filepath"
	"strings"
	"syscall"
	"unsafe"
)

var adv = syscall.NewLazyDLL("advapi32.dll")
var createKey = adv.NewProc("RegCreateKeyExW")
var setValue = adv.NewProc("RegSetValueExW")
var deleteValue = adv.NewProc("RegDeleteValueW")

func change(home, action string) (string, error) {
	path, _ := syscall.UTF16PtrFromString(`Software\Microsoft\Windows\CurrentVersion\Run`)
	value, _ := syscall.UTF16PtrFromString(name)
	var key syscall.Handle
	access := uint32(syscall.KEY_QUERY_VALUE)
	if action != "status" {
		access |= syscall.KEY_SET_VALUE
	}
	err := syscall.RegOpenKeyEx(syscall.HKEY_CURRENT_USER, path, 0, access, &key)
	if errors.Is(err, syscall.ERROR_FILE_NOT_FOUND) {
		if action != "enable" {
			return "off", nil
		}
		n, _, _ := createKey.Call(syscall.HKEY_CURRENT_USER, uintptr(unsafe.Pointer(path)), 0, 0, 0, uintptr(access), 0, uintptr(unsafe.Pointer(&key)), 0)
		if n != 0 {
			return "", syscall.Errno(n)
		}
	} else if err != nil {
		return "", err
	}
	defer syscall.RegCloseKey(key)
	var typ, size uint32
	err = syscall.RegQueryValueEx(key, value, nil, &typ, nil, &size)
	exists := err == nil
	if !exists && !errors.Is(err, syscall.ERROR_FILE_NOT_FOUND) {
		return "", err
	}
	switch action {
	case "status":
		if exists {
			return "on", nil
		}
		return "off", nil
	case "disable":
		if exists {
			n, _, _ := deleteValue.Call(uintptr(key), uintptr(unsafe.Pointer(value)))
			if n != 0 {
				return "", syscall.Errno(n)
			}
		}
		return "off", nil
	case "migrate":
		if !exists {
			return "off", nil
		}
		if typ != syscall.REG_SZ || size < 2 || size > 65536 {
			return "existing registration retained", nil
		}
		buf := make([]uint16, (size+1)/2)
		if err = syscall.RegQueryValueEx(key, value, nil, &typ, (*byte)(unsafe.Pointer(&buf[0])), &size); err != nil {
			return "", err
		}
		cmd := strings.ToLower(syscall.UTF16ToString(buf))
		suffix := "\" \"" + strings.ToLower(filepath.Join(home, "launcher.py")) + "\" run"
		if !strings.HasSuffix(cmd, suffix) {
			return "existing registration retained", nil
		}
		exe := filepath.Base(strings.TrimPrefix(strings.TrimSuffix(cmd, suffix), "\""))
		if exe != "python.exe" && exe != "pythonw.exe" {
			return "existing registration retained", nil
		}
	}
	command := "\"" + filepath.Join(home, "skynet-agent.exe") + "\" launch run"
	data, err := syscall.UTF16FromString(command)
	if err != nil {
		return "", err
	}
	n, _, _ := setValue.Call(uintptr(key), uintptr(unsafe.Pointer(value)), 0, syscall.REG_SZ, uintptr(unsafe.Pointer(&data[0])), uintptr(len(data)*2))
	if n != 0 {
		return "", syscall.Errno(n)
	}
	return "on", nil
}
