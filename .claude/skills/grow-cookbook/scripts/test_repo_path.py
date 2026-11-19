"""repo_path.py: how every script that reads the cookbook finds --repo (G76, 1.4.25)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import repo_path  # noqa: E402


def test_a_given_repo_must_hold_cookbook_guidelines(tmp_path):
    (tmp_path / "r" / "cookbook" / "guidelines").mkdir(parents=True)
    assert repo_path.cookbook_repo(str(tmp_path / "r"), "x.py") == (tmp_path / "r").resolve()
    with pytest.raises(SystemExit) as e:
        repo_path.cookbook_repo(str(tmp_path / "nowhere"), "x.py")
    assert "x.py" in str(e.value) and "nowhere" in str(e.value) and "cookbook/guidelines" in str(e.value)


def test_without_one_the_nearest_cookbook_at_or_above_the_directory_is_used(tmp_path, monkeypatch):
    (tmp_path / "r" / "cookbook" / "guidelines").mkdir(parents=True)
    (tmp_path / "r" / "deep" / "er").mkdir(parents=True)
    monkeypatch.chdir(tmp_path / "r" / "deep" / "er")
    assert repo_path.cookbook_repo(None, "x.py") == (tmp_path / "r").resolve()
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit) as e:          # a workspace outside the repo: never a silent "."
        repo_path.cookbook_repo(None, "x.py")
    assert "--repo" in str(e.value)


@pytest.mark.parametrize("script", ["stage_status", "unmeasured", "copy_check", "mark", "quote_building"])
def test_each_area_script_takes_area_and_calls_the_positional_deprecated(script, capsys):
    # G169 (N20, 1.4.37): every script naming an area takes `--area AREA`, and
    # its help calls the positional form deprecated.
    import importlib
    mod = importlib.import_module(script)
    with pytest.raises(SystemExit):
        mod.main(["--help"])
    text = " ".join(capsys.readouterr().out.split())
    assert "[--area AREA]" in text and "deprecated" in text, text


# --- gapfix11 (1.4.39) ---------------------------------------------------------------------------


def test_check_area_names_an_unknown_area_and_a_workspace_without_areas(tmp_path):
    # G198 (L13)
    (tmp_path / "ws" / "areas" / "implementing" / "x").mkdir(parents=True)
    (tmp_path / "r" / "cookbook" / "guidelines" / "shipping").mkdir(parents=True)
    ws, r = tmp_path / "ws", tmp_path / "r"
    assert repo_path.check_area("x.py", ws, "implementing/x") is None
    assert repo_path.check_area("x.py", ws, "shipping", r) is None
    assert "no areas/" in repo_path.check_area("x.py", tmp_path, "implementing/x")
    for bad in ("nope", "implementing/x --workspace y", "../x", "/abs"):
        assert "unknown area" in repo_path.check_area("x.py", ws, bad, r), bad
    (ws / "areas" / "implementing" / "x y").mkdir()      # a folder, but whitespace is never an area
    assert "unknown area" in repo_path.check_area("x.py", ws, "implementing/x y", r)


def _area_ws(tmp: Path) -> tuple[Path, Path]:
    ws, r = tmp / "ws", tmp / "r"
    (ws / "areas" / "implementing" / "x").mkdir(parents=True)
    (r / "cookbook" / "guidelines" / "implementing" / "x").mkdir(parents=True)
    (r / "skills" / "cookr").mkdir(parents=True)
    (r / "skills" / "cookr" / "SKILL.md").write_text("x")
    (ws / "worklist.json").write_text('{"batches": []}')
    return ws, r


@pytest.mark.parametrize("script,extra", [
    ("stage_status", []), ("unmeasured", []), ("copy_check", []), ("plan_skeleton", []),
    ("mark", ["--held", "a:1@t", "held"]), ("run_gaps", []),
    ("quote_building", ["--speciality", "building/s", "--file", "f.txt"])])
def test_every_area_script_refuses_an_unknown_area_and_a_workspace_without_areas(tmp_path, capsys, script, extra):
    # G198 (L13): exit 2 naming it, in every script taking --area or --workspace.
    import importlib
    mod = importlib.import_module(script)
    ws, r = _area_ws(tmp_path)
    for area, w in (("no/such", ws), ("implementing/x --workspace y", ws), ("implementing/x", tmp_path)):
        capsys.readouterr()
        try:
            code = mod.main(["--area", area, "--workspace", str(w), "--repo", str(r), *extra])
        except SystemExit as e:
            code = e.code
        err = capsys.readouterr().err
        assert code == 2 and ("unknown area" in err or "no areas/" in err), (script, area, err)


def test_a_one_string_argument_list_gets_the_zsh_hint_and_a_separate_one_does_not(tmp_path, monkeypatch):
    # G240 (L18, 1.4.40): `$ARGS` unsplit by zsh reaches a script as one argument holding ` --`; the no-cookbook
    # message then says so.
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["x.py", "--area a --workspace w --repo r"])
    with pytest.raises(SystemExit) as e:
        repo_path.cookbook_repo(None, "x.py")
    assert "zsh passes them as one word: write each flag out" in str(e.value)
    monkeypatch.setattr(sys, "argv", ["x.py", "--area", "a"])
    with pytest.raises(SystemExit) as e:
        repo_path.cookbook_repo(None, "x.py")
    assert "zsh" not in str(e.value)


def test_the_re_run_checklist_commands_carry_area_workspace_and_repo():
    # G240 (L18, 1.4.40): every backticked command of the re-run checklist that runs one of the five scripts is
    # written whole, so copying it never ends in a failed call.
    import re
    doc = (Path(__file__).resolve().parent.parent / "references" / "stage-1.md").read_text(encoding="utf-8")
    checklist = doc.split("## Re-run checklist", 1)[1].split("\n## ", 1)[0]
    cmds = [c for c in re.findall(r"`([^`]+)`", checklist)
            if re.match(r"(?:scripts/)?(copy_check|unmeasured|plan_skeleton|run_gaps|stage_status)\.py\b", c) and " --" in c]
    assert cmds, "no checklist command found"
    for c in cmds:
        for flag in ("--area", "--workspace", "--repo"):
            assert flag in c, f"{c!r} lacks {flag}"


# gapfix13 (1.4.42): G263, G271

def test_an_argparse_exit_2_from_one_argument_holding_spaces_names_the_cause(capsys, monkeypatch):
    import argparse

    def main(argv=None):
        ap = argparse.ArgumentParser()
        ap.add_argument("--area")
        ap.parse_args(argv)
        return 0
    monkeypatch.setattr(sys, "argv", ["x.py", "--area implementing/sec --workspace W"])
    with pytest.raises(SystemExit) as e:
        repo_path.run_main(main)
    assert e.value.code == 2
    err = capsys.readouterr().err
    assert "one word" in err and "write each flag out" in err


def test_a_refusal_that_is_no_argparse_error_prints_no_hint(capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["x.py", "--area", "a b"])
    with pytest.raises(SystemExit) as e:
        repo_path.run_main(lambda: 2)
    assert e.value.code == 2 and "one word" not in capsys.readouterr().err


@pytest.mark.parametrize("script", ["apply_second_check.py", "check_cookr_python.py", "copy_check.py", "devteam_checkout.py", "mark.py", "owner_list.py", "paraphrase_hints.py", "plan_skeleton.py", "quote_building.py", "r9_stamp.py", "review_findings.py", "run_gaps.py", "stage_status.py", "team_probe.py", "unmeasured.py", "write_brief.py", "write_on_success.py"])
def test_every_script_exits_cleanly_on_a_closed_pipe(script):
    import subprocess
    p = subprocess.Popen([sys.executable, str(Path(repo_path.__file__).parent / script), "--help"],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.stdout.close()
    err = p.stderr.read().decode()
    p.wait()
    assert "BrokenPipeError" not in err and "Traceback" not in err


def test_a_wrong_python_error_names_the_python_to_use():
    # gapfix13 (G269, 1.4.42): /usr/bin/python3 (3.9) says "Unknown option: -P"; a python without cookr's modules
    # "No module named"; each gets the hint naming $COOKR_PY and check_cookr_python.py.
    for err in ("Unknown option: -P\nusage: python3 [option]", "ModuleNotFoundError: No module named 'yaml'"):
        h = repo_path.python_hint(err, "/usr/bin/python3")
        assert "/usr/bin/python3" in h and "$COOKR_PY" in h and "check_cookr_python.py" in h, h
    assert repo_path.python_hint("cookr: no such folder", "py") == ""


def test_a_missing_module_names_the_python_to_use(capsys):
    def main():
        import no_such_module_gapfix13  # noqa: F401
    with pytest.raises(SystemExit) as e:
        repo_path.run_main(main)
    assert e.value.code == 2
    err = capsys.readouterr().err
    assert "no_such_module_gapfix13" in err and "$COOKR_PY" in err
