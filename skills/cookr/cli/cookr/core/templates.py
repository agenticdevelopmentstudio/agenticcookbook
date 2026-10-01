"""The ingredient and recipe templates: where they live and which sections they hold.

The `cookbook` package's install materializes the content repo's
`cookbook/ingredients/_template.md` and `cookbook/recipes/_template.md` into its
references dir as `templates/ingredient.md` and `templates/recipe.md` (see
skills/cookbook/cli/reference-manifest.json). That is the single copy cookr
reads: the extract prompt embeds it, and completeness grades a recipe against
its `## ` headings, so a section added to a template is required everywhere at
once instead of in a second hand-kept list.
"""

from __future__ import annotations

import functools
from pathlib import Path

from cookbook.core import history, refs
from cookbook.core.frontmatter import parse_file

TYPES: tuple[str, ...] = ("ingredient", "recipe")


def templates_dir() -> Path:
    """Where the cookbook package's install put the templates."""
    return refs.references_dir() / "templates"


def template_path(rtype: str) -> Path:
    """The template for `rtype`, one of TYPES."""
    if rtype not in TYPES:
        raise ValueError(f"unknown template type `{rtype}`; expected one of: {', '.join(TYPES)}")
    path = templates_dir() / f"{rtype}.md"
    if not path.is_file():
        raise FileNotFoundError(
            f"the {rtype} template is missing: {path}. Run install.sh in the "
            f"agenticcookbook repo to materialize the cookbook package's references."
        )
    return path


def required_sections(rtype: str) -> tuple[str, ...]:
    """The `## ` headings of `rtype`'s template, in template order."""
    return _headings(template_path(rtype))


@functools.cache
def _headings(path: Path) -> tuple[str, ...]:
    # Keyed on the path, so pointing templates_dir elsewhere (as tests do) reads
    # the other copy; a template is read at most once per process. history's
    # history.h2_sections is the one fence-aware `## ` splitter, so a heading shown in a
    # fenced example never reads as a section the template requires.
    return tuple(heading for heading, _ in history.h2_sections(parse_file(path).body))
