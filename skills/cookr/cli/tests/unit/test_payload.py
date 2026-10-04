"""Self-tuning: target parsing, the survey, worklists, stamping, staleness."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from cookr.cli import main
from cookr.core import always_on, hosts, payload, skill, tuning
from cookr.core.artifact import find_folders

from .test_skill import make


@pytest.fixture
def book(tmp_path):
    root = tmp_path / "cookbook"
    make(root, "guidelines/implementing/data/use-wal", "guideline")
    make(root, "principles/simplicity", "principle")
    return root


@pytest.fixture
def templates(tmp_path):
    s, a = tmp_path / "t" / "skill", tmp_path / "t" / "always"
    shutil.copytree(skill.TEMPLATES, s, ignore=shutil.ignore_patterns(tuning.HOSTS_DIR))
    shutil.copytree(always_on.TEMPLATES, a, ignore=shutil.ignore_patterns(tuning.HOSTS_DIR))
    return payload.template_levels(s, a)


def test_parse_target_names_host_family_or_model():
    assert hosts.parse_target("claude") == ("claude", "claude.opus", "claude.opus-5-5")
    assert hosts.parse_target("claude.opus") == ("claude", "claude.opus")
    assert hosts.parse_target("claude.claude-opus-5-5") == hosts.parse_target("claude.opus-5-5")
    assert hosts.parse_target("codex.gpt-5-codex") == ("codex", "codex.gpt-5", "codex.gpt-5-codex")
    with pytest.raises(hosts.HostError):
        hosts.parse_target("nope.x")


def test_levels_cover_every_template_and_find_an_additions_owner(book, templates):
    names = [lv.name for lv in templates]
    assert names == ["template:guideline", "template:ingredient", "template:principle",
                     "template:recipe", "always:principles"]
    wal = book / "guidelines/implementing/data/use-wal"
    assert payload.level_of(wal / "hosts/claude.add.md", templates).kind == payload.ARTIFACT
    assert payload.level_of(templates[0].hosts_dir / "codex.add.md", templates) == templates[0]
    with pytest.raises(payload.PayloadError):
        payload.level_of(wal / "claude.add.md", templates)


def test_a_stamped_addition_goes_stale_when_its_template_changes(book, templates):
    lv = templates[0]
    lv.hosts_dir.mkdir(parents=True)
    add = lv.hosts_dir / "claude.opus.add.md"
    add.write_text("Opus: read the MUST rules first.\n")
    chain = hosts.parse_target("claude.opus-5-5")
    entry = payload.describe(lv, chain, text=True)
    assert entry["additions"][0]["stamped"] is False and "{{body}}" in entry["text"]
    assert payload.stamp_addition(add, templates) == (lv, True)
    assert payload.stamp_addition(add, templates) == (lv, False)
    assert payload.describe(lv, chain)["additions"][0] == {
        "target": "claude.opus", "kind": ".md", "path": str(add), "stamped": True, "stale": False}
    lv.source_path.write_text(lv.source_path.read_text() + "Edited.\n")
    assert payload.describe(lv, chain)["additions"][0]["stale"] is True
    assert payload.describe(lv, ("codex",))["additions"] == []


def test_an_artifact_addition_is_stale_after_a_body_edit_not_a_history_row(book):
    wal = book / "guidelines/implementing/data/use-wal"
    (wal / "hosts").mkdir()
    add = wal / "hosts/codex.add.md"
    add.write_text("Codex: run the migration check.\n")
    payload.stamp_addition(add)
    lv = payload.artifact_level(wal)
    assert not payload.describe(lv, ("codex",))["additions"][0]["stale"]
    (wal / "history.md").write_text((wal / "history.md").read_text() + "| 1.2.1 | x | y | z |\n")
    assert not payload.describe(lv, ("codex",))["additions"][0]["stale"]
    (wal / "intro.md").write_text((wal / "intro.md").read_text() + "More.\n")
    assert payload.describe(lv, ("codex",))["additions"][0]["stale"]


def test_the_worklist_holds_the_skill_as_the_target_reads_it(book):
    wal = book / "guidelines/implementing/data/use-wal"
    (wal / "hosts").mkdir()
    (wal / "hosts/claude.opus.add.md").write_text("Opus note.\n")
    chain = hosts.parse_target("claude.opus-5-5")
    items = {i["skill"]: i for i in payload.worklist(chain, find_folders([book]))}
    item = items["implementing-data-use-wal"]
    assert item["text"].endswith("Opus note.\n")
    assert item["write_to"] == str(wal / "hosts/claude.opus-5-5.add.md")
    assert item["existing"] == [str(wal / "hosts/claude.opus.add.md")]
    assert "Opus note." not in items["principle-simplicity"]["text"]


def test_the_cli_surveys_writes_worklists_and_stamps(book, tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(book.parent)
    assert main(["payload", "--target", "codex", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["chain"] == ["codex"] and len(data["artifacts"]) == 2 and data["worklists"] == []
    assert main(["payload", "--target", "claude.opus-5-5", "--out-dir", "wl", "--batch-size", "1"]) == 0
    assert sorted(p.name for p in (book.parent / "wl").iterdir()) == ["worklist-01.json", "worklist-02.json"]
    assert main(["payload", "--target", "nope"]) == 2
    wal = book / "guidelines/implementing/data/use-wal"
    (wal / "hosts").mkdir()
    (wal / "hosts/codex.add.md").write_text("Note.\n")
    (wal / "hosts/nope.add.md").write_text("Note.\n")
    capsys.readouterr()
    assert main(["stamp", str(wal / "hosts/codex.add.md"), "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["results"][0]["stamped"] is True
    assert (wal / "hosts/codex.add.md").read_text().startswith("<!-- cookr:source sha256:")
    assert main(["stamp", str(wal / "hosts/nope.add.md")]) == 1
    assert main(["stamp", str(wal / "hosts/missing.md")]) == 1
