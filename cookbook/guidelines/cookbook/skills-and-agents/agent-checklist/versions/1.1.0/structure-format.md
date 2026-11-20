
| ID  | Criterion | How to check | Severity |
|-----|-----------|-------------|----------|
| S01 | YAML frontmatter present | File starts with `---`, has closing `---` | FAIL |
| S02 | `name` field present | Frontmatter contains `name:` | WARN |
| S03 | `name` is kebab-case, lowercase, ≤64 chars | Regex: `^[a-z][a-z0-9-]{0,63}$` | FAIL |
| S04 | `description` field present | Frontmatter contains `description:` | FAIL |
| S05 | Description uses natural trigger keywords | Description includes phrases users would say; not too vague or too narrow | WARN |
| S11 | Correct file location | Agent is in `.claude/agents/` or `~/.claude/agents/` | WARN |
| S12 | Only recognized frontmatter fields | Check against known fields: name, description, tools, disallowedTools, model, permissionMode, maxTurns, skills, mcpServers, hooks, memory, background, effort, isolation | WARN |
| S13 | Filename is lowercase kebab-case | Filename matches `^[a-z][a-z0-9-]*\.md$`; UPPERCASE stems are reserved for identity files like `SKILL.md` and `CLAUDE.md` | WARN |

---

