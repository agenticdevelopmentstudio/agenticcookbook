from __future__ import annotations

from cookr.core.compliance import load_checks, summary, unknown_citations


def _catalog(tmp_path):
    cat = tmp_path / "compliance"
    (cat / "artifact-formatting").mkdir(parents=True)
    (cat / "security.md").write_text("# Security\n\n### secure-storage\n\ntext\n\n### input-validation\n")
    (cat / "artifact-formatting" / "recipe-formatting.md").write_text("### has-frontmatter\n")
    # Files no cookbook walk counts as content never define checks.
    (cat / "INDEX.md").write_text("### not-a-check\n")
    (cat / "artifact-formatting" / "index.md").write_text("### not-a-check\n")
    (cat / "_template.md").write_text("### check-name\n")
    (cat / "references.md").write_text("### not-a-check\n")
    return cat


def test_load_checks_keys_by_document_path_and_skips_non_content_files(tmp_path):
    assert load_checks(_catalog(tmp_path)) == frozenset({
        "security#secure-storage", "security#input-validation",
        "artifact-formatting/recipe-formatting#has-frontmatter",
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


def test_nested_citations_are_checked_and_the_directory_form_names_no_document(tmp_path):
    checks = load_checks(_catalog(tmp_path))
    body = ("agenticdevelopercookbook://compliance/artifact-formatting/recipe-formatting#has-frontmatter "
            "agenticdevelopercookbook://compliance/artifact-formatting/recipe-formatting#has-frontmatter-typo "
            "agenticdevelopercookbook://compliance/artifact-formatting#has-frontmatter")
    assert unknown_citations(body, checks) == [
        "artifact-formatting#has-frontmatter",
        "artifact-formatting/recipe-formatting#has-frontmatter-typo",
    ]


def test_summary_groups_by_document(tmp_path):
    assert summary(load_checks(_catalog(tmp_path))) == (
        "- `artifact-formatting/recipe-formatting`: has-frontmatter\n"
        "- `security`: input-validation, secure-storage"
    )
