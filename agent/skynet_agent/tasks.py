"""The task list: what it must look like and how this device picks work from it.

The list is tasks/index.json in the repository, with a detached signature.
A task is data only: a kernel name, parameters, and how many independent
units the work is split into. There is no scheduler: every agent picks a
random unit it has not done yet. Several agents landing on the same unit is
intended: equal answers from different people are how results are checked.
"""

import random
import re

from . import RELEASE_SEQ, signed
from .kernels import REGISTRY

INDEX_PATH = "tasks/index.json"
COVERAGE_PATH = "results/coverage.json"
MAX_INDEX_BYTES = 2 << 20
MAX_TASKS = 500

_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_TASK_KEYS = {"id", "kernel", "kernel_version", "units", "params", "issue", "title",
              "max_seconds", "priority", "redundancy", "min_agent_seq"}


class IndexError_(Exception):
    """The task list is signed correctly but its content is not acceptable."""


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def validate_index(index):
    """Check the structure of a task list. Returns the list of task objects."""
    if not isinstance(index, dict):
        raise IndexError_("the task list is not an object")
    if index.get("format") != 1:
        raise IndexError_("unknown task list format: %r" % (index.get("format"),))
    if not _is_int(index.get("seq")) or index["seq"] < 1:
        raise IndexError_("seq must be a positive integer")
    for key in ("issued", "expires"):
        value = index.get(key)
        if value is not None and (not isinstance(value, str) or not _DATE_RE.match(value)):
            raise IndexError_("%s must be a date YYYY-MM-DD" % key)
    tasks = index.get("tasks")
    if not isinstance(tasks, list) or len(tasks) > MAX_TASKS:
        raise IndexError_("tasks must be a list of at most %d entries" % MAX_TASKS)
    seen = set()
    for task in tasks:
        if not isinstance(task, dict):
            raise IndexError_("a task is not an object")
        extra = set(task) - _TASK_KEYS
        if extra:
            raise IndexError_("unknown task fields: %s" % sorted(extra))
        tid = task.get("id")
        if not isinstance(tid, str) or not _ID_RE.match(tid):
            raise IndexError_("bad task id: %r" % (tid,))
        if tid in seen:
            raise IndexError_("duplicate task id: %s" % tid)
        seen.add(tid)
        if not isinstance(task.get("kernel"), str) or not _ID_RE.match(task["kernel"]):
            raise IndexError_("%s: bad kernel name" % tid)
        if not _is_int(task.get("kernel_version")) or task["kernel_version"] < 1:
            raise IndexError_("%s: kernel_version must be a positive integer" % tid)
        if not _is_int(task.get("units")) or not 1 <= task["units"] <= 10 ** 6:
            raise IndexError_("%s: units must be 1..1000000" % tid)
        if not isinstance(task.get("params"), dict):
            raise IndexError_("%s: params must be an object" % tid)
        for key, lo, hi in (("issue", 0, 10 ** 9), ("max_seconds", 10, 86400),
                            ("priority", 0, 100), ("redundancy", 1, 100),
                            ("min_agent_seq", 1, 10 ** 9)):
            if key in task and (not _is_int(task[key]) or not lo <= task[key] <= hi):
                raise IndexError_("%s: %s must be an integer %d..%d" % (tid, key, lo, hi))
        if "title" in task and (not isinstance(task["title"], str) or len(task["title"]) > 200):
            raise IndexError_("%s: title must be a string up to 200 characters" % tid)
    return tasks


def is_expired(index, today):
    """today is 'YYYY-MM-DD' (UTC). A list without 'expires' never expires."""
    expires = index.get("expires")
    return bool(expires) and today > expires


def fetch_index(base_url):
    """Fetch, verify the signature and validate. Returns the index object."""
    index, _, _ = signed.fetch_signed_json(base_url, INDEX_PATH, max_bytes=MAX_INDEX_BYTES)
    validate_index(index)
    return index


def usable(task, cfg):
    """Return None if this device can take the task, otherwise a short reason."""
    if task.get("priority", 10) == 0:
        return "closed"
    if task.get("min_agent_seq", 1) > RELEASE_SEQ:
        return "needs a newer agent"
    module = REGISTRY.get(task["kernel"])
    if module is None:
        return "unknown kernel (needs a newer agent)"
    if module.VERSION != task["kernel_version"]:
        return "kernel version %d, this agent has %d" % (task["kernel_version"], module.VERSION)
    if module.KIND == "ai" and not cfg.get("ai", {}).get("enabled"):
        return "AI mode is off"
    try:
        module.validate(task["params"], task["units"])
    except ValueError as e:
        return "rejected: %s" % e
    return None


def _coverage_for(coverage, task_id):
    if not isinstance(coverage, dict):
        return {}
    entry = coverage.get(task_id)
    return entry if isinstance(entry, dict) else {}


def pick(index, cfg, state, coverage=None, busy=(), rng=None):
    """Choose (task, unit) for this device, or None if there is nothing to do.

    busy: (task id, unit) pairs already running here.
    coverage: optional {task id: {unit as text: number of results}} published by
    the maintainers; units with fewer results than the task's redundancy are
    preferred. It is advisory only and need not be signed.
    """
    rng = rng or random.SystemRandom()
    busy = set(busy)
    candidates = []
    for task in index.get("tasks", []):
        if usable(task, cfg) is not None:
            continue
        if task["id"] in state.get("skip", {}):
            continue
        done = set(state.get("done", {}).get(task["id"], []))
        taken = done | set(u for t, u in busy if t == task["id"])
        if len(taken) >= task["units"]:
            continue
        candidates.append((task, taken))
    if not candidates:
        return None
    weights = [max(1, task.get("priority", 10)) for task, _ in candidates]
    task, taken = rng.choices(candidates, weights=weights, k=1)[0]
    units = task["units"]
    cov = _coverage_for(coverage, task["id"])
    need = task.get("redundancy", 2)

    def uncovered(u):
        count = cov.get(str(u), 0)
        return not _is_int(count) or count < need

    # a few random probes, preferring units that still lack results
    fallback = None
    for _ in range(64):
        u = rng.randrange(units)
        if u in taken:
            continue
        if uncovered(u):
            return task, u
        if fallback is None:
            fallback = u
    if fallback is not None:
        return task, fallback
    free = [u for u in range(units) if u not in taken]
    if not free:
        return None
    lacking = [u for u in free if uncovered(u)]
    return task, rng.choice(lacking or free)
