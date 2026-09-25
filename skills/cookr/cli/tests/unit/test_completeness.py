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


def _edit(mini_repo, old, new, slug="button"):
    p = mini_repo / "recipes" / f"{slug}.md"
    text = p.read_text(encoding="utf-8")
    assert old in text, old
    p.write_text(text.replace(old, new, 1), encoding="utf-8")
    return load_corpus(mini_repo / "recipes")[slug]


NEWEST_ROW = "| 1.1.0 | 2026-09-20 | Fixture Author | Filled every template section |"


def test_marker_phrase_in_change_history_is_not_a_problem(mini_repo):
    # A changelog row that records removing the marker is a record of the
    # fix, not a gap.
    info = _edit(mini_repo, NEWEST_ROW,
                 "| 1.1.0 | 2026-09-20 | Fixture Author | Removed the NEEDS REVIEW marker |")
    assert problems(info) == []


def test_marker_outside_change_history_still_a_problem_when_history_present(mini_repo):
    info = _edit(mini_repo, "## States", "## States\n\nNEEDS REVIEW: which states matter?\n")
    assert any("NEEDS REVIEW" in q for q in problems(info))


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
    info = _edit(mini_repo, "The button keeps rendering",
                 "- **gap**: NEEDS REVIEW: Not implemented in source. Contrast unknown.\n\n"
                 "The button keeps rendering")
    assert any("Compliance carries" in q for q in problems(info))


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
    info = _edit(mini_repo, "The button keeps rendering",
                 "[transport-security](agenticdevelopercookbook://compliance/security#transport-security)"
                 "\n\nThe button keeps rendering")
    catalog = frozenset({"best-practices#unit-test-coverage", "best-practices#separation-of-concerns"})
    assert problems(info, catalog) == [
        "cites compliance checks not in the catalog: security#transport-security"]


def test_compliance_citations_unchecked_without_a_catalog(mini_repo):
    text = "[x](agenticdevelopercookbook://compliance/security#transport-security)"
    assert _append(mini_repo, "## More\n\n" + text) == []


# --- A-cookr_6 / D_5: line citations need a sign they point at source ---------

@pytest.mark.parametrize("text", [
    "| x-1 | caret-reset | Enter at end of block | caret at line 1 of the new block |",
    "- **line-numbers**: The gutter shows numbers starting on line 1.",
    "The reply wraps (line 2 of the bubble) when long.",
    "| v-2 | goto | `:50` | cursor at line 50 |",
    "The build pipeline 12 stage and outline 30 view are unrelated.",
])
def test_behavioral_line_positions_are_not_citations(mini_repo, text):
    assert _append(mini_repo, "## More\n\n" + text) == []


@pytest.mark.parametrize("text", [
    "Traced to `Store.swift:88`.",
    "defined at `cascade-rules.ts:441`",
    "`avatar.tsx:7-9` documents why the class names must stay stable.",
    "see button.tsx line 42",
    "Store.swift, line 88 sets the default.",
    "The guard is at (line 920, Checkbox.tsx).",
    "There is a check at line 952.",
])
def test_source_line_citation_shapes_are_problems(mini_repo, text):
    assert any("line numbers" in q for q in _append(mini_repo, "## More\n\n" + text))


def test_line_citation_inside_a_fence_is_code_not_a_citation(mini_repo):
    text = "## More\n\n```python\nprint('see Store.swift:88')\n```"
    assert _append(mini_repo, text) == []


# --- D_4: an empty WinUI bullet never borrows the next line ----------------------

@pytest.mark.parametrize("after", [
    "\n- **Android**: Use Compose.",
    "\n\nThe web build is the reference.",
])
def test_empty_winui_bullet_does_not_borrow_the_next_line(mini_repo, after):
    old = "- **WinUI 3**: `Microsoft.UI.Xaml.Controls.Button` with the `AccentButtonStyle` resource."
    info = _edit(mini_repo, old, "- **WinUI 3**:" + after)
    assert "Platform Notes has no filled `WinUI 3` bullet" in problems(info)


def test_winui_guidance_on_an_indented_continuation_line_counts(mini_repo):
    old = "- **WinUI 3**: `Microsoft.UI.Xaml.Controls.Button` with the `AccentButtonStyle` resource."
    assert problems(_edit(mini_repo, old, "- **WinUI 3**:\n  Use a `Button`.")) == []


# --- K07: a marker wrapped inside the phrase is still a marker -------------------

@pytest.mark.parametrize("text", [
    "- **hover**: NEEDS\n  REVIEW: Not implemented in source. No hover.",
    "The hover state is undefined; this is NEEDS\nREVIEW: Not implemented in source.",
])
def test_marker_wrapped_mid_phrase_is_a_problem(mini_repo, text):
    found = _append(mini_repo, "## Notes\n\n" + text)
    assert "body carries a `NEEDS REVIEW` marker" in found
    assert any("one-line" in q for q in found)


# --- K08: sections are fence-aware ------------------------------------------------

def test_hash_comment_in_a_fence_does_not_end_platform_notes(mini_repo):
    info = _edit(mini_repo, "## Platform Notes\n",
                 "## Platform Notes\n\n```sh\n# install the package\n## defaults\n```\n")
    assert problems(info) == []


def test_fenced_heading_sample_does_not_replace_a_real_section(mini_repo):
    info = _edit(mini_repo, "## Design Decisions\n",
                 "## Design Decisions\n\n```markdown\n## Platform Notes\n\n- **WinUI 3**:\n```\n")
    assert problems(info) == []


# --- Reuse_0: required sections come from the template ----------------------------

@pytest.mark.parametrize("section", ["Compliance", "Logging", "Deep Linking", "Change History"])
def test_every_template_section_is_required(mini_repo, section):
    p = mini_repo / "recipes" / "button.md"
    text = p.read_text(encoding="utf-8")
    start = text.index(f"## {section}\n")
    nxt = text.find("\n## ", start + 1)
    p.write_text(text[:start] + (text[nxt + 1:] if nxt != -1 else ""), encoding="utf-8")
    assert f"section `{section}` is missing" in problems(load_corpus(mini_repo / "recipes")["button"])


def test_required_sections_mapping_reads_the_templates():
    from cookr.core import templates
    from cookr.core.completeness import REQUIRED_SECTIONS

    assert "recipe" in REQUIRED_SECTIONS and "guidline" not in REQUIRED_SECTIONS
    assert REQUIRED_SECTIONS["ingredient"] == templates.required_sections("ingredient")
    assert "Compliance" in REQUIRED_SECTIONS["recipe"]


# --- Altitude_3: script-visible writer rules are graded ---------------------------

def test_compliance_must_cite_the_required_checks(mini_repo):
    info = _edit(mini_repo, "| [separation-of-concerns](agenticdevelopercookbook://compliance/"
                 "best-practices#separation-of-concerns) | passed | best-practices |\n", "")
    assert any("best-practices#separation-of-concerns" in q and "Compliance does not cite" in q
               for q in problems(info))


def test_fewer_than_five_vectors_is_a_problem(mini_repo):
    info = _edit(mini_repo, "| button-005 | case-5 | input 5 | output 5 |\n", "")
    assert "Conformance Test Vectors has 4 rows; at least 5 are required" in problems(info)


def test_design_decisions_as_bullets_is_a_problem(mini_repo):
    info = _edit(mini_repo, "**Decision**: Button uses semantic colors.\n"
                 "**Rationale**: Consistency across the product.\n**Approved**: pending\n",
                 "- **Semantic colors**: consistency.\n")
    assert any("Design Decisions" in q for q in problems(info))


@pytest.mark.parametrize("sources, expected", [
    (["web", "apple"], []),
    (["web"], ["frontmatter `platforms` lists `macos`, `swift`, not a source platform (sources: web)"]),
    (["apple", "python", "web"],
     ["frontmatter `platforms` lacks `python` (sources: apple, python, web)"]),
    (["android"], []),  # no known identifiers: ungraded
])
def test_frontmatter_platforms_follow_the_source_platforms(mini_repo, sources, expected):
    info = load_corpus(mini_repo / "recipes")["button"]
    assert problems(info, source_platforms=sources) == expected


def test_apple_source_needs_macos_or_ios(mini_repo):
    info = _edit(mini_repo, "platforms: [typescript, web, swift, macos]", "platforms: [swift]")
    assert problems(info, source_platforms=["apple"]) == [
        "frontmatter `platforms` lacks `ios` or `macos` (sources: apple)"]


# --- ADD-HIST: Change History is graded -------------------------------------------

def test_mixed_order_history_is_a_problem(mini_repo):
    info = _edit(mini_repo, "| 1.0.0 | 2026-09-01 | Fixture Author | Initial creation |",
                 "| 1.0.0 | 2026-09-01 | Fixture Author | Initial creation |\n"
                 "| 1.0.5 | 2026-09-05 | Fixture Author | Patch |")
    assert any("not in one version order" in q for q in problems(info))


def test_oldest_first_history_is_fine(mini_repo):
    info = _edit(mini_repo, NEWEST_ROW + "\n| 1.0.0 | 2026-09-01 | Fixture Author | Initial creation |",
                 "| 1.0.0 | 2026-09-01 | Fixture Author | Initial creation |\n" + NEWEST_ROW)
    assert problems(info) == []


def test_newest_row_must_match_frontmatter_version(mini_repo):
    info = _edit(mini_repo, "version: 1.1.0", "version: 1.0.0")
    assert ("frontmatter `version` is `1.0.0` but the newest Change History row is 1.1.0"
            in problems(info))


def test_modified_older_than_newest_row_is_a_problem(mini_repo):
    info = _edit(mini_repo, "modified: 2026-09-20", "modified: 2026-09-10")
    assert any("frontmatter `modified` (2026-09-10) is older" in q for q in problems(info))


@pytest.mark.parametrize("row", [
    "| 1.1.0 |  | Fixture Author | Filled |",
    "| 1.1.0 | 2026-09-20 |  | Filled |",
])
def test_blank_history_cell_is_a_problem(mini_repo, row):
    assert any("blank version, date or author" in q
               for q in problems(_edit(mini_repo, NEWEST_ROW, row)))


def test_row_separated_from_its_table_is_a_problem(mini_repo):
    info = _edit(mini_repo, NEWEST_ROW + "\n", NEWEST_ROW + "\n\n")
    assert any("the table is split" in q for q in problems(info))


@pytest.mark.parametrize("triple", [
    "1. **Decision**: One.\n   **Rationale**: Why.\n   **Approved**: pending\n",
    "- **Decision**: One.\n  **Rationale**: Why.\n  **Approved**: pending\n",
])
def test_design_decision_triples_as_list_items_are_fine(mini_repo, triple):
    info = _edit(mini_repo, "**Decision**: Button uses semantic colors.\n"
                 "**Rationale**: Consistency across the product.\n**Approved**: pending\n", triple)
    assert problems(info) == []


def test_design_decision_missing_its_approved_line_is_a_problem(mini_repo):
    info = _edit(mini_repo, "**Approved**: pending\n", "\n")
    assert any("Design Decisions" in q for q in problems(info))


def test_domain_matching_its_path_is_not_a_problem(mini_repo):
    corpus = load_corpus(mini_repo / "recipes")
    assert problems(corpus["button"], domain="mini-repo://recipes/button") == []


@pytest.mark.parametrize("line", [
    "domain: agenticdevelopercookbook://recipes/button",  # another repo's scheme
    "domain: mini-repo://ingredients/button",             # wrong directory
    "domain: mini-repo://recipes/toolbar-button",         # longer slug, same suffix
])
def test_domain_not_matching_its_path_is_a_problem(mini_repo, line):
    path = mini_repo / "recipes" / "button.md"
    path.write_text(path.read_text().replace("domain: mini-repo://recipes/button", line))
    got = problems(load_corpus(mini_repo / "recipes")["button"], domain="mini-repo://recipes/button")
    assert got == [f"frontmatter `domain` is `{line.split(': ', 1)[1]}`, not `mini-repo://recipes/button`"]
