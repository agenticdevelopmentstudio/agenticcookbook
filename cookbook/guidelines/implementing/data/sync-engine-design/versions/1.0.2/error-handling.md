
**Exponential backoff with jitter:** Apply to all transient failures.

```
delay = min(MAX_DELAY, BASE_DELAY * 2^attempt) + random(0, JITTER)
```

Typical values: `BASE_DELAY = 1s`, `MAX_DELAY = 15min`, `JITTER = 0–1s`.

**Retry categories:**

| Error | Action |
|-------|--------|
| Network timeout, 503 | Retry with backoff |
| 400, 401, 403 | Do not retry — surface to user |
| 409 Conflict | Apply conflict resolution strategy, then retry |
| 500 | Retry with longer backoff |

**Circuit breaker:** After N consecutive sync failures (e.g., 5), stop retrying automatically. Enter a degraded mode: the app continues to work offline, changes queue locally. Resume sync only after a cooldown period (e.g., 30 minutes) or explicit user action. Log the failure reason for diagnostics.

MUST surface persistent sync failures to the user — never silently fail. A status indicator showing "Sync paused — check connection" is acceptable; silently losing changes is not.

