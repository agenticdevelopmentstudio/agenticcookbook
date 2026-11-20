
- `may-use-type-hints`: nothing to flag for type hints being present or absent; a review that demands them where they are missing goes past the rule
- `must-keep-python-39-compatibility`: annotation syntax that fails on Python 3.9, such as `X | None` or other newer forms evaluated at runtime without `from __future__ import annotations`
