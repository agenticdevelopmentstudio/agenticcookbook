---
id: 6f6ccc46-33fb-44ad-8dce-d65581d8dfe0
title: "Kubernetes workloads"
domain: agenticdevelopercookbook://guidelines/implementing/infrastructure/kubernetes-workloads
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Run Kubernetes workloads with explicit resource requests/limits, health probes, hardened pod security, and safe rollout strategies."
platforms: []
tags:
  - kubernetes
  - workloads
  - deployment
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/infrastructure/kubernetes-configuration
  - agenticdevelopercookbook://guidelines/planning/infrastructure/immutable-infrastructure
references:
  - https://kubernetes.io/docs/concepts/configuration/overview/
  - https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
  - https://kubernetes.io/docs/concepts/security/pod-security-standards/
  - https://kubernetes.io/docs/concepts/workloads/pods/disruptions/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - configuration
  - performance-optimization
---

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

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add k8s resource/PSA/PDB primary sources |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
