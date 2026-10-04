"""The neutrality census and `names_hosts`."""

from __future__ import annotations

from cookr.core import neutrality
from cookr.core.artifact import Artifact, Part, dump_manifest, load_folder, save_document, write_folder


def make(folder, text, reason=None, history="v1 tuned for Claude\n"):
    write_folder(Artifact(meta={"id": "x", "type": "guideline"}, parts=[
        Part("intro", f"# T\n\n{text}\n"),
        Part("history", history, "Change History"),
    ], names_hosts=reason), folder)
    return folder


def kinds(*folders):
    return [(f.folder.name, f.kind) for f in neutrality.census(folders)]


def test_neutral_text_passes(tmp_path):
    assert kinds(make(tmp_path / "a", "Plain advice.")) == []


def test_naming_a_host_without_a_reason_fails(tmp_path):
    f = make(tmp_path / "a", "Use Opus for this, or ask Claude.")
    [finding] = neutrality.census([f])
    assert finding.kind == "unlisted" and finding.words == ["opus", "claude"]


def test_a_reason_lets_it_name_hosts(tmp_path):
    assert kinds(make(tmp_path / "a", "Claude Code reads CLAUDE.md.",
                      "Documents Claude Code's instruction file.")) == []


def test_a_reason_with_nothing_to_explain_is_stale(tmp_path):
    assert kinds(make(tmp_path / "a", "Plain.", "Used to name a host here.")) == [("a", "stale")]


def test_a_short_reason_is_flagged(tmp_path):
    assert kinds(make(tmp_path / "a", "Claude.", "subject")) == [("a", "short")]


def test_history_and_word_fragments_do_not_count(tmp_path):
    assert kinds(make(tmp_path / "a", "An octopus, claudette's codexes and sonnets.")) == []


def test_names_hosts_round_trips_and_survives_a_doc_edit(tmp_path):
    folder = make(tmp_path / "a", "Claude.", "Documents a Claude feature.")
    assert load_folder(folder).names_hosts == "Documents a Claude feature."
    assert '"names_hosts"' in dump_manifest(load_folder(folder))
    doc = tmp_path / "a.md"
    save_document(doc, "---\nid: x\ntype: guideline\n---\n# T\n\nClaude, edited.\n")
    assert load_folder(folder).names_hosts == "Documents a Claude feature."


def test_no_reason_writes_no_key(tmp_path):
    assert "names_hosts" not in dump_manifest(load_folder(make(tmp_path / "a", "Plain.")))
