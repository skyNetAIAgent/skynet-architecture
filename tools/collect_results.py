#!/usr/bin/env python3
"""Collect and cross-check the results published by research agents.

    python tools/collect_results.py              read GitHub, write results/
    python tools/collect_results.py --from FILE  read comments from a JSON file (for tests)

Results are comments in the tracking issue of each task (and issues titled
"[agent-result] ..." from people who publish by hand). For every unit of every
task the tool groups the results by their hash and by GitHub account:

  * confirmed   at least `redundancy` different accounts published the same hash;
  * single      fewer accounts so far;
  * CONFLICT    different accounts published different hashes: a bug or a forgery.
                A maintainer recomputes the unit; the computation is deterministic.

For the exit-scam search every reported "hit" (a strategy whose expected payout
exceeds honest leaving) is recomputed here exactly before it is listed.

It writes results/coverage.json (how many agreeing results each unit has; the
agents use it to prefer units that still lack results), results/summary.json
and results/REPORT.md. Reading public issues needs no token; a token (from the
GITHUB_TOKEN variable or "gh auth token") only raises the rate limit.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "agent"))

from skynet_agent import signed, submit, tasks, trust  # noqa: E402
from skynet_agent.kernels import exit_scam_a, lottery_b  # noqa: E402

API = "https://api.github.com"


def find_token():
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        return token
    gh = shutil.which("gh")
    if gh:
        try:
            done = subprocess.run([gh, "auth", "token"], capture_output=True, timeout=20)
            if done.returncode == 0:
                return done.stdout.decode("ascii", "replace").strip() or None
        except (OSError, subprocess.SubprocessError):
            pass
    return None


def api_get(path, token):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "skynet-collect"}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(API + path, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def paged(path, token, limit=100):
    out = []
    for page in range(1, limit + 1):
        sep = "&" if "?" in path else "?"
        items = api_get("%s%sper_page=100&page=%d" % (path, sep, page), token)
        out.extend(items)
        if len(items) < 100:
            break
    return out


def fetch_live(index, token):
    """Return a list of {"author", "body", "url"} from GitHub."""
    repo = "/repos/%s/%s" % (trust.REPO_OWNER, trust.REPO_NAME)
    found = []
    issues = sorted(set(t.get("issue", 0) for t in index["tasks"] if t.get("issue", 0) > 0))
    for number in issues:
        for c in paged("%s/issues/%d/comments" % (repo, number), token):
            found.append({"author": (c.get("user") or {}).get("login", ""),
                          "body": c.get("body") or "", "url": c.get("html_url", "")})
    for issue in paged("%s/issues?state=all" % repo, token, limit=20):
        if "pull_request" in issue:
            continue
        if str(issue.get("title", "")).startswith("[agent-result]"):
            found.append({"author": (issue.get("user") or {}).get("login", ""),
                          "body": issue.get("body") or "", "url": issue.get("html_url", "")})
    return found


def collect(index, comments):
    """Group valid results. Returns {task id: {unit: {hash: {"authors": set, "record": r, "texts": []}}}}."""
    known = dict((t["id"], t) for t in index["tasks"])
    grouped = {}
    rejected = 0
    for c in comments:
        items = submit.parse_all(c.get("body", ""))
        if not items:
            if submit.MARKER in str(c.get("body", "")):
                rejected += 1
            continue
        for record, text in items:
            task = known.get(record["task"])
            if (task is None or not 0 <= record["unit"] < task["units"]
                    or record["kernel"] != "%s@%d" % (task["kernel"], task["kernel_version"])):
                rejected += 1
                continue
            slot = grouped.setdefault(task["id"], {}).setdefault(record["unit"], {})
            entry = slot.setdefault(record["result_sha256"],
                                    {"authors": set(), "record": record, "texts": []})
            entry["authors"].add(c.get("author") or "?")
            if text is not None:
                entry["texts"].append({"author": c.get("author") or "?",
                                       "model": record["result"].get("model", ""),
                                       "text": text, "url": c.get("url", "")})
    return grouped, rejected


def verify_hit(task, q, hit):
    """Recompute one reported hit exactly. True if it really beats honest leaving."""
    try:
        num, den = exit_scam_a.evaluate_path(task["params"], [tuple(s) for s in hit["path"]], q=q)
    except (ValueError, TypeError, KeyError):
        return False
    return num > task["params"]["H0"] * den


def summarise(index, grouped):
    coverage, summary = {}, {}
    for task in index["tasks"]:
        tid = task["id"]
        need = task.get("redundancy", 2)
        units = grouped.get(tid, {})
        cov = {}
        confirmed, conflicts, hits = 0, [], []
        best = None
        answers = []
        table = []
        for unit in sorted(units):
            by_hash = units[unit]
            top_hash = max(by_hash, key=lambda h: (len(by_hash[h]["authors"]), h))
            agree = len(by_hash[top_hash]["authors"])
            cov[str(unit)] = agree
            if len(by_hash) > 1:
                conflicts.append({"unit": unit, "hashes": dict(
                    (h, sorted(e["authors"])) for h, e in sorted(by_hash.items()))})
            if agree >= need and len(by_hash) == 1:
                confirmed += 1
            result = by_hash[top_hash]["record"]["result"]
            if task["kernel"] == "exit-scam-a":
                for share in result.get("by_q", []) or []:
                    if not isinstance(share, dict):
                        continue
                    q = share.get("q")
                    key = json.dumps(q)
                    b = share.get("best")
                    if isinstance(b, dict) and isinstance(b.get("ev_ppb"), int):
                        if best is None:
                            best = {}
                        if key not in best or b["ev_ppb"] > best[key]["ev_ppb"]:
                            best[key] = {"q": q, "ev_ppb": b["ev_ppb"], "path": b.get("path"), "unit": unit}
                    reported = share.get("top_hits")
                    for hit in (reported if isinstance(reported, list) else [])[:exit_scam_a.TOP_HITS]:
                        if isinstance(hit, dict) and verify_hit(task, q, hit):
                            hits.append({"unit": unit, "q": q, "ev_ppb": hit.get("ev_ppb"),
                                         "path": hit.get("path")})
            if task["kernel"] == "lottery-b":
                reported = result.get("rows")
                for row in (reported if isinstance(reported, list) else [])[:lottery_b.MAX_CELLS_PER_UNIT]:
                    if isinstance(row, list) and len(row) == 8 and all(isinstance(v, int) for v in row):
                        table.append(row)
            for e in by_hash.values():
                answers.extend(e["texts"])
        coverage[tid] = cov
        entry = {"kernel": "%s@%d" % (task["kernel"], task["kernel_version"]),
                 "units": task["units"], "units_with_results": len(units),
                 "units_confirmed": confirmed, "redundancy": need, "conflicts": conflicts}
        if task["kernel"] == "exit-scam-a":
            hits.sort(key=lambda h: -(h["ev_ppb"] or 0))
            entry["verified_hits"] = hits[:50]
            # best strategy found so far for each collusion share, in the order of the task
            order = [json.dumps(q) for q in exit_scam_a.shares(task["params"])]
            entry["best_by_q"] = [best[k] for k in order if best and k in best]
            entry["lowest_q_with_hit"] = None
            hit_shares = [h["q"] for h in hits if isinstance(h.get("q"), list) and len(h["q"]) == 2]
            if hit_shares:
                entry["lowest_q_with_hit"] = min(hit_shares, key=lambda q: q[0] / q[1])
        if task["kernel"] == "lottery-b":
            # the cells reported so far (from the most agreed result of each unit)
            entry["columns"] = ["tasks", "check_one_in", "cost_num", "cost_den", "months",
                                "loss_ppb", "half_ppb", "zero_ppb"]
            entry["rows"] = sorted(table)
        if answers:
            entry["answers"] = len(answers)
        summary[tid] = entry
        summary[tid]["_answers"] = answers
    return coverage, summary


def write_outputs(root, index, coverage, summary, rejected):
    out_dir = os.path.join(root, "results")
    os.makedirs(os.path.join(out_dir, "ai"), exist_ok=True)
    lines = ["# Agent results", "",
             "Generated by `tools/collect_results.py` from public comments. "
             "Task list number %d. Rejected malformed results: %d." % (index["seq"], rejected), "",
             "| Task | Kernel | Units | With results | Confirmed | Conflicts | Verified hits |",
             "|---|---|---:|---:|---:|---:|---:|"]
    for tid, entry in summary.items():
        answers = entry.pop("_answers")
        lines.append("| %s | %s | %d | %d | %d | %d | %s |" % (
            tid, entry["kernel"], entry["units"], entry["units_with_results"],
            entry["units_confirmed"], len(entry["conflicts"]),
            len(entry["verified_hits"]) if "verified_hits" in entry else "-"))
        if answers:
            doc = ["# Answers of local AI models: %s" % tid, "",
                   "Machine-generated and not verified. Collected from public comments.", ""]
            for a in answers:
                doc += ["## %s, model `%s`" % (a["author"], a["model"]), "", a["url"], "",
                        "~~~~~~~~text", a["text"], "~~~~~~~~", ""]
            with open(os.path.join(out_dir, "ai", tid + ".md"), "w", encoding="utf-8", newline="\n") as f:
                f.write("\n".join(doc))
    lines.append("")
    for tid, entry in summary.items():
        if entry.get("verified_hits"):
            lines += ["## Hits in %s" % tid, "",
                      "Strategies whose exact expected payout exceeds honest leaving (recomputed here):", ""]
            for hit in entry["verified_hits"][:10]:
                lines.append("- unit %d, collusion share %s: path %s, expected payout %.6f of H0" % (
                    hit["unit"], "/".join(str(x) for x in hit["q"]), json.dumps(hit["path"]),
                    (hit["ev_ppb"] or 0) / 1e9))
            if entry.get("lowest_q_with_hit"):
                lines.append("")
                lines.append("Lowest collusion share with a verified hit so far: %s" % (
                    "/".join(str(x) for x in entry["lowest_q_with_hit"])))
            lines.append("")
        for conflict in entry["conflicts"]:
            lines += ["## CONFLICT in %s unit %d" % (tid, conflict["unit"]), "",
                      "Different accounts published different results. Recompute this unit.", ""]
    for name, obj in (("coverage.json", coverage), ("summary.json", summary)):
        with open(os.path.join(out_dir, name), "w", encoding="utf-8", newline="\n") as f:
            json.dump(obj, f, indent=1, sort_keys=True)
            f.write("\n")
    with open(os.path.join(out_dir, "REPORT.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=os.path.join(HERE, ".."))
    parser.add_argument("--from", dest="source", help="JSON file with [{author, body, url}, ...]")
    args = parser.parse_args(argv)
    root = os.path.abspath(args.root)
    with open(os.path.join(root, "tasks", "index.json"), "rb") as f:
        index = signed.strict_json_loads(f.read())
    tasks.validate_index(index)
    if args.source:
        with open(args.source, "r", encoding="utf-8") as f:
            comments = json.load(f)
    else:
        try:
            comments = fetch_live(index, find_token())
        except (urllib.error.URLError, OSError, ValueError) as e:
            print("Cannot read GitHub: %s" % e)
            return 1
    grouped, rejected = collect(index, comments)
    coverage, summary = summarise(index, grouped)
    write_outputs(root, index, coverage, summary, rejected)
    total = sum(len(u) for u in grouped.values())
    print("Read %d comment(s): %d unit(s) with results, %d rejected. Wrote results/." % (
        len(comments), total, rejected))
    return 0


if __name__ == "__main__":
    sys.exit(main())
