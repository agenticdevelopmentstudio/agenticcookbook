
Review Kimi configuration against the rules above.

- `must-not-assume-a-home-directory`: No script hardcodes `~/.kimi` or `~/.kimi-code`; the location is checked or overridable.
- `must-check-the-installed-home-directory`: code that reads or writes the home directory without checking which one the installed version uses.
- `should-accept-a-path-override`: a script touching these paths with no override for the location.
- `must-keep-the-api-key-in-the-environment`: API keys and base URLs come from the environment variables, not from a checked-in file.
- `should-write-agent-neutral-agents-md`: `AGENTS.md` is agent-neutral and placed at the root or in the subdirectory it covers.
- `should-place-agents-md-where-it-applies`: an `AGENTS.md` placed away from the root or the subdirectory it covers.
- `must-give-directory-form-skills-a-description`: Directory-form skills have `name` and `description` in frontmatter.
- `should-prefer-agents-skills`: a repository skill other tools should discover placed in `.kimi-code/skills/` rather than `.agents/skills/`.
- `should-put-repository-skills-under-the-root`: Repository skills are in `.kimi-code/skills/` or `.agents/skills/` under the repository root.
- `should-not-shadow-a-skill-by-accident`: A new skill name does not shadow a skill at a lower priority level by accident.

