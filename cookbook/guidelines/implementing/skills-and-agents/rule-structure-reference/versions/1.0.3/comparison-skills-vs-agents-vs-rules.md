
| Aspect | Skill | Agent | Rule |
|--------|-------|-------|------|
| Format | Directory with `SKILL.md` | Single `.md` with agent frontmatter | Single `.md`, plain markdown |
| Frontmatter | Skill-specific (name, description, allowed-tools, etc.) | Agent-specific (tools, permissionMode, maxTurns, etc.) | None required |
| Invocation | `/command` or auto-invoked | Via Agent tool or `--agent` CLI | Loaded into context passively |
| Execution | Runs as task or reference | Runs as isolated subagent | Shapes behavior of the main session |
| Purpose | Do a specific task | Delegate a specific task | Enforce behavioral constraints |

