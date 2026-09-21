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
