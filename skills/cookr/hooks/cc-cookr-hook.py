#!/usr/bin/env python3
"""The recipes-first hook for repos that carry a `.cookr.json`.

One script, four events (spec section 7). The logic lives in cookr; this only
decides whether the event applies and shells out:

  SessionStart / UserPromptSubmit  once per session: a reminder naming
                                   `cookr scope` and the cookr skill, after
                                   `cookr skills sync` (a failure is one more
                                   context line; it never blocks)
  PreToolUse:Bash on a commit      `cookr check --staged --hook`, in the repo
                                   the commit runs in (`git -C <dir>` and
                                   `cd <dir> &&` are followed)
  Stop                             `cookr check --branch --hook`

Exit 2 blocks and its stderr goes back to the agent; a block always carries a
reason (cookr's stderr, else its stdout, else a line naming the check to rerun).
Everything else is exit 0:
a repo without `.cookr.json`, a missing cookr, a state refusal (cookr exit 1),
and any unexpected exception -- this hook must never break a session.

Escape hatch: `CC_ALLOW_COOKR=1` as an environment assignment on the commit
command itself (hook input does not reliably carry the parent environment).

Environment: COOKR_BIN (command line that runs cookr, default `cookr` on PATH),
COOKR_HOME (default ~/.cookr; holds the once-per-session markers).
"""
from __future__ import annotations

import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from hook_payload import session_cwd  # noqa: E402

OVERRIDE = "CC_ALLOW_COOKR=1"
SYNC_TIMEOUT = 300
CHECK_TIMEOUT = 120

REMINDER = (
    "This repo is recipes-first (.cookr.json). Before planning code changes run "
    "`cookr scope` on the planned files and give Mike the minimum and the siblings; "
    "write or update the recipes in the worktree before the code, keep them current, "
    "`cookr confirm` an implementation that matches, then `cookr bump` each changed "
    "recipe and `cookr validate`. Procedure: the cookr skill, \"Working in a cookr repo\"."
)

_COMMIT_RE = re.compile(r"\bgit\s+commit(?![\w-])")
_GLOBAL_ARG_OPTS = frozenset({"-C", "-c", "--git-dir", "--work-tree", "--namespace"})
_SEPARATORS = ("&&", "||", ";", "|", "(", ")", "{", "}")


def find_repo(start: str | Path) -> Path | None:
    """The nearest directory at or above `start` holding `.cookr.json`."""
    here = Path(start).resolve()
    for d in (here, *here.parents):
        if (d / ".cookr.json").is_file():
            return d
    return None


def override_requested(cmd: str) -> bool:
    """Whether `cmd` SETS `CC_ALLOW_COOKR=1` in a leading assignment, rather than
    merely mentioning it (a commit message that documents the override must not
    switch the check off)."""
    try:
        tokens = shlex.split(cmd)
    except ValueError:
        return False
    leading = True
    for token in tokens:
        if token in _SEPARATORS:
            leading = True
            continue
        if not leading:
            continue
        if token == OVERRIDE:
            return True
        if token == "env":
            continue
        name = token.split("=", 1)[0] if "=" in token else ""
        if name and name.isidentifier():
            continue
        leading = False
    return False


def commit_target(cmd: str) -> tuple[bool, str | None]:
    """(is a commit, the directory it runs in if not the session's). The directory
    comes from `git -C <dir>` and from any `cd <dir> &&` (or `;`) before the git,
    so `cd other-repo && git commit` checks other-repo; a relative one is relative
    to the one before it. The VCS binary is matched by basename so an absolute
    path to it counts."""
    try:
        tokens = shlex.split(cmd)
    except ValueError:
        return (bool(_COMMIT_RE.search(cmd)), None)
    cd: str | None = None
    i = 0
    while i < len(tokens):
        # `cd dir && …`, `cd dir ; …`, or `cd dir; …` (shlex keeps the `;` on the word).
        glued = (tokens[i] == "cd" and i + 1 < len(tokens) and len(tokens[i + 1]) > 1
                 and tokens[i + 1].endswith(";"))
        if glued or (tokens[i] == "cd" and i + 2 < len(tokens) and tokens[i + 2] in ("&&", ";")):
            word = tokens[i + 1][:-1] if glued else tokens[i + 1]
            if word != "-":
                d = os.path.expanduser(word)
                cd = d if cd is None or os.path.isabs(d) else os.path.join(cd, d)
            i += 2 if glued else 3
            continue
        if os.path.basename(tokens[i]) != "git":
            i += 1
            continue
        j, target = i + 1, None
        while j < len(tokens) and tokens[j].startswith("-"):
            opt = tokens[j]
            if opt in _GLOBAL_ARG_OPTS and j + 1 < len(tokens):
                if opt == "-C":
                    target = tokens[j + 1]
                j += 2
            else:
                j += 1
        if j < len(tokens) and tokens[j] == "commit":
            if cd is not None:
                target = cd if target is None else os.path.join(cd, os.path.expanduser(target))
            return True, target
        i = j
    return False, None


def cookr_argv() -> list[str] | None:
    """The command that runs cookr, or None when there is none."""
    override = os.environ.get("COOKR_BIN", "").strip()
    if override:
        return shlex.split(override)
    found = shutil.which("cookr")
    return [found] if found else None


def run_cookr(argv: list[str], args: list[str], timeout: int):
    try:
        return subprocess.run(argv + args, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return None


def _marker(session_id: str) -> Path:
    home = Path(os.environ.get("COOKR_HOME") or (Path.home() / ".cookr"))
    safe = re.sub(r"[^A-Za-z0-9._-]", "_", session_id) or "unknown"
    return home / "sessions" / safe


def on_session(event: str, data: dict, repo: Path, argv: list[str]) -> int:
    session_id = data.get("session_id")
    marker = _marker(session_id if isinstance(session_id, str) else "")
    if marker.exists():
        return 0
    lines = [REMINDER]
    sync = run_cookr(argv, ["skills", "sync", "-p", str(repo)], SYNC_TIMEOUT)
    if sync is None:
        lines.append("cookr skills sync failed: could not run cookr")
    elif sync.returncode != 0:
        detail = (sync.stderr or sync.stdout).strip().splitlines()
        lines.append("cookr skills sync failed: " + (detail[-1] if detail else "exit %d" % sync.returncode))
    try:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": event, "additionalContext": "\n".join(lines)}}), flush=True)
    except OSError:
        # Undeliverable: leave no marker so the next prompt sends it again, and
        # point stdout away so interpreter shutdown does not fail on the flush.
        sys.stdout = open(os.devnull, "w")
        return 0
    # Only now: a reminder that was never delivered must be sent again.
    try:
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text("")
    except OSError:
        pass  # no marker: the reminder may repeat, which is harmless
    return 0


def run_check(argv: list[str], scope: str, repo: Path) -> int:
    proc = run_cookr(argv, ["check", scope, "--hook", "-p", str(repo)], CHECK_TIMEOUT)
    if proc is None:
        print("cookr: check could not run", file=sys.stderr)
        return 0
    blocks = proc.returncode in (2, 3)  # 3 (an upgrade happened) blocks like findings
    # A block always carries a reason: stdout when cookr put nothing on stderr.
    text = proc.stderr.strip() or (proc.stdout.strip() if blocks else "")
    if blocks and not text:
        text = f"cookr: cookr check exited {proc.returncode} and gave no reason; run " \
               f"`cookr check {scope}` to see it"
    if text:
        sys.stderr.write(text + "\n")
    if blocks:
        return 2
    return 0  # 0 clean; 1 is a state refusal, a warning only


def main() -> int:
    try:
        data = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return 0
    if not isinstance(data, dict):
        return 0
    event = data.get("hook_event_name")
    cwd = session_cwd(data)

    if event == "PreToolUse":
        if data.get("tool_name") != "Bash":
            return 0
        tool_input = data.get("tool_input")
        cmd = tool_input.get("command") if isinstance(tool_input, dict) else None
        if not isinstance(cmd, str) or not cmd:
            return 0
        is_commit, target = commit_target(cmd)
        if not is_commit or override_requested(cmd):
            return 0
        where = Path(target) if target else Path(cwd)
        if not where.is_absolute():
            where = Path(cwd) / where
    elif event in ("SessionStart", "UserPromptSubmit", "Stop"):
        if event == "Stop" and data.get("stop_hook_active") is True:
            return 0
        where = Path(cwd)
    else:
        return 0

    repo = find_repo(where)
    if repo is None:
        return 0
    argv = cookr_argv()
    if argv is None:
        return 0

    if event == "PreToolUse":
        return run_check(argv, "--staged", repo)
    if event == "Stop":
        return run_check(argv, "--branch", repo)
    return on_session(event, data, repo, argv)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # never crash a session
        print("cookr hook: %s: %s" % (type(exc).__name__, exc), file=sys.stderr)
        sys.exit(0)
