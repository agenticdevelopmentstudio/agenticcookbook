---
id: cadf17c9-e809-4324-acb3-a430c54a81b4
title: "A/B testing"
domain: agenticdevelopercookbook://guidelines/shipping/ab-testing
type: guideline
version: 1.1.1
status: accepted
language: en
created: 2026-03-27
modified: 2026-04-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Pre-ship A/B test verification: ensure experiment variants are configured, defaults are safe, and the debug panel override works."
platforms: []
tags:
  - ab-testing
  - feature-management
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
triggers:
  - feature-flags
  - logging
---

# A/B testing

Before shipping a feature with experiment support, verify the A/B testing configuration is correct.

## Pre-ship verification

1. **Variant assignment works** — the `ExperimentProvider` interface (`variant(key) -> String`) returns valid variants for all experiment keys used by the feature.
2. **Default variant is safe** — when the experiment provider is unavailable or returns an unknown key, the feature SHOULD fall back to the control (default) variant.
3. **Debug panel override works** — verify the debug panel can force each variant locally for QA testing.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.1 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.1.0 | 2026-04-09 | Mike Fullerton | Tailor for shipping use case — focus on pre-ship experiment verification |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
