from __future__ import annotations

from cookr.core.compliance import (
    check_links, cited_checks, citations, load_checks, unknown_citations,
)
from cookr.core.identity import CookbookIdentity, check_uuid
from cookr.core.index import Entry, Index
from cookr.core.links import Resolver

OWN = "c0000000-0000-4000-8000-000000000000"
FAR = "f0000000-0000-4000-8000-000000000000"
SPEC = "a0000000-0000-4000-8000-000000000001"


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


def _check(document, name):
    uid = check_uuid(OWN, document, name)
    rdid = f"t.check.{document.replace('/', '.')}.{name}"
    return Entry(id=uid, kind="check", rdid=rdid, path=f"{document}#{name}")


def _index():
    entries = [_check("security", "secure-storage"), _check("security", "input-validation"),
               Entry(id=SPEC, kind="ingredient", rdid="t.ingredient.button", path="button")]
    return Index(cookbook=CookbookIdentity(id=OWN, rdid="t"), entries={e.id: e for e in entries})


def _resolver(tmp_path):
    return Resolver(tmp_path, _index(), {})


def _cite(label, artifact, cookbook=OWN):
    return f"[{label}](cookbook:{cookbook}/{artifact})"


def test_load_checks_keys_by_document_path_and_skips_non_content_files(tmp_path):
    assert load_checks(_catalog(tmp_path)) == frozenset({
        "security#secure-storage", "security#input-validation",
        "artifact-formatting/recipe-formatting#has-frontmatter",
    })


def test_missing_catalog_is_none(tmp_path):
    assert load_checks(tmp_path / "absent") is None


def test_citations_are_in_text_links_with_a_check_label():
    text = (_cite("t.check.security.secure-storage", check_uuid(OWN, "security", "secure-storage"))
            + " " + _cite("t.ingredient.button", SPEC))
    assert [label for label, _ in citations(text)] == ["t.check.security.secure-storage"]


def test_unknown_citations_report_missing_links_and_links_to_non_checks(tmp_path):
    ghost = "00000000-0000-4000-8000-000000000000"
    text = " ".join([
        _cite("t.check.security.secure-storage", check_uuid(OWN, "security", "secure-storage")),
        _cite("t.check.security.zeta", ghost),
        _cite("t.check.security.alpha", SPEC),
        _cite("t.check.security.zeta", ghost),
    ])
    assert unknown_citations(text, _resolver(tmp_path)) == [
        f"t.check.security.alpha ({OWN}/{SPEC})",
        f"t.check.security.zeta ({OWN}/{ghost})",
    ]


def test_a_citation_into_an_unreachable_cookbook_is_not_judged(tmp_path):
    text = _cite("far.check.security.whatever", SPEC, cookbook=FAR)
    assert unknown_citations(text, _resolver(tmp_path)) == []


def test_cited_checks_use_the_entry_path_else_the_label(tmp_path):
    text = (_cite("t.check.renamed.label", check_uuid(OWN, "security", "input-validation"))
            + " " + _cite("far.check.artifact-formatting.recipe-formatting.has-frontmatter",
                          SPEC, cookbook=FAR))
    assert cited_checks(text, _resolver(tmp_path)) == {
        "security#input-validation",
        "artifact-formatting/recipe-formatting#has-frontmatter",
    }


def test_check_links_list_every_check_by_rdid():
    assert check_links(_index()) == [
        _cite("t.check.security.input-validation", check_uuid(OWN, "security", "input-validation")),
        _cite("t.check.security.secure-storage", check_uuid(OWN, "security", "secure-storage")),
    ]
