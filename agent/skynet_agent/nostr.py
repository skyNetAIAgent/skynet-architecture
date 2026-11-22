"""Public Nostr relays as one of the channels for signed records.

A relay accepts a small signed event from any key and gives it to anyone who
asks. No account is needed. Standard library only: the BIP-340 signature
(Schnorr over secp256k1) and the WebSocket client are written out here.

What a relay is NOT: storage. It may drop events at any time and may refuse
them (payment, spam rules). The agent therefore sends every record to several
relays of different owners and counts a record as delivered only when at least
MIN_ACCEPTED of them (or a receiver) confirmed it. The Nostr key is derived
from the device's seed and carries no authority: a record is believed only
because of its inner Ed25519 signature (records.py).

Checked on 22 November 2026: 7 of 10 well-known open relays accepted an event
from a key created seconds earlier and returned it to a second connection.
How long they keep it is not known.
"""

import base64
import hashlib
import json
import os
import socket
import ssl
import struct
import time
import urllib.parse

from . import net, records, signed, trust

MIN_ACCEPTED = 2
TIMEOUT = 15

# ---------------------------------------------------------------- BIP-340

_P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
_G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
      0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)


def _padd(a, b):
    if a is None:
        return b
    if b is None:
        return a
    if a[0] == b[0] and a[1] != b[1]:
        return None
    if a == b:
        lam = 3 * a[0] * a[0] * pow(2 * a[1], _P - 2, _P) % _P
    else:
        lam = (b[1] - a[1]) * pow(b[0] - a[0], _P - 2, _P) % _P
    x = (lam * lam - a[0] - b[0]) % _P
    return x, (lam * (a[0] - x) - a[1]) % _P


def _pmul(point, n):
    out = None
    while n:
        if n & 1:
            out = _padd(out, point)
        point = _padd(point, point)
        n >>= 1
    return out


def _tagged(tag, msg):
    t = hashlib.sha256(tag.encode("ascii")).digest()
    return hashlib.sha256(t + t + msg).digest()


def _b32(x):
    return x.to_bytes(32, "big")


def _lift_x(x):
    if x >= _P:
        return None
    y2 = (pow(x, 3, _P) + 7) % _P
    y = pow(y2, (_P + 1) // 4, _P)
    if pow(y, 2, _P) != y2:
        return None
    return x, (y if y % 2 == 0 else _P - y)


def secret_from_seed(seed):
    if len(seed) != 32:
        raise ValueError("a seed is 32 bytes")
    """The device's Nostr secret key (32 bytes), derived from its identity seed."""
    k = int.from_bytes(hashlib.sha256(b"skynet-nostr-key:1" + seed).digest(), "big") % (_N - 1) + 1
    return _b32(k)


def schnorr_public(secret):
    if len(secret) != 32 or not 1 <= int.from_bytes(secret, "big") < _N:
        raise ValueError("bad secret key")
    return _b32(_pmul(_G, int.from_bytes(secret, "big"))[0])


def schnorr_sign(msg32, secret, aux=None):
    d0 = int.from_bytes(secret, "big")
    if not 1 <= d0 < _N or len(msg32) != 32:
        raise ValueError("bad key or message")
    aux = os.urandom(32) if aux is None else aux
    if len(secret) != 32 or len(aux) != 32:
        raise ValueError("bad key or aux length")
    p = _pmul(_G, d0)
    d = d0 if p[1] % 2 == 0 else _N - d0
    t = bytes(a ^ b for a, b in zip(_b32(d), _tagged("BIP0340/aux", aux)))
    k0 = int.from_bytes(_tagged("BIP0340/nonce", t + _b32(p[0]) + msg32), "big") % _N
    if k0 == 0:
        raise ValueError("nonce is zero")
    r = _pmul(_G, k0)
    k = k0 if r[1] % 2 == 0 else _N - k0
    e = int.from_bytes(_tagged("BIP0340/challenge", _b32(r[0]) + _b32(p[0]) + msg32), "big") % _N
    sig = _b32(r[0]) + _b32((k + e * d) % _N)
    if not schnorr_verify(msg32, _b32(p[0]), sig):
        raise ValueError("signature self-check failed")
    return sig


def schnorr_verify(msg32, public, sig):
    if len(public) != 32 or len(sig) != 64 or len(msg32) != 32:
        return False
    p = _lift_x(int.from_bytes(public, "big"))
    r = int.from_bytes(sig[:32], "big")
    s = int.from_bytes(sig[32:], "big")
    if p is None or r >= _P or s >= _N:
        return False
    e = int.from_bytes(_tagged("BIP0340/challenge", sig[:32] + public + msg32), "big") % _N
    point = _padd(_pmul(_G, s), _pmul(p, _N - e))
    return point is not None and point[1] % 2 == 0 and point[0] == r


# ---------------------------------------------------------------- events

def make_event(secret, envelope, created=None):
    """Wrap a record into a Nostr event of kind trust.NOSTR_KIND.

    The event time is the record's own time, so sending the same record again gives
    the same event id and relays keep one copy, not one per attempt.
    """
    if len(secret) != 32:
        raise ValueError("a Nostr secret key is 32 bytes")
    public = schnorr_public(secret).hex()
    created = int(envelope["body"]["created"] if created is None else created)
    tags = [["t", trust.NOSTR_TOPIC], ["x", envelope["body"]["type"]]]
    content = records.wire(envelope).decode("utf-8")
    serial = json.dumps([0, public, created, trust.NOSTR_KIND, tags, content],
                        separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    eid = hashlib.sha256(serial).digest()
    return {"id": eid.hex(), "pubkey": public, "created_at": created, "kind": trust.NOSTR_KIND,
            "tags": tags, "content": content, "sig": schnorr_sign(eid, secret).hex()}


# ---------------------------------------------------------------- WebSocket

def _xor_mask(data, mask):
    n = len(data)
    if not n:
        return b""
    return (int.from_bytes(data, "big") ^ int.from_bytes((mask * (n // 4 + 1))[:n], "big")).to_bytes(n, "big")


class WebSocket:
    """A minimal RFC 6455 client for text messages.

    Every operation shares one deadline (time.monotonic), so a slow or chatty server
    cannot hold a call longer than the timeout given at connection time.
    """

    MAX_FRAMES = 4096

    def __init__(self, url, timeout=TIMEOUT, max_message=1 << 20):
        parts = urllib.parse.urlsplit(url)
        if parts.scheme not in ("wss", "ws") or not parts.hostname:
            raise OSError("unsupported relay address: %r" % (url,))
        secure = parts.scheme == "wss"
        port = parts.port or (443 if secure else 80)
        self.deadline = time.monotonic() + timeout
        self.max_message = max_message
        self.buf = bytearray()
        raw = socket.create_connection((parts.hostname, port), timeout=timeout)
        try:
            if secure:
                context = net.system_ca_context() or ssl.create_default_context()
                self.sock = context.wrap_socket(raw, server_hostname=parts.hostname)
            else:
                self.sock = raw
            key = base64.b64encode(os.urandom(16)).decode("ascii")
            host = parts.hostname if parts.port is None else "%s:%d" % (parts.hostname, port)
            target = (parts.path or "/") + ("?" + parts.query if parts.query else "")
            self._sendall(("GET %s HTTP/1.1\r\nHost: %s\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
                           "Sec-WebSocket-Key: %s\r\nSec-WebSocket-Version: 13\r\nUser-Agent: %s\r\n\r\n"
                           % (target, host, key, net.USER_AGENT)).encode("ascii"))
            while b"\r\n\r\n" not in self.buf:
                if len(self.buf) > 16384:
                    raise OSError("WebSocket handshake too long")
                self._fill()
            end = self.buf.index(b"\r\n\r\n")
            head = bytes(self.buf[:end]).decode("latin-1")
            del self.buf[:end + 4]
            lines = head.split("\r\n")
            status = lines[0].split(" ")
            if len(status) < 2 or status[1] != "101":
                raise OSError("relay answered: %s" % lines[0][:80])
            headers = {}
            for line in lines[1:]:
                name, _, value = line.partition(":")
                headers[name.strip().lower()] = value.strip()
            expected = base64.b64encode(hashlib.sha1(
                (key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode("ascii")).digest()).decode("ascii")
            if headers.get("upgrade", "").lower() != "websocket" or headers.get("sec-websocket-accept") != expected:
                raise OSError("bad WebSocket handshake")
        except BaseException:
            raw.close()
            raise

    def _left(self):
        left = self.deadline - time.monotonic()
        if left <= 0:
            raise OSError("timed out")
        return left

    def _sendall(self, data):
        self.sock.settimeout(self._left())
        self.sock.sendall(data)

    def _fill(self):
        self.sock.settimeout(self._left())
        chunk = self.sock.recv(65536)
        if not chunk:
            raise OSError("connection closed")
        self.buf += chunk

    def _need(self, n):
        while len(self.buf) < n:
            self._fill()
        out = bytes(self.buf[:n])
        del self.buf[:n]
        return out

    def send(self, data, opcode=1):
        if isinstance(data, str):
            data = data.encode("utf-8")
        n = len(data)
        if n < 126:
            head = bytes([0x80 | opcode, 0x80 | n])
        elif n < 65536:
            head = bytes([0x80 | opcode, 0xFE]) + struct.pack(">H", n)
        else:
            head = bytes([0x80 | opcode, 0xFF]) + struct.pack(">Q", n)
        mask = os.urandom(4)
        self._sendall(head + mask + _xor_mask(data, mask))

    def recv(self):
        """Return the next text message (strict UTF-8)."""
        message = bytearray()
        started = False
        for _ in range(self.MAX_FRAMES):
            b0, b1 = self._need(2)
            fin, opcode, n = b0 & 0x80, b0 & 15, b1 & 127
            if b0 & 0x70:
                raise OSError("bad WebSocket frame")
            if b1 & 0x80:
                raise OSError("a server frame must not be masked")
            if n == 126:
                n = struct.unpack(">H", self._need(2))[0]
            elif n == 127:
                n = struct.unpack(">Q", self._need(8))[0]
            if opcode >= 8:                      # control frame
                if n > 125 or not fin:
                    raise OSError("bad WebSocket control frame")
                data = self._need(n)
                if opcode == 9:
                    self.send(data, 10)
                elif opcode == 8:
                    raise OSError("closed by the relay")
                continue
            if n + len(message) > self.max_message:
                raise OSError("message too large")
            if opcode == 1 and not started:
                started = True
            elif opcode == 0 and started:
                pass
            else:
                raise OSError("unexpected WebSocket frame")
            message += self._need(n)
            if fin:
                return bytes(message).decode("utf-8")      # UnicodeDecodeError is a ValueError
        raise OSError("too many WebSocket frames")

    def close(self):
        try:
            self.sock.close()
        except OSError:
            pass


# ---------------------------------------------------------------- relay calls

def relays():
    env = os.environ.get("SKYNET_AGENT_RELAYS")
    items = env.split(",") if env is not None else list(trust.RELAYS)
    out = []
    for r in items:
        r = r.strip().rstrip("/")
        if r and r != "none" and r not in out:
            out.append(r)
    return out


def _load(text):
    """Parse one relay message; anything malformed becomes ValueError."""
    try:
        return signed.strict_json_loads(text)
    except (ValueError, RecursionError, UnicodeError, TypeError) as e:
        raise ValueError("bad message from the relay: %s" % type(e).__name__)


def publish(relay, event, timeout=TIMEOUT):
    """Send one event. Returns (True, "") only if the relay confirmed this very event."""
    ws = None
    try:
        ws = WebSocket(relay, timeout=timeout)
        ws.send(json.dumps(["EVENT", event], separators=(",", ":"), ensure_ascii=False))
        while True:
            msg = _load(ws.recv())
            if isinstance(msg, list) and len(msg) >= 3 and msg[0] == "OK" and msg[1] == event["id"]:
                if msg[2] is True:
                    return True, ""
                return False, str(msg[3])[:200] if len(msg) > 3 else "refused"
            if isinstance(msg, list) and msg and msg[0] == "AUTH":
                return False, "the relay asks for a login"
    except (OSError, ValueError) as e:
        return False, "%s: %s" % (type(e).__name__, str(e)[:160])
    finally:
        if ws is not None:
            ws.close()


def fetch(relay, since=0, until=None, limit=500, timeout=TIMEOUT):
    """Ask one relay for the network's events in [since, until].

    Returns (records, info): info["status"] is "complete" (the relay said it has no
    more), "partial" (limit reached, time out or the subscription was closed: there may
    be more) or "error"; info["oldest"] is the oldest event time seen, for paging back
    with until. Events of another kind or topic are ignored; the inner record is
    verified, the outer event signature is not (it carries no authority).
    """
    ws = None
    out, seen, oldest = [], 0, None
    sub = "s" + os.urandom(4).hex()
    try:
        ws = WebSocket(relay, timeout=timeout)
        query = {"kinds": [trust.NOSTR_KIND], "#t": [trust.NOSTR_TOPIC], "limit": limit}
        if since > 0:
            query["since"] = int(since)
        if until is not None:
            query["until"] = int(until)
        ws.send(json.dumps(["REQ", sub, query], separators=(",", ":")))
        while True:
            msg = _load(ws.recv())
            if not isinstance(msg, list) or len(msg) < 2 or msg[1] != sub:
                continue
            if msg[0] == "EVENT" and len(msg) >= 3 and isinstance(msg[2], dict):
                ev = msg[2]
                if ev.get("kind") != trust.NOSTR_KIND or ["t", trust.NOSTR_TOPIC] not in (ev.get("tags") or []):
                    continue
                seen += 1
                if type(ev.get("created_at")) is int:
                    oldest = ev["created_at"] if oldest is None else min(oldest, ev["created_at"])
                try:
                    out.append(records.parse(ev.get("content", "")))
                except records.RecordError:
                    pass
                if seen >= limit:
                    return out, {"status": "partial", "oldest": oldest, "seen": seen}
            elif msg[0] == "EOSE":
                return out, {"status": "complete", "oldest": oldest, "seen": seen}
            elif msg[0] == "CLOSED":
                return out, {"status": "partial", "oldest": oldest, "seen": seen, "error": str(msg[2:])[:160]}
    except (OSError, ValueError) as e:
        status = "partial" if seen else "error"
        return out, {"status": status, "oldest": oldest, "seen": seen,
                     "error": "%s: %s" % (type(e).__name__, str(e)[:160])}
    finally:
        if ws is not None:
            ws.close()


def fetch_all(relay, since=0, limit=500, max_pages=20, timeout=TIMEOUT):
    """Page backwards with until until the relay has nothing more or a page fails.

    Returns (records, complete): complete is True only if every page ended with EOSE
    below the limit, i.e. the relay gave everything it has since `since`.
    """
    out, until = [], None
    for _ in range(max_pages):
        got, info = fetch(relay, since=since, until=until, limit=limit, timeout=timeout)
        out.extend(got)
        if info["status"] == "complete" and info["seen"] < limit:
            return out, True
        if info["status"] == "error" or info["oldest"] is None:
            return out, False
        if until is not None and info["oldest"] >= until:
            return out, False           # a full second of events: cannot page past it
        until = info["oldest"]          # events at this very second are asked again: duplicates are fine
    return out, False
