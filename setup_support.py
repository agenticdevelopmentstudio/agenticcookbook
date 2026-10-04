"""Shared by the repo's install/uninstall scripts (./install, ./uninstall and
skills/<name>/setup/{install,uninstall}).

Standard library only: these scripts run before any Python deps are installed.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
SKILLS_SRC = REPO_ROOT / "skills"

BIN_DIR = Path.home() / ".local" / "bin"
# What ./install actually installed, so ./uninstall also removes a CLI skill
# that has since left the layout.
CLI_RECORD = BIN_DIR / ".adh-cli-skills"

CLAUDE_DIR = Path.home() / ".claude"
KNOWN_MARKETPLACES = CLAUDE_DIR / "plugins" / "known_marketplaces.json"
PLUGIN_CACHE = CLAUDE_DIR / "plugins" / "cache"
CLAUDE_SETTINGS = CLAUDE_DIR / "settings.json"

# What earlier layouts installed and this one no longer ships: the adh plugin
# (registered from this repo as the `agenticcookbook` directory marketplace),
# its generated skills dir, and the cookbook skill's even older global location.
# retire() removes them, so an install over an old one leaves nothing stale.
RETIRED_MARKETPLACE = "agenticcookbook"
RETIRED_PLUGIN_ID = f"adh@{RETIRED_MARKETPLACE}"
RETIRED_PATHS = (REPO_ROOT / "plugins", CLAUDE_DIR / "skills" / "cookbook")


def cli_skills() -> list[str]:
    """Skills that carry a CLI: skills/<name>/bin/<name> plus a
    skills/<name>/cli/<name>/ package. Each ships as ~/.local/bin/<name> and
    ~/.local/bin/_<name>_pkg/."""
    return sorted(
        d.name
        for d in SKILLS_SRC.iterdir()
        if d.is_dir() and (d / "bin" / d.name).is_file() and (d / "cli" / d.name).is_dir()
    )


def standalone_skills() -> list[str]:
    """Skills that install themselves globally with skills/<name>/setup/install
    (and reverse it with setup/uninstall)."""
    return sorted(
        d.name for d in SKILLS_SRC.iterdir() if d.is_dir() and (d / "setup" / "install").is_file()
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


def recorded_cli_skills() -> list[str]:
    """The CLI skills the last ./install recorded installing."""
    return CLI_RECORD.read_text(encoding="utf-8").split() if CLI_RECORD.is_file() else []


def remove_cli(skill: str) -> None:
    remove(BIN_DIR / skill)
    remove(BIN_DIR / f"_{skill}_pkg")


def _load_or_none(path: Path) -> dict | None:
    try:
        return load_json(path)
    except json.JSONDecodeError as e:
        warn(f"{path} is not valid JSON ({e}); leaving it unchanged.")
        return None


def _claude_plugin(*args: str) -> None:
    """Run `claude plugin <args>`, Claude Code's own bookkeeping (it also clears
    installed_plugins.json and the plugin cache). Best effort: the JSON edits in
    retire() cover a machine without the `claude` CLI."""
    claude = shutil.which("claude")
    if claude is None:
        return
    proc = subprocess.run([claude, "plugin", *args], capture_output=True, text=True)
    if proc.returncode == 0:
        ok(f"claude plugin {' '.join(args)}")


def retire() -> None:
    """Remove what earlier layouts installed (see RETIRED_*). Idempotent."""
    known = _load_or_none(KNOWN_MARKETPLACES)
    if known is not None and RETIRED_MARKETPLACE in known:
        _claude_plugin("uninstall", RETIRED_PLUGIN_ID)
        _claude_plugin("marketplace", "remove", RETIRED_MARKETPLACE)
    known = _load_or_none(KNOWN_MARKETPLACES)
    if known is not None and RETIRED_MARKETPLACE in known:
        del known[RETIRED_MARKETPLACE]
        write_json(KNOWN_MARKETPLACES, known)
        ok(f"known_marketplaces.json: removed {RETIRED_MARKETPLACE}")

    settings = _load_or_none(CLAUDE_SETTINGS)
    if settings is not None:
        changed = False
        for key, entry in (("extraKnownMarketplaces", RETIRED_MARKETPLACE),
                           ("enabledPlugins", RETIRED_PLUGIN_ID)):
            block = settings.get(key)
            if isinstance(block, dict) and entry in block:
                del block[entry]
                if not block:
                    del settings[key]
                changed = True
                ok(f"settings.json: removed {key}.{entry}")
        if changed:
            write_json(CLAUDE_SETTINGS, settings)

    for path in (*RETIRED_PATHS, PLUGIN_CACHE / RETIRED_MARKETPLACE):
        if path.exists():
            remove(path)
