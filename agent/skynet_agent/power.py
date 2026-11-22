"""Being a polite guest: low priority, and (if we can tell) no work on battery."""

import glob
import json
import os
import platform
import shutil
import subprocess
import sys


def is_android():
    return "ANDROID_ROOT" in os.environ or "TERMUX_VERSION" in os.environ


def platform_tag():
    """A coarse, non-identifying description: os-arch-pythonX.Y."""
    system = platform.system().lower() or "unknown"
    if is_android():
        system = "android"
    machine = platform.machine().lower() or "unknown"
    machine = {"x86_64": "amd64", "aarch64": "arm64"}.get(machine, machine)
    return "%s-%s-py%d.%d" % (system, machine, sys.version_info[0], sys.version_info[1])


def set_low_priority():
    """Ask the OS to give this process the lowest CPU priority. Never fails."""
    try:
        if os.name == "nt":
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.GetCurrentProcess.restype = ctypes.c_void_p
            kernel32.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
            kernel32.SetPriorityClass(kernel32.GetCurrentProcess(), 0x00000040)  # IDLE_PRIORITY_CLASS
        else:
            os.nice(19)
    except Exception:
        pass


def _windows_on_battery():
    import ctypes

    class SYSTEM_POWER_STATUS(ctypes.Structure):
        _fields_ = [
            ("ACLineStatus", ctypes.c_ubyte),
            ("BatteryFlag", ctypes.c_ubyte),
            ("BatteryLifePercent", ctypes.c_ubyte),
            ("SystemStatusFlag", ctypes.c_ubyte),
            ("BatteryLifeTime", ctypes.c_uint32),
            ("BatteryFullLifeTime", ctypes.c_uint32),
        ]

    status = SYSTEM_POWER_STATUS()
    if not ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(status)):
        return None
    if status.ACLineStatus == 0:
        return True
    if status.ACLineStatus == 1:
        return False
    return None


def _read(file_path):
    try:
        with open(file_path, "r", encoding="ascii", errors="replace") as f:
            return f.read().strip()
    except OSError:
        return None


def _sysfs_on_battery():
    supplies = glob.glob("/sys/class/power_supply/*")
    if not supplies:
        return None
    mains_online = None
    discharging = False
    for supply in supplies:
        kind = (_read(os.path.join(supply, "type")) or "").lower()
        if kind in ("mains", "usb", "usb_pd", "usb_c", "wireless"):
            online = _read(os.path.join(supply, "online"))
            if online == "1":
                mains_online = True
            elif online == "0" and mains_online is None:
                mains_online = False
        elif kind == "battery":
            if (_read(os.path.join(supply, "status")) or "").lower() == "discharging":
                discharging = True
    if mains_online is True:
        return False
    if discharging:
        return True
    if mains_online is False:
        return True
    return None


def _termux_on_battery():
    tool = shutil.which("termux-battery-status")
    if not tool:
        return None
    try:
        out = subprocess.run([tool], capture_output=True, timeout=8).stdout
        info = json.loads(out.decode("utf-8", "replace"))
    except Exception:
        return None
    plugged = str(info.get("plugged", "")).upper()
    if not plugged:
        return None
    return plugged == "UNPLUGGED"


def _mac_on_battery():
    tool = shutil.which("pmset")
    if not tool:
        return None
    try:
        out = subprocess.run([tool, "-g", "batt"], capture_output=True, timeout=8).stdout
    except Exception:
        return None
    text = out.decode("utf-8", "replace")
    if "'Battery Power'" in text:
        return True
    if "'AC Power'" in text:
        return False
    return None


def on_battery():
    """True: running on battery. False: on mains power. None: cannot tell."""
    try:
        if os.name == "nt":
            return _windows_on_battery()
        if sys.platform == "darwin":
            return _mac_on_battery()
        answer = _termux_on_battery()
        if answer is None:
            answer = _sysfs_on_battery()
        return answer
    except Exception:
        return None
