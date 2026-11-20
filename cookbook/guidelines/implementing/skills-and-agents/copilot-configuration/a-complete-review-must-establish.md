
- `should-put-everywhere-guidance-in-one-file`: whether guidance that applies everywhere is in the one file `.github/copilot-instructions.md`
- `should-keep-copilot-instructions-short`: whether `.github/copilot-instructions.md` is short
- `should-put-narrower-guidance-in-instructions-files`: whether narrower guidance is in `.github/instructions/NAME.instructions.md` files
- `should-match-intended-files-with-apply-to`: whether each path-specific file's `applyTo` glob matches the files it intends
- `may-exclude-one-agent`: whether each `excludeAgent` names `"code-review"` or `"cloud-agent"`
- `should-set-exclude-agent-only-on-purpose`: whether every `excludeAgent` is set on purpose
- `must-not-repeat-repo-wide-rules-in-path-files`: whether any path file repeats repository-wide rules
- `should-prefer-agents-md`: whether the project uses `AGENTS.md` in preference to `CLAUDE.md` or `GEMINI.md`
- `should-not-carry-conflicting-agent-files`: whether the repository carries both an `AGENTS.md` and a `CLAUDE.md` or `GEMINI.md` with different content
- `should-not-restate-organization-policy`: whether repository instructions restate organization policy
- `must-use-agent-key-not-mode`: whether every prompt file's frontmatter uses `agent`, not `mode`
- `should-use-input-and-selection-variables`: whether prompts take user values through `${input:...}` and the selection through `${selection}`
- `must-not-take-a-users-prompt-name`: whether any prompt file takes the name of a user's own prompt
- `should-put-repeatable-tasks-in-prompt-files`: whether repeatable tasks are prompt files in `.github/prompts/`

- `should-not-carry-conflicting-agent-files`: agent instruction files do not disagree.
