"""References dir resolution + prompt template loading."""

from __future__ import annotations

from pathlib import Path

import pytest

from cookr.core import refs


def test_references_dir_resolves_to_sibling_of_pkg():
    """references_dir() is `<package>/../references` regardless of test cwd."""
    rd = refs.references_dir()
    import cookr
    pkg_parent = Path(cookr.__file__).resolve().parent.parent
    assert rd == pkg_parent / "references"


def test_index_configs_dir_under_refs(patch_refs):
    assert refs.index_configs_dir() == patch_refs / "index-configs"


def test_prompts_dir_under_refs(patch_refs):
    assert refs.prompts_dir() == patch_refs / "prompts"


def test_prompt_template_reads_bundled(patch_refs):
    text = refs.prompt_template("lint")
    assert "{{file_path}}" in text or "{{file_contents}}" in text


def test_prompt_template_with_or_without_md_suffix(patch_refs):
    a = refs.prompt_template("lint")
    b = refs.prompt_template("lint.md")
    assert a == b


def test_missing_prompt_raises(patch_refs):
    with pytest.raises(FileNotFoundError):
        refs.prompt_template("does-not-exist")
