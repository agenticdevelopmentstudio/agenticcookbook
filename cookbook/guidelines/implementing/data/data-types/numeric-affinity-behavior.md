
NUMERIC affinity aggressively converts text-like values to numbers:

```sql
CREATE TABLE demo (val NUMERIC);
INSERT INTO demo VALUES ('3.0e+5');
SELECT typeof(val), val FROM demo;
-- Returns: integer, 300000
```

