"""Locate the bundled `references/` dir at runtime.

The package is installed at ~/.local/bin/_cookr_pkg/ (see ./install).
`references/` lives one level up from the `cookr/` package dir.
"""

from __future__ import annotations

from pathlib import Path

import cookr as _pkg


def references_dir() -> Path:
    """Path to the bundled references dir. Created by ./install from the manifest."""
    pkg_dir = Path(_pkg.__file__).resolve().parent
    return pkg_dir.parent / "references"


def index_configs_dir() -> Path:
    return references_dir() / "index-configs"


def prompts_dir() -> Path:
    return references_dir() / "prompts"


def prompt_template(name: str) -> str:
    """Read a prompt template (`name` is filename without .md, or full filename)."""
    fn = name if name.endswith(".md") else f"{name}.md"
    return (prompts_dir() / fn).read_text(encoding="utf-8")
