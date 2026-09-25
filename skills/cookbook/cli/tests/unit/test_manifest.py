import json

import pytest

from cookbook.core.manifest import ManifestError, main, materialize


def _repo(tmp_path, files, **extra):
    repo = tmp_path / "repo"
    (repo / "content" / "tree" / "sub").mkdir(parents=True)
    (repo / "content" / "one.md").write_text("one")
    (repo / "content" / "tree" / "a.md").write_text("a")
    (repo / "content" / "tree" / "sub" / "b.md").write_text("b")
    (repo / "content" / "tree" / "skip.txt").write_text("x")
    manifest = repo / "pkg" / "reference-manifest.json"
    manifest.parent.mkdir()
    manifest.write_text(json.dumps({"version": 1, "source_root": "content",
                                    "destination": "pkg/references", "files": files, **extra}))
    return repo, manifest


def test_files_and_trees_land_under_the_destination_and_old_content_goes(tmp_path):
    repo, manifest = _repo(tmp_path, [
        {"src": "one.md", "dst": "x/one.md", "type": "file"},
        {"src": "tree", "dst": "t", "type": "tree", "include": "*.md"},
    ])
    dest = repo / "pkg" / "references"
    dest.mkdir()
    (dest / ".gitkeep").write_text("")
    (dest / "stale.md").write_text("old")
    assert materialize(manifest, repo) == dest.resolve()
    got = sorted(p.relative_to(dest).as_posix() for p in dest.rglob("*") if p.is_file())
    assert got == [".gitkeep", "t/a.md", "t/sub/b.md", "x/one.md"]


def test_dest_override_and_embedded_overlay(tmp_path):
    repo, manifest = _repo(tmp_path, [{"src": "one.md", "dst": "one.md", "type": "file"}],
                           embedded_dir="extra")
    (manifest.parent / "extra").mkdir()
    (manifest.parent / "extra" / "e.md").write_text("e")
    out = materialize(manifest, repo, tmp_path / "elsewhere")
    assert sorted(p.name for p in out.iterdir()) == ["e.md", "one.md"]


@pytest.mark.parametrize("entry, message", [
    ({"src": "nope.md", "dst": "n.md", "type": "file"}, "MISSING file"),
    ({"src": "nope", "dst": "n", "type": "tree"}, "MISSING dir"),
    ({"src": "one.md", "dst": "n.md", "type": "tre"}, "unknown entry type"),
    ({"src": "../../etc", "dst": "n", "type": "tree"}, "escapes source_root"),
    ({"src": "one.md", "dst": "../out.md", "type": "file"}, "escapes destination"),
])
def test_bad_entries_are_refused(tmp_path, entry, message):
    repo, manifest = _repo(tmp_path, [entry])
    with pytest.raises(ManifestError, match=message):
        materialize(manifest, repo)


def test_main_reports_a_refusal_and_exits_1(tmp_path, capsys):
    repo, manifest = _repo(tmp_path, [{"src": "nope.md", "dst": "n.md", "type": "file"}])
    assert main([str(repo), str(manifest)]) == 1
    assert "MISSING file" in capsys.readouterr().err


def test_main_prompts_materializes_every_prompt_module(tmp_path, capsys):
    repo, _ = _repo(tmp_path, [])
    prompts = repo / "skills" / "tool" / "cli" / "tool" / "modules" / "prompt" / "prompts"
    (prompts / "act" / "references").mkdir(parents=True)
    (prompts / "act" / "references" / "stale.md").write_text("old")
    (prompts / "act" / "reference-manifest.json").write_text(json.dumps({
        "version": 1, "source_root": "content",
        "destination": "skills/tool/cli/tool/modules/prompt/prompts/act/references",
        "files": [{"src": "one.md", "dst": "one.md", "type": "file"}]}))
    assert main([str(repo), "--prompts", "tool", "absent"]) == 0
    assert [p.name for p in (prompts / "act" / "references").iterdir()] == ["one.md"]
    assert "materialized 1 prompt-module manifest(s)" in capsys.readouterr().out
