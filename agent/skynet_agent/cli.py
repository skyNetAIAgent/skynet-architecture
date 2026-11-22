"""Command line of the SkyNet research agent."""

import argparse
import datetime
import json
import logging
import logging.handlers
import os
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from . import MIN_PYTHON, RELEASE_SEQ, __version__
from . import autostart, config, net, power, runner, signed, submit, tasks, trust, updater
from .kernels import REGISTRY

EXIT_RESTART = 75          # tells the launcher: start the newly installed version
EXIT_NOTHING = 3           # "run --once" found nothing to do
EXIT_ALREADY_RUNNING = 4   # another agent holds the lock (the launcher must not retry)
SKIP_SECONDS = {"failed": 24 * 3600, "slow": 7 * 24 * 3600, "enough": 24 * 3600}

log = logging.getLogger("skynet-agent")


def setup_logging(verbose=False, to_file=True):
    log.setLevel(logging.DEBUG if verbose else logging.INFO)
    log.handlers[:] = []
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
    if sys.stderr is not None:
        console = logging.StreamHandler(sys.stderr)
        console.setFormatter(fmt)
        log.addHandler(console)
    if to_file:
        try:
            config.ensure_dirs()
            handler = logging.handlers.RotatingFileHandler(
                config.path("logs", "agent.log"), maxBytes=1 << 20, backupCount=3, encoding="utf-8")
            handler.setFormatter(fmt)
            log.addHandler(handler)
        except OSError:
            pass
    return log


def today_utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")


def say(text=""):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", "replace").decode("ascii"))


# ------------------------------------------------------------------ run

class _Battery:
    """on_battery() can be slow (it may start a helper program); ask once a minute."""

    def __init__(self):
        self._at = 0.0
        self._value = None

    def get(self):
        now = time.time()
        if now - self._at > 60:
            self._value = power.on_battery()
            self._at = now
        return self._value


def _skip(state, task_id, why, reason):
    state["skip"][task_id] = {"reason": reason, "until": int(time.time()) + SKIP_SECONDS[why]}


def _expire_skips(state, index):
    now = int(time.time())
    ids = set(t["id"] for t in index.get("tasks", [])) if index else None
    for task_id in list(state["skip"]):
        entry = state["skip"][task_id]
        until = entry.get("until", 0) if isinstance(entry, dict) else 0
        if until <= now or (ids is not None and task_id not in ids):
            del state["skip"][task_id]
    if ids is not None:
        for task_id in list(state["done"]):
            if task_id not in ids:
                del state["done"][task_id]
        for task_id in list(state["fails"]):
            if task_id not in ids:
                del state["fails"][task_id]


def _fetch_coverage(base):
    try:
        raw = net.get(base + "/" + tasks.COVERAGE_PATH, max_bytes=4 << 20, timeout=20)
        data = json.loads(raw.decode("utf-8"))
        return data if isinstance(data, dict) else None
    except (net.NetError, ValueError, UnicodeDecodeError):
        return None


def _poll(args, cfg, state, current_index):
    """One look at the repository. Returns (index, coverage, halt reason, restart needed).

    The halt reason is None when the release description could not be read: the caller then
    keeps the pause it already knows instead of resuming work because of a network failure.
    """
    base = updater.base_url()
    halt, restart = None, False
    try:
        # --no-update acts like the setting update=off: nothing is installed or reported, but
        # the release description is still read, because it carries the maintainers' pause.
        mode = dict(cfg, update="off") if args.no_update else cfg
        res = updater.check_and_apply(config.home(), base, mode)
        halt = res.halt
        if res.installed:
            log.info("installed version %s (release %d); restarting", res.available[1], res.available[0])
            restart = True
        elif res.available:
            log.info("version %s is available. %s", res.available[1], res.note)
    except (net.NetError, signed.SignatureError, updater.ReleaseError, OSError) as e:
        log.warning("update check failed: %s", e)
    index = current_index
    try:
        fresh = tasks.fetch_index(base)
        if fresh["seq"] < state["index_seq"]:
            log.warning("ignoring a task list older than the one already seen")
        elif tasks.is_expired(fresh, today_utc()):
            log.warning("the task list has expired; waiting for a new one")
            index = None
        else:
            index = fresh
            state["index_seq"] = fresh["seq"]
    except (net.NetError, signed.SignatureError, tasks.IndexError_) as e:
        log.warning("could not get the task list: %s", e)
        state["last_error"] = str(e)[:300]
    coverage = _fetch_coverage(base) if index else None
    _expire_skips(state, index)
    return index, coverage, halt, restart


def _issues(index):
    """Tracking issue of every task in the current list."""
    if not index:
        return {}
    return dict((t["id"], t.get("issue", 0)) for t in index.get("tasks", []))


def _job_for(task, unit, cfg):
    ctx = {}
    kind = REGISTRY[task["kernel"]].KIND
    if kind == "ai":
        ctx = {"ai": cfg.get("ai", {}), "base_url": updater.base_url()}
        timeout = cfg.get("ai", {}).get("timeout_minutes", 30) * 60 + 120
    else:
        timeout = min(task.get("max_seconds", 3600), cfg.get("max_task_minutes", 120) * 60)
    job = {"kernel": task["kernel"], "kernel_version": task["kernel_version"],
           "params": task["params"], "unit": unit, "units": task["units"], "ctx": ctx}
    return job, timeout


def _handle_outcome(task, unit, outcome, cfg, state):
    task_id = task["id"]
    kind = REGISTRY[task["kernel"]].KIND
    if outcome.get("ok"):
        record, text = submit.make_record(task, unit, outcome, cfg)
        submit.save_to_outbox(task, record, text, kind)
        state["done"].setdefault(task_id, []).append(unit)
        state["counters"]["units_done"] += 1
        state["fails"].pop(task_id, None)
        log.info("finished %s unit %d in %.1f s", task_id, unit, outcome.get("elapsed_s", 0))
        return True
    error = str(outcome.get("error", "unknown error"))[:300]
    state["counters"]["units_failed"] += 1
    state["last_error"] = "%s: %s" % (task_id, error)
    if outcome.get("timeout"):
        log.warning("%s unit %d took too long on this device; leaving this task to others", task_id, unit)
        _skip(state, task_id, "slow", "too slow on this device")
    else:
        fails = state["fails"].get(task_id, 0) + 1
        state["fails"][task_id] = fails
        log.warning("%s unit %d failed: %s", task_id, unit, error)
        if fails >= 3:
            _skip(state, task_id, "failed", error)
    return False


def _run_loop(args):
    cfg = config.load_config()
    state = config.load_state()
    battery = _Battery()
    executor = ThreadPoolExecutor(max_workers=256)
    futures = {}                      # future -> (task, unit)
    index = coverage = None
    halt, restart = "", False
    next_poll = 0.0
    finished = 0
    waiting_note = ""
    stop_file = config.path("stop")
    try:
        os.unlink(stop_file)
    except OSError:
        pass
    log.info("SkyNet research agent %s (release %d) on %s, home %s",
             __version__, RELEASE_SEQ, power.platform_tag(), config.home())
    if not trust.RELEASE_KEYS:
        log.error("this copy has no release key and cannot accept tasks or updates")
    try:
        while True:
            if os.path.exists(stop_file):
                log.info("stop requested")
                try:
                    os.unlink(stop_file)
                except OSError:
                    pass
                break
            now = time.time()
            if now >= next_poll:
                cfg = config.load_config()
                index, coverage, new_halt, restart_now = _poll(args, cfg, state, index)
                if new_halt is not None:
                    halt = new_halt
                restart = restart or restart_now
                if halt:
                    log.warning("the maintainers paused this version: %s", halt)
                if not args.no_submit:
                    submit.flush_outbox(cfg, state, log, issues=_issues(index), force=args.once)
                state["last_poll"] = int(now)
                config.save_state(state)
                next_poll = now + cfg["poll_minutes"] * 60 * random.uniform(0.8, 1.2)

            for fut in [f for f in futures if f.done()]:
                task, unit = futures.pop(fut)
                try:
                    outcome = fut.result()
                except Exception as e:
                    outcome = {"ok": False, "error": "%s: %s" % (type(e).__name__, e)}
                ok = _handle_outcome(task, unit, outcome, cfg, state)
                finished += 1
                if ok and not args.no_submit:
                    submit.flush_outbox(cfg, state, log, issues=_issues(index), force=args.once)
                config.save_state(state)

            if restart and not futures:
                config.save_state(state)
                return EXIT_RESTART
            if args.once and finished >= 1 and not futures:
                break

            note = ""
            if index is None:
                note = "no task list yet"
            elif tasks.is_expired(index, today_utc()):
                note = "the task list has expired; waiting for a new one"
            elif halt:
                note = "paused by the maintainers"
            elif cfg["paused"]:
                note = "paused (run: skynet-agent resume)"
            elif submit.outbox_count() >= submit.MAX_OUTBOX:
                # Computing more makes no sense while nothing can be published.
                note = ("%d results are waiting to be published; check the GitHub login "
                        "(skynet-agent github)" % submit.MAX_OUTBOX)
            elif not cfg["run_on_battery"] and battery.get() is True:
                note = "on battery, waiting for mains power"
            elif not cfg["run_on_battery"] and battery.get() is None and power.is_android():
                # A phone must not be drained by surprise: when we cannot tell, we do not work.
                note = ("cannot tell whether the phone is charging; install Termux:API "
                        "(pkg install termux-api) or run: skynet-agent config set run_on_battery true")
            may_start = (not note and not restart and len(futures) < cfg["workers"]
                         and not (args.once and finished + len(futures) >= 1))
            if may_start:
                busy = [(t["id"], u) for t, u in futures.values()]
                choice = tasks.pick(index, cfg, state, coverage, busy=busy)
                if choice is None:
                    note = "all available tasks are done on this device"
                    if args.once and not futures:
                        log.info(note)
                        break
                else:
                    task, unit = choice
                    if REGISTRY[task["kernel"]].KIND == "ai" and task.get("issue", 0) > 0:
                        have = submit.count_results(task["issue"])
                        if have is not None and have >= task["params"].get("max_answers", 20):
                            _skip(state, task["id"], "enough", "the question already has enough answers")
                            continue
                    job, timeout = _job_for(task, unit, cfg)
                    futures[executor.submit(runner.run_job, job, timeout)] = (task, unit)
                    log.info("started %s unit %d of %d", task["id"], unit, task["units"])
                    continue
            if note and note != waiting_note:
                log.info("waiting: %s", note)
            waiting_note = note
            if args.once and note and not futures:
                break
            time.sleep(0.2 if args.once else 1.0)
    finally:
        runner.kill_all()
        executor.shutdown(wait=False)
        config.save_state(state)
    if args.once and not finished:
        return EXIT_NOTHING
    return 0


def cmd_run(args):
    setup_logging(args.verbose)
    lock = config.InstanceLock()
    try:
        lock.acquire()
    except config.AlreadyRunning as e:
        say(str(e))
        return EXIT_ALREADY_RUNNING
    try:
        return _run_loop(args)
    except KeyboardInterrupt:
        log.info("interrupted")
        return 0
    finally:
        lock.release()


# ------------------------------------------------------------------ other commands

def cmd_worker(args):
    from . import worker
    return worker.main()


def cmd_version(args):
    say("skynet-agent %s (release %d), Python %d.%d.%d, %s" % (
        (__version__, RELEASE_SEQ) + tuple(sys.version_info[:3]) + (power.platform_tag(),)))
    return 0


def cmd_status(args):
    cfg = config.load_config()
    state = config.load_state()
    say("SkyNet research agent %s (release %d)" % (__version__, RELEASE_SEQ))
    say("Home folder:      %s" % config.home())
    say("Installed copy:   %s" % ("yes" if updater.is_installed_layout(config.home()) else "no (development run)"))
    say("Release keys:     %d" % len(trust.RELEASE_KEYS))
    say("Workers:          %d   paused: %s   on battery: %s" % (
        cfg["workers"], "yes" if cfg["paused"] else "no",
        {True: "yes", False: "no", None: "unknown"}[power.on_battery()]))
    say("Update mode:      %s   publish: %s   AI mode: %s" % (
        cfg["update"], cfg["submit"], "on" if cfg["ai"]["enabled"] else "off"))
    say("Autostart:        %s" % autostart.status())
    c = state["counters"]
    say("Units done:       %d   failed: %d   published: %d" % (
        c.get("units_done", 0), c.get("units_failed", 0), c.get("published", 0)))
    pending = submit.outbox_entries()
    say("Outbox:           %d result(s) waiting" % len(pending))
    wait = state.get("publish_after", 0) - time.time()
    if pending and wait > 0:
        say("Publishing:       the last attempt failed; next one in about %d min "
            "(now: skynet-agent outbox send)" % (wait // 60 + 1))
    if state.get("last_poll"):
        say("Last check:       %s UTC" % datetime.datetime.fromtimestamp(
            state["last_poll"], datetime.timezone.utc).strftime("%Y-%m-%d %H:%M"))
    if state.get("last_error"):
        say("Last problem:     %s" % state["last_error"])
    token, source = submit.find_token()
    say("GitHub login:     %s" % (("found in " + source) if token else source))
    return 0


def cmd_config(args):
    cfg = config.load_config()
    if args.action == "show" or args.action is None:
        say(json.dumps(cfg, indent=2, sort_keys=True))
        return 0
    if args.action == "get":
        try:
            say(json.dumps(config.get_key(cfg, args.key)))
        except (KeyError, TypeError):
            say("unknown setting: %s" % args.key)
            return 1
        return 0
    try:
        value = config.parse_value(args.key, args.value)
    except ValueError as e:
        say(str(e))
        say("Settings: %s" % ", ".join(sorted(config.SETTABLE)))
        return 1
    config.ensure_dirs()
    config.set_key(cfg, args.key, value)
    config.save_config(cfg)
    say("%s = %s" % (args.key, json.dumps(value)))
    say("A running agent picks this up at its next check of the repository.")
    return 0


def cmd_selftest(args):
    say("Python %d.%d.%d on %s" % (tuple(sys.version_info[:3]) + (power.platform_tag(),)))
    if sys.version_info[:2] < MIN_PYTHON:
        say("FAILED: Python %d.%d or newer is required" % MIN_PYTHON)
        return 1
    result = REGISTRY["selftest"].run({"rounds": 8}, 0, 1, {})
    say("Self-test digest: %s" % result["digest"])
    ok = bool(result["ok"])
    home = config.home()
    if updater.is_installed_layout(home):
        problems = updater.verify_installed(runner.version_root())
        for p in problems:
            say("PROBLEM: %s" % p)
        ok = ok and not problems
        say("Installed files match the signed release: %s" % ("yes" if not problems else "NO"))
    if args.online:
        base = updater.base_url()
        try:
            rel, _, _ = updater.fetch_release(base)
            say("Latest signed release: %s (release %d)" % (rel["version"], rel["seq"]))
            index = tasks.fetch_index(base)
            say("Signed task list: number %d with %d task(s)" % (index["seq"], len(index["tasks"])))
        except (net.NetError, signed.SignatureError, updater.ReleaseError, tasks.IndexError_) as e:
            say("PROBLEM: %s" % e)
            ok = False
    say("OK" if ok else "FAILED")
    return 0 if ok else 1


def cmd_verify_install(args):
    problems = updater.verify_installed(runner.version_root())
    for p in problems:
        say(p)
    if not problems:
        result = REGISTRY["selftest"].run({"rounds": 2}, 0, 1, {})
        if not result["ok"]:
            say("self-test failed")
            return 1
    return 1 if problems else 0


def cmd_tasks(args):
    cfg = config.load_config()
    state = config.load_state()
    try:
        index = tasks.fetch_index(updater.base_url())
    except (net.NetError, signed.SignatureError, tasks.IndexError_) as e:
        say("Could not get the task list: %s" % e)
        return 1
    say("Task list number %d, issued %s, expires %s" % (
        index["seq"], index.get("issued", "?"), index.get("expires", "never")))
    for task in index["tasks"]:
        reason = tasks.usable(task, cfg)
        done = len(state["done"].get(task["id"], []))
        skip = state["skip"].get(task["id"])
        if reason is None and skip:
            reason = "skipped here: %s" % skip.get("reason", "")
        say("  %-28s %-14s units %-7d done here %-5d %s" % (
            task["id"], "%s@%d" % (task["kernel"], task["kernel_version"]), task["units"], done,
            "ready" if reason is None else reason))
        if task.get("title"):
            say("      %s" % task["title"])
    return 0


def cmd_outbox(args):
    cfg = config.load_config()
    entries = submit.outbox_entries()
    action = args.action or "list"
    if action == "list":
        if not entries:
            say("The outbox is empty.")
            return 0
        for name, entry in entries:
            r = entry["record"]
            flag = ""
            if entry.get("kind") == "ai" and not entry.get("approved"):
                flag = "  (AI answer, waiting for your approval)"
            if not entry.get("issue"):
                flag += "  (the task has no tracking issue yet)"
            say("%s  %s unit %d%s" % (name, r["task"], r["unit"], flag))
        say("Commands: outbox show NAME | outbox approve NAME|all | outbox send | outbox link | outbox drop NAME")
        return 0
    if action == "show":
        for name, entry in entries:
            if name == args.name:
                say(submit.format_comment(entry["record"], entry.get("text")))
                return 0
        say("No such entry: %s" % args.name)
        return 1
    if action == "approve":
        count = 0
        for name, entry in entries:
            if args.name in ("all", name) and not entry.get("approved"):
                entry["approved"] = True
                config.write_json_atomic(config.path("outbox", name), entry)
                count += 1
        say("Approved %d answer(s)." % count)
        return 0
    if action == "drop":
        for name, entry in entries:
            if name == args.name:
                os.unlink(config.path("outbox", name))
                say("Dropped %s." % name)
                return 0
        say("No such entry: %s" % args.name)
        return 1
    if action == "link":
        if not entries:
            say("The outbox is empty.")
            return 0
        say("Open a link in your browser, sign in to GitHub and press the green button:")
        for name, entry in entries:
            url = submit.manual_issue_url(entry)
            say("")
            say(url if url else "%s is too large for a link; publish it with a GitHub login instead" % name)
        return 0
    if action == "send":
        setup_logging(False, to_file=False)
        state = config.load_state()
        forced = dict(cfg)
        forced["submit"] = "auto"
        issues = {}
        try:
            issues = _issues(tasks.fetch_index(updater.base_url()))
        except (net.NetError, signed.SignatureError, tasks.IndexError_):
            pass
        n = submit.flush_outbox(forced, state, log, issues=issues, force=True)
        config.save_state(state)
        say("Published %d result(s); %d left in the outbox." % (n, len(submit.outbox_entries())))
        return 0
    return 1


def cmd_github(args):
    token, source = submit.find_token()
    if not token:
        say(source)
        say("Without a login the results stay in the outbox; see: skynet-agent outbox link")
        return 1
    try:
        login = submit.whoami(token)
    except (net.NetError, ValueError) as e:
        say("The login from %s does not work: %s" % (source, e))
        return 1
    say("Results will be published as GitHub user %s (login found in %s)." % (login, source))
    return 0


def cmd_ai(args):
    cfg = config.load_config()
    module = REGISTRY["ai-answer"]
    try:
        endpoint, model = module.discover(cfg["ai"])
        models = module.list_models(endpoint)
    except (ValueError, net.NetError) as e:
        say("No usable AI server: %s" % e)
        say("Start Ollama, the llama.cpp server or LM Studio with a model loaded, then try again.")
        return 1
    say("AI server: %s" % endpoint)
    say("Models:    %s" % (", ".join(models) or "(none listed)"))
    say("Will use:  %s" % model)
    say("AI mode is %s (switch with: skynet-agent config set ai.enabled true)" % (
        "ON" if cfg["ai"]["enabled"] else "off"))
    return 0


def cmd_update(args):
    setup_logging(False, to_file=False)
    cfg = config.load_config()
    forced = dict(cfg)
    forced["update"] = "auto"
    try:
        res = updater.check_and_apply(config.home(), updater.base_url(), forced)
    except (net.NetError, signed.SignatureError, updater.ReleaseError, OSError) as e:
        say("Update check failed: %s" % e)
        return 1
    if res.installed:
        say("Installed version %s (release %d)." % (res.available[1], res.available[0]))
        say("A running agent restarts into it at its next check of the repository.")
        return 0
    if res.available:
        say("Version %s is available. %s" % (res.available[1], res.note))
        return 0
    say("This is the latest version (%s, release %d)." % (__version__, RELEASE_SEQ))
    return 0


def _set_paused(value):
    config.ensure_dirs()
    cfg = config.load_config()
    cfg["paused"] = value
    config.save_config(cfg)


def cmd_pause(args):
    _set_paused(True)
    say("Paused. Running tasks finish; no new ones start. Resume with: skynet-agent resume")
    return 0


def cmd_resume(args):
    _set_paused(False)
    say("Resumed.")
    return 0


def cmd_stop(args):
    config.ensure_dirs()
    with open(config.path("stop"), "w") as f:
        f.write("stop\n")
    say("Asked the running agent to stop. It exits within a few seconds.")
    return 0


def cmd_autostart(args):
    action = args.action or "status"
    if action == "status":
        say("Autostart: %s" % autostart.status())
        return 0
    if not os.path.exists(autostart.launcher_path()):
        say("Autostart needs an installed copy (run the installer first).")
        return 1
    try:
        say(autostart.enable() if action == "enable" else autostart.disable())
    except OSError as e:
        say("Could not change autostart: %s" % e)
        return 1
    return 0


def cmd_uninstall(args):
    if not args.yes:
        say("This turns autostart off and asks a running agent to stop.")
        say("Run it again with --yes to continue.")
        return 1
    try:
        say(autostart.disable())
    except OSError as e:
        say("Could not change autostart: %s" % e)
    cmd_stop(args)
    say("To remove the agent completely, delete this folder: %s" % config.home())
    return 0


# ------------------------------------------------------------------ entry point

def build_parser():
    parser = argparse.ArgumentParser(
        prog="skynet-agent",
        description="SkyNet research agent: runs research computations from the project "
                    "repository on this computer and publishes the results. No rewards.")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("run", help="work until stopped (this is what autostart runs)")
    p.add_argument("--once", action="store_true", help="do one unit of work and exit")
    p.add_argument("--no-update", action="store_true", help="do not look for new versions")
    p.add_argument("--no-submit", action="store_true", help="keep results in the outbox")
    p.add_argument("--verbose", action="store_true")
    p.set_defaults(func=cmd_run)

    p = sub.add_parser("status", help="show what the agent is doing")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("config", help="show or change settings")
    p.add_argument("action", nargs="?", choices=["show", "get", "set"])
    p.add_argument("key", nargs="?")
    p.add_argument("value", nargs="?")
    p.set_defaults(func=cmd_config)

    p = sub.add_parser("tasks", help="list the tasks currently published")
    p.set_defaults(func=cmd_tasks)

    p = sub.add_parser("outbox", help="results waiting to be published")
    p.add_argument("action", nargs="?", choices=["list", "show", "approve", "send", "link", "drop"])
    p.add_argument("name", nargs="?")
    p.set_defaults(func=cmd_outbox)

    p = sub.add_parser("github", help="check which GitHub account will publish results")
    p.set_defaults(func=cmd_github)

    p = sub.add_parser("ai", help="check the optional local AI model")
    p.set_defaults(func=cmd_ai)

    p = sub.add_parser("selftest", help="check that this device computes correctly")
    p.add_argument("--online", action="store_true", help="also check signatures of the published files")
    p.set_defaults(func=cmd_selftest)

    p = sub.add_parser("update", help="install the newest signed version now")
    p.set_defaults(func=cmd_update)

    p = sub.add_parser("pause", help="stop taking new tasks")
    p.set_defaults(func=cmd_pause)
    p = sub.add_parser("resume", help="take tasks again")
    p.set_defaults(func=cmd_resume)
    p = sub.add_parser("stop", help="ask the running agent to exit")
    p.set_defaults(func=cmd_stop)

    p = sub.add_parser("autostart", help="start the agent when you log in")
    p.add_argument("action", nargs="?", choices=["status", "enable", "disable"])
    p.set_defaults(func=cmd_autostart)

    p = sub.add_parser("uninstall", help="turn autostart off and stop the agent")
    p.add_argument("--yes", action="store_true")
    p.set_defaults(func=cmd_uninstall)

    p = sub.add_parser("version", help="show the version")
    p.set_defaults(func=cmd_version)

    p = sub.add_parser("worker")           # internal: runs one unit
    p.set_defaults(func=cmd_worker)
    p = sub.add_parser("verify-install")   # internal: used by the installer
    p.set_defaults(func=cmd_verify_install)
    return parser


def main(argv=None):
    if sys.version_info[:2] < MIN_PYTHON:
        sys.stderr.write("skynet-agent needs Python %d.%d or newer\n" % MIN_PYTHON)
        return 1
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 0
    if args.command == "config":
        if args.action == "get" and not args.key:
            parser.error("config get needs a setting name")
        if args.action == "set" and (not args.key or args.value is None):
            parser.error("config set needs a setting name and a value")
    if args.command == "outbox" and args.action in ("show", "approve", "drop") and not args.name:
        parser.error("outbox %s needs an entry name" % args.action)
    return args.func(args)
