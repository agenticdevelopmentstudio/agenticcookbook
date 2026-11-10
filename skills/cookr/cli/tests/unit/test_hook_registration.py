"""The settings.json registration the cookr installer performs, on a tmp file."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[5]
_spec = importlib.util.spec_from_file_location(
    "hook_registration", REPO_ROOT / "skills" / "cookr" / "setup" / "hook_registration.py")
reg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(reg)

CMD = reg.hook_command(Path("/home/u"))
OTHER = {"type": "command", "command": "/usr/bin/python3 /x/other-hook.py"}


def read(p):
    return json.loads(p.read_text())


def test_command_uses_absolute_home():
    assert CMD == "/usr/bin/python3 /home/u/.claude/skills/cookr/hooks/cc-cookr-hook.py"


def test_register_creates_the_three_reminder_events(tmp_path):
    p = tmp_path / "settings.json"
    assert sorted(reg.register(p, CMD)) == ["PreToolUse", "SessionStart", "UserPromptSubmit"]
    hooks = read(p)["hooks"]
    assert hooks["PreToolUse"] == [{"matcher": "Bash", "hooks": [{"type": "command", "command": CMD}]}]
    for ev in ("SessionStart", "UserPromptSubmit"):
        assert hooks[ev] == [{"hooks": [{"type": "command", "command": CMD}]}]
    assert "Stop" not in hooks


def test_register_drops_an_older_installs_stop_entry(tmp_path):
    p = tmp_path / "settings.json"
    p.write_text(json.dumps({"hooks": {"Stop": [
        {"hooks": [{"type": "command", "command": CMD}]}, {"hooks": [OTHER]}]}}))
    assert "Stop" in reg.register(p, CMD)
    assert read(p)["hooks"]["Stop"] == [{"hooks": [OTHER]}]


def test_register_is_idempotent(tmp_path):
    p = tmp_path / "settings.json"
    reg.register(p, CMD)
    before = p.read_text()
    assert reg.register(p, CMD) == []
    assert p.read_text() == before


def test_register_keeps_other_settings_and_hooks(tmp_path):
    p = tmp_path / "settings.json"
    p.write_text(json.dumps({"model": "x", "hooks": {"Stop": [{"hooks": [OTHER]}]}}))
    reg.register(p, CMD)
    data = read(p)
    assert data["model"] == "x"
    assert data["hooks"]["Stop"] == [{"hooks": [OTHER]}]


def test_unregister_removes_only_ours(tmp_path):
    p = tmp_path / "settings.json"
    p.write_text(json.dumps({"hooks": {
        "Stop": [{"hooks": [OTHER]}],
        "PreToolUse": [{"matcher": "Bash", "hooks": [OTHER]}],
    }}))
    reg.register(p, CMD)
    assert sorted(reg.unregister(p)) == ["PreToolUse", "SessionStart", "UserPromptSubmit"]
    assert read(p) == {"hooks": {"Stop": [{"hooks": [OTHER]}],
                                 "PreToolUse": [{"matcher": "Bash", "hooks": [OTHER]}]}}
    assert reg.unregister(p) == []


def test_unregister_shared_group_keeps_sibling_hook(tmp_path):
    p = tmp_path / "settings.json"
    p.write_text(json.dumps({"hooks": {"Stop": [{"hooks": [OTHER, {"type": "command", "command": CMD}]}]}}))
    reg.unregister(p)
    assert read(p) == {"hooks": {"Stop": [{"hooks": [OTHER]}]}}


def test_unregister_drops_empty_hooks_key_and_tolerates_missing_file(tmp_path):
    p = tmp_path / "settings.json"
    assert reg.unregister(p) == []
    assert not p.exists()
    p.write_text(json.dumps({"model": "x"}))
    reg.register(p, CMD)
    reg.unregister(p)
    assert read(p) == {"model": "x"}


def test_malformed_json_raises_and_leaves_file_unchanged(tmp_path):
    p = tmp_path / "settings.json"
    p.write_bytes(b'{"hooks": {')
    for fn in (lambda: reg.register(p, CMD), lambda: reg.unregister(p)):
        with pytest.raises(ValueError):
            fn()
        assert p.read_bytes() == b'{"hooks": {'


def test_wrong_shapes_raise_and_leave_file_unchanged(tmp_path):
    bad = [
        {"hooks": []},
        {"hooks": {"Stop": {}}},
        {"hooks": {"Stop": ["x"]}},
        {"hooks": {"Stop": [{"hooks": {}}]}},
        {"hooks": {"Stop": [{"matcher": "Bash"}]}},
        [],
    ]
    for content in bad:
        p = tmp_path / "settings.json"
        p.write_text(json.dumps(content))
        before = p.read_bytes()
        for fn in (lambda: reg.register(p, CMD), lambda: reg.unregister(p)):
            with pytest.raises(ValueError):
                fn()
            assert p.read_bytes() == before
