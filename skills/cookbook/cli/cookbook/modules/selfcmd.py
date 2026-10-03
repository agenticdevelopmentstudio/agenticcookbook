"""`cookbook self update` — re-run ./install from the source location stamped at install time.

`./install` writes the absolute repo path into `${PKG_DIR}/.install_source`. The
update action reads that, validates the path still contains an executable
`install`, and re-runs it inline (forwarding output). If the stamp is missing
or the path has been moved, we surface a clear error rather than guessing.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

NAME = "self"
HELP = "Self-management: `cookbook self update` re-runs ./install from the source path stamped at install time."


def register(parser: argparse.ArgumentParser) -> None:
    sub = parser.add_subparsers(dest="self_action", metavar="<action>", required=False)
    sub.add_parser("update", help="Re-run ./install from the recorded source path.")


def _pkg_dir() -> Path:
    return Path(__file__).resolve().parents[2]


def _read_install_source(ui) -> Path | None:
    stamp = _pkg_dir() / ".install_source"
    if not stamp.is_file():
        ui.error(
            f"No install-source stamp at {stamp}. The CLI was likely installed by an "
            "older `./install`; re-run it from the agenticcookbook repo to write the stamp."
        )
        return None
    source = Path(stamp.read_text(encoding="utf-8").strip())
    if not source.is_dir() or not (source / "install").is_file():
        ui.error(
            f"Stamped install source `{source}` is missing or does not contain `./install`. "
            "Re-run ./install from your current copy of the agenticcookbook repo."
        )
        return None
    return source


def _do_update(ctx) -> int:
    source = _read_install_source(ctx.ui)
    if source is None:
        return 1

    ctx.ui.section(f"cookbook self update · {source}")
    ctx.ui.info("Re-running ./install from the recorded source path.")
    proc = subprocess.run(
        [sys.executable, str(source / "install")],
        cwd=source,
        stdin=sys.stdin,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
    return proc.returncode


def run(args, ctx) -> int:
    ctx.ui.title("cookbook self")
    action = getattr(args, "self_action", None)
    if action == "update":
        return _do_update(ctx)
    ctx.ui.info("Available actions: `update`.")
    ctx.ui.info("Run `cookbook self update` to refresh the installed CLI from the recorded source path.")
    return 0 if action is None else 2
