
# Idempotency keys for write APIs

A client-supplied `Idempotency-Key` header lets a state-changing request (typically `POST`) be retried over an unreliable network without creating duplicate side effects. This is the widely-adopted pattern (Stripe, PayPal, others) and is being standardized as the IETF Internet-Draft `draft-ietf-httpapi-idempotency-key-header` — **treat the spec as in-progress/forecast, not a finalized RFC**.

This differs from the cookbook's offline-sync outbox dedup (see `agenticdevelopercookbook://principles/idempotency`): there the *server* derives a deterministic key from the operation; here the *client* supplies an opaque key it can reuse across retries.

