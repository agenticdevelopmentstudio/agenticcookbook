
- The client sends `Idempotency-Key: <opaque-value>`. A UUIDv4 or other high-entropy value is a sensible default; the server treats it as opaque.
- The key is scoped per endpoint and per authenticated principal — **MUST NOT** let one tenant's key collide with another's. Store the tuple `(principal, endpoint, key)`.

