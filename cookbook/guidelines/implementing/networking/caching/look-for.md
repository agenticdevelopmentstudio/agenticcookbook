
- `should-use-http-caching-headers`: responses with no `Cache-Control`, or caching done with a home-grown scheme instead of HTTP headers.
- `should-let-the-server-set-cache-policy`: a client that overrides or ignores the server's cache headers.
- `should-cache-immutable-assets-for-a-year`: versioned JS/CSS/images sent without `public, max-age=31536000, immutable`.
- `should-cache-dynamic-responses-privately`: cacheable API responses sent `public`, or with no `max-age`.
- `must-not-cache-sensitive-data-or-mutations`: a response carrying sensitive data, or the result of a mutation, without `Cache-Control: no-store`.
- `should-revalidate-with-etags`: re-downloading unchanged data with no `ETag` / `If-None-Match` / 304 path.
- `must-invalidate-after-mutations`: a POST/PUT/DELETE that leaves related cache entries in place.
- `should-stale-while-revalidate`: a client that blocks on the network when it holds cached data it could show while refreshing.
