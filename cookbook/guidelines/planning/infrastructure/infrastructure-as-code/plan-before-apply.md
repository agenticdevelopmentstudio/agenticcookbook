
- Every change MUST be previewed with a **plan/preview** (`tofu plan`, `terraform plan`, `pulumi preview`) before apply.
- Treat the plan diff like a code review: a human (or a gated CI step) MUST inspect adds, changes, and especially **destroys/replaces** before approving.
- Run `plan` in CI on every pull request and surface the diff in the PR. `apply` SHOULD run only from a protected branch or a gated pipeline, not from developer laptops.
- Be wary of resources marked for replacement — confirm the underlying cause (a deliberate change vs. drift vs. a provider upgrade) before applying.

