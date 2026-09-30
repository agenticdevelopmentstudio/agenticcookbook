"""The pure pieces of `cookbook skills build`: rule extraction, leaf splitting,
grouping (including index-budget refinement) and the output gates."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pytest

from cookbook.skillgen import gates, groups, leaves, rules
from cookbook.skillgen.groups import Placement
from cookbook.skillgen.source import Doc


# ── rules ────────────────────────────────────────────────────────────────


def _extract(text: str) -> list[rules.Rule]:
    return rules.extract(text, Counter())


def test_an_explicit_kebab_label_is_the_slug():
    [rule] = _extract("- **validate-at-boundary**: Handlers MUST validate input.\n")
    assert (rule.slug, rule.level, rule.explicit) == ("validate-at-boundary", "MUST", True)


def test_a_label_qualifier_is_kept():
    [rule] = _extract("- **reject-unknown** (api): Parsers SHOULD reject unknown fields.\n")
    assert rule.qualifier == "api"


def test_an_unlabelled_rule_gets_a_slug_from_the_words_around_its_keyword():
    [rule] = _extract("Error messages MUST NOT echo raw input back to the caller.\n")
    assert rule.slug == "error-messages-not-echo-raw-input-back"
    assert not rule.explicit
    assert rule.excerpt.startswith("Error messages MUST NOT")


def test_the_strongest_keyword_in_a_unit_sets_its_level():
    [rule] = _extract("You MAY cache it, but you MUST invalidate on write.\n")
    assert rule.level == "MUST"


def test_repeated_slugs_within_a_doc_are_numbered():
    seen: Counter = Counter()
    first = rules.extract("- **x-y**: A MUST b.\n", seen)
    second = rules.extract("- **x-y**: C MUST d.\n", seen)
    assert [r.slug for r in first + second] == ["x-y", "x-y-2"]


def test_keywords_in_fences_tables_and_headings_are_not_rules():
    text = "## Things you MUST know\n\n```\nfoo MUST bar\n```\n\n| a | MUST |\n|---|---|\n"
    assert _extract(text) == []


def test_lowercase_must_is_not_a_keyword():
    assert _extract("You must not do this.\n") == []


def test_test_vectors_come_from_an_id_requirements_table():
    text = "| ID | Requirements |\n|----|----|\n| t-1 | `a`, `b` |\n| t-2 | c |\n\nafter\n"
    assert [(v.id, v.requirements) for v in rules.test_vectors(text)] == [("t-1", ("a", "b")), ("t-2", ("c",))]


def test_other_tables_are_not_test_vectors():
    assert rules.test_vectors("| Name | Value |\n|---|---|\n| a | b |\n") == []


# ── leaves ───────────────────────────────────────────────────────────────


def test_clean_drops_change_history_and_placeholder_sections_and_unwraps_relative_links():
    body = ("# T\n\nSee [the doc](../x.md) and [site](https://e.com).\n\n"
            "## Accessibility\n\n_None yet._\n\n## Change History\n\n- 1.0.0\n")
    out = leaves.clean(body)
    assert "Change History" not in out and "Accessibility" not in out
    assert "See the doc and [site](https://e.com)." in out


def test_a_recipe_splits_its_states_section_into_its_own_part():
    body = "# R\n\n## Overview\n\nA MUST b.\n\n## States\n\n- **empty**: X MUST y.\n"
    parts = leaves.split(body, "recipe", 12_000, "r.md")
    assert [(p.suffix, p.heading) for p in parts] == [("", ""), ("states", "States")]
    assert parts[1].text.startswith("## States")


def test_a_guideline_is_not_split_by_section():
    body = "# G\n\n## States\n\nA MUST b.\n"
    assert [p.suffix for p in leaves.split(body, "guideline", 12_000, "g.md")] == [""]


def test_fit_packs_by_h2_first():
    text = "## A\n" + "a" * 60 + "\n## B\n" + "b" * 60
    chunks = leaves.fit(text, 80, "x")
    assert [c.split("\n")[0] for c in chunks] == ["## A", "## B"]


def test_fit_falls_back_to_top_level_list_items():
    text = "\n".join(f"- item {i} " + "x" * 30 for i in range(6))
    chunks = leaves.fit(text, 100, "x")
    assert len(chunks) > 1 and all(len(c) <= 100 for c in chunks)
    assert all(c.startswith("- item") for c in chunks)


def test_fit_splits_a_table_and_repeats_its_header():
    rows = "\n".join(f"| r{i} | " + "v" * 30 + " |" for i in range(8))
    text = "| k | v |\n|---|---|\n" + rows
    chunks = leaves.fit(text, 120, "x")
    assert len(chunks) > 1
    assert all(c.startswith("| k | v |\n|---|---|") and len(c) <= 120 for c in chunks)


def test_fit_keeps_a_code_fence_whole():
    fence = "```\n" + "\n".join("line" for _ in range(5)) + "\n```"
    text = "para one\n\n" + fence + "\n\npara two"
    chunks = leaves.fit(text, 45, "x")
    assert any(fence in c for c in chunks)
    assert all(c.count("```") % 2 == 0 for c in chunks)


def test_an_unsplittable_block_is_refused():
    with pytest.raises(leaves.LeafTooLarge, match="x.md"):
        leaves.fit("y" * 500, 100, "x.md")


def test_split_honours_an_explicit_budget():
    body = "\n\n".join("p" * 50 for _ in range(10))
    parts = leaves.split(body, "guideline", 12_000, "g.md", budget=120)
    assert len(parts) > 1 and all(len(p.text) <= 121 for p in parts)
    assert [p.suffix for p in parts][:2] == ["", "part-2"]


# ── groups ───────────────────────────────────────────────────────────────


def _doc(rel: str, body: str = "x\n") -> Doc:
    return Doc(rel=Path(rel), data={"title": "T"}, body=body, source_hash="h")


def test_cookbook_placements():
    g = groups.group([
        _doc("guidelines/reviewing/security/auth.md"),
        _doc("guidelines/reviewing/naming.md"),
        _doc("recipes/ui/login-form.md"),
        _doc("principles/yagni.md"),
        _doc("introduction/conventions.md"),
        _doc("guidelines/dancing/x/y.md"),
    ], "cookbook")
    assert g.placements["guidelines/reviewing/security/auth.md"].router == "review-security"
    assert g.placements["guidelines/reviewing/naming.md"].router == "review-general"
    assert g.placements["recipes/ui/login-form.md"].router == "recipes-ui"
    assert g.placements["principles/yagni.md"].router == "principles"
    assert dict(g.skipped) == {
        "introduction/conventions.md": "introduction/ is not rule content",
        "guidelines/dancing/x/y.md": "unknown use case 'dancing'",
    }


def test_identical_guidelines_alias_to_the_first_by_path_and_different_ones_drift():
    g = groups.group([
        _doc("guidelines/reviewing/security/auth.md", "same\n"),
        _doc("guidelines/implementing/security/auth.md", "same\n\n## Change History\n\n- other\n"),
        _doc("guidelines/testing/security/auth.md", "different\n"),
    ], "cookbook")
    assert g.aliases == {"guidelines/reviewing/security/auth.md": "guidelines/implementing/security/auth.md"}
    assert [key for key, _ in g.drift] == ["security/auth"]


def test_recipes_layout_routes_by_a_shared_name_prefix():
    names = [f"status-server-{n}" for n in "abcd"] + ["tab-view", "notes"]
    g = groups.group([_doc(f"{n}.md") for n in names], "recipes")
    assert g.placements["status-server-a.md"] == Placement("implement-status-server", "implement", "status-server", "a")
    assert g.placements["tab-view.md"].router == "implement-general"


def _placements(router: str, stems: list[str]) -> dict[str, Placement]:
    verb, domain = router.split("-", 1)
    return {f"{s}.md": Placement(router, verb, domain, s) for s in stems}


def test_refine_leaves_a_router_within_budget_alone():
    p = _placements("implement-general", ["a", "b"])
    assert groups.refine(p, lambda rel: 10, 100) == p


def test_refine_splits_by_a_shared_leading_token_and_drops_it_from_the_stem():
    stems = [f"server-{i}" for i in range(4)] + ["x", "y"]
    out = groups.refine(_placements("implement-general", stems), lambda rel: 10, 50)
    assert out["server-0.md"] == Placement("implement-general-server", "implement", "general-server", "0")
    assert out["x.md"].router == "implement-general"


def test_refine_splits_by_a_shared_trailing_token_and_keeps_the_stem():
    stems = [f"{n}-view" for n in "abcd"] + ["x-model", "y-model"]
    out = groups.refine(_placements("implement-general", stems), lambda rel: 10, 50)
    assert out["a-view.md"] == Placement("implement-general-view", "implement", "general-view", "a-view")


def test_refine_does_not_rename_when_every_doc_shares_the_token():
    """Moving every doc into one child is a rename that would recurse forever;
    the fallback is alphabetical runs."""
    stems = [f"{n}-view" for n in "abcdef"]
    out = groups.refine(_placements("implement-general", stems), lambda rel: 10, 30)
    assert {p.router for p in out.values()} == {"implement-general-1", "implement-general-2"}
    assert all(p.stem.endswith("-view") for p in out.values())


def test_refine_names_a_child_after_its_parent_router():
    stems = [f"ui-{n}" for n in "abcd"] + ["x"]
    p = {f"{s}.md": Placement("ingredients", "ingredients", "ingredients", s) for s in stems}
    out = groups.refine(p, lambda rel: 10, 45)
    assert out["ui-a.md"].router == "ingredients-ui"


def test_refine_gives_up_on_a_single_over_budget_doc():
    p = _placements("implement-general", ["huge"])
    assert groups.refine(p, lambda rel: 999, 10) == p


def test_refine_is_deterministic():
    stems = [f"{a}-{b}" for a in ("server", "web", "hub") for b in ("x", "y", "z", "w", "v")]
    p = _placements("implement-general", stems)
    assert groups.refine(p, lambda rel: 10, 60) == groups.refine(dict(reversed(p.items())), lambda rel: 10, 60)


# ── gates ────────────────────────────────────────────────────────────────


def _skill(name: str, description: str = "d", body: str = "") -> str:
    return f'---\nname: {name}\ndescription: "{description}"\n---\n{body}'


def test_names_must_match_their_directory_and_be_kebab_case():
    files = {"skills/a-b/SKILL.md": _skill("a-c"), "skills/Bad/SKILL.md": _skill("Bad")}
    errors = gates.names(files)
    assert any("does not match its directory 'a-b'" in e for e in errors)
    assert any("'Bad' is not lowercase kebab-case" in e for e in errors)


def test_descriptions_have_a_budget():
    assert gates.descriptions({"skills/a/SKILL.md": _skill("a", "x" * 20)}, budget=10)


def test_every_local_link_must_resolve():
    files = {"skills/a/SKILL.md": _skill("a", body="[i](index.md) [w](https://e.com)")}
    assert gates.links(files) == ["skills/a/SKILL.md: link to skills/a/index.md does not resolve"]


def test_depth_allows_two_hops_and_no_more():
    files = {
        "skills/a/SKILL.md": _skill("a", body="[i](index.md)"),
        "skills/a/index.md": "[l](leaves/l.md)",
        "skills/a/leaves/l.md": "[m](m.md)",
        "skills/a/leaves/m.md": "",
    }
    assert gates.depth(files) == ["skills/a/SKILL.md: skills/a/leaves/m.md is 3 hops deep (max 2)"]


def test_leaf_and_index_sizes_are_capped():
    files = {"skills/a/leaves/l.md": "x" * 11, "skills/a/index.md": "x" * 21, "skills/a/SKILL.md": "x" * 99}
    assert gates.leaf_sizes(files, 10) == ["skills/a/leaves/l.md: 11 chars exceeds the 10-char leaf cap"]
    assert gates.index_sizes(files, 20) == ["skills/a/index.md: 21 chars exceeds the 20-char index budget"]
