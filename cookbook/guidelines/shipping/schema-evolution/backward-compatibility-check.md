
Before shipping, verify the migration is backward-compatible:

- **Safe changes** (can ship without coordination): adding a nullable column, adding a column with a DEFAULT, creating a new index, renaming a column.
- **Breaking changes** (require migration coordination): changing column types, removing columns, adding NOT NULL constraints without defaults, dropping tables.

Breaking changes require the 12-step recreate procedure and MUST be tested against production-equivalent data before shipping. See the implementing copy of this guideline for the procedure.

