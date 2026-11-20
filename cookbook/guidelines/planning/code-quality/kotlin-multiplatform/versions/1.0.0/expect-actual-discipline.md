
- `expect`/`actual` **SHOULD** be reserved for thin platform shims (e.g., logging sink, secure storage, file paths, UUID/clock). Most common code needs none.
- Every `expect` declaration **MUST** have a matching `actual` in the same package for every target; the compiler enforces this. Prefer interfaces plus dependency injection over `expect`/`actual` when the seam is non-trivial — it is easier to test and delete.
- Use the hierarchical source-set structure (e.g., an intermediate `appleMain` shared by `iosMain`/`macosMain`) so common-but-not-universal code is not duplicated.

