---
id: 39c2d053-006f-42c9-9db4-d991c1688024
title: "Idempotency"
domain: agenticdevelopercookbook://principles/idempotency
type: principle
version: 1.0.1
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "User actions and system operations should be safe to repeat without duplicate side effects: debounce async actions, use idempotency keys, and check current state before transitions."
platforms: []
tags:
  - idempotency
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
---

# Idempotency

User actions and system operations should be safe to repeat without duplicate side effects:

- Debounce or disable buttons during async operations
- Use idempotency keys for API calls with side effects
- Database migrations must be safe to run multiple times
- Check current state before applying state transitions

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-10-04 | Mike Fullerton | Complete the summary, which was cut off |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
