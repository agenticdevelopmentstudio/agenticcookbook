"""Cover every rule emitted by `core.checks.phase_a`.

Each test builds the minimal markdown that triggers one rule; we then assert
the report contains an issue for that rule (and that no unrelated rule fired
for a clean baseline)."""

from __future__ import annotations

from pathlib import Path

import pytest

from cookr.core.checks import phase_a


# Every tmp_path here is a git repo, as a real cookbook checkout is.
pytestmark = pytest.mark.usefixtures("git_tmp_path")


GOOD_FRONTMATTER = """\
---
id: 11111111-2222-3333-4444-555555555555
title: T
type: recipe
version: 1.0.0
status: draft
language: en
created: 2026-05-15
modified: 2026-05-15
author: T
copyright: 2026 T
license: MIT
summary: x
---
# T

Body.
"""


def _cookbook_with(tmp_path: Path, name: str, body: str) -> Path:
    root = tmp_path / "cookbook"
    (root / "recipes").mkdir(parents=True)
    (root / "recipes" / name).write_text(body, encoding="utf-8")
    return root


def test_clean_baseline_passes(tmp_path):
    root = _cookbook_with(tmp_path, "r.md", GOOD_FRONTMATTER)
    report = phase_a(root)
    assert report.ok, report.issues


def test_no_format_2_manifest_warns_once_that_links_went_unchecked(tmp_path):
    body = GOOD_FRONTMATTER.replace("Body.", "See [a](cookbook:0b0b0b0b-0000-4000-8000-000000000000) "
                                             "and [b](cookbook:0c0c0c0c-0000-4000-8000-000000000000).")
    root = _cookbook_with(tmp_path, "r.md", body)
    report = phase_a(root)
    assert report.ok, report.issues
    [warning] = report.warnings
    assert warning.rule == "links-unchecked"
    assert warning.file == "cookbook/cookbook.json"
    assert "UUID links and index implementations were not checked" in warning.detail


def test_missing_frontmatter(tmp_path):
    root = _cookbook_with(tmp_path, "r.md", "# Just a header\n")
    report = phase_a(root)
    rules = {i.rule for i in report.issues}
    assert "frontmatter-present" in rules


def test_missing_required_field(tmp_path):
    body = GOOD_FRONTMATTER.replace("license: MIT\n", "")
    root = _cookbook_with(tmp_path, "r.md", body)
    report = phase_a(root)
    rules = {i.rule for i in report.issues}
    assert "required-field:license" in rules


def test_bad_uuid(tmp_path):
    body = GOOD_FRONTMATTER.replace(
        "id: 11111111-2222-3333-4444-555555555555",
        "id: not-a-uuid",
    )
    root = _cookbook_with(tmp_path, "r.md", body)
    report = phase_a(root)
    rules = {i.rule for i in report.issues}
    assert "id-uuid" in rules


def test_bad_semver(tmp_path):
    body = GOOD_FRONTMATTER.replace("version: 1.0.0", "version: v1.x")
    root = _cookbook_with(tmp_path, "r.md", body)
    report = phase_a(root)
    rules = {i.rule for i in report.issues}
    assert "version-semver" in rules


def test_bad_type(tmp_path):
    body = GOOD_FRONTMATTER.replace("type: recipe", "type: bogus")
    root = _cookbook_with(tmp_path, "r.md", body)
    report = phase_a(root)
    rules = {i.rule for i in report.issues}
    assert "type-valid" in rules


def test_bad_status(tmp_path):
    body = GOOD_FRONTMATTER.replace("status: draft", "status: rejected")
    root = _cookbook_with(tmp_path, "r.md", body)
    report = phase_a(root)
    rules = {i.rule for i in report.issues}
    assert "status-valid" in rules


def test_broken_link(tmp_path):
    root = _cookbook_with(
        tmp_path,
        "r.md",
        GOOD_FRONTMATTER.replace("Body.", "See [missing](./does-not-exist.md)."),
    )
    report = phase_a(root)
    rules = {i.rule for i in report.issues}
    assert "link-resolves" in rules


def test_web_and_mail_links_pass(tmp_path):
    body = GOOD_FRONTMATTER.replace("Body.", "Links: [a](https://example.com) [b](mailto:x@y).")
    root = _cookbook_with(tmp_path, "r.md", body)
    report = phase_a(root)
    assert report.ok, report.issues


@pytest.mark.parametrize("link", ["agenticdevelopercookbook://x/y", "adhsdk://recipes/button#pressed"])
def test_format_1_domain_links_are_link_format_issues(tmp_path, link):
    body = GOOD_FRONTMATTER.replace("Body.", f"See [x]({link}).")
    root = _cookbook_with(tmp_path, "r.md", body)
    [issue] = phase_a(root).issues
    assert issue.rule == "link-format" and link.split("#")[0] in issue.detail


def test_duplicate_id(tmp_path):
    root = tmp_path / "cookbook"
    (root / "recipes").mkdir(parents=True)
    (root / "recipes" / "a.md").write_text(GOOD_FRONTMATTER, encoding="utf-8")
    (root / "recipes" / "b.md").write_text(GOOD_FRONTMATTER, encoding="utf-8")
    report = phase_a(root)
    rules = {i.rule for i in report.issues}
    assert "id-unique" in rules


def test_fix_for_known_rule_returns_hint():
    from cookr.core.checks import fix_for

    assert "UUID" in fix_for("id-uuid")
    assert "semver" in fix_for("version-semver").lower()


def test_fix_for_required_field_includes_field_name():
    from cookr.core.checks import fix_for

    hint = fix_for("required-field:title")
    assert "title" in hint
    assert "cookr update" in hint


def test_fix_for_unknown_rule_returns_empty():
    from cookr.core.checks import fix_for

    assert fix_for("not-a-real-rule") == ""


# --- UUID links resolve through the index ---------------------------------------------

FULL_META = {
    "title": "T", "version": "1.0.0", "language": "en", "created": "2026-05-15",
    "modified": "2026-05-15", "author": "T", "copyright": "2026 T", "license": "MIT",
    "summary": "x",
}
GONE = "0b0b0b0b-0000-4000-8000-000000000000"
ELSEWHERE = "0e0e0e0e-0000-4000-8000-000000000000"


def _repo(tmp_path: Path, body: str = "# T\n\nBody.\n", meta=None, impls=(), roots=()):
    """A format-2 repo holding recipes/r (with `body`) and recipes/label;
    returns its cookbook dir and label's id."""
    from .cookbook_helpers import add_spec, new_repo
    new_repo(tmp_path, roots)
    label = add_spec(tmp_path, "recipes/label", type="recipe", meta=FULL_META)
    add_spec(tmp_path, "recipes/r", type="recipe", body=body.replace("LABEL", label),
             meta={**FULL_META, **(meta or {})}, impls=impls)
    return tmp_path / "cookbook", label


def _rules(report, prefix: str) -> list[tuple[str, str]]:
    return [(i.rule, i.detail) for i in report.issues if i.rule.startswith(prefix)]


def test_format_2_baseline_passes(tmp_path):
    root, _ = _repo(tmp_path, "# T\n\nSee [label](cookbook:LABEL).\n")
    report = phase_a(root)
    assert report.ok and not report.warnings, (report.issues, report.warnings)


def test_depends_on_a_local_uuid_resolves(tmp_path):
    from .cookbook_helpers import add_spec, new_repo
    new_repo(tmp_path)
    label = add_spec(tmp_path, "recipes/label", type="recipe", meta=FULL_META)
    add_spec(tmp_path, "recipes/r", type="recipe", meta={**FULL_META, "depends-on": [label]})
    report = phase_a(tmp_path / "cookbook")
    assert report.ok, report.issues


def test_missing_link_is_an_issue(tmp_path):
    root, _ = _repo(tmp_path, f"# T\n\nSee [gone](cookbook:{GONE}).\n")
    [(rule, detail)] = _rules(phase_a(root), "link")
    assert rule == "link-resolves" and "names no artifact in its cookbook" in detail


def test_missing_depends_on_entry_is_an_issue(tmp_path):
    root, _ = _repo(tmp_path, meta={"depends-on": [GONE]})
    [(rule, detail)] = _rules(phase_a(root), "link")
    assert rule == "link-resolves" and detail.startswith("`depends-on` entry")


def test_depends_on_entry_that_is_not_a_uuid_is_an_issue(tmp_path):
    root, _ = _repo(tmp_path, meta={"related": ["recipes/label"]})
    [(rule, detail)] = _rules(phase_a(root), "link")
    assert rule == "link-resolves" and "is not a UUID link" in detail


def test_link_into_an_unreachable_cookbook_is_a_warning(tmp_path):
    from .cookbook_helpers import edit_repo_config
    root, _ = _repo(tmp_path, f"# T\n\nSee [far](cookbook:{ELSEWHERE}/{GONE}).\n")
    edit_repo_config(tmp_path, lambda d: d.update(dependencies={ELSEWHERE: {"rdid": "far"}}))
    report = phase_a(root)
    assert report.ok, report.issues
    [warning] = report.warnings
    assert warning.rule == "link-resolves" and f"cookbook {ELSEWHERE} cannot be reached here" in warning.detail


def test_links_inside_code_are_examples_not_links(tmp_path):
    root, _ = _repo(
        tmp_path,
        f"# T\n\nWrite `[Button](cookbook:{GONE})` like this.\n\n"
        f"```markdown\n[Button](cookbook:{GONE})\n[rel](./nope.md)\n```\n",
    )
    assert _rules(phase_a(root), "link") == []


# --- index implementations -------------------------------------------------------------

def _impl_rules(root: Path) -> list[tuple[str, str]]:
    return _rules(phase_a(root), "reference-implementation")


def test_implementations_resolve_from_the_repo_top(tmp_path):
    (tmp_path / "Sources/Kit").mkdir(parents=True)
    (tmp_path / "Sources/Kit/Label.swift").write_text("", encoding="utf-8")
    (tmp_path / "packages/kit/label").mkdir(parents=True)
    root, _ = _repo(tmp_path, impls=[("apple", "Sources/Kit/Label.swift"),
                                     ("web", "packages/kit/label/")])
    assert _impl_rules(root) == []


def test_missing_implementation_location_is_reported(tmp_path):
    root, _ = _repo(tmp_path, impls=[("apple", "Sources/Kit/Label.swift")])
    assert _impl_rules(root) == [("reference-implementation-exists",
                                  "implementation location `Sources/Kit/Label.swift` does not exist")]


def test_url_and_planned_implementations_are_not_looked_for(tmp_path):
    root, _ = _repo(tmp_path, impls=[("web", "https://example.com/kit/label"),
                                     ("android", "app/Label.kt", "planned"),
                                     ("ios", None, "planned")])
    assert _impl_rules(root) == []


def test_unknown_implementation_platform_is_reported(tmp_path):
    (tmp_path / "x.swift").write_text("", encoding="utf-8")
    root, _ = _repo(tmp_path, impls=[("visionos", "x.swift")])
    [(rule, detail)] = _impl_rules(root)
    assert rule == "reference-implementation-platform" and "`visionos`" in detail
