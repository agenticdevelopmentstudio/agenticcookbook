<!-- leaf: implement-networking/idempotency-keys · source: guidelines/implementing/networking/idempotency-keys.md -->

**Rules** (cite as `implement-networking/idempotency-keys#<slug>`):

- `payment-sending-message-accept-idempotency-key` SHOULD — State-changing endpoints that are not naturally idempotent — POST creating a resource, charging a payment, sending a …
- `per-authenticated-principal-not-let-one-tenant-key` MUST — The key is scoped per endpoint and per authenticated principal — MUST NOT let one tenant's key collide with another's. …
- `look-up-the-key` MUST — New key: acquire a lock on the key, then execute the operation. On completion, persist the key → {request-fingerprint, …
- `must` MUST — set a TTL on each record (24 hours is a common default). After expiry the same key value is treated as new. Keep the …
- `must-not` MUST — mutate the request body between retries that share a key — that triggers the 422 rejection above.

# Idempotency keys for write APIs

A client-supplied `Idempotency-Key` header lets a state-changing request (typically `POST`) be retried over an unreliable network without creating duplicate side effects. This is the widely-adopted pattern (Stripe, PayPal, others) and is being standardized as the IETF Internet-Draft `draft-ietf-httpapi-idempotency-key-header` — **treat the spec as in-progress/forecast, not a finalized RFC**.

This differs from the cookbook's offline-sync outbox dedup (see `agenticdevelopercookbook://principles/idempotency`): there the *server* derives a deterministic key from the operation; here the *client* supplies an opaque key it can reuse across retries.

## When to use it

- State-changing endpoints that are not naturally idempotent — `POST` creating a resource, charging a payment, sending a message — **SHOULD** accept an idempotency key.
- `GET`, `HEAD`, `PUT`, and `DELETE` are already idempotent by HTTP semantics and **do not** need a key. Do not add one out of habit (yagni).

## The header

- The client sends `Idempotency-Key: <opaque-value>`. A UUIDv4 or other high-entropy value is a sensible default; the server treats it as opaque.
- The key is scoped per endpoint and per authenticated principal — **MUST NOT** let one tenant's key collide with another's. Store the tuple `(principal, endpoint, key)`.

## Server-side algorithm

Process a write request carrying a key as follows:

1. **Fingerprint the request.** Compute a hash of the request payload (and any semantically significant headers). Store it alongside the key.
2. **Look up the key.**
   - **New key:** acquire a lock on the key, then execute the operation. On completion, persist the key → `{request-fingerprint, status-code, response-body}` and release the lock.
   - **Known key, request still in flight:** a concurrent retry **MUST** be blocked or rejected (return `409 Conflict`) rather than executed a second time. Use a row lock, advisory lock, or atomic conditional insert — not a read-then-write race.
   - **Known key, completed, same fingerprint:** **MUST** replay the stored response (same status and body) without re-executing the operation.
   - **Known key, completed, different fingerprint:** the client reused a key with different parameters. The server **MUST** reject it — return `422 Unprocessable Content` — rather than silently re-executing or overwriting. Failing fast here surfaces a client bug instead of double-charging.

## Persistence and expiry

- Persist key records durably (database or shared cache), not in per-process memory — a retry can land on any instance.
- **MUST** set a TTL on each record (24 hours is a common default). After expiry the same key value is treated as new. Keep the TTL longer than the client's maximum retry window.
- Only finalize (persist as replayable) once the side effect has committed. Recording the key before the operation succeeds risks replaying a response for work that never happened.

## Client responsibilities

- Generate the key **once per logical operation**, before the first attempt, and reuse the *same* key for every retry of that operation.
- **MUST NOT** mutate the request body between retries that share a key — that triggers the `422` rejection above.
- A fresh user-initiated action gets a fresh key.

## Anti-patterns

- Deriving the key from a timestamp or auto-increment — low entropy invites collisions.
- Treating a `409`/`422` from key handling as a transient error and retrying blindly (see `agenticdevelopercookbook://guidelines/implementing/networking/retry-and-resilience`).
- Caching only the status code and not the body, so a replay returns an incomplete response.
