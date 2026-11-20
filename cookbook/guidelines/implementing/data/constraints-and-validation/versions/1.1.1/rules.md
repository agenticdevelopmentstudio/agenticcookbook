
- **should-use-table-level-checks-only-for-multi-column**: Schemas SHOULD use table-level CHECK constraints only when the expression references multiple columns.
- **should-name-checks-in-large-schemas**: Large schemas SHOULD use named constraints (`CONSTRAINT ck_… CHECK (…)`).
- **must-declare-not-null-alongside-check**: If NULL should be prohibited, the column MUST also declare `NOT NULL` as a separate constraint — it is not implied by CHECK.
- **must-not-use-prohibited-check-expressions**: A CHECK expression MUST NOT use subqueries (`SELECT ...`), `CURRENT_TIME`, `CURRENT_DATE` or `CURRENT_TIMESTAMP`; they are explicitly prohibited.
- **must-validate-now-dependent-dates-outside-check**: Date validation that depends on "now" (e.g., `CHECK (event_date <= CURRENT_DATE)`) cannot be expressed in a schema constraint. Such validation MUST use triggers or application-layer validation instead.
- **should-design-constraints-upfront**: Constraints SHOULD be designed upfront.
- **should-use-triggers-for-cross-row-validation**: Cross-row validation SHOULD use triggers.
- **must-not-trust-checks-on-bypassed-data**: Code reading data that bypassed constraints (via external file manipulation or `PRAGMA ignore_check_constraints`) MUST NOT assume it satisfies them; CHECK constraints are not verified on SELECT.
- **must-not-rely-on-on-conflict-for-checks**: Code MUST NOT rely on an `ON CONFLICT` clause to resolve CHECK violations; the `ON CONFLICT` clause is parsed but ignored for CHECK constraints — violations always abort the statement.
- **may-disable-checks-for-dirty-import**: When importing potentially dirty data, a script MAY turn CHECK enforcement off.
- **must-verify-integrity-after-unchecked-import**: After an import run with CHECK enforcement off, the import script MUST verify integrity.

