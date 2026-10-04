---
id: 0de6da80-6793-4ef5-afd3-c7663da1d952
title: "Ephemeral preview environments"
domain: agenticdevelopercookbook://guidelines/shipping/ephemeral-environments
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Provision a disposable per-PR environment from IaC, seed it with throwaway data, test against it, and auto-destroy on merge or close."
platforms: []
tags:
  - ci-cd
  - environments
  - testing
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/shipping/continuous-delivery
  - agenticdevelopercookbook://guidelines/testing/contract-testing
references:
  - https://www.getambassador.io/docs/telepresence
  - https://ephemeralenvironments.io/
  - https://northflank.com/blog/the-what-and-why-of-ephemeral-preview-environments-on-kubernetes-sandbox-testing
  - https://www.uffizzi.com/preview-environments-guide
  - https://www.bunnyshell.com/blog/best-practices-for-end-to-end-testing-in-2025/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - pre-pr
---

# Ephemeral preview environments

An ephemeral preview environment is an isolated, fully disposable stack provisioned automatically when a PR opens and destroyed automatically when it merges or closes. It exists to give reviewers and CI a realistic place to exercise the change end-to-end. Where feasible, every PR SHOULD get one.

## Lifecycle (three invariants)

- **created-automatically**: The environment MUST be provisioned on a PR `opened`/`synchronize` event, not by hand. Spin-up MUST be defined entirely in infrastructure-as-code (Compose, Helm, K8s manifests, Terraform, or a platform manifest) so it is reproducible.
- **isolated**: Each environment MUST own its services, datastore, and DNS, namespaced by the PR identifier (e.g. `pr-123.preview.example.com`, `app-pr-123-db`). The namespace is the isolation boundary; resources from different PRs MUST NOT collide.
- **destroyed-automatically**: Teardown MUST fire on the PR `closed` event (covers both merge and abandon). A scheduled reaper SHOULD also sweep orphans by age/TTL in case a teardown job fails. No environment may outlive its PR.

## Design for deletion — keep them cattle, not pets

These environments are throwaway by design (per *design-for-deletion*). To prevent drift into long-lived "pets":

- All state MUST be recreatable from IaC plus seed scripts; manual hotfixes to a live preview are forbidden — change the code or the IaC and let the environment rebuild.
- Environments SHOULD be cheap and short-lived: prefer spot/preemptible compute, scale-to-zero when idle, and a TTL-based auto-shutdown.
- Tear-down MUST remove every namespaced resource (compute, DB, buckets, DNS, secrets). Leaked resources are the dominant cost and security failure mode.

## Test data — disposable, never production

- Seed each environment with synthetic or anonymized fixtures (per *test-data-management*). Production PII MUST NOT be copied into a preview.
- Choose a database strategy: **fresh provision** (blank DB + run migrations + seed) is simplest and works anywhere; **copy-on-write branching** (e.g. Neon/PlanetScale-style branches, or a snapshot restore) is faster when the engine supports it natively. Pick fresh-provision by default and adopt branching only when spin-up latency is a measured bottleneck (per *yagni*).

## What to run against it

- Full-stack previews SHOULD include the real backend, not just a static frontend against shared staging — interaction bugs between front and back surface only when both run the PR's code.
- Run E2E/smoke suites and contract tests (see `agenticdevelopercookbook://guidelines/testing/contract-testing`) against the live URL, and post the preview link plus check results back as a PR comment for human review.
- For changes too large to stand up a full stack per PR, a request-routing / intercept approach (e.g. Telepresence-style local interception into a shared cluster) MAY substitute — treat that as a deliberate decision, not the default.

## Guardrails

- Preview environments MUST NOT have write access to production data stores, queues, or third-party prod accounts; point them at sandbox credentials.
- Spin-up and teardown jobs SHOULD be idempotent so a re-run or retried webhook does not duplicate or orphan resources.
- Note: managed-platform feature names and DB-branching capabilities evolve quickly — verify current behavior against the vendor's docs before relying on a specific guarantee. FORECAST: treat any "instant branch" or per-PR-cost claim as vendor-specific and unverified until measured in your own pipeline.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add recovered Tier-1 research sources (adversarially-audited) |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
