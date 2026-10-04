---
id: cf698150-45b0-4a20-881b-7d0f04208198
title: "Support Automation"
domain: agenticdevelopercookbook://principles/support-automation
type: principle
version: 1.0.1
status: accepted
language: en
created: 2026-04-02
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Applications should expose their capabilities through automation interfaces, not just interactive UI."
platforms: []
tags:
  - automation
  - scriptability
  - accessibility
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/platform-integration/shortcuts-and-automation
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
---

# Support Automation

Applications should expose their capabilities through automation interfaces, not just interactive UI. Automation support is a design constraint — not an afterthought — that improves accessibility, testability, and composability.

- Expose core actions through platform automation frameworks (AppIntents, AppActions, UI Automation, APIs) wherever the platform provides them
- Treat the accessibility tree as the automation backbone — scriptability and assistive technology share the same semantic foundation
- Design operations as discrete, composable commands that can be invoked programmatically, not just through clicks and taps
- Provide non-interactive entry points (CLI, URL schemes, intent filters) so workflows and tools can drive the app without a human in the loop

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-09 | Mike Fullerton | Repair stale cross-reference link scheme |
| 1.0.0 | 2026-04-02 | Mike Fullerton | Initial creation |
