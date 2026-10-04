
**Cannot be added via ALTER TABLE.** Adding a CHECK constraint to an existing table requires the full recreate-copy-drop-rename procedure. Design constraints upfront.

**Row-scoped only.** CHECK constraints cannot reference other rows or tables. For cross-row validation, use triggers.

**Not verified on SELECT.** Data that bypassed constraints (via external file manipulation or `PRAGMA ignore_check_constraints`) can be read even if it violates constraints.

**Conflict resolution is always ABORT.** The `ON CONFLICT` clause is parsed but ignored for CHECK constraints — violations always abort the statement.

