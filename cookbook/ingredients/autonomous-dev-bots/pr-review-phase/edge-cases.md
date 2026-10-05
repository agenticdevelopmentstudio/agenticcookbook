
- **Non-recipe files**: Guidelines and principles still get Phase 1 checks against their own type's format.
- **Fix loop oscillation**: If a fix in one iteration reintroduces an issue fixed in a previous one, the loop MUST stop and flag the issue rather than continue to the iteration cap.
- **Tool unavailable**: If `vale` or `markdownlint-cli2` is not installed, the phase MUST fail with a reported error rather than silently skipping the check.

