"""The SkyNet research agent inside the Android app.

The app carries the same agent code as the desktop version (the package
skynet_agent). Android cannot start extra Python processes, so this module
replaces the desktop launcher and the worker processes:

  * one unit of work at a time, computed inside the app's background process;
  * a watchdog ends that process when a unit runs longer than its limit (the
    task is then left to faster devices), and Android starts the service again;
  * a newer agent version is taken from the repository only if the code BUILT
    INTO THE APK accepts it: its signature with the built-in release key, every
    file against the signed list, no file that is not on the list, and a release
    number not lower than the highest one that already worked here;
  * a new version gets three tries to start; if it does not reach the
    repository within them, it is marked bad and the built-in code runs again.

The app itself (this file and the Java part) changes only with a new APK.

`host` is the Android service. It provides isCharging(), stopRequested() and
setWorking(bool). On a computer the same loop runs with a stand-in host, which
is how it is tested (agent/tests/test_android_glue.py).
"""

import argparse
import json
import os
import re
import sys
import threading
import time

EXIT_TIMEOUT = 3
MAX_TRIES = 3
_DIR_RE = re.compile(r"^versions/[0-9]{1,9}-[0-9.]{1,20}$")
_state = {"version_dir": None}
_builtin = {}                       # modules of the code built into the APK, kept for all checks
_attempt = {"unit": None}           # the unit in progress, for the watchdog
_lock = threading.Lock()


def _purge():
    for name in list(sys.modules):
        if name == "skynet_agent" or name.startswith("skynet_agent."):
            del sys.modules[name]


def _read_json(path, default=None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def _write_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _mark_bad(home, seq):
    path = os.path.join(home, "bad_seqs.json")
    bad = _read_json(path, [])
    if not isinstance(bad, list):
        bad = []
    if _is_int(seq) and seq not in bad:
        bad.append(seq)
    _write_json(path, bad)


def _max_seq(home):
    value = _read_json(os.path.join(home, "max_seq.json"), 0)
    return value if _is_int(value) else 0


def _load_builtin():
    """Import the copy built into the APK once; its checks are used for every downloaded version."""
    if not _builtin:
        _purge()
        import skynet_agent
        from skynet_agent import net, signed, updater
        _builtin.update(seq=skynet_agent.RELEASE_SEQ, updater=updater, signed=signed, net=net)
    return _builtin


def unlisted_files(vdir):
    """Files and folders in a version folder that its signed release does not list (and links)."""
    rel = _read_json(os.path.join(vdir, "release.json"), {})
    allowed = set((rel.get("files") or {}).keys()) | {"release.json", "release.json.sig"}
    extra = []
    for folder, dirs, names in os.walk(vdir):
        for name in dirs + names:
            full = os.path.join(folder, name)
            rel_path = os.path.relpath(full, vdir).replace(os.sep, "/")
            if os.path.islink(full):
                extra.append(rel_path)
            elif os.path.isfile(full) and rel_path not in allowed:
                extra.append(rel_path)
            elif os.path.isdir(full) and not any(a.startswith(rel_path + "/") for a in allowed):
                extra.append(rel_path)
    return sorted(extra)


def select_code(home):
    """Decide which agent code runs: a verified newer version from home/versions, else the built-in one.

    Returns the release number of the downloaded version in use, or None for the built-in code.
    """
    built = _load_builtin()
    updater = built["updater"]
    if _state["version_dir"]:
        try:
            sys.path.remove(_state["version_dir"])
        except ValueError:
            pass
        _state["version_dir"] = None
    _purge()
    cur = updater.read_current(home)
    if not cur:
        import skynet_agent  # noqa: F401
        return None
    seq, rel_dir = cur.get("seq"), cur.get("dir")
    if (not _is_int(seq) or seq <= built["seq"] or seq < _max_seq(home)
            or seq in updater.bad_seqs(home) or not isinstance(rel_dir, str) or not _DIR_RE.match(rel_dir)):
        import skynet_agent  # noqa: F401
        return None
    vdir = os.path.join(home, *rel_dir.split("/"))
    # Checked by the code built into the APK: signature with its release key, every file, nothing extra.
    if updater.verify_installed(vdir) or unlisted_files(vdir):
        _mark_bad(home, seq)
        import skynet_agent  # noqa: F401
        return None
    trial_path = os.path.join(home, "trial.json")
    trial = _read_json(trial_path, {})
    tries = trial.get("tries", 0) if isinstance(trial, dict) and trial.get("seq") == seq else 0
    if tries >= MAX_TRIES:
        _mark_bad(home, seq)
        import skynet_agent  # noqa: F401
        return None
    _write_json(trial_path, {"seq": seq, "tries": tries + 1})     # before the first line of it runs
    sys.path.insert(0, vdir)
    try:
        import skynet_agent as newer
        from skynet_agent import cli, worker, submit, tasks  # noqa: F401  (must all import)
        if newer.RELEASE_SEQ != seq:
            raise ImportError("the version reports another release number")
    except Exception:
        sys.path.remove(vdir)
        _purge()
        _mark_bad(home, seq)
        import skynet_agent  # noqa: F401
        return None
    _state["version_dir"] = vdir
    return seq


def confirm(home, seq):
    """A downloaded version has worked here (it reached the repository): it is no longer on trial."""
    if seq is None:
        return
    if seq > _max_seq(home):
        _write_json(os.path.join(home, "max_seq.json"), seq)
    try:
        os.unlink(os.path.join(home, "trial.json"))
    except OSError:
        pass


def on_trial(home, seq):
    trial = _read_json(os.path.join(home, "trial.json"), {})
    return seq is not None and isinstance(trial, dict) and trial.get("seq") == seq


def _watchdog(home):
    """End the process when the unit in progress runs longer than its limit (monotonic clock)."""
    while True:
        time.sleep(5)
        with _lock:
            unit = _attempt["unit"]
        if unit and time.monotonic() - unit["start"] > unit["limit"]:
            try:
                _write_json(os.path.join(home, "timed_out.json"), {"task": unit["task"], "unit": unit["unit"]})
            finally:
                os._exit(EXIT_TIMEOUT)


def _set_working(host, working):
    fn = getattr(host, "setWorking", None)
    if fn is not None:
        fn(working)


def _loop(home, host, downloaded_seq, hooks):
    from skynet_agent import RELEASE_SEQ, __version__, cli, config, submit, tasks
    from skynet_agent import worker
    from skynet_agent.kernels import REGISTRY

    log = cli.setup_logging(False)
    config.ensure_dirs()
    cfg = config.load_config()
    state = config.load_state()
    status_path = os.path.join(home, "status.json")
    args = argparse.Namespace(no_update=True, no_submit=False, once=False)

    left_path = os.path.join(home, "timed_out.json")
    left = _read_json(left_path)
    if isinstance(left, dict) and isinstance(left.get("task"), str):
        log.warning("%s unit %s took too long on this device; leaving this task to others",
                    left["task"], left.get("unit"))
        cli._skip(state, left["task"], "slow", "too slow on this device")
        config.save_state(state)
    try:
        os.unlink(left_path)
    except OSError:
        pass

    def status(note, current="", code=""):
        counters = state["counters"]
        problem, problem_code = state.get("last_error", ""), ""
        if "GitHub CLI" in problem or "gh auth login" in problem:
            # the desktop hint fits no phone; the app shows its own words for it, in its language
            problem, problem_code = "no GitHub token yet: paste one below to publish the results", "no_token"
        _write_json(status_path, {
            "time": int(time.time()), "note": note, "code": code, "current": current,
            "version": __version__, "release": RELEASE_SEQ, "downloaded": downloaded_seq is not None,
            "units_done": counters.get("units_done", 0), "units_failed": counters.get("units_failed", 0),
            "published": counters.get("published", 0), "outbox": submit.outbox_count(),
            "last_error": problem, "problem_code": problem_code,
            "login": bool(submit.find_token()[0])})

    log.info("SkyNet research agent %s (release %d) in the Android app, home %s", __version__, RELEASE_SEQ, home)
    index = coverage = None
    halt = ""
    next_poll = 0.0
    waiting = None
    while not host.stopRequested():
        now = time.time()
        if now >= next_poll:
            cfg = config.load_config()
            cfg["ai"]["enabled"] = False                 # the app has no local AI model
            index, coverage, new_halt, _ = cli._poll(args, cfg, state, index)
            if new_halt is not None:                     # None: the repository could not be read
                halt = new_halt
                confirm(home, downloaded_seq)
            if halt:
                log.warning("the maintainers paused this version: %s", halt)
            if cfg["update"] == "auto" and _update(home, log):
                config.save_state(state)
                return "restart"
            submit.flush_outbox(cfg, state, log, issues=cli._issues(index))
            state["last_poll"] = int(now)
            config.save_state(state)
            next_poll = now + cfg["poll_minutes"] * 60
        else:
            cfg = config.load_config()                   # a switch changed on the screen applies at once
            cfg["ai"]["enabled"] = False

        note, code = "", ""
        if index is None:
            note, code = "no task list yet", "no_tasks"
        elif tasks.is_expired(index, cli.today_utc()):
            note, code = "the task list has expired; waiting for a new one", "expired"
        elif halt:
            note, code = "paused by the maintainers", "halted"
        elif cfg["paused"]:
            note, code = "paused", "paused"
        elif submit.outbox_count() >= submit.MAX_OUTBOX:
            note = "%d results are waiting to be published; add a GitHub token" % submit.MAX_OUTBOX
            code = "outbox_full"
        elif not cfg["run_on_battery"] and not host.isCharging():
            note, code = "not charging, waiting for the charger", "not_charging"
        choice = None if note else tasks.pick(index, cfg, state, coverage)
        if not note and choice is None:
            note, code = "all available tasks are done on this device", "all_done"
        if note:
            if note != waiting:
                log.info("waiting: %s", note)
            waiting = note
            status(note, code=code)
            time.sleep(hooks.get("idle_sleep", 5))
            continue

        waiting = None
        task, unit = choice
        job, limit = cli._job_for(task, unit, cfg)
        if REGISTRY[task["kernel"]].KIND != "compute":
            cli._skip(state, task["id"], "failed", "not available in the app")
            continue
        log.info("started %s unit %d of %d", task["id"], unit, task["units"])
        status("working", "%s, %d / %d" % (task["id"], unit, task["units"]), code="working")
        _set_working(host, True)
        with _lock:
            _attempt["unit"] = {"task": task["id"], "unit": unit, "start": time.monotonic(), "limit": limit}
        try:
            outcome = worker.run_job(job)
        finally:
            with _lock:
                _attempt["unit"] = None
            _set_working(host, False)
        cli._handle_outcome(task, unit, outcome, cfg, state)
        config.save_state(state)                         # the unit is recorded before anything is sent
        if outcome.get("ok"):
            submit.flush_outbox(cfg, state, log, issues=cli._issues(index))
            config.save_state(state)
        status("working", code="working")
    config.save_state(state)
    status("stopped", code="stopped")
    return "stop"


def _update(home, log):
    """Download a newer signed release with the code built into the APK. True if one was installed."""
    built = _load_builtin()
    updater, net, signed = built["updater"], built["net"], built["signed"]
    from skynet_agent import RELEASE_SEQ
    try:
        rel, raw, sig = updater.fetch_release(updater.base_url())     # checked with the APK's release key
        if (rel["seq"] <= max(RELEASE_SEQ, _max_seq(home)) or rel["seq"] in updater.bad_seqs(home)
                or not updater.python_ok(rel)):
            return False
        rel_dir = updater.download_release(home, updater.base_url(), rel, raw, sig)
        updater.activate(home, rel, rel_dir)
        log.info("installed version %s (release %d)", rel["version"], rel["seq"])
        return True
    except (net.NetError, signed.SignatureError, updater.ReleaseError, OSError) as e:
        log.warning("update failed: %s", e)
        return False


def run(home, host, hooks=None):
    """Work until the host asks to stop. Called by the Android service on its own thread."""
    hooks = hooks or {}
    home = str(home)
    sys.dont_write_bytecode = True          # nothing but signed source files in the version folders
    os.makedirs(home, exist_ok=True)
    os.environ["SKYNET_AGENT_HOME"] = home
    if not hooks.get("no_watchdog"):
        threading.Thread(target=_watchdog, args=(home,), daemon=True).start()
    failures = 0
    while True:
        seq = select_code(home)
        try:
            from skynet_agent import power
            power.set_low_priority()
            if _loop(home, host, seq, hooks) == "stop":
                return 0
            failures = 0
        except Exception as e:                      # never let the service die silently
            failures += 1
            if on_trial(home, seq):
                _mark_bad(home, seq)                # a new version failed before it ever worked here
            _write_json(os.path.join(home, "status.json"),
                        {"time": int(time.time()), "code": "error",
                         "note": "error: %s: %s" % (type(e).__name__, e)})
            if failures >= 5:
                return 1
            time.sleep(hooks.get("idle_sleep", 5) * failures)
