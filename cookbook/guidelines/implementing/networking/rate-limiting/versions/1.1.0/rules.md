
- **should-respect-server-rate-limits**: Clients SHOULD respect server rate limits.
- **should-handle-429-gracefully**: Clients SHOULD handle 429 responses gracefully.
- **must-honor-retry-after**: Clients MUST honor the `Retry-After` header (seconds or HTTP-date)
- **should-back-off-without-retry-after**: If no `Retry-After`, clients SHOULD use exponential backoff (see Retry section)
- **should-track-ratelimit-remaining**: Clients SHOULD track `RateLimit-Remaining` headers proactively — slow down before hitting 429
- **should-queue-and-batch-at-the-allowed-rate**: Clients SHOULD queue and batch requests at the allowed rate rather than fire-and-retry
