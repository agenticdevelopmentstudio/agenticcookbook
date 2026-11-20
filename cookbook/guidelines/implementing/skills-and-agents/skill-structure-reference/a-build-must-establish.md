
- `should-load-reference-content-automatically-only-when-meant-to`: every reference skill meant only to load automatically sets `user-invocable: false`
- `should-disable-model-invocation-for-side-effect-tasks`: every side-effect task skill sets `disable-model-invocation: true`
- `should-keep-skill-md-under-500-lines`: SKILL.md is under 500 lines and detailed content lives in references/
- `should-reference-supporting-files-with-skill-dir`: every supporting-file reference uses `${CLAUDE_SKILL_DIR}`
- `should-use-natural-keywords-in-the-description`: the description contains the keywords users would naturally say
- `must-name-the-main-file-skill-md`: the main file is named exactly `SKILL.md`
- `should-name-supporting-files-lowercase`: every supporting file has a lowercase descriptive name

- `should-follow-skills-directory-layout`: every skill directory follows the `.claude/skills/<name>/SKILL.md` layout, or the code says why not
- `should-set-argument-hint-when-using-arguments`: every skill that uses `$ARGUMENTS` sets `argument-hint`, or the code says why not
