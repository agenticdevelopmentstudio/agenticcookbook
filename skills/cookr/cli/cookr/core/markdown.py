"""Walk a cookbook tree and read/write markdown files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Optional

SKIP_NAMES = {"index.md", "INDEX.md", "references.md", "_template.md"}

# The file that marks an artifact source folder (cookr.core.artifact). Its
# parts are .md files without frontmatter; a walk sees the folder's compiled
# doc beside it instead.
ARTIFACT_FILE = "artifact.json"
# Where a source folder keeps its per-host tuning additions (cookr.core.tuning).
HOSTS_DIR = "hosts"


def part_files(folder: Path) -> Optional[set[str]]:
    """The file names of the parts source folder `folder` lists; None when it
    is not a source folder, or its manifest cannot be read."""
    try:
        data = json.loads((folder / ARTIFACT_FILE).read_text(encoding="utf-8"))
        return {f"{e['part']}.md" for e in data.get("parts", [])}
    except (OSError, ValueError, TypeError, KeyError, AttributeError):
        return None


def in_source_folder(path: Path, root: Path) -> bool:
    """True when `path` is a source folder's own file: a part its manifest
    lists (every `.md` in it, when the manifest is unreadable), or anything in
    a subdirectory of it that is no spec's, such as `hosts/`. A child spec's
    doc kept in its parent's folder (`telemetry/sources.md`, and below it
    `telemetry/sources/…` once `sources.md` exists) is a doc, not a part."""
    d = path.parent
    if (d / ARTIFACT_FILE).is_file():
        parts = part_files(d)
        return parts is None or path.name in parts
    while d == root or root in d.parents:
        if (d / ARTIFACT_FILE).is_file():
            return True                       # in a source folder's non-spec subdirectory
        if d == root or (d.parent / f"{d.name}.md").is_file():
            return False                      # in a spec's own directory, or nothing's
        d = d.parent
    return False


def reserved_name(name: str, cookbook: Optional[Path] = None) -> Optional[str]:
    """Why spec `name` (cookbook-relative, no `.md`) can name no spec, or None:
    its file name is one the corpus skips; it is `hosts`, a source folder's
    additions directory; or its doc would be a part of the parent spec's
    source folder under `cookbook`."""
    parent, _, leaf = name.rpartition("/")
    if f"{leaf}.md" in SKIP_NAMES:
        return f"`{leaf}.md` is a file name the spec corpus skips ({', '.join(sorted(SKIP_NAMES))})"
    if leaf == HOSTS_DIR:
        return f"`{HOSTS_DIR}/` is where a source folder keeps its host additions"
    if cookbook is not None and parent and f"{leaf}.md" in (part_files(cookbook / parent) or ()):
        return f"`{parent}/{leaf}.md` is a part of the `{parent}` source folder"
    return None


def iter_markdown(root: Path, skip_dirs: Iterable[str] = ()) -> list[Path]:
    """Every cookbook `.md` under `root`, leaving out reserved index/template
    names, `skip_dirs` and the parts of source folders."""
    skip = set(skip_dirs)
    out: list[Path] = []
    for p in sorted(root.rglob("*.md")):
        if p.name in SKIP_NAMES:
            continue
        if any(part in skip for part in p.relative_to(root).parts):
            continue
        if in_source_folder(p, root):
            continue
        out.append(p)
    return out
