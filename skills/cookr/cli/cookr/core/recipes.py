"""Read a spec corpus: every artifact source folder under a cookbook.

A spec is keyed by its folder's path below the cookbook
(`ai-plugin-kit/chat/chat-context`), so two groups can each hold a `catalog`.
Its implementations are the cookbook index's (`index.json`) rows for its UUID;
a cookbook cookr has not indexed yet has none. A folder that cannot be read
(an older format, a broken manifest) raises CookbookError, which the CLI turns
into a clean message and exit 2.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from cookr.core.artifact import ArtifactError, find_folders, load_folder
from cookr.core.errors import CookbookError
from cookr.core.index import Implementation, Index, current_index


@dataclass(frozen=True)
class RecipeInfo:
    slug: str  # the folder's path below the cookbook
    path: Path  # the source folder
    type: str
    status: str
    body: str
    data: dict = field(default_factory=dict)  # the artifact's meta (its frontmatter)
    id: str = ""
    rdid: str = ""
    implementations: tuple[Implementation, ...] = ()


def spec_id(folder: Path, base: Path) -> str:
    return folder.relative_to(base).as_posix()


def load_corpus(cookbook_dir: Path, index: Optional[Index] = None) -> dict[str, RecipeInfo]:
    """Every artifact folder under `cookbook_dir`, with its index entry's rdid and
    implementations (`index` defaults to `current_index(cookbook_dir)`)."""
    if index is None:
        index = current_index(cookbook_dir)
    corpus = {}
    for folder in find_folders([cookbook_dir]):
        slug = spec_id(folder, cookbook_dir)
        try:
            art = load_folder(folder)
        except (ArtifactError, OSError, UnicodeDecodeError) as e:
            raise CookbookError(f"{folder}: cannot read artifact — {e}") from e
        uid = str(art.meta.get("id", "") or "").lower()
        entry = index.entries.get(uid)
        corpus[slug] = RecipeInfo(
            slug=slug,
            path=folder,
            type=str(art.meta.get("type", "") or ""),
            status=str(art.meta.get("status", "") or ""),
            body=art.body(),
            data=dict(art.meta),
            id=uid,
            rdid=entry.rdid if entry else "",
            implementations=tuple(entry.implementations) if entry else (),
        )
    return corpus
