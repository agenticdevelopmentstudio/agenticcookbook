"""cookr --version reports the version its SKILL.md declares."""

from __future__ import annotations

import re
from pathlib import Path

from cookr import __version__

SKILL = Path(__file__).resolve().parents[3] / "SKILL.md"


def test_the_package_version_matches_the_skill():
    text = SKILL.read_text(encoding="utf-8")
    declared = re.search(r'^version:\s*"?([^"\s]+)"?\s*$', text, re.M).group(1)
    assert __version__ == declared
    assert f"# cookr v{declared}" in text


def test_the_version_is_pinned():
    # 0.21.1: a bare lead-in is judged against its rules' names too.
    # 0.21.2: a moved entry may be retargeted once after a judged fail
    # (`retargeted`), and a judged fail after that retarget is final.
    # 0.21.3: `--retarget` writes the one retarget (sealed, ledgered) and
    # refuses a second; a retarget made by hand fails by name; a retargeted
    # entry's stale fail is re-judged after the rewrite.
    # 0.21.4: `--retarget` refuses targets that fail the bar or a tripwire
    # (nothing spent), and the seal is taken over canonical JSON.
    # 0.22.0: merges main's 0.14.0 (a builder skill tells whoever builds to
    # settle the artifact's NEEDS REVIEW markers first); a roled artifact's
    # builder carries that notice, its reviewer and verifiers do not.
    assert __version__ == "0.22.0"
