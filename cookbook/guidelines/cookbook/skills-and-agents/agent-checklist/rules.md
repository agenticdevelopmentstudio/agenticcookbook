
### Structure & Format

- **must-have-yaml-frontmatter**: The agent file MUST have YAML frontmatter: it starts with `---` and has a closing `---`. (S01, FAIL)
- **should-have-name-field**: The frontmatter SHOULD contain a `name:` field. (S02, WARN)
- **must-use-kebab-case-name**: The `name` MUST be lowercase kebab-case of at most 64 characters, matching `^[a-z][a-z0-9-]{0,63}$`. (S03, FAIL)
- **must-have-description-field**: The frontmatter MUST contain a `description:` field. (S04, FAIL)
- **should-use-natural-trigger-keywords**: The description SHOULD use natural trigger keywords: phrases users would say, neither too vague nor too narrow. (S05, WARN)
- **should-be-in-agents-directory**: The agent SHOULD be in `.claude/agents/` or `~/.claude/agents/`. (S11, WARN)
- **should-use-only-recognized-frontmatter-fields**: The frontmatter SHOULD use only recognized fields: name, description, tools, disallowedTools, model, permissionMode, maxTurns, skills, mcpServers, hooks, memory, background, effort, isolation. (S12, WARN)
- **should-use-lowercase-kebab-case-filename**: The filename SHOULD be lowercase kebab-case, matching `^[a-z][a-z0-9-]*\.md$`; UPPERCASE stems are reserved for identity files like `SKILL.md` and `CLAUDE.md`. (S13, WARN)

### Content Quality

- **should-have-single-responsibility**: The agent SHOULD have one clear purpose, not a grab-bag of unrelated tasks. (C01, WARN)
- **should-cover-error-handling**: The system prompt SHOULD address what to do when things go wrong (tool failures, missing files, bad input). (C04, WARN)
- **should-give-actionable-specific-instructions**: The system prompt SHOULD tell the agent concretely what to do. (C07, WARN)
- **must-not-conflict-with-itself**: The body MUST NOT contradict itself. (C08, FAIL)
- **should-use-well-structured-markdown**: The body SHOULD use headings, lists and code blocks, not a wall of unstructured text. (C09, WARN)

### Best Practices

- **should-provide-verification-method**: The agent SHOULD include how to validate that it completed successfully. (B01, WARN)
- **should-not-replicate-native-capabilities**: The agent SHOULD NOT teach Claude things it already knows. (B02, WARN)
- **should-include-usage-examples**: The body or description SHOULD include examples or usage patterns giving the expected usage context. (B05, WARN)
- **must-not-be-kitchen-sink**: The agent MUST NOT try to do everything; it stays focused on its stated purpose. (B06, FAIL)
- **should-not-explore-unbounded**: The agent SHOULD scope its investigation and not read unbounded numbers of files. (B07, WARN)
- **should-not-be-claude-md-dump**: Agent content SHOULD be agent-appropriate, not a copy-paste of project rules that belong in CLAUDE.md. (B08, WARN)
- **should-match-model-override-to-complexity**: If `model:` is set, it SHOULD match the agent's complexity. (B10, WARN)
- **should-keep-description-under-200-characters**: The description SHOULD be under ~200 characters to avoid consuming excessive context. (B12, WARN)

### Agent-Specific

- **must-have-name-and-description**: The agent .md file MUST have both `name` and `description` frontmatter fields. (A01, FAIL)
- **should-restrict-tool-access**: A specialized agent SHOULD have its tool access limited by `tools` or `disallowedTools`. (A02, WARN)
- **may-specify-model**: The `model` field MAY be specified when the agent benefits from a specific model for its task. (A03, INFO)
- **should-have-clear-focused-system-prompt**: The markdown body SHOULD give the agent a clear role and scope. (A04, WARN)
- **should-set-permission-mode-appropriately**: `permissionMode` SHOULD be set appropriately: `plan` for read-only agents, `bypassPermissions` for fully automated ones. (A05, WARN)
- **should-set-max-turns-for-bounded-tasks**: A simple agent that should finish quickly SHOULD have a `maxTurns` turn limit. (A06, WARN)
- **may-preload-skills**: An agent that needs domain knowledge MAY list relevant preloaded skills in `skills`. (A07, INFO)
- **may-scope-memory**: If the agent accumulates knowledge, its `memory` scope MAY be set so it is scoped correctly. (A08, INFO)
