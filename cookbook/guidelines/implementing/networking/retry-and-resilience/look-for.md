
- `should-retry-transient-failures`: a transient failure surfaced at once with no retry, or retried with no backoff or jitter.
- `should-back-off-with-full-jitter`: a fixed delay, a delay with no random component, or one with no `max_delay` cap.
- `should-use-the-default-retry-parameters`: a base delay, cap or retry count that departs from the table with no stated reason, or retries of a non-idempotent call that is not safe to repeat.
- `should-treat-listed-codes-as-retryable`: a retryable status (408, 429, 502, 503, 504, or 500 on an idempotent call) handled as final, or a 500 from a non-idempotent call retried.
- `must-respect-retry-after`: a retry after a 429 or 503 sent before its `Retry-After` has passed.
- `must-not-retry-deterministic-failures`: a retry on 400, 401, 403, 404, 409 or 422.
- `should-use-a-circuit-breaker`: calls to a failing dependency with no circuit breaker, or one with no sliding window, threshold, cooldown or single half-open probe.
