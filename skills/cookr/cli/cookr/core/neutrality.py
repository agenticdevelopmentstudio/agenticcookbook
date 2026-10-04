"""The neutrality census: shared text names no host or model.

Wording that is true for one host or model belongs in a `hosts/` addition
(core/tuning.py), so every target reads shared text that is true for it. The
census scans each artifact folder's parts, history excepted, for the words
cookr's host manifest declares (hosts and model families), case-insensitive,
whole words. An artifact whose subject is a host, such as one documenting
Claude Code's file layout, records why in `names_hosts` in its artifact.json.

Findings:
- `unlisted`: names a host and records no reason.
- `stale`: records a reason but names no host any more.
- `short`: a reason under 16 characters, which explains nothing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional

from .artifact import HISTORY, ArtifactError, load_folder
from .hosts import Host, names

MIN_REASON = 16


@dataclass
class Finding:
    folder: Path
    kind: str                     # "unlisted" | "stale" | "short"
    words: list[str] = field(default_factory=list)


def pattern(words: Iterable[str]) -> re.Pattern:
    alts = "|".join(re.escape(w) for w in sorted(words, key=len, reverse=True))
    return re.compile(rf"(?<![A-Za-z0-9])({alts})(?![A-Za-z0-9])", re.I)


def mentions(folder: Path, pat: re.Pattern) -> list[str]:
    """The host and model words in the folder's shared parts, lowercased, in
    first-seen order."""
    artifact = load_folder(folder)
    seen: dict[str, None] = {}
    for p in artifact.parts:
        if p.name == HISTORY:
            continue
        for m in pat.finditer(f"{p.heading or ''}\n{p.text}"):
            seen.setdefault(m.group(1).lower(), None)
    return list(seen)


def census(folders: Iterable[Path], hosts: Optional[dict[str, Host]] = None) -> list[Finding]:
    pat = pattern(names(hosts))
    findings = []
    for folder in folders:
        try:
            reason = load_folder(folder).names_hosts
            words = mentions(folder, pat)
        except ArtifactError:
            continue  # a broken folder is the compile check's to report
        if words and reason is None:
            findings.append(Finding(folder, "unlisted", words))
        elif reason is not None and not words:
            findings.append(Finding(folder, "stale"))
        elif reason is not None and len(reason.strip()) < MIN_REASON:
            findings.append(Finding(folder, "short", words))
    return findings


FIX = {
    "unlisted": "Move the host-specific wording into hosts/<target>.add.md, or, when the artifact's "
                "subject is that host, set `names_hosts` in its artifact.json to the reason.",
    "stale": "It no longer names a host: remove `names_hosts` from its artifact.json.",
    "short": f"Say why in at least {MIN_REASON} characters.",
}
