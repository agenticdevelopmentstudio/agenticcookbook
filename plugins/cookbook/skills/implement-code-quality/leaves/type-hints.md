<!-- leaf: implement-code-quality/type-hints · source: guidelines/implementing/code-quality/type-hints.md -->

**Rules** (cite as `implement-code-quality/type-hints#<slug>`):

- `type-hints-used-but-python-compatibility` MUST — Type hints MAY be used but are not required. Python 3.9 compatibility MUST be maintained — use from __future__ import …

# Type hints

Type hints MAY be used but are not required. Python 3.9 compatibility MUST be maintained — use `from __future__ import annotations` or `typing` module forms (e.g., `list[str]` requires 3.9+, `Optional[str]` works everywhere).
