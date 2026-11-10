import pytest

from cookr.cli import main

from .cookbook_helpers import add_doc, add_spec, edit_repo_config, new_repo


# Every tmp_path here is a git repo, as a real cookbook checkout is.
pytestmark = pytest.mark.usefixtures("git_tmp_path")


def test_validate_fails_on_a_doc_edited_by_hand(tmp_path, monkeypatch, patch_refs, capsys):
    monkeypatch.chdir(tmp_path)
    new_repo(tmp_path)
    cb = tmp_path / "cookbook"
    add_doc(tmp_path, "recipes/alpha", "# Alpha Recipe\n\n## Change History\n\nx\n")
    assert main(["validate", "-p", str(cb)]) == 0
    doc = cb / "recipes" / "alpha.md"
    doc.write_text(doc.read_text() + "Hand edit.\n", encoding="utf-8")
    capsys.readouterr()
    assert main(["validate", "-p", str(cb)]) == 1
    assert "recipes/alpha.md" in capsys.readouterr().out


def test_validate_green_then_drift(tmp_path, monkeypatch, patch_refs):
    monkeypatch.chdir(tmp_path)
    new_repo(tmp_path)
    cb = tmp_path / "cookbook"
    add_doc(tmp_path, "recipes/alpha", "# Alpha Recipe\n")
    assert main(["validate", "-p", str(cb)]) == 0  # green

    # Induce drift: a compiled doc that no longer matches its folder.
    doc = cb / "recipes" / "alpha.md"
    doc.write_text(doc.read_text() + "Drift.\n", encoding="utf-8")
    rc = main(["validate", "-p", str(cb)])
    assert rc != 0  # drift detected


def test_validate_passes_a_folder_without_its_compiled_doc(tmp_path, monkeypatch, patch_refs,
                                                          capsys):
    # The folder is the only committed form: a clean checkout has no docs.
    monkeypatch.chdir(tmp_path)
    new_repo(tmp_path)
    cb = tmp_path / "cookbook"
    add_doc(tmp_path, "recipes/alpha", "# Alpha Recipe\n\n## Change History\n\nx\n")
    (cb / "recipes" / "alpha.md").unlink()
    capsys.readouterr()
    assert main(["validate", "-p", str(cb)]) == 0
    assert "0 compiled docs present" in capsys.readouterr().out


def _converted(tmp_path, monkeypatch, body):
    monkeypatch.chdir(tmp_path)
    new_repo(tmp_path)
    add_doc(tmp_path, "recipes/alpha", f"# Alpha Recipe\n\n{body}\n\n## Change History\n\nx\n")
    return tmp_path / "cookbook"


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


def _guideline(tmp_path, use_case, body):
    return add_doc(tmp_path, f"guidelines/{use_case}/logging", f"# Logging\n\n{body}\n\n## Change History\n\nx\n",
                   type="guideline")


def test_validate_fails_on_twins_that_drifted_and_on_a_guideline_with_no_rule(
        tmp_path, monkeypatch, patch_refs, capsys):
    monkeypatch.chdir(tmp_path)
    new_repo(tmp_path)
    cb = tmp_path / "cookbook"
    _guideline(tmp_path, "implementing", "Logs MUST be JSON.")
    _guideline(tmp_path, "reviewing", "Check the logs.")
    capsys.readouterr()
    assert main(["validate", "-p", str(cb)]) == 1
    out = capsys.readouterr().out
    assert "drift" in out and "no-rules" in out

    manifest = cb / "guidelines" / "reviewing" / "logging" / "artifact.json"
    manifest.write_text(manifest.read_text().replace(
        '  "parts"', '  "twin_differs": "A review checklist of the implementing guideline.",\n'
                     '  "informational": "A checklist; its rules are its twin\'s.",\n  "parts"'),
        encoding="utf-8")
    assert main(["validate", "-p", str(cb)]) == 0


# --- UUID links: missing is an issue, unreachable a warning ---------------------------

GONE = "0b0b0b0b-0000-4000-8000-000000000000"
ELSEWHERE = "0e0e0e0e-0000-4000-8000-000000000000"


def _format_2(tmp_path, monkeypatch, body, dependencies=None):
    """A converted cookbook made format 2, so its UUID links resolve."""
    cb = _converted(tmp_path, monkeypatch, body)
    if dependencies:
        edit_repo_config(tmp_path, lambda d: d.update(dependencies=dependencies))
    return cb


def test_validate_reports_missing_link(tmp_path, monkeypatch, patch_refs, capsys):
    monkeypatch.setenv("COLUMNS", "300")
    cb = _format_2(tmp_path, monkeypatch, f"See [gone](cookbook:{GONE}).")
    capsys.readouterr()
    assert main(["validate", "-p", str(cb)]) == 1
    out = capsys.readouterr().out
    assert f"`{GONE}` names no artifact in its cookbook" in out


def test_validate_warns_unreachable_cookbook(tmp_path, monkeypatch, patch_refs, capsys):
    monkeypatch.setenv("COLUMNS", "300")
    cb = _format_2(tmp_path, monkeypatch, f"See [far](cookbook:{ELSEWHERE}/{GONE}).",
                   dependencies={ELSEWHERE: {"rdid": "elsewhere"}})
    capsys.readouterr()
    assert main(["validate", "-p", str(cb)]) == 0  # a warning never fails validate
    out = capsys.readouterr().out
    assert f"cookbook {ELSEWHERE} cannot be reached here" in out
    assert "1 warning(s)" in out



# Opts out of upgrade-on-contact: validate must itself report a loose doc that no source folder
# compiles (contact would otherwise convert it first and exit 3).
@pytest.mark.usefixtures("legacy_no_upgrade")
def test_validate_fails_on_a_loose_doc_with_no_source_folder(tmp_path, monkeypatch, patch_refs,
                                                             capsys):
    monkeypatch.chdir(tmp_path)
    new_repo(tmp_path)
    cb = tmp_path / "cookbook"
    (cb / "recipes").mkdir()
    (cb / "recipes" / "loose.md").write_text("---\ntitle: Loose\ntype: recipe\n---\n# Loose\n",
                                             encoding="utf-8")
    capsys.readouterr()
    assert main(["validate", "-p", str(cb)]) == 1
    assert "recipes/loose.md" in capsys.readouterr().out


def test_validate_finds_index_configs_in_a_source_checkout(tmp_path, monkeypatch, capsys):
    # From source, ./install has not built references/: the embedded copy is used.
    from cookr.core import refs
    empty = tmp_path / "built-references"
    empty.mkdir()
    monkeypatch.setattr(refs, "references_dir", lambda: empty)
    assert refs.embedded(empty, "index-configs") == refs._root() / "references-src" / "index-configs"
    (empty / "index-configs").mkdir()
    assert refs.embedded(empty, "index-configs") == empty / "index-configs"
    (empty / "index-configs").rmdir()
    monkeypatch.chdir(tmp_path)
    new_repo(tmp_path)
    capsys.readouterr()
    main(["validate", "-p", str(tmp_path / "cookbook")])
    out = capsys.readouterr().out
    assert "No index configs found" not in out
    assert "recipes-flat" in out
