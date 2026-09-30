<!-- leaf: implement-networking/retry-and-resilience · source: guidelines/implementing/networking/retry-and-resilience.md -->

**Rules** (cite as `implement-networking/retry-and-resilience#<slug>`):

- `retryable-status-codes` MUST — 408, 429, 500 (idempotent only), 502, 503, 504. Clients MUST respect Retry-After header on 429 and 503.
- `clients-must-not-retry` MUST — 400, 401, 403, 404, 409, 422 — these are deterministic failures.

# Retry and Resilience

Not every failure is permanent. Retry transient failures with exponential backoff and jitter.

**Exponential backoff with full jitter:**
```
delay = random(0, min(max_delay, base * 2^attempt))
```

| Parameter | Default |
|-----------|---------|
| Base delay | 1 second |
| Max delay cap | 30 seconds |
| Max retries | 3-5 (idempotent), 0 (non-idempotent unless safe) |

**Retryable status codes:** 408, 429, 500 (idempotent only), 502, 503, 504.
Clients MUST respect `Retry-After` header on 429 and 503.

**Clients MUST NOT retry:** 400, 401, 403, 404, 409, 422 — these are deterministic failures.

**Circuit breaker** for cascading failure prevention:
- Track failure rate over a sliding window (e.g., 10 requests)
- Open circuit when failure rate exceeds threshold (e.g., 50%)
- Stay open for a cooldown period (e.g., 30 seconds)
- Half-open: allow 1 probe request to test recovery

References:
- [AWS: Exponential Backoff and Jitter](https://docs.aws.amazon.com/general/latest/gr/api-retries.html)
- [Microsoft: Transient Fault Handling](https://learn.microsoft.com/en-us/azure/architecture/best-practices/transient-faults)
- [Microsoft: Circuit Breaker Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker)
