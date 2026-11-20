
- Conflict resolution strategy chosen and documented for each entity type
- LWW implementation uses reliable timestamps (Hybrid Logical Clocks or server-assigned monotonic versions)
- Field-level merge strategy includes base version for three-way comparison when applicable
- Manual resolution queue exists for conflicts that cannot be automatically resolved
- Policy justification documented (why this strategy fits the data semantics)
- `must-have-explicit-conflict-strategy`: A review passes when it establishes every item above.
