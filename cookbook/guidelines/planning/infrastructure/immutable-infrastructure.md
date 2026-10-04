---
id: 60b3f760-f397-4762-b2d5-5aba80fd51f8
title: "Immutable infrastructure"
domain: agenticdevelopercookbook://guidelines/planning/infrastructure/immutable-infrastructure
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Never mutate running servers in place; build a versioned image artifact and replace instances to deploy or roll back."
platforms: []
tags:
  - infrastructure
  - deployment
  - immutability
depends-on: []
related:
  - agenticdevelopercookbook://principles/immutability-by-default
  - agenticdevelopercookbook://principles/design-for-deletion
  - agenticdevelopercookbook://guidelines/planning/infrastructure/infrastructure-as-code
references:
  - https://martinfowler.com/bliki/ImmutableServer.html
  - https://docs.docker.com/build/building/best-practices/
  - https://12factor.net/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - configuration
---

# Immutable infrastructure

Never patch a running server in place. Build a versioned, immutable artifact — a machine or container image — and deploy by replacing the old instance with a new one. The running system stays a faithful copy of a known, reproducible build.

## Core rule

- Deployments **MUST** ship immutable, versioned artifacts and replace instances rather than mutating them.
- Once built, an artifact **MUST NOT** be modified; a change means building a new version.
- Servers are **cattle, not pets** — interchangeable and disposable, never hand-tuned and irreplaceable.

## Rebuild-and-redeploy over patch-in-place

- To change configuration, dependencies, or code, you **MUST** rebuild the image and roll out new instances — not SSH in to mutate the live one.
- Running instances **SHOULD** be treated as read-only; no manual `apt install`, no live config edits, no hotfix scripts that survive a restart.
- This eliminates **configuration drift**: every instance of version `vN` is byte-identical, so "works on that box but not this one" cannot happen.

## Rollback is a redeploy

- Rollback **MUST** be performed by redeploying the previous known-good image version, not by undoing changes on a live host.
- Keep prior image versions retained and addressable (immutable tags or digests, e.g. `app@sha256:...`) so any past release can be restored deterministically.
- Avoid mutable tags like `latest` for what is actually deployed; pin to an immutable digest or version tag.

## Pairs with IaC and containerization

- Pair this with **infrastructure-as-code** (see related): the artifact is built from version-controlled definitions (`Dockerfile`, Packer template) so builds are reproducible and reviewable.
- Containers are the common implementation, but the principle predates and outlives them — a baked VM image (Packer/AMI) is equally immutable.
- Provisioning of replacement instances **SHOULD** be automated end-to-end so replacement is routine, not a manual event.

## Build vs. runtime state

- Bake application code and dependencies **into** the image at build time.
- Inject environment-specific config at **deploy/runtime** via environment variables or a config service — do not bake secrets or per-environment values into the image.
- Persistent data (databases, user uploads) **MUST** live in external, durable stores or attached volumes — never on the instance's ephemeral disk, which is destroyed on replace.

## Scope and trade-offs (YAGNI)

- This applies wherever you deploy servers; you do not need an orchestrator to benefit. A single image redeployed to one VM already gives you reproducibility and clean rollback.
- Adopt heavier machinery — Kubernetes, managed image pipelines, blue-green or canary rollout infrastructure — only **when a measured need justifies it** (scale, zero-downtime SLAs, fleet size), not as a default.
- Faster iteration: optimize image builds (layer caching, small base images) so rebuild-to-deploy stays quick enough that no one is tempted to patch in place.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add Docker build + 12-factor sources |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
