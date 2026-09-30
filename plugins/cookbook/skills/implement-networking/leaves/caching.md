<!-- leaf: implement-networking/caching · source: guidelines/implementing/networking/caching.md -->

**Rules** (cite as `implement-networking/caching#<slug>`):

- `must-not-cache` MUST (sensitive data, mutations) — 
- `related-cache-entries-invalidated` MUST — After mutations (POST/PUT/DELETE), related cache entries MUST be invalidated

# Caching

Use HTTP caching headers. The server controls cache policy; the client honors it.

**Immutable assets** (versioned JS/CSS/images):
```
Cache-Control: public, max-age=31536000, immutable
```

**Dynamic but cacheable** (API responses):
```
Cache-Control: private, max-age=60
```

**MUST NOT cache** (sensitive data, mutations):
```
Cache-Control: no-store
```

**Conditional requests** — use ETags to avoid re-downloading unchanged data:
1. Server sends `ETag: "abc123"`
2. Client revalidates with `If-None-Match: "abc123"`
3. Server responds 304 Not Modified (no body) or 200 with new data

**Client-side invalidation:**
- After mutations (POST/PUT/DELETE), related cache entries MUST be invalidated
- Stale-while-revalidate: serve cached data immediately, refresh in background
- Framework support: React Query, SWR, Apollo Client all handle this natively

References:
- [RFC 9111: HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111)
- [web.dev: HTTP Cache](https://web.dev/articles/http-cache)
- [MDN: Cache-Control](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)
