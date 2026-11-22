#!/usr/bin/env python3
"""Release key of the SkyNet research agent (for maintainers).

    python tools/keytool.py generate      create a new release key
    python tools/keytool.py public        print the public key of the stored key
    python tools/keytool.py backup        print the SECRET key for an offline backup
                                          (run it yourself, never through an assistant or a script)
    python tools/keytool.py restore       store a key from such a backup on this computer

The release key signs agent versions and task lists. Whoever holds it can
ship code to every installed agent, so:

  * it is created and kept on the maintainer's own computer, outside the
    repository (default: the folder ".skynet" in the user's profile);
  * on Windows the file is encrypted with DPAPI for the current Windows user;
    elsewhere it is a file readable only by its owner;
  * it is never uploaded, e-mailed or pasted anywhere. Keep an offline backup:
    if the key is lost, installed agents can no longer be updated.

Another location can be given with --key FILE or the SKYNET_RELEASE_KEY variable.
"""

import argparse
import os
import secrets
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "agent"))

from skynet_agent import ed25519  # noqa: E402


def default_key_path():
    env = os.environ.get("SKYNET_RELEASE_KEY")
    if env:
        return os.path.abspath(env)
    name = "release-key.dpapi" if os.name == "nt" else "release-key"
    return os.path.join(os.path.expanduser("~"), ".skynet", name)


def _dpapi(data, protect):
    import ctypes
    from ctypes import wintypes

    class BLOB(ctypes.Structure):
        _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

    crypt32 = ctypes.windll.crypt32
    kernel32 = ctypes.windll.kernel32
    kernel32.LocalFree.argtypes = [ctypes.c_void_p]
    buf = ctypes.create_string_buffer(data, len(data))
    blob_in = BLOB(len(data), ctypes.cast(buf, ctypes.POINTER(ctypes.c_char)))
    blob_out = BLOB()
    func = crypt32.CryptProtectData if protect else crypt32.CryptUnprotectData
    ok = func(ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out))
    if not ok:
        raise OSError("DPAPI call failed (is this the Windows user who created the key?)")
    try:
        return ctypes.string_at(blob_out.pbData, blob_out.cbData)
    finally:
        kernel32.LocalFree(ctypes.cast(blob_out.pbData, ctypes.c_void_p))


def save_seed(path, seed):
    if os.path.exists(path):
        raise FileExistsError("refusing to overwrite the existing key file %s" % path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.name == "nt":
        data = _dpapi(seed, True)
        with open(path, "wb") as f:
            f.write(data)
    else:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="ascii") as f:
            f.write(seed.hex() + "\n")


def load_seed(path=None):
    """Return the 32-byte seed. For tests SKYNET_RELEASE_SEED_HEX may hold a throw-away seed."""
    test_seed = os.environ.get("SKYNET_RELEASE_SEED_HEX")
    if test_seed:
        seed = bytes.fromhex(test_seed)
    else:
        path = path or default_key_path()
        with open(path, "rb") as f:
            data = f.read()
        seed = _dpapi(data, False) if os.name == "nt" else bytes.fromhex(data.decode("ascii").strip())
    if len(seed) != 32:
        raise ValueError("a release key is 32 bytes")
    return seed


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("action", choices=["generate", "public", "backup", "restore"])
    parser.add_argument("--key", help="key file (default: %s)" % default_key_path())
    args = parser.parse_args(argv)
    path = os.path.abspath(args.key) if args.key else default_key_path()
    if args.action == "backup":
        # Prints the secret itself. Only the key holder should run this, by hand,
        # with nobody and nothing else reading the screen.
        try:
            seed = load_seed(path)
        except (OSError, ValueError) as e:
            print("Cannot read the key: %s" % e)
            return 1
        print("SECRET release key (write it down or put it in a password manager, then clear the screen):")
        print(seed.hex())
        print("To restore it on another computer run:  python tools/keytool.py restore")
        return 0
    if args.action == "restore":
        try:
            seed = bytes.fromhex(input("Type or paste the 64-character secret key: ").strip())
            if len(seed) != 32:
                raise ValueError("a release key is 64 hexadecimal characters")
            save_seed(path, seed)
        except (ValueError, OSError) as e:
            print("Not restored: %s" % e)
            return 1
        print("Release key stored: %s" % path)
        print("Public key: %s" % ed25519.public_key(seed).hex())
        return 0
    if args.action == "generate":
        seed = secrets.token_bytes(32)
        try:
            save_seed(path, seed)
        except FileExistsError as e:
            print(e)
            return 1
        print("Release key created: %s" % path)
        print("Public key: %s" % ed25519.public_key(seed).hex())
        print("Make an offline backup of the key file and never upload it.")
        return 0
    try:
        seed = load_seed(path)
    except (OSError, ValueError) as e:
        print("Cannot read the key: %s" % e)
        return 1
    print(ed25519.public_key(seed).hex())
    return 0


if __name__ == "__main__":
    sys.exit(main())
