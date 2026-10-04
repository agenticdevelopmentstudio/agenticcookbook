import pytest

from cookr.cli import main


# Every tmp_path here is a git repo, as a real cookbook checkout is.
pytestmark = pytest.mark.usefixtures("git_tmp_path")


def test_validate_fails_on_a_doc_edited_by_hand(tmp_path, monkeypatch, patch_refs, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["create"]) == 0
    cb = tmp_path / "cookbook"
    (cb / "recipes" / "alpha.md").write_text("# Alpha Recipe\n\n## Change History\n\nx\n", encoding="utf-8")
    assert main(["update", "-p", str(cb), "--author", "Tester"]) == 0
    assert main(["convert", str(cb / "recipes" / "alpha.md")]) == 0
    assert main(["update", "-p", str(cb), "--author", "Tester"]) == 0
    assert main(["validate", "-p", str(cb)]) == 0
    doc = cb / "recipes" / "alpha.md"
    doc.write_text(doc.read_text() + "Hand edit.\n", encoding="utf-8")
    capsys.readouterr()
    assert main(["validate", "-p", str(cb)]) == 1
    assert "recipes/alpha.md" in capsys.readouterr().out


def test_validate_green_then_drift(tmp_path, monkeypatch, patch_refs):
    monkeypatch.chdir(tmp_path)
    assert main(["create"]) == 0
    cb = tmp_path / "cookbook"
    (cb / "recipes" / "alpha.md").write_text("# Alpha Recipe\n", encoding="utf-8")
    assert main(["update", "-p", str(cb), "--author", "Tester"]) == 0
    assert main(["validate", "-p", str(cb)]) == 1  # a doc no folder compiles is checked by nothing
    assert main(["convert", str(cb / "recipes" / "alpha.md")]) == 0
    assert main(["validate", "-p", str(cb)]) == 0  # green

    # Induce drift by adding a new file without re-running update.
    (cb / "recipes" / "gamma.md").write_text(
        "---\ntitle: Gamma\nid: 22222222-3333-4444-5555-666666666666\n"
        "domain: agenticdevelopercookbook://cookbook/recipes/gamma\ntype: recipe\n"
        "version: 1.0.0\nstatus: draft\nlanguage: en\ncreated: 2026-05-15\n"
        "modified: 2026-05-15\nauthor: T\ncopyright: 2026 T\nlicense: MIT\nsummary: x\n"
        "---\n# Gamma\n",
        encoding="utf-8",
    )
    assert main(["convert", str(cb / "recipes" / "gamma.md")]) == 0
    rc = main(["validate", "-p", str(cb)])
    assert rc != 0  # drift detected


def _converted(tmp_path, monkeypatch, body):
    monkeypatch.chdir(tmp_path)
    assert main(["create"]) == 0
    cb = tmp_path / "cookbook"
    (cb / "recipes" / "alpha.md").write_text(f"# Alpha Recipe\n\n{body}\n\n## Change History\n\nx\n",
                                             encoding="utf-8")
    assert main(["update", "-p", str(cb), "--author", "Tester"]) == 0
    assert main(["convert", str(cb / "recipes" / "alpha.md")]) == 0
    assert main(["update", "-p", str(cb), "--author", "Tester"]) == 0
    return cb


def test_validate_fails_on_shared_text_that_names_a_host(tmp_path, monkeypatch, patch_refs, capsys):
    cb = _converted(tmp_path, monkeypatch, "Ask Claude to do it.")
    capsys.readouterr()
    assert main(["validate", "-p", str(cb)]) == 1
    assert "unlisted" in capsys.readouterr().out
    manifest = cb / "recipes" / "alpha" / "artifact.json"
    manifest.write_text(manifest.read_text().replace(
        '  "parts"', '  "names_hosts": "Its subject is a Claude feature.",\n  "parts"'), encoding="utf-8")
    assert main(["validate", "-p", str(cb)]) == 0


def test_validate_fails_on_a_broken_addition_and_warns_on_a_stale_one(tmp_path, monkeypatch,
                                                                       patch_refs, capsys):
    from cookr.core import tuning
    cb = _converted(tmp_path, monkeypatch, "Plain.")
    hosts_dir = cb / "recipes" / "alpha" / "hosts"
    hosts_dir.mkdir()
    (hosts_dir / "claude.add.md").write_text(tuning.stamp("Tuned.\n", ".md", tuning.source_hash("old")))
    capsys.readouterr()
    assert main(["validate", "-p", str(cb)]) == 0
    assert "older source" in capsys.readouterr().out
    (hosts_dir / "gemini.add.md").write_text("x\n")
    assert main(["validate", "-p", str(cb)]) == 1
