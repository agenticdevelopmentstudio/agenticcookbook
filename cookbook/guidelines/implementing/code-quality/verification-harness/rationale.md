
- `should-state-expected-observed-and-location`, `should-name-concrete-next-step`, `should-keep-output-concise`: The agent acts on the harness's stdout/stderr, so error messages are part of the interface.
- `should-choose-weakest-enforcement-level-that-holds`, `must-gate-correctness-deterministically`: Instructions in a prompt, CLAUDE.md, or skill are advisory — an agent can and will sometimes ignore them. Per Anthropic's Claude Code best practices, hooks and external gates "are deterministic and guarantee the action happens."
