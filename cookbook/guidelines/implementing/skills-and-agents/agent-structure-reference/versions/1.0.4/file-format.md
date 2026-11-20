
Agents are markdown files with YAML frontmatter, placed in `.claude/agents/`.

```
.claude/agents/<agent-name>.md
```

The markdown body serves as the agent's system prompt.

The filename MUST be lowercase kebab-case (e.g., `build-runner.md`). Uppercase stems are reserved for identity files like `SKILL.md` and `CLAUDE.md`.

