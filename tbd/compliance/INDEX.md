---
id: 0E83CCE2-6343-4E54-B125-86D58EB9AE45
title: "Compliance"
domain: agenticdevelopercookbook://compliance/INDEX
type: reference
version: 1.1.0
status: draft
language: en
created: 2026-03-28
modified: 2026-03-28
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Index of all compliance categories and their checks."
platforms: []
tags:
  - compliance
  - index
depends-on: []
related: []
references: []
---

# Compliance

Compliance checks are curated indexes of guideline-derived requirements, grouped by concern. Each recipe and guideline includes a Compliance section listing the checks that were evaluated and their status.

## Architecture

```
Recipes/Guidelines  →  Compliance Checks  →  Guidelines  →  External Standards
(results)              (curated indexes)      (guidance)       (OWASP, WCAG, etc.)
```

- **Compliance checks** group and distill guidelines into named, checkable items
- **Guidelines** contain the detailed guidance and reference external standards
- Each check links back to its source guideline(s)
- Only applicable checks are listed in each item's Compliance section

## Categories

| Category | File | Checks | Scope |
|----------|------|--------|-------|
| Security | [security.md](security.md) | 12 | Auth, storage, input, transport, logging, dependencies |
| User Safety | [user-safety.md](user-safety.md) | 6 | Content moderation, age-gating, abuse prevention |
| Performance | [performance.md](performance.md) | 8 | Render time, animation, resources, caching |
| Best Practices | [best-practices.md](best-practices.md) | 8 | Testing, linting, error handling, code quality |
| Access Patterns | [access-patterns.md](access-patterns.md) | 8 | Client-server, offline, retry, pagination |
| Accessibility | [accessibility.md](accessibility.md) | 8 | Screen readers, keyboard, contrast, motion |
| Privacy & Data | [privacy-and-data.md](privacy-and-data.md) | 8 | Collection, storage, retention, consent |
| Platform Compliance | [platform-compliance.md](platform-compliance.md) | 8 | App Store, Google Play, design language |
| Reliability | [reliability.md](reliability.md) | 8 | Error recovery, degradation, state, idempotency |
| Internationalization | [internationalization.md](internationalization.md) | 7 | Strings, RTL, locale formatting, Unicode |
| Artifact Formatting | [artifact-formatting/INDEX.md](artifact-formatting/INDEX.md) | 55 | Required structure for principles (7), guidelines (8), ingredients (16), recipes (14), cookbooks (10) |

## Per-Item Compliance Section Format

Each recipe or guideline includes a `## Compliance` section listing evaluated checks:

| Check | Status | Category |
|-------|--------|----------|
| [secure-log-output](security.md#secure-log-output) | passed | Security |
| [keyboard-navigable](accessibility.md#keyboard-navigable) | passed | Accessibility |

- Only applicable checks are listed (omit entire categories that don't apply)
- Status values: `passed`, `failed`, `partial`
- Each check name links to its definition

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.0 | 2026-04-04 | Mike Fullerton | Add Artifact Formatting category |
| 1.0.0 | 2026-03-28 | Mike Fullerton | Initial creation |
