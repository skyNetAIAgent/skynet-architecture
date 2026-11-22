"""Child process that runs exactly one unit of one task.

It reads a job (JSON) from standard input, runs the built-in kernel at the
lowest CPU priority, and prints one line of JSON. A separate process lets the
parent enforce a time limit and keeps a failing task from stopping the agent.
"""

import json
import sys
import time

from . import power
from .kernels import REGISTRY


def run_job(job):
    started = time.monotonic()
    try:
        module = REGISTRY.get(job["kernel"])
        if module is None:
            raise ValueError("unknown kernel: %s" % job["kernel"])
        if module.VERSION != job["kernel_version"]:
            raise ValueError("kernel version mismatch")
        module.validate(job["params"], job["units"])
        result = module.run(job["params"], job["unit"], job["units"], job.get("ctx") or {})
        return {"ok": True, "result": result, "elapsed_s": round(time.monotonic() - started, 3)}
    except Exception as e:  # a task must never crash the agent
        return {"ok": False, "error": "%s: %s" % (type(e).__name__, e),
                "elapsed_s": round(time.monotonic() - started, 3)}


def main():
    power.set_low_priority()
    try:
        job = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    except Exception as e:
        out = {"ok": False, "error": "bad job: %s" % e}
    else:
        out = run_job(job)
    sys.stdout.write(json.dumps(out, ensure_ascii=True) + "\n")
    sys.stdout.flush()
    return 0
