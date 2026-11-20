
- `must-apply-writes-only-on-matching-etag`: This is the read-modify-write guard against lost updates: two clients editing the same version cannot both succeed.
- `should-use-if-match-and-idempotency-keys-together`: **Distinct from idempotency keys.** `If-Match` rejects a write against a stale version; an idempotency key lets the SAME write be retried safely after a network failure.
