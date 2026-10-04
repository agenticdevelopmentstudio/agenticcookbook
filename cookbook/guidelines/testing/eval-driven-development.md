---
id: 7a942d3d-eb47-4eb2-8ed1-bebbcda6f7e6
title: "Eval-driven development for agent behavior"
domain: agenticdevelopercookbook://guidelines/testing/eval-driven-development
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "When the unit under test is agent or LLM behavior, build a calibrated eval harness instead of relying on ordinary unit tests."
platforms: []
tags:
  - evals
  - ai
  - testing
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/testing/the-testing-workflow
  - agenticdevelopercookbook://principles/tight-feedback-loops
references:
  - https://code.claude.com/docs/en/best-practices
  - https://arxiv.org/abs/2411.13768
  - https://huggingface.co/blog/evaleval/eval-costs-bottleneck
  - https://www.digitalapplied.com/blog/ai-agent-evaluation-pipeline-2026-testing-methodology
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - writing-tests
  - ai-api-integration
---

# Eval-driven development for agent behavior

Deterministic code is verified with ordinary unit tests. Agent and LLM behavior is probabilistic — the same input can yield different valid (or invalid) outputs across runs — so it requires an **eval harness** that scores behavior over many trials. Treat evals as the test suite for the non-deterministic parts of the system.

## When evals apply (and when they do not)

- **MUST** use ordinary deterministic tests for parsers, schema validation, tool-call argument construction, retries, and any logic with a fixed correct output. Do not wrap deterministic code in an LLM judge.
- **MUST** use an eval harness when the artifact under test is an agent's decisions, an LLM's generated text, multi-step tool use, or RAG answer quality — outputs that vary run to run.
- **SHOULD** isolate the deterministic and probabilistic layers so each is tested with the cheaper appropriate method.

## Choosing a grader

| Grader type | Strengths | Limits | Use when |
|---|---|---|---|
| Code-based (assertion, regex, exact/structured match) | Fast, cheap, reproducible, easy to debug | Brittle to valid phrasing variations | Output is objectively checkable |
| Model-based (LLM-as-judge) | Flexible, scalable, captures nuance, handles open-ended tasks | Non-deterministic, costs tokens, can be biased | Output is open-ended or subjective |

- **MUST** prefer a code-based grader whenever the success criterion can be expressed in code.
- **SHOULD** grade each quality dimension (e.g., groundedness, coverage, tone) with a separate, isolated LLM-judge rather than one judge scoring everything at once.
- **SHOULD** use a judge model deliberately different from the model under test to reduce self-preference bias (a documented but still-active research concern, not a settled magnitude).

## Calibrating an LLM judge

A model-based grader **MUST NOT** be allowed to gate (block a merge, fail a build, accept a release) until it has been calibrated against a human-labeled gold set.

- **MUST** assemble a human-labeled gold set, run the judge over it, and measure agreement (e.g., divergence rate or correlation) before trusting the judge.
- **MUST** re-calibrate when the judge prompt, the judge model, or the rubric changes.
- **SHOULD** instruct the judge to return "Unknown" or abstain when it lacks evidence, rather than guessing.
- **SHOULD** periodically read raw transcripts and grades; a passing aggregate score can hide a judge that is rejecting valid answers or rubber-stamping bad ones.

## Reliability over multiple runs

A single passing run proves nothing about probabilistic behavior.

- **MUST** report results across multiple runs of the same input, not one pass.
- **SHOULD** distinguish "succeeds at least once" from "succeeds every time" — these are different product guarantees. Anthropic's eval guidance frames these as `pass@k` (success in at least one of k attempts) and `pass^k` (all k trials succeed); pick the metric that matches your reliability requirement.
- **SHOULD** track the consistency metric over time so regressions in flakiness are visible, not just regressions in best-case quality.

## Holding out a test set

- **MUST** keep a held-out test set that is not used while iterating on prompts, rubrics, or the judge — otherwise you are tuning to the eval and overstating quality.
- **SHOULD** treat the gold set used for judge calibration and the held-out behavior test set as distinct; do not let one leak into the other.
- **SHOULD** version eval datasets alongside the code so a result is reproducible against a known dataset revision.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add recovered Tier-1 research sources (adversarially-audited) |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
