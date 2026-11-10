"""Register and unregister the cookr hook in a Claude Code settings.json.

Importable by `install` and `uninstall` (which sit beside this file) and by the
tests, which pass a tmp settings path. Standard library only.

The hook is one command registered for four events: SessionStart and
UserPromptSubmit with no matcher, PreToolUse with matcher `Bash`, and Stop.
Registering twice adds nothing; unregistering removes only entries running the
cookr hook script and leaves every other hook alone.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

HOOK_SCRIPT = "cc-cookr-hook.py"

# event -> matcher (None: the group carries no `matcher` key)
EVENTS: dict[str, str | None] = {
    "SessionStart": None,
    "UserPromptSubmit": None,
    "PreToolUse": "Bash",
    "Stop": None,
}


def hook_command(home: Path) -> str:
    """The command line registered for every event, with the absolute home path."""
    return f"/usr/bin/python3 {home}/.claude/skills/cookr/hooks/{HOOK_SCRIPT}"


def _load(path: Path) -> dict:
    if not path.exists() or path.stat().st_size == 0:
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a JSON object")
    return data


def _write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def _shaped(data: dict, path: Path) -> dict | None:
    """data["hooks"], after checking each level has the shape settings.json defines
    (event -> list of groups, each with a list of hooks). Raises ValueError before
    anything is changed. None when there is no `hooks` key."""
    hooks = data.get("hooks")
    if hooks is None:
        return None
    if not isinstance(hooks, dict):
        raise ValueError(f"{path}: `hooks` is not an object")
    for event, groups in hooks.items():
        if not isinstance(groups, list):
            raise ValueError(f"{path}: hooks.{event} is not a list")
        for group in groups:
            if not isinstance(group, dict) or not isinstance(group.get("hooks"), list):
                raise ValueError(f"{path}: hooks.{event} has a group without a `hooks` list")
    return hooks


def _is_ours(hook: object) -> bool:
    return isinstance(hook, dict) and HOOK_SCRIPT in str(hook.get("command", ""))


def register(settings_path: Path, command: str) -> list[str]:
    """Add the hook for each event that lacks it; returns the events changed.

    An existing entry running `command` for the event (under the same matcher)
    is left as is, so a re-run never duplicates."""
    data = _load(settings_path)
    hooks = _shaped(data, settings_path)
    if hooks is None:
        hooks = data["hooks"] = {}
    changed: list[str] = []
    for event, matcher in EVENTS.items():
        groups = hooks.setdefault(event, [])
        present = any(
            g.get("matcher") == matcher
            and any(isinstance(h, dict) and h.get("command") == command for h in g["hooks"])
            for g in groups
        )
        if present:
            continue
        group: dict = {"hooks": [{"type": "command", "command": command}]}
        if matcher is not None:
            group = {"matcher": matcher, **group}
        groups.append(group)
        changed.append(event)
    if changed:
        _write(settings_path, data)
    return changed


def unregister(settings_path: Path) -> list[str]:
    """Remove every entry running the cookr hook script; returns the events changed.

    Groups and events left empty are dropped; nothing else is touched."""
    if not settings_path.exists():
        return []
    data = _load(settings_path)
    hooks = _shaped(data, settings_path)
    if hooks is None:
        return []
    changed: list[str] = []
    for event in list(hooks):
        groups = hooks[event]
        kept, touched = [], False
        for group in groups:
            inner = group["hooks"]
            if not any(_is_ours(h) for h in inner):
                kept.append(group)
                continue
            touched = True
            rest = [h for h in inner if not _is_ours(h)]
            if rest:
                kept.append({**group, "hooks": rest})
        if not touched:
            continue
        changed.append(event)
        if kept:
            hooks[event] = kept
        else:
            del hooks[event]
    if changed:
        if not hooks:
            del data["hooks"]
        _write(settings_path, data)
    return changed
