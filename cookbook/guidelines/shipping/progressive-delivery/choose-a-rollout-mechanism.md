
Pick the lightest mechanism that fits the risk; do not stack all of them.

| Mechanism | What varies | Use when |
|---|---|---|
| Feature flag / percentage | User cohort sees new behavior | Application-level changes; per-user targeting; instant kill switch |
| Canary | Small slice of live traffic hits new version | Service/deploy-level risk; want real-traffic signal before fleet-wide |
| Ring deployment | Rollout advances by audience tier (internal -> early -> broad) | Many tenants/regions; staged confidence building |
| Blue-green | Two full environments; traffic cut over atomically | Need instant full cutover + instant rollback; can afford 2x capacity |

- High-risk changes (schema-affecting, auth, payment, irreversible side effects) SHOULD be rolled out progressively rather than shipped to 100% at once.
- A typical canary ramp holds at each step long enough to observe peak load, cache warming, and background jobs — e.g. 1% -> 5% -> 25% -> 50% -> 100%. Each step MUST have an explicit hold duration and pass/fail criteria.
- Schema and data changes MUST stay backward-compatible across the rollout window (expand-then-contract): old and new code run against the same store simultaneously.

