#!/usr/bin/env python3
"""Whether the Python running this script can run cookr: Python 3.11 or later
that imports `rich`, `questionary` and `yaml` (pyyaml).

    $COOKR_PY check_cookr_python.py

Prints JSON `{"python", "version", "missing", "too_old", "ok"}`. Exits 0 when
ok; otherwise 2, with a message on stderr naming what is missing.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REQUIRED = ("rich", "questionary", "yaml")
MINIMUM = (3, 11)


def check(required=REQUIRED, minimum=MINIMUM) -> dict:
    missing = [m for m in required if importlib.util.find_spec(m) is None]
    too_old = sys.version_info[:2] < tuple(minimum)
    return {"python": sys.executable, "version": "%d.%d.%d" % sys.version_info[:3],
            "missing": missing, "too_old": too_old, "ok": not missing and not too_old}


def main() -> int:
    result = check(REQUIRED, MINIMUM)
    print(json.dumps(result, indent=2))
    if result["ok"]:
        return 0
    problems = []
    if result["too_old"]:
        problems.append(f"it is Python {result['version']}, and cookr needs {MINIMUM[0]}.{MINIMUM[1]} or later")
    if result["missing"]:
        problems.append("it cannot import " + ", ".join(result["missing"]))
    print(f"COOKR_PY ({result['python']}) cannot run cookr: {'; '.join(problems)}. "
          "Set COOKR_PY to a Python 3.11+ that imports rich, questionary and yaml.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))      # run with -I too
    from repo_path import run_main      # gapfix13 (G263, G271)
    run_main(main)
