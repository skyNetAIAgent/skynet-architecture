"""Where the agent keeps its files, its settings and its local state."""

import json
import os
import sys
import tempfile

DEFAULT_CONFIG = {
    # How many tasks to run at the same time (each uses about one CPU core).
    "workers": 1,
    # How often to look at the repository for new tasks and versions.
    "poll_minutes": 30,
    # "auto": install signed updates; "notify": only report them; "off": ignore them.
    # A pause requested by the maintainers applies in every mode.
    "update": "auto",
    # "auto": publish results with your GitHub login; "manual": keep them in the outbox.
    "submit": "auto",
    # "net": signed records over public relays and receivers, no account needed;
    # "github": comments in the task's issue under your GitHub login (the older way).
    "submit_via": "net",
    # Do not start new tasks while the device runs on battery.
    "run_on_battery": False,
    # True stops the agent from taking new tasks until you resume it.
    "paused": False,
    # Upper limit for one task, whatever the task itself allows.
    "max_task_minutes": 120,
    # Results of one task are published together, at most one comment per this many minutes
    # (0 = publish every result at once).
    "batch_minutes": 60,
    # Upper limit of comments published per day from this device.
    "max_submissions_per_day": 48,
    # Include a coarse platform tag (os-arch-python) in published results.
    "report_platform": True,
    # Optional: answer research questions with a local AI model you run yourself.
    "ai": {
        "enabled": False,
        "endpoint": "",          # empty = look for a local server (Ollama, llama.cpp, LM Studio)
        "model": "",             # empty = first model the server lists
        "allow_remote": False,   # allow an endpoint that is not on this computer
        "review_before_submit": True,
        "timeout_minutes": 30,
    },
}

# Settings a user may change with "config set", with their types.
SETTABLE = {
    "workers": int,
    "poll_minutes": int,
    "update": str,
    "submit": str,
    "submit_via": str,
    "run_on_battery": bool,
    "paused": bool,
    "max_task_minutes": int,
    "batch_minutes": int,
    "max_submissions_per_day": int,
    "report_platform": bool,
    "ai.enabled": bool,
    "ai.endpoint": str,
    "ai.model": str,
    "ai.allow_remote": bool,
    "ai.review_before_submit": bool,
    "ai.timeout_minutes": int,
}

CHOICES = {
    "update": ("auto", "notify", "off"),
    "submit": ("auto", "manual"),
    "submit_via": ("net", "github"),
}

LIMITS = {
    "workers": (1, 256),
    "poll_minutes": (5, 1440),
    "max_task_minutes": (1, 1440),
    "batch_minutes": (0, 1440),
    "max_submissions_per_day": (0, 500),
    "ai.timeout_minutes": (1, 240),
}


def is_store_python():
    """Python from the Microsoft Store: it sees a private copy of AppData and of the registry."""
    where = (sys.executable + "|" + getattr(sys, "base_prefix", "")).lower()
    return sys.platform == "win32" and "\\windowsapps\\pythonsoftwarefoundation." in where


def home():
    """The agent's own directory. Nothing is written outside it without a command."""
    env = os.environ.get("SKYNET_AGENT_HOME")
    if env:
        return os.path.abspath(env)
    if sys.platform == "win32":
        if is_store_python():
            # AppData is private to the Store package; a folder there is invisible to other programs.
            return os.path.join(os.path.expanduser("~"), "SkyNetAgent")
        base = os.environ.get("LOCALAPPDATA") or os.path.join(os.path.expanduser("~"), "AppData", "Local")
        return os.path.join(base, "SkyNetAgent")
    if sys.platform == "darwin":
        return os.path.join(os.path.expanduser("~"), "Library", "Application Support", "SkyNetAgent")
    base = os.environ.get("XDG_DATA_HOME") or os.path.join(os.path.expanduser("~"), ".local", "share")
    return os.path.join(base, "skynet-agent")


def path(*parts):
    return os.path.join(home(), *parts)


def ensure_dirs():
    for sub in ("", "outbox", "sent", "logs", "versions", "net"):
        os.makedirs(path(sub) if sub else home(), exist_ok=True)


def read_json(file_path, default=None):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except (OSError, ValueError):
        return default


def write_json_atomic(file_path, obj):
    """Write JSON so that a crash never leaves a half-written file."""
    directory = os.path.dirname(file_path) or "."
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".tmp-", dir=directory)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=True)
            f.write("\n")
            f.flush()
            try:
                os.fsync(f.fileno())
            except OSError:
                pass
        os.replace(tmp, file_path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _merge(defaults, loaded):
    out = {}
    for key, value in defaults.items():
        if isinstance(value, dict):
            sub = loaded.get(key) if isinstance(loaded, dict) else None
            out[key] = _merge(value, sub if isinstance(sub, dict) else {})
        else:
            cand = loaded.get(key, value) if isinstance(loaded, dict) else value
            # keep the default if the stored value has the wrong type
            if isinstance(value, bool):
                out[key] = cand if isinstance(cand, bool) else value
            elif isinstance(value, int):
                out[key] = cand if isinstance(cand, int) and not isinstance(cand, bool) else value
            elif isinstance(value, str):
                out[key] = cand if isinstance(cand, str) else value
            else:
                out[key] = cand
    return out


def submit_via(cfg):
    """How results leave this device. SKYNET_AGENT_SUBMIT_VIA overrides the setting
    (tests use it; a participant may use it to try a channel out)."""
    forced = os.environ.get("SKYNET_AGENT_SUBMIT_VIA")
    if forced in CHOICES["submit_via"]:
        return forced
    value = cfg.get("submit_via", DEFAULT_CONFIG["submit_via"])
    return value if value in CHOICES["submit_via"] else DEFAULT_CONFIG["submit_via"]


def load_config():
    cfg = _merge(DEFAULT_CONFIG, read_json(path("config.json"), {}) or {})
    for key, (lo, hi) in LIMITS.items():
        cur = get_key(cfg, key)
        set_key(cfg, key, max(lo, min(hi, cur)))
    for key, allowed in CHOICES.items():
        if get_key(cfg, key) not in allowed:
            set_key(cfg, key, get_key(DEFAULT_CONFIG, key))
    return cfg


def save_config(cfg):
    write_json_atomic(path("config.json"), cfg)


def get_key(cfg, dotted):
    cur = cfg
    for part in dotted.split("."):
        cur = cur[part]
    return cur


def set_key(cfg, dotted, value):
    parts = dotted.split(".")
    cur = cfg
    for part in parts[:-1]:
        cur = cur[part]
    cur[parts[-1]] = value


def parse_value(dotted, text):
    """Convert the text of "config set KEY VALUE" to the right type, or raise ValueError."""
    if dotted not in SETTABLE:
        raise ValueError("unknown setting: %s" % dotted)
    kind = SETTABLE[dotted]
    if kind is bool:
        low = text.strip().lower()
        if low in ("true", "yes", "on", "1"):
            return True
        if low in ("false", "no", "off", "0"):
            return False
        raise ValueError("%s takes true or false" % dotted)
    if kind is int:
        value = int(text)
        if dotted in LIMITS:
            lo, hi = LIMITS[dotted]
            if not lo <= value <= hi:
                raise ValueError("%s must be between %d and %d" % (dotted, lo, hi))
        return value
    value = text.strip()
    if dotted in CHOICES and value not in CHOICES[dotted]:
        raise ValueError("%s must be one of: %s" % (dotted, ", ".join(CHOICES[dotted])))
    return value


DEFAULT_STATE = {
    "done": {},            # task id -> list of unit numbers finished on this device
    "skip": {},            # task id -> {reason, until}: tasks this device leaves alone for a while
    "fails": {},           # task id -> number of failures in a row
    "index_seq": 0,        # highest task-list number seen (older lists are ignored)
    "submitted": [],       # timestamps of recent publications (for the daily limit)
    "last_post": {},       # tracking issue (as text) -> time of our last comment there
    "publish_fails": 0,    # failed attempts to publish in a row
    "publish_after": 0,    # no new attempt before this time (grows with every failure)
    "counters": {"units_done": 0, "units_failed": 0, "published": 0},
    "last_error": "",
    "last_poll": 0,
    "poll_error": "",
    "poll_failures": 0,
    "retry_at": 0,
    "halt": "",
    "halt_seq": 0,
    "halt_through": 0,
}


def load_state():
    stored = read_json(path("state.json"), {}) or {}
    state = json.loads(json.dumps(DEFAULT_STATE))
    if isinstance(stored, dict):
        for key in state:
            if key in stored and isinstance(stored[key], type(state[key])):
                state[key] = stored[key]
    return state


def save_state(state):
    write_json_atomic(path("state.json"), state)


class AlreadyRunning(Exception):
    pass


class InstanceLock:
    """Only one "run" per agent directory. The OS releases the lock if we die."""

    def __init__(self):
        self._file = None

    def acquire(self):
        ensure_dirs()
        f = open(path("agent.lock"), "a+")
        try:
            if os.name == "nt":
                import msvcrt
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            f.close()
            raise AlreadyRunning("another agent is already running in %s" % home())
        self._file = f
        return self

    def release(self):
        f, self._file = self._file, None
        if f is None:
            return
        try:
            if os.name == "nt":
                import msvcrt
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        except OSError:
            pass
        f.close()

    def __enter__(self):
        return self.acquire()

    def __exit__(self, *exc):
        self.release()
