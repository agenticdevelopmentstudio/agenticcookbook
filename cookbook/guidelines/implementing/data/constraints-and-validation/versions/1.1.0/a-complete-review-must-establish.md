
- Boolean columns use `INTEGER` type with `CHECK(col IN (0,1))` constraint
- Enum-like columns use `TEXT` or `INTEGER` with `CHECK(col IN (...))` constraint
- All CHECK constraints have documented enumeration of allowed values (in comment or constraint name)
- No CHECK expressions that evaluate NULL as truthy (NULL in any constraint expression prevents row from failing check)
- Range constraints (e.g., `CHECK(age >= 0 AND age <= 150)`) explicitly bounded
- Pattern validation via `CHECK(col LIKE pattern)` only for simple patterns; regex deferred to application layer
- CHECK constraints exclude domain validation that might be partially applied (validate in application or use NOT NULL + other constraints)
- No negation logic that silently accepts NULL: `CHECK(status != 'deleted')` will accept NULL (use explicit whitelist instead)

