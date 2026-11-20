
- `must-build-for-all-target-platforms`: a generated artifact built for only some of its target platforms, or not built at all
- `must-pass-full-test-suite`: a partial test run, or any failing test, behind generated work
- `must-run-platform-linter`: generated code with no platform linter run, or with lint findings left
- `must-verify-expected-log-messages`: no run that greps for the expected log messages from the Logging section
- `must-audit-accessibility`: missing VoiceOver/TalkBack labels, tap targets under 44pt iOS or 48dp Android, or unchecked contrast ratios
- `must-review-against-best-practices`: generated code never checked against the platform best practices references
- `must-fix-failures-before-complete`: work called complete while any verification step still fails
