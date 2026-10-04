
Strict application causes wrapper/delegation bloat and fights idiomatic code. A method chain is **acceptable** and **SHOULD NOT** be flagged when:

- **Fluent builders / DSLs**: `builder.with(x).with(y).build()` — each call returns the same builder, not a traversed collaborator.
- **Immutable pipelines**: `items.map(...).filter(...).reduce(...)` and similar LINQ/stream/sequence chains operate on transformed values, not nested object internals.
- **Boundary DTOs / config / response models**: data-holder objects (parsed JSON, protobuf messages, config trees) exist to be read; navigating their fields is their purpose.
- **Standard-library and framework value types**: e.g. dates, paths, URIs.

Because of these cases, this guideline is SHOULD-level. A reviewer **MUST NOT** demand a wrapper method whose only job is to relay one call to a stable data object — that trades real coupling for ceremony.

