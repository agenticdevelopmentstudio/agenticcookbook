
- `should-respect-server-rate-limits`: whether the client stays within the server's rate limits
- `should-handle-429-gracefully`: whether 429 responses are handled gracefully
- `must-honor-retry-after`: whether `Retry-After` is honored in both its seconds and HTTP-date forms
- `should-back-off-without-retry-after`: whether a 429 without `Retry-After` uses exponential backoff
- `should-track-ratelimit-remaining`: whether the client tracks `RateLimit-Remaining` and slows down before a 429
- `should-queue-and-batch-at-the-allowed-rate`: whether requests are queued and batched at the allowed rate
