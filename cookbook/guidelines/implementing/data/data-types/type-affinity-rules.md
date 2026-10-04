
SQLite assigns affinity from the declared type name using these rules in order:

| Rule | If declared type contains... | Affinity |
|------|------------------------------|----------|
| 1 | `"INT"` | INTEGER |
| 2 | `"CHAR"`, `"CLOB"`, `"TEXT"` | TEXT |
| 3 | `"BLOB"` or no type | BLOB |
| 4 | `"REAL"`, `"FLOA"`, `"DOUB"` | REAL |
| 5 | Otherwise | NUMERIC |

Order matters. `"FLOATING POINT"` contains `"INT"` (in "POINT"), so affinity is INTEGER, not REAL.

