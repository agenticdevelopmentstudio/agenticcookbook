"""Cover every rule emitted by `core.checks.phase_a`.

Each test builds the minimal markdown that triggers one rule; we then assert
the report contains an issue for that rule (and that no unrelated rule fired
for a clean baseline)."""

from __future__ import annotations

from pathlib import Path

import pytest

from cookbook.core.checks import phase_a


GOOD_FRONTMATTER = """\
---
id: 11111111-2222-3333-4444-555555555555
title: T
domain: agenticdevelopercookbook://cookbook/recipes/r
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


def test_domain_mismatch(tmp_path):
    body = GOOD_FRONTMATTER.replace(
        "domain: agenticdevelopercookbook://cookbook/recipes/r",
        "domain: agenticdevelopercookbook://cookbook/recipes/wrong",
    )
    root = _cookbook_with(tmp_path, "r.md", body)
    report = phase_a(root)
    rules = {i.rule for i in report.issues}
    assert "domain-matches-path" in rules


def test_broken_link(tmp_path):
    root = _cookbook_with(
        tmp_path,
        "r.md",
        GOOD_FRONTMATTER.replace("Body.", "See [missing](./does-not-exist.md)."),
    )
    report = phase_a(root)
    rules = {i.rule for i in report.issues}
    assert "link-resolves" in rules


def test_external_links_ignored(tmp_path):
    body = GOOD_FRONTMATTER.replace(
        "Body.",
        "Links: [a](https://example.com) [b](mailto:x@y) [c](agenticdevelopercookbook://x/y)"
        " [d](agenticdevelopertoolkit://recipes/button#pressed).",
    )
    root = _cookbook_with(tmp_path, "r.md", body)
    report = phase_a(root)
    assert report.ok, report.issues


def test_duplicate_id(tmp_path):
    root = tmp_path / "cookbook"
    (root / "recipes").mkdir(parents=True)
    (root / "recipes" / "a.md").write_text(
        GOOD_FRONTMATTER.replace(
            "domain: agenticdevelopercookbook://cookbook/recipes/r",
            "domain: agenticdevelopercookbook://cookbook/recipes/a",
        ),
        encoding="utf-8",
    )
    (root / "recipes" / "b.md").write_text(
        GOOD_FRONTMATTER.replace(
            "domain: agenticdevelopercookbook://cookbook/recipes/r",
            "domain: agenticdevelopercookbook://cookbook/recipes/b",
        ),
        encoding="utf-8",
    )
    report = phase_a(root)
    rules = {i.rule for i in report.issues}
    assert "id-unique" in rules


def test_fix_for_known_rule_returns_hint():
    from cookbook.core.checks import fix_for

    assert "UUID" in fix_for("id-uuid")
    assert "semver" in fix_for("version-semver").lower()


def test_fix_for_required_field_includes_field_name():
    from cookbook.core.checks import fix_for

    hint = fix_for("required-field:title")
    assert "title" in hint
    assert "cookbook update" in hint


def test_fix_for_unknown_rule_returns_empty():
    from cookbook.core.checks import fix_for

    assert fix_for("not-a-real-rule") == ""


# --- domain links and the repo's scheme (K09, B_3) -----------------------------------

def _toolkit(tmp_path: Path, body: str) -> Path:
    """An ADT-like repo: origin `agenticdevelopertoolkit`, no index.md, recipes/ at
    the top; returns recipes/ as the root, as `cookbook validate -p recipes` does."""
    import subprocess
    repo = tmp_path / "checkout"
    (repo / "recipes").mkdir(parents=True)
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "remote", "add", "origin",
                    "git@github.com:org/agenticdevelopertoolkit.git"], check=True)
    fm = GOOD_FRONTMATTER.replace(
        "domain: agenticdevelopercookbook://cookbook/recipes/r",
        "domain: agenticdevelopertoolkit://recipes/r",
    )
    (repo / "recipes" / "r.md").write_text(fm.replace("Body.", body), encoding="utf-8")
    (repo / "recipes" / "label.md").write_text(
        fm.replace("recipes/r", "recipes/label").replace("555555555555", "555555555556"),
        encoding="utf-8")
    return repo / "recipes"


def _link_issues(root: Path) -> list[str]:
    return [i.detail for i in phase_a(root).issues if i.rule == "link-resolves"]


def test_same_repo_domain_link_resolves(tmp_path):
    root = _toolkit(tmp_path, "See [label](agenticdevelopertoolkit://recipes/label#pressed).")
    assert phase_a(root).ok, phase_a(root).issues


def test_dangling_same_repo_domain_link_fails(tmp_path):
    root = _toolkit(tmp_path, "See [themed](agenticdevelopertoolkit://recipes/themed-label).")
    issues = _link_issues(root)
    assert len(issues) == 1 and "agenticdevelopertoolkit://recipes/themed-label" in issues[0]


@pytest.mark.parametrize("scheme", ["agenticdevelopercookbok", "agenticdevelopertoolkt"])
def test_near_miss_scheme_is_a_typo(tmp_path, scheme):
    root = _toolkit(tmp_path, f"See [x]({scheme}://compliance/security#secure-log-output).")
    issues = _link_issues(root)
    assert len(issues) == 1 and "did you mean" in issues[0]


def test_other_repos_and_the_cookbooks_schemes_pass(tmp_path):
    root = _toolkit(
        tmp_path,
        "See [a](agenticdevelopercookbook://compliance/security#secure-log-output) "
        "[b](temporal://docs/workers) [c](https://example.com/x).",
    )
    assert _link_issues(root) == []


def test_links_inside_code_are_examples_not_links(tmp_path):
    root = _toolkit(
        tmp_path,
        "Write `[Button](agenticdevelopertoolkit://recipes/nope)` like this.\n\n"
        "```markdown\n[Button](agenticdevelopertoolkit://recipes/nope-either)\n"
        "[rel](./nope.md)\n```\n",
    )
    assert _link_issues(root) == []


def test_domain_mismatch_names_the_expected_domain_in_this_repos_scheme(tmp_path):
    root = _toolkit(tmp_path, "Body.")
    md = root / "r.md"
    md.write_text(md.read_text().replace("recipes/r\n", "recipes/xyz\n"), encoding="utf-8")
    [issue] = [i for i in phase_a(root).issues if i.rule == "domain-matches-path"]
    assert "expected `agenticdevelopertoolkit://r`" in issue.detail


def test_domain_hint_does_not_prescribe_the_cookbooks_scheme():
    from cookbook.core.checks import fix_for
    assert "agenticdevelopercookbook" not in fix_for("domain-matches-path")
