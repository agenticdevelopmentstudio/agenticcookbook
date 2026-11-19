
```
delay = min(MAX_DELAY, BASE_DELAY * 2^attempt) + random(0, JITTER)
```

Typical values: `BASE_DELAY = 1s`, `MAX_DELAY = 15min`, `JITTER = 0–1s`.

Classify errors before retrying:

| Error Category | Action |
|---------------|--------|
| Transient (timeout, 503) | Retry with backoff |
| Client error (400, 401, 403) | Do not retry — surface to user |
| Conflict (409) | Apply conflict resolution strategy, do not retry blindly |
| Server error (500) | Retry with longer backoff |

