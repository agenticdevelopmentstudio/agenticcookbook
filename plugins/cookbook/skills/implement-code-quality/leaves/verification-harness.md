<!-- leaf: implement-code-quality/verification-harness · source: guidelines/implementing/code-quality/verification-harness.md -->

**Rules** (cite as `implement-code-quality/verification-harness#<slug>`):

- `harness-single-command-short-script` MUST — The harness MUST be a single command (or short script) the agent can invoke and that returns a machine-readable signal: …
- `check-deterministic-same-input-produces` MUST — The check MUST be deterministic: the same input produces the same pass/fail. Flaky, time-, or network-dependent checks …
- `agent-show-evidence-command-run` MUST — The agent MUST show evidence (the command run and its output), not assert success. Reviewing evidence is faster than …
- `failures-state-what-expected-what` SHOULD — Failures SHOULD state what was expected, what was observed, and the location (file:line) — not just a stack trace or a …
- `failure-name-concrete-next-step` SHOULD — Each failure SHOULD name a concrete next step ("rename x to y", "add a test for the logged-out case"), because an …
- `output-concise-dumping-thousands-lines` SHOULD — Output SHOULD be concise; dumping thousands of lines floods the agent's context and degrades subsequent reasoning.
- `unattended-merged-change-enforced-deterministic-gate-ci` MUST — Any check that protects correctness for an unattended or merged change MUST be enforced by a deterministic gate (CI, …
- `can-loop-forever-cap-retries-surface-human` SHOULD — Gates that can loop forever SHOULD cap retries and surface to a human on repeated failure rather than spinning.
- `gates-fail-only-correctness-stated` MUST — Gates MUST fail only on correctness or stated requirements (broken build, failing test, violated contract). They MUST …
- `find-gaps-check-told-flag-only-gaps` SHOULD — An adversarial reviewer or "find the gaps" check SHOULD be told to flag only gaps affecting correctness or the stated …

# Verification harnesses as agent guardrails

A verification harness is a runnable pass/fail check the agent can execute on its own output. Without one, "looks done" is the only stop signal the agent has, and a human becomes the verification loop. Providing a check the agent can read and iterate against closes that loop autonomously — widely treated as the single highest-leverage practice for unattended agent reliability.

## Make the check runnable and deterministic

- The harness **MUST** be a single command (or short script) the agent can invoke and that returns a machine-readable signal: a process exit code, a test summary, a diff against a fixture, or a screenshot compared to a target.
- The check **MUST** be deterministic: the same input produces the same pass/fail. Flaky, time-, or network-dependent checks **MUST NOT** gate completion — they teach the agent to retry randomly or suppress the signal.
- The agent **MUST** show evidence (the command run and its output), not assert success. Reviewing evidence is faster than re-running the check.
- Wire the command into the project so the agent can discover it (e.g., a documented `verify`/`lint`/`test` entry point referenced in agent-readable docs).

## Optimize failure output for an LLM reader

The agent acts on the harness's stdout/stderr, so error messages are part of the interface.

- Failures **SHOULD** state what was expected, what was observed, and the location (file:line) — not just a stack trace or a bare assertion.
- Each failure **SHOULD** name a concrete next step ("rename `x` to `y`", "add a test for the logged-out case"), because an actionable message turns into a correct edit; a vague one turns into a guess.
- Output **SHOULD** be concise; dumping thousands of lines floods the agent's context and degrades subsequent reasoning.

## Escalate enforcement: prompt text is advisory, gates are deterministic

Instructions in a prompt, CLAUDE.md, or skill are advisory — an agent can and will sometimes ignore them. Per Anthropic's Claude Code best practices, hooks and external gates "are deterministic and guarantee the action happens." Choose the weakest level that holds:

| Level | Mechanism | Enforcement |
|-------|-----------|-------------|
| In-prompt | "run the tests and fix failures" in the same message | Advisory — best for one-off tasks |
| Per-session | An evaluator re-checks a stated condition after each turn | Stronger — keeps an unattended run on target |
| Deterministic gate | A Stop hook / pre-commit hook / CI job that blocks completion until the check passes | Hard — does not depend on the agent choosing to comply |

- Any check that protects correctness for an unattended or merged change **MUST** be enforced by a deterministic gate (CI, pre-commit, or stop-hook), **MUST NOT** rely on prompt instructions alone.
- Gates that can loop forever **SHOULD** cap retries and surface to a human on repeated failure rather than spinning.

## Gate on correctness, not taste

- Gates **MUST** fail only on correctness or stated requirements (broken build, failing test, violated contract). They **MUST NOT** block on style nitpicks an autoformatter or optional linter can handle non-blockingly.
- An adversarial reviewer or "find the gaps" check **SHOULD** be told to flag only gaps affecting correctness or the stated spec; chasing every speculative finding drives over-engineering.

## Build it incrementally

- Start with the cheapest check that catches a real failure, then add cases as concrete failure patterns emerge. Do **NOT** pre-build an exhaustive suite up front (YAGNI).
- When a new class of agent error appears, encode a check for it so the harness — not a human — catches the recurrence next time.
