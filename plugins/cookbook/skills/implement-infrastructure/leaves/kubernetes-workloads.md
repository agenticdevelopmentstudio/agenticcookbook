<!-- leaf: implement-infrastructure/kubernetes-workloads · source: guidelines/implementing/infrastructure/kubernetes-workloads.md -->

**Rules** (cite as `implement-infrastructure/kubernetes-workloads#<slug>`):

- `rbac-upgrades-you-not-default-prefer-managed-paas` SHOULD — Kubernetes adds substantial operational surface (control plane, networking, RBAC, upgrades). You SHOULD NOT default to …
- `need-justifies-use-managed-control-plane` SHOULD — When the need justifies it, SHOULD use a managed control plane (e.g., EKS, GKE, AKS) rather than self-hosting, to shift …
- `container-declare-cpu-memory-requests` MUST — Every container MUST declare CPU and memory requests (for scheduling) and memory limits (to bound usage). Without …
- `burstable-memory-cpu-omit-limits-cpu-avoid` MAY — Set requests.memory == limits.memory for predictable, non-burstable memory. For CPU, MAY omit limits.cpu to avoid …
- `should` SHOULD — assign a priorityClass to critical workloads so they survive node pressure.
- `probe-lightweight-dependency-free-where` MUST — Each probe MUST be lightweight and dependency-free where possible — a liveness probe that checks a database will …
- `should-2` SHOULD — use the default RollingUpdate strategy with explicit maxUnavailable and maxSurge. Set minReadySeconds so new pods prove …
- `must` MUST — define a PodDisruptionBudget for any workload that needs availability during voluntary disruptions (node drains, …
- `should-3` SHOULD — spread replicas with topologySpreadConstraints across nodes and zones.
- `pods-run-hardened-securitycontext-runasnonroot` SHOULD — Pods SHOULD run with a hardened securityContext: runAsNonRoot: true, readOnlyRootFilesystem: true, …
- `should-4` SHOULD — enforce baseline guarantees at the namespace level with Pod Security Admission (restricted profile) as of Kubernetes …
- `must-not` MUST — mount the default ServiceAccount token unless the workload calls the API server.
- `should-5` SHOULD — isolate workloads with namespaces and apply the recommended app.kubernetes.io/* labels for selection and tooling.
- `should-6` SHOULD — scale stateless workloads with a HorizontalPodAutoscaler driven by CPU, memory, or custom metrics; pair it with cluster …

# Kubernetes workloads

Guidance for running production workloads on Kubernetes. Adopt Kubernetes only when measured scale and operational needs justify its complexity; once committed, declare resources and health, harden pods, and roll out safely.

## Adopt only when the need is measured

- Kubernetes adds substantial operational surface (control plane, networking, RBAC, upgrades). You **SHOULD NOT** default to it. Prefer a managed PaaS, container service, or single VM until you have a measured need — multi-service orchestration, autoscaling, or multi-team self-service (per YAGNI).
- When the need justifies it, **SHOULD** use a managed control plane (e.g., EKS, GKE, AKS) rather than self-hosting, to shift undifferentiated operational load.

## Resources: requests and limits

- Every container **MUST** declare CPU and memory `requests` (for scheduling) and memory `limits` (to bound usage). Without requests the scheduler cannot place pods predictably; without a memory limit a leak can evict neighbors.
- Set `requests.memory == limits.memory` for predictable, non-burstable memory. For CPU, **MAY** omit `limits.cpu` to avoid throttling latency-sensitive workloads, but always set `requests.cpu`.
- **SHOULD** assign a `priorityClass` to critical workloads so they survive node pressure.

## Health probes

| Probe | Purpose | Note |
|-------|---------|------|
| `startupProbe` | Gate slow-starting apps before other probes run | **SHOULD** use for apps with long init |
| `readinessProbe` | Remove pod from Service endpoints when not ready | **MUST** define; failing it stops traffic without a restart |
| `livenessProbe` | Restart a wedged container | **SHOULD** define; keep it cheap and distinct from readiness |

- Each probe **MUST** be lightweight and dependency-free where possible — a liveness probe that checks a database will cascade failures.

## Rollout and availability

- **SHOULD** use the default `RollingUpdate` strategy with explicit `maxUnavailable` and `maxSurge`. Set `minReadySeconds` so new pods prove healthy before old ones retire.
- **MUST** define a `PodDisruptionBudget` for any workload that needs availability during voluntary disruptions (node drains, upgrades).
- **SHOULD** spread replicas with `topologySpreadConstraints` across nodes and zones.

## Pod security

- Pods **SHOULD** run with a hardened `securityContext`: `runAsNonRoot: true`, `readOnlyRootFilesystem: true`, `allowPrivilegeEscalation: false`, drop all Linux capabilities, and set a `seccompProfile` of `RuntimeDefault`.
- **SHOULD** enforce baseline guarantees at the namespace level with Pod Security Admission (`restricted` profile) as of Kubernetes 1.25+.
- **MUST NOT** mount the default ServiceAccount token unless the workload calls the API server.

## Organization and scaling

- **SHOULD** isolate workloads with namespaces and apply the recommended `app.kubernetes.io/*` labels for selection and tooling.
- **SHOULD** scale stateless workloads with a `HorizontalPodAutoscaler` driven by CPU, memory, or custom metrics; pair it with cluster autoscaling so capacity follows demand.

> Security and isolation guidance here is engineering practice, not a compliance certification; validate against your own regulatory and threat-model requirements.
