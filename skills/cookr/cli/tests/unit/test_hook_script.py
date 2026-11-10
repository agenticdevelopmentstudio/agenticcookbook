"""The cookr hook script, run as Claude Code runs it: a JSON payload on stdin."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[5]
HOOK = REPO_ROOT / "skills" / "cookr" / "hooks" / "cc-cookr-hook.py"

# A stand-in for cookr: logs its arguments and exits/prints as FAKE_* say.
FAKE = '''\
import os, sys
with open(os.environ["FAKE_LOG"], "a") as f:
    f.write(" ".join(sys.argv[1:]) + "\\n")
sys.stderr.write(os.environ.get("FAKE_STDERR", ""))
sys.stdout.write(os.environ.get("FAKE_STDOUT", ""))
sys.exit(int(os.environ.get("FAKE_EXIT", "0")))
'''


@pytest.fixture
def env(tmp_path):
    fake = tmp_path / "fake_cookr.py"
    fake.write_text(FAKE)
    e = dict(os.environ)
    e.update(
        COOKR_BIN=f"{sys.executable} {fake}",
        COOKR_HOME=str(tmp_path / "home"),
        FAKE_LOG=str(tmp_path / "calls.log"),
    )
    for k in ("FAKE_EXIT", "FAKE_STDERR", "FAKE_STDOUT"):
        e.pop(k, None)
    return e


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    (r / "sub").mkdir(parents=True)
    (r / ".cookr.json").write_text("{}")
    return r


def run_hook(payload, env, **extra):
    e = {**env, **extra}
    return subprocess.run(
        [sys.executable, str(HOOK)], input=json.dumps(payload), capture_output=True, text=True, env=e
    )


def calls(env):
    log = Path(env["FAKE_LOG"])
    return log.read_text().splitlines() if log.exists() else []


def bash(cmd, cwd, **more):
    return {"hook_event_name": "PreToolUse", "tool_name": "Bash", "tool_input": {"command": cmd},
            "cwd": str(cwd), **more}


def advice(r) -> str:
    """The advisory context a commit check handed the agent ("" when none)."""
    if not r.stdout.strip():
        return ""
    out = json.loads(r.stdout)["hookSpecificOutput"]
    assert out["hookEventName"] == "PreToolUse"
    return out["additionalContext"]


def test_non_cookr_repo_exits_0(tmp_path, env):
    plain = tmp_path / "plain"
    plain.mkdir()
    for payload in (bash("git commit -m x", plain),
                    {"hook_event_name": "SessionStart", "session_id": "s", "cwd": str(plain)}):
        r = run_hook(payload, env, FAKE_EXIT="2")
        assert r.returncode == 0 and r.stdout == ""
    assert calls(env) == []


def test_non_commit_bash_exits_0(repo, env):
    r = run_hook(bash("git status && ls", repo), env, FAKE_EXIT="2")
    assert r.returncode == 0
    assert calls(env) == []
    assert run_hook({"hook_event_name": "PreToolUse", "tool_name": "Edit", "cwd": str(repo)}, env).returncode == 0


def test_commit_with_findings_advises_and_never_blocks(repo, env):
    r = run_hook(bash("git commit -m x", repo / "sub"), env, FAKE_EXIT="2", FAKE_STDERR="update X\n")
    assert r.returncode == 0
    ctx = advice(r)
    assert "not blocked" in ctx and "update X" in ctx
    assert calls(env) == [f"check --staged --hook -p {repo.resolve()}"]


def test_a_clean_commit_says_nothing(repo, env):
    r = run_hook(bash("git commit -m x", repo), env)
    assert r.returncode == 0 and r.stdout == "" and r.stderr == ""


@pytest.mark.parametrize("code", ["1", "2", "3"])
def test_no_exit_code_from_cookr_blocks(repo, env, code):
    r = run_hook(bash("git commit -m x", repo), env, FAKE_EXIT=code, FAKE_STDERR="why\n")
    assert r.returncode == 0 and "why" in advice(r)


def test_stdout_is_the_advice_when_stderr_is_empty(repo, env):
    r = run_hook(bash("git commit -m x", repo), env, FAKE_EXIT="2", FAKE_STDOUT="bad roots\n")
    assert r.returncode == 0 and "bad roots" in advice(r)
    r = run_hook(bash("git commit -m x", repo), env, FAKE_EXIT="2")
    assert r.returncode == 0 and r.stdout == ""


def test_commit_in_other_dir_via_dash_C(tmp_path, repo, env):
    r = run_hook(bash(f"git -C {repo} commit -m x", tmp_path), env, FAKE_EXIT="2", FAKE_STDERR="e\n")
    assert r.returncode == 0 and "e" in advice(r)
    assert calls(env) == [f"check --staged --hook -p {repo.resolve()}"]


@pytest.mark.parametrize("cmd", [
    "cd {repo} && git commit -m x",                 # absolute
    "cd repo && git commit -m x",                   # relative to the session's cwd
    "cd repo ; git add a && git commit -m x",
    "cd repo; git commit -m x",                     # `;` glued to the dir
    "cd {tmp} && cd repo/sub && git commit -m x",   # each cd from the one before
    "cd {tmp} && git -C repo commit -m x",          # -C relative to the cd
])
def test_commit_in_other_dir_via_cd(tmp_path, repo, env, cmd):
    r = run_hook(bash(cmd.format(repo=repo, tmp=tmp_path), tmp_path), env,
                 FAKE_EXIT="2", FAKE_STDERR="e\n")
    assert r.returncode == 0
    assert calls(env) == [f"check --staged --hook -p {repo.resolve()}"]


def test_a_cd_out_of_the_repo_is_not_checked(tmp_path, repo, env):
    plain = tmp_path / "plain"
    plain.mkdir()
    r = run_hook(bash(f"cd {plain} && git commit -m x", repo), env, FAKE_EXIT="2")
    assert r.returncode == 0 and calls(env) == []


def test_override_env_in_command_quiets_the_advice(repo, env):
    r = run_hook(bash("CC_ALLOW_COOKR=1 git commit -m x", repo), env, FAKE_EXIT="2")
    assert r.returncode == 0 and calls(env) == []
    # Mentioning the override in a message is not setting it.
    r = run_hook(bash("git commit -m 'CC_ALLOW_COOKR=1'", repo), env, FAKE_EXIT="2", FAKE_STDERR="e\n")
    assert r.returncode == 0 and len(calls(env)) == 1


def test_stop_is_not_handled(repo, env):
    r = run_hook({"hook_event_name": "Stop", "cwd": str(repo)}, env, FAKE_EXIT="2", FAKE_STDERR="bump X\n")
    assert r.returncode == 0 and r.stdout == "" and r.stderr == ""
    assert calls(env) == []


def test_session_reminder_once_and_runs_no_cookr(repo, env):
    payload = {"hook_event_name": "SessionStart", "session_id": "abc", "cwd": str(repo)}
    first = run_hook(payload, env)
    assert first.returncode == 0
    out = json.loads(first.stdout)["hookSpecificOutput"]
    assert out["hookEventName"] == "SessionStart"
    ctx = out["additionalContext"]
    assert "cookr scope" in ctx and "cookr skill" in ctx and "not a gate" in ctx
    assert calls(env) == []  # no `skills sync`, nothing that writes
    assert (Path(env["COOKR_HOME"]) / "sessions" / "abc").exists()

    again = run_hook({**payload, "hook_event_name": "UserPromptSubmit"}, env)
    assert again.returncode == 0 and again.stdout == ""


def test_reminder_names_the_upgrade_only_for_a_format_1_repo(repo, env):
    payload = {"hook_event_name": "UserPromptSubmit", "session_id": "f1", "cwd": str(repo)}
    ctx = json.loads(run_hook(payload, env).stdout)["hookSpecificOutput"]["additionalContext"]
    assert "format 1" in ctx and "cookr upgrade" in ctx and "Nothing converts it automatically" in ctx
    (repo / ".cookr.json").write_text(json.dumps({"format": 2}))
    payload["session_id"] = "f2"
    ctx = json.loads(run_hook(payload, env).stdout)["hookSpecificOutput"]["additionalContext"]
    assert "format 1" not in ctx


def test_marker_written_only_after_reminder_printed(repo, env):
    payload = {"hook_event_name": "SessionStart", "session_id": "m", "cwd": str(repo)}
    marker = Path(env["COOKR_HOME"]) / "sessions" / "m"
    # stdout is a pipe with no reader: the reminder cannot be delivered, so no
    # marker may be left behind (and the hook still exits 0).
    rd, wr = os.pipe()
    os.close(rd)
    try:
        r = subprocess.run([sys.executable, str(HOOK)], input=json.dumps(payload), text=True,
                           stdout=wr, stderr=subprocess.PIPE, env=env)
    finally:
        os.close(wr)
    assert r.returncode == 0
    assert not marker.exists()
    assert "additionalContext" in run_hook(payload, env).stdout
    assert marker.exists()


def test_missing_cookr_and_bad_input_exit_0(repo, env, tmp_path):
    assert run_hook(bash("git commit -m x", repo), env, COOKR_BIN=str(tmp_path / "nope")).returncode == 0
    r = subprocess.run([sys.executable, str(HOOK)], input="not json", capture_output=True, text=True, env=env)
    assert r.returncode == 0
    r = subprocess.run([sys.executable, str(HOOK)], input="[]", capture_output=True, text=True, env=env)
    assert r.returncode == 0
