
- **type-matches-query**: The index type **SHOULD** match how the column is queried, not default to B-tree reflexively:

| Type | Use when | Notes |
|------|----------|-------|
| B-tree | Equality, ranges, `ORDER BY`, `=`/`<`/`>`/`BETWEEN` | The default; supports unique constraints and sorted output |
| GIN | JSONB containment, arrays, full-text (`tsvector`) | Multiple keys per row; expensive to maintain on write-heavy columns |
| GiST | Ranges, geometry, nearest-neighbor, exclusion constraints | Lossy; basis for PostGIS and `tstzrange` overlap |
| BRIN | Very large, naturally-ordered or append-only tables | Stores per-block min/max; tiny and cheap, but only helps correlated data |
| Hash | Equality only | Rarely worth it over B-tree; no range or ordering support |

