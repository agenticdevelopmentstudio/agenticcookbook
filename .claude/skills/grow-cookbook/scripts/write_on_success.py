#!/usr/bin/env python3
"""Write a command's stdout to a file only when the command succeeds.

    python3 write_on_success.py [--mkdir] <out-file> -- [NAME=VALUE]... <command> [arg]...

`<out-file>` must be absolute (a relative one exits 2: G44, 1.4.24).
Its folder must exist (G174, 1.4.37: a missing one exits 2 and creates
nothing, so a mistyped path leaves no empty folders) unless `--mkdir` is
given, which creates it; a folder that cannot hold a temporary file exits 2
with one line. Runs the command with its stdout going to a
temporary file beside `<out-file>`, and moves that into place only on exit 0.
On any other exit what the command printed is shown, not kept (cookr prints
its errors on stdout), and the temporary file is removed, so a failed run
never leaves an empty or partial `<out-file>` (a previous one stays as it
was). A success that prints `<out-file>`'s own bytes leaves it untouched, its
modification time too, so an idempotent re-run changes nothing; the command's stderr passes through and its exit code is this script's. Leading
`NAME=VALUE` words set the command's environment, as they would in a shell, so
a whole `PYTHONPATH=... <python> -P -m cookr ...` line fits after `--`.

G231 (1.4.40): a command that edits `<out-file>` itself (an in-place editor
that prints nothing; `sed -i`) is refused: exit 2, nothing written over it,
its edit stands, one line says so. Run such an edit on its own, never under
this wrapper.

G215 (1.4.39): a write into an area folder (the nearest folder above
`<out-file>`, below `areas/`, that holds `area-plan.md`) with no
`first-check.txt` beside that plan warns on stderr, once, and still writes:
a re-run takes its first check into A/first-check.txt before step 1.1
rewrites the saved reports.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

_ASSIGNMENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*=")


def _stat(path: Path) -> tuple | None:
    """G231 (1.4.40): what an in-place edit of `path` changes: (inode, size, mtime); None when it is not there."""
    try:
        st = path.stat()
    except OSError:
        return None
    return (st.st_ino, st.st_size, st.st_mtime_ns)


def first_check_warning(out: Path) -> None:
    """G215 (1.4.39): warn when `out` is inside an area with a plan and no first-check.txt."""
    if out.name == "first-check.txt" or out.name.startswith("first-check-before-"):
        return      # gapfix13 (G267): writing the first check itself never warns that it is missing
    for folder in out.parents:
        if folder.name == "areas" or folder == folder.parent:
            return
        if (folder / "area-plan.md").is_file():
            if not (folder / "first-check.txt").is_file():
                print(f"write_on_success.py: {folder} has a plan and no first-check.txt: take the re-run's first "
                      "check (stage-1.md re-run checklist, item 3) into it before step 1.1 rewrites the saved "
                      "reports", file=sys.stderr)
            return


def main(argv: list[str]) -> int:
    mkdir = bool(argv) and argv[0] == "--mkdir"
    argv = argv[1:] if mkdir else argv
    if len(argv) < 3 or argv[1] != "--":
        print("usage: write_on_success.py [--mkdir] <out-file> -- [NAME=VALUE]... <command> [arg]...",
              file=sys.stderr)
        return 2
    out, command = Path(argv[0]), argv[2:]
    if not out.is_absolute():   # G44: never a file wherever the caller stands
        print(f"write_on_success.py: <out-file> must be an absolute path, not {argv[0]!r}", file=sys.stderr)
        return 2
    first_check_warning(out)
    env = dict(os.environ)
    while command and _ASSIGNMENT.match(command[0]):
        name, value = command.pop(0).split("=", 1)
        env[name] = value
    if not command:
        print("write_on_success.py: no command after the assignments", file=sys.stderr)
        return 2
    if not command[0].strip():      # gapfix14 (G299, 1.4.43): an unset `$COOKR_PY` is no command
        print("write_on_success.py: the command is empty (an unset variable such as $COOKR_PY?): "
              "nothing run, nothing written", file=sys.stderr)
        return 2
    if mkdir:
        try:
            out.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"write_on_success.py: cannot create {out.parent}: {e.strerror or e}", file=sys.stderr)
            return 2
    elif not out.parent.is_dir():      # G174: never junk folders from a malformed path
        print(f"write_on_success.py: the folder {out.parent} does not exist: create it, or pass --mkdir",
              file=sys.stderr)
        return 2
    try:
        fd, tmp = tempfile.mkstemp(prefix=f".{out.name}.", dir=out.parent)
    except OSError as e:
        print(f"write_on_success.py: cannot write a temporary file in {out.parent}: {e.strerror or e}",
              file=sys.stderr)
        return 2
    before = _stat(out)
    try:
        with os.fdopen(fd, "wb") as stdout:
            try:
                code = subprocess.run(command, stdout=stdout, env=env).returncode
            except OSError as e:
                print(f"write_on_success.py: cannot run {command[0]}: {e.strerror}", file=sys.stderr)
                return 127
        if _stat(out) != before:      # G231 (1.4.40): an in-place editor wrote `out` itself
            print(f"write_on_success.py: the command edited {out} in place (its size, modification time or file "
                  "changed while it ran): nothing was written over it; its edit stands. A command that edits a file "
                  "is run on its own, never under this wrapper (it writes stdout to <out-file>)", file=sys.stderr)
            return 2
        if code == 0 and out.is_file() and out.read_bytes() == Path(tmp).read_bytes():
            pass  # the same bytes: leave the file as it is (its mtime too)
        elif code == 0:
            umask = os.umask(0)
            os.umask(umask)
            os.chmod(tmp, 0o666 & ~umask)
            os.replace(tmp, out)
        else:
            sys.stdout.buffer.write(Path(tmp).read_bytes())
            sys.stdout.flush()
        return code
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))      # run with -I too
    from repo_path import run_main      # gapfix13 (G263, G271)
    run_main(main, sys.argv[1:])
