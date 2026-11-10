"""Guideline twins and the rule census (core/twins.py)."""

from __future__ import annotations

from cookr.core import twins
from cookr.core.artifact import Artifact, Part, dump_manifest, load_folder, save_document, write_folder

URI = "agenticdevelopercookbook://guidelines"


def make(root, use_case, rel, text, *, differs=None, informational=None):
    folder = root / "guidelines" / use_case / rel
    write_folder(Artifact(meta={"id": f"{use_case}-{rel}", "type": "guideline"}, parts=[
        Part("intro", f"# T\n\n{text}\n"),
        Part("history", f"| 1.0.0 | {use_case} |\n", "Change History"),
    ], twin_differs=differs, informational=informational), folder)
    return folder


def drift(*folders):
    return sorted((f.key, f.kind, tuple(sorted(p.parent.name for p in f.folders)))
                  for f in twins.twin_census(folders))


# ── twins ────────────────────────────────────────────────────────────────────

def test_identical_twins_pass_even_with_their_own_history(tmp_path):
    a = make(tmp_path, "implementing", "logging", "Logs MUST be JSON.")
    b = make(tmp_path, "reviewing", "logging", "Logs MUST be JSON.")
    assert drift(a, b) == []


def test_a_link_to_the_twins_own_use_case_is_not_drift(tmp_path):
    a = make(tmp_path, "implementing", "x", f"See [t]({URI}/implementing/ui/targets).")
    b = make(tmp_path, "reviewing", "x", f"See [t]({URI}/reviewing/ui/targets).")
    assert drift(a, b) == []


def test_a_uuid_link_to_the_twins_own_use_case_is_not_drift(tmp_path):
    a = make(tmp_path, "implementing", "x",
             "See [adc.guideline.implementing.ui.targets](cookbook:1111).")
    b = make(tmp_path, "reviewing", "x",
             "See [adc.guideline.reviewing.ui.targets](cookbook:2222).")
    assert drift(a, b) == []


def test_a_uuid_link_to_a_different_guideline_drifts(tmp_path):
    a = make(tmp_path, "implementing", "x",
             "See [adc.guideline.implementing.ui.targets](cookbook:1111).")
    b = make(tmp_path, "reviewing", "x",
             "See [adc.guideline.reviewing.ui.color](cookbook:2222).")
    assert drift(a, b) == [("x", "drift", ("implementing", "reviewing"))]


def test_twins_that_differ_without_a_reason_drift(tmp_path):
    a = make(tmp_path, "implementing", "logging", "Logs MUST be JSON.")
    b = make(tmp_path, "reviewing", "logging", "Logs SHOULD be JSON.")
    assert drift(a, b) == [("logging", "drift", ("implementing", "reviewing"))]


def test_a_reason_lets_a_twin_differ(tmp_path):
    a = make(tmp_path, "implementing", "logging", "Logs MUST be JSON.")
    b = make(tmp_path, "reviewing", "logging", "- Flag logs that are not JSON.",
             differs="A review checklist of the implementing guideline.")
    assert drift(a, b) == []


def test_unexplained_twins_must_still_agree_with_each_other(tmp_path):
    a = make(tmp_path, "implementing", "x", "A MUST.")
    b = make(tmp_path, "testing", "x", "A MUST NOT.")
    c = make(tmp_path, "reviewing", "x", "Checklist.", differs="A review checklist of the guideline.")
    assert drift(a, b, c) == [("x", "drift", ("implementing", "testing"))]


def test_a_reason_on_a_twin_that_matches_is_stale(tmp_path):
    a = make(tmp_path, "implementing", "x", "Same.")
    b = make(tmp_path, "reviewing", "x", "Same.", differs="A review checklist of the guideline.")
    assert drift(a, b) == [("x", "stale", ("reviewing",))]


def test_a_short_reason_is_flagged(tmp_path):
    a = make(tmp_path, "implementing", "x", "One.")
    b = make(tmp_path, "reviewing", "x", "Two.", differs="checklist")
    assert drift(a, b) == [("x", "short", ("reviewing",))]


def test_a_guideline_with_no_twin_is_not_checked(tmp_path):
    assert drift(make(tmp_path, "implementing", "solo", "Anything.",
                      differs="A reason with nothing to differ from.")) == []


def test_non_guidelines_are_ignored(tmp_path):
    folder = tmp_path / "recipes" / "implementing" / "x"
    write_folder(Artifact(meta={"id": "r", "type": "recipe"}, parts=[Part("intro", "# R\n")]), folder)
    assert drift(folder, make(tmp_path, "implementing", "x", "Text.")) == []


# ── rules ────────────────────────────────────────────────────────────────────

def rules(*folders):
    return sorted((f.folder.name, f.kind) for f in twins.rule_census(folders))


def test_a_guideline_stating_a_rule_passes(tmp_path):
    assert rules(make(tmp_path, "implementing", "a", "Code **MUST** compile.")) == []


def test_a_guideline_with_no_rule_is_flagged(tmp_path):
    assert rules(make(tmp_path, "implementing", "a", "Code compiles, usually.")) == [("a", "no-rules")]


def test_keywords_in_code_lowercase_or_history_do_not_count(tmp_path):
    folder = make(tmp_path, "implementing", "a", "It must work.\n\n```\nMUST\n```")
    assert rules(folder) == [("a", "no-rules")]


def test_an_informational_reason_exempts_it(tmp_path):
    assert rules(make(tmp_path, "implementing", "a", "Background reading.",
                      informational="A reading list of external references.")) == []


def test_an_informational_reason_on_a_guideline_with_rules_is_stale(tmp_path):
    assert rules(make(tmp_path, "implementing", "a", "It MUST work.",
                      informational="A reading list of external references.")) == [("a", "stale")]


# ── the artifact.json fields ─────────────────────────────────────────────────

def test_reasons_round_trip_and_survive_a_doc_edit(tmp_path):
    folder = make(tmp_path, "reviewing", "x", "Two.", differs="A review checklist of it.",
                  informational="A checklist with no rules of its own.")
    text = dump_manifest(load_folder(folder))
    assert '"twin_differs"' in text and '"informational"' in text
    save_document(folder.parent / "x.md", "---\nid: x\ntype: guideline\n---\n# T\n\nEdited.\n")
    loaded = load_folder(folder)
    assert loaded.twin_differs == "A review checklist of it."
    assert loaded.informational == "A checklist with no rules of its own."


def test_no_reason_writes_no_key(tmp_path):
    text = dump_manifest(load_folder(make(tmp_path, "implementing", "x", "Plain.")))
    assert "twin_differs" not in text and "informational" not in text
