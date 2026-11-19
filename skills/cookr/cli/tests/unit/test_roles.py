"""The role census (core/roles.py)."""

from __future__ import annotations

import pytest

from cookr.core import roles
from cookr.core.artifact import ROLES, Artifact, Part, load_folder, write_folder

RULES = "- **must-index-foreign-keys**: Every foreign key MUST have an index.\n"
BAR = "- `must-index-foreign-keys`: every foreign key is indexed.\n"


def parts(**overrides):
    """A complete roled artifact's parts: one per needed role. A keyword set
    to None drops that part; a Part replaces it."""
    base = {
        "rules": Part("rules", RULES, "Rules", "rules"),
        "focus": Part("focus", "Look at the joins.\n", "Review focus", "review-focus"),
        "review_bar": Part("review_bar", "Flag an unindexed key.\n", "Review bar", "review-bar"),
        "build_bar": Part("build_bar", BAR, "Build bar", "build-bar"),
    }
    base.update(overrides)
    return ([Part("intro", "# T\n\nIndexes.\n")]
            + [p for p in base.values() if p is not None]
            + [Part("history", "| 1.0.0 | x |\n", "Change History")])


def make(root, rel="guidelines/implementing/data/t", **overrides):
    folder = root / rel
    write_folder(Artifact(meta={"id": "t", "type": "guideline"}, parts=parts(**overrides)), folder)
    return folder


def found(*folders):
    return [(f.kind, f.detail) for f in roles.census(folders)]


def test_the_tables_cover_the_four_skills():
    assert roles.SKILL_ROLES == {
        "builder": ("rules", "how-to", "examples"),
        "build-verifier": ("build-bar",),
        "reviewer": ("rules", "review-focus"),
        "review-verifier": ("review-bar",),
    }
    assert roles.NEEDS == {"builder": "rules", "build-verifier": "build-bar",
                           "reviewer": "review-focus", "review-verifier": "review-bar"}
    assert all(r in ROLES for kind in roles.SKILL_ROLES.values() for r in kind)


def test_a_complete_roled_artifact_has_no_finding(tmp_path):
    assert found(make(tmp_path)) == []


def test_an_artifact_with_no_role_has_no_finding(tmp_path):
    folder = tmp_path / "guidelines" / "implementing" / "data" / "t"
    write_folder(Artifact(meta={"id": "t", "type": "guideline"}, parts=[
        Part("intro", "# T\n"), Part("notes", "- Keys MUST be indexed.\n", "Notes"),
        Part("history", "x\n", "Change History")]), folder)
    (tmp_path / "guidelines" / "reviewing" / "data" / "t").mkdir(parents=True)
    (folder / "hosts").mkdir()
    assert found(folder) == []


def test_an_unknown_role(tmp_path):
    folder = make(tmp_path, tips=Part("tips", "Be nice.\n", "Tips", "tips"))
    assert found(folder) == [("unknown-role", "part 'tips' has role 'tips'")]


def test_a_headed_part_with_no_role_in_a_roled_artifact(tmp_path):
    folder = make(tmp_path, notes=Part("notes", "Some notes.\n", "Notes"))
    assert found(folder) == [("unroled-part", "part 'notes' has no role")]


def test_a_missing_role_names_the_skill_it_stops(tmp_path):
    folder = make(tmp_path, build_bar=None)
    assert found(folder) == [("missing-role", "no 'build-bar' part, so no build-verifier skill")]


def test_a_missing_rules_part_stops_only_the_builder(tmp_path):
    folder = make(tmp_path, rules=None)
    assert found(folder) == [("missing-role", "no 'rules' part, so no builder skill")]


def test_a_rule_bullet_with_no_name(tmp_path):
    folder = make(tmp_path, rules=Part("rules", RULES + "\nProse is fine.\n\n- Logs MUST be JSON, always.\n",
                                       "Rules", "rules"))
    assert found(folder) == [("unnamed-rule", "part 'rules': '- Logs MUST be JSON, always.' is not "
                                              "`- **name**: …`")]


def test_a_long_unnamed_bullet_is_quoted_by_its_start(tmp_path):
    bullet = "- Every table that holds customer data MUST be encrypted at rest and in transit."
    folder = make(tmp_path, rules=Part("rules", RULES + bullet + "\n", "Rules", "rules"))
    assert found(folder) == [("unnamed-rule", f"part 'rules': '{bullet[:40]}…' is not `- **name**: …`")]


def test_a_rules_part_with_no_rule(tmp_path):
    folder = make(tmp_path, rules=Part("rules", "Index things.\n", "Rules", "rules"))
    assert found(folder) == [("unnamed-rule", "part 'rules' states no named rule"),
                             ("unknown-citation", "build-bar part 'build_bar' cites "
                                                  "'must-index-foreign-keys', which is no rule")]


def test_a_continuation_line_belongs_to_its_rule(tmp_path):
    text = ("- **index-keys**: Keys are indexed;\n  the index MUST be btree.\n"
            "  - a nested note MUST NOT count as its own rule.\n")
    folder = make(tmp_path, rules=Part("rules", text, "Rules", "rules"),
                  build_bar=Part("build_bar", "- `index-keys`: keys are indexed.\n", "Build bar", "build-bar"))
    assert found(folder) == []
    assert roles.rule_names(load_folder(folder)) == ["index-keys"]


def test_a_keyword_in_code_is_not_a_rule(tmp_path):
    text = RULES + "```\n- x MUST y\n```\n"
    assert found(make(tmp_path, rules=Part("rules", text, "Rules", "rules"))) == []


def test_rule_names_across_rules_parts_in_order(tmp_path):
    folder = make(tmp_path, more=Part("more", "- **b-rule**: B MUST.\n- **a-rule**: A MAY.\n",
                                      "More rules", "rules"))
    assert roles.rule_names(load_folder(folder)) == ["must-index-foreign-keys", "b-rule", "a-rule"]


def test_a_duplicate_rule_name(tmp_path):
    folder = make(tmp_path, more=Part("more", RULES, "More rules", "rules"))
    assert found(folder) == [("duplicate-rule", "rule 'must-index-foreign-keys' is named 2 times")]


def test_a_roled_twin_not_folded(tmp_path):
    folder = make(tmp_path)
    (tmp_path / "guidelines" / "reviewing" / "data" / "t").mkdir(parents=True)
    assert found(folder) == [("twin-not-folded",
                              "guidelines/implementing/data/t has a twin at guidelines/reviewing/data/t")]


def test_a_roled_artifact_with_host_tuning(tmp_path):
    folder = make(tmp_path)
    (folder / "hosts").mkdir()
    assert found(folder) == [("tuned", "it has a hosts/ directory")]


def test_every_kind_has_a_fix():
    assert set(roles.FIX) == {"unknown-role", "unroled-part", "missing-role", "empty-part",
                              "unnamed-rule", "duplicate-rule", "uncited-rule", "unknown-citation",
                              "twin-not-folded", "tuned", "routed", "reviewing-folder",
                              "unroled-type", "name-collision"}


# ── where a roled artifact may live ──────────────────────────────────────────


def test_a_roled_guideline_under_planning_passes_the_census(tmp_path):
    assert found(make(tmp_path, "guidelines/planning/data/t")) == []


def test_a_roled_planning_topic_with_a_reviewing_twin_is_not_folded(tmp_path):
    folder = make(tmp_path, "guidelines/planning/data/t")
    (tmp_path / "guidelines" / "reviewing" / "data" / "t").mkdir(parents=True)
    assert found(folder) == [("twin-not-folded",
                              "guidelines/planning/data/t has a twin at guidelines/reviewing/data/t")]


def test_a_roled_guideline_under_reviewing_is_refused(tmp_path):
    folder = make(tmp_path, "guidelines/reviewing/data/t")
    assert found(folder) == [("reviewing-folder", "it lives under guidelines/reviewing/, which is "
                                                  "folded into its topic, never roled")]


def test_a_roled_principle_passes_the_census(tmp_path):
    folder = tmp_path / "principles" / "t"
    write_folder(Artifact(meta={"id": "t", "type": "principle"}, parts=parts()), folder)
    assert found(folder) == []


def test_a_roled_principle_colliding_with_a_guideline_is_found(tmp_path):
    a = tmp_path / "principles" / "t"
    write_folder(Artifact(meta={"id": "t", "type": "principle"}, parts=parts()), a)
    b = tmp_path / "guidelines" / "reviewing" / "principle" / "t"
    write_folder(Artifact(meta={"id": "u", "type": "guideline"}, parts=[Part("intro", "# U\n")]), b)
    assert found(a, b) == [("name-collision", "its reviewer skill 'reviewing-principle-t' "
                                              "is also derived for guidelines/reviewing/principle/t")]


@pytest.mark.parametrize("type_, rel", [("ingredient", "ingredients/ui/t"), ("recipe", "recipes/ui/t")])
def test_a_roled_ingredient_or_recipe_is_refused(tmp_path, type_, rel):
    folder = tmp_path / rel
    write_folder(Artifact(meta={"id": "t", "type": type_}, parts=parts()), folder)
    assert found(folder) == [("unroled-type", f"{'an' if type_ == 'ingredient' else 'a'} {type_} "
                                              "is never roled")]


@pytest.mark.parametrize("use_case, other", [("verifying-build", "build-verifier"),
                                              ("verifying-review", "review-verifier")])
def test_a_roled_topic_under_verifying_build_fails_the_census(tmp_path, use_case, other):
    folder = make(tmp_path, f"guidelines/{use_case}/data/t")
    assert found(folder) == [("name-collision", f"its builder and {other} skills are both named "
                                                f"'{use_case}-data-t'")]


def test_two_roled_topics_whose_derived_names_collide_are_found_naming_both(tmp_path):
    tail = "data/" + "a-very-long-topic-name-" * 3 + "t"
    a = make(tmp_path, f"guidelines/implementing/{tail}")
    b = make(tmp_path, f"guidelines/planning/{tail}")
    got = found(a, b)
    assert [k for k, _ in got] == ["name-collision"] * 6
    assert all(f"guidelines/planning/{tail}" in d for _, d in got[:3])
    assert all(f"guidelines/implementing/{tail}" in d for _, d in got[3:])
    assert {d.split("'")[1] for _, d in got[:3]} == {d.split("'")[1] for _, d in got[3:]}


def test_a_roled_topic_colliding_with_an_unroled_artifact_is_found(tmp_path):
    a = make(tmp_path, "guidelines/planning/data/t")
    b = tmp_path / "guidelines" / "verifying-build" / "data" / "t"
    write_folder(Artifact(meta={"id": "u", "type": "guideline"}, parts=[Part("intro", "# U\n")]), b)
    assert found(a, b) == [("name-collision", "its build-verifier skill 'verifying-build-data-t' "
                                              "is also derived for guidelines/verifying-build/data/t")]


def test_an_unreadable_folder_is_skipped(tmp_path):
    folder = tmp_path / "recipes" / "broken"
    folder.mkdir(parents=True)
    (folder / "artifact.json").write_text("{", encoding="utf-8")
    assert found(folder) == []


def test_a_role_on_the_intro_or_the_history(tmp_path):
    folder = tmp_path / "guidelines" / "implementing" / "data" / "t"
    ps = parts()
    ps[0].role, ps[-1].role = "how-to", "references"
    write_folder(Artifact(meta={"id": "t", "type": "guideline"}, parts=ps), folder)
    assert found(folder) == [
        ("unknown-role", "part 'intro' has role 'how-to'; the intro never carries a role"),
        ("unknown-role", "part 'history' has role 'references'; the history never carries a role")]


def test_a_roled_artifact_with_its_own_routes(tmp_path):
    folder = tmp_path / "guidelines" / "implementing" / "data" / "t"
    write_folder(Artifact(meta={"id": "t", "type": "guideline"}, parts=parts(), routes=["coding/data"]), folder)
    assert found(folder) == [("routed", "a roled artifact derives its routes; it may not set `routes` "
                                        "in artifact.json")]


def test_an_unroled_artifact_may_set_its_routes(tmp_path):
    folder = tmp_path / "guidelines" / "implementing" / "data" / "t"
    write_folder(Artifact(meta={"id": "t", "type": "guideline"}, parts=[Part("intro", "# T\n")],
                          routes=["coding/data"]), folder)
    assert found(folder) == []


# ── a needed part with no text ────────────────────────────────────────────────


@pytest.mark.parametrize("key, role, kind", [
    ("rules", "rules", "builder"),
    ("build_bar", "build-bar", "build-verifier"),
    ("focus", "review-focus", "reviewer"),
    ("review_bar", "review-bar", "review-verifier"),
])
def test_a_needed_part_with_no_text_names_its_role_and_skill(tmp_path, key, role, kind):
    folder = make(tmp_path, **{key: Part(key, "\n  \n", "Blank", role)})
    assert found(folder) == [("empty-part", f"part '{key}' with role '{role}' has no text, "
                                            f"so no {kind} skill")]


def test_a_blank_needed_part_beside_a_full_one_is_still_a_finding(tmp_path):
    folder = make(tmp_path, bar2=Part("bar2", "\n", "Second bar", "review-bar"))
    assert found(folder) == [("empty-part", "part 'bar2' with role 'review-bar' has no text, "
                                            "so no review-verifier skill")]


# ── what a rules part's census sees ──────────────────────────────────────────

def rules_part(text):
    return Part("rules", RULES + text, "Rules", "rules")


def test_a_numbered_item_stating_a_requirement_is_an_unnamed_rule(tmp_path):
    folder = make(tmp_path, rules=rules_part("\n1. Code MUST frobnicate.\n"))
    assert found(folder) == [("unnamed-rule", "part 'rules': '1. Code MUST frobnicate.' is not "
                                              "`- **name**: …`")]


def test_a_numbered_item_with_a_name_is_still_not_the_rule_form(tmp_path):
    folder = make(tmp_path, rules=rules_part("\n1. **frob**: Code MUST frobnicate.\n"))
    assert [k for k, _ in found(folder)] == ["unnamed-rule"]


def test_a_numbered_item_under_a_named_rule_belongs_to_it(tmp_path):
    folder = make(tmp_path, rules=rules_part("  1. which column MUST come first?\n"))
    assert found(folder) == []


def test_an_indented_named_bullet_is_its_own_rule(tmp_path):
    text = RULES + "\nSome lead-in.\n\n  - **indented-rule**: Code MUST be indented.\n"
    folder = make(tmp_path, rules=Part("rules", text, "Rules", "rules"))
    assert roles.rule_names(load_folder(folder)) == ["must-index-foreign-keys", "indented-rule"]


def test_an_indented_named_bullet_reusing_a_name_is_a_duplicate(tmp_path):
    text = RULES + "  - **must-index-foreign-keys**: Keys MUST be indexed again.\n"
    folder = make(tmp_path, rules=Part("rules", text, "Rules", "rules"))
    assert ("duplicate-rule", "rule 'must-index-foreign-keys' is named 2 times") in found(folder)


def test_a_named_bullet_with_a_lower_case_requirement_is_a_rule(tmp_path):
    folder = make(tmp_path, rules=rules_part("- **no-secrets**: you must never store secrets.\n"))
    assert roles.rule_names(load_folder(folder)) == ["must-index-foreign-keys", "no-secrets"]


def test_an_unnamed_bullet_with_a_lower_case_word_states_no_rule(tmp_path):
    folder = make(tmp_path, rules=rules_part("- you may read the how-to first.\n"))
    assert found(folder) == []


def test_an_unnamed_bullet_with_an_upper_case_requirement_is_an_unnamed_rule(tmp_path):
    folder = make(tmp_path, rules=rules_part("- you MUST never store secrets.\n"))
    assert found(folder) == [("unnamed-rule", "part 'rules': '- you MUST never store secrets.' is not "
                                              "`- **name**: …`")]


def test_a_numbered_item_with_a_lower_case_word_states_no_rule(tmp_path):
    folder = make(tmp_path, rules=rules_part("\n1. These steps may run in any order.\n"))
    assert found(folder) == []


def test_a_second_bullet_reusing_a_name_without_a_keyword_is_a_duplicate(tmp_path):
    folder = make(tmp_path, rules=rules_part("- **must-index-foreign-keys**: index them with btree.\n"))
    assert found(folder) == [("duplicate-rule", "rule 'must-index-foreign-keys' is named 2 times")]


def test_a_prose_requirement_outside_a_named_bullet_is_an_unnamed_rule(tmp_path):
    folder = make(tmp_path, rules=rules_part("\nProse: code MUST NOT store blobs.\n"))
    assert found(folder) == [("unnamed-rule", "part 'rules': 'Prose: code MUST NOT store blobs.' is not "
                                              "`- **name**: …`")]


@pytest.mark.parametrize("prose", ["These rules may be applied in any order.",
                                   "> Note: you should read the how-to."])
def test_lower_case_words_in_prose_state_no_rule(tmp_path, prose):
    folder = make(tmp_path, rules=rules_part(f"\n{prose}\n"))
    assert found(folder) == []


def test_an_upper_case_prose_requirement_is_still_an_unnamed_rule(tmp_path):
    folder = make(tmp_path, rules=rules_part("\nCode MUST x.\n"))
    assert found(folder) == [("unnamed-rule", "part 'rules': 'Code MUST x.' is not `- **name**: …`")]


def test_prose_with_no_requirement_is_allowed(tmp_path):
    folder = make(tmp_path, rules=Part("rules", "These are the rules.\n\n" + RULES, "Rules", "rules"))
    assert found(folder) == []


def test_a_paragraph_after_a_blank_line_indented_under_a_rule_belongs_to_it(tmp_path):
    folder = make(tmp_path, rules=rules_part("\n  It MUST be a btree index.\n"))
    assert found(folder) == []


def test_a_lazy_continuation_line_belongs_to_its_rule(tmp_path):
    folder = make(tmp_path, rules=Part("rules", "- **index-keys**: Keys are indexed;\nthe index MUST "
                                                "be btree.\n", "Rules", "rules"))
    assert found(folder) == [("uncited-rule", "rule 'index-keys' has no line in a build-bar part"),
                             ("unknown-citation", "build-bar part 'build_bar' cites "
                                                  "'must-index-foreign-keys', which is no rule")]


# ── the build bar against the rules ──────────────────────────────────────────

def test_a_rule_the_build_bar_does_not_cite(tmp_path):
    folder = make(tmp_path, rules=rules_part("- **may-cache**: Code MAY cache keys.\n"))
    assert found(folder) == [("uncited-rule", "rule 'may-cache' has no line in a build-bar part")]


def test_a_build_bar_citing_a_name_that_is_no_rule(tmp_path):
    folder = make(tmp_path, build_bar=Part("build_bar", BAR + "- `gone-rule`: it holds.\n",
                                           "Build bar", "build-bar"))
    assert found(folder) == [("unknown-citation", "build-bar part 'build_bar' cites 'gone-rule', "
                                                  "which is no rule")]


def test_a_renamed_rule_is_both_uncited_and_an_unknown_citation(tmp_path):
    folder = make(tmp_path, rules=Part("rules", RULES.replace("must-index-foreign-keys", "must-index-keys"),
                                       "Rules", "rules"))
    assert found(folder) == [("uncited-rule", "rule 'must-index-keys' has no line in a build-bar part"),
                             ("unknown-citation", "build-bar part 'build_bar' cites "
                                                  "'must-index-foreign-keys', which is no rule")]


@pytest.mark.parametrize("line", ["- `pytest` passes on the module.\n",
                                  "- `ruff check` is clean.\n",
                                  "- Run `must-index-foreign-keys` checks: none.\n"])
def test_a_build_bar_line_naming_code_is_no_citation(tmp_path, line):
    folder = make(tmp_path, build_bar=Part("build_bar", BAR + line, "Build bar", "build-bar"))
    assert found(folder) == []


def test_only_the_documented_form_cites_a_rule(tmp_path):
    bar = "- `must-index-foreign-keys` passes.\n"
    folder = make(tmp_path, build_bar=Part("build_bar", bar, "Build bar", "build-bar"))
    assert found(folder) == [("uncited-rule", "rule 'must-index-foreign-keys' has no line in a "
                                              "build-bar part")]


def test_a_shorter_fence_inside_a_longer_one_is_still_code(tmp_path):
    code = "\n````md\n```\n- code MUST x\n```\n````\n"
    folder = make(tmp_path, rules=rules_part(code))
    assert found(folder) == []


def test_a_backtick_line_inside_a_tilde_fence_is_still_code(tmp_path):
    folder = make(tmp_path, rules=rules_part("\n~~~\n```\n- code MUST x\n~~~\n"),
                  build_bar=Part("build_bar", BAR + "~~~\n```\n- `gone-rule`: x\n~~~\n",
                                 "Build bar", "build-bar"))
    assert found(folder) == []


def test_a_requirement_after_a_long_fence_closes_is_seen(tmp_path):
    folder = make(tmp_path, rules=rules_part("\n````\n```\n````\n\nCode MUST x.\n"))
    assert [k for k, _ in found(folder)] == ["unnamed-rule"]


def test_a_citation_in_code_is_not_a_citation(tmp_path):
    folder = make(tmp_path, build_bar=Part("build_bar", BAR + "```\n- `gone-rule`: x\n```\n",
                                           "Build bar", "build-bar"))
    assert found(folder) == []
