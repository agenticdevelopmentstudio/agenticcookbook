
- Validate at construction and reject invalid input there (parse, don't validate) — a constructed instance MUST be known-valid.
- Make it immutable with value equality (two value objects with the same contents are equal).
- Keep it small and focused on the single concept it represents.

