
| Probe | Purpose | Note |
|-------|---------|------|
| `startupProbe` | Gate slow-starting apps before other probes run | **SHOULD** use for apps with long init |
| `readinessProbe` | Remove pod from Service endpoints when not ready | **MUST** define; failing it stops traffic without a restart |
| `livenessProbe` | Restart a wedged container | **SHOULD** define; keep it cheap and distinct from readiness |
