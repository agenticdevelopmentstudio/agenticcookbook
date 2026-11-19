
- **must-use-snake-case-identifiers**: ALL identifiers MUST use `snake_case`.
- **should-use-one-table-number-convention**: SHOULD pick singular or plural table names and be consistent within a project.
- **should-prefer-singular-for-compound-names**: SHOULD prefer singular table names when compound names are common (`workflow_run` composes more naturally than `workflows_runs`).
- **should-prefer-plural-to-avoid-reserved-words**: SHOULD prefer plural table names when avoiding SQL reserved word collisions matters (`users` avoids the reserved word `user`).
- **should-document-table-number-convention**: Whatever you choose, SHOULD document the singular-or-plural choice.
- **must-not-mix-table-number-conventions**: MUST NOT mix singular and plural table names within a single schema.
- **must-name-primary-keys-table-id**: Primary key columns MUST use `<table_name>_id`, not bare `id`.
- **must-match-foreign-key-to-referenced-column**: Foreign key columns MUST match the referenced column name when possible.
- **should-qualify-repeated-parent-references**: When a table references the same parent table more than once, SHOULD add a descriptive qualifier to each foreign key column (`source_actor_id`, `destination_actor_id`).
- **must-prefix-booleans-is-or-has**: Boolean columns MUST be prefixed with `is_` or `has_`.
- **must-name-date-columns-by-event**: Date/time columns MUST use descriptive event names.
- **should-not-use-vague-time-suffixes**: Date/time columns SHOULD NOT use vague suffixes like `_at`.
- **should-not-use-reserved-words-as-identifiers**: SHOULD NOT use a SQLite reserved keyword (such as `order`, `group`, `index`, `key`, `value`) as an identifier; renaming is always preferred to quoting.
- **should-quote-reserved-word-identifiers**: If you must use a reserved word as an identifier, SHOULD quote it with double quotes (`"order"`).
- **should-quote-english-word-identifiers**: SHOULD quote any English word used as an identifier, even if not currently reserved.
- **should-prefix-named-objects-by-type**: SHOULD use these prefixes for all named objects: indexes `ix_tablename_purpose` (unique indexes `ux_`), check constraints `ck_tablename_column`, triggers `tr_tablename_event_purpose`.

