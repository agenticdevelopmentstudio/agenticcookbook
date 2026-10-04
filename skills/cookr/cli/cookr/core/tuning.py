"""Layered tuning: render shared text for a target, and check it loads there.

Shared source is neutral. A `hosts/` directory beside it holds opt-in
**additions**, one or two per target (see core/hosts.py for targets):

    hosts/claude.add.md            appended to the body
    hosts/claude.opus.add.yaml     frontmatter keys merged in
    hosts/codex.gpt-5-codex.add.md

An addition is never named `<target>.md`: on a case-insensitive filesystem
the host level, `claude.md`, is `CLAUDE.md`, which Claude Code loads as
instructions for the directory it sits in.

A `.yaml` addition is flat `key: value` lines, spliced verbatim: a key already
present is replaced in place (later duplicates dropped), a new key is
appended. Nothing is re-serialized, so quoting and formatting survive. A `.md`
addition is appended after a blank line.

`layers` orders additions by level, then by chain: every level's host, family
and version additions, with a later level (an artifact's own `hosts/`) after
an earlier one (its type template's), so the most specific word is the last
word. With no additions, `render` returns its input unchanged, byte for byte.

**Provenance.** An addition written by a tool records, on its first line, the
hash of the shared source it was written against:

    <!-- cookr:source sha256:<hex> -->      (.md)
    # cookr:source sha256:<hex>             (.yaml)

The stamp is stripped before rendering. When the source changes, `stale`
names the additions written against the old text. A hand-written addition has
no stamp and is never stale.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import yaml

from .hosts import Host, host_of
from .markdown import HOSTS_DIR

KINDS = (".yaml", ".md")
MARK = ".add"

_KEY = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):")
_ADDED = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*): *(\S.*)$")
_TARGET = re.compile(r"^[a-z0-9][a-z0-9-]*(\.[a-z0-9][a-z0-9-]*){0,2}$")
_STAMP_MD = re.compile(r"^<!-- cookr:source sha256:([0-9a-f]{12,64}) -->\n")
_STAMP_YAML = re.compile(r"^# cookr:source sha256:([0-9a-f]{12,64})\n")
_DEBRIS = re.compile(r"(^\.|~$|\.(swp|swo|bak|orig|pyc|pyo)$)")
_FENCE = re.compile(r"^(```|~~~)")


class TuningError(ValueError):
    """An addition cookr cannot apply, or text it cannot render."""


@dataclass(frozen=True)
class Addition:
    path: Path
    target: str
    kind: str                 # ".yaml" | ".md"
    text: str                 # without the provenance stamp
    stamp: Optional[str]      # recorded source hash, None when hand-written


# ── provenance ───────────────────────────────────────────────────────────────

def source_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stamp(text: str, kind: str, digest: str) -> str:
    """`text` as an addition recording `digest`, replacing any earlier stamp."""
    text = _unstamped(text, kind)[0]
    line = (f"<!-- cookr:source sha256:{digest} -->\n" if kind == ".md"
            else f"# cookr:source sha256:{digest}\n")
    return line + text


def _unstamped(text: str, kind: str) -> tuple[str, Optional[str]]:
    m = (_STAMP_MD if kind == ".md" else _STAMP_YAML).match(text)
    return (text[m.end():], m.group(1)) if m else (text, None)


# ── additions ────────────────────────────────────────────────────────────────

def addition_name(target: str, kind: str) -> str:
    """The file name of `target`'s addition of `kind`."""
    return f"{target}{MARK}{kind}"


def parse_name(name: str) -> Optional[tuple[str, str]]:
    """(target, kind) for an addition's file name, None for any other name."""
    for kind in KINDS:
        if name.endswith(MARK + kind):
            return name[:-len(MARK + kind)], kind
    return None


def additions(hosts_dir: Path) -> dict[tuple[str, str], Addition]:
    """The additions in `hosts_dir`, keyed by (target, kind). Editor debris
    is ignored; anything else that is not an addition raises TuningError."""
    found: dict[tuple[str, str], Addition] = {}
    if not hosts_dir.is_dir():
        return found
    for p in sorted(hosts_dir.iterdir()):
        if _DEBRIS.search(p.name):
            continue
        problem = _file_problem(p)
        if problem:
            raise TuningError(problem)
        target, kind = parse_name(p.name)
        text, recorded = _unstamped(p.read_text(encoding="utf-8"), kind)
        found[(target, kind)] = Addition(p, target, kind, text, recorded)
    return found


def _file_problem(p: Path) -> Optional[str]:
    if p.is_symlink() and not p.exists():
        return f"{p} is a broken symlink, not an addition cookr can read"
    if not p.is_file():
        return f"{p} is not a regular file, so it is not an addition cookr can read"
    parsed = parse_name(p.name)
    if parsed is None:
        return (f"{p} is not an addition cookr composes (expected <target>{MARK}.md or "
                f"<target>{MARK}.yaml)")
    if not _TARGET.match(parsed[0]):
        return f"{p}: {parsed[0]!r} is not a target (host, host.family or host.version)"
    return None


def addition_problems(adds: Iterable[Addition], hosts: dict[str, Host]) -> list[str]:
    """What is wrong with each addition before anything is rendered."""
    problems = []
    for a in adds:
        if host_of(a.target) not in hosts:
            problems.append(f"{a.path} is an addition for host {host_of(a.target)!r}, which the "
                            f"manifest does not declare (declared: {', '.join(sorted(hosts))})")
        if a.kind == ".yaml":
            problems += _yaml_problems(a)
    return problems


def _yaml_problems(a: Addition) -> list[str]:
    problems, seen = [], set()
    for n, line in enumerate(a.text.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = _ADDED.match(line)
        if not m:
            problems.append(f'{a.path}:{n}: an addition\'s frontmatter must be "key: value" on one '
                            f"line; got {line!r}")
            continue
        key, value = m.groups()
        if key in seen:
            problems.append(f"{a.path}:{n}: {key} is set twice")
        seen.add(key)
        trap = _plain_scalar_trap(value)
        if trap:
            problems.append(f"{a.path}:{n}: the value of {key} {trap}; quote it if that is what you meant")
    return problems


def _plain_scalar_trap(value: str) -> Optional[str]:
    v = value.strip()
    if (len(v) > 1 and v[0] == v[-1] and v[0] in "'\"") or v[:1] in "[{":
        return None
    if ": " in v:
        return 'contains ": ", which YAML reads as a nested key'
    if v.endswith(":"):
        return 'ends in ":", which YAML reads as a key with no value'
    if " #" in v:
        return 'contains " #", which YAML reads as the start of a comment'
    return None


def layers(levels: Iterable[Path], chain: Iterable[str]) -> list[Addition]:
    """The additions that apply to `chain`, in the order `render` applies
    them. `levels` are `hosts/` directories, least specific first."""
    chain = tuple(chain)
    out = []
    for d in levels:
        found = additions(d)
        for target in chain:
            for kind in KINDS:
                if (target, kind) in found:
                    out.append(found[(target, kind)])
    return out


# ── render ───────────────────────────────────────────────────────────────────

def split(text: str) -> tuple[Optional[list[str]], str]:
    """(frontmatter lines without the fences, body). None when `text` has no
    frontmatter."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], "".join(lines[i + 1:])
    raise TuningError("the text opens a --- frontmatter fence that is never closed")


def _entries(lines: list[str]) -> list[tuple[str, str]]:
    """Frontmatter as (key, text) entries; continuation lines stay with their
    key, and anything before the first key is kept under ""."""
    entries: list[tuple[str, str]] = []
    for line in lines:
        m = _KEY.match(line)
        if m:
            entries.append((m.group(1), line))
        elif entries:
            entries[-1] = (entries[-1][0], entries[-1][1] + line)
        else:
            entries.append(("", line))
    return entries


def merge_frontmatter(lines: list[str], added: str) -> list[str]:
    entries = _entries(lines)
    for line in added.splitlines():
        m = _ADDED.match(line)
        if not m:
            continue
        key, new = m.group(1), line + "\n"
        at = [i for i, (k, _) in enumerate(entries) if k == key]
        if at:
            entries[at[0]] = (key, new)
            entries = [e for i, e in enumerate(entries) if i not in at[1:]]
        else:
            entries.append((key, new))
    return [text for _, text in entries]


def append_body(body: str, added: str) -> str:
    section = added.strip("\n")
    if not section:
        return body
    return f"{body.rstrip(chr(10))}\n\n{section}\n"


def render(text: str, adds: Iterable[Addition]) -> str:
    adds = list(adds)
    if not adds:
        return text
    fm, body = split(text)
    for a in adds:
        if a.kind == ".yaml":
            fm = merge_frontmatter(fm or [], a.text)
        else:
            body = append_body(body, a.text)
    return body if fm is None else "---\n" + "".join(fm) + "---\n" + body


def stale(adds: Iterable[Addition], current: str) -> list[Addition]:
    """Stamped additions written against a source whose hash is not `current`."""
    return [a for a in adds if a.stamp is not None and not current.startswith(a.stamp)]


# ── load rules ───────────────────────────────────────────────────────────────

def load_problems(text: str, host: Host) -> list[str]:
    """Why a rendered skill would not load on `host`; empty when it would.
    Every host needs a name and a real description; `host.rules` adds the
    host's own limits."""
    try:
        fm, body = split(text)
    except TuningError as e:
        return [str(e)]
    if fm is None:
        return [f"has no frontmatter, so {host.name} cannot discover it"]
    try:
        meta = yaml.safe_load("".join(fm)) or {}
    except yaml.YAMLError as e:
        return [f"renders frontmatter that is not valid YAML ({str(e).splitlines()[0]})"]
    if not isinstance(meta, dict):
        return ["renders frontmatter that is not a mapping"]

    rules, problems = host.rules, []
    allowed = rules.get("frontmatter_keys")
    if allowed is not None:
        extra = sorted(set(meta) - set(allowed))
        if extra:
            problems.append(f"renders frontmatter keys {host.name} rejects: {', '.join(extra)} "
                            f"(allowed: {', '.join(sorted(allowed))})")

    name = meta.get("name")
    if not isinstance(name, str) or not name:
        problems.append("renders no `name`")
    else:
        pattern = rules.get("name_pattern")
        if pattern and not re.match(pattern, name):
            problems.append(f"renders name {name!r}, which does not match {pattern}")
        if rules.get("name_max") and len(name) > rules["name_max"]:
            problems.append(f"renders a name of {len(name)} chars (max {rules['name_max']})")

    desc = meta.get("description")
    if not isinstance(desc, str) or not desc.strip():
        problems.append("renders no `description`, so nothing matches an intent to it")
    else:
        if desc.lstrip().startswith("[TODO:"):
            problems.append("renders a placeholder description")
        forbid = [c for c in rules.get("description_forbid", "") if c in desc]
        if forbid:
            problems.append(f"renders a description containing {' or '.join(forbid)}, "
                            f"which {host.name} rejects")
        if rules.get("description_max") and len(desc) > rules["description_max"]:
            problems.append(f"renders a description of {len(desc)} chars "
                            f"(max {rules['description_max']})")

    fenced = False
    for line in body.splitlines():
        if _FENCE.match(line.lstrip()):
            fenced = not fenced
        elif not fenced and line.lstrip().startswith("[TODO:"):
            problems.append("leaves an unfenced [TODO:...] line in the body")
            break
    return problems
