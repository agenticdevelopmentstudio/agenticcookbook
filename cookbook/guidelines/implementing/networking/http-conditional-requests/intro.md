
# HTTP conditional requests and optimistic concurrency

Conditional requests attach a precondition (an ETag validator) to a request so the server can short-circuit a read or reject a stale write. Per RFC 9110 (June 2022), use `If-None-Match` for cache-efficient reads and `If-Match` for optimistic concurrency on mutations. This prevents lost updates without server-side locking and is distinct from idempotency keys (which make retries safe).

