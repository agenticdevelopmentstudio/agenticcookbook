
# DRY

Every piece of knowledge — a business rule, a constant, a data schema, a validation — should have a single, unambiguous, authoritative representation in the system. When that knowledge changes, one place updates. DRY is a rule about knowledge, not about code shape: two fragments that look alike but encode different rules are not duplicates, and deduplicating them creates coupling where none existed.

- Ask "does this code encode the same knowledge?" before deduplicating — if two fragments will evolve for different reasons, leave them alone
- When the same fact appears across layers (model, validation, UI copy, tests), consolidate to one source and derive the rest
- Prefer code generation, configuration, or derivation over hand-synchronized copies of the same fact
- If you are unsure whether two fragments represent the same knowledge, duplicate — a coincidental twin is cheaper to split later than a wrong abstraction is to unwind

