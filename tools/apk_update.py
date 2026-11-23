"""APK manifest validation shared by release tooling and its offline tests."""

import hashlib
import os
import re
from urllib.parse import unquote

from skynet_agent import signed, trust

RELEASE_URL = trust.WEB_BASE + "/releases/download/"


def validate(doc):
    if not isinstance(doc, dict):
        raise ValueError("expected a manifest object")
    for key, limit in (("format", 1), ("version_code", 2**31 - 1),
                       ("size", 2**63 - 1), ("min_sdk", 2**31 - 1)):
        value = doc.get(key)
        if type(value) is not int or not 1 <= value <= limit:
            raise ValueError("invalid " + key)
    for key, limit in (("version_name", 64), ("notes", 500)):
        value = doc.get(key)
        if not isinstance(value, str) or not value.strip() or not value.isprintable() or len(value) > limit:
            raise ValueError("invalid " + key)
    digest = doc.get("sha256")
    if not isinstance(digest, str) or not re.fullmatch("[0-9a-f]{64}", digest):
        raise ValueError("invalid sha256")
    url = doc.get("url")
    if not isinstance(url, str) or not url.startswith(RELEASE_URL):
        raise ValueError("invalid release URL")
    # Two encoded path components: the release tag and its APK asset.
    parts = url[len(RELEASE_URL):].split("/")
    if len(parts) != 2 or not unquote(parts[1]).lower().endswith(".apk"):
        raise ValueError("expected an APK release asset")
    for part in parts:
        decoded = unquote(part, errors="strict")
        if (not re.fullmatch(r"(?:[A-Za-z0-9._~+-]|%[0-9A-Fa-f]{2})+", part)
                or any(p in ("", ".", "..") for p in decoded.split("/"))
                or "\\" in decoded or not decoded.isprintable()):
            raise ValueError("invalid release path")


def manifest(raw, signature, installed, sdk):
    raw = bytes(raw)
    signed.verify_detached(raw, bytes(signature))
    doc = signed.strict_json_loads(raw)
    validate(doc)
    if doc["version_code"] > installed and doc["min_sdk"] <= sdk:
        return raw.decode("utf-8")
    return None


def file_hash(path):
    digest = hashlib.sha256()
    with open(path, "rb") as src:
        for block in iter(lambda: src.read(128 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def matches(path, size, sha256):
    return os.path.isfile(path) and os.path.getsize(path) == size and file_hash(path) == sha256
