"""Sending signed records out and collecting them back, over every channel at once.

Channels: public Nostr relays (nostr.py) and receivers, which are small HTTP
services run by participants on full nodes (node/receiver.py):

    POST <receiver>/v1/records              body: one record (JSON)
                                            -> {"ok": true, "id": <id>, "new": ...}
    GET  <receiver>/v1/records?after=N      -> {"next": M, "records": [...]}

A record counts as delivered when one receiver confirmed this very id or when at
least nostr.MIN_ACCEPTED relays confirmed its event. A confirmation is a promise
of a stranger, not proof of storage: the device keeps its own copy in
<folder>/records.jsonl, and every store keeps its own reading positions next to it.
"""

import json
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from . import config, net, nostr, records, signed, trust

MAX_LOCAL_BYTES = 256 << 20     # a device keeps at most this much of the history
PAGE_LIMIT = 200
PAGE_BYTES = 12 << 20


def receivers():
    env = os.environ.get("SKYNET_AGENT_RECEIVERS")
    items = env.split(",") if env is not None else list(trust.RECEIVERS)
    out = []
    for r in items:
        r = r.strip().rstrip("/")
        if r and r != "none" and r not in out:
            out.append(r)
    return out


# ---------------------------------------------------------------- local copy

class Store:
    """Append-only file of verified records and the reading positions for this file."""

    def __init__(self, folder=None, max_bytes=MAX_LOCAL_BYTES):
        self.folder = folder or config.path("net")
        self.file = os.path.join(self.folder, "records.jsonl")
        self.cursor_file = os.path.join(self.folder, "cursors.json")
        self.max_bytes = max_bytes
        self.items = {}
        self.size = 0
        self.lock = threading.Lock()
        os.makedirs(self.folder, exist_ok=True)
        try:
            with open(self.file, "rb") as f:
                data = f.read()
        except FileNotFoundError:
            data = b""
        if data and not data.endswith(b"\n"):
            # a crash in the middle of a line: drop the broken tail so that the next
            # record does not get glued to it
            keep = data.rfind(b"\n") + 1
            with open(self.file, "r+b") as f:
                f.truncate(keep)
            data = data[:keep]
        for line in data.split(b"\n"):
            if not line:
                continue
            try:
                env = records.parse(line, now=float("inf"))
            except records.RecordError:
                continue
            if env["id"] not in self.items:
                self.items[env["id"]] = env
                self.size += len(line) + 1

    def add(self, envelope):
        """Store a verified record. Returns "new", "known" or "full"."""
        data = records.wire(envelope) + b"\n"
        with self.lock:
            if envelope["id"] in self.items:
                return "known"
            if self.size + len(data) > self.max_bytes:
                return "full"
            with open(self.file, "ab") as f:
                f.write(data)
                f.flush()
                try:
                    os.fsync(f.fileno())
                except OSError:
                    pass
            self.items[envelope["id"]] = envelope
            self.size += len(data)
            return "new"

    def all(self):
        return list(self.items.values())

    def cursors(self):
        data = config.read_json(self.cursor_file, {})
        return data if isinstance(data, dict) else {}

    def save_cursors(self, cursors):
        config.write_json_atomic(self.cursor_file, cursors)


# ---------------------------------------------------------------- receivers

def post_to_receiver(base, envelope):
    try:
        status, body, _ = net.request(base + "/v1/records", method="POST", data=records.wire(envelope),
                                      headers={"Content-Type": "application/json"}, timeout=30,
                                      max_bytes=65536, follow_redirects=False)
    except net.NetError as e:
        return False, str(e)[:200]
    if status != 200:
        return False, "HTTP %d %s" % (status, body[:120].decode("utf-8", "replace"))
    try:
        answer = signed.strict_json_loads(body)
    except (ValueError, UnicodeError, RecursionError):
        return False, "the receiver gave no proper answer"
    if isinstance(answer, dict) and answer.get("ok") is True and answer.get("id") == envelope["id"]:
        return True, ""
    return False, "the receiver did not confirm this record"


def fetch_from_receiver(base, after=0, max_pages=20):
    """Return (verified records, next cursor, error text or "").

    The cursor stops before a record that is dated in the future (it is asked for again
    later) and never moves further than the records actually returned.
    """
    out = []
    for _ in range(max_pages):
        try:
            raw = net.get("%s/v1/records?after=%d&limit=%d" % (base, after, PAGE_LIMIT),
                          max_bytes=PAGE_BYTES, timeout=60)
            page = signed.strict_json_loads(raw)
            items, nxt = page["records"], page["next"]
            if not isinstance(items, list) or type(nxt) is not int or len(items) > PAGE_LIMIT \
                    or nxt != after + len(items):
                raise ValueError("bad page")
        except (net.NetError, ValueError, KeyError, TypeError, UnicodeError, RecursionError) as e:
            return out, after, str(e)[:200] or type(e).__name__
        for i, item in enumerate(items):
            try:
                out.append(records.verify(item))
            except records.RecordFromFuture:
                return out, after + i, ""
            except records.RecordError:
                pass                    # broken for good: skip it
        if not items:
            break
        after = nxt
    return out, after, ""


# ---------------------------------------------------------------- everything at once

def send(envelope, seed, log=None):
    """Send one record everywhere. Returns (delivered, human readable summary)."""
    bases, relay_list = receivers(), nostr.relays()
    event = nostr.make_event(nostr.secret_from_seed(seed), envelope) if relay_list else None
    jobs = []
    with ThreadPoolExecutor(max_workers=max(1, len(bases) + len(relay_list))) as pool:
        for base in bases:
            jobs.append(("receiver", base, pool.submit(post_to_receiver, base, envelope)))
        for relay in relay_list:
            jobs.append(("relay", relay, pool.submit(nostr.publish, relay, event)))
    ok = {"receiver": 0, "relay": 0}
    for kind, where, fut in jobs:
        try:
            good, why = fut.result()
        except Exception as e:      # a channel must never break the agent
            good, why = False, "%s: %s" % (type(e).__name__, e)
        if good:
            ok[kind] += 1
        elif log is not None:
            log.debug("%s %s did not take the record: %s", kind, where, why)
    delivered = ok["receiver"] >= 1 or ok["relay"] >= nostr.MIN_ACCEPTED
    return delivered, "%d of %d receivers, %d of %d relays" % (ok["receiver"], len(bases), ok["relay"], len(relay_list))


RELAY_OVERLAP = 3600            # ask again for the last hour: relays deliver late


def sync(store, log=None, now=None):
    """Pull new records from every channel into the store. Returns how many were new.

    Every receiver and every relay has its own position. A relay's position moves only
    when it gave everything it has since that position (nostr.fetch_all).
    """
    now = int(time.time() if now is None else now)
    cursors = store.cursors()
    new = 0
    full = False

    def take(envs):
        nonlocal new, full
        for env in envs:
            outcome = store.add(env)
            if outcome == "new":
                new += 1
            elif outcome == "full":
                full = True

    for base in receivers():
        key = "receiver " + base
        try:
            got, nxt, err = fetch_from_receiver(base, int(cursors.get(key, 0)))
        except Exception as e:      # one bad source must not stop the others
            got, nxt, err = [], int(cursors.get(key, 0)), "%s: %s" % (type(e).__name__, e)
        take(got)
        if not full:
            cursors[key] = nxt
        if err and log is not None:
            log.debug("receiver %s: %s", base, err)
    relay_list = nostr.relays()
    if relay_list:
        def one(relay):
            since = max(0, int(cursors.get("relay " + relay, 0)) - RELAY_OVERLAP)
            try:
                return nostr.fetch_all(relay, since=since)
            except Exception as e:
                return [], False
        with ThreadPoolExecutor(max_workers=len(relay_list)) as pool:
            results = list(pool.map(one, relay_list))
        for relay, (got, complete) in zip(relay_list, results):
            take(got)
            if complete and not full:
                cursors["relay " + relay] = now
            elif log is not None:
                log.debug("relay %s: incomplete reading, will ask again", relay)
    store.save_cursors(cursors)
    if full and log is not None:
        log.warning("the local copy of the history is full (%d MB); older records are kept", store.max_bytes >> 20)
    return new
