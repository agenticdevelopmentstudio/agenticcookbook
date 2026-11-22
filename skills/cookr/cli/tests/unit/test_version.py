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
    # builder carries that notice, its reviewer and verifiers do not. A
    # cookbook with research-exempt.json is research-first: every artifact
    # it does not list needs research/ (the 21-topic pin is gone).
    # 0.22.1: `roles lossless` reads a renamed topic's base at the path its
    # lossless.json names in "renamed_from" (gone now, same artifact id), and a
    # same-named folder renamed away (its id still live) is no twin to list.
    # 0.22.2: a twin carrying the topic's own id was folded into it, not
    # renamed away: `roles lossless` asks it to be listed.
    # 0.23.0: a roled artifact's reviewer and verifiers route under their own use
    # case with the artifact's below it (coding/reviewing/planning/data; a
    # principle's coding/reviewing/principles), so the whole cookbook stays
    # under FANOUT_CAP once every topic is roled.
    # 0.23.1: roles lossless: a topic moved to another use case under the same folder name is no longer reported as its own unread twin.
    # 0.23.2: roles lossless: a renamed topic's twin check also matches folders named after its old name.
    # 0.23.3: roles lossless: a renamed_from for another base is ignored, so the base mismatch is reported instead of raised.
    # 0.23.4: roles lossless measures a sentence without its links to its own topic
    # 0.23.5: validate --research takes a new topic's folder holding only research/
    # 0.23.6: a citation written in code is never cited
    # 0.23.7: a code span inside a citation comes back readable, never NUL bytes
    # 0.23.8: validate --research refuses a folder holding parts but no artifact.json
    assert __version__ == "0.23.8"
