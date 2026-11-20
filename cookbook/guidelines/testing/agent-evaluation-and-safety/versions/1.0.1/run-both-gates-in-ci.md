
- You **MUST** trigger both gates on every change to the model/version, system prompt, tool definitions, retrieval corpus, or guardrail config — any of these can regress behavior.
- You **MUST** treat a model-version bump from a provider as a code change: re-run both gates before rolling it forward, even if the prompt is unchanged.
- You **SHOULD** record each result against the dataset revision and model id so regressions are attributable to a specific change.
- You **SHOULD** keep a held-out set that never informs iteration, so the gate measures generalization, not memorization.

