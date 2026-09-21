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
