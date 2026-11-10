"""Locate the bundled `references/` dir at runtime.

The package is installed at ~/.local/bin/_cookr_pkg/ (see ./install).
`references/` lives one level up from the `cookr/` package dir.
"""

from __future__ import annotations

from pathlib import Path

import cookr as _pkg


# What cookr embeds in its own source (reference-manifest.json's `embedded_dir`).
# ./install copies it into `references/`; a source checkout has only this.
EMBEDDED_DIR = "references-src"


def _root() -> Path:
    return Path(_pkg.__file__).resolve().parent.parent


def references_dir() -> Path:
    """Path to the bundled references dir. Created by ./install from the manifest."""
    return _root() / "references"


def embedded(base: Path, name: str) -> Path:
    """`base/name`, or, when `base` lacks it because cookr runs from a source
    checkout that ./install has not built, cookr's embedded copy."""
    path = base / name
    if path.exists():
        return path
    src = _root() / EMBEDDED_DIR / name
    return src if src.exists() else path


def index_configs_dir() -> Path:
    return embedded(references_dir(), "index-configs")


def prompts_dir() -> Path:
    return references_dir() / "prompts"


def prompt_template(name: str) -> str:
    """Read a prompt template (`name` is filename without .md, or full filename)."""
    fn = name if name.endswith(".md") else f"{name}.md"
    return (prompts_dir() / fn).read_text(encoding="utf-8")
