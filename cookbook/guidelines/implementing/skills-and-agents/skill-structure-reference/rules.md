
- **should-load-reference-content-automatically-only-when-meant-to**: Reference content SHOULD use `user-invocable: false` if it should only load automatically.
- **should-disable-model-invocation-for-side-effect-tasks**: Task content SHOULD use `disable-model-invocation: true` for side-effect operations.
- **should-keep-skill-md-under-500-lines**: You SHOULD keep SKILL.md under 500 lines; you SHOULD put detailed content in references/
- **should-reference-supporting-files-with-skill-dir**: You SHOULD use `${CLAUDE_SKILL_DIR}` to reference supporting files
- **should-use-natural-keywords-in-the-description**: Description SHOULD use keywords users would naturally say
- **must-name-the-main-file-skill-md**: The main file MUST be named `SKILL.md` (uppercase stem) — Claude Code looks for this exact filename
- **should-name-supporting-files-lowercase**: Supporting files in references/, scripts/, examples/ SHOULD use lowercase descriptive names

