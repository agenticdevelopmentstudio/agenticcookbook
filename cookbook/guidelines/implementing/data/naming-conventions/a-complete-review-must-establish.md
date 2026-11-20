
- All identifiers use snake_case exclusively (no camelCase, PascalCase, or mixed case)
- No bare `id` columns; all primary keys follow pattern `<table>_id` or semantic name
- Foreign key columns named as `<referenced_table>_id` for clarity
- No SQL reserved words used as unquoted identifiers
- Indexes follow `ix_<table>_<columns>` convention
- Unique constraints follow `uq_<table>_<columns>` convention
- Check constraints follow `ck_<table>_<constraint_name>` convention
- Foreign key constraints follow `fk_<table>_<referenced_table>` convention
- Triggers follow `trg_<table>_<action>_<timing>` convention (e.g., `trg_users_update_before`)

A review passes when it establishes every item above.
