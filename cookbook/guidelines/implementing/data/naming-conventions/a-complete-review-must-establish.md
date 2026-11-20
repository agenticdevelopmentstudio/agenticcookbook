
- All identifiers use snake_case exclusively (no camelCase, PascalCase, or mixed case)
- No bare `id` columns; all primary keys follow pattern `<table>_id` or semantic name
- Foreign key columns named as `<referenced_table>_id` for clarity
- No SQL reserved words used as unquoted identifiers
- Indexes follow `ix_<table>_<columns>` convention
- Unique constraints follow `uq_<table>_<columns>` convention
- Check constraints follow `ck_<table>_<constraint_name>` convention
- Foreign key constraints follow `fk_<table>_<referenced_table>` convention
- Triggers follow `trg_<table>_<action>_<timing>` convention (e.g., `trg_users_update_before`)
- Every MUST rule is kept, with no exception: `must-use-snake-case-identifiers`, `must-not-mix-table-number-conventions`, `must-name-primary-keys-table-id`, `must-match-foreign-key-to-referenced-column`, `must-prefix-booleans-is-or-has`, `must-name-date-columns-by-event`
- Every SHOULD rule is kept, or the change says why not: `should-use-one-table-number-convention`, `should-prefer-singular-for-compound-names`, `should-prefer-plural-to-avoid-reserved-words`, `should-document-table-number-convention`, `should-qualify-repeated-parent-references`, `should-not-use-vague-time-suffixes`, `should-not-use-reserved-words-as-identifiers`, `should-quote-reserved-word-identifiers`, `should-quote-english-word-identifiers`, `should-prefix-named-objects-by-type`


A review passes when it establishes every item above.
