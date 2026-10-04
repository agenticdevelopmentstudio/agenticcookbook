
# Post-generation verification

Every generated artifact MUST be verified:

1. **Build**: Compile for all target platforms (`xcodebuild`, `./gradlew build`, `npm run build`, `dotnet build`)
2. **Test**: Run the full test suite — all tests MUST pass
3. **Lint**: Run the platform linter (see agenticdevelopercookbook://guidelines/implementing/code-quality/linting)
4. **Log verification**: Build, run, and grep for expected log messages from the Logging section
5. **Accessibility audit**: Verify VoiceOver/TalkBack labels, tap target minimums (44pt iOS, 48dp Android), contrast ratios
6. **Code review against best practices**: Check against platform best practices references

If any step fails, the issue MUST be fixed before considering the work complete.

