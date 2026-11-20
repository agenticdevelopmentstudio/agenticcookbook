
- `must-build-for-all-target-platforms`: a build log for each target platform shows success
- `must-pass-full-test-suite`: the full-suite test output shows zero failures
- `must-run-platform-linter`: the platform linter's output is clean
- `must-verify-expected-log-messages`: a grep of the run's log output finds each expected message
- `must-audit-accessibility`: an accessibility audit result covers labels, tap target minimums (44pt iOS, 48dp Android) and contrast ratios
- `must-review-against-best-practices`: a best-practices review against the platform references is recorded
- `must-fix-failures-before-complete`: every verification step's latest result is a pass
