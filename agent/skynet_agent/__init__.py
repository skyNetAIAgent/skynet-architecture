"""SkyNet research agent: a volunteer client for the research stage of SkyNet.

It periodically reads signed task lists from the project repository, runs
built-in deterministic computations on this computer, and publishes results.
It never downloads or runs code from tasks. See agent/README.md.
"""

__version__ = "0.1.0"

# Monotonic release number. A signed release with a higher number replaces
# this one; a lower or equal number is ignored (protection against rollback).
RELEASE_SEQ = 1

MIN_PYTHON = (3, 9)
