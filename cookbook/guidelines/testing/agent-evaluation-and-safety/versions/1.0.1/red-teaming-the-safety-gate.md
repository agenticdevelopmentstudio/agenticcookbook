
- You **MUST** seed the safety gate with an adversarial suite (jailbreaks, direct and indirect prompt injection, role-play coercion, encoding tricks) — passing benign inputs proves nothing about resistance.
- You **SHOULD** combine curated known-attack cases with periodic automated/agentic red-teaming; treat any new bypass as a permanent regression case added to the suite.
- You **SHOULD** layer runtime guardrails (input/output filters, allow-lists, tool-permission scoping) as defense-in-depth, and **MUST NOT** treat a guardrail as a substitute for the gate that tests it.

