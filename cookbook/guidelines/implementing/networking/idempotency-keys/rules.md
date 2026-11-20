
**When to use it**
- **should-accept-keys-on-non-idempotent-writes**: State-changing endpoints that are not naturally idempotent — `POST` creating a resource, charging a payment, sending a message — **SHOULD** accept an idempotency key.
- **should-not-add-keys-out-of-habit**: On `GET`, `HEAD`, `PUT` or `DELETE`, endpoints SHOULD NOT add one (an idempotency key) out of habit (yagni).
  - `GET`, `HEAD`, `PUT`, and `DELETE` are already idempotent by HTTP semantics and **do not** need a key.

**The header**
- **should-send-the-key-in-the-header**: The client SHOULD send `Idempotency-Key: <opaque-value>`.
  - A UUIDv4 or other high-entropy value is a sensible default; the server treats it as opaque.
- **must-scope-keys-per-principal-and-endpoint**: The key is scoped per endpoint and per authenticated principal — **MUST NOT** let one tenant's key collide with another's.
- **should-store-the-principal-endpoint-key-tuple**: The server SHOULD store the tuple `(principal, endpoint, key)`.

**Server-side algorithm**

Process a write request carrying a key as follows:
- **should-fingerprint-the-request**: The server SHOULD fingerprint the request: compute a hash of the request payload (and any semantically significant headers) and store it alongside the key.

**Look up the key.**
- **should-lock-new-keys-before-executing**: For a **new key**, the server SHOULD acquire a lock on the key, then execute the operation; on completion, persist the key → `{request-fingerprint, status-code, response-body}` and release the lock.
- **must-block-concurrent-retries**: **Known key, request still in flight:** a concurrent retry **MUST** be blocked or rejected (return `409 Conflict`) rather than executed a second time.
- **should-lock-atomically**: The server SHOULD use a row lock, advisory lock, or atomic conditional insert — not a read-then-write race.
- **must-replay-completed-requests**: **Known key, completed, same fingerprint:** **MUST** replay the stored response (same status and body) without re-executing the operation.
- **must-reject-a-reused-key-with-new-parameters**: The server **MUST** reject it — return `422 Unprocessable Content` — rather than silently re-executing or overwriting.
  - **Known key, completed, different fingerprint:** the client reused a key with different parameters.

**Persistence and expiry**
- **should-persist-key-records-durably**: The server SHOULD persist key records durably (database or shared cache), not in per-process memory — a retry can land on any instance.
- **must-expire-key-records**: **MUST** set a TTL on each record (24 hours is a common default).
  - After expiry the same key value is treated as new.
- **should-outlast-the-retry-window**: The server SHOULD keep the TTL longer than the client's maximum retry window.
- **should-finalize-after-commit**: The server SHOULD only finalize (persist as replayable) once the side effect has committed.

**Client responsibilities**
- **should-generate-one-key-per-operation**: The client SHOULD generate the key **once per logical operation**, before the first attempt, and reuse the *same* key for every retry of that operation.
- **must-not-mutate-the-body-between-retries**: **MUST NOT** mutate the request body between retries that share a key — that triggers the `422` rejection above.
- **should-use-a-fresh-key-per-user-action**: A fresh user-initiated action SHOULD get a fresh key.

**Anti-patterns**
- **should-not-derive-keys-from-timestamps**: Keys SHOULD NOT be derived from a timestamp or auto-increment — low entropy invites collisions.
- **should-not-retry-key-rejections-blindly**: Clients SHOULD NOT treat a `409`/`422` from key handling as a transient error and retry blindly (see [adc.guideline.implementing.networking.retry-and-resilience](cookbook:cef41f52-bfc6-4ff0-bb67-eb52521c7391)).
- **should-not-cache-status-without-body**: The server SHOULD NOT cache only the status code and not the body, so a replay returns an incomplete response.
