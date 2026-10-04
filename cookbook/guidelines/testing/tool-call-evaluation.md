---
id: d53b7623-38ee-4d9f-a99b-f54b6a64f7a6
title: "Tool-call evaluation"
domain: agenticdevelopercookbook://guidelines/testing/tool-call-evaluation
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Evaluate agent tool use for selection, argument correctness, ordering, and stopping against a fixed trajectory suite with error-recovery cases."
platforms: []
tags:
  - ai
  - agents
  - evals
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/testing/agent-evaluation-and-safety
  - agenticdevelopercookbook://guidelines/implementing/networking/mcp-server-design
references:
  - https://gorilla.cs.berkeley.edu/leaderboard.html
  - https://gorilla.cs.berkeley.edu/blogs/13_bfcl_v3_multi_turn.html
  - https://proceedings.mlr.press/v267/patil25a.html
  - https://modelcontextprotocol.io/specification/2025-06-18
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - ai-api-integration
  - writing-tests
---

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

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add BFCL v3 multi-turn, BFCL paper, MCP spec sources |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
