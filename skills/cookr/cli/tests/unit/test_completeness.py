from __future__ import annotations

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
