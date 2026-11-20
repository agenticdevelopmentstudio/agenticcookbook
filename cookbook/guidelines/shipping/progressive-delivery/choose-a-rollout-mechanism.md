
| Mechanism | What varies | Use when |
|---|---|---|
| Feature flag / percentage | User cohort sees new behavior | Application-level changes; per-user targeting; instant kill switch |
| Canary | Small slice of live traffic hits new version | Service/deploy-level risk; want real-traffic signal before fleet-wide |
| Ring deployment | Rollout advances by audience tier (internal -> early -> broad) | Many tenants/regions; staged confidence building |
| Blue-green | Two full environments; traffic cut over atomically | Need instant full cutover + instant rollback; can afford 2x capacity |

