"""Every cookr command that names an artifact gives the same result from any
working directory: the artifact given absolute, relative to the working
directory, relative to the repo (`cookbook/...`) or to the cookbook
(`guidelines/...`) with `-p <repo>`, as when run from the repo root."""

from __future__ import annotations

import json
import os
import shutil
import subprocess

import pytest

from cookr.cli import main
from cookr.core.artifact import load_folder

from ..conftest import FIXTURES
from .test_fold import _copy, _topic
from .test_research import TOPIC, roled, write_research

pytestmark = pytest.mark.usefixtures("git_tmp_path", "patch_refs")

COPY = "guidelines/planning/data/t"         # test_fold's copy
INTO = "guidelines/implementing/data/t"     # test_fold's topic
DOC = "yagni.md"                            # an unconverted doc, for `convert`

#: How the artifact is named, and from where. `root` is the reference: run from
#: the repo root with a repo-relative path, as the skill's own examples do.
SPELLINGS = ("root", "absolute", "cwd-relative", "repo-relative", "cookbook-relative")


def _build(base, monkeypatch):
    """A committed repo at <base>/repo (a researched roled topic, a topic and its
    copy to fold, an unconverted doc), and an unrelated <base>/elsewhere."""
    repo = base / "repo"
    repo.mkdir(parents=True)
    _, folder = roled(repo, monkeypatch, cite="")
    write_research(folder)
    cb = repo / "cookbook"
    _topic(cb), _copy(cb)
    shutil.copy(FIXTURES / "artifacts" / "docs" / DOC, cb / DOC)
    root = subprocess.run(["git", "-C", str(repo), "rev-parse", "--show-toplevel"],
                          check=True, capture_output=True, text=True).stdout.strip()
    subprocess.run(["git", "-C", root, "add", "-A"], check=True, capture_output=True)
    subprocess.run(["git", "-C", root, "-c", "user.name=T", "-c", "user.email=t@t",
                    "commit", "-qm", "base"], check=True, capture_output=True)
    (base / "elsewhere").mkdir()
    return repo


def _named(spelling, base, repo, monkeypatch):
    """(how to spell a cookbook-relative artifact path, the -p args), with the cwd set."""
    elsewhere = base / "elsewhere"
    monkeypatch.chdir(repo if spelling == "root" else elsewhere)
    spell = {
        "root": lambda rel: f"cookbook/{rel}",
        "absolute": lambda rel: str(repo / "cookbook" / rel),
        "cwd-relative": lambda rel: os.path.relpath(repo / "cookbook" / rel, elsewhere),
        "repo-relative": lambda rel: f"cookbook/{rel}",
        "cookbook-relative": lambda rel: rel,
    }[spelling]
    return spell, ["-p", str(repo)]


def _run(argv, capsys, monkeypatch):
    monkeypatch.setenv("COLUMNS", "300")
    capsys.readouterr()
    code = main(argv)
    cap = capsys.readouterr()
    return code, cap.out, cap.err


# One function per command: run it, return what must not depend on the cwd.

def _validate_research(a, p, repo, capsys, mp):
    code, out, _ = _run([*p, "validate", "--research", a(TOPIC)], capsys, mp)
    return code, "Research passed" in out, "no-research" in out


def _roles_check(a, p, repo, capsys, mp):
    code, out, _ = _run([*p, "roles", "check", a(TOPIC)], capsys, mp)
    data = json.loads(out) if code in (0, 1) and out.startswith("{") else None
    return code, data and (data["ok"], data["findings"], data["skills"])


def _roles_set(a, p, repo, capsys, mp):
    code, out, _ = _run([*p, "roles", "set", a(TOPIC), "--part", "what-a-reviewer-looks-for=none"],
                        capsys, mp)
    roles = {pt.name: pt.role for pt in load_folder(repo / "cookbook" / TOPIC).parts}
    return code, roles


def _roles_lossless(a, p, repo, capsys, mp):
    code, out, _ = _run([*p, "roles", "lossless", a(TOPIC), "--base", "HEAD"], capsys, mp)
    data = json.loads(out) if out.startswith("{") else None
    return code, data and (data["missing"], data["counts"])


def _roles_lossless_copy(a, p, repo, capsys, mp):
    # The copy is folded away: its path is named as it was at --base.
    assert main(["fold", str(repo / "cookbook" / COPY), "--into", str(repo / "cookbook" / INTO),
                 "--author", "T", "--date", "2026-11-16"]) == 0
    code, out, _ = _run([*p, "roles", "lossless", a(INTO), "--base", "HEAD", "--copy", a(COPY)],
                        capsys, mp)
    data = json.loads(out) if out.startswith("{") else None
    return code, data and (data["copies"] and len(data["copies"]), data["missing"], data["counts"])


def _roles_pin_for(a, p, repo, capsys, mp):
    folder = repo / "cookbook" / TOPIC
    (folder / "lossless.json").write_text(json.dumps({"base": "HEAD", "moved": [
        {"sentence": "Index every key.", "to": "must-index-keys"}]}), encoding="utf-8")
    code, out, _ = _run([*p, "roles", "lossless", "--pin-for", a(TOPIC), "--entry", "1"], capsys, mp)
    data = json.loads(out) if out.startswith("{") else None
    return code, data and {k: v for k, v in data.items() if k != "folder"}


def _roles_gaps(a, p, repo, capsys, mp):
    ref = repo.parent / "reference.txt"
    ref.write_text("Index every key.\nCascade deletes are declared explicitly on every relationship.\n",
                   encoding="utf-8")
    code, out, _ = _run([*p, "roles", "gaps", a(TOPIC), "--against", str(ref), "--json"], capsys, mp)
    data = json.loads(out) if out.startswith("{") else None
    return code, data and [(r["sentences"], r["held"], r["lacking"]) for r in data["references"]]


def _bump(a, p, repo, capsys, mp):
    code, _, _ = _run([*p, "bump", a(INTO), "--summary", "s", "--author", "T", "--date", "2026-11-16"],
                      capsys, mp)
    return code, load_folder(repo / "cookbook" / INTO).meta.get("version")


def _convert(a, p, repo, capsys, mp):
    code, out, _ = _run([*p, "convert", "--json", a(DOC)], capsys, mp)
    return code, (repo / "cookbook" / "yagni" / "artifact.json").is_file()


def _compile(a, p, repo, capsys, mp):
    code, _, _ = _run([*p, "compile", a(TOPIC)], capsys, mp)
    return code, (repo / "cookbook" / f"{TOPIC}.md").is_file()


def _fold(a, p, repo, capsys, mp):
    code, out, _ = _run([*p, "fold", a(COPY), "--into", a(INTO), "--author", "T", "--date", "2026-11-16"],
                        capsys, mp)
    return code, (repo / "cookbook" / COPY).exists(), out.startswith("{") and json.loads(out)["identical"]


def _payload(a, p, repo, capsys, mp):
    code, out, _ = _run([*p, "payload", "--target", "codex", "--json", a(TOPIC)], capsys, mp)
    data = json.loads(out) if out.startswith("{") else None
    return code, data and json.dumps(data, sort_keys=True).replace(str(repo), "<repo>")


def _install(a, p, repo, capsys, mp):
    # --check writes nothing, and exits 1 for a skill not installed yet (the answer
    # expected here, so read as success); HOME and COOKR_HOME are the test's own.
    mp.setenv("HOME", str(repo.parent / "home"))
    mp.setenv("COOKR_HOME", str(repo.parent / "cookr-home"))
    code, out, _ = _run([*p, "install", "--check", "--json", "--target", "claude", a(TOPIC)], capsys, mp)
    data = json.loads(out) if out.startswith("{") else None
    return (0 if code == 1 else code), data and sorted((i["state"], i.get("name")) for i in data["items"])


COMMANDS = {f.__name__.lstrip("_"): f for f in (
    _validate_research, _roles_check, _roles_set, _roles_lossless, _roles_lossless_copy,
    _roles_pin_for, _roles_gaps,
    _bump, _convert, _compile, _fold, _payload, _install)}


@pytest.mark.parametrize("command", sorted(COMMANDS))
def test_a_command_gives_the_same_result_from_any_directory(command, tmp_path, monkeypatch, capsys):
    results = {}
    for spelling in SPELLINGS:
        base = tmp_path / spelling
        repo = _build(base, monkeypatch)
        a, p = _named(spelling, base, repo, monkeypatch)
        results[spelling] = COMMANDS[command](a, p, repo, capsys, monkeypatch)
    expected = results["root"]
    assert expected[0] == 0, f"{command} fails even from the repo root: {expected}"
    assert {s: r for s, r in results.items() if r != expected} == {}


def test_validate_research_needs_no_p_for_an_absolute_artifact(tmp_path, monkeypatch, capsys):
    # The cookbook is found from the artifact itself, not from the cwd.
    repo = _build(tmp_path, monkeypatch)
    monkeypatch.chdir(tmp_path / "elsewhere")
    code, out, _ = _run(["validate", "--research", str(repo / "cookbook" / TOPIC)], capsys, monkeypatch)
    assert code == 0 and "Research passed" in out
