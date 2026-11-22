"""ai-answer@1: let a local AI model you run yourself answer a research question.

This is optional and off by default. The agent never downloads a model and
never starts one: you run your own OpenAI-compatible server (for example
Ollama, the llama.cpp server or LM Studio) and switch "ai.enabled" on.

The question and the documents it refers to come from the signed task list.
Each document is fetched from the repository and accepted only if its SHA-256
matches the task, so the prompt is exactly what the maintainers published.
The answer is plain text from the model. It is not verified by anyone and is
published as "machine-generated".
"""

import hashlib
import json
import os
import re

from .. import net

VERSION = 1
KIND = "ai"

DEFAULT_ENDPOINTS = (
    "http://127.0.0.1:11434/v1",   # Ollama
    "http://127.0.0.1:8080/v1",    # llama.cpp server
    "http://127.0.0.1:1234/v1",    # LM Studio
)

DEFAULT_SYSTEM = (
    "You help design SkyNet, a distributed network where AI models run and learn on "
    "participants' computers. Rules: be concrete; separate what is decided from what you "
    "propose; name every assumption (trusted hardware, honest majority, sampling); do not "
    "weaken the mandatory requirements; do not invent sources or numbers; if you find no "
    "solution, say so. Answer in the language of the task."
)

MAX_CONTEXT_CHARS = 120000
MAX_DOC_BYTES = 512 * 1024
_PATH_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_./-]{0,199}$")
_SHA_RE = re.compile(r"^[0-9a-f]{64}$")
_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)
_ALLOWED = {"question", "system", "context", "max_output_chars", "max_tokens",
            "temperature_milli", "max_answers"}


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)


def _opt_int(params, name, lo, hi, default):
    value = params.get(name, default)
    if not _is_int(value) or not lo <= value <= hi:
        raise ValueError("%s must be an integer from %d to %d" % (name, lo, hi))
    return value


def validate(params, units):
    if not isinstance(params, dict):
        raise ValueError("params must be an object")
    extra = set(params) - _ALLOWED
    if extra:
        raise ValueError("unknown parameters: %s" % sorted(extra))
    question = params.get("question")
    if not isinstance(question, str) or not 1 <= len(question) <= 8000:
        raise ValueError("question must be 1..8000 characters")
    system = params.get("system", "")
    if not isinstance(system, str) or len(system) > 8000:
        raise ValueError("system must be at most 8000 characters")
    context = params.get("context", [])
    if not isinstance(context, list) or len(context) > 8:
        raise ValueError("context must be a list of at most 8 documents")
    for doc in context:
        if not isinstance(doc, dict) or set(doc) - {"path", "sha256", "lines"}:
            raise ValueError("a context document takes: path, sha256, lines")
        path = doc.get("path")
        if not isinstance(path, str) or not _PATH_RE.match(path) or ".." in path:
            raise ValueError("bad context path: %r" % (path,))
        sha = doc.get("sha256")
        if not isinstance(sha, str) or not _SHA_RE.match(sha):
            raise ValueError("context sha256 must be 64 lowercase hex digits")
        lines = doc.get("lines")
        if lines is not None:
            if (not isinstance(lines, list) or len(lines) != 2 or not _is_int(lines[0])
                    or not _is_int(lines[1]) or not 1 <= lines[0] <= lines[1] <= 10 ** 6):
                raise ValueError("lines must be [first, last], counted from 1")
    _opt_int(params, "max_output_chars", 200, 20000, 8000)
    _opt_int(params, "max_tokens", 64, 8192, 2000)
    _opt_int(params, "temperature_milli", 0, 2000, 700)
    _opt_int(params, "max_answers", 1, 1000, 20)
    if units != 1:
        raise ValueError("an AI question has exactly one unit (one answer per device)")


def _endpoint_ok(endpoint, allow_remote):
    net.check_url(endpoint)
    if not allow_remote and not net.is_loopback(endpoint):
        raise ValueError("the AI endpoint is not on this computer; set ai.allow_remote to use it")


def _auth_headers(endpoint):
    key = os.environ.get("SKYNET_AI_API_KEY", "")
    if key and net.is_private_safe(endpoint):
        return {"Authorization": "Bearer " + key}
    return {}


def list_models(endpoint, timeout=5):
    """Return model ids offered by an OpenAI-compatible server, or raise NetError."""
    body = net.get(endpoint.rstrip("/") + "/models", max_bytes=1 << 20, timeout=timeout,
                   headers=_auth_headers(endpoint))
    data = json.loads(body.decode("utf-8", "replace"))
    out = []
    for item in (data.get("data") or []) if isinstance(data, dict) else []:
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            out.append(item["id"])
    return out


def discover(ai_cfg):
    """Return (endpoint, model) to use, or raise ValueError with a readable reason."""
    allow_remote = bool(ai_cfg.get("allow_remote"))
    wanted = (ai_cfg.get("endpoint") or "").strip()
    candidates = [wanted] if wanted else list(DEFAULT_ENDPOINTS)
    last = "no local AI server found (tried %s)" % ", ".join(candidates)
    for endpoint in candidates:
        try:
            _endpoint_ok(endpoint, allow_remote)
            models = list_models(endpoint)
        except (net.NetError, ValueError) as e:
            last = str(e)
            continue
        model = (ai_cfg.get("model") or "").strip()
        if not model:
            if not models:
                last = "%s lists no models" % endpoint
                continue
            model = models[0]
        return endpoint.rstrip("/"), model
    raise ValueError(last)


def build_prompt(params, base_url):
    """Fetch and verify the context documents; return (system, user) texts."""
    parts = []
    total = 0
    for doc in params.get("context", []):
        url = base_url.rstrip("/") + "/" + doc["path"]
        raw = net.get(url, max_bytes=MAX_DOC_BYTES)
        if hashlib.sha256(raw).hexdigest() != doc["sha256"]:
            raise ValueError("document %s does not match the task (it changed after the task "
                             "was published)" % doc["path"])
        text = raw.decode("utf-8")
        label = doc["path"]
        if doc.get("lines"):
            first, last = doc["lines"]
            text = "\n".join(text.split("\n")[first - 1:last])
            label += " (lines %d-%d)" % (first, last)
        total += len(text)
        if total > MAX_CONTEXT_CHARS:
            raise ValueError("context is larger than %d characters" % MAX_CONTEXT_CHARS)
        parts.append("=== %s ===\n%s\n" % (label, text))
    parts.append("=== TASK ===\n%s\n" % params["question"])
    system = params.get("system") or DEFAULT_SYSTEM
    return system, "\n".join(parts)


def clean_output(text, max_chars):
    text = _THINK_RE.sub("", text).strip()
    text = "".join(ch for ch in text if ch == "\n" or ch == "\t" or ord(ch) >= 32)
    if len(text) > max_chars:
        text = text[:max_chars].rstrip() + "\n[truncated]"
    return text


def run(params, unit, units, ctx=None):
    validate(params, units)
    ctx = ctx or {}
    ai_cfg = ctx.get("ai") or {}
    if not ai_cfg.get("enabled"):
        raise ValueError("AI mode is off on this device")
    endpoint, model = discover(ai_cfg)
    system, user = build_prompt(params, ctx["base_url"])
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "temperature": params.get("temperature_milli", 700) / 1000.0,
        "max_tokens": params.get("max_tokens", 2000),
        "stream": False,
    }
    headers = {"Content-Type": "application/json"}
    headers.update(_auth_headers(endpoint))
    timeout = max(60, int(ai_cfg.get("timeout_minutes", 30)) * 60)
    status, body, _ = net.request(endpoint + "/chat/completions", method="POST",
                                  data=json.dumps(payload).encode("utf-8"),
                                  headers=headers, timeout=timeout, max_bytes=4 << 20)
    if status != 200:
        raise ValueError("the AI server answered HTTP %d" % status)
    reply = json.loads(body.decode("utf-8", "replace"))
    try:
        content = reply["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise ValueError("unexpected answer format from the AI server")
    if not isinstance(content, str) or not content.strip():
        raise ValueError("the AI server returned an empty answer")
    output = clean_output(content, params.get("max_output_chars", 8000))
    if not output:
        raise ValueError("the answer is empty after cleaning")
    result = {
        "kernel": "ai-answer@1",
        "model": str(reply.get("model") or model)[:120],
        "local": net.is_loopback(endpoint),
        "prompt_sha256": hashlib.sha256((system + "\n\n" + user).encode("utf-8")).hexdigest(),
        "output": output,
    }
    usage = reply.get("usage")
    if isinstance(usage, dict):
        result["usage"] = {k: v for k, v in usage.items() if _is_int(v) and k.endswith("_tokens")}
    return result
