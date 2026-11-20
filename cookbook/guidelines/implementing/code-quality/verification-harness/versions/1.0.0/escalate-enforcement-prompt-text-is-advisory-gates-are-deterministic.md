
Instructions in a prompt, CLAUDE.md, or skill are advisory — an agent can and will sometimes ignore them. Per Anthropic's Claude Code best practices, hooks and external gates "are deterministic and guarantee the action happens." Choose the weakest level that holds:

| Level | Mechanism | Enforcement |
|-------|-----------|-------------|
| In-prompt | "run the tests and fix failures" in the same message | Advisory — best for one-off tasks |
| Per-session | An evaluator re-checks a stated condition after each turn | Stronger — keeps an unattended run on target |
| Deterministic gate | A Stop hook / pre-commit hook / CI job that blocks completion until the check passes | Hard — does not depend on the agent choosing to comply |

- Any check that protects correctness for an unattended or merged change **MUST** be enforced by a deterministic gate (CI, pre-commit, or stop-hook), **MUST NOT** rely on prompt instructions alone.
- Gates that can loop forever **SHOULD** cap retries and surface to a human on repeated failure rather than spinning.

