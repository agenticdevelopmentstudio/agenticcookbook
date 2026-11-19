#!/usr/bin/env python3
"""The keys of a script's JSON output, for `--keys` / `--summary` (G119, 1.4.33).

stage_status.py, run_gaps.py and paraphrase_hints.py print long JSON; a re-run
that reads only some keys can miss one that holds the area. `keys(result)`
keeps every top-level key, in order, and shortens only its value: a scalar
(str, number, bool, None) as it is, an empty list as `[]`, a list of N items
as {"rows": N}, an empty dict as {}, any other dict as {"keys": [its keys,
sorted]}. No key is ever dropped, so an empty list still shows as `[]`.
G138 (1.4.36): a list under one of ROW_KEYS (a hold, an advisory list, and
`new_keys` and `changes` of a check) is printed whole, its rows never only
counted: the hand-off reads them.
Stdlib only.
"""

from __future__ import annotations


ROW_KEYS = frozenset({"plan_sections", "stale_reference", "r9_stale", "stale_copy_check", "other_plans_changed",
                      "carries_asked", "held_by_wording",
                      "survivor_carries", "new_keys", "changes",
                      # 1.4.39: G188 host_check, G190 shared_no_host, G216 stale_pointer, G205 stale_home
                      "host_check", "shared_no_host", "stale_pointer", "stale_home", "gap_total",
                      # 1.4.41: G251 stale_verdicts
                      "stale_verdicts",
                      # gapfix13 (1.4.42): G253, G254, G256, G257, G269
                      "cite_moved", "hand_lacks", "home_lacking", "r9_lacking", "topic_totals", "non_home_lacking",
                      "counted_rows", "check_homes", "report_refresh",
                      # gapfix13b (1.4.42): platform-integration#5
                      "short_not_owed"})

# G220 (1.4.39): which script prints each output key a re-run asks another
# script for, and which row a field belongs to, so `--rows K` names the owner.
OWNER = {**{k: "run_gaps.py" for k in (
    "out", "note", "reference_format", "why_empty", "building", "same_text", "measured_elsewhere", "unmeasurable",
    "missing_files", "hints", "cleared", "stale_gaps", "r9_targets", "r9_missing", "failed", "unplaced",
    "short_sentences", "markers", "repeat_of", "held_by_wording", "home_measures", "home_unguessed",
    "numbering_differs", "advisory_failed", "stale_home", "gap_total", "hand_lacks", "home_lacking", "r9_lacking",
    "topic_totals", "counted_rows", "counted_with_prior_verdict", "counted_never_judged", "check_homes",
    "measured_total", "lacking_pieces", "skill_version")},
         **{k: "unmeasured.py" for k in (
    "new_topics", "marked_here", "mark_conflicts", "against_survivor", "survivor_elsewhere", "unread_marks",
    "ignored_marks")},
         **{k: "stage_status.py" for k in (
    "plan", "approval", "approval_why", "reference_hash", "cookr", "topics", "incoming", "incoming_unplanned",
    "conflicts", "pending_target", "speciality_points_at_copy", "stale_reference", "r9_stale", "plan_sections",
    "stale_copy_check", "host_check", "other_plans_changed", "survivor_carries", "carries_asked", "shared_no_host",
    "stale_pointer", "cite_moved", "stale_verdicts", "report_refresh", "next", "next_why")}}
FIELD_OF = {"home_recorded": ("run_gaps.py", "home_unguessed"), "verdict": ("run_gaps.py", "held_by_wording"),
            "topic_sentence": ("run_gaps.py", "held_by_wording"), "piece": ("run_gaps.py", "held_by_wording"),
            "modal_differs": ("run_gaps.py", "held_by_wording"), "home_topic": ("run_gaps.py", "held_by_wording"),
            "cited_at": ("stage_status.py", "other_plans_changed"),
            "question_cites": ("stage_status.py", "other_plans_changed"),
            "kind": ("stage_status.py", "survivor_carries and carries_asked")}


def split_keys(text: str | None) -> list[str]:
    """L17 (1.4.40): `--rows a,b`'s keys, in order, one parse for every script that takes it."""
    return [k.strip() for k in text.split(",") if k.strip()] if text is not None else []


def owner_of(key: str, script: str) -> str:
    """G220 (1.4.39): what `--rows KEY` says when `script` prints no KEY."""
    if key in FIELD_OF:
        owner, row = FIELD_OF[key]
        return (f"{key} is a field of {owner}'s {row} rows, not an output key"
                + (" (the piece's own text is the row's `text`)" if key == "piece" else "")
                + f": run {owner} --rows {row.split()[0]}")
    if key in OWNER and OWNER[key] != script:
        return f"{key} is {OWNER[key]}'s output key: run {OWNER[key]} --rows {key}"
    return ""


CAP = 40      # gapfix13 (G271, 1.4.42): rows printed per key by --keys and --check


def _cut(v, key: str, limit: int):
    if isinstance(v, list):
        kept = [_cut(x, key, limit) for x in v[:limit]]
        return kept + [f"({len(v) - limit} more: --rows {key})"] if len(v) > limit else kept
    if isinstance(v, dict):
        return {k: _cut(x, key, limit) for k, x in v.items()}
    return v


def cap(result: dict, limit: int = CAP) -> dict:
    """G271 (1.4.42): each list in `result`, at any depth, cut to `limit`
    rows, a last item `(N more: --rows <key>)` naming the top-level key that
    prints it whole; nothing else changes."""
    return {k: _cut(v, k, limit) for k, v in result.items()}


def keys(result: dict) -> dict:
    out = {}
    for k, v in result.items():
        if k in ROW_KEYS and isinstance(v, list):
            out[k] = cap({k: v})[k]
        elif isinstance(v, list):
            out[k] = {"rows": len(v)} if v else []
        elif isinstance(v, dict):
            out[k] = {"keys": sorted(v)} if v else {}
        else:
            out[k] = v
    return out
