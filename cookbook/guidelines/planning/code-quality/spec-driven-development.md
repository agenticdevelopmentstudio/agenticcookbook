---
id: 138eed2b-6b13-40ac-8c99-1f7860420b42
title: "Spec-driven development (plan before code)"
domain: agenticdevelopercookbook://guidelines/planning/code-quality/spec-driven-development
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "For non-trivial agent work, write a self-contained spec before code, separating planning from execution and ending with a verification step."
platforms: []
tags:
  - planning
  - ai-workflow
  - spec
depends-on: []
related:
  - agenticdevelopercookbook://principles/steel-thread-first
  - agenticdevelopercookbook://principles/small-reversible-decisions
  - agenticdevelopercookbook://guidelines/planning/code-quality/scope-discipline
references:
  - https://code.claude.com/docs/en/best-practices
  - https://github.com/github/spec-kit
  - https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - new-module
---

# Spec-driven development (plan before code)

Separate research and planning from execution: produce a written, self-contained spec before any non-trivial change, then implement against it. The spec — not the conversation history or the agent's working memory — is the source of truth. This guards against an agent confidently building the wrong thing.

## When a spec is required

- A non-trivial change **MUST** start from a written spec before code is generated. "Non-trivial" means: the approach is uncertain, the change touches multiple files, or the agent is unfamiliar with the code being modified.
- If you can describe the diff in one sentence (a typo, a log line, a rename), you **SHOULD** skip the spec and do the work directly. Right-size the ceremony to the change.
- Planning and implementation **SHOULD** run in distinct phases so research context does not bleed into and bias execution.

## What a good spec contains

A spec **MUST** be self-contained — readable and executable in a fresh session with no prior context. It **MUST** include:

| Section | Requirement |
|---------|-------------|
| Goal | One or two sentences stating the "what" and "why" — not the "how". |
| Files & interfaces | Name the concrete files, functions, and interfaces to add or change. |
| Out of scope | An explicit list of what this change will **NOT** touch. This is the highest-signal section for keeping an agent on task. |
| Verification | An end-to-end check that proves the feature works (test command, build, script, or screenshot diff). |

- The spec **SHOULD** reference existing patterns to follow ("model X on the existing Y") rather than inviting a from-scratch design.
- The spec **MUST NOT** be discarded once coding starts; it is the artifact the implementation is reviewed against.

## A staged flow (name the method, not the tool)

A common shape is **Spec -> Plan -> Tasks -> Implement -> Verify**: the spec captures requirements, the plan captures the technical approach, tasks break it into ordered units, then implementation executes against the spec.

- Adopt the *methodology*; do **NOT** hard-code a specific tool, command set, or vendor flow into your process. Spec-driven tooling (e.g. plan modes, spec-kit-style scaffolds) churns fast — names and commands change between releases. The durable practice is "write the spec first, separate planning from execution, verify at the end."
- For larger features, the agent **MAY** interview the human first to surface edge cases and tradeoffs, then write the spec, then start a fresh session to implement against it with clean context.

## Verification

- Implementation **MUST** end by running the spec's verification step and showing the evidence (command output, passing tests, or screenshot), not merely asserting success.
- An independent reviewer (a fresh context or subagent) **SHOULD** check the diff against the spec: every requirement implemented, listed edge cases covered, and nothing outside the stated scope changed.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add recovered Tier-1 research sources (adversarially-audited) |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
