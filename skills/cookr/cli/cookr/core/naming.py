"""Component names: a file stem rendered as kebab-case."""

from __future__ import annotations

import re

_SPLIT_CAMEL = re.compile(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")
_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def kebab(stem: str) -> str:
    spaced = _SPLIT_CAMEL.sub("-", stem)
    lowered = spaced.lower()
    return _NON_ALNUM.sub("-", lowered).strip("-")
