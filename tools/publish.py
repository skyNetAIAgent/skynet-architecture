#!/usr/bin/env python3
"""Upload the working copy to GitHub as one commit, without git (for maintainers).

    python tools/publish.py --message "what changed"          show what would be uploaded
    python tools/publish.py --message "what changed" --yes    upload

It uses the GitHub command-line tool `gh` (you must be logged in with rights to
push). Only files that changed are sent; files that no longer exist locally are
removed from the repository. Nothing is uploaded without --yes.

The commit is attributed to your GitHub login and GitHub's "noreply" address of
that account, never to the name or the e-mail address of your profile. Another
identity can be given with --author-name and --author-email.

Safety: files that look like secrets (keys, tokens, .env files) stop the upload,
as do caches and files larger than 2 MB. After changing anything under agent/
run tools/make_release.py first, otherwise installed agents will reject the
files (the automatic check "Agent tests" also fails).
"""

import argparse
import base64
import fnmatch
import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

SKIP_DIRS = {"analysis", ".git", "__pycache__", ".pytest_cache", ".ruff_cache", ".venv", "node_modules",
             "build", ".gradle"}                        # build output of the Android app
SKIP_FILES = ["*.pyc", "*.pyo", "Thumbs.db", ".DS_Store", "local.properties", "*.apk", "*.idsig"]
SECRET_PATTERNS = ["*.pem", "*.key", "*.dpapi", "*.pfx", "*.p12", "*.jks", "*.keystore", ".env", ".env.*", "id_rsa*", "id_ed25519*",
                   "github-token", "release-key*", "*.kdbx", "credentials*", "secrets*"]
MAX_BYTES = 2 << 20


def gh(args, payload=None):
    cmd = ["gh", "api"] + args
    data = None
    if payload is not None:
        cmd += ["--input", "-"]
        data = json.dumps(payload).encode("utf-8")
    done = subprocess.run(cmd, input=data, capture_output=True)
    if done.returncode != 0:
        raise RuntimeError("gh api %s failed: %s" % (" ".join(args), done.stderr.decode("utf-8", "replace").strip()))
    out = done.stdout.decode("utf-8", "replace").strip()
    return json.loads(out) if out else None


def blob_sha(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def identity(args):
    """Name and e-mail written into the commit.

    Never the real name or the e-mail address of the GitHub profile: by default the
    login and GitHub's own "noreply" address of the account that uploads.
    """
    if args.author_name or args.author_email:
        if not (args.author_name and args.author_email):
            raise SystemExit("give both --author-name and --author-email, or neither")
        return {"name": args.author_name, "email": args.author_email}
    user = gh(["user"])
    return {"name": user["login"],
            "email": "%d+%s@users.noreply.github.com" % (user["id"], user["login"])}


def collect(root):
    """Return ({path: bytes}, [problems])."""
    files, problems = {}, []
    for folder, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(names):
            if any(fnmatch.fnmatch(name, p) for p in SKIP_FILES):
                continue
            full = os.path.join(folder, name)
            rel = os.path.relpath(full, root).replace(os.sep, "/")
            if any(fnmatch.fnmatch(name.lower(), p) for p in SECRET_PATTERNS):
                problems.append("looks like a secret: %s" % rel)
                continue
            size = os.path.getsize(full)
            if size > MAX_BYTES:
                problems.append("larger than %d bytes: %s" % (MAX_BYTES, rel))
                continue
            with open(full, "rb") as f:
                files[rel] = f.read()
    return files, problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", default="skyNetAIAgent/skynet-architecture")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--root", default=os.path.join(HERE, ".."))
    parser.add_argument("--message", required=True)
    parser.add_argument("--author-name", help="name written into the commit (default: your GitHub login)")
    parser.add_argument("--author-email", help="e-mail written into the commit (default: GitHub's noreply address)")
    parser.add_argument("--yes", action="store_true")
    args = parser.parse_args(argv)
    root = os.path.abspath(args.root)
    if not shutil.which("gh"):
        print("The GitHub command-line tool `gh` is not installed.")
        return 1

    files, problems = collect(root)
    for p in problems:
        print("STOP: %s" % p)
    if problems:
        return 1

    repo = "repos/" + args.repo
    head = None
    remote = {}
    try:
        head = gh(["%s/git/ref/heads/%s" % (repo, args.branch)])["object"]["sha"]
        commit = gh(["%s/git/commits/%s" % (repo, head)])
        tree = gh(["%s/git/trees/%s?recursive=1" % (repo, commit["tree"]["sha"])])
        if tree.get("truncated"):
            print("The repository tree is too large for this tool.")
            return 1
        remote = dict((e["path"], e["sha"]) for e in tree["tree"] if e["type"] == "blob")
    except RuntimeError as e:
        if "409" not in str(e) and "404" not in str(e) and "empty" not in str(e).lower():
            print(e)
            return 1

    changed = sorted(p for p, data in files.items() if remote.get(p) != blob_sha(data))
    removed = sorted(p for p in remote if p not in files)
    print("Repository %s, branch %s: %d file(s) locally, %d to upload, %d to remove." % (
        args.repo, args.branch, len(files), len(changed), len(removed)))
    for p in changed:
        print("  upload  %s (%d bytes)" % (p, len(files[p])))
    for p in removed:
        print("  remove  %s" % p)
    if not changed and not removed:
        print("Nothing to do.")
        return 0
    who = identity(args)
    print("The commit will be attributed to: %s <%s>" % (who["name"], who["email"]))
    if not args.yes:
        print("Nothing was uploaded. Add --yes to upload.")
        return 0

    if head is None:
        # An empty repository has no branch yet; the first file creates it.
        first = ".gitattributes" if ".gitattributes" in files else sorted(files)[0]
        created = gh(["-X", "PUT", "%s/contents/%s" % (repo, first)], {
            "message": "Start the repository", "branch": args.branch,
            "content": base64.b64encode(files[first]).decode("ascii"),
            "author": who, "committer": who})
        head = created["commit"]["sha"]

    entries = []
    for path in sorted(files):
        data = files[path]
        sha = blob_sha(data)
        if remote.get(path) != sha:
            made = gh(["-X", "POST", "%s/git/blobs" % repo], {
                "content": base64.b64encode(data).decode("ascii"), "encoding": "base64"})
            if made["sha"] != sha:
                raise RuntimeError("GitHub stored different bytes for %s" % path)
        mode = "100755" if path.endswith(".sh") else "100644"
        entries.append({"path": path, "mode": mode, "type": "blob", "sha": sha})
    tree = gh(["-X", "POST", "%s/git/trees" % repo], {"tree": entries})
    commit = gh(["-X", "POST", "%s/git/commits" % repo], {
        "message": args.message, "tree": tree["sha"], "parents": [head],
        "author": who, "committer": who})
    gh(["-X", "PATCH", "%s/git/refs/heads/%s" % (repo, args.branch)], {"sha": commit["sha"], "force": False})
    print("Published commit %s" % commit["sha"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
