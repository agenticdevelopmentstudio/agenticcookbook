
SQLite in tests does not behave identically to PostgreSQL or MySQL in production. Key differences that affect test validity:

| Behavior | SQLite | PostgreSQL |
|----------|--------|------------|
| Type enforcement | Permissive | Strict |
| Boolean | `INTEGER 0/1` | Native `BOOLEAN` |
| LIKE case sensitivity | Case-sensitive (ASCII) | Case-insensitive (`ILIKE`) |
| NULL in PK | Allowed | Not allowed |

Use SQLite for unit tests where dialect differences do not affect the logic under test. MUST use the production database for integration tests that cover type enforcement, constraint behavior, or database-specific SQL features.

