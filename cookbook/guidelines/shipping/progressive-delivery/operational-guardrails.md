
- Flags introduced purely to gate a rollout are temporary. Remove the flag and the dead branch once the change is at 100% and stable, to avoid permanent branching debt (`design-for-deletion`, `yagni`).
- Pause new progressive rollouts during an active incident or when the error budget is exhausted.
- Prefer the platform/orchestrator's native progressive-delivery support (e.g. Kubernetes-native canary controllers, or a managed flag service) before building bespoke traffic-shifting (`native-controls`, `open-source-preference`).

> FORECAST / evolving: specific controller versions, flag-vendor APIs, and SLO query syntaxes change frequently. Pin the tool and its version in your runbook rather than encoding vendor specifics here, and treat single-vendor adoption stats as marketing, not fact.

