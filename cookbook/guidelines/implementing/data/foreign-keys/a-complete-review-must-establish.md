
- `PRAGMA foreign_keys = ON` mandatory in all connection setup code (test harness, application bootstrap)
- Every foreign key column has a B-tree index (to prevent table-scan when cascading deletes/updates)
- ON DELETE action explicitly chosen and documented (CASCADE for composition, RESTRICT for integrity, SET NULL for optional refs)
- ON UPDATE action explicitly chosen and documented
- Deferred constraints (DEFERRABLE INITIALLY DEFERRED) used only where batch insert order requires temporal FK violations
- No FK constraints declared without corresponding index on the FK column
- Bidirectional references avoided; one direction always defined, back-references via query
- Cross-table constraints use correct syntax: `REFERENCES table(column)` with explicit column name
- Every MUST rule is kept, with no exception: `must-enable-foreign-keys-per-connection`, `must-reference-a-key-or-unique-column`, `must-set-foreign-keys-outside-transactions`, `must-index-every-fk-column`, `must-declare-required-fk-columns-not-null`, `must-keep-set-default-parent-row`, `must-match-composite-fks-exactly`, `must-not-add-fk-column-with-non-null-default`, `must-not-reference-attached-databases`


A review passes when it establishes every item above.
