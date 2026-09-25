"""Read a recipe corpus (a directory of cookbook-shaped markdown files).

The corpus is keyed on file stem, and `iter_markdown` walks recursively, so two
files with the same stem in different subdirectories are one slug with two
sources. That is a corpus error, not a last-writer-wins merge: it raises
CookbookError, which the CLI turns into a clean message and exit 2. So does a
recipe whose frontmatter is not valid YAML or whose bytes are not UTF-8.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from cookbook.core.deps import require
from cookbook.core.errors import CookbookError
from cookbook.core.frontmatter import parse_file
from cookbook.core.markdown import iter_markdown

yaml = require("yaml")


@dataclass(frozen=True)
class RecipeInfo:
    slug: str
    path: Path
    type: str
    status: str
    body: str
    data: dict = field(default_factory=dict)  # the parsed frontmatter


def load_corpus(recipes_dir: Path) -> dict[str, RecipeInfo]:
    corpus = {}
    for md in iter_markdown(recipes_dir):
        if md.stem in corpus:
            raise CookbookError(
                f"duplicate recipe slug `{md.stem}`: {corpus[md.stem].path} and {md}"
            )
        try:
            fm = parse_file(md)
        except (yaml.YAMLError, UnicodeDecodeError) as e:
            raise CookbookError(f"{md}: cannot read recipe (bad YAML frontmatter or not UTF-8) — {e}") from e
        corpus[md.stem] = RecipeInfo(
            slug=md.stem,
            path=md,
            type=str(fm.data.get("type", "") or ""),
            status=str(fm.data.get("status", "") or ""),
            body=fm.body,
            data=dict(fm.data),
        )
    return corpus
