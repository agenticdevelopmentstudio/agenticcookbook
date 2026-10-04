
Denormalization deliberately introduces redundancy to speed up specific read patterns. ONLY denormalize when:

1. A join has been **measured** as a performance bottleneck
2. The data is **read far more than written**
3. You have a strategy for **keeping the redundant copy in sync**

Do not denormalize preemptively based on assumptions. Measure first.

**Example: denormalize a frequently-displayed display name**

```sql
-- Instead of joining to actors on every audit log query,
-- copy display_name onto the supertype table for fast reads
CREATE TABLE actors (
    actor_id     INTEGER PRIMARY KEY,
    actor_type   TEXT NOT NULL,
    display_name TEXT NOT NULL  -- denormalized from subtypes
);
```

