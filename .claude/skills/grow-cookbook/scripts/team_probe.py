#!/usr/bin/env python3
"""Whether a myteams team can run here, checked without starting a run.

    python3 team_probe.py <team> [--myteams PATH] [--home DIR] [--package NAME]

`myteams <team> … --help` is no safe probe: myteams routes `--help` into
dispatch, so a broken install dies in a traceback and a working one may start a
run with `--help` as its prompt. This never runs myteams. It checks:

1. the `myteams` front door is on PATH (or --myteams);
2. its interpreter, read from the generated `'''exec' <python>` line, exists;
3. the team is installed: <home>/<team>/install (home: ~/.myagenticteams);
4. in that interpreter, every distribution the `myteams` package's own
   distribution requires (extras aside) is installed, recursively, and
   `myteams.front_door` imports. Importing starts nothing.

Prints JSON {"ok": bool, "why": str, "python": str|None, "missing": [names]}.
Exit 0 either way: a team that cannot run is a status, not an error. /grow-cookbook
uses the research team when `ok`, else its own research prompt.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

_EXEC = re.compile(r"^'''exec' (\S+)", re.M)

# Runs inside the team's interpreter: the requirement closure of the
# distribution that provides PACKAGE, and whether its front door imports.
_CHECK = r"""
import importlib, importlib.metadata as md, json, re, sys
package, module = sys.argv[1], sys.argv[2]


def applies(marker):
    # A requirement's environment marker, here; an extra never applies.
    if "extra" in marker:
        return False
    try:
        from packaging.markers import Marker
        return Marker(marker).evaluate()
    except Exception:  # noqa: BLE001  no packaging: judge the common markers
        import os, platform
        env = {"sys_platform": sys.platform, "os_name": os.name, "platform_system": platform.system(),
               "python_version": "%d.%d" % sys.version_info[:2]}
        for part in re.split(r"\s+and\s+", marker.strip()):
            m = re.fullmatch(r"\s*(\w+)\s*(==|!=|<|<=|>|>=)\s*['\"]([^'\"]*)['\"]\s*", part)
            if not m or m.group(1) not in env:
                continue
            have, op, want = env[m.group(1)], m.group(2), m.group(3)
            if m.group(1) == "python_version":
                have, want = tuple(map(int, have.split("."))), tuple(map(int, want.split(".")))
            ok = {"==": have == want, "!=": have != want, "<": have < want, "<=": have <= want,
                  ">": have > want, ">=": have >= want}[op]
            if not ok:
                return False
        return True

dists = md.packages_distributions().get(package, [package])
missing, seen, todo = [], set(), list(dists)
while todo:
    name = todo.pop()
    key = re.sub(r"[-_.]+", "-", name).lower()
    if key in seen:
        continue
    seen.add(key)
    try:
        dist = md.distribution(name)
    except md.PackageNotFoundError:
        missing.append(name)
        continue
    for req in dist.requires or []:
        name, _, marker = req.partition(";")
        if marker.strip() and not applies(marker):
            continue
        todo.append(re.split(r"[\s<>=!~\[(]", name.strip(), maxsplit=1)[0])
error = None
if module and not missing:
    try:
        importlib.import_module(module)
    except Exception as e:  # noqa: BLE001
        error = f"{type(e).__name__}: {e}"
print(json.dumps({"missing": sorted(missing), "error": error}))
"""


def interpreter(front_door: Path) -> str | None:
    """The python the generated front door execs, or None."""
    try:
        m = _EXEC.search(front_door.read_text(encoding="utf-8", errors="replace"))
    except OSError:
        return None
    return m.group(1) if m else None


def probe(team: str, front_door: Path | None, home: Path, package: str = "myteams",
          module: str | None = None) -> dict:
    out = {"ok": False, "why": "", "python": None, "missing": []}
    if front_door is None or not front_door.is_file():
        out["why"] = "myteams is not on PATH"
        return out
    python = interpreter(front_door)
    out["python"] = python
    if not python or not Path(python).is_file():
        out["why"] = f"myteams's interpreter {python!r} is missing"
        return out
    if not (home / team / "install").is_dir():
        out["why"] = f"{team} is not installed ({home / team / 'install'} is missing)"
        return out
    if module is None:
        module = "myteams.front_door" if package == "myteams" else ""
    done = subprocess.run([python, "-I", "-c", _CHECK, package, module], capture_output=True, text=True,
                          timeout=60)
    try:
        result = json.loads(done.stdout.strip().splitlines()[-1])
    except (ValueError, IndexError):
        out["why"] = f"the check failed in {python}: {done.stderr.strip()[-300:]}"
        return out
    out["missing"] = result["missing"]
    if result["missing"]:
        out["why"] = "missing distributions: " + ", ".join(result["missing"])
    elif result["error"]:
        out["why"] = f"{module} does not import: {result['error']}"
    else:
        out["ok"], out["why"] = True, f"{team} is installed and its requirements import"
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("team")
    ap.add_argument("--myteams", type=Path, help="the front door (default: myteams on PATH)")
    ap.add_argument("--home", type=Path, default=Path.home() / ".myagenticteams")
    ap.add_argument("--package", default="myteams")
    a = ap.parse_args(argv)
    door = a.myteams or (Path(p) if (p := shutil.which("myteams")) else None)
    print(json.dumps(probe(a.team, door, a.home, a.package), indent=2))
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))      # run with -I too
    from repo_path import run_main      # gapfix13 (G263, G271)
    run_main(main)
