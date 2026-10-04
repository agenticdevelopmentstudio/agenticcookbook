
- Define an **attack-success rate (ASR)** per attack class: fraction of adversarial prompts that achieve their objective.
- You **SHOULD** set an explicit ASR threshold (e.g., a hard ceiling for injection/jailbreak success) as a release gate, and **MUST** block release when a critical class exceeds it.
- You **MUST** track ASR over time and treat a regression as a release blocker, not a backlog item.
- You **SHOULD** record each finding with a reproducer, OWASP mapping, and severity so fixes are verifiable.

