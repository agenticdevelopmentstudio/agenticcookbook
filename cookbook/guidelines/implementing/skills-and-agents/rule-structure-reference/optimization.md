
Rules in `.claude/rules/` are injected into the system prompt on **every turn** of a conversation — every user message, every tool call, every response. This makes per-turn size the most important optimization target.

### Per-Turn vs Per-Session Cost

- **Per-turn (always-on):** Content in the rule file itself. Paid on every turn.
- **Per-session (on-demand):** External files read via tool calls during the conversation. Paid once when read.

### Reasons

- `should-name-rule-files-lowercase-kebab-case`: Uppercase stems are reserved for identity files that Claude Code looks up by exact name (`SKILL.md`, `CLAUDE.md`).
- `should-not-duplicate-across-rules`: Two rules covering the same concept means Claude processes it twice per turn.
- `should-avoid-mandatory-multi-file-reads`: Rules that require reading 6+ files before any work begins create high entry cost.

