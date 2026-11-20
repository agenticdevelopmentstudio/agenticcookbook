#!/usr/bin/env python3
"""The devteam checkout stage 1 measures an area against (1.4.45).

Stage 1 measures what an area lacks against the devteam's specialities, whose
text the devteam's own `speciality_reference.py` writes. That script lives in
an agenticdevteam checkout, not in this repo: by default the one two folders
above `<repo>` (where the cookbook sits as the devteam's submodule), or the
folder `--devteam` names. Prints that checkout's path, or exits 2 with one
plain message naming what stage 1 needs. Stdlib only.

    $COOKR_PY devteam_checkout.py --repo <repo> [--devteam <checkout>]
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))      # run with -I too

from repo_path import cookbook_repo, run_main  # noqa: E402

SCRIPT = "speciality_reference.py"


def devteam_checkout(given: str | os.PathLike | None, repo: Path) -> Path:
    """The devteam checkout holding SCRIPT; SystemExit (the plain message) when there is none."""
    where = Path(os.path.abspath(os.path.expanduser(given))) if given else repo.parent.parent
    if (where / SCRIPT).is_file():
        return where
    how = f"--devteam {given} holds" if given else f"{where} (two folders above the cookbook repo) holds"
    raise SystemExit(
        f"devteam_checkout.py: stage 1 needs an agenticdevteam checkout: it measures the area against the devteam's "
        f"specialities, whose text that checkout's {SCRIPT} writes, and {how} no {SCRIPT}. Clone agenticdevteam "
        f"and pass --devteam <its checkout> here and to run_gaps.py; stages 2 to 5 need no devteam checkout.")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--repo", help="the cookbook repo (default: the nearest one at or above here)")
    ap.add_argument("--devteam", help="the agenticdevteam checkout (default: <repo>/../..)")
    a = ap.parse_args(argv)
    repo = cookbook_repo(a.repo, "devteam_checkout.py")
    try:
        print(devteam_checkout(a.devteam, repo))
    except SystemExit as e:       # a str SystemExit would exit 1: this one is a usage refusal, 2
        print(e, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    run_main(main)
