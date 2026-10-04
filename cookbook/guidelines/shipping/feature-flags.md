---
id: 1b259fdc-1aba-48c5-a89a-b9ca01dc3351
title: "Feature flags"
domain: agenticdevelopercookbook://guidelines/shipping/feature-flags
type: guideline
version: 1.1.1
status: accepted
language: en
created: 2026-03-27
modified: 2026-04-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Pre-ship feature flag verification: ensure all new features are gated, defaults are correct, and flag keys are documented."
platforms:
  - csharp
  - kotlin
  - swift
  - typescript
tags:
  - feature-flags
  - feature-management
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
triggers:
  - feature-flags
  - new-module
---

# Feature flags

Before shipping, verify that all new features are properly gated behind feature flags and that flag configuration is correct.

## Pre-ship verification checklist

1. **Every new feature is gated** — no new user-visible behavior should ship without a feature flag. Verify by searching for UI or behavior changes that lack a flag check.
2. **Defaults are correct** — new features SHOULD default to `false` (disabled) in production. Verify the default value in the `FeatureFlagProvider` implementation.
3. **Flag keys are documented** — each feature spec SHOULD list its flag keys in a **Feature Flags** section. Verify the keys match between the spec and the code.
4. **Kill switch works** — for critical features, verify the flag can be toggled off remotely (or via local config) without a code deploy.
5. **No flag leaks** — features behind a disabled flag MUST NOT be visible in the UI, accessible via deep links, or discoverable through the API.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.1 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.1.0 | 2026-04-09 | Mike Fullerton | Tailor for shipping use case — focus on pre-ship flag verification |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
