
- `should-use-http-caching-headers`: every cacheable response sets HTTP caching headers, or the code says why not
- `should-let-the-server-set-cache-policy`: cache policy is decided by the server's headers and the client follows them, or the code says why not
- `should-cache-immutable-assets-for-a-year`: versioned assets are served with `Cache-Control: public, max-age=31536000, immutable`, or the code says why not
- `should-cache-dynamic-responses-privately`: cacheable API responses are served with `Cache-Control: private, max-age=60`, or the code says why not
- `must-not-cache-sensitive-data-or-mutations`: sensitive data and mutation responses are served with `Cache-Control: no-store`
- `should-revalidate-with-etags`: responses send an `ETag`, requests revalidate with `If-None-Match`, and an unchanged resource returns 304 with no body, or the code says why not
- `must-invalidate-after-mutations`: each POST/PUT/DELETE invalidates the cache entries it affects
- `should-stale-while-revalidate`: the client shows cached data at once and refreshes it in the background, or the code says why not
