#!/usr/bin/env python3
"""One reading of a hook payload, whichever agent sent it.

cookr's own copy of abstractr's `hook_payload`, cut to what the cookr hook uses:
the hook ships inside this skill, so what it imports ships with it. Claude Code
and Codex both carry the session's directory as `cwd`, and the hook process is
not guaranteed to be started anywhere in particular, so a path in a payload
(a `-C <relative>` target on a commit, say) is relative to this, not to the
process cwd.

Public API:

    session_cwd(payload)   -- the directory a relative path in it is relative to
"""
from __future__ import annotations

import os


def session_cwd(payload: dict) -> str:
    """The directory a relative path in this payload is relative to."""
    base = payload.get("cwd") if isinstance(payload, dict) else None
    return base if isinstance(base, str) and base else os.getcwd()
