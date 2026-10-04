---
id: 256a827e-436e-4cde-895e-a56b9783edf2
title: "DRY"
domain: agenticdevelopercookbook://principles/dry
type: principle
version: 1.0.0
status: accepted
language: en
created: 2026-04-21
modified: 2026-04-21
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Every piece of knowledge should have a single, authoritative representation. DRY is a rule about knowledge, not about code shape."
platforms: []
tags:
  - dry
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-21"
---

# DRY

Every piece of knowledge — a business rule, a constant, a data schema, a validation — should have a single, unambiguous, authoritative representation in the system. When that knowledge changes, one place updates. DRY is a rule about knowledge, not about code shape: two fragments that look alike but encode different rules are not duplicates, and deduplicating them creates coupling where none existed.

- Ask "does this code encode the same knowledge?" before deduplicating — if two fragments will evolve for different reasons, leave them alone
- When the same fact appears across layers (model, validation, UI copy, tests), consolidate to one source and derive the rest
- Prefer code generation, configuration, or derivation over hand-synchronized copies of the same fact
- If you are unsure whether two fragments represent the same knowledge, duplicate — a coincidental twin is cheaper to split later than a wrong abstraction is to unwind

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-04-21 | Mike Fullerton | Initial creation |
