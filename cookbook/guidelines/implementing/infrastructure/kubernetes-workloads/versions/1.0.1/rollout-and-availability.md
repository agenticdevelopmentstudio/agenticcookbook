
- **SHOULD** use the default `RollingUpdate` strategy with explicit `maxUnavailable` and `maxSurge`. Set `minReadySeconds` so new pods prove healthy before old ones retire.
- **MUST** define a `PodDisruptionBudget` for any workload that needs availability during voluntary disruptions (node drains, upgrades).
- **SHOULD** spread replicas with `topologySpreadConstraints` across nodes and zones.

