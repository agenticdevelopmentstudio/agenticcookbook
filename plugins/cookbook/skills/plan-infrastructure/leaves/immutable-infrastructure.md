<!-- leaf: plan-infrastructure/immutable-infrastructure · source: guidelines/planning/infrastructure/immutable-infrastructure.md -->

**Rules** (cite as `plan-infrastructure/immutable-infrastructure#<slug>`):

- `deployments-ship-immutable-versioned-artifacts` MUST — Deployments MUST ship immutable, versioned artifacts and replace instances rather than mutating them.
- `once-built-artifact-not-modified-change-means-building` MUST — Once built, an artifact MUST NOT be modified; a change means building a new version.
- `dependencies-code-you-rebuild-image-roll-out` MUST — To change configuration, dependencies, or code, you MUST rebuild the image and roll out new instances — not SSH in to …
- `running-instances-treated-read-only-manual` SHOULD — Running instances SHOULD be treated as read-only; no manual apt install, no live config edits, no hotfix scripts that …
- `rollback-performed-redeploying-previous-known` MUST — Rollback MUST be performed by redeploying the previous known-good image version, not by undoing changes on a live host.
- `provisioning-replacement-instances-automated-end-end-so` SHOULD — Provisioning of replacement instances SHOULD be automated end-to-end so replacement is routine, not a manual event.
- `databases-user-uploads-live-external-durable-stores` MUST — Persistent data (databases, user uploads) MUST live in external, durable stores or attached volumes — never on the …

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
