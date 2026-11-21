"""owner_list.py: the owner list, written and checked by script.

    python3 -m pytest .claude/skills/grow-cookbook/scripts -q
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import owner_list  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def artifact(tmp: Path, topic: str) -> Path:
    art = tmp / topic
    (art / "research").mkdir(parents=True)
    shutil.copy(FIXTURES / topic / "research.json", art / "research" / "research.json")
    return art


def test_feature_flags_owner_list_is_the_four_prior_rules_and_the_open_questions(tmp_path):
    art = artifact(tmp_path, "feature-flags")
    result = owner_list.build(art, FIXTURES / "feature-flags" / "draft.md")
    rules = {r["rule"]: r for r in result["prior"]}
    assert sorted(rules) == ["fail-fast-on-missing-config", "gate-all-features",
                             "kotlin-sharedpreferences-default", "spec-lists-flag-keys"]
    assert rules["gate-all-features"]["status"] == "verbatim"
    assert rules["kotlin-sharedpreferences-default"]["status"] == "lead-in"
    assert rules["kotlin-sharedpreferences-default"]["lead_in"] == "In Kotlin, the local default SHOULD be:"
    assert rules["fail-fast-on-missing-config"]["lead_in"] == "The app MUST do this:"
    assert len(result["open_questions"]) == 5
    assert result["problems"] == []


def test_debug_modes_lead_in_is_listed(tmp_path):
    art = artifact(tmp_path, "debug-mode")
    result = owner_list.build(art, FIXTURES / "debug-mode" / "draft.md")
    [rule] = result["prior"]
    assert rule["rule"] == "typescript-debug-access"
    assert rule["lead_in"] == "In TypeScript, the panel MUST be reached this way:"
    text = owner_list.render("debug-mode", result)
    assert "lead-in: \"In TypeScript, the panel MUST be reached this way:\"" in text
    assert "## Open questions" in text and text.count("\n- ", text.index("## Open questions")) == 3


def test_a_reworded_or_dropped_owner_rule_is_a_problem(tmp_path, capsys):
    art = artifact(tmp_path, "feature-flags")
    draft = tmp_path / "draft.md"
    text = (FIXTURES / "feature-flags" / "draft.md").read_text(encoding="utf-8")
    text = text.replace("gated behind feature flags from initial", "gated behind flags from first")
    text = "\n".join(l for l in text.splitlines() if "**spec-lists-flag-keys**" not in l)
    draft.write_text(text, encoding="utf-8")
    out = tmp_path / "owner-list.md"
    assert owner_list.main([str(art), "--draft", str(draft), "--out", str(out)]) == 1
    problems = json.loads(capsys.readouterr().out)["problems"]
    assert sorted(p["rule"] for p in problems) == ["gate-all-features", "spec-lists-flag-keys"]
    assert {p["status"] for p in problems} == {"reworded", "dropped"}
    assert out.exists()


def test_before_stage_3_the_list_is_written_without_a_draft(tmp_path):
    art = artifact(tmp_path, "feature-flags")
    out = tmp_path / "owner-list.md"
    assert owner_list.main([str(art), "--out", str(out)]) == 0
    text = out.read_text(encoding="utf-8")
    assert "**gate-all-features**" in text and "All features MUST be gated" in text
    assert "only the rule's wording is exempt from review" in text


def test_keywordless_prior_rules_are_named(tmp_path):
    art = artifact(tmp_path, "feature-flags")
    result = owner_list.build(art)
    keyless = sorted(r["rule"] for r in result["prior"] if not r["keyword"])
    assert keyless == ["fail-fast-on-missing-config", "kotlin-sharedpreferences-default"]
    text = owner_list.render("feature-flags", result)
    assert text.count("no RFC keyword") == 2


def test_a_lead_in_is_accepted_only_on_a_keywordless_prior_and_only_carrying_a_keyword():
    keyless = "the local default is false"
    assert owner_list.compare(keyless, "In Kotlin, the value SHOULD be: the local default is false") == (
        "lead-in", "In Kotlin, the value SHOULD be:")
    # the lead-in carries no RFC keyword
    assert owner_list.compare(keyless, "In Kotlin: the local default is false") == ("reworded", "")
    # the prior already has a keyword: no lead-in is allowed in front of it
    keyed = "All features MUST be gated"
    assert owner_list.compare(keyed, "In production, all MUST: All features MUST be gated") == ("reworded", "")
    assert owner_list.compare(keyed, keyed) == ("verbatim", "")


def _research(tmp: Path, verdict: str, claim_id: str = "old-rule-prior") -> Path:
    art = tmp / "topic"
    (art / "research").mkdir(parents=True)
    data = {"claims": [{"id": claim_id, "source_type": owner_list.PRIOR_SOURCE, "claim": "old",
                        "quote": "Old text MUST hold"},
                       {"id": "web", "source_type": "vendor documentation", "claim": "web says", "quote": "q"}],
            "verdicts": [{"rule": "old-rule", "verdict": verdict, "claims": [claim_id, "web"]}],
            "open_questions": []}
    (art / "research" / "research.json").write_text(json.dumps(data), encoding="utf-8")
    return art


def test_only_owner_verdicts_put_a_prior_rule_on_the_list(tmp_path):
    for verdict, listed in (("supported", False), ("new", False), ("unsupported", True), ("contradicted", True)):
        art = _research(tmp_path / verdict, verdict)
        assert bool(owner_list.build(art)["prior"]) is listed, verdict


def test_the_prior_claim_is_any_prior_source_claim_the_verdict_names(tmp_path):
    # cookr's owner-decides keys on source_type within an owner verdict, not on the id
    art = _research(tmp_path, "contradicted", claim_id="the-old-wording")
    [entry] = owner_list.build(art)["prior"]
    assert entry["prior"] == "Old text MUST hold"


def test_a_rule_keeps_its_later_paragraphs_across_blank_lines():
    text = "\n".join([
        "## Rules",
        "",
        "- **multi**: It compiles to four skills:",
        "",
        "  | Skill | Roles |",
        "  |---|---|",
        "  | builder | `rules` |",
        "",
        "  ```markdown",
        "  - **x**: y. (claim: z)",
        "  ```",
        "",
        "  **Applies when:** always. (claim: multi-prior)",
        "- **next**: Another rule. (claim: n)",
        "",
        "Prose after the list ends the last rule.",
        "",
        "## Examples",
    ])
    rules = owner_list.draft_rules(text)
    assert rules["multi"] == owner_list._norm(
        "It compiles to four skills: | Skill | Roles | |---|---| | builder | `rules` | "
        "```markdown - **x**: y. (claim: z) ``` **Applies when:** always.")
    assert rules["next"] == "Another rule."
