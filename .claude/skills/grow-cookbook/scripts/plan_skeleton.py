#!/usr/bin/env python3
"""Print an area plan's section headings with its digest lines in place (G181, 1.4.37).

    python3 plan_skeleton.py --area <area> --workspace W --repo R

Read-only: writes nothing, prints to stdout. The headings are
stage_status.PLAN_SECTIONS, in order, each `## ` heading followed by a blank
line. Under **Overlaps** it puts `copy_check.py --digest`'s line; under
**Step-4 re-check** the lines of `unmeasured.py --check --digest`,
`run_gaps.py --digest` (the saved report's, labelled `saved`; its per-topic
lines follow, indented), `run_gaps.py --check --hints --digest` (1.4.40, G248:
the line the plan records, stage-1.md step 4) and `stage_status.py --digest`. Each
line is the script's own, run with this Python; a script that cannot give one (exit 2, or no line) is named in
its place as `- (no digest: <script> exited N: <its first message line>)`,
and this script then exits 1. Stdlib only.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from repo_path import add_area, area_arg  # noqa: E402
from stage_status import PLAN_SECTIONS  # noqa: E402

SECTIONS = PLAN_SECTIONS
WHERE = {"Overlaps": [("copy_check.py", ["--digest"])],
         "Step-4 re-check": [("unmeasured.py", ["--check", "--digest"]), ("run_gaps.py", ["--digest"]),
                             ("run_gaps.py", ["--check", "--hints", "--digest"]),
                             ("stage_status.py", ["--digest"])]}


def line(script: str, flags: list[str], area: str, workspace: Path, repo: Path) -> tuple[str, bool]:
    """(the line to print, whether it is a digest) for one script."""
    r = subprocess.run([sys.executable, "-I", str(HERE / script), "--area", area, "--workspace", str(workspace),
                        "--repo", str(repo), *flags], capture_output=True, text=True, cwd=HERE)
    out = [x for x in r.stdout.splitlines() if x.strip()]
    if r.returncode in (0, 1) and out and not out[0].startswith((" ", "{", "[")):   # unmeasured --check: 1 on a change
        return "\n".join([f"- {out[0]}", *(f"  {x.strip()}" for x in out[1:])]), True
    said = next((x for x in (r.stderr + r.stdout).splitlines() if x.strip()), "no output")
    return f"- (no digest: {' '.join([script, *flags])} exited {r.returncode}: {said.strip()})", False


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    add_area(ap)
    ap.add_argument("--workspace", type=Path, required=True)
    ap.add_argument("--repo", type=Path, required=True)
    a = ap.parse_args(argv)
    a.area = area_arg(ap, a)
    from repo_path import check_area
    why = check_area("plan_skeleton.py", a.workspace, a.area, getattr(a, "repo", None))      # G198 (1.4.39)
    if why:
        print(why, file=sys.stderr)
        return 2
    ws, repo = a.workspace.resolve(), a.repo.resolve()
    ok = True
    print(f"# {a.area}: area plan\n")
    for section in SECTIONS:
        print(f"## {section}\n")
        lines = [line(s, f, a.area, ws, repo) for s, f in WHERE.get(section, [])]
        for text, good in lines:
            print(text)
            ok = ok and good
        if lines:
            print()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))      # run with -I too
    from repo_path import run_main      # gapfix13 (G263, G271)
    run_main(main)
