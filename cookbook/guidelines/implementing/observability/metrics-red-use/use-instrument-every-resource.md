
For each resource, capture all three:

| Dimension | Meaning | Example signal |
|-----------|---------|----------------|
| **Utilization** | Fraction of time (or capacity) the resource was busy | CPU %, pool in-use / pool size |
| **Saturation** | Degree of queued/unservable extra work | run-queue length, pending tasks, swap activity |
| **Errors** | Count of error events | failed allocations, disk I/O errors, pool timeouts |

- **resource-coverage**: Resources that can become a bottleneck **SHOULD** be monitored with all three USE dimensions; saturation is the most predictive of impending failure and **MUST NOT** be silently omitted.
- **saturation-signal**: Saturation **SHOULD** be a measurable queue depth or wait metric, not inferred solely from high utilization — 100% utilization without saturation is healthy throughput.

