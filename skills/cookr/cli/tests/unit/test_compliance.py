from __future__ import annotations

from cookr.core.compliance import load_checks, summary, unknown_citations


def _catalog(tmp_path):
    cat = tmp_path / "compliance"
    (cat / "artifact-formatting").mkdir(parents=True)
    (cat / "security.md").write_text("# Security\n\n### secure-storage\n\ntext\n\n### input-validation\n")
    (cat / "artifact-formatting" / "recipe-formatting.md").write_text("### has-frontmatter\n")
    (cat / "INDEX.md").write_text("### not-a-check\n")
    return cat


def test_load_checks_names_nested_files_by_directory_and_skips_index(tmp_path):
    assert load_checks(_catalog(tmp_path)) == frozenset({
        "security#secure-storage", "security#input-validation",
        "artifact-formatting#has-frontmatter",
    })


def test_missing_catalog_is_none(tmp_path):
    assert load_checks(tmp_path / "absent") is None


def test_unknown_citations_are_sorted_and_unique(tmp_path):
    checks = load_checks(_catalog(tmp_path))
    body = ("agenticdevelopercookbook://compliance/security#secure-storage "
            "agenticdevelopercookbook://compliance/security#zeta "
            "agenticdevelopercookbook://compliance/security#alpha "
            "agenticdevelopercookbook://compliance/security#zeta")
    assert unknown_citations(body, checks) == ["security#alpha", "security#zeta"]


def test_summary_groups_by_category(tmp_path):
    assert summary(load_checks(_catalog(tmp_path))) == (
        "- `artifact-formatting`: has-frontmatter\n"
        "- `security`: input-validation, secure-storage"
    )
