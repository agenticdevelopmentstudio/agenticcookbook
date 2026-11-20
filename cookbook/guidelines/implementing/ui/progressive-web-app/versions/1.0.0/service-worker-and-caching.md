
Register the service worker after the page loads and choose a caching strategy per request class — **do not** apply one strategy globally:

| Strategy | Use for |
|----------|---------|
| Cache-first | Versioned, immutable static assets (hashed JS/CSS, fonts) |
| Network-first | HTML navigations and freshness-critical API reads |
| Stale-while-revalidate | Avatars, non-critical data tolerant of brief staleness |

You **MUST** version the cache (e.g. cache name suffix) and delete stale caches in the `activate` event so old assets do not leak. Precache the app shell so navigations resolve offline. Prefer a maintained library (Workbox) over hand-rolled fetch handlers unless the surface is trivial — this is a deliberate trade for correctness on edge cases (range requests, opaque responses), not a mandate.

