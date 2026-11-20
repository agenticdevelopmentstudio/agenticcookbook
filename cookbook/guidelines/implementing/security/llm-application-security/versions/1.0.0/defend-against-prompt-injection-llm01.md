
Prompt injection is the top risk. It comes in two forms; both **MUST** be in the threat model.

- **Direct** — the user crafts input that overrides system instructions ("ignore previous instructions...").
- **Indirect** — hidden instructions arrive via content the agent *fetches or reads*: web pages, PDFs, emails, code comments, file contents, or another tool's results. This is the dominant agentic risk and is easy to miss.

Controls:

- You **MUST** keep a trust boundary between system/developer instructions and any untrusted content; clearly delimit and label retrieved or tool-returned content as data, not instructions.
- You **SHOULD** apply least-privilege so a successful injection cannot reach high-impact tools (see Excessive Agency below).
- You **SHOULD** prefer deterministic guardrails (allow-lists, output schemas, post-checks) over trusting the model to self-police — injection defenses are mitigations, not guarantees. Treat "the model was told not to" as no control at all.

