
- **should-give-each-piece-of-knowledge-one-representation**: Every piece of knowledge — a business rule, a constant, a data schema, a validation — SHOULD have a single, unambiguous, authoritative representation in the system.
- **should-ask-whether-same-knowledge-before-deduplicating**: SHOULD ask "does this code encode the same knowledge?" before deduplicating — if two fragments will evolve for different reasons, leave them alone.
- **should-consolidate-facts-across-layers**: When the same fact appears across layers (model, validation, UI copy, tests), SHOULD consolidate to one source and derive the rest.
- **should-prefer-derivation-over-synchronized-copies**: SHOULD prefer code generation, configuration, or derivation over hand-synchronized copies of the same fact.
- **should-duplicate-when-unsure**: If you are unsure whether two fragments represent the same knowledge, SHOULD duplicate — a coincidental twin is cheaper to split later than a wrong abstraction is to unwind.
