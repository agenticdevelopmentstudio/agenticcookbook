"""The research an artifact is written from (core/research.py): a `research/`
folder beside its parts, never compiled, and checked by `cookr validate` for
every artifact the research-first work has touched."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from cookr.cli import main
from cookr.core import research

from .cookbook_helpers import add_doc, new_repo

# Every tmp_path here is a git repo, as a real cookbook checkout is.
pytestmark = pytest.mark.usefixtures("git_tmp_path")

TOPIC = "guidelines/implementing/data/indexing"   # one of the 21 topics an exemption may name
NEW_TOPIC = "guidelines/implementing/data/keys"   # one no exemption may name

#: The 21 roled data topics that had no research when the research-first work began.
THE_21 = frozenset(f"guidelines/implementing/data/{t}" for t in (
    "access-pattern-analysis", "backup-and-recovery", "clock-systems", "conflict-resolution",
    "constraints-and-validation", "data-types", "foreign-keys", "indexing", "json-columns",
    "naming-conventions", "normalization-and-denormalization", "offline-first-architecture",
    "primary-keys", "query-optimization", "relationships", "schema-evolution", "sync-engine-design",
    "sync-protocol", "sync-schema-design", "sync-tooling", "transactions-and-concurrency"))
RULE = "- **must-index-keys**: Every foreign key MUST have an index.{cite}\n"
BODY = """# Keys

Index every key.

## Rules

{rules}
## What a reviewer looks for

Unindexed foreign keys.

## A complete review must establish

Every foreign key was checked for an index.

## A build must establish

- `must-index-keys`: every foreign key is indexed.

## Change History

x
"""
ROLES = ["rules=rules", "what-a-reviewer-looks-for=review-focus",
         "a-complete-review-must-establish=review-bar", "a-build-must-establish=build-bar"]


def claim(cid="fk-index", **overrides):
    """A claim carrying everything the research-results document requires."""
    c = {
        "id": cid,
        "question": "best-practices",
        "claim": "An index on a foreign key column avoids a full scan on each parent delete.",
        "citations": [{"title": "SQLite Foreign Key Support", "author": "SQLite", "publisher": "sqlite.org",
                       "date": "2025-05-31", "url": "https://sqlite.org/foreignkeys.html",
                       "accessed": "2026-11-16"}],
        "source_type": "official docs",
        "quote": "Indices are not required for child key columns but they are almost always beneficial.",
        "generated_by": "researchteam",
        "query": "sqlite foreign key index",
        "trust": {"score": 80, "basis": "primary vendor documentation, current"},
        "independence": "single",
    }
    c.update(overrides)
    return c


def research_md(headings=research.HEADINGS):
    return "# Keys: research\n\n" + "".join(f"{h}\n\nFindings.\n\n" for h in headings)


def write_research(folder, claims=None, md=None, verdicts=None):
    """research/ for `folder`; unless `verdicts` is given, one `supported`
    verdict rules on every claim."""
    d = folder / research.RESEARCH_DIR
    d.mkdir(exist_ok=True)
    doc = {"topic": "keys", "claims": [claim()] if claims is None else claims}
    if verdicts is None:
        verdicts = [{"rule": "must-index-keys", "verdict": "supported",
                     "claims": [c["id"] for c in doc["claims"]
                                if isinstance(c, dict) and research._ID.match(c.get("id") or "")]}]
    doc["verdicts"] = verdicts
    (d / research.RESEARCH_JSON).write_text(json.dumps(doc, indent=2), encoding="utf-8")
    (d / research.RESEARCH_MD).write_text(research_md() if md is None else md, encoding="utf-8")
    return d


def roled(tmp_path, monkeypatch, cite=" (claim: fk-index)", rel=TOPIC):
    """A cookbook with one complete roled guideline at `rel`, its rule citing `cite`."""
    monkeypatch.chdir(tmp_path)
    new_repo(tmp_path)
    folder = add_doc(tmp_path, rel, BODY.format(rules=RULE.format(cite=cite)), type="guideline")
    (folder.parent / f"{folder.name}.md").unlink()
    assert main(["roles", "set", str(folder), *[a for r in ROLES for a in ("--part", r)]]) == 0
    return tmp_path / "cookbook", folder


def validate(cb, capsys, monkeypatch):
    monkeypatch.setenv("COLUMNS", "300")
    capsys.readouterr()
    code = main(["validate", "-p", str(cb)])
    return code, capsys.readouterr().out


def kinds(cb, folder):
    return [(f.kind, f.detail) for f in research.census(cb, [folder])]


# --- the compile -------------------------------------------------------------------------

def test_compile_ignores_the_research_folder(tmp_path, monkeypatch, patch_refs, capsys):
    monkeypatch.chdir(tmp_path)
    new_repo(tmp_path)
    cb = tmp_path / "cookbook"
    folder = add_doc(tmp_path, "recipes/alpha", "# Alpha\n\nAlpha MUST be.\n\n## Change History\n\nx\n")
    doc = cb / "recipes" / "alpha.md"
    before = doc.read_text(encoding="utf-8")
    d = write_research(folder)
    # The research keeps a snapshot of the artifact it checked, frontmatter and all.
    (d / "existing-artifact.md").write_text(before, encoding="utf-8")

    assert main(["compile", str(folder)]) == 0
    assert doc.read_text(encoding="utf-8") == before
    assert main(["compile", "--target", "skill", "--out", str(tmp_path / "skills"), str(cb)]) == 0
    compiled = [p for p in (tmp_path / "skills").rglob("*") if p.is_file()]
    assert compiled and not any("research" in p.read_text(encoding="utf-8").lower()
                                or "research" in p.name for p in compiled)
    code, out = validate(cb, capsys, monkeypatch)
    assert code == 0, out
    assert "existing-artifact" not in out


def compiled_skills(tmp_path, cb):
    """{skill directory: its SKILL.md} of `cb` compiled to skills."""
    out = tmp_path / "skills"
    assert main(["compile", "--target", "skill", "--out", str(out), str(cb)]) == 0
    return {p.parent.name: p.read_text(encoding="utf-8") for p in out.rglob("SKILL.md")}


def test_compile_of_a_roled_artifact_ignores_its_research_folder(tmp_path, monkeypatch, patch_refs, capsys):
    cb, folder = roled(tmp_path, monkeypatch)
    d = write_research(folder, md=research_md().replace("Findings.", "Findings zzresearchtoken."))
    (d / "existing-artifact.md").write_text("---\ntitle: zzresearchtoken\n---\n\n# Keys\n", encoding="utf-8")
    skills = compiled_skills(tmp_path, cb)
    mine = {name: text for name, text in skills.items() if name.endswith("data-indexing")}
    assert len(mine) == 4, sorted(skills)
    assert not any("zzresearchtoken" in text for text in skills.values())
    assert not [p for p in (tmp_path / "skills").rglob("*") if "research" in p.name]
    code, out = validate(cb, capsys, monkeypatch)
    assert code == 0, out


def test_no_compiled_skill_carries_a_citation(tmp_path, monkeypatch, patch_refs):
    cb, folder = roled(tmp_path, monkeypatch, cite=" (claims: fk-index, fk-scan)")
    write_research(folder, claims=[claim(), claim("fk-scan")])
    add_doc(tmp_path, "recipes/alpha", "# Alpha\n\n## Requirements\n\n"
                                       "- **be**: Alpha MUST be. (claim: fk-index)\n\n## Change History\n\nx\n")
    skills = compiled_skills(tmp_path, cb)
    mine = {name: text for name, text in skills.items() if name.endswith("data-indexing")}
    assert len(mine) == 4, sorted(skills)
    rules = [text for text in mine.values() if "Every foreign key MUST have an index." in text]
    assert len(rules) >= 2
    alpha = [text for name, text in skills.items() if "alpha" in name]
    assert alpha and all("- **be**: Alpha MUST be.\n" in text for text in alpha)
    assert not [name for name, text in skills.items() if "(claim" in text]
    assert all("MUST have an index.\n" in text for text in rules)


# --- validate ----------------------------------------------------------------------------

def test_validate_refuses_an_artifact_without_research(tmp_path, monkeypatch, patch_refs, capsys):
    cb, folder = roled(tmp_path, monkeypatch)
    assert kinds(cb, folder) == [("no-research", "a roled artifact with no research/ folder")]
    code, out = validate(cb, capsys, monkeypatch)
    assert code == 1
    assert "no-research" in out and research.FIX["no-research"] in out

    write_research(folder)
    assert kinds(cb, folder) == []
    assert validate(cb, capsys, monkeypatch)[0] == 0


def test_an_unroled_artifact_without_research_is_left_alone(tmp_path, monkeypatch, patch_refs):
    monkeypatch.chdir(tmp_path)
    new_repo(tmp_path)
    folder = add_doc(tmp_path, "recipes/alpha", "# Alpha\n\n- **be**: Alpha MUST be.\n\n## Change History\n\nx\n")
    assert kinds(tmp_path / "cookbook", folder) == []


def test_an_exempt_topic_passes_until_its_research_lands(tmp_path, monkeypatch, patch_refs, capsys):
    cb, folder = roled(tmp_path, monkeypatch)
    (cb / research.EXEMPT_FILE).write_text(json.dumps({"why": "researched later", "topics": [TOPIC]}),
                                           encoding="utf-8")
    assert kinds(cb, folder) == []
    assert validate(cb, capsys, monkeypatch)[0] == 0

    write_research(folder)
    assert kinds(cb, folder) == [("stale-exemption", f"{TOPIC} is listed in {research.EXEMPT_FILE} "
                                                     "but has its research/ folder")]
    code, out = validate(cb, capsys, monkeypatch)
    assert code == 1 and TOPIC in out


def test_an_exemption_outside_the_21_is_refused(tmp_path, monkeypatch, patch_refs, capsys):
    # The list may only shrink: a topic written since must bring its research.
    cb, folder = roled(tmp_path, monkeypatch, rel=NEW_TOPIC)
    (cb / research.EXEMPT_FILE).write_text(json.dumps({"why": "x", "topics": [NEW_TOPIC]}), encoding="utf-8")
    assert kinds(cb, folder) == [
        ("no-research", "a roled artifact with no research/ folder"),
        ("unknown-exemption", f"{NEW_TOPIC} is listed in {research.EXEMPT_FILE} but is not one of the "
                              "21 topics exempted when research began; the list may only shrink"),
    ]
    code, out = validate(cb, capsys, monkeypatch)
    assert code == 1 and "unknown-exemption" in out and research.FIX["unknown-exemption"] in out


def test_an_exemption_naming_no_roled_artifact_is_refused(tmp_path, monkeypatch, patch_refs):
    cb, folder = roled(tmp_path, monkeypatch)
    write_research(folder)
    (cb / research.EXEMPT_FILE).write_text(json.dumps({"why": "x", "topics": ["guidelines/implementing/data/sync-tooling"]}),
                                           encoding="utf-8")
    assert kinds(cb, folder) == [("stale-exemption", "guidelines/implementing/data/sync-tooling is listed in "
                                                     f"{research.EXEMPT_FILE} but is no roled artifact")]


def test_validate_refuses_a_rule_citing_no_research_claim(tmp_path, monkeypatch, patch_refs, capsys):
    cb, folder = roled(tmp_path, monkeypatch, cite=" (claim: no-such-claim)")
    write_research(folder)
    assert kinds(cb, folder) == [("unknown-claim", "rule 'must-index-keys' cites 'no-such-claim', "
                                                   "which is no claim in research/research.json")]
    code, out = validate(cb, capsys, monkeypatch)
    assert code == 1 and "unknown-claim" in out and research.FIX["unknown-claim"] in out


def test_validate_refuses_a_rule_that_cites_nothing(tmp_path, monkeypatch, patch_refs):
    cb, folder = roled(tmp_path, monkeypatch, cite="")
    write_research(folder)
    assert kinds(cb, folder) == [("rule-cites-nothing", "rule 'must-index-keys' cites no research claim")]


def test_a_rule_may_cite_several_claims(tmp_path, monkeypatch, patch_refs):
    cb, folder = roled(tmp_path, monkeypatch, cite=" (claims: fk-index, fk-scan)")
    write_research(folder, claims=[claim(), claim("fk-scan")])
    assert kinds(cb, folder) == []


def test_a_citation_comes_at_the_end_of_its_rule(tmp_path, monkeypatch, patch_refs, capsys):
    cb, folder = roled(tmp_path, monkeypatch, cite=" (claim: fk-index) Unless the table is tiny.")
    write_research(folder)
    assert kinds(cb, folder) == [("citation-not-at-end", "rule 'must-index-keys' has a citation "
                                                         "before its end")]
    code, out = validate(cb, capsys, monkeypatch)
    assert code == 1 and research.FIX["citation-not-at-end"] in out


def test_every_cited_claim_has_a_verdict(tmp_path, monkeypatch, patch_refs, capsys):
    cb, folder = roled(tmp_path, monkeypatch, cite=" (claims: fk-index, fk-scan)")
    write_research(folder, claims=[claim(), claim("fk-scan"), claim("uncited")],
                   verdicts=[{"rule": "must-index-keys", "verdict": "supported", "claims": ["fk-index"]}])
    assert kinds(cb, folder) == [("unverdicted-claim", "rule 'must-index-keys' cites 'fk-scan', "
                                                       "which no verdict rules on")]
    code, out = validate(cb, capsys, monkeypatch)
    assert code == 1 and research.FIX["unverdicted-claim"] in out


def test_research_md_has_the_four_question_headings(tmp_path, monkeypatch, patch_refs, capsys):
    assert research.HEADINGS == (
        "## Best practices",
        "## Known solutions",
        "## Platform guidelines",
        "## The expert's view",
    )
    cb, folder = roled(tmp_path, monkeypatch)
    write_research(folder, md=research_md(research.HEADINGS[:3]))
    assert kinds(cb, folder) == [("missing-question", "research/research.md has no "
                                                      "\"## The expert's view\" heading")]
    code, out = validate(cb, capsys, monkeypatch)
    assert code == 1 and "missing-question" in out

    write_research(folder, md=research_md(research.HEADINGS[1:] + research.HEADINGS[:1]))
    assert kinds(cb, folder) == [("missing-question", "research/research.md puts its question headings "
                                                      "out of order")]


def test_research_needs_both_files(tmp_path, monkeypatch, patch_refs):
    cb, folder = roled(tmp_path, monkeypatch)
    (folder / research.RESEARCH_DIR).mkdir()
    assert kinds(cb, folder) == [("missing-research-file", "research/ has no research.json"),
                                 ("missing-research-file", "research/ has no research.md")]


def test_validate_refuses_a_claim_missing_its_provenance(tmp_path, monkeypatch, patch_refs):
    cb, folder = roled(tmp_path, monkeypatch)
    bad = claim(quote="", independence="lots", trust={"score": 120, "basis": "x"})
    del bad["query"]
    bad["citations"][0].pop("accessed")
    write_research(folder, claims=[bad])
    assert kinds(cb, folder) == [
        ("incomplete-claim", "claim 'fk-index': no 'quote'"),
        ("incomplete-claim", "claim 'fk-index': no 'query'"),
        ("incomplete-claim", "claim 'fk-index': citation 1 has no 'accessed'"),
        ("incomplete-claim", "claim 'fk-index': trust score 120 is not 0-100"),
        ("incomplete-claim", "claim 'fk-index': independence 'lots' is not one of "
                             "multi-independent, single, uncorroborated"),
    ]


def test_claim_ids_are_kebab_case_and_unique(tmp_path, monkeypatch, patch_refs):
    cb, folder = roled(tmp_path, monkeypatch)
    write_research(folder, claims=[claim(), claim(), claim("Not Kebab")])
    assert kinds(cb, folder) == [
        ("incomplete-claim", "claim 3: id 'Not Kebab' is not kebab-case"),
        ("duplicate-claim", "claim 'fk-index' appears 2 times"),
    ]


def test_a_verdict_is_one_of_four_and_cites_known_claims(tmp_path, monkeypatch, patch_refs):
    # A verdict may name a rule the write then drops or renames (a contradicted
    # one, say): the research records the rules as they stood when checked.
    cb, folder = roled(tmp_path, monkeypatch)
    write_research(folder, verdicts=[
        {"rule": "must-index-keys", "verdict": "supported", "claims": ["fk-index"]},
        {"rule": "gone-rule", "verdict": "contradicted", "claims": ["nope"]},
        {"rule": "must-index-keys", "verdict": "maybe"},
        {"verdict": "new", "claims": ["fk-index"]},
    ])
    assert kinds(cb, folder) == [
        ("bad-verdict", "verdict 2 cites 'nope', which is no claim"),
        ("bad-verdict", "verdict 3 is not one of supported, contradicted, unsupported, new"),
    ]


def test_unreadable_research_json(tmp_path, monkeypatch, patch_refs):
    cb, folder = roled(tmp_path, monkeypatch)
    d = write_research(folder)
    (d / research.RESEARCH_JSON).write_text("{not json", encoding="utf-8")
    assert [k for k, _ in kinds(cb, folder)] == ["unreadable-research"]


def test_an_unroled_artifact_with_research_cites_each_named_rule(tmp_path, monkeypatch, patch_refs):
    monkeypatch.chdir(tmp_path)
    new_repo(tmp_path)
    folder = add_doc(tmp_path, "recipes/alpha", "# Alpha\n\n## Requirements\n\n"
                                                "- **be**: Alpha MUST be. (claim: fk-index)\n"
                                                "- **stay**: Alpha SHOULD stay.\n\n## Change History\n\nx\n")
    write_research(folder)
    assert kinds(tmp_path / "cookbook", folder) == [("rule-cites-nothing", "rule 'stay' cites no research claim")]


def test_the_exemptions_are_pinned_to_the_21_data_topics():
    assert research.EXEMPT_TOPICS == THE_21


def test_the_cookbooks_exemption_list_names_only_roled_topics_without_research():
    """The cookbook's own list: some of the 21 data topics, each once, each
    roled and without research yet. Task P2 empties it as each topic's
    research lands; nothing is ever added."""
    from pathlib import Path
    cb = Path(__file__).resolve().parents[5] / "cookbook"
    exempt = cb / research.EXEMPT_FILE
    if not exempt.is_file():
        pytest.skip("not run from the cookbook's own checkout")
    topics = json.loads(exempt.read_text(encoding="utf-8"))["topics"]
    assert len(topics) == len(set(topics))
    assert set(topics) <= THE_21, sorted(set(topics) - THE_21)
    assert [(f.kind, f.detail) for f in research.census(cb, [cb / t for t in topics])] == []


# --- rules the research could not support: kept, cited, and left to the owner -------------

def prior(cid="must-index-keys-prior"):
    """A rule the research could not support, recorded as a claim whose source
    is the cookbook's own text at the topic's base commit."""
    return claim(cid, claim="Every foreign key MUST have an index (the cookbook's rule before research).",
                 citations=[{"title": "indexing (rules part)", "author": "Agentic Developer Cookbook",
                             "publisher": "agenticcookbook", "date": "n.d.",
                             "url": f"git:abc1234:cookbook/{TOPIC}/rules.md", "accessed": "2026-11-16"}],
                 source_type="prior cookbook text",
                 quote="Every foreign key MUST have an index.",
                 trust={"score": 0, "basis": "no research source supports it"},
                 independence="uncorroborated")


@pytest.mark.parametrize("verdict", ["unsupported", "contradicted"])
def test_a_kept_rule_the_research_does_not_support_passes_with_a_warning(
        verdict, tmp_path, monkeypatch, patch_refs, capsys):
    cb, folder = roled(tmp_path, monkeypatch, cite=" (claim: must-index-keys-prior)")
    write_research(folder, claims=[prior()],
                   verdicts=[{"rule": "must-index-keys", "verdict": verdict,
                              "claims": ["must-index-keys-prior"]}])
    assert kinds(cb, folder) == []
    assert [(f.kind, f.detail) for f in research.owner_rules(cb, [folder])] == [
        ("owner-decides", f"rule 'must-index-keys' cites 'must-index-keys-prior', which the research "
                          f"rules {verdict}")]
    code, out = validate(cb, capsys, monkeypatch)
    assert code == 0 and "owner-decides" in out and "must-index-keys-prior" in out
    assert "Validation passed." in out


def test_a_supported_rule_is_left_to_no_one(tmp_path, monkeypatch, patch_refs):
    cb, folder = roled(tmp_path, monkeypatch)
    write_research(folder)
    assert research.owner_rules(cb, [folder]) == []


FEATURE_FLAGS = Path(__file__).resolve().parent.parent / "fixtures" / "research" / "feature-flags"


def test_only_prior_rules_the_research_could_not_support_go_to_the_owner(
        tmp_path, monkeypatch, patch_refs):
    """The /grow-cookbook trial's feature-flags draft 1 against its research:
    nine rules cite a claim inside an unsupported or contradicted verdict (twelve
    pairs), but only four of them cite the prior cookbook text that verdict
    records. Those four, and only those, are the owner's to decide; a new rule
    citing a research claim of the same verdict is the author's and the reviewer's."""
    monkeypatch.chdir(tmp_path)
    new_repo(tmp_path)
    rules = (FEATURE_FLAGS / "rules.md").read_text(encoding="utf-8")
    folder = add_doc(tmp_path, NEW_TOPIC, BODY.format(rules=rules), type="guideline")
    (folder.parent / f"{folder.name}.md").unlink()
    assert main(["roles", "set", str(folder), *[a for r in ROLES for a in ("--part", r)]]) == 0
    (folder / research.RESEARCH_DIR).mkdir()
    (folder / research.RESEARCH_DIR / research.RESEARCH_JSON).write_bytes(
        (FEATURE_FLAGS / "research.json").read_bytes())
    found = research.owner_rules(tmp_path / "cookbook", [folder])
    assert sorted({f.detail.split("'")[1] for f in found}) == [
        "fail-fast-on-missing-config", "gate-all-features", "kotlin-sharedpreferences-default",
        "spec-lists-flag-keys"]
    assert all(f.detail.split("'")[3].endswith("-prior") for f in found)


def test_a_new_rule_citing_research_in_an_unsupported_verdict_is_not_the_owners(
        tmp_path, monkeypatch, patch_refs):
    cb, folder = roled(tmp_path, monkeypatch)
    write_research(folder, claims=[claim(), prior()],
                   verdicts=[{"rule": "must-index-keys", "verdict": "unsupported",
                              "claims": ["must-index-keys-prior", "fk-index"]}])
    assert research.owner_rules(cb, [folder]) == []


def test_every_verdict_names_a_claim(tmp_path, monkeypatch, patch_refs):
    cb, folder = roled(tmp_path, monkeypatch)
    write_research(folder, verdicts=[
        {"rule": "must-index-keys", "verdict": "supported", "claims": ["fk-index"]},
        {"rule": "old-rule", "verdict": "unsupported", "claims": []},
    ])
    assert kinds(cb, folder) == [("bad-verdict", "verdict 2 names no claim")]


# --- the research-only check (end of stage 2) ---------------------------------------------

def research_only(cb, folder, capsys, monkeypatch):
    monkeypatch.setenv("COLUMNS", "300")
    capsys.readouterr()
    code = main(["validate", "-p", str(cb), "--research", str(folder)])
    return code, capsys.readouterr().out


def test_the_research_only_check_ignores_the_rules(tmp_path, monkeypatch, patch_refs, capsys):
    # At the end of stage 2 the rules do not cite the research yet.
    cb, folder = roled(tmp_path, monkeypatch, cite="")
    write_research(folder)
    code, out = research_only(cb, folder, capsys, monkeypatch)
    assert code == 0 and "rule-cites-nothing" not in out and "Research passed" in out


def test_the_research_only_check_refuses_bad_research(tmp_path, monkeypatch, patch_refs, capsys):
    cb, folder = roled(tmp_path, monkeypatch, cite="")
    write_research(folder, claims=[claim(independence="lots")])
    code, out = research_only(cb, folder, capsys, monkeypatch)
    assert code == 1 and "incomplete-claim" in out and "rule-cites-nothing" not in out


def test_the_research_only_check_needs_the_research(tmp_path, monkeypatch, patch_refs, capsys):
    cb, folder = roled(tmp_path, monkeypatch, cite="", rel=NEW_TOPIC)
    code, out = research_only(cb, folder, capsys, monkeypatch)
    assert code == 1 and "no-research" in out


def test_the_research_only_check_names_a_path_that_is_no_artifact(tmp_path, monkeypatch, patch_refs, capsys):
    # A typo is the path's fault, not the research's: exit 2 naming it, never no-research.
    cb, folder = roled(tmp_path, monkeypatch, cite="")
    write_research(folder)
    capsys.readouterr()
    code = main(["validate", "-p", str(cb), "--research", str(folder.parent / "indexng")])
    cap = capsys.readouterr()
    assert code == 2 and "indexng" in cap.out + cap.err and "no-research" not in cap.out + cap.err


def test_the_research_only_check_reports_a_topic_still_exempt(tmp_path, monkeypatch, patch_refs, capsys):
    cb, folder = roled(tmp_path, monkeypatch, cite="")
    write_research(folder)
    (cb / research.EXEMPT_FILE).write_text(json.dumps({"why": "x", "topics": [TOPIC]}), encoding="utf-8")
    code, out = research_only(cb, folder, capsys, monkeypatch)
    assert code == 1 and "stale-exemption" in out
