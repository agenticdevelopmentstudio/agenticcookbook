
- Run groundedness and hallucination evals in CI on a fixed query set; **MUST** fail the build when the hallucination rate regresses past a set threshold.
- Treat groundedness as a release gate alongside latency and cost, not a one-time benchmark — retriever index drift and model swaps both move it.

> Privacy note: when eval sets contain user data, redact or synthesize PII before sending to a judge model. This is engineering guidance, not legal advice; consult counsel for regulated data.

