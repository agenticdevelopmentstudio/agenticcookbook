
```sql
-- Expand: safe, non-blocking
SET lock_timeout = '5s';
ALTER TABLE orders ADD COLUMN customer_uuid uuid;          -- nullable, instant
CREATE INDEX CONCURRENTLY idx_orders_customer_uuid          -- no transaction wrapper
  ON orders (customer_uuid);
```
