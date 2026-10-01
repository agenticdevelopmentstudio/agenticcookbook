"""A library cookbook's `cookbook.json`, and the `code` block cookr reads from it.

    <repo>/
      cookbook/
        cookbook.json          {"structure": {"kind": "library", ...},
                                "code": {"roots": [...], "ignore": [...]}, ...}
        ai-plugin-kit/
          chat/chat-context.md
      packages/...

The repo root is the directory holding the cookbook directory. Every path in
`code` and every Reference Implementations path is relative to it.

    "code": {
      "roots": [{"path": "packages/apple/Kit/AIPluginKit", "platform": "apple",
                 "kind": "logic", "recipes": "ai-plugin-kit", "ignore": ["glob", ...]}],
      "ignore": ["glob", ...]
    }

A spec is named by its path in the cookbook: `ai-plugin-kit/chat/chat-context`
is `cookbook/ai-plugin-kit/chat/chat-context.md`, and its domain is
`<scheme>://cookbook/ai-plugin-kit/chat/chat-context`. The scheme is the one
`cookbook validate` uses (`cookbook.core.scheme.cookbook_scheme`): the
cookbook's index.md `domain` scheme, else the repo's name.

The roots only find source files no spec claims yet: such a file is named
`<recipes>/<its directories below the root>/<its stem>`, all kebab-cased
(`naming.path_name`), so a new spec lands where the code's arrangement puts it.
`recipes` defaults to the cookbook's top level. `kind` says what a root's
sources are: `ui` (the default) for visual components, `logic` for non-UI
shared code. `ignore` entries are globstar globs over repo-relative paths
(`cookr.core.inventory`); a root's own `ignore` applies to that root only.

A group is a directory of the cookbook; `--tier` names one (`ai-plugin-kit`, or
a nested `ai-plugin-kit/chat`).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Optional

from cookbook.core.errors import CookbookError
from cookbook.core.scheme import cookbook_scheme

MANIFEST = "cookbook.json"
COOKBOOK_DIR = "cookbook"
PLATFORMS = ("web", "apple", "android", "windows", "python")
KINDS = ("ui", "logic")


class ConfigError(CookbookError):
    """Raised when cookbook.json is missing, malformed, or names a bad path."""


@dataclass(frozen=True)
class Root:
    path: str
    platform: str
    kind: str = "ui"
    recipes: str = ""  # cookbook-relative group for this root's unclaimed files; "" is the top
    ignore: tuple = ()

    @property
    def tier(self) -> str:
        """The top-level group this root's new specs land in; "" for the top level."""
        return self.recipes.split("/", 1)[0]


@dataclass(frozen=True)
class Config:
    repo_root: Path
    cookbook_dir: Path
    roots: list = field(default_factory=list)
    ignore: list = field(default_factory=list)

    @cached_property
    def scheme(self) -> str:
        """Derived on first use, so only a command that writes a domain needs git;
        raises SchemeError when it cannot be derived."""
        return cookbook_scheme(self.cookbook_dir)

    @property
    def cookbook(self) -> str:
        """The cookbook directory, relative to the repo root."""
        return self.cookbook_dir.relative_to(self.repo_root).as_posix()

    # The recipes directory is the cookbook: a spec anywhere in its tree is a recipe.
    @property
    def recipes_dir(self) -> Path:
        return self.cookbook_dir

    def domain(self, spec: str) -> str:
        """Path-derived domain of the spec named `spec` (its cookbook-relative path, no `.md`)."""
        return f"{self.scheme}://{self.cookbook}/{spec}"

    def spec_path(self, spec: str) -> Path:
        return self.cookbook_dir / f"{spec}.md"

    def root_for(self, rel: str) -> Optional[Root]:
        """The root holding repo-relative path `rel`; the deepest when roots nest."""
        best = None
        for r in self.roots:
            if rel == r.path or rel.startswith(r.path.rstrip("/") + "/"):
                if best is None or len(r.path) > len(best.path):
                    best = r
        return best

    def is_group(self, tier: str) -> bool:
        """True when `tier` names a directory of the cookbook or a root's `recipes`."""
        tier = tier.strip("/")
        return bool(tier) and ((self.cookbook_dir / tier).is_dir() or any(
            r.recipes == tier or r.recipes.startswith(tier + "/") for r in self.roots))

    @property
    def tiers(self) -> list[str]:
        """The top-level groups: the cookbook's directories and the roots' `recipes`."""
        seen = {d.name for d in self.cookbook_dir.iterdir()
                if d.is_dir() and not d.name.startswith(".")}
        seen |= {r.tier for r in self.roots if r.tier}
        return sorted(seen)


def find_cookbook(start: Path) -> Optional[Path]:
    """The cookbook directory for `start`: `start/cookbook` or `start` itself when
    it holds the manifest, else the same test on each parent; None when none does."""
    start = start.resolve()
    for d in (start, *start.parents):
        for c in (d / COOKBOOK_DIR, d):
            if (c / MANIFEST).is_file():
                return c
    return None


def _strings(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(g, str) for g in value)


def load_config(cookbook_dir: Path) -> Config:
    """The `code` block of `cookbook_dir/cookbook.json`."""
    # The repo root is the directory holding the cookbook as found, not the
    # parent of a symlink's target.
    cookbook_dir = cookbook_dir.parent.resolve() / cookbook_dir.name
    path = cookbook_dir / MANIFEST
    if not path.is_file():
        raise ConfigError(f"no {MANIFEST} at {cookbook_dir}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ConfigError(f"{path}: invalid JSON — {e}") from e
    if not isinstance(data, dict):
        raise ConfigError(f"{path}: top level must be an object")
    code = data.get("code")
    if not isinstance(code, dict):
        raise ConfigError(f"{path}: no `code` block; cookr needs `code.roots` to find source files")

    repo_root = cookbook_dir.parent
    raw_roots = code.get("roots")
    if not isinstance(raw_roots, list) or not raw_roots:
        raise ConfigError(f"{path}: `code.roots` must be a non-empty list")
    roots = []
    for i, r in enumerate(raw_roots):
        where = f"{path}: code.roots[{i}]"
        if not isinstance(r, dict):
            raise ConfigError(f"{where} must be an object")
        for key in ("path", "platform"):
            if not isinstance(r.get(key), str) or not r[key]:
                raise ConfigError(f"{where}.{key} must be a non-empty string")
        if r["platform"] not in PLATFORMS:
            raise ConfigError(f"{where}.platform `{r['platform']}` is not one of {', '.join(PLATFORMS)}")
        rel = r["path"].strip("/")
        if not (repo_root / rel).is_dir():
            raise ConfigError(f"{where}.path not found: {r['path']}")
        kind = r.get("kind", "ui")
        if kind not in KINDS:
            raise ConfigError(f"{where}.kind `{kind}` is not one of {', '.join(KINDS)}")
        recipes = r.get("recipes", "")
        if not isinstance(recipes, str) or ".." in recipes.split("/"):
            raise ConfigError(f"{where}.recipes must be a directory inside the cookbook")
        if not _strings(r.get("ignore", [])):
            raise ConfigError(f"{where}.ignore must be a list of strings")
        roots.append(Root(path=rel, platform=r["platform"], kind=kind, recipes=recipes.strip("/"),
                          ignore=tuple(r.get("ignore", []))))

    ignore = code.get("ignore", [])
    if not _strings(ignore):
        raise ConfigError(f"{path}: `code.ignore` must be a list of strings")
    return Config(repo_root=repo_root, cookbook_dir=cookbook_dir, roots=roots, ignore=list(ignore))
