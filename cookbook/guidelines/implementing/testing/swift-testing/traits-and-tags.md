
- Attach **traits** for behavior and metadata: `.disabled("reason")`, `.bug("url")`, `.timeLimit(.minutes(1))`, `.enabled(if:)`, and serialization via `.serialized`.
- Define **tags** with `@Tag` and apply them to filter/organize runs (e.g. `.tags(.network)`). You **SHOULD** keep a small, shared tag vocabulary rather than ad-hoc per-file tags.

