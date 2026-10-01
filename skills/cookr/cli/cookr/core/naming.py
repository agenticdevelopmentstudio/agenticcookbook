"""Names in kebab-case: component names from file stems, cookbook paths from code paths."""

from __future__ import annotations

import re

_SPLIT_CAMEL = re.compile(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")
_NON_ALNUM = re.compile(r"[^a-z0-9]+")
# Platform names whose own casing reads as two words to the camel split.
_WORDS = re.compile(r"([Mm]acOS|iOS|iPadOS|tvOS|watchOS|visionOS)(?![a-z])")


def kebab(stem: str) -> str:
    spaced = _SPLIT_CAMEL.sub("-", stem)
    lowered = spaced.lower()
    return _NON_ALNUM.sub("-", lowered).strip("-")


def path_name(stem: str) -> str:
    """`kebab`, keeping a platform name whole: `macOS` is `macos`, not `mac-os`.

    Names in a library cookbook's tree use this. `kebab` itself stays as it
    was, because a `.cookr.json` corpus was named with it and `cookr organize`
    must match those names.
    """
    return kebab(_WORDS.sub(lambda m: f"-{m.group(1).lower()}-", stem))
