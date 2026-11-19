"""reference_format.py: stale A/reference.json rows (G108, 1.4.33).

    python3 -m pytest .claude/skills/grow-cookbook/scripts -q
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import reference_format as rf  # noqa: E402
import stage_status  # noqa: E402


def test_the_stale_why_names_the_format_not_one_sections_pair():
    # G108: the cause is the format, not "Standing focus and Tidy focus" alone.
    assert rf.WHY.startswith(f"reference text predates format {rf.REFERENCE_FORMAT} (adds sections the measure needs)")
    assert "Standing focus" not in rf.WHY


def test_a_null_file_row_is_legacy_null_and_drops_on_rewrite():
    rows = [{"speciality": "data/a", "file": None}, {"speciality": "data/b", "file": "/b.txt", "format": 1},
            {"speciality": "data/c", "file": "/c.txt", "format": rf.REFERENCE_FORMAT}]
    out = rf.stale_reference(rows)
    assert [(r["speciality"], r["reason"]) for r in out] == [("data/a", "legacy_null"), ("data/b", "old_format")]
    assert "drops on rewrite, no re-measure" in out[0]["why"] and out[1]["why"] == rf.WHY


def test_next_why_counts_legacy_null_rows_apart():
    rows = rf.stale_reference([{"speciality": "data/a", "file": None}, {"speciality": "data/b", "file": "/b"}])
    why = stage_status.next_why("plan", None, {}, [], True, rows)
    assert why.startswith(f"stale_reference: 2 row(s) older than reference format {rf.REFERENCE_FORMAT} "
                          "(1 legacy_null: drops on rewrite, no re-measure); "), why
    why = stage_status.next_why("plan", None, {}, [], True, rows[1:])
    assert "legacy_null" not in why
