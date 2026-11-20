
- `should-apply-request-body-egress-controls`, `must-sanitize-output-at-trust-boundaries`, `must-validate-structured-output`: A model's output is attacker-influenceable data, not a trusted command. These rules answer OWASP LLM05: Improper Output Handling, and treat all model output as untrusted.
- `must-threat-model-both-injection-forms`: Prompt injection is the top risk (OWASP LLM01).
- `must-keep-instruction-data-trust-boundary`, `should-apply-least-privilege-against-injection`, `should-prefer-deterministic-guardrails`: These are the controls against prompt injection.
- `should-limit-capability-permissions-autonomy`, `must-grant-least-privilege`, `must-allow-list-callable-tools`: These constrain tool and agent agency (OWASP LLM06: Excessive Agency).
- `must-not-put-secrets-in-system-prompt`, `must-filter-sensitive-data-in-and-out`: These protect prompts and sensitive data (OWASP LLM07, LLM02).
- `must-treat-vector-store-documents-as-untrusted`, `should-protect-vector-store-like-source-data`: These secure RAG vectors and embeddings (OWASP LLM08).
- `should-pin-models-and-verify-provenance`, `should-mark-generated-content-unverified`, `should-not-present-output-as-authoritative`: These are related risks to verify.
