
- Boolean columns use `INTEGER` type with `CHECK(col IN (0,1))` constraint
- Enum-like columns use `TEXT` or `INTEGER` with `CHECK(col IN (...))` constraint
- All CHECK constraints have documented enumeration of allowed values (in comment or constraint name)
- No CHECK expressions that evaluate NULL as truthy (NULL in any constraint expression prevents row from failing check)
- Range constraints (e.g., `CHECK(age >= 0 AND age <= 150)`) explicitly bounded
- Pattern validation via `CHECK(col LIKE pattern)` only for simple patterns; regex deferred to application layer
- CHECK constraints exclude domain validation that might be partially applied (validate in application or use NOT NULL + other constraints)
- No negation logic that silently accepts NULL: `CHECK(status != 'deleted')` will accept NULL (use explicit whitelist instead)
- Every rule is kept, or the change says why not: `should-use-table-level-checks-only-for-multi-column`, `should-name-checks-in-large-schemas`, `must-declare-not-null-alongside-check`, `must-not-use-prohibited-check-expressions`, `must-validate-now-dependent-dates-outside-check`, `should-design-constraints-upfront`, `should-use-triggers-for-cross-row-validation`, `must-not-trust-checks-on-bypassed-data`, `must-not-rely-on-on-conflict-for-checks`, `may-disable-checks-for-dirty-import`, `must-verify-integrity-after-unchecked-import`


A review passes when it establishes every item above.
