"""`.cookr.json` loading and validation."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

from cookbook.core.errors import CookbookError
from cookbook.core.scheme import SchemeError
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
    assert cfg.renames == {}


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


def test_renames_must_name_an_existing_file(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "recipes").mkdir()
    with pytest.raises(ConfigError, match="renames key not found: src/Card.tsx"):
        load_config(_write(tmp_path, {
            "recipes": "recipes",
            "roots": [{"path": "src", "tier": "ui", "platform": "web"}],
            "renames": {"src/Card.tsx": "landing-card"},
        }))


def test_renames_accepts_a_directory_key(tmp_path):
    (tmp_path / "src" / "hooks").mkdir(parents=True)
    (tmp_path / "recipes").mkdir()
    cfg = load_config(_write(tmp_path, {
        "recipes": "recipes",
        "roots": [{"path": "src", "tier": "ui", "platform": "web"}],
        "renames": {"src/hooks/": "hooks"},
    }))
    assert cfg.renames == {"src/hooks": "hooks"}
    assert cfg.renamed("src/hooks/useThing.ts") == "hooks"
    assert cfg.renamed("src/hooksish/useThing.ts") is None
    assert cfg.renamed("src/Card.tsx") is None


def test_renames_rejects_a_missing_directory_key(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "recipes").mkdir()
    with pytest.raises(ConfigError, match="renames key not found: src/hooks"):
        load_config(_write(tmp_path, {
            "recipes": "recipes",
            "roots": [{"path": "src", "tier": "ui", "platform": "web"}],
            "renames": {"src/hooks": "hooks"},
        }))


def test_renames_rejects_an_empty_name(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "recipes").mkdir()
    (tmp_path / "src" / "Card.tsx").write_text("", encoding="utf-8")
    with pytest.raises(ConfigError, match="`renames` must map source paths to non-empty names"):
        load_config(_write(tmp_path, {
            "recipes": "recipes",
            "roots": [{"path": "src", "tier": "ui", "platform": "web"}],
            "renames": {"src/Card.tsx": ""},
        }))


def test_scheme_is_configurable(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "recipes").mkdir()
    cfg = load_config(_write(tmp_path, {
        "recipes": "recipes",
        "scheme": "toolkit",
        "roots": [{"path": "src", "tier": "ui", "platform": "web"}],
    }))
    assert cfg.domain("button") == "toolkit://recipes/button"


@pytest.mark.parametrize("bad", ["", "a/b", "x://", 3])
def test_scheme_must_be_a_bare_name(tmp_path, bad):
    (tmp_path / "src").mkdir()
    (tmp_path / "recipes").mkdir()
    with pytest.raises(ConfigError, match="`scheme`"):
        load_config(_write(tmp_path, {
            "recipes": "recipes",
            "scheme": bad,
            "roots": [{"path": "src", "tier": "ui", "platform": "web"}],
        }))


def test_root_kind_defaults_to_ui_and_accepts_logic(tmp_path):
    for d in ("src", "lib", "recipes"):
        (tmp_path / d).mkdir()
    cfg = load_config(_write(tmp_path, {
        "recipes": "recipes",
        "roots": [
            {"path": "src", "tier": "ui", "platform": "web"},
            {"path": "lib", "tier": "engine", "platform": "python", "kind": "logic"},
        ],
    }))
    assert [r.kind for r in cfg.roots] == ["ui", "logic"]


def test_root_kind_must_be_known(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "recipes").mkdir()
    with pytest.raises(ConfigError, match="kind"):
        load_config(_write(tmp_path, {
            "recipes": "recipes",
            "roots": [{"path": "src", "tier": "ui", "platform": "web", "kind": "backend"}],
        }))


# --- the default scheme (K10) --------------------------------------------------------

_GIT = ["git", "-c", "user.name=T", "-c", "user.email=t@example.com",
        "-c", "init.defaultBranch=main", "-c", "protocol.file.allow=always"]


def _git(cwd: Path, *args: str) -> None:
    subprocess.run([*_GIT, "-C", str(cwd), *args], check=True, capture_output=True)


def _repo(path: Path, origin: str | None = None) -> Path:
    """A committed repo holding a scheme-less .cookr.json, src/ and recipes/."""
    for d in ("src", "recipes"):
        (path / d).mkdir(parents=True)
        (path / d / ".keep").write_text("", encoding="utf-8")
    _write(path, {"recipes": "recipes",
                  "roots": [{"path": "src", "tier": "ui", "platform": "web"}]})
    _git(path, "init", "-q")
    _git(path, "add", "-A")
    _git(path, "commit", "-q", "-m", "init")
    if origin:
        _git(path, "remote", "add", "origin", origin)
    return path


def test_default_scheme_is_the_repos_directory_without_an_origin(tmp_path):
    repo = _repo(tmp_path / "my-project")
    cfg = load_config(repo / ".cookr.json")
    assert cfg.scheme == "my-project"
    assert cfg.domain("button") == "my-project://recipes/button"


def test_linked_worktree_gets_the_repos_scheme_not_the_worktrees(tmp_path):
    repo = _repo(tmp_path / "my-project")
    wt = repo / ".claude" / "worktrees" / "multiplatform"
    _git(repo, "worktree", "add", "-q", str(wt), "-b", "multiplatform")
    cfg = load_config(wt / ".cookr.json")
    assert cfg.repo_root == wt
    assert cfg.domain("button") == "my-project://recipes/button"


def test_default_scheme_is_the_origins_basename(tmp_path):
    repo = _repo(tmp_path / "checkout-dir", origin="git@github.com:org/real-name.git")
    assert load_config(repo / ".cookr.json").scheme == "real-name"


def test_submodule_checkout_gets_its_own_repos_scheme(tmp_path):
    lib = _repo(tmp_path / "toolkit")
    app = tmp_path / "app"
    app.mkdir()
    _git(app, "init", "-q")
    _git(app, "submodule", "add", "-q", str(lib), "external/toolkit")
    cfg = load_config(app / "external" / "toolkit" / ".cookr.json")
    assert cfg.domain("button") == "toolkit://recipes/button"


def test_explicit_scheme_wins_in_a_worktree(tmp_path):
    repo = _repo(tmp_path / "my-project")
    data = json.loads((repo / ".cookr.json").read_text())
    _write(repo, {**data, "scheme": "toolkit"})
    _git(repo, "commit", "-qam", "scheme")
    wt = tmp_path / "wt"
    _git(repo, "worktree", "add", "-q", str(wt), "-b", "wt")
    assert load_config(wt / ".cookr.json").scheme == "toolkit"


def test_outside_git_loads_but_deriving_the_scheme_fails_clearly(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "recipes").mkdir()
    cfg = load_config(_write(tmp_path, {
        "recipes": "recipes",
        "roots": [{"path": "src", "tier": "ui", "platform": "web"}],
    }))
    assert cfg.tiers == ["ui"]                       # scanning needs no scheme
    with pytest.raises(SchemeError, match="scheme"):
        cfg.domain("button")


def test_config_error_is_a_cookbook_error():
    assert issubclass(ConfigError, CookbookError)


def test_repo_root_is_the_symlinks_directory_not_its_targets(tmp_path):
    real = tmp_path / "elsewhere"
    real.mkdir()
    repo = tmp_path / "repo"
    for d in ("src", "recipes"):
        (repo / d).mkdir(parents=True)
    target = _write(real, {"recipes": "recipes", "scheme": "x",
                           "roots": [{"path": "src", "tier": "ui", "platform": "web"}]})
    os.symlink(target, repo / ".cookr.json")
    cfg = load_config(repo / ".cookr.json")
    assert cfg.repo_root == repo.resolve()
    assert cfg.recipes_dir == repo.resolve() / "recipes"
