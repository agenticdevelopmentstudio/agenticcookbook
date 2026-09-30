<!-- leaf: implement-security/llm-application-security · source: guidelines/implementing/security/llm-application-security.md -->

**Rules** (cite as `implement-security/llm-application-security#<slug>`):

- `you-sanitize-encode-parameterize-model` MUST — You MUST sanitize, encode, or parameterize model output before it crosses any trust boundary: - Shell — never pass …
- `you-validate-structured-output-json` MUST — You MUST validate structured output (JSON, function-call args) against a strict schema and reject on mismatch — fail …
- `you-not-treat-output-proof-action` MUST — You MUST NOT treat output as proof of an action; verify side effects out-of-band.
- `two-forms-both-threat-model` MUST — Prompt injection is the top risk. It comes in two forms; both MUST be in the threat model.
- `you-keep-trust-boundary-between` MUST — You MUST keep a trust boundary between system/developer instructions and any untrusted content; clearly delimit and …
- `you-apply-least-privilege-so` SHOULD — You SHOULD apply least-privilege so a successful injection cannot reach high-impact tools (see Excessive Agency below).
- `you-prefer-deterministic-guardrails-allow` SHOULD — You SHOULD prefer deterministic guardrails (allow-lists, output schemas, post-checks) over trusting the model to …
- `you-grant-agent-tool-least` MUST — You MUST grant each agent/tool the least privilege needed — scoped credentials, narrow API surface, no ambient admin …
- `you-maintain-explicit-allow-list` MUST — You MUST maintain an explicit allow-list of callable tools; MUST NOT expose open-ended capabilities (arbitrary shell, …
- `you-require-human-loop-confirmation` SHOULD — You SHOULD require human-in-the-loop confirmation for high-impact or irreversible actions: sending money, deleting …
- `you-rate-limit-budget-tool` SHOULD — You SHOULD rate-limit and budget tool calls to bound runaway loops (relates to LLM10: Unbounded Consumption).
- `you-not-place-secrets-credentials-controls` MUST — You MUST NOT place secrets, credentials, or controls you rely on for security inside the system prompt — assume the …
- `you-filter-pii-sensitive-data` MUST — You MUST filter PII and sensitive data from both inputs and outputs, and avoid logging raw prompts/completions …
- `you-scope-retrieved-context-what` SHOULD — You SHOULD scope retrieved context to what the current user is authorized to see — never let RAG return another …
- `you-treat-documents-entering-vector` MUST — You MUST treat documents entering the vector store as untrusted (they can carry indirect-injection payloads); validate …
- `you-account-embedding-inversion-membership` SHOULD — You SHOULD account for embedding-inversion and membership-inference risk: embeddings can leak source content, so …

# LLM and agentic application security

Map your controls to the OWASP Top 10 for LLM Applications **2025** (pin that revision; renumbering and category shifts between editions). The two load-bearing rules: **treat every model output as untrusted input**, and **constrain what the model is allowed to do**. Everything below derives from those.

## Treat all model output as untrusted (LLM05: Improper Output Handling)

A model's output is attacker-influenceable data, not a trusted command. Apply the same egress controls you would to a raw HTTP request body.

- You **MUST** sanitize, encode, or parameterize model output before it crosses any trust boundary:
  - **Shell** — never pass output to `exec`/`system`/a shell string. Use argument arrays; **MUST NOT** interpolate into a command line.
  - **SQL** — use parameterized queries / prepared statements; never string-concatenate model output into SQL.
  - **HTML/DOM** — context-aware output encoding; **MUST NOT** inject into `innerHTML` or render as raw markup without sanitization.
  - **Tool arguments** — validate and type-check against a schema before any tool call (see input-validation guideline).
- You **MUST** validate structured output (JSON, function-call args) against a strict schema and reject on mismatch — fail fast rather than coerce.
- You **MUST NOT** treat output as proof of an action; verify side effects out-of-band.

## Defend against prompt injection (LLM01)

Prompt injection is the top risk. It comes in two forms; both **MUST** be in the threat model.

- **Direct** — the user crafts input that overrides system instructions ("ignore previous instructions...").
- **Indirect** — hidden instructions arrive via content the agent *fetches or reads*: web pages, PDFs, emails, code comments, file contents, or another tool's results. This is the dominant agentic risk and is easy to miss.

Controls:

- You **MUST** keep a trust boundary between system/developer instructions and any untrusted content; clearly delimit and label retrieved or tool-returned content as data, not instructions.
- You **SHOULD** apply least-privilege so a successful injection cannot reach high-impact tools (see Excessive Agency below).
- You **SHOULD** prefer deterministic guardrails (allow-lists, output schemas, post-checks) over trusting the model to self-police — injection defenses are mitigations, not guarantees. Treat "the model was told not to" as no control at all.

## Constrain tool and agent agency (LLM06: Excessive Agency)

Limit blast radius by limiting capability, permissions, and autonomy.

- You **MUST** grant each agent/tool the least privilege needed — scoped credentials, narrow API surface, no ambient admin access.
- You **MUST** maintain an explicit allow-list of callable tools; **MUST NOT** expose open-ended capabilities (arbitrary shell, unrestricted HTTP, broad filesystem) without a specific justification and additional controls.
- You **SHOULD** require human-in-the-loop confirmation for high-impact or irreversible actions: sending money, deleting data, sending external communications, deploying, or modifying access. Make the confirmation describe the concrete effect, not just "approve?".
- You **SHOULD** rate-limit and budget tool calls to bound runaway loops (relates to LLM10: Unbounded Consumption).

## Protect prompts and sensitive data (LLM07, LLM02)

- You **MUST NOT** place secrets, credentials, or controls you rely on for security inside the system prompt — assume the system prompt can leak (LLM07: System Prompt Leakage).
- You **MUST** filter PII and sensitive data from both inputs and outputs, and avoid logging raw prompts/completions containing secrets (LLM02: Sensitive Information Disclosure).
- You **SHOULD** scope retrieved context to what the current user is authorized to see — never let RAG return another tenant's documents.

## Secure RAG: vectors and embeddings (LLM08)

- You **MUST** treat documents entering the vector store as untrusted (they can carry indirect-injection payloads); validate provenance and apply per-document access controls at query time.
- You **SHOULD** account for embedding-inversion and membership-inference risk: embeddings can leak source content, so protect the vector store like the underlying data.

## Related risks to verify

- **LLM03 Supply Chain** / **LLM04 Data and Model Poisoning** — pin model versions, verify provenance of models, datasets, and plugins.
- **LLM09 Misinformation** — surface citations and mark generated content as unverified; do not present model output as authoritative fact in safety-critical flows.
