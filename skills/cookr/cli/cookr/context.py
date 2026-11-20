"""Per-invocation context handed to every module's run().

The repo root is `config.repo_root`, derived in one place (core/repoconfig); the
context carries no second copy of it. `cookbook_root` is the cookbook directory
the maintenance modules (update, validate, lint) work on: any cookbook, with or
without a `cookbook.json` (core/roots.py says which directories qualify).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .core import refs, roots
from .core.repoconfig import Config
from .core.ui import UI


@dataclass
class CookrContext:
    config: Optional[Config]
    ui: UI
    config_error: Optional[str] = None  # why a config that exists gave none
    cookbook_root: Optional[Path] = None
    references_dir: Path = field(default_factory=lambda: refs.references_dir())
    cwd: Path = field(default_factory=Path.cwd)

    def artifact(self, path: Optional[Path]) -> Optional[Path]:
        """An artifact path from the command line, found the same way from any
        working directory (core/roots.artifact_path); None stays None."""
        if path is None:
            return None
        repo = self.config.repo_root if self.config is not None else None
        return roots.artifact_path(path, self.cookbook_root, repo, self.cwd)
