"""Shared by the repo's install/uninstall scripts (./install, ./uninstall and
skills/<name>/setup/{install,uninstall}).

Standard library only: these scripts run before any Python deps are installed.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
SKILLS_SRC = REPO_ROOT / "skills"
PLUGIN_DIR = REPO_ROOT / "plugins" / "adh"
PLUGIN_SKILLS_DIR = PLUGIN_DIR / "skills"

BIN_DIR = Path.home() / ".local" / "bin"
# What ./install actually installed, so ./uninstall also removes a CLI skill
# that has since left the layout.
CLI_RECORD = BIN_DIR / ".adh-cli-skills"

CLAUDE_DIR = Path.home() / ".claude"
KNOWN_MARKETPLACES = CLAUDE_DIR / "plugins" / "known_marketplaces.json"
CLAUDE_SETTINGS = CLAUDE_DIR / "settings.json"
LEGACY_SKILL_DIR = CLAUDE_DIR / "skills" / "cookbook"
MARKETPLACE_NAME = "agenticcookbook"
PLUGIN_NAME = "adh"
PLUGIN_ID = f"{PLUGIN_NAME}@{MARKETPLACE_NAME}"


def cli_skills() -> list[str]:
    """Skills that carry a CLI: skills/<name>/bin/<name> plus a
    skills/<name>/cli/<name>/ package. Each ships as ~/.local/bin/<name> and
    ~/.local/bin/_<name>_pkg/, and its cli/, bin/ and setup/ stay out of the
    plugin bundle."""
    return sorted(
        d.name
        for d in SKILLS_SRC.iterdir()
        if d.is_dir() and (d / "bin" / d.name).is_file() and (d / "cli" / d.name).is_dir()
    )


def color(code: str, text: str, stream=sys.stdout) -> None:
    print(f"\033[1;{code}m{text}\033[0m", file=stream, flush=True)


def title(text: str) -> None:
    print()
    color("36", f"› {text}")


def ok(text: str) -> None:
    color("32", f"✓ {text}")


def warn(text: str) -> None:
    color("33", f"! {text}")


def err(text: str) -> None:
    color("31", f"✗ {text}", stream=sys.stderr)


def skip(text: str) -> None:
    color("90", f"· {text}")


def load_json(path: Path) -> dict | None:
    """The JSON object at `path`, or None when it is missing or empty.
    Raises json.JSONDecodeError when it is not valid JSON."""
    if not path.exists() or path.stat().st_size == 0:
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    """Write `data` to `path` atomically, so a crash never leaves it half-written."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def remove(path: Path) -> None:
    """Delete a file, symlink or directory tree, reporting either way."""
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    elif path.exists() or path.is_symlink():
        path.unlink()
    else:
        skip(f"{path} (not present)")
        return
    ok(f"removed {path}")
