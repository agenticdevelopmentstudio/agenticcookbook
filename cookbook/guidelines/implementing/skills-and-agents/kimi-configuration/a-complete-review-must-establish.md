
- `must-not-assume-a-home-directory`: whether any code assumes one home directory
- `must-check-the-installed-home-directory`: whether code checks which directory the installed version uses
- `should-accept-a-path-override`: whether every script that touches these paths accepts an override
- `must-keep-the-api-key-in-the-environment`: whether the API key stays in the environment and appears in no checked-in file
- `should-write-agent-neutral-agents-md`: whether each `AGENTS.md` is written as agent-neutral instructions
- `should-place-agents-md-where-it-applies`: whether each `AGENTS.md` is at the root or in the subdirectory it covers
- `must-give-directory-form-skills-a-description`: whether every directory-form skill has `description` in its frontmatter
- `should-prefer-agents-skills`: whether repository skills that other tools can discover are in `.agents/skills/`
- `should-put-repository-skills-under-the-root`: whether repository skills are in `.kimi-code/skills/` or `.agents/skills/` under the repository root
- `should-not-shadow-a-skill-by-accident`: whether any new skill name shadows a lower-priority skill by accident

