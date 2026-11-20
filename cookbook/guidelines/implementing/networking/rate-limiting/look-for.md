
- `should-respect-server-rate-limits`: a client that sends at whatever rate it likes, regardless of the server's limits.
- `should-handle-429-gracefully`: a 429 treated as a hard failure, surfaced raw to the user, or retried at once.
- `must-honor-retry-after`: a 429 retried before its `Retry-After` has passed, or a parser that reads only seconds and not an HTTP-date.
- `should-back-off-without-retry-after`: a 429 without `Retry-After` retried at a fixed or immediate interval.
- `should-track-ratelimit-remaining`: `RateLimit-Remaining` ignored until a 429 arrives.
- `should-queue-and-batch-at-the-allowed-rate`: bursts fired at once and retried on 429 instead of queued at the allowed rate.
