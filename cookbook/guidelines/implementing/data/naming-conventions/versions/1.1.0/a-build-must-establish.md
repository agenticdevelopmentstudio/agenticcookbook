
- `must-use-snake-case-identifiers`: every table, column, index, constraint and trigger name is `snake_case`
- `should-use-one-table-number-convention`: the project's table names are all singular or all plural, or the code says why not
- `should-prefer-singular-for-compound-names`: a schema with many compound table names uses singular names, or the code says why not
- `should-prefer-plural-to-avoid-reserved-words`: a schema where reserved-word collisions matter uses plural table names, or the code says why not
- `should-document-table-number-convention`: the singular-or-plural choice is written down, or the code says why not
- `must-not-mix-table-number-conventions`: no schema mixes singular and plural table names
- `must-name-primary-keys-table-id`: every primary key column is named `<table_name>_id`; none is bare `id`
- `must-match-foreign-key-to-referenced-column`: every foreign key column has the referenced column's name, unless a qualifier is needed
- `should-qualify-repeated-parent-references`: a table referencing one parent more than once gives each such column a descriptive qualifier, or the code says why not
- `must-prefix-booleans-is-or-has`: every boolean column name starts with `is_` or `has_`
- `must-name-date-columns-by-event`: every date/time column is named for its event (`creation_date`, `completion_date`)
- `should-not-use-vague-time-suffixes`: no date/time column ends in a vague suffix such as `_at`, or the code says why not
- `should-not-use-reserved-words-as-identifiers`: no identifier is a SQLite reserved keyword, or the code says why not
- `should-quote-reserved-word-identifiers`: every identifier that is a reserved word is double-quoted wherever it appears, or the code says why not
- `should-quote-english-word-identifiers`: every English word used as an identifier is quoted, or the code says why not
- `should-prefix-named-objects-by-type`: indexes are named `ix_tablename_purpose` (unique `ux_`), check constraints `ck_tablename_column`, and triggers `tr_tablename_event_purpose`, or the code says why not

