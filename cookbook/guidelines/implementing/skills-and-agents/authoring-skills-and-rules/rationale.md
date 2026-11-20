
- `should-keep-skill-description-under-200-characters`, `should-include-trigger-keywords-in-description`: The description stays under 200 characters because the skill description is loaded into every session's context window.
- `should-not-fork-chainable-skills`, `should-fork-only-isolated-read-heavy-tasks`: Forked skills cannot invoke other skills or write files visible to the caller.
- `should-add-new-skill-to-claude-md-and-readme`: A skill that is not in the inventory is invisible to other sessions.
- `should-use-rfc-2119-keywords-in-rules`: Rules are not advisory or suggestive -- they are directives.
- `must-include-a-must-not-section`: This section captures anti-patterns, common mistakes, and behaviors that have caused problems in practice.
- `should-name-requirements-not-number-them`: Named requirements make cross-referencing meaningful and survive reordering.
- `should-scope-agent-tool-access`, `should-set-max-turns`, `should-write-a-clear-system-prompt`: Agent authoring is less mature than skill and rule authoring. These agent practices reflect early lessons.
- `should-scope-agent-tool-access`: An agent that can do everything is an agent that will eventually do something unexpected.
- `should-write-a-clear-system-prompt`: The markdown body IS the agent's instruction set. A vague system prompt produces vague results.

