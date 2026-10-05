
A toggleable `PermissionRequest` hook that auto-approves all Claude Code tool calls without user confirmation. This is a workaround for `--dangerously-skip-permissions` being broken in Claude Code v2.1.x, where the flag fails to propagate to subagents ([anthropics/claude-code#40241](https://github.com/anthropics/claude-code/issues/40241)) and silently stops working after exiting Plan Mode ([anthropics/claude-code#40136](https://github.com/anthropics/claude-code/issues/40136)).

Unlike the CLI flag, the hook approach works because hooks are inherited by subagents (they read the same `settings.json`) and persist across mode transitions.

### Security Warning

```
╔══════════════════════════════════════════════════╗
║                                                  ║
║           ☠  HERE BE DRAGONS  ☠                  ║
║                                                  ║
║  Yolo mode auto-approves ALL permission prompts  ║
║  with zero safety checks.                        ║
║                                                  ║
║  This means Claude can:                          ║
║    • Run any shell command                       ║
║    • Edit or delete any file                     ║
║    • Push to any remote                          ║
║    • Do anything — without asking                ║
║                                                  ║
╚══════════════════════════════════════════════════╝
```

This recipe provides the same security posture as `--dangerously-skip-permissions`: **none**. It is intended for trusted local development environments where the user is actively monitoring Claude's output. It offers no protection against prompt injection, destructive commands, or unintended side effects.

**Do not use this in:**
- Shared CI/CD environments
- Production systems
- Environments with access to sensitive credentials or infrastructure
- Sessions where untrusted content (PRs, issues, external files) will be processed

### Components

#### Hook Script

**Path:** `~/.claude/hooks/yolo-approve-all.sh`

```bash
#!/bin/bash
echo '{"hookSpecificOutput":{"hookEventName":"PermissionRequest","decision":{"behavior":"allow"}}}'
exit 0
```

The script:
- Receives permission request JSON on stdin (ignored — approves unconditionally)
- Returns the PermissionRequest hook-specific output with `"behavior": "allow"`
- Exits with code 0 (success — action proceeds)

#### Settings.json Hook Entry

**Location:** `~/.claude/settings.json` → `hooks.PermissionRequest`

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "$HOME/.claude/hooks/yolo-approve-all.sh"
          }
        ]
      }
    ]
  }
}
```

- **matcher**: Empty string matches all tool types
- **type**: `command` — executes a shell script
- **command**: Uses `$HOME` for portability across environments

#### Scope

| Scope | Affected? | Why |
|-------|-----------|-----|
| Current session | Yes | Hook fires on every permission prompt in the active session |
| Subagents (Agent tool) | Yes | Subagents read the same `~/.claude/settings.json` |
| Plan mode transitions | Yes | Hooks persist across mode changes (unlike the CLI flag) |
| New sessions | Yes | Hook is in user-level settings, applies to all future sessions |
| Headless mode (`-p`) | No | `PermissionRequest` does not fire in non-interactive mode — use `PreToolUse` with `permissionDecision` instead |
| Other users | No | User-level `~/.claude/settings.json` is per-user |
| Project-level overrides | No | Only installed at user scope; project `.claude/settings.json` is not modified |

#### Commands

An implementation MUST provide these operations:

| Operation | Effect |
|-----------|--------|
| Enable | Show warning, confirm, install hook script and settings entry |
| Disable | Remove `PermissionRequest` from settings, print confirmation |
| Status | Check settings and report whether yolo mode is active |

