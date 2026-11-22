"""Start worker processes and enforce their time limits."""

import json
import os
import subprocess
import sys
import threading

# Runs "skynet_agent.cli" from the given directory in isolated mode (-I): the
# current directory and PYTHON* variables cannot inject other code.
STUB = ("import sys; sys.path.insert(0, sys.argv[1]); "
        "sys.argv = [sys.argv[0]] + sys.argv[2:]; "
        "from skynet_agent.cli import main; sys.exit(main())")


def version_root():
    """Directory that contains the running skynet_agent package."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def agent_command(*args):
    return [sys.executable, "-I", "-c", STUB, version_root()] + list(args)


_running = set()
_lock = threading.Lock()


def kill_all():
    with _lock:
        procs = list(_running)
    for proc in procs:
        try:
            proc.kill()
        except OSError:
            pass


def run_job(job, timeout):
    """Run one unit in a child process. Always returns a dict with "ok"."""
    flags = 0
    if os.name == "nt":
        flags = getattr(subprocess, "IDLE_PRIORITY_CLASS", 0) | getattr(subprocess, "CREATE_NO_WINDOW", 0)
    try:
        proc = subprocess.Popen(agent_command("worker"), stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                creationflags=flags)
    except OSError as e:
        return {"ok": False, "error": "cannot start worker: %s" % e}
    with _lock:
        _running.add(proc)
    try:
        try:
            out, err = proc.communicate(json.dumps(job).encode("utf-8"), timeout=timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()
            return {"ok": False, "error": "timeout", "timeout": True}
    finally:
        with _lock:
            _running.discard(proc)
    lines = [line for line in out.decode("utf-8", "replace").splitlines() if line.strip()]
    if proc.returncode != 0 or not lines:
        tail = err.decode("utf-8", "replace").strip().splitlines()[-1:] or [""]
        return {"ok": False, "error": "worker exited with code %s %s" % (proc.returncode, tail[0])}
    try:
        result = json.loads(lines[-1])
    except ValueError:
        return {"ok": False, "error": "worker printed something that is not JSON"}
    if not isinstance(result, dict) or "ok" not in result:
        return {"ok": False, "error": "worker returned an unexpected object"}
    return result
