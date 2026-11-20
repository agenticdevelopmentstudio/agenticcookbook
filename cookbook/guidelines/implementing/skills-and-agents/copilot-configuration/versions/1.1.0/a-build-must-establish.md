
- `should-put-everywhere-guidance-in-one-file`: guidance that applies everywhere is in `.github/copilot-instructions.md` alone
- `should-keep-copilot-instructions-short`: `.github/copilot-instructions.md` holds only build and test commands, non-obvious conventions, and what to avoid
- `should-put-narrower-guidance-in-instructions-files`: narrower guidance is in `.github/instructions/NAME.instructions.md`
- `should-match-intended-files-with-apply-to`: every path-specific file has an `applyTo` glob matching exactly the files it intends
- `may-exclude-one-agent`: every `excludeAgent` is `"code-review"` or `"cloud-agent"`
- `should-set-exclude-agent-only-on-purpose`: every `excludeAgent` has a stated purpose
- `must-not-repeat-repo-wide-rules-in-path-files`: no path file repeats a repository-wide rule
- `should-prefer-agents-md`: agent instructions are in `AGENTS.md`, not a `CLAUDE.md` or `GEMINI.md`, or the project says why
- `should-not-carry-conflicting-agent-files`: the repository has no `AGENTS.md` beside a `CLAUDE.md` or `GEMINI.md` with different content
- `should-not-restate-organization-policy`: no repository instruction restates organization policy
- `must-use-agent-key-not-mode`: every prompt file's frontmatter uses `agent`, none `mode`
- `should-use-input-and-selection-variables`: prompt bodies use `${input:name}` or `${input:name:placeholder}` for user values and `${selection}` for the selected text
- `must-not-take-a-users-prompt-name`: no prompt file takes the name of a user's own prompt
- `should-put-repeatable-tasks-in-prompt-files`: every repeatable task is a `.github/prompts/NAME.prompt.md` file

