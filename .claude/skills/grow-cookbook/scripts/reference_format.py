#!/usr/bin/env python3
"""Which `A/reference.json` rows were written by an older speciality_reference.py (1.4.27, R-I-1).

`<devteam>/speciality_reference.py` stamps each row it writes with `format`,
the reference format its file is written in (its FORMAT). Format 2 takes
`## Standing focus` and `## Tidy focus` (grow-cookbook 1.4.26); format 3 leaves
out a roled skill's `## Review focus` and review bar, which the devteam copies
whole from the topic's reviewer pair, so they are not its own text (1.4.46); a row with no
stamp, or an older one, was written before that, its file lacking text the
measure needs. Such a row is stale: run_gaps.py, `unmeasured.py --check` and
stage_status.py list it in `stale_reference`, never measure it as current;
a stale reference holds the area at `next: plan`, approved or not (1.4.28).
Raise REFERENCE_FORMAT with the devteam's FORMAT. Stdlib only.

Every stale row names its `reason` (1.4.29), the field a script reads, never
the wording of `why`: OLD_FORMAT (an A/reference.json row), LEGACY_NULL (one
with no `file`: it drops on rewrite, no re-measure; G108, 1.4.33), NO_WRITER (a
`marked_here` reference run_gaps.py could not rewrite) or OLD_REPORT
(A/run_gaps.json itself: `report_row`), saved under an older format or
none, or saved while it listed a stale row (REPORT_STALE_WHY; N4-I-1, 1.4.30).
An A/reference.json that cannot be read as a list of rows is
UNREADABLE_REFERENCE (`unreadable_row`; stage_status.py, N5-I-1, 1.4.31).
`is_current` is the one test of a recorded format. An approval records no
format: it names A/reference.json's hash (stage_status.py, 1.4.30).

An R9 `new-<name>.json` (stage-1.md, R9) records under R9_HASHES the
`git hash-object` hash of each reference it was measured against, written by
r9_stamp.py right after the measure (1.4.33, G94). `r9_stale` lists each R9
file of a gaps folder whose recorded hash is missing or differs from the
reference as it is now: run_gaps.py and stage_status.py report it as
`r9_stale`, and it holds the area at `next: plan`.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

REFERENCE_FORMAT = 3
WHY = (f"reference text predates format {REFERENCE_FORMAT} (adds sections the measure needs): rewrite "
       "A/reference (step 1.1, then steps 1.2 and 1.3) and re-measure")
LEGACY_NULL = "legacy_null"
LEGACY_NULL_WHY = (f"a row with no file, written before reference format {REFERENCE_FORMAT} for another area's "
                   "speciality (no longer written, G57): drops on rewrite, no re-measure (step 1.1)")


OLD_FORMAT, NO_WRITER, OLD_REPORT = "old_format", "no_writer", "old_report"
NO_WRITER_WHY = "no speciality_reference.py to rewrite it"
REPORT_WHY = (f"saved under an older reference format, or none: a reference it measured may predate format "
              f"{REFERENCE_FORMAT}; re-run run_gaps.py (step 1.3), which saves it again")
REPORT_STALE_WHY = ("saved while it listed a stale row: it measured a stale reference, whatever A/reference.json "
                    "says now; re-run run_gaps.py (step 1.3), which saves it again")
NO_REPORT_WHY = ("no A/run_gaps.json beside the plan (saved before 1.4.26, or never run): no saved report "
                 "vouches for the plan's figures; re-run run_gaps.py (step 1.3), which saves it, then step 4")
UNREADABLE_REFERENCE = "unreadable_reference"
UNREADABLE_WHY = ("cannot be read as a list of rows (invalid JSON, not a list, or a row that is not an object): "
                  "rewrite A/reference (step 1.1, then steps 1.2 and 1.3) and re-measure")


def is_current(fmt) -> bool:
    """Whether a recorded format is REFERENCE_FORMAT or newer (a number, never a bool or a string)."""
    return isinstance(fmt, int) and not isinstance(fmt, bool) and fmt >= REFERENCE_FORMAT


def stale_reference(rows) -> list[dict]:
    """[{"speciality", "file", "format", "want", "why", "reason"}] for each
    row whose `format` is missing or older than REFERENCE_FORMAT, in row order;
    a row with no `file` is LEGACY_NULL (G108, 1.4.33), every other OLD_FORMAT."""
    out = []
    for r in rows if isinstance(rows, list) else []:
        if not isinstance(r, dict):
            continue
        f = r.get("format")
        if is_current(f):
            continue
        null = r.get("file") is None        # G108 (1.4.33): nothing to measure, only to drop
        out.append({"speciality": r.get("speciality"), "file": r.get("file"), "format": f,
                    "want": REFERENCE_FORMAT, "why": LEGACY_NULL_WHY if null else WHY,
                    "reason": LEGACY_NULL if null else OLD_FORMAT})
    return out


def report_row(file: str, fmt, why: str = REPORT_WHY) -> dict:
    """The stale row for a saved run_gaps report that records `fmt` (None: none)."""
    return {"speciality": None, "file": file, "format": fmt, "want": REFERENCE_FORMAT,
            "why": why, "reason": OLD_REPORT}


def unreadable_row(file: str) -> dict:
    """The stale row for an A/reference.json that cannot be read as rows."""
    return {"speciality": None, "file": file, "format": None, "want": REFERENCE_FORMAT,
            "why": UNREADABLE_WHY, "reason": UNREADABLE_REFERENCE}


R9_HASHES = "reference_hashes"
R9_FOLDER_HASH = "folder_hash"
R9_REASONS = {
    "no_hash": "records no hash of the reference it was measured against (written before 1.4.33, or by hand)",
    "changed": "the reference changed since it was measured",
    "missing_reference": "the reference it was measured against is gone",
    "unreadable": "cannot be read as an R9 measure (invalid JSON, no `folder`, or no non-empty `references` list)",
    "folder_no_hash": "records no hash of the survivor folder it was measured on (stamped before 1.4.34, or by hand)",
    "folder_changed": "the survivor folder (its artifact.json or a *.md part) changed since it was measured",
    "missing_folder": "the survivor folder it was measured on is gone",
}
R9_FIX = "re-run its R9 command and then r9_stamp.py on it (stage-1.md, R9)"


def blob_hash(path: Path) -> str:
    """The hash `git hash-object <path>` prints."""
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def folder_hash(folder: Path) -> str:
    """Fix round 1 (1.4.34, review I2): the sha1 of the sorted
    "<relpath> <blob hash>" lines of the files cookr reads in a survivor
    folder, its artifact.json and every *.md at any depth. A rename, an edit,
    an added or a removed part changes it; any other file does not."""
    d = Path(folder)
    files = sorted(p for p in d.rglob("*") if p.is_file() and (p.name == "artifact.json" or p.suffix == ".md"))
    lines = "".join(f"{p.relative_to(d).as_posix()} {blob_hash(p)}\n" for p in files)
    return hashlib.sha1(lines.encode("utf-8")).hexdigest()


def _r9_roots(gaps_dir: Path, repo: Path | None = None) -> list[Path]:
    """Where a relative R9 path is looked up, in order: the area folder (the
    gaps folder's parent) and each folder above it, up to the folder that
    holds the workspace (the parent of `areas`' parent) or a git checkout's
    root, whichever comes first; then `repo` when given. Never the cwd."""
    area = Path(os.path.abspath(gaps_dir)).parent
    roots, stop = [], None
    for p in [area, *area.parents]:
        roots.append(p)
        if p.name == "areas" and stop is None:
            stop = p.parent.parent
        if p == stop or (p / ".git").exists():
            break
    if repo is not None:
        roots.append(Path(os.path.abspath(repo)))
    return roots


def r9_reference(file: str, gaps_dir: Path, repo: Path | None = None) -> Path:
    """An R9 path (a reference `file` or the survivor `folder`) as a path:
    absolute as written; a relative one under the first of _r9_roots where it
    exists, else under the area folder (where it is then missing). Never
    resolved against the cwd (fix round 1, 1.4.34, review M6)."""
    p = Path(file)
    if p.is_absolute():
        return p
    roots = _r9_roots(gaps_dir, repo)
    return next((r / p for r in roots if (r / p).exists()), roots[0] / p)


def r9_inputs(data) -> tuple[str, list[str]]:
    """(folder, [reference files]) of a loaded R9 file; TypeError when it has
    no `folder` string or no non-empty `references` list of {"file"}
    (fix round 1, 1.4.34, review M6: an empty list is unreadable)."""
    refs = data["references"]
    folder = data["folder"]
    if not isinstance(folder, str) or not folder or not isinstance(refs, list) or not refs or not all(
            isinstance(r, dict) and isinstance(r.get("file"), str) and r["file"] for r in refs):
        raise TypeError("no folder, or no non-empty references list")
    return folder, [r["file"] for r in refs]


def r9_stale(gaps_dir: Path, repo: Path | None = None) -> list[dict]:
    """[{"file", "input", "reference", "recorded", "current", "reason", "why"}],
    one per stale input of each R9 `new-*.json` in `gaps_dir`, by file: one
    row per stale reference (`input` "reference"), then one for the survivor
    folder (`input` "folder", `reference` the folder as written) when it is
    gone, unstamped or changed (fix round 1, 1.4.34, review I2); one row with
    `input` and `reference` None for a file that cannot be read."""
    out = []
    d = Path(gaps_dir)
    for f in sorted(d.glob("new-*.json")) if d.is_dir() else []:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            folder, files = r9_inputs(data)
        except (OSError, ValueError, KeyError, TypeError):
            out.append(_r9_row(f.name, None, None, None, None, "unreadable"))
            continue
        recorded = data.get(R9_HASHES)
        recorded = recorded if isinstance(recorded, dict) else {}
        for file in files:
            path = r9_reference(file, d, repo)
            current = blob_hash(path) if path.is_file() else None
            was = recorded.get(file)
            reason = ("missing_reference" if current is None else "no_hash" if was is None
                      else "changed" if was != current else None)
            if reason:
                out.append(_r9_row(f.name, "reference", file, was, current, reason))
        path = r9_reference(folder, d, repo)
        current = folder_hash(path) if path.is_dir() else None
        was = data.get(R9_FOLDER_HASH)
        was = was if isinstance(was, str) else None
        reason = ("missing_folder" if current is None else "folder_no_hash" if was is None
                  else "folder_changed" if was != current else None)
        if reason:
            out.append(_r9_row(f.name, "folder", folder, was, current, reason))
    return out


def _r9_row(file: str, input_, reference, recorded, current, reason: str) -> dict:
    return {"file": file, "input": input_, "reference": reference, "recorded": recorded, "current": current,
            "reason": reason, "why": f"{R9_REASONS[reason]}: {R9_FIX}"}
