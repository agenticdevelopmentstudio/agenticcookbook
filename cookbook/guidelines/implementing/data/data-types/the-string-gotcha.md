
`STRING` does NOT give TEXT affinity. Rule 5 (NUMERIC) applies because "STRING" contains neither "CHAR", "CLOB", nor "TEXT". This causes silent data corruption:

```sql
CREATE TABLE demo (val STRING);
INSERT INTO demo VALUES ('007');
SELECT typeof(val), val FROM demo;
-- Returns: integer, 7   <-- leading zeros silently lost
```

**Rule: NEVER use `STRING`. Always use `TEXT`.**

