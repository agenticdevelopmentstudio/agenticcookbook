"""Read a spec corpus: every cookbook-shaped markdown file under a directory.

A spec is keyed by its path below that directory, without `.md`
(`ai-plugin-kit/chat/chat-context`), so two groups can each hold a
`catalog.md`. A recipe whose frontmatter is not valid YAML or whose bytes are
not UTF-8 raises CookbookError, which the CLI turns into a clean message and
exit 2.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from cookbook.core import refimpl
from cookbook.core.deps import require
from cookbook.core.errors import CookbookError
from cookbook.core.frontmatter import parse_file
from cookbook.core.markdown import iter_markdown

yaml = require("yaml")


@dataclass(frozen=True)
class RecipeInfo:
    slug: str  # the spec's path below the corpus directory, without `.md`
    path: Path
    type: str
    status: str
    body: str
    data: dict = field(default_factory=dict)  # the parsed frontmatter

    @property
    def implementations(self) -> list[refimpl.Implementation]:
        return refimpl.implementations(self.body)


def spec_id(md: Path, base: Path) -> str:
    return md.relative_to(base).with_suffix("").as_posix()


def load_corpus(recipes_dir: Path) -> dict[str, RecipeInfo]:
    corpus = {}
    for md in iter_markdown(recipes_dir):
        slug = spec_id(md, recipes_dir)
        try:
            fm = parse_file(md)
        except (yaml.YAMLError, UnicodeDecodeError) as e:
            raise CookbookError(f"{md}: cannot read recipe (bad YAML frontmatter or not UTF-8) — {e}") from e
        corpus[slug] = RecipeInfo(
            slug=slug,
            path=md,
            type=str(fm.data.get("type", "") or ""),
            status=str(fm.data.get("status", "") or ""),
            body=fm.body,
            data=dict(fm.data),
        )
    return corpus
