"""Start the agent when the user logs in. Only ever done on an explicit command.

Windows   a value in the current user's "Run" registry key (no administrator rights)
macOS     a launchd agent in ~/Library/LaunchAgents
Linux     a systemd user service (if systemd is there), otherwise a printed hint
Android   a Termux:Boot script in ~/.termux/boot (needs the Termux:Boot app)
"""

import os
import shutil
import subprocess
import sys

from . import config

NAME = "SkyNetAgent"
MAC_LABEL = "org.skynet.agent"
LINUX_UNIT = "skynet-agent.service"
_RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"


def is_termux():
    return "TERMUX_VERSION" in os.environ or os.environ.get("PREFIX", "").startswith("/data/data/com.termux")


def launcher_path():
    return config.path("launcher.py")


def _python_background():
    """On Windows prefer pythonw.exe so that no console window appears."""
    exe = sys.executable
    if os.name == "nt":
        cand = os.path.join(os.path.dirname(exe), "pythonw.exe")
        if os.path.exists(cand):
            return cand
    return exe


def windows_command():
    return '"%s" "%s" run' % (_python_background(), launcher_path())


def mac_plist_path():
    return os.path.join(os.path.expanduser("~"), "Library", "LaunchAgents", MAC_LABEL + ".plist")


def mac_plist():
    def esc(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" '
        '"http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
        '<plist version="1.0">\n<dict>\n'
        '  <key>Label</key><string>%s</string>\n'
        '  <key>ProgramArguments</key>\n  <array>\n'
        '    <string>%s</string>\n    <string>%s</string>\n    <string>run</string>\n'
        '  </array>\n'
        '  <key>RunAtLoad</key><true/>\n'
        '  <key>ProcessType</key><string>Background</string>\n'
        '  <key>LowPriorityIO</key><true/>\n'
        '  <key>Nice</key><integer>19</integer>\n'
        '</dict>\n</plist>\n'
    ) % (MAC_LABEL, esc(sys.executable), esc(launcher_path()))


def linux_unit_path():
    base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config")
    return os.path.join(base, "systemd", "user", LINUX_UNIT)


def linux_unit():
    return (
        "[Unit]\n"
        "Description=SkyNet research agent\n"
        "After=network-online.target\n\n"
        "[Service]\n"
        "ExecStart=\"%s\" \"%s\" run\n"
        "Restart=on-failure\n"
        "RestartSec=60\n"
        "Nice=19\n\n"
        "[Install]\n"
        "WantedBy=default.target\n"
    ) % (sys.executable, launcher_path())


def termux_boot_path():
    return os.path.join(os.path.expanduser("~"), ".termux", "boot", "skynet-agent.sh")


def termux_boot_script():
    return (
        "#!/data/data/com.termux/files/usr/bin/sh\n"
        "# Started by the Termux:Boot app when the device boots.\n"
        "termux-wake-lock 2>/dev/null\n"
        "exec \"%s\" \"%s\" run\n"
    ) % (sys.executable, launcher_path())


def _write(file_path, text, mode=None):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    if mode is not None:
        os.chmod(file_path, mode)


def _run_quiet(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, timeout=30).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def store_python_hint():
    return ("Python from the Microsoft Store cannot change the real list of programs that start "
            "with Windows (it sees a private copy of the registry). To start the agent when you "
            "sign in, do it by hand: press Win+R, type shell:startup, press Enter and put a "
            "shortcut to this file into the folder that opens:\n%s"
            % config.path("skynet-agent.cmd"))


def enable():
    """Returns a human-readable line about what was done."""
    if os.name == "nt":
        if config.is_store_python():
            return store_python_hint()
        import winreg
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, _RUN_KEY) as key:
            winreg.SetValueEx(key, NAME, 0, winreg.REG_SZ, windows_command())
        return "The agent will start when you sign in to Windows."
    if sys.platform == "darwin":
        _write(mac_plist_path(), mac_plist())
        _run_quiet(["launchctl", "unload", mac_plist_path()])
        if _run_quiet(["launchctl", "load", "-w", mac_plist_path()]):
            return "The agent is started and will start when you log in."
        return "Written %s; the agent will start at your next login." % mac_plist_path()
    if is_termux():
        _write(termux_boot_path(), termux_boot_script(), 0o700)
        return ("Written %s. Install the Termux:Boot app and open it once; "
                "the agent will then start when the device boots." % termux_boot_path())
    if shutil.which("systemctl"):
        _write(linux_unit_path(), linux_unit())
        _run_quiet(["systemctl", "--user", "daemon-reload"])
        if _run_quiet(["systemctl", "--user", "enable", "--now", LINUX_UNIT]):
            return "The agent is started and will start when you log in (systemd user service)."
        return ("Written %s, but systemd did not accept it. Try: "
                "systemctl --user enable --now %s" % (linux_unit_path(), LINUX_UNIT))
    return ("No systemd found. Add this line to your crontab (crontab -e):\n"
            "@reboot \"%s\" \"%s\" run" % (sys.executable, launcher_path()))


def disable():
    if os.name == "nt":
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _RUN_KEY, 0, winreg.KEY_SET_VALUE) as key:
                winreg.DeleteValue(key, NAME)
        except FileNotFoundError:
            pass
        if config.is_store_python():
            return ("Autostart is off as far as this Python can see. If you added a shortcut to "
                    "the Startup folder by hand (Win+R, shell:startup), delete it there.")
        return "Autostart is off."
    if sys.platform == "darwin":
        _run_quiet(["launchctl", "unload", "-w", mac_plist_path()])
        try:
            os.unlink(mac_plist_path())
        except OSError:
            pass
        return "Autostart is off."
    if is_termux():
        try:
            os.unlink(termux_boot_path())
        except OSError:
            pass
        return "Autostart is off."
    if shutil.which("systemctl"):
        _run_quiet(["systemctl", "--user", "disable", "--now", LINUX_UNIT])
    try:
        os.unlink(linux_unit_path())
    except OSError:
        pass
    return "Autostart is off. If you added a crontab line yourself, remove it with: crontab -e"


def status():
    if os.name == "nt":
        if config.is_store_python():
            return "unknown (Microsoft Store Python; see: skynet-agent autostart enable)"
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, _RUN_KEY) as key:
                value, _ = winreg.QueryValueEx(key, NAME)
            return "on: %s" % value
        except FileNotFoundError:
            return "off"
        except PermissionError:
            return "unknown (access to the startup registry key was denied)"
    if sys.platform == "darwin":
        return "on" if os.path.exists(mac_plist_path()) else "off"
    if is_termux():
        return "on" if os.path.exists(termux_boot_path()) else "off"
    return "on" if os.path.exists(linux_unit_path()) else "off"
