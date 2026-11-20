
- **must-not-assume-a-home-directory**: Code MUST NOT assume one home directory.
- **must-check-the-installed-home-directory**: Code MUST check which directory the installed version uses.
- **should-accept-a-path-override**: Scripts that touch these paths SHOULD accept an override rather than hardcoding either.
- **must-keep-the-api-key-in-the-environment**: The API key MUST stay in the environment and MUST NOT appear in a checked-in file.
- **should-write-agent-neutral-agents-md**: `AGENTS.md` SHOULD be written as agent-neutral instructions so other tools can share it.
- **should-place-agents-md-where-it-applies**: `AGENTS.md` SHOULD be placed at the root or in the subdirectory it covers.
- **must-give-directory-form-skills-a-description**: `description` MUST be present in the frontmatter for the directory form.
- **should-prefer-agents-skills**: `.agents/skills/` SHOULD be preferred for a repository skill that other tools can also discover.
- **should-put-repository-skills-under-the-root**: Repository skills SHOULD be in `.kimi-code/skills/` or `.agents/skills/` under the repository root.
- **should-not-shadow-a-skill-by-accident**: A new skill name SHOULD NOT shadow a skill at a lower priority level by accident.

