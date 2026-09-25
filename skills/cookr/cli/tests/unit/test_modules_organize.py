"""`cookr organize plan`/`apply` at the CLI level."""

from __future__ import annotations

import json
import subprocess

from cookr.cli import main


def _git(repo, *args, check=True):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=check)


def _init_git(repo):
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test Author")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "initial")


def test_organize_lists_its_actions_without_one(legacy_repo, capsys):
    assert main(["-p", str(legacy_repo), "organize"]) == 0
    out = capsys.readouterr().out
    assert "plan" in out and "apply" in out


def test_organize_plan_prints_json_to_stdout_by_default(legacy_repo, capsys):
    assert main(["-p", str(legacy_repo), "organize", "plan"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["cookbook"] == "cookbook"
    assert len(data["moves"]) == 4
    assert data["unmatched"] == ["site-menu"]


def test_organize_plan_out_writes_the_plan_and_prints_a_summary(legacy_repo, capsys, tmp_path):
    out_file = tmp_path / "plan.json"
    assert main(["-p", str(legacy_repo), "organize", "plan", "--out", str(out_file)]) == 0
    report = capsys.readouterr().out
    assert "4 move(s) written" in report
    assert "no source files (1)" in report and "site-menu" in report
    data = json.loads(out_file.read_text(encoding="utf-8"))
    assert len(data["moves"]) == 4


def test_organize_plan_without_a_legacy_config_exits_2(mini_repo, capsys):
    # mini_repo is already a library cookbook; there is no .cookr.json to convert.
    assert main(["-p", str(mini_repo), "organize", "plan"]) == 2
    assert "nothing to convert" in capsys.readouterr().out


def test_organize_apply_requires_a_plan_flag(legacy_repo, capsys):
    assert main(["-p", str(legacy_repo), "organize", "apply"]) == 2
    assert "--plan is required" in capsys.readouterr().out


def test_organize_apply_reports_bump_failures_and_exits_1(legacy_repo, capsys, tmp_path):
    _init_git(legacy_repo)
    plan_file = tmp_path / "plan.json"
    assert main(["-p", str(legacy_repo), "organize", "plan", "--out", str(plan_file)]) == 0
    capsys.readouterr()
    rc = main(["-p", str(legacy_repo), "organize", "apply", "--plan", str(plan_file), "--json"])
    data = json.loads(capsys.readouterr().out)
    assert data["moved"] == 4
    assert data["manifest"] == "cookbook/cookbook.json"
    assert data["rewritten"] == ["cookbook/ui.md"]
    assert {f["file"] for f in data["bump_failures"]} == {
        "cookbook/blocks/stat-card.md", "cookbook/components/chat-composer.md"}
    assert rc == 1  # bump failures make it a non-clean exit


def test_organize_apply_text_report_names_leftovers_and_failures(legacy_repo, capsys, tmp_path):
    _init_git(legacy_repo)
    plan_file = tmp_path / "plan.json"
    main(["-p", str(legacy_repo), "organize", "plan", "--out", str(plan_file)])
    capsys.readouterr()
    rc = main(["-p", str(legacy_repo), "organize", "apply", "--plan", str(plan_file)])
    out = capsys.readouterr().out
    assert "moved 4 spec(s); wrote cookbook/cookbook.json" in out
    assert "not bumped: cookbook/blocks/stat-card.md" in out
    assert rc == 1


def test_organize_apply_raises_a_clean_error_on_a_bad_plan(legacy_repo, capsys, tmp_path):
    _init_git(legacy_repo)
    plan_file = tmp_path / "plan.json"
    plan_file.write_text(json.dumps({"version": 99}), encoding="utf-8")
    assert main(["-p", str(legacy_repo), "organize", "apply", "--plan", str(plan_file)]) == 2
    assert "plan version must be 1" in capsys.readouterr().out
