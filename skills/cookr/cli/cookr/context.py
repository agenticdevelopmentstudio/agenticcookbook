"""Per-invocation context handed to every module's run().

The repo root is `config.repo_root`, derived in one place (load_config); the
context carries no second copy of it. `cookbook_root` is the cookbook directory
the maintenance modules (update, validate, lint) work on: any cookbook, with or
without a `cookbook.json` (core/roots.py says which directories qualify).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .core import refs
from .core.config import Config
from .core.ui import UI


@dataclass
class CookrContext:
    config: Optional[Config]
    ui: UI
    legacy: Optional[Path] = None  # a `.cookr.json` found for `cookr organize` to convert
    config_error: Optional[str] = None  # why a cookbook.json that exists gave no config
    cookbook_root: Optional[Path] = None
    references_dir: Path = field(default_factory=lambda: refs.references_dir())
    cwd: Path = field(default_factory=Path.cwd)
