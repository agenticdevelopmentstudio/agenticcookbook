
| Aspect | Skill | Agent | Rule |
|--------|-------|-------|------|
| Location | `.claude/skills/` | `.claude/agents/` | `rules/`, `.claude/`, or referenced |
| Format | Directory with `SKILL.md` | Single `.md` file | Single `.md`, plain markdown |
| Execution | Runs in current context (or fork) | Always runs as subagent | Loaded into context passively |
| Context | Shares parent context (unless forked) | Isolated context | Shapes main session |
| Tool access | `allowed-tools` in frontmatter | `tools` / `disallowedTools` | N/A |
| Invocation | Auto or `/command` | Via Agent tool or CLI `--agent` | Passive |
| State | No persistent state | Can have `memory` scope | N/A |

