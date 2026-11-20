
- The agent **MUST** treat the context window as a finite, actively curated budget — not an append-only transcript.
- The agent **MUST NOT** front-load context "just in case." Retrieve files, tool output, and references just-in-time, at the point they are needed.
- Large or read-heavy subtasks (codebase exploration, multi-file investigation, log analysis) **SHOULD** be delegated to a subagent that runs in an isolated context and returns only a condensed summary.
- The agent **SHOULD** clear or reset context between unrelated tasks rather than carrying stale history forward.
- Information that must outlive the current window (decisions, conventions, task state) **MUST** be written to a persistent memory file, not relied upon to survive in-conversation.

