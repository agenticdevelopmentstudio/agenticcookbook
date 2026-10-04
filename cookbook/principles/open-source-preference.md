---
id: 495000e6-a1fc-4b43-8999-23089505559c
title: "For novel components, prefer proven open-source solutions"
domain: agenticdevelopercookbook://principles/open-source-preference
type: principle
version: 1.1.1
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "When no native solution exists, research battle-tested open-source libraries and present options to the user before building a custom solution, which should be a deliberate choice."
platforms: []
tags:
  - open-source-preference
depends-on: []
related:
  - agenticdevelopercookbook://principles/native-controls
  - agenticdevelopercookbook://principles/dry
  - agenticdevelopercookbook://guidelines/planning/code-quality/reuse-before-build
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
---

# For novel components, prefer proven open-source solutions

When no native solution exists, research battle-tested open-source libraries and present options to the user before building a custom solution. A custom implementation can always be chosen instead, but it should be a deliberate decision, not a default.

- Before reaching outward, check what you already have: the platform's standard library and the dependencies already in the project often solve the problem — prefer those before adding anything new
- Evaluate candidates by maintenance activity, license compatibility, and community adoption before recommending
- Verify a candidate is real before adopting it: confirm the package actually exists, is actively maintained, and is widely used. Never install a package name an AI suggested without verifying it — hallucinated and typosquatted names are a live supply-chain risk
- Present at least two options with trade-offs rather than silently picking one
- If building custom, document why the available open-source options were rejected

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.1 | 2026-10-04 | Mike Fullerton | Complete the summary, which was cut off |
| 1.1.0 | 2026-06-09 | Mike Fullerton | Add check-what-you-have-first and verify-the-package-is-real (anti-slopsquatting); link reuse-before-build |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
