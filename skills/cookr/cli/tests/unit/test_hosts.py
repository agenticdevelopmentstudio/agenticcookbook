"""The host manifest and target chains."""

from __future__ import annotations

import json

import pytest

from cookr.core import hosts
from cookr.core.hosts import HostError


def test_the_shipped_manifest_loads_and_declares_claude_and_codex():
    declared = hosts.load()
    assert {"claude", "codex"} <= set(declared)
    for h in declared.values():
        assert h.chain(h.default_model)[-1] in h.targets()


@pytest.mark.parametrize("model,chain", [
    ("claude-opus-5-5", ("claude", "claude.opus", "claude.opus-5-5")),
    ("claude-haiku-4-5-20251001", ("claude", "claude.haiku", "claude.haiku-4-5")),
    ("claude-opus-5-5[1m]", ("claude", "claude.opus", "claude.opus-5-5")),
    ("Claude-Sonnet-5.5", ("claude", "claude.sonnet", "claude.sonnet-5-5")),
    ("claude-mystery-9", ("claude", "claude.mystery-9")),
    (None, ("claude",)),
])
def test_claude_models_resolve_to_a_chain(model, chain):
    assert hosts.chain("claude", model) == chain


def test_codex_family_is_the_longest_matching_prefix():
    assert hosts.chain("codex", "gpt-5-codex") == ("codex", "codex.gpt-5", "codex.gpt-5-codex")
    assert hosts.chain("codex", "gpt-5") == ("codex", "codex.gpt-5")


def test_an_unknown_host_names_the_declared_ones():
    with pytest.raises(HostError, match="unknown host 'gemini'.*claude, codex"):
        hosts.host("gemini")


def test_a_model_that_cannot_name_a_target_is_refused():
    with pytest.raises(HostError, match="not a model ID"):
        hosts.chain("claude", "claude-opus 5")


def test_targets_list_host_then_families_then_models():
    t = hosts.host("claude").targets()
    assert t[0] == "claude"
    assert t.index("claude.opus") < t.index("claude.opus-5-5")


def test_names_are_hosts_and_families():
    assert {"claude", "codex", "opus", "sonnet", "haiku", "gpt-5"} <= set(hosts.names())


def test_a_manifest_of_an_unknown_format_is_refused(tmp_path):
    p = tmp_path / "hosts.json"
    p.write_text(json.dumps({"format": 2, "hosts": {}}))
    with pytest.raises(HostError, match="unsupported format"):
        hosts.load(p)


def test_a_host_missing_a_field_is_refused(tmp_path):
    p = tmp_path / "hosts.json"
    p.write_text(json.dumps({"format": 1, "hosts": {"x": {"skills_dir": "~/x"}}}))
    with pytest.raises(HostError, match="'x'.*missing"):
        hosts.load(p)
