
# DRY

Every piece of knowledge — a business rule, a constant, a data schema, a validation — should have a single, unambiguous, authoritative representation in the system. When that knowledge changes, one place updates. DRY is a rule about knowledge, not about code shape: two fragments that look alike but encode different rules are not duplicates, and deduplicating them creates coupling where none existed.
