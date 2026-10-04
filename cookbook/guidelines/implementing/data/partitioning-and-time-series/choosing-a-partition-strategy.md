
PostgreSQL declarative partitioning (PostgreSQL 10+; mature in 14-18) supports three kinds. You **MUST** partition on column(s) that appear in the WHERE clause of hot queries, or pruning cannot fire.

| Strategy | Use when | Example key |
|----------|----------|-------------|
| RANGE | Time-series, sequential IDs, retention by window | `created_at` per month |
| LIST | Discrete categories with bounded cardinality | `region`, `tenant_id` |
| HASH | Even spread with no natural range/list key | `user_id` mod N |

- You **SHOULD** prefer native declarative partitioning over legacy inheritance + triggers.
- You **MUST** include the partition key in primary keys and unique constraints (a PostgreSQL constraint).

