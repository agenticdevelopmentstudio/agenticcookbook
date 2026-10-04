---
id: e2a99bf0-6b25-4769-9d1e-613b58b6f097
title: "Agent evaluation and safety"
domain: agenticdevelopercookbook://guidelines/testing/agent-evaluation-and-safety
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Gate every agent/LLM release on two checks: a quality eval gate and a safety gate, both run in CI on every model and prompt change."
platforms: []
tags:
  - ai
  - evals
  - safety
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/testing/eval-driven-development
  - agenticdevelopercookbook://guidelines/implementing/security/llm-application-security
references:
  - https://developers.openai.com/api/docs/guides/evals
  - https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
  - https://www.nist.gov/itl/ai-risk-management-framework
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - ai-api-integration
  - writing-tests
---

# Agent evaluation and safety

Shipping a reliable agent is one discipline with two gates: **evaluation** (is it good?) and **safety** (is it harmful or exploitable?). Treat both as release-gating, run in CI on every model, prompt, tool, or retrieval change — not as a post-launch afterthought. This guideline ties the cluster together; it cross-references rather than duplicates the detail in the related guidelines.

## Two gates, both required

A change to an agent system **SHOULD** pass both gates before release; either gate failing blocks the deploy.

| Gate | Question | SLO examples | Owned by |
|---|---|---|---|
| Eval (quality) | Does it do the job well? | task success rate, groundedness, tool-call accuracy, latency/cost budgets | eval-driven-development |
| Safety | Can it be made to cause harm? | jailbreak resistance, prompt-injection resistance, PII/secret leakage rate, refusal correctness | llm-application-security |

- For how to build graders, calibrate an LLM judge, and report `pass@k` vs `pass^k` consistency, follow **eval-driven-development**.
- For prompt injection, untrusted-output handling, and tool-agency constraints, follow **llm-application-security** (mapped to the OWASP Top 10 for LLM Applications **2025** revision — pin that edition).

## Defining SLOs

- You **MUST** define both quality SLOs and safety SLOs as explicit numeric thresholds before a model reaches production — not "looks good in testing."
- You **MUST** express each SLO against a versioned dataset so a pass/fail is reproducible.
- Safety SLOs **SHOULD** include a hard ceiling (e.g., zero tolerance for secret/PII exfiltration) distinct from soft quality targets you tune over time.
- You **SHOULD NOT** trade a safety SLO for a quality gain; surface the conflict explicitly and decide deliberately.

## Run both gates in CI

- You **MUST** trigger both gates on every change to the model/version, system prompt, tool definitions, retrieval corpus, or guardrail config — any of these can regress behavior.
- You **MUST** treat a model-version bump from a provider as a code change: re-run both gates before rolling it forward, even if the prompt is unchanged.
- You **SHOULD** record each result against the dataset revision and model id so regressions are attributable to a specific change.
- You **SHOULD** keep a held-out set that never informs iteration, so the gate measures generalization, not memorization.

## Red-teaming the safety gate

- You **MUST** seed the safety gate with an adversarial suite (jailbreaks, direct and indirect prompt injection, role-play coercion, encoding tricks) — passing benign inputs proves nothing about resistance.
- You **SHOULD** combine curated known-attack cases with periodic automated/agentic red-teaming; treat any new bypass as a permanent regression case added to the suite.
- You **SHOULD** layer runtime guardrails (input/output filters, allow-lists, tool-permission scoping) as defense-in-depth, and **MUST NOT** treat a guardrail as a substitute for the gate that tests it.

## Tracking regressions over time

- You **MUST** persist per-run gate results so a quality or safety drop is visible as a trend, not discovered by users.
- You **SHOULD** alert on regression across releases, including flakiness regressions (consistency dropping even when best-case quality holds).

> Privacy/PII leakage SLOs here are engineering guidance for measuring and constraining exposure — **not legal advice**. Confirm regulatory obligations (e.g., data-residency, consent) with qualified counsel.

## Adopt-when-measured

Heavy evaluation infrastructure (managed eval platforms, dedicated red-team services, continuous online scoring) is justified **when a measured need warrants it** — scale, regulated risk, or a real incident — not by default (per YAGNI). Start with a small versioned dataset and CI gates; add platform weight when the gate cost or coverage demands it.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Fix deprecated OpenAI evals URL; add NIST AI 600-1 + AI RMF |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
