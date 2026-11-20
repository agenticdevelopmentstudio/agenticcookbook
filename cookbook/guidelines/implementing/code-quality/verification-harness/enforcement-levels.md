
| Level | Mechanism | Enforcement |
|-------|-----------|-------------|
| In-prompt | "run the tests and fix failures" in the same message | Advisory — best for one-off tasks |
| Per-session | An evaluator re-checks a stated condition after each turn | Stronger — keeps an unattended run on target |
| Deterministic gate | A Stop hook / pre-commit hook / CI job that blocks completion until the check passes | Hard — does not depend on the agent choosing to comply |
