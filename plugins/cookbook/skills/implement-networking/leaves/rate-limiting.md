<!-- leaf: implement-networking/rate-limiting · source: guidelines/implementing/networking/rate-limiting.md -->

**Rules** (cite as `implement-networking/rate-limiting#<slug>`):

- `clients-honor-retry-after-header` MUST — Clients MUST honor the Retry-After header (seconds or HTTP-date)
- `clients-track-ratelimit-remaining-headers` SHOULD — Clients SHOULD track RateLimit-Remaining headers proactively — slow down before hitting 429

# Rate Limiting

Respect server rate limits. Handle 429 responses gracefully.

- Clients MUST honor the `Retry-After` header (seconds or HTTP-date)
- If no `Retry-After`, use exponential backoff (see Retry section)
- Clients SHOULD track `RateLimit-Remaining` headers proactively — slow down before hitting 429
- Queue and batch requests at the allowed rate rather than fire-and-retry

References:
- [RFC 6585: 429 Too Many Requests](https://www.rfc-editor.org/rfc/rfc6585)
