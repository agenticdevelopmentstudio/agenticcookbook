---
id: 563aebde-52bf-4011-8907-ecc473fd942c
title: "Post-generation verification"
domain: agenticdevelopercookbook://guidelines/testing/post-generation-verification
type: guideline
version: 1.0.4
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Verify every generated artifact: build for all target platforms, run the full test suite, lint, check log output, audit accessibility, and review against platform best practices."
platforms:
  - ios
  - kotlin
  - typescript
tags:
  - post-generation-verification
  - testing
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/code-quality/linting
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - pre-commit
  - code-review
---

# Post-generation verification

Every generated artifact MUST be verified:

1. **Build**: Compile for all target platforms (`xcodebuild`, `./gradlew build`, `npm run build`, `dotnet build`)
2. **Test**: Run the full test suite — all tests MUST pass
3. **Lint**: Run the platform linter (see agenticdevelopercookbook://guidelines/implementing/code-quality/linting)
4. **Log verification**: Build, run, and grep for expected log messages from the Logging section
5. **Accessibility audit**: Verify VoiceOver/TalkBack labels, tap target minimums (44pt iOS, 48dp Android), contrast ratios
6. **Code review against best practices**: Check against platform best practices references

If any step fails, the issue MUST be fixed before considering the work complete.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.4 | 2026-10-04 | Mike Fullerton | Complete the summary, which was cut off |
| 1.0.3 | 2026-06-09 | Mike Fullerton | Repair stale cross-reference link scheme |
| 1.0.2 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
