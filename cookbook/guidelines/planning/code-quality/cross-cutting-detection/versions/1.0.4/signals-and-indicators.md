
**Logging — the canonical cross-cutting concern:**

- `Logger.log()`, `os.log()`, `NSLog()`, `Log.d()`, `console.log()`, `_logger.LogInformation()` — logging calls scattered through every file are not a scope group; they are woven in
- A centralized `LogManager` or `Logger` configuration file that sets up log destinations IS shared infrastructure — classify as a single `Logging Infrastructure` unit
- The test: would removing all log calls from a scope group break its logic? No. Logging is decoration, not behavior.

**Error handling:**

- `do/catch`, `try/except`, `try/catch`, `.catch {}` — error handling is structural to the language, not a cross-cutting concern unto itself
- A centralized `ErrorHandler` that receives errors from all layers and routes them (to UI, analytics, retry logic) IS shared infrastructure — it has its own logic and state
- Custom error types / `enum AppError` — shared error taxonomy is shared infrastructure if it is used across 3+ scope groups
- The test: does every scope group need to know about the `ErrorHandler` explicitly? If yes, it may be an anti-pattern (forced coupling). If error types are passed as values, the error taxonomy is shared data, not cross-cutting behavior.

**Analytics instrumentation:**

- `Analytics.track("event_name", properties: [...])` calls scattered across UI and business logic — cross-cutting concern; the call sites are not a scope group
- The `Analytics` service / SDK wrapper itself — shared infrastructure with a clear boundary
- Event definition files (`AnalyticsEvents.swift`, `events.ts`) — shared data definitions; belong with the analytics infrastructure, not split across callers
- The test: if you removed all analytics calls, would each scope group still function correctly? Yes — analytics is observational, not behavioral.

**Authentication checks:**

- `guard isAuthenticated else { return }` scattered in individual handlers — these are policy enforcement points, not a scope group
- A centralized `AuthMiddleware`, `AuthGuard`, `SessionManager`, or `TokenRefreshInterceptor` with its own lifecycle and state — this IS a scope group (security infrastructure)
- The test: does removing the auth check break the underlying feature logic? No — the feature works; it just runs without access control. Auth checks are policy, not logic.

**Caching layers:**

- Cache read/write calls inside service implementations (`if let cached = cache[key] { return cached }`) — this is an optimization woven into the service; not a cross-cutting concern in the same sense as logging, but also not a separate scope group
- A dedicated caching service — `CacheService`, `ImageCache`, `ResponseCache` — with its own eviction policy and invalidation logic IS shared infrastructure
- The test: could you remove the caching layer and have everything still work correctly (just slower)? Yes — caching is an optimization. If removing it breaks correctness (not just performance), it is not a cache but a source of truth.

**Retry logic:**

- Inline retry loops within individual network calls — part of the networking layer, not cross-cutting
- A centralized `RetryPolicy` or `RetryInterceptor` applied to all outgoing requests — shared infrastructure belonging to the networking scope group
- The test: would removing retry logic break features? No — features would fail on transient errors instead of succeeding, but the logic is unchanged.

**Dependency injection containers:**

- A DI container that wires together all scope groups is a composition root — it is not itself a scope group in the functional sense, but it is a file (or files) that must be cataloged separately as the bootstrap/wiring layer

**Distinguishing cross-cutting from shared infrastructure:**

| Concern | Cross-cutting (do NOT isolate) | Shared infrastructure (IS its own scope group) |
|---|---|---|
| Logging | Log call sites throughout code | Logger configuration, log routing, log formatters |
| Analytics | Event tracking call sites | Analytics SDK wrapper, event schema definitions |
| Error handling | Try/catch at call sites | Centralized error router, custom error taxonomy |
| Auth | Auth checks at handler entry points | SessionManager, TokenRefreshService, AuthGuard |
| Caching | Cache lookups inline in services | CacheService with eviction and invalidation logic |
| Retry | Inline retry loops | RetryPolicy, RetryInterceptor applied globally |

**The definitive test for cross-cutting vs shared infrastructure:**

Ask: "Does this code have its own state, lifecycle, or logic — or does it exist only as calls woven into other code?" Code with its own state, lifecycle, or meaningful logic is shared infrastructure. Code that is only call sites in other modules is cross-cutting.

