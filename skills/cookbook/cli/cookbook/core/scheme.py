"""The URI scheme of a repo's domain identifiers (`<scheme>://<path>`).

conventions.md ("URL-Based Domain Identifiers"): the scheme identifies the
source repo. This module is the one place that derives it:

- `repo_scheme(start)` names the git repo holding `start`: the basename of its
  `origin` remote URL, else the name of the repo's MAIN worktree directory —
  never a linked worktree's directory, so every checkout of a repo agrees.
- `cookbook_scheme(root)` is the scheme of a cookbook root: the scheme its own
  `index.md` declares in its frontmatter `domain`, else `repo_scheme(root)`.
  A cookbook whose scheme is not its repo's name (agenticcookbook's is
  `agenticdevelopercookbook`) says so in its index.md.

Both raise SchemeError, naming what to set, when nothing resolves.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from .deps import require
from .errors import CookbookError
from .frontmatter import parse

yaml = require("yaml")

INDEX = "index.md"
# The Agentic Developer Cookbook's own scheme. Any repo may cite its principles,
# guidelines and compliance checks under it.
COOKBOOK_SCHEME = "agenticdevelopercookbook"
_SCHEME = re.compile(r"^([a-z][a-z0-9+.-]*)://", re.IGNORECASE)


class SchemeError(CookbookError):
    """No scheme could be derived for a repo or cookbook root."""


def scheme_of(uri: object) -> str | None:
    """`"x"` for a `"x://..."` string; None for anything else."""
    if not isinstance(uri, str):
        return None
    m = _SCHEME.match(uri.strip())
    return m.group(1) if m else None


def _git(start: Path, *args: str) -> str | None:
    try:
        proc = subprocess.run(
            ["git", "-C", str(start), *args],
            capture_output=True, text=True, check=False,
        )
    except FileNotFoundError:
        return None
    out = proc.stdout.strip()
    return out if proc.returncode == 0 and out else None


def _url_basename(url: str) -> str:
    """`git@host:org/name.git`, `https://host/org/name/`, `/path/name.git` -> `name`."""
    tail = re.split(r"[/:\\]", url.rstrip("/\\"))[-1]
    return tail[:-4] if tail.endswith(".git") else tail


def _main_worktree(start: Path) -> Path | None:
    """The top-level directory of the main worktree of the repo holding `start`.

    `git worktree list` always lists the main worktree first, from any linked
    worktree too; in a submodule it lists the submodule's own checkout.
    """
    listing = _git(start, "worktree", "list", "--porcelain")
    if not listing:
        return None
    first = listing.split("\n\n", 1)[0].splitlines()
    if "bare" in first or not first[0].startswith("worktree "):
        return None
    return Path(first[0][len("worktree "):])


def repo_top(start: Path) -> Path | None:
    """The top-level directory of the checkout holding `start`; None outside git."""
    top = _git(Path(start), "rev-parse", "--show-toplevel")
    return Path(top).resolve() if top else None


def up_to_repo_top(start: Path) -> list[Path]:
    """`start` and its parents up to the top of the checkout holding it, nearest
    first; just `[start]` outside git. Never a directory above the checkout."""
    start = Path(start).resolve()
    top = repo_top(start)
    if top is None or (start != top and top not in start.parents):
        return [start]
    return [start, *[d for d in start.parents if d == top or top in d.parents]]


def repo_scheme(start: Path) -> str:
    """The scheme of the git repo holding `start` (see the module docstring)."""
    start = Path(start)
    url = _git(start, "remote", "get-url", "origin")
    name = _url_basename(url) if url else ""
    if not name:
        main = _main_worktree(start)
        name = main.name if main is not None else ""
    if not name:
        raise SchemeError(
            f"cannot derive a domain scheme for {start}: it is not in a git repo with an "
            f"`origin` remote or a main worktree. Declare one in the cookbook's "
            f"{INDEX} frontmatter (`domain: <scheme>://index`)."
        )
    return name


def declared_scheme(root: Path) -> str | None:
    """The scheme the nearest `index.md` declares, from `root` up to its repo's top.

    `root/index.md` comes first. A root below the cookbook's own top (`-p recipes`)
    has no index.md of its own, so the walk continues upward, but never past the
    top of the git repo holding `root` (or past `root` itself outside git), so an
    unrelated `index.md` above the repo is never read.
    """
    for d in up_to_repo_top(root):
        index = d / INDEX
        if index.is_file():
            try:
                fm = parse(index.read_text(encoding="utf-8"))
            except (OSError, ValueError, yaml.YAMLError):  # unreadable: declares nothing
                fm = None
            scheme = scheme_of(fm.data.get("domain")) if fm is not None else None
            if scheme:
                return scheme
    return None


def cookbook_scheme(root: Path) -> str:
    """The scheme of the cookbook rooted at `root` (see the module docstring)."""
    return declared_scheme(root) or repo_scheme(root)


def index_domain(root: Path, output: Path, path: str) -> str:
    """The domain for a generated file at `output`: the one its frontmatter already
    carries (regeneration keeps it), else `<cookbook_scheme(root)>://<path>`.

    The scheme is derived only when the file has no domain yet, so regenerating an
    existing index never needs git.
    """
    if output.is_file():
        try:
            existing = parse(output.read_text(encoding="utf-8")).data.get("domain")
        except (OSError, ValueError, yaml.YAMLError):
            existing = None
        if isinstance(existing, str) and existing:
            return existing
    return f"{cookbook_scheme(root)}://{path}"
