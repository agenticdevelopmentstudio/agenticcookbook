<!-- leaf: test-general/tool-call-evaluation · source: guidelines/testing/tool-call-evaluation.md -->

**Rules** (cite as `test-general/tool-call-evaluation#<slug>`):

- `got-there-you-evaluate-whether-agent-selected` MUST — When an agent has tools (function calling, MCP servers), correctness is not just the final answer — it is *how* the …
- `tool-call-eval-report-dimension-separately-so` SHOULD — A tool-call eval SHOULD report each dimension separately so failures are diagnosable:
- `test-case-pin-input-expected-tool` MUST — Each test case MUST pin an input and the expected tool-call trajectory (tool names plus expected arguments). Treat this …
- `argument-checks-allow-semantic-equivalence-where` MUST — Argument checks SHOULD allow semantic equivalence where exact match is too strict (e.g., equivalent date formats), but …
- `suite-include-cases-where-tool` MUST — The suite MUST include cases where a tool returns an error, an empty result, or a timeout, and assert the agent …
- `calling-leaderboard-you-not-assume-short-chain-pass` MUST — Tool-calling accuracy degrades as chain length and the number of available tools grow (a pattern visible across …
- `non-deterministic-so-report-pass-rates-trial` SHOULD — Run each case multiple times; tool selection is non-deterministic, so SHOULD report pass rates with trial counts, not a …

# Tool-call evaluation

When an agent has tools (function calling, MCP servers), correctness is not just the final answer — it is *how* the agent got there. You **MUST** evaluate whether the agent selected the right tool, supplied correct arguments, called tools in the right order, and stopped when the task was done.

## What to score

A tool-call eval **SHOULD** report each dimension separately so failures are diagnosable:

| Dimension | Question | Signal |
|-----------|----------|--------|
| Tool selection | Did it call the correct tool (and avoid wrong/no-op calls)? | accuracy, false-call rate |
| Argument correctness | Are argument names, types, and values right? | exact/semantic match |
| Ordering | Were dependent calls made in a valid sequence? | trajectory match |
| Stopping | Did it stop instead of looping or over-calling? | extra-call count |
| Task completion | Did the end-to-end task succeed? | pass/fail |

## Build a trajectory suite

- Each test case **MUST** pin an input and the expected tool-call trajectory (tool names plus expected arguments). Treat this suite as a fixed, versioned regression set.
- Argument checks **SHOULD** allow semantic equivalence where exact match is too strict (e.g., equivalent date formats), but **MUST** stay strict on identifiers, units, and destructive parameters.
- Score against the trajectory, not just the final output — an agent can reach a correct answer through an unsafe or wasteful path.

## Error-recovery cases

- The suite **MUST** include cases where a tool returns an error, an empty result, or a timeout, and assert the agent recovers (retries sensibly, picks a fallback, or reports failure) rather than hallucinating success.
- Include cases where the correct action is to call **no** tool, to confirm the agent does not invoke tools spuriously.

## Test long compositions explicitly

- Tool-calling accuracy degrades as chain length and the number of available tools grow (a pattern visible across function-calling benchmarks such as the Berkeley Function-Calling Leaderboard). You **MUST NOT** assume short-chain pass rates generalize to long chains.
- Add multi-step cases that exercise the realistic tool count the agent ships with, and report accuracy as a function of chain length.

## Practices

- Run each case multiple times; tool selection is non-deterministic, so **SHOULD** report pass rates with trial counts, not a single run.
- Gate releases on the suite and track per-dimension scores over time so a regression in argument correctness is not masked by stable task-completion numbers.
- Keep cases hermetic: stub or record tool responses so the eval measures the agent, not live backend flakiness.
