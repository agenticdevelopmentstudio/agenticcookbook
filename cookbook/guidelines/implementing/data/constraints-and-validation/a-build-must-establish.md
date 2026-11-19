
- `should-use-table-level-checks-only-for-multi-column`: every table-level CHECK references more than one column, or the code says why not
- `should-name-checks-in-large-schemas`: in a large schema, every CHECK is a named `CONSTRAINT`, or the code says why not
- `must-declare-not-null-alongside-check`: every CHECK-constrained column that must not hold NULL also declares `NOT NULL`
- `must-not-use-prohibited-check-expressions`: no CHECK expression contains a subquery, `CURRENT_TIME`, `CURRENT_DATE` or `CURRENT_TIMESTAMP`
- `must-validate-now-dependent-dates-outside-check`: every date rule relative to "now" is enforced by a trigger or in the application layer
- `should-design-constraints-upfront`: every CHECK is declared when its table is created, not retrofitted, or the code says why not
- `should-use-triggers-for-cross-row-validation`: every validation spanning rows or tables is a trigger, or the code says why not
- `must-not-trust-checks-on-bypassed-data`: no code reading data that may have bypassed constraints (external file edits, `PRAGMA ignore_check_constraints`) assumes the data satisfies them
- `must-not-rely-on-on-conflict-for-checks`: no statement relies on an `ON CONFLICT` clause to handle a CHECK violation
- `may-disable-checks-for-dirty-import`: a script that imports potentially dirty data is permitted to turn CHECK enforcement off with `PRAGMA ignore_check_constraints = ON`
- `must-verify-integrity-after-unchecked-import`: every import that turned CHECK enforcement off runs `PRAGMA integrity_check` after it

