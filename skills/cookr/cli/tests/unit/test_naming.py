from __future__ import annotations

import pytest

from cookr.core.naming import kebab


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
