# cookr Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the `cookr` skill and CLI so that `cookr inventory`, `cookr coverage` and `cookr prompt extract` run against the `agenticdevelopertoolkit` and `agentictoolkit` repos and report every component's recipe state.

**Architecture:** `skills/cookr/` is a sibling of `skills/cookbook/`, a separate Python package that imports the installed `cookbook` package for frontmatter, markdown walking and console output, and shells out to the `cookbook` CLI for validate and lint. Modules are auto-discovered exactly as in cookbook. `install.sh` is generalised over a list of CLI-carrying skills so both ship the same way.

**Tech Stack:** Python 3.9+, argparse, pyyaml, rich (through `cookbook.core.ui`), pytest.

**Spec:** `docs/superpowers/specs/2026-09-21-cookr-design.md`

## Global Constraints

- Python 3.9 compatible: `from __future__ import annotations` in every module, no `match`, no `X | Y` at runtime.
- All new scripts are Python. `install.sh` and `uninstall.sh` stay shell (named exceptions).
- Dependencies point downward only: `cookr` imports `cookbook`; nothing in `skills/cookbook/` mentions cookr.
- Recipes stay in each target repo's top-level `recipes/`. Nothing in this plan moves them and no recipe gains a `sources:` field.
- cookr's own version starts at `0.1.0`.
- Run tests from the agenticcookbook repo root: `python3 -m pytest skills/cookr/cli/tests/unit -q`.
- Commit after every task with only the files that task touched. Commit messages end with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.
- Work happens in the `cookr` worktree at `.claude/worktrees/cookr` of `~/Development/projects/adh/agenticcookbook`. Tasks 12 and 13 run in the target repos instead and say so.

---

## File map

Created in agenticcookbook:

| Path | Responsibility |
|---|---|
| `skills/cookr/SKILL.md` | thin wrapper: startup check, routing, workflow |
| `skills/cookr/bin/cookr` | shim |
| `skills/cookr/cli/cookr/__init__.py` | `__version__` |
| `skills/cookr/cli/cookr/__main__.py` | `python3 -m cookr` entry |
| `skills/cookr/cli/cookr/cli.py` | parser, context, dispatch |
| `skills/cookr/cli/cookr/registry.py` | module discovery |
| `skills/cookr/cli/cookr/context.py` | `CookrContext` dataclass |
| `skills/cookr/cli/cookr/core/config.py` | `.cookr.json` loading and validation |
| `skills/cookr/cli/cookr/core/naming.py` | kebab-case |
| `skills/cookr/cli/cookr/core/inventory.py` | source walk |
| `skills/cookr/cli/cookr/core/recipes.py` | recipe corpus parse |
| `skills/cookr/cli/cookr/core/completeness.py` | partial/complete rules |
| `skills/cookr/cli/cookr/core/coverage.py` | join |
| `skills/cookr/cli/cookr/modules/inventory.py` | `cookr inventory` |
| `skills/cookr/cli/cookr/modules/coverage.py` | `cookr coverage` |
| `skills/cookr/cli/cookr/modules/prompt/__init__.py`, `prompt_cli.py` | `cookr prompt extract` |
| `skills/cookr/cli/cookr/modules/prompt/prompts/extract/{module.md,actions/extract.md,reference-manifest.json,references/.gitkeep}` | prompt content |
| `skills/cookr/cli/tests/conftest.py`, `unit/*`, `functional/*`, `fixtures/mini-repo/*` | tests |

Modified in agenticcookbook:

| Path | Change |
|---|---|
| `cookbook/ingredients/_template.md`, `cookbook/recipes/_template.md` | two Platform Notes bullets |
| `cookbook/introduction/conventions.md` | one sentence on the WinUI 3 note |
| `install.sh` | CLI-skill table; prompt-manifest glob over both skills |
| `uninstall.sh` | remove cookr shim and package |
| `.gitignore` | cookr materialized references |

Created in the target repos:

| Path | Change |
|---|---|
| `agenticdevelopertoolkit/.cookr.json` | roots, ignore, aliases |
| `agentictoolkit/.cookr.json` | roots, ignore, aliases |

Deleted in `agenticdevelopertoolkit`: `cookbook/` (empty scaffold).

---

### Task 1: Package skeleton, CLI entry, registry, tests harness

**Files:**
- Create: `skills/cookr/cli/cookr/__init__.py`
- Create: `skills/cookr/cli/cookr/__main__.py`
- Create: `skills/cookr/cli/cookr/registry.py`
- Create: `skills/cookr/cli/cookr/context.py`
- Create: `skills/cookr/cli/cookr/cli.py`
- Create: `skills/cookr/cli/cookr/core/__init__.py`
- Create: `skills/cookr/cli/cookr/modules/__init__.py`
- Create: `skills/cookr/bin/cookr`
- Create: `skills/cookr/cli/tests/conftest.py`
- Create: `skills/cookr/cli/tests/unit/test_cli.py`
- Create: `skills/cookr/cli/tests/README.md`

**Interfaces:**
- Produces: `cookr.cli.main(argv: list[str] | None = None) -> int`; `cookr.context.CookrContext(cwd: Path, repo_root: Path | None, config: Config | None, ui: UI)`; `cookr.registry.discover() -> list[ModuleType]`; module protocol `NAME`, `HELP`, `register(parser)`, `run(args, ctx) -> int`.
- Consumes: `cookbook.core.ui.UI`, `cookbook.core.errors.CookbookError`.

- [ ] **Step 1: Write the failing test**

`skills/cookr/cli/tests/conftest.py`:

```python
"""Shared fixtures for the `cookr` test suite.

Layout:
    skills/cookr/cli/cookr/        the package under test
    skills/cookr/cli/tests/        this suite (unit/ + functional/ + fixtures/)

Both `skills/cookr/cli/` and `skills/cookbook/cli/` are pushed onto sys.path so
`import cookr` and `import cookbook` work without running install.sh.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[4]
COOKR_PKG_PARENT = REPO_ROOT / "skills" / "cookr" / "cli"
COOKBOOK_PKG_PARENT = REPO_ROOT / "skills" / "cookbook" / "cli"
for p in (COOKR_PKG_PARENT, COOKBOOK_PKG_PARENT):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

FIXTURES = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture
def mini_repo(tmp_path) -> Path:
    """Fresh, mutable copy of fixtures/mini-repo."""
    dst = tmp_path / "mini-repo"
    shutil.copytree(FIXTURES / "mini-repo", dst)
    return dst


@pytest.fixture
def cookr_bin():
    found = shutil.which("cookr")
    if not found:
        pytest.skip("`cookr` not on PATH — run install.sh first")
    return found


@pytest.fixture
def run_cookr(cookr_bin):
    def _run(args, cwd=None, check=False, env=None):
        return subprocess.run(
            [cookr_bin, *args],
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            check=check,
            env=env,
            timeout=120,
        )

    return _run
```

`skills/cookr/cli/tests/unit/test_cli.py`:

```python
"""Top-level CLI shape: --version, module table, unknown module, -p."""

from __future__ import annotations

import pytest

from cookr import __version__
from cookr.cli import main


def test_version_flag(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_no_args_shows_module_table(capsys):
    assert main([]) == 0
    out = capsys.readouterr().out
    assert "cookr" in out


def test_unknown_module_exits_nonzero():
    with pytest.raises(SystemExit) as exc:
        main(["nope"])
    assert exc.value.code != 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest skills/cookr/cli/tests/unit/test_cli.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'cookr'`

- [ ] **Step 3: Write the package**

`skills/cookr/cli/cookr/__init__.py`:

```python
"""cookr — inventory, coverage and extraction prompts for component recipes."""

__version__ = "0.1.0"
```

`skills/cookr/cli/cookr/__main__.py`:

```python
from cookr.cli import main

raise SystemExit(main())
```

`skills/cookr/cli/cookr/registry.py`:

```python
"""Auto-discover modules in `cookr.modules`.

A module is a file under `cookr/modules/` (or a package with an __init__)
exposing NAME, HELP, register(subparsers) and run(args, ctx).
"""

from __future__ import annotations

import importlib
import pkgutil
from types import ModuleType


def discover() -> list[ModuleType]:
    from . import modules as modules_pkg

    found = []
    for info in pkgutil.iter_modules(modules_pkg.__path__):
        if info.name.startswith("_"):
            continue
        mod = importlib.import_module(f"cookr.modules.{info.name}")
        if all(hasattr(mod, attr) for attr in ("NAME", "HELP", "register", "run")):
            found.append(mod)
    return sorted(found, key=lambda m: m.NAME)
```

`skills/cookr/cli/cookr/context.py`:

```python
"""Per-invocation context handed to every module's run()."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from cookbook.core.ui import UI

from .core.config import Config


@dataclass
class CookrContext:
    cwd: Path
    repo_root: Optional[Path]
    config: Optional[Config]
    ui: UI
```

`skills/cookr/cli/cookr/core/__init__.py` and `skills/cookr/cli/cookr/modules/__init__.py`: empty files.

`skills/cookr/cli/cookr/cli.py`:

```python
"""Top-level CLI entry point.

Usage:
    cookr [--help] [-p PATH] [--version] <module> [module-args]

`-p` names the target repo root (the directory holding `.cookr.json`).
Without it, cookr walks up from cwd to the first directory holding one.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from cookbook.core.errors import CookbookError
from cookbook.core.ui import UI

from . import __version__
from .context import CookrContext
from .core.config import CONFIG_NAME, ConfigError, load_config
from .registry import discover


def find_repo_root(start: Path, explicit: Optional[Path] = None) -> Optional[Path]:
    if explicit is not None:
        p = explicit.expanduser().resolve()
        return p if (p / CONFIG_NAME).is_file() else None
    start = start.resolve()
    for d in (start, *start.parents):
        if (d / CONFIG_NAME).is_file():
            return d
    return None


def _build_parser(modules):
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "-p", "--path", type=Path, default=None,
        help=f"Repo root holding {CONFIG_NAME} (defaults to discovery from cwd).",
    )
    parser = argparse.ArgumentParser(
        prog="cookr",
        description="Inventory, coverage and extraction prompts for component recipes.",
        parents=[common],
    )
    parser.add_argument("--version", action="version", version=f"cookr {__version__}")
    sub = parser.add_subparsers(dest="module", metavar="<module>", required=False)
    for mod in modules:
        sp = sub.add_parser(mod.NAME, help=mod.HELP, description=mod.HELP, parents=[common])
        mod.register(sp)
        sp.set_defaults(_module=mod)
    return parser


def _print_module_table(ui: UI, modules) -> None:
    ui.title(f"cookr {__version__}")
    ui.info("Usage: cookr [-p PATH] <module> [args]")
    ui.blank()
    ui.table(["module", "description"], [[m.NAME, m.HELP] for m in modules], title="Modules")
    ui.blank()
    ui.info("Run `cookr <module> --help` for module-specific options.")


def main(argv: Optional[list] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    ui = UI()
    try:
        modules = discover()
        parser = _build_parser(modules)
        args = parser.parse_args(argv)
        if not getattr(args, "module", None):
            _print_module_table(ui, modules)
            return 0
        cwd = Path.cwd()
        root = find_repo_root(cwd, args.path)
        config = load_config(root / CONFIG_NAME) if root else None
        ctx = CookrContext(cwd=cwd, repo_root=root, config=config, ui=ui)
        return int(args._module.run(args, ctx) or 0)
    except (CookbookError, ConfigError) as e:
        ui.error(str(e))
        return 2
    except KeyboardInterrupt:
        ui.warn("Interrupted.")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
```

Until Task 2 lands, `cli.py` cannot import `Config`. Create a stub `skills/cookr/cli/cookr/core/config.py` now that Task 2 replaces:

```python
"""`.cookr.json` — replaced in full by Task 2."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

CONFIG_NAME = ".cookr.json"


class ConfigError(Exception):
    """Raised when .cookr.json is missing, malformed, or names a bad path."""


@dataclass
class Config:
    repo_root: Path


def load_config(path: Path) -> Config:
    return Config(repo_root=path.parent)
```

`skills/cookr/bin/cookr`:

```bash
#!/usr/bin/env bash
# Shim: run the installed cookr package with the installed cookbook package on the path.
DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="${DIR}/_cookr_pkg:${DIR}/_cookbook_pkg:${PYTHONPATH:-}"
exec python3 -m cookr "$@"
```

Make it executable: `chmod +x skills/cookr/bin/cookr`.

`skills/cookr/cli/tests/README.md`:

```markdown
# `cookr` CLI tests

```
skills/cookr/cli/tests/
  conftest.py       sys.path (cookr + cookbook) and the mini-repo fixture
  fixtures/         mini-repo: a tiny target repo with .cookr.json, sources and recipes
  unit/             in-process, no install
  functional/       subprocess against the installed `cookr` shim; skips if not on PATH
```

Run from the repo root:

```bash
python3 -m pytest skills/cookr/cli/tests/unit -q      # fast
python3 -m pytest skills/cookr/cli/tests -q           # needs ./install.sh
```
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest skills/cookr/cli/tests/unit/test_cli.py -q`
Expected: 3 passed

- [ ] **Step 5: Commit**

```bash
git add skills/cookr
git commit -m "feat(cookr): package skeleton, CLI entry, registry, test harness"
```

---

### Task 2: `.cookr.json` config loader

**Files:**
- Replace: `skills/cookr/cli/cookr/core/config.py`
- Create: `skills/cookr/cli/tests/unit/test_config.py`

**Interfaces:**
- Produces: `Root(path: str, tier: str, platform: str)`; `Config(repo_root: Path, recipes: str, roots: list[Root], ignore: list[str], aliases: dict[str, str])` with `recipes_dir` property; `load_config(path: Path) -> Config`; `ConfigError`; `CONFIG_NAME = ".cookr.json"`; `PLATFORMS = ("web", "apple", "android", "windows")`.

- [ ] **Step 1: Write the failing test**

```python
"""`.cookr.json` loading and validation."""

from __future__ import annotations

import json

import pytest

from cookr.core.config import ConfigError, load_config


def _write(tmp_path, data):
    p = tmp_path / ".cookr.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


def test_loads_minimal_config(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "recipes").mkdir()
    cfg = load_config(_write(tmp_path, {
        "recipes": "recipes",
        "roots": [{"path": "src", "tier": "ui", "platform": "web"}],
    }))
    assert cfg.repo_root == tmp_path
    assert cfg.recipes_dir == tmp_path / "recipes"
    assert cfg.roots[0].tier == "ui"
    assert cfg.ignore == []
    assert cfg.aliases == {}


def test_missing_file_raises(tmp_path):
    with pytest.raises(ConfigError):
        load_config(tmp_path / ".cookr.json")


def test_root_path_must_exist(tmp_path):
    (tmp_path / "recipes").mkdir()
    with pytest.raises(ConfigError, match="src"):
        load_config(_write(tmp_path, {
            "recipes": "recipes",
            "roots": [{"path": "src", "tier": "ui", "platform": "web"}],
        }))


def test_platform_must_be_known(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "recipes").mkdir()
    with pytest.raises(ConfigError, match="platform"):
        load_config(_write(tmp_path, {
            "recipes": "recipes",
            "roots": [{"path": "src", "tier": "ui", "platform": "amiga"}],
        }))


def test_roots_required(tmp_path):
    (tmp_path / "recipes").mkdir()
    with pytest.raises(ConfigError, match="roots"):
        load_config(_write(tmp_path, {"recipes": "recipes"}))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest skills/cookr/cli/tests/unit/test_config.py -q`
Expected: FAIL (the stub accepts anything; `test_root_path_must_exist` and friends fail)

- [ ] **Step 3: Write the loader**

```python
"""`.cookr.json` — the per-repo description of what cookr scans.

{
  "recipes": "recipes",
  "roots": [{"path": "...", "tier": "...", "platform": "web|apple|android|windows"}],
  "ignore": ["glob", ...],
  "aliases": {"component-name": "recipe-slug"}
}

`path` and `ignore` are relative to the repo root (the directory holding the file).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

CONFIG_NAME = ".cookr.json"
PLATFORMS = ("web", "apple", "android", "windows")


class ConfigError(Exception):
    """Raised when .cookr.json is missing, malformed, or names a bad path."""


@dataclass(frozen=True)
class Root:
    path: str
    tier: str
    platform: str


@dataclass(frozen=True)
class Config:
    repo_root: Path
    recipes: str
    roots: list = field(default_factory=list)
    ignore: list = field(default_factory=list)
    aliases: dict = field(default_factory=dict)

    @property
    def recipes_dir(self) -> Path:
        return self.repo_root / self.recipes

    @property
    def tiers(self) -> list:
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
        roots.append(Root(path=r["path"], tier=r["tier"], platform=r["platform"]))

    ignore = data.get("ignore", [])
    if not isinstance(ignore, list) or not all(isinstance(g, str) for g in ignore):
        raise ConfigError(f"{path}: `ignore` must be a list of strings")

    aliases = data.get("aliases", {})
    if not isinstance(aliases, dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in aliases.items()
    ):
        raise ConfigError(f"{path}: `aliases` must map strings to strings")

    return Config(repo_root=repo_root, recipes=recipes, roots=roots, ignore=ignore, aliases=aliases)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest skills/cookr/cli/tests/unit -q`
Expected: 8 passed

- [ ] **Step 5: Commit**

```bash
git add skills/cookr/cli/cookr/core/config.py skills/cookr/cli/tests/unit/test_config.py
git commit -m "feat(cookr): .cookr.json loader with validation"
```

---

### Task 3: Naming and inventory

**Files:**
- Create: `skills/cookr/cli/cookr/core/naming.py`
- Create: `skills/cookr/cli/cookr/core/inventory.py`
- Create: `skills/cookr/cli/tests/unit/test_naming.py`
- Create: `skills/cookr/cli/tests/unit/test_inventory.py`
- Create: fixture `skills/cookr/cli/tests/fixtures/mini-repo/` (sources and config only; recipes come in Task 4)

**Interfaces:**
- Produces: `naming.kebab(stem: str) -> str`; `inventory.Component(name: str, path: str, tier: str, platform: str)`; `inventory.scan(config: Config) -> list[Component]` sorted by `(tier, name, path)`; `inventory.SOURCE_SUFFIXES = (".tsx", ".ts", ".swift", ".kt", ".cs", ".xaml")`.
- Consumes: `Config`, `Root` from Task 2.

- [ ] **Step 1: Create the fixture**

```
skills/cookr/cli/tests/fixtures/mini-repo/
  .cookr.json
  web/components/Button.tsx
  web/components/chat-composer.tsx
  web/components/button.stories.tsx
  web/components/index.ts
  web/blocks/StatCard.tsx
  apple/UI/Button.swift
  apple/UI/ToolbarButton.swift
  recipes/.gitkeep
```

`.cookr.json`:

```json
{
  "recipes": "recipes",
  "roots": [
    {"path": "web/components", "tier": "primitives", "platform": "web"},
    {"path": "web/blocks", "tier": "blocks", "platform": "web"},
    {"path": "apple/UI", "tier": "apple", "platform": "apple"}
  ],
  "ignore": ["**/*.stories.tsx", "**/index.ts"],
  "aliases": {"toolbar-button": "button"}
}
```

Each source file holds one line of its language's comment naming itself, for example `Button.tsx`:

```tsx
// Button — fixture source
export const Button = () => null
```

and `Button.swift`:

```swift
// Button — fixture source
final class Button {}
```

(`chat-composer.tsx`, `button.stories.tsx`, `index.ts`, `StatCard.tsx`, `ToolbarButton.swift` follow the same one-comment-one-declaration shape.)

- [ ] **Step 2: Write the failing tests**

`test_naming.py`:

```python
from __future__ import annotations

import pytest

from cookr.core.naming import kebab


@pytest.mark.parametrize("stem,expected", [
    ("Button", "button"),
    ("ToolbarButton", "toolbar-button"),
    ("chat-composer", "chat-composer"),
    ("StatCard", "stat-card"),
    ("HTMLView", "html-view"),
    ("SemanticPalette+NSColor", "semantic-palette-ns-color"),
    ("use_editable_list", "use-editable-list"),
])
def test_kebab(stem, expected):
    assert kebab(stem) == expected
```

`test_inventory.py`:

```python
from __future__ import annotations

from cookr.core.config import load_config
from cookr.core.inventory import scan


def test_scan_lists_sources_by_tier(mini_repo):
    cfg = load_config(mini_repo / ".cookr.json")
    rows = scan(cfg)
    names = [(r.tier, r.name, r.platform) for r in rows]
    assert names == [
        ("apple", "button", "apple"),
        ("apple", "toolbar-button", "apple"),
        ("blocks", "stat-card", "web"),
        ("primitives", "button", "web"),
        ("primitives", "chat-composer", "web"),
    ]


def test_scan_drops_ignored(mini_repo):
    cfg = load_config(mini_repo / ".cookr.json")
    paths = [r.path for r in scan(cfg)]
    assert "web/components/button.stories.tsx" not in paths
    assert "web/components/index.ts" not in paths


def test_scan_paths_are_repo_relative_posix(mini_repo):
    cfg = load_config(mini_repo / ".cookr.json")
    assert "web/components/Button.tsx" in [r.path for r in scan(cfg)]
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `python3 -m pytest skills/cookr/cli/tests/unit/test_naming.py skills/cookr/cli/tests/unit/test_inventory.py -q`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 4: Write naming and inventory**

`naming.py`:

```python
"""Component names: a file stem rendered as kebab-case."""

from __future__ import annotations

import re

_SPLIT_CAMEL = re.compile(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")
_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def kebab(stem: str) -> str:
    spaced = _SPLIT_CAMEL.sub("-", stem)
    lowered = spaced.lower()
    return _NON_ALNUM.sub("-", lowered).strip("-")
```

`inventory.py`:

```python
"""Walk the configured roots and list component source files."""

from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path

from .config import Config
from .naming import kebab

SOURCE_SUFFIXES = (".tsx", ".ts", ".swift", ".kt", ".cs", ".xaml")


@dataclass(frozen=True)
class Component:
    name: str
    path: str
    tier: str
    platform: str


def _ignored(rel: str, patterns: list) -> bool:
    return any(fnmatch(rel, p) or fnmatch(rel, p.replace("**/", "", 1)) for p in patterns)


def scan(config: Config) -> list:
    out = []
    for root in config.roots:
        base = config.repo_root / root.path
        for f in sorted(base.rglob("*")):
            if not f.is_file() or f.suffix not in SOURCE_SUFFIXES:
                continue
            rel = f.relative_to(config.repo_root).as_posix()
            if _ignored(rel, config.ignore):
                continue
            out.append(Component(name=kebab(f.stem), path=rel, tier=root.tier, platform=root.platform))
    return sorted(out, key=lambda c: (c.tier, c.name, c.path))
```

`fnmatch` treats `**/*.stories.tsx` as `*` matching across `/`, so a pattern with a leading `**/` matches both nested and top-level paths through the two calls above.

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m pytest skills/cookr/cli/tests/unit -q`
Expected: 18 passed

- [ ] **Step 6: Commit**

```bash
git add skills/cookr/cli/cookr/core/naming.py skills/cookr/cli/cookr/core/inventory.py skills/cookr/cli/tests
git commit -m "feat(cookr): kebab naming and source inventory"
```

---

### Task 4: Recipe corpus parse and completeness rules

**Files:**
- Create: `skills/cookr/cli/cookr/core/recipes.py`
- Create: `skills/cookr/cli/cookr/core/completeness.py`
- Create: `skills/cookr/cli/tests/unit/test_recipes.py`
- Create: `skills/cookr/cli/tests/unit/test_completeness.py`
- Add to fixture: `recipes/button.md` (complete), `recipes/stat-card.md` (draft with NEEDS REVIEW), `recipes/chat-composer.md` (no WinUI 3 note), `recipes/site-menu.md` (type recipe, no inventory match)

**Interfaces:**
- Produces: `recipes.RecipeInfo(slug: str, path: Path, type: str, status: str, body: str)`; `recipes.load_corpus(recipes_dir: Path) -> dict[str, RecipeInfo]`; `completeness.REQUIRED_SECTIONS: dict[str, tuple]`; `completeness.problems(info: RecipeInfo) -> list[str]` (empty list means complete).
- Consumes: `cookbook.core.frontmatter.parse_file`, `cookbook.core.markdown.iter_markdown`.

- [ ] **Step 1: Add the fixture recipes**

`recipes/button.md` — complete. Frontmatter as the ingredient template with `status: accepted`, `type: ingredient`, `domain: fixture://recipes/button`. Body has every section in `REQUIRED_SECTIONS["ingredient"]` with one line of text each, and:

```markdown
## Platform Notes

- **SwiftUI**: Use `Button` with a custom `ButtonStyle`.
- **Compose**: `Button` with `ButtonDefaults.buttonColors`.
- **React/Web**: `packages/ui/button.tsx`.
- **AppKit / UIKit**: `NSButton` bezel style `.rounded`.
- **WinUI 3**: `Microsoft.UI.Xaml.Controls.Button` with the `AccentButtonStyle` resource.
```

`recipes/stat-card.md` — `status: draft`, all sections present, one line reading `NEEDS REVIEW: Not implemented in source. Behavior undefined.` under Edge Cases, WinUI 3 bullet filled.

`recipes/chat-composer.md` — `status: accepted`, all sections present, Platform Notes has the three original bullets filled and `- **WinUI 3**:` with nothing after the colon.

`recipes/site-menu.md` — `type: recipe`, `status: accepted`, every section in `REQUIRED_SECTIONS["recipe"]` filled, WinUI 3 bullet filled.

- [ ] **Step 2: Write the failing tests**

`test_recipes.py`:

```python
from __future__ import annotations

from cookr.core.recipes import load_corpus


def test_corpus_keys_are_file_stems(mini_repo):
    corpus = load_corpus(mini_repo / "recipes")
    assert set(corpus) == {"button", "stat-card", "chat-composer", "site-menu"}


def test_corpus_reads_type_and_status(mini_repo):
    corpus = load_corpus(mini_repo / "recipes")
    assert corpus["button"].type == "ingredient"
    assert corpus["button"].status == "accepted"
    assert corpus["site-menu"].type == "recipe"


def test_corpus_skips_index_and_template(mini_repo):
    (mini_repo / "recipes" / "INDEX.md").write_text("# index\n", encoding="utf-8")
    (mini_repo / "recipes" / "_template.md").write_text("---\ntype: ingredient\n---\n", encoding="utf-8")
    assert "INDEX" not in load_corpus(mini_repo / "recipes")
    assert "_template" not in load_corpus(mini_repo / "recipes")
```

`test_completeness.py`:

```python
from __future__ import annotations

from cookr.core.completeness import problems
from cookr.core.recipes import load_corpus


def test_complete_recipe_has_no_problems(mini_repo):
    corpus = load_corpus(mini_repo / "recipes")
    assert problems(corpus["button"]) == []


def test_draft_status_is_a_problem(mini_repo):
    corpus = load_corpus(mini_repo / "recipes")
    assert any("status" in p for p in problems(corpus["stat-card"]))


def test_needs_review_marker_is_a_problem(mini_repo):
    corpus = load_corpus(mini_repo / "recipes")
    assert any("NEEDS REVIEW" in p for p in problems(corpus["stat-card"]))


def test_empty_winui_note_is_a_problem(mini_repo):
    corpus = load_corpus(mini_repo / "recipes")
    assert any("WinUI 3" in p for p in problems(corpus["chat-composer"]))


def test_missing_section_is_a_problem(mini_repo):
    p = mini_repo / "recipes" / "button.md"
    text = p.read_text(encoding="utf-8")
    start = text.index("## States")
    end = text.index("## Accessibility")
    p.write_text(text[:start] + text[end:], encoding="utf-8")
    corpus = load_corpus(mini_repo / "recipes")
    assert any("States" in q for q in problems(corpus["button"]))


def test_empty_section_is_a_problem(mini_repo):
    p = mini_repo / "recipes" / "button.md"
    text = p.read_text(encoding="utf-8")
    start = text.index("## States") + len("## States")
    end = text.index("## Accessibility")
    p.write_text(text[:start] + "\n\n" + text[end:], encoding="utf-8")
    corpus = load_corpus(mini_repo / "recipes")
    assert any("States" in q for q in problems(corpus["button"]))


def test_recipe_type_uses_recipe_sections(mini_repo):
    corpus = load_corpus(mini_repo / "recipes")
    assert problems(corpus["site-menu"]) == []
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `python3 -m pytest skills/cookr/cli/tests/unit/test_recipes.py skills/cookr/cli/tests/unit/test_completeness.py -q`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 4: Write recipes.py and completeness.py**

`recipes.py`:

```python
"""Read a recipe corpus (a directory of cookbook-shaped markdown files)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from cookbook.core.frontmatter import parse_file
from cookbook.core.markdown import iter_markdown


@dataclass(frozen=True)
class RecipeInfo:
    slug: str
    path: Path
    type: str
    status: str
    body: str


def load_corpus(recipes_dir: Path) -> dict:
    corpus = {}
    for md in iter_markdown(recipes_dir):
        fm = parse_file(md)
        corpus[md.stem] = RecipeInfo(
            slug=md.stem,
            path=md,
            type=str(fm.data.get("type", "") or ""),
            status=str(fm.data.get("status", "") or ""),
            body=fm.body,
        )
    return corpus
```

`completeness.py`:

```python
"""The rules that separate a `partial` recipe from a `complete` one.

A recipe is complete when:
1. its status is `review` or `accepted`;
2. its body carries no `NEEDS REVIEW` marker;
3. every section in REQUIRED_SECTIONS[type] is present with at least one
   non-blank body line before the next `##` heading;
4. its Platform Notes section has a `- **WinUI 3**:` bullet with text after the colon.
"""

from __future__ import annotations

import re

from .recipes import RecipeInfo

COMPLETE_STATUSES = ("review", "accepted")
NEEDS_REVIEW = "NEEDS REVIEW"

REQUIRED_SECTIONS = {
    "ingredient": (
        "Overview", "Behavioral Requirements", "Appearance", "States", "Accessibility",
        "Conformance Test Vectors", "Edge Cases", "Configuration", "Platform Notes",
        "Design Decisions",
    ),
    "recipe": (
        "Overview", "Ingredients", "Integration Requirements", "Layout", "Shared State",
        "Integration Test Vectors", "Edge Cases", "Platform Notes", "Design Decisions",
    ),
}

_H2 = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_WINUI = re.compile(r"^-\s+\*\*WinUI 3\*\*:\s*(\S.*)?$", re.MULTILINE)


def sections(body: str) -> dict:
    """Map each `## Heading` to the text up to the next `##` (or `#`) heading."""
    out = {}
    matches = list(_H2.finditer(body))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        chunk = body[start:end]
        # Stop at a top-level heading if one appears before the next ##.
        h1 = re.search(r"^#\s", chunk, re.MULTILINE)
        if h1:
            chunk = chunk[: h1.start()]
        out[m.group(1)] = chunk
    return out


def _has_text(chunk: str) -> bool:
    return any(line.strip() for line in chunk.splitlines())


def problems(info: RecipeInfo) -> list:
    out = []
    if info.status not in COMPLETE_STATUSES:
        out.append(f"status is `{info.status or '(none)'}`, not review/accepted")
    if NEEDS_REVIEW in info.body:
        out.append(f"body carries a `{NEEDS_REVIEW}` marker")
    required = REQUIRED_SECTIONS.get(info.type, REQUIRED_SECTIONS["ingredient"])
    found = sections(info.body)
    for name in required:
        if name not in found:
            out.append(f"section `{name}` is missing")
        elif not _has_text(found[name]):
            out.append(f"section `{name}` is empty")
    notes = found.get("Platform Notes", "")
    m = _WINUI.search(notes)
    if not m or not (m.group(1) or "").strip():
        out.append("Platform Notes has no filled `WinUI 3` bullet")
    return out
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m pytest skills/cookr/cli/tests/unit -q`
Expected: 28 passed

- [ ] **Step 6: Commit**

```bash
git add skills/cookr/cli/cookr/core/recipes.py skills/cookr/cli/cookr/core/completeness.py skills/cookr/cli/tests
git commit -m "feat(cookr): recipe corpus parse and completeness rules"
```

---

### Task 5: Coverage join

**Files:**
- Create: `skills/cookr/cli/cookr/core/coverage.py`
- Create: `skills/cookr/cli/tests/unit/test_coverage.py`

**Interfaces:**
- Produces: `CoverageRow(name: str, tier: str, platforms: tuple, paths: tuple, state: str, recipe: str | None, problems: tuple)`; `STATES = ("missing", "partial", "complete")`; `compute(config: Config, tier: str | None = None) -> CoverageReport`; `CoverageReport(rows: list, unmatched_recipes: list)` with `tally() -> dict[tier, dict[state, int]]` and `below(level: str) -> list` returning rows whose state ranks under `level`.
- Consumes: `inventory.scan`, `recipes.load_corpus`, `completeness.problems`.

- [ ] **Step 1: Write the failing test**

```python
from __future__ import annotations

from cookr.core.config import load_config
from cookr.core.coverage import compute


def _rows(mini_repo, tier=None):
    cfg = load_config(mini_repo / ".cookr.json")
    return compute(cfg, tier=tier)


def test_one_row_per_component_name_within_tier(mini_repo):
    report = _rows(mini_repo)
    keys = [(r.tier, r.name) for r in report.rows]
    assert keys == [
        ("apple", "button"),
        ("apple", "toolbar-button"),
        ("blocks", "stat-card"),
        ("primitives", "button"),
        ("primitives", "chat-composer"),
    ]


def test_states(mini_repo):
    by = {(r.tier, r.name): r for r in _rows(mini_repo).rows}
    assert by[("primitives", "button")].state == "complete"
    assert by[("apple", "button")].state == "complete"
    assert by[("apple", "toolbar-button")].state == "complete"      # alias → button
    assert by[("apple", "toolbar-button")].recipe == "button"
    assert by[("blocks", "stat-card")].state == "partial"
    assert by[("primitives", "chat-composer")].state == "partial"


def test_missing_when_no_recipe(mini_repo):
    (mini_repo / "recipes" / "chat-composer.md").unlink()
    by = {(r.tier, r.name): r for r in _rows(mini_repo).rows}
    assert by[("primitives", "chat-composer")].state == "missing"
    assert by[("primitives", "chat-composer")].recipe is None


def test_tier_filter(mini_repo):
    assert {r.tier for r in _rows(mini_repo, tier="blocks").rows} == {"blocks"}


def test_unmatched_recipes_listed(mini_repo):
    assert _rows(mini_repo).unmatched_recipes == ["site-menu"]


def test_tally_and_below(mini_repo):
    report = _rows(mini_repo)
    assert report.tally()["primitives"] == {"missing": 0, "partial": 1, "complete": 1}
    assert [r.name for r in report.below("complete")] == ["stat-card", "chat-composer"]
    assert report.below("partial") == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest skills/cookr/cli/tests/unit/test_coverage.py -q`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Write coverage.py**

```python
"""Join the source inventory against the recipe corpus."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .completeness import problems
from .config import Config
from .inventory import scan
from .recipes import load_corpus

STATES = ("missing", "partial", "complete")
_RANK = {s: i for i, s in enumerate(STATES)}


@dataclass(frozen=True)
class CoverageRow:
    name: str
    tier: str
    platforms: tuple
    paths: tuple
    state: str
    recipe: Optional[str]
    problems: tuple


@dataclass
class CoverageReport:
    rows: list
    unmatched_recipes: list

    def tally(self) -> dict:
        out = {}
        for r in self.rows:
            t = out.setdefault(r.tier, {s: 0 for s in STATES})
            t[r.state] += 1
        return out

    def below(self, level: str) -> list:
        return [r for r in self.rows if _RANK[r.state] < _RANK[level]]


def compute(config: Config, tier: Optional[str] = None) -> CoverageReport:
    corpus = load_corpus(config.recipes_dir)
    components = [c for c in scan(config) if tier is None or c.tier == tier]

    grouped = {}
    for c in components:
        grouped.setdefault((c.tier, c.name), []).append(c)

    matched_slugs = set()
    rows = []
    for (t, name), items in sorted(grouped.items()):
        slug = config.aliases.get(name, name)
        info = corpus.get(slug)
        if info is None:
            state, recipe, probs = "missing", None, ()
        else:
            matched_slugs.add(slug)
            probs = tuple(problems(info))
            state, recipe = ("partial" if probs else "complete"), slug
        rows.append(CoverageRow(
            name=name, tier=t,
            platforms=tuple(sorted({i.platform for i in items})),
            paths=tuple(i.path for i in items),
            state=state, recipe=recipe, problems=probs,
        ))

    if tier is None:
        unmatched = sorted(s for s in corpus if s not in matched_slugs)
    else:
        unmatched = []
    return CoverageReport(rows=rows, unmatched_recipes=unmatched)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest skills/cookr/cli/tests/unit -q`
Expected: 34 passed

- [ ] **Step 5: Commit**

```bash
git add skills/cookr/cli/cookr/core/coverage.py skills/cookr/cli/tests/unit/test_coverage.py
git commit -m "feat(cookr): coverage join with three states"
```

---

### Task 6: `cookr inventory` and `cookr coverage` modules

**Files:**
- Create: `skills/cookr/cli/cookr/modules/inventory.py`
- Create: `skills/cookr/cli/cookr/modules/coverage.py`
- Create: `skills/cookr/cli/tests/unit/test_modules_inventory.py`
- Create: `skills/cookr/cli/tests/unit/test_modules_coverage.py`

**Interfaces:**
- Produces: CLI `cookr inventory [--tier T] [--json]`, `cookr coverage [--tier T] [--json] [--require partial|complete]`. Exit 2 when no `.cookr.json`; coverage exits 1 when `--require` is not met.
- Consumes: Task 3 `scan`, Task 5 `compute`, `CookrContext`.

- [ ] **Step 1: Write the failing tests**

`test_modules_inventory.py`:

```python
from __future__ import annotations

import json

from cookr.cli import main


def test_inventory_table(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "inventory"]) == 0
    out = capsys.readouterr().out
    assert "toolbar-button" in out
    assert "stories" not in out


def test_inventory_json(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "inventory", "--json"]) == 0
    rows = json.loads(capsys.readouterr().out)
    assert {"name", "path", "tier", "platform"} <= set(rows[0])
    assert len(rows) == 5


def test_inventory_tier_filter(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "inventory", "--tier", "blocks", "--json"]) == 0
    rows = json.loads(capsys.readouterr().out)
    assert [r["name"] for r in rows] == ["stat-card"]


def test_inventory_without_config_exits_2(tmp_path, capsys):
    assert main(["-p", str(tmp_path), "inventory"]) == 2
```

`test_modules_coverage.py`:

```python
from __future__ import annotations

import json

from cookr.cli import main


def test_coverage_table_and_tally(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "coverage"]) == 0
    out = capsys.readouterr().out
    assert "complete" in out and "partial" in out
    assert "site-menu" in out          # unmatched recipe listed


def test_coverage_json_shape(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "coverage", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert set(data) == {"rows", "tally", "unmatched_recipes"}
    row = data["rows"][0]
    assert {"name", "tier", "platforms", "paths", "state", "recipe", "problems"} <= set(row)


def test_require_complete_fails_on_partial(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "coverage", "--require", "complete"]) == 1


def test_require_partial_passes_when_nothing_missing(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "coverage", "--require", "partial"]) == 0


def test_require_partial_fails_on_missing(mini_repo, capsys):
    (mini_repo / "recipes" / "chat-composer.md").unlink()
    assert main(["-p", str(mini_repo), "coverage", "--require", "partial"]) == 1


def test_tier_scoped_require(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "coverage", "--tier", "apple", "--require", "complete"]) == 0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest skills/cookr/cli/tests/unit/test_modules_inventory.py skills/cookr/cli/tests/unit/test_modules_coverage.py -q`
Expected: FAIL (argparse rejects the unknown subcommands with SystemExit 2, and the config-less test passes by accident; the rest fail)

- [ ] **Step 3: Write the modules**

`modules/inventory.py`:

```python
"""`cookr inventory` — list the component source files the config names."""

from __future__ import annotations

import argparse
import json
import sys

from ..core.inventory import scan

NAME = "inventory"
HELP = "List component source files under the configured roots."


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--tier", default=None, help="Only this tier.")
    parser.add_argument("--json", action="store_true", help="Emit JSON rows instead of a table.")


def _require_config(ctx) -> bool:
    if ctx.config is None:
        ctx.ui.error("No .cookr.json found. Run from inside a configured repo, or pass -p <repo-root>.")
        return False
    return True


def run(args, ctx) -> int:
    if not _require_config(ctx):
        return 2
    rows = [c for c in scan(ctx.config) if args.tier is None or c.tier == args.tier]
    if args.json:
        sys.stdout.write(json.dumps([c.__dict__ for c in rows], indent=2) + "\n")
        return 0
    ctx.ui.title(f"cookr inventory · {ctx.repo_root}")
    ctx.ui.table(["tier", "name", "platform", "path"],
                 [[c.tier, c.name, c.platform, c.path] for c in rows])
    ctx.ui.info(f"{len(rows)} source file(s)")
    return 0
```

`modules/coverage.py`:

```python
"""`cookr coverage` — which components have a finished recipe."""

from __future__ import annotations

import argparse
import json
import sys

from ..core.coverage import STATES, compute
from .inventory import _require_config

NAME = "coverage"
HELP = "Report each component as missing, partial or complete against the recipe corpus."


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--tier", default=None, help="Only this tier.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a table.")
    parser.add_argument(
        "--require", choices=("partial", "complete"), default=None,
        help="Exit 1 if any component in scope is below this state.",
    )


def _row_dict(r) -> dict:
    return {
        "name": r.name, "tier": r.tier, "platforms": list(r.platforms),
        "paths": list(r.paths), "state": r.state, "recipe": r.recipe,
        "problems": list(r.problems),
    }


def run(args, ctx) -> int:
    if not _require_config(ctx):
        return 2
    report = compute(ctx.config, tier=args.tier)
    failing = report.below(args.require) if args.require else []

    if args.json:
        sys.stdout.write(json.dumps({
            "rows": [_row_dict(r) for r in report.rows],
            "tally": report.tally(),
            "unmatched_recipes": report.unmatched_recipes,
        }, indent=2) + "\n")
        return 1 if failing else 0

    ctx.ui.title(f"cookr coverage · {ctx.repo_root}")
    ctx.ui.table(
        ["tier", "name", "state", "recipe", "problems"],
        [[r.tier, r.name, r.state, r.recipe or "—", "; ".join(r.problems)] for r in report.rows],
    )
    for tier, counts in report.tally().items():
        ctx.ui.info("  ".join([f"{tier}:"] + [f"{s}={counts[s]}" for s in STATES]))
    if report.unmatched_recipes:
        ctx.ui.section("recipes with no inventory match")
        for slug in report.unmatched_recipes:
            ctx.ui.skip(slug)
    if args.require:
        if failing:
            ctx.ui.error(f"{len(failing)} component(s) below `{args.require}`")
            return 1
        ctx.ui.ok(f"every component in scope is at least `{args.require}`")
    return 0
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest skills/cookr/cli/tests/unit -q`
Expected: 44 passed

- [ ] **Step 5: Commit**

```bash
git add skills/cookr/cli/cookr/modules skills/cookr/cli/tests/unit/test_modules_inventory.py skills/cookr/cli/tests/unit/test_modules_coverage.py
git commit -m "feat(cookr): inventory and coverage commands"
```

---

### Task 7: Template and conventions additions

**Files:**
- Modify: `cookbook/ingredients/_template.md` (Platform Notes, after the `React/Web` bullet)
- Modify: `cookbook/recipes/_template.md` (same)
- Modify: `cookbook/introduction/conventions.md`

**Interfaces:**
- Produces: the `- **WinUI 3**:` bullet that `completeness._WINUI` matches, and the `templates/ingredient.md` / `templates/recipe.md` references Task 8 bundles.

- [ ] **Step 1: Edit both templates**

In each `_template.md`, replace

```markdown
- **SwiftUI**:
- **Compose**:
- **React/Web**:
```

with

```markdown
- **SwiftUI**:
- **Compose**:
- **React/Web**:
- **AppKit / UIKit**:
- **WinUI 3**:
```

- [ ] **Step 2: Edit conventions.md**

Find the Sections / body conventions area (search for `Design Decisions` prose in the file; if no Platform Notes prose exists, add the paragraph directly after the frontmatter field table). Add:

```markdown
### Platform Notes

An ingredient or recipe carries one bullet per platform under `## Platform Notes`:
SwiftUI, Compose, React/Web, AppKit / UIKit, and WinUI 3. The **WinUI 3** bullet
is required for any recipe counted by `cookr coverage`; a recipe with an empty
WinUI 3 bullet reports as `partial`.
```

- [ ] **Step 3: Verify**

Run: `grep -c "WinUI 3" cookbook/ingredients/_template.md cookbook/recipes/_template.md cookbook/introduction/conventions.md`
Expected: `1`, `1`, `2` (or more) respectively.

Run: `cookbook validate -p cookbook`
Expected: exit 0 (the templates are skipped by name; conventions.md is prose under `introduction/` and was valid before).

- [ ] **Step 4: Commit**

```bash
git add cookbook/ingredients/_template.md cookbook/recipes/_template.md cookbook/introduction/conventions.md
git commit -m "docs(cookbook): AppKit/UIKit and WinUI 3 platform notes in templates"
```

---

### Task 8: `cookr prompt extract`

**Files:**
- Create: `skills/cookr/cli/cookr/modules/prompt/__init__.py`
- Create: `skills/cookr/cli/cookr/modules/prompt/prompt_cli.py`
- Create: `skills/cookr/cli/cookr/modules/prompt/prompts/extract/module.md`
- Create: `skills/cookr/cli/cookr/modules/prompt/prompts/extract/actions/extract.md`
- Create: `skills/cookr/cli/cookr/modules/prompt/prompts/extract/reference-manifest.json`
- Create: `skills/cookr/cli/cookr/modules/prompt/prompts/extract/references/.gitkeep`
- Create: `skills/cookr/cli/tests/unit/test_modules_prompt.py`
- Modify: `.gitignore`

**Interfaces:**
- Produces: CLI `cookr prompt extract <name> [--type ingredient|recipe] [--json]`; `prompt_cli.PROMPTS_DIR`; `prompt_cli.build(name, ctx, rtype) -> tuple[str, dict]` returning the prompt and a dict of resolved paths.
- Consumes: `cookbook.modules.prompt.render.assemble_prompt`, `cookbook.modules.prompt.frontmatter.parse`, `scan`, `load_corpus`.

- [ ] **Step 1: Write the prompt content**

`module.md`:

```markdown
---
domain: extract
role: "UI component specification writer"
---
Operate as a specification writer producing one cookbook recipe from source code.

- Describe the code as it is. Every requirement, state, option and edge case
  you write must be traceable to a line in the sources given below. Invent
  nothing.
- Where the template asks for something the sources do not implement, write
  exactly: `NEEDS REVIEW: Not implemented in source. Behavior undefined.`
- Requirements are named kebab-case bullets using RFC 2119 words
  (`- **must-render-label**: The component MUST ...`).
- Fill every section of the template. Do not delete sections.
- Platform Notes must carry all five bullets. The **WinUI 3** bullet is the
  reason this recipe exists: name the concrete WinUI 3 control or composition
  a Windows developer would start from, and what differs from the source
  platform.
- Keep the existing recipe's frontmatter `id`, `created` and `version` if one is
  given; bump `version` minor and update `modified` to today. If starting fresh,
  leave `id`, `created`, `modified`, `author`, `copyright`, `license` empty —
  `cookbook update` fills them.
- Set `status: review` when every section is filled and no `NEEDS REVIEW`
  marker remains; otherwise `status: draft`.
```

`actions/extract.md`:

```markdown
---
description: "Write or complete the recipe for one component from its source files."
params:
  name:
    description: "Component name (kebab-case)."
  recipe_path:
    description: "Repo-relative path the finished recipe is written to."
  type:
    description: "ingredient or recipe."
    default: "ingredient"
  platforms:
    description: "Comma-separated source platforms present in the sources."
---
Write the **{{type}}** recipe for the component `{{name}}`.

Save the result to `{{recipe_path}}` (overwrite if it exists). Source platforms
present: {{platforms}}.

Use the `{{type}}` template under `## reference: templates/` above as the exact
section list and order. Use the guidelines under `## reference: guidelines/` as
the acceptance bar. The sources and any existing recipe follow.
```

`reference-manifest.json`:

```json
{
  "version": 1,
  "source_root": ".",
  "destination": "skills/cookr/cli/cookr/modules/prompt/prompts/extract/references",
  "files": [
    { "src": "cookbook/ingredients/_template.md", "dst": "templates/ingredient.md", "type": "file" },
    { "src": "cookbook/recipes/_template.md",     "dst": "templates/recipe.md",     "type": "file" },
    { "src": "cookbook/guidelines/cookbook/recipe-quality", "dst": "guidelines/recipe-quality", "type": "tree", "include": "*.md" },
    { "src": "cookbook/guidelines/ui/platform-design-languages", "dst": "guidelines/platform-design-languages", "type": "tree", "include": "*.md" }
  ]
}
```

Before committing, confirm the fourth `src` exists: `ls cookbook/guidelines/ui/platform-design-languages`. If it is a single file rather than a directory, change that entry to `"type": "file"` with the file's path and `"dst": "guidelines/platform-design-languages.md"`.

Append to `.gitignore`:

```
skills/cookr/cli/cookr/modules/prompt/prompts/*/references/
```

- [ ] **Step 2: Write the failing test**

```python
"""`cookr prompt extract` assembles module + references + action + sources + existing recipe."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from cookr.cli import main
from cookr.modules.prompt import prompt_cli


@pytest.fixture
def extract_refs(monkeypatch, tmp_path):
    """Stand-in for install.sh's materialisation: copy the manifest's files."""
    repo_root = Path(__file__).resolve().parents[5]
    manifest = json.loads((prompt_cli.PROMPTS_DIR / "extract" / "reference-manifest.json").read_text())
    dest = tmp_path / "references"
    for entry in manifest["files"]:
        src = repo_root / entry["src"]
        dst = dest / entry["dst"]
        if entry["type"] == "file":
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        else:
            for f in src.rglob(entry.get("include", "*")):
                if f.is_file():
                    t = dst / f.relative_to(src)
                    t.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, t)
    monkeypatch.setattr(prompt_cli, "references_dir", lambda: dest)
    return dest


def test_prompt_lists_actions(capsys):
    assert main(["prompt"]) == 0
    assert "extract" in capsys.readouterr().out


def test_extract_includes_sources_and_existing_recipe(mini_repo, extract_refs, capsys):
    assert main(["-p", str(mini_repo), "prompt", "extract", "button"]) == 0
    out = capsys.readouterr().out
    assert "You are a UI component specification writer." in out
    assert "## reference: templates/ingredient.md" in out
    assert "## reference: guidelines/recipe-quality/source-fidelity.md" in out
    assert "## source: web/components/Button.tsx (web)" in out
    assert "## source: apple/UI/Button.swift (apple)" in out
    assert "## existing recipe: recipes/button.md" in out
    assert "Source platforms\npresent: apple, web" in out or "present: apple, web" in out


def test_extract_alias_pulls_alias_sources_too(mini_repo, extract_refs, capsys):
    assert main(["-p", str(mini_repo), "prompt", "extract", "toolbar-button"]) == 0
    out = capsys.readouterr().out
    assert "## source: apple/UI/ToolbarButton.swift (apple)" in out
    assert "recipes/button.md" in out          # alias resolves to the button recipe


def test_extract_missing_component_exits_2(mini_repo, extract_refs, capsys):
    assert main(["-p", str(mini_repo), "prompt", "extract", "nope"]) == 2


def test_extract_json_reports_paths(mini_repo, extract_refs, capsys):
    assert main(["-p", str(mini_repo), "prompt", "extract", "chat-composer", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["recipe_path"] == "recipes/chat-composer.md"
    assert data["sources"] == ["web/components/chat-composer.tsx"]
    assert "prompt" in data


def test_extract_type_recipe_uses_recipe_template(mini_repo, extract_refs, capsys):
    assert main(["-p", str(mini_repo), "prompt", "extract", "stat-card", "--type", "recipe"]) == 0
    out = capsys.readouterr().out
    assert "Write the **recipe** recipe" in out
```

- [ ] **Step 3: Run test to verify it fails**

Run: `python3 -m pytest skills/cookr/cli/tests/unit/test_modules_prompt.py -q`
Expected: FAIL with `ModuleNotFoundError: No module named 'cookr.modules.prompt'`

- [ ] **Step 4: Write the module**

`modules/prompt/__init__.py`:

```python
"""`cookr prompt` — assemble an extraction prompt and print it."""

from .prompt_cli import NAME, HELP, register, run

__all__ = ["NAME", "HELP", "register", "run"]
```

`modules/prompt/prompt_cli.py`:

```python
"""`cookr prompt extract <name>` — the brief for writing one component's recipe.

Assembled, in order: role header + module preamble, the bundled references
(templates and guidelines), the rendered action, then every source file for the
component and the existing recipe if there is one. No LLM is called here.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from cookbook.modules.prompt.render import assemble_prompt

from ...core.inventory import scan
from ...core.recipes import load_corpus
from ..inventory import _require_config

NAME = "prompt"
HELP = "Assemble the extraction prompt for one component and print it."

PROMPTS_DIR = Path(__file__).parent / "prompts"
ACTIONS = ("extract",)


def references_dir() -> Path:
    """Materialised by install.sh from prompts/extract/reference-manifest.json."""
    return PROMPTS_DIR / "extract" / "references"


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("paction", nargs="?", help="Action: extract. Omit to list.")
    parser.add_argument("name", nargs="?", help="Component name (kebab-case).")
    parser.add_argument("--type", choices=("ingredient", "recipe"), default="ingredient",
                        help="Template to write against.")
    parser.add_argument("--json", action="store_true",
                        help="Wrap the prompt with the resolved paths as JSON.")


def build(name: str, ctx, rtype: str):
    """Return (prompt_text, info) for `name`, or raise LookupError."""
    cfg = ctx.config
    slug = cfg.aliases.get(name, name)
    components = [c for c in scan(cfg) if c.name == name]
    if not components:
        raise LookupError(f"no source file in the inventory is named `{name}`")

    recipe_rel = f"{cfg.recipes}/{slug}.md"
    corpus = load_corpus(cfg.recipes_dir)
    existing = corpus.get(slug)
    platforms = ", ".join(sorted({c.platform for c in components}))

    prompt = assemble_prompt(
        module_md_path=PROMPTS_DIR / "extract" / "module.md",
        references_dir=references_dir(),
        action_md_path=PROMPTS_DIR / "extract" / "actions" / "extract.md",
        params={"name": name, "recipe_path": recipe_rel, "type": rtype, "platforms": platforms},
        task=f"Produce `{recipe_rel}` for `{name}`.",
    )
    parts = [prompt.rstrip()]
    for c in components:
        body = (cfg.repo_root / c.path).read_text(encoding="utf-8", errors="replace")
        parts.append(f"## source: {c.path} ({c.platform})\n\n```\n{body.rstrip()}\n```")
    if existing is not None:
        parts.append(
            f"## existing recipe: {recipe_rel}\n\n```markdown\n"
            f"{existing.path.read_text(encoding='utf-8').rstrip()}\n```"
        )
    text = "\n\n".join(parts) + "\n"
    info = {
        "name": name, "slug": slug, "type": rtype, "recipe_path": recipe_rel,
        "sources": [c.path for c in components], "platforms": platforms.split(", "),
        "existing": existing is not None,
    }
    return text, info


def run(args, ctx) -> int:
    if not args.paction:
        ctx.ui.title("cookr prompt — available actions")
        for a in ACTIONS:
            ctx.ui.info(f"  {a}")
        return 0
    if args.paction not in ACTIONS:
        ctx.ui.error(f"cookr prompt: unknown action '{args.paction}'.")
        return 2
    if not _require_config(ctx):
        return 2
    if not args.name:
        ctx.ui.error("cookr prompt extract: a component name is required.")
        return 2
    try:
        text, info = build(args.name, ctx, args.type)
    except LookupError as e:
        ctx.ui.error(f"cookr prompt extract: {e}")
        return 2
    if args.json:
        info["prompt"] = text
        sys.stdout.write(json.dumps(info, indent=2) + "\n")
    else:
        sys.stdout.write(text)
    return 0
```

Note `test_prompt_lists_actions` runs without `-p`: `run` lists actions before requiring config, which the code above does.

- [ ] **Step 5: Run tests to verify they pass**

Run: `python3 -m pytest skills/cookr/cli/tests/unit -q`
Expected: 50 passed

- [ ] **Step 6: Commit**

```bash
git add skills/cookr/cli/cookr/modules/prompt skills/cookr/cli/tests/unit/test_modules_prompt.py .gitignore
git commit -m "feat(cookr): prompt extract command"
```

---

### Task 9: install.sh / uninstall.sh generalisation

**Files:**
- Modify: `install.sh` (variables near line 21–36; step 3b glob at line ~140; step 4 lines ~221–231; step 5 lines ~233–237; step 7 `EXCLUDE_PER_SKILL` line ~295)
- Modify: `uninstall.sh` (shim and package removal, lines ~14–42)
- Create: `skills/cookr/cli/tests/functional/test_install.py`

**Interfaces:**
- Produces: `~/.local/bin/cookr`, `~/.local/bin/_cookr_pkg/cookr/`, `plugins/adh/skills/cookr/` (without `cli/` or `bin/`), and materialised `prompts/extract/references/`.

- [ ] **Step 1: Write the failing functional test**

```python
"""The installed `cookr` shim works end to end."""

from __future__ import annotations

import os
from pathlib import Path

import pytest


def test_shim_runs_and_reports_version(run_cookr):
    r = run_cookr(["--version"])
    assert r.returncode == 0
    assert "cookr" in r.stdout


def test_installed_package_has_references(cookr_bin):
    pkg = Path(cookr_bin).parent / "_cookr_pkg" / "cookr" / "modules" / "prompt" / "prompts" / "extract" / "references"
    assert (pkg / "templates" / "ingredient.md").is_file()
    assert (pkg / "guidelines" / "recipe-quality" / "source-fidelity.md").is_file()


def test_shim_coverage_on_fixture(run_cookr, mini_repo):
    r = run_cookr(["-p", str(mini_repo), "coverage", "--json"])
    assert r.returncode == 0
    assert '"unmatched_recipes"' in r.stdout


def test_plugin_bundle_excludes_cli(cookr_bin):
    repo_root = Path(__file__).resolve().parents[5]
    bundled = repo_root / "plugins" / "adh" / "skills" / "cookr"
    if not bundled.is_dir():
        pytest.skip("plugin not assembled in this checkout")
    assert (bundled / "SKILL.md").is_file()
    assert not (bundled / "cli").exists()
    assert not (bundled / "bin").exists()
```

- [ ] **Step 2: Run to verify it skips (not installed yet)**

Run: `python3 -m pytest skills/cookr/cli/tests/functional/test_install.py -q`
Expected: 4 skipped (`cookr` not on PATH)

- [ ] **Step 3: Edit install.sh**

Replace the two single-skill variables

```bash
MANIFEST="${REPO_ROOT}/skills/cookbook/cli/reference-manifest.json"
PKG_SRC="${REPO_ROOT}/skills/cookbook/cli"
```

with

```bash
MANIFEST="${REPO_ROOT}/skills/cookbook/cli/reference-manifest.json"
# Skills that carry a CLI: each ships as ~/.local/bin/<name> + ~/.local/bin/_<name>_pkg
# and has its cli/ and bin/ kept out of the plugin bundle.
CLI_SKILLS=(cookbook cookr)
```

Step 3b: change the single glob root

```python
glob_root = repo_root / "skills/cookbook/cli/cookbook/modules/prompt/prompts"
```

so that it iterates over both skills. Replace from `glob_root = ...` through the `for manifest_path in sorted(glob_root.glob("*/reference-manifest.json")):` line with:

```python
skills = sys.argv[2].split()
glob_roots = [repo_root / f"skills/{s}/cli/{s}/modules/prompt/prompts" for s in skills]
glob_roots = [g for g in glob_roots if g.is_dir()]
if not glob_roots:
    print("  (no prompt modules)")
    raise SystemExit(0)

for glob_root in glob_roots:
    for refs_dir in sorted(glob_root.glob("*/references")):
        if not refs_dir.is_dir():
            continue
        for child in refs_dir.iterdir():
            if child.name == ".gitkeep":
                continue
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()

manifests = []
for glob_root in glob_roots:
    manifests.extend(sorted(glob_root.glob("*/reference-manifest.json")))

count = 0
for manifest_path in manifests:
```

and change the heredoc invocation from `python3 - "$REPO_ROOT" <<'PY'` to `python3 - "$REPO_ROOT" "${CLI_SKILLS[*]}" <<'PY'`. Keep the loop body that follows unchanged (it already dedents under `for manifest_path`).

Step 4 and 5: replace

```bash
# 4. Install package to ~/.local/bin/_cookbook_pkg
title "Installing package"
rm -rf "${PKG_DIR}"
mkdir -p "${PKG_DIR}"
# Copy only what we want to ship: the cookbook package, references, manifest, README.
cp -R "${PKG_SRC}/cookbook" "${PKG_DIR}/"
cp -R "${PKG_SRC}/references" "${PKG_DIR}/"
cp "${PKG_SRC}/reference-manifest.json" "${PKG_DIR}/"
# Stamp the source path so `cookbook self update` can re-run install.sh from here.
printf '%s\n' "${REPO_ROOT}" > "${PKG_DIR}/.install_source"
ok "package → ${PKG_DIR}"

# 5. Install the shim
title "Installing shim"
cp "${REPO_ROOT}/skills/cookbook/bin/cookbook" "${BIN_DIR}/cookbook"
chmod +x "${BIN_DIR}/cookbook"
ok "shim → ${BIN_DIR}/cookbook"
```

with

```bash
# 4 + 5. Install each CLI skill's package and shim
for skill in "${CLI_SKILLS[@]}"; do
    pkg_src="${REPO_ROOT}/skills/${skill}/cli"
    pkg_dir="${BIN_DIR}/_${skill}_pkg"
    title "Installing ${skill} package"
    rm -rf "${pkg_dir}"
    mkdir -p "${pkg_dir}"
    cp -R "${pkg_src}/${skill}" "${pkg_dir}/"
    if [ -d "${pkg_src}/references" ]; then
        cp -R "${pkg_src}/references" "${pkg_dir}/"
    fi
    if [ -f "${pkg_src}/reference-manifest.json" ]; then
        cp "${pkg_src}/reference-manifest.json" "${pkg_dir}/"
    fi
    # Stamp the source path so `<skill> self update` can re-run install.sh from here.
    printf '%s\n' "${REPO_ROOT}" > "${pkg_dir}/.install_source"
    ok "package → ${pkg_dir}"

    title "Installing ${skill} shim"
    cp "${REPO_ROOT}/skills/${skill}/bin/${skill}" "${BIN_DIR}/${skill}"
    chmod +x "${BIN_DIR}/${skill}"
    ok "shim → ${BIN_DIR}/${skill}"
done
```

`PKG_DIR` is still referenced by the legacy-cleanup section if one exists; search for `PKG_DIR` after the edit and replace any remaining use with `"${BIN_DIR}/_cookbook_pkg"`.

Step 7: replace

```python
EXCLUDE_PER_SKILL = {"cookbook": {"cli", "bin"}}
```

with

```python
CLI_SKILLS = set(sys.argv[3].split())
EXCLUDE_PER_SKILL = {name: {"cli", "bin"} for name in CLI_SKILLS}
```

and change that heredoc's invocation from `python3 - "$SKILLS_SRC" "$PLUGIN_SKILLS_DIR" <<'PY'` to `python3 - "$SKILLS_SRC" "$PLUGIN_SKILLS_DIR" "${CLI_SKILLS[*]}" <<'PY'`.

Update the header comment at the top of `install.sh` to say "Copies each CLI skill's Python package to ~/.local/bin/_<name>_pkg/ and writes a shim at ~/.local/bin/<name>".

- [ ] **Step 4: Edit uninstall.sh**

Replace

```bash
PKG_DIR="${BIN_DIR}/_cookbook_pkg"
```

with

```bash
CLI_SKILLS=(cookbook cookr)
```

and replace the "Removing CLI shim" and "Removing package" blocks with

```bash
for skill in "${CLI_SKILLS[@]}"; do
    title "Removing ${skill} CLI shim"
    if [ -f "${BIN_DIR}/${skill}" ]; then
        rm -f "${BIN_DIR}/${skill}"
        ok "removed ${BIN_DIR}/${skill}"
    else
        skip "${BIN_DIR}/${skill} (not present)"
    fi

    title "Removing ${skill} package"
    if [ -d "${BIN_DIR}/_${skill}_pkg" ]; then
        rm -rf "${BIN_DIR}/_${skill}_pkg"
        ok "removed ${BIN_DIR}/_${skill}_pkg"
    else
        skip "${BIN_DIR}/_${skill}_pkg (not present)"
    fi
done
```

- [ ] **Step 5: Run the installer and both suites**

Run: `./install.sh`
Expected: prints `Installing cookbook package`, `Installing cookr package`, both shims, `materialized 2 prompt-module manifest(s)`, and `+ cookr` under "Assembling plugin".

Run: `python3 -m pytest skills/cookbook/cli/tests/unit skills/cookr/cli/tests -q`
Expected: all pass; the cookr functional tests no longer skip.

Run: `cookbook --version && cookr --version`
Expected: both print.

- [ ] **Step 6: Commit**

```bash
git add install.sh uninstall.sh skills/cookr/cli/tests/functional/test_install.py
git commit -m "build: install every CLI-carrying skill (cookbook, cookr) the same way"
```

---

### Task 10: SKILL.md

**Files:**
- Create: `skills/cookr/SKILL.md`

- [ ] **Step 1: Write it**

```markdown
---
name: cookr
version: "0.1.0"
description: "Inventory, coverage and extraction prompts for component recipes in a repo that carries a .cookr.json. Wraps the `cookr` CLI at ~/.local/bin/cookr. Use when the user asks which components have recipes, what is left to write for a tier, or to write the recipe for a component."
argument-hint: "[--help] [-p <repo-root>] <inventory|coverage|prompt extract <name>> [...]"
allowed-tools: Bash(cookr *), Bash(cookbook *), Bash(command -v cookr)
model: sonnet
---

# cookr v0.1.0

Thin wrapper around the `cookr` CLI at `~/.local/bin/cookr`. All work goes
through the CLI — never duplicate its logic in this skill. Recipe frontmatter,
indexes, validation and lint belong to the `cookbook` CLI; call it, never
re-implement it.

## Startup

```bash
command -v cookr
```

If missing, tell the user:

> The `cookr` CLI is not installed. Run `./install.sh` from the agenticcookbook repo, then re-invoke me.

…and stop.

## Routing

| Request | Command |
|---|---|
| what components exist / what tiers there are | `cookr inventory [--tier <tier>]` |
| what is left to write | `cookr coverage [--tier <tier>]` |
| write the recipe for X | `cookr prompt extract X` → dispatch (below) |
| is the phase done | `cookr coverage --tier <tier> --require complete` then `cookbook validate -p recipes` |
| no args / `--help` | `cookr --help`, present the module table verbatim |

Forward `-p <repo-root>` when the user supplies one; otherwise run from cwd and let the CLI find `.cookr.json`.

## Extraction workflow

1. `cookr coverage --tier <tier> --json` — collect every row whose `state` is `missing` or `partial`.
2. For each name, run `cookr prompt extract <name>` (add `--type recipe` for a composite) and dispatch the printed prompt verbatim to a subagent pinned to `claude-sonnet-4-6`. The subagent writes `recipes/<slug>.md`. Run up to 8 subagents at a time.
3. `cookbook update -p recipes --author "<user>"` — fills frontmatter.
4. `cookbook validate -p recipes` and `cookr coverage --tier <tier>`.
5. Any row still `partial`: rerun step 2 for it. The prompt includes the existing recipe, so the subagent completes rather than restarts.
6. `cookbook lint -p recipes --since main` before committing.

## Interpreting coverage

The `problems` column names exactly what keeps a recipe at `partial`:
a `status` below `review`, a `NEEDS REVIEW` marker, a missing or empty required
section, or an unfilled `WinUI 3` bullet. Quote it to the subagent; do not
re-derive it.

A recipe listed under "recipes with no inventory match" is not an error: it is
a vocabulary or composite recipe with no single source file. Check `.cookr.json`
`aliases` only if the name looks like a typo of a component.

## Behavior notes

- Never edit files in `~/.local/bin/_cookr_pkg/`. Edit `skills/cookr/cli/` in agenticcookbook and re-run `./install.sh`.
- Never `pip install` from this skill.
- `.cookr.json` lives at the target repo's root. Add roots, ignores and aliases there; never in a recipe.
```

- [ ] **Step 2: Verify the plugin picks it up**

Run: `./install.sh >/dev/null && ls plugins/adh/skills/cookr`
Expected: `SKILL.md` only.

- [ ] **Step 3: Commit**

```bash
git add skills/cookr/SKILL.md
git commit -m "feat(cookr): SKILL.md wrapper"
```

---

### Task 11: Spec/plan consistency and README mention

**Files:**
- Modify: `docs/superpowers/specs/2026-09-21-cookr-design.md` (completeness rule 3)
- Modify: `README.md` (one line under the skills list, if the README lists skills)

- [ ] **Step 1: Align the spec with the implementation**

In the spec's Coverage section, completeness rule 3 says "every `##` section the template defines for that `type`". The implementation checks the fixed list in `completeness.REQUIRED_SECTIONS` (ten ingredient sections, nine recipe sections) because the ingredient template also carries sections such as Deep Linking and Feature Flags that most components legitimately leave out. Replace rule 3 with:

```
3. Every section in `completeness.REQUIRED_SECTIONS[type]` is present and has
   at least one non-blank line of body before the next heading. Ingredient:
   Overview, Behavioral Requirements, Appearance, States, Accessibility,
   Conformance Test Vectors, Edge Cases, Configuration, Platform Notes,
   Design Decisions. Recipe: Overview, Ingredients, Integration Requirements,
   Layout, Shared State, Integration Test Vectors, Edge Cases, Platform Notes,
   Design Decisions.
```

- [ ] **Step 2: README**

Run: `grep -n "cookbook" README.md | head`. If the README has a skills or CLI list, add one line: `- cookr — inventory and recipe coverage for component repos (see skills/cookr/SKILL.md)`. If it has none, skip this step and say so in the commit body.

- [ ] **Step 3: Commit**

```bash
git add docs/superpowers/specs/2026-09-21-cookr-design.md README.md
git commit -m "docs: align cookr spec with REQUIRED_SECTIONS; mention cookr in README"
```

---

### Task 12: `.cookr.json` for agenticdevelopertoolkit

Runs in `~/Development/projects/fishlampdesign/agenticdevelopertoolkit` on its current branch. Do not create a branch or PR.

**Files:**
- Create: `.cookr.json`
- Delete: `cookbook/` (contains only `index.md`, `description.md`, `recipes/.gitkeep`, `reference/.gitkeep`)

- [ ] **Step 1: Write `.cookr.json`**

```json
{
  "recipes": "recipes",
  "roots": [
    {"path": "packages/web/packages/ui/src/components",  "tier": "ui-primitives", "platform": "web"},
    {"path": "packages/web/packages/ui/src/blocks",      "tier": "ui-blocks",     "platform": "web"},
    {"path": "packages/web/packages/controls/src",       "tier": "ui-blocks",     "platform": "web"},
    {"path": "packages/web/packages/chat/src/components","tier": "chat",          "platform": "web"},
    {"path": "packages/web/packages/chat/src/modes",     "tier": "chat",          "platform": "web"},
    {"path": "packages/web/packages/popover/src",        "tier": "chrome",        "platform": "web"},
    {"path": "packages/web/packages/chrome/src",         "tier": "chrome",        "platform": "web"},
    {"path": "packages/web/packages/viewport/src",       "tier": "chrome",        "platform": "web"},
    {"path": "packages/web/packages/markdown/src/components", "tier": "markdown", "platform": "web"},
    {"path": "packages/apple/AgenticDeveloperToolkit/SourcesUI", "tier": "apple-ui", "platform": "apple"},
    {"path": "packages/web/packages/landing/src",        "tier": "page-kits",     "platform": "web"},
    {"path": "packages/web/packages/search/src/components", "tier": "page-kits",  "platform": "web"},
    {"path": "packages/web/packages/registry-profile/src", "tier": "page-kits",   "platform": "web"}
  ],
  "ignore": [
    "**/__tests__/**",
    "**/*.test.ts",
    "**/*.test.tsx",
    "**/index.ts",
    "**/types.ts",
    "**/*-types.ts",
    "**/*-log.ts",
    "**/css/**",
    "**/styles/**",
    "**/internal/**",
    "**/Resources/**",
    "packages/web/packages/landing/src/client.ts",
    "packages/web/packages/controls/src/**/*.css"
  ],
  "aliases": {}
}
```

Before writing, confirm each `path` exists (`ls` each one); drop any that does not and note it in the commit body. After writing, run `cookr inventory --json | python3 -c "import json,sys; rows=json.load(sys.stdin); print(len(rows))"` and skim `cookr inventory` for files that are plainly not components (helpers, type modules); add them to `ignore` rather than leaving them to show as `missing`. Then compare `ls recipes` against the `missing` rows of `cookr coverage`: where a recipe slug is clearly the same component under a different name (for example a `Button.tsx` and a `button-pressable.md`), add an `aliases` entry mapping the component name to the recipe slug. Add only pairs you can see are the same component; leave anything doubtful `missing`.

- [ ] **Step 2: Delete the empty scaffold**

Run: `find cookbook -type f` and confirm the only files are `index.md`, `description.md` and two `.gitkeep`s. Then `git rm -r cookbook`.

- [ ] **Step 3: Verify**

Run: `cookr coverage`
Expected: a table covering every tier, tallies per tier, and a "recipes with no inventory match" list. Every one of the 43 recipes should either match a component or appear in that list; if one you expect to match appears in the list, add an alias.

Run: `cookbook validate -p recipes`
Expected: exit 0. If a recipe fails a Phase A check, fix that file (these are pre-existing recipes; the usual cause is a missing frontmatter field, which `cookbook update -p recipes --author "Mike Fullerton"` fills).

Run: `python3 tools/check_doc_links.py && python3 tools/check_recipe_scope.py`
Expected: both exit 0 (nothing under `recipes/` changed).

- [ ] **Step 4: Commit and push**

```bash
git add .cookr.json
git commit -m "chore: add .cookr.json and drop the empty cookbook/ scaffold"
git push
```

(`git rm` already staged the deletion.)

---

### Task 13: `.cookr.json` for agentictoolkit

Runs in `~/Development/projects/fishlampdesign/agentictoolkit` on its current branch. Do not create a branch or PR.

**Files:**
- Create: `.cookr.json`

- [ ] **Step 1: Write `.cookr.json`**

```json
{
  "recipes": "recipes",
  "roots": [
    {"path": "packages/web/packages/adh-ui/src/components", "tier": "adh-ui", "platform": "web"},
    {"path": "packages/web/packages/adh-ui/src/blocks",     "tier": "adh-ui", "platform": "web"},
    {"path": "packages/apple/AgenticToolkit/CoreUI",        "tier": "apple-ui", "platform": "apple"},
    {"path": "packages/apple/AgenticToolkit/macOS",         "tier": "apple-ui", "platform": "apple"},
    {"path": "packages/apple/AgenticToolkit/PermissionsUI", "tier": "apple-ui", "platform": "apple"}
  ],
  "ignore": [
    "**/__tests__/**",
    "**/*.test.ts",
    "**/*.test.tsx",
    "**/index.ts",
    "**/Tests/**",
    "**/Resources/**",
    "**/*.xcodeproj/**"
  ],
  "aliases": {}
}
```

Before writing, `ls` each apple path and look one level down: if a framework keeps its sources under a `Sources/` subdirectory, point the root at that subdirectory. Drop any path that does not exist and note it in the commit body.

- [ ] **Step 2: Verify**

Run: `cookr coverage`
Expected: `delete-entity-section` and `send-invitation-modal` match `adh-ui` blocks; the other six recipes (crud-record-form, crud-table, focused-topic-detail, hierarchical-category-browser, site-menu, site-wordmark) appear under "recipes with no inventory match" unless a same-named source exists in the apple roots.

Run: `cookbook validate -p recipes`
Expected: exit 0, or fix as in Task 12 step 3.

- [ ] **Step 3: Commit and push**

```bash
git add .cookr.json
git commit -m "chore: add .cookr.json for cookr coverage"
git push
```

---

### Task 14: Phase 0 exit check

- [ ] **Step 1: Both repos report**

Run from each target repo root:

```bash
cookr coverage --json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['tally'])"
cookbook validate -p recipes
```

Expected: a tally dict naming every tier in that repo's `.cookr.json`, and validate exit 0.

- [ ] **Step 2: Full agenticcookbook suite**

Run from the agenticcookbook worktree: `python3 -m pytest skills -q`
Expected: all pass, none of cookr's functional tests skipped.

- [ ] **Step 3: Push the cookr branch**

```bash
git push origin cookr
```
