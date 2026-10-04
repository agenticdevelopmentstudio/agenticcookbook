
Constrain agency to the minimum required (OWASP LLM06:2025 Excessive Agency).

- **allow-list-tools**: The agent **MUST** be limited to an explicit allow-list of tools; tool guardrails **MUST** be enforced deterministically at the call boundary.
- **least-privilege**: Each tool **MUST** run with the narrowest scopes, credentials, and data access needed — no shared admin tokens.
- **human-in-the-loop**: High-impact or irreversible actions (payments, deletes, external sends, infra changes) **MUST** require explicit human confirmation before execution.
- **caps**: Spending, rate, and iteration caps **MUST** bound tool use to prevent runaway loops and unbounded consumption (OWASP LLM10:2025).

