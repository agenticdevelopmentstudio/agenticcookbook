
- A `triggers` value that is not in the canonical table, or a new value used before it was added there.
- A guideline with no triggers and no `[]`, or with more than five triggers.
- Triggers not ordered from most specific to least specific.
- A `triggers` field on an artifact that is not a guideline.
- A hand edit to `cookbook/index/triggers.yaml`, or a trigger change committed without the index regenerated.
- A vocabulary value with no definition, no scope note or no example, two values with one meaning, or overlapping values that do not say which applies.
- A value's description that does not use the words of the tasks it serves.
- A rename that drops the old value, or a retirement that deletes a value its guidelines still carry with no replacement or migration.
- A value with no history note, or a change with no date or no person responsible.
- Tooling that accepts an unlisted trigger value or a frontmatter that does not parse.
- An always-loaded tier that keeps growing with material only some work needs.
- Trigger-filtered loading with no fallback for a task whose triggers miss.
- A selection change made without a labelled task set, without a held-out part, or reported without recall and precision.

