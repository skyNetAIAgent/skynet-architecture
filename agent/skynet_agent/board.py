"""The task board: research tasks that people and their AI assistants give each other.

Everything on the board is derived from signed records (records.py) that the
device has collected (transport.py). There is no server that decides: every
participant computes the same board from the same records with these rules.

    task     anyone may post one. Its author is the key that signed it.
    claim    "I am working on this" until a stated time. It reserves nothing:
             anyone may still hand in a report, so empty claims block nobody.
    report   anyone may answer a task, with or without a claim.
    accept / revise
             count only when signed by the task's author, or by one of the
             deputies the author named in the task once handover_days have
             passed since the task was posted (by this device's clock). The
             newest verdict of the author on a report wins; deputies' verdicts
             count only for reports the author has not judged.

A task is "accepted" when at least one of its reports is accepted. Nothing is
ever removed; a later "revise" on an accepted report reopens it.

Honest limits: a key is free, so the board can be filled with junk tasks and
reports, and nothing here proves who wrote a text first. Records dated in the
past cannot be told from old ones. This board is a research tool.
"""

import sys
import time

from . import config, records, transport

MAX_CLAIM_SECONDS = 30 * 86400


def build(envelopes, now=None):
    """Return {task id: info} computed from verified records."""
    now = time.time() if now is None else now
    tasks, by_id = {}, {}
    for env in envelopes:
        by_id[env["id"]] = env
        if env["body"]["type"] == "task":
            tasks[env["id"]] = {"task": env, "claims": [], "reports": [], "verdicts": {}, "accepted": []}
    ordered = sorted(envelopes, key=lambda e: (e["body"]["created"], e["id"]))
    latest_claim = {}                    # (task, author) -> the newest claim: a newer one replaces an older one
    for env in ordered:
        body, p = env["body"], env["body"]["payload"]
        info = tasks.get(p.get("task")) if body["type"] != "task" else None
        if info is None:
            continue
        if body["type"] == "claim":
            latest_claim[(p["task"], body["author"])] = env
        elif body["type"] == "report":
            info["reports"].append(env)
    for (task_id, _), env in sorted(latest_claim.items(), key=lambda kv: (kv[1]["body"]["created"], kv[1]["id"])):
        body = env["body"]
        if now < body["payload"]["until"] <= body["created"] + MAX_CLAIM_SECONDS:
            tasks[task_id]["claims"].append(env)
    for env in ordered:
        body, p = env["body"], env["body"]["payload"]
        if body["type"] not in ("accept", "revise"):
            continue
        info = tasks.get(p["task"])
        report = by_id.get(p["report"])
        if info is None or report is None or report["body"]["type"] != "report" \
                or report["body"]["payload"]["task"] != p["task"]:
            continue
        tbody = info["task"]["body"]
        if body["created"] < report["body"]["created"]:
            continue                                     # a verdict cannot be older than its report
        if body["author"] == tbody["author"]:
            rank = 2
        elif body["author"] in tbody["payload"].get("deputies", []) \
                and body["created"] >= handover_time(info["task"]) and now >= handover_time(info["task"]):
            rank = 1                                     # signed after the handover time, not merely read after it
        else:
            continue
        current = info["verdicts"].get(p["report"])
        if current is None or rank >= current[0]:       # ordered by time: the newest of the highest rank wins
            info["verdicts"][p["report"]] = (rank, env)
    for info in tasks.values():
        info["accepted"] = sorted(rid for rid, (_, env) in info["verdicts"].items()
                                  if env["body"]["type"] == "accept")
    return tasks


def handover_time(task):
    return task["body"]["created"] + task["body"]["payload"].get("handover_days", 14) * 86400


def status(info):
    if info["accepted"]:
        return "accepted"
    if info["reports"]:
        return "reported"
    if info["claims"]:
        return "claimed"
    return "open"


def find(store, prefix, rtype=None):
    """Return the one record whose id starts with prefix, or raise ValueError."""
    prefix = (prefix or "").lower()
    if len(prefix) < 6:
        raise ValueError("give at least 6 characters of the id")
    hits = [e for e in store.all() if e["id"].startswith(prefix) and (rtype is None or e["body"]["type"] == rtype)]
    if not hits:
        raise ValueError("no %s with an id starting with %s (try: skynet-agent net sync)" % (rtype or "record", prefix))
    if len(hits) > 1:
        raise ValueError("several records start with %s; give more characters" % prefix)
    return hits[0]


# ---------------------------------------------------------------- commands

def _read_text(name):
    if name == "-":
        return sys.stdin.buffer.read().decode("utf-8")
    with open(name, "r", encoding="utf-8-sig") as f:
        return f.read()


def _publish(say, seed, store, rtype, payload):
    env = records.make(seed, rtype, payload)
    # the retry entry first, then our own copy: nothing is lost if every channel is down
    config.write_json_atomic(config.path("net", "pending", env["id"] + ".json"), env)
    store.add(env)
    delivered, summary = transport.send(env, seed)
    if delivered:
        _forget_pending(env["id"])
    say("%s %s" % (rtype, env["id"]))
    say("  delivered: %s (%s)" % ("yes" if delivered else "NOT YET, will be retried by: skynet-agent net sync", summary))
    return env


def _forget_pending(rid):
    import os
    try:
        os.unlink(config.path("net", "pending", rid + ".json"))
    except OSError:
        pass


def resend_pending(seed, log=None):
    """Try again to deliver records that no channel confirmed. Returns how many got through."""
    import os
    folder = config.path("net", "pending")
    done = 0
    try:
        names = sorted(os.listdir(folder))
    except OSError:
        return 0
    for name in names[:200]:
        env = config.read_json(os.path.join(folder, name))
        try:
            records.verify(env)
        except records.RecordFromFuture:
            continue
        except records.RecordError:
            _forget_pending(name[:-5])
            continue
        delivered, _ = transport.send(env, seed, log=log)
        if delivered:
            _forget_pending(env["id"])
            done += 1
    return done


def clean(text):
    """Text from strangers, made safe for a terminal: no control characters."""
    return "".join(ch if ch in "\n\t" or (ord(ch) >= 32 and not 0x7f <= ord(ch) < 0xa0
                                          and ch not in "\u2028\u2029\u202a\u202b\u202c\u202d\u202e"
                                          "\u2066\u2067\u2068\u2069")
                   else "\ufffd" for ch in text)


def _short(text, n=70):
    text = " ".join(clean(text).split())
    return text if len(text) <= n else text[:n - 1] + "…"


def cmd_net(args, say):
    """Entry point of "skynet-agent net ...". Returns a process exit code."""
    import json
    action = args.action or "tasks"
    try:
        seed = records.load_seed()
        store = transport.Store()
        me = records.public_hex(seed)
        if action == "id":
            say("This device's public key (its name on the board):")
            say("  " + me)
            say("The secret key is in %s. Whoever copies that file can sign as this device." % records.identity_file())
            return 0
        if action == "sync":
            sent = resend_pending(seed)
            new = transport.sync(store)
            say("%d new record(s), %d waiting record(s) delivered, %d record(s) in the local copy." % (new, sent, len(store.all())))
            return 0
        if not args.offline:
            transport.sync(store)        # every command works on the freshest copy it can get
        tasks = build(store.all())
        if action == "tasks":
            rows = sorted(tasks.values(), key=lambda i: -i["task"]["body"]["created"])
            if args.json:
                say(json.dumps([{"id": i["task"]["id"], "status": status(i), "author": i["task"]["body"]["author"],
                                 "created": i["task"]["body"]["created"], "title": i["task"]["body"]["payload"]["title"],
                                 "claims": len(i["claims"]), "reports": len(i["reports"]), "accepted": i["accepted"]}
                                for i in rows], ensure_ascii=False, indent=1))
                return 0
            if not rows:
                say("No tasks on the board yet.")
            for i in rows:
                b = i["task"]["body"]
                say("%s  %-8s  %s  claims %d, reports %d%s  %s" % (
                    i["task"]["id"][:12], status(i), time.strftime("%Y-%m-%d", time.gmtime(b["created"])),
                    len(i["claims"]), len(i["reports"]), "  (mine)" if b["author"] == me else "", _short(b["payload"]["title"])))
            return 0
        if action == "show":
            env = find(store, args.ref)
            if args.json:
                info = tasks.get(env["id"])
                out = {"record": env}
                if info:
                    out.update({"status": status(info), "claims": info["claims"], "reports": info["reports"],
                                "verdicts": {k: v[1] for k, v in info["verdicts"].items()}, "accepted": info["accepted"]})
                say(json.dumps(out, ensure_ascii=False, indent=1))
                return 0
            b, p = env["body"], env["body"]["payload"]
            say("%s %s" % (b["type"], env["id"]))
            say("author  %s%s" % (b["author"], "  (this device)" if b["author"] == me else ""))
            say("created %s UTC" % time.strftime("%Y-%m-%d %H:%M", time.gmtime(b["created"])))
            if b["type"] == "task":
                info = tasks[env["id"]]
                say("status  %s" % status(info))
                say("title   %s" % _short(p["title"], 200))
                say("")
                say(clean(p["text"]))
                say("")
                say("Accepted when: %s" % clean(p["accept"]))
                for c in info["claims"]:
                    say("claim   by %s until %s UTC" % (c["body"]["author"][:12],
                                                        time.strftime("%Y-%m-%d %H:%M", time.gmtime(c["body"]["payload"]["until"]))))
                for r in info["reports"]:
                    verdict = info["verdicts"].get(r["id"])
                    say("report  %s by %s: %s  [%s]" % (r["id"][:12], r["body"]["author"][:12],
                                                        _short(r["body"]["payload"]["summary"], 60),
                                                        verdict[1]["body"]["type"] if verdict else "not judged"))
            elif b["type"] == "report":
                say("task    %s" % p["task"])
                say("summary %s" % clean(p["summary"]))
                say("")
                say(clean(p["text"]))
            else:
                say(json.dumps(p, ensure_ascii=False, indent=1))
            return 0
        if action == "post-task":
            if not args.title or not args.file or not args.accept:
                raise ValueError("post-task needs --title, --file and --accept")
            payload = {"title": args.title.strip(), "text": _read_text(args.file).strip(), "accept": args.accept.strip(),
                       "handover_days": args.handover_days}
            if args.deputy:
                payload["deputies"] = [d.lower() for d in args.deputy]
            if args.parent:
                payload["parent"] = find(store, args.parent, "task")["id"]
            if args.base:
                payload["base"] = args.base
            _publish(say, seed, store, "task", payload)
            return 0
        if action == "claim":
            task = find(store, args.ref, "task")
            _publish(say, seed, store, "claim", {"task": task["id"], "until": int(time.time()) + args.hours * 3600})
            return 0
        if action == "report":
            if not args.file or not args.summary:
                raise ValueError("report needs --file and --summary")
            task = find(store, args.ref, "task")
            payload = {"task": task["id"], "summary": args.summary.strip(), "text": _read_text(args.file).strip()}
            if args.revises:
                payload["revises"] = find(store, args.revises, "report")["id"]
            _publish(say, seed, store, "report", payload)
            return 0
        if action in ("accept", "revise"):
            report = find(store, args.ref, "report")
            task_id = report["body"]["payload"]["task"]
            task = store.items.get(task_id)
            if task is None:
                raise ValueError("the task of this report is not in the local copy (run: skynet-agent net sync)")
            tb = task["body"]
            if me != tb["author"] and me not in tb["payload"].get("deputies", []):
                raise ValueError("only the task's author or a deputy named in the task can judge its reports")
            if me != tb["author"] and time.time() < handover_time(task):
                raise ValueError("a deputy may judge only after %s UTC" % time.strftime(
                    "%Y-%m-%d %H:%M", time.gmtime(handover_time(task))))
            payload = {"task": task_id, "report": report["id"]}
            if args.note:
                payload["note"] = args.note.strip()
            elif action == "revise":
                raise ValueError("revise needs --note with the remarks")
            _publish(say, seed, store, action, payload)
            return 0
        raise ValueError("unknown action: %s" % action)
    except (ValueError, OSError, RecursionError, records.RecordError) as e:
        say("error: %s" % e)
        return 1
