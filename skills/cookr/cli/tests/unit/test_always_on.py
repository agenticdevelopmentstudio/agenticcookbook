"""The always-on principles skill: grouping, gists, concern links, tuning."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from cookr.core import always_on, hosts, tuning
from cookr.core.artifact import find_folders

from .test_skill import make

REPO = Path(__file__).resolve().parents[5]


@pytest.fixture
def book(tmp_path):
    root = tmp_path / "cookbook"
    make(root, "principles/simplicity", "principle", summary="Simple and easy are not synonyms.  "
                                                             "Untangle concerns.")
    make(root, "principles/yagni", "principle", summary="Build for today.")
    make(root, "guidelines/implementing/data/use-wal", "guideline")
    (root / "workflows").mkdir()
    (root / "workflows/pipeline-concerns.json").write_text(json.dumps([
        {"step": 2, "concern": "wal", "apply": "always", "summary": "Use WAL.",
         "guideline_path": "../x/cookbook/guidelines/implementing/data/use-wal.md"},
        {"step": 1, "concern": "ask-first", "apply": "ask", "summary": "Ask.", "guideline_path": "gone.md"},
        {"step": 3, "concern": "wal", "apply": "always", "summary": "Again."},
    ]))
    return root


def build(book, **kw):
    return always_on.principles_skill(find_folders([book]), concerns=book / always_on.CONCERNS, **kw)


def test_the_skill_lists_every_principle_with_its_routed_skill(book):
    s = build(book)
    assert s.name == "general-principles"
    assert "description: \"The 2 engineering principles" in s.text
    assert ("- **simplicity**: Simple and easy are not synonyms. Untangle concerns. "
            "(`principle-simplicity`)") in s.text
    assert "- **yagni**: Build for today. (`principle-yagni`)" in s.text
    assert "{{" not in s.text


def test_concerns_link_the_artifact_they_name_once_each(book):
    text = build(book).text
    assert "- **wal**: Use WAL. (`implementing-data-use-wal`)" in text
    assert "Again." not in text
    assert "- **ask-first**: Ask.\n" in text


def test_a_library_names_the_skill_and_its_links(book):
    s = build(book, library="adtoolkit")
    assert s.name == "adtoolkit-principles"
    assert "(`adtoolkit-principle-simplicity`)" in s.text and 'source: "adtoolkit"' in s.text


def test_no_principles_means_no_skill(tmp_path):
    root = tmp_path / "cookbook"
    make(root, "guidelines/implementing/data/use-wal", "guideline")
    assert always_on.principles_skill(find_folders([root])) is None


def test_every_host_target_loads(book):
    s = build(book)
    for h in hosts.manifest().values():
        assert tuning.load_problems(s.render(h.chain(h.default_model)), h) == []


def test_the_real_cookbook_renders():
    folders = find_folders([REPO / "cookbook"])
    s = always_on.principles_skill(folders, concerns=REPO / "cookbook" / always_on.CONCERNS)
    assert s is not None and "..." not in s.text.split("## Full text")[0]
    assert "(`principle-meta-principle-optimize-for-change`)" in s.text
