"""`render_template`: placeholder substitution for prompt templates."""

from __future__ import annotations

import pytest

from cookr.modules.prompt.render import UnknownPlaceholderError, render_template


def test_render_template_substitutes_known_placeholders():
    body = "Design a {{target}} schema for: {{task}}"
    out = render_template(body, {"target": "postgres", "task": "blog posts"})
    assert out == "Design a postgres schema for: blog posts"


def test_render_template_raises_on_unknown_placeholder():
    with pytest.raises(UnknownPlaceholderError) as exc:
        render_template("hello {{unknown}}", {"task": "x"})
    assert "unknown" in str(exc.value)


def test_render_template_none_value_renders_as_empty():
    """A `None` value (e.g., from `default: null`) renders as empty string, not 'None'."""
    out = render_template("X{{val}}Y", {"val": None})
    assert out == "XY"
