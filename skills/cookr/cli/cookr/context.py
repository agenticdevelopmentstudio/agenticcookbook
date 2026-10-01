"""Per-invocation context handed to every module's run().

The repo root is `config.repo_root`, derived in one place (load_config); the
context carries no second copy of it.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from cookbook.core.ui import UI

from .core.config import Config


@dataclass
class CookrContext:
    config: Optional[Config]
    ui: UI
    legacy: Optional[Path] = None  # a `.cookr.json` found for `cookr organize` to convert
