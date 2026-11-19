
- Keep SKILL.md under 500 lines; put detailed content in references/
- Use `${CLAUDE_SKILL_DIR}` to reference supporting files
- Description should use keywords users would naturally say
- Skill descriptions are loaded into context to help Claude decide what's available
- Full skill content only loads when invoked
- The main file MUST be named `SKILL.md` (uppercase stem) — Claude Code looks for this exact filename
- Supporting files in references/, scripts/, examples/ should use lowercase descriptive names

