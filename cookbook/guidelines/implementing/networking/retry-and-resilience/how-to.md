
**Exponential backoff with full jitter:**
```
delay = random(0, min(max_delay, base * 2^attempt))
```

| Parameter | Default |
|-----------|---------|
| Base delay | 1 second |
| Max delay cap | 30 seconds |
| Max retries | 3-5 (idempotent), 0 (non-idempotent unless safe) |
