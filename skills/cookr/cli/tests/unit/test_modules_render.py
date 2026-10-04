"""`cookr targets` and `cookr render` at the CLI level."""

from __future__ import annotations

import json

import pytest

from cookr.cli import main

SKILL = "---\nname: demo\ndescription: Does the demo thing.\n---\n\n# Demo\n"


@pytest.fixture
def skill(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    d = tmp_path / "demo"
    (d / "hosts").mkdir(parents=True)
    (d / "SKILL.md").write_text(SKILL)
    (d / "hosts" / "claude.add.md").write_text("For Claude.\n")
    (d / "hosts" / "claude.opus.add.yaml").write_text("model: opus\n")
    return d


def test_targets_resolves_a_model_chain(capsys):
    assert main(["targets", "--host", "claude", "--model", "claude-opus-5-5", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["chain"] == ["claude", "claude.opus", "claude.opus-5-5"]


def test_targets_lists_every_host(capsys):
    assert main(["targets", "--json"]) == 0
    assert {"claude", "codex"} <= set(json.loads(capsys.readouterr().out))


def test_targets_refuses_a_model_without_a_host_and_an_unknown_host():
    assert main(["targets", "--model", "gpt-5"]) == 2
    assert main(["targets", "--host", "nope"]) == 2


def test_render_prints_the_layered_text(skill, capsys):
    assert main(["render", str(skill), "--host", "claude", "--model", "claude-opus-5-5"]) == 0
    out = capsys.readouterr().out
    assert "model: opus\n" in out and out.endswith("# Demo\n\nFor Claude.\n")


def test_render_for_another_host_is_the_source(skill, capsys):
    assert main(["render", str(skill), "--host", "codex"]) == 0
    assert capsys.readouterr().out == SKILL


def test_a_tuning_that_breaks_a_host_is_broken(skill, capsys):
    (skill / "hosts" / "codex.add.yaml").write_text("model: gpt-5\n")
    assert main(["render", str(skill), "--host", "codex", "--json"]) == 1
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "BROKEN" and "model" in result["problems"][0]


def test_render_out_writes_the_file(skill, tmp_path):
    out = tmp_path / "built" / "SKILL.md"
    assert main(["render", str(skill), "--host", "claude", "--out", str(out)]) == 0
    assert out.read_text().endswith("For Claude.\n")


def test_render_refuses_a_dir_without_a_skill(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert main(["render", str(tmp_path), "--host", "claude"]) == 2
