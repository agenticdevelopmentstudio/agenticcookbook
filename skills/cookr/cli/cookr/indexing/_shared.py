"""Shared helpers for index strategies."""

from __future__ import annotations

import os
import uuid
from datetime import date
from pathlib import Path

from ..core.artifact import ArtifactError, doc_path, find_folders, is_folder, load_folder
from ..core.deps import require
from ..core.frontmatter import parse

yaml = require("yaml")

from ..core.markdown import iter_markdown


def _folder(path: Path) -> Path | None:
    """The source folder whose doc `path` is, when there is one."""
    folder = path.with_suffix("")
    return folder if is_folder(folder) else None


def meta_of(path: Path) -> dict:
    """An artifact's metadata: its source folder's, else its doc's frontmatter.
    The folder is the committed form, so its doc need not exist."""
    folder = _folder(path)
    if folder is not None:
        try:
            return dict(load_folder(folder).meta)
        except ArtifactError:
            return {}
    if path.exists():
        fm = parse(path.read_text(encoding="utf-8"))
        if fm.had_frontmatter:
            return dict(fm.data)
    return {}


def title_of(path: Path) -> str:
    """Metadata `title` if present; else humanized filename stem."""
    title = meta_of(path).get("title")
    if isinstance(title, str):
        return title
    return path.stem.replace("-", " ").replace("_", " ").title()


def link_of(path: Path, base: Path) -> str:
    """A link from `base` to an artifact: its source folder (with a trailing
    `/`), which a checkout holds, else its doc."""
    folder = _folder(path)
    if folder is not None:
        return os.path.relpath(folder, base) + "/"
    return os.path.relpath(path, base)


def iter_artifacts(d: Path) -> list[Path]:
    """The artifacts under `d`, each as the path of its doc: every source
    folder's (whether or not compiled) and every loose doc (`iter_markdown`)."""
    docs = set(iter_markdown(d))
    docs.update(doc_path(f) for f in find_folders([d]))
    return sorted(docs)


def merge_index_frontmatter(
    output_path: Path,
    *,
    title: str,
    summary: str,
    today: date,
    type_: str = "reference",
) -> dict:
    """Return frontmatter dict for an INDEX.md. Prefers existing values when present
    so user edits to title/summary survive regeneration. A format-1 `domain` is dropped."""
    data: dict = {}
    if output_path.exists():
        fm = parse(output_path.read_text(encoding="utf-8"))
        if fm.had_frontmatter:
            data = dict(fm.data)
    today_s = today.isoformat()
    base = {
        "id": data.get("id") or str(uuid.uuid4()),
        "title": data.get("title") or title,
        "type": type_,
        "version": data.get("version") or "1.0.0",
        "status": data.get("status") or "draft",
        "language": data.get("language") or "en",
        "created": data.get("created") or today_s,
        "modified": today_s,
        "author": data.get("author", ""),
        "copyright": data.get("copyright", f"{today.year}"),
        "license": data.get("license") or "MIT",
        "summary": data.get("summary") or summary,
    }
    # preserve any extras
    for k, v in data.items():
        if k not in base and k != "domain":
            base[k] = v
    return base


def extract_change_history(output_path: Path) -> str:
    """If the existing INDEX.md has a trailing `## Change History` section, return
    that section's text (heading + body) so we can append it verbatim after
    regenerating the body. Returns "" when none exists."""
    if not output_path.exists():
        return ""
    text = output_path.read_text(encoding="utf-8")
    marker = "\n## Change History"
    idx = text.find(marker)
    if idx == -1:
        return ""
    return text[idx + 1 :].rstrip() + "\n"


def render_frontmatter(data: dict) -> str:
    return "---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n"
