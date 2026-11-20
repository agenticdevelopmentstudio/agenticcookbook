
PostgreSQL declarative partitioning (PostgreSQL 10+; mature in 14-18) supports three kinds.

| Strategy | Use when | Example key |
|----------|----------|-------------|
| RANGE | Time-series, sequential IDs, retention by window | `created_at` per month |
| LIST | Discrete categories with bounded cardinality | `region`, `tenant_id` |
| HASH | Even spread with no natural range/list key | `user_id` mod N |
