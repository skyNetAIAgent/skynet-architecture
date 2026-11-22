"""Results: how they are written down, kept in the outbox and published.

A result is published as a comment in the task's tracking issue on GitHub,
under the participant's own account. The comment has a fixed, machine-readable
shape (see format_comment / parse_comment) so that anyone can collect and
compare results. Nothing else leaves the device.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import time
import urllib.parse

from . import RELEASE_SEQ, __version__, config, net, power, signed, trust

MARKER = "<!-- skynet-agent-result:1 -->"
FENCE = "~~~~~~~~"
MAX_COMMENT_CHARS = 60000
MAX_RECORDS_PER_COMMENT = 50
MAX_URL_CHARS = 7000
MAX_OUTBOX = 300          # with this many unpublished results the agent stops taking work
_JSON_BLOCK_RE = re.compile(r"```json\n(.*?)\n```", re.DOTALL)
_TEXT_BLOCK_RE = re.compile(r"\n" + FENCE + r"text\n(.*?)\n" + FENCE + r"(?:\n|$)", re.DOTALL)
_MODEL_RE = re.compile(r"[^A-Za-z0-9._:/@+-]")


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def result_hash(result):
    return hashlib.sha256(canonical(result).encode("ascii")).hexdigest()


def safe_text(text):
    """Make model output safe to put inside our fenced block."""
    return re.sub(r"~{8,}", "~~~~~~~", text)


def make_record(task, unit, outcome, cfg):
    """Build the publishable record from a successful worker outcome."""
    result = dict(outcome["result"])
    record = {
        "v": 1,
        "task": task["id"],
        "unit": unit,
        "units": task["units"],
        "kernel": "%s@%d" % (task["kernel"], task["kernel_version"]),
        "agent": __version__,
        "seq": RELEASE_SEQ,
        "elapsed_s": outcome.get("elapsed_s", 0),
    }
    if cfg.get("report_platform", True):
        record["platform"] = power.platform_tag()
    text = None
    if "output" in result and isinstance(result["output"], str):
        text = safe_text(result.pop("output"))
        result["output_sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
        result["chars"] = len(text)
        if "model" in result:
            result["model"] = _MODEL_RE.sub("_", str(result["model"]))[:120]
    record["result"] = result
    record["result_sha256"] = result_hash(result)
    return record, text


def format_batch(records):
    """One comment with several results. Raises ValueError if it would be too large."""
    if not records or len(records) > MAX_RECORDS_PER_COMMENT:
        raise ValueError("a comment holds 1..%d results" % MAX_RECORDS_PER_COMMENT)
    lines = [MARKER,
             "SkyNet research agent · %d result(s) · agent %s" % (len(records), records[0]["agent"])]
    for record in records:
        lines += ["",
                  "`%s` unit %d of %d" % (record["task"], record["unit"], record["units"]),
                  "",
                  "```json",
                  canonical(record),
                  "```"]
    body = "\n".join(lines) + "\n"
    if len(body) > MAX_COMMENT_CHARS:
        raise ValueError("results are too large to publish together (%d characters)" % len(body))
    return body


def format_comment(record, text=None):
    """One comment with one result (and, for an AI answer, its text)."""
    body = format_batch([record])
    if text is not None:
        body += "\n".join([
            "",
            "Machine-generated answer of a local AI model. Nobody has verified it.",
            "",
            FENCE + "text",
            text,
            FENCE,
        ]) + "\n"
    if len(body) > MAX_COMMENT_CHARS:
        raise ValueError("result is too large to publish (%d characters)" % len(body))
    return body


def _check_record(raw):
    try:
        record = signed.strict_json_loads(raw)
    except (ValueError, UnicodeDecodeError):
        return None
    if not isinstance(record, dict) or record.get("v") != 1:
        return None
    for key, kind in (("task", str), ("kernel", str), ("agent", str), ("result", dict),
                      ("result_sha256", str), ("unit", int), ("units", int)):
        if not isinstance(record.get(key), kind) or isinstance(record.get(key), bool):
            return None
    if result_hash(record["result"]) != record["result_sha256"]:
        return None
    return record


def parse_all(body):
    """Return [(record, text), ...]: every valid result in a comment body. text is None
    except for an AI answer, which always travels alone in its comment."""
    if not isinstance(body, str) or MARKER not in body:
        return []
    body = body.replace("\r\n", "\n")
    # everything after the text fence is model output and is never parsed for records
    head, fence, _ = body.partition("\n" + FENCE + "text\n")
    blocks = _JSON_BLOCK_RE.findall(head)[:MAX_RECORDS_PER_COMMENT]
    out = []
    for raw in blocks:
        record = _check_record(raw)
        if record is None:
            continue
        text = None
        if "output_sha256" in record["result"]:
            t = _TEXT_BLOCK_RE.search(body)
            if len(blocks) != 1 or not fence or not t:
                continue
            text = t.group(1)
            if hashlib.sha256(text.encode("utf-8")).hexdigest() != record["result"]["output_sha256"]:
                continue
        out.append((record, text))
    return out


def parse_comment(body):
    """Return (record, text) if the body holds exactly one valid result, else None."""
    items = parse_all(body)
    return items[0] if len(items) == 1 else None


# ---------------------------------------------------------------- outbox

def save_to_outbox(task, record, text, kind):
    config.ensure_dirs()
    entry = {
        "record": record,
        "text": text,
        "issue": task.get("issue", 0),
        "kind": kind,
        "created": int(time.time()),
        "approved": kind != "ai",
    }
    name = "%d-%s-%d.json" % (int(time.time() * 1000), record["task"], record["unit"])
    config.write_json_atomic(config.path("outbox", name), entry)
    return name


def outbox_entries():
    """Return [(file name, entry)] oldest first."""
    folder = config.path("outbox")
    out = []
    try:
        names = sorted(n for n in os.listdir(folder) if n.endswith(".json"))
    except OSError:
        return out
    for name in names:
        entry = config.read_json(os.path.join(folder, name))
        if isinstance(entry, dict) and isinstance(entry.get("record"), dict):
            out.append((name, entry))
    return out


def outbox_count():
    """How many results wait in the outbox (cheap: does not read the files)."""
    try:
        return sum(1 for n in os.listdir(config.path("outbox")) if n.endswith(".json"))
    except OSError:
        return 0


def _move_to_sent(name, entry, url):
    entry["published"] = url
    entry["published_at"] = int(time.time())
    config.write_json_atomic(config.path("sent", name), entry)
    try:
        os.unlink(config.path("outbox", name))
    except OSError:
        pass
    # keep the folder small
    sent = sorted(os.listdir(config.path("sent")))
    for old in sent[:-300]:
        try:
            os.unlink(config.path("sent", old))
        except OSError:
            pass


# ---------------------------------------------------------------- GitHub

def api_base():
    return (os.environ.get("SKYNET_AGENT_API_URL") or trust.API_BASE).rstrip("/")


def find_token():
    """Return (token, where it came from) or (None, reason). The token is never stored by us."""
    token = os.environ.get("SKYNET_GITHUB_TOKEN", "").strip()
    if token:
        return token, "the SKYNET_GITHUB_TOKEN environment variable"
    token_file = config.path("github-token")
    try:
        with open(token_file, "r", encoding="ascii") as f:
            token = f.readline().strip()
        if token:
            return token, "the file %s" % token_file
    except (OSError, UnicodeDecodeError):
        pass
    gh = shutil.which("gh")
    if gh:
        try:
            flags = getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0
            done = subprocess.run([gh, "auth", "token"], capture_output=True, timeout=20,
                                  creationflags=flags)
            token = done.stdout.decode("ascii", "replace").strip()
            if done.returncode == 0 and token:
                return token, "GitHub CLI (gh)"
        except (OSError, subprocess.SubprocessError):
            pass
        return None, "GitHub CLI is installed but not logged in (run: gh auth login)"
    return None, "no GitHub login found (install GitHub CLI and run: gh auth login)"


def _api_headers(token):
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = "Bearer " + token
    return headers


def _api_message(body):
    try:
        data = json.loads(body.decode("utf-8", "replace"))
        if isinstance(data, dict) and isinstance(data.get("message"), str):
            return data["message"][:200]
    except ValueError:
        pass
    return ""


def whoami(token):
    """Return the GitHub login for a token, or raise NetError."""
    url = api_base() + "/user"
    if not net.is_private_safe(url):
        raise net.NetError("refusing to send a token over an unencrypted connection")
    status, body, _ = net.request(url, headers=_api_headers(token), follow_redirects=False)
    if status != 200:
        raise net.NetError("GitHub answered HTTP %d %s" % (status, _api_message(body)))
    return str(json.loads(body.decode("utf-8")).get("login", ""))


def post_comment(token, issue, body):
    """Publish one comment. Returns (True, url) or (False, reason)."""
    url = "%s/repos/%s/%s/issues/%d/comments" % (api_base(), trust.REPO_OWNER, trust.REPO_NAME, issue)
    if not net.is_private_safe(url):
        return False, "refusing to send a token over an unencrypted connection"
    headers = _api_headers(token)
    headers["Content-Type"] = "application/json"
    try:
        status, resp, _ = net.request(url, method="POST",
                                      data=json.dumps({"body": body}).encode("utf-8"),
                                      headers=headers, timeout=60, follow_redirects=False)
    except net.NetError as e:
        return False, str(e)
    if status == 201:
        try:
            return True, str(json.loads(resp.decode("utf-8")).get("html_url", ""))
        except ValueError:
            return True, ""
    return False, "GitHub answered HTTP %d %s" % (status, _api_message(resp))


def count_results(issue, token=None, max_pages=10):
    """How many agent results the tracking issue already has, or None if unknown."""
    total = 0
    for page in range(1, max_pages + 1):
        url = "%s/repos/%s/%s/issues/%d/comments?per_page=100&page=%d" % (
            api_base(), trust.REPO_OWNER, trust.REPO_NAME, issue, page)
        if token and not net.is_private_safe(url):
            token = None
        try:
            status, body, _ = net.request(url, headers=_api_headers(token), max_bytes=8 << 20,
                                          follow_redirects=False)
            if status != 200:
                return None
            items = json.loads(body.decode("utf-8", "replace"))
        except (net.NetError, ValueError):
            return None
        if not isinstance(items, list):
            return None
        total += sum(1 for it in items if isinstance(it, dict) and MARKER in str(it.get("body", "")))
        if len(items) < 100:
            break
    return total


def manual_issue_url(entry):
    """A link that opens a pre-filled new issue, for people without a token. None if too long."""
    record = entry["record"]
    try:
        body = format_comment(record, entry.get("text"))
    except ValueError:
        return None
    title = "[agent-result] %s unit %d" % (record["task"], record["unit"])
    url = "%s/issues/new?%s" % (trust.WEB_BASE, urllib.parse.urlencode({"title": title, "body": body}))
    return url if len(url) <= MAX_URL_CHARS else None


def _recent_submissions(state, now):
    recent = [t for t in state.get("submitted", []) if isinstance(t, int) and now - t < 86400]
    state["submitted"] = recent
    return len(recent)


def _pack(items, log):
    """Split [(name, entry)] into groups that each fit into one comment, keeping the order."""
    packs, current = [], []
    for name, entry in items:
        try:
            format_batch([entry["record"]])
        except ValueError as e:
            log.error("dropping %s: %s", name, e)
            _move_to_sent(name, entry, "dropped: %s" % e)
            continue
        try:
            format_batch([e["record"] for _, e in current] + [entry["record"]])
            current.append((name, entry))
        except ValueError:
            packs.append(current)
            current = [(name, entry)]
    if current:
        packs.append(current)
    return packs


def plan_comments(entries, cfg, state, log, issues=None, force=False, now=None):
    """Decide which comments to publish now. Returns [(issue, [(name, entry)], body)].

    Results of one tracking issue are published together: a comment that is full goes out
    at once, a partly filled one at most once per "batch_minutes" (so that an issue is not
    flooded with one comment per result), or at once when force is set. An AI answer
    always gets its own comment and waits for the participant's approval if required.
    """
    now = time.time() if now is None else now
    review = cfg.get("ai", {}).get("review_before_submit", True)
    wait = cfg.get("batch_minutes", 60) * 60
    plans = []
    groups = {}
    for name, entry in entries:
        issue = entry.get("issue", 0)
        if not isinstance(issue, int) or issue <= 0:
            issue = (issues or {}).get(entry["record"].get("task"), 0)
        if not isinstance(issue, int) or issue <= 0:
            continue
        if entry.get("kind") == "ai" or entry.get("text") is not None:
            if review and not entry.get("approved"):
                continue
            try:
                plans.append((issue, [(name, entry)], format_comment(entry["record"], entry.get("text"))))
            except ValueError as e:
                log.error("dropping %s: %s", name, e)
                _move_to_sent(name, entry, "dropped: %s" % e)
            continue
        groups.setdefault(issue, []).append((name, entry))
    for issue in sorted(groups):
        packs = _pack(groups[issue], log)
        last = state.get("last_post", {}).get(str(issue), 0)
        for i, pack in enumerate(packs):
            full = i < len(packs) - 1
            if full or force or now - last >= wait:
                plans.append((issue, pack, format_batch([e["record"] for _, e in pack])))
    return plans


def _publish_failed(state, now):
    """Remember a failed attempt: wait 1, 2, 4 ... 60 minutes before the next one."""
    fails = min(int(state.get("publish_fails", 0)) + 1, 10)
    state["publish_fails"] = fails
    state["publish_after"] = now + min(3600, 60 * 2 ** (fails - 1))


def flush_outbox(cfg, state, log, min_gap=2.0, issues=None, force=False):
    """Publish what may be published. Returns the number of results published now.

    issues: {task id: tracking issue number} from the current task list. It is used for
    results that were computed before their task had a tracking issue.

    After a failed attempt (no login, GitHub refused) the next one waits, longer each
    time, so that a device that cannot publish does not knock on GitHub after every
    finished unit. force (a command typed by the participant) skips the wait.
    """
    entries = outbox_entries()
    if not entries or cfg.get("submit") != "auto":
        return 0
    if not force and time.time() < state.get("publish_after", 0):
        return 0
    token = None
    published = 0
    for issue, pack, body in plan_comments(entries, cfg, state, log, issues=issues, force=force):
        now = int(time.time())
        if _recent_submissions(state, now) >= cfg.get("max_submissions_per_day", 48):
            log.info("daily publication limit reached; the rest stays in the outbox")
            break
        if token is None:
            token, source = find_token()
            if token is None:
                log.warning("results are waiting in the outbox: %s", source)
                state["last_error"] = source
                _publish_failed(state, now)
                break
        ok, info = post_comment(token, issue, body)
        if not ok:
            log.warning("could not publish %d result(s): %s", len(pack), info)
            state["last_error"] = info
            _publish_failed(state, now)
            break
        for name, entry in pack:
            _move_to_sent(name, entry, info)
        state["publish_fails"] = 0
        state["publish_after"] = 0
        state["submitted"].append(now)
        state.setdefault("last_post", {})[str(issue)] = now
        state["counters"]["published"] = state["counters"].get("published", 0) + len(pack)
        published += len(pack)
        log.info("published %d result(s) to issue %d: %s", len(pack), issue, info)
        time.sleep(min_gap)
    return published
