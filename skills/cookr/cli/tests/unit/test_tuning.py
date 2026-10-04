"""Layered tuning: additions, render, load rules, provenance."""

from __future__ import annotations

import pytest

from cookr.core import hosts, tuning
from cookr.core.tuning import TuningError

SKILL = """---
name: demo-skill
description: >-
  Does the demo thing
  across two lines.
version: 1.0.0
---

# Demo

Shared text.
"""


def write(d, files):
    d.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        (d / name).write_text(text)
    return d


def test_no_additions_renders_byte_identical(tmp_path):
    adds = tuning.layers([tmp_path / "hosts"], hosts.chain("claude", "claude-opus-5-5"))
    assert adds == []
    assert tuning.render(SKILL, adds) == SKILL


def test_layers_apply_host_then_family_then_version(tmp_path):
    d = write(tmp_path / "hosts", {
        "claude.add.md": "Host line.\n",
        "claude.opus.add.md": "Family line.\n",
        "claude.opus-5-5.add.md": "\n\nVersion line.\n\n",
        "claude.sonnet.add.md": "Not for opus.\n",
        "codex.add.md": "Not for claude.\n",
    })
    text = tuning.render(SKILL, tuning.layers([d], hosts.chain("claude", "claude-opus-5-5")))
    assert text.endswith("Shared text.\n\nHost line.\n\nFamily line.\n\nVersion line.\n")
    assert "Not for" not in text


def test_a_later_level_wins_over_an_earlier_one(tmp_path):
    template = write(tmp_path / "template", {"claude.add.yaml": "model: sonnet\n"})
    own = write(tmp_path / "own", {"claude.add.yaml": "model: opus\n"})
    text = tuning.render(SKILL, tuning.layers([template, own], ("claude",)))
    assert "model: opus\n" in text and "sonnet" not in text


def test_yaml_replaces_in_place_keeps_continuations_and_appends_new_keys():
    fm, _ = tuning.split(SKILL)
    merged = "".join(tuning.merge_frontmatter(fm, "description: Short.\nmodel: opus\n"))
    assert merged == "name: demo-skill\ndescription: Short.\nversion: 1.0.0\nmodel: opus\n"


def test_a_replaced_key_drops_its_later_duplicates():
    merged = tuning.merge_frontmatter(["a: 1\n", "b: 2\n", "a: 3\n"], "a: 9\n")
    assert merged == ["a: 9\n", "b: 2\n"]


def test_yaml_addition_on_text_without_frontmatter_creates_one():
    out = tuning.render("# Body\n", [tuning.Addition(None, "claude", ".yaml", "model: opus\n", None)])
    assert out == "---\nmodel: opus\n---\n# Body\n"


def test_an_empty_md_addition_changes_nothing():
    assert tuning.append_body("x\n", "\n\n") == "x\n"


def test_an_unclosed_fence_is_an_error():
    with pytest.raises(TuningError, match="never closed"):
        tuning.split("---\nname: x\n")


@pytest.mark.parametrize("line,why", [
    ("description: Use it: always\n", "nested key"),
    ("description: ends with:\n", "no value"),
    ("description: fine #not\n", "comment"),
    ("not a pair\n", "one line"),
    ("model: a\nmodel: b\n", "set twice"),
])
def test_yaml_addition_problems(tmp_path, line, why):
    d = write(tmp_path / "hosts", {"claude.add.yaml": line})
    problems = tuning.addition_problems(tuning.additions(d).values(), hosts.manifest())
    assert any(why in p for p in problems), problems


def test_quoted_values_are_not_traps(tmp_path):
    d = write(tmp_path / "hosts", {"claude.add.yaml": 'description: "Use it: always"\ntools: [a, b]\n'})
    assert tuning.addition_problems(tuning.additions(d).values(), hosts.manifest()) == []


def test_an_addition_for_an_undeclared_host_is_a_problem(tmp_path):
    d = write(tmp_path / "hosts", {"gemini.add.md": "x\n"})
    problems = tuning.addition_problems(tuning.additions(d).values(), hosts.manifest())
    assert "'gemini'" in problems[0]


def test_debris_is_ignored_and_a_wrong_suffix_is_refused(tmp_path):
    d = write(tmp_path / "hosts", {"claude.md~": "x", ".DS_Store": "x", "claude.md.swp": "x"})
    assert tuning.additions(d) == {}
    write(d, {"claude.txt": "x"})
    with pytest.raises(TuningError, match="expected <target>.add.md"):
        tuning.additions(d)


def test_a_bare_target_md_is_refused(tmp_path):
    # `claude.md` is `CLAUDE.md` on a case-insensitive filesystem, which Claude
    # Code loads as instructions, so it is never an addition's name.
    d = write(tmp_path / "hosts", {"codex.md": "x"})
    with pytest.raises(TuningError, match="expected <target>.add.md"):
        tuning.additions(d)
    assert tuning.addition_name("claude.opus", ".yaml") == "claude.opus.add.yaml"
    assert tuning.parse_name("claude.opus.add.yaml") == ("claude.opus", ".yaml")
    assert tuning.parse_name("claude.md") is None


def test_a_broken_symlink_is_refused(tmp_path):
    d = tmp_path / "hosts"
    d.mkdir()
    (d / "claude.add.md").symlink_to(tmp_path / "nowhere.md")
    with pytest.raises(TuningError, match="broken symlink"):
        tuning.additions(d)


def test_stamps_are_stripped_and_detect_a_changed_source(tmp_path):
    old, new = tuning.source_hash("old"), tuning.source_hash("new")
    d = write(tmp_path / "hosts", {
        "claude.add.md": tuning.stamp("Tuned.\n", ".md", old),
        "codex.add.yaml": tuning.stamp("model: x\n", ".yaml", new),
        "claude.opus.add.md": "Hand-written.\n",
    })
    found = tuning.additions(d)
    assert found[("claude", ".md")].text == "Tuned.\n"
    assert found[("claude", ".md")].stamp == old
    assert found[("claude.opus", ".md")].stamp is None
    assert [a.target for a in tuning.stale(found.values(), new)] == ["claude"]


def test_restamping_replaces_the_old_stamp():
    once = tuning.stamp("x\n", ".md", "a" * 64)
    assert tuning.stamp(once, ".md", "b" * 64) == f"<!-- cookr:source sha256:{'b' * 64} -->\nx\n"


def test_load_rules_pass_a_portable_skill_on_every_host():
    portable = SKILL.replace("version: 1.0.0\n", "metadata:\n  version: 1.0.0\n")
    for h in hosts.manifest().values():
        assert tuning.load_problems(portable, h) == []


def test_codex_rejects_extra_frontmatter_keys_that_claude_accepts():
    text = SKILL.replace("version: 1.0.0\n", "version: 1.0.0\nmodel: opus\n")
    assert tuning.load_problems(text, hosts.host("claude")) == []
    problems = tuning.load_problems(text, hosts.host("codex"))
    assert "model" in problems[0] and "version" in problems[0]


@pytest.mark.parametrize("text,why", [
    ("# no frontmatter\n", "no frontmatter"),
    ("---\nname: Bad Name\ndescription: x\n---\n", "does not match"),
    ("---\nname: ok\n---\n", "no `description`"),
    ("---\nname: ok\ndescription: '[TODO: fill]'\n---\n", "placeholder"),
    ("---\nname: ok\ndescription: x\n---\n[TODO: write]\n", "unfenced"),
    ("---\nname: ok\ndescription: a <b>\n---\n", "rejects"),
    ("---\nname: [unclosed\n---\n", "not valid YAML"),
])
def test_load_rule_breaches_are_reported(text, why):
    problems = tuning.load_problems(text, hosts.host("codex"))
    assert any(why in p for p in problems), problems


def test_a_fenced_todo_line_is_not_a_breach():
    text = "---\nname: ok\ndescription: x\n---\n```\n[TODO: example]\n```\n"
    assert tuning.load_problems(text, hosts.host("codex")) == []
