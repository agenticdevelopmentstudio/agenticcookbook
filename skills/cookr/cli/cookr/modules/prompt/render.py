"""Substitute `{{name}}` placeholders in a prompt template."""

from __future__ import annotations

import re
from typing import Any

_PLACEHOLDER_RE = re.compile(r"\{\{\s*([\w-]+)\s*\}\}")


class UnknownPlaceholderError(RuntimeError):
    """Raised when a template references a placeholder not in `params`."""


def render_template(body: str, params: dict[str, Any]) -> str:
    """Substitute `{{name}}` placeholders with values from `params`.

    Raises UnknownPlaceholderError if the template references a name not
    present in `params`.
    """

    def sub(match: re.Match[str]) -> str:
        name = match.group(1)
        if name not in params:
            raise UnknownPlaceholderError(name)
        value = params[name]
        return "" if value is None else str(value)

    return _PLACEHOLDER_RE.sub(sub, body)
