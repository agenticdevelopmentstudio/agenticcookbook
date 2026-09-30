"""Structural gates over a built plugin ({relative path: text}).

Each returns a list of error strings; an empty list means the gate passed.
"""

from __future__ import annotations

import posixpath
import re
from collections import deque

from .emit import DESCRIPTION_BUDGET, INDEX_BUDGET
from .groups import NAME_RE

MAX_HOPS = 2
MAX_NAME = 64
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
NAME_LINE_RE = re.compile(r"^name: (.+)$", re.MULTILINE)
DESC_LINE_RE = re.compile(r'^description: "(.*)"$', re.MULTILINE)


def _local_links(path: str, text: str) -> list[str]:
    base = posixpath.dirname(path)
    out = []
    for target in LINK_RE.findall(text):
        if "://" in target or target.startswith(("#", "mailto:")):
            continue
        out.append(posixpath.normpath(posixpath.join(base, target.split("#", 1)[0])))
    return out


def skill_paths(files: dict[str, str]) -> list[str]:
    return sorted(p for p in files if p.startswith("skills/") and p.endswith("/SKILL.md"))


def names(files: dict[str, str]) -> list[str]:
    errors, seen = [], {}
    for path in skill_paths(files):
        m = NAME_LINE_RE.search(files[path])
        name = m.group(1).strip() if m else ""
        dir_name = path.split("/")[1]
        if name != dir_name:
            errors.append(f"{path}: name {name!r} does not match its directory {dir_name!r}")
        if not NAME_RE.match(name) or len(name) > MAX_NAME:
            errors.append(f"{path}: name {name!r} is not lowercase kebab-case of at most {MAX_NAME} chars")
        if name in seen:
            errors.append(f"{path}: name {name!r} already used by {seen[name]}")
        seen[name] = path
    return errors


def descriptions(files: dict[str, str], budget: int = DESCRIPTION_BUDGET) -> list[str]:
    errors = []
    for path in skill_paths(files):
        m = DESC_LINE_RE.search(files[path])
        if not m:
            errors.append(f"{path}: no description")
        elif len(m.group(1)) > budget:
            errors.append(f"{path}: description is {len(m.group(1))} chars, budget {budget}")
    return errors


def links(files: dict[str, str]) -> list[str]:
    errors = []
    for path in sorted(files):
        if not path.endswith(".md"):
            continue
        for target in _local_links(path, files[path]):
            if target not in files:
                errors.append(f"{path}: link to {target} does not resolve")
    return errors


def depth(files: dict[str, str]) -> list[str]:
    """No file reachable from a SKILL.md may be more than MAX_HOPS links away,
    and nothing reachable may link on past it."""
    errors = []
    for skill in skill_paths(files):
        hops = {skill: 0}
        queue = deque([skill])
        while queue:
            path = queue.popleft()
            for target in _local_links(path, files.get(path, "")):
                if target in hops or target not in files:
                    continue
                hops[target] = hops[path] + 1
                if hops[target] > MAX_HOPS:
                    errors.append(f"{skill}: {target} is {hops[target]} hops deep (max {MAX_HOPS})")
                    continue
                queue.append(target)
    return errors


def leaf_sizes(files: dict[str, str], cap: int) -> list[str]:
    return [
        f"{p}: {len(t)} chars exceeds the {cap}-char leaf cap"
        for p, t in sorted(files.items())
        if "/leaves/" in p and len(t) > cap
    ]


def index_sizes(files: dict[str, str], budget: int = INDEX_BUDGET) -> list[str]:
    return [
        f"{p}: {len(t)} chars exceeds the {budget}-char index budget"
        for p, t in sorted(files.items())
        if p.startswith("skills/") and p.endswith("/index.md") and len(t) > budget
    ]


def run_all(files: dict[str, str], cap: int) -> list[str]:
    return (names(files) + descriptions(files) + links(files) + depth(files)
            + leaf_sizes(files, cap) + index_sizes(files))
