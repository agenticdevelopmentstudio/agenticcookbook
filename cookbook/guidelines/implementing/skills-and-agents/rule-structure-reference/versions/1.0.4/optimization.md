
Rules in `.claude/rules/` are injected into the system prompt on **every turn** of a conversation — every user message, every tool call, every response. This makes per-turn size the most important optimization target.

### Per-Turn vs Per-Session Cost

- **Per-turn (always-on):** Content in the rule file itself. Paid on every turn. Keep this minimal.
- **Per-session (on-demand):** External files read via tool calls during the conversation. Paid once when read. Use this for large reference material.

### Key Guidelines

1. **Target under 200 lines / ~8KB** per rule file. If larger, move content to skills or external references.
2. **Inline small, reference large.** A 5-line summary table belongs in the rule. A 200-line guideline belongs in an external file read on demand.
3. **Don't duplicate across rules.** Two rules covering the same concept means Claude processes it twice per turn.
4. **Use `globs` frontmatter** for rules that only apply to specific file patterns (e.g., `globs: .claude/**`).
5. **Deduplicate MUST NOTs.** Each item should add a unique constraint not stated elsewhere in the body.
6. **Avoid mandatory multi-file reads.** Rules that require reading 6+ files before any work begins create high entry cost. Prefer summaries, on-demand reads, or iterative approaches.
7. **Watch frontmatter ratios in referenced files.** If an external file is >50% YAML metadata, inline the content instead.

