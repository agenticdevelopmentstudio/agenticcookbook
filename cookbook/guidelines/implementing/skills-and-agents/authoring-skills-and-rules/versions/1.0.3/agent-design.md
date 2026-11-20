
Agent authoring is less mature than skill and rule authoring. The following practices reflect early lessons.

1. **Scope tool access** -- Use the `tools` or `disallowedTools` frontmatter fields to restrict what the agent can do. An agent that can do everything is an agent that will eventually do something unexpected.

2. **Set `maxTurns`** -- Prevent unbounded execution by setting a turn limit appropriate to the task complexity. Simple review tasks might need 5-10 turns; complex analysis might need 20-30.

3. **Clear system prompt** -- The markdown body IS the agent's instruction set. Make the instructions focused, unambiguous, and structured. A vague system prompt produces vague results.

4. **Always lint** -- Run `/lint-agent <path>` after creating or modifying an agent. Fix all FAILs.

