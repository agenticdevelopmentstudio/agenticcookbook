"""Read a recipe corpus (a directory of cookbook-shaped markdown files)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from cookbook.core.frontmatter import parse_file
from cookbook.core.markdown import iter_markdown


@dataclass(frozen=True)
class RecipeInfo:
    slug: str
    path: Path
    type: str
    status: str
    body: str


def load_corpus(recipes_dir: Path) -> dict:
    corpus = {}
    for md in iter_markdown(recipes_dir):
        fm = parse_file(md)
        corpus[md.stem] = RecipeInfo(
            slug=md.stem,
            path=md,
            type=str(fm.data.get("type", "") or ""),
            status=str(fm.data.get("status", "") or ""),
            body=fm.body,
        )
    return corpus
