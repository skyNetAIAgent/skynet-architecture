#!/usr/bin/env python3
"""A full node of the research network: keeps every signed record and hands it to anyone.

Any participant with a computer that is always on can run one. It needs no
account anywhere and holds no secret that matters: it cannot forge a record
(every record carries its author's signature) and it cannot hide one for long
(the same records travel through public relays and other nodes).

    python3 node/receiver.py --data ~/skynet-node --port 8790

What it does:
  * POST /v1/records          takes one signed record, checks it, stores it, and
                              answers {"ok": true, "id": ...} only after the record
                              is on disk
  * GET  /v1/records?after=N  gives stored records in the order they arrived
  * GET  /v1/records/<id>     gives one record
  * GET  /v1/info             says what this node is and how much it holds
  * POST /v1/status           stores the latest signed status for an agent
  * GET  /v1/agents           lists agents seen in status updates or result records
  * GET  /agents              displays agent hardware, activity and totals
  * answers agents on the same private network over UDP (same port number), so that
    computers behind a router without NAT loopback still find this node (--no-lan-answer)
  * every few minutes pulls new records from the public relays (--no-relays turns
    this off). Passing records received over HTTP on to the relays is OFF unless
    --push-to-relays is given: a free key costs nothing, and a node must not become
    a free amplifier of other people's floods.

Limits protect the computer, not the truth: at most --connections open connections,
10 seconds to send a request, 40 kB per record, 4 KiB per status, --rate posts and --reads page reads
per minute from one address, --global-rate posts per minute from everybody, pages of
at most 200 records / 8 MB, and the store stops growing at --max-mb. The records
stay on disk; memory holds only an index (about 150 bytes per record). Standard
library only. There is no TLS here: records are signed, so nobody on the way can
change them, but they and the sender's address can be read; put the node behind a
TLS proxy if that matters.
"""

import argparse
import ipaddress
import json
import os
import socket
import sys
import tempfile
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "agent"))
sys.path.insert(0, HERE)                    # also find the page when run with python -I

from agents_page import render_agents
from skynet_agent import __version__, ed25519, nostr, records, signed, trust  # noqa: E402

PAGE_MAX = 200
PAGE_BYTES = 8 << 20
REQUEST_SECONDS = 10
STATUS_BYTES = 4096
STATUS_TEXT = ("version", "os", "arch", "cpu_model")
STATUS_NUMBERS = ("release_seq", "cpu_threads", "ram_mb", "units_done", "started", "sent")
STATUS_FIELDS = {"v", "agent", "gpus", *STATUS_TEXT, *STATUS_NUMBERS}


def parse_status(data):
    """Return the signed status after checking its schema and canonical bytes."""
    if len(data) > STATUS_BYTES:
        raise ValueError("status too large")
    try:
        envelope = signed.strict_json_loads(data)
    except (ValueError, RecursionError) as exc:
        raise ValueError("invalid status JSON") from exc
    if not isinstance(envelope, dict) or set(envelope) != {"status", "sig"}:
        raise ValueError("invalid status envelope")
    status = envelope["status"]
    if not isinstance(status, dict) or set(status) != STATUS_FIELDS:
        raise ValueError("invalid status fields")

    def number(value):
        return type(value) is int and 0 <= value < 2 ** 63

    def label(value):
        if not isinstance(value, str):
            return False
        value.encode("utf-8")   # reject escaped lone surrogates before storing/displaying
        return True

    if type(status["v"]) is not int or status["v"] != 1 or not records.is_hex64(status["agent"]):
        raise ValueError("invalid status version or agent key")
    if not all(label(status[k]) for k in STATUS_TEXT) or not all(number(status[k]) for k in STATUS_NUMBERS):
        raise ValueError("invalid status field type or value")
    if not isinstance(status["gpus"], list) or not all(
        isinstance(gpu, dict) and set(gpu) == {"name", "vram_mb"}
        and label(gpu["name"]) and number(gpu["vram_mb"]) for gpu in status["gpus"]
    ):
        raise ValueError("invalid GPU list")
    sig = envelope["sig"]
    if not isinstance(sig, str) or len(sig) != 128:
        raise ValueError("invalid signature")
    key = bytes.fromhex(status["agent"])
    message = records.canonical(status).encode("ascii")
    if not ed25519.is_strong_public(key) or not ed25519.verify(key, message, bytes.fromhex(sig)):
        raise ValueError("invalid signature")
    return status


class NodeStore:
    """Append-only log of verified records on disk, with an index in memory."""

    def __init__(self, folder, max_bytes):
        self.folder = folder
        self.file = os.path.join(folder, "records.jsonl")
        self.max_bytes = max_bytes
        self.lock = threading.Lock()
        self.order = []          # ids in arrival order; position + 1 is the cursor
        self.where = {}          # id -> (offset, length) in the file
        self.from_relay = set()
        self.results = {}        # author -> count and time range of unique result records
        os.makedirs(folder, exist_ok=True)
        self.status_file = os.path.join(folder, "agents.json")
        try:
            with open(self.status_file, encoding="utf-8") as f:
                self.statuses = json.load(f)
        except FileNotFoundError:
            self.statuses = {}
        if not os.path.exists(self.file):
            open(self.file, "ab").close()
        self.size = os.path.getsize(self.file)
        with open(self.file, "rb") as f:
            data_end = 0
            offset = 0
            for line in f:
                if not line.endswith(b"\n"):
                    break                      # a half-written last line after a crash
                data_end = offset + len(line)
                body = line[:-1]
                try:
                    env = records.parse(body, now=float("inf"))
                except records.RecordError:
                    env = None
                if env is not None and env["id"] not in self.where:
                    self.where[env["id"]] = (offset, len(body))
                    self.order.append(env["id"])
                    self._index_result(env["body"])
                offset = data_end
        if data_end != self.size:
            with open(self.file, "r+b") as f:
                f.truncate(data_end)
            self.size = data_end
        self.reader = open(self.file, "rb")

    def add(self, envelope, from_relay=False):
        """Return "new", "known" or "full". "new" only after the bytes are on disk."""
        data = records.wire(envelope)
        with self.lock:
            if envelope["id"] in self.where:
                return "known"
            if self.size + len(data) + 1 > self.max_bytes:
                return "full"
            with open(self.file, "ab") as f:
                f.write(data + b"\n")
                f.flush()
                os.fsync(f.fileno())
            self.where[envelope["id"]] = (self.size, len(data))
            self.order.append(envelope["id"])
            self.size += len(data) + 1
            self._index_result(envelope["body"])
            if from_relay:
                self.from_relay.add(envelope["id"])
            return "new"

    def _index_result(self, body):
        if body["type"] == "result":
            created = body["created"]
            stats = self.results.setdefault(body["author"], {"first_seen": created, "last_seen": created,
                                                              "result_count": 0})
            stats["result_count"] += 1
            stats["first_seen"] = min(stats["first_seen"], created)
            stats["last_seen"] = max(stats["last_seen"], created)

    def save_status(self, status):
        key = status["agent"]
        with self.lock:
            previous = self.statuses.get(key)
            if previous and status["sent"] <= previous["sent"]:
                return
            now = int(time.time())
            row = dict(status, first_seen=previous["first_seen"] if previous else now, last_seen=now)
            updated = {**self.statuses, key: row}
            tmp = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=self.folder, delete=False)
            try:
                with tmp:
                    json.dump(updated, tmp, separators=(",", ":"))
                    tmp.flush()
                    os.fsync(tmp.fileno())
                os.replace(tmp.name, self.status_file)
            finally:
                if os.path.exists(tmp.name):
                    os.unlink(tmp.name)
            self.statuses = updated

    def agents(self):
        with self.lock:
            rows = {key: dict(stats, agent=key, legacy=True) for key, stats in self.results.items()}
            for key, status in self.statuses.items():
                results = self.results.get(key, {})
                first = min(status["first_seen"], results.get("first_seen", status["first_seen"]))
                rows[key] = dict(status, legacy=False, first_seen=first, result_count=results.get("result_count", 0))
        return sorted(rows.values(), key=lambda row: (-row["last_seen"], row["agent"]))

    def _read(self, rid):
        offset, length = self.where[rid]
        self.reader.seek(offset)
        return self.reader.read(length)

    def page(self, after, limit, max_bytes=PAGE_BYTES):
        with self.lock:
            out, total = [], 0
            for rid in self.order[after:after + limit]:
                length = self.where[rid][1]
                if out and total + length > max_bytes:
                    break
                out.append(self._read(rid))
                total += length
            return after + len(out), out

    def get(self, rid):
        with self.lock:
            return self._read(rid) if rid in self.where else None

    def count(self):
        with self.lock:
            return len(self.order), self.size

    def known(self, rid):
        with self.lock:
            return rid in self.where


class Budget:
    """Events per minute: per address and for everybody together, in one-minute windows."""

    def __init__(self, per_address, total):
        self.per_address, self.total = per_address, total
        self.lock = threading.Lock()
        self.window, self.counts, self.sum = 0, {}, 0

    def allow(self, address):
        minute = int(time.time() // 60)
        with self.lock:
            if minute != self.window:
                self.window, self.counts, self.sum = minute, {}, 0
            n = self.counts.get(address, 0)
            if n >= self.per_address or self.sum >= self.total:
                return False
            if address not in self.counts and len(self.counts) >= 100000:
                return False
            self.counts[address] = n + 1
            self.sum += 1
            return True


class Server(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 64

    def __init__(self, address, handler, max_connections):
        super().__init__(address, handler)
        self.slots = threading.BoundedSemaphore(max_connections)

    def handle_error(self, request, client_address):
        # The default socketserver error message includes the peer's address.
        sys.stderr.write("request failed: %s\n" % type(sys.exc_info()[1]).__name__)

    def process_request(self, request, client_address):
        # refuse at once, before a thread is created, when all slots are taken
        if not self.slots.acquire(blocking=False):
            try:
                request.sendall(b"HTTP/1.1 503 Service Unavailable\r\nContent-Length: 0\r\nConnection: close\r\n\r\n")
            except OSError:
                pass
            self.shutdown_request(request)
            return
        try:
            super().process_request(request, client_address)
        except BaseException:
            self.slots.release()
            raise

    def process_request_thread(self, request, client_address):
        try:
            request.settimeout(REQUEST_SECONDS)
            super().process_request_thread(request, client_address)
        finally:
            self.slots.release()


def make_handler(store, posts, reads, proxy):
    class Handler(BaseHTTPRequestHandler):
        server_version = "skynet-node/" + __version__
        protocol_version = "HTTP/1.1"
        timeout = REQUEST_SECONDS

        def log_message(self, fmt, *args):       # quiet: no addresses in logs
            pass

        def _address(self):
            peer = self.client_address[0]
            if proxy and peer == proxy:
                forwarded = self.headers.get_all("X-Forwarded-For") or []
                if len(forwarded) == 1:
                    candidate = forwarded[0].split(",")[-1].strip()
                    try:
                        return str(ipaddress.ip_address(candidate))
                    except ValueError:
                        pass
            return peer

        def _send(self, status, body, ctype="application/json"):
            if isinstance(body, (dict, list)):
                body = json.dumps(body, separators=(",", ":")).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(body)
            self.close_connection = True

        def do_GET(self):
            parts = urlsplit(self.path)
            if parts.path == "/v1/info":
                count, size = store.count()
                return self._send(200, {"net": trust.NET_ID, "software": "skynet-node", "version": __version__,
                                        "records": count, "bytes": size, "max_record_bytes": records.MAX_WIRE_BYTES})
            if not reads.allow(self._address()):
                return self._send(429, {"error": "too many requests from this address, try later"})
            if parts.path == "/v1/agents":
                return self._send(200, store.agents())
            if parts.path == "/agents":
                return self._send(200, render_agents(store.agents(), int(time.time())), "text/html; charset=utf-8")
            if parts.path == "/v1/records":
                try:
                    q = parse_qs(parts.query)
                    after = int(q.get("after", ["0"])[0])
                    limit = int(q.get("limit", [str(PAGE_MAX)])[0])
                    if not 0 <= after < 2 ** 40 or not 1 <= limit <= 10 ** 6:
                        raise ValueError
                except ValueError:
                    return self._send(400, {"error": "bad query"})
                nxt, items = store.page(after, min(limit, PAGE_MAX))
                return self._send(200, b'{"next":%d,"records":[' % nxt + b",".join(items) + b"]}")
            if parts.path.startswith("/v1/records/"):
                rid = parts.path[len("/v1/records/"):]
                data = store.get(rid) if records.is_hex64(rid) else None
                if data is None:
                    return self._send(404, {"error": "no such record"})
                return self._send(200, data)
            return self._send(404, {"error": "not found"})

        def do_POST(self):
            path = urlsplit(self.path).path
            if path not in ("/v1/records", "/v1/status"):
                return self._send(404, {"error": "not found"})
            if self.headers.get("Transfer-Encoding") is not None:
                return self._send(400, {"error": "Transfer-Encoding is not supported"})
            lengths = self.headers.get_all("Content-Length") or []
            if len(lengths) != 1 or not lengths[0].isascii() or not lengths[0].strip().isdigit():
                return self._send(411, {"error": "exactly one Content-Length is required"})
            size_limit = STATUS_BYTES if path == "/v1/status" else records.MAX_WIRE_BYTES + 1024
            digits = lengths[0].strip().lstrip("0") or "0"
            if len(digits) > len(str(size_limit)) or not 0 < int(digits) <= size_limit:
                return self._send(413, {"error": "body size outside limit"})
            length = int(digits)
            if not posts.allow(self._address()):
                return self._send(429, {"error": "too many posts, try later"})
            deadline = time.monotonic() + REQUEST_SECONDS
            data = bytearray()
            try:
                while len(data) < length:
                    left = deadline - time.monotonic()
                    if left <= 0:
                        return self._send(408, {"error": "too slow"})
                    self.connection.settimeout(left)
                    chunk = self.rfile.read1(length - len(data))
                    if not chunk:
                        return self._send(400, {"error": "the body is shorter than Content-Length"})
                    data += chunk
            except (OSError, socket.timeout):
                self.close_connection = True
                return
            if path == "/v1/status":
                try:
                    status = parse_status(data)
                except ValueError:
                    return self._send(400, {"error": "invalid signed status"})
                try:
                    store.save_status(status)
                except OSError:
                    return self._send(507, {"error": "cannot store status"})
                return self._send(200, {"ok": True})
            try:
                envelope = records.parse(bytes(data))
            except records.RecordError as e:
                return self._send(400, {"error": str(e)[:200]})
            outcome = store.add(envelope)
            if outcome == "full":
                return self._send(507, {"error": "this node is full"})
            return self._send(200, {"ok": True, "new": outcome == "new", "id": envelope["id"]})

    return Handler


def bridge(store, data_dir, interval, push, stop, log):
    """Pull records from the relays; with push, also pass records received over HTTP on."""
    state_file = os.path.join(data_dir, "bridge.json")
    try:
        with open(state_file, "r", encoding="utf-8") as f:
            state = json.load(f)
        if not isinstance(state, dict):
            state = {}
    except (OSError, ValueError):
        state = {}
    secret = None
    if push:
        key_file = os.path.join(data_dir, "node.key")
        try:
            with open(key_file, "r", encoding="ascii") as f:
                seed = bytes.fromhex(f.read().strip())
            if len(seed) != 32:
                raise ValueError
        except (OSError, ValueError):
            seed = os.urandom(32)
            fd = os.open(key_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(fd, "w", encoding="ascii") as f:
                f.write(seed.hex() + "\n")
        secret = nostr.secret_from_seed(seed)
    while not stop.is_set():
        try:
            started = int(time.time())
            for relay in nostr.relays():
                key = "since " + relay
                since = max(0, int(state.get(key, 0)) - 3600)
                envs, complete = nostr.fetch_all(relay, since=since)
                for env in envs:
                    store.add(env, from_relay=True)
                if complete:
                    state[key] = started
            if push:
                pushed = int(state.get("pushed", 0))
                nxt, items = store.page(pushed, 100)
                for raw in items:
                    env = json.loads(raw.decode("utf-8"))
                    if env["id"] in store.from_relay:
                        continue
                    event = nostr.make_event(secret, env)
                    for relay in nostr.relays():
                        nostr.publish(relay, event)
                state["pushed"] = nxt
            tmp = state_file + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(state, f)
            os.replace(tmp, state_file)
        except Exception as e:          # the bridge must survive anything a relay sends
            log("bridge round failed: %s: %s" % (type(e).__name__, str(e)[:200]))
        stop.wait(interval)


LAN_QUESTION = b"SKYNET-NODE? v1"


def answer_lan(port, stop, log):
    """Tell agents on the same private network where this node is (UDP, same port number).

    Many routers do not let a computer reach its own network's public address, so an agent
    next to the node could not deliver anything. Only questions from private or loopback
    addresses get an answer, at most one per address and second; the answer holds only the port.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("0.0.0.0", port))
        sock.settimeout(1.0)
    except OSError as e:
        log("LAN answers are off: %s" % e)
        return
    last = {}
    answer = b"SKYNET-NODE v1 %d" % port
    while not stop.is_set():
        try:
            data, (address, sender_port) = sock.recvfrom(64)
        except socket.timeout:
            continue
        except OSError:
            continue
        try:
            ip = ipaddress.ip_address(address)
        except ValueError:
            continue
        now = time.monotonic()
        if data != LAN_QUESTION or not (ip.is_private or ip.is_loopback) or now - last.get(address, -2) < 1:
            continue
        if len(last) > 4096:
            last.clear()
        last[address] = now
        try:
            sock.sendto(answer, (address, sender_port))
        except OSError:
            pass
    sock.close()


def main(argv=None):
    ap = argparse.ArgumentParser(description="SkyNet research network: full node (record receiver and relay bridge)")
    ap.add_argument("--data", required=True, help="folder for the record log")
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=8790)
    ap.add_argument("--connections", type=int, default=64, help="open connections at most")
    ap.add_argument("--rate", type=int, default=60, help="posts per minute accepted from one address")
    ap.add_argument("--global-rate", type=int, default=600, help="posts per minute accepted from everybody")
    ap.add_argument("--reads", type=int, default=120, help="page reads per minute from one address")
    ap.add_argument("--max-mb", type=int, default=2048, help="the store stops growing at this size")
    ap.add_argument("--bridge-minutes", type=float, default=5.0)
    ap.add_argument("--no-lan-answer", action="store_true", help="do not answer agents on the local network (UDP)")
    ap.add_argument("--no-relays", action="store_true", help="do not talk to public relays at all")
    ap.add_argument("--push-to-relays", action="store_true",
                    help="also publish records received over HTTP to the relays (off by default)")
    ap.add_argument("--proxy", help="address of a reverse proxy whose X-Forwarded-For header is trusted")
    args = ap.parse_args(argv)

    def log(text):
        sys.stderr.write(text + "\n")
        sys.stderr.flush()

    data_dir = os.path.abspath(os.path.expanduser(args.data))
    store = NodeStore(data_dir, args.max_mb << 20)
    handler = make_handler(store, Budget(args.rate, args.global_rate), Budget(args.reads, args.reads * 100), args.proxy)
    server = Server((args.host, args.port), handler, args.connections)
    stop = threading.Event()
    if not args.no_relays:
        threading.Thread(target=bridge, args=(store, data_dir, args.bridge_minutes * 60, args.push_to_relays,
                                              stop, log), daemon=True).start()
    if not args.no_lan_answer:
        threading.Thread(target=answer_lan, args=(args.port, stop, log), daemon=True).start()
    count, size = store.count()
    log("skynet-node %s: %d records (%d bytes), listening on %s:%d, net %s"
        % (__version__, count, size, args.host, server.server_address[1], trust.NET_ID))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        stop.set()
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
