
**Decision**: Report file as primary output, not PR comment.
**Rationale**: The report is useful as a standalone artifact that can be committed alongside optimized rules. Not all optimization runs happen in a PR context (e.g., local development, initial setup). A future extension can post the report as a PR comment when the pipeline runs in CI.
**Approved**: pending

**Decision**: Reuse lint-rule O-series checks rather than defining new validation logic.
**Rationale**: The O-series checks already encode optimization criteria from the rule-optimization research. Reusing them avoids duplication and ensures the pipeline and linter stay in sync.
**Approved**: pending

**Decision**: Enumeration-based behavioral validation.
**Rationale**: Each original MUST/MUST NOT/SHOULD constraint gets mapped to its optimized equivalent. If a constraint cannot be mapped, validation fails with a specific gap identified. This is more reliable than abstract semantic comparison.
**Approved**: pending

