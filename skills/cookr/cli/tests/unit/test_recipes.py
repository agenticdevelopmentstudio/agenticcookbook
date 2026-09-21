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
