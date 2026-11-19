
A covering index includes every column the query reads, so SQLite never has to touch the table. This roughly halves the number of disk lookups.

```sql
-- Query needs fruit, state, and price
SELECT price FROM fruitsforsale WHERE fruit = 'Orange' AND state = 'CA';

-- Covering index: filter columns first, then the output column
CREATE INDEX idx_fruit_state_price ON fruitsforsale(fruit, state, price);
```

`EXPLAIN QUERY PLAN` confirms with `USING COVERING INDEX`. Aim for covering indexes on hot read paths where the query shape is stable.

