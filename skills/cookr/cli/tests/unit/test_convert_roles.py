"""`cookr roles set|check|lossless` (modules/convert_roles.py, core/rolework.py)."""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from cookr.cli import main
from cookr.core.artifact import Artifact, Part, load_folder, write_folder

pytestmark = pytest.mark.usefixtures("git_tmp_path")

RULES = "\n- **must-index-foreign-keys**: Every foreign key MUST have an index.\n\n"
BAR = "\n- `must-index-foreign-keys`: every foreign key is indexed.\n\n"


def _topic(root, rel="cookbook/guidelines/implementing/data/t", roled=True):
    parts = [
        Part("intro", "# T\n\nIndexes keep reads fast. Joins need them.\n\n"),
        Part("rules", RULES, "Rules", "rules" if roled else None),
        Part("covering", "\nA covering index holds every column. It avoids the table.\n\n",
             "Covering Indexes", "how-to" if roled else None),
        Part("focus", "\nLook at the joins.\n\n", "Review focus", "review-focus" if roled else None),
        Part("review-bar", "\nFlag an unindexed key.\n\n", "Review bar", "review-bar" if roled else None),
        Part("build-bar", BAR, "Build bar", "build-bar" if roled else None),
        Part("history", "\n| Version | Date | Author | Summary |\n|---|---|---|---|\n"
                        "| 1.0.0 | 2026-01-01 | A | first |\n", "Change History"),
    ]
    folder = root / rel
    write_folder(Artifact(meta={"id": "6f1c1e2a-0000-4000-8000-000000000001", "type": "guideline",
                                "title": "T", "version": "1.0.0", "modified": "2026-01-01"},
                          parts=parts), folder)
    return folder


def _commit(root):
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=T", "-c", "user.email=t@t",
                    "commit", "-qm", "base"], check=True, capture_output=True)
    return subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], check=True,
                          capture_output=True, text=True).stdout.strip()


def _json(capsys):
    return json.loads(capsys.readouterr().out)


# ── lossless ────────────────────────────────────────────────────────────────

def test_lossless_names_a_dropped_sentence(tmp_path, capsys):
    folder = _topic(tmp_path)
    base = _commit(tmp_path)
    (folder / "covering.md").write_text("\nA covering index holds every column.\n\n", encoding="utf-8")
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base]) == 1
    out = _json(capsys)
    assert out["missing"] == ["It avoids the table."]


# debug-mode's intro.md at the /grow-cookbook trial's base (2071c94): its text
# twice, the copies split by a thematic break and a heading restating the title.
DEBUG_MODE_BASE = """# Debug mode

Apps MUST include a debug-only configuration panel (not in release builds):

- Feature flag overrides
- Analytics event log
- A/B test variant picker
- Environment info (version, build, OS, device)

Access methods:
- **Apple (iOS)**: Shake gesture, guarded by `#if DEBUG`
- **Apple (macOS)**: Debug menu item, guarded by `#if DEBUG`
- **Android**: Shake gesture, guarded by `BuildConfig.DEBUG`
- **Web**: `/debug` route, guarded by `NODE_ENV === 'development'`
- **Windows**: Debug-only settings page, guarded by `#if DEBUG`

---

# Debug Mode

Apps MUST include a debug-only configuration panel (not in release builds) with:

- Feature flag overrides
- Analytics event log
- A/B test variant picker
- Environment info (version, build, OS, device)
"""


def test_lossless_ignores_markdown_only_lines_of_the_debug_mode_base(tmp_path, capsys):
    # A thematic break and a heading that only restates the title say nothing:
    # dropping them loses nothing. The duplicate's one different sentence still counts.
    folder = _topic(tmp_path)
    artifact = load_folder(folder)
    artifact.meta["title"] = "Debug mode"
    write_folder(artifact, folder)
    (folder / "intro.md").write_text(DEBUG_MODE_BASE, encoding="utf-8")
    base = _commit(tmp_path)
    (folder / "intro.md").write_text(DEBUG_MODE_BASE.split("\n---\n")[0], encoding="utf-8")
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base]) == 1
    assert _json(capsys)["missing"] == [
        "Apps MUST include a debug-only configuration panel (not in release builds) with:"]


def test_lossless_ignores_a_heading_restating_the_title_the_base_had(tmp_path, capsys):
    # A renamed artifact: its base heading restates the old title, which the
    # current meta no longer holds; dropping it still loses nothing (M4).
    folder = _topic(tmp_path)
    artifact = load_folder(folder)
    artifact.meta["title"] = "Old name"
    write_folder(artifact, folder)
    (folder / "intro.md").write_text("# Old name\n\nIndexes keep reads fast. Joins need them.\n\n",
                                     encoding="utf-8")
    base = _commit(tmp_path)
    artifact = load_folder(folder)
    artifact.meta["title"] = "New name"
    write_folder(artifact, folder)
    (folder / "intro.md").write_text("# New name\n\nIndexes keep reads fast. Joins need them.\n\n",
                                     encoding="utf-8")
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base]) == 0
    assert _json(capsys)["missing"] == []


def test_lossless_still_counts_a_heading_that_is_not_the_title(tmp_path, capsys):
    folder = _topic(tmp_path)
    (folder / "intro.md").write_text("# T\n\n## Joins\n\nIndexes keep reads fast. Joins need them.\n\n",
                                     encoding="utf-8")
    base = _commit(tmp_path)
    (folder / "intro.md").write_text("# T\n\nIndexes keep reads fast. Joins need them.\n\n", encoding="utf-8")
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base]) == 1
    assert _json(capsys)["missing"] == ["## Joins"]


def test_lossless_passes_a_sentence_moved_between_parts(tmp_path, capsys):
    folder = _topic(tmp_path)
    base = _commit(tmp_path)
    (folder / "covering.md").write_text("\nA covering index holds every column.\n\n", encoding="utf-8")
    (folder / "focus.md").write_text("\nLook at the joins.\n\n- It avoids the table.\n", encoding="utf-8")
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base]) == 0
    assert _json(capsys)["missing"] == []


def test_lossless_ignores_a_rules_citation(tmp_path, capsys):
    # A rule that gains its research citation still says what it said.
    folder = _topic(tmp_path)
    base = _commit(tmp_path)
    (folder / "rules.md").write_text(RULES.replace("an index.", "an index. (claims: fk-index, fk-scan)"),
                                     encoding="utf-8")
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base]) == 0
    assert _json(capsys)["missing"] == []


def test_lossless_checks_a_folded_copy_named_with_copy(tmp_path, capsys):
    folder = _topic(tmp_path)
    copy = _topic(tmp_path, "cookbook/guidelines/planning/data/t", roled=False)
    (copy / "covering.md").write_text("\nOnly the copy says this.\n\n", encoding="utf-8")
    base = _commit(tmp_path)
    shutil.rmtree(copy)                       # folded away since the base
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base, "--copy", str(copy)]) == 1
    assert _json(capsys)["missing"] == ["Only the copy says this."]


COVER_RULE = ("\n- **must-index-foreign-keys**: Every foreign key MUST have an index.\n"
              "- **should-use-a-covering-index**: A hot query SHOULD use a covering index: it "
              "avoids the table entirely.\n\n")


def _reword(folder, to, base="HEAD"):
    """Drop "It avoids the table." from `covering` (its base sentence), give it
    a rule that carries it reworded, and map it to `to` in lossless.json."""
    (folder / "covering.md").write_text("\nA covering index holds every column.\n\n", encoding="utf-8")
    (folder / "rules.md").write_text(COVER_RULE, encoding="utf-8")
    (folder / "build-bar.md").write_text(BAR.rstrip() + "\n- `should-use-a-covering-index`: hot "
                                         "queries use a covering index.\n\n", encoding="utf-8")
    (folder / "lossless.json").write_text(json.dumps(
        {"base": base, "moved": [{"sentence": "It avoids the table.", "to": to}]}), encoding="utf-8")


def test_lossless_passes_a_reworded_sentence_mapped_to_its_rule(tmp_path, capsys):
    folder = _topic(tmp_path)
    base = _commit(tmp_path)
    _reword(folder, "should-use-a-covering-index", base[:7])
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base, "--draft"]) == 0
    out = _json(capsys)
    assert out["missing"] == [] and out["failures"] == []
    # "It avoids the table." sits inside a longer sentence of the rule: reworded, not verbatim
    assert out["moved"] == [{"sentence": "It avoids the table.", "to": "should-use-a-covering-index"}]


def test_lossless_fails_a_mapping_to_a_missing_rule(tmp_path, capsys):
    folder = _topic(tmp_path)
    base = _commit(tmp_path)
    _reword(folder, "should-use-a-covering-indx", base[:7])
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base]) == 1
    [failure] = _json(capsys)["failures"]
    assert failure["sentence"] == "It avoids the table." and failure["to"] == "should-use-a-covering-indx"
    assert "no rule or non-rule part named" in failure["reason"]


def test_lossless_fails_a_mapping_whose_rule_lacks_the_content(tmp_path, capsys):
    folder = _topic(tmp_path)
    base = _commit(tmp_path)
    _reword(folder, "must-index-foreign-keys", base[:7])
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base]) == 1
    [failure] = _json(capsys)["failures"]
    assert failure["to"] == "must-index-foreign-keys" and "content words" in failure["reason"]


def test_lossless_maps_to_a_non_rule_part_by_its_best_line_and_never_to_the_rules_part(tmp_path, capsys):
    folder = _topic(tmp_path)
    base = _commit(tmp_path)
    _reword(folder, "covering", base[:7])
    (folder / "covering.md").write_text("\nA covering index holds every column.\n\nUsed well, it "
                                        "avoids the table entirely.\n\n", encoding="utf-8")
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base, "--draft"]) == 0
    _reword(folder, "rules", base[:7])
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base]) == 1
    assert "no rule or non-rule part named 'rules'" in _json(capsys)["failures"][0]["reason"]


def _account(folder, base, *moved):
    (folder / "lossless.json").write_text(json.dumps(
        {"base": base, "moved": [{"sentence": m, "to": t} for m, t in moved]}), encoding="utf-8")


def test_lossless_reads_a_list_of_targets_together(tmp_path, capsys):
    folder = _topic(tmp_path)
    (folder / "covering.md").write_text("\nA covering index holds every column. It avoids the table, "
                                        "and keys MUST be indexed.\n\n", encoding="utf-8")
    base = _commit(tmp_path)
    (folder / "covering.md").write_text("\nA covering index holds every column. It avoids the "
                                        "table.\n\n", encoding="utf-8")
    sentence = "It avoids the table, and keys MUST be indexed."
    _account(folder, base, (sentence, "covering"))
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base]) == 1
    _account(folder, base, (sentence, ["covering", "must-index-foreign-keys"]))
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base, "--draft"]) == 0


def test_lossless_passes_a_bare_lead_in_mapped_to_its_rule_and_marks_it(tmp_path, capsys):
    folder = _topic(tmp_path)
    (folder / "rules.md").write_text("\n**Rules for foreign keys:**\n" + RULES.lstrip("\n"),
                                     encoding="utf-8")
    base = _commit(tmp_path)
    (folder / "rules.md").write_text(RULES, encoding="utf-8")
    _account(folder, base, ("**Rules for foreign keys:**", "covering"))
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base]) == 1   # a lead-in maps to rules
    _account(folder, base, ("**Rules for foreign keys:**", "must-index-foreign-keys"))
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base, "--draft"]) == 0
    assert _json(capsys)["moved"] == [{"sentence": "**Rules for foreign keys:**",
                                       "to": "must-index-foreign-keys", "lead_in": True}]


def _moved(tmp_path, capsys, sentence, rule, *, extra_rules="", rationale=None, to=None, draft=True):
    """Base: `sentence` in the covering part. Now: it is gone and the rules part
    holds `- **r**: <rule>` (plus `extra_rules`); lossless.json maps it to `to`
    (default "r"). The lossless exit code and output, run as a `--draft` (the
    tripwires, without a judge) unless `draft` is False."""
    folder = _topic(tmp_path)
    (folder / "covering.md").write_text(f"\nA covering index holds every column. {sentence}\n\n",
                                        encoding="utf-8")
    (folder / "rules.md").write_text(RULES + extra_rules, encoding="utf-8")
    base = _commit(tmp_path)
    (folder / "covering.md").write_text("\nA covering index holds every column.\n\n", encoding="utf-8")
    (folder / "rules.md").write_text(RULES + extra_rules + f"- **r**: {rule}\n\n", encoding="utf-8")
    if rationale is not None:
        art = load_folder(folder)
        at = next(i for i, p in enumerate(art.parts) if p.name == "history")
        art.parts.insert(at, Part("rationale", rationale, "Rationale", "rationale"))
        write_folder(art, folder)
    _account(folder, base, (sentence, to or "r"))
    capsys.readouterr()
    code = main(["roles", "lossless", str(folder), "--base", base, *(["--draft"] if draft else [])])
    return code, _json(capsys)


def test_lossless_fails_must_not_turned_must(tmp_path, capsys):
    code, out = _moved(tmp_path, capsys,
                       "Synced tables MUST NOT use INTEGER PRIMARY KEY AUTOINCREMENT on any device.",
                       "Synced tables MUST use INTEGER PRIMARY KEY AUTOINCREMENT on any device.")
    assert code == 1
    reason = out["failures"][0]["reason"]
    assert "its negation" in reason and "MUST NOT" in reason


def test_lossless_fails_a_dropped_never(tmp_path, capsys):
    sentence = "Never hold a write transaction open while waiting on network I/O."
    code, out = _moved(tmp_path, capsys, sentence,
                       "SHOULD hold a write transaction open while waiting on network I/O.")
    assert code == 1 and "its negation" in out["failures"][0]["reason"]
    code, out = _moved(tmp_path / "ok", capsys, sentence,   # never → MUST NOT keeps it
                       "MUST NOT hold a write transaction open while waiting on network I/O.")
    assert code == 0, out


def test_lossless_fails_must_turned_may(tmp_path, capsys):
    code, out = _moved(tmp_path, capsys,
                       "Every sync system MUST have an explicit conflict resolution strategy.",
                       "Every sync system MAY have an explicit conflict resolution strategy.")
    assert code == 1 and "its MUST" in out["failures"][0]["reason"]


def test_lossless_fails_a_changed_number(tmp_path, capsys):
    code, out = _moved(tmp_path, capsys,
                       "Alert when free_bytes / total_bytes exceeds 25% — that is a signal to VACUUM.",
                       "Alert when free_bytes / total_bytes exceeds 75% — that is a signal to VACUUM.")
    assert code == 1 and "the number(s) 25%" in out["failures"][0]["reason"]


WAL_RULES = ("- **should-not-disable-auto-checkpoint-without-replacement**: SHOULD NOT disable "
             "auto-checkpointing without a manual replacement.\n"
             "- **should-not-hold-long-read-transactions**: SHOULD NOT run long-running read "
             "transactions that prevent checkpoint completion.\n"
             "- **should-not-run-very-large-write-transactions**: SHOULD NOT run very large write "
             "transactions that block the checkpoint.\n")
WAL_NAMES = ["should-not-disable-auto-checkpoint-without-replacement",
             "should-not-hold-long-read-transactions", "should-not-run-very-large-write-transactions"]


def test_lossless_fails_a_lead_in_whose_rules_lost_its_reason(tmp_path, capsys):
    lead = "Three causes of WAL growth to avoid:"
    code, out = _moved(tmp_path, capsys, lead, "SHOULD cap WAL file size.",
                       extra_rules=WAL_RULES, to=WAL_NAMES)
    assert code == 1
    assert "wal" in out["failures"][0]["reason"] and "growth" in out["failures"][0]["reason"]
    why = "".join(f"- `{n}`: It is one of three causes of WAL growth to avoid.\n" for n in WAL_NAMES)
    code, out = _moved(tmp_path / "ok", capsys, lead, "SHOULD cap WAL file size.",
                       extra_rules=WAL_RULES, rationale="\n" + why + "\n", to=WAL_NAMES)
    assert code == 0, out
    assert out["moved"] == [{"sentence": lead, "to": WAL_NAMES, "lead_in": True}]


def test_a_normative_sentence_ending_in_a_colon_gets_no_lead_in_pass(tmp_path, capsys):
    code, out = _moved(tmp_path, capsys, "MUST NOT store secrets in plaintext columns:",
                       "SHOULD cap WAL file size.", to="must-index-foreign-keys")
    assert code == 1 and out["moved"] == []
    assert "content words" in out["failures"][0]["reason"]


def test_lossless_fails_inverted_text_hidden_in_a_large_part(tmp_path, capsys):
    folder = _topic(tmp_path)
    sentence = "Do not store counts, totals, or derived booleans as columns."
    (folder / "covering.md").write_text(f"\nA covering index holds every column. {sentence}\n\n",
                                        encoding="utf-8")
    base = _commit(tmp_path)
    (folder / "covering.md").write_text(
        "\nA covering index holds every column.\n\n- Store counts and totals in a cache table.\n"
        "- Derived booleans are not columns.\n- Do store them as columns.\n\n", encoding="utf-8")
    _account(folder, base, (sentence, "covering"))
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base]) == 1
    assert "content words" in _json(capsys)["failures"][0]["reason"]


def test_lossless_judges_a_code_only_part_by_its_best_line_too(tmp_path, capsys):
    folder = _topic(tmp_path)
    sentence = "Do not store counts, totals, or derived booleans as columns."
    (folder / "covering.md").write_text(f"\n{sentence}\n\n", encoding="utf-8")
    base = _commit(tmp_path)
    (folder / "covering.md").write_text(
        "\n```\n-- store counts and totals in a cache table\n"
        "-- derived booleans are not columns\n-- do store them as columns\n```\n\n", encoding="utf-8")
    _account(folder, base, (sentence, "covering"))
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base]) == 1
    assert "content words" in _json(capsys)["failures"][0]["reason"]


def test_lossless_counts_a_sentence_kept_as_a_named_rule_or_rationale_bullet(tmp_path, capsys):
    folder = _topic(tmp_path)
    (folder / "covering.md").write_text("\nA covering index holds every column. Synced tables MUST "
                                        "use UUIDs. It avoids the table.\n\n", encoding="utf-8")
    base = _commit(tmp_path)
    (folder / "covering.md").write_text("\nA covering index holds every column.\n\n", encoding="utf-8")
    (folder / "rules.md").write_text(RULES + "- **r**: Synced tables MUST use UUIDs.\n\n", encoding="utf-8")
    art = load_folder(folder)
    at = next(i for i, p in enumerate(art.parts) if p.name == "history")
    art.parts.insert(at, Part("rationale", "\n- `r`, `r2`: It avoids the table.\n\n", "Rationale",
                              "rationale"))
    write_folder(art, folder)
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base]) == 0
    assert _json(capsys)["missing"] == []


def test_lossless_caps_a_mapping_at_three_targets(tmp_path, capsys):
    code, out = _moved(tmp_path, capsys, "Synced tables MUST use UUIDs.", "Every synced table MUST use UUIDs.",
                       extra_rules=WAL_RULES, to=["r", *WAL_NAMES])
    assert code == 1 and "at most 3" in out["failures"][0]["reason"]


def test_lossless_counts_a_sentence_kept_only_when_it_is_whole(tmp_path, capsys):
    folder = _topic(tmp_path)
    base = _commit(tmp_path)
    (folder / "covering.md").write_text("\nA covering index holds every column. Not always: It avoids "
                                        "the table.\n\n", encoding="utf-8")
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base]) == 1
    assert _json(capsys)["missing"] == ["It avoids the table."]


def test_overlap_matches_whole_words_only():
    from cookr.core.rolework import overlap
    assert overlap("Use it.", "Reuse items.") < 0.8
    assert overlap("Use it.", "You may use it today.") == 1.0


def _obsolete(folder, base, sentence, reason):
    (folder / "lossless.json").write_text(json.dumps(
        {"base": base, "moved": [], "obsolete": [{"sentence": sentence, "reason": reason}]}),
        encoding="utf-8")


def _from_copy(tmp_path, sentence):
    """Base: the topic, and a copy whose covering part holds `sentence`. The
    topic's lossless.json names the copy and declares `sentence` obsolete.
    The topic folder and the base commit."""
    folder = _topic(tmp_path)
    rel = "cookbook/guidelines/planning/data/t"
    copy = _topic(tmp_path, rel, roled=False)
    (copy / "covering.md").write_text(f"\n{sentence}\n\n", encoding="utf-8")
    base = _commit(tmp_path)
    shutil.rmtree(copy)                       # folded away since the base
    (folder / "lossless.json").write_text(json.dumps(
        {"base": base, "copies": [rel], "moved": [],
         "obsolete": [{"sentence": sentence, "reason": "points at the copy folded into this topic"}]}),
        encoding="utf-8")
    return folder, base


def test_lossless_shows_an_obsolete_sentence_and_passes(tmp_path, capsys):
    sentence = "See the implementing copy of this guideline for detailed examples."
    folder, base = _from_copy(tmp_path, sentence)
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base, "--draft"]) == 0
    captured = capsys.readouterr()
    assert json.loads(captured.out)["obsolete"] == [
        {"sentence": sentence, "reason": "points at the copy folded into this topic"}]
    assert "obsolete: " in captured.err and sentence in captured.err


def test_lossless_refuses_an_obsolete_sentence_that_states_a_rule(tmp_path, capsys):
    folder = _topic(tmp_path)
    sentence = "See the implementing copy; it MUST be read first."
    (folder / "covering.md").write_text(f"\nA covering index holds every column. {sentence}\n\n",
                                        encoding="utf-8")
    base = _commit(tmp_path)
    (folder / "covering.md").write_text("\nA covering index holds every column.\n\n", encoding="utf-8")
    _obsolete(folder, base, sentence, "points at the copy")
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base]) == 1
    out = _json(capsys)
    assert out["obsolete"] == [] and "never obsolete" in out["failures"][0]["reason"]


def test_lossless_fails_an_accounting_for_another_base(tmp_path, capsys):
    folder = _topic(tmp_path)
    base = _commit(tmp_path)
    _reword(folder, "should-use-a-covering-index", base)
    other = _commit(tmp_path)
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", other]) == 1
    assert "accounts for base" in _json(capsys)["failures"][0]["reason"]
    assert main(["roles", "lossless", str(folder), "--base", base, "--draft"]) == 0


def test_lossless_json_never_reaches_a_compiled_skill_or_doc(tmp_path):
    folder = _topic(tmp_path)
    _reword(folder, "should-use-a-covering-index")
    (folder / "lossless.json").write_text(json.dumps(
        {"base": "base", "moved": [{"sentence": "ZZ-ACCOUNTING-MARKER", "to": "rules"}]}), encoding="utf-8")
    out = tmp_path / "out"
    assert main(["compile", "--target", "skill", "--out", str(out), str(folder)]) == 0
    assert main(["compile", str(folder)]) == 0
    built = [f for f in out.rglob("*") if f.is_file()] + [folder.parent / "t.md"]
    assert any(f.name == "SKILL.md" for f in built)
    for f in built:
        assert f.name != "lossless.json"
        assert "ZZ-ACCOUNTING-MARKER" not in f.read_text(encoding="utf-8")


# ── set ─────────────────────────────────────────────────────────────────────

def test_set_gives_named_parts_roles_and_clears_with_none(tmp_path, capsys):
    folder = _topic(tmp_path, roled=False)
    assert main(["roles", "set", str(folder), "--part", "rules=rules", "--part", "covering=how-to",
                 "--part", "focus=review-focus", "--part", "review-bar=review-bar",
                 "--part", "build-bar=build-bar"]) == 0
    art = load_folder(folder)
    assert {p.name: p.role for p in art.parts} == {
        "intro": None, "rules": "rules", "covering": "how-to", "focus": "review-focus",
        "review-bar": "review-bar", "build-bar": "build-bar", "history": None}
    capsys.readouterr()
    assert main(["roles", "set", str(folder), "--part", "covering=none"]) == 0
    out = _json(capsys)
    assert load_folder(folder).part("covering").role is None
    assert out["findings"] == [{"kind": "unroled-part", "detail": "part 'covering' has no role"}]


@pytest.mark.parametrize("spec", ["nope=rules", "rules=tips", "intro=rules", "rules"])
def test_set_refuses_an_unknown_part_or_role_and_writes_nothing(tmp_path, spec):
    folder = _topic(tmp_path, roled=False)
    before = (folder / "artifact.json").read_text()
    assert main(["roles", "set", str(folder), "--part", spec]) != 0
    assert (folder / "artifact.json").read_text() == before


# ── check ───────────────────────────────────────────────────────────────────

def test_check_reports_the_four_skills_of_a_complete_topic(tmp_path, capsys):
    folder = _topic(tmp_path)
    capsys.readouterr()
    assert main(["roles", "check", str(folder)]) == 0
    out = _json(capsys)
    assert out["ok"] is True and out["findings"] == [] and out["rules"] == 1
    assert {s["kind"]: s["name"] for s in out["skills"]} == {
        "builder": "implementing-data-t", "build-verifier": "verifying-build-data-t",
        "reviewer": "reviewing-data-t", "review-verifier": "verifying-review-data-t"}
    assert all(s["chars"] > 0 for s in out["skills"])


def test_check_fails_naming_the_census_findings(tmp_path, capsys):
    folder = _topic(tmp_path)
    main(["roles", "set", str(folder), "--part", "covering=none"])
    capsys.readouterr()
    assert main(["roles", "check", str(folder)]) == 1
    out = _json(capsys)
    assert out["ok"] is False and out["skills"] == []
    assert out["findings"] == [{"kind": "unroled-part", "detail": "part 'covering' has no role"}]


def test_check_fails_an_unroled_topic(tmp_path, capsys):
    folder = _topic(tmp_path, roled=False)
    capsys.readouterr()
    assert main(["roles", "check", str(folder)]) == 1
    assert _json(capsys)["findings"][0]["kind"] == "not-roled"


FRAMED = ("- **must-put-equality-columns-first**: In a composite index, equality columns MUST go first.\n"
          "- **must-put-inequality-columns-last**: In a composite index, inequality columns MUST go "
          "last.\n")
FRAMED_NAMES = ["must-put-equality-columns-first", "must-put-inequality-columns-last"]


def test_a_framing_lead_in_passes_when_every_rule_has_its_level(tmp_path, capsys):
    code, out = _moved(tmp_path, capsys, "**MUST follow:**", "SHOULD cap WAL file size.",
                       extra_rules=FRAMED, to=FRAMED_NAMES)
    assert code == 0, out
    assert out["moved"] == [{"sentence": "**MUST follow:**", "to": FRAMED_NAMES, "framing": True}]


def test_a_framing_lead_in_fails_when_a_rule_has_a_weaker_level(tmp_path, capsys):
    weaker = FRAMED.replace("inequality columns MUST go", "inequality columns SHOULD go")
    code, out = _moved(tmp_path, capsys, "**MUST follow:**", "SHOULD cap WAL file size.",
                       extra_rules=weaker, to=FRAMED_NAMES)
    assert code == 1 and out["moved"] == []
    reason = out["failures"][0]["reason"]
    assert "must-put-inequality-columns-last" in reason and "MUST" in reason


def test_a_framing_lead_in_still_needs_its_own_words(tmp_path, capsys):
    lead = "MUST follow these rules for any migration in a sync-capable schema:"
    code, out = _moved(tmp_path, capsys, lead, "SHOULD cap WAL file size.",
                       extra_rules=FRAMED, to=FRAMED_NAMES)
    assert code == 1 and "migration" in out["failures"][0]["reason"]


def test_a_lead_in_may_list_more_than_three_rules(tmp_path, capsys):
    names = [f"must-do-sync-migration-step-{n}" for n in ("one", "two", "three", "four", "five")]
    rules = "".join(f"- **{n}**: A sync-compatible migration MUST do step {n.rsplit('-', 1)[1]}.\n"
                    for n in names)
    lead = "Rules for sync-compatible migrations:"
    code, out = _moved(tmp_path, capsys, lead, "SHOULD cap WAL file size.", extra_rules=rules, to=names)
    assert code == 0, out
    assert out["moved"] == [{"sentence": lead, "to": names, "lead_in": True}]


def test_an_unused_accounting_entry_fails(tmp_path, capsys):
    folder = _topic(tmp_path)
    base = _commit(tmp_path)
    _account(folder, base, ("A covering index holds every column.", "must-index-foreign-keys"))
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base]) == 1
    out = _json(capsys)
    assert out["unused"] == [{"sentence": "A covering index holds every column.",
                              "to": "must-index-foreign-keys"}]
    assert out["failures"] == [] and out["missing"] == []


def test_lossless_reads_the_copies_its_accounting_names(tmp_path, capsys):
    folder = _topic(tmp_path)
    rel = "cookbook/guidelines/planning/data/t"
    copy = _topic(tmp_path, rel, roled=False)
    sentence = "See the implementing copy of this guideline."
    (copy / "covering.md").write_text(f"\n{sentence}\n\n", encoding="utf-8")
    base = _commit(tmp_path)
    shutil.rmtree(copy)                       # folded away since the base
    (folder / "lossless.json").write_text(json.dumps(
        {"base": base, "copies": [rel], "moved": [],
         "obsolete": [{"sentence": sentence, "reason": "points at the folded copy"}]}), encoding="utf-8")
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base, "--draft"]) == 0
    out = _json(capsys)
    assert out["copies"] == [rel] and out["obsolete"][0]["sentence"] == sentence
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base, "--copy", str(copy), "--draft"]) == 0
    assert _json(capsys)["copies"] == [rel]


def test_a_rule_name_lends_no_negation_or_level_to_its_rule(tmp_path, capsys):
    code, out = _moved(tmp_path, capsys,
                       "Synced tables SHOULD NOT use AUTOINCREMENT ids on any device.",
                       "SHOULD cap WAL file size.",
                       extra_rules="- **should-not-use-autoincrement-ids**: Synced tables SHOULD use "
                                   "AUTOINCREMENT ids on any device.\n",
                       to="should-not-use-autoincrement-ids")
    assert code == 1 and "negation" in out["failures"][0]["reason"]


# ── fix round 4: tripwires on the matched clause ────────────────────────────

ONLY_ADD = "MUST only add columns — never remove or rename without a migration path"


def test_removing_never_from_must_only_add_columns_fails_though_without_stays(tmp_path, capsys):
    code, out = _moved(tmp_path, capsys, ONLY_ADD,
                       "A sync-compatible migration MUST only add columns — remove or rename "
                       "without a migration path.")
    assert code == 1 and "negation" in out["failures"][0]["reason"]
    code, out = _moved(tmp_path / "ok", capsys, ONLY_ADD,
                       "A sync-compatible migration MUST only add columns — never remove or rename "
                       "without a migration path.")
    assert code == 0, out


def test_a_negation_is_not_borrowed_from_another_target(tmp_path, capsys):
    code, out = _moved(tmp_path, capsys, "MUST NOT store secrets in plaintext columns.",
                       "MUST store secrets in plaintext columns.",
                       extra_rules="- **r2**: MUST NOT log secrets.\n", to=["r", "r2"])
    assert code == 1 and "negation" in out["failures"][0]["reason"]


def test_a_negation_is_not_borrowed_from_another_clause_of_the_rule(tmp_path, capsys):
    code, out = _moved(tmp_path, capsys, "MUST NOT use AUTOINCREMENT on synced tables.",
                       "MUST use AUTOINCREMENT on synced tables, and MUST NOT reuse ids.")
    assert code == 1 and "negation" in out["failures"][0]["reason"]


def test_without_does_not_stand_in_for_never(tmp_path, capsys):
    code, out = _moved(tmp_path, capsys, "Never disable foreign keys in production.",
                       "SHOULD disable foreign keys in production without a backup.")
    assert code == 1 and "negation" in out["failures"][0]["reason"]


def test_each_source_clause_is_checked_against_its_best_clause_across_the_rules(tmp_path, capsys):
    sentence = "MUST NOT log secrets; MUST store them encrypted at rest."
    code, out = _moved(tmp_path, capsys, sentence, "MUST NOT log secrets.",
                       extra_rules="- **r2**: MUST store secrets encrypted at rest.\n", to=["r", "r2"])
    assert code == 0, out
    code, out = _moved(tmp_path / "bad", capsys, sentence, "MUST log secrets.",
                       extra_rules="- **r2**: MUST NOT store secrets encrypted at rest.\n", to=["r", "r2"])
    assert code == 1 and "negation" in out["failures"][0]["reason"]


# ── obsolete ────────────────────────────────────────────────────────────────

def test_an_obsolete_never_rule_fails(tmp_path, capsys):
    folder, base = _from_copy(tmp_path, "Never hold a write transaction open while waiting on network I/O.")
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base]) == 1
    out = _json(capsys)
    assert out["obsolete"] == [] and "never obsolete" in out["failures"][0]["reason"]


@pytest.mark.parametrize("sentence", ["See the implementing copy without the examples.",
                                      "See the implementing copy only for its examples.",
                                      "Don't read the implementing copy."])
def test_an_obsolete_sentence_with_a_negation_or_meaning_word_fails(tmp_path, capsys, sentence):
    folder, base = _from_copy(tmp_path, sentence)
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base]) == 1
    assert _json(capsys)["obsolete"] == []


def test_a_sentence_of_the_topics_own_base_is_never_obsolete(tmp_path, capsys):
    folder = _topic(tmp_path)
    sentence = "See the implementing copy of this guideline for detailed examples."
    (folder / "covering.md").write_text(f"\nA covering index holds every column. {sentence}\n\n",
                                        encoding="utf-8")
    base = _commit(tmp_path)
    (folder / "covering.md").write_text("\nA covering index holds every column.\n\n", encoding="utf-8")
    _obsolete(folder, base, sentence, "points at the copy folded into this topic")
    capsys.readouterr()
    assert main(["roles", "lossless", str(folder), "--base", base]) == 1
    out = _json(capsys)
    assert out["obsolete"] == [] and "topic's own" in out["failures"][0]["reason"]


# ── numbers ─────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("sentence, rule", [
    ("Every synced table MUST have three timestamp columns.", "Every synced table MUST have two timestamp columns."),
    ("SHOULD implement at least two scheduling modes.", "SHOULD implement at least one scheduling mode."),
    ("SHOULD retry the failed sync twice before alerting.", "SHOULD retry the failed sync once before alerting."),
    ("SHOULD keep a single writer connection per database.", "SHOULD keep a double writer connection per database."),
    ("SHOULD keep thirty days of sync history per device.", "SHOULD keep ninety days of sync history per device."),
    ("SHOULD cap each sync batch at a thousand rows.", "SHOULD cap each sync batch at a million rows."),
    ("SHOULD keep half of the cache warm on launch.", "SHOULD keep twenty of the cache warm on launch."),
])
def test_a_changed_number_word_fails(tmp_path, capsys, sentence, rule):
    code, out = _moved(tmp_path, capsys, sentence, rule)
    assert code == 1 and "number" in out["failures"][0]["reason"], out


def test_a_number_word_written_as_digits_passes(tmp_path, capsys):
    code, out = _moved(tmp_path, capsys, "Every synced table MUST have three timestamp columns.",
                       "Every synced table MUST have 3 timestamp columns.")
    assert code == 0, out


def test_a_lead_in_keeps_its_number(tmp_path, capsys):
    rule = "- **should-not-send-large-batches**: SHOULD NOT send sync batches above the row limit " \
           "that cause lock contention.\n"
    code, out = _moved(tmp_path, capsys, "Batches above 500 rows cause lock contention:",
                       "SHOULD cap WAL file size.", extra_rules=rule, to="should-not-send-large-batches")
    assert code == 1 and "500" in out["failures"][0]["reason"]


def test_a_lead_in_is_judged_against_its_rules_names(tmp_path, capsys):
    # "Access methods:" -> `platform-access-methods`: its words are only in the
    # rule's name, which carries them.
    rule = "- **platform-access-methods**: Each platform MUST reach the panel by a gesture or menu item.\n"
    code, out = _moved(tmp_path, capsys, "Access methods:", "SHOULD cap WAL file size.",
                       extra_rules=rule, to="platform-access-methods")
    assert code == 0, out["failures"]
    assert out["moved"] == [{"sentence": "Access methods:", "to": "platform-access-methods", "lead_in": True}]
    # words in neither the name nor the text still fail
    code, out = _moved(tmp_path / "no", capsys, "Entry points:", "SHOULD cap WAL file size.",
                       extra_rules=rule, to="platform-access-methods")
    assert code == 1 and "entry" in out["failures"][0]["reason"]


def test_a_framing_lead_in_keeps_its_number(tmp_path, capsys):
    code, out = _moved(tmp_path, capsys, "MUST follow these two rules:", "SHOULD cap WAL file size.",
                       extra_rules=FRAMED, to=FRAMED_NAMES)
    assert code == 1 and "number" in out["failures"][0]["reason"]


# ── framing ─────────────────────────────────────────────────────────────────

def test_a_framing_lead_in_fails_on_unrelated_rules_that_hold_its_words_between_them(tmp_path, capsys):
    rules = ("- **must-keep-key-outside**: MUST store the key outside the database; the rest of the "
             "row is plain.\n- **must-encrypt-backup**: MUST encrypt the backup file.\n"
             "- **must-snake-case-columns**: MUST name columns in snake_case.\n")
    code, out = _moved(tmp_path, capsys, "MUST encrypt these columns at rest:", "SHOULD cap WAL file size.",
                       extra_rules=rules,
                       to=["must-keep-key-outside", "must-encrypt-backup", "must-snake-case-columns"])
    assert code == 1 and out["moved"] == []
    assert "no one rule" in out["failures"][0]["reason"]


def test_a_framing_lead_in_may_introduce_a_rule_broader_than_its_scope(tmp_path, capsys):
    rules = ("- **must-only-add-columns**: In a sync-capable schema, a migration MUST only add columns.\n"
             "- **must-make-migrations-idempotent**: Each migration MUST be idempotent.\n")
    code, out = _moved(tmp_path, capsys, "MUST follow these rules for any migration in a sync-capable schema:",
                       "SHOULD cap WAL file size.", extra_rules=rules,
                       to=["must-only-add-columns", "must-make-migrations-idempotent"])
    assert code == 0, out


def test_a_framing_lead_in_needs_every_one_of_its_words(tmp_path, capsys):
    rules = "".join(f"- **must-do-{n}**: An offline sync schema change MUST do {n}.\n" for n in ("a", "b"))
    code, out = _moved(tmp_path, capsys, "MUST follow for offline sync schema change rollback:",
                       "SHOULD cap WAL file size.", extra_rules=rules, to=["must-do-a", "must-do-b"])
    assert code == 1 and "rollback" in out["failures"][0]["reason"]


# ── meaning-flip words ──────────────────────────────────────────────────────

@pytest.mark.parametrize("sentence, rule", [
    ("SHOULD avoid storing large blobs in synced tables.", "SHOULD store large blobs in synced tables."),
    ("MUST only add columns in sync migrations.", "MUST add columns in sync migrations."),
    ("MUST keep at least 3 nightly backups.", "MUST keep at most 3 nightly backups."),
    ("MUST keep at most 3 nightly backups.", "MUST keep at least 3 nightly backups."),
    ("Run foreign_key_check before committing the migration.", "Run foreign_key_check after committing the migration."),
    ("Run foreign_key_check after committing the migration.", "Run foreign_key_check before committing the migration."),
    ("Hold the lock until the sync batch commits.", "Hold the lock when the sync batch commits."),
    ("Retry the sync batch unless the server rejected it.", "Retry the sync batch when the server rejected it."),
    ("Index every foreign key column except the parent id.", "Index every foreign key column including the parent id."),
    ("Run the migration without a backup step.", "Run the migration with a backup step."),
    ("Use a change-log table instead of the flag column.", "Use a change-log table and the flag column."),
    ("SHOULD prefer UUIDv7 keys for synced tables.", "SHOULD use UUIDv7 keys for synced tables."),
    ("Keep a minimum of 3 nightly backups on the server.", "Keep a maximum of 3 nightly backups on the server."),
    ("Keep a maximum of 3 nightly backups on the server.", "Keep a minimum of 3 nightly backups on the server."),
    ("Alert when the WAL grows more than 100 MB on disk.", "Alert when the WAL grows less than 100 MB on disk."),
    ("Alert when the WAL grows less than 100 MB on disk.", "Alert when the WAL grows more than 100 MB on disk."),
    ("Warn when a table has fewer than 2 indexes defined.", "Warn when a table has more than 2 indexes defined."),
])
def test_a_swapped_meaning_word_fails(tmp_path, capsys, sentence, rule):
    code, out = _moved(tmp_path, capsys, sentence, rule)
    assert code == 1 and out["moved"] == [], out
    assert "drops" in out["failures"][0]["reason"]


# ── judged verdicts ─────────────────────────────────────────────────────────

REWORDED = ("Every sync system MUST have an explicit conflict resolution strategy.",
            "Every sync system MUST define an explicit strategy for conflict resolution.")


def _judged(tmp_path, capsys, verdict=None, *, flag=False, sentence=REWORDED[0], rule=REWORDED[1]):
    """`_moved` with the entry judged `verdict` (None: unjudged) and pinned,
    run judged-required (`flag`, the default mode) or as a `--draft`. The exit
    code, the JSON and stderr."""
    _moved(tmp_path, capsys, sentence, rule)
    folder = tmp_path / "cookbook/guidelines/implementing/data/t"
    data = json.loads((folder / "lossless.json").read_text(encoding="utf-8"))
    if verdict is not None:
        data["moved"][0]["judged"] = {"by": "judge-model", "verdict": verdict, "note": "read both"}
    (folder / "lossless.json").write_text(json.dumps(data), encoding="utf-8")
    if verdict is not None:
        _write_pins(folder)
    capsys.readouterr()
    base = data["base"]
    code = main(["roles", "lossless", str(folder), "--base", base, *([] if flag else ["--draft"])])
    captured = capsys.readouterr()
    return code, json.loads(captured.out), captured.err


def test_an_unjudged_reworded_entry_fails_with_require_judged(tmp_path, capsys):
    code, out, err = _judged(tmp_path, capsys)
    assert code == 0 and out["counts"] == {"verbatim": 0, "reworded_judged": 0, "reworded_unjudged": 1,
                                           "judged_fail": 0, "stale": 0, "obsolete_judged": 0,
                                           "obsolete_unjudged": 0}
    assert "reworded-unjudged 1" in err
    code, out, _ = _judged(tmp_path / "flag", capsys, flag=True)
    assert code == 1 and out["moved"] == []
    assert "judged" in out["failures"][0]["reason"]


def test_a_judged_pass_passes_with_require_judged(tmp_path, capsys):
    code, out, _ = _judged(tmp_path, capsys, "pass", flag=True)
    assert code == 0, out
    assert out["counts"]["reworded_judged"] == 1 and out["counts"]["reworded_unjudged"] == 0
    assert out["moved"][0]["judged"]["verdict"] == "pass"


def test_a_judged_fail_fails_even_without_the_flag(tmp_path, capsys):
    code, out, _ = _judged(tmp_path, capsys, "fail")
    assert code == 1 and out["moved"] == [] and out["counts"]["judged_fail"] == 1
    assert "judge-model" in out["failures"][0]["reason"]


def test_a_verbatim_move_needs_no_judge(tmp_path, capsys):
    code, out, _ = _judged(tmp_path, capsys, flag=True,
                           sentence="Every sync system MUST have an explicit **conflict resolution** strategy.",
                           rule="Every sync system MUST have an explicit `conflict resolution` strategy.")
    assert code == 0, out
    assert out["counts"] == {"verbatim": 1, "reworded_judged": 0, "reworded_unjudged": 0, "judged_fail": 0,
                             "stale": 0, "obsolete_judged": 0, "obsolete_unjudged": 0}
    assert out["moved"][0]["verbatim"] is True


def test_a_malformed_or_duplicate_entry_is_refused(tmp_path, capsys):
    _moved(tmp_path, capsys, *REWORDED)
    folder = tmp_path / "cookbook/guidelines/implementing/data/t"
    data = json.loads((folder / "lossless.json").read_text(encoding="utf-8"))
    from cookr.core.rolework import RoleworkError, read_accounting
    for bad in ({"by": "j", "verdict": "maybe", "note": ""}, {"verdict": "pass"}, "pass"):
        data["moved"][0]["judged"] = bad
        (folder / "lossless.json").write_text(json.dumps(data), encoding="utf-8")
        with pytest.raises(RoleworkError):
            read_accounting(folder)
    del data["moved"][0]["judged"]
    data["moved"].append(dict(data["moved"][0]))
    (folder / "lossless.json").write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(RoleworkError, match="more than once"):
        read_accounting(folder)


# ── fix round 5 ─────────────────────────────────────────────────────────────

T = "cookbook/guidelines/implementing/data/t"


def _run(folder, base, *extra):
    """`roles lossless` on `folder` (default mode: judged required). The exit
    code, the JSON and stderr."""
    code = main(["roles", "lossless", str(folder), "--base", base, *extra])
    return code


def _lossless(capsys, folder, base, *extra):
    capsys.readouterr()
    code = main(["roles", "lossless", str(folder), "--base", base, *extra])
    captured = capsys.readouterr()
    return code, json.loads(captured.out), captured.err


def _write_pins(folder):
    """What a judge does after recording its verdicts: write each judged
    entry's pin, as `roles lossless --pin-for <folder> --entry <n>` prints it.
    The sentences pinned."""
    from cookr.core.rolework import pin_for
    data = json.loads((folder / "lossless.json").read_text(encoding="utf-8"))
    entries = [*data.get("moved", []), *data.get("obsolete", [])]
    pins = {n: pin_for(folder, n)["pin"] for n, m in enumerate(entries, 1) if m.get("judged")}
    for n, pin in pins.items():
        entries[n - 1]["judged"]["pin"] = pin
    (folder / "lossless.json").write_text(json.dumps(data), encoding="utf-8")
    return [entries[n - 1]["sentence"] for n in pins]


def _pin(capsys, folder):
    return 0, {"pinned": _write_pins(folder)}, ""


def _judge_all(folder, verdict="pass"):
    data = json.loads((folder / "lossless.json").read_text(encoding="utf-8"))
    for m in [*data.get("moved", []), *data.get("obsolete", [])]:
        m["judged"] = {"by": "judge-model", "verdict": verdict, "note": "read both"}
    (folder / "lossless.json").write_text(json.dumps(data), encoding="utf-8")
    return data


KEEP = "Keep write transactions short."


# C1″: verbatim is equality with one whole sentence of a target, normalised.

@pytest.mark.parametrize("rule", [
    "SHOULD NOT keep write transactions short.",
    "~~Keep write transactions short.~~ Keep write transactions brief and short.",
    "Keep write transactions short, except in sync jobs.",
    "Do not keep write transactions short.",
    "It is a myth that you should keep write transactions short.",
])
def test_a_sentence_inside_a_longer_or_struck_target_is_reworded_not_verbatim(tmp_path, capsys, rule):
    _moved(tmp_path, capsys, KEEP, rule)
    folder = tmp_path / T
    code, out, _ = _lossless(capsys, folder, json.loads((folder / "lossless.json").read_text())["base"])
    assert code == 1, out
    assert out["counts"]["verbatim"] == 0 and out["counts"]["reworded_unjudged"] == 1
    assert "judged" in out["failures"][0]["reason"]


def test_verbatim_ignores_emphasis_code_markers_and_struck_text_only(tmp_path, capsys):
    from cookr.core.rolework import verbatim_in
    assert verbatim_in("Use `WAL` mode in **production**.", "Set it once. Use WAL mode in production.")
    assert verbatim_in("Use WAL mode in production.", "Use WAL mode ~~always~~ in production.")
    assert not verbatim_in("Use WAL mode.", "Use WAL mode, except in tests.")
    assert not verbatim_in("Use WAL mode.", "~~Use WAL mode.~~ Use rollback mode.")
    assert not verbatim_in("Use WAL mode.", "MUST use WAL mode.")


# C2″: a judged verdict is pinned to what it judged.

REWORDED_RULE = "Every sync system MUST define an explicit strategy for conflict resolution."


def _judged_pinned(tmp_path, capsys):
    """`_moved` with its entry judged pass and pinned as a judge does, from `--pin-for`."""
    _moved(tmp_path, capsys, REWORDED[0], REWORDED_RULE)
    folder = tmp_path / T
    _judge_all(folder)
    code, out, err = _pin(capsys, folder)
    assert code == 0, err
    return folder, json.loads((folder / "lossless.json").read_text())["base"]


def test_pin_stamps_a_judged_entry_and_the_pinned_verdict_passes(tmp_path, capsys):
    folder, base = _judged_pinned(tmp_path, capsys)
    pin = json.loads((folder / "lossless.json").read_text())["moved"][0]["judged"]["pin"]
    assert len(pin) == 64 and all(c in "0123456789abcdef" for c in pin)
    code, out, _ = _lossless(capsys, folder, base)
    assert code == 0, out
    assert out["counts"]["reworded_judged"] == 1 and out["counts"]["stale"] == 0


def test_a_judged_verdict_without_a_pin_is_stale(tmp_path, capsys):
    _moved(tmp_path, capsys, REWORDED[0], REWORDED_RULE)
    folder = tmp_path / T
    data = _judge_all(folder)
    code, out, err = _lossless(capsys, folder, data["base"])
    assert code == 1 and out["counts"]["stale"] == 1 and out["counts"]["reworded_judged"] == 0
    assert "stale" in out["failures"][0]["reason"] and "stale" in err


def test_a_rule_qualified_after_judging_makes_the_verdict_stale(tmp_path, capsys):
    folder, base = _judged_pinned(tmp_path, capsys)
    rules = (folder / "rules.md").read_text()
    (folder / "rules.md").write_text(rules.replace("conflict resolution.\n",
                                                   "conflict resolution, unless it is offline.\n"))
    code, out, _ = _lossless(capsys, folder, base)
    assert code == 1 and "stale" in out["failures"][0]["reason"], out


def test_a_changed_to_after_judging_makes_the_verdict_stale(tmp_path, capsys):
    folder, base = _judged_pinned(tmp_path, capsys)
    data = json.loads((folder / "lossless.json").read_text())
    data["moved"][0]["to"] = ["r", "must-index-foreign-keys"]
    (folder / "lossless.json").write_text(json.dumps(data))
    code, out, _ = _lossless(capsys, folder, base)
    assert code == 1 and "stale" in out["failures"][0]["reason"], out


def test_an_edited_source_sentence_makes_the_verdict_stale(tmp_path, capsys):
    folder = _topic(tmp_path)
    one, two = REWORDED[0], "Every sync system MUST define an explicit conflict resolution strategy."
    (folder / "covering.md").write_text(f"\nA covering index holds every column. {one}\n\n{two}\n\n",
                                        encoding="utf-8")
    base = _commit(tmp_path)
    (folder / "covering.md").write_text("\nA covering index holds every column.\n\n", encoding="utf-8")
    (folder / "rules.md").write_text(RULES + f"- **r**: {REWORDED_RULE}\n\n", encoding="utf-8")
    _account(folder, base, (one, "r"))
    _judge_all(folder)
    assert _pin(capsys, folder)[0] == 0
    data = json.loads((folder / "lossless.json").read_text())
    data["moved"][0]["sentence"] = two        # the judged record now sits on another sentence
    data["moved"].append({"sentence": one, "to": "r"})
    (folder / "lossless.json").write_text(json.dumps(data))
    code, out, _ = _lossless(capsys, folder, base)
    assert code == 1
    stale = [f for f in out["failures"] if f["sentence"] == two]
    assert stale and "stale" in stale[0]["reason"], out


def test_pin_is_gone_and_pin_for_prints_an_entrys_pin_and_writes_nothing(tmp_path, capsys):
    _moved(tmp_path, capsys, REWORDED[0], REWORDED_RULE)
    folder = tmp_path / T
    _judge_all(folder)
    before = (folder / "lossless.json").read_text()
    with pytest.raises(SystemExit):
        main(["roles", "lossless", "--pin", str(folder)])
    capsys.readouterr()
    assert main(["roles", "lossless", "--pin-for", str(folder), "--entry", "1"]) == 0
    out = _json(capsys)
    assert out["kind"] == "moved" and out["sentence"] == REWORDED[0] and len(out["pin"]) == 64
    assert (folder / "lossless.json").read_text() == before
    from cookr.core.rolework import RoleworkError, pin_for
    for n in (0, 2):
        with pytest.raises(RoleworkError, match="no entry"):
            pin_for(folder, n)


# I1″: more clause separators; judged is the default, --draft turns it off.

@pytest.mark.parametrize("rule", [
    "Disable foreign keys in production — never in tests.",
    "Disable foreign keys in production – never in tests.",
    "Disable foreign keys in production (never in tests).",
    "Disable foreign keys in production, never in tests.",
    "Disable foreign keys in production or never re-enable them.",
    "Disable foreign keys in production while no migration runs.",
    "Disable foreign keys in production: no exceptions.",
    "Disable foreign keys in production; no exceptions.",
])
def test_a_negation_in_a_neighbouring_clause_does_not_cover_the_matched_one(tmp_path, capsys, rule):
    code, out = _moved(tmp_path, capsys, "Never disable foreign keys in production.", rule)
    assert code == 1 and "negation" in out["failures"][0]["reason"], out


@pytest.mark.parametrize("sentence, rule, lost", [
    ("MUST NOT use AUTOINCREMENT on synced tables.",
     "MUST use AUTOINCREMENT on synced tables — MUST NOT reuse ids.", "MUST NOT"),
    ("MUST only add columns in a sync migration.",
     "MUST add columns in a sync migration — only after a backup.", "only"),
    ("MUST keep 3 nightly backups.", "MUST keep 2 nightly backups (3 weekly).", "3"),
])
def test_a_level_flip_word_or_number_in_a_neighbouring_clause_does_not_count(tmp_path, capsys,
                                                                             sentence, rule, lost):
    code, out = _moved(tmp_path, capsys, sentence, rule)
    assert code == 1 and lost in out["failures"][0]["reason"], out


def test_judged_is_the_default_and_draft_turns_it_off(tmp_path, capsys):
    _moved(tmp_path, capsys, REWORDED[0], REWORDED_RULE)
    folder = tmp_path / T
    base = json.loads((folder / "lossless.json").read_text())["base"]
    code, out, _ = _lossless(capsys, folder, base)
    assert code == 1 and out["draft"] is False
    code, out, _ = _lossless(capsys, folder, base, "--require-judged")
    assert code == 1
    code, out, err = _lossless(capsys, folder, base, "--draft")
    assert code == 0 and out["draft"] is True and "DRAFT" in err
    assert out["counts"]["reworded_unjudged"] == 1


# I2″: an obsolete entry needs a pinned judged pass too.

OBS = "See the implementing copy of this guideline for detailed examples."


def test_an_unjudged_obsolete_entry_fails_and_passes_in_draft(tmp_path, capsys):
    folder, base = _from_copy(tmp_path, OBS)
    code, out, _ = _lossless(capsys, folder, base)
    assert code == 1 and "judged" in out["failures"][0]["reason"] and out["obsolete"] == []
    code, out, _ = _lossless(capsys, folder, base, "--draft")
    assert code == 0 and out["obsolete"][0]["sentence"] == OBS


def test_a_pinned_obsolete_entry_passes_and_a_changed_reason_makes_it_stale(tmp_path, capsys):
    folder, base = _from_copy(tmp_path, OBS)
    _judge_all(folder)
    assert _pin(capsys, folder)[0] == 0
    code, out, _ = _lossless(capsys, folder, base)
    assert code == 0, out
    assert out["counts"]["obsolete_judged"] == 1
    data = json.loads((folder / "lossless.json").read_text())
    data["obsolete"][0]["reason"] = "no longer needed"
    (folder / "lossless.json").write_text(json.dumps(data))
    code, out, _ = _lossless(capsys, folder, base)
    assert code == 1 and "stale" in out["failures"][0]["reason"], out


# I3″: copies cannot go unread.

COPY2_ID = "6f1c1e2a-0000-4000-8000-000000000002"


def test_a_fold_history_row_must_name_a_listed_copy(tmp_path, capsys):
    folder = _topic(tmp_path)
    copy = tmp_path / "cookbook/guidelines/planning/data/t-plan"
    write_folder(Artifact(meta={"id": COPY2_ID, "type": "guideline", "title": "T", "version": "1.0.0",
                                "modified": "2026-01-01"},
                          parts=[Part("intro", "# T\n\nIndexes keep reads fast.\n\n"),
                                 Part("extra", "\nSee the planning notes.\n\n", "Extra"),
                                 Part("history", "\n| Version | Date | Author | Summary |\n|---|---|---|---|\n"
                                                 "| 1.0.0 | 2026-01-01 | A | first |\n", "Change History")]),
                 copy)
    base = _commit(tmp_path)
    capsys.readouterr()
    assert main(["fold", str(copy), "--into", str(folder), "--author", "T", "--date", "2026-11-16"]) == 0
    assert not copy.exists()
    code, out, _ = _lossless(capsys, folder, base, "--draft")
    assert code == 1
    assert any("cookbook/guidelines/planning/data/t-plan" in f["reason"] and "copies" in f["reason"]
               for f in out["failures"]), out


def test_a_deleted_same_slug_twin_must_be_listed(tmp_path, capsys):
    import shutil
    folder = _topic(tmp_path)
    twin = _topic(tmp_path, "cookbook/guidelines/reviewing/data/t", roled=False)
    base = _commit(tmp_path)
    shutil.rmtree(twin)
    code, out, _ = _lossless(capsys, folder, base, "--draft")
    assert code == 1
    assert any("cookbook/guidelines/reviewing/data/t" in f["reason"] for f in out["failures"]), out


def test_a_listed_copy_that_still_exists_fails(tmp_path, capsys):
    folder = _topic(tmp_path)
    rel = "cookbook/guidelines/planning/data/t-plan"
    _topic(tmp_path, rel, roled=False)
    base = _commit(tmp_path)
    (folder / "lossless.json").write_text(json.dumps({"base": base, "copies": [rel], "moved": []}))
    code, out, _ = _lossless(capsys, folder, base, "--draft")
    assert code == 1
    assert any(rel in f["reason"] and "exists" in f["reason"] for f in out["failures"]), out


def _rename(root, old, new):
    subprocess.run(["git", "-C", str(root), "mv", old, new], check=True, capture_output=True)
    return root / new


def test_a_renamed_topic_reads_its_old_path_as_its_own_base(tmp_path, capsys):
    from cookr.core.rolework import RoleworkError, lossless
    _topic(tmp_path)
    base = _commit(tmp_path)
    folder = _rename(tmp_path, "cookbook/guidelines/implementing/data/t",
                     "cookbook/guidelines/implementing/data/t2")
    with pytest.raises(RoleworkError, match="is not in"):
        lossless(folder, base, require_judged=False)
    (folder / "lossless.json").write_text(json.dumps(
        {"base": base, "renamed_from": "cookbook/guidelines/implementing/data/t", "moved": []}))
    code, out, _ = _lossless(capsys, folder, base, "--draft")
    assert code == 0, out
    assert out["failures"] == [] and out["missing"] == []


def test_renamed_from_must_be_gone_and_carry_the_topics_id(tmp_path):
    from cookr.core.rolework import RoleworkError, lossless
    folder = _topic(tmp_path)
    other = _topic(tmp_path, "cookbook/guidelines/planning/data/u", roled=False)
    manifest = other / "artifact.json"
    manifest.write_text(manifest.read_text().replace("6f1c1e2a-0000-4000-8000-000000000001",
                                                     "6f1c1e2a-0000-4000-8000-0000000000ff"))
    base = _commit(tmp_path)
    (folder / "lossless.json").write_text(json.dumps(
        {"base": base, "renamed_from": "cookbook/guidelines/planning/data/u", "moved": []}))
    with pytest.raises(RoleworkError, match="still exists"):
        lossless(folder, base, require_judged=False)
    import shutil
    shutil.rmtree(other)
    with pytest.raises(RoleworkError, match="not this topic"):
        lossless(folder, base, require_judged=False)


def test_a_same_named_folder_renamed_away_is_no_twin(tmp_path, capsys):
    folder = _topic(tmp_path)
    twin = _topic(tmp_path, "cookbook/guidelines/planning/data/t", roled=False)
    manifest = twin / "artifact.json"
    manifest.write_text(manifest.read_text().replace("6f1c1e2a-0000-4000-8000-000000000001",
                                                     "6f1c1e2a-0000-4000-8000-0000000000ee"))
    base = _commit(tmp_path)
    _rename(tmp_path, "cookbook/guidelines/planning/data/t", "cookbook/guidelines/planning/data/t-plan")
    code, out, _ = _lossless(capsys, folder, base, "--draft")
    assert code == 0, out
    assert not any("planning/data/t" in (f["reason"] or "") for f in out["failures"]), out


# A parenthetical gloss is read with the FLIP_WORD that opens the clause it
# glosses ("After applying server records (step 5 of the sync cycle)" says
# "after step 5"): sync-engine-design's real rule. Nothing else is inherited.

GLOSS_SOURCE = "After step 5, rebuild the derived views before notifying the UI."


def test_a_gloss_keeps_the_flip_word_that_opens_the_clause_it_glosses(tmp_path, capsys):
    code, out = _moved(tmp_path, capsys, GLOSS_SOURCE,
                       "After applying server records (step 5 of the sync cycle), SHOULD rebuild the "
                       "derived views before notifying the UI.")
    assert code == 0, out


@pytest.mark.parametrize("rule, lost", [
    # the flip word is in the glossed clause, but does not open it
    ("Apply server records after the push (step 5 of the sync cycle), then SHOULD rebuild the derived "
     "views before notifying the UI.", "after"),
    # the opening word is another flip word
    ("Before applying server records (step 5 of the sync cycle), SHOULD rebuild the derived views "
     "before notifying the UI.", "after"),
])
def test_a_gloss_inherits_only_an_opening_flip_word(tmp_path, capsys, rule, lost):
    code, out = _moved(tmp_path, capsys, GLOSS_SOURCE, rule)
    assert code == 1 and lost in out["failures"][0]["reason"], out


def test_a_gloss_inherits_no_negation_level_or_number(tmp_path, capsys):
    code, out = _moved(tmp_path, capsys, "Never skip step 5 twice.",
                       "Never skip applying server records (step 5 twice in a cycle).")
    assert code == 1 and "negation" in out["failures"][0]["reason"], out


# ── closing fix ─────────────────────────────────────────────────────────────

# C1‴: struck-through text and HTML comments are not kept, however many
# sentences or lines they cover; the sentences and the verbatim test drop them
# by one removal (`unstruck`).

GONE = "Every foreign key MUST be indexed before release."

HIDDEN = [
    f"~~Retired. {GONE} Done.~~ Keys MAY go unindexed.",                  # a struck span of 3 sentences
    f"Keys MAY go unindexed. ~~Retired:\n  {GONE}\n  end~~",              # struck across soft line breaks
    f"<!-- Retired. {GONE} Done. --> Keys MAY go unindexed.",            # a comment of 3 sentences
    f"Keys MAY go unindexed.\n<!--\n{GONE}\n-->",                          # a comment across lines
]


def _hidden(tmp_path, shape):
    """Base: GONE a sentence of the covering part. Now: it survives only inside `shape`."""
    folder = _topic(tmp_path)
    (folder / "covering.md").write_text(f"\nA covering index holds every column. {GONE}\n\n",
                                        encoding="utf-8")
    base = _commit(tmp_path)
    (folder / "covering.md").write_text(f"\nA covering index holds every column.\n\n{shape}\n\n",
                                        encoding="utf-8")
    return folder, base


@pytest.mark.parametrize("shape", HIDDEN)
def test_a_sentence_kept_only_in_struck_or_commented_text_is_missing(tmp_path, capsys, shape):
    from cookr.core.rolework import flat, now_sentences, verbatim_in
    folder, base = _hidden(tmp_path, shape)
    assert GONE not in now_sentences(load_folder(folder))
    assert "foreign key" not in flat(shape) and not verbatim_in(GONE, shape)
    code, out, _ = _lossless(capsys, folder, base)
    assert code == 1 and out["missing"] == [GONE], out


@pytest.mark.parametrize("shape", HIDDEN)
def test_a_sentence_kept_only_in_struck_or_commented_text_is_never_verbatim(tmp_path, capsys, shape):
    folder, base = _hidden(tmp_path, shape)
    _account(folder, base, (GONE, "covering"))
    code, out, _ = _lossless(capsys, folder, base)
    assert code == 1 and out["missing"] == [] and out["counts"]["verbatim"] == 0, out
    assert [f["sentence"] for f in out["failures"]] == [GONE]


# I1‴: the normalisation never touches a code span, nor a `_` or `*` that is
# not a pair of emphasis markers around words.

@pytest.mark.parametrize("one, other", [
    ("`_deleted`", "`deleted`"),
    ("`is_`", "`is`"),
    ("`<table_name>_id`", "`<table_name>id`"),
    ("`__sync_version__`", "`sync_version`"),
    ("`COUNT(*)`", "`COUNT()`"),
    ("`*-wal`", "`-wal`"),
    ("2**10", "210"),
    ("<table_name>_id", "<table_name>id"),
    ("is_ or has_", "is or has"),
])
def test_flat_keeps_identifier_and_code_characters(one, other):
    from cookr.core.rolework import flat
    assert flat(f"Name it {one} here.") != flat(f"Name it {other} here.")


def test_flat_still_drops_paired_emphasis_and_code_markers():
    from cookr.core.rolework import flat
    assert flat("**MUST** use *all* _three_ __keys__ in `WAL` mode.") == "MUST use all three keys in WAL mode."
    assert flat("~~old~~ - A `snake_case` name, not *camelCase*.") == "A snake_case name, not camelCase."


@pytest.mark.parametrize("one, other", [
    ("Boolean columns MUST be prefixed with `is_` or `has_`.",
     "Boolean columns MUST be prefixed with `is` or `has`."),
    ("MUST use `<table_name>_id`, not bare `id`.", "MUST use `<table_name>id`, not bare `id`."),
])
def test_an_identifier_edit_changes_verbatim_and_the_pin(tmp_path, capsys, one, other):
    from cookr.core.rolework import moved_pin, verbatim_in
    assert verbatim_in(one, one) and not verbatim_in(one, other)
    art = Artifact(meta={}, parts=[])
    assert moved_pin(one, "r", {"r": one}, art) != moved_pin(one, "r", {"r": other}, art)
    code, out = _moved(tmp_path, capsys, one, other, draft=False)
    assert code == 1 and out["counts"]["verbatim"] == 0, out


# I2‴: `--pin` is gone; a judge writes the pin `--pin-for` prints. Deleting a
# stale verdict's pin and running the pinning path never makes the gate pass.

def test_deleting_a_stale_pin_and_re_running_the_pinning_path_never_passes(tmp_path, capsys):
    folder, base = _judged_pinned(tmp_path, capsys)
    rules = (folder / "rules.md").read_text()
    (folder / "rules.md").write_text(rules.replace("conflict resolution.\n",
                                                   "conflict resolution, unless it is offline.\n"))
    code, out, _ = _lossless(capsys, folder, base)
    assert code == 1 and "changed" in out["failures"][0]["reason"], out
    data = json.loads((folder / "lossless.json").read_text())
    del data["moved"][0]["judged"]["pin"]
    (folder / "lossless.json").write_text(json.dumps(data))
    with pytest.raises(SystemExit):
        main(["roles", "lossless", "--pin", str(folder)])
    capsys.readouterr()
    assert main(["roles", "lossless", "--pin-for", str(folder), "--entry", "1"]) == 0
    code, out, _ = _lossless(capsys, folder, base)
    assert code == 1 and out["counts"]["stale"] == 1 and out["counts"]["reworded_judged"] == 0, out
    assert "no pin" in out["failures"][0]["reason"]


# I3‴: a gloss holding a meaning word of its own inherits none, and only an
# ordering word (before, after, until) is ever inherited.

@pytest.mark.parametrize("sentence, rule", [
    ("Run migrations before deploying.", "Before release (run migrations after deploying)."),
    ("Only add columns.", "Only on Mondays (add or drop columns freely)."),
])
def test_a_gloss_never_inherits_a_flip_word_that_hides_its_own(tmp_path, capsys, sentence, rule):
    code, out = _moved(tmp_path, capsys, sentence, rule)
    assert code == 1 and "drops" in out["failures"][0]["reason"], out


# I4‴: a clause that is only a keyword joins its neighbour.

def test_a_keyword_only_clause_joins_its_neighbour(tmp_path, capsys):
    from cookr.core.rolework import clauses
    assert clauses("Never, under any load, disable foreign keys.") == [
        "Never under any load", "disable foreign keys."]
    assert clauses("Disable foreign keys, MUST NOT.") == ["Disable foreign keys MUST NOT."]
    code, out = _moved(tmp_path, capsys, "Never, under any load, disable foreign keys.",
                       "MUST NOT log secrets; disable foreign keys under any load.")
    assert code == 1 and "negation" in out["failures"][0]["reason"], out


# m10: an obsolete verdict is pinned to the topic text it was judged against.

def test_an_obsolete_verdict_is_stale_once_the_topic_text_changes(tmp_path, capsys):
    folder, base = _from_copy(tmp_path, OBS)
    _judge_all(folder)
    _write_pins(folder)
    assert _lossless(capsys, folder, base)[0] == 0
    (folder / "rules.md").write_text(RULES + "- **must-name-keys**: Every key MUST be named.\n\n",
                                     encoding="utf-8")
    code, out, _ = _lossless(capsys, folder, base)
    assert code == 1 and "stale" in out["failures"][0]["reason"], out


# ── 0.21.2–0.21.3: one retarget after a judged fail, by `--retarget` ──────────

RETARGET_EXTRA = "- **r2**: A sync system MUST record the conflict resolution strategy it uses.\n"


def _retarget_folder(tmp_path, capsys):
    """REWORDED moved to `r` and judged fail (pinned); `r2` also exists."""
    _moved(tmp_path, capsys, *REWORDED, extra_rules=RETARGET_EXTRA)
    folder = tmp_path / T
    data = json.loads((folder / "lossless.json").read_text(encoding="utf-8"))
    data["moved"][0]["judged"] = {"by": "judge-model", "verdict": "fail",
                                  "note": "lost: the strategy is recorded, which r2 carries"}
    (folder / "lossless.json").write_text(json.dumps(data), encoding="utf-8")
    _write_pins(folder)
    return folder, data["base"]


def _edit(folder, change):
    data = json.loads((folder / "lossless.json").read_text(encoding="utf-8"))
    change(data["moved"][0])
    (folder / "lossless.json").write_text(json.dumps(data), encoding="utf-8")


def _retarget(capsys, folder, *to, entry=1):
    """`roles lossless --retarget <folder> --entry <n> --to <name>...`, the one
    way to retarget: (exit code, JSON or None, the error as one line)."""
    capsys.readouterr()
    code = main(["roles", "lossless", "--retarget", str(folder), "--entry", str(entry),
                 *[a for name in to for a in ("--to", name)]])
    captured = capsys.readouterr()
    if code == 0:
        return code, json.loads(captured.out), captured.err
    return code, None, " ".join((captured.out + captured.err).split())


def _hand_retarget(m, to):
    """A retarget made by hand, as the 1.4.7 SKILL documented it: the fail
    moved into `retargeted`, `to` changed."""
    m["retargeted"] = {"from": m["to"], "judged": m.pop("judged")}
    m["to"] = to


def _judge(folder, by, verdict, note):
    _edit(folder, lambda m: m.update(judged={"by": by, "verdict": verdict, "note": note}))
    _write_pins(folder)


def _retargeted_and_failed_again(tmp_path, capsys):
    """REWORDED retargeted once (by `--retarget`) from `r` to `r` + `r2`, then
    judged fail again by judge-2, pinned: the hard failure."""
    folder, base = _retarget_folder(tmp_path, capsys)
    code, _, err = _retarget(capsys, folder, "r", "r2")
    assert code == 0, err
    _judge(folder, "judge-2", "fail", "still lost")
    return folder, base


def test_a_judged_fail_may_be_retargeted_once_and_the_retarget_is_kept(tmp_path, capsys):
    folder, base = _retarget_folder(tmp_path, capsys)
    code, out, _ = _lossless(capsys, folder, base)
    assert code == 1 and out["counts"]["judged_fail"] == 1
    first = json.loads((folder / "lossless.json").read_text(encoding="utf-8"))["moved"][0]["judged"]
    # the one retarget, by cookr: the first fail moves into `retargeted`, `to` grows
    code, out, err = _retarget(capsys, folder, "r", "r2")
    assert code == 0, err
    assert out["entry"] == 1 and out["from"] == "r" and out["to"] == ["r", "r2"]
    data = json.loads((folder / "lossless.json").read_text(encoding="utf-8"))
    m = data["moved"][0]
    assert m["to"] == ["r", "r2"] and "judged" not in m
    assert m["retargeted"]["from"] == "r" and m["retargeted"]["to"] == ["r", "r2"]
    assert m["retargeted"]["judged"] == first and len(m["retargeted"]["seal"]) == 64
    assert data["retargets"] == [m["sentence"]]
    code, out, _ = _lossless(capsys, folder, base)
    assert code == 1 and out["failures"][0]["reason"] == "reworded, and no judged pass"
    assert out["failures"][0]["retargeted"] is True
    # a fresh judge's pass on the new targets passes, the retarget shown
    _judge(folder, "judge-2", "pass", "kept")
    code, out, _ = _lossless(capsys, folder, base)
    assert code == 0, out["failures"]
    assert out["moved"][0]["retargeted"] is True and out["counts"]["reworded_judged"] == 1


def test_a_judged_fail_after_the_retarget_is_recorded_as_the_hard_failure(tmp_path, capsys):
    folder, base = _retargeted_and_failed_again(tmp_path, capsys)
    code, out, _ = _lossless(capsys, folder, base)
    assert code == 1 and out["counts"]["judged_fail"] == 1
    assert "after its one retarget" in out["failures"][0]["reason"]


def test_a_second_retarget_is_refused_however_it_is_made(tmp_path, capsys):
    # 0.21.3, review finding 1: each way of retargeting a second time exits
    # non-zero, naming the entry.
    folder, base = _retargeted_and_failed_again(tmp_path, capsys)
    sentence = json.loads((folder / "lossless.json").read_text(encoding="utf-8"))["moved"][0]["sentence"]
    pristine = (folder / "lossless.json").read_text(encoding="utf-8")
    # by cookr, again: refused, nothing written
    code, _, err = _retarget(capsys, folder, "r", "r2", "must-index-foreign-keys")
    assert code != 0 and "second retarget" in err and "entry 1" in err
    assert (folder / "lossless.json").read_text(encoding="utf-8") == pristine

    def by_hand(change):
        (folder / "lossless.json").write_text(pristine, encoding="utf-8")
        _edit(folder, change)
        _judge(folder, "judge-3", "pass", "kept")   # a fresh judge passes the new targets
        code, out, _ = _lossless(capsys, folder, base)
        assert code == 1, out
        failure = next(f for f in out["failures"] if f["sentence"])
        assert failure["sentence"] == sentence and "a second retarget is refused" in failure["reason"], failure
        return failure

    three = ["r", "r2", "must-index-foreign-keys"]
    # the reviewer's probe: step 4 repeated by hand (the second fail moved into
    # `retargeted`, a new `to`)
    by_hand(lambda m: _hand_retarget(m, three))
    # ... with the record's `to` written too
    by_hand(lambda m: (_hand_retarget(m, three), m["retargeted"].update(to=three)))
    # the variant: only the second `judged` deleted, `to` changed
    by_hand(lambda m: (m.pop("judged"), m.update(to=three)))
    # the record deleted with it: the ledger still names the sentence
    by_hand(lambda m: (m.pop("judged"), m.pop("retargeted"), m.update(to=three)))


def test_a_lossless_round_re_arms_judging_after_the_retarget(tmp_path, capsys):
    # Controller ruling: the hard failure opens a lossless round; after the
    # author's rewrite the retargeted entry's fail is stale and is re-judged,
    # and a pass clears it. The retarget allowance stays spent.
    folder, base = _retargeted_and_failed_again(tmp_path, capsys)
    rules = folder / "rules.md"
    rules.write_text(rules.read_text(encoding="utf-8").replace(
        REWORDED[1], "Every sync system MUST have an explicit conflict resolution strategy, recorded."),
        encoding="utf-8")
    code, out, err = _lossless(capsys, folder, base)
    assert code == 1 and out["counts"]["judged_fail"] == 0 and out["counts"]["stale"] == 1, out
    failure = out["failures"][0]
    assert failure["stale"] is True and failure["retargeted"] is True
    assert "stale" in failure["reason"] and "after its one retarget" not in failure["reason"]
    assert "stale:" in err
    _judge(folder, "judge-3", "pass", "kept after the rewrite")
    code, out, _ = _lossless(capsys, folder, base)
    assert code == 0, out["failures"]
    assert out["moved"][0]["retargeted"] is True and out["counts"]["reworded_judged"] == 1
    code, _, err = _retarget(capsys, folder, "r2")
    assert code != 0 and "second retarget" in err


@pytest.mark.parametrize("case", [
    "no-fail",       # only a judged fail is retargeted
    "stale-fail",    # ... one whose pin matches the targets now
    "same-to",       # the targets must change
    "too-many",      # still at most 3
    "unknown",       # every target exists
    "obsolete",      # an obsolete entry is never retargeted
    "no-entry",
    "bar",           # 0.21.4, N2: the new targets must pass the 80% bar ...
    "bar-r2",        # ... (r2 alone holds 75%)
])
def test_retarget_refuses_what_is_not_one_retarget(tmp_path, capsys, case):
    folder, _ = _retarget_folder(tmp_path, capsys)
    to, entry = ["r", "r2"], 1
    if case == "no-fail":
        _judge(folder, "j", "pass", "kept")
    elif case == "stale-fail":
        _edit(folder, lambda m: m["judged"].update(pin="0" * 64))
    elif case == "same-to":
        to = ["r"]
    elif case == "too-many":
        (folder / "rules.md").write_text((folder / "rules.md").read_text(encoding="utf-8")
                                         + "- **r3**: x MUST y.\n- **r4**: z MUST w.\n", encoding="utf-8")
        _write_pins(folder)
        to = ["r", "r2", "r3", "r4"]
    elif case == "unknown":
        to = ["r", "nope"]
    elif case == "obsolete":
        data = json.loads((folder / "lossless.json").read_text(encoding="utf-8"))
        data["obsolete"] = [{"sentence": "x.", "reason": "gone",
                             "judged": {"by": "j", "verdict": "fail", "note": "n"}}]
        (folder / "lossless.json").write_text(json.dumps(data), encoding="utf-8")
        entry = 2
    elif case == "no-entry":
        entry = 5
    elif case == "bar":
        to = ["must-index-foreign-keys"]
    elif case == "bar-r2":
        to = ["r2"]
    before = (folder / "lossless.json").read_text(encoding="utf-8")
    code, _, err = _retarget(capsys, folder, *to, entry=entry)
    assert code != 0 and f"entry {entry}" in err, err
    assert (folder / "lossless.json").read_text(encoding="utf-8") == before
    if case.startswith("bar"):
        assert "at least 80% needed" in err, err
        # the refusal spent nothing: good targets still retarget it
        code, _, err = _retarget(capsys, folder, "r", "r2")
        assert code == 0, err


def test_a_retarget_survives_the_file_rewritten_with_sorted_keys(tmp_path, capsys):
    # 0.21.4, N3: the seal is taken over canonical JSON, so re-serialising
    # lossless.json (sorted keys, other spacing) keeps a valid retarget valid.
    folder, base = _retarget_folder(tmp_path, capsys)
    code, _, err = _retarget(capsys, folder, "r", "r2")
    assert code == 0, err
    _judge(folder, "judge-2", "pass", "kept")
    code, out, _ = _lossless(capsys, folder, base)
    assert code == 0, out["failures"]
    data = json.loads((folder / "lossless.json").read_text(encoding="utf-8"))
    (folder / "lossless.json").write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    code, out, _ = _lossless(capsys, folder, base)
    assert code == 0, out["failures"]
    (folder / "lossless.json").write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
    code, out, _ = _lossless(capsys, folder, base)
    assert code == 0, out["failures"]


@pytest.mark.parametrize("bad", [
    True,
    {"from": "r", "judged": {"by": "j", "verdict": "pass", "note": "kept"}},
    {"from": "r", "judged": "fail"},
    {"judged": {"by": "j", "verdict": "fail", "note": "lost"}},
    {"from": ["r2", "r"], "to": ["r", "r2"], "judged": {"by": "j", "verdict": "fail", "note": "lost"},
     "seal": "0" * 64},
])
def test_a_retarget_record_cookr_did_not_write_fails_by_name(tmp_path, capsys, bad):
    folder, base = _retarget_folder(tmp_path, capsys)
    _edit(folder, lambda m: m.update(to=["r", "r2"], retargeted=bad))
    code, out, _ = _lossless(capsys, folder, base, "--draft")
    assert code == 1 and "a second retarget is refused" in out["failures"][0]["reason"], out
    assert out["failures"][0]["sentence"]


def test_an_obsolete_entry_is_never_retargeted_and_the_ledger_is_names(tmp_path, capsys):
    from cookr.core.rolework import RoleworkError, read_accounting
    folder, base = _retarget_folder(tmp_path, capsys)
    data = json.loads((folder / "lossless.json").read_text(encoding="utf-8"))
    data["obsolete"] = [{"sentence": "x.", "reason": "gone",
                         "retargeted": {"from": "r", "judged": {"by": "j", "verdict": "fail", "note": "n"}}}]
    (folder / "lossless.json").write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(RoleworkError):
        read_accounting(folder)
    for ledger in ("x.", [1], [""]):
        data = json.loads((folder / "lossless.json").read_text(encoding="utf-8"))
        data["obsolete"], data["retargets"] = [], ledger
        (folder / "lossless.json").write_text(json.dumps(data), encoding="utf-8")
        with pytest.raises(RoleworkError):
            read_accounting(folder)
