---
id: 9250b0f3-b101-422b-8d40-9596493ef3b5
title: "Trigger Guide"
domain: agenticdevelopercookbook://introduction/trigger-guide
type: reference
version: 1.0.0
status: draft
language: en
created: 2026-04-09
modified: 2026-04-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Activity-based trigger system for filtering guidelines by what an AI agent is currently doing."
platforms: []
tags:
  - triggers
  - agent-workflow
  - guidelines
depends-on:
  - agenticdevelopercookbook://introduction/conventions
related: []
references: []
approved-by: ""
approved-date: ""
---

# Trigger Guide

Activity-based trigger system for filtering guidelines by what an AI agent is currently doing. Instead of loading all 240 guidelines into context, agents query by activity to get the 10-20 that matter right now.

## Purpose

The cookbook has 240 guidelines across 16 categories. Principles (27 items) are small and universal — they fit in agent context. Guidelines are the opposite: numerous, specific, and most are irrelevant to any given task. Loading all of them wastes context and dilutes signal.

Triggers solve this. Each guideline declares the activities where it's relevant. An agent about to write tests queries `writing-tests` and gets ~12 guidelines instead of 240.

## Canonical Triggers

| Trigger | When It Fires | Example Guidelines |
|---------|--------------|-------------------|
| `writing-tests` | Writing or modifying tests | test-pyramid, unit-test-patterns, properties-of-good-tests |
| `error-handling` | Adding try/except, catch, error paths | error-responses, retry-and-resilience, feedback-patterns |
| `new-module` | Creating a new file, module, or package | linting, scope-discipline, api-design |
| `api-integration` | Calling external APIs (REST, GraphQL, gRPC) | input-validation, cors, timeouts, rate-limiting |
| `ai-api-integration` | Calling AI/ML provider APIs specifically | ai-provider-observability, ai-cost-management |
| `data-modeling` | Defining types, schemas, database tables | concurrency, immutability, privacy |
| `database-operations` | Writing queries, migrations, transactions | sqlite-best-practices, indexing, query-optimization |
| `ui-implementation` | Building UI components or layouts | layout, color, typography, accessibility |
| `authentication` | Implementing auth flows, tokens, sessions | authentication, authorization, token-handling |
| `input-handling` | Processing user input, form data, file uploads | input-validation, form-design |
| `networking` | HTTP clients, WebSockets, retry logic, caching | caching, retry-and-resilience, timeouts, transport-security |
| `concurrency` | Threads, async/await, locks, queues | concurrency, immutability, background-tasks |
| `logging` | Adding log statements, analytics events | logging, analytics, sensitive-data |
| `security-review` | Reviewing code for security concerns | authentication, input-validation, secure-storage, privacy |
| `performance-optimization` | Optimizing hot paths, queries, rendering | caching, indexing, query-optimization, concurrency |
| `accessibility` | Screen readers, keyboard nav, contrast, Dynamic Type | accessibility, animation-motion, touch-click-targets |
| `internationalization` | Localization, RTL, locale formatting | localization, rtl-support |
| `feature-flags` | Adding or managing feature flags | feature-flags, ab-testing, debug-mode |
| `platform-integration` | Deep links, notifications, widgets, sharing | deep-linking, notifications, widgets-and-glanceable-surfaces |
| `code-review` | Reviewing code quality, structure, patterns | scope-discipline, properties-of-good-tests, post-generation-verification |
| `pre-commit` | Final check before committing code | linting, atomic-commits, bulk-operation-verification |
| `pre-pr` | Final check before opening a pull request | test-pyramid, flaky-test-prevention, accessibility, security-headers-checklist |
| `dependency-management` | Adding, updating, or auditing dependencies | dependency-security, no-external-dependencies-in-core-librari |
| `configuration` | App settings, environment config, build config | deep-linking, shortcuts-and-automation, backup-and-recovery |
| `offline-support` | Offline-first patterns, sync, conflict resolution | offline-and-connectivity, sync-engine-design, conflict-resolution |
| `skill-authoring` | Writing Claude Code skills, rules, or agents | authoring-skills-and-rules, skill-checklist, agent-checklist |
| `recipe-authoring` | Writing or modifying cookbook recipes | recipe-quality guidelines |
| `schema-design` | Designing database schemas, migrations | sqlite-best-practices, schema-evolution, sync-schema-design |

## Usage Pattern for AI Agents

### Escalating checkpoint pattern

The most effective usage is graduated — lightweight guardrails during active work, thorough review at natural checkpoints:

1. **Principles** — always loaded into context. Small (27 items), universal, load-bearing. These are the foundation that applies to every task.

2. **Trigger-filtered guidelines** — loaded on demand based on current activity. When an agent is about to write tests, it queries `writing-tests` and gets ~12 specific testing guidelines. When it's about to call an API, it queries `api-integration` and gets the relevant networking and security guidelines.

3. **Pre-commit checklist** — a small mandatory set (~10 rules) triggered by `pre-commit`. Checked before every commit. Fast, focused, catches common issues.

4. **Pre-PR audit** — a broader set triggered by `pre-pr`. Checked once before opening a pull request. More thorough, covers testing completeness, accessibility, security headers.

The cost of checking is proportional to the stakes of the action.

### Querying triggers

The trigger index lives at `index/triggers.yaml` (generated by `cookbook update`). Structure:

```yaml
writing-tests:
  - guidelines/testing/flaky-test-prevention.md
  - guidelines/testing/properties-of-good-tests.md
  - guidelines/testing/test-data.md
  - guidelines/testing/test-doubles.md
  - guidelines/testing/test-pyramid.md
  - guidelines/testing/testing.md
  - guidelines/testing/the-testing-workflow.md
  - guidelines/testing/unit-test-patterns.md
```

An agent can query multiple triggers at once. The union of results gives the full set of relevant guidelines:

```
Activity: "add a new provider that calls an external API"
Triggers: api-integration + new-module + error-handling
Result: ~15 relevant guidelines
```

### Regenerating the index

After adding or modifying guideline triggers, regenerate:

```bash
cookbook update
```

The index is a generated artifact — do not edit it manually.

## Adding Triggers to a Guideline

Add a `triggers` field to the guideline's YAML frontmatter, after `approved-date`:

```yaml
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
triggers:
  - writing-tests
  - code-review
```

Rules:
- Use 1-5 triggers per guideline. More than 5 means the guideline is too broad or the triggers are too granular.
- Use only values from the canonical trigger table above.
- If a new trigger is needed, add it to this document first, then use it.
- Order triggers from most specific to least specific.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-04-09 | Mike Fullerton | Initial creation |
