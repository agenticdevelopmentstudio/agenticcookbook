from __future__ import annotations

import pytest

from cookr.core.naming import kebab, path_name


@pytest.mark.parametrize("stem,expected", [
    ("Button", "button"),
    ("ToolbarButton", "toolbar-button"),
    ("chat-composer", "chat-composer"),
    ("StatCard", "stat-card"),
    ("HTMLView", "html-view"),
    ("SemanticPalette+NSColor", "semantic-palette-ns-color"),
    ("use_editable_list", "use-editable-list"),
])
def test_kebab(stem, expected):
    assert kebab(stem) == expected


@pytest.mark.parametrize("stem,expected", [
    ("macOS", "macos"),
    ("iOS", "ios"),
    ("iPadOS", "ipados"),
    ("tvOS", "tvos"),
    ("watchOS", "watchos"),
    ("visionOS", "visionos"),
    ("CoreMacOS", "core-macos"),
    ("MacOS", "macos"),
    ("Button", "button"),
    ("ToolbarButton", "toolbar-button"),
])
def test_path_name_keeps_platform_words_whole(stem, expected):
    assert path_name(stem) == expected


def test_path_name_matches_kebab_when_no_platform_word_is_present():
    assert path_name("StatCard") == kebab("StatCard")
