"""`.cookr.json` — the per-repo description of what cookr scans.

{
  "recipes": "recipes",
  "scheme": "my-repo",
  "roots": [{"path": "...", "tier": "...", "platform": "web|apple|android|windows|python",
             "kind": "ui|logic"}],
  "ignore": ["glob", ...],
  "aliases": {"component-name": "recipe-slug"},
  "renames": {"path/to/Source.tsx": "component-name"}
}

`path`, `ignore` and `renames` keys are relative to the repo root (the directory
holding the file).

`renames` gives one source file its own component name, for a file whose stem
collides with a different component elsewhere (`landing/Card.tsx` beside
`ui/card.tsx`). `aliases` then folds *names* into a recipe slug; a rename is
applied first, so an aliased name can be a renamed one.

`kind` says what a root's sources are: `ui` (the default) for visual
components, `logic` for non-UI shared code — models, clients, engines. A
`logic` component's extraction brief carries the non-UI guidance.

`scheme` is the URI scheme of this repo's recipe domains
(`<scheme>://<recipes>/<slug>`); it defaults to the repo root's directory
name.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

CONFIG_NAME = ".cookr.json"
PLATFORMS = ("web", "apple", "android", "windows", "python")
KINDS = ("ui", "logic")


class ConfigError(Exception):
    """Raised when .cookr.json is missing, malformed, or names a bad path."""


@dataclass(frozen=True)
class Root:
    path: str
    tier: str
    platform: str
    kind: str = "ui"


@dataclass(frozen=True)
class Config:
    repo_root: Path
    recipes: str
    roots: list = field(default_factory=list)
    ignore: list = field(default_factory=list)
    aliases: dict = field(default_factory=dict)
    renames: dict = field(default_factory=dict)
    scheme: str = ""

    @property
    def recipes_dir(self) -> Path:
        return self.repo_root / self.recipes

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
    path = path.resolve()
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
        roots.append(Root(path=r["path"], tier=r["tier"], platform=r["platform"], kind=kind))

    ignore = data.get("ignore", [])
    if not isinstance(ignore, list) or not all(isinstance(g, str) for g in ignore):
        raise ConfigError(f"{path}: `ignore` must be a list of strings")

    aliases = data.get("aliases", {})
    if not isinstance(aliases, dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in aliases.items()
    ):
        raise ConfigError(f"{path}: `aliases` must map strings to strings")

    renames = data.get("renames", {})
    if not isinstance(renames, dict) or not all(
        isinstance(k, str) and isinstance(v, str) and v for k, v in renames.items()
    ):
        raise ConfigError(f"{path}: `renames` must map source paths to non-empty names")
    for rel in renames:
        if not (repo_root / rel).is_file():
            raise ConfigError(f"{path}: renames key not found: {rel}")

    scheme = data.get("scheme", repo_root.name)
    if not isinstance(scheme, str) or not scheme or "://" in scheme or "/" in scheme:
        raise ConfigError(f"{path}: `scheme` must be a non-empty name without `/` (got {scheme!r})")

    return Config(repo_root=repo_root, recipes=recipes, roots=roots, ignore=ignore,
                  aliases=aliases, renames=renames, scheme=scheme)
