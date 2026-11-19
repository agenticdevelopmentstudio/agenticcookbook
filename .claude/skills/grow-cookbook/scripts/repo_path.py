#!/usr/bin/env python3
"""How every grow-cookbook script that reads the cookbook finds its repo (G76, 1.4.25).

`--repo R` when given, which must hold `cookbook/guidelines/`; without it,
the nearest folder at or above the current directory that holds
`cookbook/guidelines/`. None found exits 2, naming the script and asking for
--repo: a script run from the workspace (outside the repo) is never given a
silent ".". Stdlib only.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


def cookbook_repo(given: str | os.PathLike | None, script: str) -> Path:
    """The cookbook repo root, resolved; SystemExit (message) when there is none."""
    if given is not None:
        repo = Path(os.path.expanduser(given)).resolve()
        if not (repo / "cookbook" / "guidelines").is_dir():
            raise SystemExit(f"{script}: --repo {given} holds no cookbook/guidelines/")
        return repo
    here = Path.cwd().resolve()
    for folder in (here, *here.parents):
        if (folder / "cookbook" / "guidelines").is_dir():
            return folder
    raise SystemExit(f"{script}: no cookbook/guidelines/ at or above {here}; pass --repo <the cookbook repo>"
                     + one_word_hint())


def one_word_hint() -> str:
    """G240 (L18, 1.4.40): a hint when the script got one argument that holds ` --`: the flags came from one
    shell variable, which zsh does not split."""
    args = sys.argv[1:]
    if (len(args) == 1 and " --" in args[0]) or any(re.match(r"--?[A-Za-z][\w-]*\s", a) for a in args):
        return ("; if your flags came from one shell variable, zsh passes them as one word: write each flag out")
    return ""


def skill_version() -> str:
    """gapfix13 (G269, 1.4.42): this skill's version, from SKILL.md's `grow-cookbook vX.Y.Z` line ("" if none)."""
    try:
        m = re.search(r"^grow-cookbook v(\d+\.\d+\.\d+)\s*$", (Path(__file__).resolve().parent.parent /
                                                                "SKILL.md").read_text(encoding="utf-8"), re.M)
    except OSError:
        return ""
    return m.group(1) if m else ""


def python_hint(err: str, python: str) -> str:
    """gapfix13 (G269, 1.4.42): the hint for an error a python that cannot run
    cookr prints (too old for `-P`, or missing a module); "" for any other."""
    if "Unknown option: -P" in err or "No module named" in err or "unknown option -P" in err.lower():
        return (f" (hint: {python} cannot run cookr: every grow-cookbook script and cookr run under $COOKR_PY, the "
                "Python 3.11+ that check_cookr_python.py accepts, e.g. ~/.cache/grow-cookbook/cookr-venv/bin/python;"
                " SKILL.md, COOKR_PY)")
    return ""


def run_main(main, argv: list[str] | None = None):
    """gapfix13 (1.4.42): every script's `__main__`. G263: an argparse exit 2
    whose arguments hold a flag and its value in one word (a zsh variable
    holding several flags is passed whole) prints the hint naming the cause.
    G271: a closed stdout (`| head`) exits 0 without a traceback. G269: a
    missing module exits 2 naming the python to use."""
    try:
        try:
            code = main() if argv is None else main(argv)
        except ModuleNotFoundError as e:
            print(f"{Path(sys.argv[0]).name}: {e}" + python_hint(f"No module named {e.name}", sys.executable),
                  file=sys.stderr)
            code = 2
        except SystemExit as e:
            if e.code == 2 and one_word_hint():
                print("hint: one argument holds spaces and a flag" + one_word_hint(), file=sys.stderr)
            code = e.code
        sys.stdout.flush()
    except BrokenPipeError:
        try:
            os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        except OSError:
            pass
        code = 0
    raise SystemExit(code)


class PathHelpFormatter(argparse.HelpFormatter):
    """gapfix14 (G287, 1.4.43): help text wrapped at spaces only, so a path such as
    reference/building--platform-windows.txt#10 is never split at its hyphens."""

    def _split_lines(self, text, width):
        import textwrap
        return textwrap.wrap(self._whitespace_matcher.sub(" ", text).strip(), width, break_on_hyphens=False)


def add_area(ap: argparse.ArgumentParser) -> None:
    """G169 (1.4.37): `--area AREA`, and the positional, deprecated, kept so
    older command lines still run; area_arg reads either."""
    ap.add_argument("area", nargs="?", help="deprecated: give --area AREA")
    ap.add_argument("--area", dest="area_opt", metavar="AREA",
                    help="the area, its path below cookbook/guidelines/ (G139, G169)")


def area_arg(ap: argparse.ArgumentParser, a) -> str:
    """G139 (1.4.36): the area from the positional or `--area`, one of them."""
    if a.area and a.area_opt and a.area != a.area_opt:
        ap.error(f"two areas: {a.area} and --area {a.area_opt}")
    if not (a.area or a.area_opt):
        ap.error("name the area: <area> or --area <area>")
    return a.area or a.area_opt


def check_area(script: str, workspace: str | os.PathLike | None, area: str | None,
               repo: str | os.PathLike | None = None) -> str | None:
    """G198 (1.4.39): why `--workspace`/`--area` name no grow-cookbook state,
    or None. A workspace with no `areas/` folder is wrong; an area is known
    when the workspace has a folder for it (`areas/<area>`) or, with `repo`,
    the cookbook has `cookbook/guidelines/<area>`. A one-string argument list
    (`--area "x --workspace y"`) reads as one area and is unknown too."""
    if workspace is not None:
        ws = Path(os.path.expanduser(workspace))
        if not (ws / "areas").is_dir():
            return (f"{script}: --workspace {workspace} holds no areas/ folder: pass the grow-cookbook workspace "
                    "(the folder holding areas/ and worklist.json)")
    if area is None:
        return None
    bad = area.startswith("/") or ".." in area.split("/") or any(c.isspace() for c in area)
    known = not bad and ((workspace is not None and (Path(os.path.expanduser(workspace)) / "areas" / area).is_dir())
                         or (repo is not None and (Path(os.path.expanduser(repo)) / "cookbook" / "guidelines"
                                                   / area).is_dir()))
    if known:
        return None
    return (f"{script}: unknown area {area!r}: no areas/{area} in the workspace"
            + (f" and no cookbook/guidelines/{area} in the repo" if repo is not None else "")
            + "; check --area (each flag is its own word, never one quoted string)")
