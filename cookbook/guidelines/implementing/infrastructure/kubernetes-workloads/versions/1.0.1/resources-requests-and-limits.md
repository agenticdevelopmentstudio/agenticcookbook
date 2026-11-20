
- Every container **MUST** declare CPU and memory `requests` (for scheduling) and memory `limits` (to bound usage). Without requests the scheduler cannot place pods predictably; without a memory limit a leak can evict neighbors.
- Set `requests.memory == limits.memory` for predictable, non-burstable memory. For CPU, **MAY** omit `limits.cpu` to avoid throttling latency-sensitive workloads, but always set `requests.cpu`.
- **SHOULD** assign a `priorityClass` to critical workloads so they survive node pressure.

