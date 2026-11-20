
- `should-load-reference-content-automatically-only-when-meant-to`: a reference-content skill meant only to load automatically that lacks `user-invocable: false`
- `should-disable-model-invocation-for-side-effect-tasks`: a task skill with side effects that lacks `disable-model-invocation: true`
- `should-keep-skill-md-under-500-lines`: a SKILL.md of 500 lines or more, or detailed content kept in it rather than references/
- `should-reference-supporting-files-with-skill-dir`: a supporting file referenced by a path not built on `${CLAUDE_SKILL_DIR}`
- `should-use-natural-keywords-in-the-description`: a description without the keywords users would naturally say
- `must-name-the-main-file-skill-md`: a main skill file named anything other than `SKILL.md`
- `should-name-supporting-files-lowercase`: a file in references/, scripts/ or examples/ whose name is not lowercase and descriptive

- `should-follow-skills-directory-layout`: a skill directory that does not follow the `.claude/skills/<name>/SKILL.md` layout
- `should-set-argument-hint-when-using-arguments`: a skill that uses `$ARGUMENTS` without an `argument-hint`
