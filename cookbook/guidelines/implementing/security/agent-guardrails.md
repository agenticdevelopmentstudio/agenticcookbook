---
id: af911b49-ff36-439e-acb0-a08c80b87103
title: "Agent guardrails"
domain: agenticdevelopercookbook://guidelines/implementing/security/agent-guardrails
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Wrap agents in deterministic input/output guardrails, least-privilege tool access, human confirmation for irreversible actions, and a kill switch."
platforms: []
tags:
  - ai
  - safety
  - guardrails
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/security/llm-application-security
  - agenticdevelopercookbook://guidelines/testing/agent-evaluation-and-safety
references:
  - https://genai.owasp.org/llm-top-10/
  - https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/
  - https://www.anthropic.com/research/building-effective-agents
  - https://modelcontextprotocol.io/specification/2025-06-18
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - ai-api-integration
  - security-review
---

# Agent guardrails

Guardrails are the runtime controls that sit around an agent or LLM and constrain what enters, what leaves, and what the agent is allowed to do. They **MUST** be enforced as deterministic code, not as prompt instructions alone — a model can always be talked out of following its own prompt (OWASP LLM01:2025 Prompt Injection).

## Input guardrails

Validate and moderate everything reaching the model.

- **off-band-input**: The system **MUST** screen input for prompt injection, jailbreaks, off-topic requests, and unsafe content before it reaches the model.
- **untrusted-context**: Content from tools, retrieval, files, or other users **MUST** be treated as untrusted and labeled as data, never merged into the instruction channel.
- **layered-defense**: Input checks **SHOULD** combine cheap deterministic rules (length, encoding, allow-listed topics) with a moderation/classifier pass; prompt-level instructions **MAY** supplement but **MUST NOT** be the only defense.

## Output guardrails

Treat all model output as untrusted until it has passed checks (see `agenticdevelopercookbook://guidelines/implementing/security/llm-application-security`).

- **deterministic-output-checks**: Output guardrails **MUST** be enforced deterministically — schema/JSON validation, PII and secret detection, and unsafe-content moderation run in code, not by asking the model to self-certify.
- **schema-conformance**: Structured output **MUST** be parsed and validated against an explicit schema; non-conforming output **MUST** be rejected or repaired, never passed downstream verbatim.
- **no-leakage**: Output **MUST** be scanned for PII, credentials, and system-prompt leakage (OWASP LLM02:2025, LLM07:2025) before it is returned or persisted.

## Tool agency

Constrain agency to the minimum required (OWASP LLM06:2025 Excessive Agency).

- **allow-list-tools**: The agent **MUST** be limited to an explicit allow-list of tools; tool guardrails **MUST** be enforced deterministically at the call boundary.
- **least-privilege**: Each tool **MUST** run with the narrowest scopes, credentials, and data access needed — no shared admin tokens.
- **human-in-the-loop**: High-impact or irreversible actions (payments, deletes, external sends, infra changes) **MUST** require explicit human confirmation before execution.
- **caps**: Spending, rate, and iteration caps **MUST** bound tool use to prevent runaway loops and unbounded consumption (OWASP LLM10:2025).

## Stop controls

- **kill-switch**: A kill switch that halts the agent and revokes its tool access **MUST** exist and be reachable by operators.
- **circuit-breakers**: Repeated failures, guardrail trips, or anomalous cost/rate **SHOULD** trip a circuit breaker that pauses the agent and alerts.
- **audit-trail**: Inputs, tool calls, confirmations, and guardrail decisions **SHOULD** be logged for after-the-fact review.

## Guardrail placement

| Stage | Enforce deterministically | Confirm with human |
|-------|---------------------------|--------------------|
| Input | injection/topic/safety filter | no |
| Tool call | allow-list, scope, caps | high-impact / irreversible only |
| Output | schema, PII/secret, moderation | no |

> Privacy and PII handling here is engineering guidance, not legal advice; confirm obligations with counsel. Heavy controls (managed moderation services, dedicated policy engines, sidecar enforcement) are adopt-when-measured-need-justifies per YAGNI — start with in-process deterministic checks.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add OWASP 2025 dated page, Anthropic agents, MCP spec sources |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
