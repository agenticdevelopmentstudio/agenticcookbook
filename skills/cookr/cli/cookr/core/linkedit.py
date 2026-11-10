"""Rewrite the links inside a cookbook's artifacts, through their source folders.

`edit_links` applies one function to every `depends-on`/`related` value and
another to every part's text, in each artifact folder. A folder with a doc
compiled beside it is edited through the doc (`save_document`) so the two stay
in step. Nothing is bumped: a link edit is not a content change.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from .artifact import (
    Artifact, compose_document, doc_path, edit_text, find_folders, load_folder, read_document,
    save_document, save_folder,
)

LINK_FIELDS = ("depends-on", "related")


def _apply(art: Artifact, value_fn: Callable[[str], str],
           text_fn: Callable[[str], str]) -> tuple[bool, set[str]]:
    meta_changed = False
    for name in LINK_FIELDS:
        values = art.meta.get(name)
        if isinstance(values, list):
            new = [value_fn(v) if isinstance(v, str) else v for v in values]
            if new != values:
                art.meta[name] = new
                meta_changed = True
    changed_parts = set()
    for part in art.parts:
        new_text = text_fn(part.text)
        if new_text != part.text:
            part.text = new_text
            changed_parts.add(part.name)
    return meta_changed, changed_parts


def edit_links(cookbook_dir: Path, value_fn: Callable[[str], str],
               text_fn: Callable[[str], str]) -> list[Path]:
    """Apply the functions across every artifact folder under `cookbook_dir`;
    the folders that changed."""
    changed = []
    for folder in find_folders([Path(cookbook_dir)]):
        doc = doc_path(folder)
        if doc.is_file():
            art = read_document(edit_text(doc))
            meta_changed, parts = _apply(art, value_fn, text_fn)
            if meta_changed or parts:
                save_document(doc, compose_document(art))
                changed.append(folder)
            continue
        art = load_folder(folder)
        meta_changed, parts = _apply(art, value_fn, text_fn)
        if not (meta_changed or parts):
            continue
        save_folder(art, folder)
        changed.append(folder)
    return changed
