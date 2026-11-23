"""SkyNet research agent: a volunteer client for the research stage of SkyNet.

It periodically reads signed task lists from the project repository, runs
built-in deterministic computations on this computer, and publishes results.
It never downloads or runs code from tasks. See agent/README.md.
"""

import os
import sys


def _legacy_bytecode():
    # Older launchers start isolated Python without -B. Importing this first module
    # can already have written its cache before the package gets control.
    home = os.environ.get("SKYNET_AGENT_HOME")
    if sys.dont_write_bytecode or not sys.flags.isolated or not home:
        return
    package = os.path.dirname(__file__)
    versions = os.path.dirname(os.path.dirname(package))
    if os.path.realpath(versions) != os.path.realpath(os.path.join(home, "versions")):
        return
    sys.dont_write_bytecode = True
    cache_dir = os.path.join(package, "__pycache__")
    cached = globals().get("__cached__")
    if cached and os.path.dirname(cached) == cache_dir:
        try:
            os.unlink(cached)
            os.rmdir(cache_dir)
        except OSError:
            pass


_legacy_bytecode()

__version__ = "0.2.1"

# Monotonic release number. A signed release with a higher number replaces
# this one; a lower or equal number is ignored (protection against rollback).
RELEASE_SEQ = 3

MIN_PYTHON = (3, 9)
