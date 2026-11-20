
- Factor repeated patterns into **modules** with explicit inputs/outputs; pin module versions. Keep environments (dev/stage/prod) as separate state with shared modules — avoid copy-paste.
- Provider credentials MUST be **least-privilege**, short-lived where possible (OIDC/workload identity over long-lived static keys), and supplied via environment/secret store — never hard-coded.
- **Secrets MUST NOT be exposed in plaintext state.** State files store resource attributes (including outputs) in plaintext for HCL tools. Do not emit secrets as outputs; write them directly to a secrets manager during apply and have apps fetch at runtime. Pulumi encrypts values marked `secret` in state, but restrict state read access regardless.

