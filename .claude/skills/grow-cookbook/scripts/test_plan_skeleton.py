"""plan_skeleton.py: the plan's section headings and its digest lines (G181, 1.4.37).

    python3 -m pytest .claude/skills/grow-cookbook/scripts -q
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import plan_skeleton  # noqa: E402
import stage_status  # noqa: E402


def test_its_headings_are_stage_status_plan_sections_in_order(tmp_path):
    # G181 (N32): the headings match stage_status.PLAN_SECTIONS; each digest
    # line sits under the section that records it; a script that cannot give
    # one is named in its place, exit 1.
    repo = tmp_path / "repo"
    (repo / "cookbook" / "guidelines" / "a" / "b").mkdir(parents=True)
    ws = tmp_path / "ws"
    (ws / "areas").mkdir(parents=True)      # G198 (1.4.39): a workspace holds areas/
    (repo / "skills" / "cookr").mkdir(parents=True)
    (repo / "skills" / "cookr" / "SKILL.md").write_text("cookr\n", encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", str(HERE / "plan_skeleton.py"), "--area", "a/b", "--workspace", str(ws),
                        "--repo", str(repo)], capture_output=True, text=True)
    heads = [line[3:] for line in r.stdout.splitlines() if line.startswith("## ")]
    assert heads == list(stage_status.PLAN_SECTIONS), r.stdout
    assert plan_skeleton.SECTIONS == stage_status.PLAN_SECTIONS
    body = dict(stage_status._sections_of(r.stdout))
    assert any("copy_check.py" in line for line in body["Overlaps"])
    step4 = "\n".join(body["Step-4 re-check"])
    for script in ("unmeasured.py", "run_gaps.py", "stage_status.py"):
        assert script in step4, step4
    assert r.returncode == 1 and "no digest" in r.stdout
    # G248 (L26, 1.4.40): the line the plan records is the hand-off `--check --hints --digest` one, written (or
    # named, when it cannot be) beside the saved report's.
    assert "run_gaps.py --check --hints --digest" in step4, step4
    own = subprocess.run([sys.executable, "-I", str(HERE / "stage_status.py"), "--area", "a/b", "--workspace", str(ws),
                          "--repo", str(repo), "--digest"], capture_output=True, text=True)
    assert own.returncode == 0 and own.stdout.strip(), own.stderr
    assert f"- {own.stdout.strip()}" in body["Step-4 re-check"], step4    # stage_status's own digest line
    assert [p.name for p in ws.iterdir()] == ["areas"] and not any((ws / "areas").iterdir())   # read-only
