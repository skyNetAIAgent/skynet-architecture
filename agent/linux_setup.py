"""Linux setup and removal for the shell installer, outside the signed agent tree."""

import argparse
import errno
import getpass
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys
import time


def ask(question, default):
    if sys.stderr.isatty():
        try:
            with open("/dev/tty", encoding="utf-8") as tty:
                print(question, end=" ", file=sys.stderr, flush=True)
                answer = tty.readline()
            if answer:
                return default if not answer.strip() else answer.strip().lower() in ("y", "yes")
        except OSError:
            pass
    return None


def agent(home, *args):
    subprocess.run([sys.executable, "-I", str(Path(home, "launcher.py")), *args], check=True)


def disable(home):
    config = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    unit = config / "systemd/user/skynet-agent.service"
    if unit.exists():
        # Detect a refused stop before the signed CLI removes the unit file.
        subprocess.run(["systemctl", "--user", "disable", "--now", unit.name], check=True)
        agent(home, "autostart", "disable")


def configure(home, autostart, linger):
    interactive = autostart is None and not linger
    if interactive:
        autostart = ask("Start the agent automatically and run it now? [Y/n]", True)
    if not (autostart or linger):
        if autostart is False:
            try:
                disable(home)
            except (OSError, subprocess.SubprocessError) as exc:
                print("Could not disable the user service: %s" % exc, file=sys.stderr)
                return 1
        return 0
    # The signed 0.2.2 unit writer puts these paths in systemd double quotes.
    if any(c in home + sys.executable for c in '"\\%$\n\r'):
        print("Autostart needs paths without systemd special characters.", file=sys.stderr)
        return 1
    try:
        agent(home, "autostart", "enable")
        for state in ("is-enabled", "is-active"):
            subprocess.run(["systemctl", "--user", state, "--quiet", "skynet-agent.service"], check=True)
    except (OSError, subprocess.SubprocessError):
        print("Installed. To start the user service, sign in with systemd and run skynet-agent autostart enable.")
        return 1
    if linger or (interactive and ask("Also run before login and after logout? [y/N]", False)):
        try:
            subprocess.run(["loginctl", "--no-ask-password", "enable-linger", getpass.getuser()], check=True)
        except (OSError, subprocess.SubprocessError):
            print("Could not enable lingering. The service is enabled for your login sessions.")
            return 1
    return 0


def remove_entry(path):
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink(missing_ok=True)


def remove_empty(path):
    try:
        path.rmdir()
    except OSError as exc:
        if exc.errno not in (errno.ENOENT, errno.ENOTEMPTY, errno.EEXIST):
            raise


def uninstall(home, shim, purge):
    import fcntl

    with (home / "update.lock").open("a+b") as updating, (home / "agent.lock").open("a+b") as running:
        fcntl.flock(updating, fcntl.LOCK_EX | fcntl.LOCK_NB)
        disable(home)
        agent(home, "stop")
        deadline = time.monotonic() + 60
        while True:
            try:
                fcntl.flock(running, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise OSError("The agent is still running. Retry after it stops.")
                time.sleep(0.25)
        for folder, pattern in (("versions", r"[0-9]+-[0-9]+\.[0-9]+\.[0-9]+"), ("python", r"[0-9a-f]{64}")):
            root = home / folder
            if root.is_dir() and not root.is_symlink():
                for entry in root.iterdir():
                    if re.fullmatch(pattern, entry.name):
                        remove_entry(entry)
                remove_empty(root)
        if purge:
            for name in ("identity.key", "outbox", "net", "sent", "logs", "config.json",
                         "state.json", "task-list.json", "github-token"):
                remove_entry(home / name)
        helper = home / "uninstall.py"
        if shim and shim.is_file():
            dispatch = '    exec %s -I %s "$0" "$@"' % (shlex.quote(sys.executable), shlex.quote(str(helper)))
            if dispatch in shim.read_text(encoding="utf-8").splitlines():
                shim.unlink()
        for name in ("current.json", "max_seq.json", "bad_seqs.json", "stop", "launcher.py",
                     "uninstall.py", "agent.lock", "update.lock"):
            (home / name).unlink(missing_ok=True)
    remove_empty(home)
    print("Agent removed." if purge else "Agent removed. Device data and unsent results were kept.")


def main():
    parser = argparse.ArgumentParser(prog="skynet-agent uninstall")
    parser.add_argument("shim", help=argparse.SUPPRESS)
    parser.add_argument("--yes", required=True, action="store_true", help="confirm removal")
    parser.add_argument("--purge", action="store_true", help="also delete the device key and saved data")
    args = parser.parse_args()
    try:
        uninstall(Path(__file__).absolute().parent, Path(args.shim), args.purge)
    except (OSError, subprocess.SubprocessError) as exc:
        parser.exit(1, "Removal failed: %s\n" % exc)


if __name__ == "__main__":
    main()
