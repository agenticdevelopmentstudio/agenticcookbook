
- You **MUST** use a maintained, versioned attack suite (e.g., an OWASP-mapped open-source red-team framework) and **MUST** pin the suite version per run so results are reproducible.
- You **SHOULD** run automated red-team evaluations in CI on every change to prompts, tools, models, or RAG sources — these are silent regression surfaces.
- You **SHOULD** combine automated probes with periodic manual/expert red teaming; novel jailbreaks rarely appear first in automated corpora.
- You **MUST** test the deployed configuration (system prompt, guardrails, tool wiring), not the bare model — guardrails are part of the system under test.
- You **SHOULD** re-run the suite after every model or provider version bump; behavior and refusal boundaries shift across versions.

