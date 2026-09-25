from __future__ import annotations

import shutil

import pytest
from cookbook.core.errors import CookbookError

from cookr.core.recipes import load_corpus


def test_corpus_keys_are_file_stems(mini_repo):
    corpus = load_corpus(mini_repo / "recipes")
    assert set(corpus) == {"button", "stat-card", "chat-composer", "site-menu"}


def test_corpus_reads_type_and_status(mini_repo):
    corpus = load_corpus(mini_repo / "recipes")
    assert corpus["button"].type == "ingredient"
    assert corpus["button"].status == "accepted"
    assert corpus["site-menu"].type == "recipe"


def test_corpus_carries_the_parsed_frontmatter(mini_repo):
    # completeness grades `platforms`/`modified` from info.data instead of re-parsing the file
    info = load_corpus(mini_repo / "recipes")["button"]
    assert info.data["type"] == "ingredient"
    assert info.data["status"] == "accepted"


def test_duplicate_slug_in_a_subdirectory_raises(mini_repo):
    sub = mini_repo / "recipes" / "sub"
    sub.mkdir()
    shutil.copy2(mini_repo / "recipes" / "button.md", sub / "button.md")
    with pytest.raises(CookbookError, match="duplicate recipe slug `button`"):
        load_corpus(mini_repo / "recipes")


def test_corpus_skips_index_and_template(mini_repo):
    (mini_repo / "recipes" / "INDEX.md").write_text("# index\n", encoding="utf-8")
    (mini_repo / "recipes" / "_template.md").write_text("---\ntype: ingredient\n---\n", encoding="utf-8")
    assert "INDEX" not in load_corpus(mini_repo / "recipes")
    assert "_template" not in load_corpus(mini_repo / "recipes")


def test_invalid_yaml_frontmatter_is_a_cookbook_error_naming_the_file(mini_repo):
    (mini_repo / "recipes" / "extra.md").write_text("---\ntitle: a: b\n---\n# x\n", encoding="utf-8")
    with pytest.raises(CookbookError, match="extra.md"):
        load_corpus(mini_repo / "recipes")


def test_non_utf8_recipe_is_a_cookbook_error_naming_the_file(mini_repo):
    (mini_repo / "recipes" / "latin.md").write_bytes(b"---\ntitle: caf\xe9\n---\n")
    with pytest.raises(CookbookError, match="latin.md"):
        load_corpus(mini_repo / "recipes")
