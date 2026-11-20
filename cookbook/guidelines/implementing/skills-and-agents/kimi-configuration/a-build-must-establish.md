
- `must-not-assume-a-home-directory`: no code hardcodes one home directory
- `must-check-the-installed-home-directory`: the code determines which directory the installed version uses
- `should-accept-a-path-override`: every script touching these paths accepts an override for the location
- `must-keep-the-api-key-in-the-environment`: the API key is read from the environment and no checked-in file contains it
- `should-write-agent-neutral-agents-md`: every `AGENTS.md` is agent-neutral
- `should-place-agents-md-where-it-applies`: every `AGENTS.md` is at the root or in the subdirectory it covers
- `must-give-directory-form-skills-a-description`: every directory-form skill's frontmatter has `description`
- `should-prefer-agents-skills`: shared repository skills are in `.agents/skills/`
- `should-put-repository-skills-under-the-root`: every repository skill is in `.kimi-code/skills/` or `.agents/skills/` under the repository root
- `should-not-shadow-a-skill-by-accident`: every new skill name that shadows a lower-priority skill does so on purpose

