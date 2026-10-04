
A toggleable `PermissionRequest` hook that auto-approves all Claude Code tool calls without user confirmation. This is a workaround for `--dangerously-skip-permissions` being broken in Claude Code v2.1.x, where the flag fails to propagate to subagents ([anthropics/claude-code#40241](https://github.com/anthropics/claude-code/issues/40241)) and silently stops working after exiting Plan Mode ([anthropics/claude-code#40136](https://github.com/anthropics/claude-code/issues/40136)).

Unlike the CLI flag, the hook approach works because hooks are inherited by subagents (they read the same `settings.json`) and persist across mode transitions.

