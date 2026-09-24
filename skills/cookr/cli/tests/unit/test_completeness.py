from __future__ import annotations

import pytest

from cookr.core.completeness import problems
from cookr.core.recipes import load_corpus


def test_complete_recipe_has_no_problems(mini_repo):
    corpus = load_corpus(mini_repo / "recipes")
    assert problems(corpus["button"]) == []


def test_draft_status_is_a_problem(mini_repo):
    corpus = load_corpus(mini_repo / "recipes")
    assert any("status" in p for p in problems(corpus["stat-card"]))


def test_needs_review_marker_is_a_problem(mini_repo):
    corpus = load_corpus(mini_repo / "recipes")
    assert any("NEEDS REVIEW" in p for p in problems(corpus["stat-card"]))


def test_empty_winui_note_is_a_problem(mini_repo):
    corpus = load_corpus(mini_repo / "recipes")
    assert any("WinUI 3" in p for p in problems(corpus["chat-composer"]))


def test_missing_section_is_a_problem(mini_repo):
    p = mini_repo / "recipes" / "button.md"
    text = p.read_text(encoding="utf-8")
    start = text.index("## States")
    end = text.index("## Accessibility")
    p.write_text(text[:start] + text[end:], encoding="utf-8")
    corpus = load_corpus(mini_repo / "recipes")
    assert any("States" in q for q in problems(corpus["button"]))


def test_empty_section_is_a_problem(mini_repo):
    p = mini_repo / "recipes" / "button.md"
    text = p.read_text(encoding="utf-8")
    start = text.index("## States") + len("## States")
    end = text.index("## Accessibility")
    p.write_text(text[:start] + "\n\n" + text[end:], encoding="utf-8")
    corpus = load_corpus(mini_repo / "recipes")
    assert any("States" in q for q in problems(corpus["button"]))


def test_recipe_type_uses_recipe_sections(mini_repo):
    corpus = load_corpus(mini_repo / "recipes")
    assert problems(corpus["site-menu"]) == []


def test_unknown_type_is_a_problem_and_grades_as_ingredient(mini_repo):
    p = mini_repo / "recipes" / "button.md"
    p.write_text(
        p.read_text(encoding="utf-8").replace("type: ingredient", "type: guidline", 1),
        encoding="utf-8",
    )
    found = problems(load_corpus(mini_repo / "recipes")["button"])
    # The only complaint is the type itself: the ingredient sections it already
    # satisfies are still the list it is graded against.
    assert found == ["unknown type `guidline`"]


def _set_winui_line(mini_repo, line):
    p = mini_repo / "recipes" / "button.md"
    text = p.read_text(encoding="utf-8")
    old = "- **WinUI 3**: `Microsoft.UI.Xaml.Controls.Button` with the `AccentButtonStyle` resource."
    assert old in text
    p.write_text(text.replace(old, line), encoding="utf-8")
    return load_corpus(mini_repo / "recipes")["button"]


@pytest.mark.parametrize(
    "line",
    [
        "- **WinUI 3** (Windows): Use `ProgressRing`.",
        "- **WinUI 3 / C#**: Use `ProgressRing`.",
        "- **Windows / WinUI 3:** Use `ProgressRing`.",
        "- **WinUI 3 (C#)**: Use `ProgressRing`.",
    ],
)
def test_decorated_winui_label_counts_as_filled(mini_repo, line):
    assert problems(_set_winui_line(mini_repo, line)) == []


def test_decorated_winui_label_with_no_text_is_empty(mini_repo):
    info = _set_winui_line(mini_repo, "- **WinUI 3** (Windows):")
    assert any("no filled `WinUI 3`" in p for p in problems(info))


def test_not_applicable_winui_note_is_a_problem(mini_repo):
    info = _set_winui_line(mini_repo, "- **WinUI 3**: Not applicable — web-only component.")
    assert any("not applicable" in p for p in problems(info))


def test_combined_platform_bullet_saying_not_applicable_is_a_problem(mini_repo):
    info = _set_winui_line(
        mini_repo, "- **SwiftUI, Compose, AppKit/UIKit, WinUI 3**: Not applicable — web-only."
    )
    assert any("not applicable" in p for p in problems(info))


def test_marker_phrase_in_change_history_is_not_a_problem(mini_repo):
    # A changelog row that records removing the marker is a record of the
    # fix, not a gap.
    p = mini_repo / "recipes" / "button.md"
    p.write_text(
        p.read_text(encoding="utf-8").rstrip() + "\n\n## Change History\n\n"
        "| Date | Change |\n|---|---|\n| 2026-09-22 | Removed the NEEDS REVIEW marker from Accessibility. |\n",
        encoding="utf-8",
    )
    assert problems(load_corpus(mini_repo / "recipes")["button"]) == []


def test_marker_outside_change_history_still_a_problem_when_history_present(mini_repo):
    p = mini_repo / "recipes" / "button.md"
    text = p.read_text(encoding="utf-8")
    text = text.replace("## States", "## States\n\nNEEDS REVIEW: which states matter?\n", 1)
    p.write_text(
        text.rstrip() + "\n\n## Change History\n\n| 2026-09-22 | Removed a NEEDS REVIEW marker. |\n",
        encoding="utf-8",
    )
    assert any("NEEDS REVIEW" in q for q in problems(load_corpus(mini_repo / "recipes")["button"]))


def _append(mini_repo, text, checks=None):
    p = mini_repo / "recipes" / "button.md"
    p.write_text(p.read_text(encoding="utf-8").rstrip() + "\n\n" + text + "\n", encoding="utf-8")
    return problems(load_corpus(mini_repo / "recipes")["button"], checks)


def test_marker_on_a_named_one_line_bullet_is_only_the_marker_problem(mini_repo):
    found = _append(mini_repo, "## Edge Cases 2\n\n"
                    "- **empty-label**: NEEDS REVIEW: Not implemented in source. No empty-label rule.")
    assert found == ["body carries a `NEEDS REVIEW` marker"]


@pytest.mark.parametrize("text", [
    "NEEDS REVIEW: Not implemented in source. A standalone paragraph.",
    "- **empty-label**: **NEEDS REVIEW**: which label?",
    "- **empty-label**: NEEDS REVIEW: Not implemented in\n  source. Wrapped mid-phrase.",
])
def test_malformed_marker_is_a_problem(mini_repo, text):
    assert any("one-line" in q for q in _append(mini_repo, "## Notes\n\n" + text))


def test_marker_in_compliance_is_a_problem(mini_repo):
    found = _append(mini_repo, "## Compliance\n\n"
                    "- **gap**: NEEDS REVIEW: Not implemented in source. Contrast unknown.")
    assert any("Compliance carries" in q for q in found)


def test_rfc_word_prefixed_requirement_name_is_a_problem(mini_repo):
    found = _append(mini_repo, "## More\n\n- **may-accept-class**: The button MAY accept a class.")
    assert any("RFC 2119" in q for q in found)


@pytest.mark.parametrize("text", [
    "The default comes from the initializer (line 42).",
    "Derived from source lines 10-20.",
    "See `Store.swift` behaviour at Store.swift:88.",
])
def test_source_line_citation_is_a_problem(mini_repo, text):
    assert any("line numbers" in q for q in _append(mini_repo, "## More\n\n" + text))


@pytest.mark.parametrize("text", [
    "| v-1 | split | `'body line 1\\nbody line 2'` | two lines |",
    "Line 1 shows the prompt; line 2 shows the listing.",
])
def test_line_words_in_data_are_not_a_citation(mini_repo, text):
    assert _append(mini_repo, "## More\n\n" + text) == []


def test_unknown_compliance_check_is_a_problem_when_catalog_given(mini_repo):
    text = ("## Compliance\n\n| Check | Status | Category |\n|---|---|---|\n"
            "| [unit-test-coverage](agenticdevelopercookbook://compliance/best-practices#unit-test-coverage)"
            " | passed | best-practices |\n"
            "| [transport-security](agenticdevelopercookbook://compliance/security#transport-security)"
            " | passed | security |")
    found = _append(mini_repo, text, checks=frozenset({"best-practices#unit-test-coverage"}))
    assert found == ["cites compliance checks not in the catalog: security#transport-security"]


def test_compliance_citations_unchecked_without_a_catalog(mini_repo):
    text = "[x](agenticdevelopercookbook://compliance/security#transport-security)"
    assert _append(mini_repo, "## More\n\n" + text) == []
