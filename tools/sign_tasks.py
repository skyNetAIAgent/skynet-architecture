#!/usr/bin/env python3
"""Check and sign the task list tasks/index.json (for maintainers).

    python tools/sign_tasks.py                 check and sign
    python tools/sign_tasks.py --check         check only
    python tools/sign_tasks.py --fix-hashes    first write the SHA-256 of the context
                                               documents of AI questions into the list

Every task is checked with the same code the agents use: the structure of the
list, the parameters of each kernel, and (for AI questions) that the context
documents in the repository match the hashes in the task. A list that an agent
would reject is not signed.
"""

import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "agent"))

import keytool  # noqa: E402
from skynet_agent import ed25519, signed, tasks  # noqa: E402
from skynet_agent.kernels import REGISTRY  # noqa: E402


def check(index, root, fix_hashes=False):
    """Return (problems, changed)."""
    problems = []
    changed = False
    try:
        task_list = tasks.validate_index(index)
    except tasks.IndexError_ as e:
        return [str(e)], False
    for task in task_list:
        module = REGISTRY.get(task["kernel"])
        if module is None:
            problems.append("%s: unknown kernel %s" % (task["id"], task["kernel"]))
            continue
        if module.VERSION != task["kernel_version"]:
            problems.append("%s: kernel version %d, the agent has %d" % (
                task["id"], task["kernel_version"], module.VERSION))
            continue
        for doc in task["params"].get("context", []) if module.KIND == "ai" else []:
            path = os.path.join(root, *str(doc.get("path", "")).split("/"))
            try:
                with open(path, "rb") as f:
                    digest = hashlib.sha256(f.read()).hexdigest()
            except OSError:
                problems.append("%s: context document not found: %s" % (task["id"], doc.get("path")))
                continue
            if doc.get("sha256") != digest:
                if fix_hashes:
                    doc["sha256"] = digest
                    changed = True
                else:
                    problems.append("%s: %s changed since the task was written (use --fix-hashes)"
                                    % (task["id"], doc.get("path")))
        try:
            module.validate(task["params"], task["units"])
        except ValueError as e:
            problems.append("%s: %s" % (task["id"], e))
    return problems, changed


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--key")
    parser.add_argument("--root", default=os.path.join(HERE, ".."))
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--fix-hashes", action="store_true")
    args = parser.parse_args(argv)
    root = os.path.abspath(args.root)
    index_path = os.path.join(root, "tasks", "index.json")
    with open(index_path, "rb") as f:
        raw = f.read()
    try:
        index = signed.strict_json_loads(raw)
    except ValueError as e:
        print("tasks/index.json is not valid JSON: %s" % e)
        return 1
    problems, changed = check(index, root, fix_hashes=args.fix_hashes)
    if changed:
        raw = (json.dumps(index, indent=1, ensure_ascii=False) + "\n").encode("utf-8")
        with open(index_path, "wb") as f:
            f.write(raw)
        print("Wrote document hashes into tasks/index.json")
    if b"\r" in raw:
        problems.append("tasks/index.json must use LF line ends")
    for p in problems:
        print("PROBLEM: %s" % p)
    if problems:
        return 1
    print("Task list number %d: %d task(s), all accepted by this agent version." % (
        index["seq"], len(index["tasks"])))
    if args.check:
        return 0
    seed = keytool.load_seed(args.key)
    public = ed25519.public_key(seed)
    sig_line = signed.format_sig_line(public, ed25519.sign(seed, raw)).encode("ascii")
    signed.verify_detached(raw, sig_line, keys=[public.hex()])
    with open(index_path + ".sig", "wb") as f:
        f.write(sig_line)
    print("Signed with %s" % public.hex())
    return 0


if __name__ == "__main__":
    sys.exit(main())
