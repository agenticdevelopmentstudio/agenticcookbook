
Design columns so the same logical value maps cleanly across both databases:

| Type | SQLite DDL | PostgreSQL DDL |
|------|-----------|----------------|
| UUID | `TEXT` | `UUID` |
| Boolean | `INTEGER` (0/1) | `BOOLEAN` |
| Timestamp | `TEXT` (ISO-8601 UTC) | `TIMESTAMPTZ` |
| JSON | `TEXT` | `JSONB` |

Always use UTC. Convert to local time only at the display layer.

