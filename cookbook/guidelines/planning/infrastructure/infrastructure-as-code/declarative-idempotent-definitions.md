
- Describe the **desired end state**, not the steps to reach it. Re-applying an unchanged configuration MUST produce no changes (idempotency).
- Definitions MUST be **reproducible**: the same code plus the same inputs yields the same infrastructure, on a clean machine, with no manual prerequisites.
- Pin tool and provider versions explicitly (e.g. a `.terraform.lock.hcl` / lockfile committed to the repo). Floating versions break reproducibility.
- Prefer mature, declarative tooling: **OpenTofu** or **Terraform** (HCL), or **Pulumi** (general-purpose languages) when programmable abstractions justify the added surface area.

