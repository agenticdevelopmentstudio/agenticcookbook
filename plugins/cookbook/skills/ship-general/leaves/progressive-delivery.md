<!-- leaf: ship-general/progressive-delivery · source: guidelines/shipping/progressive-delivery.md -->

**Rules** (cite as `ship-general/progressive-delivery#<slug>`):

- `deploy-not-imply-100-exposure-ship` MUST — A deploy MUST NOT imply 100% exposure. Ship the artifact dark, then control exposure separately.
- `weights-ring-assignment-changeable-without-redeploy-keeps` MUST — The exposure control plane (feature flags, traffic weights, or ring assignment) MUST be changeable without a redeploy. …
- `progressive-change-observable-own-tag-metrics` MUST — Each progressive change MUST be observable on its own: tag metrics/logs/traces with the variant or cohort so canary and …
- `irreversible-side-effects-rolled-out-progressively-rather` SHOULD — High-risk changes (schema-affecting, auth, payment, irreversible side effects) SHOULD be rolled out progressively …
- `50-100-step-have-explicit-hold-duration` MUST — A typical canary ramp holds at each step long enough to observe peak load, cache warming, and background jobs — e.g. 1% …
- `schema-data-changes-stay-backward-compatible-across` MUST — Schema and data changes MUST stay backward-compatible across the rollout window (expand-then-contract): old and new …
- `step-define-quantitative-health-gates` MUST — Each step MUST define quantitative health gates *before* rollout — e.g. error rate, latency percentiles (p95/p99), and …
- `rollback-triggered-automatically-slo-health` SHOULD — Rollback SHOULD be triggered automatically when an SLO health gate fails or the error budget burns faster than the …
- `control-plane-expose-single-kill-switch` MUST — The control plane MUST expose a single kill switch that reverts exposure to the last-known-good state in one action.
- `rollback-re-application-idempotent-repeating-revert-produces` MUST — Rollback and re-application MUST be idempotent: repeating the revert produces the same safe state with no duplicate …
- `routine-scoring-revert-automated` SHOULD — Humans handle exceptions and ambiguous signals; routine scoring and revert SHOULD be automated.

# Progressive delivery

Progressive delivery separates *deploy* (code reaches production servers) from *release* (users see behavior), then exposes the change to a growing audience while watching health signals. It builds on continuous-delivery (the pipeline that produces a deployable build) and feature-flags (the control plane that gates exposure). The goal is to limit blast radius and roll back fast when signals degrade.

## Decouple deploy from release

- A deploy MUST NOT imply 100% exposure. Ship the artifact dark, then control exposure separately.
- The exposure control plane (feature flags, traffic weights, or ring assignment) MUST be changeable without a redeploy. This keeps rollback to seconds, not a build cycle (`small-reversible-decisions`).
- Each progressive change MUST be observable on its own: tag metrics/logs/traces with the variant or cohort so canary and baseline are comparable side by side (`explicit-over-implicit`).

## Choose a rollout mechanism

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

## Automate the rollback decision

- Each step MUST define quantitative health gates *before* rollout — e.g. error rate, latency percentiles (p95/p99), and a key business metric — compared against the baseline cohort.
- Rollback SHOULD be triggered automatically when an SLO health gate fails or the error budget burns faster than the allowed rate, not by waiting for a human to notice (`fail-fast`).
- The control plane MUST expose a single kill switch that reverts exposure to the last-known-good state in one action.
- Rollback and re-application MUST be idempotent: repeating the revert produces the same safe state with no duplicate side effects (`idempotency`).
- Humans handle exceptions and ambiguous signals; routine scoring and revert SHOULD be automated.

## Operational guardrails

- Flags introduced purely to gate a rollout are temporary. Remove the flag and the dead branch once the change is at 100% and stable, to avoid permanent branching debt (`design-for-deletion`, `yagni`).
- Pause new progressive rollouts during an active incident or when the error budget is exhausted.
- Prefer the platform/orchestrator's native progressive-delivery support (e.g. Kubernetes-native canary controllers, or a managed flag service) before building bespoke traffic-shifting (`native-controls`, `open-source-preference`).

> FORECAST / evolving: specific controller versions, flag-vendor APIs, and SLO query syntaxes change frequently. Pin the tool and its version in your runbook rather than encoding vendor specifics here, and treat single-vendor adoption stats as marketing, not fact.
