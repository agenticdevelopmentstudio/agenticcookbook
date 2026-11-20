
- `should-retry-transient-failures`: transient failures are retried with exponential backoff and jitter, or the code says why not
- `should-back-off-with-full-jitter`: the delay is `random(0, min(max_delay, base * 2^attempt))`, or the code says why not
- `should-use-the-default-retry-parameters`: base delay is 1 second, the cap 30 seconds, max retries 3-5 for idempotent and 0 for non-idempotent calls unless safe, or the code says why not
- `should-treat-listed-codes-as-retryable`: 408, 429, 502, 503, 504 and (for idempotent calls only) 500 go to the retry path, or the code says why not
- `must-respect-retry-after`: no retry after a 429 or 503 is sent before its `Retry-After`
- `must-not-retry-deterministic-failures`: 400, 401, 403, 404, 409 and 422 are never retried
- `should-use-a-circuit-breaker`: a circuit breaker tracks failure rate over a sliding window, opens past a threshold, stays open for a cooldown and half-opens with 1 probe, or the code says why not
