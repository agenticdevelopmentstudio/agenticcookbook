
# Agent guardrails

Guardrails are the runtime controls that sit around an agent or LLM and constrain what enters, what leaves, and what the agent is allowed to do. They **MUST** be enforced as deterministic code, not as prompt instructions alone — a model can always be talked out of following its own prompt (OWASP LLM01:2025 Prompt Injection).

