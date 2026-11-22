"""Signed documents: a file plus a detached signature file "<name>.sig".

Signature file format, one signer per line:

    ed25519:<public key hex>:<signature hex>

The signature covers the exact bytes of the file. A document is accepted if
at least one line verifies under a key from trust.RELEASE_KEYS.
"""

import json

from . import ed25519, net, trust


class SignatureError(Exception):
    pass


def format_sig_line(public, signature):
    return "ed25519:%s:%s\n" % (public.hex(), signature.hex())


def parse_sig(sig_bytes):
    """Return a list of (public_key_bytes, signature_bytes) from a .sig file."""
    out = []
    try:
        text = sig_bytes.decode("ascii")
    except UnicodeDecodeError:
        return out
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(":")
        if len(parts) != 3 or parts[0] != "ed25519":
            continue
        try:
            pub = bytes.fromhex(parts[1])
            sig = bytes.fromhex(parts[2])
        except ValueError:
            continue
        if len(pub) == 32 and len(sig) == 64:
            out.append((pub, sig))
    return out


def verify_detached(data, sig_bytes, keys=None):
    """Return the hex of the trusted key that signed data, or raise SignatureError."""
    if keys is None:
        keys = trust.RELEASE_KEYS
    trusted = set(k.lower() for k in keys)
    if not trusted:
        raise SignatureError("no trusted release keys are configured")
    for pub, sig in parse_sig(sig_bytes):
        if pub.hex() in trusted and ed25519.verify(pub, data, sig):
            return pub.hex()
    raise SignatureError("no valid signature from a trusted release key")


def _no_duplicates(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("duplicate key in JSON: %r" % (key,))
        obj[key] = value
    return obj


def _no_constants(name):
    raise ValueError("non-finite number in JSON: %s" % name)


def strict_json_loads(data):
    """Parse UTF-8 JSON; reject duplicate keys and NaN/Infinity."""
    if isinstance(data, (bytes, bytearray)):
        data = bytes(data).decode("utf-8")
    return json.loads(data, object_pairs_hook=_no_duplicates, parse_constant=_no_constants)


def fetch_signed_json(base_url, path, max_bytes=1 << 20, keys=None):
    """Fetch path and path + '.sig' under base_url, verify, parse.

    Returns (object, raw_bytes, sig_bytes). Raises NetError or SignatureError.
    """
    url = base_url.rstrip("/") + "/" + path.lstrip("/")
    raw = net.get(url, max_bytes=max_bytes)
    sig = net.get(url + ".sig", max_bytes=16384)
    verify_detached(raw, sig, keys=keys)
    try:
        obj = strict_json_loads(raw)
    except (ValueError, UnicodeDecodeError) as e:
        raise SignatureError("signed document is not valid JSON: %s" % e)
    if not isinstance(obj, dict):
        raise SignatureError("signed document is not a JSON object")
    return obj, raw, sig
