---
id: 588b5eae-b70e-4302-a52f-9287265ad03c
title: "Feature flags"
domain: agenticdevelopercookbook://guidelines/planning/feature-management/feature-flags
type: guideline
version: 1.1.1
status: accepted
language: en
created: 2026-03-27
modified: 2026-04-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Plan for feature flag architecture from the start: define a FeatureFlagProvider interface, choose storage backend, and identify which features need gating."
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

Plan for feature flag architecture from the start. All features MUST be gated behind flags from initial implementation.

## Architecture decisions

1. **Interface first** — define a `FeatureFlagProvider` interface (`isEnabled(key) -> Bool`) early. This is a dependency injection boundary — the provider can be swapped without touching feature code.
2. **Local default** — start with a local storage backend (UserDefaults, SharedPreferences, localStorage, JSON config). Plan for a remote backend (LaunchDarkly, Firebase Remote Config, Azure App Configuration) as a later swap via DI.
3. **Flag inventory** — each feature spec SHOULD list its flag keys in a **Feature Flags** section. Plan the flag naming convention upfront (e.g., `feature.auth.biometric`, `feature.editor.markdown`).

## What to gate

- All new user-visible features (default: off in production)
- Major refactors that change behavior (gradual rollout)
- Integrations with external services (kill switch)
- NOT: bug fixes, internal refactors, or non-behavioral changes

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.1 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.1.0 | 2026-04-09 | Mike Fullerton | Tailor for planning use case — focus on architecture decisions |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
