
- **should-put-everywhere-guidance-in-one-file**: Guidance that applies everywhere SHOULD be put in one file.
- **should-keep-copilot-instructions-short**: `.github/copilot-instructions.md` SHOULD be short: build and test commands, conventions that are not obvious from the code, and what to avoid.
- **should-put-narrower-guidance-in-instructions-files**: Narrower guidance SHOULD go in `.github/instructions/NAME.instructions.md`.
- **should-match-intended-files-with-apply-to**: Each path-specific file SHOULD have an `applyTo` glob that matches the files it intends.
- **may-exclude-one-agent**: A file MAY add `excludeAgent: "code-review"` or `excludeAgent: "cloud-agent"` to keep a file away from one of those agents.
  - Without it both use the file.
- **should-set-exclude-agent-only-on-purpose**: `excludeAgent` SHOULD be set only on purpose.
- **must-not-repeat-repo-wide-rules-in-path-files**: Path-specific and repository-wide files are both applied when a file matches, so a path file MUST NOT repeat repository-wide rules.
- **should-prefer-agents-md**: Projects SHOULD prefer `AGENTS.md`, which is not tied to one tool and can be shared with other agents.
- **should-not-carry-conflicting-agent-files**: A repository SHOULD NOT carry both an `AGENTS.md` and a `CLAUDE.md` or `GEMINI.md` with different content.
- **should-not-restate-organization-policy**: Repository instructions SHOULD NOT restate organization policy.
- **must-use-agent-key-not-mode**: The key for the agent MUST be `agent`, not the older `mode`.
- **should-use-input-and-selection-variables**: In the body, a prompt SHOULD use `${input:name}` or `${input:name:placeholder}` for values the user supplies and `${selection}` for the selected text.
- **must-not-take-a-users-prompt-name**: A prompt file MUST NOT take the name of a user's own prompt.
- **should-put-repeatable-tasks-in-prompt-files**: Repeatable tasks SHOULD be put in prompt files.

