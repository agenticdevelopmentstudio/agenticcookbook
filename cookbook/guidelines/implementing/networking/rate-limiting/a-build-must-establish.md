
- `should-respect-server-rate-limits`: the client's request rate is bounded by the server's published limits, or the code says why not
- `should-handle-429-gracefully`: a 429 leads to a paced retry or a graceful degraded result, or the code says why not
- `must-honor-retry-after`: no request is retried before `Retry-After` (seconds or HTTP-date) has elapsed
- `should-back-off-without-retry-after`: a 429 without `Retry-After` is retried with exponential backoff, or the code says why not
- `should-track-ratelimit-remaining`: the client reads `RateLimit-Remaining` and slows before it reaches zero, or the code says why not
- `should-queue-and-batch-at-the-allowed-rate`: requests go through a queue that releases them at the allowed rate, batched where possible, or the code says why not
