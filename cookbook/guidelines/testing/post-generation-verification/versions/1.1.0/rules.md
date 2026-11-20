
- **must-build-for-all-target-platforms**: Every generated artifact MUST be verified by a **Build**: compile for all target platforms (`xcodebuild`, `./gradlew build`, `npm run build`, `dotnet build`).
- **must-pass-full-test-suite**: Every generated artifact MUST be verified by a **Test** step: run the full test suite — all tests MUST pass.
- **must-run-platform-linter**: Every generated artifact MUST be verified by **Lint**: run the platform linter (see [adc.guideline.implementing.code-quality.linting](cookbook:775da457-30c7-47de-b179-0fae8a8b779d)).
- **must-verify-expected-log-messages**: Every generated artifact MUST be verified by **Log verification**: build, run, and grep for expected log messages from the Logging section.
- **must-audit-accessibility**: Every generated artifact MUST be verified by an **Accessibility audit**: verify VoiceOver/TalkBack labels, tap target minimums (44pt iOS, 48dp Android), contrast ratios.
- **must-review-against-best-practices**: Every generated artifact MUST be verified by a **Code review against best practices**: check against platform best practices references.
- **must-fix-failures-before-complete**: If any step fails, the issue MUST be fixed before considering the work complete.
