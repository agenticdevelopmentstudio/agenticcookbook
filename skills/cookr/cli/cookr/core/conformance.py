"""Conformance: does an implementation still match its recipe.

The stored state lives on the implementation row in `index.json`; the state
reported is *effective*: a changed hash or a recipe that gained a minor or major
version since the confirmed one turns `confirmed` into `needs-validation`.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Callable, Optional

from .artifact import ArtifactError, load_folder
from .history import parse_version
from .index import STATES, Entry, Implementation
from .inventory import IgnoreSet, ignored_for
from .markdown import prune_freezes
from .errors import CookbookError
from .repoconfig import Config, in_repo_path

_RANK = {s: i for i, s in enumerate(STATES)}


def is_url(location: str) -> bool:
    return "://" in location


def check_location(location: str) -> None:
    """A non-URL implementation location must stay inside the repo (no `..`, not
    absolute): CookbookError (exit 2) otherwise, before anything reads or hashes it."""
    if not is_url(location) and not in_repo_path(location):
        raise CookbookError(f"implementation location {location!r} must be a path inside "
                            "the repo (no `..`, not absolute) or a URL")


def location_hash(repo_root: Path, location: str, ignore: IgnoreSet) -> str:
    """`sha256:` over the sorted (relpath, file digest) lines of every non-ignored
    file under a directory location (relpaths relative to it), or of the one file.
    A location outside the repo is refused (`check_location`)."""
    check_location(location)
    repo_root = Path(repo_root)
    target = repo_root / location
    lines: list[str] = []
    if target.is_dir():
        for dirpath, dirnames, filenames in os.walk(target):
            d = Path(dirpath)
            drel = d.relative_to(repo_root).as_posix()
            prefix = "" if drel == "." else f"{drel}/"
            dirnames[:] = sorted(n for n in prune_freezes(d, dirnames)
                                 if not ignore.prunes(prefix + n))
            for fn in filenames:
                f = d / fn
                if ignore.ignores(prefix + fn) or not f.is_file():
                    continue
                rel = f.relative_to(target).as_posix()
                lines.append(f"{rel}\0{hashlib.sha256(f.read_bytes()).hexdigest()}")
    elif target.is_file():
        lines.append(f"{target.name}\0{hashlib.sha256(target.read_bytes()).hexdigest()}")
    digest = hashlib.sha256("\n".join(sorted(lines)).encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def current_hash(config: Config, impl: Implementation) -> Optional[str]:
    """The hash of the implementation's code now; None when there is nothing to
    compare (planned, code outside the repo, or a location gone from disk: see
    `is_missing`)."""
    loc = impl.location
    if not loc or is_url(loc) or is_missing(config, impl):
        return None
    return location_hash(config.repo_root, loc,
                         ignored_for(config, config.root_for(loc.rstrip("/"))))


def is_missing(config: Config, impl: Implementation) -> bool:
    """True when the row's in-repo location no longer exists on disk."""
    loc = impl.location
    return bool(loc) and not is_url(loc) and not (config.repo_root / loc).exists()


def _parses(version: Optional[str]) -> bool:
    return parse_version(version or "") is not None


def level_between(old: str, new: str) -> str:
    """How far `new` is past `old`: none, patch, minor or major."""
    a, b = parse_version(old or ""), parse_version(new or "")
    if a is None or b is None or b <= a:
        return "none"
    if b[0] != a[0]:
        return "major"
    if b[1] != a[1]:
        return "minor"
    return "patch"


def effective_state(impl: Implementation, current_version: str,
                    current_hash: Optional[str], missing: bool = False) -> str:
    """A None `current_hash` means no hash comparison (URL, planned); `missing`
    says the in-repo location is gone."""
    c = impl.conformance
    if c.state in ("planned", "unverified", "needs-validation"):
        return c.state
    if missing:
        return "needs-validation"
    if c.version is None:
        return "needs-validation"  # confirmed with no recorded version (hand-edited)
    if not _parses(current_version):
        return "needs-validation"  # the recipe's version is unreadable: nothing to trust
    if impl.location and not is_url(impl.location) and c.hash is None:
        return "needs-validation"  # confirmed with no recorded hash (hand-edited)
    if c.hash is not None and current_hash is not None and c.hash != current_hash:
        return "needs-validation"
    if level_between(c.version, current_version) in ("minor", "major"):
        return "needs-validation"
    return "confirmed"


def weakest(states: list[str]) -> str:
    """The weakest of `states`; `unplaced` when there are none."""
    return min(states, key=_RANK.__getitem__) if states else "unplaced"


def recipe_state(entry: Entry, current_version: str,
                 hash_of: Callable[[Implementation], Optional[str]],
                 missing_of: Callable[[Implementation], bool] = lambda i: False) -> str:
    """The weakest implementation's effective state; `unplaced` when there are none."""
    states = [effective_state(i, current_version, hash_of(i), missing_of(i))
              for i in entry.implementations]
    return weakest(states)


def stored_state(entry: Entry) -> str:
    """The weakest stored state among the entry's rows, with no drift check (for an
    entry whose code and folder are in another repo); `unplaced` when there are none."""
    states = [i.conformance.state for i in entry.implementations]
    return weakest(states)


def entry_version(cookbook_dir: Path, entry: Entry) -> str:
    """The artifact's current version, read from its folder; "" when unreadable
    (which `effective_state` never treats as conformant)."""
    try:
        meta = load_folder(Path(cookbook_dir) / entry.path).meta
    except (ArtifactError, OSError):
        return ""
    return str(meta.get("version", "") or "")
