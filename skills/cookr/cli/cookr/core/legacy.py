"""`.cookr.json` — the per-repo description cookr read before library cookbooks.

cookr now reads `cookbook/cookbook.json` (`cookr.core.config`). This module
reads the old file for one command only: `cookr organize`, which converts a flat
`.cookr.json` corpus into a library cookbook. `legacy_scan` names components the
way cookr used to, so organize can match each old recipe to its sources.

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
import os
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Optional

from cookbook.core.markdown import SKIP_NAMES
from cookbook.core.scheme import repo_scheme

from .config import KINDS, PLATFORMS, ConfigError
from .inventory import SOURCE_SUFFIXES, Component, component_stem, ignore_set
from .naming import kebab

CONFIG_NAME = ".cookr.json"


@dataclass(frozen=True)
class LegacyRoot:
    path: str
    tier: str
    platform: str
    kind: str = "ui"
    ignore: tuple = ()


@dataclass(frozen=True)
class LegacyConfig:
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


def load_legacy(path: Path) -> LegacyConfig:
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
        roots.append(LegacyRoot(path=r["path"], tier=r["tier"], platform=r["platform"], kind=kind,
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

    return LegacyConfig(repo_root=repo_root, recipes=recipes, roots=roots, ignore=ignore,
                  aliases=aliases, renames=renames, declared_scheme=scheme)


def _reserved(slug: str) -> bool:
    """True when `<slug>.md` is a name the recipe corpus never loads."""
    return f"{slug}.md" in SKIP_NAMES


def legacy_scan(config: LegacyConfig) -> list[Component]:
    """Every component source file under the old roots, named as cookr used to
    name them: a `renames` key's name, else the kebab-cased file stem. `tier` is
    the old root's tier. Raises ConfigError on a name the corpus skips."""
    out = []
    for root in config.roots:
        ignored = ignore_set(tuple(config.ignore) + tuple(root.ignore))
        base = config.repo_root / root.path
        for dirpath, dirnames, filenames in os.walk(base):
            d = Path(dirpath)
            drel = d.relative_to(config.repo_root).as_posix()
            prefix = "" if drel == "." else f"{drel}/"
            dirnames[:] = [n for n in dirnames if not ignored.prunes(prefix + n)]
            for fn in filenames:
                if os.path.splitext(fn)[1] not in SOURCE_SUFFIXES:
                    continue
                rel = prefix + fn
                if ignored.ignores(rel) or not (d / fn).is_file():
                    continue
                name = config.renamed(rel) or kebab(component_stem(fn))
                out.append(Component(name=name, path=rel, tier=root.tier, platform=root.platform,
                                     kind=root.kind))
    reserved = sorted(c.path for c in out if _reserved(config.aliases.get(c.name, c.name)))
    if reserved:
        raise ConfigError(
            "component name resolves to a file name the recipe corpus skips "
            f"({', '.join(sorted(SKIP_NAMES))}), so its recipe could never be matched: "
            f"{', '.join(reserved)}. Ignore these files, or give them a name in `renames` "
            f"or `aliases`."
        )
    return sorted(out, key=lambda c: (c.tier, c.name, c.path))
