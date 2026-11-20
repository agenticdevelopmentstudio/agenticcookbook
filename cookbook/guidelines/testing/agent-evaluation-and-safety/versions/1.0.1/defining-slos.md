
- You **MUST** define both quality SLOs and safety SLOs as explicit numeric thresholds before a model reaches production — not "looks good in testing."
- You **MUST** express each SLO against a versioned dataset so a pass/fail is reproducible.
- Safety SLOs **SHOULD** include a hard ceiling (e.g., zero tolerance for secret/PII exfiltration) distinct from soft quality targets you tune over time.
- You **SHOULD NOT** trade a safety SLO for a quality gain; surface the conflict explicitly and decide deliberately.

