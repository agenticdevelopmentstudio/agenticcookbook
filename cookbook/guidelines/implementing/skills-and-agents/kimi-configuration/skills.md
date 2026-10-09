
- Priority is Project, then User, then Extra, then Built-in. A higher level shadows a lower one of the same name.
- Project skills live in `.kimi-code/skills/` or `.agents/skills/`, relative to the nearest directory containing `.git`. User skills live in `$KIMI_CODE_HOME/skills/` and `~/.agents/skills/`. Extra directories are listed in `extra_skill_dirs` in `config.toml`.
- In a skill directory `name/SKILL.md` wins over `name.md`. Frontmatter fields are `name`, `description` (required for the directory form), `type` (`prompt`, `inline` or `flow`), `whenToUse`, `disableModelInvocation` and `arguments`.
- Invoke a skill with `/skill:<name> args`.
- Prefer `.agents/skills/` for a repository skill that other tools can also discover.

