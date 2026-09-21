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
