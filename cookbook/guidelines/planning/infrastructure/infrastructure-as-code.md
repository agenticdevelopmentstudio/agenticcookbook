---
id: cc7f5ee6-a848-490a-9a28-e4acae0855b3
title: "Infrastructure as code"
domain: agenticdevelopercookbook://guidelines/planning/infrastructure/infrastructure-as-code
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Define infrastructure declaratively in version control and apply it through a reviewed plan, never by hand."
platforms: []
tags:
  - iac
  - infrastructure
  - devops
depends-on: []
related:
  - agenticdevelopercookbook://principles/explicit-over-implicit
  - agenticdevelopercookbook://principles/idempotency
  - agenticdevelopercookbook://principles/small-reversible-decisions
references:
  - https://opentofu.org/docs/
  - https://opentofu.org/docs/language/settings/backends/s3/
  - https://developer.hashicorp.com/terraform/cli/commands/plan
  - https://developer.hashicorp.com/terraform/language/state
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - configuration
  - new-module
---

# Infrastructure as code

Infrastructure (compute, networking, DNS, IAM, managed services) MUST be defined as declarative code in version control and changed only through a reviewed, planned apply. Click-ops and ad-hoc CLI edits are debugging conveniences, not the source of truth.

## Declarative, idempotent definitions

- Describe the **desired end state**, not the steps to reach it. Re-applying an unchanged configuration MUST produce no changes (idempotency).
- Definitions MUST be **reproducible**: the same code plus the same inputs yields the same infrastructure, on a clean machine, with no manual prerequisites.
- Pin tool and provider versions explicitly (e.g. a `.terraform.lock.hcl` / lockfile committed to the repo). Floating versions break reproducibility.
- Prefer mature, declarative tooling: **OpenTofu** or **Terraform** (HCL), or **Pulumi** (general-purpose languages) when programmable abstractions justify the added surface area.

## Plan before apply

- Every change MUST be previewed with a **plan/preview** (`tofu plan`, `terraform plan`, `pulumi preview`) before apply.
- Treat the plan diff like a code review: a human (or a gated CI step) MUST inspect adds, changes, and especially **destroys/replaces** before approving.
- Run `plan` in CI on every pull request and surface the diff in the PR. `apply` SHOULD run only from a protected branch or a gated pipeline, not from developer laptops.
- Be wary of resources marked for replacement — confirm the underlying cause (a deliberate change vs. drift vs. a provider upgrade) before applying.

## Remote state with locking

- State MUST live in a **remote backend** (S3, GCS, AzureRM blob, or a managed IaC platform), versioned and recoverable — never committed to git or left only on a laptop.
- State writes MUST be **locked** to prevent concurrent corruption. For the S3 backend, prefer native S3 lockfile-based locking (`use_lockfile = true`, available since 2025); a DynamoDB lock table remains valid and can run alongside it during migration. GCS and AzureRM provide their own locking.
- Use a consistent state key convention (`<env>/<component>/terraform.tfstate`) so IAM policies can scope per environment.

## Drift detection and reconciliation

- **Drift** (out-of-band manual changes) MUST NOT become the source of truth. Reconcile it back into code, or revert it.
- Run scheduled drift detection (e.g. a periodic `plan`, `pulumi refresh` + preview, or a platform's drift feature) so manual changes are caught in hours, not at the next unrelated apply when a `destroy` appears unexpectedly.
- When drift is real and intended, encode it in the configuration and re-apply; do not leave the divergence in place.

## Modules, credentials, and secrets

- Factor repeated patterns into **modules** with explicit inputs/outputs; pin module versions. Keep environments (dev/stage/prod) as separate state with shared modules — avoid copy-paste.
- Provider credentials MUST be **least-privilege**, short-lived where possible (OIDC/workload identity over long-lived static keys), and supplied via environment/secret store — never hard-coded.
- **Secrets MUST NOT be exposed in plaintext state.** State files store resource attributes (including outputs) in plaintext for HCL tools. Do not emit secrets as outputs; write them directly to a secrets manager during apply and have apps fetch at runtime. Pulumi encrypts values marked `secret` in state, but restrict state read access regardless.

## Adopt-when-justified (YAGNI)

- Reach for managed IaC platforms, Kubernetes operators, or multi-account orchestration **only when a measured need justifies the operational weight** — not as a default. Start with the smallest backend and module layout that works and grow deliberately (small, reversible decisions).

> Privacy/compliance notes here are engineering guidance, not legal advice. Confirm data-residency and credential-handling obligations with qualified counsel.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add primary IaC sources (OpenTofu S3 backend, Terraform plan/state) |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
