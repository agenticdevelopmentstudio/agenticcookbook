"""`.cookr.json` — the per-repo description of what cookr scans.

{
  "recipes": "recipes",
  "scheme": "my-repo",
  "roots": [{"path": "...", "tier": "...", "platform": "web|apple|android|windows|python",
             "kind": "ui|logic", "ignore": ["glob", ...]}],
  "ignore": ["glob", ...],
  "aliases": {"component-name": "recipe-slug"},
  "renames": {"path/to/Source.tsx": "component-name"}
}

`path`, `ignore` and `renames` keys are relative to the repo root (the directory
holding the file). `ignore` entries are globstar globs (`cookr.core.inventory`):
`*` stays inside one directory, so `src/*.ts` matches only files directly in
`src/`; write `src/**/*.ts` for every depth.

`renames` names components on purpose. A key is a source file or a directory:
a file key gives that one file its own name, for a file whose stem collides
with a different component elsewhere (`landing/Card.tsx` beside `ui/card.tsx`);
a directory key names every source file below it, so a module directory is one
component and a file added to it later joins that component. A file key beats
any directory key, and the longest directory key wins. `aliases` then folds
*names* into a recipe slug; a rename is applied first, so an aliased name can
be a renamed one.

`kind` says what a root's sources are: `ui` (the default) for visual
components, `logic` for non-UI shared code — models, clients, engines. A
`logic` component's extraction brief carries the non-UI guidance.

A root's own `ignore` applies to that root only — for a directory that mixes
views and models, where the top-level `ignore` would also drop files another
root needs.

`scheme` is the URI scheme of this repo's recipe domains
(`<scheme>://<recipes>/<slug>`). Without it, the scheme is the repo's name
(`cookbook.core.scheme.repo_scheme`): its `origin` remote's basename, else its
main checkout's directory name, so a linked worktree never names it after the
worktree or branch.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Optional

from cookbook.core.errors import CookbookError
from cookbook.core.scheme import repo_scheme

CONFIG_NAME = ".cookr.json"
PLATFORMS = ("web", "apple", "android", "windows", "python")
KINDS = ("ui", "logic")


class ConfigError(CookbookError):
    """Raised when .cookr.json is missing, malformed, or names a bad path."""


@dataclass(frozen=True)
class Root:
    path: str
    tier: str
    platform: str
    kind: str = "ui"
    ignore: tuple = ()


@dataclass(frozen=True)
class Config:
    repo_root: Path
    recipes: str
    roots: list = field(default_factory=list)
    ignore: list = field(default_factory=list)
    aliases: dict = field(default_factory=dict)
    renames: dict = field(default_factory=dict)
    declared_scheme: str = ""  # `.cookr.json`'s `scheme`; "" when it has none

    @cached_property
    def scheme(self) -> str:
        """The declared scheme, else the repo's name. Derived on first use, so only
        a command that writes a domain needs git; raises SchemeError when neither
        resolves."""
        return self.declared_scheme or repo_scheme(self.repo_root)

    @property
    def recipes_dir(self) -> Path:
        return self.repo_root / self.recipes

    def renamed(self, rel: str) -> Optional[str]:
        """The `renames` name for repo-relative source path `rel`: its file key,
        else its longest directory key; None when no key covers it."""
        if rel in self.renames:
            return self.renames[rel]
        parts = rel.split("/")
        for i in range(len(parts) - 1, 0, -1):
            name = self.renames.get("/".join(parts[:i]))
            if name is not None:
                return name
        return None

    def domain(self, slug: str) -> str:
        """Path-derived domain of the recipe for `slug`."""
        return f"{self.scheme}://{self.recipes}/{slug}"

    @property
    def tiers(self) -> list[str]:
        seen = []
        for r in self.roots:
            if r.tier not in seen:
                seen.append(r.tier)
        return seen


def load_config(path: Path) -> Config:
    # The repo root is the directory holding the file as found, not the parent of
    # a symlink's target.
    path = path.parent.resolve() / path.name
    if not path.is_file():
        raise ConfigError(f"no {CONFIG_NAME} at {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ConfigError(f"{path}: invalid JSON — {e}") from e
    if not isinstance(data, dict):
        raise ConfigError(f"{path}: top level must be an object")

    repo_root = path.parent
    recipes = data.get("recipes")
    if not isinstance(recipes, str) or not recipes:
        raise ConfigError(f"{path}: `recipes` must be a non-empty string")
    if not (repo_root / recipes).is_dir():
        raise ConfigError(f"{path}: recipes dir not found: {recipes}")

    raw_roots = data.get("roots")
    if not isinstance(raw_roots, list) or not raw_roots:
        raise ConfigError(f"{path}: `roots` must be a non-empty list")
    roots = []
    for i, r in enumerate(raw_roots):
        if not isinstance(r, dict):
            raise ConfigError(f"{path}: roots[{i}] must be an object")
        for key in ("path", "tier", "platform"):
            if not isinstance(r.get(key), str) or not r[key]:
                raise ConfigError(f"{path}: roots[{i}].{key} must be a non-empty string")
        if r["platform"] not in PLATFORMS:
            raise ConfigError(
                f"{path}: roots[{i}].platform `{r['platform']}` is not one of {', '.join(PLATFORMS)}"
            )
        if not (repo_root / r["path"]).is_dir():
            raise ConfigError(f"{path}: roots[{i}].path not found: {r['path']}")
        kind = r.get("kind", "ui")
        if kind not in KINDS:
            raise ConfigError(f"{path}: roots[{i}].kind `{kind}` is not one of {', '.join(KINDS)}")
        root_ignore = r.get("ignore", [])
        if not isinstance(root_ignore, list) or not all(isinstance(g, str) for g in root_ignore):
            raise ConfigError(f"{path}: roots[{i}].ignore must be a list of strings")
        roots.append(Root(path=r["path"], tier=r["tier"], platform=r["platform"], kind=kind,
                          ignore=tuple(root_ignore)))

    ignore = data.get("ignore", [])
    if not isinstance(ignore, list) or not all(isinstance(g, str) for g in ignore):
        raise ConfigError(f"{path}: `ignore` must be a list of strings")

    aliases = data.get("aliases", {})
    if not isinstance(aliases, dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in aliases.items()
    ):
        raise ConfigError(f"{path}: `aliases` must map strings to strings")

    raw_renames = data.get("renames", {})
    if not isinstance(raw_renames, dict) or not all(
        isinstance(k, str) and k.strip("/") and isinstance(v, str) and v
        for k, v in raw_renames.items()
    ):
        raise ConfigError(f"{path}: `renames` must map source paths to non-empty names")
    renames = {k.strip("/"): v for k, v in raw_renames.items()}
    for rel in renames:
        if not (repo_root / rel).exists():
            raise ConfigError(f"{path}: renames key not found: {rel}")

    scheme = data.get("scheme", "")
    if "scheme" in data and (
        not isinstance(scheme, str) or not scheme or "://" in scheme or "/" in scheme
    ):
        raise ConfigError(f"{path}: `scheme` must be a non-empty name without `/` (got {scheme!r})")

    return Config(repo_root=repo_root, recipes=recipes, roots=roots, ignore=ignore,
                  aliases=aliases, renames=renames, declared_scheme=scheme)
