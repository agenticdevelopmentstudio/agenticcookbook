"""The artifact source folder: one cookbook artifact as a directory of parts.

A single-file artifact (`<name>.md`: YAML frontmatter + markdown body) becomes

    <name>/
      artifact.json    {"format": 1, "meta": {...frontmatter...}, "parts": [...]}
      intro.md         the body before its first `## ` heading (H1 + statement)
      <slug>.md        one file per `## ` section, heading line excluded
      history.md       the `## Change History` section

`parts` is the ordered list that composes the body. Each entry is
`{"part": <name>}`, plus `"heading"` for every part but the intro. The part's
file is `<part>.md`. The split is lossless: compose(split(body)) == body, byte
for byte. Only the frontmatter is normalized, because JSON holds its values,
not their YAML spelling (see `emit_frontmatter`).

A folder is the source. Every other shape, including the single-file `doc`, is
compiled from it.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml

from .markdown import ARTIFACT_FILE, HOSTS_DIR

FORMAT = 1
ARTIFACT_TYPES = ("principle", "guideline", "ingredient", "recipe")
INTRO = "intro"
HISTORY = "history"
HISTORY_HEADING = "Change History"
RESERVED = frozenset({INTRO, HISTORY, "artifact"})

_FRONTMATTER = re.compile(r"\A---\n(.*?)\n?---\n", re.S)
_FENCE = re.compile(r"^(```|~~~)")

# Frontmatter keys written double-quoted, and keys written as plain dates, so
# a compiled doc reads like a hand-written one. Every other string is plain
# when YAML reads it back unchanged, and double-quoted otherwise.
_QUOTED = frozenset({"title", "summary", "approved-by", "approved-date"})
_DATES = frozenset({"created", "modified"})


class ArtifactError(ValueError):
    """A file or folder that is not a well-formed artifact."""


@dataclass
class Part:
    name: str
    text: str
    heading: Optional[str] = None  # None only for the intro

    def entry(self) -> dict:
        return {"part": self.name} if self.heading is None else {"part": self.name, "heading": self.heading}


@dataclass
class Artifact:
    meta: dict
    parts: list[Part] = field(default_factory=list)
    # Why this artifact's shared text names a host or model, when it must
    # (core/neutrality.py). None: it must not.
    names_hosts: Optional[str] = None
    # Routes for the `skill` target, overriding the derived ones
    # (core/skill.py). None: derive them.
    routes: Optional[list[str]] = None
    # The digest of the doc cookr last wrote from (or folded into) this folder,
    # so a doc and folder that disagree say which one changed (`sync_state`).
    synced: Optional[str] = None

    @property
    def type(self) -> str:
        return str(self.meta.get("type", ""))

    def part(self, name: str) -> Optional[Part]:
        return next((p for p in self.parts if p.name == name), None)

    def body(self) -> str:
        return "".join(
            p.text if p.heading is None else f"## {p.heading}\n{p.text}" for p in self.parts
        )

    def shared_body(self) -> str:
        """The body without its history: what tuning additions are written
        against, so recording a version does not make them stale."""
        return "".join(
            p.text if p.heading is None else f"## {p.heading}\n{p.text}"
            for p in self.parts if p.name != HISTORY
        )


# ── frontmatter ──────────────────────────────────────────────────────────────

def _jsonable(value: Any) -> Any:
    """YAML's dates become ISO strings; everything else is already JSON."""
    if isinstance(value, (_dt.date, _dt.datetime)):
        return value.isoformat()
    if isinstance(value, list):
        return [_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    return value


def parse_frontmatter(text: str) -> dict:
    loaded = yaml.safe_load(text) if text.strip() else {}
    if not isinstance(loaded, dict):
        raise ArtifactError("frontmatter is not a mapping")
    return _jsonable(loaded)


def _plain_ok(s: str) -> bool:
    try:
        return s == s.strip() and s != "" and yaml.safe_load(f"k: {s}") == {"k": s}
    except yaml.YAMLError:
        return False


def _scalar(key: str, value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return json.dumps(value)
    if isinstance(value, str):
        if key in _DATES and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            return value
        if key not in _QUOTED and _plain_ok(value):
            return value
        return json.dumps(value, ensure_ascii=False)
    return json.dumps(value, ensure_ascii=False)


def emit_frontmatter(meta: dict) -> str:
    """Canonical YAML for `meta`: key order kept, block lists, `[]` when empty.
    parse_frontmatter(emit_frontmatter(m)) == m for every JSON-shaped `m`."""
    lines = []
    for key, value in meta.items():
        if isinstance(value, list):
            if not value:
                lines.append(f"{key}: []")
                continue
            lines.append(f"{key}:")
            for item in value:
                if isinstance(item, (dict, list)):
                    raise ArtifactError(f"{key}: nested values are not supported in frontmatter")
                lines.append(f"  - {_scalar(key, item)}")
        elif isinstance(value, dict):
            raise ArtifactError(f"{key}: nested mappings are not supported in frontmatter")
        else:
            rendered = _scalar(key, value)
            lines.append(f"{key}: {rendered}" if rendered else f"{key}:")
    return "\n".join(lines) + "\n"


# ── body ─────────────────────────────────────────────────────────────────────

def _slug(heading: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")
    return s or "section"


def split_body(body: str) -> list[Part]:
    """Split at every `## ` line outside a code fence. Lossless."""
    parts: list[Part] = []
    intro: list[str] = []
    current: Optional[Part] = None
    buf = intro
    fence: Optional[str] = None
    taken: set[str] = set()
    for line in body.splitlines(keepends=True):
        m = _FENCE.match(line)
        if m:
            fence = None if fence == m.group(1) else (fence or m.group(1))
        if fence is None and line.startswith("## "):
            if not line.endswith("\n"):
                raise ArtifactError(f"heading on the last line has no newline: {line!r}")
            if current is not None:
                current.text = "".join(buf)
                parts.append(current)
            heading = line[3:-1]
            name = HISTORY if heading.strip() == HISTORY_HEADING else _slug(heading)
            if name in RESERVED and name != HISTORY or name in taken:
                n = 2
                while f"{name}-{n}" in taken:
                    n += 1
                name = f"{name}-{n}"
            taken.add(name)
            current = Part(name=name, text="", heading=heading)
            buf = []
            continue
        buf.append(line)
    if current is not None:
        current.text = "".join(buf)
        parts.append(current)
    intro_text = "".join(intro)
    return ([Part(name=INTRO, text=intro_text)] if intro_text else []) + parts


# ── single-file document ↔ artifact ──────────────────────────────────────────

def read_document(text: str) -> Artifact:
    m = _FRONTMATTER.match(text)
    if not m:
        raise ArtifactError("no YAML frontmatter")
    return Artifact(meta=parse_frontmatter(m.group(1)), parts=split_body(text[m.end():]))


def compose_document(artifact: Artifact) -> str:
    """The `doc` target: canonical frontmatter + the body, composed from parts."""
    return f"---\n{emit_frontmatter(artifact.meta)}---\n{artifact.body()}"


def normalize_document(text: str) -> str:
    """`text` with only its frontmatter rewritten canonically: what a lossless
    convert-then-compile must reproduce."""
    m = _FRONTMATTER.match(text)
    if not m:
        raise ArtifactError("no YAML frontmatter")
    return f"---\n{emit_frontmatter(parse_frontmatter(m.group(1)))}---\n{text[m.end():]}"


def artifact_type_of(path: Path) -> Optional[str]:
    """The `type` of a single-file artifact, or None when it is not one."""
    try:
        m = _FRONTMATTER.match(path.read_text(encoding="utf-8"))
        meta = yaml.safe_load(m.group(1)) if m else None
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return None
    t = meta.get("type") if isinstance(meta, dict) else None
    return t if t in ARTIFACT_TYPES else None


# ── folder ───────────────────────────────────────────────────────────────────

def is_folder(path: Path) -> bool:
    return (path / ARTIFACT_FILE).is_file()


def load_folder(folder: Path) -> Artifact:
    try:
        data = json.loads((folder / ARTIFACT_FILE).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise ArtifactError(f"{folder / ARTIFACT_FILE}: {e}") from e
    if data.get("format") != FORMAT:
        raise ArtifactError(f"{folder / ARTIFACT_FILE}: unsupported format {data.get('format')!r}")
    parts = []
    for entry in data.get("parts", []):
        name = entry["part"]
        f = folder / f"{name}.md"
        if not f.is_file():
            raise ArtifactError(f"{folder}: part {name!r} has no {f.name}")
        parts.append(Part(name=name, text=f.read_text(encoding="utf-8"), heading=entry.get("heading")))
    return Artifact(meta=data.get("meta", {}), parts=parts, names_hosts=data.get("names_hosts"),
                    routes=data.get("routes"), synced=data.get("synced"))


def dump_manifest(artifact: Artifact) -> str:
    """artifact.json text: indented meta, one line per part, so the part list
    reads as the artifact's table of contents."""
    meta = json.dumps(artifact.meta, indent=2, ensure_ascii=False).replace("\n", "\n  ")
    parts = ",\n".join(f"    {json.dumps(p.entry(), ensure_ascii=False)}" for p in artifact.parts)
    reason = ("" if artifact.names_hosts is None else
              f'  "names_hosts": {json.dumps(artifact.names_hosts, ensure_ascii=False)},\n')
    routes = ("" if artifact.routes is None else
              f'  "routes": {json.dumps(artifact.routes, ensure_ascii=False)},\n')
    synced = "" if artifact.synced is None else f'  "synced": {json.dumps(artifact.synced)},\n'
    return (f'{{\n  "format": {FORMAT},\n  "meta": {meta},\n{reason}{routes}{synced}'
            f'  "parts": [\n{parts}\n  ]\n}}\n')


def _owned(folder: Path) -> set[str]:
    """File names an earlier version of the artifact at `folder` wrote there."""
    if not is_folder(folder):
        return set()
    data = json.loads((folder / ARTIFACT_FILE).read_text(encoding="utf-8"))
    return {ARTIFACT_FILE} | {f"{e['part']}.md" for e in data.get("parts", [])}


def _shared(folder: Path) -> bool:
    """True when `folder` holds anything besides one artifact's own files: a
    spec with child specs keeps them in its folder (`telemetry.md` beside
    `telemetry/sources.md`), so the folder is shared with them."""
    if not folder.is_dir():
        return False
    if not is_folder(folder):
        return any(folder.iterdir())
    return any(f.parent != folder for f in folder.rglob(ARTIFACT_FILE)) or any(
        f.suffix == ".md" and f.name not in _owned(folder) and artifact_type_of(f)
        for f in folder.iterdir() if f.is_file())


def occupied(artifact: Artifact, folder: Path) -> Optional[str]:
    """Why `artifact` cannot be written as `folder`, or None. An artifact owns
    only its manifest and its parts, so a folder it shares is free as long as
    none of those names is already another file's."""
    if folder.exists() and not folder.is_dir():
        return f"{folder} exists and is not a directory"
    parent = folder.parent
    if folder.name == HOSTS_DIR and (is_folder(parent) or doc_path(parent).is_file()):
        return f"{folder} is where {parent.name}'s host additions live; give the spec another name"
    if is_folder(parent) and f"{folder.name}.md" in _owned(parent):
        return f"{doc_path(folder)} is a part of {parent}; give the spec another name"
    if is_folder(folder / HOSTS_DIR):
        return f"{folder / HOSTS_DIR} is a child spec, but this artifact keeps its host additions there"
    if not _shared(folder):
        return None
    mine = _owned(folder)
    taken = sorted(n for n in [ARTIFACT_FILE] + [f"{p.name}.md" for p in artifact.parts]
                   if (folder / n).exists() and n not in mine)
    if taken:
        return f"{folder} already has {', '.join(taken)}, which this artifact would overwrite"
    return None


def write_folder(artifact: Artifact, folder: Path) -> None:
    """Write `artifact` as `folder`. A folder only it uses is replaced whole; a
    folder it shares with child specs or other files keeps them, losing only
    the parts an earlier version wrote. Refuses to overwrite anything it does
    not own (see `occupied`)."""
    problem = occupied(artifact, folder)
    if problem:
        raise ArtifactError(problem)
    if _shared(folder):
        for name in _owned(folder):
            (folder / name).unlink()
    elif folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents=True, exist_ok=True)
    (folder / ARTIFACT_FILE).write_text(dump_manifest(artifact), encoding="utf-8")
    for p in artifact.parts:
        (folder / f"{p.name}.md").write_text(p.text, encoding="utf-8")


def folder_for(md: Path) -> Path:
    return md.with_suffix("")


def doc_path(folder: Path) -> Path:
    return folder.parent / f"{folder.name}.md"


def doc_digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


# What changed in a folder and its doc since cookr last wrote them together.
CURRENT, MISSING, DOC_EDITED, FOLDER_EDITED, BOTH_EDITED = (
    "current", "missing", "doc-edited", "folder-edited", "both-edited")
RECONCILE = {
    DOC_EDITED: "its .md was edited since cookr wrote it: `cookr convert --update` folds the edit "
                "into the folder; `cookr compile --force` discards it",
    FOLDER_EDITED: "its folder was edited since cookr wrote the .md: `cookr compile` writes the .md; "
                   "`cookr convert --update --force` discards the folder's edit",
    BOTH_EDITED: "its .md and its folder were both edited (or cookr has no record of writing "
                 "them): keep one side with `cookr convert --update --force` (the .md) or "
                 "`cookr compile --force` (the folder)",
}


def sync_state(folder: Path) -> str:
    """Which of `folder` and its doc changed since cookr last wrote them together."""
    doc = doc_path(folder)
    if not doc.is_file():
        return MISSING
    text = doc.read_text(encoding="utf-8")
    artifact = load_folder(folder)
    composed = compose_document(artifact)
    if text == composed:
        return CURRENT
    if artifact.synced == doc_digest(composed):
        return DOC_EDITED
    if artifact.synced == doc_digest(text):
        return FOLDER_EDITED
    return BOTH_EDITED


def record_sync(folder: Path, text: str) -> None:
    """Record `text` as the doc `folder` was last written with."""
    artifact = load_folder(folder)
    if artifact.synced != doc_digest(text):
        artifact.synced = doc_digest(text)
        (folder / ARTIFACT_FILE).write_text(dump_manifest(artifact), encoding="utf-8")


def edit_text(doc: Path) -> str:
    """The text a tool edits `doc` from, to hand back to `save_document`: the
    doc, unless its folder changed since; then what the folder compiles to. An
    artifact whose doc and folder both changed raises ArtifactError, since
    either text would discard the other's edit."""
    folder = folder_for(doc)
    if not is_folder(folder):
        return doc.read_text(encoding="utf-8")
    state = sync_state(folder)
    if state == BOTH_EDITED:
        raise ArtifactError(f"{doc}: {RECONCILE[state]}")
    if state in (FOLDER_EDITED, MISSING):
        return compose_document(load_folder(folder))
    return doc.read_text(encoding="utf-8")


def save_document(doc: Path, text: str) -> None:
    """Write `text` (a whole single-file artifact) as `doc`. Read the text to
    edit with `edit_text`, which knows whether the doc or its folder is newer.

    When `doc` is compiled from a source folder, the folder is what changes:
    its manifest and parts are rewritten from `text`, parts `text` no longer
    has are removed, and every other file there (attribution, examples,
    `hosts/`) is kept. `doc` is then recompiled from the folder, so a tool that
    edits the doc form edits the source, and the two never disagree.
    """
    folder = folder_for(doc)
    if not is_folder(folder):
        with open(doc, "w", encoding="utf-8", newline="") as f:  # Path.write_text has no newline= before 3.10
            f.write(text)
        return
    artifact = read_document(text)
    problem = occupied(artifact, folder)
    if problem:
        raise ArtifactError(problem)
    current = load_folder(folder)
    artifact.names_hosts = current.names_hosts
    artifact.routes = current.routes
    for gone in {p.name for p in current.parts} - {p.name for p in artifact.parts}:
        (folder / f"{gone}.md").unlink()
    artifact.synced = doc_digest(compose_document(artifact))
    (folder / ARTIFACT_FILE).write_text(dump_manifest(artifact), encoding="utf-8")
    for p in artifact.parts:
        (folder / f"{p.name}.md").write_text(p.text, encoding="utf-8")
    composed = compose_document(load_folder(folder))
    doc.write_text(composed, encoding="utf-8")
    record_sync(folder, composed)


def find_documents(paths: list[Path]) -> list[Path]:
    """Single-file artifacts under `paths` (files or directories), sorted."""
    found: set[Path] = set()
    for p in paths:
        candidates = [p] if p.is_file() else p.rglob("*.md")
        for c in candidates:
            if c.name.startswith("_") or c.name == "INDEX.md":
                continue
            if artifact_type_of(c):
                found.add(c)
    return sorted(found)


def unconverted(paths: list[Path]) -> list[Path]:
    """Artifact docs under `paths` with no source folder: every command that
    reads folders would pass them over, so they are reported instead."""
    return [d for d in find_documents(paths) if not is_folder(folder_for(d))]


def find_folders(paths: list[Path]) -> list[Path]:
    """Artifact folders under `paths`, sorted."""
    found: set[Path] = set()
    for p in paths:
        if is_folder(p):
            found.add(p)
        elif p.is_dir():
            found.update(f.parent for f in p.rglob(ARTIFACT_FILE))
    return sorted(found)
