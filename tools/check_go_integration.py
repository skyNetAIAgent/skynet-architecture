"""Check Go delivery and Python profile compatibility using real local processes.

From the repository root, run python3 -I tools/check_go_integration.py /path/to/skynet-agent.
The receiver, task mirror, collector and profiles are temporary. Only loopback is used.
"""
import argparse
import contextlib
import functools
import http.server
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request

sys.dont_write_bytecode = True
EXPECTED_HASH = "7823a03918e86a7046e437fdf001dc40ff05fb1d241a8917baeae4d88b5629fa"
TASK = "selftest-1"
LOCAL = "127.0.0.1"


def check(ok, message):
    if not ok:
        raise RuntimeError(message)


def run(*args):
    result = subprocess.run(list(map(str, args)), capture_output=True, text=True, timeout=180)
    if result.returncode:
        raise RuntimeError(f"{args} exited {result.returncode}\n{result.stdout}\n{result.stderr}")
    return result.stdout.strip()


@contextlib.contextmanager
def receiver(repo, root):
    logpath = root / "receiver.log"
    with logpath.open("w") as log:
        proc = subprocess.Popen([sys.executable, "-I", "-B", str(repo / "node/receiver.py"),
                                 "--host", LOCAL, "--port", "0", "--no-relays",
                                 "--data", str(root / "node")], stdout=log, stderr=log)
        try:
            for _ in range(600):
                output = logpath.read_text()
                if proc.poll() is not None:
                    raise RuntimeError(f"receiver exited {proc.returncode}: {output}")
                match = re.search(r"listening on 127\.0\.0\.1:(\d+)", output)
                if match:
                    yield f"http://{LOCAL}:{match[1]}"
                    break
                time.sleep(0.1)
            else:
                raise RuntimeError(f"receiver startup timed out: {output}")
        finally:
            if proc.poll() is None:
                proc.send_signal(signal.SIGINT)
                try:
                    proc.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
                    raise
            check(proc.returncode == 0, f"receiver exited {proc.returncode}: {logpath.read_text()}")


@contextlib.contextmanager
def task_source(repo):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=repo)
    with http.server.ThreadingHTTPServer((LOCAL, 0), handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://{LOCAL}:{server.server_port}"
        finally:
            server.shutdown()
            thread.join()


def read_json(path):
    return json.loads(path.read_bytes())


def get(url):
    with urllib.request.urlopen(url, timeout=10) as response:
        return response.read()


def one(items, what):
    items = list(items)
    check(len(items) == 1, f"expected one {what}, got {len(items)}")
    return items[0]


def test_delivery(repo, binary, root, node):
    from skynet_agent import config, records, submit, tasks
    profile = root / "fresh"
    os.environ["SKYNET_AGENT_HOME"] = str(profile)
    version = run(binary, "version")
    version_match = re.search(r"skynet-agent (\S+) \(release (\d+)\)", version)
    check(version_match, f"unexpected version: {version}")
    selftest = run(binary, "selftest")
    check("a2e8f2c4" in selftest, f"unexpected selftest output: {selftest}")
    check(not (profile / "task-list.json").exists(), "profile already has a task cache")
    check(not (profile / "identity.key").exists(), "profile already has an identity")
    index_file = repo / "tasks/index.json"
    index = read_json(index_file)
    state = config.load_state()
    for task in index["tasks"]:
        if task["id"] != TASK:
            state["skip"][task["id"]] = {"reason": "choose the short selftest", "until": 4102444800}
    config.save_state(state)
    check(json.loads(get(node + "/v1/info"))["records"] == 0, "receiver already has records")
    run(binary, "run", "--once", "--no-update")
    check(tasks.cached_index(index["seq"]) == index, "Python did not verify freshly downloaded task cache")

    archive_path = one((profile / "sent").glob("*.json"), "archived result")
    archive = read_json(archive_path)
    check(submit.outbox_count() == 0, "archive left a waiting copy")
    counters = config.load_state()["counters"]
    check((counters["units_done"], counters["published"], counters["units_failed"]) == (1, 1, 0),
          f"fresh profile counters: {counters}")
    disk_rows = (root / "node/records.jsonl").read_bytes().splitlines()
    env = records.parse(one(disk_rows, "receiver record"))
    rid = env["id"]
    check(json.loads(get(node + "/v1/info"))["records"] == 1, "receiver did not report one record")
    check(records.parse(get(node + "/v1/records/" + rid)) == env, "receiver lookup differs")
    check(records.parse(one((profile / "net/records.jsonl").read_bytes().splitlines(), "agent record")) == env,
          "sender journal differs from receiver")
    check(archive["net_record"] == env and archive["published"] == "record:" + rid, "archive differs")
    check(env["body"]["author"] == records.public_hex(records.load_seed(create=False)), "record author differs")
    record = env["body"]["payload"]["record"]
    check(archive["record"] == record, "archive has different result")
    check((record["task"], record["unit"], record["agent"], record["seq"])
          == (TASK, 0, version_match[1], int(version_match[2])), "wrong task, unit or version")
    check(submit.result_hash(record["result"]) == record["result_sha256"] == EXPECTED_HASH, "result hash differs")

    scratch = root / "collector"
    store = scratch / "store"
    (scratch / "tasks").mkdir(parents=True)
    shutil.copyfile(index_file, scratch / "tasks/index.json")
    check(not store.exists(), "collector store is not fresh")
    line = run(sys.executable, "-I", "-B", repo / "tools/collect_results.py", "--net-only",
               "--net-store", store, "--root", scratch)
    check("Read 1 comment(s): 1 unit(s) with results, 0 rejected." in line, line)
    check(records.parse(one((store / "records.jsonl").read_bytes().splitlines(), "collector record")) == env,
          "collector fetched a different record")
    check(read_json(store / "cursors.json")["receiver " + node] == 1, "collector did not advance receiver cursor")
    check(read_json(scratch / "results/coverage.json")[TASK] == {"0": 1}, "wrong coverage")
    summary = read_json(scratch / "results/summary.json")[TASK]
    check(summary["units_with_results"] == 1 and summary["conflicts"] == [], "wrong collector summary")
    print(f"E2E_VERSION {version}", flush=True)
    print(f"E2E_SELFTEST {selftest}", flush=True)
    print(f"E2E_DELIVERY node=1 sender=1 collector=1 sent=1 outbox=0 task={TASK} unit=0 "
          f"id={rid} result_sha256={record['result_sha256']} index_seq={index['seq']} rejected=0", flush=True)
    print(f"E2E_COLLECTOR {line}", flush=True)


def test_profile(repo, binary, root):
    from skynet_agent import config, records, submit
    profile = root / "python-profile"
    shutil.copytree(repo / "agent-go/testdata/python-home", profile)
    os.environ["SKYNET_AGENT_HOME"] = str(profile)
    key_file = profile / "identity.key"
    key_bytes = key_file.read_bytes()
    public = records.public_hex(records.load_seed(create=False))
    old_name, old = one(submit.outbox_entries(), "original Python queue item")
    old_bytes = (profile / "outbox" / old_name).read_bytes()
    old_env = records.verify(old["net_record"])
    check(old_env["body"]["author"] == public, "fixture signature uses a different key")
    check(public in run(binary, "net", "id").split(), "Go read a different public key")
    run(binary, "run", "--once", "--no-update", "--no-submit")

    check(key_file.read_bytes() == key_bytes and records.public_hex(records.load_seed(create=False)) == public,
          "Python found a different key after the Go run")
    check((profile / "outbox" / old_name).read_bytes() == old_bytes, "original queue file changed")
    items = dict(submit.outbox_entries())
    check(submit.outbox_count() == len(items) == 2, "expected two Python-readable queue files")
    existing = items.pop(old_name)
    check(records.verify(existing["net_record"]) == old_env, "original signed record changed")
    new = one(items.values(), "new Go queue item")
    for entry in (existing, new):
        parsed = submit.parse_comment(submit.format_comment(entry["record"], entry["text"]))
        check(parsed == (entry["record"], entry["text"]), "Python did not accept the queued result")
    check((new["record"]["task"], new["record"]["unit"], new["record"]["result_sha256"])
          == (TASK, 0, EXPECTED_HASH), "unexpected new queue item")
    state = config.load_state()
    check(state["done"].get(TASK) == state["done"].get("old-task") == [0], "lost progress")
    check(state["counters"]["units_done"] == 2 and state["counters"]["published"] == 0, "wrong progress counters")
    check(not list((profile / "sent").glob("*.json")), "unsolicited publication")
    print(f"E2E_PROFILE key_bytes={len(key_bytes)} public={public} preserved_id={old_env['id']} "
          "outbox_before=1 outbox_after=2 completed=2 published=0", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("binary", type=Path)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    binary = args.binary.resolve(strict=True)
    sys.path.insert(0, str(repo / "agent"))
    for key in list(os.environ):
        if key.startswith("SKYNET_AGENT_") or key.lower().endswith("_proxy"):
            del os.environ[key]
    os.environ["NO_PROXY"] = LOCAL
    os.environ["SKYNET_AGENT_RELAYS"] = "none"
    with tempfile.TemporaryDirectory(prefix="skynet-offline-") as tmp:
        root = Path(tmp)
        with task_source(repo) as base, receiver(repo, root) as node:
            os.environ["SKYNET_AGENT_BASE_URL"] = base
            os.environ["SKYNET_AGENT_RECEIVERS"] = node
            test_delivery(repo, binary, root, node)
            test_profile(repo, binary, root)
    print("E2E_PASS", flush=True)


if __name__ == "__main__":
    main()
