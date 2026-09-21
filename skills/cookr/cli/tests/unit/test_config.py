"""`.cookr.json` loading and validation."""

from __future__ import annotations

import json

import pytest

from cookr.core.config import ConfigError, load_config


def _write(tmp_path, data):
    p = tmp_path / ".cookr.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


def test_loads_minimal_config(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "recipes").mkdir()
    cfg = load_config(_write(tmp_path, {
        "recipes": "recipes",
        "roots": [{"path": "src", "tier": "ui", "platform": "web"}],
    }))
    assert cfg.repo_root == tmp_path
    assert cfg.recipes_dir == tmp_path / "recipes"
    assert cfg.roots[0].tier == "ui"
    assert cfg.ignore == []
    assert cfg.aliases == {}


def test_tiers_are_ordered_and_deduplicated(tmp_path):
    for d in ("src", "blocks", "apple", "recipes"):
        (tmp_path / d).mkdir()
    cfg = load_config(_write(tmp_path, {
        "recipes": "recipes",
        "roots": [
            {"path": "src", "tier": "ui", "platform": "web"},
            {"path": "blocks", "tier": "blocks", "platform": "web"},
            {"path": "apple", "tier": "ui", "platform": "apple"},
        ],
    }))
    assert cfg.tiers == ["ui", "blocks"]


def test_missing_file_raises(tmp_path):
    with pytest.raises(ConfigError):
        load_config(tmp_path / ".cookr.json")


def test_root_path_must_exist(tmp_path):
    (tmp_path / "recipes").mkdir()
    with pytest.raises(ConfigError, match="src"):
        load_config(_write(tmp_path, {
            "recipes": "recipes",
            "roots": [{"path": "src", "tier": "ui", "platform": "web"}],
        }))


def test_platform_must_be_known(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "recipes").mkdir()
    with pytest.raises(ConfigError, match="platform"):
        load_config(_write(tmp_path, {
            "recipes": "recipes",
            "roots": [{"path": "src", "tier": "ui", "platform": "amiga"}],
        }))


def test_roots_required(tmp_path):
    (tmp_path / "recipes").mkdir()
    with pytest.raises(ConfigError, match="roots"):
        load_config(_write(tmp_path, {"recipes": "recipes"}))
