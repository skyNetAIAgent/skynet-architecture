"""Shared test helpers: a throw-away key, a temporary copy of the repository,
a static file server and a stand-in for the GitHub API. Standard library only."""

import functools
import http.server
import json
import os
import shutil
import subprocess
import sys
import threading

AGENT_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
REPO_ROOT = os.path.abspath(os.path.join(AGENT_DIR, ".."))
if AGENT_DIR not in sys.path:
    sys.path.insert(0, AGENT_DIR)

from skynet_agent import ed25519  # noqa: E402

# Tests never talk to public relays or receivers; a test that needs a channel starts its own.
# The older tests exercise publishing through the GitHub stand-in.
os.environ["SKYNET_AGENT_RELAYS"] = "none"
os.environ["SKYNET_AGENT_RECEIVERS"] = "none"
os.environ.setdefault("SKYNET_AGENT_SUBMIT_VIA", "github")

# A throw-away seed used only by the tests. It protects nothing.
TEST_SEED_HEX = "11" * 32
TEST_PUBLIC_HEX = ed25519.public_key(bytes.fromhex(TEST_SEED_HEX)).hex()

STUB = ("import sys; sys.path.insert(0, sys.argv[1]); "
        "sys.argv = [sys.argv[0]] + sys.argv[2:]; "
        "from skynet_agent.cli import main; sys.exit(main())")


def copy_repo(dst):
    """Copy agent/ and tools/ (without caches and tests) into dst, as a test 'repository'."""
    ignore = shutil.ignore_patterns("__pycache__", "tests", "*.pyc", "release.json", "release.json.sig")
    shutil.copytree(os.path.join(REPO_ROOT, "agent"), os.path.join(dst, "agent"), ignore=ignore)
    shutil.copytree(os.path.join(REPO_ROOT, "tools"), os.path.join(dst, "tools"),
                    ignore=shutil.ignore_patterns("__pycache__"))
    os.makedirs(os.path.join(dst, "tasks"), exist_ok=True)
    return dst


def tool_env():
    env = dict(os.environ)
    env["SKYNET_RELEASE_SEED_HEX"] = TEST_SEED_HEX
    env.pop("SKYNET_RELEASE_KEY", None)
    return env


def run_tool(repo, name, *args):
    """Run tools/<name> of the test repository with the throw-away key."""
    cmd = [sys.executable, "-I", os.path.join(repo, "tools", name), "--root", repo] + list(args)
    done = subprocess.run(cmd, env=tool_env(), capture_output=True, timeout=300)
    if done.returncode != 0:
        raise AssertionError("%s failed: %s" % (name, (done.stdout + done.stderr).decode("utf-8", "replace")))
    return done.stdout.decode("utf-8", "replace")


def make_release(repo, seq, version, *extra):
    return run_tool(repo, "make_release.py", "--seq", str(seq), "--version", version, "--set-trust", *extra)


def write_index(repo, index):
    path = os.path.join(repo, "tasks", "index.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(index, f, indent=1)
        f.write("\n")
    return run_tool(repo, "sign_tasks.py")


class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serve_directory(directory):
    """Serve a directory over HTTP on a free local port. Returns (server, base url)."""
    handler = functools.partial(_Quiet, directory=directory)
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, "http://127.0.0.1:%d" % server.server_address[1]


class FakeGitHub:
    """Remembers what was posted. Speaks just enough of the GitHub REST API for the agent."""

    def __init__(self, existing_comments=None, fail_status=None):
        self.posts = []            # (path, authorization header, body text)
        self.existing = list(existing_comments or [])
        self.fail_status = fail_status
        outer = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def _send(self, status, obj):
                data = json.dumps(obj).encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self):
                if self.path == "/user":
                    return self._send(200, {"login": "tester"})
                if "/comments" in self.path:
                    page = 1
                    if "page=" in self.path:
                        page = int(self.path.rsplit("page=", 1)[1].split("&")[0])
                    chunk = outer.existing[(page - 1) * 100: page * 100]
                    return self._send(200, [{"body": b, "user": {"login": "someone"}} for b in chunk])
                return self._send(404, {"message": "Not Found"})

            def do_POST(self):
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length).decode("utf-8"))
                if outer.fail_status:
                    return self._send(outer.fail_status, {"message": "nope"})
                outer.posts.append((self.path, self.headers.get("Authorization", ""), payload.get("body", "")))
                self._send(201, {"html_url": "https://example.invalid/comment/%d" % len(outer.posts)})

        self.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = "http://127.0.0.1:%d" % self.server.server_address[1]

    def close(self):
        self.server.shutdown()
        self.server.server_close()
