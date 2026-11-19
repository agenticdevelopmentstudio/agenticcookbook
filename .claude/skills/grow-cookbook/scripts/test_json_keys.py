"""json_keys.py, and the --keys/--summary flag of stage_status.py,
run_gaps.py and paraphrase_hints.py (G119, 1.4.33).

    python3 -m pytest .claude/skills/grow-cookbook/scripts -q
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import json_keys  # noqa: E402
import paraphrase_hints  # noqa: E402
import stage_status  # noqa: E402
import test_paraphrase_hints as tph  # noqa: E402
import test_stage_status as tss  # noqa: E402


def test_every_key_is_kept_and_an_empty_list_prints_as_one():
    out = json_keys.keys({"next": "plan", "n": 0, "flag": False, "none": None, "empty": [], "rows": [1, 2],
                          "map": {"b": 1, "a": 2}, "blank": {}})
    assert out == {"next": "plan", "n": 0, "flag": False, "none": None, "empty": [], "rows": {"rows": 2},
                   "map": {"keys": ["a", "b"]}, "blank": {}}
    assert list(out) == ["next", "n", "flag", "none", "empty", "rows", "map", "blank"]


def test_stage_status_keys_lists_every_key_of_the_full_output(tmp_path, capsys):
    repo = tmp_path
    (repo / "cookbook").mkdir()
    tss.cookr_skill(repo)
    tss.area(repo, {"t": "cookbook/guidelines/implementing/data/t"})
    args = [tss.AREA, "--repo", str(repo)]
    assert stage_status.main(args) == 0
    full = json.loads(capsys.readouterr().out)
    for flag in ("--keys", "--summary"):
        assert stage_status.main([*args, flag]) == 0
        short = json.loads(capsys.readouterr().out)
        assert list(short) == list(full) and short == json_keys.keys(full)


def test_paraphrase_hints_keys_lists_every_key(tmp_path, capsys):
    folder = tph.topic(tmp_path)                      # makes cookbook/guidelines/: a real repo
    g = tph.gaps(tmp_path / "A" / "gaps", folder)
    full = paraphrase_hints.hints(g, tmp_path)
    for flag in ("--keys", "--summary"):
        assert paraphrase_hints.main([str(g), "--repo", str(tmp_path), flag]) == 0
        assert json.loads(capsys.readouterr().out) == json_keys.keys(full)


def test_the_rows_of_every_hold_and_check_list_are_printed_whole():
    # G138 (N17, 1.4.36): never only a count for these.
    rows = [{"why": "x"}, {"why": "y"}]
    full = {k: rows for k in ("plan_sections", "stale_reference", "r9_stale", "stale_copy_check",
                              "other_plans_changed", "survivor_carries", "changes")}
    full.update(new_keys=["a.b", "c"], building=rows)
    out = json_keys.keys(full)
    assert all(out[k] == full[k] for k in full if k != "building") and out["building"] == {"rows": 2}


def test_a_row_list_over_40_rows_is_capped_naming_the_rest():
    """gapfix13 (G271, 1.4.42): --keys and --check print at most 40 rows per key."""
    out = json_keys.cap({"held_by_wording": list(range(45)), "few": [1, 2], "n": 3})
    assert out["held_by_wording"][:40] == list(range(40))
    assert out["held_by_wording"][40] == "(5 more: --rows held_by_wording)" and len(out["held_by_wording"]) == 41
    assert out["few"] == [1, 2] and out["n"] == 3
    assert json_keys.keys({"changes": list(range(41))})["changes"][-1] == "(1 more: --rows changes)"
