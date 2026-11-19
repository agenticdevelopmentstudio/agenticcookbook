#!/usr/bin/env python3
"""Record in an R9 `A/gaps/new-<name>.json` the hash of each reference it was measured against (1.4.33, G94).

    $COOKR_PY ${CLAUDE_SKILL_DIR}/scripts/r9_stamp.py A/gaps/new-<name>.json

Run right after the R9 measure (stage-1.md, R9) writes the file, and after
every re-run of it. Adds `reference_hashes`: {<each `references[].file` as
written>: <its `git hash-object` hash>}, and `folder_hash`: the hash of the
survivor `folder`'s artifact.json and *.md files (reference_format.folder_hash;
1.4.34, review I2: the measure's other input), the rest of the file kept as
it is, written atomically. A relative path resolves against the area folder
and the folders above it up to the workspace's (or `--repo`), never the cwd
(reference_format.r9_reference). run_gaps.py and stage_status.py list an R9
file whose recorded hash is missing or differs from its input now in
`r9_stale` (reference_format.r9_stale), which holds the area at `next: plan`.
Prints {"file", "reference_hashes", "folder_hash"}. Exit 0 stamped; 2 when
the file is not named `new-*.json`, cannot be read as an R9 measure, lists no
reference or no folder, or a reference or the folder it lists is missing
(nothing written). Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from reference_format import R9_FOLDER_HASH, R9_HASHES, blob_hash, folder_hash, r9_inputs, r9_reference  # noqa: E402


def stamp(path: Path, repo: Path | None = None) -> tuple[dict, str]:
    """The file's (`reference_hashes`, `folder_hash`), written into it; SystemExit naming why it cannot be."""
    if not (path.name.startswith("new-") and path.suffix == ".json"):
        raise SystemExit(f"r9_stamp.py: {path} is not an R9 file (A/gaps/new-<name>.json)")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        folder, files = r9_inputs(data)
    except (OSError, ValueError, KeyError, TypeError) as e:
        raise SystemExit(f"r9_stamp.py: {path} cannot be read as an R9 measure ({e.__class__.__name__}: {e}); "
                         "re-run its R9 command (stage-1.md, R9)")
    hashes = {}
    for f in files:
        ref = r9_reference(f, path.parent, repo)
        if not ref.is_file():
            raise SystemExit(f"r9_stamp.py: {path} lists {f}, which does not exist: rewrite A/reference "
                             "(step 1.1) and re-run the R9 command")
        hashes[f] = blob_hash(ref)
    survivor = r9_reference(folder, path.parent, repo)
    if not survivor.is_dir():
        raise SystemExit(f"r9_stamp.py: {path} was measured on {folder}, which does not exist: re-run the R9 "
                         "command on the candidate survivor as it is now")
    data[R9_HASHES] = hashes
    data[R9_FOLDER_HASH] = fhash = folder_hash(survivor)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
            fh.write("\n")
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise
    return hashes, fhash


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("file", help="the R9 file, A/gaps/new-<name>.json")
    ap.add_argument("--repo", help="also resolve a relative path against this checkout")
    a = ap.parse_args(argv)
    path = Path(os.path.abspath(os.path.expanduser(a.file)))
    try:
        hashes, fhash = stamp(path, Path(a.repo).expanduser() if a.repo else None)
    except SystemExit as e:
        print(e, file=sys.stderr)
        return 2
    print(json.dumps({"file": str(path), R9_HASHES: hashes, R9_FOLDER_HASH: fhash}, indent=2))
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))      # run with -I too
    from repo_path import run_main      # gapfix13 (G263, G271)
    run_main(main)
