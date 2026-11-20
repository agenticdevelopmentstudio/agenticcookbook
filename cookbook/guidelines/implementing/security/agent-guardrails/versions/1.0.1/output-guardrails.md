
Treat all model output as untrusted until it has passed checks (see [adc.guideline.implementing.security.llm-application-security](cookbook:a8088a6a-4542-4f6c-b74a-7c7ef7dcc63d)).

- **deterministic-output-checks**: Output guardrails **MUST** be enforced deterministically — schema/JSON validation, PII and secret detection, and unsafe-content moderation run in code, not by asking the model to self-certify.
- **schema-conformance**: Structured output **MUST** be parsed and validated against an explicit schema; non-conforming output **MUST** be rejected or repaired, never passed downstream verbatim.
- **no-leakage**: Output **MUST** be scanned for PII, credentials, and system-prompt leakage (OWASP LLM02:2025, LLM07:2025) before it is returned or persisted.

