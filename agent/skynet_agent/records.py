"""Signed records: the unit of everything a participant says to the network.

A record is a small JSON object signed with the participant's own Ed25519 key,
which is created on the device. No account anywhere is needed. The record does
not name the channel it travels through, so the same bytes can be sent to any
number of relays and receivers, and copies are recognised by their id.

    envelope = {"id": <hex>, "sig": <hex>, "body": {...}}
    body     = {"v": 1, "net": NET_ID, "type": ..., "author": <public key hex>,
                "created": <unix time>, "payload": {...}}
    id       = SHA-256("skynet-record:1\\n" + canonical(body))
    sig      = Ed25519 signature of the 32 id bytes by "author"

Types:

    result   one unit of a signed kernel task (payload.record is the same
             record the agent used to publish in a GitHub comment)
    task     a research task for people and AI assistants (free text)
    claim    "I am working on this task" - a notice only, it reserves nothing
    report   an answer to a task
    accept   the task's author accepts one report
    revise   the task's author sends one report back with remarks

Honest limits. A key costs nothing, so the number of keys that say the same
thing proves nothing: only a signature of a *particular* key (the author of a
task) or a recomputation gives a record weight. The time in a record is what
its author wrote; it is not proof of when the record was made. sign() uses the
pure Python Ed25519 of this package, which is not constant-time: a program that
can watch this device closely could learn the key. The key only gives
authorship of this device's own records.
"""

import hashlib
import json
import os
import re
import time

from . import config, ed25519, signed, trust

VERSION = 1
PREFIX = b"skynet-record:1\n"
MAX_WIRE_BYTES = 40000          # one record as UTF-8 JSON; fits the smallest relay limits seen
MAX_FUTURE_SECONDS = 86400      # a record dated further ahead than this waits
MAX_TIME = 2 ** 40              # any unix time above this is nonsense
TYPES = ("result", "task", "claim", "report", "accept", "revise")

_HEX64 = re.compile(r"[0-9a-f]{64}")
_HEX128 = re.compile(r"[0-9a-f]{128}")


class RecordError(Exception):
    pass


class RecordFromFuture(RecordError):
    """Correct in every other way but dated too far ahead: try again later."""


def canonical(obj):
    """The exact text that is hashed: sorted keys, no spaces, ASCII only."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def wire(envelope):
    """The bytes sent over a channel (UTF-8, so that non-Latin text stays small)."""
    return json.dumps(envelope, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def record_id(body):
    return hashlib.sha256(PREFIX + canonical(body).encode("ascii")).hexdigest()


def is_hex64(x):
    return isinstance(x, str) and _HEX64.fullmatch(x) is not None


# ---------------------------------------------------------------- identity

def identity_file():
    return config.path("identity.key")


def _read_seed(name):
    with open(name, "r", encoding="ascii") as f:
        text = f.readline().strip()
    if not is_hex64(text):
        raise RecordError("the identity file %s is damaged; restore it from your backup "
                          "(a new key would be a different author)" % name)
    return bytes.fromhex(text)


def load_seed(create=True):
    """Return this device's 32-byte secret seed; create it on first use.

    The new key is written to a temporary file first and then linked under the final
    name, which fails if another process got there first: then its key is used. A half
    written key file can therefore never appear under the final name.
    """
    name = identity_file()
    try:
        return _read_seed(name)
    except FileNotFoundError:
        if not create:
            return None
    except (OSError, ValueError, UnicodeDecodeError) as e:
        raise RecordError("cannot read the identity file %s: %s" % (name, e))
    config.ensure_dirs()
    tmp = "%s.%d.%s.tmp" % (name, os.getpid(), os.urandom(4).hex())
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="ascii") as f:
            f.write(os.urandom(32).hex() + "\n")
            f.flush()
            os.fsync(f.fileno())
        try:
            os.link(tmp, name)
        except FileExistsError:
            pass                      # another process created the key a moment earlier
        except OSError:
            if not os.path.exists(name):
                os.replace(tmp, name)    # file systems without hard links (rare)
    finally:
        try:
            os.unlink(tmp)
        except OSError:
            pass
    try:
        return _read_seed(name)
    except (OSError, ValueError, UnicodeDecodeError) as e:
        raise RecordError("cannot read the identity file %s: %s" % (name, e))


def public_hex(seed):
    return ed25519.public_key(seed).hex()


# ---------------------------------------------------------------- payload rules

def _is_int(x):
    return type(x) is int


def _text(payload, key, limit, required=True):
    value = payload.get(key)
    if value is None and not required:
        return
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise RecordError("%s must be text of 1..%d characters" % (key, limit))


def _ref(payload, key, required=True):
    value = payload.get(key)
    if value is None and not required:
        return
    if not is_hex64(value):
        raise RecordError("%s must be a record id" % key)


def _only(payload, allowed):
    extra = set(payload) - set(allowed)
    if extra:
        raise RecordError("unknown fields: %s" % ", ".join(sorted(str(k) for k in extra)))


def _check_result(p):
    _only(p, ("record", "text"))
    from . import submit            # late: submit imports this module
    rec = p.get("record")
    if not isinstance(rec, dict) or submit._check_record(canonical(rec)) is None:
        raise RecordError("payload.record is not a valid result")
    text = p.get("text")
    if "output_sha256" in rec["result"]:
        if not isinstance(text, str):
            raise RecordError("an AI answer must carry its text")
        if hashlib.sha256(text.encode("utf-8")).hexdigest() != rec["result"]["output_sha256"]:
            raise RecordError("the text does not match its fingerprint")
    elif text is not None:
        raise RecordError("only an AI answer carries text")


def _check_task(p):
    _only(p, ("title", "text", "accept", "base", "parent", "deputies", "handover_days", "lang"))
    _text(p, "title", 200)
    _text(p, "text", 20000)
    _text(p, "accept", 4000)
    _text(p, "base", 200, required=False)
    _text(p, "lang", 16, required=False)
    _ref(p, "parent", required=False)
    deputies = p.get("deputies", [])
    if not isinstance(deputies, list) or len(deputies) > 5 or not all(is_hex64(d) for d in deputies) \
            or len(set(deputies)) != len(deputies):
        raise RecordError("deputies must be up to 5 different public keys")
    if not all(ed25519.is_strong_public(bytes.fromhex(d)) for d in deputies):
        raise RecordError("a deputy key is not a usable public key")
    days = p.get("handover_days", 14)
    if not _is_int(days) or not 1 <= days <= 365:
        raise RecordError("handover_days must be 1..365")


def _check_claim(p):
    _only(p, ("task", "until"))
    _ref(p, "task")
    if not _is_int(p.get("until")) or not 0 < p["until"] < MAX_TIME:
        raise RecordError("until must be a unix time")


def _check_report(p):
    _only(p, ("task", "summary", "text", "revises"))
    _ref(p, "task")
    _ref(p, "revises", required=False)
    _text(p, "summary", 2000)
    _text(p, "text", 30000)


def _check_verdict(p):
    _only(p, ("task", "report", "note"))
    _ref(p, "task")
    _ref(p, "report")
    _text(p, "note", 4000, required=False)


_CHECKS = {"result": _check_result, "task": _check_task, "claim": _check_claim,
           "report": _check_report, "accept": _check_verdict, "revise": _check_verdict}


# ---------------------------------------------------------------- make / verify

def make(seed, rtype, payload, created=None):
    """Build and sign an envelope. Raises RecordError if it would not be accepted."""
    body = {"v": VERSION, "net": trust.NET_ID, "type": rtype, "author": public_hex(seed),
            "created": int(time.time() if created is None else created), "payload": payload}
    try:
        rid = record_id(body)
    except (TypeError, ValueError) as e:
        raise RecordError("record cannot be encoded: %s" % e)
    envelope = {"id": rid, "sig": ed25519.sign(seed, bytes.fromhex(rid)).hex(), "body": body}
    return verify(envelope)


def verify(envelope, now=None):
    """Return the envelope if it is well formed and correctly signed, else raise RecordError.

    RecordFromFuture means: correct, but dated more than a day ahead of this clock.
    """
    try:
        return _verify(envelope, now)
    except RecordError:
        raise
    except (TypeError, ValueError, KeyError, AttributeError, RecursionError, UnicodeError) as e:
        raise RecordError("malformed record: %s" % type(e).__name__)


def _verify(envelope, now):
    if not isinstance(envelope, dict) or set(envelope) != {"id", "sig", "body"}:
        raise RecordError("not a record")
    body = envelope["body"]
    if not isinstance(body, dict) or set(body) != {"v", "net", "type", "author", "created", "payload"}:
        raise RecordError("bad record body")
    if not _is_int(body["v"]) or body["v"] != VERSION:
        raise RecordError("unknown record version")
    if body["net"] != trust.NET_ID:
        raise RecordError("record of another network")
    if body["type"] not in TYPES:
        raise RecordError("unknown record type")
    if not is_hex64(body["author"]):
        raise RecordError("bad author key")
    if not _is_int(body["created"]) or not 0 < body["created"] < MAX_TIME:
        raise RecordError("bad time")
    if not isinstance(body["payload"], dict):
        raise RecordError("bad payload")
    if not is_hex64(envelope["id"]) or not isinstance(envelope["sig"], str) \
            or _HEX128.fullmatch(envelope["sig"]) is None:
        raise RecordError("bad id or signature field")
    if len(wire(envelope)) > MAX_WIRE_BYTES:
        raise RecordError("record larger than %d bytes" % MAX_WIRE_BYTES)
    if record_id(body) != envelope["id"]:
        raise RecordError("id does not match the content")
    _CHECKS[body["type"]](body["payload"])
    author = bytes.fromhex(body["author"])
    if not ed25519.is_strong_public(author):
        raise RecordError("the author key is not a usable public key")
    if not ed25519.verify(author, bytes.fromhex(envelope["id"]), bytes.fromhex(envelope["sig"])):
        raise RecordError("bad signature")
    now = time.time() if now is None else now
    if body["created"] > now + MAX_FUTURE_SECONDS:
        raise RecordFromFuture("dated in the future")
    return envelope


def parse(data, now=None):
    """Parse bytes or text received from a channel and verify. Raises RecordError."""
    try:
        if isinstance(data, str):
            data = data.encode("utf-8")
        if not isinstance(data, (bytes, bytearray)) or len(data) > MAX_WIRE_BYTES + 1024:
            raise RecordError("record too large")
        envelope = signed.strict_json_loads(data)
    except RecordError:
        raise
    except (ValueError, UnicodeError, RecursionError, TypeError) as e:
        raise RecordError("not JSON: %s" % type(e).__name__)
    return verify(envelope, now=now)
