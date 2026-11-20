
- `must-name-agent-files-lowercase-kebab-case`: the name of each file under `.claude/agents/` — a lowercase kebab-case stem keeps the rule, an uppercase or mixed-case stem breaks it
- `must-not-combine-tools-and-disallowed-tools`: each agent's frontmatter — `tools` or `disallowedTools` alone keeps the rule, both set together breaks it
- `should-keep-system-prompt-focused-and-unambiguous`: an agent body that spreads over several jobs or can be read more than one way

