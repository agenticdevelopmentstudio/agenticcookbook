
- **should-use-http-caching-headers**: Caching SHOULD use HTTP caching headers.
- **should-let-the-server-set-cache-policy**: The server SHOULD control cache policy, and the client SHOULD honor it.
- **should-cache-immutable-assets-for-a-year**: **Immutable assets** (versioned JS/CSS/images) SHOULD be sent with `Cache-Control: public, max-age=31536000, immutable`.
- **should-cache-dynamic-responses-privately**: **Dynamic but cacheable** (API responses) SHOULD be sent with `Cache-Control: private, max-age=60`.
- **must-not-cache-sensitive-data-or-mutations**: Sensitive data and mutations **MUST NOT be cached**: send `Cache-Control: no-store`.
- **should-revalidate-with-etags**: **Conditional requests** SHOULD use ETags to avoid re-downloading unchanged data.

**Client-side invalidation:**
- **must-invalidate-after-mutations**: After mutations (POST/PUT/DELETE), related cache entries MUST be invalidated
- **should-stale-while-revalidate**: Clients SHOULD stale-while-revalidate: serve cached data immediately, refresh in background.
