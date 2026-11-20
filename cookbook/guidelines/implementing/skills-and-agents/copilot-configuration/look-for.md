
Review Copilot configuration against the rules above.

- `should-put-everywhere-guidance-in-one-file`: Repository-wide guidance is `.github/copilot-instructions.md`.
- `should-keep-copilot-instructions-short`: a `.github/copilot-instructions.md` that runs beyond build and test commands, non-obvious conventions, and what to avoid.
- `should-put-narrower-guidance-in-instructions-files`: Path-specific files end in `.instructions.md` and live in `.github/instructions/`.
- `should-match-intended-files-with-apply-to`: Each path-specific file has an `applyTo` glob that matches the files it intends.
- `may-exclude-one-agent`: an `excludeAgent` value other than `"code-review"` or `"cloud-agent"`.
- `should-set-exclude-agent-only-on-purpose`: `excludeAgent` is set only on purpose.
- `must-not-repeat-repo-wide-rules-in-path-files`: Guidance is not duplicated between the repository-wide file and path files.
- `should-prefer-agents-md`: a `CLAUDE.md` or `GEMINI.md` used where an `AGENTS.md` would serve.
- `should-not-carry-conflicting-agent-files`: A repository does not carry both an `AGENTS.md` and a `CLAUDE.md` or `GEMINI.md` with different content.
- `should-not-restate-organization-policy`: repository instructions that restate organization policy.
- `must-use-agent-key-not-mode`: Frontmatter uses `agent` rather than `mode`.
- `should-use-input-and-selection-variables`: Variables use the `${input:...}` and `${selection}` forms.
- `must-not-take-a-users-prompt-name`: The prompt name does not collide with an existing one.
- `should-put-repeatable-tasks-in-prompt-files`: Prompt files end in `.prompt.md` and live in `.github/prompts/`.

