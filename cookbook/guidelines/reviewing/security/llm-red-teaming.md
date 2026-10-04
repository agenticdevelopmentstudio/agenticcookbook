---
id: 709aabb0-c305-4a23-8748-9f57c5bbe93d
title: "LLM red teaming"
domain: agenticdevelopercookbook://guidelines/reviewing/security/llm-red-teaming
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Adversarially test LLM and agent systems against the OWASP LLM Top 10 and gate releases on a tracked attack-success-rate threshold."
platforms: []
tags:
  - ai
  - security
  - red-team
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/security/agent-guardrails
  - agenticdevelopercookbook://guidelines/implementing/security/llm-application-security
references:
  - https://genai.owasp.org/llm-top-10/
  - https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/
  - https://arxiv.org/abs/2302.12173
  - https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - security-review
---

# LLM red teaming

Adversarially test LLM and agent systems before and after release, mapping findings to the OWASP Top 10 for LLM Applications (v2025, dated 2024-11-14). You **MUST** red-team against prompt injection and jailbreaks, and you **SHOULD** gate releases on a tracked attack-success-rate threshold.

## What to attack (OWASP LLM Top 10, v2025)

Cover, at minimum, these attack classes:

| Attack class | OWASP ref | What you are probing |
|---|---|---|
| Direct prompt injection | LLM01 | User input overrides system instructions |
| Indirect prompt injection | LLM01 | Hidden instructions in retrieved docs, web pages, or tool output |
| Jailbreaks | LLM01 | Role-play, encoding, and refusal-bypass to elicit blocked behavior |
| Sensitive info disclosure | LLM02 | Training-data, secret, or PII exfiltration |
| Improper output handling | LLM05 | Model output that triggers XSS, SQLi, or command injection downstream |
| Excessive agency / tool abuse | LLM06 | Unintended tool calls, privilege escalation, destructive actions |
| System-prompt leakage | LLM07 | Extraction of the system prompt or embedded policy/secrets |

- Indirect prompt injection (poisoned RAG content, tool results, file contents) is the highest-leverage agent attack and **MUST** be tested explicitly, not just direct user-input injection.
- Excessive agency tests **MUST** verify that the agent cannot exceed its least-privilege tool and permission scope, even when instructed to.

## How to run it

- You **MUST** use a maintained, versioned attack suite (e.g., an OWASP-mapped open-source red-team framework) and **MUST** pin the suite version per run so results are reproducible.
- You **SHOULD** run automated red-team evaluations in CI on every change to prompts, tools, models, or RAG sources — these are silent regression surfaces.
- You **SHOULD** combine automated probes with periodic manual/expert red teaming; novel jailbreaks rarely appear first in automated corpora.
- You **MUST** test the deployed configuration (system prompt, guardrails, tool wiring), not the bare model — guardrails are part of the system under test.
- You **SHOULD** re-run the suite after every model or provider version bump; behavior and refusal boundaries shift across versions.

## Release gating

- Define an **attack-success rate (ASR)** per attack class: fraction of adversarial prompts that achieve their objective.
- You **SHOULD** set an explicit ASR threshold (e.g., a hard ceiling for injection/jailbreak success) as a release gate, and **MUST** block release when a critical class exceeds it.
- You **MUST** track ASR over time and treat a regression as a release blocker, not a backlog item.
- You **SHOULD** record each finding with a reproducer, OWASP mapping, and severity so fixes are verifiable.

## Guardrails

- Red teaming reduces but never eliminates injection risk. Treat all model output as untrusted: enforce least-privilege tools, human-in-the-loop for destructive actions, and output validation downstream (defense in depth).
- Forecast: the OWASP LLM Top 10 is revised periodically; pin to a dated revision and re-baseline your suite when a new revision lands.
- Privacy/exfiltration tests are engineering guidance, not legal advice; consult counsel for regulated-data obligations.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add OWASP 2025 dated page, indirect-prompt-injection paper, NIST AI 600-1 |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
