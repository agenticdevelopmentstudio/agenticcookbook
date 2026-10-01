from datetime import date
from pathlib import Path

from cookbook.core.frontmatter import (
    REQUIRED_FIELDS,
    SEMVER_RE,
    UUID_RE,
    dump,
    fill_defaults,
    parse,
)


SAMPLE = """---
id: 11111111-2222-3333-4444-555555555555
title: Sample
version: 1.2.3
---
# Body

Some content.
"""


def test_parse_roundtrip():
    fm = parse(SAMPLE)
    assert fm.had_frontmatter
    assert fm.data["title"] == "Sample"
    rebuilt = dump(fm)
    assert rebuilt.startswith("---\n")
    assert "# Body" in rebuilt


def test_parse_no_frontmatter():
    fm = parse("# Just a body\n")
    assert not fm.had_frontmatter
    assert fm.data == {}
    assert fm.body == "# Just a body\n"


def test_fill_defaults_inserts_required():
    fm = parse("# Bare\n")
    new_fm, added = fill_defaults(
        fm, rel_path=Path("recipes/foo.md"), cookbook_name="testcb", scheme="myrepo",
        author="Tester", today=date(2026, 5, 15),
    )
    for f in REQUIRED_FIELDS:
        assert f in new_fm.data, f"missing {f}"
    assert UUID_RE.match(new_fm.data["id"])
    assert SEMVER_RE.match(new_fm.data["version"])
    assert new_fm.data["type"] == "recipe"
    assert new_fm.data["title"] == "Bare"
    assert new_fm.data["domain"] == "myrepo://testcb/recipes/foo"
    assert "id" in added


def test_fill_defaults_preserves_existing():
    fm = parse("---\nid: 11111111-2222-3333-4444-555555555555\ntitle: Keep\n---\n# Body\n")
    new_fm, added = fill_defaults(
        fm, rel_path=Path("recipes/x.md"), cookbook_name="testcb",
        scheme=lambda: "myrepo", author="Tester", today=date(2026, 5, 15),
    )
    assert new_fm.data["id"] == "11111111-2222-3333-4444-555555555555"
    assert new_fm.data["title"] == "Keep"
    assert "id" not in added and "title" not in added
    assert "version" in added  # was missing


def test_fill_defaults_derives_the_scheme_only_for_a_missing_domain():
    def boom() -> str:
        raise AssertionError("scheme derived although `domain` is set")

    fm = parse("---\ndomain: other://recipes/x\n---\n# Body\n")
    new_fm, added = fill_defaults(
        fm, rel_path=Path("recipes/x.md"), cookbook_name="testcb", scheme=boom,
        author="Tester", today=date(2026, 5, 15),
    )
    assert new_fm.data["domain"] == "other://recipes/x"
    assert "domain" not in added
